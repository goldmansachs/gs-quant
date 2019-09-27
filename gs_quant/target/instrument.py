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

from gs_quant.base import Instrument, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class CSLPython(Instrument):
        
    """Object representation of an arbitrary payoff defined in Python"""
       
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
        fx_cross_array_params: Tuple[CSLFXCrossArray, ...] = None        
    ):
        super().__init__()
        self.__class_name = class_name
        self.__denominated = get_enum_value(Currency, denominated)
        self.__double_params = double_params
        self.__date_params = date_params
        self.__string_params = string_params
        self.__simple_schedule_params = simple_schedule_params
        self.__schedule_params = schedule_params
        self.__currency_params = currency_params
        self.__stock_params = stock_params
        self.__index_params = index_params
        self.__fx_cross_params = fx_cross_params
        self.__double_array_params = double_array_params
        self.__date_array_params = date_array_params
        self.__string_array_params = string_array_params
        self.__simple_schedule_array_params = simple_schedule_array_params
        self.__schedule_array_params = schedule_array_params
        self.__currency_array_params = currency_array_params
        self.__stock_array_params = stock_array_params
        self.__index_array_params = index_array_params
        self.__fx_cross_array_params = fx_cross_array_params

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
        self.__class_name = value
        self._property_changed('class_name')        

    @property
    def denominated(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__denominated

    @denominated.setter
    def denominated(self, value: Union[Currency, str]):
        self.__denominated = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('denominated')        

    @property
    def double_params(self) -> Tuple[CSLDouble, ...]:
        """A double"""
        return self.__double_params

    @double_params.setter
    def double_params(self, value: Tuple[CSLDouble, ...]):
        self.__double_params = value
        self._property_changed('double_params')        

    @property
    def date_params(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__date_params

    @date_params.setter
    def date_params(self, value: Tuple[CSLDate, ...]):
        self.__date_params = value
        self._property_changed('date_params')        

    @property
    def string_params(self) -> Tuple[CSLString, ...]:
        """A string"""
        return self.__string_params

    @string_params.setter
    def string_params(self, value: Tuple[CSLString, ...]):
        self.__string_params = value
        self._property_changed('string_params')        

    @property
    def simple_schedule_params(self) -> Tuple[CSLSimpleSchedule, ...]:
        """A fixing date, settlement date pair"""
        return self.__simple_schedule_params

    @simple_schedule_params.setter
    def simple_schedule_params(self, value: Tuple[CSLSimpleSchedule, ...]):
        self.__simple_schedule_params = value
        self._property_changed('simple_schedule_params')        

    @property
    def schedule_params(self) -> Tuple[CSLSchedule, ...]:
        """A schedule"""
        return self.__schedule_params

    @schedule_params.setter
    def schedule_params(self, value: Tuple[CSLSchedule, ...]):
        self.__schedule_params = value
        self._property_changed('schedule_params')        

    @property
    def currency_params(self) -> Tuple[CSLCurrency, ...]:
        """A currency"""
        return self.__currency_params

    @currency_params.setter
    def currency_params(self, value: Tuple[CSLCurrency, ...]):
        self.__currency_params = value
        self._property_changed('currency_params')        

    @property
    def stock_params(self) -> Tuple[CSLStock, ...]:
        """A stock"""
        return self.__stock_params

    @stock_params.setter
    def stock_params(self, value: Tuple[CSLStock, ...]):
        self.__stock_params = value
        self._property_changed('stock_params')        

    @property
    def index_params(self) -> Tuple[CSLIndex, ...]:
        """An index"""
        return self.__index_params

    @index_params.setter
    def index_params(self, value: Tuple[CSLIndex, ...]):
        self.__index_params = value
        self._property_changed('index_params')        

    @property
    def fx_cross_params(self) -> Tuple[CSLFXCross, ...]:
        """An FX cross"""
        return self.__fx_cross_params

    @fx_cross_params.setter
    def fx_cross_params(self, value: Tuple[CSLFXCross, ...]):
        self.__fx_cross_params = value
        self._property_changed('fx_cross_params')        

    @property
    def double_array_params(self) -> Tuple[CSLDoubleArray, ...]:
        """An array of doubles"""
        return self.__double_array_params

    @double_array_params.setter
    def double_array_params(self, value: Tuple[CSLDoubleArray, ...]):
        self.__double_array_params = value
        self._property_changed('double_array_params')        

    @property
    def date_array_params(self) -> Tuple[CSLDateArray, ...]:
        """An array of dates"""
        return self.__date_array_params

    @date_array_params.setter
    def date_array_params(self, value: Tuple[CSLDateArray, ...]):
        self.__date_array_params = value
        self._property_changed('date_array_params')        

    @property
    def string_array_params(self) -> Tuple[CSLStringArray, ...]:
        """An array of strings"""
        return self.__string_array_params

    @string_array_params.setter
    def string_array_params(self, value: Tuple[CSLStringArray, ...]):
        self.__string_array_params = value
        self._property_changed('string_array_params')        

    @property
    def simple_schedule_array_params(self) -> Tuple[CSLSimpleScheduleArray, ...]:
        """An array of simple schedules"""
        return self.__simple_schedule_array_params

    @simple_schedule_array_params.setter
    def simple_schedule_array_params(self, value: Tuple[CSLSimpleScheduleArray, ...]):
        self.__simple_schedule_array_params = value
        self._property_changed('simple_schedule_array_params')        

    @property
    def schedule_array_params(self) -> Tuple[CSLScheduleArray, ...]:
        """An array of schedules"""
        return self.__schedule_array_params

    @schedule_array_params.setter
    def schedule_array_params(self, value: Tuple[CSLScheduleArray, ...]):
        self.__schedule_array_params = value
        self._property_changed('schedule_array_params')        

    @property
    def currency_array_params(self) -> Tuple[CSLCurrencyArray, ...]:
        """An array of currencies"""
        return self.__currency_array_params

    @currency_array_params.setter
    def currency_array_params(self, value: Tuple[CSLCurrencyArray, ...]):
        self.__currency_array_params = value
        self._property_changed('currency_array_params')        

    @property
    def stock_array_params(self) -> Tuple[CSLStockArray, ...]:
        """An array of stocks"""
        return self.__stock_array_params

    @stock_array_params.setter
    def stock_array_params(self, value: Tuple[CSLStockArray, ...]):
        self.__stock_array_params = value
        self._property_changed('stock_array_params')        

    @property
    def index_array_params(self) -> Tuple[CSLIndexArray, ...]:
        """An array of indices"""
        return self.__index_array_params

    @index_array_params.setter
    def index_array_params(self, value: Tuple[CSLIndexArray, ...]):
        self.__index_array_params = value
        self._property_changed('index_array_params')        

    @property
    def fx_cross_array_params(self) -> Tuple[CSLFXCrossArray, ...]:
        """An array of FX crosses"""
        return self.__fx_cross_array_params

    @fx_cross_array_params.setter
    def fx_cross_array_params(self, value: Tuple[CSLFXCrossArray, ...]):
        self.__fx_cross_array_params = value
        self._property_changed('fx_cross_array_params')        


class CommodSwap(Instrument):
        
    """Object representation of a commodities swap"""
       
    def __init__(
        self,
        commodity: Union[CommodityAsset, str],
        start: Union[datetime.date, str],
        commodity_reference_price: str = None,
        notional_amount: float = 1000000.0,
        currency: Union[Currency, str] = None,
        calculation_periods: int = None,
        calculation_period_frequency: Union[Frequency, str] = None        
    ):
        super().__init__()
        self.__commodity = get_enum_value(CommodityAsset, commodity)
        self.__commodity_reference_price = commodity_reference_price
        self.__start = start
        self.__notional_amount = notional_amount
        self.__currency = get_enum_value(Currency, currency)
        self.__calculation_periods = calculation_periods
        self.__calculation_period_frequency = get_enum_value(Frequency, calculation_period_frequency)

    @property
    def asset_class(self) -> AssetClass:
        """Commod"""
        return AssetClass.Commod        

    @property
    def type(self) -> AssetType:
        """Swap"""
        return AssetType.Swap        

    @property
    def commodity(self) -> Union[CommodityAsset, str]:
        """Commodity asset"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: Union[CommodityAsset, str]):
        self.__commodity = value if isinstance(value, CommodityAsset) else get_enum_value(CommodityAsset, value)
        self._property_changed('commodity')        

    @property
    def commodity_reference_price(self) -> str:
        return self.__commodity_reference_price

    @commodity_reference_price.setter
    def commodity_reference_price(self, value: str):
        self.__commodity_reference_price = value
        self._property_changed('commodity_reference_price')        

    @property
    def start(self) -> Union[datetime.date, str]:
        return self.__start

    @start.setter
    def start(self, value: Union[datetime.date, str]):
        self.__start = value
        self._property_changed('start')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def calculation_periods(self) -> int:
        """The number of calculation periods"""
        return self.__calculation_periods

    @calculation_periods.setter
    def calculation_periods(self, value: int):
        self.__calculation_periods = value
        self._property_changed('calculation_periods')        

    @property
    def calculation_period_frequency(self) -> Union[Frequency, str]:
        """The frequency of the calculation periods"""
        return self.__calculation_period_frequency

    @calculation_period_frequency.setter
    def calculation_period_frequency(self, value: Union[Frequency, str]):
        self.__calculation_period_frequency = value if isinstance(value, Frequency) else get_enum_value(Frequency, value)
        self._property_changed('calculation_period_frequency')        


class EqCliquet(Instrument):
        
    """Object representation of an Equity Cliquet"""
       
    def __init__(
        self,
        asset: str,
        expiration_date: Union[datetime.date, str],
        strike_price: float,
        currency: Union[Currency, str] = None,
        first_valuation_date: datetime.date = None,
        global_floor: float = -1000000,
        global_cap: float = 1000000,
        last_valuation_date: datetime.date = None,
        notional_amount: float = 1000000,
        payment_frequency: str = 'Maturity',
        return_style: str = 'Rate of Return',
        return_type: str = 'Sum',
        valuation_period: str = None        
    ):
        super().__init__()
        self.__asset = asset
        self.__currency = get_enum_value(Currency, currency)
        self.__expiration_date = expiration_date
        self.__first_valuation_date = first_valuation_date
        self.__global_floor = global_floor
        self.__global_cap = global_cap
        self.__last_valuation_date = last_valuation_date
        self.__notional_amount = notional_amount
        self.__payment_frequency = payment_frequency
        self.__return_style = return_style
        self.__return_type = return_type
        self.__strike_price = strike_price
        self.__valuation_period = valuation_period

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Cliquet"""
        return AssetType.Cliquet        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def first_valuation_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__first_valuation_date

    @first_valuation_date.setter
    def first_valuation_date(self, value: datetime.date):
        self.__first_valuation_date = value
        self._property_changed('first_valuation_date')        

    @property
    def global_floor(self) -> float:
        """Global Floor of return, relevant only if paying at maturity"""
        return self.__global_floor

    @global_floor.setter
    def global_floor(self, value: float):
        self.__global_floor = value
        self._property_changed('global_floor')        

    @property
    def global_cap(self) -> float:
        """Global Cap of return, relevant only if paying at maturity"""
        return self.__global_cap

    @global_cap.setter
    def global_cap(self, value: float):
        self.__global_cap = value
        self._property_changed('global_cap')        

    @property
    def last_valuation_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__last_valuation_date

    @last_valuation_date.setter
    def last_valuation_date(self, value: datetime.date):
        self.__last_valuation_date = value
        self._property_changed('last_valuation_date')        

    @property
    def notional_amount(self) -> float:
        """Notional of this position"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def payment_frequency(self) -> str:
        return self.__payment_frequency

    @payment_frequency.setter
    def payment_frequency(self, value: str):
        self.__payment_frequency = value
        self._property_changed('payment_frequency')        

    @property
    def return_style(self) -> str:
        """Return calculation style"""
        return self.__return_style

    @return_style.setter
    def return_style(self, value: str):
        self.__return_style = value
        self._property_changed('return_style')        

    @property
    def return_type(self) -> str:
        """Sum or Product of periodic return, relevant only if paying at maturity"""
        return self.__return_type

    @return_type.setter
    def return_type(self, value: str):
        self.__return_type = value
        self._property_changed('return_type')        

    @property
    def strike_price(self) -> float:
        """Strike price as value"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: float):
        self.__strike_price = value
        self._property_changed('strike_price')        

    @property
    def valuation_period(self) -> str:
        """Tenor"""
        return self.__valuation_period

    @valuation_period.setter
    def valuation_period(self, value: str):
        self.__valuation_period = value
        self._property_changed('valuation_period')        


class EqForward(Instrument):
        
    """Object representation of an equity forward"""
       
    def __init__(
        self,
        asset: str,
        expiration_date: Union[datetime.date, str],
        forward_price: float,
        number_of_shares: int = 1        
    ):
        super().__init__()
        self.__asset = asset
        self.__number_of_shares = number_of_shares
        self.__expiration_date = expiration_date
        self.__forward_price = forward_price

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Forward"""
        return AssetType.Forward        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def number_of_shares(self) -> int:
        """Number of shares"""
        return self.__number_of_shares

    @number_of_shares.setter
    def number_of_shares(self, value: int):
        self.__number_of_shares = value
        self._property_changed('number_of_shares')        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def forward_price(self) -> float:
        """Forward price"""
        return self.__forward_price

    @forward_price.setter
    def forward_price(self, value: float):
        self.__forward_price = value
        self._property_changed('forward_price')        


class EqOption(Instrument):
        
    """Instrument definition for equity option"""
       
    def __init__(
        self,
        asset: str,
        expiration_date: Union[datetime.date, str],
        strike_price: Union[float, str],
        option_type: Union[OptionType, str],
        option_style: Union[OptionStyle, str],
        number_of_options: float = None,
        exchange: str = None,
        multiplier: float = None,
        settlement_date: Union[datetime.date, str] = None,
        currency: Union[Currency, str] = None,
        premium: float = None        
    ):
        super().__init__()
        self.__number_of_options = number_of_options
        self.__asset = asset
        self.__exchange = exchange
        self.__expiration_date = expiration_date
        self.__strike_price = strike_price
        self.__option_type = get_enum_value(OptionType, option_type)
        self.__option_style = get_enum_value(OptionStyle, option_style)
        self.__multiplier = multiplier
        self.__settlement_date = settlement_date
        self.__currency = get_enum_value(Currency, currency)
        self.__premium = premium

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def number_of_options(self) -> float:
        """Number of options"""
        return self.__number_of_options

    @number_of_options.setter
    def number_of_options(self, value: float):
        self.__number_of_options = value
        self._property_changed('number_of_options')        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def strike_price(self) -> Union[float, str]:
        """Strike as value, percent or string e.g. 62.5, 95%, ATM, ATMF, 25ATM, 20CallDelta, 10PutDelta, 10NS"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self.__strike_price = value
        self._property_changed('strike_price')        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self.__option_type = value if isinstance(value, OptionType) else get_enum_value(OptionType, value)
        self._property_changed('option_type')        

    @property
    def option_style(self) -> Union[OptionStyle, str]:
        """Option Exercise Style"""
        return self.__option_style

    @option_style.setter
    def option_style(self, value: Union[OptionStyle, str]):
        self.__option_style = value if isinstance(value, OptionStyle) else get_enum_value(OptionStyle, value)
        self._property_changed('option_style')        

    @property
    def multiplier(self) -> float:
        """Number of stock units per option contract"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self.__multiplier = value
        self._property_changed('multiplier')        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self.__settlement_date = value
        self._property_changed('settlement_date')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        


class EqVarianceSwap(Instrument):
        
    """Instrument definition for equity variance swap"""
       
    def __init__(
        self,
        asset: str,
        expiration_date: Union[datetime.date, str],
        strike_price: Union[float, str],
        variance_cap: float = None,
        settlement_date: Union[datetime.date, str] = None,
        premium: float = None        
    ):
        super().__init__()
        self.__asset = asset
        self.__expiration_date = expiration_date
        self.__strike_price = strike_price
        self.__variance_cap = variance_cap
        self.__settlement_date = settlement_date
        self.__premium = premium

    @property
    def asset_class(self) -> AssetClass:
        """Equity"""
        return AssetClass.Equity        

    @property
    def type(self) -> AssetType:
        """VarianceSwap"""
        return AssetType.VarianceSwap        

    @property
    def asset(self) -> str:
        """Ticker of the underlying stock or index"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self.__asset = value
        self._property_changed('asset')        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def strike_price(self) -> Union[float, str]:
        """Variance strike as value or percentage string e.g. 62.5, 95%"""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self.__strike_price = value
        self._property_changed('strike_price')        

    @property
    def variance_cap(self) -> float:
        """Variance Cap as absolute value"""
        return self.__variance_cap

    @variance_cap.setter
    def variance_cap(self, value: float):
        self.__variance_cap = value
        self._property_changed('variance_cap')        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Settlement date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self.__settlement_date = value
        self._property_changed('settlement_date')        

    @property
    def premium(self) -> float:
        """VarSwap premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        


class FXForward(Instrument):
        
    """Object representation of an FX forward"""
       
    def __init__(
        self,
        pair: str = None,
        settlement_date: Union[datetime.date, str] = None,
        forward_rate: float = None,
        notional_amount: float = None        
    ):
        super().__init__()
        self.__pair = pair
        self.__settlement_date = settlement_date
        self.__forward_rate = forward_rate
        self.__notional_amount = notional_amount

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
        """Currency pair"""
        return self.__pair

    @pair.setter
    def pair(self, value: str):
        self.__pair = value
        self._property_changed('pair')        

    @property
    def settlement_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: Union[datetime.date, str]):
        self.__settlement_date = value
        self._property_changed('settlement_date')        

    @property
    def forward_rate(self) -> float:
        """Forward FX rate"""
        return self.__forward_rate

    @forward_rate.setter
    def forward_rate(self, value: float):
        self.__forward_rate = value
        self._property_changed('forward_rate')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        


class FXOption(Instrument):
        
    """Object representation of a FX option"""
       
    def __init__(
        self,
        call_currency: Union[Currency, str],
        put_currency: Union[Currency, str],
        expiration_date: Union[datetime.date, str],
        option_type: Union[OptionType, str],
        call_amount: float = 1000000.0,
        put_amount: float = 1000000.0,
        strike: Union[float, str] = None,
        premium: float = 0        
    ):
        super().__init__()
        self.__call_currency = get_enum_value(Currency, call_currency)
        self.__put_currency = get_enum_value(Currency, put_currency)
        self.__call_amount = call_amount
        self.__put_amount = put_amount
        self.__strike = strike
        self.__expiration_date = expiration_date
        self.__option_type = get_enum_value(OptionType, option_type)
        self.__premium = premium

    @property
    def asset_class(self) -> AssetClass:
        """FX"""
        return AssetClass.FX        

    @property
    def type(self) -> AssetType:
        """Option"""
        return AssetType.Option        

    @property
    def call_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__call_currency

    @call_currency.setter
    def call_currency(self, value: Union[Currency, str]):
        self.__call_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('call_currency')        

    @property
    def put_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__put_currency

    @put_currency.setter
    def put_currency(self, value: Union[Currency, str]):
        self.__put_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('put_currency')        

    @property
    def call_amount(self) -> float:
        """Amount of the call currency"""
        return self.__call_amount

    @call_amount.setter
    def call_amount(self, value: float):
        self.__call_amount = value
        self._property_changed('call_amount')        

    @property
    def put_amount(self) -> float:
        """Amount of the put currency"""
        return self.__put_amount

    @put_amount.setter
    def put_amount(self, value: float):
        self.__put_amount = value
        self._property_changed('put_amount')        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self.__option_type = value if isinstance(value, OptionType) else get_enum_value(OptionType, value)
        self._property_changed('option_type')        

    @property
    def premium(self) -> float:
        """Option premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        


class Forward(Instrument):
        
    """Object representation of a forward"""
       
    def __init__(
        self,
        currency: Union[Currency, str],
        expiration_date: Union[datetime.date, str],
        notional_amount: float = None        
    ):
        super().__init__()
        self.__currency = get_enum_value(Currency, currency)
        self.__expiration_date = expiration_date
        self.__notional_amount = notional_amount

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
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def expiration_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[datetime.date, str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        


class IRBasisSwap(Instrument):
        
    """An exchange of cashflows from different interest rate indices"""
       
    def __init__(
        self,
        termination_date: Union[Union[datetime.date, str], str],
        notional_currency: Union[Currency, str],
        notional_amount: float = 1000000.0,
        effective_date: Union[Union[datetime.date, str], str] = None,
        payer_spread: float = None,
        payer_rate_option: str = None,
        payer_designated_maturity: str = None,
        payer_frequency: str = None,
        payer_day_count_fraction: Union[DayCountFraction, str] = None,
        payer_business_day_convention: Union[BusinessDayConvention, str] = None,
        receiver_spread: float = None,
        receiver_rate_option: str = None,
        receiver_designated_maturity: str = None,
        receiver_frequency: str = None,
        receiver_day_count_fraction: Union[DayCountFraction, str] = None,
        receiver_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        clearing_house: Union[SwapClearingHouse, str] = None        
    ):
        super().__init__()
        self.__notional_amount = notional_amount
        self.__notional_currency = get_enum_value(Currency, notional_currency)
        self.__effective_date = effective_date
        self.__termination_date = termination_date
        self.__payer_spread = payer_spread
        self.__payer_rate_option = payer_rate_option
        self.__payer_designated_maturity = payer_designated_maturity
        self.__payer_frequency = payer_frequency
        self.__payer_day_count_fraction = get_enum_value(DayCountFraction, payer_day_count_fraction)
        self.__payer_business_day_convention = get_enum_value(BusinessDayConvention, payer_business_day_convention)
        self.__receiver_spread = receiver_spread
        self.__receiver_rate_option = receiver_rate_option
        self.__receiver_designated_maturity = receiver_designated_maturity
        self.__receiver_frequency = receiver_frequency
        self.__receiver_day_count_fraction = get_enum_value(DayCountFraction, receiver_day_count_fraction)
        self.__receiver_business_day_convention = get_enum_value(BusinessDayConvention, receiver_business_day_convention)
        self.__fee = fee
        self.__clearing_house = get_enum_value(SwapClearingHouse, clearing_house)

    @property
    def asset_class(self) -> AssetClass:
        """Rates"""
        return AssetClass.Rates        

    @property
    def type(self) -> AssetType:
        """BasisSwap"""
        return AssetType.BasisSwap        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self.__notional_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notional_currency')        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self.__termination_date = value
        self._property_changed('termination_date')        

    @property
    def payer_spread(self) -> float:
        """Spread over the payer rate"""
        return self.__payer_spread

    @payer_spread.setter
    def payer_spread(self, value: float):
        self.__payer_spread = value
        self._property_changed('payer_spread')        

    @property
    def payer_rate_option(self) -> str:
        """The underlying benchmark for the payer, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__payer_rate_option

    @payer_rate_option.setter
    def payer_rate_option(self, value: str):
        self.__payer_rate_option = value
        self._property_changed('payer_rate_option')        

    @property
    def payer_designated_maturity(self) -> str:
        """Tenor of the payerRateOption, e.g. 3m, 6m"""
        return self.__payer_designated_maturity

    @payer_designated_maturity.setter
    def payer_designated_maturity(self, value: str):
        self.__payer_designated_maturity = value
        self._property_changed('payer_designated_maturity')        

    @property
    def payer_frequency(self) -> str:
        """The frequency of payer payments, e.g. 6m"""
        return self.__payer_frequency

    @payer_frequency.setter
    def payer_frequency(self, value: str):
        self.__payer_frequency = value
        self._property_changed('payer_frequency')        

    @property
    def payer_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the payer"""
        return self.__payer_day_count_fraction

    @payer_day_count_fraction.setter
    def payer_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__payer_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('payer_day_count_fraction')        

    @property
    def payer_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the payer"""
        return self.__payer_business_day_convention

    @payer_business_day_convention.setter
    def payer_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__payer_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('payer_business_day_convention')        

    @property
    def receiver_spread(self) -> float:
        """Spread over the receiver rate"""
        return self.__receiver_spread

    @receiver_spread.setter
    def receiver_spread(self, value: float):
        self.__receiver_spread = value
        self._property_changed('receiver_spread')        

    @property
    def receiver_rate_option(self) -> str:
        """The underlying benchmark for the receiver, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__receiver_rate_option

    @receiver_rate_option.setter
    def receiver_rate_option(self, value: str):
        self.__receiver_rate_option = value
        self._property_changed('receiver_rate_option')        

    @property
    def receiver_designated_maturity(self) -> str:
        """Tenor of the receiverRateOption, e.g. 3m, 6m"""
        return self.__receiver_designated_maturity

    @receiver_designated_maturity.setter
    def receiver_designated_maturity(self, value: str):
        self.__receiver_designated_maturity = value
        self._property_changed('receiver_designated_maturity')        

    @property
    def receiver_frequency(self) -> str:
        """The frequency of receiver payments, e.g. 6m"""
        return self.__receiver_frequency

    @receiver_frequency.setter
    def receiver_frequency(self, value: str):
        self.__receiver_frequency = value
        self._property_changed('receiver_frequency')        

    @property
    def receiver_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the receiver"""
        return self.__receiver_day_count_fraction

    @receiver_day_count_fraction.setter
    def receiver_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__receiver_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('receiver_day_count_fraction')        

    @property
    def receiver_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the receiver"""
        return self.__receiver_business_day_convention

    @receiver_business_day_convention.setter
    def receiver_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__receiver_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('receiver_business_day_convention')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self.__clearing_house = value if isinstance(value, SwapClearingHouse) else get_enum_value(SwapClearingHouse, value)
        self._property_changed('clearing_house')        


class IRCap(Instrument):
        
    """Object representation of an interest rate cap"""
       
    def __init__(
        self,
        termination_date: Union[datetime.date, str],
        notional_currency: Union[Currency, str],
        notional_amount: float = 1000000.0,
        effective_date: Union[datetime.date, str] = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        cap_rate: Union[float, str] = None,
        premium: float = 0,
        fee: float = 0,
        premium_payment_date: Union[datetime.date, str] = None        
    ):
        super().__init__()
        self.__termination_date = termination_date
        self.__notional_currency = get_enum_value(Currency, notional_currency)
        self.__notional_amount = notional_amount
        self.__effective_date = effective_date
        self.__floating_rate_option = floating_rate_option
        self.__floating_rate_designated_maturity = floating_rate_designated_maturity
        self.__floating_rate_frequency = floating_rate_frequency
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, floating_rate_day_count_fraction)
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, floating_rate_business_day_convention)
        self.__cap_rate = cap_rate
        self.__premium = premium
        self.__fee = fee
        self.__premium_payment_date = premium_payment_date

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
        self.__termination_date = value
        self._property_changed('termination_date')        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self.__notional_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notional_currency')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def effective_date(self) -> Union[datetime.date, str]:
        """The date on which the cap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[datetime.date, str]):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self.__floating_rate_option = value
        self._property_changed('floating_rate_option')        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self.__floating_rate_designated_maturity = value
        self._property_changed('floating_rate_designated_maturity')        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self.__floating_rate_frequency = value
        self._property_changed('floating_rate_frequency')        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__floating_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floating_rate_day_count_fraction')        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__floating_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floating_rate_business_day_convention')        

    @property
    def cap_rate(self) -> Union[float, str]:
        """The rate of this cap, as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__cap_rate

    @cap_rate.setter
    def cap_rate(self, value: Union[float, str]):
        self.__cap_rate = value
        self._property_changed('cap_rate')        

    @property
    def premium(self) -> float:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self.__premium_payment_date = value
        self._property_changed('premium_payment_date')        


class IRFloor(Instrument):
        
    """Object representation of an interest rate floor"""
       
    def __init__(
        self,
        termination_date: Union[datetime.date, str],
        notional_currency: Union[Currency, str],
        notional_amount: float = 1000000.0,
        effective_date: Union[datetime.date, str] = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        floor_rate: Union[float, str] = None,
        fee: float = 0,
        premium_payment_date: Union[datetime.date, str] = None        
    ):
        super().__init__()
        self.__termination_date = termination_date
        self.__notional_currency = get_enum_value(Currency, notional_currency)
        self.__notional_amount = notional_amount
        self.__effective_date = effective_date
        self.__floating_rate_option = floating_rate_option
        self.__floating_rate_designated_maturity = floating_rate_designated_maturity
        self.__floating_rate_frequency = floating_rate_frequency
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, floating_rate_day_count_fraction)
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, floating_rate_business_day_convention)
        self.__floor_rate = floor_rate
        self.__fee = fee
        self.__premium_payment_date = premium_payment_date

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
        self.__termination_date = value
        self._property_changed('termination_date')        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self.__notional_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notional_currency')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def effective_date(self) -> Union[datetime.date, str]:
        """The date on which the floor becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[datetime.date, str]):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self.__floating_rate_option = value
        self._property_changed('floating_rate_option')        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self.__floating_rate_designated_maturity = value
        self._property_changed('floating_rate_designated_maturity')        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self.__floating_rate_frequency = value
        self._property_changed('floating_rate_frequency')        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__floating_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floating_rate_day_count_fraction')        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__floating_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floating_rate_business_day_convention')        

    @property
    def floor_rate(self) -> Union[float, str]:
        """The rate of this floor, as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__floor_rate

    @floor_rate.setter
    def floor_rate(self, value: Union[float, str]):
        self.__floor_rate = value
        self._property_changed('floor_rate')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self.__premium_payment_date = value
        self._property_changed('premium_payment_date')        


class IRSwap(Instrument):
        
    """A vanilla interest rate swap of fixed vs floating cashflows"""
       
    def __init__(
        self,
        pay_or_receive: Union[PayReceive, str],
        termination_date: Union[Union[datetime.date, str], str],
        notional_currency: Union[Currency, str],
        notional_amount: float = 1000000.0,
        effective_date: Union[Union[datetime.date, str], str] = None,
        floating_rate_for_the_initial_calculation_period: float = None,
        floating_rate_option: str = None,
        floating_rate_designated_maturity: str = None,
        floating_rate_spread: float = None,
        floating_rate_frequency: str = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate: Union[float, str] = None,
        fixed_rate_frequency: str = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0,
        clearing_house: Union[SwapClearingHouse, str] = None        
    ):
        super().__init__()
        self.__pay_or_receive = get_enum_value(PayReceive, pay_or_receive)
        self.__termination_date = termination_date
        self.__notional_currency = get_enum_value(Currency, notional_currency)
        self.__notional_amount = notional_amount
        self.__effective_date = effective_date
        self.__floating_rate_for_the_initial_calculation_period = floating_rate_for_the_initial_calculation_period
        self.__floating_rate_option = floating_rate_option
        self.__floating_rate_designated_maturity = floating_rate_designated_maturity
        self.__floating_rate_spread = floating_rate_spread
        self.__floating_rate_frequency = floating_rate_frequency
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, floating_rate_day_count_fraction)
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, floating_rate_business_day_convention)
        self.__fixed_rate = fixed_rate
        self.__fixed_rate_frequency = fixed_rate_frequency
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, fixed_rate_day_count_fraction)
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, fixed_rate_business_day_convention)
        self.__fee = fee
        self.__clearing_house = get_enum_value(SwapClearingHouse, clearing_house)

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
        self.__pay_or_receive = value if isinstance(value, PayReceive) else get_enum_value(PayReceive, value)
        self._property_changed('pay_or_receive')        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self.__termination_date = value
        self._property_changed('termination_date')        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self.__notional_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notional_currency')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def floating_rate_for_the_initial_calculation_period(self) -> float:
        """First fixing"""
        return self.__floating_rate_for_the_initial_calculation_period

    @floating_rate_for_the_initial_calculation_period.setter
    def floating_rate_for_the_initial_calculation_period(self, value: float):
        self.__floating_rate_for_the_initial_calculation_period = value
        self._property_changed('floating_rate_for_the_initial_calculation_period')        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self.__floating_rate_option = value
        self._property_changed('floating_rate_option')        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor of the floatingRateOption, e.g. 3m, 6m"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self.__floating_rate_designated_maturity = value
        self._property_changed('floating_rate_designated_maturity')        

    @property
    def floating_rate_spread(self) -> float:
        """The spread over the floating rate"""
        return self.__floating_rate_spread

    @floating_rate_spread.setter
    def floating_rate_spread(self, value: float):
        self.__floating_rate_spread = value
        self._property_changed('floating_rate_spread')        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self.__floating_rate_frequency = value
        self._property_changed('floating_rate_frequency')        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__floating_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floating_rate_day_count_fraction')        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__floating_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floating_rate_business_day_convention')        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self.__fixed_rate = value
        self._property_changed('fixed_rate')        

    @property
    def fixed_rate_frequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: str):
        self.__fixed_rate_frequency = value
        self._property_changed('fixed_rate_frequency')        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__fixed_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('fixed_rate_day_count_fraction')        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__fixed_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('fixed_rate_business_day_convention')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self.__clearing_house = value if isinstance(value, SwapClearingHouse) else get_enum_value(SwapClearingHouse, value)
        self._property_changed('clearing_house')        


class IRSwaption(Instrument):
        
    """Object representation of a swaption"""
       
    def __init__(
        self,
        pay_or_receive: str,
        termination_date: Union[Union[datetime.date, str], str],
        notional_currency: Union[Currency, str],
        effective_date: Union[Union[datetime.date, str], str] = None,
        notional_amount: float = 1000000.0,
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
        premium: float = 0,
        fee: float = 0,
        clearing_house: Union[SwapClearingHouse, str] = None,
        settlement: Union[SwapSettlement, str] = None,
        premium_payment_date: Union[datetime.date, str] = None        
    ):
        super().__init__()
        self.__pay_or_receive = pay_or_receive
        self.__effective_date = effective_date
        self.__termination_date = termination_date
        self.__notional_currency = get_enum_value(Currency, notional_currency)
        self.__notional_amount = notional_amount
        self.__expiration_date = expiration_date
        self.__floating_rate_option = floating_rate_option
        self.__floating_rate_designated_maturity = floating_rate_designated_maturity
        self.__floating_rate_spread = floating_rate_spread
        self.__floating_rate_frequency = floating_rate_frequency
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, floating_rate_day_count_fraction)
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, floating_rate_business_day_convention)
        self.__fixed_rate_frequency = fixed_rate_frequency
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, fixed_rate_day_count_fraction)
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, fixed_rate_business_day_convention)
        self.__strike = strike
        self.__premium = premium
        self.__fee = fee
        self.__clearing_house = get_enum_value(SwapClearingHouse, clearing_house)
        self.__settlement = get_enum_value(SwapSettlement, settlement)
        self.__premium_payment_date = premium_payment_date

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
        self.__pay_or_receive = value
        self._property_changed('pay_or_receive')        

    @property
    def effective_date(self) -> Union[Union[datetime.date, str], str]:
        """Swaption effective date, e.g. 2019-01-01, 10y"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[Union[datetime.date, str], str]):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def termination_date(self) -> Union[Union[datetime.date, str], str]:
        """Swaption termination date, e.g. 2030-05-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[Union[datetime.date, str], str]):
        self.__termination_date = value
        self._property_changed('termination_date')        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self.__notional_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notional_currency')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def expiration_date(self) -> Union[Union[datetime.date, str], str]:
        """Swaption expiration date, 2020-05-01, 3m"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Union[Union[datetime.date, str], str]):
        self.__expiration_date = value
        self._property_changed('expiration_date')        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-TELERATE"""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self.__floating_rate_option = value
        self._property_changed('floating_rate_option')        

    @property
    def floating_rate_designated_maturity(self) -> str:
        """Tenor"""
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: str):
        self.__floating_rate_designated_maturity = value
        self._property_changed('floating_rate_designated_maturity')        

    @property
    def floating_rate_spread(self) -> float:
        """The spread over the floating rate"""
        return self.__floating_rate_spread

    @floating_rate_spread.setter
    def floating_rate_spread(self, value: float):
        self.__floating_rate_spread = value
        self._property_changed('floating_rate_spread')        

    @property
    def floating_rate_frequency(self) -> str:
        """The frequency of floating payments, e.g. 3m"""
        return self.__floating_rate_frequency

    @floating_rate_frequency.setter
    def floating_rate_frequency(self, value: str):
        self.__floating_rate_frequency = value
        self._property_changed('floating_rate_frequency')        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction of the floating rate"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__floating_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('floating_rate_day_count_fraction')        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__floating_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floating_rate_business_day_convention')        

    @property
    def fixed_rate_frequency(self) -> str:
        """The frequency of fixed payments, e.g. 6m"""
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: str):
        self.__fixed_rate_frequency = value
        self._property_changed('fixed_rate_frequency')        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """The day count fraction for the fixed rate"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self.__fixed_rate_day_count_fraction = value if isinstance(value, DayCountFraction) else get_enum_value(DayCountFraction, value)
        self._property_changed('fixed_rate_day_count_fraction')        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__fixed_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('fixed_rate_business_day_convention')        

    @property
    def strike(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__strike

    @strike.setter
    def strike(self, value: Union[float, str]):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def premium(self) -> float:
        """The premium"""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        

    @property
    def clearing_house(self) -> Union[SwapClearingHouse, str]:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: Union[SwapClearingHouse, str]):
        self.__clearing_house = value if isinstance(value, SwapClearingHouse) else get_enum_value(SwapClearingHouse, value)
        self._property_changed('clearing_house')        

    @property
    def settlement(self) -> Union[SwapSettlement, str]:
        """Swap Settlement Type"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: Union[SwapSettlement, str]):
        self.__settlement = value if isinstance(value, SwapSettlement) else get_enum_value(SwapSettlement, value)
        self._property_changed('settlement')        

    @property
    def premium_payment_date(self) -> Union[datetime.date, str]:
        """Date or tenor, e.g. 2018-09-03, 3m"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: Union[datetime.date, str]):
        self.__premium_payment_date = value
        self._property_changed('premium_payment_date')        


class InflationSwap(Instrument):
        
    """A vanilla inflation swap of fixed vs floating cashflows adjusted to an inflation rate"""
       
    def __init__(
        self,
        termination_date: Union[datetime.date, str],
        pay_or_receive: Union[PayReceive, str] = None,
        notional_currency: Union[Currency, str] = None,
        notional_amount: float = 1000000.0,
        effective_date: Union[datetime.date, str] = None,
        index: str = None,
        floating_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fixed_rate: Union[float, str] = None,
        fixed_rate_business_day_convention: Union[BusinessDayConvention, str] = None,
        fee: float = 0        
    ):
        super().__init__()
        self.__pay_or_receive = get_enum_value(PayReceive, pay_or_receive)
        self.__termination_date = termination_date
        self.__notional_currency = get_enum_value(Currency, notional_currency)
        self.__notional_amount = notional_amount
        self.__effective_date = effective_date
        self.__index = index
        self.__floating_rate_business_day_convention = get_enum_value(BusinessDayConvention, floating_rate_business_day_convention)
        self.__fixed_rate = fixed_rate
        self.__fixed_rate_business_day_convention = get_enum_value(BusinessDayConvention, fixed_rate_business_day_convention)
        self.__fee = fee

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
        self.__pay_or_receive = value if isinstance(value, PayReceive) else get_enum_value(PayReceive, value)
        self._property_changed('pay_or_receive')        

    @property
    def termination_date(self) -> Union[datetime.date, str]:
        """The termination of the swap, e.g. 2050-04-01, 10y"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: Union[datetime.date, str]):
        self.__termination_date = value
        self._property_changed('termination_date')        

    @property
    def notional_currency(self) -> Union[Currency, str]:
        """Notional currency"""
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: Union[Currency, str]):
        self.__notional_currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('notional_currency')        

    @property
    def notional_amount(self) -> float:
        """Notional amount"""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self.__notional_amount = value
        self._property_changed('notional_amount')        

    @property
    def effective_date(self) -> Union[datetime.date, str]:
        """The date on which the swap becomes effective"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: Union[datetime.date, str]):
        self.__effective_date = value
        self._property_changed('effective_date')        

    @property
    def index(self) -> str:
        """The underlying benchmark for the floating rate, e.g. CPI-U"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self.__index = value
        self._property_changed('index')        

    @property
    def floating_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention of the floating rate"""
        return self.__floating_rate_business_day_convention

    @floating_rate_business_day_convention.setter
    def floating_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__floating_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('floating_rate_business_day_convention')        

    @property
    def fixed_rate(self) -> Union[float, str]:
        """The coupon of the fixed leg"""
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: Union[float, str]):
        self.__fixed_rate = value
        self._property_changed('fixed_rate')        

    @property
    def fixed_rate_business_day_convention(self) -> Union[BusinessDayConvention, str]:
        """The business day convention for the fixed rate"""
        return self.__fixed_rate_business_day_convention

    @fixed_rate_business_day_convention.setter
    def fixed_rate_business_day_convention(self, value: Union[BusinessDayConvention, str]):
        self.__fixed_rate_business_day_convention = value if isinstance(value, BusinessDayConvention) else get_enum_value(BusinessDayConvention, value)
        self._property_changed('fixed_rate_business_day_convention')        

    @property
    def fee(self) -> float:
        """The fee"""
        return self.__fee

    @fee.setter
    def fee(self, value: float):
        self.__fee = value
        self._property_changed('fee')        
