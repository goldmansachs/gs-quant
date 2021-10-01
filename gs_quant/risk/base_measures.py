"""
Copyright 2021 Goldman Sachs.
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
from typing import Union, Iterable

import pandas as pd
from gs_quant.base import Market, EnumBase, Base
from gs_quant.common import AssetClass, CurrencyParameter, FiniteDifferenceParameter, AggregationLevel, \
    StringParameter, ListOfStringParameter, ListOfNumberParameter, MapParameter
from gs_quant.context_base import do_not_serialise
from gs_quant.target.risk import RiskMeasure as __RiskMeasure, RiskMeasureType, RiskMeasureUnit


class RiskMeasure(__RiskMeasure):

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name or self.measure_type.name

    @property
    @do_not_serialise
    def pricing_context(self):
        from gs_quant.markets import PricingContext
        return PricingContext.current


class __RelativeRiskMeasure(RiskMeasure):

    def __init__(self,
                 to_market: Market,
                 asset_class: Union[AssetClass, str] = None,
                 measure_type: Union[RiskMeasureType, str] = None,
                 unit: Union[RiskMeasureUnit, str] = None,
                 value: Union[float, str] = None,
                 name: str = None):
        super().__init__(asset_class=asset_class, measure_type=measure_type, unit=unit, value=value, name=name)
        self.__to_market = to_market

    @property
    @do_not_serialise
    def pricing_context(self):
        from gs_quant.markets import PricingContext, RelativeMarket
        current = PricingContext.current
        return current.clone(market=RelativeMarket(from_market=current.market, to_market=self.__to_market))


class ParameterisedRiskMeasure(RiskMeasure):
    def __init__(self, name: str = None, asset_class: Union[AssetClass, str] = None,
                 measure_type: Union[RiskMeasureType, str] = None, unit: Union[RiskMeasureUnit, str] = None,
                 value: Union[float, str] = None, parameters: Base = None):
        super().__init__(asset_class=asset_class, measure_type=measure_type, unit=unit, value=value, name=name)
        if parameters:
            if getattr(parameters, "parameter_type", None):
                self.parameters = parameters
            else:
                raise TypeError(f"Unsupported parameter {parameters}")

    def __repr__(self):
        name = self.name or self.measure_type.name
        params = None
        if self.parameters:
            params = self.parameters.as_dict()
            params.pop('parameter_type', None)
            sorted_keys = sorted(params.keys(), key=lambda x: x.lower())
            params = ', '.join(
                [f'{k}:{params[k].value if isinstance(params[k], EnumBase) else params[k]}' for k in sorted_keys])
        return name + '(' + params + ')' if params else name

    def parameter_is_empty(self):
        return self.parameters is None


class RiskMeasureWithCurrencyParameter(ParameterisedRiskMeasure):
    @property
    def currency(self):
        return self.parameters.currency if self.parameters else None

    def __call__(self, currency: str = None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(currency, pd.DataFrame):
            return self

        clone = copy.copy(self)
        currency = clone.currency if currency is None else currency
        parameter = CurrencyParameter(value=currency)
        clone.parameters = parameter
        return clone


class RiskMeasureWithStringParameter(ParameterisedRiskMeasure):
    @property
    def value(self):
        return self.parameters.value if self.parameters else None

    def __call__(self, value: str = None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(value, pd.DataFrame):
            return self

        clone = copy.copy(self)
        parameter = StringParameter(value=value)
        clone.parameters = parameter
        return clone


class RiskMeasureWithListOfStringParameter(ParameterisedRiskMeasure):
    @property
    def values(self):
        return self.parameters.values if self.parameters else None

    def __call__(self, values: Iterable[str] = None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(values, pd.DataFrame):
            return self

        clone = copy.copy(self)
        parameter = ListOfStringParameter(values=values)
        clone.parameters = parameter
        return clone


class RiskMeasureWithListOfNumberParameter(ParameterisedRiskMeasure):
    @property
    def values(self):
        return self.parameters.values if self.parameters else None

    def __call__(self, values: Iterable[float] = None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(values, pd.DataFrame):
            return self

        clone = copy.copy(self)
        parameter = ListOfNumberParameter(values=values)
        clone.parameters = parameter
        return clone


class RiskMeasureWithMapParameter(ParameterisedRiskMeasure):
    @property
    def value(self):
        return self.parameters.value if self.parameters else None

    def __call__(self, value: dict = None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(value, pd.DataFrame):
            return self

        clone = copy.copy(self)
        parameter = MapParameter(value=value)
        clone.parameters = parameter
        return clone


class RiskMeasureWithFiniteDifferenceParameter(ParameterisedRiskMeasure):
    @property
    def currency(self):
        return self.parameters.currency if self.parameters else None

    @property
    def aggregation_level(self):
        return self.parameters.aggregation_level if self.parameters else None

    @property
    def local_curve(self):
        return self.parameters.local_curve if self.parameters else None

    @property
    def finite_difference_method(self):
        return self.parameters.finite_difference_method if self.parameters else None

    @property
    def mkt_marking_mode(self):
        return self.parameters.mkt_marking_mode if self.parameters else None

    @property
    def bump_size(self):
        return self.parameters.bump_size if self.parameters else None

    @property
    def scale_factor(self):
        return self.parameters.scale_factor if self.parameters else None

    def __call__(self, currency: str = None,
                 aggregation_level: Union[AggregationLevel, str] = None, local_curve: bool = None,
                 finite_difference_method: Union[FiniteDifferenceParameter, str] = None,
                 mkt_marking_mode: str = None, bump_size: float = None, scale_factor: float = None, name: str = None):
        # hack to prevent ParameterisedRiskMeasure input into pandas LocIndexer as a callable function that returns
        # output for indexing (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)
        if isinstance(currency, pd.DataFrame):
            return self

        clone = copy.copy(self)
        if name:
            clone.name = name

        aggregation_level = clone.aggregation_level if aggregation_level is None else aggregation_level
        currency = clone.currency if currency is None else currency
        local_curve = clone.local_curve if local_curve is None else local_curve
        bump_size = clone.bump_size if bump_size is None else bump_size
        finite_difference_method = clone.finite_difference_method if finite_difference_method is None \
            else finite_difference_method
        scale_factor = clone.scale_factor if scale_factor is None else scale_factor
        mkt_marking_mode = clone.mkt_marking_mode if mkt_marking_mode is None else mkt_marking_mode

        parameter = FiniteDifferenceParameter(aggregation_level=aggregation_level, currency=currency,
                                              local_curve=local_curve, bump_size=bump_size,
                                              finite_difference_method=finite_difference_method,
                                              scale_factor=scale_factor, mkt_marking_mode=mkt_marking_mode)
        clone.parameters = parameter
        return clone
