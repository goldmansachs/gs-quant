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

from enum import Enum
from gs_quant.base import Base, EnumBase, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class SortByTerm(EnumBase, Enum):    
    
    """Term to sort risk models by."""

    Short = 'Short'
    Medium = 'Medium'
    
    def __repr__(self):
        return self.value


class AdvCurveTick(Base):
               
    def __init__(
        self,
        date: datetime.date = None,
        value: float = None        
    ):
        super().__init__()
        self.__date = date
        self.__value = value

    @property
    def date(self) -> datetime.date:
        """Date of the tick in ISO 8601 format."""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self.__date = value
        self._property_changed('date')        

    @property
    def value(self) -> float:
        """Value of the advPct."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class CoordinatesRequest(Base):
               
    def __init__(
        self,
        as_of: datetime.date,
        instruments: Tuple[Priceable, ...]        
    ):
        super().__init__()
        self.__as_of = as_of
        self.__instruments = instruments

    @property
    def as_of(self) -> datetime.date:
        return self.__as_of

    @as_of.setter
    def as_of(self, value: datetime.date):
        self.__as_of = value
        self._property_changed('as_of')        

    @property
    def instruments(self) -> Tuple[Priceable, ...]:
        """Instrument or Id  
To specify a Marquee asset use the asset Id.
For listed products use an XRef, e.g. { 'bid': 'NGZ19 Comdty' }, { 'isin': 'US912810SD19' }.
To specify an instrument use one of the listed types"""
        return self.__instruments

    @instruments.setter
    def instruments(self, value: Tuple[Priceable, ...]):
        self.__instruments = value
        self._property_changed('instruments')        


class CoordinatesResponse(Base):
               
    def __init__(
        self,
        results: Tuple[MarketDataCoordinate, ...]        
    ):
        super().__init__()
        self.__results = results

    @property
    def results(self) -> Tuple[MarketDataCoordinate, ...]:
        """Object representation of a market data coordinate"""
        return self.__results

    @results.setter
    def results(self, value: Tuple[MarketDataCoordinate, ...]):
        self.__results = value
        self._property_changed('results')        


class ExecutionCostForHorizon(Base):
               
    def __init__(
        self,
        minutes_expired: int = None,
        execution_cost: float = None,
        execution_cost_long: float = None,
        execution_cost_short: float = None        
    ):
        super().__init__()
        self.__minutes_expired = minutes_expired
        self.__execution_cost = execution_cost
        self.__execution_cost_long = execution_cost_long
        self.__execution_cost_short = execution_cost_short

    @property
    def minutes_expired(self) -> int:
        """Exchange minutes taken to trade the set of positions."""
        return self.__minutes_expired

    @minutes_expired.setter
    def minutes_expired(self, value: int):
        self.__minutes_expired = value
        self._property_changed('minutes_expired')        

    @property
    def execution_cost(self) -> float:
        """Estimated transaction cost for the set of positions."""
        return self.__execution_cost

    @execution_cost.setter
    def execution_cost(self, value: float):
        self.__execution_cost = value
        self._property_changed('execution_cost')        

    @property
    def execution_cost_long(self) -> float:
        """Estimated transaction cost for the set of long positions."""
        return self.__execution_cost_long

    @execution_cost_long.setter
    def execution_cost_long(self, value: float):
        self.__execution_cost_long = value
        self._property_changed('execution_cost_long')        

    @property
    def execution_cost_short(self) -> float:
        """Estimated transaction cost for the set of short positions."""
        return self.__execution_cost_short

    @execution_cost_short.setter
    def execution_cost_short(self, value: float):
        self.__execution_cost_short = value
        self._property_changed('execution_cost_short')        


class LiquidityBucket(Base):
        
    """Positions bucketed by a certain characteristic."""
       
    def __init__(
        self,
        name: str = None,
        description: str = None,
        net_exposure: float = None,
        gross_exposure: float = None,
        net_weight: float = None,
        gross_weight: float = None,
        transaction_cost: float = None,
        marginal_cost: float = None,
        adv22_day_pct: float = None,
        number_of_positions: float = None,
        beta_adjusted_exposure: float = None,
        long_weight: float = None,
        long_exposure: float = None,
        long_transaction_cost: float = None,
        long_marginal_cost: float = None,
        long_adv22_day_pct: float = None,
        long_number_of_positions: float = None,
        long_beta_adjusted_exposure: float = None,
        short_weight: float = None,
        short_exposure: float = None,
        short_transaction_cost: float = None,
        short_marginal_cost: float = None,
        short_adv22_day_pct: float = None,
        short_number_of_positions: float = None,
        short_beta_adjusted_exposure: float = None        
    ):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__net_exposure = net_exposure
        self.__gross_exposure = gross_exposure
        self.__net_weight = net_weight
        self.__gross_weight = gross_weight
        self.__transaction_cost = transaction_cost
        self.__marginal_cost = marginal_cost
        self.__adv22_day_pct = adv22_day_pct
        self.__number_of_positions = number_of_positions
        self.__beta_adjusted_exposure = beta_adjusted_exposure
        self.__long_weight = long_weight
        self.__long_exposure = long_exposure
        self.__long_transaction_cost = long_transaction_cost
        self.__long_marginal_cost = long_marginal_cost
        self.__long_adv22_day_pct = long_adv22_day_pct
        self.__long_number_of_positions = long_number_of_positions
        self.__long_beta_adjusted_exposure = long_beta_adjusted_exposure
        self.__short_weight = short_weight
        self.__short_exposure = short_exposure
        self.__short_transaction_cost = short_transaction_cost
        self.__short_marginal_cost = short_marginal_cost
        self.__short_adv22_day_pct = short_adv22_day_pct
        self.__short_number_of_positions = short_number_of_positions
        self.__short_beta_adjusted_exposure = short_beta_adjusted_exposure

    @property
    def name(self) -> str:
        """Name of the bucket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def description(self) -> str:
        """A description of the bucket."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def net_exposure(self) -> float:
        """Net exposure of the constituent."""
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: float):
        self.__net_exposure = value
        self._property_changed('net_exposure')        

    @property
    def gross_exposure(self) -> float:
        """Gross exposure of the constituent."""
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: float):
        self.__gross_exposure = value
        self._property_changed('gross_exposure')        

    @property
    def net_weight(self) -> float:
        """Net weight of the constituent."""
        return self.__net_weight

    @net_weight.setter
    def net_weight(self, value: float):
        self.__net_weight = value
        self._property_changed('net_weight')        

    @property
    def gross_weight(self) -> float:
        """Gross weight of the constituent."""
        return self.__gross_weight

    @gross_weight.setter
    def gross_weight(self, value: float):
        self.__gross_weight = value
        self._property_changed('gross_weight')        

    @property
    def transaction_cost(self) -> float:
        """The average estimated transaction cost for the positions in the bucket."""
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self.__transaction_cost = value
        self._property_changed('transaction_cost')        

    @property
    def marginal_cost(self) -> float:
        """The average estimated transaction cost of the positions in this bucket multiplied by the bucket's gross weight in the portfolio."""
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: float):
        self.__marginal_cost = value
        self._property_changed('marginal_cost')        

    @property
    def adv22_day_pct(self) -> float:
        """The average 22 day ADV percent of the positions in the bucket."""
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value: float):
        self.__adv22_day_pct = value
        self._property_changed('adv22_day_pct')        

    @property
    def number_of_positions(self) -> float:
        """Number of positions in the bucket."""
        return self.__number_of_positions

    @number_of_positions.setter
    def number_of_positions(self, value: float):
        self.__number_of_positions = value
        self._property_changed('number_of_positions')        

    @property
    def beta_adjusted_exposure(self) -> float:
        """Net exposure of the positions in the bucket adjusted by the beta."""
        return self.__beta_adjusted_exposure

    @beta_adjusted_exposure.setter
    def beta_adjusted_exposure(self, value: float):
        self.__beta_adjusted_exposure = value
        self._property_changed('beta_adjusted_exposure')        

    @property
    def long_weight(self) -> float:
        """Gross weight of the long positions in the bucket."""
        return self.__long_weight

    @long_weight.setter
    def long_weight(self, value: float):
        self.__long_weight = value
        self._property_changed('long_weight')        

    @property
    def long_exposure(self) -> float:
        """Long exposure of the positions in the bucket."""
        return self.__long_exposure

    @long_exposure.setter
    def long_exposure(self, value: float):
        self.__long_exposure = value
        self._property_changed('long_exposure')        

    @property
    def long_transaction_cost(self) -> float:
        """The average estimated transaction cost of the long positions in the bucket."""
        return self.__long_transaction_cost

    @long_transaction_cost.setter
    def long_transaction_cost(self, value: float):
        self.__long_transaction_cost = value
        self._property_changed('long_transaction_cost')        

    @property
    def long_marginal_cost(self) -> float:
        """The estimated transaction cost of the long positions in this bucket multiplied by the sum of these positions' normalized weight with respect to all long positions in the portfolio."""
        return self.__long_marginal_cost

    @long_marginal_cost.setter
    def long_marginal_cost(self, value: float):
        self.__long_marginal_cost = value
        self._property_changed('long_marginal_cost')        

    @property
    def long_adv22_day_pct(self) -> float:
        """The average 22 day ADV percent of the long positions in the bucket."""
        return self.__long_adv22_day_pct

    @long_adv22_day_pct.setter
    def long_adv22_day_pct(self, value: float):
        self.__long_adv22_day_pct = value
        self._property_changed('long_adv22_day_pct')        

    @property
    def long_number_of_positions(self) -> float:
        """Number of long positions in the bucket."""
        return self.__long_number_of_positions

    @long_number_of_positions.setter
    def long_number_of_positions(self, value: float):
        self.__long_number_of_positions = value
        self._property_changed('long_number_of_positions')        

    @property
    def long_beta_adjusted_exposure(self) -> float:
        """Long exposure of the positions in the bucket adjusted by the beta."""
        return self.__long_beta_adjusted_exposure

    @long_beta_adjusted_exposure.setter
    def long_beta_adjusted_exposure(self, value: float):
        self.__long_beta_adjusted_exposure = value
        self._property_changed('long_beta_adjusted_exposure')        

    @property
    def short_weight(self) -> float:
        """Gross weight of the short positions in the bucket."""
        return self.__short_weight

    @short_weight.setter
    def short_weight(self, value: float):
        self.__short_weight = value
        self._property_changed('short_weight')        

    @property
    def short_exposure(self) -> float:
        """Short exposure of the positions in the bucket."""
        return self.__short_exposure

    @short_exposure.setter
    def short_exposure(self, value: float):
        self.__short_exposure = value
        self._property_changed('short_exposure')        

    @property
    def short_transaction_cost(self) -> float:
        """The average estimated transaction cost of the long positions in the bucket."""
        return self.__short_transaction_cost

    @short_transaction_cost.setter
    def short_transaction_cost(self, value: float):
        self.__short_transaction_cost = value
        self._property_changed('short_transaction_cost')        

    @property
    def short_marginal_cost(self) -> float:
        """The estimated transaction cost of the short positions in this bucket multiplied by the sum of these positions' normalized weight with respect to all short positions in the portfolio."""
        return self.__short_marginal_cost

    @short_marginal_cost.setter
    def short_marginal_cost(self, value: float):
        self.__short_marginal_cost = value
        self._property_changed('short_marginal_cost')        

    @property
    def short_adv22_day_pct(self) -> float:
        """The average 22 day ADV percent of the short positions in the bucket."""
        return self.__short_adv22_day_pct

    @short_adv22_day_pct.setter
    def short_adv22_day_pct(self, value: float):
        self.__short_adv22_day_pct = value
        self._property_changed('short_adv22_day_pct')        

    @property
    def short_number_of_positions(self) -> float:
        """Number of short positions in the bucket."""
        return self.__short_number_of_positions

    @short_number_of_positions.setter
    def short_number_of_positions(self, value: float):
        self.__short_number_of_positions = value
        self._property_changed('short_number_of_positions')        

    @property
    def short_beta_adjusted_exposure(self) -> float:
        """Short exposure of the positions in the bucket adjusted by the beta."""
        return self.__short_beta_adjusted_exposure

    @short_beta_adjusted_exposure.setter
    def short_beta_adjusted_exposure(self, value: float):
        self.__short_beta_adjusted_exposure = value
        self._property_changed('short_beta_adjusted_exposure')        


class LiquidityConstituent(Base):
        
    """A constituent of the portfolio enriched with liquidity and estimated transaction cost information."""
       
    def __init__(
        self,
        asset_id: str = None,
        name: str = None,
        exchange: str = None,
        quantity: float = None,
        gross_weight: float = None,
        net_weight: float = None,
        currency: Union[Currency, str] = None,
        gross_exposure: float = None,
        net_exposure: float = None,
        adv22_day_pct: float = None,
        transaction_cost: float = None,
        marginal_cost: float = None,
        bid_ask_spread: float = None,
        country: str = None,
        region: Union[Region, str] = None,
        type: Union[AssetType, str] = None,
        market_cap: float = None,
        market_cap_bucket=None,
        est1_day_complete_pct: float = None,
        in_benchmark: bool = None,
        in_risk_model: bool = None,
        in_cost_predict_model: bool = None,
        beta: float = None,
        daily_risk: float = None,
        annualized_risk: float = None,
        one_day_price_change_pct: float = None,
        beta_adjusted_exposure: float = None,
        adv_bucket=None,
        settlement_date: datetime.date = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__name = name
        self.__exchange = exchange
        self.__quantity = quantity
        self.__gross_weight = gross_weight
        self.__net_weight = net_weight
        self.__currency = get_enum_value(Currency, currency)
        self.__gross_exposure = gross_exposure
        self.__net_exposure = net_exposure
        self.__adv22_day_pct = adv22_day_pct
        self.__transaction_cost = transaction_cost
        self.__marginal_cost = marginal_cost
        self.__bid_ask_spread = bid_ask_spread
        self.__country = country
        self.__region = get_enum_value(Region, region)
        self.__type = get_enum_value(AssetType, type)
        self.__market_cap = market_cap
        self.__market_cap_bucket = market_cap_bucket
        self.__est1_day_complete_pct = est1_day_complete_pct
        self.__in_benchmark = in_benchmark
        self.__in_risk_model = in_risk_model
        self.__in_cost_predict_model = in_cost_predict_model
        self.__beta = beta
        self.__daily_risk = daily_risk
        self.__annualized_risk = annualized_risk
        self.__one_day_price_change_pct = one_day_price_change_pct
        self.__beta_adjusted_exposure = beta_adjusted_exposure
        self.__adv_bucket = adv_bucket
        self.__settlement_date = settlement_date

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def quantity(self) -> float:
        """The quantity of shares."""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def gross_weight(self) -> float:
        """Gross weight of the constituent."""
        return self.__gross_weight

    @gross_weight.setter
    def gross_weight(self, value: float):
        self.__gross_weight = value
        self._property_changed('gross_weight')        

    @property
    def net_weight(self) -> float:
        """Net weight of the constituent."""
        return self.__net_weight

    @net_weight.setter
    def net_weight(self, value: float):
        self.__net_weight = value
        self._property_changed('net_weight')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def gross_exposure(self) -> float:
        """Gross exposure of the constituent."""
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: float):
        self.__gross_exposure = value
        self._property_changed('gross_exposure')        

    @property
    def net_exposure(self) -> float:
        """Net exposure of the constituent."""
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: float):
        self.__net_exposure = value
        self._property_changed('net_exposure')        

    @property
    def adv22_day_pct(self) -> float:
        """Percentage of the constituent's notional to it's 22 day average daily dollar volume."""
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value: float):
        self.__adv22_day_pct = value
        self._property_changed('adv22_day_pct')        

    @property
    def transaction_cost(self) -> float:
        """The estimated transaction cost for the position."""
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self.__transaction_cost = value
        self._property_changed('transaction_cost')        

    @property
    def marginal_cost(self) -> float:
        """The estimated transaction cost multiplied by the position's gross weight in the portfolio."""
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: float):
        self.__marginal_cost = value
        self._property_changed('marginal_cost')        

    @property
    def bid_ask_spread(self) -> float:
        """The difference between the bid and ask prices for this asset."""
        return self.__bid_ask_spread

    @bid_ask_spread.setter
    def bid_ask_spread(self, value: float):
        self.__bid_ask_spread = value
        self._property_changed('bid_ask_spread')        

    @property
    def country(self) -> str:
        """Country name of asset."""
        return self.__country

    @country.setter
    def country(self, value: str):
        self.__country = value
        self._property_changed('country')        

    @property
    def region(self) -> Union[Region, str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union[Region, str]):
        self.__region = value if isinstance(value, Region) else get_enum_value(Region, value)
        self._property_changed('region')        

    @property
    def type(self) -> Union[AssetType, str]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetType, str]):
        self.__type = value if isinstance(value, AssetType) else get_enum_value(AssetType, value)
        self._property_changed('type')        

    @property
    def market_cap(self) -> float:
        """Market capitalization of a given asset denominated in the currency given in the liquidity parameters."""
        return self.__market_cap

    @market_cap.setter
    def market_cap(self, value: float):
        self.__market_cap = value
        self._property_changed('market_cap')        

    @property
    def market_cap_bucket(self):
        """Market capitalization bucket of the constituent."""
        return self.__market_cap_bucket

    @market_cap_bucket.setter
    def market_cap_bucket(self, value):
        self.__market_cap_bucket = value
        self._property_changed('market_cap_bucket')        

    @property
    def est1_day_complete_pct(self) -> float:
        """Estimated percentage of the position traded in one day."""
        return self.__est1_day_complete_pct

    @est1_day_complete_pct.setter
    def est1_day_complete_pct(self, value: float):
        self.__est1_day_complete_pct = value
        self._property_changed('est1_day_complete_pct')        

    @property
    def in_benchmark(self) -> bool:
        """Whether or not the asset is in the benchmark."""
        return self.__in_benchmark

    @in_benchmark.setter
    def in_benchmark(self, value: bool):
        self.__in_benchmark = value
        self._property_changed('in_benchmark')        

    @property
    def in_risk_model(self) -> bool:
        """Whether or not the asset is in the risk model universe."""
        return self.__in_risk_model

    @in_risk_model.setter
    def in_risk_model(self, value: bool):
        self.__in_risk_model = value
        self._property_changed('in_risk_model')        

    @property
    def in_cost_predict_model(self) -> bool:
        """Whether or not the asset is in the cost prediction model universe."""
        return self.__in_cost_predict_model

    @in_cost_predict_model.setter
    def in_cost_predict_model(self, value: bool):
        self.__in_cost_predict_model = value
        self._property_changed('in_cost_predict_model')        

    @property
    def beta(self) -> float:
        """Beta of the constituent with respect to the risk model universe."""
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def daily_risk(self) -> float:
        """Daily risk of the position in bps."""
        return self.__daily_risk

    @daily_risk.setter
    def daily_risk(self, value: float):
        self.__daily_risk = value
        self._property_changed('daily_risk')        

    @property
    def annualized_risk(self) -> float:
        """Annualized risk of the position in bps."""
        return self.__annualized_risk

    @annualized_risk.setter
    def annualized_risk(self, value: float):
        self.__annualized_risk = value
        self._property_changed('annualized_risk')        

    @property
    def one_day_price_change_pct(self) -> float:
        """One day percentage change in price."""
        return self.__one_day_price_change_pct

    @one_day_price_change_pct.setter
    def one_day_price_change_pct(self, value: float):
        self.__one_day_price_change_pct = value
        self._property_changed('one_day_price_change_pct')        

    @property
    def beta_adjusted_exposure(self) -> float:
        """Beta adjusted exposure."""
        return self.__beta_adjusted_exposure

    @beta_adjusted_exposure.setter
    def beta_adjusted_exposure(self, value: float):
        self.__beta_adjusted_exposure = value
        self._property_changed('beta_adjusted_exposure')        

    @property
    def adv_bucket(self):
        """Category based off of the position's notional with respect to its ADV."""
        return self.__adv_bucket

    @adv_bucket.setter
    def adv_bucket(self, value):
        self.__adv_bucket = value
        self._property_changed('adv_bucket')        

    @property
    def settlement_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self.__settlement_date = value
        self._property_changed('settlement_date')        


class LiquidityFactor(Base):
               
    def __init__(
        self,
        name: str = None,
        value: float = None        
    ):
        super().__init__()
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        """Name of the factor."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def value(self) -> float:
        """Value of the factor."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class LiquiditySummarySection(Base):
        
    """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
       
    def __init__(
        self,
        adv10_day_pct=None,
        adv22_day_pct=None,
        adv5_day_pct: float = None,
        annualized_risk: float = None,
        annualized_tracking_error: float = None,
        beta: float = None,
        beta_adjusted_exposure=None,
        beta_adjusted_net_exposure=None,
        bid_ask_spread: float = None,
        correlation: float = None,
        daily_risk: float = None,
        daily_tracking_error: float = None,
        est1_day_complete_pct=None,
        five_day_price_change_bps=None,
        gross_exposure: float = None,
        marginal_cost: float = None,
        market_cap: float = None,
        minutes_to_trade100_pct: float = None,
        net_exposure: float = None,
        number_of_positions=None,
        percent_in_benchmark=None,
        transaction_cost: float = None,
        weight_of_top_five_positions: float = None        
    ):
        super().__init__()
        self.__adv10_day_pct = adv10_day_pct
        self.__adv22_day_pct = adv22_day_pct
        self.__adv5_day_pct = adv5_day_pct
        self.__annualized_risk = annualized_risk
        self.__annualized_tracking_error = annualized_tracking_error
        self.__beta = beta
        self.__beta_adjusted_exposure = beta_adjusted_exposure
        self.__beta_adjusted_net_exposure = beta_adjusted_net_exposure
        self.__bid_ask_spread = bid_ask_spread
        self.__correlation = correlation
        self.__daily_risk = daily_risk
        self.__daily_tracking_error = daily_tracking_error
        self.__est1_day_complete_pct = est1_day_complete_pct
        self.__five_day_price_change_bps = five_day_price_change_bps
        self.__gross_exposure = gross_exposure
        self.__marginal_cost = marginal_cost
        self.__market_cap = market_cap
        self.__minutes_to_trade100_pct = minutes_to_trade100_pct
        self.__net_exposure = net_exposure
        self.__number_of_positions = number_of_positions
        self.__percent_in_benchmark = percent_in_benchmark
        self.__transaction_cost = transaction_cost
        self.__weight_of_top_five_positions = weight_of_top_five_positions

    @property
    def adv10_day_pct(self):
        return self.__adv10_day_pct

    @adv10_day_pct.setter
    def adv10_day_pct(self, value):
        self.__adv10_day_pct = value
        self._property_changed('adv10_day_pct')        

    @property
    def adv22_day_pct(self):
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value):
        self.__adv22_day_pct = value
        self._property_changed('adv22_day_pct')        

    @property
    def adv5_day_pct(self) -> float:
        return self.__adv5_day_pct

    @adv5_day_pct.setter
    def adv5_day_pct(self, value: float):
        self.__adv5_day_pct = value
        self._property_changed('adv5_day_pct')        

    @property
    def annualized_risk(self) -> float:
        return self.__annualized_risk

    @annualized_risk.setter
    def annualized_risk(self, value: float):
        self.__annualized_risk = value
        self._property_changed('annualized_risk')        

    @property
    def annualized_tracking_error(self) -> float:
        return self.__annualized_tracking_error

    @annualized_tracking_error.setter
    def annualized_tracking_error(self, value: float):
        self.__annualized_tracking_error = value
        self._property_changed('annualized_tracking_error')        

    @property
    def beta(self) -> float:
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def beta_adjusted_exposure(self):
        return self.__beta_adjusted_exposure

    @beta_adjusted_exposure.setter
    def beta_adjusted_exposure(self, value):
        self.__beta_adjusted_exposure = value
        self._property_changed('beta_adjusted_exposure')        

    @property
    def beta_adjusted_net_exposure(self):
        return self.__beta_adjusted_net_exposure

    @beta_adjusted_net_exposure.setter
    def beta_adjusted_net_exposure(self, value):
        self.__beta_adjusted_net_exposure = value
        self._property_changed('beta_adjusted_net_exposure')        

    @property
    def bid_ask_spread(self) -> float:
        return self.__bid_ask_spread

    @bid_ask_spread.setter
    def bid_ask_spread(self, value: float):
        self.__bid_ask_spread = value
        self._property_changed('bid_ask_spread')        

    @property
    def correlation(self) -> float:
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def daily_risk(self) -> float:
        return self.__daily_risk

    @daily_risk.setter
    def daily_risk(self, value: float):
        self.__daily_risk = value
        self._property_changed('daily_risk')        

    @property
    def daily_tracking_error(self) -> float:
        return self.__daily_tracking_error

    @daily_tracking_error.setter
    def daily_tracking_error(self, value: float):
        self.__daily_tracking_error = value
        self._property_changed('daily_tracking_error')        

    @property
    def est1_day_complete_pct(self):
        return self.__est1_day_complete_pct

    @est1_day_complete_pct.setter
    def est1_day_complete_pct(self, value):
        self.__est1_day_complete_pct = value
        self._property_changed('est1_day_complete_pct')        

    @property
    def five_day_price_change_bps(self):
        return self.__five_day_price_change_bps

    @five_day_price_change_bps.setter
    def five_day_price_change_bps(self, value):
        self.__five_day_price_change_bps = value
        self._property_changed('five_day_price_change_bps')        

    @property
    def gross_exposure(self) -> float:
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: float):
        self.__gross_exposure = value
        self._property_changed('gross_exposure')        

    @property
    def marginal_cost(self) -> float:
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: float):
        self.__marginal_cost = value
        self._property_changed('marginal_cost')        

    @property
    def market_cap(self) -> float:
        """Average market capitalization of the group of asset denominated in the currency given in the liquidity parameters."""
        return self.__market_cap

    @market_cap.setter
    def market_cap(self, value: float):
        self.__market_cap = value
        self._property_changed('market_cap')        

    @property
    def minutes_to_trade100_pct(self) -> float:
        return self.__minutes_to_trade100_pct

    @minutes_to_trade100_pct.setter
    def minutes_to_trade100_pct(self, value: float):
        self.__minutes_to_trade100_pct = value
        self._property_changed('minutes_to_trade100_pct')        

    @property
    def net_exposure(self) -> float:
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: float):
        self.__net_exposure = value
        self._property_changed('net_exposure')        

    @property
    def number_of_positions(self):
        return self.__number_of_positions

    @number_of_positions.setter
    def number_of_positions(self, value):
        self.__number_of_positions = value
        self._property_changed('number_of_positions')        

    @property
    def percent_in_benchmark(self):
        return self.__percent_in_benchmark

    @percent_in_benchmark.setter
    def percent_in_benchmark(self, value):
        self.__percent_in_benchmark = value
        self._property_changed('percent_in_benchmark')        

    @property
    def transaction_cost(self) -> float:
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self.__transaction_cost = value
        self._property_changed('transaction_cost')        

    @property
    def weight_of_top_five_positions(self) -> float:
        """What percentage of the portfolio the five largest positions take up."""
        return self.__weight_of_top_five_positions

    @weight_of_top_five_positions.setter
    def weight_of_top_five_positions(self, value: float):
        self.__weight_of_top_five_positions = value
        self._property_changed('weight_of_top_five_positions')        


class LiquidityTableRow(Base):
               
    def __init__(
        self,
        asset_id: str = None,
        name: str = None,
        adv22_day_pct: float = None,
        shares: float = None,
        net_weight: float = None,
        gross_weight: float = None,
        gross_exposure: float = None,
        net_exposure: float = None,
        transaction_cost: float = None,
        marginal_cost: float = None,
        one_day_price_change_pct: float = None,
        normalized_performance: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None        
    ):
        super().__init__()
        self.__asset_id = asset_id
        self.__name = name
        self.__adv22_day_pct = adv22_day_pct
        self.__shares = shares
        self.__net_weight = net_weight
        self.__gross_weight = gross_weight
        self.__gross_exposure = gross_exposure
        self.__net_exposure = net_exposure
        self.__transaction_cost = transaction_cost
        self.__marginal_cost = marginal_cost
        self.__one_day_price_change_pct = one_day_price_change_pct
        self.__normalized_performance = normalized_performance

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self.__asset_id = value
        self._property_changed('asset_id')        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def adv22_day_pct(self) -> float:
        """Percentage of the constituent's notional to it's 22 day average daily dollar volume."""
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value: float):
        self.__adv22_day_pct = value
        self._property_changed('adv22_day_pct')        

    @property
    def shares(self) -> float:
        """The quantity of shares."""
        return self.__shares

    @shares.setter
    def shares(self, value: float):
        self.__shares = value
        self._property_changed('shares')        

    @property
    def net_weight(self) -> float:
        """Net weight of the constituent."""
        return self.__net_weight

    @net_weight.setter
    def net_weight(self, value: float):
        self.__net_weight = value
        self._property_changed('net_weight')        

    @property
    def gross_weight(self) -> float:
        """Gross weight of the constituent."""
        return self.__gross_weight

    @gross_weight.setter
    def gross_weight(self, value: float):
        self.__gross_weight = value
        self._property_changed('gross_weight')        

    @property
    def gross_exposure(self) -> float:
        """Gross exposure of the constituent."""
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: float):
        self.__gross_exposure = value
        self._property_changed('gross_exposure')        

    @property
    def net_exposure(self) -> float:
        """Net exposure of the constituent."""
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: float):
        self.__net_exposure = value
        self._property_changed('net_exposure')        

    @property
    def transaction_cost(self) -> float:
        """The estimated transaction cost for the position."""
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self.__transaction_cost = value
        self._property_changed('transaction_cost')        

    @property
    def marginal_cost(self) -> float:
        """The estimated transaction cost multiplied by the position's gross weight in the portfolio."""
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: float):
        self.__marginal_cost = value
        self._property_changed('marginal_cost')        

    @property
    def one_day_price_change_pct(self) -> float:
        """One day percentage change in price."""
        return self.__one_day_price_change_pct

    @one_day_price_change_pct.setter
    def one_day_price_change_pct(self, value: float):
        self.__one_day_price_change_pct = value
        self._property_changed('one_day_price_change_pct')        

    @property
    def normalized_performance(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of normalized performance."""
        return self.__normalized_performance

    @normalized_performance.setter
    def normalized_performance(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__normalized_performance = value
        self._property_changed('normalized_performance')        


class LiquidityTimeSeriesItem(Base):
               
    def __init__(
        self,
        name: str = None,
        normalized_performance: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        annualized_return: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        annualized_correlation: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        annualized_volatility: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        annualized_sharp_ratio: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        annualized_tracking_error: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        max_drawdown: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        net_exposure: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        cumulative_pnl: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None        
    ):
        super().__init__()
        self.__name = name
        self.__normalized_performance = normalized_performance
        self.__annualized_return = annualized_return
        self.__annualized_correlation = annualized_correlation
        self.__annualized_volatility = annualized_volatility
        self.__annualized_sharp_ratio = annualized_sharp_ratio
        self.__annualized_tracking_error = annualized_tracking_error
        self.__max_drawdown = max_drawdown
        self.__net_exposure = net_exposure
        self.__cumulative_pnl = cumulative_pnl

    @property
    def name(self) -> str:
        """Name of the time series item."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def normalized_performance(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of normalized performance."""
        return self.__normalized_performance

    @normalized_performance.setter
    def normalized_performance(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__normalized_performance = value
        self._property_changed('normalized_performance')        

    @property
    def annualized_return(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized return."""
        return self.__annualized_return

    @annualized_return.setter
    def annualized_return(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualized_return = value
        self._property_changed('annualized_return')        

    @property
    def annualized_correlation(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized correlation."""
        return self.__annualized_correlation

    @annualized_correlation.setter
    def annualized_correlation(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualized_correlation = value
        self._property_changed('annualized_correlation')        

    @property
    def annualized_volatility(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized volatility."""
        return self.__annualized_volatility

    @annualized_volatility.setter
    def annualized_volatility(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualized_volatility = value
        self._property_changed('annualized_volatility')        

    @property
    def annualized_sharp_ratio(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized sharp ratio."""
        return self.__annualized_sharp_ratio

    @annualized_sharp_ratio.setter
    def annualized_sharp_ratio(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualized_sharp_ratio = value
        self._property_changed('annualized_sharp_ratio')        

    @property
    def annualized_tracking_error(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of annualized tracking error."""
        return self.__annualized_tracking_error

    @annualized_tracking_error.setter
    def annualized_tracking_error(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__annualized_tracking_error = value
        self._property_changed('annualized_tracking_error')        

    @property
    def max_drawdown(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of max drawdown."""
        return self.__max_drawdown

    @max_drawdown.setter
    def max_drawdown(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__max_drawdown = value
        self._property_changed('max_drawdown')        

    @property
    def net_exposure(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of net exposure."""
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__net_exposure = value
        self._property_changed('net_exposure')        

    @property
    def cumulative_pnl(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of cumulative PnL."""
        return self.__cumulative_pnl

    @cumulative_pnl.setter
    def cumulative_pnl(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self.__cumulative_pnl = value
        self._property_changed('cumulative_pnl')        


class PRateForHorizon(Base):
               
    def __init__(
        self,
        minutes_expired: int = None,
        participation_rate: float = None,
        participation_rate_long: float = None,
        participation_rate_short: float = None        
    ):
        super().__init__()
        self.__minutes_expired = minutes_expired
        self.__participation_rate = participation_rate
        self.__participation_rate_long = participation_rate_long
        self.__participation_rate_short = participation_rate_short

    @property
    def minutes_expired(self) -> int:
        """Exchange minutes taken to trade the set of positions."""
        return self.__minutes_expired

    @minutes_expired.setter
    def minutes_expired(self, value: int):
        self.__minutes_expired = value
        self._property_changed('minutes_expired')        

    @property
    def participation_rate(self) -> float:
        """Estimated participation rate needed to trade the set of positions."""
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self.__participation_rate = value
        self._property_changed('participation_rate')        

    @property
    def participation_rate_long(self) -> float:
        """Estimated participation rate needed to trade the set of long positions."""
        return self.__participation_rate_long

    @participation_rate_long.setter
    def participation_rate_long(self, value: float):
        self.__participation_rate_long = value
        self._property_changed('participation_rate_long')        

    @property
    def participation_rate_short(self) -> float:
        """Estimated participation rate needed to trade the set of short positions."""
        return self.__participation_rate_short

    @participation_rate_short.setter
    def participation_rate_short(self, value: float):
        self.__participation_rate_short = value
        self._property_changed('participation_rate_short')        


class RiskAtHorizon(Base):
               
    def __init__(
        self,
        minutes_expired: int = None,
        risk: int = None,
        risk_long: float = None,
        risk_short: float = None        
    ):
        super().__init__()
        self.__minutes_expired = minutes_expired
        self.__risk = risk
        self.__risk_long = risk_long
        self.__risk_short = risk_short

    @property
    def minutes_expired(self) -> int:
        """Exchange minutes expired since the start of trading."""
        return self.__minutes_expired

    @minutes_expired.setter
    def minutes_expired(self, value: int):
        self.__minutes_expired = value
        self._property_changed('minutes_expired')        

    @property
    def risk(self) -> int:
        """Risk of the portfolio in bps."""
        return self.__risk

    @risk.setter
    def risk(self, value: int):
        self.__risk = value
        self._property_changed('risk')        

    @property
    def risk_long(self) -> float:
        """Risk of the long positions in bps."""
        return self.__risk_long

    @risk_long.setter
    def risk_long(self, value: float):
        self.__risk_long = value
        self._property_changed('risk_long')        

    @property
    def risk_short(self) -> float:
        """Risk of the short positions in bps."""
        return self.__risk_short

    @risk_short.setter
    def risk_short(self, value: float):
        self.__risk_short = value
        self._property_changed('risk_short')        


class TradeCompleteAtHorizon(Base):
               
    def __init__(
        self,
        minutes_expired: int = None,
        positions_complete: int = None,
        positions_complete_pct: float = None,
        notional_complete_pct: float = None        
    ):
        super().__init__()
        self.__minutes_expired = minutes_expired
        self.__positions_complete = positions_complete
        self.__positions_complete_pct = positions_complete_pct
        self.__notional_complete_pct = notional_complete_pct

    @property
    def minutes_expired(self) -> int:
        """Exchange minutes taken to trade the set of positions."""
        return self.__minutes_expired

    @minutes_expired.setter
    def minutes_expired(self, value: int):
        self.__minutes_expired = value
        self._property_changed('minutes_expired')        

    @property
    def positions_complete(self) -> int:
        """Number of the portfolio's positions that have been fully traded."""
        return self.__positions_complete

    @positions_complete.setter
    def positions_complete(self, value: int):
        self.__positions_complete = value
        self._property_changed('positions_complete')        

    @property
    def positions_complete_pct(self) -> float:
        """Percentage of the portfolio's positions that have been fully traded."""
        return self.__positions_complete_pct

    @positions_complete_pct.setter
    def positions_complete_pct(self, value: float):
        self.__positions_complete_pct = value
        self._property_changed('positions_complete_pct')        

    @property
    def notional_complete_pct(self) -> float:
        """Percentage of the portfolio's notional that have been traded."""
        return self.__notional_complete_pct

    @notional_complete_pct.setter
    def notional_complete_pct(self, value: float):
        self.__notional_complete_pct = value
        self._property_changed('notional_complete_pct')        


class LiquidityFactorCategory(Base):
               
    def __init__(
        self,
        name: str = None,
        sub_factors: Tuple[LiquidityFactor, ...] = None        
    ):
        super().__init__()
        self.__name = name
        self.__sub_factors = sub_factors

    @property
    def name(self) -> str:
        """Name of the factor category."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def sub_factors(self) -> Tuple[LiquidityFactor, ...]:
        return self.__sub_factors

    @sub_factors.setter
    def sub_factors(self, value: Tuple[LiquidityFactor, ...]):
        self.__sub_factors = value
        self._property_changed('sub_factors')        


class LiquiditySummary(Base):
        
    """Summary of the liquidity analytics data."""
       
    def __init__(
        self,
        total: LiquiditySummarySection,
        long: LiquiditySummarySection = None,
        short: LiquiditySummarySection = None,
        long_vs_short: LiquiditySummarySection = None        
    ):
        super().__init__()
        self.__total = total
        self.__long = long
        self.__short = short
        self.__long_vs_short = long_vs_short

    @property
    def total(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__total

    @total.setter
    def total(self, value: LiquiditySummarySection):
        self.__total = value
        self._property_changed('total')        

    @property
    def long(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__long

    @long.setter
    def long(self, value: LiquiditySummarySection):
        self.__long = value
        self._property_changed('long')        

    @property
    def short(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__short

    @short.setter
    def short(self, value: LiquiditySummarySection):
        self.__short = value
        self._property_changed('short')        

    @property
    def long_vs_short(self) -> LiquiditySummarySection:
        """Summary of the liquidity metrics for either the total, long, or short side of the portfolio."""
        return self.__long_vs_short

    @long_vs_short.setter
    def long_vs_short(self, value: LiquiditySummarySection):
        self.__long_vs_short = value
        self._property_changed('long_vs_short')        


class RiskModelRequest(Base):
        
    """Object representation of a risk model request"""
       
    def __init__(
        self,
        asset_ids: Tuple[str, ...] = None,
        as_of_date: datetime.date = None,
        sort_by_term: Union[SortByTerm, str] = None        
    ):
        super().__init__()
        self.__asset_ids = asset_ids
        self.__as_of_date = as_of_date
        self.__sort_by_term = get_enum_value(SortByTerm, sort_by_term)

    @property
    def asset_ids(self) -> Tuple[str, ...]:
        """Assets to calculate on"""
        return self.__asset_ids

    @asset_ids.setter
    def asset_ids(self, value: Tuple[str, ...]):
        self.__asset_ids = value
        self._property_changed('asset_ids')        

    @property
    def as_of_date(self) -> datetime.date:
        """The date or time for which to check risk model availability"""
        return self.__as_of_date

    @as_of_date.setter
    def as_of_date(self, value: datetime.date):
        self.__as_of_date = value
        self._property_changed('as_of_date')        

    @property
    def sort_by_term(self) -> Union[SortByTerm, str]:
        """Term to sort risk models by."""
        return self.__sort_by_term

    @sort_by_term.setter
    def sort_by_term(self, value: Union[SortByTerm, str]):
        self.__sort_by_term = value if isinstance(value, SortByTerm) else get_enum_value(SortByTerm, value)
        self._property_changed('sort_by_term')        


class LiquidityResponse(Base):
        
    """Liquidity information for a set of weighted positions."""
       
    def __init__(
        self,
        assets_not_in_risk_model: Tuple[str, ...] = None,
        assets_not_in_cost_predict_model: Tuple[str, ...] = None,
        as_of_date: datetime.date = None,
        risk_model: str = None,
        notional: float = None,
        currency: Union[Currency, str] = None,
        report: str = None,
        summary: LiquiditySummary = None,
        constituent_transaction_costs: Tuple[LiquidityConstituent, ...] = None,
        constituents: Tuple[LiquidityConstituent, ...] = None,
        largest_holdings_by_weight: Tuple[LiquidityTableRow, ...] = None,
        least_liquid_holdings: Tuple[LiquidityTableRow, ...] = None,
        adv_buckets: Tuple[LiquidityBucket, ...] = None,
        region_buckets: Tuple[LiquidityBucket, ...] = None,
        country_buckets: Tuple[LiquidityBucket, ...] = None,
        sector_buckets: Tuple[LiquidityBucket, ...] = None,
        industry_buckets: Tuple[LiquidityBucket, ...] = None,
        market_cap_buckets: Tuple[LiquidityBucket, ...] = None,
        execution_costs_with_different_time_horizons: Tuple[ExecutionCostForHorizon, ...] = None,
        time_to_trade_with_different_participation_rates: Tuple[PRateForHorizon, ...] = None,
        risk_over_time: Tuple[RiskAtHorizon, ...] = None,
        trade_complete_percent_over_time: Tuple[TradeCompleteAtHorizon, ...] = None,
        adv_percent_over_time: Tuple[AdvCurveTick, ...] = None,
        risk_buckets: Tuple[LiquidityFactor, ...] = None,
        factor_risk_buckets: Tuple[LiquidityFactorCategory, ...] = None,
        exposure_buckets: Tuple[LiquidityFactor, ...] = None,
        factor_exposure_buckets: Tuple[LiquidityFactorCategory, ...] = None,
        timeseries_data: Tuple[LiquidityTimeSeriesItem, ...] = None,
        error_message: str = None        
    ):
        super().__init__()
        self.__assets_not_in_risk_model = assets_not_in_risk_model
        self.__assets_not_in_cost_predict_model = assets_not_in_cost_predict_model
        self.__as_of_date = as_of_date
        self.__risk_model = risk_model
        self.__notional = notional
        self.__currency = get_enum_value(Currency, currency)
        self.__report = report
        self.__summary = summary
        self.__constituent_transaction_costs = constituent_transaction_costs
        self.__constituents = constituents
        self.__largest_holdings_by_weight = largest_holdings_by_weight
        self.__least_liquid_holdings = least_liquid_holdings
        self.__adv_buckets = adv_buckets
        self.__region_buckets = region_buckets
        self.__country_buckets = country_buckets
        self.__sector_buckets = sector_buckets
        self.__industry_buckets = industry_buckets
        self.__market_cap_buckets = market_cap_buckets
        self.__execution_costs_with_different_time_horizons = execution_costs_with_different_time_horizons
        self.__time_to_trade_with_different_participation_rates = time_to_trade_with_different_participation_rates
        self.__risk_over_time = risk_over_time
        self.__trade_complete_percent_over_time = trade_complete_percent_over_time
        self.__adv_percent_over_time = adv_percent_over_time
        self.__risk_buckets = risk_buckets
        self.__factor_risk_buckets = factor_risk_buckets
        self.__exposure_buckets = exposure_buckets
        self.__factor_exposure_buckets = factor_exposure_buckets
        self.__timeseries_data = timeseries_data
        self.__error_message = error_message

    @property
    def assets_not_in_risk_model(self) -> Tuple[str, ...]:
        """Assets in the the portfolio that are not covered in the risk model."""
        return self.__assets_not_in_risk_model

    @assets_not_in_risk_model.setter
    def assets_not_in_risk_model(self, value: Tuple[str, ...]):
        self.__assets_not_in_risk_model = value
        self._property_changed('assets_not_in_risk_model')        

    @property
    def assets_not_in_cost_predict_model(self) -> Tuple[str, ...]:
        """Assets in the the portfolio that are not covered in the cost prediction model."""
        return self.__assets_not_in_cost_predict_model

    @assets_not_in_cost_predict_model.setter
    def assets_not_in_cost_predict_model(self, value: Tuple[str, ...]):
        self.__assets_not_in_cost_predict_model = value
        self._property_changed('assets_not_in_cost_predict_model')        

    @property
    def as_of_date(self) -> datetime.date:
        """Calculation date in ISO 8601 format."""
        return self.__as_of_date

    @as_of_date.setter
    def as_of_date(self, value: datetime.date):
        self.__as_of_date = value
        self._property_changed('as_of_date')        

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self.__risk_model = value
        self._property_changed('risk_model')        

    @property
    def notional(self) -> float:
        """Notional value of the positions."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self.__currency = value if isinstance(value, Currency) else get_enum_value(Currency, value)
        self._property_changed('currency')        

    @property
    def report(self) -> str:
        return self.__report

    @report.setter
    def report(self, value: str):
        self.__report = value
        self._property_changed('report')        

    @property
    def summary(self) -> LiquiditySummary:
        """Summary of the liquidity analytics data."""
        return self.__summary

    @summary.setter
    def summary(self, value: LiquiditySummary):
        self.__summary = value
        self._property_changed('summary')        

    @property
    def constituent_transaction_costs(self) -> Tuple[LiquidityConstituent, ...]:
        """Constituents of the portfolio enriched with transaction cost information."""
        return self.__constituent_transaction_costs

    @constituent_transaction_costs.setter
    def constituent_transaction_costs(self, value: Tuple[LiquidityConstituent, ...]):
        self.__constituent_transaction_costs = value
        self._property_changed('constituent_transaction_costs')        

    @property
    def constituents(self) -> Tuple[LiquidityConstituent, ...]:
        """Constituents of the portfolio enriched with liquidity and estimated transaction cost information."""
        return self.__constituents

    @constituents.setter
    def constituents(self, value: Tuple[LiquidityConstituent, ...]):
        self.__constituents = value
        self._property_changed('constituents')        

    @property
    def largest_holdings_by_weight(self) -> Tuple[LiquidityTableRow, ...]:
        """The five largest holdings by gross weight in the portfolio."""
        return self.__largest_holdings_by_weight

    @largest_holdings_by_weight.setter
    def largest_holdings_by_weight(self, value: Tuple[LiquidityTableRow, ...]):
        self.__largest_holdings_by_weight = value
        self._property_changed('largest_holdings_by_weight')        

    @property
    def least_liquid_holdings(self) -> Tuple[LiquidityTableRow, ...]:
        """The five least liquid holdings in the portfolio."""
        return self.__least_liquid_holdings

    @least_liquid_holdings.setter
    def least_liquid_holdings(self, value: Tuple[LiquidityTableRow, ...]):
        self.__least_liquid_holdings = value
        self._property_changed('least_liquid_holdings')        

    @property
    def adv_buckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__adv_buckets

    @adv_buckets.setter
    def adv_buckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__adv_buckets = value
        self._property_changed('adv_buckets')        

    @property
    def region_buckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__region_buckets

    @region_buckets.setter
    def region_buckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__region_buckets = value
        self._property_changed('region_buckets')        

    @property
    def country_buckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__country_buckets

    @country_buckets.setter
    def country_buckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__country_buckets = value
        self._property_changed('country_buckets')        

    @property
    def sector_buckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__sector_buckets

    @sector_buckets.setter
    def sector_buckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__sector_buckets = value
        self._property_changed('sector_buckets')        

    @property
    def industry_buckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__industry_buckets

    @industry_buckets.setter
    def industry_buckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__industry_buckets = value
        self._property_changed('industry_buckets')        

    @property
    def market_cap_buckets(self) -> Tuple[LiquidityBucket, ...]:
        """Positions data bucketed by common characteristic."""
        return self.__market_cap_buckets

    @market_cap_buckets.setter
    def market_cap_buckets(self, value: Tuple[LiquidityBucket, ...]):
        self.__market_cap_buckets = value
        self._property_changed('market_cap_buckets')        

    @property
    def execution_costs_with_different_time_horizons(self) -> Tuple[ExecutionCostForHorizon, ...]:
        """Execution costs at different time horizons."""
        return self.__execution_costs_with_different_time_horizons

    @execution_costs_with_different_time_horizons.setter
    def execution_costs_with_different_time_horizons(self, value: Tuple[ExecutionCostForHorizon, ...]):
        self.__execution_costs_with_different_time_horizons = value
        self._property_changed('execution_costs_with_different_time_horizons')        

    @property
    def time_to_trade_with_different_participation_rates(self) -> Tuple[PRateForHorizon, ...]:
        """Participation rates required at different time horizons."""
        return self.__time_to_trade_with_different_participation_rates

    @time_to_trade_with_different_participation_rates.setter
    def time_to_trade_with_different_participation_rates(self, value: Tuple[PRateForHorizon, ...]):
        self.__time_to_trade_with_different_participation_rates = value
        self._property_changed('time_to_trade_with_different_participation_rates')        

    @property
    def risk_over_time(self) -> Tuple[RiskAtHorizon, ...]:
        """Risk at different time horizons."""
        return self.__risk_over_time

    @risk_over_time.setter
    def risk_over_time(self, value: Tuple[RiskAtHorizon, ...]):
        self.__risk_over_time = value
        self._property_changed('risk_over_time')        

    @property
    def trade_complete_percent_over_time(self) -> Tuple[TradeCompleteAtHorizon, ...]:
        """Trade completion information at different time horizons."""
        return self.__trade_complete_percent_over_time

    @trade_complete_percent_over_time.setter
    def trade_complete_percent_over_time(self, value: Tuple[TradeCompleteAtHorizon, ...]):
        self.__trade_complete_percent_over_time = value
        self._property_changed('trade_complete_percent_over_time')        

    @property
    def adv_percent_over_time(self) -> Tuple[AdvCurveTick, ...]:
        """Historical ADV Percent curve of the portfolio."""
        return self.__adv_percent_over_time

    @adv_percent_over_time.setter
    def adv_percent_over_time(self, value: Tuple[AdvCurveTick, ...]):
        self.__adv_percent_over_time = value
        self._property_changed('adv_percent_over_time')        

    @property
    def risk_buckets(self) -> Tuple[LiquidityFactor, ...]:
        """Risk buckets."""
        return self.__risk_buckets

    @risk_buckets.setter
    def risk_buckets(self, value: Tuple[LiquidityFactor, ...]):
        self.__risk_buckets = value
        self._property_changed('risk_buckets')        

    @property
    def factor_risk_buckets(self) -> Tuple[LiquidityFactorCategory, ...]:
        """Factor risk buckets."""
        return self.__factor_risk_buckets

    @factor_risk_buckets.setter
    def factor_risk_buckets(self, value: Tuple[LiquidityFactorCategory, ...]):
        self.__factor_risk_buckets = value
        self._property_changed('factor_risk_buckets')        

    @property
    def exposure_buckets(self) -> Tuple[LiquidityFactor, ...]:
        """Exposure buckets."""
        return self.__exposure_buckets

    @exposure_buckets.setter
    def exposure_buckets(self, value: Tuple[LiquidityFactor, ...]):
        self.__exposure_buckets = value
        self._property_changed('exposure_buckets')        

    @property
    def factor_exposure_buckets(self) -> Tuple[LiquidityFactorCategory, ...]:
        """Factor exposures buckets."""
        return self.__factor_exposure_buckets

    @factor_exposure_buckets.setter
    def factor_exposure_buckets(self, value: Tuple[LiquidityFactorCategory, ...]):
        self.__factor_exposure_buckets = value
        self._property_changed('factor_exposure_buckets')        

    @property
    def timeseries_data(self) -> Tuple[LiquidityTimeSeriesItem, ...]:
        """Timeseries data."""
        return self.__timeseries_data

    @timeseries_data.setter
    def timeseries_data(self, value: Tuple[LiquidityTimeSeriesItem, ...]):
        self.__timeseries_data = value
        self._property_changed('timeseries_data')        

    @property
    def error_message(self) -> str:
        """Marquee Liquidity error message"""
        return self.__error_message

    @error_message.setter
    def error_message(self, value: str):
        self.__error_message = value
        self._property_changed('error_message')        
