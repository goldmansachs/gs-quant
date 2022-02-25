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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetConstraint(Base):
    asset_id: str = None
    max_: float = field(default=None, metadata=config(field_name='max'))
    min_: float = field(default=None, metadata=config(field_name='min'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ClassificationConstraint(Base):
    type_: str = field(default=None, metadata=config(field_name='type'))
    name: str = None
    max_: float = field(default=None, metadata=config(field_name='max'))
    min_: float = field(default=None, metadata=config(field_name='min'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ESGConstraint(Base):
    name: str = None
    max_: float = field(default=None, metadata=config(field_name='max'))
    min_: float = field(default=None, metadata=config(field_name='min'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorConstraint(Base):
    factor: str = None
    exposure: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorExposure(Base):
    factor: str = None
    exposure: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgerComparisonProperties(Base):
    hedge_value_type: str = None
    hedge_value: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorExposures(Base):
    country: Tuple[FactorExposure, ...] = None
    industry: Tuple[FactorExposure, ...] = None
    sector: Tuple[FactorExposure, ...] = None
    style: Tuple[FactorExposure, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgeUniverse(Base):
    asset_ids: Optional[Tuple[str, ...]] = None
    asset_types: Optional[Tuple[HedgeUniverseAssetType, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgerConstraintPrioritySettings(Base):
    min_sector_weights: Optional[HedgerConstraintPrioritySetting] = None
    max_sector_weights: Optional[HedgerConstraintPrioritySetting] = None
    min_industry_weights: Optional[HedgerConstraintPrioritySetting] = None
    max_industry_weights: Optional[HedgerConstraintPrioritySetting] = None
    min_region_weights: Optional[HedgerConstraintPrioritySetting] = None
    max_region_weights: Optional[HedgerConstraintPrioritySetting] = None
    min_country_weights: Optional[HedgerConstraintPrioritySetting] = None
    max_country_weights: Optional[HedgerConstraintPrioritySetting] = None
    style_exposures: Optional[HedgerConstraintPrioritySetting] = None
    country_exposures: Optional[HedgerConstraintPrioritySetting] = None
    region_exposures: Optional[HedgerConstraintPrioritySetting] = None
    industry_exposures: Optional[HedgerConstraintPrioritySetting] = None
    sector_exposures: Optional[HedgerConstraintPrioritySetting] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeConstituent(Base):
    asset_id: str = None
    name: str = None
    weight: float = None
    currency: Currency = None
    country: Optional[str] = None
    correlation: Optional[float] = None
    transaction_cost: Optional[float] = None
    marginal_cost: Optional[float] = None
    borrow_cost: Optional[float] = None
    shares: Optional[float] = None
    price: Optional[float] = None
    multiplier: Optional[float] = None
    notional: Optional[float] = None
    bbid: Optional[str] = None
    adv_percentage: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgerResultPositions(Base):
    beta_exposure: float = None
    daily_va_r: float = None
    factor_exposures: FactorExposures = None
    specific_exposure: float = None
    systematic_exposure: float = None
    total_risk: float = None
    volatility: float = None
    net_exposure: float = None
    constituents: Optional[Tuple[HedgeConstituent, ...]] = None
    number_of_positions: Optional[float] = None
    cumulative_pnl: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None
    transaction_cost: Optional[float] = None
    borrow_cost_bps: Optional[float] = None
    max_drawdown: Optional[float] = None
    gross_exposure: Optional[float] = None
    long_exposure: Optional[float] = None
    short_exposure: Optional[float] = None
    tracking_error: Optional[float] = None
    correlation: Optional[float] = None
    exposure_overlap_with_target: Optional[float] = None
    total_pnl: Optional[float] = None
    turnover_percentage: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeBenchmark(Base):
    asset_id: str = None
    cumulative_pnl: Optional[Tuple[Tuple[Union[datetime.date, float], ...], ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgeGetManyRequestPathSchema(Base):
    limit: Optional[Tuple[str, ...]] = None
    offset: Optional[Tuple[str, ...]] = None
    scroll: Optional[Tuple[str, ...]] = None
    scroll_id: Optional[Tuple[str, ...]] = None
    ids: Optional[Tuple[str, ...]] = None
    order_by: Optional[Tuple[Union[DictBase, str], ...]] = None
    hedge_tracking_error: Optional[Tuple[float, ...]] = None
    hedge_volatility: Optional[Tuple[float, ...]] = None
    tags: Optional[Tuple[str, ...]] = None
    last_updated_by_id: Optional[Tuple[str, ...]] = None
    created_by_id: Optional[Tuple[str, ...]] = None
    target_notional: Optional[Tuple[float, ...]] = None
    owner_id: Optional[Tuple[str, ...]] = None
    hedge_annualized_volatility: Optional[Tuple[float, ...]] = None
    name: Optional[Tuple[str, ...]] = None
    description: Optional[Tuple[str, ...]] = None
    id_: Optional[Tuple[str, ...]] = field(default=None, metadata=config(field_name='id'))
    objective: Optional[Tuple[str, ...]] = None
    hedge_notional: Optional[Tuple[float, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceHedgeResult(Base):
    target: DictBase = None
    hedge: Optional[DictBase] = None
    hedged_target: Optional[DictBase] = None
    benchmarks: Optional[Tuple[DictBase, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgeResult(Base):
    hedge: FactorHedgerResultPositions = None
    hedged_target: FactorHedgerResultPositions = None
    target: Optional[FactorHedgerResultPositions] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HedgerComparison(Base):
    entity_id: str = None
    entity_type: HedgerComparisonType = None
    hedge_properties: HedgerComparisonProperties = None
    result: Optional[DictBase] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Target(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    positions: Optional[Tuple[Position, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FactorHedgeParameters(Base):
    risk_model: str = None
    target_notional: float = None
    hedge_notional: float = None
    hedge_target: Target = None
    hedge_universe: FactorHedgeUniverse = None
    hedge_date: datetime.date = None
    backtest_start_date: datetime.date = None
    backtest_end_date: datetime.date = None
    fx_hedged: Optional[bool] = None
    exclude_target_assets: Optional[bool] = None
    exclude_corporate_actions: Optional[bool] = None
    exclude_corporate_actions_types: Optional[Tuple[CorporateActionsTypes, ...]] = None
    exclude_hard_to_borrow_assets: Optional[bool] = None
    exclude_restricted_assets: Optional[bool] = None
    max_adv_percentage: Optional[float] = None
    explode_universe: Optional[bool] = None
    min_names: Optional[float] = None
    max_names: Optional[float] = None
    min_weight: Optional[float] = None
    max_weight: Optional[float] = None
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    market_participation_rate: Optional[float] = 10
    asset_constraints: Optional[Tuple[AssetConstraint, ...]] = None
    factor_constraints: Optional[Tuple[FactorConstraint, ...]] = None
    classification_constraints: Optional[Tuple[ClassificationConstraint, ...]] = None
    esg_constraints: Optional[Tuple[ESGConstraint, ...]] = None
    constraint_priority_settings: Optional[FactorHedgerConstraintPrioritySettings] = None
    comparisons: Optional[Tuple[HedgerComparison, ...]] = None
    turnover_portfolio_id: Optional[str] = None
    max_turnover_percentage: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceHedgeParameters(Base):
    hedge_target: Target = None
    universe: Tuple[str, ...] = None
    notional: float = None
    observation_start_date: datetime.date = None
    observation_end_date: datetime.date = None
    backtest_start_date: Optional[datetime.date] = None
    backtest_end_date: Optional[datetime.date] = None
    sampling_period: Optional[str] = 'Weekly'
    max_leverage: Optional[float] = None
    percentage_in_cash: Optional[float] = None
    explode_universe: Optional[bool] = None
    exclude_target_assets: Optional[bool] = None
    exclude_corporate_actions: Optional[bool] = None
    exclude_corporate_actions_types: Optional[Tuple[CorporateActionsTypes, ...]] = None
    exclude_hard_to_borrow_assets: Optional[bool] = None
    exclude_restricted_assets: Optional[bool] = None
    max_adv_percentage: Optional[float] = None
    max_return_deviation: Optional[float] = None
    max_weight: Optional[float] = None
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    market_participation_rate: Optional[float] = 10
    asset_constraints: Optional[Tuple[AssetConstraint, ...]] = None
    classification_constraints: Optional[Tuple[ClassificationConstraint, ...]] = None
    esg_constraints: Optional[Tuple[ESGConstraint, ...]] = None
    benchmarks: Optional[Tuple[str, ...]] = None
    use_machine_learning: Optional[bool] = False
    lasso_weight: Optional[float] = None
    ridge_weight: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Hedge(Base):
    name: str = None
    parameters: DictBase = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    owner_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    entitlements: Optional[Entitlements] = None
    tags: Optional[Tuple[str, ...]] = None
    description: Optional[str] = None
    objective: Optional[HedgeObjective] = None
    result: Optional[DictBase] = None
    comparison_results: Optional[Tuple[HedgerComparison, ...]] = None
