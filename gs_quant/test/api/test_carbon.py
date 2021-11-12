"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import pytest

from gs_quant.api.gs.carbon import GsCarbonApi, CarbonCard
from gs_quant.session import GsSession, Environment
from gs_quant.target.common import Currency


def test_get_carbon_data(mocker):
    mock_response = {
        "coverage": {
            "weights": {
                "portfolio": {
                    "scope1": {
                        "reportedVerified": 27.172942402143175,
                        "reportedUnverified": 72.82705759785682,
                        "estimated": 0,
                        "missing": 0
                    }
                },
                "benchmark": {
                    "scope1": {
                        "reportedVerified": 56.951789932735934,
                        "reportedUnverified": 19.955009583898327,
                        "estimated": 18.412744312759482,
                        "missing": 4.680456170606256
                    }
                }
            },
            "numberOfCompanies": {
                "portfolio": {
                    "scope1": {
                        "reportedVerified": 50,
                        "reportedUnverified": 50,
                        "estimated": 0,
                        "missing": 0
                    }
                },
                "benchmark": {
                    "scope1": {
                        "reportedVerified": 34.257425742574256,
                        "reportedUnverified": 29.702970297029704,
                        "estimated": 28.91089108910891,
                        "missing": 7.128712871287124
                    }
                }
            }
        },
        "emissions": {
            "scope1": {
                "portfolio": [
                    {
                        "year": "2016",
                        "portfolioEmissions": 0.009388646556910485,
                        "emissionsIntensityRevenue": 0.2706793856871246,
                        "emissionsIntensityEnterpriseValue": 0.03388271250693313,
                        "emissionsIntensityMarketCap": 0.11190632050536728
                    },
                    {
                        "year": "2017",
                        "portfolioEmissions": 0.008619992844290039,
                        "emissionsIntensityRevenue": 0.2412522591903448,
                        "emissionsIntensityEnterpriseValue": 0.030906851992767197,
                        "emissionsIntensityMarketCap": 0.1066210865476519
                    },
                    {
                        "year": "2018",
                        "portfolioEmissions": 0.008893662072152794,
                        "emissionsIntensityRevenue": 0.21887783180015072,
                        "emissionsIntensityEnterpriseValue": 0.03144114560735717,
                        "emissionsIntensityMarketCap": 0.16376957940863043
                    },
                    {
                        "year": "2019",
                        "portfolioEmissions": 0.008896070619613242,
                        "emissionsIntensityRevenue": 0.2225589953607619,
                        "emissionsIntensityEnterpriseValue": 0.03199235113825498,
                        "emissionsIntensityMarketCap": 0.13300579690144726
                    },
                    {
                        "year": "2021",
                        "portfolioEmissions": 0.005462648973310796,
                        "emissionsIntensityRevenue": 0.17671239978936054,
                        "emissionsIntensityEnterpriseValue": 0.019184671815761833,
                        "emissionsIntensityMarketCap": 0.08433051410609066
                    }
                ],
                "benchmark": [
                    {
                        "year": "2016",
                        "portfolioEmissions": 10.7359742295746,
                        "emissionsIntensityRevenue": 128.48937740484533,
                        "emissionsIntensityEnterpriseValue": 37.874021067055146,
                        "emissionsIntensityMarketCap": 65.55320800814903
                    },
                    {
                        "year": "2017",
                        "portfolioEmissions": 10.053210673655316,
                        "emissionsIntensityRevenue": 125.70320189825257,
                        "emissionsIntensityEnterpriseValue": 35.24939382150576,
                        "emissionsIntensityMarketCap": 57.499118590386026
                    },
                    {
                        "year": "2018",
                        "portfolioEmissions": 9.795527406862018,
                        "emissionsIntensityRevenue": 111.70530289875649,
                        "emissionsIntensityEnterpriseValue": 34.343535288823446,
                        "emissionsIntensityMarketCap": 54.01561424453475
                    },
                    {
                        "year": "2019",
                        "portfolioEmissions": 8.006501437233737,
                        "emissionsIntensityRevenue": 104.83823370420704,
                        "emissionsIntensityEnterpriseValue": 28.07322928722559,
                        "emissionsIntensityMarketCap": 42.148992638800664
                    },
                    {
                        "year": "2021",
                        "portfolioEmissions": 7.419956698372355,
                        "emissionsIntensityRevenue": 104.38248106531313,
                        "emissionsIntensityEnterpriseValue": 26.429401913564423,
                        "emissionsIntensityMarketCap": 40.70785737756474
                    }
                ]
            }
        }
    }
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsCarbonApi.get_carbon_analytics(entity_id='MPRE78YG4J918ERD',
                                                benchmark_id='MA4B66MW5E27U8P32SB',
                                                include_estimates=True,
                                                currency=Currency.GBP,
                                                cards=[CarbonCard.COVERAGE, CarbonCard.EMISSIONS])
    GsSession.current._get.assert_called_with(
        '/carbon/MPRE78YG4J918ERD?benchmark=MA4B66MW5E27U8P32SB&reportingYear=Latest&currency=GBP'
        '&includeEstimates=true&useHistoricalData=false&normalizeEmissions=false&card=coverage&card=emissions'
        '&analyticsView=Long')
    assert response == mock_response


if __name__ == '__main__':
    pytest.main(args=[__file__])
