"""
Copyright 2026 Goldman Sachs.
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
from typing import Annotated, Optional

from gs_quant.data import Dataset
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier
from gs_quant.mcp.dependencies import depends_user_session
from gs_quant.mcp.tools import mcp_tool
from gs_quant.session import GsSession


@mcp_tool(tags={"data"})
def get_daily_data(
    dataset_name: Annotated[str, "The name of the dataset to retrieve data for"],
    bbid: Annotated[str, "The BBID (BloombergID) of the asset to retrieve data for"],
    start_date: Annotated[dt.date, "The start date for the data retrieval in YYYY-MM-DD ISO format"],
    end_date: Annotated[dt.date, "The end date for the data retrieval in YYYY-MM-DD ISO format"],
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Returns data from a dataset for a specific asset and date range.
    """
    ds = Dataset(dataset_name)
    with user_session:
        df = ds.get_data(start_date, end_date, bbid=bbid)
    return json.loads(df.to_json(orient='table'))


@mcp_tool(tags={"data"})
def get_intraday_data(
    dataset_name: Annotated[str, "The name of the dataset to retrieve data for"],
    bbid: Annotated[str, "The BBID (BloombergID) of the asset to retrieve data for"],
    start_datetime: Annotated[dt.datetime, "The start date for the data retrieval in ISO format"],
    end_datetime: Annotated[dt.datetime, "The end datetime for the data retrieval in ISO format"],
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Returns data from a dataset for a specific asset and date time range. Useful for datasets that have intraday data
    """
    ds = Dataset(dataset_name)
    with user_session:
        df = ds.get_data(start_datetime, end_datetime, bbid=bbid)
    return json.loads(df.to_json(orient='table'))


@mcp_tool(tags={"data"})
def get_last_data(
    dataset_name: Annotated[str, "The name of the dataset to retrieve data for"],
    bbid: Annotated[Optional[str], "The BBID (BloombergID) of the asset to retrieve data for"] = None,
    asset_id: Annotated[
        Optional[str], "The Marquee Asset ID (MAXXXXXXXXXXXX) of the asset to retrieve data for"
    ] = None,
    as_of: Annotated[Optional[dt.date], "The as of date for the data retrieval in YYYY-MM-DD format"] = None,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Returns data from a dataset for a specific asset and date. If bbid is not provided, it will return the last data for all assets in the dataset for the given date
    """
    ds = Dataset(dataset_name)
    if as_of is None:
        as_of = dt.date.today()
    with user_session:
        df = ds.get_data_last(bbid=bbid, asset_id=asset_id, as_of=as_of)
    return json.loads(df.to_json(orient='table'))


@mcp_tool(tags={"data"})
def get_dataset_coverage(
    dataset_name: Annotated[str, "The name of the dataset to retrieve data for"],
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Returns information about the assets covered in the dataset, which might include the BBID, name and other metadata
    """
    ds = Dataset(dataset_name)
    with user_session:
        coverage = ds.get_coverage()
    return json.loads(coverage.to_json(orient='table'))


@mcp_tool(tags={"secmaster"})
def find_asset_identifiers(
    asset_name: Annotated[str, "The asset name to search for"],
    is_bloomberg_id: Annotated[bool, "If you know it's a bbid/bloomberg id"] = False,
    is_isin: Annotated[bool, "If you know it's an ISIN"] = False,
    is_marquee_id: Annotated[bool, "If you know it's a marquee id, of the format MAXXXXXXXXXXX"] = False,
    is_ric: Annotated[bool, "If you know it's a Reuters ID (called a RIC)"] = False,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    Uses Security Master to get a list of identifiers for a given asset name.
    It will also return a basic name and description of the asset.
    Useful if you have a ric and need a bloombery ID, or need the marquee ID
    If you know the identifier is a Bloomberg ID, set is_bloomberg_id to True to search only in Bloomberg IDs.
    If none of the is_bloomberg_id, is_isin, is_marquee_id or is_ric flags are set to True, it will search in the ticker field by default.
    """
    id_type_mapping = {
        is_bloomberg_id: AssetIdentifier.BLOOMBERG_ID,
        is_isin: AssetIdentifier.ISIN,
        is_marquee_id: AssetIdentifier.MARQUEE_ID,
        is_ric: AssetIdentifier.REUTERS_ID,
    }

    id_type = next(
        (value for condition, value in id_type_mapping.items() if condition and value), AssetIdentifier.TICKER
    )

    with user_session:
        asset = SecurityMaster.get_asset(asset_name, id_type)
        if asset is None:
            return {"error": "Asset not found"}
        mq_id = asset.get_marquee_id()
        other_ids = asset.get_identifiers()

    return {
        "name": asset.name,
        "type": asset.get_type(),
        "currency": asset.get_currency() if hasattr(asset, "get_currency") else None,
        "description": asset.description if hasattr(asset, "description") else None,
        "identifiers": {"marquee_id": mq_id, **other_ids},
    }


@mcp_tool(tags={"data"})
def get_underliers(
    asset_id: Annotated[str, "The Marquee asset ID to use to find the underlier, of the format MAXXXXXXXXXXX"],
    as_of: Annotated[
        Optional[dt.date],
        "The as of date to use to find the underlier, in YYYY-MM-DD format. If not provided, it will use the last available position date",
    ] = None,
    user_session: GsSession = depends_user_session,
) -> dict:
    """
    If you have an "Index" or a "Research Basket" you can find information about the underlying constituents.
    It will base it on the last available position date unless you explicitly specify an as of date.
    """
    fields = [
        "type",
        "underlyingAssetId",
        "positionDate",
        "assetClass",
        "currency",
        "expirationDate",
        "closePrice",
        "quantity",
        "fxSpot",
        "name",
        "marketValue",
        "bbid",
        "assetClassificationsCountryCode",
        "assetClassificationsGicsSector",
        "assetClassificationsGicsIndustry",
    ]
    fields_str = "&".join(f"fields={f}" for f in fields)
    with user_session:
        try:
            if as_of is None:
                url = f"/indices/{asset_id}/positions/last/data?{fields_str}"
            else:
                url = f"/indices/{asset_id}/positions/data?startDate={as_of}&endDate={as_of}&{fields_str}"
            response = user_session.sync.get(url)
        except Exception as e:
            return {"error": str(e)}
    if "results" not in response:
        return {"error": "Unexpected response format, no results"}
    results_url = f"https://marquee.gs.com/s/products/{asset_id}/constituents"
    if response["results"]:
        close_positions = [r for r in response["results"] if r.get("positionType") == "close"] or response["results"]
        num_results = len(close_positions)
        if num_results > 20:
            top_n = sorted(close_positions, key=lambda x: x.get("marketValue", 0), reverse=True)
            return {
                "count": num_results,
                "limitedTo": "First 20 results (by Market Value), please refer to the full list of underliers in Marquee in fullResultsUrl",
                "fullResultsURL": results_url,
                "underliers": top_n[:20],
            }
        else:
            return {"count": num_results, "fullResultsURL": results_url, "underliers": close_positions}
