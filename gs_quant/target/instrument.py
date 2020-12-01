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
from gs_quant.instrument import Instrument
from gs_quant.base import InstrumentBase, camel_case_translate, get_enum_value


class CSLPython(Instrument):
        
    """Object representation of an arbitrary payoff defined in Python"""

    @camel_case_translate
    def __init__(
        self,
        class_name: str = None,
        denominated: Union[Currency, str] = None,
        double_params: Tuple[CSLDouble, ...] = None,
        date_params: Tuple[CSLDate, ...] = None,
        string_params: Tuple[CSLString, ...] = None,
        simple_schedule_params: Tuple[CSLSimpleSchedule, ...] = None,
        schedule_params: Tuple[CSLSchedule, ...] = None,
        currency_params: Tuple[CSLCurrency, ...] = None,
        stock_params: Tuple[CSLStock, ...] = None,
        index_params: Tuple[CSLIndex, ...] = None,
        fx_cross_params: Tuple[CSLFXCross, ...] = None,
        double_array_params: Tuple[CSLDoubleArray, ...] = None,
        date_array_params: Tuple[CSLDateArray, ...] = None,
        string_array_params: Tuple[CSLStringArray, ...] = None,
        simple_schedule_array_params: Tuple[CSLSimpleScheduleArray, ...] = None,
        schedule_array_params: Tuple[CSLScheduleArray, ...] = None,
        currency_array_params: Tuple[CSLCurrencyArray, ...] = None,
        stock_array_params: Tuple[CSLStockArray, ...] = None,
        index_array_params: Tuple[CSLIndexArray, ...] = None,
        fx_cross_array_params: Tuple[CSLFXCrossArray, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.class_name = class_name
        self.denominated = denominated
        self.double_params = double_params
        self.date_params = date_params
        self.string_params = string_params
        self.simple_schedule_params = simple_schedule_params
        self.schedule_params = schedule_params
        self.currency_params = currency_params
        self.stock_params = stock_params
        self.index_params = index_params
        self.fx_cross_params = fx_cross_params
        self.double_array_params = double_array_params
        self.date_array_params = date_array_params
        self.string_array_params = string_array_params
        self.simple_schedule_array_params = simple_schedule_array_params
        self.schedule_array_params = schedule_array_params
        self.currency_array_params = currency_array_params
        self.stock_array_params = stock_array_params
        self.index_array_params = index_array_params
        self.fx_cross_array_params = fx_cross_array_params
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Cross Asset"""
        return AssetClass.Cross_Asset        

    @property
    def type(self) -> AssetType:
        """CSL"""
        return AssetType.CSL        

    @property
    def class_name(self) -> str:
        """A reference to the Python script defining this payoff class"""
        return self.__class_name

    @class_name.setter
    def class_name(self, value: str):
        self._property_changed('class_name')
        self.__class_name = value        

    @property
    def denominated(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__denominated

    @denominated.setter
    def denominated(self, value: Union[Currency, str]):
        self._property_changed('denominated')
        self.__denominated = get_enum_value(Currency, value)        

    @property
    def double_params(self) -> Tuple[CSLDouble, ...]:
        """A double"""
        return self.__double_params

    @double_params.setter
    def double_params(self, value: Tuple[CSLDouble, ...]):
        self._property_changed('double_params')
        self.__double_params = value        

    @property
    def date_params(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__date_params

    @date_params.setter
    def date_params(self, value: Tuple[CSLDate, ...]):
        self._property_changed('date_params')
        self.__date_params = value        

    @property
    def string_params(self) -> Tuple[CSLString, ...]:
        """A string"""
        return self.__string_params

    @string_params.setter
    def string_params(self, value: Tuple[CSLString, ...]):
        self._property_changed('string_params')
        self.__string_params = value        

    @property
    def simple_schedule_params(self) -> Tuple[CSLSimpleSchedule, ...]:
        """A fixing date, settlement date pair"""
        return self.__simple_schedule_params

    @simple_schedule_params.setter
    def simple_schedule_params(self, value: Tuple[CSLSimpleSchedule, ...]):
        self._property_changed('simple_schedule_params')
        self.__simple_schedule_params = value        

    @property
    def schedule_params(self) -> Tuple[CSLSchedule, ...]:
        """A schedule"""
        return self.__schedule_params

    @schedule_params.setter
    def schedule_params(self, value: Tuple[CSLSchedule, ...]):
        self._property_changed('schedule_params')
        self.__schedule_params = value        

    @property
    def currency_params(self) -> Tuple[CSLCurrency, ...]:
        """A currency"""
        return self.__currency_params

    @currency_params.setter
    def currency_params(self, value: Tuple[CSLCurrency, ...]):
        self._property_changed('currency_params')
        self.__currency_params = value        

    @property
    def stock_params(self) -> Tuple[CSLStock, ...]:
        """A stock"""
        return self.__stock_params

    @stock_params.setter
    def stock_params(self, value: Tuple[CSLStock, ...]):
        self._property_changed('stock_params')
        self.__stock_params = value        

    @property
    def index_params(self) -> Tuple[CSLIndex, ...]:
        """An index"""
        return self.__index_params

    @index_params.setter
    def index_params(self, value: Tuple[CSLIndex, ...]):
        self._property_changed('index_params')
        self.__index_params = value        

    @property
    def fx_cross_params(self) -> Tuple[CSLFXCross, ...]:
        """An FX cross"""
        return self.__fx_cross_params

    @fx_cross_params.setter
    def fx_cross_params(self, value: Tuple[CSLFXCross, ...]):
        self._property_changed('fx_cross_params')
        self.__fx_cross_params = value        

    @property
    def double_array_params(self) -> Tuple[CSLDoubleArray, ...]:
        """An array of doubles"""
        return self.__double_array_params

    @double_array_params.setter
    def double_array_params(self, value: Tuple[CSLDoubleArray, ...]):
        self._property_changed('double_array_params')
        self.__double_array_params = value        

    @property
    def date_array_params(self) -> Tuple[CSLDateArray, ...]:
        """An array of dates"""
        return self.__date_array_params

    @date_array_params.setter
    def date_array_params(self, value: Tuple[CSLDateArray, ...]):
        self._property_changed('date_array_params')
        self.__date_array_params = value        

    @property
    def string_array_params(self) -> Tuple[CSLStringArray, ...]:
        """An array of strings"""
        return self.__string_array_params

    @string_array_params.setter
    def string_array_params(self, value: Tuple[CSLStringArray, ...]):
        self._property_changed('string_array_params')
        self.__string_array_params = value        

    @property
    def simple_schedule_array_params(self) -> Tuple[CSLSimpleScheduleArray, ...]:
        """An array of simple schedules"""
        return self.__simple_schedule_array_params

    @simple_schedule_array_params.setter
    def simple_schedule_array_params(self, value: Tuple[CSLSimpleScheduleArray, ...]):
        self._property_changed('simple_schedule_array_params')
        self.__simple_schedule_array_params = value        

    @property
    def schedule_array_params(self) -> Tuple[CSLScheduleArray, ...]:
        """An array of schedules"""
        return self.__schedule_array_params

    @schedule_array_params.setter
    def schedule_array_params(self, value: Tuple[CSLScheduleArray, ...]):
        self._property_changed('schedule_array_params')
        self.__schedule_array_params = value        

    @property
    def currency_array_params(self) -> Tuple[CSLCurrencyArray, ...]:
        """An array of currencies"""
        return self.__currency_array_params

    @currency_array_params.setter
    def currency_array_params(self, value: Tuple[CSLCurrencyArray, ...]):
        self._property_changed('currency_array_params')
        self.__currency_array_params = value        

    @property
    def stock_array_params(self) -> Tuple[CSLStockArray, ...]:
        """An array of stocks"""
        return self.__stock_array_params

    @stock_array_params.setter
    def stock_array_params(self, value: Tuple[CSLStockArray, ...]):
        self._property_changed('stock_array_params')
        self.__stock_array_params = value        

    @property
    def index_array_params(self) -> Tuple[CSLIndexArray, ...]:
        """An array of indices"""
        return self.__index_array_params

    @index_array_params.setter
    def index_array_params(self, value: Tuple[CSLIndexArray, ...]):
        self._property_changed('index_array_params')
        self.__index_array_params = value        

    @property
    def fx_cross_array_params(self) -> Tuple[CSLFXCrossArray, ...]:
        """An array of FX crosses"""
        return self.__fx_cross_array_params

    @fx_cross_array_params.setter
    def fx_cross_array_params(self, value: Tuple[CSLFXCrossArray, ...]):
        self._property_changed('fx_cross_array_params')
        self.__fx_cross_array_params = value        


class Cash(Instrument):
        
    """Cash payment"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str] = None,
        payment_date: datetime.date = None,
        notional_amount: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.payment_date = payment_date
        self.notional_amount = notional_amount
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Cash"""
        return AssetClass.Cash        

    @property
    def type(self) -> AssetType:
        """Cash"""
        return AssetType.Cash        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def payment_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__payment_date

    @payment_date.setter
    def payment_date(self, value: datetime.date):
        self._property_changed('payment_date')
        self.__payment_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        


class CommodOTCOptionLeg(Instrument):
        
    """Commodities OTC option leg"""

    @camel_case_translate
    def __init__(
        self,
        underlier: str = None,
        contract: str = None,
        leg_description: str = None,
        fixing_currency: Union[CurrencyName, str] = None,
        fixing_currency_source: str = None,
        option_type: Union[OptionType, str] = None,
        quantity_multiplier: int = None,
        premium: CommodPrice = None,
        premium_settlement: str = None,
        strike: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.contract = contract
        self.leg_description = leg_description
        self.fixing_currency = fixing_currency
        self.fixing_currency_source = fixing_currency_source
        self.option_type = option_type
        self.quantity_multiplier = quantity_multiplier
        self.premium = premium
        self.premium_settlement = premium_settlement
        self.strike = strike
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """OptionLeg"""
        return AssetType.OptionLeg        

    @property
    def underlier(self) -> str:
        """Commodity asset"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: str):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def contract(self) -> str:
        """The observed contract at each pricing date e.g First Nearby, Second Nearby"""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def leg_description(self) -> str:
        """The description of the averaging style"""
        return self.__leg_description

    @leg_description.setter
    def leg_description(self, value: str):
        self._property_changed('leg_description')
        self.__leg_description = value        

    @property
    def fixing_currency(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__fixing_currency

    @fixing_currency.setter
    def fixing_currency(self, value: Union[CurrencyName, str]):
        self._property_changed('fixing_currency')
        self.__fixing_currency = get_enum_value(CurrencyName, value)        

    @property
    def fixing_currency_source(self) -> str:
        """fixing currency conversion rate source"""
        return self.__fixing_currency_source

    @fixing_currency_source.setter
    def fixing_currency_source(self, value: str):
        self._property_changed('fixing_currency_source')
        self.__fixing_currency_source = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def quantity_multiplier(self) -> int:
        """quantity multiplier for driving the long/short direction of the leg"""
        return self.__quantity_multiplier

    @quantity_multiplier.setter
    def quantity_multiplier(self, value: int):
        self._property_changed('quantity_multiplier')
        self.__quantity_multiplier = value        

    @property
    def premium(self) -> CommodPrice:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: CommodPrice):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_settlement(self) -> str:
        """read only description in plain English of settlement terms"""
        return self.__premium_settlement

    @premium_settlement.setter
    def premium_settlement(self, value: str):
        self._property_changed('premium_settlement')
        self.__premium_settlement = value        

    @property
    def strike(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        


class CommodOTCSwapLeg(Instrument):
        
    """Commodities OTC swap leg"""

    @camel_case_translate
    def __init__(
        self,
        underlier: str = None,
        contract: str = None,
        leg_description: str = None,
        fixing_currency: Union[CurrencyName, str] = None,
        fixing_currency_source: str = None,
        quantity_multiplier: int = None,
        fixed_price: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.contract = contract
        self.leg_description = leg_description
        self.fixing_currency = fixing_currency
        self.fixing_currency_source = fixing_currency_source
        self.quantity_multiplier = quantity_multiplier
        self.fixed_price = fixed_price
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """SwapLeg"""
        return AssetType.SwapLeg        

    @property
    def underlier(self) -> str:
        """Commodity asset"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: str):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def contract(self) -> str:
        """The observed contract at each pricing date e.g First Nearby, Second Nearby"""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def leg_description(self) -> str:
        """The description of the averaging style"""
        return self.__leg_description

    @leg_description.setter
    def leg_description(self, value: str):
        self._property_changed('leg_description')
        self.__leg_description = value        

    @property
    def fixing_currency(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__fixing_currency

    @fixing_currency.setter
    def fixing_currency(self, value: Union[CurrencyName, str]):
        self._property_changed('fixing_currency')
        self.__fixing_currency = get_enum_value(CurrencyName, value)        

    @property
    def fixing_currency_source(self) -> str:
        """fixing currency conversion rate source"""
        return self.__fixing_currency_source

    @fixing_currency_source.setter
    def fixing_currency_source(self, value: str):
        self._property_changed('fixing_currency_source')
        self.__fixing_currency_source = value        

    @property
    def quantity_multiplier(self) -> int:
        """quantity multiplier for driving the long/short direction of the leg"""
        return self.__quantity_multiplier

    @quantity_multiplier.setter
    def quantity_multiplier(self, value: int):
        self._property_changed('quantity_multiplier')
        self.__quantity_multiplier = value        

    @property
    def fixed_price(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__fixed_price

    @fixed_price.setter
    def fixed_price(self, value: Union[float, str]):
        self._property_changed('fixed_price')
        self.__fixed_price = value        


class CommodOption(Instrument):
        
    """Flat object representation of a commodities option"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        commodity: str = None,
        commodity_reference_price: str = None,
        underlier_short_name: str = None,
        start: Union[datetime.date, str] = None,
        end: Union[datetime.date, str] = None,
        number_of_periods: int = None,
        strategy: str = None,
        quantity: Union[float, str] = None,
        quantity_unit: str = None,
        quantity_period: str = None,
        settlement: str = None,
        contract: str = None,
        floating_type: str = None,
        fixing_currency: Union[CurrencyName, str] = None,
        fixing_currency_source: str = None,
        strike: str = None,
        strike_currency: Union[CurrencyName, str] = None,
        currency_summary: Union[CurrencyName, str] = None,
        strike_unit: str = None,
        option_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.commodity = commodity
        self.commodity_reference_price = commodity_reference_price
        self.underlier_short_name = underlier_short_name
        self.start = start
        self.end = end
        self.number_of_periods = number_of_periods
        self.strategy = strategy
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.quantity_period = quantity_period
        self.settlement = settlement
        self.contract = contract
        self.floating_type = floating_type
        self.fixing_currency = fixing_currency
        self.fixing_currency_source = fixing_currency_source
        self.strike = strike
        self.strike_currency = strike_currency
        self.currency_summary = currency_summary
        self.strike_unit = strike_unit
        self.option_type = option_type
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def commodity(self) -> str:
        """Commodity asset"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: str):
        self._property_changed('commodity')
        self.__commodity = value        

    @property
    def commodity_reference_price(self) -> str:
        """The ISDA reference price"""
        return self.__commodity_reference_price

    @commodity_reference_price.setter
    def commodity_reference_price(self, value: str):
        self._property_changed('commodity_reference_price')
        self.__commodity_reference_price = value        

    @property
    def underlier_short_name(self) -> str:
        """Plain-English underlier short name"""
        return self.__underlier_short_name

    @underlier_short_name.setter
    def underlier_short_name(self, value: str):
        self._property_changed('underlier_short_name')
        self.__underlier_short_name = value        

    @property
    def start(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__start

    @start.setter
    def start(self, value: Union[datetime.date, str]):
        self._property_changed('start')
        self.__start = value        

    @property
    def end(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__end

    @end.setter
    def end(self, value: Union[datetime.date, str]):
        self._property_changed('end')
        self.__end = value        

    @property
    def number_of_periods(self) -> int:
        """The number of settlement periods"""
        return self.__number_of_periods

    @number_of_periods.setter
    def number_of_periods(self, value: int):
        self._property_changed('number_of_periods')
        self.__number_of_periods = value        

    @property
    def strategy(self) -> str:
        """Option Strategy"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def quantity(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: Union[float, str]):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def quantity_unit(self) -> str:
        """Commodity asset"""
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: str):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def quantity_period(self) -> str:
        """period corresponding to a quantity amount"""
        return self.__quantity_period

    @quantity_period.setter
    def quantity_period(self, value: str):
        self._property_changed('quantity_period')
        self.__quantity_period = value        

    @property
    def settlement(self) -> str:
        """read only description in plain English of settlement terms"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: str):
        self._property_changed('settlement')
        self.__settlement = value        

    @property
    def contract(self) -> str:
        """The observed contract at each pricing date e.g First Nearby, Second Nearby"""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def floating_type(self) -> str:
        """The description of the averaging style"""
        return self.__floating_type

    @floating_type.setter
    def floating_type(self, value: str):
        self._property_changed('floating_type')
        self.__floating_type = value        

    @property
    def fixing_currency(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__fixing_currency

    @fixing_currency.setter
    def fixing_currency(self, value: Union[CurrencyName, str]):
        self._property_changed('fixing_currency')
        self.__fixing_currency = get_enum_value(CurrencyName, value)        

    @property
    def fixing_currency_source(self) -> str:
        """fixing currency conversion rate source"""
        return self.__fixing_currency_source

    @fixing_currency_source.setter
    def fixing_currency_source(self, value: str):
        self._property_changed('fixing_currency_source')
        self.__fixing_currency_source = value        

    @property
    def strike(self) -> str:
        """strike price (e.g. 50 or 50qd)"""
        return self.__strike

    @strike.setter
    def strike(self, value: str):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def strike_currency(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__strike_currency

    @strike_currency.setter
    def strike_currency(self, value: Union[CurrencyName, str]):
        self._property_changed('strike_currency')
        self.__strike_currency = get_enum_value(CurrencyName, value)        

    @property
    def currency_summary(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__currency_summary

    @currency_summary.setter
    def currency_summary(self, value: Union[CurrencyName, str]):
        self._property_changed('currency_summary')
        self.__currency_summary = get_enum_value(CurrencyName, value)        

    @property
    def strike_unit(self) -> str:
        """Commodity asset"""
        return self.__strike_unit

    @strike_unit.setter
    def strike_unit(self, value: str):
        self._property_changed('strike_unit')
        self.__strike_unit = value        

    @property
    def option_type(self) -> str:
        """e.g. call or put"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: str):
        self._property_changed('option_type')
        self.__option_type = value        


class CommodSwap(Instrument):
        
    """Flat representation of a commodities swap"""

    @camel_case_translate
    def __init__(
        self,
        commodity: str = None,
        commodity_reference_price: str = None,
        start: Union[datetime.date, str] = None,
        end: Union[datetime.date, str] = None,
        contract: str = None,
        number_of_periods: int = None,
        strategy: str = None,
        quantity: Union[float, str] = None,
        quantity_unit: str = None,
        quantity_period: Union[Period, str] = None,
        settlement: str = None,
        floating_type: str = None,
        fixing_currency: Union[CurrencyName, str] = None,
        fixing_currency_source: str = None,
        fixed_price: Union[float, str] = None,
        fixed_price_unit: str = None,
        name: str = None
    ):        
        super().__init__()
        self.commodity = commodity
        self.commodity_reference_price = commodity_reference_price
        self.start = start
        self.end = end
        self.contract = contract
        self.number_of_periods = number_of_periods
        self.strategy = strategy
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.quantity_period = quantity_period
        self.settlement = settlement
        self.floating_type = floating_type
        self.fixing_currency = fixing_currency
        self.fixing_currency_source = fixing_currency_source
        self.fixed_price = fixed_price
        self.fixed_price_unit = fixed_price_unit
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """Swap"""
        return AssetType.Swap        

    @property
    def commodity(self) -> str:
        """Commodity asset"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: str):
        self._property_changed('commodity')
        self.__commodity = value        

    @property
    def commodity_reference_price(self) -> str:
        """The ISDA reference price"""
        return self.__commodity_reference_price

    @commodity_reference_price.setter
    def commodity_reference_price(self, value: str):
        self._property_changed('commodity_reference_price')
        self.__commodity_reference_price = value        

    @property
    def start(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__start

    @start.setter
    def start(self, value: Union[datetime.date, str]):
        self._property_changed('start')
        self.__start = value        

    @property
    def end(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__end

    @end.setter
    def end(self, value: Union[datetime.date, str]):
        self._property_changed('end')
        self.__end = value        

    @property
    def contract(self) -> str:
        """The observed contract at each pricing date e.g First Nearby, Second Nearby"""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def number_of_periods(self) -> int:
        """The number of settlement periods"""
        return self.__number_of_periods

    @number_of_periods.setter
    def number_of_periods(self, value: int):
        self._property_changed('number_of_periods')
        self.__number_of_periods = value        

    @property
    def strategy(self) -> str:
        """Swap Strategy : Strip and Commodity Spread"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def quantity(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: Union[float, str]):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def quantity_unit(self) -> str:
        """Commodity asset"""
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: str):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def quantity_period(self) -> Union[Period, str]:
        """A coding scheme to define a period corresponding to a quantity amount"""
        return self.__quantity_period

    @quantity_period.setter
    def quantity_period(self, value: Union[Period, str]):
        self._property_changed('quantity_period')
        self.__quantity_period = get_enum_value(Period, value)        

    @property
    def settlement(self) -> str:
        """read only description in plain English of settlement terms"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: str):
        self._property_changed('settlement')
        self.__settlement = value        

    @property
    def floating_type(self) -> str:
        """The description of the averaging style"""
        return self.__floating_type

    @floating_type.setter
    def floating_type(self, value: str):
        self._property_changed('floating_type')
        self.__floating_type = value        

    @property
    def fixing_currency(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__fixing_currency

    @fixing_currency.setter
    def fixing_currency(self, value: Union[CurrencyName, str]):
        self._property_changed('fixing_currency')
        self.__fixing_currency = get_enum_value(CurrencyName, value)        

    @property
    def fixing_currency_source(self) -> str:
        """fixing currency conversion rate source"""
        return self.__fixing_currency_source

    @fixing_currency_source.setter
    def fixing_currency_source(self, value: str):
        self._property_changed('fixing_currency_source')
        self.__fixing_currency_source = value        

    @property
    def fixed_price(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__fixed_price

    @fixed_price.setter
    def fixed_price(self, value: Union[float, str]):
        self._property_changed('fixed_price')
        self.__fixed_price = value        

    @property
    def fixed_price_unit(self) -> str:
        """Commodity asset"""
        return self.__fixed_price_unit

    @fixed_price_unit.setter
    def fixed_price_unit(self, value: str):
        self._property_changed('fixed_price_unit')
        self.__fixed_price_unit = value        


class CommodVarianceSwap(Instrument):
        
    """Object representation of a commodities volitility / variance swap"""

    @camel_case_translate
    def __init__(
        self,
        side: Union[BuySell, str] = None,
        notional: float = 1,
        notional_currency: Union[Currency, str] = None,
        asset: str = None,
        asset_fixing_source: str = None,
        contract: str = None,
        fixing_currency: Union[Currency, str] = None,
        fx_fixing_source: str = None,
        settlement_date: Union[datetime.date, str] = None,
        strike: Union[float, str] = None,
        variance_convention: Union[VarianceConvention, str] = None,
        annualization_factor: float = None,
        divisor: str = None,
        start_date: datetime.date = None,
        end_date: Union[datetime.date, str] = None,
        mean_rule: Union[CommodMeanRule, str] = None,
        fixed_mean: float = None,
        first_fixing: float = None,
        name: str = None
    ):        
        super().__init__()
        self.side = side
        self.notional = notional
        self.notional_currency = notional_currency
        self.asset = asset
        self.asset_fixing_source = asset_fixing_source
        self.contract = contract
        self.fixing_currency = fixing_currency
        self.fx_fixing_source = fx_fixing_source
        self.settlement_date = settlement_date
        self.strike = strike
        self.variance_convention = variance_convention
        self.annualization_factor = annualization_factor
        self.divisor = divisor
        self.start_date = start_date
        self.end_date = end_date
        self.mean_rule = mean_rule
        self.fixed_mean = fixed_mean
        self.first_fixing = first_fixing
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """VarianceSwap"""
        return AssetType.VarianceSwap        

    @property
    def side(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__side

    @side.setter
    def side(self, value: Union[BuySell, str]):
        self._property_changed('side')
        self.__side = get_enum_value(BuySell, value)        

    @property
    def notional(self) -> float:
        """The notional amount of the variance swap"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """The currency of the notional amount"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def asset(self) -> str:
        """Commodity asset"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self._property_changed('asset')
        self.__asset = value        

    @property
    def asset_fixing_source(self) -> str:
        return self.__asset_fixing_source

    @asset_fixing_source.setter
    def asset_fixing_source(self, value: str):
        self._property_changed('asset_fixing_source')
        self.__asset_fixing_source = value        

    @property
    def contract(self) -> str:
        """The contract we are observing (e.g. Z24)"""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def fixing_currency(self) -> Union[Currency, str]:
        """The currency in which we observe the fix"""
        return self.__fixing_currency

    @fixing_currency.setter
    def fixing_currency(self, value: Union[Currency, str]):
        self._property_changed('fixing_currency')
        self.__fixing_currency = get_enum_value(Currency, value)        

    @property
    def fx_fixing_source(self) -> str:
        """The source to use in the condition that the fixing currency is different from
           the underlying currency"""
        return self.__fx_fixing_source

    @fx_fixing_source.setter
    def fx_fixing_source(self, value: str):
        self._property_changed('fx_fixing_source')
        self.__fx_fixing_source = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date of the trade"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def strike(self) -> Union[float, str]:
        """The strike in variance, default to ATM"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def variance_convention(self) -> Union[VarianceConvention, str]:
        """'Annualized' to annualize the variance (using Annualization Factor) or 'total'
           for no annualization'"""
        return self.__variance_convention

    @variance_convention.setter
    def variance_convention(self, value: Union[VarianceConvention, str]):
        self._property_changed('variance_convention')
        self.__variance_convention = get_enum_value(VarianceConvention, value)        

    @property
    def annualization_factor(self) -> float:
        """Annualization factor used to compute variance, defaults to 252"""
        return self.__annualization_factor

    @annualization_factor.setter
    def annualization_factor(self, value: float):
        self._property_changed('annualization_factor')
        self.__annualization_factor = value        

    @property
    def divisor(self) -> str:
        """Number of returns or Number of returns - 1"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: str):
        self._property_changed('divisor')
        self.__divisor = value        

    @property
    def start_date(self) -> datetime.date:
        """The start date of the observation"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> Union[datetime.date, str]:
        """The end date of the observation"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: Union[datetime.date, str]):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def mean_rule(self) -> Union[CommodMeanRule, str]:
        """Commodity mean rule"""
        return self.__mean_rule

    @mean_rule.setter
    def mean_rule(self, value: Union[CommodMeanRule, str]):
        self._property_changed('mean_rule')
        self.__mean_rule = get_enum_value(CommodMeanRule, value)        

    @property
    def fixed_mean(self) -> float:
        """True if we want to specify the mean to be used in variance computation"""
        return self.__fixed_mean

    @fixed_mean.setter
    def fixed_mean(self, value: float):
        self._property_changed('fixed_mean')
        self.__fixed_mean = value        

    @property
    def first_fixing(self) -> float:
        """By default there is none, if populate would use it as the first fixing"""
        return self.__first_fixing

    @first_fixing.setter
    def first_fixing(self, value: float):
        self._property_changed('first_fixing')
        self.__first_fixing = value        


class EqCliquet(Instrument):
        
    """Object representation of an Equity Cliquet"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str] = None,
        underlier_type: Union[UnderlierType, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        strike_price: float = None,
        currency: Union[Currency, str] = None,
        first_valuation_date: datetime.date = None,
        global_floor: float = -1000000,
        global_cap: float = 1000000,
        last_valuation_date: datetime.date = None,
        notional_amount: Union[float, str] = None,
        payment_frequency: str = 'Maturity',
        return_style: str = 'Rate of Return',
        return_type: str = 'Sum',
        valuation_period: str = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.underlier_type = underlier_type
        self.expiration_date = expiration_date
        self.strike_price = strike_price
        self.currency = currency
        self.first_valuation_date = first_valuation_date
        self.global_floor = global_floor
        self.global_cap = global_cap
        self.last_valuation_date = last_valuation_date
        self.notional_amount = notional_amount
        self.payment_frequency = payment_frequency
        self.return_style = return_style
        self.return_type = return_type
        self.valuation_period = valuation_period
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Cliquet"""
        return AssetType.Cliquet        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def strike_price(self) -> float:
        """Strike price as value"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: float):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def first_valuation_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__first_valuation_date

    @first_valuation_date.setter
    def first_valuation_date(self, value: datetime.date):
        self._property_changed('first_valuation_date')
        self.__first_valuation_date = value        

    @property
    def global_floor(self) -> float:
        """Global Floor of return, relevant only if paying at maturity"""
        return self.__global_floor

    @global_floor.setter
    def global_floor(self, value: float):
        self._property_changed('global_floor')
        self.__global_floor = value        

    @property
    def global_cap(self) -> float:
        """Global Cap of return, relevant only if paying at maturity"""
        return self.__global_cap

    @global_cap.setter
    def global_cap(self, value: float):
        self._property_changed('global_cap')
        self.__global_cap = value        

    @property
    def last_valuation_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__last_valuation_date

    @last_valuation_date.setter
    def last_valuation_date(self, value: datetime.date):
        self._property_changed('last_valuation_date')
        self.__last_valuation_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional of this position"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def payment_frequency(self) -> str:
        return self.__payment_frequency

    @payment_frequency.setter
    def payment_frequency(self, value: str):
        self._property_changed('payment_frequency')
        self.__payment_frequency = value        

    @property
    def return_style(self) -> str:
        """Return calculation style"""
        return self.__return_style

    @return_style.setter
    def return_style(self, value: str):
        self._property_changed('return_style')
        self.__return_style = value        

    @property
    def return_type(self) -> str:
        """Sum or Product of periodic return, relevant only if paying at maturity"""
        return self.__return_type

    @return_type.setter
    def return_type(self, value: str):
        self._property_changed('return_type')
        self.__return_type = value        

    @property
    def valuation_period(self) -> str:
        """Tenor"""
        return self.__valuation_period

    @valuation_period.setter
    def valuation_period(self, value: str):
        self._property_changed('valuation_period')
        self.__valuation_period = value        


class EqForward(Instrument):
        
    """Object representation of an equity forward"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str] = None,
        underlier_type: Union[UnderlierType, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        forward_price: float = None,
        number_of_shares: int = 1,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.underlier_type = underlier_type
        self.expiration_date = expiration_date
        self.forward_price = forward_price
        self.number_of_shares = number_of_shares
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def forward_price(self) -> float:
        """Forward price"""
        return self.__forward_price

    @forward_price.setter
    def forward_price(self, value: float):
        self._property_changed('forward_price')
        self.__forward_price = value        

    @property
    def number_of_shares(self) -> int:
        """Number of shares"""
        return self.__number_of_shares

    @number_of_shares.setter
    def number_of_shares(self, value: int):
        self._property_changed('number_of_shares')
        self.__number_of_shares = value        


class EqOption(Instrument):
        
    """Instrument definition for equity option"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        strike_price: Union[float, str] = None,
        option_type: Union[OptionType, str] = None,
        option_style: Union[OptionStyle, str] = None,
        number_of_options: float = None,
        exchange: str = None,
        multiplier: float = None,
        settlement_date: Union[datetime.date, str] = None,
        settlement_currency: Union[Currency, str] = None,
        premium: float = 0,
        premium_payment_date: Union[datetime.date, str] = None,
        valuation_time: Union[ValuationTime, str] = None,
        method_of_settlement: Union[OptionSettlementMethod, str] = None,
        underlier_type: Union[UnderlierType, str] = None,
        buy_sell: Union[BuySell, str] = None,
        premium_currency: Union[Currency, str] = None,
        trade_as: Union[TradeAs, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.expiration_date = expiration_date
        self.strike_price = strike_price
        self.option_type = option_type
        self.option_style = option_style
        self.number_of_options = number_of_options
        self.exchange = exchange
        self.multiplier = multiplier
        self.settlement_date = settlement_date
        self.settlement_currency = settlement_currency
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.valuation_time = valuation_time
        self.method_of_settlement = method_of_settlement
        self.underlier_type = underlier_type
        self.buy_sell = buy_sell
        self.premium_currency = premium_currency
        self.trade_as = trade_as
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def option_style(self) -> Union[OptionStyle, str]:
        """Option Exercise Style"""
        return self.__option_style

    @option_style.setter
    def option_style(self, value: Union[OptionStyle, str]):
        self._property_changed('option_style')
        self.__option_style = get_enum_value(OptionStyle, value)        

    @property
    def number_of_options(self) -> float:
        """Number of options"""
        return self.__number_of_options

    @number_of_options.setter
    def number_of_options(self, value: float):
        self._property_changed('number_of_options')
        self.__number_of_options = value        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def multiplier(self) -> float:
        """Number of stock units per option contract"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def valuation_time(self) -> Union[ValuationTime, str]:
        """Valuation time (e.g. MktClose, MktOpen) of the underlying level for exercise"""
        return self.__valuation_time

    @valuation_time.setter
    def valuation_time(self, value: Union[ValuationTime, str]):
        self._property_changed('valuation_time')
        self.__valuation_time = get_enum_value(ValuationTime, value)        

    @property
    def method_of_settlement(self) -> Union[OptionSettlementMethod, str]:
        """How the option is settled (e.g. Cash, Physical)"""
        return self.__method_of_settlement

    @method_of_settlement.setter
    def method_of_settlement(self, value: Union[OptionSettlementMethod, str]):
        self._property_changed('method_of_settlement')
        self.__method_of_settlement = get_enum_value(OptionSettlementMethod, value)        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def trade_as(self) -> Union[TradeAs, str]:
        """Option trade as (i.e. listed, otc, lookalike etc)"""
        return self.__trade_as

    @trade_as.setter
    def trade_as(self, value: Union[TradeAs, str]):
        self._property_changed('trade_as')
        self.__trade_as = get_enum_value(TradeAs, value)        


class EqOptionLeg(Instrument):
        
    """Instrument definition for equity option leg"""

    @camel_case_translate
    def __init__(
        self,
        expiration_date: Union[datetime.date, str] = None,
        strike_price: Union[float, str] = None,
        option_type: Union[OptionType, str] = None,
        option_style: Union[OptionStyle, str] = None,
        number_of_options: float = None,
        exchange: str = None,
        multiplier: float = None,
        settlement_date: Union[datetime.date, str] = None,
        settlement_currency: Union[Currency, str] = None,
        premium: float = None,
        premium_payment_date: Union[datetime.date, str] = None,
        valuation_time: Union[ValuationTime, str] = None,
        method_of_settlement: Union[OptionSettlementMethod, str] = None,
        buy_sell: Union[BuySell, str] = None,
        premium_currency: Union[Currency, str] = None,
        trade_as: Union[TradeAs, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.expiration_date = expiration_date
        self.strike_price = strike_price
        self.option_type = option_type
        self.option_style = option_style
        self.number_of_options = number_of_options
        self.exchange = exchange
        self.multiplier = multiplier
        self.settlement_date = settlement_date
        self.settlement_currency = settlement_currency
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.valuation_time = valuation_time
        self.method_of_settlement = method_of_settlement
        self.buy_sell = buy_sell
        self.premium_currency = premium_currency
        self.trade_as = trade_as
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """OptionLeg"""
        return AssetType.OptionLeg        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def option_style(self) -> Union[OptionStyle, str]:
        """Option Exercise Style"""
        return self.__option_style

    @option_style.setter
    def option_style(self, value: Union[OptionStyle, str]):
        self._property_changed('option_style')
        self.__option_style = get_enum_value(OptionStyle, value)        

    @property
    def number_of_options(self) -> float:
        """Number of options"""
        return self.__number_of_options

    @number_of_options.setter
    def number_of_options(self, value: float):
        self._property_changed('number_of_options')
        self.__number_of_options = value        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def multiplier(self) -> float:
        """Number of stock units per option contract"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def valuation_time(self) -> Union[ValuationTime, str]:
        """Valuation time (e.g. MktClose, MktOpen) of the underlying level for exercise"""
        return self.__valuation_time

    @valuation_time.setter
    def valuation_time(self, value: Union[ValuationTime, str]):
        self._property_changed('valuation_time')
        self.__valuation_time = get_enum_value(ValuationTime, value)        

    @property
    def method_of_settlement(self) -> Union[OptionSettlementMethod, str]:
        """How the option is settled (e.g. Cash, Physical)"""
        return self.__method_of_settlement

    @method_of_settlement.setter
    def method_of_settlement(self, value: Union[OptionSettlementMethod, str]):
        self._property_changed('method_of_settlement')
        self.__method_of_settlement = get_enum_value(OptionSettlementMethod, value)        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def trade_as(self) -> Union[TradeAs, str]:
        """Option trade as (i.e. listed, otc, lookalike etc)"""
        return self.__trade_as

    @trade_as.setter
    def trade_as(self, value: Union[TradeAs, str]):
        self._property_changed('trade_as')
        self.__trade_as = get_enum_value(TradeAs, value)        


class EqStock(Instrument):
        
    """Instrument definition for equities"""

    @camel_case_translate
    def __init__(
        self,
        asset_name: str = None,
        buy_sell: Union[BuySell, str] = None,
        premium: float = None,
        premium_currency: str = None,
        quantity: float = None,
        settlement_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_name = asset_name
        self.buy_sell = buy_sell
        self.premium = premium
        self.premium_currency = premium_currency
        self.quantity = quantity
        self.settlement_date = settlement_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Single Stock"""
        return AssetType.Single_Stock        

    @property
    def asset_name(self) -> str:
        return self.__asset_name

    @asset_name.setter
    def asset_name(self, value: str):
        self._property_changed('asset_name')
        self.__asset_name = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def premium(self) -> float:
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> str:
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: str):
        self._property_changed('premium_currency')
        self.__premium_currency = value        

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def settlement_date(self) -> datetime.date:
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        


class EqSynthetic(Instrument):
        
    """Instrument definition for equity synthetics"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str],
        expiry: str,
        currency: Union[Currency, str] = None,
        swap_type: str = 'Eq Swap',
        buy_sell: Union[BuySell, str] = None,
        underlier_type: Union[UnderlierType, str] = None,
        effective_date: datetime.date = None,
        num_of_underlyers: float = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.currency = currency
        self.swap_type = swap_type
        self.buy_sell = buy_sell
        self.underlier_type = underlier_type
        self.effective_date = effective_date
        self.num_of_underlyers = num_of_underlyers
        self.expiry = expiry
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Synthetic"""
        return AssetType.Synthetic        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def swap_type(self) -> str:
        return self.__swap_type

    @swap_type.setter
    def swap_type(self, value: str):
        self._property_changed('swap_type')
        self.__swap_type = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        

    @property
    def effective_date(self) -> datetime.date:
        """The date on which the synthetic becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: datetime.date):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def num_of_underlyers(self) -> float:
        """number of underlyers referenced in synthetic contract"""
        return self.__num_of_underlyers

    @num_of_underlyers.setter
    def num_of_underlyers(self, value: float):
        self._property_changed('num_of_underlyers')
        self.__num_of_underlyers = value        

    @property
    def expiry(self) -> str:
        """Tenor"""
        return self.__expiry

    @expiry.setter
    def expiry(self, value: str):
        self._property_changed('expiry')
        self.__expiry = value        


class EqVarianceSwap(Instrument):
        
    """Instrument definition for equity variance swap"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str] = None,
        underlier_type: Union[UnderlierType, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        strike_price: Union[float, str] = None,
        variance_cap: float = None,
        settlement_date: Union[datetime.date, str] = None,
        premium: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.underlier_type = underlier_type
        self.expiration_date = expiration_date
        self.strike_price = strike_price
        self.variance_cap = variance_cap
        self.settlement_date = settlement_date
        self.premium = premium
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """VarianceSwap"""
        return AssetType.VarianceSwap        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Variance strike as value or percentage string e.g. 62.5, 95%"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def variance_cap(self) -> float:
        """Variance Cap as absolute value"""
        return self.__variance_cap

    @variance_cap.setter
    def variance_cap(self, value: float):
        self._property_changed('variance_cap')
        self.__variance_cap = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def premium(self) -> Union[float, str]:
        """VarSwap premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        


class FRA(Instrument):
        
    """A forward rate agreement"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        clearing_house: Union[SwapClearingHouse, str] = None,
        clearing_legally_binding: float = None,
        day_count_fraction: Union[DayCountFraction, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        fixed_rate: Union[float, str] = None,
        frequency: str = None,
        calendar: str = None,
        rate_option: str = None,
        maturity: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        payment_delay: str = None,
        roll_convention: str = None,
        notional_amount: Union[float, str] = None,
        spread: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.clearing_house = clearing_house
        self.clearing_legally_binding = clearing_legally_binding
        self.day_count_fraction = day_count_fraction
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.fixed_rate = fixed_rate
        self.frequency = frequency
        self.calendar = calendar
        self.rate_option = rate_option
        self.maturity = maturity
        self.notional_currency = notional_currency
        self.payment_delay = payment_delay
        self.roll_convention = roll_convention
        self.notional_amount = notional_amount
        self.spread = spread
        self.effective_date = effective_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """FRA"""
        return AssetType.FRA        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self._property_changed('clearing_house')
        self.__clearing_house = get_enum_value(SwapClearingHouse, value)        

    @property
    def clearing_legally_binding(self) -> float:
        return self.__clearing_legally_binding

    @clearing_legally_binding.setter
    def clearing_legally_binding(self, value: float):
        self._property_changed('clearing_legally_binding')
        self.__clearing_legally_binding = value        

    @property
    def day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction"""
        return self.__day_count_fraction

    @day_count_fraction.setter
    def day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('day_count_fraction')
        self.__day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The forward rate"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self._property_changed('fixed_rate')
        self.__fixed_rate = value        

    @property
    def frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def calendar(self) -> str:
        """The calendar"""
        return self.__calendar

    @calendar.setter
    def calendar(self, value: str):
        self._property_changed('calendar')
        self.__calendar = value        

    @property
    def rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__rate_option

    @rate_option.setter
    def rate_option(self, value: str):
        self._property_changed('rate_option')
        self.__rate_option = value        

    @property
    def maturity(self) -> Union[Union[datetime.date, str], str]:
        """The maturity of the FRA, e.g. 2050-04-01, 10y"""
        return self.__maturity

    @maturity.setter
    def maturity(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('maturity')
        self.__maturity = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def payment_delay(self) -> str:
        """The delay of payments"""
        return self.__payment_delay

    @payment_delay.setter
    def payment_delay(self, value: str):
        self._property_changed('payment_delay')
        self.__payment_delay = value        

    @property
    def roll_convention(self) -> str:
        """The roll convention"""
        return self.__roll_convention

    @roll_convention.setter
    def roll_convention(self, value: str):
        self._property_changed('roll_convention')
        self.__roll_convention = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def spread(self) -> Union[float, str]:
        """The spread over the floating rate"""
        return self.__spread

    @spread.setter
    def spread(self, value: Union[float, str]):
        self._property_changed('spread')
        self.__spread = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the FRA becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        


class FXBinary(Instrument):
        
    """Object representation of a FX binary option"""

    @camel_case_translate
    def __init__(
        self,
        pair: str = None,
        buy_sell: Union[BuySell, str] = None,
        option_type: Union[OptionType, str] = None,
        notional_amount: Union[float, str] = None,
        notional_currency: Union[Currency, str] = None,
        strike_price: Union[float, str] = None,
        settlement_date: Union[datetime.date, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        expiration_time: str = None,
        premium: Union[float, str] = None,
        premium_currency: Union[Currency, str] = None,
        premium_payment_date: str = None,
        fixing_source: str = None,
        name: str = None
    ):        
        super().__init__()
        self.pair = pair
        self.buy_sell = buy_sell
        self.option_type = option_type
        self.notional_amount = notional_amount
        self.notional_currency = notional_currency
        self.strike_price = strike_price
        self.settlement_date = settlement_date
        self.expiration_date = expiration_date
        self.expiration_time = expiration_time
        self.premium = premium
        self.premium_currency = premium_currency
        self.premium_payment_date = premium_payment_date
        self.fixing_source = fixing_source
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """Binary"""
        return AssetType.Binary        

    @property
    def pair(self) -> str:
        """A currency pair, e.g.: EURUSD or EUR USD"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self._property_changed('pair')
        self.__pair = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date of the option, after expiration"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def expiration_time(self) -> str:
        """The location and (optionally) time of spot for expiration"""
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value: str):
        self._property_changed('expiration_time')
        self.__expiration_time = value        

    @property
    def premium(self) -> Union[float, str]:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def premium_payment_date(self) -> str:
        """Payment date of the option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: str):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fixing_source(self) -> str:
        """The data source to be used for observation of FX spot on the fixing date"""
        return self.__fixing_source

    @fixing_source.setter
    def fixing_source(self, value: str):
        self._property_changed('fixing_source')
        self.__fixing_source = value        


class FXForward(Instrument):
        
    """Object representation of an FX forward"""

    @camel_case_translate
    def __init__(
        self,
        pair: str = None,
        settlement_date: Union[datetime.date, str] = None,
        forward_rate: Union[float, str] = None,
        notional_amount: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.pair = pair
        self.settlement_date = settlement_date
        self.forward_rate = forward_rate
        self.notional_amount = notional_amount
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def pair(self) -> str:
        """A currency pair, e.g.: EURUSD or EUR USD"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self._property_changed('pair')
        self.__pair = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def forward_rate(self) -> Union[float, str]:
        """Forward FX rate"""
        return self.__forward_rate

    @forward_rate.setter
    def forward_rate(self, value: Union[float, str]):
        self._property_changed('forward_rate')
        self.__forward_rate = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        


class FXMultiCrossBinaryLeg(Instrument):
        
    """Object representation of a single leg of a multi-cross binary option"""

    @camel_case_translate
    def __init__(
        self,
        pair: str = None,
        option_type: Union[OptionType, str] = None,
        strike_price: Union[float, str] = None,
        fixing_source: str = None,
        name: str = None
    ):        
        super().__init__()
        self.pair = pair
        self.option_type = option_type
        self.strike_price = strike_price
        self.fixing_source = fixing_source
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """MultiCrossBinaryLeg"""
        return AssetType.MultiCrossBinaryLeg        

    @property
    def pair(self) -> str:
        """A currency pair, e.g.: EURUSD or EUR USD"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self._property_changed('pair')
        self.__pair = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def fixing_source(self) -> str:
        """The data source to be used for observation of FX spot on the fixing date"""
        return self.__fixing_source

    @fixing_source.setter
    def fixing_source(self, value: str):
        self._property_changed('fixing_source')
        self.__fixing_source = value        


class FXOption(Instrument):
        
    """Object representation of an FX option"""

    @camel_case_translate
    def __init__(
        self,
        pair: str = None,
        buy_sell: Union[BuySell, str] = None,
        option_type: Union[OptionType, str] = None,
        notional_amount: Union[float, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount_other_currency: Union[float, str] = None,
        strike_price: Union[float, str] = None,
        settlement_date: Union[datetime.date, str] = None,
        settlement_currency: Union[Currency, str] = None,
        settlement_rate_option: str = None,
        method_of_settlement: Union[OptionSettlementMethod, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        expiration_time: str = None,
        premium: Union[float, str] = None,
        premium_currency: Union[Currency, str] = None,
        premium_payment_date: str = None,
        name: str = None
    ):        
        super().__init__()
        self.pair = pair
        self.buy_sell = buy_sell
        self.option_type = option_type
        self.notional_amount = notional_amount
        self.notional_currency = notional_currency
        self.notional_amount_other_currency = notional_amount_other_currency
        self.strike_price = strike_price
        self.settlement_date = settlement_date
        self.settlement_currency = settlement_currency
        self.settlement_rate_option = settlement_rate_option
        self.method_of_settlement = method_of_settlement
        self.expiration_date = expiration_date
        self.expiration_time = expiration_time
        self.premium = premium
        self.premium_currency = premium_currency
        self.premium_payment_date = premium_payment_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def pair(self) -> str:
        """A currency pair, e.g.: EURUSD or EUR USD"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self._property_changed('pair')
        self.__pair = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount_other_currency(self) -> Union[float, str]:
        """Notional amount in currency other than NotionalCurrency from the pair"""
        return self.__notional_amount_other_currency

    @notional_amount_other_currency.setter
    def notional_amount_other_currency(self, value: Union[float, str]):
        self._property_changed('notional_amount_other_currency')
        self.__notional_amount_other_currency = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date of the option, after expiration"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency of settlement"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        

    @property
    def settlement_rate_option(self) -> str:
        """The source of spot for settlement"""
        return self.__settlement_rate_option

    @settlement_rate_option.setter
    def settlement_rate_option(self, value: str):
        self._property_changed('settlement_rate_option')
        self.__settlement_rate_option = value        

    @property
    def method_of_settlement(self) -> Union[OptionSettlementMethod, str]:
        """How the option is settled (e.g. Cash, Physical)"""
        return self.__method_of_settlement

    @method_of_settlement.setter
    def method_of_settlement(self, value: Union[OptionSettlementMethod, str]):
        self._property_changed('method_of_settlement')
        self.__method_of_settlement = get_enum_value(OptionSettlementMethod, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def expiration_time(self) -> str:
        """The location and (optionally) time of spot for expiration"""
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value: str):
        self._property_changed('expiration_time')
        self.__expiration_time = value        

    @property
    def premium(self) -> Union[float, str]:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def premium_payment_date(self) -> str:
        """Payment date of the option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: str):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        


class FXOptionLeg(Instrument):
        
    """Object representation of a FX option leg used in FXOptionStrategy"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        option_type: Union[OptionType, str] = None,
        notional_amount: Union[float, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount_other_currency: Union[float, str] = None,
        strike_price: Union[float, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        settlement_date: Union[datetime.date, str] = None,
        premium: Union[float, str] = None,
        premium_currency: Union[Currency, str] = None,
        premium_payment_date: str = None,
        settlement_currency: Union[Currency, str] = None,
        settlement_rate_option: str = None,
        method_of_settlement: Union[OptionSettlementMethod, str] = None,
        expiration_time: str = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.option_type = option_type
        self.notional_amount = notional_amount
        self.notional_currency = notional_currency
        self.notional_amount_other_currency = notional_amount_other_currency
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.settlement_date = settlement_date
        self.premium = premium
        self.premium_currency = premium_currency
        self.premium_payment_date = premium_payment_date
        self.settlement_currency = settlement_currency
        self.settlement_rate_option = settlement_rate_option
        self.method_of_settlement = method_of_settlement
        self.expiration_time = expiration_time
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """OptionLeg"""
        return AssetType.OptionLeg        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount_other_currency(self) -> Union[float, str]:
        """Notional amount in currency other than NotionalCurrency from the pair"""
        return self.__notional_amount_other_currency

    @notional_amount_other_currency.setter
    def notional_amount_other_currency(self, value: Union[float, str]):
        self._property_changed('notional_amount_other_currency')
        self.__notional_amount_other_currency = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date of the option, after expiration"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def premium(self) -> Union[float, str]:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def premium_payment_date(self) -> str:
        """Payment date of the option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: str):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency of settlement"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        

    @property
    def settlement_rate_option(self) -> str:
        """The source of spot for settlement"""
        return self.__settlement_rate_option

    @settlement_rate_option.setter
    def settlement_rate_option(self, value: str):
        self._property_changed('settlement_rate_option')
        self.__settlement_rate_option = value        

    @property
    def method_of_settlement(self) -> Union[OptionSettlementMethod, str]:
        """How the option is settled (e.g. Cash, Physical)"""
        return self.__method_of_settlement

    @method_of_settlement.setter
    def method_of_settlement(self, value: Union[OptionSettlementMethod, str]):
        self._property_changed('method_of_settlement')
        self.__method_of_settlement = get_enum_value(OptionSettlementMethod, value)        

    @property
    def expiration_time(self) -> str:
        """The location and (optionally) time of spot for expiration"""
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value: str):
        self._property_changed('expiration_time')
        self.__expiration_time = value        


class FXVolatilitySwap(Instrument):
        
    """Object representation of an FX Vol Swap"""

    @camel_case_translate
    def __init__(
        self,
        pair: str = None,
        buy_sell: Union[BuySell, str] = None,
        strike_vol: Union[float, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        first_fixing_date: Union[datetime.date, str] = None,
        last_fixing_date: Union[datetime.date, str] = None,
        settlement_date: Union[datetime.date, str] = None,
        fixing_source: str = None,
        fixing_frequency: str = None,
        annualization_factor: float = None,
        calculate_mean_return: float = 0,
        name: str = None
    ):        
        super().__init__()
        self.pair = pair
        self.buy_sell = buy_sell
        self.strike_vol = strike_vol
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.first_fixing_date = first_fixing_date
        self.last_fixing_date = last_fixing_date
        self.settlement_date = settlement_date
        self.fixing_source = fixing_source
        self.fixing_frequency = fixing_frequency
        self.annualization_factor = annualization_factor
        self.calculate_mean_return = calculate_mean_return
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """VolatilitySwap"""
        return AssetType.VolatilitySwap        

    @property
    def pair(self) -> str:
        """A currency pair, e.g.: EURUSD or EUR USD"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self._property_changed('pair')
        self.__pair = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def strike_vol(self) -> Union[float, str]:
        """Volatility strike"""
        return self.__strike_vol

    @strike_vol.setter
    def strike_vol(self, value: Union[float, str]):
        self._property_changed('strike_vol')
        self.__strike_vol = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """ Notional amount in dollar terms"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def first_fixing_date(self) -> Union[datetime.date, str]:
        """First averaging date or observation date"""
        return self.__first_fixing_date

    @first_fixing_date.setter
    def first_fixing_date(self, value: Union[datetime.date, str]):
        self._property_changed('first_fixing_date')
        self.__first_fixing_date = value        

    @property
    def last_fixing_date(self) -> Union[datetime.date, str]:
        """Last averaging date or valuation date"""
        return self.__last_fixing_date

    @last_fixing_date.setter
    def last_fixing_date(self, value: Union[datetime.date, str]):
        self._property_changed('last_fixing_date')
        self.__last_fixing_date = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def fixing_source(self) -> str:
        """The data source to be used for observations of FX spot on each fixing"""
        return self.__fixing_source

    @fixing_source.setter
    def fixing_source(self, value: str):
        self._property_changed('fixing_source')
        self.__fixing_source = value        

    @property
    def fixing_frequency(self) -> str:
        """Fixing frequency (ex. Daily / Business Days)"""
        return self.__fixing_frequency

    @fixing_frequency.setter
    def fixing_frequency(self, value: str):
        self._property_changed('fixing_frequency')
        self.__fixing_frequency = value        

    @property
    def annualization_factor(self) -> float:
        """Annualization factor is the number of days used per year to compute volatility"""
        return self.__annualization_factor

    @annualization_factor.setter
    def annualization_factor(self, value: float):
        self._property_changed('annualization_factor')
        self.__annualization_factor = value        

    @property
    def calculate_mean_return(self) -> float:
        """Indicates whether the mean return is calculated (true) or taken as zero (false)
           in the realized volatility computation"""
        return self.__calculate_mean_return

    @calculate_mean_return.setter
    def calculate_mean_return(self, value: float):
        self._property_changed('calculate_mean_return')
        self.__calculate_mean_return = value        


class Forward(Instrument):
        
    """Forward cash payment"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        notional_amount: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.expiration_date = expiration_date
        self.notional_amount = notional_amount
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Cash"""
        return AssetClass.Cash        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        


class IRBasisSwap(Instrument):
        
    """A single currency exchange of cashflows from different interest rate indices"""

    @camel_case_translate
    def __init__(
        self,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        payer_spread: Union[float, str] = None,
        payer_rate_option: str = None,
        payer_designated_maturity: str = None,
        payer_frequency: str = None,
        payer_day_count_fraction: Union[DayCountFraction, str] = None,
        payer_business_day_convention: Union[BusinessDayConvention, str] = None,
        receiver_spread: Union[float, str] = None,
        receiver_rate_option: str = None,
        receiver_designated_maturity: str = None,
        receiver_frequency: str = None,
        receiver_day_count_fraction: Union[DayCountFraction, str] = None,
        receiver_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        clearing_house: Union[SwapClearingHouse, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.principal_exchange = principal_exchange
        self.payer_spread = payer_spread
        self.payer_rate_option = payer_rate_option
        self.payer_designated_maturity = payer_designated_maturity
        self.payer_frequency = payer_frequency
        self.payer_day_count_fraction = payer_day_count_fraction
        self.payer_business_day_convention = payer_business_day_convention
        self.receiver_spread = receiver_spread
        self.receiver_rate_option = receiver_rate_option
        self.receiver_designated_maturity = receiver_designated_maturity
        self.receiver_frequency = receiver_frequency
        self.receiver_day_count_fraction = receiver_day_count_fraction
        self.receiver_business_day_convention = receiver_business_day_convention
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.clearing_house = clearing_house
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """BasisSwap"""
        return AssetType.BasisSwap        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """The date on which the swap becomes effective"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def payer_spread(self) -> Union[float, str]:
        """Spread over the payer rate"""
        return self.__payer_spread

    @payer_spread.setter
    def payer_spread(self, value: Union[float, str]):
        self._property_changed('payer_spread')
        self.__payer_spread = value        

    @property
    def payer_rate_option(self) -> str:
        """The underlying benchmark for the payer, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__payer_rate_option

    @payer_rate_option.setter
    def payer_rate_option(self, value: str):
        self._property_changed('payer_rate_option')
        self.__payer_rate_option = value        

    @property
    def payer_designated_maturity(self) -> str:
        """Tenor of the payerRateOption, e.g. 3m, 6m"""
        return self.__payer_designated_maturity

    @payer_designated_maturity.setter
    def payer_designated_maturity(self, value: str):
        self._property_changed('payer_designated_maturity')
        self.__payer_designated_maturity = value        

    @property
    def payer_frequency(self) -> str:
        """The frequency of payer payments, e.g. 6m"""
        return self.__payer_frequency

    @payer_frequency.setter
    def payer_frequency(self, value: str):
        self._property_changed('payer_frequency')
        self.__payer_frequency = value        

    @property
    def payer_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the payer"""
        return self.__payer_day_count_fraction

    @payer_day_count_fraction.setter
    def payer_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('payer_day_count_fraction')
        self.__payer_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def payer_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the payer"""
        return self.__payer_business_day_convention

    @payer_business_day_convention.setter
    def payer_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('payer_business_day_convention')
        self.__payer_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def receiver_spread(self) -> Union[float, str]:
        """Spread over the receiver rate"""
        return self.__receiver_spread

    @receiver_spread.setter
    def receiver_spread(self, value: Union[float, str]):
        self._property_changed('receiver_spread')
        self.__receiver_spread = value        

    @property
    def receiver_rate_option(self) -> str:
        """The underlying benchmark for the receiver, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__receiver_rate_option

    @receiver_rate_option.setter
    def receiver_rate_option(self, value: str):
        self._property_changed('receiver_rate_option')
        self.__receiver_rate_option = value        

    @property
    def receiver_designated_maturity(self) -> str:
        """Tenor of the receiverRateOption, e.g. 3m, 6m"""
        return self.__receiver_designated_maturity

    @receiver_designated_maturity.setter
    def receiver_designated_maturity(self, value: str):
        self._property_changed('receiver_designated_maturity')
        self.__receiver_designated_maturity = value        

    @property
    def receiver_frequency(self) -> str:
        """The frequency of receiver payments, e.g. 6m"""
        return self.__receiver_frequency

    @receiver_frequency.setter
    def receiver_frequency(self, value: str):
        self._property_changed('receiver_frequency')
        self.__receiver_frequency = value        

    @property
    def receiver_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the receiver"""
        return self.__receiver_day_count_fraction

    @receiver_day_count_fraction.setter
    def receiver_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('receiver_day_count_fraction')
        self.__receiver_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def receiver_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the receiver"""
        return self.__receiver_business_day_convention

    @receiver_business_day_convention.setter
    def receiver_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('receiver_business_day_convention')
        self.__receiver_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self._property_changed('clearing_house')
        self.__clearing_house = get_enum_value(SwapClearingHouse, value)        


class IRBondFuture(Instrument):
        
    """A future on a (treasury) bond"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        notional_amount: Union[float, str] = None,
        underlier: Union[float, str] = None,
        currency: Union[Currency, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        exchange: str = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.notional_amount = notional_amount
        self.underlier = underlier
        self.currency = currency
        self.expiration_date = expiration_date
        self.exchange = exchange
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """BondFuture"""
        return AssetType.BondFuture        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        


class IRBondOption(Instrument):
        
    """Object representation of a bond option"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str] = None,
        notional_amount: Union[float, str] = None,
        expiration_date: Union[Union[datetime.date, str], str] = None,
        option_type: Union[OptionType, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        strike: Union[float, str] = None,
        strike_type: Union[BondStrikeType, str] = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        settlement: Union[SettlementType, str] = None,
        underlier_type: Union[UnderlierType, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.notional_amount = notional_amount
        self.expiration_date = expiration_date
        self.option_type = option_type
        self.effective_date = effective_date
        self.strike = strike
        self.strike_type = strike_type
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.settlement = settlement
        self.underlier_type = underlier_type
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """BondOption"""
        return AssetType.BondOption        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def expiration_date(self) -> Union[Union[datetime.date, str], str]:
        """Bond option expiration date, 2020-05-01, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """Bond option effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def strike(self) -> Union[float, str]:
        """The strike of the option"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def strike_type(self) -> Union[BondStrikeType, str]:
        """The type of the bond strike - price, yield etc"""
        return self.__strike_type

    @strike_type.setter
    def strike_type(self, value: Union[BondStrikeType, str]):
        self._property_changed('strike_type')
        self.__strike_type = get_enum_value(BondStrikeType, value)        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def settlement(self) -> Union[SettlementType, str]:
        """Settlement Type"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: Union[SettlementType, str]):
        self._property_changed('settlement')
        self.__settlement = get_enum_value(SettlementType, value)        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        


class IRCMSOption(Instrument):
        
    """Object representation of a constant maturity option (cap, floor, straddle)"""

    @camel_case_translate
    def __init__(
        self,
        cap_floor: str = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        strike: Union[float, str] = None,
        index: str = None,
        multiplier: float = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        buy_sell: Union[BuySell, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.cap_floor = cap_floor
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.strike = strike
        self.index = index
        self.multiplier = multiplier
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.buy_sell = buy_sell
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """CMSOption"""
        return AssetType.CMSOption        

    @property
    def cap_floor(self) -> str:
        """Structure type, e.g. Cap, Floor, Straddle, Binary Cap"""
        return self.__cap_floor

    @cap_floor.setter
    def cap_floor(self, value: str):
        self._property_changed('cap_floor')
        self.__cap_floor = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """Swap termination date, e.g. 2030-05-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """CMS option effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def index(self) -> str:
        """The underlying benchmark i.e. 30yUSD"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self._property_changed('index')
        self.__index = value        

    @property
    def multiplier(self) -> float:
        """Multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        


class IRCMSOptionStrip(Instrument):
        
    """Object representation of a constant maturity option strip (cap, floor, straddle)"""

    @camel_case_translate
    def __init__(
        self,
        cap_floor: str = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        strike: Union[float, str] = None,
        index: str = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        reset_delay: str = None,
        multiplier: float = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        buy_sell: Union[BuySell, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.cap_floor = cap_floor
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.strike = strike
        self.index = index
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.reset_delay = reset_delay
        self.multiplier = multiplier
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.buy_sell = buy_sell
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """CMSOptionStrip"""
        return AssetType.CMSOptionStrip        

    @property
    def cap_floor(self) -> str:
        """Structure type, e.g. Cap, Floor, Straddle, Binary Cap"""
        return self.__cap_floor

    @cap_floor.setter
    def cap_floor(self, value: str):
        self._property_changed('cap_floor')
        self.__cap_floor = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """Swap termination date, e.g. 2030-05-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """CMS option effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def index(self) -> str:
        """The underlying benchmark i.e. 30yUSD"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self._property_changed('index')
        self.__index = value        

    @property
    def floating_rate_frequency(self) -> str:
        """Period e.g. 3m, 1y"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def reset_delay(self) -> str:
        """Delay of the reset e.g. 2d"""
        return self.__reset_delay

    @reset_delay.setter
    def reset_delay(self, value: str):
        self._property_changed('reset_delay')
        self.__reset_delay = value        

    @property
    def multiplier(self) -> float:
        """Multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        


class IRCMSSpreadOption(Instrument):
        
    """Object representation of a constant maturity spread option (cap, floor,
       straddle)"""

    @camel_case_translate
    def __init__(
        self,
        cap_floor: str = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        strike: Union[float, str] = None,
        index1_tenor: str = None,
        index2_tenor: str = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        buy_sell: Union[BuySell, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.cap_floor = cap_floor
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.strike = strike
        self.index1_tenor = index1_tenor
        self.index2_tenor = index2_tenor
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.buy_sell = buy_sell
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """CMSSpreadOption"""
        return AssetType.CMSSpreadOption        

    @property
    def cap_floor(self) -> str:
        """Structure type, e.g. Cap, Floor, Straddle"""
        return self.__cap_floor

    @cap_floor.setter
    def cap_floor(self, value: str):
        self._property_changed('cap_floor')
        self.__cap_floor = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """Swap termination date, e.g. 2030-05-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """CMS option effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def index1_tenor(self) -> str:
        """The tenor of the underlying benchmark to be the first element i.e. 30y"""
        return self.__index1_tenor

    @index1_tenor.setter
    def index1_tenor(self, value: str):
        self._property_changed('index1_tenor')
        self.__index1_tenor = value        

    @property
    def index2_tenor(self) -> str:
        """The  tenor of the underlying benchmark to be the second element i.e. 5y"""
        return self.__index2_tenor

    @index2_tenor.setter
    def index2_tenor(self, value: str):
        self._property_changed('index2_tenor')
        self.__index2_tenor = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        


class IRCMSSpreadOptionStrip(Instrument):
        
    """Object representation of a constant maturity spread option strip (cap, floor,
       straddle)"""

    @camel_case_translate
    def __init__(
        self,
        cap_floor: str = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        strike: Union[float, str] = None,
        index1: str = None,
        index2: str = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        reset_delay: str = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        buy_sell: Union[BuySell, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.cap_floor = cap_floor
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.strike = strike
        self.index1 = index1
        self.index2 = index2
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.reset_delay = reset_delay
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.buy_sell = buy_sell
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """CMSSpreadOptionStrip"""
        return AssetType.CMSSpreadOptionStrip        

    @property
    def cap_floor(self) -> str:
        """Structure type, e.g. Cap, Floor, Straddle, Binary Cap"""
        return self.__cap_floor

    @cap_floor.setter
    def cap_floor(self, value: str):
        self._property_changed('cap_floor')
        self.__cap_floor = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """Swap termination date, e.g. 2030-05-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """CMS option effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def index1(self) -> str:
        """The underlying benchmark to be the first element from i.e. 30yUSD"""
        return self.__index1

    @index1.setter
    def index1(self, value: str):
        self._property_changed('index1')
        self.__index1 = value        

    @property
    def index2(self) -> str:
        """The underlying benchmark to be the second element from i.e. 5yUSD"""
        return self.__index2

    @index2.setter
    def index2(self, value: str):
        self._property_changed('index2')
        self.__index2 = value        

    @property
    def floating_rate_frequency(self) -> str:
        """Period e.g. 3m, 1y"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def reset_delay(self) -> str:
        """Delay of the reset e.g. 2d"""
        return self.__reset_delay

    @reset_delay.setter
    def reset_delay(self, value: str):
        self._property_changed('reset_delay')
        self.__reset_delay = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        


class IRCap(Instrument):
        
    """Object representation of an interest rate cap"""

    @camel_case_translate
    def __init__(
        self,
        termination_date: Union[datetime.date, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[datetime.date, str] = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        cap_rate: Union[float, str] = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.floating_rate_option = floating_rate_option
        self.floating_rate_designated_maturity = floating_rate_designated_maturity
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.cap_rate = cap_rate
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Cap"""
        return AssetType.Cap        

    @property
    def termination_date(self) -> Union[datetime.date, str]:
        """The termination of the cap, e.g. 2025-04-01, 2y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[datetime.date, str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[datetime.date, str]:
        """The date on which the cap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[datetime.date, str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def cap_rate(self) -> Union[float, str]:
        """The rate of this cap, as value, percent or at-the-money e.g. 62.5, 95%, ATM-25,
           ATMF"""
        return self.__cap_rate

    @cap_rate.setter
    def cap_rate(self, value: Union[float, str]):
        self._property_changed('cap_rate')
        self.__cap_rate = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        


class IRFixedLeg(Instrument):
        
    """A strip of vanilla fixed rate cashflows"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        fixed_first_stub: Union[Union[datetime.date, str], str] = None,
        fixed_rate_frequency: str = None,
        fixed_holidays: str = None,
        fixed_last_stub: Union[Union[datetime.date, str], str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate: Union[float, str] = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        roll_convention: str = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.fixed_rate_day_count_fraction = fixed_rate_day_count_fraction
        self.fixed_first_stub = fixed_first_stub
        self.fixed_rate_frequency = fixed_rate_frequency
        self.fixed_holidays = fixed_holidays
        self.fixed_last_stub = fixed_last_stub
        self.fixed_rate_business_day_convention = fixed_rate_business_day_convention
        self.fixed_rate = fixed_rate
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.principal_exchange = principal_exchange
        self.roll_convention = roll_convention
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """FixedLeg"""
        return AssetType.FixedLeg        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the fixed rate"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def fixed_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for fixed leg"""
        return self.__fixed_first_stub

    @fixed_first_stub.setter
    def fixed_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('fixed_first_stub')
        self.__fixed_first_stub = value        

    @property
    def fixed_rate_frequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: str):
        self._property_changed('fixed_rate_frequency')
        self.__fixed_rate_frequency = value        

    @property
    def fixed_holidays(self) -> str:
        """The accrual calendar for fixed leg"""
        return self.__fixed_holidays

    @fixed_holidays.setter
    def fixed_holidays(self, value: str):
        self._property_changed('fixed_holidays')
        self.__fixed_holidays = value        

    @property
    def fixed_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for fixed leg"""
        return self.__fixed_last_stub

    @fixed_last_stub.setter
    def fixed_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('fixed_last_stub')
        self.__fixed_last_stub = value        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('fixed_rate_business_day_convention')
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self._property_changed('fixed_rate')
        self.__fixed_rate = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the leg, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """When the exchange of principal is done"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def roll_convention(self) -> str:
        """The roll convention"""
        return self.__roll_convention

    @roll_convention.setter
    def roll_convention(self, value: str):
        self._property_changed('roll_convention')
        self.__roll_convention = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the instrument becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        


class IRFloatLeg(Instrument):
        
    """A strip of vanilla floating rate cashflows"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        floating_rate_for_the_initial_calculation_period: float = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_first_stub: Union[Union[datetime.date, str], str] = None,
        floating_rate_frequency: str = None,
        floating_holidays: str = None,
        floating_last_stub: Union[Union[datetime.date, str], str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        roll_convention: str = None,
        notional_amount: Union[float, str] = None,
        floating_rate_spread: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.floating_rate_for_the_initial_calculation_period = floating_rate_for_the_initial_calculation_period
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_first_stub = floating_first_stub
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_holidays = floating_holidays
        self.floating_last_stub = floating_last_stub
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.floating_rate_option = floating_rate_option
        self.floating_rate_designated_maturity = floating_rate_designated_maturity
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.principal_exchange = principal_exchange
        self.roll_convention = roll_convention
        self.notional_amount = notional_amount
        self.floating_rate_spread = floating_rate_spread
        self.effective_date = effective_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """FloatLeg"""
        return AssetType.FloatLeg        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def floating_rate_for_the_initial_calculation_period(self) -> float:
        """First fixing"""
        return self.__floating_rate_for_the_initial_calculation_period

    @floating_rate_for_the_initial_calculation_period.setter
    def floating_rate_for_the_initial_calculation_period(self, value: float):
        self._property_changed('floating_rate_for_the_initial_calculation_period')
        self.__floating_rate_for_the_initial_calculation_period = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for floating leg"""
        return self.__floating_first_stub

    @floating_first_stub.setter
    def floating_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('floating_first_stub')
        self.__floating_first_stub = value        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 6m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_holidays(self) -> str:
        """The accrual calendar for floating leg"""
        return self.__floating_holidays

    @floating_holidays.setter
    def floating_holidays(self, value: str):
        self._property_changed('floating_holidays')
        self.__floating_holidays = value        

    @property
    def floating_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for floating leg"""
        return self.__floating_last_stub

    @floating_last_stub.setter
    def floating_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('floating_last_stub')
        self.__floating_last_stub = value        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the leg, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """When the exchange of principals is done"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def roll_convention(self) -> str:
        """The roll convention"""
        return self.__roll_convention

    @roll_convention.setter
    def roll_convention(self, value: str):
        self._property_changed('roll_convention')
        self.__roll_convention = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def floating_rate_spread(self) -> Union[float, str]:
        """The spread over the floating rate"""
        return self.__floating_rate_spread

    @floating_rate_spread.setter
    def floating_rate_spread(self, value: Union[float, str]):
        self._property_changed('floating_rate_spread')
        self.__floating_rate_spread = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the instrument becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        


class IRFloor(Instrument):
        
    """Object representation of an interest rate floor"""

    @camel_case_translate
    def __init__(
        self,
        termination_date: Union[datetime.date, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[datetime.date, str] = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        floor_rate: Union[float, str] = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.floating_rate_option = floating_rate_option
        self.floating_rate_designated_maturity = floating_rate_designated_maturity
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.floor_rate = floor_rate
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Floor"""
        return AssetType.Floor        

    @property
    def termination_date(self) -> Union[datetime.date, str]:
        """The termination of the floor, e.g. 2025-04-01, 2y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[datetime.date, str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[datetime.date, str]:
        """The date on which the floor becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[datetime.date, str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def floor_rate(self) -> Union[float, str]:
        """The rate of this floor, as value, percent or at-the-money e.g. 62.5, 95%,
           ATM-25, ATMF"""
        return self.__floor_rate

    @floor_rate.setter
    def floor_rate(self, value: Union[float, str]):
        self._property_changed('floor_rate')
        self.__floor_rate = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        


class IRSwap(Instrument):
        
    """A vanilla interest rate swap of fixed vs floating cashflows"""

    @camel_case_translate
    def __init__(
        self,
        pay_or_receive: Union[PayReceive, str] = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        floating_rate_for_the_initial_calculation_period: float = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_spread: Union[float, str] = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate: Union[float, str] = None,
        fixed_rate_frequency: str = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        clearing_house: Union[SwapClearingHouse, str] = None,
        fixed_first_stub: Union[Union[datetime.date, str], str] = None,
        floating_first_stub: Union[Union[datetime.date, str], str] = None,
        fixed_last_stub: Union[Union[datetime.date, str], str] = None,
        floating_last_stub: Union[Union[datetime.date, str], str] = None,
        fixed_holidays: str = None,
        floating_holidays: str = None,
        roll_convention: str = None,
        name: str = None
    ):        
        super().__init__()
        self.pay_or_receive = pay_or_receive
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.principal_exchange = principal_exchange
        self.floating_rate_for_the_initial_calculation_period = floating_rate_for_the_initial_calculation_period
        self.floating_rate_option = floating_rate_option
        self.floating_rate_designated_maturity = floating_rate_designated_maturity
        self.floating_rate_spread = floating_rate_spread
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.fixed_rate = fixed_rate
        self.fixed_rate_frequency = fixed_rate_frequency
        self.fixed_rate_day_count_fraction = fixed_rate_day_count_fraction
        self.fixed_rate_business_day_convention = fixed_rate_business_day_convention
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.clearing_house = clearing_house
        self.fixed_first_stub = fixed_first_stub
        self.floating_first_stub = floating_first_stub
        self.fixed_last_stub = fixed_last_stub
        self.floating_last_stub = floating_last_stub
        self.fixed_holidays = fixed_holidays
        self.floating_holidays = floating_holidays
        self.roll_convention = roll_convention
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Swap"""
        return AssetType.Swap        

    @property
    def pay_or_receive(self) -> Union[PayReceive, str]:
        """Pay or receive fixed"""
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: Union[PayReceive, str]):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = get_enum_value(PayReceive, value)        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """The date on which the swap becomes effective"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def floating_rate_for_the_initial_calculation_period(self) -> float:
        """First fixing"""
        return self.__floating_rate_for_the_initial_calculation_period

    @floating_rate_for_the_initial_calculation_period.setter
    def floating_rate_for_the_initial_calculation_period(self, value: float):
        self._property_changed('floating_rate_for_the_initial_calculation_period')
        self.__floating_rate_for_the_initial_calculation_period = value        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def floating_rate_spread(self) -> Union[float, str]:
        """The spread over the floating rate"""
        return self.__floating_rate_spread

    @floating_rate_spread.setter
    def floating_rate_spread(self, value: Union[float, str]):
        self._property_changed('floating_rate_spread')
        self.__floating_rate_spread = value        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self._property_changed('fixed_rate')
        self.__fixed_rate = value        

    @property
    def fixed_rate_frequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: str):
        self._property_changed('fixed_rate_frequency')
        self.__fixed_rate_frequency = value        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('fixed_rate_business_day_convention')
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self._property_changed('clearing_house')
        self.__clearing_house = get_enum_value(SwapClearingHouse, value)        

    @property
    def fixed_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for fixed leg"""
        return self.__fixed_first_stub

    @fixed_first_stub.setter
    def fixed_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('fixed_first_stub')
        self.__fixed_first_stub = value        

    @property
    def floating_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for floating leg"""
        return self.__floating_first_stub

    @floating_first_stub.setter
    def floating_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('floating_first_stub')
        self.__floating_first_stub = value        

    @property
    def fixed_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for fixed leg"""
        return self.__fixed_last_stub

    @fixed_last_stub.setter
    def fixed_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('fixed_last_stub')
        self.__fixed_last_stub = value        

    @property
    def floating_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for floating leg"""
        return self.__floating_last_stub

    @floating_last_stub.setter
    def floating_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('floating_last_stub')
        self.__floating_last_stub = value        

    @property
    def fixed_holidays(self) -> str:
        """The accrual calendar for fixed leg"""
        return self.__fixed_holidays

    @fixed_holidays.setter
    def fixed_holidays(self, value: str):
        self._property_changed('fixed_holidays')
        self.__fixed_holidays = value        

    @property
    def floating_holidays(self) -> str:
        """The accrual calendar for floating leg"""
        return self.__floating_holidays

    @floating_holidays.setter
    def floating_holidays(self, value: str):
        self._property_changed('floating_holidays')
        self.__floating_holidays = value        

    @property
    def roll_convention(self) -> str:
        """The roll convention"""
        return self.__roll_convention

    @roll_convention.setter
    def roll_convention(self, value: str):
        self._property_changed('roll_convention')
        self.__roll_convention = value        


class IRSwaption(Instrument):
        
    """Object representation of a swaption"""

    @camel_case_translate
    def __init__(
        self,
        pay_or_receive: str = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_currency: Union[Currency, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        notional_amount: Union[float, str] = None,
        expiration_date: Union[Union[datetime.date, str], str] = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_spread: float = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate_frequency: str = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        strike: Union[float, str] = None,
        premium: Union[float, str] = None,
        premium_payment_date: Union[datetime.date, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        clearing_house: Union[SwapClearingHouse, str] = None,
        settlement: Union[SwapSettlement, str] = None,
        buy_sell: Union[BuySell, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.pay_or_receive = pay_or_receive
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.effective_date = effective_date
        self.notional_amount = notional_amount
        self.expiration_date = expiration_date
        self.floating_rate_option = floating_rate_option
        self.floating_rate_designated_maturity = floating_rate_designated_maturity
        self.floating_rate_spread = floating_rate_spread
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.fixed_rate_frequency = fixed_rate_frequency
        self.fixed_rate_day_count_fraction = fixed_rate_day_count_fraction
        self.fixed_rate_business_day_convention = fixed_rate_business_day_convention
        self.strike = strike
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.clearing_house = clearing_house
        self.settlement = settlement
        self.buy_sell = buy_sell
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """Swaption"""
        return AssetType.Swaption        

    @property
    def pay_or_receive(self) -> str:
        """Pay or receive fixed"""
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: str):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = value        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """Swaption termination date, e.g. 2030-05-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """Swaption effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def expiration_date(self) -> Union[Union[datetime.date, str], str]:
        """Swaption expiration date, 2020-05-01, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def floating_rate_spread(self) -> float:
        """The spread over the floating rate"""
        return self.__floating_rate_spread

    @floating_rate_spread.setter
    def floating_rate_spread(self, value: float):
        self._property_changed('floating_rate_spread')
        self.__floating_rate_spread = value        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fixed_rate_frequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: str):
        self._property_changed('fixed_rate_frequency')
        self.__fixed_rate_frequency = value        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('fixed_rate_business_day_convention')
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def premium(self) -> Union[float, str]:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self._property_changed('clearing_house')
        self.__clearing_house = get_enum_value(SwapClearingHouse, value)        

    @property
    def settlement(self) -> Union[SwapSettlement, str]:
        """Swap Settlement Type"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: Union[SwapSettlement, str]):
        self._property_changed('settlement')
        self.__settlement = get_enum_value(SwapSettlement, value)        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        


class IRXccySwap(Instrument):
        
    """An exchange of cashflows from different interest rate indices"""

    @camel_case_translate
    def __init__(
        self,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_amount: float = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        payer_currency: Union[Currency, str] = None,
        payer_spread: Union[float, str] = None,
        payer_rate_option: str = None,
        payer_designated_maturity: str = None,
        payer_frequency: str = None,
        payer_day_count_fraction: Union[DayCountFraction, str] = None,
        payer_business_day_convention: Union[BusinessDayConvention, str] = None,
        receiver_currency: Union[Currency, str] = None,
        receiver_spread: Union[float, str] = None,
        receiver_rate_option: str = None,
        receiver_designated_maturity: str = None,
        receiver_frequency: str = None,
        receiver_day_count_fraction: Union[DayCountFraction, str] = None,
        receiver_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        initial_fx_rate: float = None,
        payer_first_stub: Union[Union[datetime.date, str], str] = None,
        receiver_first_stub: Union[Union[datetime.date, str], str] = None,
        payer_last_stub: Union[Union[datetime.date, str], str] = None,
        receiver_last_stub: Union[Union[datetime.date, str], str] = None,
        payer_holidays: str = None,
        receiver_holidays: str = None,
        notional_reset_side: Union[PayReceive, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.termination_date = termination_date
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.principal_exchange = principal_exchange
        self.payer_currency = payer_currency
        self.payer_spread = payer_spread
        self.payer_rate_option = payer_rate_option
        self.payer_designated_maturity = payer_designated_maturity
        self.payer_frequency = payer_frequency
        self.payer_day_count_fraction = payer_day_count_fraction
        self.payer_business_day_convention = payer_business_day_convention
        self.receiver_currency = receiver_currency
        self.receiver_spread = receiver_spread
        self.receiver_rate_option = receiver_rate_option
        self.receiver_designated_maturity = receiver_designated_maturity
        self.receiver_frequency = receiver_frequency
        self.receiver_day_count_fraction = receiver_day_count_fraction
        self.receiver_business_day_convention = receiver_business_day_convention
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.initial_fx_rate = initial_fx_rate
        self.payer_first_stub = payer_first_stub
        self.receiver_first_stub = receiver_first_stub
        self.payer_last_stub = payer_last_stub
        self.receiver_last_stub = receiver_last_stub
        self.payer_holidays = payer_holidays
        self.receiver_holidays = receiver_holidays
        self.notional_reset_side = notional_reset_side
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """XccySwapMTM"""
        return AssetType.XccySwapMTM        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """The date on which the swap becomes effective"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def payer_currency(self) -> Union[Currency, str]:
        """Payer currency"""
        return self.__payer_currency

    @payer_currency.setter
    def payer_currency(self, value: Union[Currency, str]):
        self._property_changed('payer_currency')
        self.__payer_currency = get_enum_value(Currency, value)        

    @property
    def payer_spread(self) -> Union[float, str]:
        """Spread over the payer rate"""
        return self.__payer_spread

    @payer_spread.setter
    def payer_spread(self, value: Union[float, str]):
        self._property_changed('payer_spread')
        self.__payer_spread = value        

    @property
    def payer_rate_option(self) -> str:
        """The underlying benchmark for the payer, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__payer_rate_option

    @payer_rate_option.setter
    def payer_rate_option(self, value: str):
        self._property_changed('payer_rate_option')
        self.__payer_rate_option = value        

    @property
    def payer_designated_maturity(self) -> str:
        """Tenor of the payerRateOption, e.g. 3m, 6m"""
        return self.__payer_designated_maturity

    @payer_designated_maturity.setter
    def payer_designated_maturity(self, value: str):
        self._property_changed('payer_designated_maturity')
        self.__payer_designated_maturity = value        

    @property
    def payer_frequency(self) -> str:
        """The frequency of payer payments, e.g. 6m"""
        return self.__payer_frequency

    @payer_frequency.setter
    def payer_frequency(self, value: str):
        self._property_changed('payer_frequency')
        self.__payer_frequency = value        

    @property
    def payer_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the payer"""
        return self.__payer_day_count_fraction

    @payer_day_count_fraction.setter
    def payer_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('payer_day_count_fraction')
        self.__payer_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def payer_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the payer"""
        return self.__payer_business_day_convention

    @payer_business_day_convention.setter
    def payer_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('payer_business_day_convention')
        self.__payer_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def receiver_currency(self) -> Union[Currency, str]:
        """Receiver currency"""
        return self.__receiver_currency

    @receiver_currency.setter
    def receiver_currency(self, value: Union[Currency, str]):
        self._property_changed('receiver_currency')
        self.__receiver_currency = get_enum_value(Currency, value)        

    @property
    def receiver_spread(self) -> Union[float, str]:
        """Spread over the receiver rate"""
        return self.__receiver_spread

    @receiver_spread.setter
    def receiver_spread(self, value: Union[float, str]):
        self._property_changed('receiver_spread')
        self.__receiver_spread = value        

    @property
    def receiver_rate_option(self) -> str:
        """The underlying benchmark for the receiver, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__receiver_rate_option

    @receiver_rate_option.setter
    def receiver_rate_option(self, value: str):
        self._property_changed('receiver_rate_option')
        self.__receiver_rate_option = value        

    @property
    def receiver_designated_maturity(self) -> str:
        """Tenor of the receiverRateOption, e.g. 3m, 6m"""
        return self.__receiver_designated_maturity

    @receiver_designated_maturity.setter
    def receiver_designated_maturity(self, value: str):
        self._property_changed('receiver_designated_maturity')
        self.__receiver_designated_maturity = value        

    @property
    def receiver_frequency(self) -> str:
        """The frequency of receiver payments, e.g. 6m"""
        return self.__receiver_frequency

    @receiver_frequency.setter
    def receiver_frequency(self, value: str):
        self._property_changed('receiver_frequency')
        self.__receiver_frequency = value        

    @property
    def receiver_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the receiver"""
        return self.__receiver_day_count_fraction

    @receiver_day_count_fraction.setter
    def receiver_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('receiver_day_count_fraction')
        self.__receiver_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def receiver_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the receiver"""
        return self.__receiver_business_day_convention

    @receiver_business_day_convention.setter
    def receiver_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('receiver_business_day_convention')
        self.__receiver_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def initial_fx_rate(self) -> float:
        """Payment date of the fee"""
        return self.__initial_fx_rate

    @initial_fx_rate.setter
    def initial_fx_rate(self, value: float):
        self._property_changed('initial_fx_rate')
        self.__initial_fx_rate = value        

    @property
    def payer_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for payer leg"""
        return self.__payer_first_stub

    @payer_first_stub.setter
    def payer_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('payer_first_stub')
        self.__payer_first_stub = value        

    @property
    def receiver_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for receiver leg"""
        return self.__receiver_first_stub

    @receiver_first_stub.setter
    def receiver_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('receiver_first_stub')
        self.__receiver_first_stub = value        

    @property
    def payer_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for payer leg"""
        return self.__payer_last_stub

    @payer_last_stub.setter
    def payer_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('payer_last_stub')
        self.__payer_last_stub = value        

    @property
    def receiver_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for receiver leg"""
        return self.__receiver_last_stub

    @receiver_last_stub.setter
    def receiver_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('receiver_last_stub')
        self.__receiver_last_stub = value        

    @property
    def payer_holidays(self) -> str:
        """The accrual calendar for payer leg"""
        return self.__payer_holidays

    @payer_holidays.setter
    def payer_holidays(self, value: str):
        self._property_changed('payer_holidays')
        self.__payer_holidays = value        

    @property
    def receiver_holidays(self) -> str:
        """The accrual calendar for receiver leg"""
        return self.__receiver_holidays

    @receiver_holidays.setter
    def receiver_holidays(self, value: str):
        self._property_changed('receiver_holidays')
        self.__receiver_holidays = value        

    @property
    def notional_reset_side(self) -> Union[PayReceive, str]:
        """Pay or Rec leg resetting"""
        return self.__notional_reset_side

    @notional_reset_side.setter
    def notional_reset_side(self, value: Union[PayReceive, str]):
        self._property_changed('notional_reset_side')
        self.__notional_reset_side = get_enum_value(PayReceive, value)        


class IRXccySwapFixFix(Instrument):
        
    """An exchange of fixed cashflows in different currencies"""

    @camel_case_translate
    def __init__(
        self,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_amount: float = None,
        receiver_notional_amount: float = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        payer_currency: Union[Currency, str] = None,
        payer_rate: Union[float, str] = None,
        payer_frequency: str = None,
        payer_day_count_fraction: Union[DayCountFraction, str] = None,
        payer_business_day_convention: Union[BusinessDayConvention, str] = None,
        receiver_currency: Union[Currency, str] = None,
        receiver_rate: Union[float, str] = None,
        receiver_frequency: str = None,
        receiver_day_count_fraction: Union[DayCountFraction, str] = None,
        receiver_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.termination_date = termination_date
        self.notional_amount = notional_amount
        self.receiver_notional_amount = receiver_notional_amount
        self.effective_date = effective_date
        self.principal_exchange = principal_exchange
        self.payer_currency = payer_currency
        self.payer_rate = payer_rate
        self.payer_frequency = payer_frequency
        self.payer_day_count_fraction = payer_day_count_fraction
        self.payer_business_day_convention = payer_business_day_convention
        self.receiver_currency = receiver_currency
        self.receiver_rate = receiver_rate
        self.receiver_frequency = receiver_frequency
        self.receiver_day_count_fraction = receiver_day_count_fraction
        self.receiver_business_day_convention = receiver_business_day_convention
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """XccySwapFixFix"""
        return AssetType.XccySwapFixFix        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def receiver_notional_amount(self) -> float:
        """Receiver notional amount"""
        return self.__receiver_notional_amount

    @receiver_notional_amount.setter
    def receiver_notional_amount(self, value: float):
        self._property_changed('receiver_notional_amount')
        self.__receiver_notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """The date on which the swap becomes effective"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def payer_currency(self) -> Union[Currency, str]:
        """Payer currency"""
        return self.__payer_currency

    @payer_currency.setter
    def payer_currency(self, value: Union[Currency, str]):
        self._property_changed('payer_currency')
        self.__payer_currency = get_enum_value(Currency, value)        

    @property
    def payer_rate(self) -> Union[float, str]:
        """Payer rate"""
        return self.__payer_rate

    @payer_rate.setter
    def payer_rate(self, value: Union[float, str]):
        self._property_changed('payer_rate')
        self.__payer_rate = value        

    @property
    def payer_frequency(self) -> str:
        """The frequency of payer payments, e.g. 6m"""
        return self.__payer_frequency

    @payer_frequency.setter
    def payer_frequency(self, value: str):
        self._property_changed('payer_frequency')
        self.__payer_frequency = value        

    @property
    def payer_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the payer"""
        return self.__payer_day_count_fraction

    @payer_day_count_fraction.setter
    def payer_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('payer_day_count_fraction')
        self.__payer_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def payer_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the payer"""
        return self.__payer_business_day_convention

    @payer_business_day_convention.setter
    def payer_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('payer_business_day_convention')
        self.__payer_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def receiver_currency(self) -> Union[Currency, str]:
        """Receiver currency"""
        return self.__receiver_currency

    @receiver_currency.setter
    def receiver_currency(self, value: Union[Currency, str]):
        self._property_changed('receiver_currency')
        self.__receiver_currency = get_enum_value(Currency, value)        

    @property
    def receiver_rate(self) -> Union[float, str]:
        """Receiver rate"""
        return self.__receiver_rate

    @receiver_rate.setter
    def receiver_rate(self, value: Union[float, str]):
        self._property_changed('receiver_rate')
        self.__receiver_rate = value        

    @property
    def receiver_frequency(self) -> str:
        """The frequency of receiver payments, e.g. 6m"""
        return self.__receiver_frequency

    @receiver_frequency.setter
    def receiver_frequency(self, value: str):
        self._property_changed('receiver_frequency')
        self.__receiver_frequency = value        

    @property
    def receiver_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the receiver"""
        return self.__receiver_day_count_fraction

    @receiver_day_count_fraction.setter
    def receiver_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('receiver_day_count_fraction')
        self.__receiver_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def receiver_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the receiver"""
        return self.__receiver_business_day_convention

    @receiver_business_day_convention.setter
    def receiver_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('receiver_business_day_convention')
        self.__receiver_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        


class IRXccySwapFixFlt(Instrument):
        
    """An exchange of fixed vs floating cashflows in different currencies"""

    @camel_case_translate
    def __init__(
        self,
        pay_or_receive: Union[PayReceive, str] = None,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        floating_rate_currency: Union[Currency, str] = None,
        floating_rate_for_the_initial_calculation_period: float = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_spread: Union[float, str] = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate_currency: Union[Currency, str] = None,
        fixed_rate: Union[float, str] = None,
        fixed_rate_frequency: str = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        fixed_first_stub: Union[Union[datetime.date, str], str] = None,
        floating_first_stub: Union[Union[datetime.date, str], str] = None,
        fixed_last_stub: Union[Union[datetime.date, str], str] = None,
        floating_last_stub: Union[Union[datetime.date, str], str] = None,
        fixed_holidays: str = None,
        floating_holidays: str = None,
        name: str = None
    ):        
        super().__init__()
        self.pay_or_receive = pay_or_receive
        self.termination_date = termination_date
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.principal_exchange = principal_exchange
        self.floating_rate_currency = floating_rate_currency
        self.floating_rate_for_the_initial_calculation_period = floating_rate_for_the_initial_calculation_period
        self.floating_rate_option = floating_rate_option
        self.floating_rate_designated_maturity = floating_rate_designated_maturity
        self.floating_rate_spread = floating_rate_spread
        self.floating_rate_frequency = floating_rate_frequency
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.fixed_rate_currency = fixed_rate_currency
        self.fixed_rate = fixed_rate
        self.fixed_rate_frequency = fixed_rate_frequency
        self.fixed_rate_day_count_fraction = fixed_rate_day_count_fraction
        self.fixed_rate_business_day_convention = fixed_rate_business_day_convention
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.fixed_first_stub = fixed_first_stub
        self.floating_first_stub = floating_first_stub
        self.fixed_last_stub = fixed_last_stub
        self.floating_last_stub = floating_last_stub
        self.fixed_holidays = fixed_holidays
        self.floating_holidays = floating_holidays
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """XccySwapFixFlt"""
        return AssetType.XccySwapFixFlt        

    @property
    def pay_or_receive(self) -> Union[PayReceive, str]:
        """Pay or receive fixed"""
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: Union[PayReceive, str]):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = get_enum_value(PayReceive, value)        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """The date on which the swap becomes effective"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def floating_rate_currency(self) -> Union[Currency, str]:
        """Floating rate currency"""
        return self.__floating_rate_currency

    @floating_rate_currency.setter
    def floating_rate_currency(self, value: Union[Currency, str]):
        self._property_changed('floating_rate_currency')
        self.__floating_rate_currency = get_enum_value(Currency, value)        

    @property
    def floating_rate_for_the_initial_calculation_period(self) -> float:
        """First fixing"""
        return self.__floating_rate_for_the_initial_calculation_period

    @floating_rate_for_the_initial_calculation_period.setter
    def floating_rate_for_the_initial_calculation_period(self, value: float):
        self._property_changed('floating_rate_for_the_initial_calculation_period')
        self.__floating_rate_for_the_initial_calculation_period = value        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def floating_rate_spread(self) -> Union[float, str]:
        """The spread over the floating rate"""
        return self.__floating_rate_spread

    @floating_rate_spread.setter
    def floating_rate_spread(self, value: Union[float, str]):
        self._property_changed('floating_rate_spread')
        self.__floating_rate_spread = value        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self._property_changed('floating_rate_frequency')
        self.__floating_rate_frequency = value        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fixed_rate_currency(self) -> Union[Currency, str]:
        """Fixed rate currency"""
        return self.__fixed_rate_currency

    @fixed_rate_currency.setter
    def fixed_rate_currency(self, value: Union[Currency, str]):
        self._property_changed('fixed_rate_currency')
        self.__fixed_rate_currency = get_enum_value(Currency, value)        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self._property_changed('fixed_rate')
        self.__fixed_rate = value        

    @property
    def fixed_rate_frequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: str):
        self._property_changed('fixed_rate_frequency')
        self.__fixed_rate_frequency = value        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('fixed_rate_business_day_convention')
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def fixed_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for fixed leg"""
        return self.__fixed_first_stub

    @fixed_first_stub.setter
    def fixed_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('fixed_first_stub')
        self.__fixed_first_stub = value        

    @property
    def floating_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for floating leg"""
        return self.__floating_first_stub

    @floating_first_stub.setter
    def floating_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('floating_first_stub')
        self.__floating_first_stub = value        

    @property
    def fixed_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for fixed leg"""
        return self.__fixed_last_stub

    @fixed_last_stub.setter
    def fixed_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('fixed_last_stub')
        self.__fixed_last_stub = value        

    @property
    def floating_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for floating leg"""
        return self.__floating_last_stub

    @floating_last_stub.setter
    def floating_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('floating_last_stub')
        self.__floating_last_stub = value        

    @property
    def fixed_holidays(self) -> str:
        """The accrual calendar for fixed leg"""
        return self.__fixed_holidays

    @fixed_holidays.setter
    def fixed_holidays(self, value: str):
        self._property_changed('fixed_holidays')
        self.__fixed_holidays = value        

    @property
    def floating_holidays(self) -> str:
        """The accrual calendar for floating leg"""
        return self.__floating_holidays

    @floating_holidays.setter
    def floating_holidays(self, value: str):
        self._property_changed('floating_holidays')
        self.__floating_holidays = value        


class IRXccySwapFltFlt(Instrument):
        
    """An exchange of cashflows from different interest rate indices, non-resetting"""

    @camel_case_translate
    def __init__(
        self,
        termination_date: Union[Union[datetime.date, str], str] = None,
        notional_amount: Union[float, str] = None,
        effective_date: Union[Union[datetime.date, str], str] = None,
        principal_exchange: Union[PrincipalExchange, str] = None,
        payer_currency: Union[Currency, str] = None,
        payer_spread: Union[float, str] = None,
        payer_rate_option: str = None,
        payer_designated_maturity: str = None,
        payer_frequency: str = None,
        payer_day_count_fraction: Union[DayCountFraction, str] = None,
        payer_business_day_convention: Union[BusinessDayConvention, str] = None,
        receiver_currency: Union[Currency, str] = None,
        receiver_spread: Union[float, str] = None,
        receiver_rate_option: str = None,
        receiver_designated_maturity: str = None,
        receiver_frequency: str = None,
        receiver_day_count_fraction: Union[DayCountFraction, str] = None,
        receiver_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        fee_currency: Union[Currency, str] = None,
        fee_payment_date: Union[datetime.date, str] = None,
        payer_first_stub: Union[Union[datetime.date, str], str] = None,
        receiver_first_stub: Union[Union[datetime.date, str], str] = None,
        payer_last_stub: Union[Union[datetime.date, str], str] = None,
        receiver_last_stub: Union[Union[datetime.date, str], str] = None,
        payer_holidays: str = None,
        receiver_holidays: str = None,
        name: str = None
    ):        
        super().__init__()
        self.termination_date = termination_date
        self.notional_amount = notional_amount
        self.effective_date = effective_date
        self.principal_exchange = principal_exchange
        self.payer_currency = payer_currency
        self.payer_spread = payer_spread
        self.payer_rate_option = payer_rate_option
        self.payer_designated_maturity = payer_designated_maturity
        self.payer_frequency = payer_frequency
        self.payer_day_count_fraction = payer_day_count_fraction
        self.payer_business_day_convention = payer_business_day_convention
        self.receiver_currency = receiver_currency
        self.receiver_spread = receiver_spread
        self.receiver_rate_option = receiver_rate_option
        self.receiver_designated_maturity = receiver_designated_maturity
        self.receiver_frequency = receiver_frequency
        self.receiver_day_count_fraction = receiver_day_count_fraction
        self.receiver_business_day_convention = receiver_business_day_convention
        self.fee = fee
        self.fee_currency = fee_currency
        self.fee_payment_date = fee_payment_date
        self.payer_first_stub = payer_first_stub
        self.receiver_first_stub = receiver_first_stub
        self.payer_last_stub = payer_last_stub
        self.receiver_last_stub = receiver_last_stub
        self.payer_holidays = payer_holidays
        self.receiver_holidays = receiver_holidays
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """XccySwap"""
        return AssetType.XccySwap        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def principal_exchange(self) -> Union[PrincipalExchange, str]:
        """Principal exchanges at inception, termination or both"""
        return self.__principal_exchange

    @principal_exchange.setter
    def principal_exchange(self, value: Union[PrincipalExchange, str]):
        self._property_changed('principal_exchange')
        self.__principal_exchange = get_enum_value(PrincipalExchange, value)        

    @property
    def payer_currency(self) -> Union[Currency, str]:
        """Payer currency"""
        return self.__payer_currency

    @payer_currency.setter
    def payer_currency(self, value: Union[Currency, str]):
        self._property_changed('payer_currency')
        self.__payer_currency = get_enum_value(Currency, value)        

    @property
    def payer_spread(self) -> Union[float, str]:
        """Spread over the payer rate"""
        return self.__payer_spread

    @payer_spread.setter
    def payer_spread(self, value: Union[float, str]):
        self._property_changed('payer_spread')
        self.__payer_spread = value        

    @property
    def payer_rate_option(self) -> str:
        """The underlying benchmark for the payer, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__payer_rate_option

    @payer_rate_option.setter
    def payer_rate_option(self, value: str):
        self._property_changed('payer_rate_option')
        self.__payer_rate_option = value        

    @property
    def payer_designated_maturity(self) -> str:
        """Tenor of the payerRateOption, e.g. 3m, 6m"""
        return self.__payer_designated_maturity

    @payer_designated_maturity.setter
    def payer_designated_maturity(self, value: str):
        self._property_changed('payer_designated_maturity')
        self.__payer_designated_maturity = value        

    @property
    def payer_frequency(self) -> str:
        """The frequency of payer payments, e.g. 6m"""
        return self.__payer_frequency

    @payer_frequency.setter
    def payer_frequency(self, value: str):
        self._property_changed('payer_frequency')
        self.__payer_frequency = value        

    @property
    def payer_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the payer"""
        return self.__payer_day_count_fraction

    @payer_day_count_fraction.setter
    def payer_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('payer_day_count_fraction')
        self.__payer_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def payer_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the payer"""
        return self.__payer_business_day_convention

    @payer_business_day_convention.setter
    def payer_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('payer_business_day_convention')
        self.__payer_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def receiver_currency(self) -> Union[Currency, str]:
        """Receiver currency"""
        return self.__receiver_currency

    @receiver_currency.setter
    def receiver_currency(self, value: Union[Currency, str]):
        self._property_changed('receiver_currency')
        self.__receiver_currency = get_enum_value(Currency, value)        

    @property
    def receiver_spread(self) -> Union[float, str]:
        """Spread over the receiver rate"""
        return self.__receiver_spread

    @receiver_spread.setter
    def receiver_spread(self, value: Union[float, str]):
        self._property_changed('receiver_spread')
        self.__receiver_spread = value        

    @property
    def receiver_rate_option(self) -> str:
        """The underlying benchmark for the receiver, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE"""
        return self.__receiver_rate_option

    @receiver_rate_option.setter
    def receiver_rate_option(self, value: str):
        self._property_changed('receiver_rate_option')
        self.__receiver_rate_option = value        

    @property
    def receiver_designated_maturity(self) -> str:
        """Tenor of the receiverRateOption, e.g. 3m, 6m"""
        return self.__receiver_designated_maturity

    @receiver_designated_maturity.setter
    def receiver_designated_maturity(self, value: str):
        self._property_changed('receiver_designated_maturity')
        self.__receiver_designated_maturity = value        

    @property
    def receiver_frequency(self) -> str:
        """The frequency of receiver payments, e.g. 6m"""
        return self.__receiver_frequency

    @receiver_frequency.setter
    def receiver_frequency(self, value: str):
        self._property_changed('receiver_frequency')
        self.__receiver_frequency = value        

    @property
    def receiver_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the receiver"""
        return self.__receiver_day_count_fraction

    @receiver_day_count_fraction.setter
    def receiver_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('receiver_day_count_fraction')
        self.__receiver_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def receiver_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the receiver"""
        return self.__receiver_business_day_convention

    @receiver_business_day_convention.setter
    def receiver_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('receiver_business_day_convention')
        self.__receiver_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def fee_currency(self) -> Union[Currency, str]:
        """Currency of the fee"""
        return self.__fee_currency

    @fee_currency.setter
    def fee_currency(self, value: Union[Currency, str]):
        self._property_changed('fee_currency')
        self.__fee_currency = get_enum_value(Currency, value)        

    @property
    def fee_payment_date(self) -> Union[datetime.date, str]:
        """Payment date of the fee"""
        return self.__fee_payment_date

    @fee_payment_date.setter
    def fee_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('fee_payment_date')
        self.__fee_payment_date = value        

    @property
    def payer_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for payer leg"""
        return self.__payer_first_stub

    @payer_first_stub.setter
    def payer_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('payer_first_stub')
        self.__payer_first_stub = value        

    @property
    def receiver_first_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the first stub for receiver leg"""
        return self.__receiver_first_stub

    @receiver_first_stub.setter
    def receiver_first_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('receiver_first_stub')
        self.__receiver_first_stub = value        

    @property
    def payer_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for payer leg"""
        return self.__payer_last_stub

    @payer_last_stub.setter
    def payer_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('payer_last_stub')
        self.__payer_last_stub = value        

    @property
    def receiver_last_stub(self) -> Union[Union[datetime.date, str], str]:
        """The date of the last stub for receiver leg"""
        return self.__receiver_last_stub

    @receiver_last_stub.setter
    def receiver_last_stub(self, value: Union[Union[datetime.date, str], str]):
        self._property_changed('receiver_last_stub')
        self.__receiver_last_stub = value        

    @property
    def payer_holidays(self) -> str:
        """The accrual calendar for payer leg"""
        return self.__payer_holidays

    @payer_holidays.setter
    def payer_holidays(self, value: str):
        self._property_changed('payer_holidays')
        self.__payer_holidays = value        

    @property
    def receiver_holidays(self) -> str:
        """The accrual calendar for receiver leg"""
        return self.__receiver_holidays

    @receiver_holidays.setter
    def receiver_holidays(self, value: str):
        self._property_changed('receiver_holidays')
        self.__receiver_holidays = value        


class InflationSwap(Instrument):
        
    """A vanilla inflation swap of fixed vs floating cashflows adjusted to an inflation
       rate"""

    @camel_case_translate
    def __init__(
        self,
        pay_or_receive: Union[PayReceive, str] = None,
        termination_date: Union[datetime.date, str] = None,
        notional_currency: Union[Currency, str] = None,
        effective_date: Union[datetime.date, str] = None,
        notional_amount: Union[float, str] = None,
        index: str = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate: Union[float, str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        base_cpi: float = None,
        clearing_house: Union[SwapClearingHouse, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.pay_or_receive = pay_or_receive
        self.termination_date = termination_date
        self.notional_currency = notional_currency
        self.effective_date = effective_date
        self.notional_amount = notional_amount
        self.index = index
        self.floating_rate_business_day_convention = floating_rate_business_day_convention
        self.fixed_rate = fixed_rate
        self.fixed_rate_business_day_convention = fixed_rate_business_day_convention
        self.fee = fee
        self.base_cpi = base_cpi
        self.clearing_house = clearing_house
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """InflationSwap"""
        return AssetType.InflationSwap        

    @property
    def pay_or_receive(self) -> Union[PayReceive, str]:
        """Pay or receive fixed"""
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: Union[PayReceive, str]):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = get_enum_value(PayReceive, value)        

    @property
    def termination_date(self) -> Union[datetime.date, str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[datetime.date, str]):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def effective_date(self) -> Union[datetime.date, str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[datetime.date, str]):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def index(self) -> str:
        """The underlying benchmark for the floating rate, e.g. CPI-U"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self._property_changed('index')
        self.__index = value        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('floating_rate_business_day_convention')
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self._property_changed('fixed_rate')
        self.__fixed_rate = value        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self._property_changed('fixed_rate_business_day_convention')
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, value)        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self._property_changed('fee')
        self.__fee = value        

    @property
    def base_cpi(self) -> float:
        """Base CPI level"""
        return self.__base_cpi

    @base_cpi.setter
    def base_cpi(self, value: float):
        self._property_changed('base_cpi')
        self.__base_cpi = value        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self._property_changed('clearing_house')
        self.__clearing_house = get_enum_value(SwapClearingHouse, value)        


class InstrumentsAnyAssetRef(Instrument):
        
    """An instrument that references an asset ID (from the asset service)"""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        buy_sell: Union[BuySell, str] = None,
        size: float = None,
        product_code: Union[ProductCode, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.buy_sell = buy_sell
        self.size = size
        self.product_code = product_code
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Cross Asset"""
        return AssetClass.Cross_Asset        

    @property
    def type(self) -> AssetType:
        """Any"""
        return AssetType.Any        

    @property
    def asset_id(self) -> str:
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def size(self) -> float:
        return self.__size

    @size.setter
    def size(self, value: float):
        self._property_changed('size')
        self.__size = value        

    @property
    def product_code(self) -> Union[ProductCode, str]:
        """Override the clearing destination/symbol"""
        return self.__product_code

    @product_code.setter
    def product_code(self, value: Union[ProductCode, str]):
        self._property_changed('product_code')
        self.__product_code = get_enum_value(ProductCode, value)        


class InstrumentsXassetBond(Instrument):
        
    """A bond"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        identifier: str = None,
        identifier_type: Union[UnderlierType, str] = None,
        size: float = None,
        settlement_date: Union[datetime.date, str] = None,
        settlement_currency: Union[Currency, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.size = size
        self.settlement_date = settlement_date
        self.settlement_currency = settlement_currency
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Cross Asset"""
        return AssetClass.Cross_Asset        

    @property
    def type(self) -> AssetType:
        """Bond"""
        return AssetType.Bond        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def identifier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__identifier_type

    @identifier_type.setter
    def identifier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('identifier_type')
        self.__identifier_type = get_enum_value(UnderlierType, value)        

    @property
    def size(self) -> float:
        return self.__size

    @size.setter
    def size(self, value: float):
        self._property_changed('size')
        self.__size = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        


class CommodOTCOption(Instrument):
        
    """Object representation of a commodities OTC option strategies"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        start: Union[datetime.date, str] = None,
        end: Union[datetime.date, str] = None,
        number_of_periods: int = None,
        strategy: str = None,
        quantity: Union[float, str] = None,
        quantity_unit: str = None,
        quantity_period: Union[Period, str] = None,
        legs: Tuple[CommodOTCOptionLeg, ...] = None,
        settlement: str = None,
        premium_summary: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.start = start
        self.end = end
        self.number_of_periods = number_of_periods
        self.strategy = strategy
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.quantity_period = quantity_period
        self.legs = legs
        self.settlement = settlement
        self.premium_summary = premium_summary
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """OptionStrategy"""
        return AssetType.OptionStrategy        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def start(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__start

    @start.setter
    def start(self, value: Union[datetime.date, str]):
        self._property_changed('start')
        self.__start = value        

    @property
    def end(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__end

    @end.setter
    def end(self, value: Union[datetime.date, str]):
        self._property_changed('end')
        self.__end = value        

    @property
    def number_of_periods(self) -> int:
        """The number of settlement periods"""
        return self.__number_of_periods

    @number_of_periods.setter
    def number_of_periods(self, value: int):
        self._property_changed('number_of_periods')
        self.__number_of_periods = value        

    @property
    def strategy(self) -> str:
        """Option Strategy"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def quantity(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: Union[float, str]):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def quantity_unit(self) -> str:
        """Commodity asset"""
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: str):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def quantity_period(self) -> Union[Period, str]:
        """A coding scheme to define a period corresponding to a quantity amount"""
        return self.__quantity_period

    @quantity_period.setter
    def quantity_period(self, value: Union[Period, str]):
        self._property_changed('quantity_period')
        self.__quantity_period = get_enum_value(Period, value)        

    @property
    def legs(self) -> Tuple[CommodOTCOptionLeg, ...]:
        """Commodities OTC option leg"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[CommodOTCOptionLeg, ...]):
        self._property_changed('legs')
        self.__legs = value        

    @property
    def settlement(self) -> str:
        """read only description in plain English of settlement terms"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: str):
        self._property_changed('settlement')
        self.__settlement = value        

    @property
    def premium_summary(self) -> Union[float, str]:
        """TBD : Overall Option premium for all Legs"""
        return self.__premium_summary

    @premium_summary.setter
    def premium_summary(self, value: Union[float, str]):
        self._property_changed('premium_summary')
        self.__premium_summary = value        


class CommodOTCSwap(Instrument):
        
    """Object representation of a commodities swap"""

    @camel_case_translate
    def __init__(
        self,
        start: Union[datetime.date, str] = None,
        end: Union[datetime.date, str] = None,
        number_of_periods: int = None,
        strategy: str = None,
        quantity: Union[float, str] = None,
        quantity_unit: str = None,
        quantity_period: Union[Period, str] = None,
        legs: Tuple[CommodOTCSwapLeg, ...] = None,
        settlement: str = None,
        name: str = None
    ):        
        super().__init__()
        self.start = start
        self.end = end
        self.number_of_periods = number_of_periods
        self.strategy = strategy
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.quantity_period = quantity_period
        self.legs = legs
        self.settlement = settlement
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """SwapStrategy"""
        return AssetType.SwapStrategy        

    @property
    def start(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__start

    @start.setter
    def start(self, value: Union[datetime.date, str]):
        self._property_changed('start')
        self.__start = value        

    @property
    def end(self) -> Union[datetime.date, str]:
        """Date or Contract Month"""
        return self.__end

    @end.setter
    def end(self, value: Union[datetime.date, str]):
        self._property_changed('end')
        self.__end = value        

    @property
    def number_of_periods(self) -> int:
        """The number of settlement periods"""
        return self.__number_of_periods

    @number_of_periods.setter
    def number_of_periods(self, value: int):
        self._property_changed('number_of_periods')
        self.__number_of_periods = value        

    @property
    def strategy(self) -> str:
        """Swap Strategy : Strip and Commodity Spread"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def quantity(self) -> Union[float, str]:
        """Size of some value, i.e. notional like 1.3b, 1.5, 1000"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: Union[float, str]):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def quantity_unit(self) -> str:
        """Commodity asset"""
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: str):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def quantity_period(self) -> Union[Period, str]:
        """A coding scheme to define a period corresponding to a quantity amount"""
        return self.__quantity_period

    @quantity_period.setter
    def quantity_period(self, value: Union[Period, str]):
        self._property_changed('quantity_period')
        self.__quantity_period = get_enum_value(Period, value)        

    @property
    def legs(self) -> Tuple[CommodOTCSwapLeg, ...]:
        """Commodities OTC swap leg"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[CommodOTCSwapLeg, ...]):
        self._property_changed('legs')
        self.__legs = value        

    @property
    def settlement(self) -> str:
        """read only description in plain English of settlement terms"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: str):
        self._property_changed('settlement')
        self.__settlement = value        


class EqOptionStrategy(Instrument):
        
    """Instrument definition for equity option strategy"""

    @camel_case_translate
    def __init__(
        self,
        underlier: Union[float, str],
        strategy: str,
        legs: Tuple[EqOptionLeg, ...],
        underlier_type: Union[UnderlierType, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        strike_price: Union[float, str] = None,
        option_type: Union[OptionType, str] = None,
        option_style: Union[OptionStyle, str] = None,
        number_of_options: float = None,
        multiplier: float = None,
        settlement_date: Union[datetime.date, str] = None,
        settlement_currency: Union[Currency, str] = None,
        premium: float = None,
        premium_payment_date: Union[datetime.date, str] = None,
        valuation_time: Union[ValuationTime, str] = None,
        method_of_settlement: Union[OptionSettlementMethod, str] = None,
        buy_sell: Union[BuySell, str] = None,
        premium_currency: Union[Currency, str] = None,
        exchange: str = None,
        trade_as: Union[TradeAs, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.underlier = underlier
        self.underlier_type = underlier_type
        self.strategy = strategy
        self.legs = legs
        self.expiration_date = expiration_date
        self.strike_price = strike_price
        self.option_type = option_type
        self.option_style = option_style
        self.number_of_options = number_of_options
        self.multiplier = multiplier
        self.settlement_date = settlement_date
        self.settlement_currency = settlement_currency
        self.premium = premium
        self.premium_payment_date = premium_payment_date
        self.valuation_time = valuation_time
        self.method_of_settlement = method_of_settlement
        self.buy_sell = buy_sell
        self.premium_currency = premium_currency
        self.exchange = exchange
        self.trade_as = trade_as
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """OptionStrategy"""
        return AssetType.OptionStrategy        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier security identifier"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def underlier_type(self) -> Union[UnderlierType, str]:
        """Type of underlyer"""
        return self.__underlier_type

    @underlier_type.setter
    def underlier_type(self, value: Union[UnderlierType, str]):
        self._property_changed('underlier_type')
        self.__underlier_type = get_enum_value(UnderlierType, value)        

    @property
    def strategy(self) -> str:
        """Option Strategy"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def legs(self) -> Tuple[EqOptionLeg, ...]:
        """Instrument definition for equity option leg"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[EqOptionLeg, ...]):
        self._property_changed('legs')
        self.__legs = value        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def option_style(self) -> Union[OptionStyle, str]:
        """Option Exercise Style"""
        return self.__option_style

    @option_style.setter
    def option_style(self, value: Union[OptionStyle, str]):
        self._property_changed('option_style')
        self.__option_style = get_enum_value(OptionStyle, value)        

    @property
    def number_of_options(self) -> float:
        """Number of options"""
        return self.__number_of_options

    @number_of_options.setter
    def number_of_options(self, value: float):
        self._property_changed('number_of_options')
        self.__number_of_options = value        

    @property
    def multiplier(self) -> float:
        """Number of stock units per option contract"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def valuation_time(self) -> Union[ValuationTime, str]:
        """Valuation time (e.g. MktClose, MktOpen) of the underlying level for exercise"""
        return self.__valuation_time

    @valuation_time.setter
    def valuation_time(self, value: Union[ValuationTime, str]):
        self._property_changed('valuation_time')
        self.__valuation_time = get_enum_value(ValuationTime, value)        

    @property
    def method_of_settlement(self) -> Union[OptionSettlementMethod, str]:
        """How the option is settled (e.g. Cash, Physical)"""
        return self.__method_of_settlement

    @method_of_settlement.setter
    def method_of_settlement(self, value: Union[OptionSettlementMethod, str]):
        self._property_changed('method_of_settlement')
        self.__method_of_settlement = get_enum_value(OptionSettlementMethod, value)        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def trade_as(self) -> Union[TradeAs, str]:
        """Option trade as (i.e. listed, otc, lookalike etc)"""
        return self.__trade_as

    @trade_as.setter
    def trade_as(self, value: Union[TradeAs, str]):
        self._property_changed('trade_as')
        self.__trade_as = get_enum_value(TradeAs, value)        


class FXMultiCrossBinary(Instrument):
        
    """Object representation of an FX multi-cross binary"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        legs: Tuple[FXMultiCrossBinaryLeg, ...] = None,
        notional_amount: Union[float, str] = None,
        notional_currency: Union[Currency, str] = None,
        settlement_date: Union[datetime.date, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        expiration_time: str = None,
        premium: Union[float, str] = None,
        premium_currency: Union[Currency, str] = None,
        premium_payment_date: str = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.legs = legs
        self.notional_amount = notional_amount
        self.notional_currency = notional_currency
        self.settlement_date = settlement_date
        self.expiration_date = expiration_date
        self.expiration_time = expiration_time
        self.premium = premium
        self.premium_currency = premium_currency
        self.premium_payment_date = premium_payment_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """MultiCrossBinary"""
        return AssetType.MultiCrossBinary        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def legs(self) -> Tuple[FXMultiCrossBinaryLeg, ...]:
        """Object representation of a single leg of a multi-cross binary option"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[FXMultiCrossBinaryLeg, ...]):
        self._property_changed('legs')
        self.__legs = value        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date of the option, after expiration"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def expiration_time(self) -> str:
        """The location and (optionally) time of spot for expiration"""
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value: str):
        self._property_changed('expiration_time')
        self.__expiration_time = value        

    @property
    def premium(self) -> Union[float, str]:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def premium_payment_date(self) -> str:
        """Payment date of the option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: str):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        


class FXOptionStrategy(Instrument):
        
    """Object representation of a FX option Strategy"""

    @camel_case_translate
    def __init__(
        self,
        pair: str = None,
        buy_sell: Union[BuySell, str] = None,
        strategy_name: str = None,
        legs: Tuple[FXOptionLeg, ...] = None,
        option_type: Union[OptionType, str] = None,
        notional_amount: Union[float, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount_other_currency: Union[float, str] = None,
        strike_price: Union[float, str] = None,
        settlement_date: Union[datetime.date, str] = None,
        settlement_currency: Union[Currency, str] = None,
        settlement_rate_option: str = None,
        method_of_settlement: Union[OptionSettlementMethod, str] = None,
        expiration_date: Union[datetime.date, str] = None,
        expiration_time: str = None,
        premium: Union[float, str] = None,
        premium_currency: Union[Currency, str] = None,
        premium_payment_date: str = None,
        name: str = None
    ):        
        super().__init__()
        self.pair = pair
        self.buy_sell = buy_sell
        self.strategy_name = strategy_name
        self.legs = legs
        self.option_type = option_type
        self.notional_amount = notional_amount
        self.notional_currency = notional_currency
        self.notional_amount_other_currency = notional_amount_other_currency
        self.strike_price = strike_price
        self.settlement_date = settlement_date
        self.settlement_currency = settlement_currency
        self.settlement_rate_option = settlement_rate_option
        self.method_of_settlement = method_of_settlement
        self.expiration_date = expiration_date
        self.expiration_time = expiration_time
        self.premium = premium
        self.premium_currency = premium_currency
        self.premium_payment_date = premium_payment_date
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """OptionStrategy"""
        return AssetType.OptionStrategy        

    @property
    def pair(self) -> str:
        """A currency pair, e.g.: EURUSD or EUR USD"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self._property_changed('pair')
        self.__pair = value        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def strategy_name(self) -> str:
        return self.__strategy_name

    @strategy_name.setter
    def strategy_name(self, value: str):
        self._property_changed('strategy_name')
        self.__strategy_name = value        

    @property
    def legs(self) -> Tuple[FXOptionLeg, ...]:
        """Object representation of a FX option leg used in FXOptionStrategy"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[FXOptionLeg, ...]):
        self._property_changed('legs')
        self.__legs = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self._property_changed('notional_currency')
        self.__notional_currency = get_enum_value(Currency, value)        

    @property
    def notional_amount_other_currency(self) -> Union[float, str]:
        """Notional amount in currency other than NotionalCurrency from the pair"""
        return self.__notional_amount_other_currency

    @notional_amount_other_currency.setter
    def notional_amount_other_currency(self, value: Union[float, str]):
        self._property_changed('notional_amount_other_currency')
        self.__notional_amount_other_currency = value        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF, 10/vol,
           100k/pv, p=10000, p=10000USD, $200K/BP, or multiple strikes
           65.4/-45.8"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date of the option, after expiration"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_currency(self) -> Union[Currency, str]:
        """Currency of settlement"""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: Union[Currency, str]):
        self._property_changed('settlement_currency')
        self.__settlement_currency = get_enum_value(Currency, value)        

    @property
    def settlement_rate_option(self) -> str:
        """The source of spot for settlement"""
        return self.__settlement_rate_option

    @settlement_rate_option.setter
    def settlement_rate_option(self, value: str):
        self._property_changed('settlement_rate_option')
        self.__settlement_rate_option = value        

    @property
    def method_of_settlement(self) -> Union[OptionSettlementMethod, str]:
        """How the option is settled (e.g. Cash, Physical)"""
        return self.__method_of_settlement

    @method_of_settlement.setter
    def method_of_settlement(self, value: Union[OptionSettlementMethod, str]):
        self._property_changed('method_of_settlement')
        self.__method_of_settlement = get_enum_value(OptionSettlementMethod, value)        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m, Dec21"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def expiration_time(self) -> str:
        """The location and (optionally) time of spot for expiration"""
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, value: str):
        self._property_changed('expiration_time')
        self.__expiration_time = value        

    @property
    def premium(self) -> Union[float, str]:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: Union[float, str]):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency of the option premium"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def premium_payment_date(self) -> str:
        """Payment date of the option premium"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: str):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        


class InvoiceSpread(Instrument):
        
    """An interest swap vs a bond future"""

    @camel_case_translate
    def __init__(
        self,
        buy_sell: Union[BuySell, str] = None,
        notional_amount: Union[float, str] = None,
        underlier: Union[float, str] = None,
        swap: IRSwap = None,
        future: IRBondFuture = None,
        name: str = None
    ):        
        super().__init__()
        self.buy_sell = buy_sell
        self.notional_amount = notional_amount
        self.underlier = underlier
        self.swap = swap
        self.future = future
        self.name = name

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """InvoiceSpread"""
        return AssetType.InvoiceSpread        

    @property
    def buy_sell(self) -> Union[BuySell, str]:
        """Buy or Sell side of contract"""
        return self.__buy_sell

    @buy_sell.setter
    def buy_sell(self, value: Union[BuySell, str]):
        self._property_changed('buy_sell')
        self.__buy_sell = get_enum_value(BuySell, value)        

    @property
    def notional_amount(self) -> Union[float, str]:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: Union[float, str]):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def underlier(self) -> Union[float, str]:
        """Underlier of the bond future"""
        return self.__underlier

    @underlier.setter
    def underlier(self, value: Union[float, str]):
        self._property_changed('underlier')
        self.__underlier = value        

    @property
    def swap(self) -> IRSwap:
        """A vanilla interest rate swap of fixed vs floating cashflows"""
        return self.__swap

    @swap.setter
    def swap(self, value: IRSwap):
        self._property_changed('swap')
        self.__swap = value        

    @property
    def future(self) -> IRBondFuture:
        """A future on a (treasury) bond"""
        return self.__future

    @future.setter
    def future(self, value: IRBondFuture):
        self._property_changed('future')
        self.__future = value        
