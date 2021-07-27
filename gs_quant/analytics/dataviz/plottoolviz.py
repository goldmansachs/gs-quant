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

This product uses the FRED® API but is not endorsed or certified
by the Federal Reserve Bank of St. Louis. FRED terms of use
available at https://research.stlouisfed.org/docs/api/terms_of_use.html
"""

from datetime import date
from functools import wraps
from typing import List, Union

from gs_quant.analytics.dataviz.dataviz_base import __DataVizBase, SupportedFigure, DataVizSource, DataVizSourceType
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset
from gs_quant.target.common import Entitlements as Entitlements_


class PlotToolViz(__DataVizBase):
    def __init__(self,
                 id_: str = None,
                 *,
                 entitlements: Union[Entitlements, Entitlements_] = None,
                 dataviz_dict: dict = None):
        super().__init__(self.__class__.__name__, id_, entitlements=entitlements, dataviz_dict=dataviz_dict)
        self.type = SupportedFigure.PLOT
        self.__initialized = False
        sources = None

        if id_:
            if not self._viz_response:
                raise MqValueError('Unable to instantiate DataViz. Unable to fetch visualization entity.')
            sources = self._viz_response['sources']
        elif dataviz_dict:
            sources = dataviz_dict['sources'] if sources in dataviz_dict else None

        if sources:
            for source in sources:
                if source["type"] == DataVizSourceType.HEADER.value:
                    if source["id"]:
                        self.__header_id = source["id"]
                    elif source["alias"]:
                        self.__header_alias = source["alias"]
                    else:
                        raise MqValueError('Unable to instantiate DataViz. Header ID or alias missing.')
                elif source["type"] == DataVizSourceType.TEMPLATE.value:
                    if source["id"]:
                        self.__template_id = source["id"]
                    elif source["alias"]:
                        self.__template_alias = source["alias"]
                    else:
                        raise MqValueError('Unable to instantiate DataViz. Template ID or alias missing.')
        else:
            self.__header_id = None
            self.__header_alias = None
            self.__template_id = None
            self.__template_alias = None

    def __with_source(header_alias: str, template_alias: str, header_id: str = None, template_id: str = None):
        def outer(fn):
            @wraps(fn)
            def inner(self, *args, **kwargs):
                self.__header_id = header_id
                self.__header_alias = header_alias
                self.__template_id = template_id
                self.__template_alias = template_alias
                self.__initialized = True
                fn(self, *args, **kwargs)

            return inner

        return outer

    def save(self) -> str:
        if self.__initialized:
            if not (self.__header_id or self.__header_alias) or \
                    not (self.__template_id or self.__template_alias):
                raise MqValueError('Header and Template ID or alias required to persist component.')

            dataviz_id = super()._save(sources=[
                DataVizSource(type=DataVizSourceType.HEADER, id=self.__header_id, alias=self.__header_alias),
                DataVizSource(type=DataVizSourceType.TEMPLATE, id=self.__template_id, alias=self.__template_alias)
            ])

            return dataviz_id
        else:
            raise MqValueError('Figure not yet initialized/created. Please create a figure before saving it.')

    @__with_source(header_alias='price.chart.header', template_alias='price.chart.template')
    def price_chart(self, assets: List[Asset] = None, start_date: date = None):
        super()._create_payload(locals())

    @__with_source(header_alias='market.cap.header', template_alias='market.cap.template')
    def market_cap(self, assets: List[Asset] = None, start_date: date = None):
        super()._create_payload(locals())
