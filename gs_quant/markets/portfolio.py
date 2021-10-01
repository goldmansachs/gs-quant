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
import copy
import datetime as dt
import logging
from itertools import chain
from typing import Iterable, Optional, Tuple, Union

import deprecation
import numpy as np
import pandas as pd
from more_itertools import unique_everseen

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.instrument import Instrument
from gs_quant.markets import HistoricalPricingContext, OverlayMarket, PricingContext, PositionContext
from gs_quant.priceable import PriceableImpl
from gs_quant.risk import RiskMeasure, ResolvedInstrumentValues
from gs_quant.risk.results import CompositeResultFuture, PortfolioRiskResult, PortfolioPath, PricingFuture
from gs_quant.target.common import RiskPosition
from gs_quant.target.portfolios import Portfolio as MarqueePortfolio
from gs_quant.target.portfolios import Position, PositionSet, RiskRequest, PricingDateAndMarketDataAsOf

_logger = logging.getLogger(__name__)


class Portfolio(PriceableImpl):
    """A collection of instruments

    Portfolio holds a collection of instruments in order to run pricing and risk scenarios

    """

    def __init__(self,
                 priceables: Optional[Union[PriceableImpl, Iterable[PriceableImpl], dict]] = (),
                 name: Optional[str] = None):
        """
        Creates a portfolio object which can be used to hold instruments

        :param priceables: constructed with an instrument, portfolio, iterable of either, or a dictionary where
            key is name and value is a priceable
        """
        super().__init__()
        if isinstance(priceables, dict):
            priceables_list = []
            for name, priceable in priceables.items():
                priceable.name = name
                priceables_list.append(priceable)
            self.priceables = priceables_list
        else:
            self.priceables = priceables

        self.__name = name
        self.__id = None

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.__priceables[item]
        elif isinstance(item, PortfolioPath):
            return item(self, rename_to_parent=True)
        else:
            values = tuple(self[p] for it in item for p in self.paths(it)) if isinstance(item, list) else tuple(
                self[p] for p in self.paths(item))
            return values[0] if len(values) == 1 else values

    def __contains__(self, item):
        if isinstance(item, PriceableImpl):
            return any(item in p.__priceables for p in self.all_portfolios + (self,))
        elif isinstance(item, str):
            return any(item in p.__priceables_by_name for p in self.all_portfolios + (self,))
        else:
            return False

    def __len__(self):
        return len(self.__priceables)

    def __iter__(self):
        return iter(self.__priceables)

    def __hash__(self):
        hash_code = hash(self.__name) ^ hash(self.__id)
        for priceable in self.__priceables:
            hash_code ^= hash(priceable)

        return hash_code

    def __eq__(self, other):
        if not isinstance(other, Portfolio):
            return False

        for path in self.all_paths:
            try:
                if path(self) != path(other):
                    return False
            except (IndexError, TypeError):
                # indexerror occurs when two portfolios are of different lengths
                # typeerror: instrument is not subscriptable occurs when two portfolios are of different depths
                return False

        return True

    def __add__(self, other):
        if not isinstance(other, Portfolio):
            raise ValueError('Can only add instances of Portfolio')

        return Portfolio(self.__priceables + other.__priceables)

    @property
    def __position_context(self) -> PositionContext:
        return PositionContext.current if PositionContext.current.is_entered else PositionContext.default_value()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def priceables(self) -> Tuple[PriceableImpl, ...]:
        return self.__priceables

    @priceables.setter
    def priceables(self, priceables: Union[PriceableImpl, Iterable[PriceableImpl]]):
        self.__priceables = (priceables,) if isinstance(priceables, PriceableImpl) else tuple(priceables)
        self.__priceables_by_name = {}

        for idx, i in enumerate(self.__priceables):
            if i and i.name:
                self.__priceables_by_name.setdefault(i.name, []).append(idx)

    @priceables.deleter
    def priceables(self):
        self.__priceables = None
        self.__priceables_by_name = None

    @property
    def instruments(self) -> Tuple[Instrument, ...]:
        return tuple(unique_everseen(i for i in self.__priceables if isinstance(i, Instrument)))

    @property
    def all_instruments(self) -> Tuple[Instrument, ...]:
        instr = chain(self.instruments, chain.from_iterable(p.all_instruments for p in self.all_portfolios))
        return tuple(unique_everseen(instr))

    @property
    def portfolios(self) -> Tuple[PriceableImpl, ...]:
        return tuple(i for i in self.__priceables if isinstance(i, Portfolio))

    @property
    def all_portfolios(self) -> Tuple[PriceableImpl, ...]:
        stack = list(self.portfolios)
        portfolios = list(unique_everseen(stack))

        while stack:
            portfolio = stack.pop()
            if portfolio in portfolios:
                continue

            sub_portfolios = portfolio.portfolios
            portfolios.extend(sub_portfolios)
            stack.extend(sub_portfolios)

        return tuple(unique_everseen(portfolios))

    def subset(self, paths: Iterable[PortfolioPath], name=None):
        # Do our paths represent a single portfolio?
        paths_tuple = tuple(paths)
        if len(paths_tuple) == 1 and isinstance(self[paths_tuple[0]], Portfolio):
            return self[paths_tuple[0]]
        else:
            return Portfolio(tuple(self[p] for p in paths_tuple), name=name)

    @staticmethod
    def __from_internal_positions(id_type: str, positions_id):
        instruments = GsPortfolioApi.get_instruments_by_position_type(id_type, positions_id)
        return Portfolio(instruments, name=positions_id)

    @staticmethod
    def from_eti(eti: str):
        return Portfolio.__from_internal_positions('ETI', eti.replace(',', '%2C'))

    @staticmethod
    def from_book(book: str, book_type: str = 'risk'):
        return Portfolio.__from_internal_positions(book_type, book)

    @staticmethod
    def from_asset_id(asset_id: str, date=None):
        asset = GsAssetApi.get_asset(asset_id)
        response = GsAssetApi.get_asset_positions_for_date(asset_id, date) if date else \
            GsAssetApi.get_latest_positions(asset_id)
        response = response[0] if isinstance(response, tuple) else response
        positions = response.positions if isinstance(response, PositionSet) else response['positions']
        instruments = GsAssetApi.get_instruments_for_positions(positions)
        ret = Portfolio(instruments, name=asset.name)
        ret.__id = asset_id
        return ret

    @staticmethod
    def from_asset_name(name: str):
        asset = GsAssetApi.get_asset_by_name(name)
        return Portfolio.load_from_portfolio_id(asset.id)

    @classmethod
    def get(cls,
            portfolio_id: str = None,
            portfolio_name: str = None):
        if portfolio_name:
            portfolio = GsPortfolioApi.get_portfolio_by_name(portfolio_name)
            portfolio_id = portfolio.id
        position_date = PositionContext.current.position_date if PositionContext.is_entered else dt.date.today()
        portfolio = GsPortfolioApi.get_portfolio(portfolio_id)
        ret = Portfolio(name=portfolio.name)
        ret.__id = portfolio_id
        ret._get_instruments(position_date, True)
        return ret

    @classmethod
    @deprecation.deprecated(deprecated_in='0.8.293',
                            details='from_portfolio_id is now deprecated, please use '
                                    'Portfolio.get(portfolio_id=portfolio_id) instead.')
    def from_portfolio_id(cls, portfolio_id: str):
        return cls.get(portfolio_id=portfolio_id)

    @classmethod
    @deprecation.deprecated(deprecated_in='0.8.293',
                            details='from_portfolio_name is now deprecated, please use '
                                    'Portfolio.get(portfolio_name=portfolio_name) instead.')
    def from_portfolio_name(cls, name: str):
        return cls.get(portfolio_name=name)

    @staticmethod
    def from_quote(quote_id: str):
        instruments = GsPortfolioApi.get_instruments_by_workflow_id(quote_id)
        return Portfolio(instruments, name=quote_id)

    def save(self, overwrite: Optional[bool] = False):
        if self.portfolios:
            raise ValueError('Cannot save portfolios with nested portfolios')

        if self.__id:
            if not overwrite:
                raise ValueError(f'Portfolio with id {id} already exists. Use overwrite=True to overwrite')
        else:
            if not self.__name:
                raise ValueError('name not set')
            self.__id = GsPortfolioApi.create_portfolio(MarqueePortfolio('USD', self.__name)).id
            _logger.info(f'Created Marquee portfolio {self.__name} with id {self.__id}')

        position_set = PositionSet(
            position_date=self.__position_context.position_date,
            positions=tuple(Position(asset_id=GsAssetApi.get_or_create_asset_from_instrument(i))
                            for i in self.instruments))
        if len(position_set.positions) > 0:
            GsPortfolioApi.update_positions(self.__id, [position_set])

    def save_as_quote(self, overwrite: Optional[bool] = False):
        if self.portfolios:
            raise ValueError('Cannot save portfolios with nested portfolios')

        pricing_context = self._pricing_context

        request = RiskRequest(
            tuple(RiskPosition(instrument=i, quantity=i.instrument_quantity) for i in self.instruments),
            (ResolvedInstrumentValues,),
            pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=pricing_context.pricing_date,
                                                                        market=pricing_context.market),)
        )

        if self.__id:
            if not overwrite:
                raise ValueError(f'Portfolio with id {id} already exists. Use overwrite=True to overwrite')
            else:
                GsPortfolioApi.update_quote(self.__id, request)
                _logger.info(f'Updated Structuring with id {self.__id}')
        else:
            self.__id = GsPortfolioApi.save_quote(request)
            _logger.info(f'Created Structuring with id {self.__id}')

    def save_to_shadowbook(self, name: str):
        if self.portfolios:
            raise ValueError('Cannot save portfolios with nested portfolios')

        pricing_context = self._pricing_context

        request = RiskRequest(
            tuple(RiskPosition(instrument=i, quantity=i.instrument_quantity) for i in self.instruments),
            (ResolvedInstrumentValues,),
            pricing_and_market_data_as_of=(PricingDateAndMarketDataAsOf(pricing_date=pricing_context.pricing_date,
                                                                        market=pricing_context.market),)
        )
        status = GsPortfolioApi.save_to_shadowbook(request, name)
        print(f'Save to shadowbook status - {status}')

    @classmethod
    def from_frame(cls, data: pd.DataFrame, mappings: dict = None):
        def get_value(this_row: pd.Series, attribute: str):
            value = mappings.get(attribute, attribute)
            return value(this_row) if callable(value) else this_row.get(value)

        instruments = []
        mappings = mappings or {}
        data = data.replace({np.nan: None})

        for row in (r for _, r in data.iterrows() if any(v for v in r.values if v is not None)):
            instrument = None
            for init_keys in (('asset_class', 'type'), ('$type',)):
                init_values = tuple(filter(None, (get_value(row, k) for k in init_keys)))
                if len(init_keys) == len(init_values):
                    instrument = Instrument.from_dict(dict(zip(init_keys, init_values)))
                    instrument = instrument.from_dict({p: get_value(row, p) for p in instrument.properties()})
                    break

            if instrument:
                instruments.append(instrument)
            else:
                raise ValueError('Neither asset_class/type nor $type specified')

        return cls(instruments)

    @classmethod
    def from_csv(
            cls,
            csv_file: str,
            mappings: Optional[dict] = None
    ):
        data = pd.read_csv(csv_file, skip_blank_lines=True).replace({np.nan: None})
        return cls.from_frame(data, mappings)

    def scale(self, scaling: int, in_place: bool = True):
        instruments = self._get_instruments(self.__position_context.position_date, in_place, False)
        if in_place:
            for inst in self.all_instruments:
                inst.scale(scaling, in_place)
        else:
            return Portfolio([inst.scale(scaling, in_place) for inst in instruments])

    def append(self, priceables: Union[PriceableImpl, Iterable[PriceableImpl]]):
        self.priceables += ((priceables,) if isinstance(priceables, PriceableImpl) else tuple(priceables))

    def pop(self, item) -> PriceableImpl:
        priceable = self[item]
        self.priceables = [inst for inst in self.instruments if inst != priceable]
        return priceable

    def to_frame(self, mappings: Optional[dict] = None) -> pd.DataFrame:
        def to_records(portfolio: Portfolio) -> list:
            records = []

            for priceable in portfolio.priceables:
                if isinstance(priceable, Portfolio):
                    records.extend(to_records(priceable))
                else:
                    as_dict = priceable.as_dict()
                    if hasattr(priceable, '_type'):
                        as_dict['$type'] = priceable._type

                    records.append(dict(chain(as_dict.items(),
                                              (('instrument', priceable), ('portfolio', portfolio.name)))))

            return records

        df = pd.DataFrame.from_records(to_records(self)).set_index(['portfolio', 'instrument'])
        all_columns = df.columns.to_list()
        columns = sorted(c for c in all_columns if c not in ('asset_class', 'type', '$type'))

        for asset_column in ('$type', 'type', 'asset_class'):
            if asset_column in all_columns:
                columns = [asset_column] + columns

        df = df[columns]
        mappings = mappings or {}

        for key, value in mappings.items():
            if isinstance(value, str):
                df[key] = df[value]
            elif callable(value):
                df[key] = len(df) * [None]
                df[key] = df.apply(value, axis=1)

        return df

    def to_csv(self, csv_file: str, mappings: Optional[dict] = None, ignored_cols: Optional[list] = None):
        port_df = self.to_frame(mappings or {})
        port_df = port_df[np.setdiff1d(port_df.columns, ignored_cols or [])]
        port_df.reset_index(drop=True, inplace=True)

        port_df.to_csv(csv_file)

    @property
    def all_paths(self) -> Tuple[PortfolioPath, ...]:
        paths = ()
        stack = [(None, self)]
        while stack:
            parent, portfolio = stack.pop()

            for idx, priceable in enumerate(portfolio.__priceables):
                path = parent + PortfolioPath(idx) if parent is not None else PortfolioPath(idx)
                if isinstance(priceable, Portfolio):
                    stack.insert(0, (path, priceable))
                else:
                    paths += (path,)

        return paths

    def paths(self, key: Union[str, PriceableImpl]) -> Tuple[PortfolioPath, ...]:
        if not isinstance(key, (str, Instrument, Portfolio)):
            raise ValueError('key must be a name or Instrument or Portfolio')

        if isinstance(key, str):
            idx = self.__priceables_by_name.get(key)
        else:
            idx = []
            for p_idx, p in enumerate(self.__priceables):
                if p == key or getattr(p, "unresolved", None) == key:
                    idx.append(p_idx)

        paths = tuple(PortfolioPath(i) for i in idx) if idx else ()

        for path, porfolio in ((PortfolioPath(i), p)
                               for i, p in enumerate(self.__priceables) if isinstance(p, Portfolio)):
            paths += tuple(path + sub_path for sub_path in porfolio.paths(key))

        return paths

    def resolve(self, in_place: bool = True) -> Optional[Union[PricingFuture, PriceableImpl, dict]]:
        priceables = self._get_instruments(self.__position_context.position_date, in_place, True)
        pricing_context = self._pricing_context
        with pricing_context:
            futures = [p.resolve(in_place) for p in priceables]

        if not in_place:
            ret = {} if isinstance(PricingContext.current, HistoricalPricingContext) else Portfolio(name=self.name)
            result_future = PricingFuture() if self._return_future else None

            def cb(future: CompositeResultFuture):
                if isinstance(ret, Portfolio):
                    ret.priceables = [f.result() for f in future.futures]
                else:
                    priceables_by_date = {}
                    for future in futures:
                        for date, priceable in future.result().items():
                            priceables_by_date.setdefault(date, []).append(priceable)

                    for date, priceables in priceables_by_date.items():
                        if any(p for p in priceables if not isinstance(p, PriceableImpl)):
                            _logger.error(f'Error resolving on {date}, skipping that date')
                        else:
                            ret[date] = Portfolio(priceables, name=self.name)

                if result_future:
                    result_future.set_result(ret)

            CompositeResultFuture(futures).add_done_callback(cb)
            return result_future or ret

    def market(self) -> Union[OverlayMarket, PricingFuture, dict]:
        """
        Market Data map of coordinates and values. Note that this is not yet supported on all instruments

        ***Examples**

        >>> from gs_quant.markets.portfolio import Portfolio
        >>>
        >>> portfolio = Portfolio(...)
        >>> market = portfolio.market()

        """
        pricing_context = self._pricing_context
        instruments = self._get_instruments(self.__position_context.position_date, False, False)
        with pricing_context:
            futures = [i.market() for i in instruments]

        result_future = PricingFuture()

        def cb(future: CompositeResultFuture):
            def update_market_data(all_market_data, this_market_data):
                for item in this_market_data:
                    existing_value = all_market_data.setdefault(item.coordinate, item.value)
                    if abs(existing_value - item.value) > 1e-6:
                        raise ValueError(
                            f'Conflicting values for {item.coordinate}: {existing_value} vs {item.value}')

            results = [f.result() for f in future.futures]
            is_historical = isinstance(results[0], dict)
            market_data = None if is_historical else {}
            overlay_markets = {} if is_historical else None

            for result in results:
                if market_data is not None:
                    update_market_data(market_data, result.market_data)
                else:
                    for market in result.values():
                        update_market_data(overlay_markets.setdefault(market.base_market, {}), market.market_data)

            if market_data:
                ret = OverlayMarket(base_market=results[0].base_market, market_data=market_data)
            else:
                ret = {base_market.date: OverlayMarket(base_market=base_market, market_data=market_data)
                       for base_market, market_data in overlay_markets.items()}

            if result_future:
                result_future.set_result(ret)

        CompositeResultFuture(futures).add_done_callback(cb)
        return result_future if self._return_future else result_future.result()

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]], fn=None) -> PortfolioRiskResult:
        priceables = self._get_instruments(self.__position_context.position_date, False, True)
        with self._pricing_context:
            # PortfolioRiskResult should hold a copy of the portfolio instead of a reference to the portfolio
            # this is to prevent the portfolio object within portfolioriskresult to hold a reference to the portfolio
            # object should it later be modified in place (eg: resolution)
            return PortfolioRiskResult(copy.deepcopy(self),
                                       (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure,
                                       [p.calc(risk_measure, fn=fn) for p in priceables])

    def _get_instruments(self, position_date: dt.date, in_place: bool, return_priceables: bool = True):
        if self.id:
            dates_prior = list(filter(lambda date: date < position_date,
                                      GsPortfolioApi.get_position_dates(self.id)))
            if len(dates_prior) == 0:
                raise ValueError('Your portfolio has no positions on the PositionContext date')
            date = max(dates_prior)
            response = GsPortfolioApi.get_positions_for_date(self.id, date)
            positions = response.positions if response else []
            instruments = GsAssetApi.get_instruments_for_positions(positions)
            if in_place:
                self.__priceables = instruments
            return instruments
        return self.__priceables if return_priceables else self.all_instruments
