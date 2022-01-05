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
import json
from enum import Enum
from typing import List

from gs_quant.session import GsSession


class ThematicMeasure(Enum):
    """
    Thematic Measures
    """
    ALL_THEMATIC_EXPOSURES = 'allThematicExposures'
    TOP_FIVE_THEMATIC_EXPOSURES = 'topFiveThematicExposures'
    BOTTOM_FIVE_THEMATIC_EXPOSURES = 'bottomFiveThematicExposures'
    THEMATIC_BREAKDOWN_BY_ASSET = 'thematicBreakdownByAsset'
    NO_THEMATIC_DATA = 'noThematicData'
    NO_PRICING_DATA = 'noPricingData'

    def __str__(self):
        return self.value


class Region(Enum):
    """
    Thematic Regions
    """
    AMERICAS = 'Americas'
    ASIA = 'Asia'
    EUROPE = 'Europe'


class GsThematicApi:
    """GS Thematic API client implementation"""

    @classmethod
    def get_thematics(cls,
                      entity_id: str,
                      basket_ids: List[str] = None,
                      regions: List[Region] = None,
                      start_date: dt.date = None,
                      end_date: dt.date = None,
                      measures: List[ThematicMeasure] = None,
                      notional: float = None) -> List:
        payload = {
            'id': entity_id,
        }
        if basket_ids:
            payload['basketId'] = basket_ids
        if regions:
            payload['region'] = [r.value for r in regions]
        if start_date:
            payload['startDate'] = start_date.strftime("%Y-%m-%d")
        if end_date:
            payload['endDate'] = end_date.strftime("%Y-%m-%d")
        if measures:
            payload['measures'] = [m.value for m in measures]
        if notional:
            payload['notional'] = notional
        return GsSession.current._post('/thematics', payload=json.dumps(payload)).get('results', [])
