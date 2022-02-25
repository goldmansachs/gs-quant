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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AdvCurveTick(Base):
    date: Optional[datetime.date] = None
    value: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ExecutionCostForHorizon(Base):
    minutes_expired: Optional[int] = None
    execution_cost: Optional[float] = None
    execution_cost_long: Optional[float] = None
    execution_cost_short: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityBucket(Base):
    name: Optional[str] = None
    description: Optional[str] = None
    net_exposure: Optional[float] = None
    gross_exposure: Optional[float] = None
    net_weight: Optional[float] = None
    gross_weight: Optional[float] = None
    transaction_cost: Optional[float] = None
    marginal_cost: Optional[float] = None
    adv22_day_pct: Optional[float] = None
    number_of_positions: Optional[float] = None
    beta_adjusted_exposure: Optional[float] = None
    long_weight: Optional[float] = None
    long_exposure: Optional[float] = None
    long_transaction_cost: Optional[float] = None
    long_marginal_cost: Optional[float] = None
    long_adv22_day_pct: Optional[float] = None
    long_number_of_positions: Optional[float] = None
    long_beta_adjusted_exposure: Optional[float] = None
    short_weight: Optional[float] = None
    short_exposure: Optional[float] = None
    short_transaction_cost: Optional[float] = None
    short_marginal_cost: Optional[float] = None
    short_adv22_day_pct: Optional[float] = None
    short_number_of_positions: Optional[float] = None
    short_beta_adjusted_exposure: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityFactor(Base):
    name: Optional[str] = None
    value: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquiditySummarySection(Base):
    adv10_day_pct: Optional[float] = None
    adv22_day_pct: Optional[float] = None
    adv5_day_pct: Optional[float] = None
    annualized_risk: Optional[float] = None
    annualized_tracking_error: Optional[float] = None
    beta: Optional[float] = None
    beta_adjusted_exposure: Optional[float] = None
    beta_adjusted_net_exposure: Optional[float] = None
    bid_ask_spread: Optional[float] = None
    correlation: Optional[float] = None
    daily_risk: Optional[float] = None
    daily_tracking_error: Optional[float] = None
    est1_day_complete_pct: Optional[float] = None
    five_day_price_change_bps: Optional[float] = None
    gross_exposure: Optional[float] = None
    marginal_cost: Optional[float] = None
    market_cap: Optional[float] = None
    minutes_to_trade100_pct: Optional[float] = None
    net_exposure: Optional[float] = None
    number_of_positions: Optional[float] = None
    percent_in_benchmark: Optional[object] = None
    transaction_cost: Optional[float] = None
    weight_of_top_five_positions: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAssetAnalyticsDaily(Base):
    asset_id: str = None
    trade_day_number: int = None
    total_cost: float = None
    total_variance_contribution: float = None
    total_portfolio_risk_on_day: float = None
    total_risk: float = None
    cratos: float = None
    adv: float = None
    cluster_id: int = None
    cluster_label: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAssetAnalyticsDayOne(Base):
    asset_id: str = None
    auction_trade_percentage: float = None
    auction_pov_percentage: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAssetAnalyticsIntraday(Base):
    period_number: int = None
    trade_day_number: int = None
    period_start_time: datetime.datetime = None
    period_end_time: datetime.datetime = None
    is_trading: bool = None
    buy: float = None
    sell: float = None
    gross: float = None
    net: float = None
    trade_absolute: float = None
    asset_id: str = None
    volume: float = None
    volatility: float = None
    fx: float = None
    price_local: float = None
    currency: str = None
    total_cost_spread: float = None
    total_cost_volatility: float = None
    total_cost_permanent: float = None
    beta_historical: float = None
    mcr: float = None
    total_cost: float = None
    adv_percentage: float = None
    country: str = None
    industry: str = None
    sector: str = None
    spread: float = None
    region: str = None
    region_minor: str = None
    quantity: int = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationCloseAuctionAnalytics(Base):
    exchange_city: str = None
    trade_absolute: float = None
    trade_net: float = None
    gross: float = None
    net: float = None
    auction_pov_percentage: float = None
    close_auction_start_time: datetime.datetime = None
    number_of_assets: int = None
    close_auction_trade_percentage: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationClusterAnalytics(Base):
    cluster_id: int = None
    cluster_label: str = None
    gross: float = None
    total_cost_bps: float = None
    total_risk_bps: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationClusterAnalyticsIntradayItem(Base):
    cluster_id: int = None
    cluster_label: str = None
    adv_percentage: float = None
    gross_percentage: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationEodCashPositionsItem(Base):
    trade_day_num: str = None
    net: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationExcludedAsset(Base):
    asset_id: str = None
    security_type: str = None
    quantity: int = None
    reason: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationFactorAnalyticsItem(Base):
    period_number: int = None
    trade_day_number: int = None
    period_start_time: datetime.datetime = None
    period_end_time: datetime.datetime = None
    factors: Tuple[DictBase, ...] = None
    time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioAnalyticsDaily(Base):
    trade_day_number: int = None
    estimated_cost_bps: float = None
    completion_rate_percent: float = None
    mean_expected_cost_versus_benchmark: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioAnalyticsIntraday(Base):
    period_number: int = None
    trade_day_number: int = None
    period_start_time: datetime.datetime = None
    period_end_time: datetime.datetime = None
    time: datetime.datetime = None
    sell: float = None
    buy: float = None
    gross: float = None
    net: float = None
    trade_absolute: float = None
    total_cost_spread: float = None
    total_cost_volatility: float = None
    total_cost_permanent: float = None
    total_cost: float = None
    adv_average_percentage: float = None
    total_risk: float = None
    factor_risk: float = None
    specific_risk: float = None
    diagonal_risk: float = None
    total_risk_objective: float = None
    factor_risk_objective: float = None
    specific_risk_objective: float = None
    diagonal_risk_objective: float = None
    total_risk_bps: float = None
    trade_percentage_cumulative_sum: float = None
    net_period_percentage: float = None
    total_cost_budget_percentage: float = None
    total_risk_percentage: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioSummarySection(Base):
    position: float = None
    number_of_assets: int = None
    diagonal_risk: float = None
    total_risk: float = None
    factor_risk: float = None
    specific_risk: float = None
    historical_beta: float = None
    spread: float = None
    total_risk_bps: float = None
    adv_average_percentage: float = None
    adv_max_percentage: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationTradedPosition(Base):
    asset_id: str = None
    quantity: int = None
    position: int = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PRateForHorizon(Base):
    minutes_expired: Optional[int] = None
    participation_rate: Optional[float] = None
    participation_rate_long: Optional[float] = None
    participation_rate_short: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskAtHorizon(Base):
    minutes_expired: Optional[int] = None
    risk: Optional[int] = None
    risk_long: Optional[float] = None
    risk_short: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TradeCompleteAtHorizon(Base):
    minutes_expired: Optional[int] = None
    positions_complete: Optional[int] = None
    positions_complete_pct: Optional[float] = None
    notional_complete_pct: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityConstituent(Base):
    asset_id: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[str] = None
    quantity: Optional[float] = None
    gross_weight: Optional[float] = None
    net_weight: Optional[float] = None
    currency: Optional[Currency] = None
    gross_exposure: Optional[float] = None
    net_exposure: Optional[float] = None
    transaction_cost: Optional[float] = None
    marginal_cost: Optional[float] = None
    country: Optional[str] = None
    region: Optional[Region] = None
    type_: Optional[AssetType] = field(default=None, metadata=config(field_name='type'))
    market_cap_bucket: Optional[object] = None
    est1_day_complete_pct: Optional[float] = None
    in_benchmark: Optional[bool] = None
    in_risk_model: Optional[bool] = None
    in_cost_predict_model: Optional[bool] = None
    beta: Optional[float] = None
    daily_risk: Optional[float] = None
    annualized_risk: Optional[float] = None
    one_day_price_change_pct: Optional[float] = None
    beta_adjusted_exposure: Optional[float] = None
    adv_bucket: Optional[object] = None
    settlement_date: Optional[datetime.date] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityFactorCategory(Base):
    name: Optional[str] = None
    sub_factors: Optional[Tuple[LiquidityFactor, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquiditySummary(Base):
    total: LiquiditySummarySection = None
    long: Optional[LiquiditySummarySection] = None
    short: Optional[LiquiditySummarySection] = None
    long_vs_short: Optional[LiquiditySummarySection] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationClusterAnalyticsIntraday(Base):
    time: datetime.datetime = None
    period_number: int = None
    trade_day_number: int = None
    clusters: Tuple[OptimizationClusterAnalyticsIntradayItem, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationEodCashPositions(Base):
    currency: str = None
    positions: Tuple[OptimizationEodCashPositionsItem, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationPortfolioCharacteristics(Base):
    sell: OptimizationPortfolioSummarySection = None
    buy: OptimizationPortfolioSummarySection = None
    net: OptimizationPortfolioSummarySection = None
    gross: OptimizationPortfolioSummarySection = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityTableRow(Base):
    asset_id: Optional[str] = None
    name: Optional[str] = None
    adv22_day_pct: Optional[float] = None
    shares: Optional[float] = None
    net_weight: Optional[float] = None
    gross_weight: Optional[float] = None
    gross_exposure: Optional[float] = None
    net_exposure: Optional[float] = None
    transaction_cost: Optional[float] = None
    marginal_cost: Optional[float] = None
    one_day_price_change_pct: Optional[float] = None
    normalized_performance: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityTimeSeriesItem(Base):
    name: Optional[str] = None
    normalized_performance: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    annualized_return: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    annualized_correlation: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    annualized_volatility: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    annualized_sharp_ratio: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    annualized_tracking_error: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    max_drawdown: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    net_exposure: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    cumulative_pnl: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationFactorAnalyticsIntraday(Base):
    country: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    sector: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    domestic_china: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    market: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    currency: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    industry: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    risk: Tuple[OptimizationFactorAnalyticsItem, ...] = None
    cluster_classification: Tuple[OptimizationFactorAnalyticsItem, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationTradeSchedule(Base):
    period_number: int = None
    trade_day_number: int = None
    period_start_time: datetime.datetime = None
    period_end_time: datetime.datetime = None
    traded_positions: Tuple[OptimizationTradedPosition, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityResponse(Base):
    as_of_date: Optional[datetime.date] = None
    risk_model: Optional[str] = None
    notional: Optional[float] = None
    currency: Optional[Currency] = None
    report: Optional[str] = None
    summary: Optional[LiquiditySummary] = None
    constituent_transaction_costs: Optional[Tuple[LiquidityConstituent, ...]] = None
    constituents: Optional[Tuple[LiquidityConstituent, ...]] = None
    largest_holdings_by_weight: Optional[Tuple[LiquidityTableRow, ...]] = None
    least_liquid_holdings: Optional[Tuple[LiquidityTableRow, ...]] = None
    adv_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    region_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    country_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    sector_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    industry_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    market_cap_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    currency_buckets: Optional[Tuple[LiquidityBucket, ...]] = None
    execution_costs_with_different_time_horizons: Optional[Tuple[ExecutionCostForHorizon, ...]] = None
    time_to_trade_with_different_participation_rates: Optional[Tuple[PRateForHorizon, ...]] = None
    risk_over_time: Optional[Tuple[RiskAtHorizon, ...]] = None
    trade_complete_percent_over_time: Optional[Tuple[TradeCompleteAtHorizon, ...]] = None
    adv_percent_over_time: Optional[Tuple[AdvCurveTick, ...]] = None
    risk_buckets: Optional[Tuple[LiquidityFactor, ...]] = None
    factor_risk_buckets: Optional[Tuple[LiquidityFactorCategory, ...]] = None
    exposure_buckets: Optional[Tuple[LiquidityFactor, ...]] = None
    factor_exposure_buckets: Optional[Tuple[LiquidityFactorCategory, ...]] = None
    timeseries_data: Optional[Tuple[LiquidityTimeSeriesItem, ...]] = None
    assets_not_in_risk_model: Optional[Tuple[str, ...]] = None
    assets_not_in_cost_predict_model: Optional[Tuple[str, ...]] = None
    assets_without_compositions: Optional[Tuple[str, ...]] = None
    error_message: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationAnalytics(Base):
    portfolio_characteristics: OptimizationPortfolioCharacteristics = None
    asset_analytics_daily: Tuple[OptimizationAssetAnalyticsDaily, ...] = None
    portfolio_analytics_daily: Tuple[OptimizationPortfolioAnalyticsDaily, ...] = None
    assets_excluded: Tuple[OptimizationExcludedAsset, ...] = None
    constraints_consultations: Tuple[DictBase, ...] = None
    factor_analytics_intraday: OptimizationFactorAnalyticsIntraday = None
    asset_analytics_intraday: Tuple[OptimizationAssetAnalyticsIntraday, ...] = None
    portfolio_analytics_intraday: Tuple[OptimizationPortfolioAnalyticsIntraday, ...] = None
    cluster_analytics_intraday: Tuple[OptimizationClusterAnalyticsIntraday, ...] = None
    cluster_analytics: Tuple[OptimizationClusterAnalytics, ...] = None
    eod_cash_positions: Tuple[OptimizationEodCashPositions, ...] = None
    asset_analytics_day_one: Optional[Tuple[OptimizationAssetAnalyticsDayOne, ...]] = None
    close_auction_analytics: Optional[Tuple[OptimizationCloseAuctionAnalytics, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationResult(Base):
    created_by_id: str = None
    created_time: datetime.datetime = None
    entitlements: Entitlements = None
    entitlement_exclusions: EntitlementExclusions = None
    id_: str = field(default=None, metadata=config(field_name='id'))
    last_updated_by_id: str = None
    last_updated_time: datetime.datetime = None
    owner_id: str = None
    analytics: OptimizationAnalytics = None
    status: OptimizationStatus = None
    trade_schedule: Optional[Tuple[OptimizationTradeSchedule, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OptimizationRequest(Base):
    positions: Tuple[Position, ...] = None
    execution_start_time: datetime.datetime = None
    execution_end_time: datetime.datetime = None
    parameters: DictBase = None
    type_: OptimizationType = field(default=None, metadata=config(field_name='type'))
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    owner_id: Optional[str] = None
    wait_for_results: Optional[bool] = False
