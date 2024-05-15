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
import json
import pandas as pd

from typing import Dict, Optional, List, Tuple
from pydash import get

from gs_quant.api.gs.assets import Currency, GsAsset, GsAssetApi
from gs_quant.common import DateLimit
from gs_quant.data.fields import DataMeasure
from gs_quant.entities.entity import EntityType, PositionedEntity
from gs_quant.errors import MqValueError
from gs_quant.instrument import Instrument
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets.securities import Asset, AssetType
from gs_quant.markets.indices_utils import *
from gs_quant.target.data import DataQuery
from gs_quant.entities.tree_entity import AssetTreeNode, TreeHelper


class Index(Asset, PositionedEntity):
    """
    Index which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets.
    Includes support for STS indices.
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

        if entity:
            self.asset_type = AssetType(entity['type'])
        else:
            self.asset_type = AssetType.INDEX

        if self.__is_sts_index():
            self.tree_helper = TreeHelper(id_, tree_underlier_dataset='STS_UNDERLIER_WEIGHTS')
            self.tree_df = pd.DataFrame()

    def __str__(self):
        return self.name

    def get_type(self) -> AssetType:
        return self.asset_type

    def get_currency(self) -> Optional[Currency]:
        return self.currency

    def get_return_type(self) -> ReturnType:
        if self.parameters is None or self.parameters.index_return_type is None:
            return ReturnType.TOTAL_RETURN

        return ReturnType(self.parameters.index_return_type)

    @classmethod
    def get(cls, identifier: str) -> Optional['Index']:
        """
        Fetch an existing index

        :param identifier: Any common identifier for an index(ric, ticker, etc.)
        :return: Index object

        **Usage**

        Get existing Index instance

        **Examples**

        Get index details:

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        """
        gs_asset = cls.__get_gs_asset(identifier)
        asset_entity: Dict = json.loads(json.dumps(gs_asset.as_dict(), cls=JSONEncoder))
        if gs_asset.type.value in STSIndexType.to_list() or gs_asset.type.value == 'Index':
            return cls(gs_asset.id, gs_asset.asset_class, gs_asset.name, exchange=gs_asset.exchange,
                       currency=gs_asset.currency, entity=asset_entity)
        else:
            raise MqValueError(f'{identifier} is not an Index identifier')

    def get_fundamentals(self,
                         start: dt.date = DateLimit.LOW_LIMIT.value,
                         end: dt.date = dt.date.today(),
                         period: Optional[DataMeasure] = None,
                         direction: DataMeasure = DataMeasure.FORWARD.value,
                         metrics: List[DataMeasure] = DataMeasure.list_fundamentals()) -> pd.DataFrame:
        """
        Retrieve fundamentals data for an index across a date range. Currently supports STS indices only

        :param start: start date (default is 1 January, 1970)
        :param end: end date (default is today)
        :param period: period for the relevant metric.  Can be one of ONE_YEAR('1y'), TWO_YEARS('2y'), \
            THREE_YEARS('3y') (default is all periods)
        :param direction: direction of the outlook period. Can be one of 'forward' or 'trailing' (default is forward)
        :param metrics: list of fundamentals metrics. (default is all)
        :return: dataframe with fundamentals information

        **Usage**

        Retrieve fundamentals data for an index across a date range

        **Examples**

        Retrieve historical dividend yield data for an index

        >>> from gs_quant.markets.index import Index
        >>> from gs_quant.data.fields import DataMeasure
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_fundamentals(metrics=[DataMeasure.DIVIDEND_YIELD])
        """
        if self.__is_sts_index():
            where = dict(assetId=self.id, periodDirection=direction, metric=metrics)
            if period:
                where["period"] = period
            query = DataQuery(where=where, start_date=start, end_date=end)
            response = GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.STS_FUNDAMENTALS.value)
            return pd.DataFrame(response)

        else:
            raise MqValueError('This method currently supports STS indices only')

    def get_latest_close_price(self, price_type: List[PriceType] = None) -> pd.DataFrame:
        """
        Retrieve latest close prices for an index. Only STS indices support indicative prices.

        :param price_type: Type of prices to return. Default returns official close price
        :return: dataframe with latest close price

        **Usage**

        Retrieve latest close prices for an index

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_latest_close_price([PriceType.OFFICIAL_CLOSE_PRICE, PriceType.INDICATIVE_CLOSE_PRICE])
        """
        if (not price_type) or (price_type == [PriceType.OFFICIAL_CLOSE_PRICE]):
            return super().get_latest_close_price()

        prices = pd.DataFrame()
        if PriceType.OFFICIAL_CLOSE_PRICE in price_type:
            official_level = super().get_latest_close_price()
            prices['date'] = official_level.index
            prices['closePrice'] = official_level[0]

        if PriceType.INDICATIVE_CLOSE_PRICE in price_type:
            if self.__is_sts_index():
                where = dict(assetId=self.id)
                query = DataQuery(where=where)
                response = GsDataApi.last_data(query=query, dataset_id=IndicesDatasets.STS_INDICATIVE_LEVELS.value)
                indicative_level = pd.DataFrame(response).iloc[-1:][['date', 'indicativeClosePrice']]
                prices['date'] = indicative_level['date'].iat[0]
                prices['indicativeClosePrice'] = indicative_level['indicativeClosePrice'].iat[0]

            else:
                raise MqValueError('PriceType.INDICATIVE_CLOSE_PRICE currently supports STS indices only')

        return prices

    def get_close_price_for_date(self,
                                 date: dt.date = dt.date.today(),
                                 price_type: List[PriceType] = None) -> pd.DataFrame:
        """
        Retrieve close prices for an index. Only STS indices support indicative prices.

        :param date: date of the required prices (default is today)
        :param price_type: Type of prices to return. Default returns official close price
        :return: dataframe with date's close prices

        **Usage**

        Retrieve the close prices for an index for a given date

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_close_price_for_date(dt.date(2021, 1, 7), \
        [PriceType.OFFICIAL_CLOSE_PRICE, PriceType.INDICATIVE_CLOSE_PRICE])
        """
        if (not price_type) or (price_type == [PriceType.OFFICIAL_CLOSE_PRICE]):
            return super().get_close_price_for_date(date)

        prices = pd.DataFrame()
        if PriceType.OFFICIAL_CLOSE_PRICE in price_type:
            official_level = super().get_close_price_for_date(date)
            prices['date'] = official_level.index
            prices['closePrice'] = official_level[0]

        if PriceType.INDICATIVE_CLOSE_PRICE in price_type:
            if self.__is_sts_index():
                response = self.__query_indicative_levels_dataset(start=date, end=date)
                indicative_level = pd.DataFrame(response)
                prices['date'] = indicative_level['date'].iat[0]
                prices['indicativeClosePrice'] = indicative_level['indicativeClosePrice'].iat[0]

            else:
                raise MqValueError('PriceType.INDICATIVE_CLOSE_PRICE currently supports STS indices only')

        return prices

    def get_close_prices(self,
                         start: dt.date = DateLimit.LOW_LIMIT.value,
                         end: dt.date = dt.date.today(),
                         price_type: List[PriceType] = None) -> pd.DataFrame:
        """
        Retrieve close prices for an index for a date range. Only STS indices support indicative prices.

        :param start: start date (default is 1 January, 1970)
        :param end: end date (default is today)
        :param price_type: Type of prices to return. Default returns official close price
        :return: dataframe with the close price between start and end date

        **Usage**

        Retrieve the close prices for an index for a given date range.

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_close_prices(dt.date(2021, 1, 7), dt.date(2021, 3, 27), \
        [PriceType.OFFICIAL_CLOSE_PRICE, PriceType.INDICATIVE_CLOSE_PRICE])
        """
        if (not price_type) or (price_type == [PriceType.OFFICIAL_CLOSE_PRICE]):
            return super().get_close_prices(start, end)

        prices = pd.DataFrame()

        if self.__is_sts_index():
            if price_type == [PriceType.INDICATIVE_CLOSE_PRICE]:
                indicative_level = self.__query_indicative_levels_dataset(start=start, end=end)
                indicative_level.drop(['updateTime', 'assetId'], axis=1, inplace=True)
                indicative_level = indicative_level.astype({'date': 'datetime64[ns]'})
                prices['date'] = indicative_level['date']
                prices['indicativeClosePrice'] = indicative_level['indicativeClosePrice']
                return prices

            official_level = super().get_close_prices(start=start, end=end).to_frame('closePrice')
            indicative_level = self.__query_indicative_levels_dataset(start=start, end=end)

            official_level.reset_index(inplace=True)
            indicative_level.drop(['updateTime', 'assetId'], axis=1, inplace=True)
            indicative_levels = indicative_level.astype({'date': official_level.dtypes['date']})
            merged = pd.merge(official_level, indicative_levels, on='date', how='outer')
            return merged

        else:
            raise MqValueError('PriceType.INDICATIVE_CLOSE_PRICE currently supports STS indices only')

    def get_underlier_tree(self,
                           refresh_tree: Optional[bool] = False) -> AssetTreeNode:
        """
        Get the root node of the tree formed by the Index, as an AssetTreeNode object.

        :param refresh_tree: Refresh the underliers information of the entire tree

        Please refer to the documenation of the AssetTreeNode class for more information.
        Currently supports STS indices only.

        :return: root node of the tree formed by the Index, as an AssetTreeNode object.

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_underlier_tree()
        """
        if self.__is_sts_index():
            if (not self.tree_helper.tree_built) or refresh_tree:

                self.tree_helper.build_tree()
                self.tree_helper.populate_weights('STS_UNDERLIER_WEIGHTS')
                self.tree_helper.populate_attribution('STS_UNDERLIER_ATTRIBUTION')
                self.tree_df = self.tree_helper.to_frame()

            return self.tree_helper.root

        else:
            raise MqValueError('This method currently supports STS indices only')

    def get_underlier_weights(self) -> pd.DataFrame:
        """
        Get the weights of the immediate (one-level-down) underliers of the Index.
        Currently supports STS indices only.

        :return: pandas DataFrame with the weights of the immediate underliers.

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_underlier_weights()
        """
        if self.__is_sts_index():
            if len(self.tree_df) == 0:
                self.get_underlier_tree()

            return self.tree_df.loc[self.tree_df.depth == 1].drop(columns=['absoluteAttribution', 'assetId',
                                                                           'assetName', 'depth'])
        else:
            raise MqValueError('This method currently supports STS indices only')

    def get_underlier_attribution(self) -> pd.DataFrame:
        """
        Get the attribution of the immediate (one-level-down) underliers of the Index.
        Currently supports STS indices only.

        :return: pandas DataFrame with the attribution of the immediate underliers.

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_underlier_attribution()
        """
        if self.__is_sts_index():
            if len(self.tree_df) == 0:
                self.get_underlier_tree()

            return self.tree_df.loc[self.tree_df.depth == 1].drop(columns=['weight', 'assetId', 'assetName', 'depth'])

        else:
            raise MqValueError('This method currently supports STS indices only')

    def visualise_tree(self,
                       visualise_by: Optional[str] = 'asset_name'):

        """
        Visualise the tree by printing the structure of the entire tree.
        The visualise_by argument can be either 'asset_name' or 'bbid'. Currently supports STS indices only.

        :param visualise_by: Parameter to visualise by. Default uses Asset Name to label the nodes
        :return: treelib Tree object, which can be printed to see the tree structure.

        **Examples**

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> print(index.visualise_tree())
        """

        if self.__is_sts_index():
            return self.tree_helper.get_visualisation(visualise_by)

        else:
            raise MqValueError('This method currently supports STS indices only')

    def get_latest_constituents(self) -> pd.DataFrame:
        """
        Fetch the latest constituents of the index in a pandas dataframe.

        :return: pandas dataframe with the index constituents, weights and other details.

        **Usage**

        Get the latest constituents of the index

        **Examples**

        Get latest index constituents:

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_latest_constituents()
        """

        return self.get_latest_position_set().get_positions()

    def get_constituents_for_date(self,
                                  date: dt.date = dt.date.today()) -> pd.DataFrame:
        """
        Fetch the constituents of the index in a pandas dataframe for a the given date.

        :return: pandas dataframe with the index constituents, weights and other details.

        **Usage**

        Get the constituents of the index for the given date

        **Examples**

        Get index constituents:

        >>> import datetime as dt
        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_constituents_for_date(dt.date(2021, 7, 1))
        """

        return self.get_position_set_for_date(date).get_positions()

    def get_constituents(self,
                         start: dt.date = DateLimit.LOW_LIMIT.value,
                         end: dt.date = dt.date.today()) -> List[pd.DataFrame]:
        """
        Fetch the constituents of the index in a pandas dataframe for the given date range

        :return: pandas dataframe with the index constituents, weights and other details.

        **Usage**

        Get the constituents of the index for the given date range

        **Examples**

        Get index constituents:

        >>> import datetime as dt
        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_constituents(dt.date(2021, 6, 1), dt.date(2021, 6, 10))
        """

        return [position_set.get_positions() for position_set in self.get_position_sets(start, end)]

    def get_latest_constituent_instruments(self) -> Tuple[Instrument, ...]:
        """
        Fetch the latest constituents of the index as instrument objects.

        :return: A Tuple of instrument objects

        **Usage**

        Get the latest constituents of the index

        **Examples**

        Get latest index constituent instruments:

        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_latest_constituent_instruments()
        """

        return GsAssetApi.get_instruments_for_positions(self.get_latest_position_set().to_target().positions)

    def get_constituent_instruments_for_date(self,
                                             date: dt.date = dt.date.today()) -> Tuple[Instrument, ...]:
        """
        Fetch the constituents of the index for a given date as instrument objects.

        :return: A Tuple of instrument objects

        **Usage**

        Get the constituents of the index for the given date as instrument objects

        **Examples**

        Get index constituent instruments:

        >>> import datetime as dt
        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_constituent_instruments_for_date(dt.date(2021, 7, 1))
        """

        return GsAssetApi.get_instruments_for_positions(self.get_position_set_for_date(date).to_target().positions)

    def get_constituent_instruments(self,
                                    start: dt.date = DateLimit.LOW_LIMIT.value,
                                    end: dt.date = dt.date.today()) -> Tuple[Tuple[Instrument, ...], ...]:
        """
        Fetch the constituents of the index as instrument objects for the given date range

        :return: Tuple of Tuples, containing all instrument objects for each date.

        **Usage**

        Get the constituents of the index for the given date range as instrument objects.

        **Examples**

        Get index constituent instruments:

        >>> import datetime as dt
        >>> from gs_quant.markets.index import Index
        >>>
        >>> index = Index.get("GSMBXXXX")
        >>> index.get_constituent_instruments(dt.date(2021, 6, 1), dt.date(2021, 6, 10))
        """
        position_sets = self.get_position_sets(start, end)
        return [GsAssetApi.get_instruments_for_positions(position_set.to_target().positions)
                for position_set in position_sets]

    def __is_sts_index(self) -> bool:
        """Checks if is an STS get_index"""

        if self.get_type().value in STSIndexType.to_list():
            return True
        return False

    def __query_indicative_levels_dataset(self, start=None, end=None) -> pd.DataFrame:

        where = dict(assetId=self.id)
        if start is None:
            query = DataQuery(where=where)
        else:
            query = DataQuery(where=where, start_date=start, end_date=end)

        response = GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.STS_INDICATIVE_LEVELS.value)
        indicative_level = pd.DataFrame(response)
        if (len(indicative_level) == 0):
            indicative_level['date'] = ''
            indicative_level['assetId'] = ''
            indicative_level['updateTime'] = ''
            indicative_level['indicativeClosePrice'] = ''
        return indicative_level

    @staticmethod
    def __get_gs_asset(identifier: str) -> GsAsset:
        """ Resolves index identifier during initialization """
        response = GsAssetApi.resolve_assets(identifier=[identifier], fields=['id'], limit=1)[identifier]
        if len(response) == 0 or get(response, '0.id') is None:
            raise MqValueError(f'Asset could not be found using identifier {identifier}')
        return GsAssetApi.get_asset(get(response, '0.id'))
