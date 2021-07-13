"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import math
from math import sqrt
from typing import Dict, Union

import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.data.core import DataContext
from gs_quant.datetime import date
from gs_quant.errors import MqValueError
from gs_quant.models.risk_model import FactorRiskModel, ReturnFormat
from gs_quant.session import GsSession
from gs_quant.target.data import DataQuery


class Factor:

    def __init__(self, risk_model_id: str, id_: str, name: str, type: str, category: str):
        self.__risk_model_id = risk_model_id
        self.__id = id_
        self.__name = name
        self.__type = type
        self.__category = category

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def category(self):
        return self.__category

    @property
    def risk_model_id(self):
        return self.__risk_model_id

    @classmethod
    def get(cls, risk_model_id: str, factor_name: str):
        risk_model = FactorRiskModel.get(risk_model_id)
        factor_data = risk_model.get_factor_data(format=ReturnFormat.JSON)
        name_matches = [factor for factor in factor_data if factor['name'] == factor_name]

        if not name_matches:
            raise MqValueError(f'Factor with name {factor_name} does not in exist in risk model {risk_model_id}')

        factor = name_matches.pop()
        return Factor(risk_model_id, factor['identifier'], factor['name'], factor['type'], factor.get('factorCategory'))

    def covariance(self,
                   factor,
                   start_date: date = DataContext.current.start_date,
                   end_date: date = DataContext.current.end_date,
                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->covariance values between this factor and another for a date
        range """
        appendage = self.__get_dataset_trial_appendage()
        covariance_data_raw = GsDataApi.execute_query(
            f'RISK_MODEL_COVARIANCE_MATRIX{appendage}',
            DataQuery(
                where={"riskModel": self.risk_model_id, "factorId": self.id},
                start_date=start_date,
                end_date=end_date
            )
        ).get('data', [])

        date_to_matrix_order = factor.__matrix_order(start_date, end_date, appendage)

        covariance_data = {}
        for data in covariance_data_raw:
            date = data['date']
            if date_to_matrix_order.get(date):
                matrix_order_on_date = date_to_matrix_order[date]
                covariance_data[date] = data[matrix_order_on_date] * math.sqrt(252)

        if format == ReturnFormat.DATA_FRAME:
            return pd.DataFrame.from_dict(covariance_data, orient='index', columns=['covariance'])
        return covariance_data

    def variance(self,
                 start_date: date = DataContext.current.start_date,
                 end_date: date = DataContext.current.end_date,
                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->variance values for a factor over a date range """
        variance_data = self.covariance(self, start_date, end_date, ReturnFormat.JSON)

        if format == ReturnFormat.DATA_FRAME:
            return pd.DataFrame.from_dict(variance_data, orient='index', columns=['variance'])
        return variance_data

    def volatility(self,
                   start_date: date = DataContext.current.start_date,
                   end_date: date = DataContext.current.end_date,
                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->volatility values for a factor over a date range """
        variance = self.variance(start_date, end_date, ReturnFormat.JSON)
        volatility_data = {k: sqrt(v) for k, v in variance.items()}

        if format == ReturnFormat.DATA_FRAME:
            return pd.DataFrame.from_dict(volatility_data, orient='index', columns=['volatility'])
        return volatility_data

    def correlation(self,
                    other_factor,
                    start_date: date = DataContext.current.start_date,
                    end_date: date = DataContext.current.end_date,
                    format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->correlation values between this factor and another for a date
        range """

        factor_vol = self.volatility(start_date, end_date, ReturnFormat.JSON)
        other_factor_vol = other_factor.volatility(start_date, end_date, ReturnFormat.JSON)
        covariance = self.covariance(other_factor, start_date, end_date, ReturnFormat.JSON)

        correlation_data = {}
        for _date, covar in covariance.items():
            if _date in factor_vol and _date in other_factor_vol:
                denominator = factor_vol[_date] * other_factor_vol[_date]
                if denominator != 0:
                    correlation_data[_date] = covar / denominator

        if format == ReturnFormat.DATA_FRAME:
            return pd.DataFrame.from_dict(correlation_data, orient='index', columns=['correlation'])
        return correlation_data

    def returns(self,
                start_date: date = DataContext.current.start_date,
                end_date: date = DataContext.current.end_date,
                format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->factor return values for a date range """
        appendage = self.__get_dataset_trial_appendage()
        data_query_results = GsDataApi.execute_query(
            f'RISK_MODEL_FACTOR{appendage}',
            DataQuery(
                where={"riskModel": self.risk_model_id, "factorId": self.id},
                fields=['return'],
                start_date=start_date,
                end_date=end_date
            )
        ).get('data', [])

        return_data = {factor_data['date']: factor_data['return'] for factor_data in data_query_results
                       if factor_data.get('return')}

        if format == ReturnFormat.DATA_FRAME:
            return pd.DataFrame.from_dict(return_data, orient='index', columns=['return'])
        return return_data

    def __matrix_order(self, start_date: date, end_date: date, appendage: str) -> Dict:
        """ Retrieve Dictionary of date->matrix_order for the factor in the covariance matrix """
        query_results = GsDataApi.execute_query(
            f'RISK_MODEL_COVARIANCE_MATRIX{appendage}',
            DataQuery(
                where={"riskModel": self.risk_model_id, "factorId": self.id},
                fields=['matrixOrder'],
                start_date=start_date,
                end_date=end_date
            )
        ).get('data', [])
        return {data['date']: str(data['matrixOrder']) for data in query_results}

    def __get_dataset_trial_appendage(self):
        availability_response = [model_dataset for model_dataset in
                                 GsSession.current._get(f'/data/measures/{self.risk_model_id}/availability?entityType'
                                                        f'=RISK_MODEL').get('data')
                                 if model_dataset.get('type') == 'Factor Return']
        availability_response = sorted(availability_response, key=lambda k: k['rank'], reverse=True)
        for availability in availability_response:
            dataset_id = availability.get('datasetId')
            models_covered = GsDataApi.get_coverage(dataset_id, limit=1000)
            for model in models_covered:
                if model.get('riskModel') == self.risk_model_id:
                    return dataset_id.replace('RISK_MODEL_FACTOR', '')
