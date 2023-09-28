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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from enum import Enum


class BacktestRiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Price = 'Price'
    Delta = 'Delta'
    Gamma = 'Gamma'
    Vega = 'Vega'
    Forward = 'Forward'
    Implied_Volatility = 'Implied Volatility'
    Fair_Variance = 'Fair Variance'
    Strike_Level = 'Strike Level'
    Spot = 'Spot'
    Price_ATMS = 'Price ATMS'
    Price_ATMF_Volatility = 'Price ATMF Volatility'    


class BacktestTradingQuantityType(EnumBase, Enum):    
    
    """The trading quantity unit of a backtest strategy"""

    notional = 'notional'
    quantity = 'quantity'
    vega = 'vega'
    gamma = 'gamma'
    NAV = 'NAV'
    premium = 'premium'
    vegaNotional = 'vegaNotional'    


class BacktestType(EnumBase, Enum):    
    
    """Backtest type differentiates the backtest type."""

    Basket = 'Basket'
    Volatility = 'Volatility'
    Volatility_Flow = 'Volatility Flow'
    Enhanced_Beta = 'Enhanced Beta'
    ISelect = 'ISelect'    


class EquityMarketModel(EnumBase, Enum):    
    
    """Market model for pricing"""

    SFK = 'SFK'
    SD = 'SD'
    SVR = 'SVR'    


class FlowVolBacktestMeasure(EnumBase, Enum):    
    
    """Metric which can be calculated using Flow Vol. Backtester"""

    ALL_MEASURES = 'ALL MEASURES'
    PNL_spot = 'PNL_spot'
    PNL_vol = 'PNL_vol'
    PNL_carry = 'PNL_carry'
    PNL_delta = 'PNL_delta'
    PNL_gamma = 'PNL_gamma'
    PNL_higher_order_spot = 'PNL_higher_order_spot'
    PNL_higher_order_vol = 'PNL_higher_order_vol'
    PNL_theta = 'PNL_theta'
    Total = 'Total'
    transaction_costs = 'transaction_costs'
    PNL_unexplained = 'PNL_unexplained'
    PNL_vega = 'PNL_vega'
    PNL = 'PNL'
    delta = 'delta'
    gamma = 'gamma'
    vega = 'vega'
    portfolio = 'portfolio'
    NAV = 'NAV'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestComparison(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    correlation: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRebalanceParameters(Base):
    frequency_period: Optional[str] = field(default=None, metadata=field_metadata)
    frequency: Optional[int] = field(default=None, metadata=field_metadata)
    day_of_week: Optional[str] = field(default=None, metadata=field_metadata)
    day_of_month: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestSignalSeriesItem(Base):
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    value: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BaseIndexRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BuySellRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedgeParameters(Base):
    frequency: str = field(default=None, metadata=field_metadata)
    fixing_time: Optional[str] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    delta_type: Optional[str] = field(init=False, default='BlackScholes', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedgingParameters(Base):
    enabled: bool = field(default=None, metadata=field_metadata)
    frequency: str = field(default=None, metadata=field_metadata)
    fixing_time: str = field(default=None, metadata=field_metadata)
    notional_percentage: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaUnderlier(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    month_add: Optional[float] = field(default=None, metadata=field_metadata)
    valid_months: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    is_included: Optional[bool] = field(default=None, metadata=field_metadata)
    weight_scale: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaUnderlierRefData(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    valid_months: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    current: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityCorrelation(Base):
    primary_id: Optional[str] = field(default=None, metadata=field_metadata)
    secondary_id: Optional[str] = field(default=None, metadata=field_metadata)
    correlation: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExpirationRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FixingTimeRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FrequencyRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HistoricalUnderlier(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    weight: Optional[float] = field(default=None, metadata=field_metadata)
    date: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LookBackPeriodRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class NotionalPercentageRefData(Base):
    default: Optional[float] = field(default=None, metadata=field_metadata)
    min_: Optional[float] = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    max_: Optional[float] = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptionStrikeTypeRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptionTypeRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScalingMethodRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class StrikeRefData(Base):
    default: Optional[float] = field(default=None, metadata=field_metadata)
    min_: Optional[float] = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    max_: Optional[float] = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TradeInMethodRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TradeInTimeRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityWeightedWeightingModifier(Base):
    em_aalpha: Optional[float] = field(default=None, metadata=config(field_name='EMAalpha', exclude=exclude_none))
    look_back_period: Optional[str] = field(default=None, metadata=field_metadata)
    use_log_return: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(init=False, default='Volatility Weighted', metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityWeightedWeightingModifierRefData(Base):
    em_aalpha: Optional[DictBase] = field(default=None, metadata=config(field_name='EMAalpha', exclude=exclude_none))
    look_back_period: Optional[DictBase] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestStrategyUnderlierHedge(Base):
    risk_details: Optional[DeltaHedgeParameters] = field(default=None, metadata=field_metadata)
    quantity_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestTradingParameters(Base):
    quantity_type: Optional[BacktestTradingQuantityType] = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    trade_in_method: Optional[str] = field(default=None, metadata=field_metadata)
    roll_frequency: Optional[str] = field(default=None, metadata=field_metadata)
    roll_date_mode: Optional[str] = field(default=None, metadata=field_metadata)
    scaling_method: Optional[str] = field(default=None, metadata=field_metadata)
    trade_in_signals: Optional[Tuple[BacktestSignalSeriesItem, ...]] = field(default=None, metadata=field_metadata)
    trade_out_signals: Optional[Tuple[BacktestSignalSeriesItem, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasketBacktestParameters(Base):
    underliers: Tuple[Union[float, str], ...] = field(default=None, metadata=field_metadata)
    rebalance_parameters: Optional[BacktestRebalanceParameters] = field(default=None, metadata=field_metadata)
    weighting_modifiers: Optional[Tuple[VolatilityWeightedWeightingModifier, ...]] = field(default=None, metadata=field_metadata)
    weighting_strategy: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CurrencyRefData(Base):
    default: Optional[Currency] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[Currency, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedgingRefData(Base):
    fixing_time: Optional[FixingTimeRefData] = field(default=None, metadata=field_metadata)
    frequency: Optional[FrequencyRefData] = field(default=None, metadata=field_metadata)
    notional_percentage: Optional[NotionalPercentageRefData] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaBacktestParameters(Base):
    underliers: Tuple[EnhancedBetaUnderlier, ...] = field(default=None, metadata=field_metadata)
    roll_start: float = field(default=None, metadata=field_metadata)
    roll_end: float = field(default=None, metadata=field_metadata)
    base_index: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectBacktestParameters(Base):
    max_leverage: float = field(default=None, metadata=field_metadata)
    underliers: Tuple[HistoricalUnderlier, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptionBacktestUnderlier(Base):
    buy_sell: str = field(default=None, metadata=field_metadata)
    expiration: str = field(default=None, metadata=field_metadata)
    option_type: str = field(default=None, metadata=field_metadata)
    option_strike_type: str = field(default=None, metadata=field_metadata)
    strike: float = field(default=None, metadata=field_metadata)
    underlying_asset_id: str = field(default=None, metadata=field_metadata)
    notional_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    delta_hedging: Optional[DeltaHedgingParameters] = field(default=None, metadata=field_metadata)
    trade_in_time: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceRange(Base):
    horizon: Optional[str] = field(default=None, metadata=field_metadata)
    stats: Optional[PerformanceStats] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UnderlyingAssetIdDataRefData(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    fixing_time: Optional[FixingTimeRefData] = field(default=None, metadata=field_metadata)
    frequency: Optional[FrequencyRefData] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestPerformanceDecomposition(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    performance: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    stats: Optional[PerformanceStats] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRisk(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    timeseries: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRiskPosition(Base):
    instrument: DictBase = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    market_model: Optional[EquityMarketModel] = field(default=None, metadata=field_metadata)
    expiry_date_mode: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestStrategyUnderlier(Base):
    instrument: DictBase = field(default=None, metadata=field_metadata)
    market_model: EquityMarketModel = field(default=None, metadata=field_metadata)
    notional_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    expiry_date_mode: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    hedge: Optional[BacktestStrategyUnderlierHedge] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasketBacktestRefData(Base):
    currency: Optional[CurrencyRefData] = field(default=None, metadata=field_metadata)
    look_back_period: Optional[LookBackPeriodRefData] = field(default=None, metadata=field_metadata)
    weighting_strategy: Optional[DictBase] = field(default=None, metadata=field_metadata)
    weighting_modifiers: Optional[DictBase] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ComparisonBacktestResult(Base):
    stats: Optional[PerformanceStats] = field(default=None, metadata=field_metadata)
    performance: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaRefData(Base):
    look_back_period: Optional[LookBackPeriodRefData] = field(default=None, metadata=field_metadata)
    currency: Optional[CurrencyRefData] = field(default=None, metadata=field_metadata)
    base_index: Optional[BaseIndexRefData] = field(default=None, metadata=field_metadata)
    MASJ8W49Y02X9CGS: Optional[DictBase] = field(default=None, metadata=field_metadata)
    MAAHST8JED9B607H: Optional[DictBase] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UnderlyingAssetIdRefData(Base):
    default: Optional[str] = field(default=None, metadata=field_metadata)
    enum: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[UnderlyingAssetIdDataRefData, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityBacktestParameters(Base):
    underliers: Tuple[OptionBacktestUnderlier, ...] = field(default=None, metadata=field_metadata)
    trade_in_method: Optional[str] = field(default=None, metadata=field_metadata)
    scaling_method: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestResult(Base):
    backtest_id: Optional[str] = field(default=None, metadata=field_metadata)
    performance: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    portfolio: Optional[Tuple[FieldValueMap, ...]] = field(default=None, metadata=field_metadata)
    stats: Optional[PerformanceStats] = field(default=None, metadata=field_metadata)
    performance_decompositions: Optional[Tuple[BacktestPerformanceDecomposition, ...]] = field(default=None, metadata=field_metadata)
    risks: Optional[Tuple[BacktestRisk, ...]] = field(default=None, metadata=field_metadata)
    history: Optional[Tuple[PerformanceRange, ...]] = field(default=None, metadata=field_metadata)
    underlier_correlation: Optional[Tuple[EntityCorrelation, ...]] = field(default=None, metadata=field_metadata)
    comparisons: Optional[Tuple[BacktestComparison, ...]] = field(default=None, metadata=field_metadata)
    backtest_version: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRiskRequest(Base):
    positions: Tuple[BacktestRiskPosition, ...] = field(default=None, metadata=field_metadata)
    measures: Tuple[BacktestRiskMeasureType, ...] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolBacktestRefData(Base):
    buy_sell: Optional[BuySellRefData] = field(default=None, metadata=field_metadata)
    currency: Optional[CurrencyRefData] = field(default=None, metadata=field_metadata)
    delta_hedging: Optional[DeltaHedgingRefData] = field(default=None, metadata=field_metadata)
    delta_strike: Optional[StrikeRefData] = field(default=None, metadata=field_metadata)
    notional_percentage: Optional[NotionalPercentageRefData] = field(default=None, metadata=field_metadata)
    expiration: Optional[ExpirationRefData] = field(default=None, metadata=field_metadata)
    look_back_period: Optional[LookBackPeriodRefData] = field(default=None, metadata=field_metadata)
    option_type: Optional[OptionTypeRefData] = field(default=None, metadata=field_metadata)
    option_strike_type: Optional[OptionStrikeTypeRefData] = field(default=None, metadata=field_metadata)
    relative_strike: Optional[StrikeRefData] = field(default=None, metadata=field_metadata)
    strike: Optional[StrikeRefData] = field(default=None, metadata=field_metadata)
    scaling_method: Optional[ScalingMethodRefData] = field(default=None, metadata=field_metadata)
    underlying_asset_id: Optional[UnderlyingAssetIdRefData] = field(default=None, metadata=field_metadata)
    trade_in_method: Optional[TradeInMethodRefData] = field(default=None, metadata=field_metadata)
    trade_in_time: Optional[TradeInTimeRefData] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityFlowBacktestParameters(Base):
    trading_parameters: BacktestTradingParameters = field(default=None, metadata=field_metadata)
    index_initial_value: float = field(default=None, metadata=field_metadata)
    underliers: Optional[Tuple[BacktestStrategyUnderlier, ...]] = field(default=None, metadata=field_metadata)
    measures: Optional[Tuple[FlowVolBacktestMeasure, ...]] = field(default=('ALL MEASURES',), metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Backtest(Base):
    name: str = field(default=None, metadata=field_metadata)
    type_: BacktestType = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    asset_class: AssetClass = field(default=None, metadata=field_metadata)
    cost_netting: Optional[bool] = field(default=False, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    mq_symbol: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    report_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    parameters: Optional[DictBase] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    version: Optional[float] = field(default=None, metadata=field_metadata)
    cash_accrual: Optional[bool] = field(default=True, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRefData(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    volatility: Optional[DictBase] = field(default=None, metadata=field_metadata)
    enhanced_beta: Optional[EnhancedBetaRefData] = field(default=None, metadata=config(field_name='enhanced_beta', exclude=exclude_none))
    basket: Optional[BasketBacktestRefData] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
