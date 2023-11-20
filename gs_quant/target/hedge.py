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


class CorporateActionsTypes(EnumBase, Enum):    
    
    """Types of corporate actions in the hedge"""

    Mergers = 'Mergers'
    Quote_lot_adjustments = 'Quote lot adjustments'
    Rights = 'Rights'
    Spinoffs = 'Spinoffs'
    Cash_dividends = 'Cash dividends'
    Stock_splits = 'Stock splits'
    Reorganization = 'Reorganization'    


class HedgeObjective(EnumBase, Enum):    
    
    """The objective of the hedge."""

    Minimize_Factor_Risk = 'Minimize Factor Risk'
    Replicate_Performance = 'Replicate Performance'    


class HedgeUniverseAssetType(EnumBase, Enum):    
    
    """Type of assets that will be added to the hedge universe."""

    Custom_Basket = 'Custom Basket'
    ETF = 'ETF'
    Research_Basket = 'Research Basket'
    Single_Stock = 'Single Stock'    


class HedgerComparisonType(EnumBase, Enum):    
    
    Asset = 'Asset'
    Portfolio = 'Portfolio'
    Hedge = 'Hedge'    


class HedgerConstraintPrioritySetting(EnumBase, Enum):    
    
    """Priority of the constraint from 0-5 (prioritized in that order). The
       optimization will fail if it cannot meet a constraint with 0 priority. A
       constraint with priority of 1-5 can be called a relaxed constraint, which
       means that the optimization will make its best effort to meet the
       constraint but will not fail if it cannot."""

    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'    


class SamplingPeriod(EnumBase, Enum):    
    
    """The length of time in between return samples."""

    Daily = 'Daily'
    Weekly = 'Weekly'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetConstraint(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    max_: float = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    min_: float = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


class BasketConditions(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ClassificationConstraint(Base):
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    max_: float = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    min_: float = field(default=None, metadata=config(field_name='min', exclude=exclude_none))


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ESGConstraint(Base):
    name: str = field(default=None, metadata=field_metadata)
    max_: float = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    min_: float = field(default=None, metadata=config(field_name='min', exclude=exclude_none))


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorConstraint(Base):
    factor: str = field(default=None, metadata=field_metadata)
    exposure: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorExposure(Base):
    factor: str = field(default=None, metadata=field_metadata)
    exposure: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorMCTRByGroupConstraint(Base):
    factors: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    max_: float = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgerComparisonProperties(Base):
    hedge_value_type: str = field(default=None, metadata=field_metadata)
    hedge_value: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorExposures(Base):
    country: Tuple[FactorExposure, ...] = field(default=None, metadata=field_metadata)
    industry: Tuple[FactorExposure, ...] = field(default=None, metadata=field_metadata)
    sector: Tuple[FactorExposure, ...] = field(default=None, metadata=field_metadata)
    style: Tuple[FactorExposure, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgeUniverse(Base):
    asset_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_types: Optional[Tuple[HedgeUniverseAssetType, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgerConstraintPrioritySettings(Base):
    min_sector_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    max_sector_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    min_industry_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    max_industry_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    min_region_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    max_region_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    min_country_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    max_country_weights: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    style_exposures: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    country_exposures: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    region_exposures: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    industry_exposures: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    sector_exposures: Optional[HedgerConstraintPrioritySetting] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeConstituent(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    weight: float = field(default=None, metadata=field_metadata)
    currency: Currency = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    correlation: Optional[float] = field(default=None, metadata=field_metadata)
    transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    marginal_cost: Optional[float] = field(default=None, metadata=field_metadata)
    borrow_cost: Optional[float] = field(default=None, metadata=field_metadata)
    shares: Optional[float] = field(default=None, metadata=field_metadata)
    price: Optional[float] = field(default=None, metadata=field_metadata)
    multiplier: Optional[float] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    bbid: Optional[str] = field(default=None, metadata=field_metadata)
    adv_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    sector: Optional[str] = field(default=None, metadata=field_metadata)
    industry: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgerResultPositions(Base):
    beta_exposure: float = field(default=None, metadata=field_metadata)
    daily_va_r: float = field(default=None, metadata=field_metadata)
    factor_exposures: FactorExposures = field(default=None, metadata=field_metadata)
    specific_exposure: float = field(default=None, metadata=field_metadata)
    systematic_exposure: float = field(default=None, metadata=field_metadata)
    total_risk: float = field(default=None, metadata=field_metadata)
    volatility: float = field(default=None, metadata=field_metadata)
    net_exposure: float = field(default=None, metadata=field_metadata)
    constituents: Optional[Tuple[HedgeConstituent, ...]] = field(default=None, metadata=field_metadata)
    number_of_positions: Optional[float] = field(default=None, metadata=field_metadata)
    cumulative_pnl: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    transaction_cost: Optional[float] = field(default=None, metadata=field_metadata)
    borrow_cost_bps: Optional[float] = field(default=None, metadata=field_metadata)
    max_drawdown: Optional[float] = field(default=None, metadata=field_metadata)
    gross_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    long_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    short_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    tracking_error: Optional[float] = field(default=None, metadata=field_metadata)
    correlation: Optional[float] = field(default=None, metadata=field_metadata)
    exposure_overlap_with_target: Optional[float] = field(default=None, metadata=field_metadata)
    total_pnl: Optional[float] = field(default=None, metadata=field_metadata)
    turnover_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeBenchmark(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    cumulative_pnl: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeGetManyRequestPathSchema(Base):
    limit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    offset: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    scroll: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    order_by: Optional[Tuple[Union[DictBase, str], ...]] = field(default=None, metadata=field_metadata)
    hedge_tracking_error: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    hedge_volatility: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    target_notional: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    owner_id: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    hedge_annualized_volatility: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    description: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    id_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    objective: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    hedge_notional: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceHedgeResult(Base):
    target: DictBase = field(default=None, metadata=field_metadata)
    hedge: Optional[DictBase] = field(default=None, metadata=field_metadata)
    hedged_target: Optional[DictBase] = field(default=None, metadata=field_metadata)
    benchmarks: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgeResult(Base):
    hedge: FactorHedgerResultPositions = field(default=None, metadata=field_metadata)
    hedged_target: FactorHedgerResultPositions = field(default=None, metadata=field_metadata)
    target: Optional[FactorHedgerResultPositions] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgerComparison(Base):
    entity_id: str = field(default=None, metadata=field_metadata)
    entity_type: HedgerComparisonType = field(default=None, metadata=field_metadata)
    hedge_properties: HedgerComparisonProperties = field(default=None, metadata=field_metadata)
    result: Optional[DictBase] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Target(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    positions: Optional[Tuple[Position, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgeParameters(Base):
    risk_model: str = field(default=None, metadata=field_metadata)
    target_notional: float = field(default=None, metadata=field_metadata)
    hedge_notional: float = field(default=None, metadata=field_metadata)
    hedge_target: Target = field(default=None, metadata=field_metadata)
    hedge_universe: FactorHedgeUniverse = field(default=None, metadata=field_metadata)
    hedge_date: datetime.date = field(default=None, metadata=field_metadata)
    backtest_start_date: datetime.date = field(default=None, metadata=field_metadata)
    backtest_end_date: datetime.date = field(default=None, metadata=field_metadata)
    fx_hedged: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_target_assets: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_corporate_actions: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_corporate_actions_types: Optional[Tuple[CorporateActionsTypes, ...]] = field(default=None, metadata=field_metadata)
    exclude_hard_to_borrow_assets: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_restricted_assets: Optional[bool] = field(default=None, metadata=field_metadata)
    max_adv_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    explode_universe: Optional[bool] = field(default=None, metadata=field_metadata)
    min_names: Optional[float] = field(default=None, metadata=field_metadata)
    max_names: Optional[float] = field(default=None, metadata=field_metadata)
    max_trades: Optional[float] = field(default=None, metadata=field_metadata)
    min_weight: Optional[float] = field(default=None, metadata=field_metadata)
    max_weight: Optional[float] = field(default=None, metadata=field_metadata)
    min_market_cap: Optional[float] = field(default=None, metadata=field_metadata)
    max_market_cap: Optional[float] = field(default=None, metadata=field_metadata)
    max_factor_mctr: Optional[float] = field(default=None, metadata=config(field_name='maxFactorMCTR', exclude=exclude_none))
    max_factor_mctr_by_group: Optional[Tuple[FactorMCTRByGroupConstraint, ...]] = field(default=None, metadata=config(field_name='maxFactorMCTRByGroup', exclude=exclude_none))
    market_participation_rate: Optional[float] = field(default=10, metadata=field_metadata)
    asset_constraints: Optional[Tuple[AssetConstraint, ...]] = field(default=None, metadata=field_metadata)
    constrain_assets_by_notional: Optional[bool] = field(default=None, metadata=field_metadata)
    allow_long_short: Optional[bool] = field(default=None, metadata=field_metadata)
    only_reweight_target_composition: Optional[bool] = field(default=None, metadata=field_metadata)
    factor_constraints: Optional[Tuple[FactorConstraint, ...]] = field(default=None, metadata=field_metadata)
    classification_constraints: Optional[Tuple[ClassificationConstraint, ...]] = field(default=None, metadata=field_metadata)
    esg_constraints: Optional[Tuple[ESGConstraint, ...]] = field(default=None, metadata=field_metadata)
    constraint_priority_settings: Optional[FactorHedgerConstraintPrioritySettings] = field(default=None, metadata=field_metadata)
    comparisons: Optional[Tuple[HedgerComparison, ...]] = field(default=None, metadata=field_metadata)
    turnover_portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    max_turnover_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    return_type: Optional[ReturnType] = field(default=None, metadata=field_metadata)
    is_best_basket: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceHedgeParameters(Base):
    hedge_target: Target = field(default=None, metadata=field_metadata)
    universe: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    notional: float = field(default=None, metadata=field_metadata)
    observation_start_date: datetime.date = field(default=None, metadata=field_metadata)
    observation_end_date: datetime.date = field(default=None, metadata=field_metadata)
    backtest_start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    backtest_end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    sampling_period: Optional[SamplingPeriod] = field(default=SamplingPeriod.Weekly, metadata=field_metadata)
    max_leverage: Optional[float] = field(default=None, metadata=field_metadata)
    percentage_in_cash: Optional[float] = field(default=None, metadata=field_metadata)
    explode_universe: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_target_assets: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_corporate_actions: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_corporate_actions_types: Optional[Tuple[CorporateActionsTypes, ...]] = field(default=None, metadata=field_metadata)
    exclude_hard_to_borrow_assets: Optional[bool] = field(default=None, metadata=field_metadata)
    exclude_restricted_assets: Optional[bool] = field(default=None, metadata=field_metadata)
    max_adv_percentage: Optional[float] = field(default=None, metadata=field_metadata)
    max_return_deviation: Optional[float] = field(default=None, metadata=field_metadata)
    max_weight: Optional[float] = field(default=None, metadata=field_metadata)
    min_market_cap: Optional[float] = field(default=None, metadata=field_metadata)
    max_market_cap: Optional[float] = field(default=None, metadata=field_metadata)
    market_participation_rate: Optional[float] = field(default=10, metadata=field_metadata)
    asset_constraints: Optional[Tuple[AssetConstraint, ...]] = field(default=None, metadata=field_metadata)
    classification_constraints: Optional[Tuple[ClassificationConstraint, ...]] = field(default=None, metadata=field_metadata)
    esg_constraints: Optional[Tuple[ESGConstraint, ...]] = field(default=None, metadata=field_metadata)
    benchmarks: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    use_machine_learning: Optional[bool] = field(default=False, metadata=field_metadata)
    lasso_weight: Optional[float] = field(default=None, metadata=field_metadata)
    ridge_weight: Optional[float] = field(default=None, metadata=field_metadata)
    return_type: Optional[ReturnType] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Hedge(Base):
    name: str = field(default=None, metadata=field_metadata)
    parameters: DictBase = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    objective: Optional[HedgeObjective] = field(default=None, metadata=field_metadata)
    result: Optional[DictBase] = field(default=None, metadata=field_metadata)
    comparison_results: Optional[Tuple[HedgerComparison, ...]] = field(default=None, metadata=field_metadata)
