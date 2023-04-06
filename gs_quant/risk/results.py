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
import copy
import datetime as dt
import logging
import operator as op
import weakref
from concurrent.futures import Future
from itertools import chain
from typing import Any, Iterable, Mapping, Optional, Tuple, Union

import pandas as pd
from gs_quant.base import Priceable, RiskKey, Sentinel, InstrumentBase, is_instance_or_iterable, is_iterable, Scenario
from gs_quant.common import RiskMeasure
from gs_quant.config import DisplayOptions
from gs_quant.risk import DataFrameWithInfo, ErrorValue, UnsupportedValue, FloatWithInfo, SeriesWithInfo, ResultInfo, \
    ScalarWithInfo, aggregate_results
from gs_quant.risk.transform import Transformer
from more_itertools import unique_everseen

_logger = logging.getLogger(__name__)


def get_default_pivots(cls: str, has_dates: bool, multi_measures: bool,
                       multi_scen: bool, simple_port: bool = None, ori_cols=None):
    if cls == 'MultipleScenarioResult':
        return 'value', 'scenario', 'dates' if has_dates else None
    elif cls == 'MultipleRiskMeasureResult':
        return 'value', ('risk_measure', 'scenario') if multi_scen else 'risk_measure', 'dates' if has_dates else None
    elif cls == 'PortfolioRiskResult':
        if ori_cols is None:
            raise ValueError('columns of dataframe required to get default pivots')
        portfolio_names = list(filter(lambda x: 'portfolio_name_' in x, ori_cols))
        port_and_inst_names = portfolio_names + ['instrument_name']
        pivot_rules = [
            # has_dates, multi_measures,  simple_port, multi_scen
            # output: (value,index,columns)
            [True, True, None, False, ('value', 'dates', port_and_inst_names + ['risk_measure'])],
            [True, False, None, False, ('value', 'dates', port_and_inst_names)],
            [False, False, False, False, ('value', portfolio_names, 'instrument_name')],
            [False, None, None, False, ('value', port_and_inst_names, 'risk_measure')],

            [True, True, None, True, ('value', 'dates', port_and_inst_names + ['risk_measure', 'scenario'])],
            [True, False, None, True, ('value', 'dates', port_and_inst_names + ['scenario'])],
            [False, True, None, True, ('value', port_and_inst_names, ['risk_measure', 'scenario'])],
            [False, False, None, True, ('value', port_and_inst_names, 'scenario')],
        ]

        def match(rule_value, check_value) -> bool:
            if rule_value is None:
                return True
            elif callable(rule_value):
                return rule_value(check_value)
            else:
                return rule_value == check_value

        for rule in pivot_rules:
            [rule_has_dates, rule_multi_measures, rule_simple_port, rule_multi_scen, rule_output] = rule
            if match(rule_has_dates, has_dates) and match(rule_multi_measures, multi_measures) and \
                    match(rule_simple_port, simple_port) and match(rule_multi_scen, multi_scen):
                return rule_output
        return None, None, None


def pivot_to_frame(df, values, index, columns, aggfunc):
    try:
        pivot_df = df.pivot_table(values=values, index=index, columns=columns, aggfunc=aggfunc)
    except ValueError:
        raise RuntimeError('Unable to successfully pivot data')

    try:  # attempt to correct order of index
        if index is not None:
            idx = df.set_index(list(pivot_df.index.names)).index.unique()
            pivot_df = pivot_df.reindex(index=idx)
        if columns is not None:
            cols = df.set_index(list(pivot_df.columns.names)).index.unique()
            pivot_df = pivot_df.reindex(columns=cols)
        return pivot_df
    except KeyError:
        return pivot_df


def _compose(lhs: ResultInfo, rhs: ResultInfo) -> ResultInfo:
    if isinstance(lhs, ScalarWithInfo):
        if isinstance(rhs, ScalarWithInfo):
            return rhs if lhs.risk_key.date == rhs.risk_key.date else lhs.compose((lhs, rhs))
        elif isinstance(rhs, SeriesWithInfo):
            return lhs.compose((lhs,)).combine_first(rhs).sort_index()
    elif isinstance(lhs, SeriesWithInfo):
        if isinstance(rhs, SeriesWithInfo):
            return rhs.combine_first(lhs).sort_index()
        elif isinstance(rhs, ScalarWithInfo):
            return rhs.compose((rhs,)).combine_first(lhs).sort_index()
    elif isinstance(lhs, DataFrameWithInfo):
        if lhs.index.name != 'date':
            lhs = lhs.assign(date=lhs.risk_key.date).set_index('date')

        if isinstance(rhs, DataFrameWithInfo):
            if rhs.index.name != 'date':
                rhs = rhs.assign(date=rhs.risk_key.date).set_index('date')

            return lhs.loc[set(lhs.index) - set(rhs.index)].append(rhs).sort_index()
    elif isinstance(lhs, MultipleRiskMeasureResult):
        if isinstance(rhs, MultipleRiskMeasureResult):
            return lhs + rhs

    raise RuntimeError(f'{lhs} and {rhs} cannot be composed')


def _value_for_date(result: Union[DataFrameWithInfo, SeriesWithInfo], date: Union[Iterable, dt.date]) -> \
        Union[DataFrameWithInfo, ErrorValue, FloatWithInfo, SeriesWithInfo]:
    from gs_quant.markets import CloseMarket

    raw_value = result.loc[date]
    key = result.risk_key

    risk_key = RiskKey(
        key.provider,
        date if isinstance(date, dt.date) else tuple(date),
        CloseMarket(date=date, location=key.market.location if isinstance(key.market, CloseMarket) else None),
        key.params,
        key.scenario,
        key.risk_measure)

    unit = result.unit
    error = result.error
    if isinstance(raw_value, DataFrameWithInfo):
        raw_value = raw_value.raw_value.set_index('dates')
        raw_value = raw_value.reset_index(drop=True) if isinstance(date, dt.date) else raw_value
    elif isinstance(raw_value, float):
        unit = result.unit.get(date, result.unit) if unit else None
    return _get_value_with_info(raw_value, risk_key, unit, error)


def _get_value_with_info(value, risk_key, unit, error):
    if isinstance(value, ErrorValue):
        return value
    elif isinstance(value, pd.DataFrame):
        return DataFrameWithInfo(value, risk_key=risk_key, unit=unit, error=error)
    elif isinstance(value, pd.Series):
        return SeriesWithInfo(value.raw_value, risk_key=risk_key, unit=unit, error=error)
    else:
        return FloatWithInfo(risk_key, value, unit=unit, error=error)


def _risk_keys_compatible(lhs, rhs) -> bool:
    from gs_quant.markets import historical_risk_key

    while isinstance(lhs, MultipleRiskMeasureResult):
        lhs = next(iter(lhs.values()))

    while isinstance(rhs, MultipleRiskMeasureResult):
        rhs = next(iter(rhs.values()))

    return historical_risk_key(lhs.risk_key).ex_measure == historical_risk_key(rhs.risk_key).ex_measure


def _value_for_measure_or_scen(res: dict, item: Union[Iterable, RiskMeasure, Scenario]) -> dict:
    result = copy.copy(res)
    if isinstance(item, Iterable):
        for value in list(result):
            if value not in item:
                del result[value]
    else:
        for value in list(result):
            if value != item:
                del result[value]
    return result


class PricingFuture(Future):
    __RESULT_SENTINEL = Sentinel('PricingFuture')

    def __init__(self, result: Optional[Any] = __RESULT_SENTINEL):
        super().__init__()
        self.__pricing_context = None

        if result is not self.__RESULT_SENTINEL:
            self.set_result(result)
        else:
            from gs_quant.markets import PricingContext
            self.__pricing_context = weakref.ref(PricingContext.current.active_context)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            operand = other
        elif isinstance(other, self.__class__):
            operand = other.result()
        else:
            raise ValueError(f'Cannot add {self.__class__.__name__} and {other.__class__.name}')

        return self.__class__(_compose(self.result(), operand))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.result() * other)
        else:
            raise ValueError('Can only multiply by an int or float')

    def result(self, timeout=None):
        """Return the result of the call that the future represents.

        :param timeout: The number of seconds to wait for the result if the future isn't done.
        If None, then there is no limit on the wait time.

        Returns:
            The result of the call that the future represents.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given timeout.

        Exception: If the call raised then that exception will be raised.
        """
        if not self.done():
            pricing_context = self.__pricing_context() if self.__pricing_context else None
            if pricing_context is not None and pricing_context.is_entered:
                raise RuntimeError('Cannot evaluate results under the same pricing context being used to produce them')

        return super().result(timeout=timeout)


class CompositeResultFuture(PricingFuture):

    def __init__(self, futures: Iterable[PricingFuture]):
        super().__init__()
        self.__futures = tuple(futures)
        self.__pending = set()

        for future in self.__futures:
            if not future.done():
                future.add_done_callback(self.__cb)
                self.__pending.add(future)

        if not self.__pending:
            self._set_result()

    def __getitem__(self, item):
        return self.result()[item]

    def __cb(self, future: PricingFuture):
        self.__pending.discard(future)
        if not self.__pending:
            self._set_result()

    def _set_result(self):
        self.set_result([f.result() for f in self.__futures])

    @property
    def futures(self) -> Tuple[PricingFuture, ...]:
        return self.__futures


class MultipleRiskMeasureResult(dict):

    def __init__(self, instrument, dict_values: Iterable):
        super().__init__(dict_values)
        self.__instrument = instrument

    def __getitem__(self, item):
        if is_instance_or_iterable(item, dt.date):
            if all(isinstance(v, (DataFrameWithInfo, SeriesWithInfo)) for v in self.values()):
                return MultipleRiskMeasureResult(self.__instrument, ((k, _value_for_date(v, item))
                                                                     for k, v in self.items()))
            elif all(isinstance(v, MultipleScenarioResult) for v in self.values()):
                return MultipleRiskMeasureResult(self.__instrument, ((k, v[item]) for k, v in self.items()))
            else:
                raise ValueError('Can only index by date on historical results')
        elif is_instance_or_iterable(item, Scenario):
            if all(isinstance(v, MultipleScenarioResult) for v in self.values()):
                return MultipleRiskMeasureResult(self.__instrument, ((k, _value_for_measure_or_scen(v, item))
                                                                     for k, v in self.items()))
            else:
                raise ValueError('Can only index by scenario on multiple scenario results')

        else:
            return super().__getitem__(item)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__op(op.mul, other)
        else:
            return ValueError('Can only multiply by an int or float')

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.__op(op.add, other)
        elif isinstance(other, MultipleRiskMeasureResult):
            if not _risk_keys_compatible(self, other):
                raise ValueError('Results must have matching scenario and location')

            instruments_equal = self.__instrument == other.__instrument

            self_dt = [list(self.values())[0].risk_key.date] if len(self.dates) == 0 else self.dates
            other_dt = [list(other.values())[0].risk_key.date] if len(other.dates) == 0 else other.dates
            dates_overlap = not set(self_dt).isdisjoint(other_dt)

            if not set(self.keys()).isdisjoint(other.keys()) and instruments_equal and dates_overlap:
                raise ValueError('Results overlap on risk measures, instruments or dates')

            all_keys = set(chain(self.keys(), other.keys()))

            if not instruments_equal:
                from gs_quant.markets.portfolio import Portfolio
                return PortfolioRiskResult(
                    Portfolio((self.__instrument, other.__instrument)),
                    all_keys,
                    tuple(MultipleRiskMeasureFuture(
                        r.__instrument,
                        {k: PricingFuture(r[k]) if k in r else None for k in all_keys}) for r in (self, other))
                )
            else:
                results = {}
                for result in (self, other):
                    for key in all_keys:
                        if key in result:
                            results[key] = _compose(results[key], result[key]) if key in results else result[key]

                return MultipleRiskMeasureResult(self.__instrument, results)
        else:
            raise ValueError('Can only add instances of MultipleRiskMeasureResult or int, float')

    def __op(self, operator, operand):
        values = {}
        for key, value in self.items():
            if isinstance(value, SeriesWithInfo) or isinstance(value, DataFrameWithInfo):
                new_value = value.copy_with_resultinfo()
                new_value.value = operator(value.value, operand)
            elif isinstance(value, pd.DataFrame) or isinstance(value, pd.Series):
                new_value = value.copy()
                new_value.value = operator(value.value, operand)
            else:
                new_value = operator(value, operand)

            values[key] = new_value

        return MultipleRiskMeasureResult(self.__instrument, values)

    @property
    def instrument(self):
        return self.__instrument

    @property
    def dates(self) -> Tuple[dt.date, ...]:
        dates = set()
        for value in self.values():
            if isinstance(value, (DataFrameWithInfo, SeriesWithInfo)):
                if all([isinstance(i, dt.date) for i in value.index]):
                    dates.update(value.index)

        return tuple(sorted(dates))

    @property
    def _multi_scen_key(self) -> Iterable[Scenario]:
        for value in self.values():
            if isinstance(value, MultipleScenarioResult):
                return tuple(value.scenarios)
        return tuple()

    def to_frame(self, values='default', index='default', columns='default', aggfunc=sum,
                 display_options: DisplayOptions = None):
        df = pd.DataFrame.from_records(self._to_records({}, display_options=display_options))
        if values is None and index is None and columns is None:
            return df
        elif values == 'default' and index == 'default' and columns == 'default':
            if 'mkt_type' in df.columns:
                return df.set_index('risk_measure')
            values, columns, index = get_default_pivots('MultipleRiskMeasureResult', multi_measures=True,
                                                        has_dates='dates' in df.columns,
                                                        multi_scen='scenario' in df.columns)
        else:
            values = 'value' if values == 'default' or values is ['value'] else values
            index = None if index == 'default' else index
            columns = None if columns == 'default' else columns
        return pivot_to_frame(df, values, index, columns, aggfunc)

    def _to_records(self, extra_dict, display_options: DisplayOptions = None):
        return list(chain.from_iterable(
            [dict(item, **{'risk_measure': rm}) for item in self[rm]._to_records(extra_dict, display_options)] for rm in
            self))


class MultipleRiskMeasureFuture(CompositeResultFuture):

    def __init__(self, instrument: InstrumentBase, measures_to_futures: Mapping[RiskMeasure, PricingFuture]):
        self.__measures_to_futures = measures_to_futures
        self.__instrument = instrument
        super().__init__(measures_to_futures.values())

    def __add__(self, other):
        result = self.result() + other.result() if isinstance(other, MultipleRiskMeasureFuture) else other
        return MultipleRiskMeasureFuture(self.__instrument, {k: PricingFuture(v) for k, v in result.items()})

    def _set_result(self):
        self.set_result(MultipleRiskMeasureResult(self.__instrument,
                                                  zip(self.__measures_to_futures.keys(),
                                                      (f.result() for f in self.futures))))

    @property
    def measures_to_futures(self) -> Mapping[RiskMeasure, PricingFuture]:
        return self.__measures_to_futures


class MultipleScenarioFuture(CompositeResultFuture):
    def __init__(self, instrument: InstrumentBase, scenarios: Iterable[Scenario], futures: Iterable[PricingFuture]):
        self.__instrument = instrument
        self.__scenarios = scenarios
        super().__init__(futures)

    def _set_result(self):
        res = next(iter(self.futures)).result()
        values = tuple(res[res['label'] == r]['value'] for r in
                       tuple(unique_everseen(res['label'].values))) if res.index.name == 'date' else tuple(
            v for v in res['value'])
        val_w_info = tuple(_get_value_with_info(v, res.risk_key, res.unit, res.error) for v in values)
        self.set_result(MultipleScenarioResult(self.__instrument, {k: v for k, v in zip(self.__scenarios, val_w_info)}))


class MultipleScenarioResult(dict):
    def __init__(self, instrument, dict_values: Iterable):
        super().__init__(dict_values)
        self.__instrument = instrument

    def __getitem__(self, item):
        if is_instance_or_iterable(item, dt.date):
            if all(isinstance(v, (DataFrameWithInfo, SeriesWithInfo)) for v in self.values()):
                return MultipleScenarioResult(self.__instrument,
                                              ((k, _value_for_date(v, item)) for k, v in self.items()))
            else:
                raise ValueError('Can only index by date on historical results')
        return super().__getitem__(item)

    def to_frame(self, values='default', index='default', columns='default', aggfunc=sum,
                 display_options: DisplayOptions = None):
        df = pd.DataFrame.from_records(self._to_records({}, display_options=display_options))
        if values is None and index is None and columns is None:
            return df
        elif values == 'default' and index == 'default' and columns == 'default':
            if 'mkt_type' in df.columns:
                return df.set_index('scenario')
            values, columns, index = get_default_pivots('MultipleScenarioResult', has_dates='dates' in df.columns,
                                                        multi_measures=False, multi_scen=True)
        else:
            values = 'value' if values == 'default' or values is ['value'] else values
            index = None if index == 'default' else index
            columns = None if columns == 'default' else columns
        return pivot_to_frame(df, values, index, columns, aggfunc)

    @property
    def instrument(self):
        return self.__instrument

    @property
    def scenarios(self):
        return self.keys()

    def _to_records(self, extra_dict, display_options: DisplayOptions = None):
        return list(chain.from_iterable(
            [dict(item, **{'scenario': scen}) for item in self[scen]._to_records(extra_dict, display_options)]
            for scen in self))


class HistoricalPricingFuture(CompositeResultFuture):

    def _set_result(self):
        results = [f.result() for f in self.futures]
        base = next((r for r in results if not isinstance(r, (ErrorValue, UnsupportedValue, Exception))), None)

        if base is None:
            _logger.error(f'Historical pricing failed: {results[0]}')
            self.set_result(results[0])
        else:
            if isinstance(base, MultipleRiskMeasureResult):
                result = MultipleRiskMeasureResult(base.instrument,
                                                   {k: base[k].compose(r[k] for r in results) for k in base.keys()})
            else:
                result = base.compose(results)
            self.set_result(result)


class PortfolioPath:

    def __init__(self, path):
        self.__path = (path,) if isinstance(path, int) else path

    def __repr__(self):
        return repr(self.__path)

    def __iter__(self):
        return iter(self.__path)

    def __len__(self):
        return len(self.__path)

    def __add__(self, other):
        return PortfolioPath(self.__path + other.__path)

    def __eq__(self, other):
        return self.__path == other.__path

    def __hash__(self):
        return hash(self.__path)

    def __call__(self, target, rename_to_parent: Optional[bool] = False):
        parent = None
        path = list(self.__path)

        while path:
            elem = path.pop(0)
            parent = target if len(self) - len(path) > 1 else None
            target = target.futures[elem] if isinstance(target, CompositeResultFuture) else target[elem]

            if isinstance(target, PricingFuture) and path:
                target = target.result()

        if rename_to_parent and parent and getattr(parent, 'name', None) and not isinstance(target, InstrumentBase):
            target = copy.copy(target)
            target.name = parent.name

        return target

    @property
    def path(self):
        return self.__path


class PortfolioRiskResult(CompositeResultFuture):

    def __init__(self,
                 portfolio,
                 risk_measures: Iterable[RiskMeasure],
                 futures: Iterable[PricingFuture]):
        super().__init__(futures)
        self.__portfolio = portfolio
        self.__risk_measures = tuple(risk_measures)

    def __getitem__(self, item):
        futures = []

        if is_instance_or_iterable(item, RiskMeasure):
            '''Slicing a list of risk measures'''
            if isinstance(item, Iterable):
                if any(it not in self.risk_measures for it in item):
                    raise ValueError('{} not computed'.format(item))
            else:
                if item not in self.risk_measures:
                    raise ValueError('{} not computed'.format(item))

            if len(self.risk_measures) == 1:
                return self
            else:
                for idx, priceable in enumerate(self.portfolio):
                    result = self.__result(PortfolioPath(idx))
                    if isinstance(result, PortfolioRiskResult):
                        futures.append(result[item])
                    else:
                        futures.append(MultipleRiskMeasureFuture(priceable,
                                                                 {k: PricingFuture(v) for k, v in
                                                                  _value_for_measure_or_scen(result, item).items()}))

                risk_measure = tuple(item) if isinstance(item, Iterable) else (item,)
                return PortfolioRiskResult(self.__portfolio, risk_measure, futures)

        elif is_instance_or_iterable(item, Scenario):
            '''Slicing a list of scenarios'''
            if isinstance(item, Iterable) and any(it not in self._multi_scen_key for it in item):
                raise ValueError('{} not computed'.format(item))
            else:
                if item not in self._multi_scen_key:
                    raise ValueError('{} not computed'.format(item))

            if len(self._multi_scen_key) == 0:  # field not used if not multiscenario
                return self
            else:
                for idx, priceable in enumerate(self.portfolio):
                    result = self.__result(PortfolioPath(idx))
                    if isinstance(result, PortfolioRiskResult):
                        futures.append(result[item])
                    elif isinstance(result, MultipleRiskMeasureResult):
                        futures.append(MultipleRiskMeasureFuture(priceable, {
                            k: PricingFuture(_value_for_measure_or_scen(result[k], item)) for k in result}))
                    elif isinstance(result, MultipleScenarioResult):
                        futures.append(PricingFuture(_value_for_measure_or_scen(result, item)))
                return PortfolioRiskResult(self.__portfolio, self.risk_measures, futures)

        elif is_instance_or_iterable(item, dt.date):
            for idx, _ in enumerate(self.portfolio):
                result = self.__result(PortfolioPath(idx))
                if isinstance(result, (MultipleRiskMeasureResult, PortfolioRiskResult, MultipleScenarioResult)):
                    futures.append(PricingFuture(result[item]))
                elif isinstance(result, (DataFrameWithInfo, SeriesWithInfo)):
                    futures.append(PricingFuture(_value_for_date(result, item)))
                else:
                    raise RuntimeError('Can only index by date on historical results')
            return PortfolioRiskResult(self.__portfolio, self.risk_measures, futures)

        elif is_iterable(item, InstrumentBase):
            '''Slicing a list/tuple of instruments (not an Portfolio iterable)'''
            return self.subset(item)

        # Inputs from excel always becomes a list
        # Catch list length = 1 so that it doesn't return a sub-PortfolioRiskResult
        elif isinstance(item, list) and len(item) == 1:
            return self.__results(items=item[0])

        else:
            return self.__results(items=item)

    def __contains__(self, item):
        if isinstance(item, RiskMeasure):
            return item in self.__risk_measures
        elif isinstance(item, dt.date):
            return item in self.dates
        else:
            return item in self.__portfolio

    def __repr__(self):
        ret = f'{self.__risk_measures} Results'
        if self.__portfolio.name:
            ret += f' for {self.__portfolio.name}'

        return ret + f' ({len(self)})'

    def __len__(self):
        return len(self.futures)

    def __iter__(self):
        return iter(self.__results())

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return PortfolioRiskResult(self.__portfolio, self.__risk_measures, [f * other for f in self.futures])
        else:
            return ValueError('Can only multiply by an int or float')

    def __add__(self, other):
        def as_multiple_result_futures(portfolio_result):
            if len(portfolio_result.__risk_measures) > 1:
                return portfolio_result
            mr_futures = []
            for p, f in zip(portfolio_result.__portfolio, portfolio_result.futures):
                if isinstance(f, PortfolioRiskResult):
                    mr_futures.append(as_multiple_result_futures(f))
                elif isinstance(f, MultipleRiskMeasureFuture):
                    mr_futures.append(f)
                else:
                    mr_futures.append(MultipleRiskMeasureFuture(p, {portfolio_result.__risk_measures[0]: f}))
            return PortfolioRiskResult(portfolio_result.__portfolio, portfolio_result.__risk_measures, mr_futures)

        def set_value(dest_result, src_result, src_risk_measure):
            for priceable, future in zip(dest_result.__portfolio, dest_result.futures):
                if isinstance(future, PortfolioRiskResult):
                    set_value(future, src_result, src_risk_measure)
                else:
                    try:
                        value = src_result[priceable]
                        value = value[src_risk_measure] if isinstance(value, MultipleRiskMeasureResult) else value
                        future.result()[src_risk_measure] = value
                    except KeyError:
                        pass

        def first_value(portfolio_result):
            if len(portfolio_result.__risk_measures) > 1:
                return next(iter(portfolio_result[next(iter(portfolio_result.portfolio.all_instruments))].values()))
            else:
                return portfolio_result[next(iter(portfolio_result.__portfolio.all_instruments))]

        if isinstance(other, (int, float)):
            return PortfolioRiskResult(self.__portfolio, self.__risk_measures, [f + other for f in self.futures])
        elif isinstance(other, PortfolioRiskResult):
            if not _risk_keys_compatible(first_value(self), first_value(other)) and not \
                    set(self.__portfolio.all_instruments).isdisjoint(other.__portfolio.all_instruments):
                raise ValueError('Results must have matching scenario and location')

            self_dt = (first_value(self).risk_key.date,) if len(self.dates) == 0 else self.dates
            other_dt = (first_value(other).risk_key.date,) if len(other.dates) == 0 else other.dates
            dates_overlap = not set(self_dt).isdisjoint(other_dt)

            if not set(self.__risk_measures).isdisjoint(other.__risk_measures) and dates_overlap and not \
                    set(self.__portfolio.all_instruments).isdisjoint(other.__portfolio.all_instruments):
                raise ValueError('Results overlap on risk measures, instruments or dates')

            self_futures = as_multiple_result_futures(self).futures
            other_futures = as_multiple_result_futures(other).futures

            if self.__portfolio is other.__portfolio or self.__portfolio == other.__portfolio:
                portfolio = self.__portfolio
                futures = [future + other_future for future, other_future in zip(self_futures, other_futures)]
            else:
                portfolio = self.__portfolio + other.__portfolio
                futures = self_futures + other_futures

            ret = PortfolioRiskResult(portfolio, set(chain(self.risk_measures, other.risk_measures)), futures)

            if portfolio is not self.__portfolio and len(ret.risk_measures) > 1:
                # Now fill in overlapping values
                for dest, src in ((self, other), (other, self)):
                    for risk_measure in (m for m in src.risk_measures if dest == self or m not in dest.risk_measures):
                        set_value(ret, src, risk_measure)

            return ret
        else:
            raise ValueError('Can only add instances of PortfolioRiskResult or int, float')

    @property
    def portfolio(self):
        return self.__portfolio

    @property
    def risk_measures(self) -> Tuple[RiskMeasure, ...]:
        return self.__risk_measures

    @property
    def dates(self) -> Tuple[dt.date, ...]:
        dates = set()
        for result in self.__results():
            if isinstance(result, (MultipleRiskMeasureResult, PortfolioRiskResult)):
                if all([isinstance(i, dt.date) for i in result.dates]):
                    dates.update(result.dates)
            elif isinstance(result, (pd.DataFrame, pd.Series)):
                if all([isinstance(i, dt.date) for i in result.index]):
                    dates.update(result.index)
        try:
            return tuple(sorted(dates))
        except TypeError:
            return tuple()

    @property
    def _multi_scen_key(self) -> Iterable[Scenario]:
        for result in self.__results():
            if isinstance(result, MultipleScenarioResult):
                return tuple(result.scenarios)
            elif isinstance(result, (MultipleRiskMeasureResult, PortfolioRiskResult)):
                return result._multi_scen_key
        return tuple()

    def result(self, timeout: Optional[int] = None):
        super().result(timeout=timeout)
        return self

    def subset(self, items: Iterable[Union[int, str, PortfolioPath, Priceable]], name: Optional[str] = None):
        paths = tuple(chain.from_iterable((i,) if isinstance(i, PortfolioPath) else self.__paths(i) for i in items))
        sub_portfolio = self.__portfolio.subset(paths, name=name)
        return PortfolioRiskResult(sub_portfolio, self.risk_measures, [p(self.futures) for p in paths])

    def transform(self, risk_transformation: Transformer = None):
        if risk_transformation is None:
            return self
        elif len(self.__risk_measures) > 1:
            return MultipleRiskMeasureResult(self.portfolio,
                                             ((r, self[r].transform(risk_transformation)) for r in
                                              self.__risk_measures))
        elif len(self.__risk_measures) == 1:
            flattened_results = risk_transformation.apply(self.__results())
            futures = []
            for result in flattened_results:
                transformed_future = PricingFuture()
                transformed_future.set_result(result)
                transformed_future.done()
                futures.append(transformed_future)
            return PortfolioRiskResult(self.portfolio, self.risk_measures, futures)
        else:
            return self

    def aggregate(self, allow_mismatch_risk_keys=False) -> Union[float, pd.DataFrame, pd.Series,
                                                                 MultipleRiskMeasureResult]:
        if len(self.__risk_measures) > 1:
            return MultipleRiskMeasureResult(self.portfolio, ((r, self[r].aggregate()) for r in self.__risk_measures))
        else:
            return aggregate_results(self.__results(), allow_mismatch_risk_keys=allow_mismatch_risk_keys)

    def _to_records(self, display_options: DisplayOptions = None):
        def get_records(rec):
            temp = []
            for f in rec.futures:
                if isinstance(f.result(), ResultInfo) or isinstance(f.result(), MultipleRiskMeasureResult) \
                        or isinstance(f.result(), MultipleScenarioResult):
                    temp.append(f.result())
                else:
                    temp.extend(get_records(f.result()))
            return temp

        future_records = get_records(self)
        portfolio_records = self.__portfolio._to_records()
        records = []
        if len(future_records) == len(portfolio_records):
            for i in range(len(future_records)):
                records.extend(future_records[i]._to_records({**portfolio_records[i]}, display_options))
        return records

    def to_frame(self, values='default', index='default', columns='default', aggfunc=sum,
                 display_options: DisplayOptions = None):
        final_records = self._to_records(display_options=display_options)
        if len(final_records) > 0:
            ori_df = pd.DataFrame.from_records(final_records)
            if 'risk_measure' not in ori_df.columns.values:
                ori_df['risk_measure'] = self.risk_measures[0]
        else:
            return
        df_cols = list(ori_df.columns.values)
        # fill n/a values for different sub-portfolio depths
        cols_except_value = [c for c in df_cols if c != 'value']
        ori_df[cols_except_value] = ori_df[cols_except_value].fillna("N/A")

        has_dt = True if 'dates' in df_cols else False
        other_cols = sorted([p for p in df_cols if 'portfolio' in p]) + ['instrument_name', 'risk_measure']
        other_cols = other_cols + ['dates'] if has_dt else other_cols
        val_cols = [col for col in df_cols if col not in other_cols]
        if 'value' in val_cols and val_cols[-1] != 'value':
            val_cols = [col for col in val_cols if col != 'value'] + ['value']
        sorted_col = other_cols + val_cols
        ori_df = ori_df[sorted_col]

        if values is None and index is None and columns is None:  # to_frame(None, None, None)
            return ori_df
        elif values == 'default' and index == 'default' and columns == 'default':  # to_frame()
            multi_scen = len(self._multi_scen_key) > 1
            has_bucketed = True if 'mkt_type' in df_cols else False
            has_cashflows = True if 'payment_amount' in df_cols else False
            multi_rm = True if len(self.risk_measures) > 1 else False
            port_depth_one = True if len(max(self.portfolio.all_paths, key=len)) == 1 else False
            if has_bucketed or has_cashflows:
                return ori_df.set_index(other_cols)
            else:
                values, index, columns = get_default_pivots('PortfolioRiskResult', has_dates=has_dt,
                                                            multi_measures=multi_rm, simple_port=port_depth_one,
                                                            multi_scen=multi_scen, ori_cols=df_cols)
        else:  # user defined pivoting
            values = 'value' if values == 'default' or values is ['value'] else values

        return pivot_to_frame(ori_df, values, index, columns, aggfunc)

    def __paths(self, items: Union[int, slice, str, Priceable]) -> Tuple[PortfolioPath, ...]:
        if isinstance(items, int):
            return PortfolioPath(items),
        elif isinstance(items, slice):
            return tuple(PortfolioPath(i) for i in range(len(self.__portfolio))[items])
        elif isinstance(items, (str, Priceable)):
            paths = self.__portfolio.paths(items)
            # will enter in here only if trying to slice an unresolved portfolio with a resolved instrument
            if not paths and isinstance(items, InstrumentBase) and items.unresolved:
                paths = self.__portfolio.paths(items.unresolved)
                if not paths:
                    raise KeyError(f'{items} not in portfolio')
                key = items.resolution_key.ex_measure
                paths = tuple(p for p in paths if self.__result(p, self.risk_measures[0]).risk_key.ex_measure == key)

                if not paths:
                    raise KeyError(f'Cannot slice {items} which is resolved in a different pricing context')

            return paths

    def __results(self, items: Optional[Union[int, slice, str, Priceable]] = None):
        if items is None:
            return tuple(self.__result(p) for p in self.__portfolio.all_paths)

        paths = self.__paths(items)
        if not paths:
            raise KeyError(f'{items}')

        return self.__result(paths[0]) if not isinstance(items, slice) else self.subset(paths)

    def __result(self, path: PortfolioPath, risk_measure: Optional[RiskMeasure] = None):
        res = path(self.futures).result()

        if len(self.risk_measures) == 1 and not risk_measure:
            risk_measure = self.risk_measures[0]

        return res[risk_measure] \
            if risk_measure and isinstance(res, (MultipleRiskMeasureResult, PortfolioRiskResult)) else res

    def get(self, item, default):
        try:
            value = self.__getitem__(item)
        except (KeyError, ValueError):
            value = default
        return value
