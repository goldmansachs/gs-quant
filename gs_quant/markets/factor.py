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
from enum import auto
from typing import Dict, Union

import numpy as np
import pandas as pd
import math

from gs_quant.data.core import DataContext
from gs_quant.datetime import date
from gs_quant.target.common import Enum
from gs_quant.api.gs.risk_models import GsFactorRiskModelApi, RiskModelDataMeasure
from gs_quant.models.risk_model_utils import get_covariance_matrix_dataframe, build_factor_volatility_dataframe, \
    build_factor_data_map


class ReturnFormat(Enum):
    """Alternative format for data to be returned from get_data functions"""
    JSON = auto()
    DATA_FRAME = auto()


class Factor:

    def __init__(self,
                 risk_model_id: str,
                 id_: str,
                 type_: str,
                 name: str = None,
                 category: str = None,
                 tooltip: str = None,
                 description: str = None,
                 glossary_description: str = None):
        self.__risk_model_id = risk_model_id
        self.__id = id_
        self.__name = name
        self.__type = type_
        self.__category = category
        self.__tooltip = tooltip
        self.__description = description
        self.__glossary_description = glossary_description

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def type(self) -> str:
        return self.__type

    @property
    def category(self) -> str:
        return self.__category

    @property
    def tooltip(self):
        return self.__tooltip

    @property
    def description(self):
        return self.__description

    @property
    def glossary_description(self):
        return self.__glossary_description

    @property
    def risk_model_id(self):
        return self.__risk_model_id

    def covariance(self,
                   factor: 'Factor',
                   start_date: date = DataContext.current.start_date,
                   end_date: date = DataContext.current.end_date,
                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->covariance values between this factor and another for a date
                range """
        covariance_data_raw = GsFactorRiskModelApi.get_risk_model_data(self.risk_model_id,
                                                                       start_date,
                                                                       end_date,
                                                                       measures=[RiskModelDataMeasure.Covariance_Matrix,
                                                                                 RiskModelDataMeasure.Factor_Name,
                                                                                 RiskModelDataMeasure.Factor_Id],
                                                                       factors=list({self.name, factor.name}),
                                                                       limit_factors=False).get('results')

        covariance_data_raw = get_covariance_matrix_dataframe(covariance_data_raw)

        covariance_data_df = covariance_data_raw.stack().loc[pd.IndexSlice[:, self.name, factor.name]] * 252

        if format == ReturnFormat.JSON:
            return covariance_data_df.to_dict()

        return covariance_data_df.to_frame(name="covariance")

    def variance(self,
                 start_date: date = DataContext.current.start_date,
                 end_date: date = DataContext.current.end_date,
                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->variance values for a factor over a date range """
        variance_raw_data = self.covariance(self, start_date, end_date, ReturnFormat.DATA_FRAME) \
            .rename(columns={"covariance": "variance"})

        if format == ReturnFormat.JSON:
            return variance_raw_data.squeeze().to_dict()

        return variance_raw_data

    def volatility(self,
                   start_date: date = DataContext.current.start_date,
                   end_date: date = DataContext.current.end_date,
                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->volatility values for a factor over a date range """
        volatility_raw_data = GsFactorRiskModelApi.get_risk_model_data(self.risk_model_id,
                                                                       start_date,
                                                                       end_date,
                                                                       measures=[RiskModelDataMeasure.Factor_Volatility,
                                                                                 RiskModelDataMeasure.Factor_Id,
                                                                                 RiskModelDataMeasure.Factor_Name],
                                                                       factors=[self.name],
                                                                       limit_factors=False).get('results')

        volatility_data_df = build_factor_volatility_dataframe(volatility_raw_data, True, None) * math.sqrt(252)
        if format == ReturnFormat.JSON:
            return volatility_data_df.squeeze(axis=1).to_dict()

        return volatility_data_df

    def correlation(self,
                    other_factor,
                    start_date: date = DataContext.current.start_date,
                    end_date: date = DataContext.current.end_date,
                    format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->correlation values between this factor and another for a date
        range """

        raw_data = GsFactorRiskModelApi.get_risk_model_data(self.risk_model_id,
                                                            start_date,
                                                            end_date,
                                                            measures=[RiskModelDataMeasure.Covariance_Matrix,
                                                                      RiskModelDataMeasure.Factor_Name,
                                                                      RiskModelDataMeasure.Factor_Id],
                                                            factors=[self.name, other_factor.name],
                                                            limit_factors=False).get('results')

        covariance_data_raw = get_covariance_matrix_dataframe(raw_data) * 252
        numerator = covariance_data_raw.stack().loc[pd.IndexSlice[:, self.name, other_factor.name]]
        denominator = np.sqrt(covariance_data_raw.stack().loc[pd.IndexSlice[:, self.name, self.name]] *
                              covariance_data_raw.stack().loc[pd.IndexSlice[:, other_factor.name, other_factor.name]])

        correlation_df = numerator / denominator

        if format == ReturnFormat.JSON:
            return correlation_df.to_dict()
        return correlation_df.to_frame(name="correlation")

    def returns(self,
                start_date: date = DataContext.current.start_date,
                end_date: date = DataContext.current.end_date,
                format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve a Dataframe or Dictionary of date->factor return values for a date range """
        factor_returns_raw = GsFactorRiskModelApi.get_risk_model_data(self.risk_model_id,
                                                                      start_date,
                                                                      end_date,
                                                                      measures=[RiskModelDataMeasure.Factor_Return,
                                                                                RiskModelDataMeasure.Factor_Name,
                                                                                RiskModelDataMeasure.Factor_Id],
                                                                      factors=[self.name],
                                                                      limit_factors=False).get('results')

        factor_returns_formatted = build_factor_data_map(factor_returns_raw, 'factorName', self.risk_model_id,
                                                         RiskModelDataMeasure.Factor_Return, None)
        factor_returns_df = factor_returns_formatted.rename(columns={self.name: 'return'}).rename_axis(None, axis=1)

        if format == ReturnFormat.JSON:
            return factor_returns_df.squeeze().to_dict()

        return factor_returns_df
