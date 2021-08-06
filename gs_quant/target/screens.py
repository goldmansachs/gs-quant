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

from gs_quant.common import (AssetScreenerRequestFilterLimits, AssetScreenerRequestFilterDateLimits,
                             AssetScreenerCreditStandardAndPoorsRatingOptions, Entitlements)
import datetime
from typing import Tuple
from gs_quant.base import Base, camel_case_translate


class ScreenParameters(Base):
    """Filters for credit asset screener in saved screen."""

    @camel_case_translate
    def __init__(
            self,
            face_value: float = None,
            direction: str = None,
            currency: Tuple[str, ...] = None,
            gs_liquidity_score: AssetScreenerRequestFilterLimits = None,
            gs_charge_bps: AssetScreenerRequestFilterLimits = None,
            gs_charge_dollars: AssetScreenerRequestFilterLimits = None,
            modified_duration: AssetScreenerRequestFilterLimits = None,
            issue_date: AssetScreenerRequestFilterDateLimits = None,
            yield_to_convention: AssetScreenerRequestFilterLimits = None,
            spread_to_benchmark: AssetScreenerRequestFilterLimits = None,
            z_spread: AssetScreenerRequestFilterLimits = None,
            g_spread: AssetScreenerRequestFilterLimits = None,
            bval_mid_price: AssetScreenerRequestFilterLimits = None,
            maturity: AssetScreenerRequestFilterLimits = None,
            amount_outstanding: AssetScreenerRequestFilterLimits = None,
            rating_standard_and_poors: AssetScreenerCreditStandardAndPoorsRatingOptions = None,
            seniority: Tuple[str, ...] = None,
            sector: Tuple[str, ...] = None,
            name: str = None
    ):
        super().__init__()
        self.face_value = face_value
        self.direction = direction
        self.currency = currency
        self.gs_liquidity_score = gs_liquidity_score
        self.gs_charge_bps = gs_charge_bps
        self.gs_charge_dollars = gs_charge_dollars
        self.modified_duration = modified_duration
        self.issue_date = issue_date
        self.yield_to_convention = yield_to_convention
        self.spread_to_benchmark = spread_to_benchmark
        self.z_spread = z_spread
        self.g_spread = g_spread
        self.bval_mid_price = bval_mid_price
        self.maturity = maturity
        self.amount_outstanding = amount_outstanding
        self.rating_standard_and_poors = rating_standard_and_poors
        self.seniority = seniority
        self.sector = sector
        self.name = name

    @property
    def face_value(self) -> float:
        """Face value of the bonds in universe."""
        return self.__face_value

    @face_value.setter
    def face_value(self, value: float):
        self._property_changed('face_value')
        self.__face_value = value

    @property
    def direction(self) -> str:
        """Whether the bonds are a buy or sell."""
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self._property_changed('direction')
        self.__direction = value

    @property
    def currency(self) -> Tuple[str, ...]:
        """Currency of bonds in the universe."""
        return self.__currency

    @currency.setter
    def currency(self, value: Tuple[str, ...]):
        self._property_changed('currency')
        self.__currency = value

    @property
    def gs_liquidity_score(self) -> AssetScreenerRequestFilterLimits:
        """Liquidity score assigned to buying/selling the bond."""
        return self.__gs_liquidity_score

    @gs_liquidity_score.setter
    def gs_liquidity_score(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('gs_liquidity_score')
        self.__gs_liquidity_score = value

    @property
    def gs_charge_bps(self) -> AssetScreenerRequestFilterLimits:
        """Goldman Sachs' indicative charge of the bond (bps)."""
        return self.__gs_charge_bps

    @gs_charge_bps.setter
    def gs_charge_bps(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('gs_charge_bps')
        self.__gs_charge_bps = value

    @property
    def gs_charge_dollars(self) -> AssetScreenerRequestFilterLimits:
        """Goldman Sachs' indicative charge of the bond (dollars)."""
        return self.__gs_charge_dollars

    @gs_charge_dollars.setter
    def gs_charge_dollars(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('gs_charge_dollars')
        self.__gs_charge_dollars = value

    @property
    def modified_duration(self) -> AssetScreenerRequestFilterLimits:
        """Measure of a bond's price sensitivity to changes in interest rates."""
        return self.__modified_duration

    @modified_duration.setter
    def modified_duration(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('modified_duration')
        self.__modified_duration = value

    @property
    def issue_date(self) -> AssetScreenerRequestFilterDateLimits:
        """Issue date of the instrument."""
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: AssetScreenerRequestFilterDateLimits):
        self._property_changed('issue_date')
        self.__issue_date = value

    @property
    def yield_to_convention(self) -> AssetScreenerRequestFilterLimits:
        """Return an investor realizes on a bond sold at the mid price."""
        return self.__yield_to_convention

    @yield_to_convention.setter
    def yield_to_convention(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('yield_to_convention')
        self.__yield_to_convention = value

    @property
    def spread_to_benchmark(self) -> AssetScreenerRequestFilterLimits:
        """Spread between the yields of a debt security and its benchmark when both are
           purchased at bid price."""
        return self.__spread_to_benchmark

    @spread_to_benchmark.setter
    def spread_to_benchmark(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('spread_to_benchmark')
        self.__spread_to_benchmark = value

    @property
    def z_spread(self) -> AssetScreenerRequestFilterLimits:
        """Zero volatility spread of a bond."""
        return self.__z_spread

    @z_spread.setter
    def z_spread(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('z_spread')
        self.__z_spread = value

    @property
    def g_spread(self) -> AssetScreenerRequestFilterLimits:
        """Difference between yield on treasury bonds and yield on corporate bonds of same
           maturity."""
        return self.__g_spread

    @g_spread.setter
    def g_spread(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('g_spread')
        self.__g_spread = value

    @property
    def bval_mid_price(self) -> AssetScreenerRequestFilterLimits:
        """BVAL mid price."""
        return self.__bval_mid_price

    @bval_mid_price.setter
    def bval_mid_price(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('bval_mid_price')
        self.__bval_mid_price = value

    @property
    def maturity(self) -> AssetScreenerRequestFilterLimits:
        """Length of time bond owner will receive interest payments on the investment."""
        return self.__maturity

    @maturity.setter
    def maturity(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('maturity')
        self.__maturity = value

    @property
    def amount_outstanding(self) -> AssetScreenerRequestFilterLimits:
        """Aggregate principal amount of the total number of bonds not redeemed or
           otherwise discharged."""
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value

    @property
    def rating_standard_and_poors(self) -> AssetScreenerCreditStandardAndPoorsRatingOptions:
        """S&P rating given to a bond."""
        return self.__rating_standard_and_poors

    @rating_standard_and_poors.setter
    def rating_standard_and_poors(self, value: AssetScreenerCreditStandardAndPoorsRatingOptions):
        self._property_changed('rating_standard_and_poors')
        self.__rating_standard_and_poors = value

    @property
    def seniority(self) -> Tuple[str, ...]:
        """Seniority of the bond."""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: Tuple[str, ...]):
        self._property_changed('seniority')
        self.__seniority = value

    @property
    def sector(self) -> Tuple[str, ...]:
        """Sector / industry of the bond."""
        return self.__sector

    @sector.setter
    def sector(self, value: Tuple[str, ...]):
        self._property_changed('sector')
        self.__sector = value


class Screen(Base):
    """Object representation of a Screen"""

    @camel_case_translate
    def __init__(
            self,
            name: str,
            parameters: ScreenParameters,
            id_: str = None,
            active: bool = None,
            owner_id: str = None,
            created_by_id: str = None,
            created_time: datetime.datetime = None,
            last_updated_by_id: str = None,
            last_updated_time: datetime.datetime = None,
            entitlements: Entitlements = None
    ):
        super().__init__()
        self.__id = id_
        self.active = active
        self.owner_id = owner_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.entitlements = entitlements
        self.name = name
        self.parameters = parameters

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        self._property_changed('active')
        self.__active = value

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value

    @property
    def name(self) -> str:
        """Display name of the screen"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value

    @property
    def parameters(self) -> ScreenParameters:
        """The parameters used in the screen."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ScreenParameters):
        self._property_changed('parameters')
        self.__parameters = value
