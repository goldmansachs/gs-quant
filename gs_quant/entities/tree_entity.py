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

import pandas as pd
import datetime as dt

from typing import Optional
from pydash import get

from gs_quant.api.gs.assets import GsAsset, GsAssetApi
from gs_quant.data import Dataset
from gs_quant.errors import MqValueError


class AssetTreeNode:
    def __init__(self, id, depth: Optional[int] = 0, date: Optional[dt.date] = None, asset: Optional[GsAsset] = None):

        self.id = id
        self.date = date    # date for which the Tree is constructed. If None, it is set to the latest available date.
        self.depth = depth  # depth of the node with respect to the root node
        self.asset = asset
        self.name = get(self.asset, 'name')
        self.bbid = get(get(self.asset, 'xref'), 'bbid')
        self.asset_type = get(self.asset, 'type')
        self.data = {}
        self.constituents_df = pd.DataFrame()
        self.direct_underlier_assets_as_nodes = []  # holds the child nodes as AssetTreeNode objects.

    def __str__(self):
        result = self.bbid if self.bbid is not None else self.id
        return f'Tree Node - {result}'

    def to_frame(self) -> pd.DataFrame:
        if len(self.constituents_df) > 0:
            return self.constituents_df
        else:
            self.constituents_df = self.__build_constituents_df(pd.DataFrame()).drop_duplicates().\
                sort_values(by='depth').reset_index(drop=True)
            return self.constituents_df

    def populate_values(self, dataset, value_column, underlier_column):
        ds = Dataset(dataset)
        query = ds.get_data(start=self.date, end=self.date, assetId=[self.id])
        if len(query) > 0:
            for node in self.direct_underlier_assets_as_nodes:
                value = query.loc[query[underlier_column] == node.id][value_column].iloc[0]
                node.data[value_column] = value
                node.populate_values(dataset, value_column, underlier_column)

    def build_tree(self, dataset, underlier_column):
        """
        Build the full tree and return the root node
        """
        query = self.__get_direct_underliers(self.id, dataset)
        if len(query) > 0:
            all_ids = query[underlier_column].tolist()
            all_assets = GsAssetApi.get_many_assets(id=all_ids)
            asset_lookup = {mq_id: asset_obj for mq_id, asset_obj in zip(all_ids, all_assets)}
            for i_, row in query.iterrows():
                child_node = AssetTreeNode(row[underlier_column], self.depth + 1, self.date,
                                           asset_lookup[row[underlier_column]])
                child_node.build_tree(dataset, underlier_column)
                self.direct_underlier_assets_as_nodes.append(child_node)

    def __get_direct_underliers(self, asset_id, dataset) -> pd.DataFrame:
        """
        Queries the dataset for the date passed during initialisation. If date isn't passed, returns the data of the
        latest available date.
        """
        ds = Dataset(dataset)
        if self.date:
            query = ds.get_data(start=self.date, end=self.date, assetId=[asset_id]).drop_duplicates()
        else:
            query = ds.get_data(assetId=[asset_id]).drop_duplicates()

        if len(query) > 0:
            self.date = query.index.max().date()
            query = query[query.index == query.index.max()].reset_index()
        return query

    def __build_constituents_df(self, constituents_df) -> pd.DataFrame:

        for node in self.direct_underlier_assets_as_nodes:
            data = {'date': self.date, 'assetName': self.name, 'assetId': self.id, 'assetBbid': self.bbid,
                    'underlyingAssetName': node.name, 'underlyingAssetId': node.id, 'underlyingAssetBbid': node.bbid,
                    'depth': node.depth}

            for key, value in node.data.items():
                data[key] = value
            constituents_df = constituents_df.append(pd.DataFrame(data, index=[0]))
            d = node.__build_constituents_df(constituents_df)
            if len(d) > 0:
                constituents_df = constituents_df.append(d)
        return constituents_df


class TreeHelper:

    def __init__(self,
                 id,
                 date: Optional[dt.date] = None,
                 tree_underlier_dataset: Optional[str] = None,
                 underlier_column: Optional[str] = 'underlyingAssetId'):

        self.id = id
        self.root = AssetTreeNode(self.id, 0, date, GsAssetApi.get_asset(asset_id=self.id))
        self.date = self.root.date
        self.update_time = dt.datetime.now()
        self.constituents_df = pd.DataFrame()
        self.tree_built = False
        self.__tree_underlier_dataset = tree_underlier_dataset
        self.__underlier_column = underlier_column

    def populate_weights(self,
                         dataset,
                         weight_column: Optional[str] = 'weight'):

        if not self.tree_built:
            self.build_tree()

        self.root.data['weight'] = 1
        self.root.populate_values(dataset, weight_column, self.__underlier_column)

    def populate_attribution(self,
                             dataset,
                             attribution_column: Optional[str] = 'absoluteAttribution'):

        if not self.tree_built:
            self.build_tree()

        self.root.data['absoluteAttribution'] = 1
        self.root.populate_values(dataset, attribution_column, self.__underlier_column)

    def to_frame(self) -> pd.DataFrame:
        """
        Retrieve constituents of the full tree. If it has already been fetched once, it is stored and returned when
        called later in the future.

        :return: dataframe with constituents of the full tree, with parent AssetID, underlying AssetID, depth and weight

        **Usage**

        Retrieve constituents of the full tree.
        """

        if not self.tree_built:
            self.build_tree()

        self.constituents_df = self.root.to_frame()
        if len(self.constituents_df) > 0:
            return self.constituents_df
        else:
            raise MqValueError('No constituents found for the asset')

    def build_tree(self):
        if not self.tree_built:
            self.root.build_tree(self.__tree_underlier_dataset, self.__underlier_column)
            self.tree_built = True
            self.update_time = dt.datetime.now()

    def get_tree(self) -> AssetTreeNode:
        """
        Build the full tree and return the root node of the full-fledged tree.
        If the tree has been built already, return it on future calls.

        :return: AssetTreeNode object of the root node, with a list attribute direct_underlier_assets_as_nodes that
        holds the child AssetTreeNode object.

        **Usage**

        Root AssetTreeNode object of the tree entity
        """

        if not self.tree_built:
            self.build_tree()

        return self.root

    def get_visualisation(self, visualise_by: Optional[str] = 'asset_name'):
        try:
            from treelib import Tree
        except ModuleNotFoundError:
            raise RuntimeError('You must install treelib to be able use this function.')

        if not self.tree_built:
            self.build_tree()

        if visualise_by in ['asset_name', 'bbid']:
            parent_field = 'assetName' if visualise_by == 'asset_name' else 'assetBbid'
            child_field = 'underlyingAssetName' if visualise_by == 'asset_name' else 'underlyingAssetBbid'

            df = self.to_frame()
            tree_vis = Tree()
            tree_vis.create_node(f'0 - {df[parent_field][0]}', df[parent_field][0])
            for depth, parent, child in zip(df['depth'], df[parent_field], df[child_field]):
                tree_vis.create_node(f'{depth} - {child}', child, parent=parent)

        else:
            raise MqValueError('visualise_by argument has to be either asset_name or bbid')

        return tree_vis.show()
