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

from typing import Union
from enum import Enum
import datetime as dt
from abc import ABCMeta, abstractmethod
from gs_quant.api.gs.assets import GsAssetApi, GsAsset, AssetClass, AssetType as GsAssetType
from gs_quant.markets.core import MarketDataContext


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


class AssetIdentifier(Enum):
    """Asset type enumeration

    Enumeration of different security identifiers

    """

    MARQUEE_ID = "MQID"                 #: Goldman Sachs Marquee identifier code (MA4B66MW5E27UAHKG34)
    REUTERS_ID = "RIC"                  #: Thompson Reuters Instrument Code (RIC), (GS.N)
    BLOOMBERG_ID = "BBID"               #: Bloomberg identifier and exchange code (GS UN)
    BLOOMBERG_COMPOSITE_ID = "BCID"     #: Bloomberg composite identifier and exchange code (GS US)
    CUSIP = "CUSIP"                     #: Committee on Uniform Security Identification Procedures code (38141G104)
    ISIN = "ISIN"                       #: International Securities Identification Number (US38141G1040)
    SEDOL = "SEDOL"                     #: LSE Stock Exchange Daily Official List code (2407966)
    TICKER = "TICKER"                   #: Exchange ticker (GS)


class Asset(metaclass=ABCMeta):

    def __init__(self, id_: str, asset_class: AssetClass, name: str):

        self.__id = id_
        self.asset_class = asset_class
        self.name = name

    def get_identifiers(self, as_of: dt.date=None):
        """
        Get asset identifiers

        :param as_of: As of date for query
        :return: dict of identifiers

        **Usage**

        Get asset identifiers as of a given date. Where the identifiers are temporal (and can change over time), this
        function will return the identifiers as of that point in time. If no date is provided as a parameter, will use
        the current MarketDataContext.

        **Examples**

        Get current asset identifiers:

        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)
        >>> gs.get_identifiers()

        Get identifiers as of 1Jan18:

        >>> gs.get_identifiers(date(2018,1,1))

        Use MarketDataContext to determine as of date:

        >>> ctx = MarketDataContext(date(2018,1,1))
        >>> with(ctx):
        >>>     gs.get_identifiers()

        **See also**

        :class:`AssetIdentifier`
        :func:`get_asset`

        """
        if not as_of:
            as_of = MarketDataContext.current.as_of

            if type(as_of) is dt.datetime:
                as_of = as_of.date()

        valid_ids = set(item.value for item in AssetIdentifier)
        xrefs = GsAssetApi.get_asset_xrefs(self.__id)['xrefs']
        identifiers = {}

        for xref in xrefs:
            start_date = xref.startDate
            end_date = xref.endDate

            if start_date <= as_of <= end_date:
                identifiers = {k.upper(): v for k, v in xref.identifiers.items() if k.upper() in valid_ids}

        return identifiers

    @abstractmethod
    def get_type(self):
        """Overridden by sub-classes to return security type"""


class Stock(Asset):
    """Base Security Type

    Represents a financial asset which can be held in a portfolio, or has an observable price fixing which can be
    referenced in a derivative transaction

    """

    def __init__(self, id_: str, name: str):
        Asset.__init__(self, id_, AssetClass.Equity, name)

    def get_type(self):
        return AssetType.STOCK


class PositionType(Enum):
    """Position type enumeration

    Enumeration of different position types for a portfolio or index

    """

    OPEN = "open"           #: Open positions (corporate action adjusted)
    CLOSE = "close"         #: Close positions (reflect trading activity on the close)


class IndexConstituentProvider(metaclass=ABCMeta):

    def __init__(self, id_: str):
        self.__id = id_

    def get_constituents(self, as_of: dt.date=None, position_type: PositionType=PositionType.CLOSE) -> list:
        """
        Get asset constituents

        :param as_of: As of date for query
        :param position_type:
        :return: dict of identifiers

        **Usage**

        Get index constituents as of a given date. If no date is provided as a parameter, will use the current
        MarketDataContext.

        **Examples**

        Get current index constituents (defaults to close):

        >>> gs = SecurityMaster.get_asset("GSTHHVIP", AssetIdentifier.TICKER)
        >>> gs.get_constituents()

        Get constituents as of market open on 3Jan18:

        >>> gs.get_constituents(date(2018,1,3), PositionType.OPEN)

        Use MarketDataContext to determine as of date:

        >>> ctx = MarketDataContext(date(2018,1,1))
        >>> with(ctx):
        >>>     gs.get_constituents()

        **See also**

        :class:`AssetIdentifier`
        :func:`get_asset`

        """
        if not as_of:
            as_of = MarketDataContext.current.as_of

            if type(as_of) is dt.datetime:
                as_of = as_of.date()

        positions = GsAssetApi.get_asset_positions_for_date(self.__id, as_of, position_type.value)

        if len(positions['results']) == 1:
            return positions['results'][0].positions

        return list


class Index(Asset, IndexConstituentProvider):
    """Index Asset

    Index which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets
    """

    def __init__(self, id_: str, asset_class: AssetClass, name: str):
        Asset.__init__(self, id_, asset_class, name)
        IndexConstituentProvider.__init__(self, id_)

    def get_type(self):
        return AssetType.INDEX


class ETF(Asset, IndexConstituentProvider):
    """ETF Asset

    ETF which tracks an evolving portfolio of securities, and can be traded on exchange
    """
    def __init__(self, id_: str, asset_class: AssetClass,  name: str):
        Asset.__init__(self, id_, asset_class, name)
        IndexConstituentProvider.__init__(self, id_)

    def get_type(self):
        return AssetType.ETF


class Basket(Asset, IndexConstituentProvider):
    """Basket Asset

    Basket which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets
    """
    def __init__(self, id_: str, asset_class: AssetClass,  name: str):
        Asset.__init__(self, id_, asset_class, name)
        IndexConstituentProvider.__init__(self, id_)

    def get_type(self):
        return AssetType.BASKET


class SecurityMaster:
    """Security Master

     The SecurityMaster class provides an interface to security lookup functions. This allows querying and retrieval of
     different security types (assets) based on a variety of different identifiers through point-in-time lookups.

     Uses the current MarketDataContext to provide as of dates if optional arguments are not provided. Will return
     the relevant asset subclass depending on the type of the security

    **See also**

    :class:`Asset`

     """

    @classmethod
    def __gs_asset_to_asset(cls, gs_asset: GsAsset) -> Asset:

        if gs_asset.type.value in [GsAssetType.Single_Stock.value]:
            return Stock(gs_asset.id, gs_asset.name)

        if gs_asset.type.value in [GsAssetType.ETF.value]:
            return ETF(gs_asset.id, gs_asset.assetClass, gs_asset.name)

        if gs_asset.type.value in [
                GsAssetType.Index.value,
                GsAssetType.Risk_Premia.value,
                GsAssetType.Access.value,
                GsAssetType.Multi_Asset_Allocation.value]:
            return Index(gs_asset.id, gs_asset.assetClass, gs_asset.name)

        if gs_asset.type.value in [
                GsAssetType.Custom_Basket.value,
                GsAssetType.Research_Basket.value]:
            return Basket(gs_asset.id, gs_asset.assetClass, gs_asset.name)

    @classmethod
    def get_asset(cls, id_value: str, id_type: AssetIdentifier, as_of: dt.date=None) -> Union[Asset, None]:
        """
        Get an asset by identifier and identifier type

        :param id_value: identifier value
        :param id_type: identifier type
        :param as_of: As of date for query
        :return: Asset object or None

        **Usage**

        Get asset object using a specified identifier and identifier type. Where the identifiers are temporal (and can
        change over time), will use the current MarketContext to evaluate based on the specified date.

        **Examples**

        Get asset by ticker

        >>> gs = SecurityMaster.get_asset("GS", AssetIdentifier.TICKER)

        **See also**

        :class:`AssetIdentifier`
        :func:`get_many_assets`

        """

        if id_type is AssetIdentifier.MARQUEE_ID:

            gs_asset = GsAssetApi.get_asset(id_value)
            return cls.__gs_asset_to_asset(gs_asset)

        query = {id_type.value.lower(): id_value}

        results = GsAssetApi.get_many_assets(as_of=as_of, **query)
        if results['totalResults'] == 1:
            return cls.__gs_asset_to_asset(results['results'][0])

        return None
