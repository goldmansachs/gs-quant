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


class FactorRiskTableMode(EnumBase, Enum):    
    
    """View the table data in tables endpoint as either Exposure or Z-Score data."""

    Exposure = 'Exposure'
    ZScore = 'ZScore'    


class OptimizationStatus(EnumBase, Enum):    
    
    """Optimization status."""

    Running = 'Running'
    Completed = 'Completed'    


class OptimizationType(EnumBase, Enum):    
    
    """Pretrade optimization algorithm type."""

    APEX = 'APEX'    


class OptimizationUrgency(EnumBase, Enum):    
    
    """Parameter which controls the urgency of executing the basket from very low to
       very high. Very High urgency tilts the schedule towards the benchmark,
       whereas Very Low would minimise cost, carrying a relatively higher risk
       to the benchmark."""

    VERY_LOW = 'VERY_LOW'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERY_HIGH = 'VERY_HIGH'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AdvCurveTick(Base):
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    value: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExecutionCostForHorizon(Base):
    minutes_expired: Optional[int] = field(default=None, metadata=field_metadata)
    execution_cost: Optional[float] = field(default=None, metadata=field_metadata)
    execution_cost_long: Optional[float] = field(default=None, metadata=field_metadata)
    execution_cost_short: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityBucket(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    net_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    gross_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    net_weight: Optional[float] = field(default=None, metadata=field_metadata)
    gross_weight: Optional[float] = field(default=None, metadata=field_metadata)
    transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    adv22_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    number_of_positions: Optional[float] = field(default=None, metadata=field_metadata)
    beta_adjusted_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    long_weight: Optional[float] = field(default=None, metadata=field_metadata)
    long_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    long_transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    long_marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    long_adv22_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    long_number_of_positions: Optional[float] = field(default=None, metadata=field_metadata)
    long_beta_adjusted_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    short_weight: Optional[float] = field(default=None, metadata=field_metadata)
    short_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    short_transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    short_marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    short_adv22_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    short_number_of_positions: Optional[float] = field(default=None, metadata=field_metadata)
    short_beta_adjusted_exposure: Optional[float] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityFactor(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    value: Optional[float] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquiditySummarySection(Base):
    adv10_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    adv22_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    adv5_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    annualized_risk: Optional[float] = field(default=None, metadata=field_metadata)
    annualized_tracking_error: Optional[float] = field(default=None, metadata=field_metadata)
    beta: Optional[float] = field(default=None, metadata=field_metadata)
    beta_adjusted_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    beta_adjusted_net_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    bid_ask_spread: Optional[float] = field(default=None, metadata=field_metadata)
    correlation: Optional[float] = field(default=None, metadata=field_metadata)
    daily_risk: Optional[float] = field(default=None, metadata=field_metadata)
    daily_tracking_error: Optional[float] = field(default=None, metadata=field_metadata)
    est1_day_complete_pct: Optional[float] = field(default=None, metadata=field_metadata)
    five_day_price_change_bps: Optional[float] = field(default=None, metadata=field_metadata)
    gross_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    market_cap: Optional[float] = field(default=None, metadata=field_metadata)
    minutes_to_trade100_pct: Optional[float] = field(default=None, metadata=field_metadata)
    net_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    number_of_positions: Optional[float] = field(default=None, metadata=field_metadata)
    percent_in_benchmark: Optional[object] = field(default=None, metadata=field_metadata)
    transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    weight_of_top_five_positions: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAssetAnalyticsDaily(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    trade_day_number: int = field(default=None, metadata=field_metadata)
    total_cost: float = field(default=None, metadata=field_metadata)
    total_variance_contribution: float = field(default=None, metadata=field_metadata)
    total_portfolio_risk_on_day: float = field(default=None, metadata=field_metadata)
    total_risk: float = field(default=None, metadata=field_metadata)
    cratos: float = field(default=None, metadata=field_metadata)
    adv: float = field(default=None, metadata=field_metadata)
    cluster_id: int = field(default=None, metadata=field_metadata)
    cluster_label: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAssetAnalyticsDayOne(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    auction_trade_percentage: float = field(default=None, metadata=field_metadata)
    auction_pov_percentage: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAssetAnalyticsIntraday(Base):
    period_number: int = field(default=None, metadata=field_metadata)
    trade_day_number: int = field(default=None, metadata=field_metadata)
    period_start_time: datetime.datetime = field(default=None, metadata=field_metadata)
    period_end_time: datetime.datetime = field(default=None, metadata=field_metadata)
    is_trading: bool = field(default=None, metadata=field_metadata)
    buy: float = field(default=None, metadata=field_metadata)
    sell: float = field(default=None, metadata=field_metadata)
    gross: float = field(default=None, metadata=field_metadata)
    net: float = field(default=None, metadata=field_metadata)
    trade_absolute: float = field(default=None, metadata=field_metadata)
    asset_id: str = field(default=None, metadata=field_metadata)
    volume: float = field(default=None, metadata=field_metadata)
    volatility: float = field(default=None, metadata=field_metadata)
    fx: float = field(default=None, metadata=field_metadata)
    price_local: float = field(default=None, metadata=field_metadata)
    currency: str = field(default=None, metadata=field_metadata)
    total_cost_spread: float = field(default=None, metadata=field_metadata)
    total_cost_volatility: float = field(default=None, metadata=field_metadata)
    total_cost_permanent: float = field(default=None, metadata=field_metadata)
    beta_historical: float = field(default=None, metadata=field_metadata)
    mcr: float = field(default=None, metadata=field_metadata)
    total_cost: float = field(default=None, metadata=field_metadata)
    adv_percentage: float = field(default=None, metadata=field_metadata)
    country: str = field(default=None, metadata=field_metadata)
    industry: str = field(default=None, metadata=field_metadata)
    sector: str = field(default=None, metadata=field_metadata)
    spread: float = field(default=None, metadata=field_metadata)
    region: str = field(default=None, metadata=field_metadata)
    region_minor: str = field(default=None, metadata=field_metadata)
    quantity: int = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationCloseAuctionAnalytics(Base):
    exchange_city: str = field(default=None, metadata=field_metadata)
    trade_absolute: float = field(default=None, metadata=field_metadata)
    trade_net: float = field(default=None, metadata=field_metadata)
    gross: float = field(default=None, metadata=field_metadata)
    net: float = field(default=None, metadata=field_metadata)
    auction_pov_percentage: float = field(default=None, metadata=field_metadata)
    close_auction_start_time: datetime.datetime = field(default=None, metadata=field_metadata)
    number_of_assets: int = field(default=None, metadata=field_metadata)
    close_auction_trade_percentage: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationClusterAnalytics(Base):
    cluster_id: int = field(default=None, metadata=field_metadata)
    cluster_label: str = field(default=None, metadata=field_metadata)
    gross: float = field(default=None, metadata=field_metadata)
    total_cost_bps: float = field(default=None, metadata=field_metadata)
    total_risk_bps: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationClusterAnalyticsIntradayItem(Base):
    cluster_id: int = field(default=None, metadata=field_metadata)
    cluster_label: str = field(default=None, metadata=field_metadata)
    adv_percentage: float = field(default=None, metadata=field_metadata)
    gross_percentage: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationEodCashPositionsItem(Base):
    trade_day_num: str = field(default=None, metadata=field_metadata)
    net: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationExcludedAsset(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    security_type: str = field(default=None, metadata=field_metadata)
    quantity: int = field(default=None, metadata=field_metadata)
    reason: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationFactorAnalyticsItem(Base):
    period_number: int = field(default=None, metadata=field_metadata)
    trade_day_number: int = field(default=None, metadata=field_metadata)
    period_start_time: datetime.datetime = field(default=None, metadata=field_metadata)
    period_end_time: datetime.datetime = field(default=None, metadata=field_metadata)
    factors: Tuple[DictBase, ...] = field(default=None, metadata=field_metadata)
    time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioAnalyticsDaily(Base):
    trade_day_number: int = field(default=None, metadata=field_metadata)
    estimated_cost_bps: float = field(default=None, metadata=field_metadata)
    completion_rate_percent: float = field(default=None, metadata=field_metadata)
    mean_expected_cost_versus_benchmark: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioAnalyticsIntraday(Base):
    period_number: int = field(default=None, metadata=field_metadata)
    trade_day_number: int = field(default=None, metadata=field_metadata)
    period_start_time: datetime.datetime = field(default=None, metadata=field_metadata)
    period_end_time: datetime.datetime = field(default=None, metadata=field_metadata)
    time: datetime.datetime = field(default=None, metadata=field_metadata)
    sell: float = field(default=None, metadata=field_metadata)
    buy: float = field(default=None, metadata=field_metadata)
    gross: float = field(default=None, metadata=field_metadata)
    net: float = field(default=None, metadata=field_metadata)
    trade_absolute: float = field(default=None, metadata=field_metadata)
    total_cost_spread: float = field(default=None, metadata=field_metadata)
    total_cost_volatility: float = field(default=None, metadata=field_metadata)
    total_cost_permanent: float = field(default=None, metadata=field_metadata)
    total_cost: float = field(default=None, metadata=field_metadata)
    adv_average_percentage: float = field(default=None, metadata=field_metadata)
    total_risk: float = field(default=None, metadata=field_metadata)
    factor_risk: float = field(default=None, metadata=field_metadata)
    specific_risk: float = field(default=None, metadata=field_metadata)
    diagonal_risk: float = field(default=None, metadata=field_metadata)
    total_risk_objective: float = field(default=None, metadata=field_metadata)
    factor_risk_objective: float = field(default=None, metadata=field_metadata)
    specific_risk_objective: float = field(default=None, metadata=field_metadata)
    diagonal_risk_objective: float = field(default=None, metadata=field_metadata)
    total_risk_bps: float = field(default=None, metadata=field_metadata)
    trade_percentage_cumulative_sum: float = field(default=None, metadata=field_metadata)
    net_period_percentage: float = field(default=None, metadata=field_metadata)
    total_cost_budget_percentage: float = field(default=None, metadata=field_metadata)
    total_risk_percentage: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioSummarySection(Base):
    position: float = field(default=None, metadata=field_metadata)
    number_of_assets: int = field(default=None, metadata=field_metadata)
    diagonal_risk: float = field(default=None, metadata=field_metadata)
    total_risk: float = field(default=None, metadata=field_metadata)
    factor_risk: float = field(default=None, metadata=field_metadata)
    specific_risk: float = field(default=None, metadata=field_metadata)
    historical_beta: float = field(default=None, metadata=field_metadata)
    spread: float = field(default=None, metadata=field_metadata)
    total_risk_bps: float = field(default=None, metadata=field_metadata)
    adv_average_percentage: float = field(default=None, metadata=field_metadata)
    adv_max_percentage: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationTradedPosition(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    quantity: int = field(default=None, metadata=field_metadata)
    position: int = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PRateForHorizon(Base):
    minutes_expired: Optional[int] = field(default=None, metadata=field_metadata)
    participation_rate: Optional[float] = field(default=None, metadata=field_metadata)
    participation_rate_long: Optional[float] = field(default=None, metadata=field_metadata)
    participation_rate_short: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskAtHorizon(Base):
    minutes_expired: Optional[int] = field(default=None, metadata=field_metadata)
    risk: Optional[int] = field(default=None, metadata=field_metadata)
    risk_long: Optional[float] = field(default=None, metadata=field_metadata)
    risk_short: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TradeCompleteAtHorizon(Base):
    minutes_expired: Optional[int] = field(default=None, metadata=field_metadata)
    positions_complete: Optional[int] = field(default=None, metadata=field_metadata)
    positions_complete_pct: Optional[float] = field(default=None, metadata=field_metadata)
    notional_complete_pct: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityConstituent(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    exchange: Optional[str] = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    gross_weight: Optional[float] = field(default=None, metadata=field_metadata)
    net_weight: Optional[float] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    gross_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    net_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    region: Optional[Region] = field(default=None, metadata=field_metadata)
    type_: Optional[AssetType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    market_cap_bucket: Optional[object] = field(default=None, metadata=field_metadata)
    est1_day_complete_pct: Optional[float] = field(default=None, metadata=field_metadata)
    in_benchmark: Optional[bool] = field(default=None, metadata=field_metadata)
    in_risk_model: Optional[bool] = field(default=None, metadata=field_metadata)
    in_cost_predict_model: Optional[bool] = field(default=None, metadata=field_metadata)
    beta: Optional[float] = field(default=None, metadata=field_metadata)
    daily_risk: Optional[float] = field(default=None, metadata=field_metadata)
    annualized_risk: Optional[float] = field(default=None, metadata=field_metadata)
    one_day_price_change_pct: Optional[float] = field(default=None, metadata=field_metadata)
    beta_adjusted_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    adv_bucket: Optional[object] = field(default=None, metadata=field_metadata)
    settlement_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityFactorCategory(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    sub_factors: Optional[Tuple[LiquidityFactor, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquiditySummary(Base):
    total: LiquiditySummarySection = field(default=None, metadata=field_metadata)
    long: Optional[LiquiditySummarySection] = field(default=None, metadata=field_metadata)
    short: Optional[LiquiditySummarySection] = field(default=None, metadata=field_metadata)
    long_vs_short: Optional[LiquiditySummarySection] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationClusterAnalyticsIntraday(Base):
    time: datetime.datetime = field(default=None, metadata=field_metadata)
    period_number: int = field(default=None, metadata=field_metadata)
    trade_day_number: int = field(default=None, metadata=field_metadata)
    clusters: Tuple[OptimizationClusterAnalyticsIntradayItem, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationEodCashPositions(Base):
    currency: str = field(default=None, metadata=field_metadata)
    positions: Tuple[OptimizationEodCashPositionsItem, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioCharacteristics(Base):
    sell: OptimizationPortfolioSummarySection = field(default=None, metadata=field_metadata)
    buy: OptimizationPortfolioSummarySection = field(default=None, metadata=field_metadata)
    net: OptimizationPortfolioSummarySection = field(default=None, metadata=field_metadata)
    gross: OptimizationPortfolioSummarySection = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityTableRow(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    adv22_day_pct: Optional[float] = field(default=None, metadata=field_metadata)
    shares: Optional[float] = field(default=None, metadata=field_metadata)
    net_weight: Optional[float] = field(default=None, metadata=field_metadata)
    gross_weight: Optional[float] = field(default=None, metadata=field_metadata)
    gross_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    net_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    one_day_price_change_pct: Optional[float] = field(default=None, metadata=field_metadata)
    normalized_performance: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityTimeSeriesItem(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    normalized_performance: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    annualized_return: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    annualized_correlation: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    annualized_volatility: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    annualized_sharp_ratio: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    annualized_tracking_error: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    max_drawdown: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    net_exposure: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    cumulative_pnl: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationFactorAnalyticsIntraday(Base):
    country: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    sector: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    domestic_china: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    market: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    currency: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    industry: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    risk: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    cluster_classification: Tuple[OptimizationFactorAnalyticsItem, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationTradeSchedule(Base):
    period_number: int = field(default=None, metadata=field_metadata)
    trade_day_number: int = field(default=None, metadata=field_metadata)
    period_start_time: datetime.datetime = field(default=None, metadata=field_metadata)
    period_end_time: datetime.datetime = field(default=None, metadata=field_metadata)
    traded_positions: Tuple[OptimizationTradedPosition, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityResponse(Base):
    as_of_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    risk_model: Optional[str] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    report: Optional[str] = field(default=None, metadata=field_metadata)
    summary: Optional[LiquiditySummary] = field(default=None, metadata=field_metadata)
    constituent_transaction_costs: Optional[Tuple[LiquidityConstituent, ...]] = field(default=None, metadata=field_metadata)
    constituents: Optional[Tuple[LiquidityConstituent, ...]] = field(default=None, metadata=field_metadata)
    largest_holdings_by_weight: Optional[Tuple[LiquidityTableRow, ...]] = field(default=None, metadata=field_metadata)
    least_liquid_holdings: Optional[Tuple[LiquidityTableRow, ...]] = field(default=None, metadata=field_metadata)
    adv_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    region_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    country_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    sector_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    industry_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    market_cap_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    currency_buckets: Optional[Tuple[LiquidityBucket, ...]] = field(default=None, metadata=field_metadata)
    execution_costs_with_different_time_horizons: Optional[Tuple[ExecutionCostForHorizon, ...]] = field(default=None, metadata=field_metadata)
    time_to_trade_with_different_participation_rates: Optional[Tuple[PRateForHorizon, ...]] = field(default=None, metadata=field_metadata)
    risk_over_time: Optional[Tuple[RiskAtHorizon, ...]] = field(default=None, metadata=field_metadata)
    trade_complete_percent_over_time: Optional[Tuple[TradeCompleteAtHorizon, ...]] = field(default=None, metadata=field_metadata)
    adv_percent_over_time: Optional[Tuple[AdvCurveTick, ...]] = field(default=None, metadata=field_metadata)
    risk_buckets: Optional[Tuple[LiquidityFactor, ...]] = field(default=None, metadata=field_metadata)
    factor_risk_buckets: Optional[Tuple[LiquidityFactorCategory, ...]] = field(default=None, metadata=field_metadata)
    exposure_buckets: Optional[Tuple[LiquidityFactor, ...]] = field(default=None, metadata=field_metadata)
    factor_exposure_buckets: Optional[Tuple[LiquidityFactorCategory, ...]] = field(default=None, metadata=field_metadata)
    timeseries_data: Optional[Tuple[LiquidityTimeSeriesItem, ...]] = field(default=None, metadata=field_metadata)
    assets_not_in_risk_model: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    assets_not_in_cost_predict_model: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    assets_without_compositions: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    error_message: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAnalytics(Base):
    portfolio_characteristics: OptimizationPortfolioCharacteristics = field(default=None, metadata=field_metadata)
    asset_analytics_daily: Tuple[OptimizationAssetAnalyticsDaily, ...] = field(default=None, metadata=field_metadata)
    portfolio_analytics_daily: Tuple[OptimizationPortfolioAnalyticsDaily, ...] = field(default=None, metadata=field_metadata)
    assets_excluded: Tuple[OptimizationExcludedAsset, ...] = field(default=None, metadata=field_metadata)
    constraints_consultations: Tuple[DictBase, ...] = field(default=None, metadata=field_metadata)
    factor_analytics_intraday: OptimizationFactorAnalyticsIntraday = field(default=None, metadata=field_metadata)
    asset_analytics_intraday: Tuple[OptimizationAssetAnalyticsIntraday, ...] = field(default=None, metadata=field_metadata)
    portfolio_analytics_intraday: Tuple[OptimizationPortfolioAnalyticsIntraday, ...] = field(default=None, metadata=field_metadata)
    cluster_analytics_intraday: Tuple[OptimizationClusterAnalyticsIntraday, ...] = field(default=None, metadata=field_metadata)
    cluster_analytics: Tuple[OptimizationClusterAnalytics, ...] = field(default=None, metadata=field_metadata)
    eod_cash_positions: Tuple[OptimizationEodCashPositions, ...] = field(default=None, metadata=field_metadata)
    asset_analytics_day_one: Optional[Tuple[OptimizationAssetAnalyticsDayOne, ...]] = field(default=None, metadata=field_metadata)
    close_auction_analytics: Optional[Tuple[OptimizationCloseAuctionAnalytics, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationResult(Base):
    created_by_id: str = field(default=None, metadata=field_metadata)
    created_time: datetime.datetime = field(default=None, metadata=field_metadata)
    entitlements: Entitlements = field(default=None, metadata=field_metadata)
    entitlement_exclusions: EntitlementExclusions = field(default=None, metadata=field_metadata)
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    last_updated_by_id: str = field(default=None, metadata=field_metadata)
    last_updated_time: datetime.datetime = field(default=None, metadata=field_metadata)
    owner_id: str = field(default=None, metadata=field_metadata)
    analytics: OptimizationAnalytics = field(default=None, metadata=field_metadata)
    status: OptimizationStatus = field(default=None, metadata=field_metadata)
    trade_schedule: Optional[Tuple[OptimizationTradeSchedule, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationRequest(Base):
    positions: Tuple[Position, ...] = field(default=None, metadata=field_metadata)
    execution_start_time: datetime.datetime = field(default=None, metadata=field_metadata)
    execution_end_time: datetime.datetime = field(default=None, metadata=field_metadata)
    parameters: DictBase = field(default=None, metadata=field_metadata)
    type_: OptimizationType = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    wait_for_results: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
