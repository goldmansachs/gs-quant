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
from gs_quant.entities.entitlements import Entitlements, User, EntitlementBlock
from gs_quant.markets.portfolio_manager import PortfolioManager
from gs_quant.markets.report import FactorRiskReport, PerformanceReport
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

    result = {("Asset Information", "Asset Name"): {"1": "asset1", "2": "asset2", "Total Factor Exposure": np.NAN},
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


if __name__ == '__main__':
    pytest.main(args=[__file__])
