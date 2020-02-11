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
from gs_quant.markets import PricingContext, PricingFuture
from gs_quant.priceable import PriceableImpl
from gs_quant.risk import ResolvedInstrumentValues, RiskMeasure
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.assets import GsAssetApi

import copy
import pandas as pd
from itertools import chain
from typing import Iterable, Optional, Tuple, Union


class Portfolio(PriceableImpl):
    """
    A collection of instruments
    """

    def __init__(self, instruments: Optional[Union[Instrument, Iterable[Instrument], dict]] = ()):
        """
        Creates a portfolio object which can be used to hold instruments
        :param instruments: constructed with an instrument, a list or tuple of instruments or a dictionary where
                            key is instrument name and value is an instrument
        """
        super().__init__()
        if isinstance(instruments, dict):
            inst_list = []
            for k, v in instruments.items():
                v.name = k
                inst_list.append(v)
            self.instruments = inst_list
        else:
            self.instruments = instruments

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.__instruments[item]
        else:
            idx = self.index(item)
            return self.__instruments[idx] if isinstance(idx, int) else tuple(self.__instruments[i] for i in idx)

    def __len__(self):
        return len(self.instruments)

    @property
    def __pricing_context(self) -> PricingContext:
        return PricingContext.current if not PricingContext.current.is_entered else nullcontext()

    @property
    def instruments(self) -> Tuple[Instrument, ...]:
        return self.__instruments

    @instruments.setter
    def instruments(self, instruments: Union[Instrument, Iterable[Instrument]]):
        self.__instruments = (instruments,) if isinstance(instruments, Instrument) else tuple(instruments)
        self.__instruments_lookup = {}
        self.__instruments_by_name = {}

        for idx, i in enumerate(self.__instruments):
            self.__instruments_lookup.setdefault(copy.copy(i), []).append(idx)
            if i.name:
                self.__instruments_by_name.setdefault(i.name, []).append(idx)

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

    def append(self, instruments: Union[Instrument, Iterable[Instrument]]):
        self.instruments = self.instruments + ((instruments,) if isinstance(instruments, Instrument)
                                               else tuple(instruments))

    def pop(self, item):
        instrument = self[item]
        self.instruments = [inst for inst in self.instruments if inst != instrument]
        return instrument

    def to_frame(self) -> pd.DataFrame:
        inst_list = [dict(chain(inst.as_dict().items(), (('instrument', inst),))) for inst in self.instruments]
        return pd.DataFrame(inst_list).set_index('instrument')

    def index(self, key: Union[str, Instrument]) -> Union[int, Tuple[int, ...]]:
        if isinstance(key, str):
            idx = self.__instruments_by_name.get(key)
            if idx is None:
                raise KeyError('No instrument named {} exists'.format(key))
            return tuple(idx) if len(idx) > 1 else idx[0]
        elif isinstance(key, Instrument):
            idx = self.__instruments_lookup.get(key)
            if idx is None:
                raise KeyError('Instrument not in portfolio')
            return tuple(idx) if len(idx) > 1 else idx[0]
        else:
            raise ValueError('key must be either a name or Instrument')

    def resolve(self, in_place: bool = True) -> Optional[dict]:
        with self.__pricing_context:
            futures = [i.resolve(in_place) for i in self.__instruments]

        if not in_place:
            return PortfolioRiskResult(self,
                                       (ResolvedInstrumentValues,),
                                       futures,
                                       result_future=PricingFuture(PricingContext.current))

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]]) -> PortfolioRiskResult:
        with self.__pricing_context:
            return PortfolioRiskResult(self,
                                       (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure,
                                       [i.calc(risk_measure) for i in self.__instruments],
                                       result_future=PricingFuture(PricingContext.current))
