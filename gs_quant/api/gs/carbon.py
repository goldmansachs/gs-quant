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
import logging
from enum import Enum
from typing import Dict, List
from urllib.parse import urlencode

from gs_quant.session import GsSession
from gs_quant.target.common import Currency

_logger = logging.getLogger(__name__)


class CarbonCard(Enum):
    """
    Carbon Cards
    """
    COVERAGE = 'coverage'
    SBTI_AND_NET_ZERO_TARGETS = 'sbtiAndNetZeroTargets'
    EMISSIONS = 'emissions'
    ALLOCATIONS = 'allocations'
    ATTRIBUTION = 'attribution'

    # highestEmitters should not be accessible through API

    def __str__(self):
        return self.value


class CarbonCoverageCategory(Enum):
    """
    Carbon Coverage Category
    """
    WEIGHTS = 'weights'
    NUMBER_OF_COMPANIES = 'numberOfCompanies'

    def __str__(self):
        return self.value


class CarbonTargetCoverageCategory(Enum):
    """
    Carbon Targets Coverage Category
    """
    CAPITAL_ALLOCATED = 'capitalAllocated'
    PORTFOLIO_EMISSIONS = 'portfolioEmissions'

    def __str__(self):
        return self.value


class CarbonScope(Enum):
    """
    Carbon Scopes
    """
    TOTAL_GHG = 'totalGHG'
    SCOPE1 = 'scope1'
    SCOPE2 = 'scope2'

    def __str__(self):
        return self.value


class CarbonEmissionsAllocationCategory(Enum):
    """
    Carbon Emissions Allocation Category
    """
    GICS_SECTOR = 'gicsSector'
    GICS_INDUSTRY = 'gicsIndustry'
    REGION = 'region'

    def __str__(self):
        return self.value


class CarbonEmissionsIntensityType(Enum):
    """
    Carbon Emissions Intensity Type
    """
    EI_ENTERPRISE_VALUE = 'emissionsIntensityEnterpriseValue'
    EI_REVENUE = 'emissionsIntensityRevenue'
    EI_MARKETCAP = 'emissionsIntensityMarketCap'

    def __str__(self):
        return self.value


class CarbonEntityType(Enum):
    """
    Carbon analytics at portfolio or benchmark
    """
    PORTFOLIO = 'portfolio'
    BENCHMARK = 'benchmark'

    def __str__(self):
        return self.value


class CarbonAnalyticsView(Enum):
    """
    Carbon analytics at Long or Short component of
    """
    LONG = 'Long'
    SHORT = 'Short'

    def __str__(self):
        return self.value


class GsCarbonApi:
    """GS Carbon API client implementation"""

    @classmethod
    def get_carbon_analytics(cls,
                             entity_id: str,
                             benchmark_id: str = None,
                             reporting_year: str = 'Latest',
                             currency: Currency = None,
                             include_estimates: bool = False,
                             use_historical_data: bool = False,
                             normalize_emissions: bool = False,
                             cards: List[CarbonCard] = [],
                             analytics_view: CarbonAnalyticsView = CarbonAnalyticsView.LONG) -> Dict:
        url = f'/carbon/{entity_id}?'
        url += urlencode(
            dict(filter(lambda item: item[1] is not None,
                        dict(benchmark=benchmark_id,
                             reportingYear=reporting_year,
                             currency=currency.value if currency is not None else None,
                             includeEstimates=str(include_estimates).lower(),
                             useHistoricalData=str(use_historical_data).lower(),
                             normalizeEmissions=str(normalize_emissions).lower(),
                             card=[c for c in CarbonCard] if len(cards) == 0 else cards,
                             analyticsView=analytics_view.value).items())), True)

        # TODO: Add scope as API parameter
        return GsSession.current._get(url)
