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

import datetime as dt
import threading
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Optional, Tuple, Union

import cachetools
import pytz

from gs_quant.api.gs.assets import GsAssetApi, GsAsset, AssetClass, AssetType as GsAssetType, PositionSet
from gs_quant.base import get_enum_value
from gs_quant.common import PositionType
from gs_quant.markets import PricingContext


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
    BASKET = "Custom Basket"

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

    #: Option
    OPTION = "Option"

    #: Commodity Reference Price
    COMMODITY_REFERENCE_PRICE = "Commodity Reference Price"

    #: Bond
    BOND = "Bond"


class AssetIdentifier(Enum):
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


class Asset(metaclass=ABCMeta):
    def __init__(self, id_: str, asset_class: AssetClass, name: str, exchange: Optional[str] = None):
        self.__id = id_
        self.asset_class = asset_class
        self.name = name
        self.exchange = exchange

    def get_marquee_id(self):
        return self.__id

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
        ids = self.get_identifiers(as_of=as_of)
        return ids.get(id_type.value)

    @abstractmethod
    def get_type(self) -> AssetType:
        """Overridden by sub-classes to return security type"""


class Stock(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self, id_: str, name: str, exchange=None):
        Asset.__init__(self, id_, AssetClass.Equity, name, exchange)

    def get_type(self) -> AssetType:
        return AssetType.STOCK


class Cross(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.FX, name)

    def get_type(self) -> AssetType:
        return AssetType.CROSS


class Future(Asset):
    """Future Security Type

    Represents a standardized listed contract which provides delivery of an asset at a pre-defined forward date and can
    be settled in cash or physical form

    """

    def __init__(self, id_: str, asset_class: Union[AssetClass, str], name: str):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name)

    def get_type(self) -> AssetType:
        return AssetType.FUTURE


class Currency(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Cash, name)

    def get_type(self) -> AssetType:
        return AssetType.CURRENCY


class Rate(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Rates, name)

    def get_type(self) -> AssetType:
        return AssetType.RATE


class Cash(Asset):
    """Cash Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Cash, name)

    def get_type(self) -> AssetType:
        return AssetType.CASH


class WeatherIndex(Asset):
    """Weather Index Type

    Represents an underlying index on a weather derivative, including where the data (e.g. CPD) has been collected,
    an actual physical reference point (weather station) and various fall back arrangements.

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Commod, name)

    def get_type(self) -> AssetType:
        return AssetType.WEATHER_INDEX


class CommodityReferencePrice(Asset):
    """Commodity Reference Price

    Represents an underlying index for commodities in the event that no ISDA Commodity Reference Price exists.
    Includes base, details, unit, currency and exchange id or publication etc.

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Commod, name)

    def get_type(self) -> AssetType:
        return AssetType.COMMODITY_REFERENCE_PRICE


class Bond(Asset):
    """Bond

    Represents a bond.

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Credit, name)

    def get_type(self) -> AssetType:
        return AssetType.BOND


class Swap(Asset):
    """Swap Instrument Type

    Represents a Swap Instrument

    """

    def __init__(self, id_: str, asset_class: Union[AssetClass, str], name: str):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name)

    def get_type(self) -> AssetType:
        return AssetType.SWAP


class Option(Asset):
    """Option Instrument Type

    Represents an Option Instrument

    """

    def __init__(self, id_: str, asset_class: Union[AssetClass, str], name: str):
        if isinstance(asset_class, str):
            asset_class = get_enum_value(AssetClass, asset_class)

        Asset.__init__(self, id_, asset_class, name)

    def get_type(self) -> AssetType:
        return AssetType.OPTION


class IndexConstituentProvider(metaclass=ABCMeta):
    def __init__(self, id_: str):
        self.__id = id_

    def get_constituents(self, as_of: dt.date = None, position_type: PositionType = PositionType.CLOSE) -> Tuple[
            PositionSet, ...]:
        """
        Get asset constituents

        :param as_of: As of date for query
        :param position_type:
        :return: dict of identifiers

        **Usage**

        Get index constituents as of a given date. If no date is provided as a parameter, will use the current
        PricingContext.

        **Examples**

        Get current index constituents (defaults to close):

        >>> import datetime as dt
        >>>
        >>> gs = SecurityMaster.get_asset('GSTHHVIP', AssetIdentifier.TICKER)
        >>> gs.get_constituents()

        Get constituents as of market open on 3Jan18:

        >>> gs.get_constituents(dt.date(2018,1,3), PositionType.OPEN)

        Use PricingContext to determine as of date:

        >>> with PricingContext(dt.date(2018,1,1)) as ctx:
        >>>     gs.get_constituents()

        **See also**

        :class:`AssetIdentifier`
        :func:`get_asset`

        """
        if not as_of:
            as_of = PricingContext.current.pricing_date

            if isinstance(as_of, dt.datetime):
                as_of = as_of.date()

        return GsAssetApi.get_asset_positions_for_date(self.__id, as_of, position_type.value)


class Index(Asset, IndexConstituentProvider):
    """Index Asset

    Index which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets
    """

    def __init__(self, id_: str, asset_class: AssetClass, name: str, exchange=None):
        Asset.__init__(self, id_, asset_class, name, exchange)
        IndexConstituentProvider.__init__(self, id_)

    def get_type(self) -> AssetType:
        return AssetType.INDEX


class ETF(Asset, IndexConstituentProvider):
    """ETF Asset

    ETF which tracks an evolving portfolio of securities, and can be traded on exchange
    """

    def __init__(self, id_: str, asset_class: AssetClass, name: str, exchange=None):
        Asset.__init__(self, id_, asset_class, name, exchange)
        IndexConstituentProvider.__init__(self, id_)

    def get_type(self) -> AssetType:
        return AssetType.ETF


class Basket(Asset, IndexConstituentProvider):
    """Basket Asset

    Basket which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets
    """

    def __init__(self, id_: str, asset_class: AssetClass, name: str):
        Asset.__init__(self, id_, asset_class, name)
        IndexConstituentProvider.__init__(self, id_)

    def get_type(self) -> AssetType:
        return AssetType.BASKET


class SecurityMaster:
    """Security Master

     The SecurityMaster class provides an interface to security lookup functions. This allows querying and retrieval of
     different security types (assets) based on a variety of different identifiers through point-in-time lookups.

     Uses the current PricingContext to provide as of dates if optional arguments are not provided. Will return
     the relevant asset subclass depending on the type of the security

    **See also**

    :class:`Asset`

     """

    @classmethod
    def __gs_asset_to_asset(cls, gs_asset: GsAsset) -> Asset:
        asset_type = gs_asset.type.value

        if asset_type in (GsAssetType.Single_Stock.value,):
            return Stock(gs_asset.id, gs_asset.name, gs_asset.exchange)

        if asset_type in (GsAssetType.ETF.value,):
            return ETF(gs_asset.id, gs_asset.assetClass, gs_asset.name, gs_asset.exchange)

        if asset_type in (
                GsAssetType.Index.value,
                GsAssetType.Risk_Premia.value,
                GsAssetType.Access.value,
                GsAssetType.Multi_Asset_Allocation.value):
            return Index(gs_asset.id, gs_asset.assetClass, gs_asset.name, gs_asset.exchange)

        if asset_type in (
                GsAssetType.Custom_Basket.value,
                GsAssetType.Research_Basket.value):
            return Basket(gs_asset.id, gs_asset.assetClass, gs_asset.name)

        if asset_type in (GsAssetType.Future.value,):
            return Future(gs_asset.id, gs_asset.assetClass, gs_asset.name)

        if asset_type in (GsAssetType.Cross.value,):
            return Cross(gs_asset.id, gs_asset.name)

        if asset_type in (GsAssetType.Currency.value,):
            return Currency(gs_asset.id, gs_asset.name)

        if asset_type in (GsAssetType.Rate.value,):
            return Rate(gs_asset.id, gs_asset.name)

        if asset_type in (GsAssetType.Cash.value,):
            return Cash(gs_asset.id, gs_asset.name)

        if asset_type in (GsAssetType.WeatherIndex.value,):
            return WeatherIndex(gs_asset.id, gs_asset.name)

        if asset_type in (GsAssetType.Swap.value,):
            return Swap(gs_asset.id, gs_asset.assetClass, gs_asset.name)

        if asset_type in (GsAssetType.Option.value,):
            return Option(gs_asset.id, gs_asset.assetClass, gs_asset.name)

        if asset_type in (GsAssetType.CommodityReferencePrice.value,):
            return CommodityReferencePrice(gs_asset.id, gs_asset.name)

        if asset_type in (GsAssetType.Bond.value,):
            return Bond(gs_asset.id, gs_asset.name)

        raise TypeError(f'unsupported asset type {asset_type}')

    @classmethod
    def __asset_type_to_gs_types(cls, asset_type: AssetType) -> Tuple[GsAssetType, ...]:
        asset_map = {
            AssetType.STOCK: (GsAssetType.Single_Stock,),
            AssetType.INDEX: (
                GsAssetType.Index, GsAssetType.Multi_Asset_Allocation, GsAssetType.Risk_Premia, GsAssetType.Access),
            AssetType.ETF: (GsAssetType.ETF, GsAssetType.ETN),
            AssetType.BASKET: (GsAssetType.Custom_Basket, GsAssetType.Research_Basket),
            AssetType.FUTURE: (GsAssetType.Future,),
            AssetType.RATE: (GsAssetType.Rate,),
        }

        return asset_map.get(asset_type)

    @classmethod
    def get_asset(cls,
                  id_value: str,
                  id_type: AssetIdentifier,
                  as_of: Union[dt.date, dt.datetime] = None,
                  exchange_code: ExchangeCode = None,
                  asset_type: AssetType = None,
                  sort_by_rank: bool = False
                  ) -> Asset:
        """
        Get an asset by identifier and identifier type

        :param id_value: identifier value
        :param id_type: identifier type
        :param exchange_code: exchange code
        :param asset_type: asset type
        :param as_of: As of date for query
        :param sort_by_rank: whether to sort assets by rank.
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
            results = GsAssetApi.get_many_assets(as_of=as_of, return_type=dict, **query)
            results = sorted(results, key=lambda d: d.get('rank', 0), reverse=True)
            result = next(iter(results), None)

            if result:
                result = GsAsset.from_dict(result)
        else:
            results = GsAssetApi.get_many_assets(as_of=as_of, **query)
            result = next(iter(results), None)

        if result:
            return cls.__gs_asset_to_asset(result)
