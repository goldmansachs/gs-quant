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


class Encoding(EnumBase, Enum):    
    
    HTML = 'HTML'
    URL = 'URL'
    Unicode = 'Unicode'
    Base64 = 'Base64'
    Hex = 'Hex'
    ASCII = 'ASCII'    


class HedgeModel(EnumBase, Enum):    
    
    Smile = 'Smile'
    BlackScholes = 'BlackScholes'    


class ImgType(EnumBase, Enum):    
    
    APNG = 'APNG'
    AVIF = 'AVIF'
    GIF = 'GIF'
    JPEG = 'JPEG'
    PNG = 'PNG'
    SVG = 'SVG'
    WEBP = 'WEBP'    


class MarketRefOverrideType(EnumBase, Enum):    
    
    """Market Ref Override Type Spot or Fwd"""

    Spot = 'Spot'
    Fwd = 'Fwd'    


class OverlayType(EnumBase, Enum):    
    
    """Type"""

    Payout = 'Payout'
    Price = 'Price'
    MtM = 'MtM'
    Delta = 'Delta'
    Vega = 'Vega'
    Theta = 'Theta'
    RelativeCheapness = 'RelativeCheapness'
    ProbabilityDistribution = 'ProbabilityDistribution'
    RealisedProbability = 'RealisedProbability'
    MacroEvents = 'MacroEvents'
    MicroEvents = 'MicroEvents'
    Gamma = 'Gamma'
    _None = 'None'    


class PriceFormat(EnumBase, Enum):    
    
    """display unit for price"""

    Absolute = 'Absolute'
    Relative = 'Relative'
    Cents = 'Cents'    


class RelativeExpiryType(EnumBase, Enum):    
    
    Relative = 'Relative'
    Fixed = 'Fixed'    


class RelativeStrikeType(EnumBase, Enum):    
    
    Relative_Delta = 'Relative Delta'
    Relative_Spot = 'Relative Spot'
    Relative_Fwd = 'Relative Fwd'
    Fixed = 'Fixed'    


@dataclass
class HedgeTypes(Base):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomDeltaHedge(HedgeTypes):
    amount: float = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(init=False, default='CustomDeltaHedge', metadata=config(field_name='type', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


class GenericResponse(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class HyperLinkImageComments(CustomComments):
    url: Optional[str] = field(default=None, metadata=field_metadata)
    comment_type: Optional[str] = field(init=False, default='hyperLinkImageComments', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SalesPremiumAdjustment(Base):
    value: Optional[float] = field(default=None, metadata=field_metadata)
    unit: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SolvingTarget(Base):
    constraint: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkflowEntitlement(Base):
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    value: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BinaryImageComments(CustomComments):
    data: Optional[str] = field(default=None, metadata=field_metadata)
    img_type: Optional[ImgType] = field(default=None, metadata=field_metadata)
    encoding: Optional[Encoding] = field(default=None, metadata=field_metadata)
    comment_type: Optional[str] = field(init=False, default='binaryImageComments', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartingParameters(Base):
    spot_style: Optional[str] = field(default=None, metadata=field_metadata)
    overlay: Optional[OverlayType] = field(default=None, metadata=field_metadata)
    underlay: Optional[OverlayType] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeltaHedge(HedgeTypes):
    model: Optional[HedgeModel] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(init=False, default='DeltaHedge', metadata=config(field_name='type', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketRefOverride(Base):
    asset: Optional[str] = field(default=None, metadata=field_metadata)
    value: Optional[float] = field(default=None, metadata=field_metadata)
    mkt_ref_override_type: Optional[MarketRefOverrideType] = field(default=None, metadata=field_metadata)
    ref_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OverlayParameters(Base):
    overlay_type: Optional[OverlayType] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SolvingInfo(Base):
    target: Optional[SolvingTarget] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class StrategyDescription(Base):
    strategy_type: Optional[str] = field(default=None, metadata=field_metadata)
    long_short: Optional[LongShort] = field(default=LongShort.Long, metadata=field_metadata)
    assets: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    asset_classes: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkflowEntitlements(Base):
    version: Optional[int] = field(default=None, metadata=field_metadata)
    readers: Optional[Tuple[WorkflowEntitlement, ...]] = field(default=None, metadata=field_metadata)
    writers: Optional[Tuple[WorkflowEntitlement, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataParameters(Base):
    max_history: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    timestamp: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    spot_ref: Optional[float] = field(default=None, metadata=field_metadata)
    mkt_ref_override: Optional[Tuple[MarketRefOverride, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VisualStructuringReport(QuoteReport):
    report_type: Optional[str] = field(default='VisualStructuringReport', metadata=field_metadata)
    position_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    quick_entry_text: Optional[str] = field(default=None, metadata=field_metadata)
    as_of_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    market_data_parameters: Optional[MarketDataParameters] = field(default=None, metadata=field_metadata)
    overlay_parameters: Optional[OverlayParameters] = field(default=None, metadata=field_metadata)
    solving_info: Optional[SolvingInfo] = field(default=None, metadata=field_metadata)
    charting_parameters: Optional[ChartingParameters] = field(default=None, metadata=field_metadata)
    comments: Optional[Tuple[CustomComments, ...]] = field(default=None, metadata=field_metadata)
    strategy_description: Optional[StrategyDescription] = field(default=None, metadata=field_metadata)
    asset_class: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_instruction: Optional[HedgeTypes] = field(default=None, metadata=field_metadata)
    sales_premium_adjustment: Optional[SalesPremiumAdjustment] = field(default=None, metadata=field_metadata)
    price_format: Optional[PriceFormat] = field(default=None, metadata=field_metadata)
    strike_and_barrier_type: Optional[RelativeStrikeType] = field(default=None, metadata=field_metadata)
    expiry_type: Optional[RelativeExpiryType] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SaveQuoteRequest(Base):
    positions: Tuple[PositionSet, ...] = field(default=None, metadata=field_metadata)
    measures: Tuple[RiskMeasure, ...] = field(default=None, metadata=field_metadata)
    pricing_and_market_data_as_of: Optional[Tuple[PricingDateAndMarketDataAsOf, ...]] = field(default=None, metadata=field_metadata)
    pricing_location: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    scenario: Optional[MarketDataScenario] = field(default=None, metadata=field_metadata)
    parameters: Optional[RiskRequestParameters] = field(default=None, metadata=field_metadata)
    reports: Optional[Tuple[QuoteReport, ...]] = field(default=None, metadata=field_metadata)
    shared_users: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    comments: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    original_workflow_id: Optional[str] = field(default=None, metadata=field_metadata)
    is_sharing_parent: Optional[bool] = field(default=None, metadata=field_metadata)
    entitlements: Optional[WorkflowEntitlements] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkflowPosition(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    position_sets: Optional[Tuple[PositionSet, ...]] = field(default=None, metadata=field_metadata)
    reports: Optional[Tuple[QuoteReport, ...]] = field(default=None, metadata=field_metadata)
    comments: Optional[str] = field(default=None, metadata=field_metadata)
    original_workflow_id: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[WorkflowEntitlements] = field(default=None, metadata=field_metadata)
    creator: Optional[str] = field(default=None, metadata=field_metadata)
    originating_system: Optional[str] = field(default=None, metadata=field_metadata)
    is_read_only: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkflowPositionsResponse(Base):
    results: Optional[Tuple[WorkflowPosition, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
