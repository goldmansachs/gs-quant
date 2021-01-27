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

from gs_quant.datetime import date
from gs_quant.markets.risk_model import RiskModel
from gs_quant.target.risk_models import RiskModelFactor


class Factor:

    def __init__(self, risk_model_id: str, factor_name: str):
        self.risk_model_id = risk_model_id
        factors = RiskModel(risk_model_id).get_factor_data()
        factors = [factor for factor in factors if factor['name'] == factor_name]
        self.factor = RiskModelFactor(identifier=factors[0]['identifier'],
                                      type_=factors[0]['type'],
                                      name=factors[0]['name']) if factors else None

    def get_covariance(self, factor, start_date: date, end_date: date) -> List:
        """ Retrieve a list of covariances between this factor and another for a range of dates """
        covariance_data = []
        query_results = RiskModel(self.risk_model_id).get_covariance_matrix(start_date, end_date).get('results', [])
        for result in query_results:
            date = result['date']
            factor_1_index = -1
            factor_2_index = -1
            factors = result['factorData']
            for index in range(0, len(factors)):
                name = factors[index]['factorName']
                if name == self.factor.name:
                    factor_1_index = index
                if name == factor.factor.name:
                    factor_2_index = index
            if -1 not in [factor_1_index, factor_2_index]:
                covariance_data.append({'date': date,
                                        'covariance': result['covarianceMatrix'][factor_1_index][factor_2_index]})
        return covariance_data
