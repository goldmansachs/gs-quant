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

import datetime

from enum import Enum
from typing import Mapping, Tuple, Union

from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value
from gs_quant.target.common import PositionSet as PosSet, OptionType

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
    
    def __repr__(self):
        return self.value


class CreditOptionStrikeType(EnumBase, Enum):    
    
    Spread_Adj = 'Spread Adj'
    Delta = 'Delta'
    
    def __repr__(self):
        return self.value


class CreditOptionType(EnumBase, Enum):    
    
    Payer = 'Payer'
    Receiver = 'Receiver'
    
    def __repr__(self):
        return self.value


class IndexNotTradingReasons(EnumBase, Enum):    
    
    """Reasons the index was not traded"""

    Cost = 'Cost'
    Client_does_not_like_the_construction = 'Client does not like the construction'
    Basket_created_prematurely = 'Basket created prematurely'
    Economics_of_the_basket_changed__client_no_longer_interested_in_trading = 'Economics of the basket changed: client no longer interested in trading'
    GS_booking_OVER_operational_issues = 'GS booking/operational issues'
    _ = ''
    
    def __repr__(self):
        return self.value


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
    SEK = 'SEK'
    SGD = 'SGD'
    THB = 'THB'
    TRY = 'TRY'
    TWD = 'TWD'
    ZAR = 'ZAR'
    BRL = 'BRL'
    
    def __repr__(self):
        return self.value


class MarketDataFrequency(EnumBase, Enum):    
    
    Real_Time = 'Real Time'
    End_Of_Day = 'End Of Day'
    
    def __repr__(self):
        return self.value


class MarketDataVendor(EnumBase, Enum):    
    
    Goldman_Sachs = 'Goldman Sachs'
    Thomson_Reuters = 'Thomson Reuters'
    Solactive = 'Solactive'
    Bloomberg = 'Bloomberg'
    Axioma = 'Axioma'
    Goldman_Sachs_Prime_Services = 'Goldman Sachs Prime Services'
    Goldman_Sachs_Global_Investment_Research = 'Goldman Sachs Global Investment Research'
    National_Weather_Service = 'National Weather Service'
    WM = 'WM'
    Hedge_Fund_Research__Inc_ = 'Hedge Fund Research, Inc.'
    London_Stock_Exchange = 'London Stock Exchange'
    Goldman_Sachs_MDFarm = 'Goldman Sachs MDFarm'
    PredictIt = 'PredictIt'
    Iowa_Electronic_Markets = 'Iowa Electronic Markets'
    RealClearPolitics = 'RealClearPolitics'
    _538 = '538'
    FiveThirtyEight = 'FiveThirtyEight'
    Opinium = 'Opinium'
    YouGov = 'YouGov'
    MorningStar = 'MorningStar'
    Survation = 'Survation'
    Survation__YouGov = 'Survation, YouGov'
    European_Centre_for_Disease_Prevention_and_Control = 'European Centre for Disease Prevention and Control'
    Centers_for_Disease_Control_and_Prevention = 'Centers for Disease Control and Prevention'
    Johns_Hopkins_University = 'Johns Hopkins University'
    Google = 'Google'
    National_Health_Service = 'National Health Service'
    World_Health_Organization = 'World Health Organization'
    Wikipedia = 'Wikipedia'
    StarSchema = 'StarSchema'
    Covid_Working_Group = 'Covid Working Group'
    CovidTracking = 'CovidTracking'
    Bing = 'Bing'
    FRED = 'FRED'
    Institute_for_Health_Metrics_and_Evaluation = 'Institute for Health Metrics and Evaluation'
    Refinitiv = 'Refinitiv'
    Goldman_Sachs_Global_Investment_Research__Refinitiv = 'Goldman Sachs Global Investment Research, Refinitiv'
    EPFR = 'EPFR'
    Coin_Metrics = 'Coin Metrics'
    MSCI = 'MSCI'
    
    def __repr__(self):
        return self.value


class OptionExpiryType(EnumBase, Enum):    
    
    _1m = '1m'
    _2m = '2m'
    _3m = '3m'
    _4m = '4m'
    _5m = '5m'
    _6m = '6m'
    
    def __repr__(self):
        return self.value


class OptionStrikeType(EnumBase, Enum):    
    
    Relative = 'Relative'
    Delta = 'Delta'
    
    def __repr__(self):
        return self.value


class StrikeMethodType(EnumBase, Enum):    
    
    Spread = 'Spread'
    Delta = 'Delta'
    Percentage_of_Price = 'Percentage of Price'
    Fixed = 'Fixed'
    
    def __repr__(self):
        return self.value


class TradeType(EnumBase, Enum):    
    
    """Direction"""

    Buy = 'Buy'
    Sell = 'Sell'
    
    def __repr__(self):
        return self.value


class ApprovalComment(Base):
        
    @camel_case_translate
    def __init__(
        self,
        timestamp: datetime.datetime = None,
        message: str = None,
        name: str = None
    ):        
        super().__init__()
        self.timestamp = timestamp
        self.message = message
        self.name = name

    @property
    def timestamp(self) -> datetime.datetime:
        """Timestamp of when the comment was made."""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        self._property_changed('timestamp')
        self.__timestamp = value        

    @property
    def message(self) -> str:
        """The message of the comment."""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        


class CustomBasketRiskParams(Base):
        
    """parameters used to schedule, edit, and delete risk reports for a basket"""

    @camel_case_translate
    def __init__(
        self,
        risk_model: str = None,
        fx_hedged: bool = None,
        delete: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.risk_model = risk_model
        self.fx_hedged = fx_hedged
        self.delete = delete
        self.name = name

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def fx_hedged(self) -> bool:
        """Assume portfolio is FX Hedged"""
        return self.__fx_hedged

    @fx_hedged.setter
    def fx_hedged(self, value: bool):
        self._property_changed('fx_hedged')
        self.__fx_hedged = value        

    @property
    def delete(self) -> bool:
        """Whether or not the risk report is to be deleted"""
        return self.__delete

    @delete.setter
    def delete(self, value: bool):
        self._property_changed('delete')
        self.__delete = value        


class CustomBasketsRebalanceAction(Base):
        
    """Comments for the rebalance action"""

    @camel_case_translate
    def __init__(
        self,
        comment: str = None,
        action_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.comment = comment
        self.action_type = action_type
        self.name = name

    @property
    def comment(self) -> str:
        """Free text to mention the reason for cancelling rebalance"""
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self._property_changed('comment')
        self.__comment = value        

    @property
    def action_type(self) -> str:
        return self.__action_type

    @action_type.setter
    def action_type(self, value: str):
        self._property_changed('action_type')
        self.__action_type = value        


class CustomBasketsResponse(Base):
        
    """Response object for basket creation/edit/rebalance indicating the status of the
       request"""

    @camel_case_translate
    def __init__(
        self,
        status: str = None,
        report_id: str = None,
        asset_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.report_id = report_id
        self.asset_id = asset_id
        self.name = name

    @property
    def status(self) -> str:
        """Basket action request status. Status is done if basket is successfully
           created/updated and report is triggered for downstream updates"""
        return self.__status

    @status.setter
    def status(self, value: str):
        self._property_changed('status')
        self.__status = value        

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


class ISelectActionRequest(Base):
        
    @camel_case_translate
    def __init__(
        self,
        action_comment: str,
        trader_attestations: Tuple[str, ...] = None,
        user_action: str = None,
        name: str = None
    ):        
        super().__init__()
        self.action_comment = action_comment
        self.trader_attestations = trader_attestations
        self.user_action = user_action
        self.name = name

    @property
    def action_comment(self) -> str:
        """Comment for request the action"""
        return self.__action_comment

    @action_comment.setter
    def action_comment(self, value: str):
        self._property_changed('action_comment')
        self.__action_comment = value        

    @property
    def trader_attestations(self) -> Tuple[str, ...]:
        """Attestations for traders when there is a waiver"""
        return self.__trader_attestations

    @trader_attestations.setter
    def trader_attestations(self, value: Tuple[str, ...]):
        self._property_changed('trader_attestations')
        self.__trader_attestations = value        

    @property
    def user_action(self) -> str:
        """What action is the user performing?"""
        return self.__user_action

    @user_action.setter
    def user_action(self, value: str):
        self._property_changed('user_action')
        self.__user_action = value        


class ISelectIndexParameter(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        value: Union[float, str] = None
    ):        
        super().__init__()
        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def value(self) -> Union[float, str]:
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


class ISelectIndexParameters(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        value: Union[float, str] = None
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
    def value(self) -> Union[float, str]:
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


class ISelectNewUnit(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        new_units: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.new_units = new_units
        self.name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def new_units(self) -> float:
        return self.__new_units

    @new_units.setter
    def new_units(self, value: float):
        self._property_changed('new_units')
        self.__new_units = value        


class ISelectNewWeight(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        new_weight: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.new_weight = new_weight
        self.name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def new_weight(self) -> float:
        return self.__new_weight

    @new_weight.setter
    def new_weight(self, value: float):
        self._property_changed('new_weight')
        self.__new_weight = value        


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


class IndicesPositionInput(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        weight: float,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.weight = weight
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
    def weight(self) -> float:
        """Relative weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        


class IndicesValidateInputs(Base):
        
    """Indices Validate Inputs"""

    @camel_case_translate
    def __init__(
        self,
        ticker: str = None,
        name: str = None
    ):        
        super().__init__()
        self.ticker = ticker
        self.name = name

    @property
    def ticker(self) -> str:
        """Ticker Identifier"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self._property_changed('ticker')
        self.__ticker = value        


class Link(Base):
        
    """Hyperlink"""

    @camel_case_translate
    def __init__(
        self,
        title: str = None,
        source: str = None,
        name: str = None
    ):        
        super().__init__()
        self.title = title
        self.source = source
        self.name = name

    @property
    def title(self) -> str:
        """display text"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def source(self) -> str:
        """link"""
        return self.__source

    @source.setter
    def source(self, value: str):
        self._property_changed('source')
        self.__source = value        


class PositionPriceInput(Base):
        
    """Information relating to each constituent"""

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
        """Marquee unique identifier for the asset"""
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
        
    """Publishing parameters to determine where and how to publish baskets, default all
       to false. If not provided when rebalance/edit, selections during create
       will be continued."""

    @camel_case_translate
    def __init__(
        self,
        publish_to_reuters: bool,
        publish_to_bloomberg: bool,
        include_price_history: bool,
        publish_to_factset: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.include_price_history = include_price_history
        self.publish_to_bloomberg = publish_to_bloomberg
        self.publish_to_reuters = publish_to_reuters
        self.publish_to_factset = publish_to_factset
        self.name = name

    @property
    def include_price_history(self) -> bool:
        """Include full price history when publishing to Bloomberg, default to false. Can
           only be set to true when publishing to Bloomberg"""
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

    @property
    def publish_to_factset(self) -> bool:
        """Publish Basket to Factset, default to false"""
        return self.__publish_to_factset

    @publish_to_factset.setter
    def publish_to_factset(self, value: bool):
        self._property_changed('publish_to_factset')
        self.__publish_to_factset = value        


class SimpleParty(Base):
        
    @camel_case_translate
    def __init__(
        self,
        party_type: str = None,
        party_name: str = None,
        party_book: str = None,
        name: str = None
    ):        
        super().__init__()
        self.party_type = party_type
        self.party_name = party_name
        self.party_book = party_book
        self.name = name

    @property
    def party_type(self) -> str:
        return self.__party_type

    @party_type.setter
    def party_type(self, value: str):
        self._property_changed('party_type')
        self.__party_type = value        

    @property
    def party_name(self) -> str:
        return self.__party_name

    @party_name.setter
    def party_name(self, value: str):
        self._property_changed('party_name')
        self.__party_name = value        

    @property
    def party_book(self) -> str:
        return self.__party_book

    @party_book.setter
    def party_book(self, value: str):
        self._property_changed('party_book')
        self.__party_book = value        


class CustomBasketsPricingParameters(Base):
        
    """Parameters for pricing baskets"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[IndicesCurrency, str] = None,
        asset_data_set_id: str = None,
        divisor: float = None,
        fx_data_set_id: str = None,
        fallback_date: str = None,
        initial_price: float = None,
        target_notional: float = None,
        pricing_date: datetime.date = None,
        vendor: Union[MarketDataVendor, str] = None,
        weighting_strategy: str = None,
        reweight: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.asset_data_set_id = asset_data_set_id
        self.divisor = divisor
        self.fx_data_set_id = fx_data_set_id
        self.fallback_date = fallback_date
        self.initial_price = initial_price
        self.target_notional = target_notional
        self.pricing_date = pricing_date
        self.vendor = vendor
        self.weighting_strategy = weighting_strategy
        self.reweight = reweight
        self.name = name

    @property
    def currency(self) -> Union[IndicesCurrency, str]:
        """Currencies supported for basket creation. During rebalance, cannot change basket
           currency hence the input value will be discarded."""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[IndicesCurrency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(IndicesCurrency, value)        

    @property
    def asset_data_set_id(self) -> str:
        """DataSet to use for getting the asset prices from, either real-time (TR) or end-
           of-day (GSEOD)"""
        return self.__asset_data_set_id

    @asset_data_set_id.setter
    def asset_data_set_id(self, value: str):
        self._property_changed('asset_data_set_id')
        self.__asset_data_set_id = value        

    @property
    def divisor(self) -> float:
        """Divisor to be applied to the overall position set"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: float):
        self._property_changed('divisor')
        self.__divisor = value        

    @property
    def fx_data_set_id(self) -> str:
        """DataSet to use for getting FX cross values from"""
        return self.__fx_data_set_id

    @fx_data_set_id.setter
    def fx_data_set_id(self, value: str):
        self._property_changed('fx_data_set_id')
        self.__fx_data_set_id = value        

    @property
    def fallback_date(self) -> str:
        """Number of days to search back in order to get pricing relative from pricing
           date. For same day use '0d', for day before use '1d' etc."""
        return self.__fallback_date

    @fallback_date.setter
    def fallback_date(self, value: str):
        self._property_changed('fallback_date')
        self.__fallback_date = value        

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
    def pricing_date(self) -> datetime.date:
        """Pricing date, default to prior day"""
        return self.__pricing_date

    @pricing_date.setter
    def pricing_date(self, value: datetime.date):
        self._property_changed('pricing_date')
        self.__pricing_date = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

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


class CustomBasketsRiskScheduleInputs(Base):
        
    """inputs used to schedule risk reports for a basket"""

    @camel_case_translate
    def __init__(
        self,
        risk_models: Tuple[CustomBasketRiskParams, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.risk_models = risk_models
        self.name = name

    @property
    def risk_models(self) -> Tuple[CustomBasketRiskParams, ...]:
        """Risk models"""
        return self.__risk_models

    @risk_models.setter
    def risk_models(self, value: Tuple[CustomBasketRiskParams, ...]):
        self._property_changed('risk_models')
        self.__risk_models = value        


class Entitlements(Base):
        
    """Defines the entitlements of a given resource."""

    @camel_case_translate
    def __init__(
        self,
        view: Tuple[str, ...] = None,
        edit: Tuple[str, ...] = None,
        admin: Tuple[str, ...] = None,
        rebalance: Tuple[str, ...] = None,
        execute: Tuple[str, ...] = None,
        trade: Tuple[str, ...] = None,
        upload: Tuple[str, ...] = None,
        query: Tuple[str, ...] = None,
        performance_details: Tuple[str, ...] = None,
        plot: Tuple[str, ...] = None,
        delete: Tuple[str, ...] = None,
        display: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.view = view
        self.edit = edit
        self.admin = admin
        self.rebalance = rebalance
        self.execute = execute
        self.trade = trade
        self.upload = upload
        self.query = query
        self.performance_details = performance_details
        self.plot = plot
        self.delete = delete
        self.display = display
        self.name = name

    @property
    def view(self) -> Tuple[str, ...]:
        """Permission to view the resource and its contents"""
        return self.__view

    @view.setter
    def view(self, value: Tuple[str, ...]):
        self._property_changed('view')
        self.__view = value        

    @property
    def edit(self) -> Tuple[str, ...]:
        """Permission to edit details about the resource content, excluding entitlements.
           Can also delete the resource"""
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[str, ...]):
        self._property_changed('edit')
        self.__edit = value        

    @property
    def admin(self) -> Tuple[str, ...]:
        """Permission to edit all details of the resource, including entitlements. Can also
           delete the resource"""
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[str, ...]):
        self._property_changed('admin')
        self.__admin = value        

    @property
    def rebalance(self) -> Tuple[str, ...]:
        """Permission to rebalance the constituent weights of the resource"""
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value: Tuple[str, ...]):
        self._property_changed('rebalance')
        self.__rebalance = value        

    @property
    def execute(self) -> Tuple[str, ...]:
        """Permission to execute functions and/or reports with the resource"""
        return self.__execute

    @execute.setter
    def execute(self, value: Tuple[str, ...]):
        self._property_changed('execute')
        self.__execute = value        

    @property
    def trade(self) -> Tuple[str, ...]:
        """Permission to trade the resource"""
        return self.__trade

    @trade.setter
    def trade(self, value: Tuple[str, ...]):
        self._property_changed('trade')
        self.__trade = value        

    @property
    def upload(self) -> Tuple[str, ...]:
        """Permission to upload data to the given resource"""
        return self.__upload

    @upload.setter
    def upload(self, value: Tuple[str, ...]):
        self._property_changed('upload')
        self.__upload = value        

    @property
    def query(self) -> Tuple[str, ...]:
        """Permission to query data from the given resource"""
        return self.__query

    @query.setter
    def query(self, value: Tuple[str, ...]):
        self._property_changed('query')
        self.__query = value        

    @property
    def performance_details(self) -> Tuple[str, ...]:
        """Permission to view the resource, it's entire contents, and related data"""
        return self.__performance_details

    @performance_details.setter
    def performance_details(self, value: Tuple[str, ...]):
        self._property_changed('performance_details')
        self.__performance_details = value        

    @property
    def plot(self) -> Tuple[str, ...]:
        """Permission to plot data from the given resource"""
        return self.__plot

    @plot.setter
    def plot(self, value: Tuple[str, ...]):
        self._property_changed('plot')
        self.__plot = value        

    @property
    def delete(self) -> Tuple[str, ...]:
        """Permission to delete the resource"""
        return self.__delete

    @delete.setter
    def delete(self, value: Tuple[str, ...]):
        self._property_changed('delete')
        self.__delete = value        

    @property
    def display(self) -> Tuple[str, ...]:
        """Permission to query data for web router request so that it can prevent
           programmatic access (api access) to the licensed data."""
        return self.__display

    @display.setter
    def display(self, value: Tuple[str, ...]):
        self._property_changed('display')
        self.__display = value        


class FieldValueMap(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class GIRDomain(Base):
        
    @camel_case_translate
    def __init__(
        self,
        document_links: Tuple[Link, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.document_links = document_links
        self.name = name

    @property
    def document_links(self) -> Tuple[Link, ...]:
        """Documents related to this asset"""
        return self.__document_links

    @document_links.setter
    def document_links(self, value: Tuple[Link, ...]):
        self._property_changed('document_links')
        self.__document_links = value        


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


class ISelectNewParameter(Base):
        
    _name_mappings = {'is_fsr_target_factor': 'isFSRTargetFactor'}

    @camel_case_translate
    def __init__(
        self,
        early_unwind_after: float = None,
        early_unwind_applicable: str = None,
        expiry_date_rule: str = None,
        option_target_expiry_parameter: float = None,
        option_early_unwind_days: float = None,
        in_alpha: bool = None,
        is_fsr_target_factor: bool = None,
        fsr_max_ratio: float = None,
        fsr_min_ratio: float = None,
        module_enabled: bool = None,
        module_name: str = None,
        target_strike: float = None,
        strike_method: Union[StrikeMethodType, str] = None,
        option_expiry: Union[OptionExpiryType, str] = None,
        bloomberg_id: str = None,
        stock_id: str = None,
        ric: str = None,
        new_weight: float = None,
        notional: float = None,
        leverage: float = None,
        quantity: float = None,
        hedge_ratio: float = None,
        option_type: Union[OptionType, str] = None,
        option_strike_type: Union[OptionStrikeType, str] = None,
        credit_option_type: Union[CreditOptionType, str] = None,
        credit_option_strike_type: Union[CreditOptionStrikeType, str] = None,
        strike_relative: float = None,
        trade_type: Union[TradeType, str] = None,
        signal: float = None,
        new_signal: float = None,
        new_min_weight: float = None,
        new_max_weight: float = None,
        min_weight: float = None,
        max_weight: float = None,
        election: str = None,
        base_date: str = None,
        commodity: str = None,
        component_weight: float = None,
        contract_nearby_number: float = None,
        expiration_schedule: str = None,
        fixing_type: str = None,
        last_eligible_date: float = None,
        num_roll_days: float = None,
        roll_end: float = None,
        roll_start: float = None,
        roll_type: str = None,
        valid_contract_expiry: str = None,
        name: str = None
    ):        
        super().__init__()
        self.early_unwind_after = early_unwind_after
        self.early_unwind_applicable = early_unwind_applicable
        self.expiry_date_rule = expiry_date_rule
        self.option_target_expiry_parameter = option_target_expiry_parameter
        self.option_early_unwind_days = option_early_unwind_days
        self.in_alpha = in_alpha
        self.is_fsr_target_factor = is_fsr_target_factor
        self.fsr_max_ratio = fsr_max_ratio
        self.fsr_min_ratio = fsr_min_ratio
        self.module_enabled = module_enabled
        self.module_name = module_name
        self.target_strike = target_strike
        self.strike_method = strike_method
        self.option_expiry = option_expiry
        self.bloomberg_id = bloomberg_id
        self.stock_id = stock_id
        self.ric = ric
        self.new_weight = new_weight
        self.notional = notional
        self.leverage = leverage
        self.quantity = quantity
        self.hedge_ratio = hedge_ratio
        self.option_type = option_type
        self.option_strike_type = option_strike_type
        self.credit_option_type = credit_option_type
        self.credit_option_strike_type = credit_option_strike_type
        self.strike_relative = strike_relative
        self.trade_type = trade_type
        self.signal = signal
        self.new_signal = new_signal
        self.new_min_weight = new_min_weight
        self.new_max_weight = new_max_weight
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.election = election
        self.base_date = base_date
        self.commodity = commodity
        self.component_weight = component_weight
        self.contract_nearby_number = contract_nearby_number
        self.expiration_schedule = expiration_schedule
        self.fixing_type = fixing_type
        self.last_eligible_date = last_eligible_date
        self.num_roll_days = num_roll_days
        self.roll_end = roll_end
        self.roll_start = roll_start
        self.roll_type = roll_type
        self.valid_contract_expiry = valid_contract_expiry
        self.name = name

    @property
    def early_unwind_after(self) -> float:
        return self.__early_unwind_after

    @early_unwind_after.setter
    def early_unwind_after(self, value: float):
        self._property_changed('early_unwind_after')
        self.__early_unwind_after = value        

    @property
    def early_unwind_applicable(self) -> str:
        """Indicates whether the module can be unwinded early"""
        return self.__early_unwind_applicable

    @early_unwind_applicable.setter
    def early_unwind_applicable(self, value: str):
        self._property_changed('early_unwind_applicable')
        self.__early_unwind_applicable = value        

    @property
    def expiry_date_rule(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__expiry_date_rule

    @expiry_date_rule.setter
    def expiry_date_rule(self, value: str):
        self._property_changed('expiry_date_rule')
        self.__expiry_date_rule = value        

    @property
    def option_target_expiry_parameter(self) -> float:
        return self.__option_target_expiry_parameter

    @option_target_expiry_parameter.setter
    def option_target_expiry_parameter(self, value: float):
        self._property_changed('option_target_expiry_parameter')
        self.__option_target_expiry_parameter = value        

    @property
    def option_early_unwind_days(self) -> float:
        return self.__option_early_unwind_days

    @option_early_unwind_days.setter
    def option_early_unwind_days(self, value: float):
        self._property_changed('option_early_unwind_days')
        self.__option_early_unwind_days = value        

    @property
    def in_alpha(self) -> bool:
        return self.__in_alpha

    @in_alpha.setter
    def in_alpha(self, value: bool):
        self._property_changed('in_alpha')
        self.__in_alpha = value        

    @property
    def is_fsr_target_factor(self) -> bool:
        return self.__is_fsr_target_factor

    @is_fsr_target_factor.setter
    def is_fsr_target_factor(self, value: bool):
        self._property_changed('is_fsr_target_factor')
        self.__is_fsr_target_factor = value        

    @property
    def fsr_max_ratio(self) -> float:
        return self.__fsr_max_ratio

    @fsr_max_ratio.setter
    def fsr_max_ratio(self, value: float):
        self._property_changed('fsr_max_ratio')
        self.__fsr_max_ratio = value        

    @property
    def fsr_min_ratio(self) -> float:
        return self.__fsr_min_ratio

    @fsr_min_ratio.setter
    def fsr_min_ratio(self, value: float):
        self._property_changed('fsr_min_ratio')
        self.__fsr_min_ratio = value        

    @property
    def module_enabled(self) -> bool:
        """Enable to disable the module"""
        return self.__module_enabled

    @module_enabled.setter
    def module_enabled(self, value: bool):
        self._property_changed('module_enabled')
        self.__module_enabled = value        

    @property
    def module_name(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__module_name

    @module_name.setter
    def module_name(self, value: str):
        self._property_changed('module_name')
        self.__module_name = value        

    @property
    def target_strike(self) -> float:
        return self.__target_strike

    @target_strike.setter
    def target_strike(self, value: float):
        self._property_changed('target_strike')
        self.__target_strike = value        

    @property
    def strike_method(self) -> Union[StrikeMethodType, str]:
        return self.__strike_method

    @strike_method.setter
    def strike_method(self, value: Union[StrikeMethodType, str]):
        self._property_changed('strike_method')
        self.__strike_method = get_enum_value(StrikeMethodType, value)        

    @property
    def option_expiry(self) -> Union[OptionExpiryType, str]:
        return self.__option_expiry

    @option_expiry.setter
    def option_expiry(self, value: Union[OptionExpiryType, str]):
        self._property_changed('option_expiry')
        self.__option_expiry = get_enum_value(OptionExpiryType, value)        

    @property
    def bloomberg_id(self) -> str:
        return self.__bloomberg_id

    @bloomberg_id.setter
    def bloomberg_id(self, value: str):
        self._property_changed('bloomberg_id')
        self.__bloomberg_id = value        

    @property
    def stock_id(self) -> str:
        return self.__stock_id

    @stock_id.setter
    def stock_id(self, value: str):
        self._property_changed('stock_id')
        self.__stock_id = value        

    @property
    def ric(self) -> str:
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def new_weight(self) -> float:
        return self.__new_weight

    @new_weight.setter
    def new_weight(self, value: float):
        self._property_changed('new_weight')
        self.__new_weight = value        

    @property
    def notional(self) -> float:
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def leverage(self) -> float:
        return self.__leverage

    @leverage.setter
    def leverage(self, value: float):
        self._property_changed('leverage')
        self.__leverage = value        

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def hedge_ratio(self) -> float:
        return self.__hedge_ratio

    @hedge_ratio.setter
    def hedge_ratio(self, value: float):
        self._property_changed('hedge_ratio')
        self.__hedge_ratio = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def option_strike_type(self) -> Union[OptionStrikeType, str]:
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: Union[OptionStrikeType, str]):
        self._property_changed('option_strike_type')
        self.__option_strike_type = get_enum_value(OptionStrikeType, value)        

    @property
    def credit_option_type(self) -> Union[CreditOptionType, str]:
        return self.__credit_option_type

    @credit_option_type.setter
    def credit_option_type(self, value: Union[CreditOptionType, str]):
        self._property_changed('credit_option_type')
        self.__credit_option_type = get_enum_value(CreditOptionType, value)        

    @property
    def credit_option_strike_type(self) -> Union[CreditOptionStrikeType, str]:
        return self.__credit_option_strike_type

    @credit_option_strike_type.setter
    def credit_option_strike_type(self, value: Union[CreditOptionStrikeType, str]):
        self._property_changed('credit_option_strike_type')
        self.__credit_option_strike_type = get_enum_value(CreditOptionStrikeType, value)        

    @property
    def strike_relative(self) -> float:
        return self.__strike_relative

    @strike_relative.setter
    def strike_relative(self, value: float):
        self._property_changed('strike_relative')
        self.__strike_relative = value        

    @property
    def trade_type(self) -> Union[TradeType, str]:
        """Direction"""
        return self.__trade_type

    @trade_type.setter
    def trade_type(self, value: Union[TradeType, str]):
        self._property_changed('trade_type')
        self.__trade_type = get_enum_value(TradeType, value)        

    @property
    def signal(self) -> float:
        return self.__signal

    @signal.setter
    def signal(self, value: float):
        self._property_changed('signal')
        self.__signal = value        

    @property
    def new_signal(self) -> float:
        return self.__new_signal

    @new_signal.setter
    def new_signal(self, value: float):
        self._property_changed('new_signal')
        self.__new_signal = value        

    @property
    def new_min_weight(self) -> float:
        return self.__new_min_weight

    @new_min_weight.setter
    def new_min_weight(self, value: float):
        self._property_changed('new_min_weight')
        self.__new_min_weight = value        

    @property
    def new_max_weight(self) -> float:
        return self.__new_max_weight

    @new_max_weight.setter
    def new_max_weight(self, value: float):
        self._property_changed('new_max_weight')
        self.__new_max_weight = value        

    @property
    def min_weight(self) -> float:
        return self.__min_weight

    @min_weight.setter
    def min_weight(self, value: float):
        self._property_changed('min_weight')
        self.__min_weight = value        

    @property
    def max_weight(self) -> float:
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, value: float):
        self._property_changed('max_weight')
        self.__max_weight = value        

    @property
    def election(self) -> str:
        return self.__election

    @election.setter
    def election(self, value: str):
        self._property_changed('election')
        self.__election = value        

    @property
    def base_date(self) -> str:
        """The base date type to use for the nearby contract roll"""
        return self.__base_date

    @base_date.setter
    def base_date(self, value: str):
        self._property_changed('base_date')
        self.__base_date = value        

    @property
    def commodity(self) -> str:
        """The commodity symbol for the module"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: str):
        self._property_changed('commodity')
        self.__commodity = value        

    @property
    def component_weight(self) -> float:
        """The weight allocated to the specified module"""
        return self.__component_weight

    @component_weight.setter
    def component_weight(self, value: float):
        self._property_changed('component_weight')
        self.__component_weight = value        

    @property
    def contract_nearby_number(self) -> float:
        """The nearby contract to roll into"""
        return self.__contract_nearby_number

    @contract_nearby_number.setter
    def contract_nearby_number(self, value: float):
        self._property_changed('contract_nearby_number')
        self.__contract_nearby_number = value        

    @property
    def expiration_schedule(self) -> str:
        """The contract expiration schedule to be used"""
        return self.__expiration_schedule

    @expiration_schedule.setter
    def expiration_schedule(self, value: str):
        self._property_changed('expiration_schedule')
        self.__expiration_schedule = value        

    @property
    def fixing_type(self) -> str:
        """Type of fixing used to determine the price"""
        return self.__fixing_type

    @fixing_type.setter
    def fixing_type(self, value: str):
        self._property_changed('fixing_type')
        self.__fixing_type = value        

    @property
    def last_eligible_date(self) -> float:
        """The last eligible date for the roll"""
        return self.__last_eligible_date

    @last_eligible_date.setter
    def last_eligible_date(self, value: float):
        self._property_changed('last_eligible_date')
        self.__last_eligible_date = value        

    @property
    def num_roll_days(self) -> float:
        """The number of days over which the roll is spread"""
        return self.__num_roll_days

    @num_roll_days.setter
    def num_roll_days(self, value: float):
        self._property_changed('num_roll_days')
        self.__num_roll_days = value        

    @property
    def roll_end(self) -> float:
        """Day on which to end the roll"""
        return self.__roll_end

    @roll_end.setter
    def roll_end(self, value: float):
        self._property_changed('roll_end')
        self.__roll_end = value        

    @property
    def roll_start(self) -> float:
        """Day on which to start the roll"""
        return self.__roll_start

    @roll_start.setter
    def roll_start(self, value: float):
        self._property_changed('roll_start')
        self.__roll_start = value        

    @property
    def roll_type(self) -> str:
        """Type of contract roll"""
        return self.__roll_type

    @roll_type.setter
    def roll_type(self, value: str):
        self._property_changed('roll_type')
        self.__roll_type = value        

    @property
    def valid_contract_expiry(self) -> str:
        """The valid contract expiry months"""
        return self.__valid_contract_expiry

    @valid_contract_expiry.setter
    def valid_contract_expiry(self, value: str):
        self._property_changed('valid_contract_expiry')
        self.__valid_contract_expiry = value        


class IndicesPositionSet(Base):
        
    """Information of constituents associated with the index."""

    @camel_case_translate
    def __init__(
        self,
        positions: Tuple[IndicesPositionInput, ...],
        position_date: datetime.date,
        name: str = None
    ):        
        super().__init__()
        self.positions = positions
        self.position_date = position_date
        self.name = name

    @property
    def positions(self) -> Tuple[IndicesPositionInput, ...]:
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[IndicesPositionInput, ...]):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def position_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__position_date

    @position_date.setter
    def position_date(self, value: datetime.date):
        self._property_changed('position_date')
        self.__position_date = value        


class CustomBasketsBackcastInputs(Base):
        
    """Inputs used to backcast a custom basket"""

    @camel_case_translate
    def __init__(
        self,
        position_set: Tuple[IndicesPositionSet, ...],
        name: str = None
    ):        
        super().__init__()
        self.position_set = position_set
        self.name = name

    @property
    def position_set(self) -> Tuple[IndicesPositionSet, ...]:
        """Information of constituents associated with the basket."""
        return self.__position_set

    @position_set.setter
    def position_set(self, value: Tuple[IndicesPositionSet, ...]):
        self._property_changed('position_set')
        self.__position_set = value        


class CustomBasketsCreateInputs(Base):
        
    """Inputs required to create a basket"""

    _name_mappings = {'allow_ca_restricted_assets': 'allowCARestrictedAssets'}

    @camel_case_translate
    def __init__(
        self,
        ticker: str,
        name: str,
        pricing_parameters: CustomBasketsPricingParameters,
        position_set: Tuple[PositionPriceInput, ...],
        return_type: str,
        description: str = None,
        styles: Tuple[str, ...] = None,
        related_content: GIRDomain = None,
        hedge_id: str = None,
        clone_parent_id: str = None,
        publish_parameters: PublishParameters = None,
        index_notes: str = None,
        flagship: bool = None,
        on_behalf_of: str = None,
        allow_limited_access_assets: bool = False,
        allow_ca_restricted_assets: bool = False,
        vendor: str = None,
        default_backcast: bool = True
    ):        
        super().__init__()
        self.ticker = ticker
        self.name = name
        self.description = description
        self.styles = styles
        self.related_content = related_content
        self.hedge_id = hedge_id
        self.clone_parent_id = clone_parent_id
        self.return_type = return_type
        self.position_set = position_set
        self.publish_parameters = publish_parameters
        self.pricing_parameters = pricing_parameters
        self.index_notes = index_notes
        self.flagship = flagship
        self.on_behalf_of = on_behalf_of
        self.allow_limited_access_assets = allow_limited_access_assets
        self.allow_ca_restricted_assets = allow_ca_restricted_assets
        self.vendor = vendor
        self.default_backcast = default_backcast

    @property
    def ticker(self) -> str:
        """Ticker Identifier for the basket (Prefix with 'GS' to publish to Bloomberg).
           Please note ticker should start with your assigned prefix. If you do
           not have a prefix setup, reach out to your GS representative or you
           can use the default prefix GSMB"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self._property_changed('ticker')
        self.__ticker = value        

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
        """Free text description of basket, default to empty. Description provided will be
           indexed in the search service for free text relevance match."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the basket (max 50), default to Bespoke"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def related_content(self) -> GIRDomain:
        """Links to content related to this basket or any of its constituents (optional)"""
        return self.__related_content

    @related_content.setter
    def related_content(self, value: GIRDomain):
        self._property_changed('related_content')
        self.__related_content = value        

    @property
    def hedge_id(self) -> str:
        """Marquee Id of the source hedge, in case current basket composition is sourced
           from marquee hedge"""
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: str):
        self._property_changed('hedge_id')
        self.__hedge_id = value        

    @property
    def clone_parent_id(self) -> str:
        """Marquee Id of the source basket, in case current basket composition is sourced
           from another marquee basket"""
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: str):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def return_type(self) -> str:
        """Determines the index calculation methodology with respect to dividend
           reinvestment."""
        return self.__return_type

    @return_type.setter
    def return_type(self, value: str):
        self._property_changed('return_type')
        self.__return_type = value        

    @property
    def position_set(self) -> Tuple[PositionPriceInput, ...]:
        """Information of constituents associated with the basket. Need to supply one of
           weight or quantity. If using weight, need to provide weight for all
           constituents and similarly for quantity"""
        return self.__position_set

    @position_set.setter
    def position_set(self, value: Tuple[PositionPriceInput, ...]):
        self._property_changed('position_set')
        self.__position_set = value        

    @property
    def publish_parameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish baskets, default all
           to false. If not provided when rebalance/edit, selections during
           create will be continued."""
        return self.__publish_parameters

    @publish_parameters.setter
    def publish_parameters(self, value: PublishParameters):
        self._property_changed('publish_parameters')
        self.__publish_parameters = value        

    @property
    def pricing_parameters(self) -> CustomBasketsPricingParameters:
        """Parameters for pricing baskets"""
        return self.__pricing_parameters

    @pricing_parameters.setter
    def pricing_parameters(self, value: CustomBasketsPricingParameters):
        self._property_changed('pricing_parameters')
        self.__pricing_parameters = value        

    @property
    def index_notes(self) -> str:
        """Notes for the index"""
        return self.__index_notes

    @index_notes.setter
    def index_notes(self, value: str):
        self._property_changed('index_notes')
        self.__index_notes = value        

    @property
    def flagship(self) -> bool:
        """Is a flagship basket."""
        return self.__flagship

    @flagship.setter
    def flagship(self, value: bool):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def on_behalf_of(self) -> str:
        """If creating the basket on behalf of a client, please provide the client's guid
           here."""
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def allow_limited_access_assets(self) -> bool:
        """To allow basket creation with constituents GS has limited access to. Default is
           false."""
        return self.__allow_limited_access_assets

    @allow_limited_access_assets.setter
    def allow_limited_access_assets(self, value: bool):
        self._property_changed('allow_limited_access_assets')
        self.__allow_limited_access_assets = value        

    @property
    def allow_ca_restricted_assets(self) -> bool:
        """To allow basket creation with constituents that will not be corporate action
           adjusted in the future. Default is false."""
        return self.__allow_ca_restricted_assets

    @allow_ca_restricted_assets.setter
    def allow_ca_restricted_assets(self, value: bool):
        self._property_changed('allow_ca_restricted_assets')
        self.__allow_ca_restricted_assets = value        

    @property
    def vendor(self) -> str:
        """If the basket composition was sourced from a vendor, please provide vendor oeid
           here"""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def default_backcast(self) -> bool:
        """Should basket be backcasted using the current composition"""
        return self.__default_backcast

    @default_backcast.setter
    def default_backcast(self, value: bool):
        self._property_changed('default_backcast')
        self.__default_backcast = value        


class CustomBasketsEditInputs(Base):
        
    """parameters used to edit a basket"""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        description: str = None,
        styles: Tuple[str, ...] = None,
        related_content: GIRDomain = None,
        publish_parameters: PublishParameters = None,
        index_notes: str = None,
        index_not_trading_reasons: Union[IndexNotTradingReasons, str] = None,
        flagship: bool = None,
        clone_parent_id: str = None
    ):        
        super().__init__()
        self.name = name
        self.description = description
        self.styles = styles
        self.related_content = related_content
        self.publish_parameters = publish_parameters
        self.index_notes = index_notes
        self.index_not_trading_reasons = index_not_trading_reasons
        self.flagship = flagship
        self.clone_parent_id = clone_parent_id

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
        """Free text description of basket, default to empty. Description provided will be
           indexed in the search service for free text relevance match."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the basket (max 50), default to Bespoke"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def related_content(self) -> GIRDomain:
        """Links to content related to this basket or any of its constituents (optional)"""
        return self.__related_content

    @related_content.setter
    def related_content(self, value: GIRDomain):
        self._property_changed('related_content')
        self.__related_content = value        

    @property
    def publish_parameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish baskets, default all
           to false. If not provided when rebalance/edit, selections during
           create will be continued."""
        return self.__publish_parameters

    @publish_parameters.setter
    def publish_parameters(self, value: PublishParameters):
        self._property_changed('publish_parameters')
        self.__publish_parameters = value        

    @property
    def index_notes(self) -> str:
        """Notes for the index"""
        return self.__index_notes

    @index_notes.setter
    def index_notes(self, value: str):
        self._property_changed('index_notes')
        self.__index_notes = value        

    @property
    def index_not_trading_reasons(self) -> Union[IndexNotTradingReasons, str]:
        """Reasons the index was not traded"""
        return self.__index_not_trading_reasons

    @index_not_trading_reasons.setter
    def index_not_trading_reasons(self, value: Union[IndexNotTradingReasons, str]):
        self._property_changed('index_not_trading_reasons')
        self.__index_not_trading_reasons = get_enum_value(IndexNotTradingReasons, value)        

    @property
    def flagship(self) -> bool:
        """Is a flagship basket."""
        return self.__flagship

    @flagship.setter
    def flagship(self, value: bool):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def clone_parent_id(self) -> str:
        """Marquee Id of the source basket, in case current basket composition is sourced
           from another marquee basket"""
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: str):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        


class CustomBasketsRebalanceInputs(Base):
        
    """Inputs used to rebalance a custom basket"""

    _name_mappings = {'allow_ca_restricted_assets': 'allowCARestrictedAssets'}

    @camel_case_translate
    def __init__(
        self,
        position_set: Tuple[PositionPriceInput, ...] = None,
        publish_parameters: PublishParameters = None,
        pricing_parameters: CustomBasketsPricingParameters = None,
        allow_limited_access_assets: bool = False,
        allow_ca_restricted_assets: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.position_set = position_set
        self.publish_parameters = publish_parameters
        self.pricing_parameters = pricing_parameters
        self.allow_limited_access_assets = allow_limited_access_assets
        self.allow_ca_restricted_assets = allow_ca_restricted_assets
        self.name = name

    @property
    def position_set(self) -> Tuple[PositionPriceInput, ...]:
        """Information of constituents associated with the basket. Need to supply one of
           weight or quantity. If using weight, need to provide weight for all
           constituents and similarly for quantity"""
        return self.__position_set

    @position_set.setter
    def position_set(self, value: Tuple[PositionPriceInput, ...]):
        self._property_changed('position_set')
        self.__position_set = value        

    @property
    def publish_parameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish baskets, default all
           to false. If not provided when rebalance/edit, selections during
           create will be continued."""
        return self.__publish_parameters

    @publish_parameters.setter
    def publish_parameters(self, value: PublishParameters):
        self._property_changed('publish_parameters')
        self.__publish_parameters = value        

    @property
    def pricing_parameters(self) -> CustomBasketsPricingParameters:
        """Parameters for pricing baskets"""
        return self.__pricing_parameters

    @pricing_parameters.setter
    def pricing_parameters(self, value: CustomBasketsPricingParameters):
        self._property_changed('pricing_parameters')
        self.__pricing_parameters = value        

    @property
    def allow_limited_access_assets(self) -> bool:
        """To allow basket rebalance with constituents GS has limited access to. Default is
           false."""
        return self.__allow_limited_access_assets

    @allow_limited_access_assets.setter
    def allow_limited_access_assets(self, value: bool):
        self._property_changed('allow_limited_access_assets')
        self.__allow_limited_access_assets = value        

    @property
    def allow_ca_restricted_assets(self) -> bool:
        """To allow basket rebalance with constituents that will not be corporate action
           adjusted in the future. Default is false."""
        return self.__allow_ca_restricted_assets

    @allow_ca_restricted_assets.setter
    def allow_ca_restricted_assets(self, value: bool):
        self._property_changed('allow_ca_restricted_assets')
        self.__allow_ca_restricted_assets = value        


class DynamicConstructionResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        action=None,
        columns: Tuple[ISelectConstituentColumn, ...] = None,
        constituent_validations: tuple = None,
        date_validation_status: str = None,
        types: tuple = None,
        date_validations: tuple = None,
        new_parameters: Tuple[ISelectNewParameter, ...] = None,
        index_type: str = None,
        index_parameter_definitions: tuple = None,
        index_metadata: tuple = None,
        index_parameters: tuple = None,
        index_parameter_validation: tuple = None,
        status=None,
        valid: int = None,
        validation_messages: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.action = action
        self.columns = columns
        self.constituent_validations = constituent_validations
        self.date_validation_status = date_validation_status
        self.types = types
        self.date_validations = date_validations
        self.new_parameters = new_parameters
        self.index_type = index_type
        self.index_parameter_definitions = index_parameter_definitions
        self.index_metadata = index_metadata
        self.index_parameters = index_parameters
        self.index_parameter_validation = index_parameter_validation
        self.status = status
        self.valid = valid
        self.validation_messages = validation_messages
        self.name = name

    @property
    def action(self):
        """Action type"""
        return self.__action

    @action.setter
    def action(self, value):
        self._property_changed('action')
        self.__action = value        

    @property
    def columns(self) -> Tuple[ISelectConstituentColumn, ...]:
        """NewParameters Columns Definition"""
        return self.__columns

    @columns.setter
    def columns(self, value: Tuple[ISelectConstituentColumn, ...]):
        self._property_changed('columns')
        self.__columns = value        

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
    def types(self) -> tuple:
        return self.__types

    @types.setter
    def types(self, value: tuple):
        self._property_changed('types')
        self.__types = value        

    @property
    def date_validations(self) -> tuple:
        return self.__date_validations

    @date_validations.setter
    def date_validations(self, value: tuple):
        self._property_changed('date_validations')
        self.__date_validations = value        

    @property
    def new_parameters(self) -> Tuple[ISelectNewParameter, ...]:
        """New parameters for the index"""
        return self.__new_parameters

    @new_parameters.setter
    def new_parameters(self, value: Tuple[ISelectNewParameter, ...]):
        self._property_changed('new_parameters')
        self.__new_parameters = value        

    @property
    def index_type(self) -> str:
        """What type of index is the user constructing?"""
        return self.__index_type

    @index_type.setter
    def index_type(self, value: str):
        self._property_changed('index_type')
        self.__index_type = value        

    @property
    def index_parameter_definitions(self) -> tuple:
        return self.__index_parameter_definitions

    @index_parameter_definitions.setter
    def index_parameter_definitions(self, value: tuple):
        self._property_changed('index_parameter_definitions')
        self.__index_parameter_definitions = value        

    @property
    def index_metadata(self) -> tuple:
        return self.__index_metadata

    @index_metadata.setter
    def index_metadata(self, value: tuple):
        self._property_changed('index_metadata')
        self.__index_metadata = value        

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
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self._property_changed('status')
        self.__status = value        

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


class ISelectRebalance(Base):
        
    @camel_case_translate
    def __init__(
        self,
        new_weights: Tuple[ISelectNewWeight, ...] = None,
        rebalance_date: str = None,
        new_parameters: Tuple[ISelectNewParameter, ...] = None,
        index_parameters: Tuple[ISelectIndexParameters, ...] = None,
        waiver_requested: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.new_weights = new_weights
        self.rebalance_date = rebalance_date
        self.new_parameters = new_parameters
        self.index_parameters = index_parameters
        self.waiver_requested = waiver_requested
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

    @property
    def waiver_requested(self) -> bool:
        """Flag to see if client requested waiver"""
        return self.__waiver_requested

    @waiver_requested.setter
    def waiver_requested(self, value: bool):
        self._property_changed('waiver_requested')
        self.__waiver_requested = value        


class ISelectRequest(Base):
        
    @camel_case_translate
    def __init__(
        self,
        rebalance_date: str,
        request_counter: int,
        use_new_rebalance_interface: bool,
        new_parameters: Tuple[ISelectNewParameter, ...] = None,
        index_parameters: Tuple[ISelectIndexParameter, ...] = None,
        new_weights: Tuple[ISelectNewWeight, ...] = None,
        new_units: Tuple[ISelectNewUnit, ...] = None,
        entry_type: str = None,
        waiver_requested: bool = None,
        presubmit: bool = None,
        requester_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.use_new_rebalance_interface = use_new_rebalance_interface
        self.new_parameters = new_parameters
        self.index_parameters = index_parameters
        self.new_weights = new_weights
        self.new_units = new_units
        self.rebalance_date = rebalance_date
        self.entry_type = entry_type
        self.request_counter = request_counter
        self.waiver_requested = waiver_requested
        self.presubmit = presubmit
        self.requester_id = requester_id
        self.name = name

    @property
    def use_new_rebalance_interface(self) -> bool:
        """Flag to route to original ISelect or DynVol ISelect"""
        return self.__use_new_rebalance_interface

    @use_new_rebalance_interface.setter
    def use_new_rebalance_interface(self, value: bool):
        self._property_changed('use_new_rebalance_interface')
        self.__use_new_rebalance_interface = value        

    @property
    def new_parameters(self) -> Tuple[ISelectNewParameter, ...]:
        """New parameters to be updated"""
        return self.__new_parameters

    @new_parameters.setter
    def new_parameters(self, value: Tuple[ISelectNewParameter, ...]):
        self._property_changed('new_parameters')
        self.__new_parameters = value        

    @property
    def index_parameters(self) -> Tuple[ISelectIndexParameter, ...]:
        """Index Parameters to be updated"""
        return self.__index_parameters

    @index_parameters.setter
    def index_parameters(self, value: Tuple[ISelectIndexParameter, ...]):
        self._property_changed('index_parameters')
        self.__index_parameters = value        

    @property
    def new_weights(self) -> Tuple[ISelectNewWeight, ...]:
        """New Weight array to be updated"""
        return self.__new_weights

    @new_weights.setter
    def new_weights(self, value: Tuple[ISelectNewWeight, ...]):
        self._property_changed('new_weights')
        self.__new_weights = value        

    @property
    def new_units(self) -> Tuple[ISelectNewUnit, ...]:
        """New Unit array to be updated"""
        return self.__new_units

    @new_units.setter
    def new_units(self, value: Tuple[ISelectNewUnit, ...]):
        self._property_changed('new_units')
        self.__new_units = value        

    @property
    def rebalance_date(self) -> str:
        return self.__rebalance_date

    @rebalance_date.setter
    def rebalance_date(self, value: str):
        self._property_changed('rebalance_date')
        self.__rebalance_date = value        

    @property
    def entry_type(self) -> str:
        """Rebalance type"""
        return self.__entry_type

    @entry_type.setter
    def entry_type(self, value: str):
        self._property_changed('entry_type')
        self.__entry_type = value        

    @property
    def request_counter(self) -> int:
        return self.__request_counter

    @request_counter.setter
    def request_counter(self, value: int):
        self._property_changed('request_counter')
        self.__request_counter = value        

    @property
    def waiver_requested(self) -> bool:
        return self.__waiver_requested

    @waiver_requested.setter
    def waiver_requested(self, value: bool):
        self._property_changed('waiver_requested')
        self.__waiver_requested = value        

    @property
    def presubmit(self) -> bool:
        return self.__presubmit

    @presubmit.setter
    def presubmit(self, value: bool):
        self._property_changed('presubmit')
        self.__presubmit = value        

    @property
    def requester_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__requester_id

    @requester_id.setter
    def requester_id(self, value: str):
        self._property_changed('requester_id')
        self.__requester_id = value        


class ISelectResponse(Base):
        
    _name_mappings = {'action': 'Action', 'action_comment': 'ActionComment'}

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


class IndicesDynamicConstructInputs(Base):
        
    """STS Indices Dynamic Construction Inputs"""

    @camel_case_translate
    def __init__(
        self,
        index_type: str,
        new_parameters: Tuple[ISelectNewParameter, ...],
        index_parameters: Tuple[ISelectIndexParameters, ...],
        index_metadata: Tuple[ISelectIndexParameters, ...],
        name: str = None
    ):        
        super().__init__()
        self.index_type = index_type
        self.new_parameters = new_parameters
        self.index_parameters = index_parameters
        self.index_metadata = index_metadata
        self.name = name

    @property
    def index_type(self) -> str:
        """What type of index is the user constructing?"""
        return self.__index_type

    @index_type.setter
    def index_type(self, value: str):
        self._property_changed('index_type')
        self.__index_type = value        

    @property
    def new_parameters(self) -> Tuple[ISelectNewParameter, ...]:
        """New parameters for the index"""
        return self.__new_parameters

    @new_parameters.setter
    def new_parameters(self, value: Tuple[ISelectNewParameter, ...]):
        self._property_changed('new_parameters')
        self.__new_parameters = value        

    @property
    def index_parameters(self) -> Tuple[ISelectIndexParameters, ...]:
        """Index Parameters for the index"""
        return self.__index_parameters

    @index_parameters.setter
    def index_parameters(self, value: Tuple[ISelectIndexParameters, ...]):
        self._property_changed('index_parameters')
        self.__index_parameters = value        

    @property
    def index_metadata(self) -> Tuple[ISelectIndexParameters, ...]:
        """Top level Index metadata"""
        return self.__index_metadata

    @index_metadata.setter
    def index_metadata(self, value: Tuple[ISelectIndexParameters, ...]):
        self._property_changed('index_metadata')
        self.__index_metadata = value        


class IndicesBackcastInputs(Base):
        
    @camel_case_translate
    def __init__(
        self,
        parameters: CustomBasketsBackcastInputs,
        name: str = None
    ):        
        super().__init__()
        self.parameters = parameters
        self.name = name

    @property
    def parameters(self) -> CustomBasketsBackcastInputs:
        """The inputs used to backcast an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: CustomBasketsBackcastInputs):
        self._property_changed('parameters')
        self.__parameters = value        


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
        """parameters used to edit a basket"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: CustomBasketsEditInputs):
        self._property_changed('parameters')
        self.__parameters = value        


class IndicesRebalanceInputs(Base):
        
    @camel_case_translate
    def __init__(
        self,
        parameters: Union[CustomBasketsRebalanceInputs, ISelectRebalance],
        name: str = None
    ):        
        super().__init__()
        self.parameters = parameters
        self.name = name

    @property
    def parameters(self) -> Union[CustomBasketsRebalanceInputs, ISelectRebalance]:
        """The inputs used to rebalance an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: Union[CustomBasketsRebalanceInputs, ISelectRebalance]):
        self._property_changed('parameters')
        self.__parameters = value        


class ApprovalCustomBasketResponse(Base):
        
    """Rebalance custom basket approval response"""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        positions_to_rebalance: PosSet,
        entitlements: Entitlements = None,
        status: Union[ApprovalStatus, str] = None,
        parent_id: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        approved_by_id: str = None,
        approved_time: datetime.datetime = None,
        submitted_by_id: str = None,
        submitted_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        comments: Tuple[ApprovalComment, ...] = None,
        notifyees: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.entitlements = entitlements
        self.status = status
        self.parent_id = parent_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.approved_by_id = approved_by_id
        self.approved_time = approved_time
        self.submitted_by_id = submitted_by_id
        self.submitted_time = submitted_time
        self.last_updated_time = last_updated_time
        self.comments = comments
        self.positions_to_rebalance = positions_to_rebalance
        self.notifyees = notifyees
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def status(self) -> Union[ApprovalStatus, str]:
        """Current state of the approval."""
        return self.__status

    @status.setter
    def status(self, value: Union[ApprovalStatus, str]):
        self._property_changed('status')
        self.__status = get_enum_value(ApprovalStatus, value)        

    @property
    def parent_id(self) -> str:
        """An optional ID of a parent approval which is linked to this instance."""
        return self.__parent_id

    @parent_id.setter
    def parent_id(self, value: str):
        self._property_changed('parent_id')
        self.__parent_id = value        

    @property
    def created_by_id(self) -> str:
        """Id of the creator of the approval."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Timestamp of when the approval was created."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def approved_by_id(self) -> str:
        """Id of the approval's approver."""
        return self.__approved_by_id

    @approved_by_id.setter
    def approved_by_id(self, value: str):
        self._property_changed('approved_by_id')
        self.__approved_by_id = value        

    @property
    def approved_time(self) -> datetime.datetime:
        """Timestamp of when the approval was approved."""
        return self.__approved_time

    @approved_time.setter
    def approved_time(self, value: datetime.datetime):
        self._property_changed('approved_time')
        self.__approved_time = value        

    @property
    def submitted_by_id(self) -> str:
        """Id of the submitter."""
        return self.__submitted_by_id

    @submitted_by_id.setter
    def submitted_by_id(self, value: str):
        self._property_changed('submitted_by_id')
        self.__submitted_by_id = value        

    @property
    def submitted_time(self) -> datetime.datetime:
        """Timestamp of when the approval was submitted."""
        return self.__submitted_time

    @submitted_time.setter
    def submitted_time(self, value: datetime.datetime):
        self._property_changed('submitted_time')
        self.__submitted_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the approval was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def comments(self) -> Tuple[ApprovalComment, ...]:
        """A set of comments that apply to this approval."""
        return self.__comments

    @comments.setter
    def comments(self, value: Tuple[ApprovalComment, ...]):
        self._property_changed('comments')
        self.__comments = value        

    @property
    def positions_to_rebalance(self) -> PosSet:
        """Position set to rebalance"""
        return self.__positions_to_rebalance

    @positions_to_rebalance.setter
    def positions_to_rebalance(self, value: PosSet):
        self._property_changed('positions_to_rebalance')
        self.__positions_to_rebalance = value        

    @property
    def notifyees(self) -> Tuple[str, ...]:
        """Notifyees of actions regarding to this approval"""
        return self.__notifyees

    @notifyees.setter
    def notifyees(self, value: Tuple[str, ...]):
        self._property_changed('notifyees')
        self.__notifyees = value        
