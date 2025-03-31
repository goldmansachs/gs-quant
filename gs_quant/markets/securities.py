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
import datetime as dt
import json
import logging
import threading
import time
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from copy import deepcopy
from enum import auto, Enum
from functools import partial
from typing import Tuple, Generator, Iterable, Optional, Dict, List, Union

import backoff
import cachetools
import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from pydash import get

from gs_quant.api.gs.assets import GsAsset, AssetParameters, AssetType as GsAssetType, Currency, GsIdType, GsAssetApi
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.utils import ThreadPoolManager
from gs_quant.base import get_enum_value
from gs_quant.common import DateLimit
from gs_quant.data import DataMeasure, DataFrequency, Dataset, AssetMeasure
from gs_quant.data.coordinate import DataDimensions
from gs_quant.data.coordinate import DateOrDatetime
from gs_quant.data.core import IntervalFrequency, DataAggregationOperator
from gs_quant.entities.entity import Entity, EntityIdentifier, EntityType, PositionedEntity
from gs_quant.errors import MqValueError, MqTypeError, MqRequestError
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets import PricingContext
from gs_quant.markets.indices_utils import BasketType, IndicesDatasets
from gs_quant.session import GsSession
from gs_quant.target.common import AssetClass
from gs_quant.target.data import DataQuery

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
    EQUITY_INDEX = 'Equity Index'
    COMMON_STOCK = 'Common Stock'


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
    CUSIP8 = "cusip8"
    CINS = "cins"
    SEDOL = "sedol"
    ISIN = "isin"
    TICKER = "ticker"
    BBID = "bbid"
    BCID = "bcid"
    GSS = "gss"
    PRIMEID = "primeId"
    BBG = "bbg"
    ASSET_ID = "assetId"
    ANY = "identifiers"
    BARRA_ID = "barraId"
    AXIOMA_ID = "axiomaId"


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
        return f'https://marquee{env}.gs.com/s/products/{self.get_marquee_id()}/summary'

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
            current = PricingContext.current
            if not current.is_entered:
                with current:
                    as_of = current.pricing_date
            else:
                as_of = current.pricing_date

            if isinstance(as_of, dt.datetime):
                as_of = as_of.date()

        valid_ids = set(item.value for item in AssetIdentifier)
        xrefs = GsAssetApi.get_asset_xrefs(self.get_marquee_id())
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
            return self.get_marquee_id()

        ids = self.get_identifiers(as_of=as_of)
        return ids.get(id_type.value)

    def get_asset_measures(self) -> List[AssetMeasure]:
        """
        Get asset measures

        :return: A list consisting of the following measures available for an asset: type, frequency, datasetField.
        For more details check the fields defined in class: 'AssetMeasures'

        **Usage**

        Get list of measures available for an asset

        **Examples**

        >>> from gs_quant.markets.securities import SecurityMaster,AssetIdentifier
        >>>
        >>> asset = SecurityMaster.get_asset("USDJPY", AssetIdentifier.BLOOMBERG_ID)
        >>> asset.get_asset_measures()

        **See also**

        :class:`AssetMeasures`

        """

        availability_response = GsSession.current._get(f'/data/measures/{self.get_marquee_id()}/availability')
        final_measure_set = set()

        if availability_response['data']:
            for measure_set in availability_response['data']:
                asset_measures = AssetMeasure.from_dict(measure_set)

                if {'type', 'frequency', 'datasetField'} <= measure_set.keys():
                    final_measure_set.add(asset_measures)

        return list(final_measure_set)

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
        elif coordinate.dataset_id is None:
            raise MqValueError(f"Measure '{measure.value}' not found for asset: {self.__id}")
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

        if self.asset_class == AssetClass.Equity:
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
        elif self.asset_class == AssetClass.FX:
            if interval_frequency != IntervalFrequency.DAILY:
                raise MqValueError('Unsupported IntervalFrequency for FX asset class.')
            ds = Dataset('FX_HLOC')
            df = ds.get_data(start=start, end=end, assetId=self.get_marquee_id())
            df = df.drop(columns=['assetId', 'updateTime']).reindex(columns=['high', 'low', 'open', 'close'])
        else:
            raise MqValueError('Unsupported AssetClass for HLOC data.')

        return df.dropna()

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


class SecMasterAsset(Asset):
    def __init__(self,
                 id_: str,
                 asset_type: AssetType,
                 asset_class: AssetClass,
                 name: str,
                 exchange: Optional[str] = None,
                 currency: Optional[str] = None,
                 parameters: AssetParameters = None,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class=asset_class, name=name, exchange=exchange, currency=currency,
                       parameters=parameters, entity=entity)
        self.__asset_type = asset_type
        self.__cached_identifiers = None

    def get_type(self) -> AssetType:
        return self.__asset_type

    def get_marquee_id(self):
        marquee_id = self.get_identifier(SecurityIdentifier.ASSET_ID)
        self.__id = marquee_id  # Updates Marquee Id in case it changes from context change
        if marquee_id is None:
            current = PricingContext.current
            if not current.is_entered:
                with current:
                    current_pricing_date = current.pricing_date
            else:
                current_pricing_date = current.pricing_date
            raise MqValueError(
                f"Current SecMasterAsset does not have a Marquee Id as of {current_pricing_date}. "
                f"Perhaps asset did not exist at that time, or is a not an exchange-level asset.")
        return marquee_id

    def get_identifier(self, id_type: Union[AssetIdentifier, SecurityIdentifier], as_of: dt.date = None):
        # Add an exception since original get_identifier() takes id_type: AssetIdentifier
        if not isinstance(id_type, SecurityIdentifier):
            raise MqTypeError(
                f"""Expected id_type: SecurityIdentifier.enum for Assets sourced from SecurityMaster.
                Received: {id_type}""")
        if id_type == SecurityIdentifier.GSID:
            return self.entity['identifiers'].get(SecurityIdentifier.GSID.value)
        if id_type == SecurityIdentifier.ID:
            return self.entity['id']
        ids = self.get_identifiers(as_of=as_of)
        return ids.get(id_type.value, None)

    def get_identifiers(self, as_of: dt.date = None) -> dict:
        # Cache identifiers if not already there
        if self.__cached_identifiers is None:
            self.__load_identifiers()
        # Retrieve from cached identifiers
        if as_of is None:
            current = PricingContext.current
            if not current.is_entered:
                with current:
                    as_of = current.pricing_date
            else:
                as_of = current.pricing_date
        identifiers = dict()
        for id_type in SecurityIdentifier:
            id_history = self.__cached_identifiers.get(id_type.value)
            if id_history is not None:
                for xref in id_history:
                    if xref["start_date"] <= as_of <= xref["end_date"]:
                        identifiers[id_type.value] = xref["value"]
                        break
        # Add GSID and ID as it is not exposed in Get Identifiers History
        identifiers[SecurityIdentifier.ID.value] = self.entity.get('id')
        identifiers[SecurityIdentifier.GSID.value] = self.entity.get('identifiers').get(SecurityIdentifier.GSID.value)
        # Mainly for currencies, where assetId is not exposed in Get Identifiers History
        if SecurityIdentifier.ASSET_ID.value not in identifiers and self.__asset_type == AssetType.CURRENCY:
            identifiers[SecurityIdentifier.ASSET_ID.value] = self.entity.get("identifiers").get("assetId")
        # TODO: BCID and BBID are not exposed in Get Identifiers History.
        return identifiers

    def get_data_series(self,
                        measure: DataMeasure,
                        dimensions: Optional[DataDimensions] = None,
                        frequency: Optional[DataFrequency] = None,
                        start: Optional[DateOrDatetime] = None,
                        end: Optional[DateOrDatetime] = None,
                        dates: List[dt.date] = None,
                        operator: DataAggregationOperator = None) -> pd.Series:
        """
        Will be also called by Asset.get_close_prices(),  Asset.get_close_price_for_date().
        """

        coordinate = self.get_data_coordinate(measure, dimensions, frequency)
        if coordinate is None:
            raise MqValueError(f"No data coordinate found for parameters:{measure, dimensions, frequency}")
        range_start, range_end = coordinate.get_range(start, end)

        if self.__is_validate_range(start=range_start, end=range_end):
            with PricingContext(range_start):
                return super(SecMasterAsset, self).get_data_series(measure=measure,
                                                                   dimensions=dimensions,
                                                                   frequency=frequency,
                                                                   start=range_start,
                                                                   end=range_end,
                                                                   dates=dates,
                                                                   operator=operator)

    def get_hloc_prices(self,
                        start: dt.date = DateLimit.LOW_LIMIT.value,
                        end: dt.date = dt.date.today(),
                        interval_frequency: IntervalFrequency = IntervalFrequency.DAILY) -> pd.DataFrame:

        if self.__is_validate_range(start=start, end=end):
            with PricingContext(start):
                return super(SecMasterAsset, self).get_hloc_prices(start=start, end=end,
                                                                   interval_frequency=interval_frequency)

    def __is_validate_range(self, start: DateOrDatetime, end: DateOrDatetime = dt.date.today()) -> bool:
        """
        Validates that only one Marquee Id exist in start and end.
        -   This function will return True if only one Marquee id exists in range.
        -   This function will raise MqValueError if either many Marquee Ids exists in or none exist in input range or
        the Id at start_date is not equal to id at end_date.

        Example:
                __cached_identifiers = {"assetId" : [{start: 2020-01-01, end: 2020-01-05, value: "marqueeId1"}
                                                     {start: 2020-01-06, end: 2020-10-10, value: "marqueeId2"}]}
                args = {start: 2020-01-01, end: 2020-01-07}

                return: MqValueError
        """
        if self.__cached_identifiers is None:
            self.__load_identifiers()

        if isinstance(start, datetime.datetime):
            start_date = start.date
        else:
            start_date = start

        if isinstance(end, datetime.datetime):
            end_date = end.date
        else:
            end_date = end

        with PricingContext(start_date):
            start_marquee_id = self.get_marquee_id()
        with PricingContext(end_date):
            end_marquee_id = self.get_marquee_id()
        if start_marquee_id is None or end_marquee_id is None or start_marquee_id != end_marquee_id:
            raise MqValueError(
                f"Asset's Marquee Id is either none or different. start:[{start_date}->{start_marquee_id}] to "
                f"end=[{end_date}->{end_marquee_id}].")

        marquee_id_xref = self.__cached_identifiers.get(SecurityIdentifier.ASSET_ID.value)
        marquee_ids = set()
        output_range_start = None
        output_range_end = None
        overlap_ranges = defaultdict(list)
        for xref in marquee_id_xref:
            if end_date < xref['start_date'] or start_date > xref['end_date']:  # Skip xrefs that are outside range
                continue
            marquee_id = xref.get("value")
            range_start = max(start_date, xref['start_date'])
            range_end = min(end_date, xref['end_date'])

            if range_start <= range_end:
                marquee_ids.add(marquee_id)
                overlap_ranges[marquee_id].append([range_start.strftime("%Y-%m-%d"),
                                                   range_end.strftime("%Y-%m-%d")])
                output_range_start = min(output_range_start,
                                         range_start) if output_range_start is not None else output_range_start
                output_range_end = max(output_range_end,
                                       range_end) if output_range_end is not None else output_range_end

        if len(marquee_ids) > 1:
            raise MqValueError(
                f"Asset has multiple Marquee ids between [start,end]=[{start_date},{end_date}] due to corporate "
                f"actions. Try limiting the range over a single Marquee id. Marquee Ids found: {overlap_ranges}.")
        if len(marquee_ids) == 0:
            raise MqValueError(
                f"Asset was not assigned Marquee Id over range [start,end]=[{start_date},{end_date}]. "
                f"Perhaps asset did not exist at that range, or is a not an exchange-level asset.")
        return True

    def __load_identifiers(self) -> None:
        if self.__cached_identifiers is None:
            r = GsSession.current._get(f'/markets/securities/{self.entity["id"]}/identifiers')
            results = r['results']
            xrefs = defaultdict(list)
            for temporal_xref in results:
                id_type = temporal_xref['type']
                xref_dict = {
                    "start_date": datetime.datetime.strptime(temporal_xref['startDate'], "%Y-%m-%d").date(),
                    "update_date": temporal_xref['updateTime'],
                    "value": temporal_xref['value']
                }
                if temporal_xref['endDate'] == "9999-99-99":
                    xref_dict['end_date'] = datetime.datetime.max.date()
                else:
                    xref_dict['end_date'] = datetime.datetime.strptime(temporal_xref['endDate'], "%Y-%m-%d").date()
                xrefs[id_type].append(xref_dict)
            self.__cached_identifiers = xrefs


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

    def get_thematic_beta(self,
                          basket_identifier: str,
                          start: dt.date = DateLimit.LOW_LIMIT.value,
                          end: dt.date = dt.date.today()) -> pd.DataFrame:

        response = GsAssetApi.resolve_assets(identifier=[basket_identifier],
                                             fields=['id', 'type'], limit=1)[basket_identifier]
        _id, _type = get(response, '0.id'), get(response, '0.type')
        if len(response) == 0 or _id is None:
            raise MqValueError(f'Basket could not be found using identifier {basket_identifier}.')
        if _type not in BasketType.to_list():
            raise MqValueError(f'Asset {basket_identifier} of type {_type} is not a Custom or Research Basket.')

        query = DataQuery(where={'gsid': self.get_identifier(AssetIdentifier.GSID, end), 'basketId': _id},
                          start_date=start, end_date=end)
        response = GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.THEMATIC_FACTOR_BETAS_STANDARD.value)
        df = []
        for r in response:
            df.append({'date': r['date'], 'gsid': r['gsid'], 'basketId': r['basketId'],
                       'thematicBeta': r['beta']})
        df = pd.DataFrame(df)
        return df.set_index('date')


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
                 asset_class: AssetClass = AssetClass.Credit,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class, name, entity=entity)

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
                 name: str,
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


class XccySwapMTM(Asset):
    """XccySwapMTM

    Represents a cross-currency mark-to-market swap.

    """

    def __init__(self,
                 id_: str,
                 name: str,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, AssetClass.Rates, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.XccySwapMTM


class MutualFund(Asset):
    """MutualFund

    Represents a mutual fund asset.
    """

    def __init__(self,
                 id_: str,
                 name: str,
                 asset_class: AssetClass,
                 entity: Optional[Dict] = None):
        Asset.__init__(self, id_, asset_class, name, entity=entity)

    def get_type(self) -> AssetType:
        return AssetType.MUTUAL_FUND


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
            return Bond(gs_asset.id, gs_asset.name, gs_asset.assetClass or AssetClass.Credit, entity=asset_entity)

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
            return DefaultSwap(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type == GsAssetType.Swaption.value:
            return Swaption(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type == GsAssetType.Binary.value:
            return Binary(gs_asset.id, gs_asset.name, gs_asset.assetClass, entity=asset_entity)

        if asset_type == GsAssetType.XccySwapMTM.value:
            return XccySwapMTM(gs_asset.id, gs_asset.name, entity=asset_entity)

        if asset_type == GsAssetType.Mutual_Fund.value:
            return MutualFund(gs_asset.id, gs_asset.name, gs_asset.asset_class, entity=asset_entity)

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
    def _get_asset_query(cls,
                         id_value: Union[str, List[str]],
                         id_type: Union[AssetIdentifier, SecurityIdentifier],
                         as_of: Union[dt.date, dt.datetime] = None,
                         exchange_code: ExchangeCode = None,
                         asset_type: AssetType = None) -> Tuple[Dict, dt.datetime]:
        if not as_of:
            current = PricingContext.current
            if not current.is_entered:
                with current:
                    as_of = current.pricing_date
            else:
                as_of = current.pricing_date
        if isinstance(as_of, dt.date):
            as_of = dt.datetime.combine(as_of, dt.time(0, 0), pytz.utc)
        query = {id_type.value.lower(): id_value}
        if exchange_code is not None:
            query['exchange'] = exchange_code.value
        if asset_type is not None:
            query['type'] = [t.value for t in cls.__asset_type_to_gs_types(asset_type)]
        return query, as_of

    @classmethod
    def _get_asset_results(cls, results, sort_by_rank) -> Asset:
        if sort_by_rank:
            result = get(results, '0')
            if result:
                result = GsAsset.from_dict(result)
        else:
            result = next(iter(results), None)
        if result:
            return cls.__gs_asset_to_asset(result)
        return None

    @classmethod
    def _get_many_assets_results(cls, results) -> List[Asset]:
        if results is not None:
            return [cls.__gs_asset_to_asset(result) for result in results]
        return []

    @classmethod
    def get_asset(cls,
                  id_value: str,
                  id_type: Union[AssetIdentifier, SecurityIdentifier],
                  as_of: Union[dt.date, dt.datetime] = None,
                  exchange_code: ExchangeCode = None,
                  asset_type: AssetType = None,
                  sort_by_rank: bool = True,
                  fields: Optional[List[str]] = None) -> Asset:
        """
        Get an asset by identifier and identifier type

        :param id_value: identifier value
        :param id_type: identifier type
        :param exchange_code: exchange code
        :param asset_type: asset type
        :param as_of: As of date for query
        :param sort_by_rank: whether to sort assets by rank. This flag is ignored when using SecMasterContext
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
            if exchange_code or asset_type:
                raise NotImplementedError('argument not implemented for Security Master (supported in Asset Service)')
            return cls._get_security_master_asset(id_value, id_type, as_of=as_of, fields=fields)

        if id_type is AssetIdentifier.MARQUEE_ID:
            gs_asset = GsAssetApi.get_asset(id_value)
            return cls.__gs_asset_to_asset(gs_asset)

        query, as_of = cls._get_asset_query(id_value, id_type, as_of, exchange_code, asset_type)
        if sort_by_rank:
            results = GsAssetApi.get_many_assets(as_of=as_of, return_type=dict, order_by=['>rank'], **query)
            return cls._get_asset_results(results, sort_by_rank)
        else:
            results = GsAssetApi.get_many_assets(as_of=as_of, **query)
            return cls._get_asset_results(results, sort_by_rank)

    @classmethod
    async def get_asset_async(cls,
                              id_value: str,
                              id_type: Union[AssetIdentifier, SecurityIdentifier],
                              as_of: Union[dt.date, dt.datetime] = None,
                              exchange_code: ExchangeCode = None,
                              asset_type: AssetType = None,
                              sort_by_rank: bool = True,
                              fields: Optional[List[str]] = None) -> Asset:
        """
        Get an asset by identifier and identifier type

        :param id_value: identifier value
        :param id_type: identifier type
        :param exchange_code: exchange code
        :param asset_type: asset type
        :param as_of: As of date for query
        :param sort_by_rank: whether to sort assets by rank. This flag is ignored when using SecMasterContext
        :param fields: asset fields to return
        :return: Asset object or None

        **Usage**

        Get asset object using a specified identifier and identifier type. Where the identifiers are temporal (and can
        change over time), will use the current MarketContext to evaluate based on the specified date.

        **Examples**

        Get asset by bloomberg id:

        >>> gs = await SecurityMaster.get_asset_async("GS UN", AssetIdentifier.BLOOMBERG_ID)

        Get asset by ticker and exchange code:

        >>> gs = await SecurityMaster.get_asset_async("GS", AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE)

        Get asset by ticker and asset type:

        >>> spx = await SecurityMaster.get_asset_async("SPX", AssetIdentifier.TICKER, asset_type=AssetType.INDEX)

        **See also**

        :class:`AssetIdentifier`
        :func:`get_many_assets`

        """
        if cls._source == SecurityMasterSource.SECURITY_MASTER:
            if not isinstance(id_type, SecurityIdentifier):
                raise MqTypeError('expected a security identifier')
            if exchange_code or asset_type:
                raise NotImplementedError('argument not implemented for Security Master (supported in Asset Service)')
            return await cls._get_security_master_asset_async(id_value, id_type, as_of=as_of, fields=fields)

        if id_type is AssetIdentifier.MARQUEE_ID:
            gs_asset = await GsAssetApi.get_asset_async(id_value)
            return cls.__gs_asset_to_asset(gs_asset)

        query, as_of = cls._get_asset_query(id_value, id_type, as_of, exchange_code, asset_type)
        if sort_by_rank:
            results = await GsAssetApi.get_many_assets_async(as_of=as_of, return_type=dict, order_by=['>rank'], **query)
            return cls._get_asset_results(results, sort_by_rank)
        else:
            results = await GsAssetApi.get_many_assets_async(as_of=as_of, **query)
            return cls._get_asset_results(results, sort_by_rank)

    @classmethod
    def get_many_assets(cls,
                        id_values: List[str],
                        id_type: AssetIdentifier,
                        limit: int = 100,
                        as_of: Union[dt.date, dt.datetime] = None,
                        exchange_code: ExchangeCode = None,
                        sort_by_rank: bool = True) -> List[Asset]:
        """
        Get an asset by identifier and identifier type

        :param id_values: identifier values
        :param id_type: identifiers type
        :param limit: max number of results
        :param exchange_code: exchange code
        :param as_of: As of date for query
        :param sort_by_rank: whether to sort assets by rank. This flag is ignored when using SecMasterContext
        :return: list of Asset objects or None

        **Usage**

        Get asset object using a specified identifier and identifier type. Where the identifiers are temporal (and can
        change over time), will use the current MarketContext to evaluate based on the specified date.

        **Examples**

        Get asset by bloomberg id:

        >>> gs = SecurityMaster.get_many_assets(["GS UN", "MSFT UW"], AssetIdentifier.BLOOMBERG_ID)

        Get asset by ticker and exchange code:

        >>> gs = SecurityMaster.get_many_assets(["GS", "MSFT"], AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE)

        Get asset by ticker and asset type:

        >>> spx = SecurityMaster.get_many_assets(["SPX"], AssetIdentifier.TICKER, asset_type=AssetType.INDEX)

        **See also**

        :class:`AssetIdentifier`
        :func:`get_many_assets`

        """
        query, as_of = cls._get_asset_query(id_values, id_type, as_of, exchange_code)
        if sort_by_rank:
            results = GsAssetApi.get_many_assets(as_of=as_of, order_by=['>rank'], limit=limit, **query)
        else:
            results = GsAssetApi.get_many_assets(as_of=as_of, limit=limit, **query)
        return cls._get_many_assets_results(results)

    @classmethod
    async def get_many_assets_async(cls,
                                    id_values: List[str],
                                    id_type: AssetIdentifier,
                                    limit: int = 100,
                                    as_of: Union[dt.date, dt.datetime] = None,
                                    exchange_code: ExchangeCode = None,
                                    sort_by_rank: bool = True) -> List[Asset]:
        """
        Get an asset by identifier and identifier type

        :param id_values: identifier values
        :param id_type: identifiers type
        :param limit: max number of results
        :param exchange_code: exchange code
        :param as_of: As of date for query
        :param sort_by_rank: whether to sort assets by rank. This flag is ignored when using SecMasterContext
        :return: list of Asset objects or None

        **Usage**

        Get asset object using a specified identifier and identifier type. Where the identifiers are temporal (and can
        change over time), will use the current MarketContext to evaluate based on the specified date.

        **Examples**

        Get asset by bloomberg id:

        >>> gs = await SecurityMaster.get_many_assets_async(["GS UN"], AssetIdentifier.BLOOMBERG_ID)

        Get asset by ticker and exchange code:

        >>> gs = await SecurityMaster.get_many_assets_async(["GS"], AssetIdentifier.TICKER,
        >>>                                                 exchange_code=ExchangeCode.NYSE)

        Get asset by ticker and asset type:

        >>> spx = await SecurityMaster.get_many_assets_async(["SPX"], AssetIdentifier.TICKER,
        >>>                                                  asset_type=AssetType.INDEX)

        **See also**

        :class:`AssetIdentifier`
        :func:`get_many_assets`

        """
        query, as_of = cls._get_asset_query(id_values, id_type, as_of, exchange_code)
        if sort_by_rank:
            results = await GsAssetApi.get_many_assets_async(as_of=as_of, order_by=['>rank'], limit=limit, **query)
        else:
            results = await GsAssetApi.get_many_assets_async(as_of=as_of, limit=limit, **query)
        return cls._get_many_assets_results(results)

    @classmethod
    def _get_security_master_asset_params(cls,
                                          id_value: str,
                                          id_type: SecurityIdentifier,
                                          as_of: Union[dt.date, dt.datetime] = None,
                                          fields: Optional[List[str]] = None) -> dict:
        as_of = as_of or datetime.datetime(2100, 1, 1)
        type_ = id_type.value
        params = {
            type_: id_value,
            'asOfDate': as_of.strftime('%Y-%m-%d')  # TODO: update endpoint to take times
        }
        if fields is not None:
            request_fields = {
                'identifiers',
                'assetClass',
                'type',
                'currency',
                'exchange',
                'id'
            }
            request_fields.update(fields)
            params['fields'] = request_fields
        return params

    @classmethod
    def _get_security_master_asset_response(cls, response) -> SecMasterAsset:
        if response['totalResults'] == 0:
            return None
        asset_dict = response['results'][0]
        asset_id = asset_dict['identifiers'].get("assetId", None)
        # Converting dict to Asset Class
        asset_name = asset_dict.get('name', None)
        asset_exchange = asset_dict.get("exchange").get("name", None) if "exchange" in asset_dict else None
        asset_currency = asset_dict.get('currency', None)
        try:
            asset_type = AssetType(asset_dict['type'])
            asset_class = AssetClass(asset_dict['assetClass'])
            return SecMasterAsset(id_=asset_id,
                                  asset_type=asset_type,
                                  asset_class=asset_class,
                                  name=asset_name,
                                  exchange=asset_exchange,
                                  currency=asset_currency,
                                  entity=asset_dict)
        except ValueError:
            raise NotImplementedError(f"Not yet implemented for AssetType={asset_dict['type']}, "
                                      f"AssetClass={asset_dict['assetClass']}.")

    @classmethod
    def _get_security_master_asset(cls,
                                   id_value: str,
                                   id_type: SecurityIdentifier,
                                   as_of: Union[dt.date, dt.datetime] = None,
                                   fields: Optional[List[str]] = None) -> SecMasterAsset:
        params = cls._get_security_master_asset_params(id_value, id_type, as_of, fields)
        response = GsSession.current._get('/markets/securities', payload=params)
        return cls._get_security_master_asset_response(response)

    @classmethod
    async def _get_security_master_asset_async(cls,
                                               id_value: str,
                                               id_type: SecurityIdentifier,
                                               as_of: Union[dt.date, dt.datetime] = None,
                                               fields: Optional[List[str]] = None) -> SecMasterAsset:
        params = cls._get_security_master_asset_params(id_value, id_type, as_of, fields)
        response = await GsSession.current._get_async('/markets/securities', payload=params)
        return cls._get_security_master_asset_response(response)

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
            p = partial(cls.asset_type_to_str, class_)
            types = set(map(p, types))

        params = {
            'fields': ['id', 'identifiers', 'assetClass', 'type'],
            'asOfDate': as_of.date(),
            'limit': cls._page_size,
            'type': types
        }

        while True:
            r = _get_with_retries('/markets/securities', params)
            if r['totalResults'] == 0:
                return

            output = {}

            for e in r['results']:
                # TODO: perform assetClass filtering on server side once assetClass is supported (just Equties is
                #  supported for now)
                if class_ is None or e['assetClass'] == class_.value:
                    box = e['identifiers']
                    box['id'] = e['id']  # copy top-level security id into result
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
    def map_identifiers(
            cls,
            input_type: SecurityIdentifier,
            ids: Iterable[str],
            output_types: Iterable[SecurityIdentifier] = frozenset([SecurityIdentifier.GSID]),
            start_date: datetime.date = None,
            end_date: datetime.date = None,
            as_of_date: datetime.date = None
    ) -> Dict[datetime.date, dict]:
        """
        Map to other identifier types, from given IDs.

        :param input_type: type of input IDs
        :param ids: security IDs
        :param output_types: types of IDs to map to
        :param start_date: first as-of date (defaults to current date)
        :param end_date: last as-of date (defaults to current date)
        :param as_of_date: an exact as-of date for mapping
        :return: dict containing mappings for as-of date(s)

        **Examples**

        Get CUSIP for GS UN:
        >>> result = SecurityMaster.map_identifiers(SecurityIdentifier.BBID, ["GS UN"], [SecurityIdentifier.CUSIP])

        Get Bloomberg ticker for 104563 as-of a past date:
        >>> result = SecurityMaster.map_identifiers(SecurityIdentifier.GSID, ["104563"], [SecurityIdentifier.BBG],
        ...                                         as_of_date=datetime.date(2021, 4, 19))
        """
        if isinstance(ids, str):
            raise MqTypeError("expected an iterable of strings e.g. list of strings")

        def get_asset_id_type(type_: SecurityIdentifier):
            try:
                return GsIdType[type_.value]
            except KeyError:
                raise MqValueError(f'unsupported type {type_.value}')

        if cls._source == SecurityMasterSource.ASSET_SERVICE:
            output_types = list(output_types)
            if len(output_types) != 1:
                raise MqValueError('provide exactly one output type')
            if (start_date or end_date) is not None:
                raise MqValueError('use as_of_date instead of start_date and/or end_date')
            if as_of_date is None:
                as_of_date = datetime.date.today()

            input_type = get_asset_id_type(input_type)
            output_type = get_asset_id_type(output_types[0])
            as_of = None if as_of_date is None else datetime.datetime.combine(as_of_date,
                                                                              datetime.time(tzinfo=pytz.UTC))
            result = GsAssetApi.map_identifiers(input_type, output_type, list(ids), as_of=as_of, multimap=True)
            if len(result) == 0:
                return result
            inner = {k: {output_type.name: v} for k, v in result.items()}
            return {as_of.strftime('%Y-%m-%d'): inner}

        assert cls._source == SecurityMasterSource.SECURITY_MASTER
        params = {
            input_type.value: list(ids),
            'toIdentifiers': [identifier.value for identifier in output_types],
            'compact': True
        }
        if as_of_date is not None:
            if (start_date or end_date) is not None:
                raise MqValueError('provide (start date / end date) or as-of date, but not both')
            params['startDate'] = as_of_date
            params['endDate'] = as_of_date

        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['endDate'] = end_date
        r = _get_with_retries('/markets/securities/map', params)

        results = r['results']
        if isinstance(results, dict):
            return results

        output = dict()
        date_format = '%Y-%m-%d'
        date_delta = datetime.timedelta(days=1)
        for row in results:
            current = datetime.datetime.strptime(row['startDate'], date_format)
            end = datetime.datetime.strptime(row['endDate'], date_format)
            while current <= end:
                outer = output.setdefault(current, dict())
                inner = outer.setdefault(row["input"], dict())
                output_type = row["outputType"]
                output_value = row["outputValue"]
                if output_type == "ric":
                    if SecurityIdentifier.RIC in output_types:
                        values = inner.setdefault('ric', [])
                        if output_value not in values:
                            values.append(output_value)
                    if SecurityIdentifier.ASSET_ID in output_types and "assetId" in row:
                        values = inner.setdefault('assetId', [])
                        asset_id = row['assetId']
                        if asset_id not in values:
                            values.append(asset_id)
                elif output_type == "bbg":
                    if SecurityIdentifier.BBG in output_types:
                        if SecurityIdentifier.BBG.value not in inner:
                            inner[SecurityIdentifier.BBG.value] = []
                        inner[SecurityIdentifier.BBG.value].append(output_value)
                    if SecurityIdentifier.BBID in output_types:
                        exchange = row.get('exchange')
                        if SecurityIdentifier.BBID.value not in inner:
                            inner[SecurityIdentifier.BBID.value] = []
                        if exchange is not None:
                            inner[SecurityIdentifier.BBID.value].append(f"{output_value} {exchange}")
                        else:
                            inner[SecurityIdentifier.BBID.value].append(f"{output_value}")
                    if SecurityIdentifier.BCID in output_types:
                        composite_exchange = row.get('compositeExchange')
                        if composite_exchange is not None:
                            if SecurityIdentifier.BCID.value not in inner:
                                inner[SecurityIdentifier.BCID.value] = []
                            inner[SecurityIdentifier.BCID.value].append(f"{output_value} {composite_exchange}")
                else:
                    if SecurityIdentifier(output_type) in output_types:
                        if output_type not in inner:
                            inner[output_type] = []
                        if output_value not in inner[output_type]:
                            inner[output_type].append(output_value)

                current += date_delta

        # much faster to run strftime (once for each date) at the end
        return {k.strftime(date_format): v for k, v in output.items()}
