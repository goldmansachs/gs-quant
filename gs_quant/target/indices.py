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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class IndicesCurrency(EnumBase, Enum):    
    
    """Currencies supported for Indices"""

    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    CAD = 'CAD'
    AUD = 'AUD'
    CHF = 'CHF'
    CNY = 'CNY'
    DKK = 'DKK'
    HKD = 'HKD'
    IDR = 'IDR'
    INR = 'INR'
    JPY = 'JPY'
    KRW = 'KRW'
    MXN = 'MXN'
    MYR = 'MYR'
    NOK = 'NOK'
    NZD = 'NZD'
    PHP = 'PHP'
    RUB = 'RUB'
    SEK = 'SEK'
    SGD = 'SGD'
    THB = 'THB'
    TRY = 'TRY'
    TWD = 'TWD'
    ZAR = 'ZAR'
    BRL = 'BRL'
    
    def __repr__(self):
        return self.value


class ApprovalAction(Base):
        
    """Comments for the approval action"""

    @camel_case_translate
    def __init__(
        self,
        comment: str = None,
        name: str = None
    ):        
        super().__init__()
        self.comment = comment
        self.name = name

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self._property_changed('comment')
        self.__comment = value        


class CustomBasketsResponse(Base):
        
    """Rebalance custom basket response"""

    @camel_case_translate
    def __init__(
        self,
        status: str = None,
        approval_id: str = None,
        report_id: str = None,
        asset_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.approval_id = approval_id
        self.report_id = report_id
        self.asset_id = asset_id
        self.name = name

    @property
    def status(self) -> str:
        """Indices rebalance process status. Status is done if basket assets rebalance,
           report creation and scheduling are all successfully executed."""
        return self.__status

    @status.setter
    def status(self, value: str):
        self._property_changed('status')
        self.__status = value        

    @property
    def approval_id(self) -> str:
        """Marquee unique identifier of approval created"""
        return self.__approval_id

    @approval_id.setter
    def approval_id(self, value: str):
        self._property_changed('approval_id')
        self.__approval_id = value        

    @property
    def report_id(self) -> str:
        """Marquee unique identifier of report created"""
        return self.__report_id

    @report_id.setter
    def report_id(self, value: str):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def asset_id(self) -> str:
        """Marquee unique identifier of asset created"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        


class ISelectConstituentColumn(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        field: str,
        name: str,
        aggregator_string: str = None,
        class_: str = None,
        filter_: str = None,
        formatter_string: str = None,
        ID: int = None,
        max_width: int = None,
        min_width: int = None,
        precision: int = None,
        sortable: int = None,
        tooltip: str = None
    ):        
        super().__init__()
        self.aggregator_string = aggregator_string
        self.__class = class_
        self.field = field
        self.__filter = filter_
        self.formatter_string = formatter_string
        self.__id = id_
        self.ID = ID
        self.max_width = max_width
        self.min_width = min_width
        self.name = name
        self.precision = precision
        self.sortable = sortable
        self.tooltip = tooltip

    @property
    def aggregator_string(self) -> str:
        return self.__aggregator_string

    @aggregator_string.setter
    def aggregator_string(self, value: str):
        self._property_changed('aggregator_string')
        self.__aggregator_string = value        

    @property
    def class_(self) -> str:
        return self.__class

    @class_.setter
    def class_(self, value: str):
        self._property_changed('class_')
        self.__class = value        

    @property
    def field(self) -> str:
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def filter(self) -> str:
        return self.__filter

    @filter.setter
    def filter(self, value: str):
        self._property_changed('filter')
        self.__filter = value        

    @property
    def formatter_string(self) -> str:
        return self.__formatter_string

    @formatter_string.setter
    def formatter_string(self, value: str):
        self._property_changed('formatter_string')
        self.__formatter_string = value        

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def ID(self) -> int:
        return self.__ID

    @ID.setter
    def ID(self, value: int):
        self._property_changed('ID')
        self.__ID = value        

    @property
    def max_width(self) -> int:
        return self.__max_width

    @max_width.setter
    def max_width(self, value: int):
        self._property_changed('max_width')
        self.__max_width = value        

    @property
    def min_width(self) -> int:
        return self.__min_width

    @min_width.setter
    def min_width(self, value: int):
        self._property_changed('min_width')
        self.__min_width = value        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def precision(self) -> int:
        return self.__precision

    @precision.setter
    def precision(self, value: int):
        self._property_changed('precision')
        self.__precision = value        

    @property
    def sortable(self) -> int:
        return self.__sortable

    @sortable.setter
    def sortable(self, value: int):
        self._property_changed('sortable')
        self.__sortable = value        

    @property
    def tooltip(self) -> str:
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class ISelectIndexParameters(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        value: float = None
    ):        
        super().__init__()
        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        


class ISelectSeries(Base):
        
    @camel_case_translate
    def __init__(
        self,
        data: tuple = None,
        identifier: str = None,
        identifier_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.data = data
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.name = name

    @property
    def data(self) -> tuple:
        return self.__data

    @data.setter
    def data(self, value: tuple):
        self._property_changed('data')
        self.__data = value        

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def identifier_type(self) -> str:
        return self.__identifier_type

    @identifier_type.setter
    def identifier_type(self, value: str):
        self._property_changed('identifier_type')
        self.__identifier_type = value        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class PositionPriceInput(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        quantity: float = None,
        weight: float = None,
        notional: float = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.quantity = quantity
        self.weight = weight
        self.notional = notional
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique identifier"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def quantity(self) -> float:
        """Quantity of the given position"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def weight(self) -> float:
        """Relative weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        

    @property
    def notional(self) -> float:
        """Notional of the given position"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        


class PublishParameters(Base):
        
    """Publishing parameters to determine where and how to publish indices, default all
       to false"""

    @camel_case_translate
    def __init__(
        self,
        publish_to_reuters: bool,
        publish_to_bloomberg: bool,
        include_price_history: bool,
        name: str = None
    ):        
        super().__init__()
        self.include_price_history = include_price_history
        self.publish_to_bloomberg = publish_to_bloomberg
        self.publish_to_reuters = publish_to_reuters
        self.name = name

    @property
    def include_price_history(self) -> bool:
        """Include full price history, default to false"""
        return self.__include_price_history

    @include_price_history.setter
    def include_price_history(self, value: bool):
        self._property_changed('include_price_history')
        self.__include_price_history = value        

    @property
    def publish_to_bloomberg(self) -> bool:
        """Publish Basket to Bloomberg, default to false"""
        return self.__publish_to_bloomberg

    @publish_to_bloomberg.setter
    def publish_to_bloomberg(self, value: bool):
        self._property_changed('publish_to_bloomberg')
        self.__publish_to_bloomberg = value        

    @property
    def publish_to_reuters(self) -> bool:
        """Publish Basket to Reuters, default to false"""
        return self.__publish_to_reuters

    @publish_to_reuters.setter
    def publish_to_reuters(self, value: bool):
        self._property_changed('publish_to_reuters')
        self.__publish_to_reuters = value        


class CustomBasketsEditInputs(Base):
        
    """parameters used to edit a basket"""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        description: str = None,
        styles: Tuple[str, ...] = None,
        related_content: GIRDomain = None,
        publish_parameters: PublishParameters = None
    ):        
        super().__init__()
        self.name = name
        self.description = description
        self.styles = styles
        self.related_content = related_content
        self.publish_parameters = publish_parameters

    @property
    def name(self) -> str:
        """Display name of the basket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the asset (max 50)"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def related_content(self) -> GIRDomain:
        return self.__related_content

    @related_content.setter
    def related_content(self, value: GIRDomain):
        self._property_changed('related_content')
        self.__related_content = value        

    @property
    def publish_parameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish indices, default all
           to false"""
        return self.__publish_parameters

    @publish_parameters.setter
    def publish_parameters(self, value: PublishParameters):
        self._property_changed('publish_parameters')
        self.__publish_parameters = value        


class ISelectRebalance(Base):
        
    @camel_case_translate
    def __init__(
        self,
        new_weights: Tuple[ISelectNewWeight, ...] = None,
        rebalance_date: str = None,
        new_parameters: Tuple[ISelectNewParameter, ...] = None,
        index_parameters: Tuple[ISelectIndexParameters, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.new_weights = new_weights
        self.rebalance_date = rebalance_date
        self.new_parameters = new_parameters
        self.index_parameters = index_parameters
        self.name = name

    @property
    def new_weights(self) -> Tuple[ISelectNewWeight, ...]:
        """New Weight array to be updated"""
        return self.__new_weights

    @new_weights.setter
    def new_weights(self, value: Tuple[ISelectNewWeight, ...]):
        self._property_changed('new_weights')
        self.__new_weights = value        

    @property
    def rebalance_date(self) -> str:
        """Date the rebalance will occur"""
        return self.__rebalance_date

    @rebalance_date.setter
    def rebalance_date(self, value: str):
        self._property_changed('rebalance_date')
        self.__rebalance_date = value        

    @property
    def new_parameters(self) -> Tuple[ISelectNewParameter, ...]:
        """New parameters to be updated"""
        return self.__new_parameters

    @new_parameters.setter
    def new_parameters(self, value: Tuple[ISelectNewParameter, ...]):
        self._property_changed('new_parameters')
        self.__new_parameters = value        

    @property
    def index_parameters(self) -> Tuple[ISelectIndexParameters, ...]:
        """Index parameters to be updated"""
        return self.__index_parameters

    @index_parameters.setter
    def index_parameters(self, value: Tuple[ISelectIndexParameters, ...]):
        self._property_changed('index_parameters')
        self.__index_parameters = value        


class ISelectResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        action=None,
        action_comment: str = None,
        asset_name: str = None,
        asset_short_name: str = None,
        available_action_confirms: Tuple[Tuple[str, ...], ...] = None,
        available_actions: tuple = None,
        available_rebalance_dates: Tuple[str, ...] = None,
        constituent_validations: tuple = None,
        date_validation_status: str = None,
        date_validations: tuple = None,
        entry_mode: str = None,
        entry_type: str = None,
        internal_rebalance: int = None,
        index_parameter_definitions: tuple = None,
        index_parameters: tuple = None,
        index_parameter_validation: tuple = None,
        new_units: Tuple[ISelectNewUnit, ...] = None,
        new_weights: Tuple[ISelectNewWeight, ...] = None,
        notification_date: str = None,
        rebalance_date: str = None,
        rebalance_determination_date: str = None,
        reb_determination_index_level: float = None,
        request_counter: int = None,
        series: ISelectSeries = None,
        status=None,
        submission_data: tuple = None,
        submission_data_columns: Tuple[ISelectConstituentColumn, ...] = None,
        submission_text: str = None,
        valid: int = None,
        validation_messages: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.action = action
        self.action_comment = action_comment
        self.asset_name = asset_name
        self.asset_short_name = asset_short_name
        self.available_action_confirms = available_action_confirms
        self.available_actions = available_actions
        self.available_rebalance_dates = available_rebalance_dates
        self.constituent_validations = constituent_validations
        self.date_validation_status = date_validation_status
        self.date_validations = date_validations
        self.entry_mode = entry_mode
        self.entry_type = entry_type
        self.internal_rebalance = internal_rebalance
        self.index_parameter_definitions = index_parameter_definitions
        self.index_parameters = index_parameters
        self.index_parameter_validation = index_parameter_validation
        self.new_units = new_units
        self.new_weights = new_weights
        self.notification_date = notification_date
        self.rebalance_date = rebalance_date
        self.rebalance_determination_date = rebalance_determination_date
        self.reb_determination_index_level = reb_determination_index_level
        self.request_counter = request_counter
        self.series = series
        self.status = status
        self.submission_data = submission_data
        self.submission_data_columns = submission_data_columns
        self.submission_text = submission_text
        self.valid = valid
        self.validation_messages = validation_messages
        self.name = name

    @property
    def action(self):
        """Rebalance type"""
        return self.__action

    @action.setter
    def action(self, value):
        self._property_changed('action')
        self.__action = value        

    @property
    def action_comment(self) -> str:
        """Comment for request the action"""
        return self.__action_comment

    @action_comment.setter
    def action_comment(self, value: str):
        self._property_changed('action_comment')
        self.__action_comment = value        

    @property
    def asset_name(self) -> str:
        """Asset name"""
        return self.__asset_name

    @asset_name.setter
    def asset_name(self, value: str):
        self._property_changed('asset_name')
        self.__asset_name = value        

    @property
    def asset_short_name(self) -> str:
        """Short name of asset which can be displayed where there are constraints on space."""
        return self.__asset_short_name

    @asset_short_name.setter
    def asset_short_name(self, value: str):
        self._property_changed('asset_short_name')
        self.__asset_short_name = value        

    @property
    def available_action_confirms(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__available_action_confirms

    @available_action_confirms.setter
    def available_action_confirms(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('available_action_confirms')
        self.__available_action_confirms = value        

    @property
    def available_actions(self) -> tuple:
        return self.__available_actions

    @available_actions.setter
    def available_actions(self, value: tuple):
        self._property_changed('available_actions')
        self.__available_actions = value        

    @property
    def available_rebalance_dates(self) -> Tuple[str, ...]:
        return self.__available_rebalance_dates

    @available_rebalance_dates.setter
    def available_rebalance_dates(self, value: Tuple[str, ...]):
        self._property_changed('available_rebalance_dates')
        self.__available_rebalance_dates = value        

    @property
    def constituent_validations(self) -> tuple:
        return self.__constituent_validations

    @constituent_validations.setter
    def constituent_validations(self, value: tuple):
        self._property_changed('constituent_validations')
        self.__constituent_validations = value        

    @property
    def date_validation_status(self) -> str:
        return self.__date_validation_status

    @date_validation_status.setter
    def date_validation_status(self, value: str):
        self._property_changed('date_validation_status')
        self.__date_validation_status = value        

    @property
    def date_validations(self) -> tuple:
        return self.__date_validations

    @date_validations.setter
    def date_validations(self, value: tuple):
        self._property_changed('date_validations')
        self.__date_validations = value        

    @property
    def entry_mode(self) -> str:
        return self.__entry_mode

    @entry_mode.setter
    def entry_mode(self, value: str):
        self._property_changed('entry_mode')
        self.__entry_mode = value        

    @property
    def entry_type(self) -> str:
        return self.__entry_type

    @entry_type.setter
    def entry_type(self, value: str):
        self._property_changed('entry_type')
        self.__entry_type = value        

    @property
    def internal_rebalance(self) -> int:
        """Indicate if Workflow Sender User is internal user"""
        return self.__internal_rebalance

    @internal_rebalance.setter
    def internal_rebalance(self, value: int):
        self._property_changed('internal_rebalance')
        self.__internal_rebalance = value        

    @property
    def index_parameter_definitions(self) -> tuple:
        return self.__index_parameter_definitions

    @index_parameter_definitions.setter
    def index_parameter_definitions(self, value: tuple):
        self._property_changed('index_parameter_definitions')
        self.__index_parameter_definitions = value        

    @property
    def index_parameters(self) -> tuple:
        return self.__index_parameters

    @index_parameters.setter
    def index_parameters(self, value: tuple):
        self._property_changed('index_parameters')
        self.__index_parameters = value        

    @property
    def index_parameter_validation(self) -> tuple:
        return self.__index_parameter_validation

    @index_parameter_validation.setter
    def index_parameter_validation(self, value: tuple):
        self._property_changed('index_parameter_validation')
        self.__index_parameter_validation = value        

    @property
    def new_units(self) -> Tuple[ISelectNewUnit, ...]:
        return self.__new_units

    @new_units.setter
    def new_units(self, value: Tuple[ISelectNewUnit, ...]):
        self._property_changed('new_units')
        self.__new_units = value        

    @property
    def new_weights(self) -> Tuple[ISelectNewWeight, ...]:
        return self.__new_weights

    @new_weights.setter
    def new_weights(self, value: Tuple[ISelectNewWeight, ...]):
        self._property_changed('new_weights')
        self.__new_weights = value        

    @property
    def notification_date(self) -> str:
        return self.__notification_date

    @notification_date.setter
    def notification_date(self, value: str):
        self._property_changed('notification_date')
        self.__notification_date = value        

    @property
    def rebalance_date(self) -> str:
        return self.__rebalance_date

    @rebalance_date.setter
    def rebalance_date(self, value: str):
        self._property_changed('rebalance_date')
        self.__rebalance_date = value        

    @property
    def rebalance_determination_date(self) -> str:
        return self.__rebalance_determination_date

    @rebalance_determination_date.setter
    def rebalance_determination_date(self, value: str):
        self._property_changed('rebalance_determination_date')
        self.__rebalance_determination_date = value        

    @property
    def reb_determination_index_level(self) -> float:
        return self.__reb_determination_index_level

    @reb_determination_index_level.setter
    def reb_determination_index_level(self, value: float):
        self._property_changed('reb_determination_index_level')
        self.__reb_determination_index_level = value        

    @property
    def request_counter(self) -> int:
        return self.__request_counter

    @request_counter.setter
    def request_counter(self, value: int):
        self._property_changed('request_counter')
        self.__request_counter = value        

    @property
    def series(self) -> ISelectSeries:
        return self.__series

    @series.setter
    def series(self, value: ISelectSeries):
        self._property_changed('series')
        self.__series = value        

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self._property_changed('status')
        self.__status = value        

    @property
    def submission_data(self) -> tuple:
        return self.__submission_data

    @submission_data.setter
    def submission_data(self, value: tuple):
        self._property_changed('submission_data')
        self.__submission_data = value        

    @property
    def submission_data_columns(self) -> Tuple[ISelectConstituentColumn, ...]:
        return self.__submission_data_columns

    @submission_data_columns.setter
    def submission_data_columns(self, value: Tuple[ISelectConstituentColumn, ...]):
        self._property_changed('submission_data_columns')
        self.__submission_data_columns = value        

    @property
    def submission_text(self) -> str:
        return self.__submission_text

    @submission_text.setter
    def submission_text(self, value: str):
        self._property_changed('submission_text')
        self.__submission_text = value        

    @property
    def valid(self) -> int:
        return self.__valid

    @valid.setter
    def valid(self, value: int):
        self._property_changed('valid')
        self.__valid = value        

    @property
    def validation_messages(self) -> Tuple[str, ...]:
        return self.__validation_messages

    @validation_messages.setter
    def validation_messages(self, value: Tuple[str, ...]):
        self._property_changed('validation_messages')
        self.__validation_messages = value        


class IndicesPriceParameters(Base):
        
    """Parameters for pricing indices"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[IndicesCurrency, str] = None,
        divisor: float = None,
        initial_price: float = None,
        target_notional: float = None,
        weighting_strategy: str = None,
        reweight: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.divisor = divisor
        self.initial_price = initial_price
        self.target_notional = target_notional
        self.weighting_strategy = weighting_strategy
        self.reweight = reweight
        self.name = name

    @property
    def currency(self) -> Union[IndicesCurrency, str]:
        """Currencies supported for Indices Create, default to USD during create. During
           rebalance, cannot change basket currency hence the input value will
           be discarded."""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[IndicesCurrency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(IndicesCurrency, value)        

    @property
    def divisor(self) -> float:
        """Divisor to be applied to the overall position set"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: float):
        self._property_changed('divisor')
        self.__divisor = value        

    @property
    def initial_price(self) -> float:
        """Initial overall price for the position set"""
        return self.__initial_price

    @initial_price.setter
    def initial_price(self, value: float):
        self._property_changed('initial_price')
        self.__initial_price = value        

    @property
    def target_notional(self) -> float:
        """Target notional for the position set"""
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: float):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def weighting_strategy(self) -> str:
        """Strategy used to price the position set. If not supplied, it is inferred from
           the quantities or weights in the positions."""
        return self.__weighting_strategy

    @weighting_strategy.setter
    def weighting_strategy(self, value: str):
        self._property_changed('weighting_strategy')
        self.__weighting_strategy = value        

    @property
    def reweight(self) -> bool:
        """To reweight positions if input weights don't add up to 1, default to false"""
        return self.__reweight

    @reweight.setter
    def reweight(self, value: bool):
        self._property_changed('reweight')
        self.__reweight = value        


class CustomBasketsRebalanceInputs(Base):
        
    """Inputs used to rebalance a custom basket"""

    @camel_case_translate
    def __init__(
        self,
        position_set: Tuple[PositionPriceInput, ...] = None,
        publish_parameters: PublishParameters = None,
        pricing_parameters: IndicesPriceParameters = None,
        name: str = None
    ):        
        super().__init__()
        self.position_set = position_set
        self.publish_parameters = publish_parameters
        self.pricing_parameters = pricing_parameters
        self.name = name

    @property
    def position_set(self) -> Tuple[PositionPriceInput, ...]:
        """Information of constituents associated with the rebalance."""
        return self.__position_set

    @position_set.setter
    def position_set(self, value: Tuple[PositionPriceInput, ...]):
        self._property_changed('position_set')
        self.__position_set = value        

    @property
    def publish_parameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish indices, default all
           to false"""
        return self.__publish_parameters

    @publish_parameters.setter
    def publish_parameters(self, value: PublishParameters):
        self._property_changed('publish_parameters')
        self.__publish_parameters = value        

    @property
    def pricing_parameters(self) -> IndicesPriceParameters:
        """Parameters for pricing indices"""
        return self.__pricing_parameters

    @pricing_parameters.setter
    def pricing_parameters(self, value: IndicesPriceParameters):
        self._property_changed('pricing_parameters')
        self.__pricing_parameters = value        


class IndicesCreateInputs(Base):
        
    """Inputs used to create an index"""

    @camel_case_translate
    def __init__(
        self,
        ticker: str,
        name: str,
        pricing_parameters: IndicesPriceParameters,
        position_set: Tuple[PositionPriceInput, ...],
        description: str = None,
        styles: Tuple[str, ...] = None,
        related_content: GIRDomain = None,
        index_create_source: Union[IndexCreateSource, str] = None,
        return_type: str = 'Price Return',
        publish_parameters: PublishParameters = None,
        on_behalf_of: str = None
    ):        
        super().__init__()
        self.ticker = ticker
        self.name = name
        self.description = description
        self.styles = styles
        self.related_content = related_content
        self.index_create_source = index_create_source
        self.return_type = return_type
        self.position_set = position_set
        self.publish_parameters = publish_parameters
        self.pricing_parameters = pricing_parameters
        self.on_behalf_of = on_behalf_of

    @property
    def ticker(self) -> str:
        """Ticker Identifier of the new asset (Prefix with 'GS' to publish to Bloomberg)"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def name(self) -> str:
        """Display name of the index"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Free text description of asset, default to empty. Description provided will be
           indexed in the search service for free text relevance match."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the asset (max 50), default to Bespoke"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def related_content(self) -> GIRDomain:
        """Links to content related to this index or any of its constituents (optional)"""
        return self.__related_content

    @related_content.setter
    def related_content(self, value: GIRDomain):
        self._property_changed('related_content')
        self.__related_content = value        

    @property
    def index_create_source(self) -> Union[IndexCreateSource, str]:
        """Source of basket create"""
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: Union[IndexCreateSource, str]):
        self._property_changed('index_create_source')
        self.__index_create_source = get_enum_value(IndexCreateSource, value)        

    @property
    def return_type(self) -> str:
        """Determines the index calculation methodology with respect to dividend
           reinvestment, default to Price Return"""
        return self.__return_type

    @return_type.setter
    def return_type(self, value: str):
        self._property_changed('return_type')
        self.__return_type = value        

    @property
    def position_set(self) -> Tuple[PositionPriceInput, ...]:
        """Information of constituents associated with the index. Need to supply one of
           weight, quantity."""
        return self.__position_set

    @position_set.setter
    def position_set(self, value: Tuple[PositionPriceInput, ...]):
        self._property_changed('position_set')
        self.__position_set = value        

    @property
    def publish_parameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish indices, default all
           to false"""
        return self.__publish_parameters

    @publish_parameters.setter
    def publish_parameters(self, value: PublishParameters):
        self._property_changed('publish_parameters')
        self.__publish_parameters = value        

    @property
    def pricing_parameters(self) -> IndicesPriceParameters:
        """Parameters for pricing indices"""
        return self.__pricing_parameters

    @pricing_parameters.setter
    def pricing_parameters(self, value: IndicesPriceParameters):
        self._property_changed('pricing_parameters')
        self.__pricing_parameters = value        

    @property
    def on_behalf_of(self) -> str:
        """Marquee unique identifier"""
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        


class IndicesEditInputs(Base):
        
    @camel_case_translate
    def __init__(
        self,
        parameters: CustomBasketsEditInputs,
        name: str = None
    ):        
        super().__init__()
        self.parameters = parameters
        self.name = name

    @property
    def parameters(self) -> CustomBasketsEditInputs:
        """The inputs used to edit an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: CustomBasketsEditInputs):
        self._property_changed('parameters')
        self.__parameters = value        


class IndicesRebalanceInputs(Base):
        
    @camel_case_translate
    def __init__(
        self,
        parameters: dict,
        name: str = None
    ):        
        super().__init__()
        self.parameters = parameters
        self.name = name

    @property
    def parameters(self) -> dict:
        """The inputs used to rebalance an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        
