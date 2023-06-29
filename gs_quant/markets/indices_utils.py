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
import pandas as pd

from enum import Enum
from functools import partial, reduce
from pydash import get
from time import sleep
from typing import Dict, List, Optional, Union

from gs_quant.api.gs.assets import AssetClass, GsAssetApi
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.monitors import GsMonitorsApi
from gs_quant.api.utils import ThreadPoolManager
from gs_quant.base import EnumBase
from gs_quant.datetime.date import prev_business_date
from gs_quant.session import GsSession
from gs_quant.target.data import DataQuery


QUERY_LIMIT = 1000


class BasketType(EnumBase, Enum):
    """ Basket Types """
    CUSTOM_BASKET = 'Custom Basket'
    RESEARCH_BASKET = 'Research Basket'

    def __repr__(self):
        return self.value

    @classmethod
    def to_list(cls):
        return [basket_type.value for basket_type in cls]


class CorporateActionType(EnumBase, Enum):
    """ Different types of corporate actions """
    ACQUISITION = 'Acquisition'
    CASH_DIVIDEND = 'Cash Dividend'
    IDENTIFIER_CHANGE = 'Identifier Change'
    RIGHTS_ISSUE = 'Rights Issue'
    SHARE_CHANGE = 'Share Change'
    SPECIAL_DIVIDEND = 'Special Dividend'
    SPIN_OFF = 'Spin Off'
    STOCK_DIVIDEND = 'Stock Dividend'
    STOCK_SPLIT = 'Stock Split'

    def __repr__(self):
        return self.value

    @classmethod
    def to_list(cls):
        return [ca_type.value for ca_type in cls]


class CustomBasketStyles(EnumBase, Enum):
    """ Styles for Custom Baskets """
    AD_HOC_DESK_WORK = 'Ad Hoc Desk Work'
    CLIENT_CONSTRUCTED_WRAPPER = 'Client Constructed/Wrapper'
    CONSUMER = 'Consumer'
    ENERGY = 'Energy'
    ENHANCED_INDEX_SOLUTIONS = 'Enhanced Index Solutions'
    ESG = 'ESG'
    FACTORS = 'Factors'
    FINANCIALS = 'Financials'
    FLAGSHIP = 'Flagship'
    GEOGRAPHIC = 'Geographic'
    GROWTH = 'Growth'
    HEALTHCARE = 'Health Care'
    HEDGING = 'Hedging'
    INDUSTRIALS = 'Industrials'
    MATERIALS = 'Materials'
    MOMENTUM = 'Momentum'
    PIPG = 'PIPG'
    SECTORS_INDUSTRIES = 'Sectors/Industries'
    SIZE = 'Size'
    STRUCTURED_ONE_DELTA = 'Structured One Delta'
    THEMATIC = 'Thematic'
    TMT = 'TMT'
    UTILITIES = 'Utilities'
    VALUE = 'Value'
    VOLATILITY = 'Volatility'

    def __repr__(self):
        return self.value


class IndicesDatasets(EnumBase, Enum):
    """ Indices Datasets """
    BASKET_FUNDAMENTALS = 'BASKET_FUNDAMENTALS'
    COMPOSITE_THEMATIC_BETAS = 'COMPOSITE_THEMATIC_BETAS'
    CREDIT_EOD_PRICING_V1_STANDARD = 'CREDIT_EOD_PRICING_V1_STANDARD'
    CORPORATE_ACTIONS = 'CA'
    GIRBASKETCONSTITUENTS = 'GIRBASKETCONSTITUENTS'
    GSBASKETCONSTITUENTS = 'GSBASKETCONSTITUENTS'
    GSCB_FLAGSHIP = 'GSCB_FLAGSHIP'
    GSCREDITBASKETCONSTITUENTS = 'GSCREDITBASKETCONSTITUENTS'
    STS_FUNDAMENTALS = 'STS_FUNDAMENTALS'
    STS_INDICATIVE_LEVELS = 'STS_INDICATIVE_LEVELS'
    THEMATIC_FACTOR_BETAS_STANDARD = 'THEMATIC_FACTOR_BETAS_V2_STANDARD'

    def __repr__(self):
        return self.value


class PriceType(EnumBase, Enum):
    """ Index Price Types """
    INDICATIVE_CLOSE_PRICE = 'indicativeClosePrice'
    OFFICIAL_CLOSE_PRICE = 'officialClosePrice'

    def __repr__(self):
        return self.value

    @classmethod
    def to_list(cls):
        return [price_type for price_type in cls]


class Region(EnumBase, Enum):
    """ Region of the index """
    AMERICAS = 'Americas'
    ASIA = 'Asia'
    EM = 'EM'
    EUROPE = 'Europe'
    GLOBAL = 'Global'

    def __repr__(self):
        return self.value


class ResearchBasketStyles(EnumBase, Enum):
    """ Styles for Research Baskets """
    ASIA_EX_JAPAN = 'Asia ex-Japan'
    EQUITY_THEMATIC = 'Equity Thematic'
    EUROPE = 'Europe'
    FUND_OWNERSHIP = 'Fund Ownership'
    FUNDAMENTALS = 'Fundamentals'
    FX_OIL = 'FX/Oil'
    GEOGRAPHICAL_EXPOSURE = 'Geographical Exposure'
    HEDGE_FUND = 'Hedge Fund'
    IP_FACTORS = 'Investment Profile (IP) Factors'
    JAPAN = 'Japan'
    MACRO = 'Macro'
    MACRO_SLICE_STYLES = 'Macro Slice/Styles'
    MUTUAL_FUND = 'Mutual Fund'
    POSITIONING = 'Positioning'
    PORTFOLIO_STRATEGY = 'Portfolio Strategy'
    RISK_AND_LIQUIDITY = 'Risk & Liquidity'
    SECTOR = 'Sector'
    SHAREHOLDER_RETURN = 'Shareholder Return'
    STYLE_FACTOR_AND_FUNDAMENTAL = 'Style, Factor and Fundamental'
    STYLES_THEMES = 'Style/Themes'
    TACTICAL_RESEARCH = 'Tactical Research'
    THEMATIC = 'Thematic'
    US = 'US'
    WAVEFRONT_COMPONENTS = 'Wavefront Components'
    WAVEFRONT_PAIRS = 'Wavefront Pairs'
    WAVEFRONTS = 'Wavefronts'

    def __repr__(self):
        return self.value


class ReturnType(EnumBase, Enum):
    """ Determines the index calculation methodology with respect to dividend reinvestment """
    GROSS_RETURN = 'Gross Return'
    PRICE_RETURN = 'Price Return'
    TOTAL_RETURN = 'Total Return'

    def __repr__(self):
        return self.value


class STSIndexType(EnumBase, Enum):
    """ STS Types """

    ACCESS = 'Access'
    MULTI_ASSET_ALLOCATION = 'Multi-Asset Allocation'
    RISK_PREMIA = 'Risk Premia'
    SYSTEMATIC_HEDGING = 'Systematic Hedging'

    def __repr__(self):
        return self.value

    @classmethod
    def to_list(cls):
        return [sts_type.value for sts_type in cls]


class WeightingStrategy(EnumBase, Enum):
    """ Strategy used to price the index's position set """
    EQUAL = 'Equal'
    MARKET_CAPITALIZATION = 'Market Capitalization'
    QUANTITY = 'Quantity'
    WEIGHT = 'Weight'

    def __repr__(self):
        return self.value


def get_my_baskets(user_id: str = None) -> Optional[pd.DataFrame]:
    """
    Retrieve a list of baskets a user is permissioned to

    :param user_id: Marquee user/app ID (default is current application's id)
    :return: dataframe of baskets user has access to

    **Usage**

    Retrieve a list of baskets a user is permissioned to

    **Examples**

    Retrieve a list of baskets the current user is permissioned to

    >>> from gs_quant.markets.indices_utils import *
    >>>
    >>> get_my_baskets()
    """
    user_id = user_id if user_id is not None else GsSession.current.client_id
    tag = f'Custom Basket:{user_id}'
    response = GsMonitorsApi.get_monitors(tags=tag)
    if len(response):
        row_groups = get(response, '0.parameters.row_groups')
        my_baskets = []
        for row_group in row_groups:
            entity_ids = [entity.id for entity in row_group.entity_ids]
            baskets = GsAssetApi.get_many_assets_data(id=entity_ids, fields=['id', 'ticker', 'name', 'liveDate'])
            my_baskets += [dict(monitor_name=row_group.name, id=get(basket, 'id'), ticker=get(basket, 'ticker'),
                                name=get(basket, 'name'), live_date=get(basket, 'liveDate')) for basket in baskets]
        return pd.DataFrame(my_baskets)


def __get_baskets(fields: List[str] = [],
                  basket_type: List[BasketType] = BasketType.to_list(),
                  asset_class: List[AssetClass] = [AssetClass.Equity],
                  region: List[Region] = None,
                  styles: List[Union[CustomBasketStyles, ResearchBasketStyles]] = None,
                  as_of: dt.datetime = None,
                  **kwargs) -> Dict:
    default_fields = set(['id', 'name', 'ticker', 'region', 'type', 'description', 'styles', 'liveDate', 'assetClass'])
    query, fields = {}, list(set(fields).union(default_fields))
    for k, v in kwargs.items():
        query[k] = v
    if region:
        query['region'] = region
    if styles:
        query['styles'] = styles
    query = dict(fields=fields, type=basket_type, asset_class=asset_class, is_pair_basket=[False],
                 flagship=[True], **query)
    return GsAssetApi.get_many_assets_data_scroll(**query, as_of=as_of, limit=QUERY_LIMIT, scroll='1m')


def __get_dataset_id(asset_class: AssetClass, basket_type: BasketType, data_type: str) -> str:
    if asset_class == AssetClass.Equity or asset_class == AssetClass.Equity.value:
        if data_type == 'price':
            return IndicesDatasets.GSCB_FLAGSHIP.value
        elif basket_type == BasketType.CUSTOM_BASKET or basket_type == BasketType.CUSTOM_BASKET.value:
            return IndicesDatasets.GSBASKETCONSTITUENTS.value
        else:
            return IndicesDatasets.GIRBASKETCONSTITUENTS.value
    raise NotImplementedError(f'{data_type} data for {asset_class} baskets is unsupported at this time')


def get_flagship_baskets(fields: List[str] = [],
                         basket_type: List[BasketType] = BasketType.to_list(),
                         asset_class: List[AssetClass] = [AssetClass.Equity],
                         region: List[Region] = None,
                         styles: List[Union[CustomBasketStyles, ResearchBasketStyles]] = None,
                         as_of: dt.datetime = None,
                         **kwargs) -> pd.DataFrame:
    """
    Retrieve flagship baskets

    :param fields: Fields to retrieve in addition to mqid, name, ticker, region, basket type, \
        description, styles, live date, and asset class
    :param basket_type: Basket type(s)
    :param asset_class: Asset class (defaults to Equity)
    :param region: Basket region(s)
    :param styles: Basket style(s)
    :param as_of: Datetime for which to retrieve baskets (defaults to current time)
    :return: flagship baskets

    **Usage**

    Retrieve a list of flagship baskets

    **Examples**

    Retrieve a list of flagship baskets

    >>> from gs_quant.markets.indices_utils import *
    >>>
    >>> get_flagship_baskets()

    **See also**

    :func:`get_flagships_with_assets` :func:`get_flagships_performance` :func:`get_flagships_constituents`
    """
    response = __get_baskets(fields=fields, as_of=as_of, basket_type=basket_type, asset_class=asset_class,
                             region=region, styles=styles, **kwargs)
    return pd.DataFrame(response)


def get_flagships_with_assets(identifiers: List[str],
                              fields: List[str] = [],
                              basket_type: List[BasketType] = BasketType.to_list(),
                              asset_class: List[AssetClass] = [AssetClass.Equity],
                              region: List[Region] = None,
                              styles: List[Union[CustomBasketStyles, ResearchBasketStyles]] = None,
                              as_of: dt.datetime = None,
                              **kwargs) -> pd.DataFrame:
    """
    Retrieve a list of flagship baskets containing specified assets

    :param identifiers: List of asset identifiers
    :param fields: Fields to retrieve in addition to mqid, name, ticker, region, basket type, \
        description, styles, live date, and asset class
    :param basket_type: Basket type(s)
    :param asset_class: Asset class (defaults to Equity)
    :param region: Basket region(s)
    :param styles: Basket style(s)
    :param as_of: Datetime for which to retrieve baskets (defaults to current time)
    :return: flagship baskets containing specified assets

    **Usage**

    Retrieve a list of flagship baskets containing specified assets

    **Examples**

    Retrieve a list of flagship custom baskets containing 'AAPL UW' single stock

    >>> from gs_quant.markets.indices_utils import *
    >>>
    >>> get_flagships_with_assets(identifiers=['AAPL UW'], basket_type=[BasketType.CUSTOM_BASKET])

    **See also**

    :func:`get_flagship_baskets` :func:`get_flagships_performance` :func:`get_flagships_constituents`
    """
    response = GsAssetApi.resolve_assets(identifier=identifiers, fields=['id'], limit=1)
    mqids = [get(asset, '0.id') for asset in response.values()]
    response = __get_baskets(fields=fields, as_of=as_of, basket_type=basket_type, asset_class=asset_class,
                             region=region, styles=styles, underlying_asset_ids=mqids, **kwargs)
    return pd.DataFrame(response)


def get_flagships_performance(fields: List[str] = [],
                              basket_type: List[BasketType] = BasketType.to_list(),
                              asset_class: List[AssetClass] = [AssetClass.Equity],
                              region: List[Region] = None,
                              styles: List[Union[CustomBasketStyles, ResearchBasketStyles]] = None,
                              start: dt.date = None,
                              end: dt.date = None,
                              **kwargs) -> pd.DataFrame:
    """
    Retrieve performance data for flagship baskets

    :param fields: Fields to retrieve in addition to bbid, mqid, name, region, basket type, \
        styles, live date, and asset class
    :param basket_type: Basket type(s)
    :param asset_class: Asset class (defaults to Equity)
    :param region: Basket region(s)
    :param styles: Basket style(s)
    :param start: Date for which to retrieve pricing (defaults to previous business day)
    :param end: Date for which to retrieve pricing (defaults to previous business day)
    :return: pricing data for flagship baskets

    **Usage**

    Retrieve performance data for flagship baskets

    **Examples**

    Retrieve performance data for flagship Asia custom baskets

    >>> from gs_quant.markets.indices_utils import *
    >>>
    >>> get_flagships_performance(basket_type=[BasketType.CUSTOM_BASKET], region=[Region.ASIA])

    **See also**

    :func:`get_flagships_with_assets` :func:`get_flagship_baskets` :func:`get_flagships_constituents`
    """
    start, end = start or prev_business_date(), end or prev_business_date()
    assets = __get_baskets(fields=fields, basket_type=basket_type, asset_class=asset_class, region=region,
                           styles=styles, **kwargs)
    baskets = {b.get('id'): b for b in assets}
    dataset_id = __get_dataset_id(asset_class=asset_class[0], basket_type=basket_type[0], data_type='price')
    coverage = GsDataApi.get_coverage(dataset_id=dataset_id, fields=['id'])
    mqids = [b.get('assetId') for b in coverage if b.get('assetId') in baskets.keys()]
    batches = [mqids[i * 500:(i + 1) * 500] for i in range((len(mqids) + 500 - 1) // 500)]
    response, performance = [], []
    for b in batches:
        response += GsDataApi.query_data(query=DataQuery(where={'assetId': b}, startDate=start, endDate=end),
                                         dataset_id=dataset_id)
    for b in response:
        data = baskets.get(b.get('assetId'))
        b.update(data)
        b.pop('assetId')
        b.pop('updateTime')
        performance.append(b)
    return pd.DataFrame(performance)


def get_flagships_constituents(fields: List[str] = [],
                               basket_type: List[BasketType] = BasketType.to_list(),
                               asset_class: List[AssetClass] = [AssetClass.Equity],
                               region: List[Region] = None,
                               styles: List[Union[CustomBasketStyles, ResearchBasketStyles]] = None,
                               start: dt.date = None,
                               end: dt.date = None,
                               **kwargs) -> pd.DataFrame:
    """
    Retrieve flagship baskets constituents

    :param fields: Fields to retrieve in addition to mqid, name, ticker, region, basket type, \
        styles, live date, and asset class
    :param basket_type: Basket type(s)
    :param asset_class: Asset class (defaults to Equity)
    :param region: Basket region(s)
    :param styles: Basket style(s)
    :param start: Start date for which to retrieve constituents (defaults to previous business day)
    :param end: End date for which to retrieve constituents (defaults to previous business day)
    :return: flagship baskets constituents

    **Usage**

    Retrieve flagship baskets constituents

    **Examples**

    Retrieve a list of flagship baskets constituents

    >>> from gs_quant.markets.indices_utils import *
    >>>
    >>> get_flagships_constituents()

    **See also**

    :func:`get_flagships_with_assets` :func:`get_flagships_performance` :func:`get_flagship_baskets`
    """
    start, end = start or prev_business_date(), end or prev_business_date()
    basket_fields = list(set(fields).union(set(['id', 'name', 'ticker', 'region', 'type', 'styles',
                                               'liveDate', 'assetClass'])))
    fields = list(set(fields).union(set(['id'])))
    response = __get_baskets(fields=['id'], basket_type=basket_type, asset_class=asset_class,
                             region=region, styles=styles, **kwargs)
    basket_ids = [b.get('id') for b in response]
    cov_dataset_id = __get_dataset_id(asset_class=asset_class[0], basket_type=basket_type[0], data_type='price')
    coverage = GsDataApi.get_coverage(dataset_id=cov_dataset_id, fields=basket_fields, include_history=True)
    basket_map = {b['assetId']: {**b, 'constituents': []} for b in coverage if b['assetId'] in basket_ids}

    basket_dataset_query_map, constituents_data, tasks = {}, [], []
    # get appropriate dataset for each basket
    for b in basket_map.values():
        dataset_id = __get_dataset_id(asset_class=b['assetClass'], basket_type=b['type'], data_type='constituents')
        if dataset_id:
            basket_dataset_query_map[dataset_id] = basket_dataset_query_map.get(dataset_id, []) + [b['assetId']]

    # query constituents in batches of 25
    for ds, ids in basket_dataset_query_map.items():
        batches = [ids[i * 25:(i + 1) * 25] for i in range((len(ids) + 25 - 1) // 25)]
        for batch in batches:
            tasks.append(partial(GsDataApi.query_data,
                                 query=DataQuery(where={'assetId': batch}, startDate=start, endDate=end),
                                 dataset_id=ds))

    # run 5 parallel dataset queries at a time
    tasks = [tasks[i * 5:(i + 1) * 5] for i in range((len(tasks) + 5 - 1) // 5)]
    for task in tasks:
        constituents_data += ThreadPoolManager.run_async(task)
        sleep(1)
    constituents_data = reduce(lambda a, b: a + b, constituents_data)

    # fetch asset positions data
    asset_ids = set([row['underlyingAssetId'] for row in constituents_data])
    asset_data = GsAssetApi.get_many_assets_data_scroll(id=asset_ids, fields=fields, limit=QUERY_LIMIT, scroll='1m')
    asset_data_map = {get(asset, 'id'): asset for asset in asset_data}

    for row in constituents_data:
        basket_id = get(row, 'assetId', '')
        asset_id = get(row, 'underlyingAssetId', '')
        asset_id_map = get(asset_data_map, asset_id, {})
        for f in fields:
            row[f] = get(asset_id_map, f)
        basket_map[basket_id]['constituents'].append(row)

    return pd.DataFrame([r for r in basket_map.values() if r is not None])


def get_constituents_dataset_coverage(basket_type: BasketType = BasketType.CUSTOM_BASKET,
                                      asset_class: AssetClass = AssetClass.Equity,
                                      as_of: dt.datetime = None) -> pd.DataFrame:
    """
    Retrieve a list of baskets covered by constituents datasets

    :param basket_type: Basket type
    :param asset_class: Asset class (defaults to Equity)
    :param as_of: Date for which to retrieve coverage
    :return: baskets covered by the constituents dataset

    **Usage**

    Retrieve a list of baskets covered by constituents datasets

    **Examples**

    Retrieve basket constituent dataset coverage

    >>> from gs_quant.markets.indices_utils import *
    >>>
    >>> GSBASKETCONSTITUENTS_COVERAGE = get_constituents_dataset_coverage()
    >>> GIRBASKETCONSTITUENTS_COVERAGE = get_constituents_dataset_coverage(basket_type=BasketType.RESEARCH_BASKET)
    >>> GSCREDITBASKETCONSTITUENTS_COVERAGE = get_constituents_dataset_coverage(asset_class=AssetClass.Credit)

    **See also**

    :func:`get_flagships_constituents`
    """
    query = dict(fields=['id', 'name', 'region', 'ticker', 'type', 'assetClass'], type=[basket_type],
                 asset_class=[asset_class], is_pair_basket=[False], listed=[True])
    if asset_class != AssetClass.Equity:
        query.pop('is_pair_basket')
    response = GsAssetApi.get_many_assets_data_scroll(**query, as_of=as_of, limit=QUERY_LIMIT, scroll='1m')
    return pd.DataFrame(response)
