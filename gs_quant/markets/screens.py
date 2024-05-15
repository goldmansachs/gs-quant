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
import logging
from datetime import date
from enum import Enum, unique
from typing import Union, Tuple

from pandas import DataFrame
from pydash import set_, get

from gs_quant.api.gs.screens import GsScreenApi
from gs_quant.errors import MqValueError
from gs_quant.target.assets_screener import AssetScreenerCreditRequestFilters, AssetScreenerRequest, \
    AssetScreenerRequestFilterLimits, AssetScreenerRequestStringOptions
from gs_quant.target.screens import Screen as TargetScreen, ScreenParameters as TargetScreenParameters
from gs_quant.common import Currency as CurrencyImport

logging.root.setLevel('INFO')


class RangeFilter:
    """ Respresents asset filters that are ranges """

    def __init__(self, min_: Union[float, str] = None, max_: Union[float, str] = None):
        self.__min = min_
        self.__max = max_

    def __str__(self) -> str:
        range_filter = f'{{Min: {self.min}, Max: {self.max}}}'
        return range_filter

    @property
    def min(self) -> Union[float, str]:
        return self.__min

    @min.setter
    def min(self, value: Union[float, str]):
        self.__min = value

    @property
    def max(self) -> Union[float, str]:
        return self.__max

    @max.setter
    def max(self, value: Union[float, str]):
        self.__max = value


@unique
class CheckboxType(Enum):
    INCLUDE = "Include"
    EXCLUDE = "Exclude"


@unique
class Sector(Enum):
    COMMUNICATION_SERVICES = "Communication Services"
    CONSUMER_DISCRETIONARY = "Consumer Discretionary"
    CONSUMER_STAPLES = "Consumer Staples"
    ENERGY = "Energy"
    FINANCIALS = "Financials"
    HEALTH_CARE = "Health Care"
    INDUSTRIALS = "Industrials"
    INFORMATION_TECHNOLOGY = "Information Technology"
    MATERIALS = "Materials"
    REAL_ESTATE = "Real Estate"
    UTILITIES = "Utilities"


@unique
class Seniority(Enum):
    JUNIOR_SUBORDINATE = "Junior Subordinate"
    SENIOR = "Senior"
    SENIOR_SUBORDINATE = "Senior Subordinate"
    SUBORDINATE = "Subordinate"


@unique
class Direction(Enum):
    BUY = "Buy"
    SELL = "Sell"


@unique
class Currency(CurrencyImport, Enum):
    pass


class CheckboxFilter:
    """ Represents asset filters that have multiple enumerated options"""

    def __init__(self, checkbox_type: CheckboxType = None, selections: Tuple[Enum, ...] = None):
        self.__selections = selections
        self.__checkbox_type = checkbox_type

    def __str__(self) -> str:
        checkbox_filter = f'{{Type: {self.checkbox_type}, Selections: {self.selections}}}'
        return checkbox_filter

    @property
    def checkbox_type(self) -> CheckboxType:
        return self.__checkbox_type

    @checkbox_type.setter
    def checkbox_type(self, value: CheckboxType):
        self.__checkbox_type = value

    @property
    def selections(self) -> Tuple[Enum, ...]:
        return self.__selections

    @selections.setter
    def selections(self, value: Tuple[Enum, ...]):
        self.__selections = value

    def add(self, new_selections: Tuple[Enum, ...]):
        new_selections = set(new_selections)
        old_selections = set(self.selections)
        self.selections = tuple(set(new_selections).union(set(old_selections)))

    def remove(self, remove_selections: Tuple[Enum, ...]):
        remove_selections = set(remove_selections)
        old_selections = set(self.selections)
        self.selections = tuple(old_selections.difference(remove_selections))


class ScreenFilters:
    def __init__(self,
                 face_value: float = 1000000,
                 direction: str = "Buy",
                 liquidity_score: RangeFilter = RangeFilter(),
                 gs_charge_bps: RangeFilter = RangeFilter(),
                 gs_charge_dollars: RangeFilter = RangeFilter(),
                 duration: RangeFilter = RangeFilter(),
                 yield_: RangeFilter = RangeFilter(),
                 spread: RangeFilter = RangeFilter(),
                 z_spread: RangeFilter = RangeFilter(),
                 g_spread: RangeFilter = RangeFilter(),
                 mid_price: RangeFilter = RangeFilter(),
                 maturity: RangeFilter = RangeFilter(),
                 amount_outstanding: RangeFilter = RangeFilter(),
                 letter_rating: RangeFilter = RangeFilter(),
                 seniority: CheckboxFilter = CheckboxFilter(),
                 currency: CheckboxFilter = CheckboxFilter(),
                 sector: CheckboxFilter = CheckboxFilter()):
        self.__face_value = face_value
        self.__direction = direction
        self.__liquidity_score = liquidity_score
        self.__gs_charge_bps = gs_charge_bps
        self.__gs_charge_dollars = gs_charge_dollars
        self.__duration = duration
        self.__yield_ = yield_
        self.__spread = spread
        self.__z_spread = z_spread
        self.__g_spread = g_spread
        self.__mid_price = mid_price
        self.__maturity = maturity
        self.__amount_outstanding = amount_outstanding
        self.__rating = letter_rating
        self.__seniority = seniority
        self.__currency = currency
        self.__sector = sector

    def __str__(self) -> str:
        to_return = {}
        filter_names = self.__dict__.keys()
        for name in filter_names:
            if self.__dict__[name]:
                to_return[name] = self.__dict__[name].__str__()
        return str(to_return)

    @property
    def face_value(self) -> float:
        """Face value of the bond."""
        return self.__face_value

    @face_value.setter
    def face_value(self, value: float):
        self.__face_value = value

    @property
    def direction(self) -> str:
        """Whether the position is a buy or sell."""
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self.__direction = value

    @property
    def liquidity_score(self) -> RangeFilter:
        """Liquidity score assigned to buying/selling the bond."""
        return self.__liquidity_score

    @liquidity_score.setter
    def liquidity_score(self, value: RangeFilter):
        self.__validate_range_settings(min_=1, max_=6, value=self.__liquidity_score)
        self.__liquidity_score = value

    @property
    def gs_charge_bps(self) -> RangeFilter:
        """Goldman Sachs' indicative charge of the bond (bps)."""
        return self.__gs_charge_bps

    @gs_charge_bps.setter
    def gs_charge_bps(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=10, value=self.__gs_charge_bps)
        self.__gs_charge_bps = value

    @property
    def gs_charge_dollars(self) -> RangeFilter:
        """Goldman Sachs' indicative charge of the bond (dollars)."""
        return self.__gs_charge_dollars

    @gs_charge_dollars.setter
    def gs_charge_dollars(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=2, value=self.__gs_charge_dollars)
        self.__gs_charge_dollars = value

    @property
    def duration(self) -> RangeFilter:
        """Measure of a bond's price sensitivity to changes in interest rates."""
        return self.__duration

    @duration.setter
    def duration(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=20, value=self.__duration)
        self.__duration = value

    @property
    def yield_(self) -> RangeFilter:
        """Return an investor realizes on a bond sold at the mid price."""
        return self.__yield_

    @yield_.setter
    def yield_(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=10, value=self.__yield_)
        self.__yield_ = value

    @property
    def spread(self) -> RangeFilter:
        """Spread between the yields of a debt security and its benchmark when both are
           purchased at bid price."""
        return self.__spread

    @spread.setter
    def spread(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=1000, value=self.__spread)
        self.__spread = value

    @property
    def z_spread(self) -> RangeFilter:
        """Zero volatility spread of a bond."""
        return self.__z_spread

    @z_spread.setter
    def z_spread(self, value: RangeFilter):
        self.__z_spread = value

    @property
    def g_spread(self) -> RangeFilter:
        """Difference between yield on treasury bonds and yield on corporate bonds of same
           maturity."""
        return self.__g_spread

    @g_spread.setter
    def g_spread(self, value: RangeFilter):
        self.__g_spread = value

    @property
    def mid_price(self) -> RangeFilter:
        """Mid price."""
        return self.__mid_price

    @mid_price.setter
    def mid_price(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=200, value=self.__mid_price)
        self.__mid_price = value

    @property
    def maturity(self) -> RangeFilter:
        """Length of time bond owner will receive interest payments on the investment."""
        return self.__maturity

    @maturity.setter
    def maturity(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=40, value=self.__maturity)
        self.__maturity = value

    @property
    def amount_outstanding(self) -> RangeFilter:
        """Aggregate principal amount of the total number of bonds not redeemed or
           otherwise discharged."""
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: RangeFilter):
        self.__validate_range_settings(min_=0, max_=1000000000, value=self.__amount_outstanding)
        self.__amount_outstanding = value

    @property
    def rating(self) -> RangeFilter:
        """S&P rating given to a bond."""
        return self.__rating

    @rating.setter
    def rating(self, value: RangeFilter):
        self.__rating = value

    @property
    def seniority(self) -> CheckboxFilter:
        """Seniority of the bond."""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: CheckboxFilter):
        self.__seniority = value

    @property
    def currency(self) -> CheckboxFilter:
        """Currency of the bond."""
        return self.__currency

    @currency.setter
    def currency(self, value: CheckboxFilter):
        self.__currency = value

    @property
    def sector(self) -> CheckboxFilter:
        """Sector / industry of the bond."""
        return self.__sector

    @sector.setter
    def sector(self, value: CheckboxFilter):
        self.__sector = value

    @staticmethod
    def __validate_range_settings(min_: int, max_: int, value: RangeFilter):
        if value.min is None and value.max is None:
            return
        if value.min < min_ or value.max > max_:
            raise MqValueError(f'Please ensure your min and max values are in the range of {min} <= x <= {max}')


class Screen:
    """"Private variables"""

    def __init__(self, filters: ScreenFilters = None, screen_id: str = None, name: str = None):
        if not filters:
            self.__filters = ScreenFilters()
        else:
            self.__filters = filters

        self.__id = screen_id
        self.__name = name if name is not None else f"Screen {date.today().strftime('%d-%b-%Y')}"

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def filters(self) -> ScreenFilters:
        return self.__filters

    @filters.setter
    def filters(self, filters: ScreenFilters):
        self.__filters = filters

    @classmethod
    def get(cls, screen_id: str):
        screen = GsScreenApi.get_screen(screen_id=screen_id)
        return Screen.__from_target(screen)

    def calculate(self, format_: str = None):
        """ Applies screen filters, returning assets that satisfy the condition(s) """
        filters = self.__to_target_filters()
        payload = AssetScreenerRequest(filters=filters)
        assets = GsScreenApi.calculate(payload)
        dataframe = DataFrame(assets)
        if format_ == 'json':
            return dataframe['results'].to_json(indent=4)
        if format_ == 'csv':
            return dataframe.to_csv()
        return dataframe

    def save(self):
        """ Create a screen using GsScreenApi if it doesn't exist. Update the report if it does. """
        parameters = self.__to_target_parameters()
        target_screen = TargetScreen(name=self.name, parameters=parameters)
        if self.id:
            target_screen.id = self.id
            GsScreenApi.update_screen(target_screen)
        else:
            screen = GsScreenApi.create_screen(target_screen)
            self.__id = screen.id
            logging.info(f'New screen created with ID: {self.id} \n')

    def delete(self):
        """ Hits GsScreensApi to delete a report """
        GsScreenApi.delete_screen(self.id)

    @classmethod
    def __from_target(cls, screen):
        return Screen(filters=screen.parameters, screen_id=screen.id, name=screen.name)

    def __to_target_filters(self) -> AssetScreenerCreditRequestFilters:
        payload = {}
        filters = self.__set_up_filters()

        for name in filters:
            if name == 'face_value' or name == 'direction':
                payload[name] = filters[name]
            elif isinstance(filters[name], RangeFilter):
                payload[name] = AssetScreenerRequestFilterLimits(min_=filters[name].min, max_=filters[name].max)
            elif isinstance(filters[name], CheckboxFilter):
                if filters[name].selections and filters[name].checkbox_type:
                    payload[name] = AssetScreenerRequestStringOptions(options=filters[name].selections,
                                                                      type_=filters[name].checkbox_type)
        return AssetScreenerCreditRequestFilters(**payload)

    def __set_up_filters(self) -> dict:
        filters = {}
        for prop in AssetScreenerCreditRequestFilters.properties():
            set_(filters, prop, get(self.__filters, prop))
        return filters

    def __to_target_parameters(self) -> TargetScreenParameters:
        payload = {}
        parameters = self.__set_up_parameters()

        for name in parameters:
            if name == 'face_value' or name == 'direction':
                payload[name] = parameters[name]
            elif isinstance(parameters[name], RangeFilter):
                payload[name] = AssetScreenerRequestFilterLimits(min_=parameters[name].min, max_=parameters[name].max)
            elif isinstance(parameters[name], CheckboxFilter):
                if parameters[name].selections and parameters[name].checkbox_type:
                    payload[name] = parameters[name].selections
        return TargetScreenParameters(**payload)

    def __set_up_parameters(self) -> dict:
        filter_to_parameter = {'face_value': 'face_value', 'direction': 'direction',
                               'gs_liquidity_score': 'liquidity_score', 'gs_charge_bps': 'gs_charge_bps',
                               'gs_charge_dollars': 'gs_charge_dollars', 'modified_duration': 'duration',
                               'yield_to_convention': 'yield_', 'spread_to_benchmark': 'spread', 'z_spread': 'z_spread',
                               'g_spread': 'g_spread', 'bval_mid_price': 'mid_price', 'maturity': 'maturity',
                               'amount_outstanding': 'amount_outstanding', 'rating_standard_and_poors': 'rating',
                               'seniority': 'seniority', 'currency': 'currency', 'sector': 'sector',
                               'issue_date': 'issue_date'}

        parameters = {}
        for prop in TargetScreenParameters.properties():
            set_(parameters, prop, get(self.__filters, filter_to_parameter[prop]))
        return parameters
