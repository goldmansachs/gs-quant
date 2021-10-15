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
import calendar
import datetime
import functools
import json
import logging
import threading
import time
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from enum import auto
from functools import partial
from typing import Dict, Tuple, Generator, Iterable

import backoff
import cachetools
import pytz
from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.assets import GsAsset, AssetParameters, \
    AssetType as GsAssetType, Currency
from gs_quant.api.utils import ThreadPoolManager
from gs_quant.base import get_enum_value
from gs_quant.common import DateLimit
from gs_quant.data import DataMeasure, DataFrequency
from gs_quant.data.coordinate import DataDimensions
from gs_quant.data.coordinate import DateOrDatetime
from gs_quant.data.core import IntervalFrequency, DataAggregationOperator
from gs_quant.entities.entity import Entity, EntityIdentifier, EntityType, PositionedEntity
from gs_quant.errors import MqValueError, MqTypeError, MqRequestError
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets import PricingContext
from gs_quant.markets.indices_utils import *

_logger = logging.getLogger(__name__)


class ExchangeCode(Enum):
    """Exchange enumeration

    Exchange codes representing global venues where Securities are listed and traded

    """

    NASDAQ = "NASD"  # Nasdaq Global Stock Market
    NYSE = "NYSE"  # New York Stock Exchange


class AssetType(Enum):
    """Asset type enumeration

    Enumeration of different types of asset or security.

    """

    #: Index which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets
    INDEX = "Index"

    #: Exchange traded fund which tracks an evolving portfolio of securities and is listed on an exchange to be
    #: traded as a security
    ETF = "ETF"

    #: Bespoke basket which provides exposure to a customized collection of assets with levels published daily; can be
    #: traded on swap and rebalanced programmatically
    CUSTOM_BASKET = "Custom Basket"

    #: Bespoke basket which provides exposure to a customized collection of assets with levels published daily;
    #: basket composition maintained by Goldman Sachs Investment Research
    RESEARCH_BASKET = "Research Basket"

    #: Listed equities which provide access to equity holding in a company and participation in dividends and other
    #: distributions in common, preferred or other variants which provide different investor rights
    STOCK = "Single Stock"

    #: Standardized listed contract which provides delivery of an asset at a pre-defined forward date and can be
    #: settled in cash or physical form
    FUTURE = "Future"

    #: FX cross or currency pair
    CROSS = "Cross"

    #: Currency
    CURRENCY = "Currency"

    #: Rate
    RATE = "Rate"

    #: Cash
    CASH = "Cash"

    #: Weather Index
    WEATHER_INDEX = "Weather Index"

    #: Swap
    SWAP = "Swap"

    #: Swaption
    SWAPTION = "Swaption"

    #: Option
    OPTION = "Option"

    #: Binary
    BINARY = "Binary"

    #: Commodity Reference Price
    COMMODITY_REFERENCE_PRICE = "Commodity Reference Price"

    # COMMODITY NATURAL GAS Hub
    COMMODITY_NATURAL_GAS_HUB = "Commodity Natural Gas Hub"

    # COMMODITY EU NATURAL GAS Hub
    COMMODITY_EU_NATURAL_GAS_HUB = "Commodity EU Natural Gas Hub"

    #: Commodity Power Node
    COMMODITY_POWER_NODE = "Commodity Power Node"

    #: Commodity Power Aggregated Nodes
    COMMODITY_POWER_AGGREGATED_NODES = "Commodity Power Aggregated Nodes"

    #: Bond
    BOND = "Bond"

    #: Future Market
    FUTURE_MARKET = "Future Market"

    #: Future Contract
    FUTURE_CONTRACT = "Future Contract"

    #: Commodity
    COMMODITY = "Commodity"

    #: Crypto
    CRYPTOCURRENCY = "Cryptocurrency"

    #: Forward
    FORWARD = "Forward"

    #: Fund
    FUND = "Fund"

    #: Default Swap
    DEFAULT_SWAP = "Default Swap"

    #: Systematic Hedging
    SYSTEMATIC_HEDGING = 'Systematic Hedging'

    #: Access
    ACCESS = 'Access'

    #: Risk Premia
    RISK_PREMIA = 'Risk Premia'

    #: Multi Asset Allocation
    MULTI_ASSET_ALLOCATION = 'Multi-Asset Allocation'

    # Sec Master types

    ADR = 'ADR'
    GDR = 'GDR'
    DUTCH_CERT = 'Dutch Cert'
    NYRS = 'NY Reg Shrs'
    RECEIPT = 'Receipt'
    UNIT = 'Unit'
    MUTUAL_FUND = 'Mutual Fund'
    RIGHT = 'Right'
    PREFERRED = 'Preferred'
    MISC = 'Misc.'
    REIT = 'REIT'
    PRIVATE_COMP = 'Private Comp'
    PREFERENCE = 'Preference'
    LIMITED_PARTNERSHIP = 'Ltd Part'
    TRACKING_STOCK = 'Tracking Stk'
    ROYALTY_TRUST = 'Royalty Trst'
    CLOSED_END_FUND = 'Closed-End Fund'
    OPEN_END_FUND = 'Open-End Fund'
    FUND_OF_FUNDS = 'Fund of Funds'
    MLP = 'MLP'
    STAPLED_SECURITY = 'Stapled Security'
    SAVINGS_SHARE = 'Savings Share'
    EQUITY_WRT = 'Equity WRT'
    # ETF already defined
    SAVINGS_PLAN = 'Savings Plan'


class AssetIdentifier(EntityIdentifier):
    """Asset type enumeration

    Enumeration of different security identifiers

    """

    MARQUEE_ID = "MQID"  #: Goldman Sachs Marquee identifier code (MA4B66MW5E27UAHKG34)
    REUTERS_ID = "RIC"  #: Thompson Reuters Instrument Code (RIC), (GS.N)
    BLOOMBERG_ID = "BBID"  #: Bloomberg identifier and exchange code (GS UN)
    BLOOMBERG_COMPOSITE_ID = "BCID"  #: Bloomberg composite identifier and exchange code (GS US)
    CUSIP = "CUSIP"  #: Committee on Uniform Security Identification Procedures code (38141G104)
    ISIN = "ISIN"  #: International Securities Identification Number (US38141G1040)
    SEDOL = "SEDOL"  #: LSE Stock Exchange Daily Official List code (2407966)
    TICKER = "TICKER"  #: Exchange ticker (GS)
    PLOT_ID = "PLOT_ID"  #: ID for Marquee PlotTool
    GSID = "GSID"


class SecurityIdentifier(EntityIdentifier):
    GSID = "gsid"
    RCIC = "rcic"
    RIC = "ric"
    ID = "id"
    CUSIP = "cusip"
    SEDOL = "sedol"
    ISIN = "isin"
    TICKER = "ticker"
    BBID = "bbid"
    BCID = "bcid"
    GSS = "gss"
    PRIMEID = "primeId"
    BBG = "bbg"


class ReturnType(Enum):
    """Index return type

    Represents different index return types or funding models

    """

    EXCESS_RETURN = "Excess Return"  # Returns are excess of funding rate in denominated currency
    TOTAL_RETURN = "Total Return"  # Returns are inclusive of funding rate in denominated currency


class Asset(Entity, metaclass=ABCMeta):
    def __init__(self,
                 id_: str,
                 asset_class: AssetClass,
                 name: str,
                 exchange: Optional[str] = None,
                 currency: Optional[str] = None,
                 parameters: AssetParameters = None,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.ASSET, entity=entity)
        self.__id = id_
        self.asset_class = asset_class
        self.name = name
        self.exchange = exchange
        self.currency = currency
        self.parameters = parameters
        self.entity = entity

    def get_marquee_id(self):
        return self.__id

    def get_url(self) -> str:
        """
        Retrieve url to asset's product page on Marquee
        """
        env = '-dev-ext.web' if 'dev' in get(GsSession, 'current.domain', '') else ''
        env = '-qa' if 'qa' in get(GsSession, 'current.domain', '') else env
        return f'https://marquee{env}.gs.com/s/products/{self.__id}/summary'

    def get_identifiers(self, as_of: dt.date = None) -> dict:
        """
        Get asset identifiers

        :param as_of: As of date for query
        :return: dict of identifiers

        **Usage**

        Get asset identifiers as of a given date. Where the identifiers are temporal (and can change over time), this
        function will return the identifiers as of that point in time. If no date is provided as a parameter, will use
        the current PricingContext.

        **Examples**

        Get current asset identifiers:

        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)
        >>> gs.get_identifiers()

        Get identifiers as of 1Jan18:

        >>> gs.get_identifiers(dt.date(2018,1,1))

        Use PricingContext to determine as of date:

        >>> with PricingContext(dt.date(2018,1,1)) as ctx:
        >>>     gs.get_identifiers()

        **See also**

        :class:`AssetIdentifier`
        :func:`get_asset`
        """
        if not as_of:
            as_of = PricingContext.current.pricing_date

            if isinstance(as_of, dt.datetime):
                as_of = as_of.date()

        valid_ids = set(item.value for item in AssetIdentifier)
        xrefs = GsAssetApi.get_asset_xrefs(self.__id)
        identifiers = {}

        for xref in xrefs:
            start_date = xref.startDate
            end_date = xref.endDate

            if start_date <= as_of <= end_date:
                identifiers = {k.upper(): v for k, v in xref.identifiers.as_dict().items() if k.upper() in valid_ids}

        return identifiers

    @cachetools.cached(cachetools.TTLCache(256, 600),
                       lambda s, id_type, as_of=None: cachetools.keys.hashkey(s.get_marquee_id(), id_type, as_of),
                       threading.RLock())
    def get_identifier(self, id_type: AssetIdentifier, as_of: dt.date = None):
        """
        Get asset identifier

        :param as_of: As of date for query
        :param id_type: requested id type
        :return: identifier value

        **Usage**

        Get asset identifier as of a given date. Where the identifiers are temporal (and can change over time), this
        function will return the identifier as of that point in time. If no date is provided as a parameter, will use
        the current PricingContext.

        **Examples**

        Get current SEDOL:

        >>> import datetime as dt
        >>>
        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)
        >>> gs.get_identifier(AssetIdentifier.SEDOL)

        Get SEDOL as of 1Jan18:

        >>> gs.get_identifier(AssetIdentifier.SEDOL, as_of=dt.date(2018,1,1))

        Use PricingContext to determine as of date:

        >>> with PricingContext(dt.date(2018,1,1)) as ctx:
        >>>     gs.get_identifier(AssetIdentifier.SEDOL)

        **See also**

        :class:`AssetIdentifier`
        :func:`get_asset_identifiers`

        """
        if id_type == AssetIdentifier.MARQUEE_ID:
            return self.__id

        ids = self.get_identifiers(as_of=as_of)
        return ids.get(id_type.value)

    def get_data_series(self,
                        measure: DataMeasure,
                        dimensions: Optional[DataDimensions] = None,
                        frequency: Optional[DataFrequency] = None,
                        start: Optional[DateOrDatetime] = None,
                        end: Optional[DateOrDatetime] = None,
                        dates: List[dt.date] = None,
                        operator: DataAggregationOperator = None) -> pd.Series:
        """
        Get asset series

        :param measure: measure to get as series
        :param dimensions: dimensions to query (e.g. tenor)
        :param frequency: data frequency to query
        :param start: start of the series
        :param end: end of the series
        :return: timeseries of given measure

        **Usage**

        Get a given timeseries for the asset

        **Examples**

        Get close price series:

        >>> from gs_quant.markets.securities import SecurityMaster
        >>> from gs_quant.data import DataMeasure
        >>>
        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)
        >>> gs.get_data_series(DataMeasure.CLOSE_PRICE)

        **See also**

        :class:`DataMeasure`

        """

        coordinate = self.get_data_coordinate(measure, dimensions, frequency)
        if coordinate is None:
            raise MqValueError(f"No data coordinate found for parameters: {measure, dimensions, frequency}")
        return coordinate.get_series(start=start, end=end, dates=dates, operator=operator)

    def get_latest_close_price(self) -> float:
        coordinate = self.get_data_coordinate(DataMeasure.CLOSE_PRICE, None, DataFrequency.DAILY)
        if coordinate is None:
            raise MqValueError(f"No data co-ordinate found for these parameters: \
                {DataMeasure.CLOSE_PRICE, None, DataFrequency.DAILY}")
        return coordinate.last_value()

    def get_close_price_for_date(self, date: dt.date) -> pd.Series:
        return self.get_data_series(DataMeasure.CLOSE_PRICE, None, DataFrequency.DAILY, date, date)

    def get_close_prices(self,
                         start: dt.date = DateLimit.LOW_LIMIT.value,
                         end: dt.date = dt.date.today()) -> pd.Series:
        """
        Get close price series

        :return: timeseries of close prices

        **Usage**

        Get close prices for an asset

        **Examples**

        Get close price series:

        >>> from gs_quant.markets.securities import SecurityMaster
        >>>
        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)
        >>> gs.get_close_prices()

        **See also**

        :class:`DataMeasure`
        :func:`get_data_series`
        """
        return self.get_data_series(DataMeasure.CLOSE_PRICE, None, DataFrequency.DAILY, start, end)

    def get_hloc_prices(self,
                        start: dt.date = DateLimit.LOW_LIMIT.value,
                        end: dt.date = dt.date.today(),
                        interval_frequency: IntervalFrequency = IntervalFrequency.DAILY) -> pd.DataFrame:
        """
        Get high, low, open, close (hloc) prices

        :return: dataframe indexed by datetimes bucketed by the given interval_frequency with High, Low, Open, and Close
        columns

        **Usage**

        Get high, low, open, and close prices for an asset for the given interval frequency.

        **Examples**

        Get hloc price series:

        >>> from gs_quant.markets.securities import SecurityMaster
        >>>
        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)
        >>> gs.get_hloc_prices()

        **See also**

        :class:`DataMeasure`
        :func:`get_close_prices`
        """
        if interval_frequency == IntervalFrequency.DAILY:
            dates = None
            use_field = False
        elif interval_frequency == IntervalFrequency.MONTHLY:
            d = dt.date(start.year, start.month, 1)
            dates = [d, dt.date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1])]
            d += relativedelta(months=1)
            while d < end:
                dates.append(dt.date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1]))
                d += relativedelta(months=1)
            dates.append(end)
            use_field = True
        else:
            raise MqValueError(f'Unsupported IntervalFrequency {interval_frequency.value} for get_hloc_prices')

        tasks = [
            partial(self.get_data_series, DataMeasure.ADJUSTED_HIGH_PRICE, None, DataFrequency.DAILY, start, end,
                    dates=dates, operator=DataAggregationOperator.MAX if use_field else None),
            partial(self.get_data_series, DataMeasure.ADJUSTED_LOW_PRICE, None, DataFrequency.DAILY, start, end,
                    dates=dates, operator=DataAggregationOperator.MIN if use_field else None),
            partial(self.get_data_series, DataMeasure.ADJUSTED_OPEN_PRICE, None, DataFrequency.DAILY, start, end,
                    dates=dates, operator=DataAggregationOperator.FIRST if use_field else None),
            partial(self.get_data_series, DataMeasure.ADJUSTED_CLOSE_PRICE, None, DataFrequency.DAILY, start, end,
                    dates=dates, operator=DataAggregationOperator.LAST if use_field else None)
        ]

        results = ThreadPoolManager.run_async(tasks)
        df = pd.DataFrame({'high': results[0], 'low': results[1], 'open': results[2], 'close': results[3]})
        return df.dropna()

    def get_thematic_exposure(self,
                              basket_identifier: str,
                              notional: int = None,
                              start: dt.date = DateLimit.LOW_LIMIT.value,
                              end: dt.date = dt.date.today()) -> pd.DataFrame:
        """Timeseries of daily thematic exposure of asset to requested flagship basket (only composites currently)"""
        pass

    def get_thematic_beta(self,
                          basket_identifier: str,
                          start: dt.date = DateLimit.LOW_LIMIT.value,
                          end: dt.date = dt.date.today()) -> pd.DataFrame:
        """Timeseries of daily thematic beta of asset to requested flagship basket (only composites currently)"""
        pass

    @abstractmethod
    def get_type(self) -> AssetType:
        """Overridden by sub-classes to return security type"""

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.ASSET

    @property
    def data_dimension(self) -> str:
        return 'assetId'

    @classmethod
    def get(cls,
            id_value: str,
            id_type: AssetIdentifier,
            as_of: Union[dt.date, dt.datetime] = None,
            exchange_code: ExchangeCode = None,
            asset_type: AssetType = None,
            sort_by_rank: bool = False) -> Optional['Asset']:
        asset = SecurityMaster.get_asset(id_value, id_type, as_of, exchange_code, asset_type, sort_by_rank)
        return asset


class Stock(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 exchange: Optional[str] = None,
                 currency: Optional[Currency] = None,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Equity, name, exchange, currency, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.STOCK

    def get_currency(self) -> Optional[Currency]:
        return self.currency


class Cross(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None,
                 asset_class: Optional[Union[AssetClass, str]] = AssetClass.FX):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.CROSS


class Future(Asset):
    """Future Security Type

    Represents a standardized listed contract which provides delivery of an asset at a pre-defined forward date and can
    be settled in cash or physical form

    """

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: str,
                 currency: Optional[Currency] = None,
                 entity: Optional[Dict] = None):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name, currency=currency, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.FUTURE

    def get_currency(self) -> Optional[Currency]:
        return self.currency


class Currency(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Cash, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.CURRENCY


class Rate(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Rates, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.RATE


class Cash(Asset):
    """Cash Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Cash, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.CASH


class WeatherIndex(Asset):
    """Weather Index Type

    Represents an underlying index on a weather derivative, including where the data (e.g. CPD) has been collected,
    an actual physical reference point (weather station) and various fall back arrangements.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.WEATHER_INDEX


class CommodityReferencePrice(Asset):
    """Commodity Reference Price

    Represents an underlying index for commodities in the event that no ISDA Commodity Reference Price exists.
    Includes base, details, unit, currency and exchange id or publication etc.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY_REFERENCE_PRICE


class CommodityNaturalGasHub(Asset):
    """Commodity Natural Gas Hub

    Represents a distinct location in commodity Natural Gas markets

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY_NATURAL_GAS_HUB


class CommodityEUNaturalGasHub(Asset):
    """Commodity EU Natural Gas Hub

    Represents a virtual/physical hub in EU Natural Gas markets

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY_EU_NATURAL_GAS_HUB


class Cryptocurrency(Asset):
    """Cryptocurrency

    Represents a cryptocurrency

    """

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.CRYPTOCURRENCY


class CommodityPowerNode(Asset):
    """Commodity Power Node

    Represents a distinct location in commodity power markets

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY_POWER_NODE


class CommodityPowerAggregatedNodes(Asset):
    """Commodity Power Aggregated Nodes

    Represents a group of locations in commodity power markets

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY_POWER_AGGREGATED_NODES


class Commodity(Asset):
    """Commodity

    Represents a commodity.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Commod, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY


class Bond(Asset):
    """Bond

    Represents a bond.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Credit, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.BOND


class Fund(Asset):
    """Fund
    Represents a fund.
    """

    def __init__(self,
                 id_: str,
                 name: str,
                 asset_class: AssetClass,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.FUND


class FutureMarket(Asset):
    """Future Market

    Represents a future market

    """

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: str,
                 entity: Optional[Dict] = None):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.FUTURE_MARKET


class FutureContract(Asset):
    """Future Contract

    Represents a future contract

    """

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: Union[AssetClass, str],
                 entity: Optional[Dict] = None):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.FUTURE_CONTRACT


class Swap(Asset):
    """Swap Instrument Type

    Represents a Swap Instrument

    """

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: str,
                 entity: Optional[Dict] = None):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.SWAP


class Option(Asset):
    """Option Instrument Type

    Represents an Option Instrument

    """

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: str,
                 entity: Optional[Dict] = None):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.OPTION


class Forward(Asset):

    def __init__(self,
                 id_: str,
                 asset_class: Union[AssetClass, str],
                 name: str,
                 entity: Optional[Dict] = None):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.FORWARD


class ETF(Asset, PositionedEntity):
    """ETF Asset

    ETF which tracks an evolving portfolio of securities, and can be traded on exchange
    """

    def __init__(self,
                 id_: str,
                 asset_class: AssetClass,
                 name: str,
                 exchange: Optional[str] = None,
                 currency: Optional[Currency] = None,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class, name, exchange, currency, entity=entity)
        PositionedEntity.__init__(self, id_, EntityType.ASSET)

    def get_type(self) -> AssetType:
        return AssetType.ETF

    def get_currency(self) -> Optional[Currency]:
        return self.currency


class Swaption(Asset):
    """Swaption

    Represents a swaption.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Rates, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.SWAPTION


class Binary(Asset):
    """Binary
    Represents a binary.
    """

    def __init__(self,
                 id_: str,
                 name: str,
                 asset_class: AssetClass,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.BINARY


class DefaultSwap(Asset):
    """DefaultSwap

    Represents a default swap.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Credit, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.DEFAULT_SWAP


class SecurityMasterSource(Enum):
    ASSET_SERVICE = auto()
    SECURITY_MASTER = auto()


class Security:
    def __init__(self, json: dict):
        for k, v in json.items():
            if k == 'identifiers':
                self._ids = {inner_k: inner_v for inner_k, inner_v in v.items()}
            else:
                setattr(self, k, v)

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    def get_identifiers(self):
        return deepcopy(self._ids)


@backoff.on_exception(backoff.expo, MqRequestError, giveup=lambda e: e.status != 429)
def _get_with_retries(url, payload):
    return GsSession.current._get(url, payload=payload)


class SecurityMaster:
    """Security Master

     The SecurityMaster class provides an interface to security lookup functions. This allows querying and retrieval of
     different security types (assets) based on a variety of different identifiers through point-in-time lookups.

     Uses the current PricingContext to provide as of dates if optional arguments are not provided. Will return
     the relevant asset subclass depending on the type of the security

    **See also**

    :class:`Asset`

     """
    _source = SecurityMasterSource.ASSET_SERVICE
    _page_size = 1000

    @classmethod
    def __gs_asset_to_asset(cls, gs_asset: GsAsset) -> Asset:
        asset_type = gs_asset.type.value
        asset_entity: Dict = json.loads(json.dumps(gs_asset.as_dict(), cls=JSONEncoder))

        if asset_type in (GsAssetType.Single_Stock.value,):
            return Stock(gs_asset.id, gs_asset.name, gs_asset.exchange, gs_asset.currency, entity=asset_entity)

        if asset_type in (GsAssetType.ETF.value,):
            return ETF(gs_asset.id, gs_asset.assetClass, gs_asset.name, gs_asset.exchange, gs_asset.currency,
                       entity=asset_entity)

        if asset_type in (
                GsAssetType.Index.value,
                GsAssetType.Access.value,
                GsAssetType.Multi_Asset_Allocation.value,
                GsAssetType.Risk_Premia.value,
                GsAssetType.Systematic_Hedging.value):
            from gs_quant.markets.index import Index
            return Index(gs_asset.id, gs_asset.assetClass, gs_asset.name, gs_asset.exchange, gs_asset.currency,
                         entity=asset_entity)

        if asset_type in (
                GsAssetType.Custom_Basket.value,
                GsAssetType.Research_Basket.value):
            from gs_quant.markets.baskets import Basket
            return Basket(gs_asset=gs_asset)

        if asset_type in (GsAssetType.Future.value,):
            return Future(gs_asset.id, gs_asset.assetClass, gs_asset.name, gs_asset.currency, entity=asset_entity)

        if asset_type in (GsAssetType.Cross.value,):
            return Cross(gs_asset.id, gs_asset.name, entity=asset_entity, asset_class=gs_asset.assetClass)

        if asset_type in (GsAssetType.Currency.value,):
            return Currency(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.Rate.value,):
            return Rate(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.Cash.value,):
            return Cash(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.WeatherIndex.value,):
            return WeatherIndex(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.Swap.value,):
            return Swap(gs_asset.id, gs_asset.assetClass, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.Option.value,):
            return Option(gs_asset.id, gs_asset.assetClass, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.CommodityReferencePrice.value,):
            return CommodityReferencePrice(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.CommodityNaturalGasHub.value,):
            return CommodityNaturalGasHub(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.CommodityEUNaturalGasHub.value,):
            return CommodityEUNaturalGasHub(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.CommodityPowerNode.value,):
            return CommodityPowerNode(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.CommodityPowerAggregatedNodes.value,):
            return CommodityPowerAggregatedNodes(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.Bond.value,):
            return Bond(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.Commodity.value,):
            return Commodity(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.FutureMarket.value,):
            return FutureMarket(gs_asset.id, gs_asset.assetClass, gs_asset.name, entity=asset_entity)

        if asset_type in (GsAssetType.FutureContract.value,):
            return FutureContract(gs_asset.id, gs_asset.assetClass, gs_asset.name, entity=asset_entity)

        # workaround as casing is being migrated
        if asset_type == GsAssetType.Cryptocurrency.value:
            return Cryptocurrency(gs_asset.id, gs_asset.assetClass, gs_asset.name, entity=asset_entity)

        if asset_type == GsAssetType.Forward.value:
            return Forward(gs_asset.id, gs_asset.assetClass, gs_asset.name, entity=asset_entity)

        if asset_type == GsAssetType.Fund.value:
            return Fund(gs_asset.id, gs_asset.name, gs_asset.assetClass, entity=asset_entity)

        if asset_type == GsAssetType.Default_Swap.value:
            return DefaultSwap(gs_asset.id, gs_asset.asset_class, entity=asset_entity)

        if asset_type == GsAssetType.Swaption.value:
            return Swaption(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type == GsAssetType.Binary.value:
            return Binary(gs_asset.id, gs_asset.name, gs_asset.assetClass, entity=asset_entity)

        raise TypeError(f'unsupported asset type {asset_type}')

    @classmethod
    def __asset_type_to_gs_types(cls, asset_type: AssetType) -> Tuple[GsAssetType, ...]:
        asset_map = {
            AssetType.STOCK: (GsAssetType.Single_Stock,),
            AssetType.INDEX: (
                GsAssetType.Index, GsAssetType.Multi_Asset_Allocation, GsAssetType.Risk_Premia, GsAssetType.Access),
            AssetType.ETF: (GsAssetType.ETF, GsAssetType.ETN),
            AssetType.CUSTOM_BASKET: (GsAssetType.Custom_Basket,),
            AssetType.RESEARCH_BASKET: (GsAssetType.Research_Basket,),
            AssetType.FUTURE: (GsAssetType.Future,),
            AssetType.RATE: (GsAssetType.Rate,),
        }

        return asset_map.get(asset_type)

    @classmethod
    def set_source(cls, source: SecurityMasterSource):
        cls._source = source

    @classmethod
    def get_asset(cls,
                  id_value: str,
                  id_type: Union[AssetIdentifier, SecurityIdentifier],
                  as_of: Union[dt.date, dt.datetime] = None,
                  exchange_code: ExchangeCode = None,
                  asset_type: AssetType = None,
                  sort_by_rank: bool = False,
                  fields: Optional[List[str]] = None) -> Union[Asset, Security]:
        """
        Get an asset by identifier and identifier type

        :param id_value: identifier value
        :param id_type: identifier type
        :param exchange_code: exchange code
        :param asset_type: asset type
        :param as_of: As of date for query
        :param sort_by_rank: whether to sort assets by rank.
        :param fields: asset fields to return
        :return: Asset object or None

        **Usage**

        Get asset object using a specified identifier and identifier type. Where the identifiers are temporal (and can
        change over time), will use the current MarketContext to evaluate based on the specified date.

        **Examples**

        Get asset by bloomberg id:

        >>> gs = SecurityMaster.get_asset("GS UN", AssetIdentifier.BLOOMBERG_ID)

        Get asset by ticker and exchange code:

        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE)

        Get asset by ticker and asset type:

        >>> spx = SecurityMaster.get_asset("SPX", AssetIdentifier.TICKER, asset_type=AssetType.INDEX)

        **See also**

        :class:`AssetIdentifier`
        :func:`get_many_assets`

        """
        if cls._source == SecurityMasterSource.SECURITY_MASTER:
            if not isinstance(id_type, SecurityIdentifier):
                raise MqTypeError('expected a security identifier')
            if exchange_code or asset_type or sort_by_rank:
                raise NotImplementedError('argument not implemented for Security Master (supported in Asset Service)')
            return cls._get_security(id_value, id_type, as_of=as_of, fields=fields)

        if not as_of:
            as_of = PricingContext.current.pricing_date

        if isinstance(as_of, dt.date):
            as_of = dt.datetime.combine(as_of, dt.time(0, 0), pytz.utc)

        if id_type is AssetIdentifier.MARQUEE_ID:
            gs_asset = GsAssetApi.get_asset(id_value)
            return cls.__gs_asset_to_asset(gs_asset)

        query = {id_type.value.lower(): id_value}

        if exchange_code is not None:
            query['exchange'] = exchange_code.value

        if asset_type is not None:
            query['type'] = [t.value for t in cls.__asset_type_to_gs_types(asset_type)]

        if sort_by_rank:
            results = GsAssetApi.get_many_assets(as_of=as_of, return_type=dict, order_by=['>rank'], **query)
            result = get(results, '0')

            if result:
                result = GsAsset.from_dict(result)
        else:
            results = GsAssetApi.get_many_assets(as_of=as_of, **query)
            result = next(iter(results), None)

        if result:
            return cls.__gs_asset_to_asset(result)

    @classmethod
    def _get_security(cls,
                      id_value: str,
                      id_type: SecurityIdentifier,
                      as_of: Union[dt.date, dt.datetime] = None,
                      fields: Optional[List[str]] = None) -> Optional[Security]:
        as_of = as_of or datetime.datetime(2100, 1, 1)
        type_ = id_type.value
        params = {
            type_: id_value,
            'asOfDate': as_of.strftime('%Y-%m-%d')  # TODO: update endpoint to take times
        }
        if fields is not None:
            if 'identifiers' not in fields:
                fields.append('identifiers')
            params['fields'] = fields

        r = GsSession.current._get('/markets/securities', payload=params)
        if r['totalResults'] == 0:
            return None
        return Security(r['results'][0])

    @classmethod
    def get_identifiers(cls, id_values: List[str], id_type: SecurityIdentifier, as_of: datetime.datetime = None,
                        start: datetime.datetime = None, end: datetime.datetime = None) -> dict:
        """
        Get identifiers for given assets.

        :param id_values: identifier values e.g. ['GS UN']
        :param id_type: identifier type e.g. BBID
        :param as_of: point in time to use for resolving given ids to assets
        :param start: restrict results to ids updated after this time
        :param end: restrict results to ids updated before this time
        :return: dict from IDs (of id_type) to available identifiers
        """
        if cls._source != SecurityMasterSource.SECURITY_MASTER:
            raise NotImplementedError("method not available when using Asset Service")

        as_of = as_of or datetime.datetime.now()
        start = start or datetime.datetime(1970, 1, 1)
        end = end or datetime.datetime(2100, 1, 1)

        type_ = id_type.value
        params = {
            type_: id_values,
            'fields': ['id', 'identifiers'],
            'asOfDate': as_of.strftime('%Y-%m-%d')  # TODO: update endpoint to take times
        }

        r = GsSession.current._get('/markets/securities', payload=params)
        id_map = {}
        for asset in r['results']:
            id_map[asset['identifiers'][type_]] = asset['id']

        if len(id_map) == 0:
            return {}

        output = {}
        for k, v in id_map.items():
            r = GsSession.current._get(f'/markets/securities/{v}/identifiers')
            piece = []
            for e in r['results']:
                time_str = e['updateTime'].split('.')[0]
                if time_str.endswith('Z'):
                    time_str = time_str[0:-1]
                time = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
                if start <= time <= end:
                    piece.append(e)
            output[k] = piece

        return output

    @staticmethod
    def asset_type_to_str(asset_class: AssetClass, asset_type: AssetType):
        if asset_type == AssetType.STOCK:
            return "Common Stock"
        if asset_type == AssetType.INDEX and asset_class == AssetClass.Equity:
            return "Equity Index"
        return asset_type.value

    @classmethod
    def get_all_identifiers_gen(cls, class_: AssetClass = None, types: Optional[List[AssetType]] = None,
                                as_of: datetime.datetime = None, *, id_type: SecurityIdentifier = SecurityIdentifier.ID,
                                use_offset_key=True, sleep=0.5) -> Generator[dict, None, None]:
        """
        Get identifiers for all matching assets. Returns a generator iterator so that the caller can load each page of
        results using next().

        :param class_: if not None, restrict results to assets of given class e.g. Equity
        :param types: if not None, restrict results to given types e.g. Stock
        :param as_of: point in time for which identifiers are fetched
        :param id_type: identifier type to use for keys of results
        :param use_offset_key: whether to use offset keys for pagination (required for large result sets)
        :param sleep: seconds to sleep between API calls (to avoid server-side throttling)
        :return: a generator iterator that yields dicts from id (of the id_type) to available identifiers
        """
        if cls._source != SecurityMasterSource.SECURITY_MASTER:
            raise NotImplementedError("method not available when using Asset Service")

        as_of = as_of or datetime.datetime.now()
        if types is not None:
            p = functools.partial(cls.asset_type_to_str, class_)
            types = set(map(p, types))

        params = {
            'fields': ['id', 'identifiers', 'assetClass', 'type'],
            'asOfDate': as_of.date(),
            'limit': cls._page_size
        }

        while True:
            r = _get_with_retries('/markets/securities', params)
            if r['totalResults'] == 0:
                return

            output = {}
            for e in r['results']:
                # TODO: perform filtering on server side
                if (class_ is None or e['assetClass'] == class_.value) and (types is None or e['type'] in types):
                    box = e['identifiers']
                    key = box[id_type.value]
                    if key in box:
                        _logger.debug(f'encountered duplicate key {key}')
                    output[key] = box

            yield output
            if use_offset_key:
                if 'offsetKey' not in r:
                    return
                params['offsetKey'] = r['offsetKey']
            else:
                params['offset'] = params.get('offset', 0) + cls._page_size
                if params['offset'] + params['limit'] > 10000:
                    _logger.warning('reached result size limit; enable use of offset keys to retrieve all results')
                    return
            time.sleep(sleep)

    @classmethod
    def get_all_identifiers(cls, class_: AssetClass = None, types: Optional[List[AssetType]] = None,
                            as_of: datetime.datetime = None, *, id_type: SecurityIdentifier = SecurityIdentifier.ID,
                            use_offset_key=True, sleep=0.5) -> Dict[str, dict]:
        """
        Get identifiers for all matching assets.

        :param class_: if not None, restrict results to assets of given class e.g. Equity
        :param types: if not None, restrict results to given types e.g. Stock
        :param as_of: point in time for which identifiers are fetched
        :param id_type: identifier type to use for keys of results
        :param use_offset_key: whether to use offset keys for pagination (required for large result sets)
        :param sleep: seconds to sleep between API calls (to avoid server-side throttling)
        :return: dict from id (of the id_type) to available identifiers
        """
        gen = cls.get_all_identifiers_gen(class_, types, as_of, id_type=id_type, use_offset_key=use_offset_key,
                                          sleep=sleep)
        accumulator = dict()
        while True:
            try:
                accumulator.update(next(gen))
            except StopIteration:
                return accumulator

    @classmethod
    def map_identifiers(cls, ids: Iterable[str],
                        to_identifiers: Iterable[SecurityIdentifier] = frozenset([SecurityIdentifier.GSID]),
                        start_date: datetime.date = None, end_date: datetime.date = None) -> Dict[datetime.date, dict]:
        """
        Map to (other) identifiers from given IDs.

        :param ids: security IDs e.g. GSIDs or BBIDs
        :param to_identifiers: types of IDs to map to
        :param start_date: start of date range
        :param end_date: end of date range
        :return: dict containing mappings for each date in range

        **Examples**

        Get CUSIP for GS UN:
        >>> result = SecurityMaster.map_identifiers(["GS UN"], [SecurityIdentifier.CUSIP])

        Get Bloomberg ticker for 104563 over a range of dates:
        >>> result = SecurityMaster.map_identifiers(["104563"], [SecurityIdentifier.BBG],
        ...                                         datetime.date(2021, 4, 16), datetime.date(2021, 4, 19))
        """
        if cls._source != SecurityMasterSource.SECURITY_MASTER:
            raise NotImplementedError("method not available when using Asset Service")

        if isinstance(ids, str):
            raise MqTypeError("expected an iterable of strings e.g. a list of strings")

        params = {
            'identifiers': list(ids),
            'toIdentifiers': [identifier.value for identifier in to_identifiers]
        }
        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['endDate'] = end_date
        r = _get_with_retries('/markets/securities/map', params)
        return r['results']
