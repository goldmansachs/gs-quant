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
from typing import Optional, Dict

from pydash import get

from gs_quant.api.gs.assets import GsAssetApi, GsAsset, AssetParameters
from gs_quant.common import DateLimit
from gs_quant.entities.entity import EntityType, PositionedEntity
from gs_quant.errors import MqUninitialisedError, MqValueError
from gs_quant.json_encoder import JSONEncoder
from gs_quant.markets.indices_utils import BasketTypes, CorporateActionType, IndicesDatasets, \
    FundamentalsMetrics, FundamentalMetricPeriod, FundamentalMetricPeriodDirection
from gs_quant.markets.securities import Asset, AssetType as SecAssetType
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.indices import GsIndexApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.target.data import DataQuery, DataQueryResponse
from gs_quant.target.reports import Report


class Basket(Asset, PositionedEntity):
    """
    Basket which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets
    """
    def __init__(self, identifier: str = None, gs_asset: GsAsset = None):
        if identifier:
            gs_asset = self.__get_gs_asset(identifier)

        if gs_asset:
            if gs_asset.type.value not in BasketTypes.to_list():
                raise MqValueError(f'Failed to initialize. Asset {gs_asset.id} of type {gs_asset.type.value} \
                    is not a basket')
            self.__id = gs_asset.id
            asset_entity: Dict = json.loads(json.dumps(gs_asset.as_dict(), cls=JSONEncoder))
            asset_parameters = get(asset_entity, 'parameters', {})
            Asset.__init__(self, gs_asset.id, gs_asset.asset_class, gs_asset.name, exchange=gs_asset.exchange,
                           currency=gs_asset.currency, parameters=AssetParameters(**asset_parameters),
                           entity=asset_entity, entitlements=gs_asset.entitlements)
            PositionedEntity.__init__(self, gs_asset.id, EntityType.ASSET)
            self.__populate_current_attributes_for_existing_basket(gs_asset)

        else:
            self.__raise_initialization_error('use currently implemented class functionality')

    def get_last_rebalance_data(self) -> Dict:
        if not self.id:
            self.__raise_initialization_error('retrieve latest rebalance data')

        return GsIndexApi.last_rebalance_data(self.id)

    def get_last_rebalance_date(self) -> dt.date:
        if not self.id:
            self.__raise_initialization_error('retrieve latest rebalance date')

        last_rebalance = GsIndexApi.last_rebalance_data(self.id)
        return dt.datetime.strptime(last_rebalance['date'], '%Y-%m-%d').date()

    def get_corporate_actions(self,
                              ca_type: [CorporateActionType] = CorporateActionType.to_list(),
                              start_date: dt.date = DateLimit.LOW_LIMIT.value,
                              end_date: dt.date = DateLimit.HIGH_LIMIT.value) -> DataQueryResponse:
        if not self.id:
            self.__raise_initialization_error('retrieve corporate actions data')

        where = dict(assetId=self.id, corporateActionType=ca_type)
        query = DataQuery(where=where, start_date=start_date, end_date=end_date)
        return GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.CORPORATE_ACTIONS.value)

    def get_fundamentals(self,
                         period: FundamentalMetricPeriod = FundamentalMetricPeriod.ONE_YEAR.value,
                         direction: FundamentalMetricPeriodDirection = FundamentalMetricPeriodDirection.FORWARD.value,
                         metrics: [FundamentalsMetrics] = FundamentalsMetrics.to_list(),
                         start_date: dt.date = DateLimit.LOW_LIMIT.value,
                         end_date: dt.date = DateLimit.TODAY.value) -> DataQueryResponse:
        if not self.id:
            self.__raise_initialization_error('retrieve fundamentals data')

        where = dict(assetId=self.id, period=period, periodDirection=direction, metric=metrics)
        query = DataQuery(where=where, start_date=start_date, end_date=end_date)
        return GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.BASKET_FUNDAMENTALS.value)

    def get_live_date(self) -> Optional[dt.date]:
        if not self.id:
            self.__raise_initialization_error('retrieve live date')

        return self.live_date

    def get_type(self) -> SecAssetType:
        if not self.id or not self.__gs_asset_type:
            self.__raise_initialization_error('retrieve asset type')

        return SecAssetType[self.__gs_asset_type.name.upper()]

    @property
    def clone_parent_id(self) -> Optional[str]:
        return self.__clone_parent_id

    @property
    def default_backcast(self) -> Optional[bool]:
        return self.__default_backcast

    @property
    def description(self) -> Optional[str]:
        return self.__description

    @property
    def divisor(self) -> Optional[float]:
        return self.__divisor

    @property
    def flagship(self) -> Optional[bool]:
        return self.__flagship

    @property
    def hedge_id(self) -> Optional[str]:
        return self.__hedge_id

    @property
    def include_price_history(self) -> Optional[bool]:
        return self.__include_price_history

    @property
    def initial_price(self) -> Optional[float]:
        return self.__initial_price

    @property
    def publish_to_bloomberg(self) -> Optional[bool]:
        return self.__publish_to_bloomberg

    @property
    def publish_to_factset(self) -> Optional[bool]:
        return self.__publish_to_factset

    @property
    def publish_to_reuters(self) -> Optional[bool]:
        return self.__publish_to_reuters

    @property
    def return_type(self) -> Optional[str]:
        return self.__return_type

    @property
    def ticker(self) -> Optional[str]:
        return self.__ticker

    def __raise_initialization_error(self, action_msg: str):
        raise MqUninitialisedError(f'Basket must be initialized with some identifier to {action_msg}')

    def __get_gs_asset(self, identifier: str) -> GsAsset:
        response = GsAssetApi.resolve_assets(identifier=[identifier], limit=1)[identifier]
        gs_asset = None if len(response) == 0 else GsAsset.from_dict(response[0])
        if gs_asset is None:
            raise MqValueError(f'Basket could not be found using identifier {identifier}')
        return gs_asset

    def __get_last_create_report(self) -> Report:
        return GsReportApi.get_reports(limit=1, position_source_id=self.id, report_type='Basket Create',
                                       order_by='>latestExecutionTime')

    def __populate_current_attributes_for_existing_basket(self, gs_asset: GsAsset):
        self.__description = get(gs_asset, 'description', None)
        self.__gs_asset_type = get(gs_asset, 'type', None)
        self.__live_date = get(gs_asset, 'live_date', None)
        self.__ticker = get(gs_asset, 'xref.ticker', None)

        self.__clone_parent_id = get(gs_asset, 'parameters.clone_parent_id', None)
        self.__default_backcast = get(gs_asset, 'parameters.default_backcast', None)
        self.__flagship = get(gs_asset, 'parameters.flagship', None)
        self.__hedge_id = get(gs_asset, 'parameters.hedge_id', None)
        self.__return_type = get(gs_asset, 'parameters.index_calculation_type', None)

        last_positions = GsAssetApi.get_latest_positions(self.__id)
        self.__divisor = get(last_positions, 'divisor', None)
        last_initial_price = GsIndexApi.initial_price(gs_asset.id, DateLimit.TODAY.value)
        self.__initial_price = get(last_initial_price, 'price', None)

        report = self.__get_last_create_report()
        self.__include_price_history = get(report, 'parameters.include_price_history', None)
        self.__publish_to_bloomberg = get(report, 'parameters.publish_to_bloomberg', None)
        self.__publish_to_factset = get(report, 'parameters.publish_to_factset', None)
        self.__publish_to_reuters = get(report, 'parameters.publish_to_reuters', None)
