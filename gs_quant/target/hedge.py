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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class CorporateActionsTypes(EnumBase, Enum):    
    
    """Types of corporate actions in the hedge"""

    Mergers = 'Mergers'
    Quote_lot_adjustments = 'Quote lot adjustments'
    Rights = 'Rights'
    Spinoffs = 'Spinoffs'
    Cash_dividends = 'Cash dividends'
    Stock_splits = 'Stock splits'
    Reorganization = 'Reorganization'    


class HedgeObjective(EnumBase, Enum):    
    
    """The objective of the hedge."""

    Minimize_Factor_Risk = 'Minimize Factor Risk'
    Replicate_Performance = 'Replicate Performance'    


class HedgeUniverseAssetType(EnumBase, Enum):    
    
    """Type of assets that will be added to the hedge universe."""

    Custom_Basket = 'Custom Basket'
    ETF = 'ETF'
    Research_Basket = 'Research Basket'
    Single_Stock = 'Single Stock'    


class HedgerComparisonType(EnumBase, Enum):    
    
    Asset = 'Asset'
    Portfolio = 'Portfolio'
    Hedge = 'Hedge'    


class HedgerConstraintPrioritySetting(EnumBase, Enum):    
    
    """Priority of the constraint from 0-5 (prioritized in that order). The
       optimization will fail if it cannot meet a constraint with 0 priority. A
       constraint with priority of 1-5 can be called a relaxed constraint, which
       means that the optimization will make its best effort to meet the
       constraint but will not fail if it cannot."""

    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'    


class AssetConstraint(Base):
        
    """Constraint on a specific asset in the hedge universe."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        max_: float,
        min_: float,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.__max = max_
        self.__min = min_
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def max(self) -> float:
        """Maximum percentage weight of the asset in the hedge."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self._property_changed('max')
        self.__max = value        

    @property
    def min(self) -> float:
        """Minimum percentage weight of the asset in the hedge."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self._property_changed('min')
        self.__min = value        


class ClassificationConstraint(Base):
        
    """Constraint on an asset classification to be applied to the hedge."""

    @camel_case_translate
    def __init__(
        self,
        type_: str,
        name: str,
        max_: float,
        min_: float
    ):        
        super().__init__()
        self.__type = type_
        self.name = name
        self.__max = max_
        self.__min = min_

    @property
    def type(self) -> str:
        """Type of classification."""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def name(self) -> str:
        """Name of classification."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def max(self) -> float:
        """Maximum combined weight of any universe assets that fall under this
           classification in the hedge result (0-100)."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self._property_changed('max')
        self.__max = value        

    @property
    def min(self) -> float:
        """Minimum combined weight of any universe assets that fall under this
           classification in the hedge result (0-100)."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self._property_changed('min')
        self.__min = value        


class ESGConstraint(Base):
        
    """Constraint on ESG metric values of assets to be included in a hedge."""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        max_: float,
        min_: float
    ):        
        super().__init__()
        self.name = name
        self.__max = max_
        self.__min = min_

    @property
    def name(self) -> str:
        """Name of ESG Metric by which to filter asset universe."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def max(self) -> float:
        """Maximum score of chosen ESG metric for any universe assets in the hedge result."""
        return self.__max

    @max.setter
    def max(self, value: float):
        self._property_changed('max')
        self.__max = value        

    @property
    def min(self) -> float:
        """Minimum score of chosen ESG metric for any universe assets in the hedge result."""
        return self.__min

    @min.setter
    def min(self, value: float):
        self._property_changed('min')
        self.__min = value        


class FactorConstraint(Base):
        
    """Constraint on a specific risk model factor."""

    @camel_case_translate
    def __init__(
        self,
        factor: str,
        exposure: float,
        name: str = None
    ):        
        super().__init__()
        self.factor = factor
        self.exposure = exposure
        self.name = name

    @property
    def factor(self) -> str:
        """Risk model factor name."""
        return self.__factor

    @factor.setter
    def factor(self, value: str):
        self._property_changed('factor')
        self.__factor = value        

    @property
    def exposure(self) -> float:
        """Exposure in USD."""
        return self.__exposure

    @exposure.setter
    def exposure(self, value: float):
        self._property_changed('exposure')
        self.__exposure = value        


class FactorExposure(Base):
        
    """Object representation of a Factor Exposure."""

    @camel_case_translate
    def __init__(
        self,
        factor: str,
        exposure: float,
        name: str = None
    ):        
        super().__init__()
        self.factor = factor
        self.exposure = exposure
        self.name = name

    @property
    def factor(self) -> str:
        """Name of the Risk Model factor."""
        return self.__factor

    @factor.setter
    def factor(self, value: str):
        self._property_changed('factor')
        self.__factor = value        

    @property
    def exposure(self) -> float:
        """Exposure in USD."""
        return self.__exposure

    @exposure.setter
    def exposure(self, value: float):
        self._property_changed('exposure')
        self.__exposure = value        


class HedgerComparisonProperties(Base):
        
    """properties used to hedge the comparison."""

    @camel_case_translate
    def __init__(
        self,
        hedge_value_type: str,
        hedge_value: float,
        name: str = None
    ):        
        super().__init__()
        self.hedge_value_type = hedge_value_type
        self.hedge_value = hedge_value
        self.name = name

    @property
    def hedge_value_type(self) -> str:
        """The type of value for which is applied to value the hedge in the comparison."""
        return self.__hedge_value_type

    @hedge_value_type.setter
    def hedge_value_type(self, value: str):
        self._property_changed('hedge_value_type')
        self.__hedge_value_type = value        

    @property
    def hedge_value(self) -> float:
        return self.__hedge_value

    @hedge_value.setter
    def hedge_value(self, value: float):
        self._property_changed('hedge_value')
        self.__hedge_value = value        


class FactorExposures(Base):
        
    """Breakdown of factor exposures by category."""

    @camel_case_translate
    def __init__(
        self,
        country: Tuple[FactorExposure, ...],
        industry: Tuple[FactorExposure, ...],
        sector: Tuple[FactorExposure, ...],
        style: Tuple[FactorExposure, ...],
        name: str = None
    ):        
        super().__init__()
        self.country = country
        self.industry = industry
        self.sector = sector
        self.style = style
        self.name = name

    @property
    def country(self) -> Tuple[FactorExposure, ...]:
        """List of country factor exposures."""
        return self.__country

    @country.setter
    def country(self, value: Tuple[FactorExposure, ...]):
        self._property_changed('country')
        self.__country = value        

    @property
    def industry(self) -> Tuple[FactorExposure, ...]:
        """List of industry factor exposures."""
        return self.__industry

    @industry.setter
    def industry(self, value: Tuple[FactorExposure, ...]):
        self._property_changed('industry')
        self.__industry = value        

    @property
    def sector(self) -> Tuple[FactorExposure, ...]:
        """List of sector factor exposures."""
        return self.__sector

    @sector.setter
    def sector(self, value: Tuple[FactorExposure, ...]):
        self._property_changed('sector')
        self.__sector = value        

    @property
    def style(self) -> Tuple[FactorExposure, ...]:
        """List of style factor exposures."""
        return self.__style

    @style.setter
    def style(self, value: Tuple[FactorExposure, ...]):
        self._property_changed('style')
        self.__style = value        


class FactorHedgeUniverse(Base):
        
    """Any combination of asset ids and bulk asset types that make up the universe."""

    @camel_case_translate
    def __init__(
        self,
        asset_ids: Tuple[str, ...] = None,
        asset_types: Tuple[Union[HedgeUniverseAssetType, str], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_ids = asset_ids
        self.asset_types = asset_types
        self.name = name

    @property
    def asset_ids(self) -> Tuple[str, ...]:
        """Set of marquee unique asset identifiers that make up the hedge universe. Any
           identifiers that are not for single stocks will be exploded into
           their underliers."""
        return self.__asset_ids

    @asset_ids.setter
    def asset_ids(self, value: Tuple[str, ...]):
        self._property_changed('asset_ids')
        self.__asset_ids = value        

    @property
    def asset_types(self) -> Tuple[Union[HedgeUniverseAssetType, str], ...]:
        """Types of assets that will be added to the hedge universe."""
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: Tuple[Union[HedgeUniverseAssetType, str], ...]):
        self._property_changed('asset_types')
        self.__asset_types = value        


class FactorHedgerConstraintPrioritySettings(Base):
        
    """Specify the priority of constraints"""

    @camel_case_translate
    def __init__(
        self,
        min_sector_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        max_sector_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        min_industry_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        max_industry_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        min_region_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        max_region_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        min_country_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        max_country_weights: Union[HedgerConstraintPrioritySetting, str] = None,
        style_exposures: Union[HedgerConstraintPrioritySetting, str] = None,
        country_exposures: Union[HedgerConstraintPrioritySetting, str] = None,
        region_exposures: Union[HedgerConstraintPrioritySetting, str] = None,
        industry_exposures: Union[HedgerConstraintPrioritySetting, str] = None,
        sector_exposures: Union[HedgerConstraintPrioritySetting, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.min_sector_weights = min_sector_weights
        self.max_sector_weights = max_sector_weights
        self.min_industry_weights = min_industry_weights
        self.max_industry_weights = max_industry_weights
        self.min_region_weights = min_region_weights
        self.max_region_weights = max_region_weights
        self.min_country_weights = min_country_weights
        self.max_country_weights = max_country_weights
        self.style_exposures = style_exposures
        self.country_exposures = country_exposures
        self.region_exposures = region_exposures
        self.industry_exposures = industry_exposures
        self.sector_exposures = sector_exposures
        self.name = name

    @property
    def min_sector_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__min_sector_weights

    @min_sector_weights.setter
    def min_sector_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('min_sector_weights')
        self.__min_sector_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def max_sector_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__max_sector_weights

    @max_sector_weights.setter
    def max_sector_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('max_sector_weights')
        self.__max_sector_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def min_industry_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__min_industry_weights

    @min_industry_weights.setter
    def min_industry_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('min_industry_weights')
        self.__min_industry_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def max_industry_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__max_industry_weights

    @max_industry_weights.setter
    def max_industry_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('max_industry_weights')
        self.__max_industry_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def min_region_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__min_region_weights

    @min_region_weights.setter
    def min_region_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('min_region_weights')
        self.__min_region_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def max_region_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__max_region_weights

    @max_region_weights.setter
    def max_region_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('max_region_weights')
        self.__max_region_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def min_country_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__min_country_weights

    @min_country_weights.setter
    def min_country_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('min_country_weights')
        self.__min_country_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def max_country_weights(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__max_country_weights

    @max_country_weights.setter
    def max_country_weights(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('max_country_weights')
        self.__max_country_weights = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def style_exposures(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__style_exposures

    @style_exposures.setter
    def style_exposures(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('style_exposures')
        self.__style_exposures = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def country_exposures(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__country_exposures

    @country_exposures.setter
    def country_exposures(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('country_exposures')
        self.__country_exposures = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def region_exposures(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__region_exposures

    @region_exposures.setter
    def region_exposures(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('region_exposures')
        self.__region_exposures = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def industry_exposures(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__industry_exposures

    @industry_exposures.setter
    def industry_exposures(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('industry_exposures')
        self.__industry_exposures = get_enum_value(HedgerConstraintPrioritySetting, value)        

    @property
    def sector_exposures(self) -> Union[HedgerConstraintPrioritySetting, str]:
        """Priority of the constraint from 0-5 (prioritized in that order). The
           optimization will fail if it cannot meet a constraint with 0
           priority. A constraint with priority of 1-5 can be called a relaxed
           constraint, which means that the optimization will make its best
           effort to meet the constraint but will not fail if it cannot."""
        return self.__sector_exposures

    @sector_exposures.setter
    def sector_exposures(self, value: Union[HedgerConstraintPrioritySetting, str]):
        self._property_changed('sector_exposures')
        self.__sector_exposures = get_enum_value(HedgerConstraintPrioritySetting, value)        


class HedgeConstituent(Base):
        
    """Fields returned for each hedge constituent."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        name: str,
        weight: float,
        currency: Union[Currency, str],
        country: str = None,
        correlation: float = None,
        transaction_cost: float = None,
        marginal_cost: float = None,
        borrow_cost: float = None,
        shares: float = None,
        price: float = None,
        multiplier: float = None,
        notional: float = None,
        bbid: str = None,
        adv_percentage: float = None,
        sector: str = None,
        industry: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.name = name
        self.weight = weight
        self.currency = currency
        self.country = country
        self.correlation = correlation
        self.transaction_cost = transaction_cost
        self.marginal_cost = marginal_cost
        self.borrow_cost = borrow_cost
        self.shares = shares
        self.price = price
        self.multiplier = multiplier
        self.notional = notional
        self.bbid = bbid
        self.adv_percentage = adv_percentage
        self.sector = sector
        self.industry = industry

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def weight(self) -> float:
        """Weight of the constituent."""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def country(self) -> str:
        """Country name of asset."""
        return self.__country

    @country.setter
    def country(self, value: str):
        self._property_changed('country')
        self.__country = value        

    @property
    def correlation(self) -> float:
        """Max 44 day rolling correlation between the constituent and target returns."""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self._property_changed('correlation')
        self.__correlation = value        

    @property
    def transaction_cost(self) -> float:
        """The estimated market impact cost for trading a position or set of positions at a
           specified market participation rate or trade-out period."""
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self._property_changed('transaction_cost')
        self.__transaction_cost = value        

    @property
    def marginal_cost(self) -> float:
        """The estimated market impact cost multiplied by the position's gross weight in
           the portfolio."""
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: float):
        self._property_changed('marginal_cost')
        self.__marginal_cost = value        

    @property
    def borrow_cost(self) -> float:
        """The estimated borrow fee in bps to short the position or position set."""
        return self.__borrow_cost

    @borrow_cost.setter
    def borrow_cost(self, value: float):
        self._property_changed('borrow_cost')
        self.__borrow_cost = value        

    @property
    def shares(self) -> float:
        """The quantity of shares."""
        return self.__shares

    @shares.setter
    def shares(self, value: float):
        self._property_changed('shares')
        self.__shares = value        

    @property
    def price(self) -> float:
        """The price in USD."""
        return self.__price

    @price.setter
    def price(self, value: float):
        self._property_changed('price')
        self.__price = value        

    @property
    def multiplier(self) -> float:
        """Underlying unit per asset multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def notional(self) -> float:
        """Notional of the position"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def bbid(self) -> str:
        """Bloomberg Id Identifier"""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def adv_percentage(self) -> float:
        """Percentage of the constituent's notional in the hedge to it's average daily
           dollar volume."""
        return self.__adv_percentage

    @adv_percentage.setter
    def adv_percentage(self, value: float):
        self._property_changed('adv_percentage')
        self.__adv_percentage = value        

    @property
    def sector(self) -> str:
        """GICS Sector classification (level 1)."""
        return self.__sector

    @sector.setter
    def sector(self, value: str):
        self._property_changed('sector')
        self.__sector = value        

    @property
    def industry(self) -> str:
        """GICS industry classification (level 3)."""
        return self.__industry

    @industry.setter
    def industry(self, value: str):
        self._property_changed('industry')
        self.__industry = value        


class FactorHedgerResultPositions(Base):
        
    """The set of values returned for either the target, hedge, or hedged target
       positions in a hedge calculation with an objective to minimize factor
       risk."""

    @camel_case_translate
    def __init__(
        self,
        beta_exposure: float,
        daily_va_r: float,
        factor_exposures: FactorExposures,
        specific_exposure: float,
        systematic_exposure: float,
        total_risk: float,
        volatility: float,
        net_exposure: float,
        constituents: Tuple[HedgeConstituent, ...] = None,
        number_of_positions: float = None,
        cumulative_pnl: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        transaction_cost: float = None,
        borrow_cost_bps: float = None,
        max_drawdown: float = None,
        gross_exposure: float = None,
        long_exposure: float = None,
        short_exposure: float = None,
        tracking_error: float = None,
        correlation: float = None,
        exposure_overlap_with_target: float = None,
        total_pnl: float = None,
        turnover_percentage: float = None,
        name: str = None
    ):        
        super().__init__()
        self.beta_exposure = beta_exposure
        self.constituents = constituents
        self.number_of_positions = number_of_positions
        self.daily_va_r = daily_va_r
        self.factor_exposures = factor_exposures
        self.cumulative_pnl = cumulative_pnl
        self.specific_exposure = specific_exposure
        self.systematic_exposure = systematic_exposure
        self.total_risk = total_risk
        self.transaction_cost = transaction_cost
        self.borrow_cost_bps = borrow_cost_bps
        self.volatility = volatility
        self.max_drawdown = max_drawdown
        self.net_exposure = net_exposure
        self.gross_exposure = gross_exposure
        self.long_exposure = long_exposure
        self.short_exposure = short_exposure
        self.tracking_error = tracking_error
        self.correlation = correlation
        self.exposure_overlap_with_target = exposure_overlap_with_target
        self.total_pnl = total_pnl
        self.turnover_percentage = turnover_percentage
        self.name = name

    @property
    def beta_exposure(self) -> float:
        """Exposure to beta."""
        return self.__beta_exposure

    @beta_exposure.setter
    def beta_exposure(self, value: float):
        self._property_changed('beta_exposure')
        self.__beta_exposure = value        

    @property
    def constituents(self) -> Tuple[HedgeConstituent, ...]:
        """Composition of asset positions that make up the hedge."""
        return self.__constituents

    @constituents.setter
    def constituents(self, value: Tuple[HedgeConstituent, ...]):
        self._property_changed('constituents')
        self.__constituents = value        

    @property
    def number_of_positions(self) -> float:
        """Number of positions in the entity."""
        return self.__number_of_positions

    @number_of_positions.setter
    def number_of_positions(self, value: float):
        self._property_changed('number_of_positions')
        self.__number_of_positions = value        

    @property
    def daily_va_r(self) -> float:
        """Daily value at risk."""
        return self.__daily_va_r

    @daily_va_r.setter
    def daily_va_r(self, value: float):
        self._property_changed('daily_va_r')
        self.__daily_va_r = value        

    @property
    def factor_exposures(self) -> FactorExposures:
        """Breakdown of factor exposures by category."""
        return self.__factor_exposures

    @factor_exposures.setter
    def factor_exposures(self, value: FactorExposures):
        self._property_changed('factor_exposures')
        self.__factor_exposures = value        

    @property
    def cumulative_pnl(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """Time series of cumulative Pnl."""
        return self.__cumulative_pnl

    @cumulative_pnl.setter
    def cumulative_pnl(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self._property_changed('cumulative_pnl')
        self.__cumulative_pnl = value        

    @property
    def specific_exposure(self) -> float:
        """Change in portfolio value which is idiosyncratic to individual assets."""
        return self.__specific_exposure

    @specific_exposure.setter
    def specific_exposure(self, value: float):
        self._property_changed('specific_exposure')
        self.__specific_exposure = value        

    @property
    def systematic_exposure(self) -> float:
        """Change in portfolio value attributable to systematic risk factors."""
        return self.__systematic_exposure

    @systematic_exposure.setter
    def systematic_exposure(self, value: float):
        self._property_changed('systematic_exposure')
        self.__systematic_exposure = value        

    @property
    def total_risk(self) -> float:
        """Cumulative daily fluctuation in portfolio value."""
        return self.__total_risk

    @total_risk.setter
    def total_risk(self, value: float):
        self._property_changed('total_risk')
        self.__total_risk = value        

    @property
    def transaction_cost(self) -> float:
        """The estimated market impact cost for trading a position or set of positions at a
           specified market participation rate or trade-out period."""
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self._property_changed('transaction_cost')
        self.__transaction_cost = value        

    @property
    def borrow_cost_bps(self) -> float:
        """The estimated borrow fee in bps to short the position or position set."""
        return self.__borrow_cost_bps

    @borrow_cost_bps.setter
    def borrow_cost_bps(self, value: float):
        self._property_changed('borrow_cost_bps')
        self.__borrow_cost_bps = value        

    @property
    def volatility(self) -> float:
        """Annualized ex-ante risk a percentage of your portfolio's notional."""
        return self.__volatility

    @volatility.setter
    def volatility(self, value: float):
        self._property_changed('volatility')
        self.__volatility = value        

    @property
    def max_drawdown(self) -> float:
        """Maximum loss from a peak to a trough within the specified dates."""
        return self.__max_drawdown

    @max_drawdown.setter
    def max_drawdown(self, value: float):
        self._property_changed('max_drawdown')
        self.__max_drawdown = value        

    @property
    def net_exposure(self) -> float:
        """Combined exposure of long and short positions."""
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: float):
        self._property_changed('net_exposure')
        self.__net_exposure = value        

    @property
    def gross_exposure(self) -> float:
        """Combined exposure of long and short positions."""
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: float):
        self._property_changed('gross_exposure')
        self.__gross_exposure = value        

    @property
    def long_exposure(self) -> float:
        """Long exposure of the position set."""
        return self.__long_exposure

    @long_exposure.setter
    def long_exposure(self, value: float):
        self._property_changed('long_exposure')
        self.__long_exposure = value        

    @property
    def short_exposure(self) -> float:
        """Short exposure of the position set."""
        return self.__short_exposure

    @short_exposure.setter
    def short_exposure(self, value: float):
        self._property_changed('short_exposure')
        self.__short_exposure = value        

    @property
    def tracking_error(self) -> float:
        """Standard deviation of the difference in the portfolio and benchmark returns over
           time."""
        return self.__tracking_error

    @tracking_error.setter
    def tracking_error(self, value: float):
        self._property_changed('tracking_error')
        self.__tracking_error = value        

    @property
    def correlation(self) -> float:
        """Max 44 day rolling correlation."""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self._property_changed('correlation')
        self.__correlation = value        

    @property
    def exposure_overlap_with_target(self) -> float:
        """Overlapping exposure with the target portfolio."""
        return self.__exposure_overlap_with_target

    @exposure_overlap_with_target.setter
    def exposure_overlap_with_target(self, value: float):
        self._property_changed('exposure_overlap_with_target')
        self.__exposure_overlap_with_target = value        

    @property
    def total_pnl(self) -> float:
        """Total PnL of the position set over the backtest period."""
        return self.__total_pnl

    @total_pnl.setter
    def total_pnl(self, value: float):
        self._property_changed('total_pnl')
        self.__total_pnl = value        

    @property
    def turnover_percentage(self) -> float:
        """Turnover value of the hedge with the turnover portfolio."""
        return self.__turnover_percentage

    @turnover_percentage.setter
    def turnover_percentage(self, value: float):
        self._property_changed('turnover_percentage')
        self.__turnover_percentage = value        


class HedgeBenchmark(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        cumulative_pnl: Tuple[Tuple[Union[datetime.date, float], ...], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.cumulative_pnl = cumulative_pnl
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def cumulative_pnl(self) -> Tuple[Tuple[Union[datetime.date, float], ...], ...]:
        """An array of tuples that represent values in a time series."""
        return self.__cumulative_pnl

    @cumulative_pnl.setter
    def cumulative_pnl(self, value: Tuple[Tuple[Union[datetime.date, float], ...], ...]):
        self._property_changed('cumulative_pnl')
        self.__cumulative_pnl = value        


class PerformanceHedgeResult(Base):
        
    """Result of a performance replication hedge."""

    @camel_case_translate
    def __init__(
        self,
        target: dict,
        hedge: dict = None,
        hedged_target: dict = None,
        benchmarks: Tuple[dict, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.target = target
        self.hedge = hedge
        self.hedged_target = hedged_target
        self.benchmarks = benchmarks
        self.name = name

    @property
    def target(self) -> dict:
        """Statistics of the target."""
        return self.__target

    @target.setter
    def target(self, value: dict):
        self._property_changed('target')
        self.__target = value        

    @property
    def hedge(self) -> dict:
        """Statistics of the portfolio of assets making up the hedge."""
        return self.__hedge

    @hedge.setter
    def hedge(self, value: dict):
        self._property_changed('hedge')
        self.__hedge = value        

    @property
    def hedged_target(self) -> dict:
        """Statistics of the portfolio resulting from combining the target and hedge
           portfolios."""
        return self.__hedged_target

    @hedged_target.setter
    def hedged_target(self, value: dict):
        self._property_changed('hedged_target')
        self.__hedged_target = value        

    @property
    def benchmarks(self) -> Tuple[dict, ...]:
        """Benchmarks compared against the target."""
        return self.__benchmarks

    @benchmarks.setter
    def benchmarks(self, value: Tuple[dict, ...]):
        self._property_changed('benchmarks')
        self.__benchmarks = value        


class FactorHedgeResult(Base):
        
    """Result of a hedge calculation with an objective to minimize factor risk."""

    @camel_case_translate
    def __init__(
        self,
        hedge: FactorHedgerResultPositions,
        hedged_target: FactorHedgerResultPositions,
        target: FactorHedgerResultPositions = None,
        name: str = None
    ):        
        super().__init__()
        self.target = target
        self.hedge = hedge
        self.hedged_target = hedged_target
        self.name = name

    @property
    def target(self) -> FactorHedgerResultPositions:
        """Statistics of the target portfolio."""
        return self.__target

    @target.setter
    def target(self, value: FactorHedgerResultPositions):
        self._property_changed('target')
        self.__target = value        

    @property
    def hedge(self) -> FactorHedgerResultPositions:
        """Statistics of the portfolio of assets making up the hedge."""
        return self.__hedge

    @hedge.setter
    def hedge(self, value: FactorHedgerResultPositions):
        self._property_changed('hedge')
        self.__hedge = value        

    @property
    def hedged_target(self) -> FactorHedgerResultPositions:
        """Statistics of the portfolio resulting from combining the target and hedge
           portfolios."""
        return self.__hedged_target

    @hedged_target.setter
    def hedged_target(self, value: FactorHedgerResultPositions):
        self._property_changed('hedged_target')
        self.__hedged_target = value        


class HedgerComparison(Base):
        
    """Comparison of a hedge."""

    @camel_case_translate
    def __init__(
        self,
        entity_id: str,
        entity_type: Union[HedgerComparisonType, str],
        hedge_properties: HedgerComparisonProperties,
        result: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.hedge_properties = hedge_properties
        self.result = result
        self.name = name

    @property
    def entity_id(self) -> str:
        """Id of the marquee entity"""
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, value: str):
        self._property_changed('entity_id')
        self.__entity_id = value        

    @property
    def entity_type(self) -> Union[HedgerComparisonType, str]:
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[HedgerComparisonType, str]):
        self._property_changed('entity_type')
        self.__entity_type = get_enum_value(HedgerComparisonType, value)        

    @property
    def hedge_properties(self) -> HedgerComparisonProperties:
        """properties used to hedge the comparison."""
        return self.__hedge_properties

    @hedge_properties.setter
    def hedge_properties(self, value: HedgerComparisonProperties):
        self._property_changed('hedge_properties')
        self.__hedge_properties = value        

    @property
    def result(self) -> dict:
        """Result of the hedge comparison."""
        return self.__result

    @result.setter
    def result(self, value: dict):
        self._property_changed('result')
        self.__result = value        


class Target(Base):
        
    """The asset id, portfolio id, or set of positions that make up the hedge target."""

    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        positions: Tuple[Position, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.positions = positions
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
    def positions(self) -> Tuple[Position, ...]:
        """Array of quantity position objects."""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[Position, ...]):
        self._property_changed('positions')
        self.__positions = value        


class FactorHedgeParameters(Base):
        
    """Parameters for a hedge calculation to minimize factor risk."""

    @camel_case_translate
    def __init__(
        self,
        risk_model: str,
        target_notional: float,
        hedge_notional: float,
        hedge_target: Target,
        hedge_universe: FactorHedgeUniverse,
        hedge_date: datetime.date,
        backtest_start_date: datetime.date,
        backtest_end_date: datetime.date,
        fx_hedged: bool = None,
        exclude_target_assets: bool = None,
        exclude_corporate_actions: bool = None,
        exclude_corporate_actions_types: Tuple[Union[CorporateActionsTypes, str], ...] = None,
        exclude_hard_to_borrow_assets: bool = None,
        exclude_restricted_assets: bool = None,
        max_adv_percentage: float = None,
        explode_universe: bool = None,
        min_names: float = None,
        max_names: float = None,
        min_weight: float = None,
        max_weight: float = None,
        min_market_cap: float = None,
        max_market_cap: float = None,
        market_participation_rate: float = 10,
        asset_constraints: Tuple[AssetConstraint, ...] = None,
        factor_constraints: Tuple[FactorConstraint, ...] = None,
        classification_constraints: Tuple[ClassificationConstraint, ...] = None,
        esg_constraints: Tuple[ESGConstraint, ...] = None,
        constraint_priority_settings: FactorHedgerConstraintPrioritySettings = None,
        comparisons: Tuple[HedgerComparison, ...] = None,
        turnover_portfolio_id: str = None,
        max_turnover_percentage: float = None,
        name: str = None
    ):        
        super().__init__()
        self.risk_model = risk_model
        self.hedge_target = hedge_target
        self.target_notional = target_notional
        self.hedge_notional = hedge_notional
        self.hedge_universe = hedge_universe
        self.hedge_date = hedge_date
        self.backtest_start_date = backtest_start_date
        self.backtest_end_date = backtest_end_date
        self.fx_hedged = fx_hedged
        self.exclude_target_assets = exclude_target_assets
        self.exclude_corporate_actions = exclude_corporate_actions
        self.exclude_corporate_actions_types = exclude_corporate_actions_types
        self.exclude_hard_to_borrow_assets = exclude_hard_to_borrow_assets
        self.exclude_restricted_assets = exclude_restricted_assets
        self.max_adv_percentage = max_adv_percentage
        self.explode_universe = explode_universe
        self.min_names = min_names
        self.max_names = max_names
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.min_market_cap = min_market_cap
        self.max_market_cap = max_market_cap
        self.market_participation_rate = market_participation_rate
        self.asset_constraints = asset_constraints
        self.factor_constraints = factor_constraints
        self.classification_constraints = classification_constraints
        self.esg_constraints = esg_constraints
        self.constraint_priority_settings = constraint_priority_settings
        self.comparisons = comparisons
        self.turnover_portfolio_id = turnover_portfolio_id
        self.max_turnover_percentage = max_turnover_percentage
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
    def hedge_target(self) -> Target:
        """The asset id, portfolio id, or set of positions that make up the hedge target."""
        return self.__hedge_target

    @hedge_target.setter
    def hedge_target(self, value: Target):
        self._property_changed('hedge_target')
        self.__hedge_target = value        

    @property
    def target_notional(self) -> float:
        """Notional value of the hedge target."""
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: float):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def hedge_notional(self) -> float:
        """Notional value of the hedge."""
        return self.__hedge_notional

    @hedge_notional.setter
    def hedge_notional(self, value: float):
        self._property_changed('hedge_notional')
        self.__hedge_notional = value        

    @property
    def hedge_universe(self) -> FactorHedgeUniverse:
        """Any combination of asset ids and bulk asset types that make up the universe."""
        return self.__hedge_universe

    @hedge_universe.setter
    def hedge_universe(self, value: FactorHedgeUniverse):
        self._property_changed('hedge_universe')
        self.__hedge_universe = value        

    @property
    def hedge_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__hedge_date

    @hedge_date.setter
    def hedge_date(self, value: datetime.date):
        self._property_changed('hedge_date')
        self.__hedge_date = value        

    @property
    def backtest_start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__backtest_start_date

    @backtest_start_date.setter
    def backtest_start_date(self, value: datetime.date):
        self._property_changed('backtest_start_date')
        self.__backtest_start_date = value        

    @property
    def backtest_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__backtest_end_date

    @backtest_end_date.setter
    def backtest_end_date(self, value: datetime.date):
        self._property_changed('backtest_end_date')
        self.__backtest_end_date = value        

    @property
    def fx_hedged(self) -> bool:
        """Assume portfolio is FX Hedged."""
        return self.__fx_hedged

    @fx_hedged.setter
    def fx_hedged(self, value: bool):
        self._property_changed('fx_hedged')
        self.__fx_hedged = value        

    @property
    def exclude_target_assets(self) -> bool:
        """Exclude assets in the target composition from being in the hedge."""
        return self.__exclude_target_assets

    @exclude_target_assets.setter
    def exclude_target_assets(self, value: bool):
        self._property_changed('exclude_target_assets')
        self.__exclude_target_assets = value        

    @property
    def exclude_corporate_actions(self) -> bool:
        """Exclude assets pending for corporate actions from being in the hedge. Default
           corporate action types excluded are Merges, Quote lot adjustments,
           Rights, Spinoffs, and Reorganizations."""
        return self.__exclude_corporate_actions

    @exclude_corporate_actions.setter
    def exclude_corporate_actions(self, value: bool):
        self._property_changed('exclude_corporate_actions')
        self.__exclude_corporate_actions = value        

    @property
    def exclude_corporate_actions_types(self) -> Tuple[Union[CorporateActionsTypes, str], ...]:
        """Set of of corporate actions to be excluded in the hedge"""
        return self.__exclude_corporate_actions_types

    @exclude_corporate_actions_types.setter
    def exclude_corporate_actions_types(self, value: Tuple[Union[CorporateActionsTypes, str], ...]):
        self._property_changed('exclude_corporate_actions_types')
        self.__exclude_corporate_actions_types = value        

    @property
    def exclude_hard_to_borrow_assets(self) -> bool:
        """Whether hard to borrow assets should be excluded in the universe or not. True
           for exclude."""
        return self.__exclude_hard_to_borrow_assets

    @exclude_hard_to_borrow_assets.setter
    def exclude_hard_to_borrow_assets(self, value: bool):
        self._property_changed('exclude_hard_to_borrow_assets')
        self.__exclude_hard_to_borrow_assets = value        

    @property
    def exclude_restricted_assets(self) -> bool:
        """Whether to include assets in restricted trading lists or not."""
        return self.__exclude_restricted_assets

    @exclude_restricted_assets.setter
    def exclude_restricted_assets(self, value: bool):
        self._property_changed('exclude_restricted_assets')
        self.__exclude_restricted_assets = value        

    @property
    def max_adv_percentage(self) -> float:
        """Maximum percentage notional to average daily dollar volume allowed for any hedge
           constituent."""
        return self.__max_adv_percentage

    @max_adv_percentage.setter
    def max_adv_percentage(self, value: float):
        self._property_changed('max_adv_percentage')
        self.__max_adv_percentage = value        

    @property
    def explode_universe(self) -> bool:
        """Explode the assets in the universe into their underliers to be used as the hedge
           universe."""
        return self.__explode_universe

    @explode_universe.setter
    def explode_universe(self, value: bool):
        self._property_changed('explode_universe')
        self.__explode_universe = value        

    @property
    def min_names(self) -> float:
        """Minimum number of assets allowed in the hedge."""
        return self.__min_names

    @min_names.setter
    def min_names(self, value: float):
        self._property_changed('min_names')
        self.__min_names = value        

    @property
    def max_names(self) -> float:
        """Maximum number of assets allowed in the hedge."""
        return self.__max_names

    @max_names.setter
    def max_names(self, value: float):
        self._property_changed('max_names')
        self.__max_names = value        

    @property
    def min_weight(self) -> float:
        """Minimum weight of any constituent in hedge."""
        return self.__min_weight

    @min_weight.setter
    def min_weight(self, value: float):
        self._property_changed('min_weight')
        self.__min_weight = value        

    @property
    def max_weight(self) -> float:
        """Maximum weight of any constituent in hedge."""
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, value: float):
        self._property_changed('max_weight')
        self.__max_weight = value        

    @property
    def min_market_cap(self) -> float:
        """Lowest market cap allowed for any hedge constituent."""
        return self.__min_market_cap

    @min_market_cap.setter
    def min_market_cap(self, value: float):
        self._property_changed('min_market_cap')
        self.__min_market_cap = value        

    @property
    def max_market_cap(self) -> float:
        """Highest market cap allowed for any hedge constituent."""
        return self.__max_market_cap

    @max_market_cap.setter
    def max_market_cap(self, value: float):
        self._property_changed('max_market_cap')
        self.__max_market_cap = value        

    @property
    def market_participation_rate(self) -> float:
        """Maximum market participation rate used to estimate the cost of trading a
           portfolio of stocks. This does not effect the optimization."""
        return self.__market_participation_rate

    @market_participation_rate.setter
    def market_participation_rate(self, value: float):
        self._property_changed('market_participation_rate')
        self.__market_participation_rate = value        

    @property
    def asset_constraints(self) -> Tuple[AssetConstraint, ...]:
        """Constraints to be applied to specific assets in the hedge universe."""
        return self.__asset_constraints

    @asset_constraints.setter
    def asset_constraints(self, value: Tuple[AssetConstraint, ...]):
        self._property_changed('asset_constraints')
        self.__asset_constraints = value        

    @property
    def factor_constraints(self) -> Tuple[FactorConstraint, ...]:
        """Constraints to be applied to specific risk model factors in the hedge."""
        return self.__factor_constraints

    @factor_constraints.setter
    def factor_constraints(self, value: Tuple[FactorConstraint, ...]):
        self._property_changed('factor_constraints')
        self.__factor_constraints = value        

    @property
    def classification_constraints(self) -> Tuple[ClassificationConstraint, ...]:
        """Constraints to be applied to assets in the universe that are classified by the
           industry, sector, country, or region in the constraint."""
        return self.__classification_constraints

    @classification_constraints.setter
    def classification_constraints(self, value: Tuple[ClassificationConstraint, ...]):
        self._property_changed('classification_constraints')
        self.__classification_constraints = value        

    @property
    def esg_constraints(self) -> Tuple[ESGConstraint, ...]:
        """Constraints to be applied to assets in the universe based off of their ESG
           metric values in the ESG_HEADLINE_METRICS dataset."""
        return self.__esg_constraints

    @esg_constraints.setter
    def esg_constraints(self, value: Tuple[ESGConstraint, ...]):
        self._property_changed('esg_constraints')
        self.__esg_constraints = value        

    @property
    def constraint_priority_settings(self) -> FactorHedgerConstraintPrioritySettings:
        """Specify the priority of constraints"""
        return self.__constraint_priority_settings

    @constraint_priority_settings.setter
    def constraint_priority_settings(self, value: FactorHedgerConstraintPrioritySettings):
        self._property_changed('constraint_priority_settings')
        self.__constraint_priority_settings = value        

    @property
    def comparisons(self) -> Tuple[HedgerComparison, ...]:
        """Specifies the list of assets, hedges, or portfolios to compare the hedge
           against."""
        return self.__comparisons

    @comparisons.setter
    def comparisons(self, value: Tuple[HedgerComparison, ...]):
        self._property_changed('comparisons')
        self.__comparisons = value        

    @property
    def turnover_portfolio_id(self) -> str:
        """Specifies the hedge, basket or a portfolio which is used to restrict the of the
           optimized hedge with max turnover percentage."""
        return self.__turnover_portfolio_id

    @turnover_portfolio_id.setter
    def turnover_portfolio_id(self, value: str):
        self._property_changed('turnover_portfolio_id')
        self.__turnover_portfolio_id = value        

    @property
    def max_turnover_percentage(self) -> float:
        """Maximum value of turnover allowed for the hedge, relative to the turnover
           portfolio."""
        return self.__max_turnover_percentage

    @max_turnover_percentage.setter
    def max_turnover_percentage(self, value: float):
        self._property_changed('max_turnover_percentage')
        self.__max_turnover_percentage = value        


class PerformanceHedgeParameters(Base):
        
    """Parameters for a performance replication hedge calculation."""

    @camel_case_translate
    def __init__(
        self,
        hedge_target: Target,
        universe: Tuple[str, ...],
        notional: float,
        observation_start_date: datetime.date,
        observation_end_date: datetime.date,
        backtest_start_date: datetime.date = None,
        backtest_end_date: datetime.date = None,
        sampling_period: str = 'Weekly',
        max_leverage: float = None,
        percentage_in_cash: float = None,
        explode_universe: bool = None,
        exclude_target_assets: bool = None,
        exclude_corporate_actions: bool = None,
        exclude_corporate_actions_types: Tuple[Union[CorporateActionsTypes, str], ...] = None,
        exclude_hard_to_borrow_assets: bool = None,
        exclude_restricted_assets: bool = None,
        max_adv_percentage: float = None,
        max_return_deviation: float = None,
        max_weight: float = None,
        min_market_cap: float = None,
        max_market_cap: float = None,
        market_participation_rate: float = 10,
        asset_constraints: Tuple[AssetConstraint, ...] = None,
        classification_constraints: Tuple[ClassificationConstraint, ...] = None,
        esg_constraints: Tuple[ESGConstraint, ...] = None,
        benchmarks: Tuple[str, ...] = None,
        use_machine_learning: bool = False,
        lasso_weight: float = None,
        ridge_weight: float = None,
        name: str = None
    ):        
        super().__init__()
        self.hedge_target = hedge_target
        self.universe = universe
        self.observation_start_date = observation_start_date
        self.observation_end_date = observation_end_date
        self.backtest_start_date = backtest_start_date
        self.backtest_end_date = backtest_end_date
        self.sampling_period = sampling_period
        self.notional = notional
        self.max_leverage = max_leverage
        self.percentage_in_cash = percentage_in_cash
        self.explode_universe = explode_universe
        self.exclude_target_assets = exclude_target_assets
        self.exclude_corporate_actions = exclude_corporate_actions
        self.exclude_corporate_actions_types = exclude_corporate_actions_types
        self.exclude_hard_to_borrow_assets = exclude_hard_to_borrow_assets
        self.exclude_restricted_assets = exclude_restricted_assets
        self.max_adv_percentage = max_adv_percentage
        self.max_return_deviation = max_return_deviation
        self.max_weight = max_weight
        self.min_market_cap = min_market_cap
        self.max_market_cap = max_market_cap
        self.market_participation_rate = market_participation_rate
        self.asset_constraints = asset_constraints
        self.classification_constraints = classification_constraints
        self.esg_constraints = esg_constraints
        self.benchmarks = benchmarks
        self.use_machine_learning = use_machine_learning
        self.lasso_weight = lasso_weight
        self.ridge_weight = ridge_weight
        self.name = name

    @property
    def hedge_target(self) -> Target:
        """The asset id, portfolio id, or set of positions that make up the hedge target."""
        return self.__hedge_target

    @hedge_target.setter
    def hedge_target(self, value: Target):
        self._property_changed('hedge_target')
        self.__hedge_target = value        

    @property
    def universe(self) -> Tuple[str, ...]:
        """Set of marquee unique asset identifiers that make up the hedge universe. Any
           identifiers that are not for single stocks will be exploded into
           their underliers."""
        return self.__universe

    @universe.setter
    def universe(self, value: Tuple[str, ...]):
        self._property_changed('universe')
        self.__universe = value        

    @property
    def observation_start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__observation_start_date

    @observation_start_date.setter
    def observation_start_date(self, value: datetime.date):
        self._property_changed('observation_start_date')
        self.__observation_start_date = value        

    @property
    def observation_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__observation_end_date

    @observation_end_date.setter
    def observation_end_date(self, value: datetime.date):
        self._property_changed('observation_end_date')
        self.__observation_end_date = value        

    @property
    def backtest_start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__backtest_start_date

    @backtest_start_date.setter
    def backtest_start_date(self, value: datetime.date):
        self._property_changed('backtest_start_date')
        self.__backtest_start_date = value        

    @property
    def backtest_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__backtest_end_date

    @backtest_end_date.setter
    def backtest_end_date(self, value: datetime.date):
        self._property_changed('backtest_end_date')
        self.__backtest_end_date = value        

    @property
    def sampling_period(self) -> str:
        """The length of time in between return samples."""
        return self.__sampling_period

    @sampling_period.setter
    def sampling_period(self, value: str):
        self._property_changed('sampling_period')
        self.__sampling_period = value        

    @property
    def notional(self) -> float:
        """Notional value of the hedge target."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def max_leverage(self) -> float:
        """Maximum percentage of the notional that can be used to hedge."""
        return self.__max_leverage

    @max_leverage.setter
    def max_leverage(self, value: float):
        self._property_changed('max_leverage')
        self.__max_leverage = value        

    @property
    def percentage_in_cash(self) -> float:
        """Percentage of the hedge notional that will be in cash."""
        return self.__percentage_in_cash

    @percentage_in_cash.setter
    def percentage_in_cash(self, value: float):
        self._property_changed('percentage_in_cash')
        self.__percentage_in_cash = value        

    @property
    def explode_universe(self) -> bool:
        """Explode the assets in the universe into their underliers to be used as the hedge
           universe."""
        return self.__explode_universe

    @explode_universe.setter
    def explode_universe(self, value: bool):
        self._property_changed('explode_universe')
        self.__explode_universe = value        

    @property
    def exclude_target_assets(self) -> bool:
        """Exclude assets in the target composition from being in the hedge."""
        return self.__exclude_target_assets

    @exclude_target_assets.setter
    def exclude_target_assets(self, value: bool):
        self._property_changed('exclude_target_assets')
        self.__exclude_target_assets = value        

    @property
    def exclude_corporate_actions(self) -> bool:
        """Exclude assets pending for corporate actions from being in the hedge"""
        return self.__exclude_corporate_actions

    @exclude_corporate_actions.setter
    def exclude_corporate_actions(self, value: bool):
        self._property_changed('exclude_corporate_actions')
        self.__exclude_corporate_actions = value        

    @property
    def exclude_corporate_actions_types(self) -> Tuple[Union[CorporateActionsTypes, str], ...]:
        """Set of of corporate actions to be excluded in the hedge"""
        return self.__exclude_corporate_actions_types

    @exclude_corporate_actions_types.setter
    def exclude_corporate_actions_types(self, value: Tuple[Union[CorporateActionsTypes, str], ...]):
        self._property_changed('exclude_corporate_actions_types')
        self.__exclude_corporate_actions_types = value        

    @property
    def exclude_hard_to_borrow_assets(self) -> bool:
        """Whether hard to borrow assets should be excluded in the universe or not. True
           for exclude."""
        return self.__exclude_hard_to_borrow_assets

    @exclude_hard_to_borrow_assets.setter
    def exclude_hard_to_borrow_assets(self, value: bool):
        self._property_changed('exclude_hard_to_borrow_assets')
        self.__exclude_hard_to_borrow_assets = value        

    @property
    def exclude_restricted_assets(self) -> bool:
        """Whether to include assets in restricted trading lists or not."""
        return self.__exclude_restricted_assets

    @exclude_restricted_assets.setter
    def exclude_restricted_assets(self, value: bool):
        self._property_changed('exclude_restricted_assets')
        self.__exclude_restricted_assets = value        

    @property
    def max_adv_percentage(self) -> float:
        """Maximum percentage notional to average daily dollar volume allowed for any hedge
           constituent."""
        return self.__max_adv_percentage

    @max_adv_percentage.setter
    def max_adv_percentage(self, value: float):
        self._property_changed('max_adv_percentage')
        self.__max_adv_percentage = value        

    @property
    def max_return_deviation(self) -> float:
        """Maximum percentage difference in annualized return between the target and the
           hedge result."""
        return self.__max_return_deviation

    @max_return_deviation.setter
    def max_return_deviation(self, value: float):
        self._property_changed('max_return_deviation')
        self.__max_return_deviation = value        

    @property
    def max_weight(self) -> float:
        """Maximum weight of any constituent in hedge."""
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, value: float):
        self._property_changed('max_weight')
        self.__max_weight = value        

    @property
    def min_market_cap(self) -> float:
        """Lowest market cap allowed for any hedge constituent."""
        return self.__min_market_cap

    @min_market_cap.setter
    def min_market_cap(self, value: float):
        self._property_changed('min_market_cap')
        self.__min_market_cap = value        

    @property
    def max_market_cap(self) -> float:
        """Highest market cap allowed for any hedge constituent."""
        return self.__max_market_cap

    @max_market_cap.setter
    def max_market_cap(self, value: float):
        self._property_changed('max_market_cap')
        self.__max_market_cap = value        

    @property
    def market_participation_rate(self) -> float:
        """Maximum market participation rate used to estimate the cost of trading a
           portfolio of stocks. This does not effect the optimization."""
        return self.__market_participation_rate

    @market_participation_rate.setter
    def market_participation_rate(self, value: float):
        self._property_changed('market_participation_rate')
        self.__market_participation_rate = value        

    @property
    def asset_constraints(self) -> Tuple[AssetConstraint, ...]:
        """Constraints to be applied to specific assets in the hedge universe."""
        return self.__asset_constraints

    @asset_constraints.setter
    def asset_constraints(self, value: Tuple[AssetConstraint, ...]):
        self._property_changed('asset_constraints')
        self.__asset_constraints = value        

    @property
    def classification_constraints(self) -> Tuple[ClassificationConstraint, ...]:
        """Constraints to be applied to assets in the universe that are classified by the
           industry, sector, country, or region in the constraint."""
        return self.__classification_constraints

    @classification_constraints.setter
    def classification_constraints(self, value: Tuple[ClassificationConstraint, ...]):
        self._property_changed('classification_constraints')
        self.__classification_constraints = value        

    @property
    def esg_constraints(self) -> Tuple[ESGConstraint, ...]:
        """Constraints to be applied to assets in the universe based off of their ESG
           metric values in the ESG_HEADLINE_METRICS dataset."""
        return self.__esg_constraints

    @esg_constraints.setter
    def esg_constraints(self, value: Tuple[ESGConstraint, ...]):
        self._property_changed('esg_constraints')
        self.__esg_constraints = value        

    @property
    def benchmarks(self) -> Tuple[str, ...]:
        """Marquee unique identifiers of assets to be used as benchmarks."""
        return self.__benchmarks

    @benchmarks.setter
    def benchmarks(self, value: Tuple[str, ...]):
        self._property_changed('benchmarks')
        self.__benchmarks = value        

    @property
    def use_machine_learning(self) -> bool:
        """Use Machine learning."""
        return self.__use_machine_learning

    @use_machine_learning.setter
    def use_machine_learning(self, value: bool):
        self._property_changed('use_machine_learning')
        self.__use_machine_learning = value        

    @property
    def lasso_weight(self) -> float:
        """Value of the lasso hyperparameter for machine learning hedges."""
        return self.__lasso_weight

    @lasso_weight.setter
    def lasso_weight(self, value: float):
        self._property_changed('lasso_weight')
        self.__lasso_weight = value        

    @property
    def ridge_weight(self) -> float:
        """Value of the ridge hyperparameter for machine learning hedges"""
        return self.__ridge_weight

    @ridge_weight.setter
    def ridge_weight(self, value: float):
        self._property_changed('ridge_weight')
        self.__ridge_weight = value        


class Hedge(Base):
        
    """Object representation of a Hedge"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        parameters: dict,
        id_: str = None,
        owner_id: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        entitlements: Entitlements = None,
        tags: Tuple[str, ...] = None,
        description: str = None,
        objective: Union[HedgeObjective, str] = None,
        result: dict = None,
        comparison_results: Tuple[HedgerComparison, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.owner_id = owner_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.entitlements = entitlements
        self.tags = tags
        self.name = name
        self.description = description
        self.objective = objective
        self.parameters = parameters
        self.result = result
        self.comparison_results = comparison_results

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

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
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def name(self) -> str:
        """Display name of the hedge"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Free text description of a Hedge"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def objective(self) -> Union[HedgeObjective, str]:
        """The objective of the hedge."""
        return self.__objective

    @objective.setter
    def objective(self, value: Union[HedgeObjective, str]):
        self._property_changed('objective')
        self.__objective = get_enum_value(HedgeObjective, value)        

    @property
    def parameters(self) -> dict:
        """The parameters used in the hedge calculation."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def result(self) -> dict:
        """Result of the hedge."""
        return self.__result

    @result.setter
    def result(self, value: dict):
        self._property_changed('result')
        self.__result = value        

    @property
    def comparison_results(self) -> Tuple[HedgerComparison, ...]:
        """Results of the comparisons."""
        return self.__comparison_results

    @comparison_results.setter
    def comparison_results(self, value: Tuple[HedgerComparison, ...]):
        self._property_changed('comparison_results')
        self.__comparison_results = value        
