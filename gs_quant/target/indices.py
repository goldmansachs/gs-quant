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


class ApprovalStatus(EnumBase, Enum):    
    
    """Current status of an approval"""

    Draft = 'Draft'
    Cancelled = 'Cancelled'
    Submitted = 'Submitted'
    Approved = 'Approved'
    Approving = 'Approving'
    Rejected = 'Rejected'
    Locked = 'Locked'
    Error = 'Error'    


class IndicesCurrency(EnumBase, Enum):    
    
    """Currencies supported for Indices"""

    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    CAD = 'CAD'
    AUD = 'AUD'
    CHF = 'CHF'
    CNH = 'CNH'
    CNY = 'CNY'
    DKK = 'DKK'
    HKD = 'HKD'
    IDR = 'IDR'
    ILS = 'ILS'
    INR = 'INR'
    JPY = 'JPY'
    KRW = 'KRW'
    KWD = 'KWD'
    MXN = 'MXN'
    MYR = 'MYR'
    NOK = 'NOK'
    NZD = 'NZD'
    PHP = 'PHP'
    PLN = 'PLN'
    RUB = 'RUB'
    SAR = 'SAR'
    SEK = 'SEK'
    SGD = 'SGD'
    THB = 'THB'
    TRY = 'TRY'
    TWD = 'TWD'
    ZAR = 'ZAR'
    BRL = 'BRL'    


class IndicesConstructRequestTypes(Base):
    pass


class IndicesConstructResponseTypes(Base):
    pass


class IndicesRebalanceActionTypes(Base):
    pass


class IndicesRebalanceInputTypes(Base):
    pass


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ApprovalComment(Base):
    timestamp: Optional[datetime.datetime] = None
    message: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketRiskParams(Base):
    risk_model: Optional[str] = None
    fx_hedged: Optional[bool] = None
    delete: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsRebalanceAction(IndicesRebalanceActionTypes):
    comment: Optional[str] = None
    action_type: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsResponse(IndicesConstructResponseTypes):
    status: Optional[str] = None
    report_id: Optional[str] = None
    asset_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectActionRequest(IndicesRebalanceActionTypes):
    action_comment: str = None
    trader_attestations: Optional[Tuple[str, ...]] = None
    user_action: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectIndexParameter(Base):
    name: Optional[str] = None
    value: Optional[Union[float, str]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectIndexParameters(Base):
    name: Optional[str] = None
    value: Optional[Union[float, str]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectSeries(Base):
    data: Optional[tuple] = None
    identifier: Optional[str] = None
    identifier_type: Optional[str] = None
    name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesPositionInput(Base):
    asset_id: str = None
    weight: float = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionPriceInput(Base):
    asset_id: str = None
    quantity: Optional[float] = None
    weight: Optional[float] = None
    notional: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PublishParameters(Base):
    publish_to_bloomberg: bool = False
    include_price_history: bool = False
    publish_to_reuters: Optional[bool] = False
    publish_to_factset: Optional[bool] = False


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditCustomBasketPricingParameters(Base):
    quote_source: BasketValuationSource = None
    quote_time: str = '16:00:00'
    quote_side: Side = 'Mid'
    quoting_type: QuoteType = None
    weighting_type: WeightingType = None
    currency: Optional[Currency] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsPricingParameters(Base):
    currency: Optional[IndicesCurrency] = None
    asset_data_set_id: Optional[str] = None
    divisor: Optional[float] = None
    fx_data_set_id: Optional[str] = None
    fallback_date: Optional[str] = None
    initial_price: Optional[float] = None
    target_notional: Optional[float] = None
    pricing_date: Optional[datetime.date] = None
    vendor: Optional[MarketDataVendor] = None
    weighting_strategy: Optional[str] = None
    reweight: Optional[bool] = False
    asset_overwrite_data_set_id: Optional[str] = 'BASKET_EOD_OVERWRITE'


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsRiskScheduleInputs(Base):
    risk_models: Optional[Tuple[CustomBasketRiskParams, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectConstituentColumn(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    field_: str = field(default=None, metadata=config(field_name='field'))
    name: str = None
    aggregator_string: Optional[str] = None
    class_: Optional[str] = field(default=None, metadata=config(field_name='class'))
    filter_: Optional[str] = field(default=None, metadata=config(field_name='filter'))
    formatter_string: Optional[str] = None
    ID: Optional[int] = None
    max_width: Optional[int] = None
    min_width: Optional[int] = None
    precision: Optional[int] = None
    sortable: Optional[int] = None
    tooltip: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesPositionSet(Base):
    positions: Tuple[IndicesPositionInput, ...] = None
    position_date: datetime.date = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditCustomBasketCreateInputs(IndicesConstructRequestTypes):
    ticker: str = None
    name: str = None
    pricing_parameters: CreditCustomBasketPricingParameters = None
    position_set: Tuple[PositionPriceInput, ...] = None
    return_type: IndexCalculationType = 'Price Return'
    styles: Tuple[str, ...] = None
    asset_class: Optional[AssetClass] = 'Credit'
    description: Optional[str] = None
    related_content: Optional[GIRDomain] = None
    portfolio_id: Optional[str] = None
    publish_parameters: Optional[PublishParameters] = None
    index_notes: Optional[str] = None
    flagship: Optional[bool] = False
    on_behalf_of: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsBackcastInputs(Base):
    position_set: Tuple[IndicesPositionSet, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsCreateInputs(IndicesConstructRequestTypes):
    ticker: str = None
    name: str = None
    pricing_parameters: CustomBasketsPricingParameters = None
    position_set: Tuple[PositionPriceInput, ...] = None
    return_type: str = None
    description: Optional[str] = None
    styles: Optional[Tuple[str, ...]] = None
    related_content: Optional[GIRDomain] = None
    portfolio_id: Optional[str] = None
    hedge_id: Optional[str] = None
    clone_parent_id: Optional[str] = None
    publish_parameters: Optional[PublishParameters] = None
    index_notes: Optional[str] = None
    flagship: Optional[bool] = None
    on_behalf_of: Optional[str] = None
    allow_limited_access_assets: Optional[bool] = False
    allow_ca_restricted_assets: Optional[bool] = field(default=False, metadata=config(field_name='allowCARestrictedAssets'))
    vendor: Optional[str] = None
    default_backcast: Optional[bool] = True


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsEditInputs(Base):
    name: Optional[str] = None
    description: Optional[str] = None
    styles: Optional[Tuple[str, ...]] = None
    related_content: Optional[GIRDomain] = None
    publish_parameters: Optional[PublishParameters] = None
    index_notes: Optional[str] = None
    index_not_trading_reasons: Optional[IndexNotTradingReasons] = None
    flagship: Optional[bool] = None
    clone_parent_id: Optional[str] = None
    hedge_id: Optional[str] = None
    portfolio_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsRebalanceInputs(Base):
    position_set: Optional[Tuple[PositionPriceInput, ...]] = None
    publish_parameters: Optional[PublishParameters] = None
    pricing_parameters: Optional[CustomBasketsPricingParameters] = None
    allow_limited_access_assets: Optional[bool] = False
    allow_ca_restricted_assets: Optional[bool] = field(default=False, metadata=config(field_name='allowCARestrictedAssets'))
    allow_system_approval: Optional[bool] = False
    clone_parent_id: Optional[str] = None
    hedge_id: Optional[str] = None
    portfolio_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DynamicConstructionResponse(IndicesConstructResponseTypes):
    action: Optional[object] = None
    columns: Optional[Tuple[ISelectConstituentColumn, ...]] = None
    constituent_validations: Optional[tuple] = None
    date_validation_status: Optional[str] = None
    types: Optional[tuple] = None
    date_validations: Optional[tuple] = None
    new_parameters: Optional[Tuple[ISelectNewParameter, ...]] = None
    index_type: Optional[str] = None
    index_parameter_definitions: Optional[tuple] = None
    index_metadata: Optional[tuple] = None
    index_parameters: Optional[tuple] = None
    index_parameter_validation: Optional[tuple] = None
    status: Optional[object] = None
    valid: Optional[int] = None
    validation_messages: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectRebalance(Base):
    new_weights: Optional[Tuple[ISelectNewWeight, ...]] = None
    rebalance_date: Optional[str] = None
    new_parameters: Optional[Tuple[ISelectNewParameter, ...]] = None
    index_parameters: Optional[Tuple[ISelectIndexParameters, ...]] = None
    waiver_requested: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectRequest(IndicesRebalanceInputTypes):
    rebalance_date: str = None
    request_counter: int = None
    use_new_rebalance_interface: bool = None
    new_parameters: Optional[Tuple[ISelectNewParameter, ...]] = None
    index_parameters: Optional[Tuple[ISelectIndexParameter, ...]] = None
    new_weights: Optional[Tuple[ISelectNewWeight, ...]] = None
    new_units: Optional[Tuple[ISelectNewUnit, ...]] = None
    entry_type: Optional[str] = None
    waiver_requested: Optional[bool] = None
    presubmit: Optional[bool] = None
    requester_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectResponse(Base):
    action: Optional[object] = field(default=None, metadata=config(field_name='Action'))
    action_comment: Optional[str] = field(default=None, metadata=config(field_name='ActionComment'))
    asset_name: Optional[str] = None
    asset_short_name: Optional[str] = None
    available_action_confirms: Optional[Tuple[Tuple[str, ...], ...]] = None
    available_actions: Optional[tuple] = None
    available_rebalance_dates: Optional[Tuple[str, ...]] = None
    constituent_validations: Optional[tuple] = None
    date_validation_status: Optional[str] = None
    date_validations: Optional[tuple] = None
    entry_mode: Optional[str] = None
    entry_type: Optional[str] = None
    internal_rebalance: Optional[int] = None
    index_parameter_definitions: Optional[tuple] = None
    index_parameters: Optional[tuple] = None
    index_parameter_validation: Optional[tuple] = None
    new_units: Optional[Tuple[ISelectNewUnit, ...]] = None
    new_weights: Optional[Tuple[ISelectNewWeight, ...]] = None
    notification_date: Optional[str] = None
    rebalance_date: Optional[str] = None
    rebalance_determination_date: Optional[str] = None
    reb_determination_index_level: Optional[float] = None
    request_counter: Optional[int] = None
    series: Optional[ISelectSeries] = None
    status: Optional[object] = None
    submission_data: Optional[tuple] = None
    submission_data_columns: Optional[Tuple[ISelectConstituentColumn, ...]] = None
    submission_text: Optional[str] = None
    valid: Optional[int] = None
    validation_messages: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesDynamicConstructInputs(IndicesConstructRequestTypes):
    index_type: str = None
    new_parameters: Tuple[ISelectNewParameter, ...] = None
    index_parameters: Tuple[ISelectIndexParameters, ...] = None
    index_metadata: Tuple[ISelectIndexParameters, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesBackcastInputs(Base):
    parameters: CustomBasketsBackcastInputs = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesEditInputs(Base):
    parameters: CustomBasketsEditInputs = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesRebalanceInputs(IndicesRebalanceInputTypes):
    parameters: DictBase = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ApprovalCustomBasketResponse(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    positions_to_rebalance: PositionSet = None
    entitlements: Optional[Entitlements] = None
    status: Optional[ApprovalStatus] = None
    parent_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    approved_by_id: Optional[str] = None
    approved_time: Optional[datetime.datetime] = None
    submitted_by_id: Optional[str] = None
    submitted_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    comments: Optional[Tuple[ApprovalComment, ...]] = None
    notifyees: Optional[Tuple[str, ...]] = None
