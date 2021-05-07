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
import sys
from functools import wraps
from itertools import chain
from time import sleep
from typing import Iterable, Optional, Tuple, Union, List

import deprecation
import numpy as np
import pandas as pd
from more_itertools import unique_everseen
from pydash import has
from tqdm import tqdm

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.base import get_enum_value
from gs_quant.context_base import nullcontext
from gs_quant.datetime import prev_business_date
from gs_quant.entities.entitlements import Entitlements
from gs_quant.entities.entity import PositionedEntity, EntityType, Entity
from gs_quant.errors import MqValueError
from gs_quant.instrument import Instrument
from gs_quant.markets import HistoricalPricingContext, OverlayMarket, PricingContext
from gs_quant.markets.position_set import PositionSet
from gs_quant.markets.report import PerformanceReport
from gs_quant.priceable import PriceableImpl
from gs_quant.risk import RiskMeasure, ResolvedInstrumentValues
from gs_quant.risk.results import CompositeResultFuture, PortfolioRiskResult, PortfolioPath, PricingFuture
from gs_quant.target.common import RiskPosition, Currency
from gs_quant.target.portfolios import Portfolio as MQPortfolio
from gs_quant.target.portfolios import RiskRequest, PricingDateAndMarketDataAsOf

_logger = logging.getLogger(__name__)


def _validate_portfolio():
    def _outer(fn):
        @wraps(fn)
        def _inner(self, *args, **kwargs):
            if has(self, '_Portfolio__id') and self._Portfolio__id is None:
                raise NotImplementedError
            return fn(self, *args, **kwargs)
        return _inner
    return _outer


class Portfolio(PriceableImpl, PositionedEntity, Entity):
    """A collection of instruments

    Portfolio holds a collection of instruments in order to run pricing and risk scenarios

    """

    def __init__(self,
                 priceables: Optional[Union[PriceableImpl, Iterable[PriceableImpl], dict]] = (),
                 name: Optional[str] = 'Portfolio ' + dt.datetime.today().strftime("%d %b, %Y"),
                 position_sets: Optional[List] = None,
                 currency: Optional[Currency] = Currency.USD,
                 entitlements: Entitlements = None,
                 *, portfolio_id: str = None):
        """
        Creates a portfolio object which can be used to hold instruments

        :param priceables: constructed with an instrument, portfolio, iterable of either, or a dictionary where
            key is name and value is a priceable
        """
        PriceableImpl.__init__(self)
        Entity.__init__(self, portfolio_id, EntityType.PORTFOLIO)
        self.__name = name
        self.__id = portfolio_id
        self.__currency = currency
        self.__need_to_schedule_reports = False
        self.__entitlements = entitlements if entitlements else Entitlements()
        self.__position_sets = position_sets

        # Can't initialize a portfolio with both priceables or position sets
        if priceables and position_sets:
            raise ValueError('Cannot initialize a portfolio with both position sets and priceables. Please pick one.')

        if portfolio_id:
            # Can't add positions to an existing portfolio within the constructor
            if position_sets:
                raise ValueError(
                    'Cannot add positions to an existing portfolio at construction.'
                    'Please initialize the portfolio without the position sets and then update positions using the '
                    'update_positions(position_sets) function.')
            PositionedEntity.__init__(self, portfolio_id, EntityType.PORTFOLIO)

        if isinstance(priceables, dict):
            priceables_list = []
            for name, priceable in priceables.items():
                priceable.name = name
                priceables_list.append(priceable)
            self.priceables = priceables_list
        else:
            self.priceables = priceables

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
    def __pricing_context(self) -> PricingContext:
        return PricingContext.current if not PricingContext.current.is_entered else nullcontext()

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
    def currency(self) -> Union[Currency, str]:
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = get_enum_value(Currency, value)
        self.__need_to_schedule_reports = True

    @property
    def entitlements(self) -> Entitlements:
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value

    @property
    def position_sets(self) -> List[PositionSet]:
        return self.__position_sets

    @position_sets.setter
    def position_sets(self, value: List[PositionSet]):
        self.__position_sets = value

    @property
    def priceables(self) -> Tuple[PriceableImpl, ...]:
        return self.__priceables

    @priceables.setter
    def priceables(self, priceables: Union[PriceableImpl, Iterable[PriceableImpl]]):
        # Cannot add priceables to a Marquee / position set portfolio
        if (self.id or self.position_sets) and priceables:
            raise ValueError('Cannot add priceables to a portfolio with position sets.')
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

    def data_dimension(self) -> str:
        pass

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.PORTFOLIO

    def subset(self, paths: Iterable[PortfolioPath], name=None):
        return Portfolio(tuple(self[p] for p in paths), name=name)

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

    @staticmethod
    @deprecation.deprecated(deprecated_in='0.8.285',
                            details='from_portfolio_id is now deprecated, please use '
                                    'Portfolio.get(portfolio_id=portfolio_id) instead.')
    def from_portfolio_id(portfolio_id: str):
        return Portfolio.get(portfolio_id=portfolio_id)

    @staticmethod
    @deprecation.deprecated(deprecated_in='0.8.285',
                            details='from_portfolio_id is now deprecated, please use '
                                    'Portfolio.get(name=name) instead.')
    def from_portfolio_name(name: str):
        return Portfolio.get(name=name)

    @staticmethod
    def from_quote(quote_id: str):
        instruments = GsPortfolioApi.get_instruments_by_workflow_id(quote_id)
        return Portfolio(instruments, name=quote_id)

    def save(self):
        if self.portfolios:
            raise ValueError('Cannot save portfolios with nested portfolios')

        if self.__id:
            self._update()
        else:
            self._create()

    def save_as_quote(self, overwrite: Optional[bool] = False):
        if self.portfolios:
            raise ValueError('Cannot save portfolios with nested portfolios')

        pricing_context = self.__pricing_context

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
        if in_place:
            for inst in self.all_instruments:
                inst.scale(scaling, in_place)
        else:
            return Portfolio([inst.scale(scaling, in_place) for inst in self.all_instruments])

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

    @classmethod
    def get(cls, portfolio_id: str = None, name: str = None, **kwargs):
        if portfolio_id is None and name is None:
            raise MqValueError('Please specify a portfolio ID and/or portfolio name.')

        portfolios = GsPortfolioApi.get_portfolios(portfolio_ids=[portfolio_id] if portfolio_id else None,
                                                   portfolio_names=[name] if name else None)
        if len(portfolios) == 0:
            raise ValueError('No portfolios in Marquee match the requested name and/or ID.')
        if len(portfolios) > 1:
            portfolios = {
                'Name': [p.name for p in portfolios],
                'ID': [p.id for p in portfolios],
                'Created Time': [p.created_time for p in portfolios]
            }
            cls._print_dict(portfolios)
            raise ValueError('More than one portfolio matches the requested name and/or ID. To resolve,'
                             ' please find the correct portfolio ID below and set it as your portfolio_id.')
        port = portfolios[0]
        return Portfolio(name=port.name,
                         portfolio_id=port.id,
                         currency=port.currency,
                         entitlements=Entitlements.from_target(port.entitlements))

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
        pricing_context = self.__pricing_context
        with pricing_context:
            if self.id or self.position_sets:
                futures = [p.resolve(in_place)
                           for p in self._get_priceables_from_map(priceables_map=self.convert_positions_to_priceables(),
                                                                  date=pricing_context.pricing_date)]
            else:
                futures = [p.resolve(in_place) for p in self.__priceables]

        if not in_place:
            ret = {} if isinstance(PricingContext.current, HistoricalPricingContext) else Portfolio(name=self.name)
            result_future = PricingFuture() if not isinstance(
                pricing_context, PricingContext) or pricing_context.is_async or pricing_context.is_entered else None

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
        pricing_context = self.__pricing_context
        with pricing_context:
            if self.id or self.position_sets:
                futures = [i.market()
                           for i in self._get_priceables_from_map(priceables_map=self.convert_positions_to_priceables(),
                                                                  date=pricing_context.pricing_date)]
            else:
                futures = [i.market() for i in self.all_instruments]

        result_future = PricingFuture()
        return_future = not isinstance(pricing_context,
                                       PricingContext) or pricing_context.is_async or pricing_context.is_entered

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
        return result_future if return_future else result_future.result()

    def calc(self, risk_measure: Union[RiskMeasure, Iterable[RiskMeasure]], fn=None) -> PortfolioRiskResult:
        # PortfolioRiskResult should hold a copy of the portfolio instead of a reference to the portfolio
        # this is to prevent the portfolio object within portfolioriskresult to hold a reference to the portfolio
        # object should it later be modified in place (eg: resolution)

        # If a position set portfolio, resolve positions held on each date in pricing context
        if self.priceables:
            with self.__pricing_context:
                return PortfolioRiskResult(copy.deepcopy(self),
                                           (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure,
                                           [p.calc(risk_measure, fn=fn) for p in self.__priceables])
        if self.id or self.position_sets:
            priceables_map = self.convert_positions_to_priceables()
            list_of_risk_measures = (risk_measure,) if isinstance(risk_measure, RiskMeasure) else risk_measure
            risk_pricing_context = list_of_risk_measures[0].pricing_context

            # If the pricing context is historical, calc based on position sets held on each date
            if isinstance(risk_pricing_context, HistoricalPricingContext):
                date_range = risk_pricing_context._HistoricalPricingContext__date_range
                start_date = min(date_range)
                end_date = max(date_range)
                position_dates = priceables_map.keys()
                futures = []
                while start_date <= end_date:
                    position_dates_after_start = sorted(list(filter(lambda date: start_date < date, position_dates)))
                    context_end = min(position_dates_after_start[0], end_date) \
                        if position_dates_after_start else end_date
                    if context_end != end_date:
                        context_end = context_end - dt.timedelta(days=1)

                    historical_pricing_context = HistoricalPricingContext(
                        start=start_date,
                        end=prev_business_date(context_end) if context_end != end_date else end_date)
                    with historical_pricing_context:
                        futures = futures + [p.calc(risk_measure, fn=fn)
                                             for p in self._get_priceables_from_map(priceables_map, start_date)]
                    start_date = context_end + dt.timedelta(days=1)
                with self.__pricing_context:
                    return PortfolioRiskResult(copy.deepcopy(self),
                                               (risk_measure,) if isinstance(risk_measure,
                                                                             RiskMeasure) else risk_measure,
                                               futures)

            # If the pricing context exists, calc based on the position set held on the pricing date
            elif isinstance(risk_pricing_context, PricingContext):
                futures = [p.calc(risk_measure, fn=fn)
                           for p in self._get_priceables_from_map(priceables_map, risk_pricing_context.pricing_date)]
                with self.__pricing_context:
                    return PortfolioRiskResult(copy.deepcopy(self),
                                               (risk_measure,) if isinstance(risk_measure,
                                                                             RiskMeasure) else risk_measure,
                                               futures)
            return None

    def _create(self):
        # If a priceables portfolio, try resolving to MQ portfolio
        if self.__priceables:
            self.save()
            self.priceables = None
            return

        # If a positions portfolio, create using MQ API
        port = GsPortfolioApi.create_portfolio(portfolio=MQPortfolio(name=self.name,
                                                                     currency=self.currency,
                                                                     entitlements=self.entitlements.to_target()))
        PositionedEntity.__init__(self, port.id, EntityType.PORTFOLIO)
        Entity.__init__(self, port.id, EntityType.PORTFOLIO)
        self.__id = port.id
        self._PositionedEntity__entity_type = EntityType.PORTFOLIO
        self.entitlements = Entitlements.from_target(port.entitlements)
        self.currency = Currency(port.currency)

        # If the portfolio contains positions, upload them to the MQ portfolio and schedule reports
        if self.position_sets:
            position_sets = self.position_sets
            self.position_sets = None
            self.update_positions(position_sets, False)
            self._schedule_first_reports([pos_set.date for pos_set in position_sets])
            self.position_sets = None

    @_validate_portfolio()
    def delete(self):
        GsPortfolioApi.delete_portfolio(portfolio_id=self.id)
        self.__id = None
        self.name = None
        self.priceables = ()
        self.position_sets = None
        self.currency = None
        self.entitlements = None

    @_validate_portfolio()
    def _update(self):
        GsPortfolioApi.update_portfolio(portfolio=MQPortfolio(name=self.name,
                                                              id_=self.id,
                                                              currency=self.currency,
                                                              entitlements=self.entitlements.to_target()))
        if self.__need_to_schedule_reports:
            self._schedule_first_reports(self.get_position_dates())
            self.__need_to_schedule_reports = False

    @_validate_portfolio()
    def get_performance_report(self) -> PerformanceReport:
        reports = GsReportApi.get_reports(limit=1,
                                          position_source_type='Portfolio',
                                          position_source_id=self.id,
                                          report_type='Portfolio Performance Analytics')
        return PerformanceReport.from_target(reports[0]) if reports else None

    @_validate_portfolio()
    def backcast_reports(self, start_date: dt.date):
        position_dates = self.get_position_dates()
        if len(position_dates) == 0:
            raise MqValueError('Cannot backcast reports on a portfolio with no positions')
        earliest_position_date = min(position_dates)
        if start_date >= earliest_position_date:
            raise MqValueError(f'Backcasting start date must be before {earliest_position_date.strftime("%d %b, %Y")}')
        self._schedule_reports(start_date=start_date,
                               end_date=earliest_position_date,
                               backcast=True)

    def convert_positions_to_priceables(self) -> dict:
        position_sets = self.get_position_sets() if self.id else self.position_sets
        date_to_priceables_map = {}
        for pos_set in position_sets:
            date = pos_set.date
            priceables = GsAssetApi.get_instruments_for_positions([pos.to_target() for pos in pos_set.positions])
            if None in priceables:
                raise MqValueError('All positions on {} could not be successfully resolved into instruments')
            date_to_priceables_map[date] = priceables
        return date_to_priceables_map

    def _schedule_first_reports(self,
                                position_dates: List[dt.date],
                                show_progress: bool = True):
        dates_before_today = list(filter(lambda x: x < dt.date.today(), position_dates))
        latest_date_before_today = max(dates_before_today)
        self._schedule_reports(start_date=min(position_dates),
                               end_date=max(latest_date_before_today, prev_business_date()))
        if dt.date.today() in position_dates:
            self._schedule_reports(start_date=latest_date_before_today,
                                   end_date=dt.date.today())
        if show_progress:
            self._show_report_progress()

    def _schedule_reports(self,
                          start_date,
                          end_date,
                          backcast: bool = False,
                          show_progress: bool = True):
        GsPortfolioApi.schedule_reports(portfolio_id=self.id,
                                        start_date=start_date,
                                        end_date=end_date,
                                        backcast=backcast)
        if show_progress:
            self._show_report_progress()

    @staticmethod
    def _get_priceables_from_map(priceables_map: dict,
                                 date) -> List:
        dates_before = list(filter(lambda d: d <= date, priceables_map.keys()))
        # Convert latest positions to priceables if latest date exists, else return an empty list
        return priceables_map[max(dates_before)] if dates_before else []

    @classmethod
    def _print_dict(cls,
                    dictionary: dict):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        print(pd.DataFrame.from_dict(dictionary))

    def _show_report_progress(self):
        with tqdm(total=100,
                  position=0,
                  maxinterval=1,
                  file=sys.stdout,
                  desc=f'Scheduling Reports for Portfolio "{self.name}"') as progress_bar:
            reports = self.get_reports()
            total_percent_complete = 0
            for report in reports:
                total_percent_complete = total_percent_complete + report.percentage_complete \
                    if report.percentage_complete else total_percent_complete
            progress_bar.n = total_percent_complete / len(reports)
            sleep(5)
