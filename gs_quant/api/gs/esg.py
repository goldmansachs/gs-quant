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
import datetime as dt
import logging
from enum import Enum
from typing import List, Dict

from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)


class ESGCard(Enum):
    """
    ESG Cards
    """
    QUINTILES = 'quintiles'
    SUMMARY = 'summary'
    WEIGHTS_BY_SECTOR = 'weightsBySector'
    MEASURES_BY_SECTOR = 'measuresBySector'
    WEIGHTS_BY_REGION = 'weightsByRegion'
    MEASURES_BY_REGION = 'measuresByRegion'
    TOP_TEN_RANKED = 'topTenRanked'
    BOTTOM_TEN_RANKED = 'bottomTenRanked'

    def __str__(self):
        return self.value


class ESGMeasure(Enum):
    """
    ESG Measures
    """
    G_PERCENTILE = 'gPercentile'
    G_REGIONAL_PERCENTILE = 'gRegionalPercentile'
    ES_PERCENTILE = 'esPercentile'
    ES_DISCLOSURE_PERCENTAGE = 'esDisclosurePercentage'
    ES_MOMENTUM_PERCENTILE = 'esMomentumPercentile'

    def __str__(self):
        return self.value


class GsEsgApi:
    """GS ESG API client implementation"""

    @classmethod
    def get_esg(cls,
                entity_id: str,
                benchmark_id: str = None,
                pricing_date: dt.date = dt.date.today(),
                measures: List[ESGMeasure] = [],
                cards: List[ESGCard] = []) -> Dict:
        url = f'/esg/{entity_id}?'
        if pricing_date:
            url += f'&date={pricing_date.strftime("%Y-%m-%d")}'
        if benchmark_id:
            url += f'&benchmark={benchmark_id}'
        for measure in measures:
            url += f'&measure={measure}'
        for card in cards:
            url += f'&card={card}'

        return GsSession.current._get(url)
