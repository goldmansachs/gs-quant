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
from gs_quant.context_base import nullcontext
from gs_quant.instrument import Instrument
from gs_quant.markets import PricingContext
from gs_quant.priceable import PriceableImpl
from gs_quant.risk import RiskMeasure
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.assets import GsAssetApi

import copy
from typing import Iterable, Optional, Tuple, Union


class Portfolio(PriceableImpl):
    """
    A collection of instruments
    """

    def __init__(self, instruments: Union[Instrument, Iterable[Instrument]]):
        super().__init__()
        self.instruments = instruments

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.__instruments[item]
        else:
            idx = self.index(item)
            return self.__instruments[idx] if isinstance(idx, int) else tuple(self.__instruments[i] for i in idx)

    @property
    def instruments(self) -> Tuple[Instrument, ...]:
        return self.__instruments

    @instruments.setter
    def instruments(self, instruments: Union[Instrument, Iterable[Instrument]]):
        self.__instruments = (instruments,) if isinstance(instruments, Instrument) else tuple(instruments)
        self.__instruments_lookup = {}
        self.__instruments_by_name = {}

        for idx, p in enumerate(self.__instruments):
            self.__instruments_lookup.setdefault(p, []).append(idx)
            if p.name:
                self.__instruments_by_name.setdefault(p.name, []).append(idx)

    @instruments.deleter
    def instruments(self):
        self.__instruments = None
        self.__instruments_lookup = None
        self.__instruments_by_name = None

    @staticmethod
    def load_from_portfolio_id(portfolio_id):
        positions = GsPortfolioApi.get_latest_positions(portfolio_id)
        instruments = GsAssetApi.get_instruments_for_positions(positions.positions)
        return Portfolio(instruments)

    def index(self, key: Union[str, Instrument]) -> Union[int, Tuple[int, ...]]:
        if isinstance(key, str):
            idx = self.__instruments_by_name.get(key)
            if idx is None:
                raise ValueError('No instrument named {} exists'.format(key))
            return tuple(idx) if len(idx) > 1 else idx[0]
        elif isinstance(key, Instrument):
            idx = self.__instruments_lookup.get(key)
            if idx is None:
                raise ValueError('Instrument not in portfolio')
            return tuple(idx) if len(idx) > 1 else idx[0]
        else:
            raise ValueError('key must be either a name or Instrument')

    def resolve(self, in_place: bool = True) -> Optional[dict]:
        with copy.copy(PricingContext.current):
            futures = [i.resolve(in_place) for i in self.__instruments]

        return dict(zip(self.__instruments, (f.result() for f in futures))) if not in_place else None

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]]) -> PortfolioRiskResult:
        with PricingContext.current if not PricingContext.current._is_entered else nullcontext():
            return PortfolioRiskResult(self,
                                       (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure,
                                       [p.calc(risk_measure) for p in self.__instruments])
