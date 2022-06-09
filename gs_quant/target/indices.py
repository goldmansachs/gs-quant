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
    CNO = 'CNO'
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


@dataclass
class IndicesConstructRequestTypes(Base):
    pass


@dataclass
class IndicesConstructResponseTypes(Base):
    pass


@dataclass
class IndicesRebalanceActionTypes(Base):
    pass


@dataclass
class IndicesRebalanceInputTypes(Base):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ApprovalComment(Base):
    timestamp: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketRiskParams(Base):
    risk_model: Optional[str] = field(default=None, metadata=field_metadata)
    fx_hedged: Optional[bool] = field(default=None, metadata=field_metadata)
    delete: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsRebalanceAction(IndicesRebalanceActionTypes):
    comment: Optional[str] = field(default=None, metadata=field_metadata)
    action_type: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsResponse(IndicesConstructResponseTypes):
    status: Optional[str] = field(default=None, metadata=field_metadata)
    report_id: Optional[str] = field(default=None, metadata=field_metadata)
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectActionRequest(IndicesRebalanceActionTypes):
    action_comment: str = field(default=None, metadata=field_metadata)
    trader_attestations: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    user_action: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectIndexParameter(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectIndexParameters(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectSeries(Base):
    data: Optional[tuple] = field(default=None, metadata=field_metadata)
    identifier: Optional[str] = field(default=None, metadata=field_metadata)
    identifier_type: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesPositionInput(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    weight: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionPriceInput(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    weight: Optional[float] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PublishParameters(Base):
    publish_to_bloomberg: bool = field(default=False, metadata=field_metadata)
    include_price_history: bool = field(default=False, metadata=field_metadata)
    publish_to_reuters: Optional[bool] = field(default=False, metadata=field_metadata)
    publish_to_factset: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditCustomBasketPricingParameters(Base):
    quote_source: BasketValuationSource = field(default=None, metadata=field_metadata)
    quote_time: str = field(default='16:00:00', metadata=field_metadata)
    quote_side: Side = field(default='Mid', metadata=field_metadata)
    quoting_type: QuoteType = field(default=None, metadata=field_metadata)
    weighting_type: WeightingType = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsPricingParameters(Base):
    currency: Optional[IndicesCurrency] = field(default=None, metadata=field_metadata)
    asset_data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    divisor: Optional[float] = field(default=None, metadata=field_metadata)
    fx_data_set_id: Optional[str] = field(default=None, metadata=field_metadata)
    fallback_date: Optional[str] = field(default=None, metadata=field_metadata)
    initial_price: Optional[float] = field(default=None, metadata=field_metadata)
    target_notional: Optional[float] = field(default=None, metadata=field_metadata)
    pricing_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    vendor: Optional[MarketDataVendor] = field(default=None, metadata=field_metadata)
    weighting_strategy: Optional[str] = field(default=None, metadata=field_metadata)
    reweight: Optional[bool] = field(default=False, metadata=field_metadata)
    asset_overwrite_data_set_id: Optional[str] = field(default='BASKET_EOD_OVERWRITE', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsRiskScheduleInputs(Base):
    risk_models: Optional[Tuple[CustomBasketRiskParams, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectConstituentColumn(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    field_: str = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    aggregator_string: Optional[str] = field(default=None, metadata=field_metadata)
    class_: Optional[str] = field(default=None, metadata=config(field_name='class', exclude=exclude_none))
    filter_: Optional[str] = field(default=None, metadata=config(field_name='filter', exclude=exclude_none))
    formatter_string: Optional[str] = field(default=None, metadata=field_metadata)
    ID: Optional[int] = field(default=None, metadata=field_metadata)
    max_width: Optional[int] = field(default=None, metadata=field_metadata)
    min_width: Optional[int] = field(default=None, metadata=field_metadata)
    precision: Optional[int] = field(default=None, metadata=field_metadata)
    sortable: Optional[int] = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesPositionSet(Base):
    positions: Tuple[IndicesPositionInput, ...] = field(default=None, metadata=field_metadata)
    position_date: datetime.date = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditCustomBasketCreateInputs(IndicesConstructRequestTypes):
    ticker: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    pricing_parameters: CreditCustomBasketPricingParameters = field(default=None, metadata=field_metadata)
    position_set: Tuple[PositionPriceInput, ...] = field(default=None, metadata=field_metadata)
    return_type: IndexCalculationType = field(default='Price Return', metadata=field_metadata)
    styles: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    asset_class: Optional[AssetClass] = field(default='Credit', metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    related_content: Optional[GIRDomain] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    publish_parameters: Optional[PublishParameters] = field(default=None, metadata=field_metadata)
    index_notes: Optional[str] = field(default=None, metadata=field_metadata)
    flagship: Optional[bool] = field(default=False, metadata=field_metadata)
    on_behalf_of: Optional[str] = field(default=None, metadata=field_metadata)
    clone_parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CreditCustomBasketRebalanceInputs(IndicesRebalanceInputTypes):
    asset_class: AssetClass = field(default='Credit', metadata=field_metadata)
    position_set: Tuple[PositionPriceInput, ...] = field(default=None, metadata=field_metadata)
    publish_parameters: Optional[PublishParameters] = field(default=None, metadata=field_metadata)
    pricing_parameters: Optional[CreditCustomBasketPricingParameters] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)
    save_as_draft: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsBackcastInputs(Base):
    position_set: Tuple[IndicesPositionSet, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsCreateInputs(IndicesConstructRequestTypes):
    ticker: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    pricing_parameters: CustomBasketsPricingParameters = field(default=None, metadata=field_metadata)
    position_set: Tuple[PositionPriceInput, ...] = field(default=None, metadata=field_metadata)
    return_type: str = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    styles: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    related_content: Optional[GIRDomain] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)
    clone_parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    publish_parameters: Optional[PublishParameters] = field(default=None, metadata=field_metadata)
    index_notes: Optional[str] = field(default=None, metadata=field_metadata)
    flagship: Optional[bool] = field(default=None, metadata=field_metadata)
    on_behalf_of: Optional[str] = field(default=None, metadata=field_metadata)
    allow_limited_access_assets: Optional[bool] = field(default=False, metadata=field_metadata)
    allow_ca_restricted_assets: Optional[bool] = field(default=False, metadata=config(field_name='allowCARestrictedAssets', exclude=exclude_none))
    vendor: Optional[str] = field(default=None, metadata=field_metadata)
    default_backcast: Optional[bool] = field(default=True, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsEditInputs(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    styles: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    related_content: Optional[GIRDomain] = field(default=None, metadata=field_metadata)
    publish_parameters: Optional[PublishParameters] = field(default=None, metadata=field_metadata)
    index_notes: Optional[str] = field(default=None, metadata=field_metadata)
    index_not_trading_reasons: Optional[IndexNotTradingReasons] = field(default=None, metadata=field_metadata)
    flagship: Optional[bool] = field(default=None, metadata=field_metadata)
    clone_parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CustomBasketsRebalanceInputs(Base):
    position_set: Optional[Tuple[PositionPriceInput, ...]] = field(default=None, metadata=field_metadata)
    publish_parameters: Optional[PublishParameters] = field(default=None, metadata=field_metadata)
    pricing_parameters: Optional[CustomBasketsPricingParameters] = field(default=None, metadata=field_metadata)
    allow_limited_access_assets: Optional[bool] = field(default=False, metadata=field_metadata)
    allow_ca_restricted_assets: Optional[bool] = field(default=False, metadata=config(field_name='allowCARestrictedAssets', exclude=exclude_none))
    allow_system_approval: Optional[bool] = field(default=False, metadata=field_metadata)
    clone_parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    save_as_draft: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DynamicConstructionResponse(IndicesConstructResponseTypes):
    action: Optional[object] = field(default=None, metadata=field_metadata)
    columns: Optional[Tuple[ISelectConstituentColumn, ...]] = field(default=None, metadata=field_metadata)
    constituent_validations: Optional[tuple] = field(default=None, metadata=field_metadata)
    date_validation_status: Optional[str] = field(default=None, metadata=field_metadata)
    types: Optional[tuple] = field(default=None, metadata=field_metadata)
    date_validations: Optional[tuple] = field(default=None, metadata=field_metadata)
    new_parameters: Optional[Tuple[ISelectNewParameter, ...]] = field(default=None, metadata=field_metadata)
    index_type: Optional[str] = field(default=None, metadata=field_metadata)
    index_parameter_definitions: Optional[tuple] = field(default=None, metadata=field_metadata)
    index_metadata: Optional[tuple] = field(default=None, metadata=field_metadata)
    index_parameters: Optional[tuple] = field(default=None, metadata=field_metadata)
    index_parameter_validation: Optional[tuple] = field(default=None, metadata=field_metadata)
    status: Optional[object] = field(default=None, metadata=field_metadata)
    valid: Optional[int] = field(default=None, metadata=field_metadata)
    validation_messages: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectRebalance(Base):
    new_weights: Optional[Tuple[ISelectNewWeight, ...]] = field(default=None, metadata=field_metadata)
    rebalance_date: Optional[str] = field(default=None, metadata=field_metadata)
    new_parameters: Optional[Tuple[ISelectNewParameter, ...]] = field(default=None, metadata=field_metadata)
    index_parameters: Optional[Tuple[ISelectIndexParameters, ...]] = field(default=None, metadata=field_metadata)
    waiver_requested: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectRequest(IndicesRebalanceInputTypes):
    rebalance_date: str = field(default=None, metadata=field_metadata)
    request_counter: int = field(default=None, metadata=field_metadata)
    use_new_rebalance_interface: bool = field(default=None, metadata=field_metadata)
    new_parameters: Optional[Tuple[ISelectNewParameter, ...]] = field(default=None, metadata=field_metadata)
    index_parameters: Optional[Tuple[ISelectIndexParameter, ...]] = field(default=None, metadata=field_metadata)
    new_weights: Optional[Tuple[ISelectNewWeight, ...]] = field(default=None, metadata=field_metadata)
    new_units: Optional[Tuple[ISelectNewUnit, ...]] = field(default=None, metadata=field_metadata)
    entry_type: Optional[str] = field(default=None, metadata=field_metadata)
    waiver_requested: Optional[bool] = field(default=None, metadata=field_metadata)
    presubmit: Optional[bool] = field(default=None, metadata=field_metadata)
    requester_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectResponse(Base):
    action: Optional[object] = field(default=None, metadata=config(field_name='Action', exclude=exclude_none))
    action_comment: Optional[str] = field(default=None, metadata=config(field_name='ActionComment', exclude=exclude_none))
    asset_name: Optional[str] = field(default=None, metadata=field_metadata)
    asset_short_name: Optional[str] = field(default=None, metadata=field_metadata)
    available_action_confirms: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    available_actions: Optional[tuple] = field(default=None, metadata=field_metadata)
    available_rebalance_dates: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    constituent_validations: Optional[tuple] = field(default=None, metadata=field_metadata)
    date_validation_status: Optional[str] = field(default=None, metadata=field_metadata)
    date_validations: Optional[tuple] = field(default=None, metadata=field_metadata)
    entry_mode: Optional[str] = field(default=None, metadata=field_metadata)
    entry_type: Optional[str] = field(default=None, metadata=field_metadata)
    internal_rebalance: Optional[int] = field(default=None, metadata=field_metadata)
    index_parameter_definitions: Optional[tuple] = field(default=None, metadata=field_metadata)
    index_parameters: Optional[tuple] = field(default=None, metadata=field_metadata)
    index_parameter_validation: Optional[tuple] = field(default=None, metadata=field_metadata)
    new_units: Optional[Tuple[ISelectNewUnit, ...]] = field(default=None, metadata=field_metadata)
    new_weights: Optional[Tuple[ISelectNewWeight, ...]] = field(default=None, metadata=field_metadata)
    notification_date: Optional[str] = field(default=None, metadata=field_metadata)
    rebalance_date: Optional[str] = field(default=None, metadata=field_metadata)
    rebalance_determination_date: Optional[str] = field(default=None, metadata=field_metadata)
    reb_determination_index_level: Optional[float] = field(default=None, metadata=field_metadata)
    request_counter: Optional[int] = field(default=None, metadata=field_metadata)
    series: Optional[ISelectSeries] = field(default=None, metadata=field_metadata)
    status: Optional[object] = field(default=None, metadata=field_metadata)
    submission_data: Optional[tuple] = field(default=None, metadata=field_metadata)
    submission_data_columns: Optional[Tuple[ISelectConstituentColumn, ...]] = field(default=None, metadata=field_metadata)
    submission_text: Optional[str] = field(default=None, metadata=field_metadata)
    valid: Optional[int] = field(default=None, metadata=field_metadata)
    validation_messages: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesDynamicConstructInputs(IndicesConstructRequestTypes):
    index_type: str = field(default=None, metadata=field_metadata)
    new_parameters: Tuple[ISelectNewParameter, ...] = field(default=None, metadata=field_metadata)
    index_parameters: Tuple[ISelectIndexParameters, ...] = field(default=None, metadata=field_metadata)
    index_metadata: Tuple[ISelectIndexParameters, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesBackcastInputs(Base):
    parameters: CustomBasketsBackcastInputs = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesEditInputs(Base):
    parameters: CustomBasketsEditInputs = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndicesRebalanceInputs(IndicesRebalanceInputTypes):
    parameters: DictBase = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ApprovalCustomBasketResponse(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    positions_to_rebalance: PositionSet = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    status: Optional[ApprovalStatus] = field(default=None, metadata=field_metadata)
    parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    approved_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    approved_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    submitted_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    submitted_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    comments: Optional[Tuple[ApprovalComment, ...]] = field(default=None, metadata=field_metadata)
    notifyees: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    action_type: Optional[object] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
