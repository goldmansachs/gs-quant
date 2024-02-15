"""
Copyright 2023 Goldman Sachs.
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
import math
from enum import Enum
from functools import partial
from itertools import groupby
from typing import Union, Iterable, Dict

import tqdm

from gs_quant.json_encoder import JSONEncoder
from gs_quant.session import GsSession
from gs_quant.target.secmaster import SecMasterAssetType

DEFAULT_SCROLL_PAGE_SIZE = 500


class SecMasterIdentifiers(Enum):
    CUSIP = 'cusip'
    TICKER = 'ticker'
    ISIN = 'isin'
    GSID = 'gsid'
    BBG = 'bbg'
    BBID = 'bbid'
    BCID = 'bcid'
    RIC = 'ric'
    RCIC = 'rcic'
    ID = 'id'
    ASSET_ID = 'assetId'
    CUSIP8 = 'cusip8'
    SEDOL = 'sedol'
    PRIMEID = 'primeId'
    FACTSET_REGIONAL_ID = 'factSetRegionalId'
    TOKEN_ID = 'tokenId'
    COMPOSITE_FIGI = 'compositeFigi'


def __extend_enum(base_enum, new_values):
    members = {item.name: item.value for item in base_enum}
    members.update(new_values)
    return Enum('CapitalStructureIdentifiers', members)


# FIXME Create an enum in service def for this and reference once module_generator get fixed.
CapitalStructureIdentifiers = __extend_enum(SecMasterIdentifiers, {"ISSUER_ID": "issuerId"})


class ExchangeId(Enum):
    RIC_SUFFIX_CODE = "ricSuffixCode"
    RIC_EXCHANGE_CODE = "ricExchangeCode"
    DATASCOPE_IPC_CODE = "datascopeIpcCode"
    BBG_EXCHANGE_CODE = "bbgExchangeCode"
    TAQ_EXCHANGE_CODE = "taqExchangeCode"
    IVERSON_EXCHANGE_CODE = "iversonExchangeCode"
    INDEX_CHANGE_EXCHANGE_CODE = "indexChangeExchangeCode"
    DOW_JONES_EXCHANGE_CODE = "dowJonesExchangeCode"
    STOXX_EXCHANGE_CODE = "stoxxExchangeCode"
    ML_ETF_EXCHANGE_CODE = "mlEtfExchangeCode"
    FTSE_EXCHANGE_CODE = "ftseExchangeCode"
    DJGI_EXCHANGE_CODE = "djgiExchangeCode"
    SECDB_EXCHANGE_CODE = "secdbExchangeCode"
    DADD_EXCHANGE_CODE = "daddExchangeCode"
    MIC = "mic"
    OPERATING_MIC = "operatingMic"
    GS_EXCHANGE_ID = "gsExchangeId"
    COUNTRY = "country"
    EXCHANGE_NAME = "name"


class GsSecurityMasterApi:

    @classmethod
    def get_security(cls, id_value: str,
                     id_type: SecMasterIdentifiers,
                     effective_date: dt.date = None):
        """
        Get flatten asset reference data

        @param id_value: identifier value
        @param id_type: identifier type
        @param effective_date: As of date for query
        @return: dict or None
        """
        args = {id_type.value: id_value}
        results = cls.get_many_securities(effective_date=effective_date, flatten=False, **args)
        if results is not None:
            return results["results"][0]
        return results

    @classmethod
    def get_many_securities(cls, type_: SecMasterAssetType = None,
                            effective_date: dt.date = None,
                            limit: int = 10, flatten=False,
                            is_primary=None,
                            offset_key: str = None,
                            **query_params: Dict[SecMasterIdentifiers, Union[str, Iterable[str]]]) \
            -> Union[Iterable[dict], None]:
        """
        Get reference data for a single page of a given asset type. Use returned offsetKey to fetch next page.

        @param is_primary:
        @param flatten: flag if data should be flattened
        @param type_: asset type
        @param effective_date: As of date for query
        @param limit: integer of individual page
        @param offset_key: string, an offset indicating where the page ends.
        @return: list of dict
        """

        if (query_params is None or len(query_params) == 0) and type_ is None:
            raise ValueError("Neither '_type' nor 'query_params' are provided")

        params = {
            "limit": limit
        }

        cls.prepare_params(params, is_primary, offset_key, type_, effective_date)

        params = {**params, **query_params}
        payload = json.loads(json.dumps(params, cls=JSONEncoder))

        if flatten:
            r = GsSession.current._get('/markets/securities/data', payload=payload)
        else:
            r = GsSession.current._get('/markets/securities', payload=payload)
        if r['totalResults'] == 0:
            return None
        return r

    @classmethod
    def get_all_securities(cls, type_: SecMasterAssetType,
                           effective_date: dt.date = None,
                           is_primary=None,
                           flatten=False, **query_params) -> \
            Union[Iterable[dict], None]:
        """
        Get all securities reference data matching the type, with respect of effective_date property.
        Function runs in batches fetching all securities.

        @param flatten: Flag, whether data should be flattened
        @param is_primary: Restrict to primary listings
        @param type_: asset type
        @param effective_date: As of date for query
        @return:" list of dict
        """
        if 'limit' in query_params:
            limit = query_params['limit']
            del query_params['limit']
        else:
            limit = DEFAULT_SCROLL_PAGE_SIZE

        response = cls.get_many_securities(type_, effective_date, limit=limit, offset_key=None,
                                           flatten=flatten, is_primary=is_primary,
                                           **query_params)
        if response is None or "offsetKey" not in response:
            return response

        if response['totalResults'] == 0:
            return None

        results = response["results"]
        offset_key = response["offsetKey"]

        fn = partial(cls.get_many_securities, type_=type_, effective_date=effective_date,
                     limit=limit, flatten=flatten,
                     **query_params)
        results.extend(cls.__fetch_all(fn, offset_key))
        response["totalResults"] = len(results)
        response["results"] = results

        return response

    @classmethod
    def get_security_data(cls, id_value: str,
                          id_type: SecMasterIdentifiers,
                          effective_date: dt.date = None) -> Union[dict, None]:
        """
        Get flatten asset reference data

        @param id_value: identifier value
        @param id_type: identifier type
        @param effective_date: As of date for query
        @return: dict or None
        """
        args = {id_type.value: id_value}
        results = cls.get_many_securities(effective_date=effective_date, flatten=True, **args)
        if results is not None:
            return results["results"][0]
        return results

    @classmethod
    def get_identifiers(cls, secmaster_id: str) -> dict:
        """
        Get identifiers history for given secmaster id.

        @param secmaster_id:  secmaster id  e.g. ['GSPD111E123']
        @return: list of dict with date ranges of the identifiers.
        """
        if not secmaster_id.startswith("GS"):
            raise ValueError(f"Invalid id_value {secmaster_id}. Secmaster id starts with 'GS'")
        r = GsSession.current._get(f'/markets/securities/{secmaster_id}/identifiers')
        return r['results']

    @classmethod
    def map(cls, input_type: SecMasterIdentifiers,
            ids: Iterable[str],
            output_types: Iterable[SecMasterIdentifiers] = frozenset([SecMasterIdentifiers.GSID]),
            start_date: dt.date = None,
            end_date: dt.date = None,
            effective_date: dt.date = None) -> Iterable[dict]:
        """
        Map to other identifier types, from given IDs.

        :param input_type: type of input IDs
        :param ids: security IDs
        :param output_types: types of IDs to map to
        :param start_date: first as-of date (defaults to current date)
        :param end_date: last as-of date (defaults to current date)
        :param effective_date: an exact as-of date for mapping
        :return: dict containing mappings for as-of date(s)
        """
        params = {
            input_type.value: list(ids),
            'toIdentifiers': [identifier.value for identifier in output_types],
            'compact': True
        }
        if effective_date is not None:
            if (start_date or end_date) is not None:
                raise ValueError('provide (start date / end date) or as-of date, but not both')
            params['startDate'] = effective_date
            params['endDate'] = effective_date

        if start_date is not None:
            params['startDate'] = start_date
        if end_date is not None:
            params['endDate'] = end_date
        payload = json.loads(json.dumps(params, cls=JSONEncoder))

        r = GsSession.current._get('/markets/securities/map', payload)
        results = r['results']
        return results

    @classmethod
    def search(cls, q: str, limit: int = 10, type_: SecMasterAssetType = None, is_primary: bool = None,
               active_listing: bool = None) -> Union[Iterable[dict], None]:
        """
        Search securities by a query string. It does a full text search among names, identifiers, company
        @param q: query string
        @param limit: number of returned matches
        @param type_: filter restricting the type of results
        @param is_primary: filter restricting the matches to primary listings
        @param active_listing: filter restricting the matches to active listings
        @return:
        """
        params = {
            "q": q,
            "limit": limit
        }
        if type_ is not None:
            params["type"] = type_.value
        if is_primary is not None:
            params["isPrimary"] = is_primary
        if active_listing is not None:
            params["activeListing"] = active_listing
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        r = GsSession.current._get('/v2/markets/securities/search', payload=payload, include_version=False)
        if r['totalResults'] == 0:
            return None
        return r["results"]

    @classmethod
    def __stringify_boolean(cls, bool_value):
        return str(bool_value).lower()

    @classmethod
    def __fetch_all(cls, fetch_fn, offset_key, total_batches=None):
        accumulator = []
        offset = offset_key
        progress_info = tqdm.tqdm(desc="Processing", unit=" batch") if total_batches is None else tqdm.tqdm(
            range(total_batches), desc="Processing", unit=" batch", ascii=True)
        while True:
            progress_info.update(1)
            data = fetch_fn(offset_key=offset)
            if data is not None:
                accumulator.extend(data['results'])
                if 'offsetKey' not in data:
                    progress_info.close()
                    break
                offset = data["offsetKey"]
        return accumulator

    @classmethod
    def _get_corporate_actions(cls, id_value: str, id_type: SecMasterIdentifiers,
                               effective_date: dt.date, offset_key):

        params = {
            id_type.value: id_value,
        }
        if effective_date is not None:
            params['effectiveDate'] = effective_date

        if offset_key is not None:
            params["offsetKey"] = offset_key
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        r = GsSession.current._get("/markets/corpactions", payload=payload)
        return r

    @classmethod
    def get_corporate_actions(cls, id_value: str, id_type: SecMasterIdentifiers = SecMasterIdentifiers.GSID,
                              effective_date: dt.date = None) -> Iterable[dict]:
        """
        Get corporate actions from a given security.
        @param effective_date: parameter to query securities at a given date
        @param id_value: identifier value
        @param id_type: identifier type
        @return:
        """
        supported_identifiers = [SecMasterIdentifiers.GSID, SecMasterIdentifiers.ID]
        if id_type not in supported_identifiers:
            raise ValueError(
                f"Unsupported identifier {id_type} for this endpoint. Use one of this {supported_identifiers}")

        fn = partial(cls._get_corporate_actions, id_value, id_type, effective_date)
        results = cls.__fetch_all(fn, None)
        return results

    @classmethod
    def get_capital_structure(cls, id_value: str,
                              id_type: CapitalStructureIdentifiers,
                              type_: SecMasterAssetType = None, is_primary: bool = None,
                              effective_date: dt.date = None) -> dict:
        """
        Get a capital structure of the given company by id_value of the security.
         It runs in batches till all data is  fetched
        @param is_primary: filter to select primary listings only
        @param type_:  filter to restrict data to a given type
        @param effective_date: parameter to query securities at a given date
        @param id_value: identifier value
        @param id_type: identifier type
        @return: dict
        """
        response = cls._get_capital_structure(id_value=id_value, id_type=id_type, type_=type_, is_primary=is_primary,
                                              effective_date=effective_date, offset_key=None)
        if "offsetKey" not in response:
            return response

        asset_types_total = response["assetTypesTotal"]
        batch_count = math.floor(sum(asset_types_total.values()) / 100)
        results = response["results"]
        offset_key = response["offsetKey"]
        fn = partial(cls._get_capital_structure, id_value, id_type, type_, is_primary, effective_date)

        results.extend(cls.__fetch_all(fn, offset_key, total_batches=batch_count))
        aggregated_results, total_results = cls.__capital_structure_aggregate(asset_types_total, results)
        response["results"] = aggregated_results
        response["totalResults"] = total_results
        del response["offsetKey"]

        return response

    @classmethod
    def __capital_structure_aggregate(cls, asset_types_total, results):
        group_by_issuer_id = {k: list(g) for k, g in groupby(results, lambda x: x["issuerId"])}
        aggregated_results = []
        aggregated_total_results = 0
        for issuer_id in group_by_issuer_id:
            issuer_id_data = group_by_issuer_id[issuer_id]
            issuer_id_data_instance = issuer_id_data[0]
            consolidated_types_obj = {key: [] for key in asset_types_total}
            for obj in group_by_issuer_id[issuer_id]:
                aggregated_total_results += sum(len(e) for e in obj["types"].values())
                [consolidated_types_obj.get(asset_type).extend(obj["types"].get(asset_type))
                 for asset_type in obj["types"]]
                issuer_id_data_instance["types"] = consolidated_types_obj
            aggregated_results.append(issuer_id_data_instance)
        return aggregated_results, aggregated_total_results

    @classmethod
    def _get_capital_structure(cls, id_value: str, id_type: Union[CapitalStructureIdentifiers, SecMasterIdentifiers],
                               type_, is_primary, effective_date, offset_key: Union[str, None]):
        params = {
            id_type.value: id_value
        }
        cls.prepare_params(params, is_primary, offset_key, type_, effective_date)
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        r = GsSession.current._get("/markets/capitalstructure", payload=payload)
        return r

    @classmethod
    def prepare_params(cls, params, is_primary, offset_key, type_, effective_date=None):
        if type_ is not None:
            params["type"] = type_.value
        if is_primary is not None:
            params["isPrimary"] = is_primary
        if offset_key is not None:
            params["offsetKey"] = offset_key
        if effective_date is not None:
            params["effectiveDate"] = effective_date

    @classmethod
    def get_deltas(cls, start_time: dt.datetime = None, end_time: dt.datetime = None, raw: bool = None) -> \
            Iterable[dict]:
        """
        Get all identifier changes betwen two time stamps
        @param start_time: start time
        @param end_time: end time
        @param raw: flag, if true (default) aggregates data to more readable form, if false shows unprocessed results.
        @return: list of dict
        """
        params = {}

        if raw is not None:
            params["raw"] = GsSecurityMasterApi.__stringify_boolean(raw)
        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        r = GsSession.current._get("/markets/securities/identifiers/updates-feed", payload=payload)
        return r

    @classmethod
    def get_exchanges(cls, effective_date: dt.date = None,
                      **query_params: Dict[str, Union[str, Iterable[str]]]):
        """
        Returns reference data for exchanges - e.g. MICs, exchange codes, name, listing country.

        @param effective_date: As of date for query
        @param query_params: one of allowed params:
         'ricSuffixCode', 'ricExchangeCode', 'datascopeIpcCode', 'bbgExchangeCode', 'taqExchangeCode',
        'iversonExchangeCode', 'indexChangeExchangeCode', 'dowJonesExchangeCode', 'stoxxExchangeCode',
        'mlEtfExchangeCode', 'ftseExchangeCode', 'djgiExchangeCode', 'secdbExchangeCode', 'daddExchangeCode', 'mic',
        'operatingMic', 'gsExchangeId', 'country', 'name'
        @return:
        """
        results = []
        fn = partial(cls._get_exchanges, effective_date, DEFAULT_SCROLL_PAGE_SIZE, query_params)
        results.extend(cls.__fetch_all(fn, offset_key=None))
        response = dict()
        response["totalResults"] = len(results)
        response["results"] = results

        return response

    @classmethod
    def _get_exchanges(cls, effective_date: dt.date = None, limit: int = 10,
                       query_params=None,
                       offset_key: Union[str, None] = None):

        if query_params is None:
            query_params = dict()
        allowed_keys = list(ExchangeId._value2member_map_.keys())
        for qp in query_params.keys():
            if qp not in allowed_keys:
                raise ValueError(f" Parameter '{qp}' is not supported. Allowed parameters:  {allowed_keys}")
        params = {
            "limit": limit
        }
        if effective_date is not None:
            params['effectiveDate'] = effective_date

        params = {**params, **query_params}
        if offset_key is not None:
            params["offsetKey"] = offset_key
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        r = GsSession.current._get('/markets/exchanges', payload=payload)
        if r['totalResults'] == 0:
            return None
        return r

    @classmethod
    def get_exchange_identifiers_history(cls, gs_exchange_id: str) -> Iterable[dict]:
        """
        Get identifiers history for given exchange id.

        @param gs_exchange_id:  exchange_id id
        @return: list of dict with date ranges of the identifiers.
        """
        r = GsSession.current._get(f'/markets/exchanges/{gs_exchange_id}/identifiers')
        return r['results']
