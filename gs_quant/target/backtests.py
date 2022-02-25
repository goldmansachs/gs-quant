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


class BacktestTradingQuantityType(EnumBase, Enum):    
    
    """The trading quantity unit of a backtest strategy"""

    notional = 'notional'
    quantity = 'quantity'
    vega = 'vega'
    gamma = 'gamma'
    NAV = 'NAV'    


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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestComparison(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    correlation: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRebalanceParameters(Base):
    frequency_period: Optional[str] = None
    frequency: Optional[int] = None
    day_of_week: Optional[str] = None
    day_of_month: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestSignalSeriesItem(Base):
    date: Optional[datetime.date] = None
    value: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BaseIndexRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BuySellRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedgeParameters(Base):
    frequency: str = None
    delta_type: Optional[str] = 'BlackScholes'
    fixing_time: Optional[str] = None
    notional: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedgingParameters(Base):
    enabled: bool = None
    frequency: str = None
    fixing_time: str = None
    notional_percentage: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaUnderlier(Base):
    asset_id: str = None
    month_add: Optional[float] = None
    valid_months: Optional[Tuple[str, ...]] = None
    is_included: Optional[bool] = None
    weight_scale: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaUnderlierRefData(Base):
    asset_id: Optional[str] = None
    valid_months: Optional[Tuple[str, ...]] = None
    current: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityCorrelation(Base):
    primary_id: Optional[str] = None
    secondary_id: Optional[str] = None
    correlation: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExpirationRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FixingTimeRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FrequencyRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HistoricalUnderlier(Base):
    asset_id: str = None
    weight: Optional[float] = None
    date: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LookBackPeriodRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class NotionalPercentageRefData(Base):
    default: Optional[float] = None
    min_: Optional[float] = field(default=None, metadata=config(field_name='min'))
    max_: Optional[float] = field(default=None, metadata=config(field_name='max'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptionStrikeTypeRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptionTypeRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScalingMethodRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class StrikeRefData(Base):
    default: Optional[float] = None
    min_: Optional[float] = field(default=None, metadata=config(field_name='min'))
    max_: Optional[float] = field(default=None, metadata=config(field_name='max'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TradeInMethodRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TradeInTimeRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityWeightedWeightingModifier(Base):
    name: Optional[str] = 'Volatility Weighted'
    em_aalpha: Optional[float] = field(default=None, metadata=config(field_name='EMAalpha'))
    look_back_period: Optional[str] = None
    use_log_return: Optional[bool] = False


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityWeightedWeightingModifierRefData(Base):
    em_aalpha: Optional[DictBase] = field(default=None, metadata=config(field_name='EMAalpha'))
    look_back_period: Optional[DictBase] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestStrategyUnderlierHedge(Base):
    risk_details: Optional[DeltaHedgeParameters] = None
    quantity_percentage: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestTradingParameters(Base):
    quantity_type: Optional[BacktestTradingQuantityType] = None
    quantity: Optional[float] = None
    trade_in_method: Optional[str] = None
    roll_frequency: Optional[str] = None
    roll_date_mode: Optional[str] = None
    scaling_method: Optional[str] = None
    trade_in_signals: Optional[Tuple[BacktestSignalSeriesItem, ...]] = None
    trade_out_signals: Optional[Tuple[BacktestSignalSeriesItem, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasketBacktestParameters(Base):
    underliers: Tuple[Union[float, str], ...] = None
    rebalance_parameters: Optional[BacktestRebalanceParameters] = None
    weighting_modifiers: Optional[Tuple[VolatilityWeightedWeightingModifier, ...]] = None
    weighting_strategy: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CurrencyRefData(Base):
    default: Optional[Currency] = None
    enum: Optional[Tuple[Currency, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedgingRefData(Base):
    fixing_time: Optional[FixingTimeRefData] = None
    frequency: Optional[FrequencyRefData] = None
    notional_percentage: Optional[NotionalPercentageRefData] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaBacktestParameters(Base):
    underliers: Tuple[EnhancedBetaUnderlier, ...] = None
    roll_start: float = None
    roll_end: float = None
    base_index: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectBacktestParameters(Base):
    max_leverage: float = None
    underliers: Tuple[HistoricalUnderlier, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptionBacktestUnderlier(Base):
    buy_sell: str = None
    expiration: str = None
    option_type: str = None
    option_strike_type: str = None
    strike: float = None
    underlying_asset_id: str = None
    notional_percentage: Optional[float] = None
    delta_hedging: Optional[DeltaHedgingParameters] = None
    trade_in_time: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceRange(Base):
    horizon: Optional[str] = None
    stats: Optional[PerformanceStats] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UnderlyingAssetIdDataRefData(Base):
    asset_id: Optional[str] = None
    fixing_time: Optional[FixingTimeRefData] = None
    frequency: Optional[FrequencyRefData] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestPerformanceDecomposition(Base):
    name: Optional[str] = None
    performance: Optional[Tuple[FieldValueMap, ...]] = None
    stats: Optional[PerformanceStats] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRisk(Base):
    name: Optional[str] = None
    timeseries: Optional[Tuple[FieldValueMap, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRiskPosition(Base):
    instrument: DictBase = None
    quantity: Optional[float] = None
    market_model: Optional[EquityMarketModel] = None
    expiry_date_mode: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestStrategyUnderlier(Base):
    instrument: DictBase = None
    market_model: str = None
    notional_percentage: Optional[float] = None
    expiry_date_mode: Optional[str] = None
    name: Optional[str] = None
    hedge: Optional[BacktestStrategyUnderlierHedge] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasketBacktestRefData(Base):
    currency: Optional[CurrencyRefData] = None
    look_back_period: Optional[LookBackPeriodRefData] = None
    weighting_strategy: Optional[DictBase] = None
    weighting_modifiers: Optional[DictBase] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ComparisonBacktestResult(Base):
    stats: Optional[PerformanceStats] = None
    performance: Optional[Tuple[FieldValueMap, ...]] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EnhancedBetaRefData(Base):
    look_back_period: Optional[LookBackPeriodRefData] = None
    currency: Optional[CurrencyRefData] = None
    base_index: Optional[BaseIndexRefData] = None
    MASJ8W49Y02X9CGS: Optional[DictBase] = None
    MAAHST8JED9B607H: Optional[DictBase] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UnderlyingAssetIdRefData(Base):
    default: Optional[str] = None
    enum: Optional[Tuple[str, ...]] = None
    data: Optional[Tuple[UnderlyingAssetIdDataRefData, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityBacktestParameters(Base):
    underliers: Tuple[OptionBacktestUnderlier, ...] = None
    trade_in_method: Optional[str] = None
    scaling_method: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestResult(Base):
    backtest_id: Optional[str] = None
    performance: Optional[Tuple[FieldValueMap, ...]] = None
    portfolio: Optional[Tuple[FieldValueMap, ...]] = None
    stats: Optional[PerformanceStats] = None
    performance_decompositions: Optional[Tuple[BacktestPerformanceDecomposition, ...]] = None
    risks: Optional[Tuple[BacktestRisk, ...]] = None
    history: Optional[Tuple[PerformanceRange, ...]] = None
    underlier_correlation: Optional[Tuple[EntityCorrelation, ...]] = None
    comparisons: Optional[Tuple[BacktestComparison, ...]] = None
    backtest_version: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRiskRequest(Base):
    positions: Tuple[BacktestRiskPosition, ...] = None
    measures: Tuple[BacktestRiskMeasureType, ...] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolBacktestRefData(Base):
    buy_sell: Optional[BuySellRefData] = None
    currency: Optional[CurrencyRefData] = None
    delta_hedging: Optional[DeltaHedgingRefData] = None
    delta_strike: Optional[StrikeRefData] = None
    notional_percentage: Optional[NotionalPercentageRefData] = None
    expiration: Optional[ExpirationRefData] = None
    look_back_period: Optional[LookBackPeriodRefData] = None
    option_type: Optional[OptionTypeRefData] = None
    option_strike_type: Optional[OptionStrikeTypeRefData] = None
    relative_strike: Optional[StrikeRefData] = None
    strike: Optional[StrikeRefData] = None
    scaling_method: Optional[ScalingMethodRefData] = None
    underlying_asset_id: Optional[UnderlyingAssetIdRefData] = None
    trade_in_method: Optional[TradeInMethodRefData] = None
    trade_in_time: Optional[TradeInTimeRefData] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VolatilityFlowBacktestParameters(Base):
    trading_parameters: BacktestTradingParameters = None
    index_initial_value: float = None
    underliers: Optional[Tuple[BacktestStrategyUnderlier, ...]] = None
    measures: Optional[Tuple[FlowVolBacktestMeasure, ...]] = ('ALL MEASURES',)


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Backtest(Base):
    name: str = None
    type_: BacktestType = field(default=None, metadata=config(field_name='type'))
    asset_class: AssetClass = None
    cost_netting: Optional[bool] = False
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    currency: Optional[Currency] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    mq_symbol: Optional[str] = None
    owner_id: Optional[str] = None
    report_ids: Optional[Tuple[str, ...]] = None
    parameters: Optional[DictBase] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    version: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BacktestRefData(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    volatility: Optional[DictBase] = None
    enhanced_beta: Optional[EnhancedBetaRefData] = field(default=None, metadata=config(field_name='enhanced_beta'))
    basket: Optional[BasketBacktestRefData] = None
    owner_id: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
