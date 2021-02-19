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

from gs_quant.markets.securities import AssetIdentifier, SecurityMaster
from gs_quant.risk.scenarios import MarketDataVolShockScenario
from gs_quant.data import Dataset
from datetime import datetime, timedelta, date


def build_eq_vol_scenario_intraday(asset_name: str, source_dataset: str, ref_spot: float = None,
                                   asset_name_type: AssetIdentifier = AssetIdentifier.REUTERS_ID,
                                   start_time: datetime = datetime.now() - timedelta(hours=1),
                                   end_time: datetime = datetime.now()) -> MarketDataVolShockScenario:

    asset = SecurityMaster.get_asset(asset_name, asset_name_type)
    vol_dataset = Dataset(source_dataset)
    vol_data = vol_dataset.get_data(
        assetId=[asset.get_marquee_id()],
        strikeReference='forward',
        startTime=start_time,
        endTime=end_time
    )
    asset_ric = asset.get_identifier(AssetIdentifier.REUTERS_ID)
    return MarketDataVolShockScenario.from_dataframe(asset_ric, vol_data, ref_spot)


def build_eq_vol_scenario_eod(asset_name: str, source_dataset: str, ref_spot: float = None,
                              asset_name_type: AssetIdentifier = AssetIdentifier.REUTERS_ID,
                              vol_date: date = date.today()) -> MarketDataVolShockScenario:

    asset = SecurityMaster.get_asset(asset_name, asset_name_type)
    vol_dataset = Dataset(source_dataset)
    vol_data = vol_dataset.get_data(
        assetId=[asset.get_marquee_id()],
        strikeReference='forward',
        startDate=vol_date,
        endDate=vol_date
    )
    asset_ric = asset.get_identifier(AssetIdentifier.REUTERS_ID)
    return MarketDataVolShockScenario.from_dataframe(asset_ric, vol_data, ref_spot)
