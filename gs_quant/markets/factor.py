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
from typing import List

from gs_quant.api.gs.data import GsDataApi
from gs_quant.datetime import date
from gs_quant.markets.risk_model import RiskModel
from gs_quant.target.data import DataQuery
from gs_quant.target.risk_models import RiskModelFactor


class Factor:

    def __init__(self, risk_model_id: str, factor_name: str):
        self.risk_model_id = risk_model_id
        factors = RiskModel(risk_model_id).get_factor_data()
        factors = [factor for factor in factors if factor['name'] == factor_name]
        self.factor = RiskModelFactor(identifier=factors[0]['identifier'],
                                      type_=factors[0]['type'],
                                      name=factors[0]['name']) if factors else None

    def get_name(self):
        return self.factor.name

    def get_id(self):
        return self.factor.identifier

    def get_covariance(self, factor, start_date: date, end_date: date) -> List:
        """ Retrieve a list of covariances between this factor and another for a range of dates """
        covariance_data = []

        # Collect matrix order for requested factor on all available dates
        query = DataQuery(where={"riskModel": self.risk_model_id, "factorId": factor.factor.identifier},
                          start_date=start_date,
                          end_date=end_date)
        factor_covariances = GsDataApi.execute_query('RISK_MODEL_COVARIANCE_MATRIX', query).get('data', [])
        matrix_order_map = {data['date']: data['matrixOrder'] for data in factor_covariances}

        # Collect covariances at relevant matrix order on all available dates
        query = DataQuery(where={"riskModel": self.risk_model_id, "factorId": self.factor.identifier},
                          start_date=start_date,
                          end_date=end_date)
        factor_covariances = GsDataApi.execute_query('RISK_MODEL_COVARIANCE_MATRIX', query).get('data', [])
        for data in factor_covariances:
            date = data['date']
            if matrix_order_map.get(date):
                covariance_data.append({'date': date, 'covariance': data[str(matrix_order_map[date])]})
        return covariance_data
