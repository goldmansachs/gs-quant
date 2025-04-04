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
import copy
import datetime as dt

import pytest

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.carbon import GsCarbonApi, CarbonTargetCoverageCategory, CarbonScope, \
    CarbonEmissionsAllocationCategory, CarbonEmissionsIntensityType, CarbonCard, CarbonCoverageCategory, \
    CarbonEntityType
from gs_quant.api.gs.esg import GsEsgApi, ESGMeasure
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.api.gs.scenarios import GsFactorScenarioApi
from gs_quant.entities.entitlements import Entitlements, User, EntitlementBlock
from gs_quant.markets.portfolio_manager import PortfolioManager, ScenarioCalculationMeasure
from gs_quant.markets.report import FactorRiskReport, PerformanceReport
from gs_quant.markets.scenario import FactorScenario, HistoricalSimulationParameters, FactorScenarioType
from gs_quant.models.risk_model import MacroRiskModel, FactorType, UniverseIdentifier, CoverageType, Term
from gs_quant.session import GsSession, Environment
from gs_quant.target.portfolios import Portfolio as TargetPortfolio
from gs_quant.target.reports import ReportStatus, PositionSourceType, ReportType, Report
import pandas as pd
import numpy as np

esg_data = {
    'pricingDate': '2021-08-25',
    'quintiles': [{
        'measure': 'gPercentile',
        'results': [{
            'name': 'Q1',
            'description': '<=80-100%',
            'gross': 91.03557560284325,
            'long': 91.03557560284325,
            'short': 0
        }, {
            'name': 'Q2',
            'description': '<=60-80%',
            'gross': 0,
            'long': 0,
            'short': 0
        }, {
            'name': 'Q3',
            'description': '<=40-60%',
            'gross': 0,
            'long': 0,
            'short': 0
        }, {
            'name': 'Q4',
            'description': '<=20-40%',
            'gross': 8.955474904385047,
            'long': 0,
            'short': 8.955474904385047
        }, {
            'name': 'Q5',
            'description': '<=0-20%',
            'gross': 0,
            'long': 0,
            'short': 0
        }, {
            'name': 'Not Included',
            'description': 'Not Included',
            'gross': 0.008949492771697426,
            'long': 0.008949492771697426,
            'short': 0
        }]
    }],
    'summary': {
        'gross': {
            'gPercentile': 91.71440761636107,
            'gRegionalPercentile': 84.58263751763046,
            'esPercentile': 90.07443582510577,
            'esDisclosurePercentage': 78.50077574047954,
            'esMomentumPercentile': 74.20073342736248
        },
        'long': {
            'gPercentile': 97.39,
            'gRegionalPercentile': 92.62,
            'esPercentile': 94.24,
            'esDisclosurePercentage': 83.33,
            'esMomentumPercentile': 76.85
        },
        'short': {
            'gPercentile': 34.02,
            'gRegionalPercentile': 2.88,
            'esPercentile': 47.73,
            'esDisclosurePercentage': 29.41,
            'esMomentumPercentile': 47.27
        }
    },
    'weightsBySector': [{
        'name': 'Diversified Financials',
        'gross': 91.03557560284325,
        'long': 91.03557560284325,
        'short': 0
    }, {
        'name': 'Automobile Manufacturers',
        'gross': 8.955474904385047,
        'long': 0,
        'short': 8.955474904385047
    }, {
        'name': 'Total',
        'gross': 99.99105050722832,
        'long': 91.03557560284325,
        'short': 8.955474904385047
    }, {
        'name': 'Not Included',
        'gross': 0.008949492771697426,
        'long': 0.008949492771697426,
        'short': 0
    }],
    'measuresBySector': [{
        'measure': 'gPercentile',
        'results': [{
            'name': 'Diversified Financials',
            'gross': 97.39,
            'long': 97.39,
            'short': 0
        }, {
            'name': 'Automobile Manufacturers',
            'gross': 34.02,
            'long': 0,
            'short': 34.02
        }, {
            'name': 'Total',
            'gross': 91.71440761636107,
            'long': 97.39,
            'short': 34.02
        }]
    }],
    'weightsByRegion': [{
        'name': 'N. America',
        'gross': 99.99105050722832,
        'long': 91.03557560284325,
        'short': 8.955474904385047
    }, {
        'name': 'Total',
        'gross': 99.99105050722832,
        'long': 91.03557560284325,
        'short': 8.955474904385047
    }, {
        'name': 'Not Included',
        'gross': 0.008949492771697426,
        'long': 0.008949492771697426,
        'short': 0
    }],
    'measuresByRegion': [{
        'measure': 'gPercentile',
        'results': [{
            'name': 'N. America',
            'gross': 91.71440761636107,
            'long': 97.39,
            'short': 34.02
        }, {
            'name': 'Total',
            'gross': 91.71440761636107,
            'long': 97.39,
            'short': 34.02
        }]
    }],
    'topTenRanked': [{
        'measure': 'gPercentile',
        'results': [{
            'assetId': 'MA4B66MW5E27UAHKG34',
            'name': 'The Goldman Sachs Group, Inc.',
            'value': 97.39
        }, {
            'assetId': 'MA4B66MW5E27UANEQ6R',
            'name': 'Tesla Inc',
            'value': 34.02
        }]
    }],
    'bottomTenRanked': [{
        'measure': 'gPercentile',
        'results': [{
            'assetId': 'MA4B66MW5E27UANEQ6R',
            'name': 'Tesla Inc',
            'value': 34.02
        }, {
            'assetId': 'MA4B66MW5E27UAHKG34',
            'name': 'The Goldman Sachs Group, Inc.',
            'value': 97.39
        }]
    }],
    'noESGData': {
        'gross': {
            'weight': 0.008949492771697426,
            'assets': [{
                'assetId': 'MA4B66MW5E27UAL9SX6',
                'name': 'Mustek LTD',
                'weight': 0.008949492771697426
            }]
        },
        'long': {
            'weight': 0.008949492771697426,
            'assets': [{
                'assetId': 'MA4B66MW5E27UAL9SX6',
                'name': 'Mustek LTD',
                'weight': 0.008949492771697426
            }]
        },
        'short': {
            'weight': 0.0,
            'assets': []
        }
    }
}
carbon_data = {
    "coverage": {
        "weights": {
            "portfolio": {
                "totalGHG": {
                    "reportedVerified": 27.432014892432875,
                    "reportedUnverified": 72.56798510756713,
                    "estimated": 0,
                    "missing": 0
                },
                "scope1": {
                    "reportedVerified": 27.432014892432875,
                    "reportedUnverified": 72.56798510756713,
                    "estimated": 0,
                    "missing": 0
                },
                "scope2": {
                    "reportedVerified": 27.432014892432875,
                    "reportedUnverified": 72.56798510756713,
                    "estimated": 0,
                    "missing": 0
                }
            },
            "benchmark": {
                "totalGHG": {
                    "reportedVerified": 27.432014892432875,
                    "reportedUnverified": 72.56798510756713,
                    "estimated": 0,
                    "missing": 0
                },
                "scope1": {
                    "reportedVerified": 27.432014892432875,
                    "reportedUnverified": 72.56798510756713,
                    "estimated": 0,
                    "missing": 0
                },
                "scope2": {
                    "reportedVerified": 27.432014892432875,
                    "reportedUnverified": 72.56798510756713,
                    "estimated": 0,
                    "missing": 0
                }
            }
        },
        "numberOfCompanies": {
            "portfolio": {
                "totalGHG": {
                    "reportedVerified": 50,
                    "reportedUnverified": 50,
                    "estimated": 0,
                    "missing": 0
                },
                "scope1": {
                    "reportedVerified": 50,
                    "reportedUnverified": 50,
                    "estimated": 0,
                    "missing": 0
                },
                "scope2": {
                    "reportedVerified": 50,
                    "reportedUnverified": 50,
                    "estimated": 0,
                    "missing": 0
                }
            },
            "benchmark": {
                "totalGHG": {
                    "reportedVerified": 50,
                    "reportedUnverified": 50,
                    "estimated": 0,
                    "missing": 0
                },
                "scope1": {
                    "reportedVerified": 50,
                    "reportedUnverified": 50,
                    "estimated": 0,
                    "missing": 0
                },
                "scope2": {
                    "reportedVerified": 50,
                    "reportedUnverified": 50,
                    "estimated": 0,
                    "missing": 0
                }
            }
        }
    },
    "sbtiAndNetZeroTargets": {
        "capitalAllocated": {
            "scienceBasedTarget": {
                "portfolio": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 100
                },
                "benchmark": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 100
                }
            },
            "netZeroEmissionsTarget": {
                "portfolio": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 100
                },
                "benchmark": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 100
                }
            }
        },
        "portfolioEmissions": {
            "scienceBasedTarget": {
                "portfolio": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 99.99999999999997
                },
                "benchmark": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 99.99999999999997
                }
            },
            "netZeroEmissionsTarget": {
                "portfolio": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 99.99999999999997
                },
                "benchmark": {
                    "targetsSet": 0,
                    "targetsNotSet": 0,
                    "missing": 99.99999999999997
                }
            }
        }
    },
    "emissions": {
        "totalGHG": {
            "portfolio": [
                {
                    "year": "2016",
                    "portfolioEmissions": 0.03161404863641,
                    "emissionsIntensityRevenue": 5.165017590856768,
                    "emissionsIntensityEnterpriseValue": 0.6417863895887255,
                    "emissionsIntensityMarketCap": 2.136864492580658
                },
                {
                    "year": "2017",
                    "portfolioEmissions": 0.02557473780478448,
                    "emissionsIntensityRevenue": 4.152366329764957,
                    "emissionsIntensityEnterpriseValue": 0.5150082275283909,
                    "emissionsIntensityMarketCap": 1.8566214684311595
                },
                {
                    "year": "2018",
                    "portfolioEmissions": 0.025883906301863414,
                    "emissionsIntensityRevenue": 3.6355870431327695,
                    "emissionsIntensityEnterpriseValue": 0.514601211522207,
                    "emissionsIntensityMarketCap": 2.7567883404035856
                },
                {
                    "year": "2019",
                    "portfolioEmissions": 0.02488419915490657,
                    "emissionsIntensityRevenue": 3.3508727584974998,
                    "emissionsIntensityEnterpriseValue": 0.5058550746653679,
                    "emissionsIntensityMarketCap": 1.915020016654778
                },
                {
                    "year": "2021",
                    "portfolioEmissions": 0.016784770256626273,
                    "emissionsIntensityRevenue": 3.010184293088453,
                    "emissionsIntensityEnterpriseValue": 0.3321381204145429,
                    "emissionsIntensityMarketCap": 1.370060537473572
                }
            ],
            "benchmark": [
                {
                    "year": "2016",
                    "portfolioEmissions": 0.03161404863641,
                    "emissionsIntensityRevenue": 5.165017590856768,
                    "emissionsIntensityEnterpriseValue": 0.6417863895887255,
                    "emissionsIntensityMarketCap": 2.136864492580658
                },
                {
                    "year": "2017",
                    "portfolioEmissions": 0.02557473780478448,
                    "emissionsIntensityRevenue": 4.152366329764957,
                    "emissionsIntensityEnterpriseValue": 0.5150082275283909,
                    "emissionsIntensityMarketCap": 1.8566214684311595
                },
                {
                    "year": "2018",
                    "portfolioEmissions": 0.025883906301863414,
                    "emissionsIntensityRevenue": 3.6355870431327695,
                    "emissionsIntensityEnterpriseValue": 0.514601211522207,
                    "emissionsIntensityMarketCap": 2.7567883404035856
                },
                {
                    "year": "2019",
                    "portfolioEmissions": 0.02488419915490657,
                    "emissionsIntensityRevenue": 3.3508727584974998,
                    "emissionsIntensityEnterpriseValue": 0.5058550746653679,
                    "emissionsIntensityMarketCap": 1.915020016654778
                },
                {
                    "year": "2021",
                    "portfolioEmissions": 0.016784770256626273,
                    "emissionsIntensityRevenue": 3.010184293088453,
                    "emissionsIntensityEnterpriseValue": 0.3321381204145429,
                    "emissionsIntensityMarketCap": 1.370060537473572
                }
            ]
        },
        "scope1": {
            "portfolio": [
                {
                    "year": "2016",
                    "portfolioEmissions": 0.0016712755532904242,
                    "emissionsIntensityRevenue": 0.27028638660867355,
                    "emissionsIntensityEnterpriseValue": 0.0339529985038069,
                    "emissionsIntensityMarketCap": 0.11170603861184672
                },
                {
                    "year": "2017",
                    "portfolioEmissions": 0.0015352826311627388,
                    "emissionsIntensityRevenue": 0.24110061666622948,
                    "emissionsIntensityEnterpriseValue": 0.030986711463004902,
                    "emissionsIntensityMarketCap": 0.1064282069728648
                },
                {
                    "year": "2018",
                    "portfolioEmissions": 0.001582778525839715,
                    "emissionsIntensityRevenue": 0.21882979028252364,
                    "emissionsIntensityEnterpriseValue": 0.03149430343217062,
                    "emissionsIntensityMarketCap": 0.16344626276984683
                },
                {
                    "year": "2019",
                    "portfolioEmissions": 0.0015833905465049197,
                    "emissionsIntensityRevenue": 0.22245885390039408,
                    "emissionsIntensityEnterpriseValue": 0.032053991311445595,
                    "emissionsIntensityMarketCap": 0.1326706476709381
                },
                {
                    "year": "2021",
                    "portfolioEmissions": 0.0009713787667226322,
                    "emissionsIntensityRevenue": 0.1766993497855956,
                    "emissionsIntensityEnterpriseValue": 0.019200832225828832,
                    "emissionsIntensityMarketCap": 0.08410551021114267
                }
            ],
            "benchmark": [
                {
                    "year": "2016",
                    "portfolioEmissions": 0.0016712755532904242,
                    "emissionsIntensityRevenue": 0.27028638660867355,
                    "emissionsIntensityEnterpriseValue": 0.0339529985038069,
                    "emissionsIntensityMarketCap": 0.11170603861184672
                },
                {
                    "year": "2017",
                    "portfolioEmissions": 0.0015352826311627388,
                    "emissionsIntensityRevenue": 0.24110061666622948,
                    "emissionsIntensityEnterpriseValue": 0.030986711463004902,
                    "emissionsIntensityMarketCap": 0.1064282069728648
                },
                {
                    "year": "2018",
                    "portfolioEmissions": 0.001582778525839715,
                    "emissionsIntensityRevenue": 0.21882979028252364,
                    "emissionsIntensityEnterpriseValue": 0.03149430343217062,
                    "emissionsIntensityMarketCap": 0.16344626276984683
                },
                {
                    "year": "2019",
                    "portfolioEmissions": 0.0015833905465049197,
                    "emissionsIntensityRevenue": 0.22245885390039408,
                    "emissionsIntensityEnterpriseValue": 0.032053991311445595,
                    "emissionsIntensityMarketCap": 0.1326706476709381
                },
                {
                    "year": "2021",
                    "portfolioEmissions": 0.0009713787667226322,
                    "emissionsIntensityRevenue": 0.1766993497855956,
                    "emissionsIntensityEnterpriseValue": 0.019200832225828832,
                    "emissionsIntensityMarketCap": 0.08410551021114267
                }
            ]
        },
        "scope2": {
            "portfolio": [
                {
                    "year": "2016",
                    "portfolioEmissions": 0.02994277308311958,
                    "emissionsIntensityRevenue": 4.894731204248094,
                    "emissionsIntensityEnterpriseValue": 0.6078333910849186,
                    "emissionsIntensityMarketCap": 2.0251584539688117
                },
                {
                    "year": "2017",
                    "portfolioEmissions": 0.02403945517362174,
                    "emissionsIntensityRevenue": 3.9112657130987274,
                    "emissionsIntensityEnterpriseValue": 0.484021516065386,
                    "emissionsIntensityMarketCap": 1.750193261458295
                },
                {
                    "year": "2018",
                    "portfolioEmissions": 0.0243011277760237,
                    "emissionsIntensityRevenue": 3.4167572528502457,
                    "emissionsIntensityEnterpriseValue": 0.4831069080900363,
                    "emissionsIntensityMarketCap": 2.593342077633739
                },
                {
                    "year": "2019",
                    "portfolioEmissions": 0.02330080860840165,
                    "emissionsIntensityRevenue": 3.1284139045971058,
                    "emissionsIntensityEnterpriseValue": 0.4738010833539224,
                    "emissionsIntensityMarketCap": 1.7823493689838397
                },
                {
                    "year": "2021",
                    "portfolioEmissions": 0.015813391489903638,
                    "emissionsIntensityRevenue": 2.8334849433028575,
                    "emissionsIntensityEnterpriseValue": 0.312937288188714,
                    "emissionsIntensityMarketCap": 1.2859550272624294
                }
            ],
            "benchmark": [
                {
                    "year": "2016",
                    "portfolioEmissions": 0.02994277308311958,
                    "emissionsIntensityRevenue": 4.894731204248094,
                    "emissionsIntensityEnterpriseValue": 0.6078333910849186,
                    "emissionsIntensityMarketCap": 2.0251584539688117
                },
                {
                    "year": "2017",
                    "portfolioEmissions": 0.02403945517362174,
                    "emissionsIntensityRevenue": 3.9112657130987274,
                    "emissionsIntensityEnterpriseValue": 0.484021516065386,
                    "emissionsIntensityMarketCap": 1.750193261458295
                },
                {
                    "year": "2018",
                    "portfolioEmissions": 0.0243011277760237,
                    "emissionsIntensityRevenue": 3.4167572528502457,
                    "emissionsIntensityEnterpriseValue": 0.4831069080900363,
                    "emissionsIntensityMarketCap": 2.593342077633739
                },
                {
                    "year": "2019",
                    "portfolioEmissions": 0.02330080860840165,
                    "emissionsIntensityRevenue": 3.1284139045971058,
                    "emissionsIntensityEnterpriseValue": 0.4738010833539224,
                    "emissionsIntensityMarketCap": 1.7823493689838397
                },
                {
                    "year": "2021",
                    "portfolioEmissions": 0.015813391489903638,
                    "emissionsIntensityRevenue": 2.8334849433028575,
                    "emissionsIntensityEnterpriseValue": 0.312937288188714,
                    "emissionsIntensityMarketCap": 1.2859550272624294
                }
            ]
        }
    },
    "allocations": {
        "totalGHG": {
            "portfolio": {
                "gicsSector": [
                    {
                        "name": "Information Technology",
                        "portfolioEmissions": 0.00641159391374359,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Financials",
                        "portfolioEmissions": 0.010373176342882682,
                        "capitalAllocated": 37813
                    }
                ],
                "gicsIndustry": [
                    {
                        "name": "Technology Hardware & Equipment",
                        "portfolioEmissions": 0.00641159391374359,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Diversified Financials",
                        "portfolioEmissions": 0.010373176342882682,
                        "capitalAllocated": 37813
                    }
                ],
                "region": [
                    {
                        "name": "Americas",
                        "portfolioEmissions": 0.016784770256626273,
                        "capitalAllocated": 52107
                    }
                ]
            },
            "benchmark": {
                "gicsSector": [
                    {
                        "name": "Information Technology",
                        "portfolioEmissions": 0.00641159391374359,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Financials",
                        "portfolioEmissions": 0.010373176342882682,
                        "capitalAllocated": 37813
                    }
                ],
                "gicsIndustry": [
                    {
                        "name": "Technology Hardware & Equipment",
                        "portfolioEmissions": 0.00641159391374359,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Diversified Financials",
                        "portfolioEmissions": 0.010373176342882682,
                        "capitalAllocated": 37813
                    }
                ],
                "region": [
                    {
                        "name": "Americas",
                        "portfolioEmissions": 0.016784770256626273,
                        "capitalAllocated": 52107
                    }
                ]
            }
        },
        "scope1": {
            "portfolio": {
                "gicsSector": [
                    {
                        "name": "Information Technology",
                        "portfolioEmissions": 0.000324399112301343,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Financials",
                        "portfolioEmissions": 0.0006469796544212892,
                        "capitalAllocated": 37813
                    }
                ],
                "gicsIndustry": [
                    {
                        "name": "Technology Hardware & Equipment",
                        "portfolioEmissions": 0.000324399112301343,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Diversified Financials",
                        "portfolioEmissions": 0.0006469796544212892,
                        "capitalAllocated": 37813
                    }
                ],
                "region": [
                    {
                        "name": "Americas",
                        "portfolioEmissions": 0.0009713787667226322,
                        "capitalAllocated": 52107
                    }
                ]
            },
            "benchmark": {
                "gicsSector": [
                    {
                        "name": "Information Technology",
                        "portfolioEmissions": 0.000324399112301343,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Financials",
                        "portfolioEmissions": 0.0006469796544212892,
                        "capitalAllocated": 37813
                    }
                ],
                "gicsIndustry": [
                    {
                        "name": "Technology Hardware & Equipment",
                        "portfolioEmissions": 0.000324399112301343,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Diversified Financials",
                        "portfolioEmissions": 0.0006469796544212892,
                        "capitalAllocated": 37813
                    }
                ],
                "region": [
                    {
                        "name": "Americas",
                        "portfolioEmissions": 0.0009713787667226322,
                        "capitalAllocated": 52107
                    }
                ]
            }
        },
        "scope2": {
            "portfolio": {
                "gicsSector": [
                    {
                        "name": "Information Technology",
                        "portfolioEmissions": 0.006087194801442247,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Financials",
                        "portfolioEmissions": 0.009726196688461392,
                        "capitalAllocated": 37813
                    }
                ],
                "gicsIndustry": [
                    {
                        "name": "Technology Hardware & Equipment",
                        "portfolioEmissions": 0.006087194801442247,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Diversified Financials",
                        "portfolioEmissions": 0.009726196688461392,
                        "capitalAllocated": 37813
                    }
                ],
                "region": [
                    {
                        "name": "Americas",
                        "portfolioEmissions": 0.015813391489903638,
                        "capitalAllocated": 52107
                    }
                ]
            },
            "benchmark": {
                "gicsSector": [
                    {
                        "name": "Information Technology",
                        "portfolioEmissions": 0.006087194801442247,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Financials",
                        "portfolioEmissions": 0.009726196688461392,
                        "capitalAllocated": 37813
                    }
                ],
                "gicsIndustry": [
                    {
                        "name": "Technology Hardware & Equipment",
                        "portfolioEmissions": 0.006087194801442247,
                        "capitalAllocated": 14294
                    },
                    {
                        "name": "Diversified Financials",
                        "portfolioEmissions": 0.009726196688461392,
                        "capitalAllocated": 37813
                    }
                ],
                "region": [
                    {
                        "name": "Americas",
                        "portfolioEmissions": 0.015813391489903638,
                        "capitalAllocated": 52107
                    }
                ]
            }
        }
    },
    "attribution": {
        "totalGHG": [
            {
                "sector": "Information Technology",
                "weightPortfolio": 27.432014892432875,
                "weightBenchmark": 27.432014892432875,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.4689622231002765,
                    "emissionsIntensityBenchmark": 0.4689622231002765,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 0.41664352605700944,
                    "emissionsIntensityBenchmark": 0.41664352605700944,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 3.420131314973555,
                    "emissionsIntensityBenchmark": 3.420131314973555,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            },
            {
                "sector": "Financials",
                "weightPortfolio": 72.56798510756713,
                "weightBenchmark": 72.56798510756713,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.2804161273489338,
                    "emissionsIntensityBenchmark": 0.2804161273489338,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 1.730469464593566,
                    "emissionsIntensityBenchmark": 1.730469464593566,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 2.855216881594373,
                    "emissionsIntensityBenchmark": 2.855216881594373,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            },
            {
                "sector": "Total",
                "weightPortfolio": 100,
                "weightBenchmark": 100,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.3321381204145429,
                    "emissionsIntensityBenchmark": 0.3321381204145429,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 1.370060537473572,
                    "emissionsIntensityBenchmark": 1.370060537473572,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 3.010184293088453,
                    "emissionsIntensityBenchmark": 3.010184293088453,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            }
        ],
        "scope1": [
            {
                "sector": "Information Technology",
                "weightPortfolio": 27.432014892432875,
                "weightBenchmark": 27.432014892432875,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.02372747415435862,
                    "emissionsIntensityBenchmark": 0.02372747415435862,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 0.021080372808589036,
                    "emissionsIntensityBenchmark": 0.021080372808589036,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 0.17304395403975925,
                    "emissionsIntensityBenchmark": 0.17304395403975925,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            },
            {
                "sector": "Financials",
                "weightPortfolio": 72.56798510756713,
                "weightBenchmark": 72.56798510756713,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.01748967945491923,
                    "emissionsIntensityBenchmark": 0.01748967945491923,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 0.10793015554560705,
                    "emissionsIntensityBenchmark": 0.10793015554560705,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 0.17808115569337823,
                    "emissionsIntensityBenchmark": 0.17808115569337823,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            },
            {
                "sector": "Total",
                "weightPortfolio": 100,
                "weightBenchmark": 100,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.019200832225828832,
                    "emissionsIntensityBenchmark": 0.019200832225828832,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 0.08410551021114267,
                    "emissionsIntensityBenchmark": 0.08410551021114267,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 0.1766993497855956,
                    "emissionsIntensityBenchmark": 0.1766993497855956,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            }
        ],
        "scope2": [
            {
                "sector": "Information Technology",
                "weightPortfolio": 27.432014892432875,
                "weightBenchmark": 27.432014892432875,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.44523474894591797,
                    "emissionsIntensityBenchmark": 0.44523474894591797,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 0.3955631532484204,
                    "emissionsIntensityBenchmark": 0.3955631532484204,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 3.2470873609337954,
                    "emissionsIntensityBenchmark": 3.2470873609337954,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            },
            {
                "sector": "Financials",
                "weightPortfolio": 72.56798510756713,
                "weightBenchmark": 72.56798510756713,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.26292644789401454,
                    "emissionsIntensityBenchmark": 0.26292644789401454,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 1.6225393090479594,
                    "emissionsIntensityBenchmark": 1.6225393090479594,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 2.6771357259009947,
                    "emissionsIntensityBenchmark": 2.6771357259009947,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            },
            {
                "sector": "Total",
                "weightPortfolio": 100,
                "weightBenchmark": 100,
                "weightComparison": 0,
                "emissionsIntensityEnterpriseValue": {
                    "emissionsIntensityPortfolio": 0.312937288188714,
                    "emissionsIntensityBenchmark": 0.312937288188714,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityMarketCap": {
                    "emissionsIntensityPortfolio": 1.2859550272624294,
                    "emissionsIntensityBenchmark": 1.2859550272624294,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                },
                "emissionsIntensityRevenue": {
                    "emissionsIntensityPortfolio": 2.8334849433028575,
                    "emissionsIntensityBenchmark": 2.8334849433028575,
                    "emissionsIntensityComparison": 0,
                    "sectorAllocation": 0,
                    "securityAllocation": 0
                }
            }
        ]
    }
}
scenario_data = {
    "scenarios": [
        "MS0VH86TEJGWDK8V"
    ],
    "results": [
        {
            "summary": {
                "estimatedPnl": -10570.100235985032,
                "estimatedPerformance": 5.867062741998796,
                "stressedMarketValue": -190730.10023598504
            },
            "factorPnl": [
                {
                    "name": "Currency",
                    "factorExposure": -360320,
                    "estimatedPnl": -3471.845645552283,
                    "factors": [
                        {
                            "name": "AED",
                            "factorExposure": -180160.00000000003,
                            "factorShock": 0.0027226443140238032,
                            "estimatedPnl": -4.905115996145284,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 189689.99999999997,
                                    "estimatedPnl": 5.164583999271752
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -369850,
                                    "estimatedPnl": -10.069699995417036
                                }
                            ]
                        },
                        {
                            "name": "BRL",
                            "factorExposure": -180160,
                            "factorShock": 1.9243675230662394,
                            "estimatedPnl": -3466.9405295561373,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 189690,
                                    "estimatedPnl": 3650.3327545043494
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -369850,
                                    "estimatedPnl": -7117.273284060487
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Industry",
                    "factorExposure": -180160,
                    "estimatedPnl": -6040.119337162676,
                    "factors": [
                        {
                            "name": "Biotechnology",
                            "factorExposure": 189690,
                            "factorShock": -7.941253726728414,
                            "estimatedPnl": -15063.76419423113,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 189690,
                                    "estimatedPnl": -15063.76419423113
                                }
                            ]
                        },
                        {
                            "name": "Health Care Providers & Services",
                            "factorExposure": -369850,
                            "factorShock": -2.4398120473349882,
                            "estimatedPnl": 9023.644857068453,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -369850,
                                    "estimatedPnl": 9023.644857068453
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Style",
                    "factorExposure": 375097.91196133004,
                    "estimatedPnl": 5023.410933430805,
                    "factors": [
                        {
                            "name": "Dividend Yield",
                            "factorExposure": 39292.92823909999,
                            "factorShock": 0.6191212422128611,
                            "estimatedPnl": 243.27086541572396,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": -80909.0466669,
                                    "estimatedPnl": -500.9250947866948
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 120201.97490599999,
                                    "estimatedPnl": 744.1959602024187
                                }
                            ]
                        },
                        {
                            "name": "Earnings Yield",
                            "factorExposure": 28047.463723279994,
                            "factorShock": 1.0996305646159277,
                            "estimatedPnl": 308.41848370075127,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": -14836.828701720004,
                                    "estimatedPnl": -163.15030322382168
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 42884.292425,
                                    "estimatedPnl": 471.568786924573
                                }
                            ]
                        },
                        {
                            "name": "Exchange Rate Sensitivity",
                            "factorExposure": 253936.74563119997,
                            "factorShock": 0.1803193519871238,
                            "estimatedPnl": 457.8970941793707,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 225295.87526399997,
                                    "estimatedPnl": 406.2520623297635
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 28640.8703672,
                                    "estimatedPnl": 51.6450318496072
                                }
                            ]
                        },
                        {
                            "name": "Growth",
                            "factorExposure": -44761.018989899996,
                            "factorShock": -0.7552222730204394,
                            "estimatedPnl": 338.0451850426333,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": -26364.8708325,
                                    "estimatedPnl": 199.11337678010935
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -18396.1481574,
                                    "estimatedPnl": 138.93180826252396
                                }
                            ]
                        },
                        {
                            "name": "Leverage",
                            "factorExposure": 191868.018137,
                            "factorShock": 0.167948580725219,
                            "estimatedPnl": 322.2396133266973,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 52489.679485500004,
                                    "estimatedPnl": 88.1556717231137
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 139378.3386515,
                                    "estimatedPnl": 234.0839416035836
                                }
                            ]
                        },
                        {
                            "name": "Liquidity",
                            "factorExposure": 88641.57049540001,
                            "factorShock": -1.2990094028817012,
                            "estimatedPnl": -1151.4623355972578,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 19569.494045400003,
                                    "estimatedPnl": -254.20956774612065
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 69072.07645000001,
                                    "estimatedPnl": -897.2527678511373
                                }
                            ]
                        },
                        {
                            "name": "Market Sensitivity",
                            "factorExposure": 9435.966403949995,
                            "factorShock": 1.8499630741892314,
                            "estimatedPnl": 174.5618941659764,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 36458.8713591,
                                    "estimatedPnl": 674.4756574095036
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -27022.904955150003,
                                    "estimatedPnl": -499.91376324352717
                                }
                            ]
                        },
                        {
                            "name": "Medium-Term Momentum",
                            "factorExposure": -158802.2664814,
                            "factorShock": -0.8293589360579001,
                            "estimatedPnl": 1317.0407877259704,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 19560.973170600002,
                                    "estimatedPnl": -162.23067897025948
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -178363.23965200002,
                                    "estimatedPnl": 1479.27146669623
                                }
                            ]
                        },
                        {
                            "name": "Profitability",
                            "factorExposure": 123348.2983915,
                            "factorShock": 0.44359069709951626,
                            "estimatedPnl": 547.1615766952461,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 201297.377697,
                                    "estimatedPnl": 892.9364409691684
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -77949.0793055,
                                    "estimatedPnl": -345.7748642739222
                                }
                            ]
                        },
                        {
                            "name": "Size",
                            "factorExposure": -156279.36591819994,
                            "factorShock": -1.2578893438789152,
                            "estimatedPnl": 1965.8214905665745,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 170372.65707780002,
                                    "estimatedPnl": -2143.0994982650127
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -326652.02299599996,
                                    "estimatedPnl": 4108.920988831587
                                }
                            ]
                        },
                        {
                            "name": "Value",
                            "factorExposure": 38081.90757720001,
                            "factorShock": 1.660035175814345,
                            "estimatedPnl": 632.1730614026285,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": -77920.3687998,
                                    "estimatedPnl": -1293.5055312009458
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 116002.276377,
                                    "estimatedPnl": 1925.6785926035743
                                }
                            ]
                        },
                        {
                            "name": "Volatility",
                            "factorExposure": -37712.3352478,
                            "factorShock": 0.34937317545509217,
                            "estimatedPnl": -131.75678319350888,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": -74956.7850228,
                                    "estimatedPnl": -261.8789000532033
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": 37244.449775,
                                    "estimatedPnl": 130.12211685969444
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Country",
                    "factorExposure": -180160,
                    "estimatedPnl": -6081.546186700877,
                    "factors": [
                        {
                            "name": "United States",
                            "factorExposure": -180160,
                            "factorShock": 3.375636204873933,
                            "estimatedPnl": -6081.546186700877,
                            "byAsset": [
                                {
                                    "assetId": "MA4B66MW5E27U9VBB94",
                                    "name": "Apple Inc",
                                    "bbid": "AAPL UW",
                                    "factorExposure": 189690,
                                    "estimatedPnl": 6403.244317025364
                                },
                                {
                                    "assetId": "MA4B66MW5E27UAL9SUX",
                                    "name": "Microsoft Corp",
                                    "bbid": "MSFT UW",
                                    "factorExposure": -369850,
                                    "estimatedPnl": -12484.79050372624
                                }
                            ]
                        }
                    ]
                }
            ],
            "bySectorAggregations": [
                {
                    "name": "Information Technology",
                    "exposure": -2882560,
                    "estimatedPnl": -10570.100235985032,
                    "industries": [
                        {
                            "name": "Software",
                            "exposure": -5917600,
                            "estimatedPnl": -3047.0113322484867
                        },
                        {
                            "name": "Technology Hardware, Storage & Peripherals",
                            "exposure": 3035040,
                            "estimatedPnl": -7523.088903736546
                        }
                    ]
                }
            ],
            "byRegionAggregations": [
                {
                    "name": "United States",
                    "exposure": -2882560,
                    "estimatedPnl": -10570.100235985032
                }
            ],
            "byDirectionAggregations": [
                {
                    "name": "LONG",
                    "exposure": 3035040,
                    "estimatedPnl": -7523.088903736546
                },
                {
                    "name": "SHORT",
                    "exposure": -5917600,
                    "estimatedPnl": -3047.0113322484867
                }
            ],
            "byAsset": [
                {
                    "assetId": "MA4B66MW5E27U9VBB94",
                    "name": "Apple Inc",
                    "sector": "Information Technology",
                    "industry": "Technology Hardware, Storage & Peripherals",
                    "country": "United States",
                    "direction": "LONG",
                    "exposure": 3035040,
                    "estimatedPnl": -7523.088903736545,
                    "estimatedPerformance": -0.24787445647294748
                },
                {
                    "assetId": "MA4B66MW5E27UAL9SUX",
                    "name": "Microsoft Corp",
                    "sector": "Information Technology",
                    "industry": "Software",
                    "country": "United States",
                    "direction": "SHORT",
                    "exposure": -5917600,
                    "estimatedPnl": -3047.0113322484845,
                    "estimatedPerformance": 0.05149066060985001
                }
            ]
        }
    ]
}
scenario_results = {
    'byAsset': [{'assetId': 'MA4B66MW5E27U9VBB94',
                 'country': 'United States',
                 'direction': 'LONG',
                 'estimatedPerformance': -0.24787445647294748,
                 'estimatedPnl': -7523.088903736545,
                 'exposure': 3035040,
                 'industry': 'Technology Hardware, Storage & Peripherals',
                 'name': 'Apple Inc',
                 'scenarioId': 'MS0VH86TEJGWDK8V',
                 'scenarioName': 'US Presidential Election 2016',
                 'scenarioType': 'Factor Historical Simulation',
                 'sector': 'Information Technology'},
                {'assetId': 'MA4B66MW5E27UAL9SUX',
                 'country': 'United States',
                 'direction': 'SHORT',
                 'estimatedPerformance': 0.05149066060985001,
                 'estimatedPnl': -3047.0113322484845,
                 'exposure': -5917600,
                 'industry': 'Software',
                 'name': 'Microsoft Corp',
                 'scenarioId': 'MS0VH86TEJGWDK8V',
                 'scenarioName': 'US Presidential Election 2016',
                 'scenarioType': 'Factor Historical Simulation',
                 'sector': 'Information Technology'}],
    'byDirectionAggregations': [{'direction': 'LONG',
                                 'estimatedPnl': -7523.088903736546,
                                 'exposure': 3035040,
                                 'scenarioId': 'MS0VH86TEJGWDK8V',
                                 'scenarioName': 'US Presidential Election 2016',
                                 'scenarioType': 'Factor Historical Simulation'},
                                {'direction': 'SHORT',
                                 'estimatedPnl': -3047.0113322484867,
                                 'exposure': -5917600,
                                 'scenarioId': 'MS0VH86TEJGWDK8V',
                                 'scenarioName': 'US Presidential Election 2016',
                                 'scenarioType': 'Factor Historical Simulation'}],
    'byRegionAggregations': [{'country': 'United States',
                              'estimatedPnl': -10570.100235985032,
                              'exposure': -2882560,
                              'scenarioId': 'MS0VH86TEJGWDK8V',
                              'scenarioName': 'US Presidential Election 2016',
                              'scenarioType': 'Factor Historical Simulation'}],
    'bySectorAggregations': [{'estimatedPnl': -3047.0113322484867,
                              'exposure': -5917600,
                              'industry': 'Software',
                              'scenarioId': 'MS0VH86TEJGWDK8V',
                              'scenarioName': 'US Presidential Election 2016',
                              'scenarioType': 'Factor Historical Simulation',
                              'sector': 'Information Technology'},
                             {'estimatedPnl': -7523.088903736546,
                              'exposure': 3035040,
                              'industry': 'Technology Hardware, Storage & '
                                          'Peripherals',
                              'scenarioId': 'MS0VH86TEJGWDK8V',
                              'scenarioName': 'US Presidential Election 2016',
                              'scenarioType': 'Factor Historical Simulation',
                              'sector': 'Information Technology'}],
    'factorPnl': [{'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 5.164583999271752,
                   'factor': 'AED',
                   'factorCategory': 'Currency',
                   'factorExposure': 189689.99999999997,
                   'factorShock': 0.0027226443140238032,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': -10.069699995417036,
                   'factor': 'AED',
                   'factorCategory': 'Currency',
                   'factorExposure': -369850.0,
                   'factorShock': 0.0027226443140238032,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 3650.3327545043494,
                   'factor': 'BRL',
                   'factorCategory': 'Currency',
                   'factorExposure': 189690.0,
                   'factorShock': 1.9243675230662394,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': -7117.273284060487,
                   'factor': 'BRL',
                   'factorCategory': 'Currency',
                   'factorExposure': -369850.0,
                   'factorShock': 1.9243675230662394,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -15063.76419423113,
                   'factor': 'Biotechnology',
                   'factorCategory': 'Industry',
                   'factorExposure': 189690.0,
                   'factorShock': -7.941253726728414,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 9023.644857068453,
                   'factor': 'Health Care Providers & Services',
                   'factorCategory': 'Industry',
                   'factorExposure': -369850.0,
                   'factorShock': -2.4398120473349882,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -500.9250947866948,
                   'factor': 'Dividend Yield',
                   'factorCategory': 'Style',
                   'factorExposure': -80909.0466669,
                   'factorShock': 0.6191212422128611,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 744.1959602024187,
                   'factor': 'Dividend Yield',
                   'factorCategory': 'Style',
                   'factorExposure': 120201.97490599999,
                   'factorShock': 0.6191212422128611,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -163.15030322382168,
                   'factor': 'Earnings Yield',
                   'factorCategory': 'Style',
                   'factorExposure': -14836.828701720004,
                   'factorShock': 1.0996305646159277,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 471.568786924573,
                   'factor': 'Earnings Yield',
                   'factorCategory': 'Style',
                   'factorExposure': 42884.292425,
                   'factorShock': 1.0996305646159277,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 406.2520623297635,
                   'factor': 'Exchange Rate Sensitivity',
                   'factorCategory': 'Style',
                   'factorExposure': 225295.87526399997,
                   'factorShock': 0.1803193519871238,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 51.6450318496072,
                   'factor': 'Exchange Rate Sensitivity',
                   'factorCategory': 'Style',
                   'factorExposure': 28640.8703672,
                   'factorShock': 0.1803193519871238,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 199.11337678010935,
                   'factor': 'Growth',
                   'factorCategory': 'Style',
                   'factorExposure': -26364.8708325,
                   'factorShock': -0.7552222730204394,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 138.93180826252396,
                   'factor': 'Growth',
                   'factorCategory': 'Style',
                   'factorExposure': -18396.1481574,
                   'factorShock': -0.7552222730204394,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 88.1556717231137,
                   'factor': 'Leverage',
                   'factorCategory': 'Style',
                   'factorExposure': 52489.679485500004,
                   'factorShock': 0.167948580725219,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 234.0839416035836,
                   'factor': 'Leverage',
                   'factorCategory': 'Style',
                   'factorExposure': 139378.3386515,
                   'factorShock': 0.167948580725219,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -254.20956774612065,
                   'factor': 'Liquidity',
                   'factorCategory': 'Style',
                   'factorExposure': 19569.494045400003,
                   'factorShock': -1.2990094028817012,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': -897.2527678511373,
                   'factor': 'Liquidity',
                   'factorCategory': 'Style',
                   'factorExposure': 69072.07645000001,
                   'factorShock': -1.2990094028817012,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 674.4756574095036,
                   'factor': 'Market Sensitivity',
                   'factorCategory': 'Style',
                   'factorExposure': 36458.8713591,
                   'factorShock': 1.8499630741892314,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': -499.91376324352717,
                   'factor': 'Market Sensitivity',
                   'factorCategory': 'Style',
                   'factorExposure': -27022.904955150003,
                   'factorShock': 1.8499630741892314,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -162.23067897025948,
                   'factor': 'Medium-Term Momentum',
                   'factorCategory': 'Style',
                   'factorExposure': 19560.973170600002,
                   'factorShock': -0.8293589360579001,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 1479.27146669623,
                   'factor': 'Medium-Term Momentum',
                   'factorCategory': 'Style',
                   'factorExposure': -178363.23965200002,
                   'factorShock': -0.8293589360579001,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 892.9364409691684,
                   'factor': 'Profitability',
                   'factorCategory': 'Style',
                   'factorExposure': 201297.377697,
                   'factorShock': 0.44359069709951626,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': -345.7748642739222,
                   'factor': 'Profitability',
                   'factorCategory': 'Style',
                   'factorExposure': -77949.0793055,
                   'factorShock': 0.44359069709951626,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -2143.0994982650127,
                   'factor': 'Size',
                   'factorCategory': 'Style',
                   'factorExposure': 170372.65707780002,
                   'factorShock': -1.2578893438789152,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 4108.920988831587,
                   'factor': 'Size',
                   'factorCategory': 'Style',
                   'factorExposure': -326652.02299599996,
                   'factorShock': -1.2578893438789152,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -1293.5055312009458,
                   'factor': 'Value',
                   'factorCategory': 'Style',
                   'factorExposure': -77920.3687998,
                   'factorShock': 1.660035175814345,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 1925.6785926035743,
                   'factor': 'Value',
                   'factorCategory': 'Style',
                   'factorExposure': 116002.276377,
                   'factorShock': 1.660035175814345,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': -261.8789000532033,
                   'factor': 'Volatility',
                   'factorCategory': 'Style',
                   'factorExposure': -74956.7850228,
                   'factorShock': 0.34937317545509217,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': 130.12211685969444,
                   'factor': 'Volatility',
                   'factorCategory': 'Style',
                   'factorExposure': 37244.449775,
                   'factorShock': 0.34937317545509217,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27U9VBB94',
                   'bbid': 'AAPL UW',
                   'estimatedPnl': 6403.244317025364,
                   'factor': 'United States',
                   'factorCategory': 'Country',
                   'factorExposure': 189690.0,
                   'factorShock': 3.375636204873933,
                   'name': 'Apple Inc',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'},
                  {'assetId': 'MA4B66MW5E27UAL9SUX',
                   'bbid': 'MSFT UW',
                   'estimatedPnl': -12484.79050372624,
                   'factor': 'United States',
                   'factorCategory': 'Country',
                   'factorExposure': -369850.0,
                   'factorShock': 3.375636204873933,
                   'name': 'Microsoft Corp',
                   'scenarioId': 'MS0VH86TEJGWDK8V',
                   'scenarioName': 'US Presidential Election 2016',
                   'scenarioType': 'Factor Historical Simulation'}],
    'summary': [{'estimatedPerformance': 5.867062741998796,
                 'estimatedPnl': -10570.100235985032,
                 'scenarioId': 'MS0VH86TEJGWDK8V',
                 'scenarioName': 'US Presidential Election 2016',
                 'scenarioType': 'Factor Historical Simulation',
                 'stressedMarketValue': -190730.10023598504}
                ]}


def test_get_reports(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    mock_reports = (Report.from_dict({'id': 'PPAID', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP',
                                      'type': 'Portfolio Performance Analytics',
                                      'parameters': {'transactionCostModel': 'FIXED'},
                                      'percentageComplete': 0, 'status': 'new'}),
                    Report.from_dict({'id': 'PFRID', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP',
                                      'type': 'Portfolio Factor Risk', 'parameters': {'riskModel': 'AXUS4M',
                                                                                      'transactionCostModel': 'FIXED'},
                                      'percentageComplete': 0, 'status': 'new'}))

    mocker.patch.object(GsPortfolioApi, 'get_portfolio',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)
    mocker.patch.object(GsPortfolioApi, 'get_reports',
                        return_value=mock_reports)

    # run test
    pm = PortfolioManager('MP')
    reports = pm.get_reports()
    assert len(reports) == 2
    assert isinstance(reports[0], PerformanceReport)
    assert isinstance(reports[1], FactorRiskReport)


def test_get_schedule_dates(mocker):
    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value={'startDate': '2019-01-01', 'endDate': '2020-01-02'})

    # run test
    pm = PortfolioManager('MP')
    dates = pm.get_schedule_dates()
    assert dates[1] == dt.date(2020, 1, 2)


def test_set_entitlements(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    entitlements = Entitlements(view=EntitlementBlock(users=[User(user_id='fakeId',
                                                                  name='Fake User',
                                                                  email='fake@gs.com',
                                                                  company='Goldman Sachs')]))

    mocker.patch.object(GsSession, '_get',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 2), dt.date(2020, 2, 1), dt.date(2020, 3, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)
    mocker.patch.object(GsPortfolioApi, 'update_portfolio',
                        return_value='')

    # run test
    pm = PortfolioManager('MP')
    pm.set_entitlements(entitlements)


def test_run_reports(mocker):
    mock_portfolio = TargetPortfolio(id='MP', currency='USD', name='Example Port')
    mock_reports = (Report.from_dict({'id': 'PPAID', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP',
                                      'type': 'Portfolio Performance Analytics',
                                      'parameters': {'transactionCostModel': 'FIXED'},
                                      'percentageComplete': 0, 'status': 'new'}),)
    mock_report_jobs = ({'startDate': '2020-01-01',
                         'endDate': '2020-03-02',
                         'id': 'jobId1',
                         'createdTime': '2021-05-18T17:08:18.72Z',
                         'reportType': 'Portfolio Factor Risk'
                         },
                        {'startDate': '2020-05-01',
                         'endDate': '2020-07-02',
                         'id': 'jobId1',
                         'createdTime': '2020-05-18T17:08:18.72Z',
                         'reportType': 'Portfolio Factor Risk'
                         })
    mock_report_job = {
        'startDate': '2020-01-01',
        'endDate': '2020-03-02',
        'id': 'jobId1',
        'createdTime': '2021-05-18T17:08:18.72Z',
        'reportType': 'Portfolio Factor Risk',
        'status': 'done'
    }
    mock_results = [{
        'date': "2019-08-27",
        'factor': "United States",
        'factorCategory': "Country",
        'pnl': -162.93571064768423,
        'exposure': 19878.043518298073,
        'sensitivity': 52.7507947211687,
        'proportionOfRisk': 0.050898995661382604
    }]

    mocker.patch.object(GsPortfolioApi, 'get_portfolio',
                        return_value=mock_portfolio)
    mocker.patch.object(GsPortfolioApi, 'schedule_reports',
                        return_value='')
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2020, 1, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_positions_for_date',
                        return_value=None)
    mocker.patch.object(GsPortfolioApi, 'get_reports',
                        return_value=mock_reports)
    mocker.patch.object(GsReportApi, 'get_report_jobs',
                        return_value=mock_report_jobs)
    mocker.patch.object(GsReportApi, 'get_report_job',
                        return_value=mock_report_job)
    mocker.patch.object(GsReportApi, 'get_factor_risk_report_results',
                        return_value=mock_results)

    # run test
    pm = PortfolioManager('MP')
    pm.run_reports(is_async=False)


# noinspection DuplicatedCode
def test_batched_schedule_reports(mocker):
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2022, 2, 1), dt.date(2022, 8, 1),
                                      dt.date(2022, 10, 1), dt.date(2022, 11, 1)])

    mocker.patch.object(GsPortfolioApi, 'schedule_reports')
    schedule_spy = mocker.spy(GsPortfolioApi, 'schedule_reports')

    pid = 'MP'
    pm = PortfolioManager(pid)

    pm.schedule_reports(start_date=dt.date(2022, 2, 1), end_date=dt.date(2022, 11, 10),
                        backcast=False, months_per_batch=2)
    assert schedule_spy.call_count == 3, 'For the given positions, batch period of 2 months should result in 3 batches'
    batch_boundaries = [dt.date(2022, 2, 1), dt.date(2022, 8, 1), dt.date(2022, 10, 1), dt.date(2022, 11, 10)]
    for i in range(len(batch_boundaries) - 1):
        schedule_spy.assert_any_call(pid, batch_boundaries[i], batch_boundaries[i + 1], backcast=False)

    schedule_spy.reset_mock()
    pm.schedule_reports(start_date=dt.date(2022, 2, 1), end_date=dt.date(2022, 11, 10),
                        backcast=False, months_per_batch=4)
    assert schedule_spy.call_count == 2, 'For the given positions, batch period of 4 months should result in 2 batches'
    batch_boundaries = [dt.date(2022, 2, 1), dt.date(2022, 8, 1), dt.date(2022, 11, 10)]
    for i in range(len(batch_boundaries) - 1):
        schedule_spy.assert_any_call(pid, batch_boundaries[i], batch_boundaries[i + 1], backcast=False)


# noinspection DuplicatedCode
def test_batched_schedule_reports_wo_dates(mocker):
    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2022, 2, 1), dt.date(2022, 8, 1),
                                      dt.date(2022, 10, 1), dt.date(2022, 11, 1)])
    mocker.patch.object(GsPortfolioApi, 'get_schedule_dates',
                        return_value=[dt.date(2022, 2, 1), dt.date(2022, 11, 10)])

    mocker.patch.object(GsPortfolioApi, 'schedule_reports')
    schedule_spy = mocker.spy(GsPortfolioApi, 'schedule_reports')

    pid = 'MP'
    pm = PortfolioManager(pid)

    pm.schedule_reports(backcast=False, months_per_batch=2)
    assert schedule_spy.call_count == 3, 'For the given positions, batch period of 2 months should result in 3 batches'
    batch_boundaries = [dt.date(2022, 2, 1), dt.date(2022, 8, 1), dt.date(2022, 10, 1), dt.date(2022, 11, 10)]
    for i in range(len(batch_boundaries) - 1):
        schedule_spy.assert_any_call(pid, batch_boundaries[i], batch_boundaries[i + 1], backcast=False)


def test_batched_schedule_validations(mocker):
    pm = PortfolioManager('PM')

    # start date should be before end date
    with pytest.raises(Exception):
        pm.schedule_reports(backcast=False, start_date=dt.date(2022, 2, 1), end_date=dt.date(2022, 1, 1))

    mocker.patch.object(GsPortfolioApi, 'get_schedule_dates',
                        return_value=[dt.date(2022, 2, 1), dt.date(2022, 11, 5)])

    # start date should be before maximum possible end date
    with pytest.raises(Exception):
        pm.schedule_reports(backcast=False, start_date=dt.date(2022, 12, 1))

    # end date should be after first possible start date
    with pytest.raises(Exception):
        pm.schedule_reports(backcast=False, end_date=dt.date(2022, 1, 1))

    mocker.patch.object(GsPortfolioApi, 'get_position_dates',
                        return_value=[dt.date(2022, 2, 1), dt.date(2022, 8, 1),
                                      dt.date(2022, 10, 1), dt.date(2022, 11, 1)])
    # start date should be on a position date
    with pytest.raises(Exception):
        pm.schedule_reports(backcast=False, start_date=dt.date(2022, 3, 1))


def test_esg_summary(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    summary = pm.get_esg_summary()
    assert all(summary.columns.values == ['gross', 'long', 'short'])


def test_esg_quintiles(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    quintiles = pm.get_esg_quintiles(measure=ESGMeasure.G_PERCENTILE)
    assert all(quintiles.columns.values == ['description', 'gross', 'long', 'short'])


def test_esg_by_sector(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    breakdown = pm.get_esg_by_region(measure=ESGMeasure.G_PERCENTILE)
    assert all(breakdown.columns.values == ['name', 'gross', 'long', 'short'])


def test_esg_by_region(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    breakdown = pm.get_esg_by_region(measure=ESGMeasure.G_PERCENTILE)
    assert all(breakdown.columns.values == ['name', 'gross', 'long', 'short'])


def test_esg_top_ten(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    ranked = pm.get_esg_top_ten(measure=ESGMeasure.G_PERCENTILE)
    assert ranked.size == 6


def test_esg_bottom_ten(mocker):
    mocker.patch.object(GsEsgApi, 'get_esg',
                        return_value=esg_data)

    # run test
    pm = PortfolioManager('MP')
    ranked = pm.get_esg_bottom_ten(measure=ESGMeasure.G_PERCENTILE)
    assert ranked.size == 6


def test_carbon_coverage(mocker):
    mocker.patch.object(GsCarbonApi, 'get_carbon_analytics', return_value=carbon_data)

    pm = PortfolioManager('MP')
    coverage = pm.get_carbon_coverage(coverage_category=CarbonCoverageCategory.NUMBER_OF_COMPANIES)
    assert coverage.to_dict() == carbon_data.get(CarbonCard.COVERAGE.value).get(
        CarbonCoverageCategory.NUMBER_OF_COMPANIES.value).get(CarbonEntityType.PORTFOLIO.value)


def test_carbon_sbti_netzero_coverage(mocker):
    mocker.patch.object(GsCarbonApi, 'get_carbon_analytics', return_value=carbon_data)

    pm = PortfolioManager('MP')
    coverage = pm.get_carbon_sbti_netzero_coverage(
        target_coverage_category=CarbonTargetCoverageCategory.CAPITAL_ALLOCATED)
    assert coverage.to_dict().get('scienceBasedTarget') == carbon_data.get(
        CarbonCard.SBTI_AND_NET_ZERO_TARGETS.value).get(CarbonTargetCoverageCategory.CAPITAL_ALLOCATED.value).get(
        'scienceBasedTarget').get(CarbonEntityType.PORTFOLIO.value)


def test_carbon_emissions(mocker):
    mocker.patch.object(GsCarbonApi, 'get_carbon_analytics', return_value=carbon_data)

    pm = PortfolioManager('MP')
    emissions = pm.get_carbon_emissions(scope=CarbonScope.SCOPE1)
    assert emissions.to_dict('records') == carbon_data.get(CarbonCard.EMISSIONS.value).get(
        CarbonScope.SCOPE1.value).get(CarbonEntityType.PORTFOLIO.value)


def test_carbon_emissions_allocation(mocker):
    mocker.patch.object(GsCarbonApi, 'get_carbon_analytics', return_value=carbon_data)

    pm = PortfolioManager('MP')
    emissions = pm.get_carbon_emissions_allocation(classification=CarbonEmissionsAllocationCategory.GICS_INDUSTRY)
    assert emissions.rename(columns={CarbonEmissionsAllocationCategory.GICS_INDUSTRY.value: 'name'}).to_dict(
        'records') == carbon_data.get(CarbonCard.ALLOCATIONS.value).get(CarbonScope.TOTAL_GHG.value).get(
        CarbonEntityType.PORTFOLIO.value).get(CarbonEmissionsAllocationCategory.GICS_INDUSTRY.value)


def test_carbon_attribution_table(mocker):
    mocker.patch.object(GsCarbonApi, 'get_carbon_analytics', return_value=carbon_data)

    pm = PortfolioManager('MP')
    attribution = pm.get_carbon_attribution_table(benchmark_id='MA', scope=CarbonScope.SCOPE2,
                                                  intensity_metric=CarbonEmissionsIntensityType.EI_REVENUE)
    attribution = attribution.to_dict('records')
    for entry in attribution:
        entry[CarbonEmissionsIntensityType.EI_REVENUE.value] = {
            'emissionsIntensityPortfolio': entry.pop('emissionsIntensityPortfolio'),
            'emissionsIntensityBenchmark': entry.pop('emissionsIntensityBenchmark'),
            'emissionsIntensityComparison': entry.pop('emissionsIntensityComparison'),
            'sectorAllocation': entry.pop('sectorAllocation'),
            'securityAllocation': entry.pop('securityAllocation')
        }
    actual_table = []
    for entry in carbon_data.get(CarbonCard.ATTRIBUTION.value).get(CarbonScope.SCOPE2.value):
        new_entry = copy.deepcopy(entry)
        new_entry.pop(CarbonEmissionsIntensityType.EI_ENTERPRISE_VALUE.value)
        new_entry.pop(CarbonEmissionsIntensityType.EI_MARKETCAP.value)
        actual_table.append(new_entry)
    assert attribution == actual_table


def test_get_macro_exposure(mocker):
    portfolio_constituents = {"date": ["2022-05-02", "2022-05-02"],
                              "assetId": ["mq1", "mq2"],
                              "direction": ["LONG", "LONG"],
                              "netExposure": [1000, 1000]}
    assets_data = [{"id": "mq1", "name": "asset1", "gsid": "1"},
                   {"id": "mq2", "name": "asset2", "gsid": "2"}]
    factor_sens = {"factor1": {("1", "2022-05-02"): 1,
                               ("2", "2022-05-02"): 1},
                   "factor2": {("1", "2022-05-02"): 5,
                               ("2", "2022-05-02"): 5}}
    factor_data = {"identifier": ["15", "17"],
                   "name": ["factor1", "factor2"],
                   "type": ["Factor", "Factor"],
                   "factorCategory": ["category1", "category2"],
                   "factorCategoryId": ["c1", "c2"]}

    result = {("Asset Information", "Asset Name"): {"1": "asset1", "2": "asset2", "Total Factor Exposure": np.nan},
              ("Asset Information", "Notional"): {"1": 1000, "2": 1000, "Total Factor Exposure": 2000},
              ("category2", "factor2"): {"1": 50.0, "2": 50.0, "Total Factor Exposure": 100.0},
              ("category1", "factor1"): {"1": 10.0, "2": 10.0, "Total Factor Exposure": 20.0}}

    pm = PortfolioManager("portfolioId")
    macro_model = MacroRiskModel(id_="fake_macro_model",
                                 name="fake_model",
                                 coverage=CoverageType.Region,
                                 vendor="fake_vendor",
                                 term=Term.Long,
                                 universe_identifier=UniverseIdentifier.sedol,
                                 version=0.1)
    fake_ppa = PerformanceReport(report_id='id',
                                 position_source_type=PositionSourceType.Portfolio,
                                 position_source_id='PORTFOLIOID',
                                 report_type=ReportType.Portfolio_Performance_Analytics,
                                 parameters=None,
                                 status=ReportStatus.done
                                 )

    mocker.patch.object(PortfolioManager, "get_performance_report", return_value=fake_ppa)
    mocker.patch.object(fake_ppa, "get_portfolio_constituents",
                        return_value=pd.DataFrame.from_dict(portfolio_constituents))
    mocker.patch.object(GsAssetApi, "get_many_assets_data_scroll", return_value=assets_data)
    mocker.patch.object(macro_model, "get_factor_data", return_value=pd.DataFrame.from_dict(factor_data))
    mocker.patch.object(macro_model, "get_universe_sensitivity",
                        return_value=pd.DataFrame.from_dict(factor_sens))

    exposure_df = pm.get_macro_exposure(model=macro_model, date=dt.date(2022, 5, 2), factor_type=FactorType.Factor)

    assert exposure_df.equals(pd.DataFrame.from_dict(result))


def test_get_factor_scenario_analytics(mocker):
    risk_report = FactorRiskReport(report_id='id',
                                   risk_model='RISK_MODEL')

    mocker.patch.object(PortfolioManager, "get_factor_risk_report", return_value=risk_report)
    mocker.patch.object(GsFactorScenarioApi, "calculate_scenario", return_value=scenario_data)

    pm = PortfolioManager("portfolioId")

    factor_scenario = FactorScenario(name='US Presidential Election 2016',
                                     description='Presidential Elections in 2016 when Donald Trump won',
                                     id_="MS0VH86TEJGWDK8V",
                                     type=FactorScenarioType.Factor_Historical_Simulation,
                                     parameters=HistoricalSimulationParameters(start_date=dt.date(2016, 1, 1),
                                                                               end_date=dt.date(2020, 1, 1)))

    scenario_analytics_data = pm.get_factor_scenario_analytics(
        scenarios=[factor_scenario],
        date=dt.date(2024, 3, 5),
        measures=[ScenarioCalculationMeasure.SUMMARY,
                  ScenarioCalculationMeasure.ESTIMATED_FACTOR_PNL,
                  ScenarioCalculationMeasure.ESTIMATED_PNL_BY_SECTOR,
                  ScenarioCalculationMeasure.ESTIMATED_PNL_BY_REGION,
                  ScenarioCalculationMeasure.ESTIMATED_PNL_BY_DIRECTION,
                  ScenarioCalculationMeasure.ESTIMATED_PNL_BY_ASSET],
        risk_model="RISK_MODEL")

    assert len(
        set(scenario_analytics_data.keys()) - {"summary", "factorPnl", "bySectorAggregations",
                                               "byRegionAggregations", "byDirectionAggregations", "byAsset"}) == 0
    for key, value in scenario_analytics_data.items():
        result_df = pd.DataFrame(scenario_results[key])
        result_df.columns = result_df.columns.map(lambda x: {
            "factorCategory": "Factor Category",
            "factor": "Factor",
            "sector": "Sector",
            "country": "Country",
            "industry": "Industry",
            "direction": "Direction",
            "scenarioId": "Scenario ID",
            "scenarioName": "Scenario Name",
            "scenarioType": "Scenario Type",
            "assetId": "Asset ID",
            "name": "Asset Name",
            "bbid": "BBID",
            "factorExposure": "Factor Exposure",
            "factorShock": "Factor Shock (%)",
            "exposure": "Exposure",
            "estimatedPnl": "Estimated Pnl",
            "estimatedPerformance": "Estimated Performance (%)",
            "stressedMarketValue": "Stressed Market Value"

        }.get(x, x))
        result_df = result_df.reindex(columns=value.columns.tolist())
        pd.testing.assert_frame_equal(value, result_df)


if __name__ == '__main__':
    pytest.main(args=[__file__])
