"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicablNe law or agreed to in writing,
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
from gs_quant.target.portfolios import Position, PositionSet
from gs_quant.risk import ResolvedInstrumentValues, RiskMeasure
from gs_quant.risk.results import PortfolioRiskResult
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.assets import GsAssetApi

import copy
import datetime as dt
import pandas as pd
from itertools import chain
import logging
from typing import Iterable, Optional, Tuple, Union

_logger = logging.getLogger(__name__)


class Portfolio(PriceableImpl):
    """A collection of instruments

    Portfolio holds a collection of instruments in order to run pricing and risk scenarios

    """

    def __init__(self,
                 instruments: Optional[Union[Instrument, Iterable[Instrument], dict]] = (),
                 name: Optional[str] = None):
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

        self.name = name

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
    def __from_internal_positions(id_type: str, positions_id):
        instruments = GsPortfolioApi.get_instruments_by_position_type(id_type, positions_id)
        return Portfolio(instruments=instruments, name=positions_id)

    @staticmethod
    def from_eti(eti: str):
        return Portfolio.__from_internal_positions('ETI', eti)

    @staticmethod
    def from_book(book: str, book_type: str = 'risk'):
        return Portfolio.__from_internal_positions(book_type, book)

    @staticmethod
    def from_portfolio_id(portfolio_id: str):
        response = GsPortfolioApi.get_latest_positions(portfolio_id)
        positions = response.positions if isinstance(response, PositionSet) else response['positions']
        instruments = GsAssetApi.get_instruments_for_positions(positions)
        ret = Portfolio(instruments)
        ret.name = portfolio_id
        return ret

    @staticmethod
    def from_portfolio_name(name: str):
        portfolio = GsPortfolioApi.get_portfolio_by_name(name)
        ret = Portfolio.load_from_portfolio_id(portfolio.id)
        ret.name = name
        return ret

    def save(self):
        if not self.name:
            raise ValueError('name not set')

        try:
            portfolio_id = GsPortfolioApi.get_portfolio_by_name(self.name).id
        except ValueError:
            from gs_quant.target.portfolios import Portfolio as MarqueePortfolio
            portfolio_id = GsPortfolioApi.create_portfolio(MarqueePortfolio('USD', self.name)).id
            _logger.info('Created Marquee portfolio with ID: {}'.format(portfolio_id))

        position_set = PositionSet(
            position_date=dt.date.today(),
            positions=tuple(Position(asset_id=GsAssetApi.get_or_create_asset_from_instrument(i))
                            for i in self.instruments))

        GsPortfolioApi.update_positions(portfolio_id, (position_set,))

    def append(self, instruments: Union[Instrument, Iterable[Instrument]]):
        self.instruments = self.instruments + ((instruments,) if isinstance(instruments, Instrument)
                                               else tuple(instruments))

    def pop(self, item):
        instrument = self[item]
        self.instruments = [inst for inst in self.instruments if inst != instrument]
        return instrument

    def to_frame(self) -> pd.DataFrame:
        def to_records(portfolio: Portfolio) -> list:
            records = []

            for inst in portfolio.instruments:
                if isinstance(inst, Portfolio):
                    records.extend(to_records(inst))
                else:
                    records.append(dict(chain(inst.as_dict().items(),
                                              (('instrument', inst), ('portfolio', self.name)))))

            return records

        return pd.DataFrame.from_records(to_records(self)).set_index(['portfolio', 'instrument'])

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

    def resolve(self, in_place: bool = True) -> Optional[PortfolioRiskResult]:
        with self.__pricing_context:
            futures = [i.resolve(in_place) for i in self.__instruments]

        if not in_place:
            return PortfolioRiskResult(self, (ResolvedInstrumentValues,), futures)

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]], fn=None) -> PortfolioRiskResult:
        with self.__pricing_context:
            return PortfolioRiskResult(self,
                                       (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure,
                                       [i.calc(risk_measure, fn=fn) for i in self.__instruments])
