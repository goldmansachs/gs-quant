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
from gs_quant.base import EnumBase, Base, get_enum_value


class RiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Delta = 'Delta'
    Dollar_Price = 'Dollar Price'
    Forward_Price = 'Forward Price'
    Price = 'Price'
    DV01 = 'DV01'
    Gamma = 'Gamma'
    OAS = 'OAS'
    PNL = 'PNL'
    PV = 'PV'
    Theta = 'Theta'
    Vanna = 'Vanna'
    Vega = 'Vega'
    Annual_Implied_Volatility = 'Annual Implied Volatility'
    Annual_ATMF_Implied_Volatility = 'Annual ATMF Implied Volatility'
    Daily_Implied_Volatility = 'Daily Implied Volatility'
    Resolved_Instrument_Values = 'Resolved Instrument Values'
    
    def __repr__(self):
        return self.value


class RiskMeasureUnit(EnumBase, Enum):    
    
    """The unit of change of underlying in the risk computation."""

    Percent = 'Percent'
    Dollar = 'Dollar'
    BPS = 'BPS'
    
    def __repr__(self):
        return self.value


class RiskPosition(Base):
               
    def __init__(self, instrument: Priceable, quantity: float):
        super().__init__()
        self.__instrument = instrument
        self.__quantity = quantity

    @property
    def instrument(self) -> Priceable:
        """Instrument or Id  
To specify a Marquee asset use the asset Id.
For listed products use an XRef, e.g. { 'bid': 'NGZ19 Comdty' }, { 'isin': 'US912810SD19' }.
To specify an instrument use one of the listed types"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: Priceable):
        self.__instrument = value
        self._property_changed('instrument')        

    @property
    def quantity(self) -> float:
        """Quantity of instrument"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        


class CoordinatesRequest(Base):
               
    def __init__(self, asOf: datetime.date, instruments: Tuple[Priceable, ...]):
        super().__init__()
        self.__asOf = asOf
        self.__instruments = instruments

    @property
    def asOf(self) -> datetime.date:
        return self.__asOf

    @asOf.setter
    def asOf(self, value: datetime.date):
        self.__asOf = value
        self._property_changed('asOf')        

    @property
    def instruments(self) -> Tuple[Priceable, ...]:
        return self.__instruments

    @instruments.setter
    def instruments(self, value: Tuple[Priceable, ...]):
        self.__instruments = value
        self._property_changed('instruments')        


class CoordinatesResponse(Base):
               
    def __init__(self, results: Tuple[MarketDataCoordinate, ...]):
        super().__init__()
        self.__results = results

    @property
    def results(self) -> Tuple[MarketDataCoordinate, ...]:
        return self.__results

    @results.setter
    def results(self, value: Tuple[MarketDataCoordinate, ...]):
        self.__results = value
        self._property_changed('results')        


class RiskMeasure(Base):
        
    """The measure to perform risk on. Each risk measure consists of an asset class, a measure type, and a unit."""
       
    def __init__(self, assetClass: Union[AssetClass, str] = None, measureType: Union[RiskMeasureType, str] = None, unit: Union[RiskMeasureUnit, str] = None):
        super().__init__()
        self.__assetClass = assetClass if isinstance(assetClass, AssetClass) else get_enum_value(AssetClass, assetClass)
        self.__measureType = measureType if isinstance(measureType, RiskMeasureType) else get_enum_value(RiskMeasureType, measureType)
        self.__unit = unit if isinstance(unit, RiskMeasureUnit) else get_enum_value(RiskMeasureUnit, unit)

    @property
    def assetClass(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[AssetClass, str]):
        self.__assetClass = value if isinstance(value, AssetClass) else get_enum_value(AssetClass, value)
        self._property_changed('assetClass')        

    @property
    def measureType(self) -> Union[RiskMeasureType, str]:
        """The type of measure to perform risk on. e.g. Greeks"""
        return self.__measureType

    @measureType.setter
    def measureType(self, value: Union[RiskMeasureType, str]):
        self.__measureType = value if isinstance(value, RiskMeasureType) else get_enum_value(RiskMeasureType, value)
        self._property_changed('measureType')        

    @property
    def unit(self) -> Union[RiskMeasureUnit, str]:
        """The unit of change of underlying in the risk computation."""
        return self.__unit

    @unit.setter
    def unit(self, value: Union[RiskMeasureUnit, str]):
        self.__unit = value if isinstance(value, RiskMeasureUnit) else get_enum_value(RiskMeasureUnit, value)
        self._property_changed('unit')        


class RiskRequest(Base):
        
    """Object representation of a risk calculation request"""
       
    def __init__(self, positions: Tuple[RiskPosition, ...], measures: Tuple[RiskMeasure, ...], asOf: Union[datetime.datetime, datetime.date], waitForResults: bool = False):
        super().__init__()
        self.__positions = positions
        self.__measures = measures
        self.__asOf = asOf
        self.__waitForResults = waitForResults

    @property
    def positions(self) -> Tuple[RiskPosition, ...]:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[RiskPosition, ...]):
        self.__positions = value
        self._property_changed('positions')        

    @property
    def measures(self) -> Tuple[RiskMeasure, ...]:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta', 'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[RiskMeasure, ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def asOf(self) -> Union[datetime.datetime, datetime.date]:
        """The date or time for which to run the calculation and snap market data"""
        return self.__asOf

    @asOf.setter
    def asOf(self, value: Union[datetime.datetime, datetime.date]):
        self.__asOf = value
        self._property_changed('asOf')        

    @property
    def waitForResults(self) -> bool:
        """For short-running requests this may be set to true and the results will be returned directly. If false, the response will contain the Id to retrieve the results"""
        return self.__waitForResults

    @waitForResults.setter
    def waitForResults(self, value: bool):
        self.__waitForResults = value
        self._property_changed('waitForResults')        
