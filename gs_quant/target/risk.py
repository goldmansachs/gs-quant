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
from typing import Any, Iterable, Union
from enum import Enum
from gs_quant.api.base import EnumBase, Base


class RiskMeasureUnit(EnumBase, Enum):    
    
    """The unit of change of underlying in the risk computation."""

    Percent = 'Percent'
    Dollar = 'Dollar'
    BPS = 'BPS'
    
    def __repr__(self):
        return self.value


class RiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Delta = 'Delta'
    Dollar_Price = 'Dollar Price'
    DV01 = 'DV01'
    Gamma = 'Gamma'
    OAS = 'OAS'
    PNL = 'PNL'
    PV = 'PV'
    Theta = 'Theta'
    Vanna = 'Vanna'
    Vega = 'Vega'
    
    def __repr__(self):
        return self.value


class RiskRequest(Base):
        
    """Object representation of a risk calculation request"""
       
    def __init__(self, positions: Iterable['RiskPosition'], measures: Iterable['RiskMeasure'], asOf, waitForResults: bool = False, userId: Union[str, str] = None):
        super().__init__()
        self.__positions = positions
        self.__measures = measures
        self.__asOf = asOf
        self.__waitForResults = waitForResults
        self.__userId = userId

    @property
    def positions(self) -> Iterable['RiskPosition']:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Iterable['RiskPosition']):
        self.__positions = value
        self._property_changed('positions')        

    @property
    def measures(self) -> Iterable['RiskMeasure']:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta', 'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Iterable['RiskMeasure']):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def asOf(self):
        """The date or time for which to run the calculation and snap market data"""
        return self.__asOf

    @asOf.setter
    def asOf(self, value):
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

    @property
    def userId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__userId

    @userId.setter
    def userId(self, value: Union[str, str]):
        self.__userId = value
        self._property_changed('userId')        


class RiskMeasure(Base):
        
    """The measure to perform risk on. Each risk measure consists of an asset class, a measure type, and a unit."""
       
    def __init__(self, assetClass: Union['AssetClass', str] = None, measureType: Union['RiskMeasureType', str] = None, unit: Union['RiskMeasureUnit', str] = None):
        super().__init__()
        self.__assetClass = assetClass
        self.__measureType = measureType
        self.__unit = unit

    @property
    def assetClass(self) -> Union['AssetClass', str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union['AssetClass', str]):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def measureType(self) -> Union['RiskMeasureType', str]:
        """The type of measure to perform risk on. e.g. Greeks"""
        return self.__measureType

    @measureType.setter
    def measureType(self, value: Union['RiskMeasureType', str]):
        self.__measureType = value
        self._property_changed('measureType')        

    @property
    def unit(self) -> Union['RiskMeasureUnit', str]:
        """The unit of change of underlying in the risk computation."""
        return self.__unit

    @unit.setter
    def unit(self, value: Union['RiskMeasureUnit', str]):
        self.__unit = value
        self._property_changed('unit')        


class RiskPosition(Base):
               
    def __init__(self, instrument: Union['Priceable', str], quantity: float):
        super().__init__()
        self.__instrument = instrument
        self.__quantity = quantity

    @property
    def instrument(self) -> Union['Priceable', str]:
        """Instrument or Id  
To specify a Marquee asset use the asset Id.
For listed products use an XRef, e.g. { 'bid': 'NGZ19 Comdty' }, { 'isin': 'US912810SD19' }.
To specify an instrument use one of the listed types"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: Union['Priceable', str]):
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


class CoordinatesResponse(Base):
               
    def __init__(self, results: Iterable['MarketDataCoordinate']):
        super().__init__()
        self.__results = results

    @property
    def results(self) -> Iterable['MarketDataCoordinate']:
        return self.__results

    @results.setter
    def results(self, value: Iterable['MarketDataCoordinate']):
        self.__results = value
        self._property_changed('results')        


class MarketDataCoordinate(Base):
        
    """Object representation of a market data coordinate"""
       
    def __init__(self, marketDataType, assetId: Union[str, str] = None, pointClass=None, point: str = None, field: str = None):
        super().__init__()
        self.__marketDataType = marketDataType
        self.__assetId = assetId
        self.__pointClass = pointClass
        self.__point = point
        self.__field = field

    @property
    def marketDataType(self):
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def assetId(self) -> Union[str, str]:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def pointClass(self):
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def point(self) -> str:
        """The specific point, e.g. 3m, 10y,11y, Dec19"""
        return self.__point

    @point.setter
    def point(self, value: str):
        self.__point = value
        self._property_changed('point')        

    @property
    def field(self) -> str:
        """The specific field: bid, mid, rate etc"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        


class CoordinatesRequest(Base):
               
    def __init__(self, asOf: datetime.date, instruments: Iterable['Priceable']):
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
    def instruments(self) -> Iterable['Priceable']:
        return self.__instruments

    @instruments.setter
    def instruments(self, value: Iterable['Priceable']):
        self.__instruments = value
        self._property_changed('instruments')        
