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
from typing import Union, Iterable, Dict, Optional

import tqdm

from gs_quant.data.utilities import SecmasterXrefFormatter
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
    CINS = 'cins'
    PRIMEID = 'primeId'
    FACTSET_REGIONAL_ID = 'factSetRegionalId'
    TOKEN_ID = 'tokenId'
    COMPOSITE_FIGI = 'compositeFigi'
    BARRA_ID = 'barraId'
    AXIOMA_ID = 'axiomaId'
    FIGI = 'figi'


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
            -> Optional[dict]:
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
    def get_all_securities(cls, type_: SecMasterAssetType = None,
                           effective_date: dt.date = None,
                           is_primary=None,
                           flatten=False, **query_params) -> Optional[dict]:
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
                          effective_date: dt.date = None) -> Optional[dict]:
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
    def get_many_identifiers(cls, ids: Iterable[str], limit=100, xref_format=False) -> dict:
        """
          Get identifiers for a list of secmaster ids. It runs in batches till all data is fetched.

          This method retrieves identifier information for multiple securities.
          The data can be returned in either standard format or transformed using the SecmasterXrefFormatter
          for time-based cross-reference analysis.

          Args:
              ids (Iterable[str]): An iterable collection of secmaster identifiers to query.
                                  Examples: ['GSPD111E123', 'GSPD222F456', 'GSPD333G789']

              limit (int, optional): Maximum number of identifier records to return per secmaster id.
                                    Defaults to 100. Used to control response size and prevent
                                    memory issues with large datasets.

              xref_format (bool, optional): Flag to control output format. Defaults to False.
                                          - False: Returns raw identifier data in standard format
                                          - True: Returns data transformed by SecmasterXrefFormatter,
                                                 where identifiers are grouped by overlapping date
                                                 ranges

          Returns:
              dict: A dictionary containing identifier information for the requested secmaster ids.

                    Standard format (xref_format=False):
                    {
                        'secmaster_id_1': [
                            {
                                'type': 'ISIN',
                                'value': 'US1234567890',
                                'startDate': '2020-01-01',
                                'endDate': '2023-12-31'
                            },
                            ...
                        ],
                        'secmaster_id_2': [...],
                        ...
                    }

                    Xref format (xref_format=True):
                    {
                        'secmaster_id_1': {
                            'xrefs': [
                                {
                                    'startDate': '2020-01-01',
                                    'endDate': '2023-12-31',
                                    'identifiers': [
                                        {'type': 'ISIN', 'value': 'US1234567890'},
                                        {'type': 'CUSIP', 'value': '123456789'},
                                        ...
                                    ]
                                },
                                ...
                            ]
                        },
                        'secmaster_id_2': {...},
                        ...
                    }

          Raises:
              ValueError: If ids parameter is empty or contains invalid secmaster identifiers
              ConnectionError: If unable to connect to secmaster database
              TimeoutError: If database query exceeds timeout limits

          Note:
              - The method processes requests in batches to handle large datasets efficiently
              - Infinity dates ('9999-99-99') are normalized to '9999-12-31' in xref format


          Example:
              >>> # Standard format
              >>> result = GsSecurityMasterApi.get_many_identifiers(['GSPD111E123'], limit=50, xref_format=False)
              >>> print(result['GSPD111E123'][0]['type'])  # 'ISIN'

              >>> # Xref format for time-based analysis
              >>> xref_result = GsSecurityMasterApi.get_many_identifiers(['GSPD111E123'], xref_format=True)
              >>> print(xref_result['GSPD111E123']['xrefs'][0]['startDate'])  # '2020-01-01'
          """
        if not isinstance(ids, Iterable):
            raise ValueError(f"secmaster_id must be an iterable, got {type(ids)}")
        if len(ids) == 0:
            raise ValueError("secmaster_id cannot be an empty iterable")
        ids = list(ids)

        for id_value in ids:
            if not id_value.startswith("GS"):
                raise ValueError(f"Invalid id_value {id_value}. Secmaster id starts with 'GS'")

        consolidated_results = {}
        current_offset_key = None

        while True:
            payload = {'id': ids}

            if current_offset_key is not None:
                payload['offsetKey'] = current_offset_key
            if limit is not None:
                payload['limit'] = limit

            payload = json.loads(json.dumps(payload, cls=JSONEncoder))
            response = GsSession.current._get('/markets/securities/identifiers', payload=payload)

            if 'results' in response:
                for entity_id, data in response['results'].items():
                    if entity_id not in consolidated_results:
                        consolidated_results[entity_id] = []
                    consolidated_results[entity_id].extend(data)

            current_offset_key = response.get('offsetKey')
            if current_offset_key is None:
                break

        if xref_format:
            return SecmasterXrefFormatter.convert(consolidated_results)
        return consolidated_results

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
                raise ValueError('provide (start date / end date) or effective_date, but not both')
            params['effectiveDate'] = effective_date

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
    def __fetch_all(cls, fetch_fn, offset_key, total_batches=None, extract_results=True):
        accumulator = []
        offset = offset_key
        progress_info = tqdm.tqdm(desc="Processing", unit=" batch") if total_batches is None else tqdm.tqdm(
            range(total_batches), desc="Processing", unit=" batch", ascii=True)
        while True:
            progress_info.update(1)
            data = fetch_fn(offset_key=offset)
            if data is not None:
                if extract_results is True:
                    accumulator.extend(data['results'])
                else:
                    accumulator.append(data)
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
    def get_capital_structure(cls, id_value: Union[str, list],
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
    def _get_capital_structure(cls, id_value: Union[str, list],
                               id_type: Union[CapitalStructureIdentifiers, SecMasterIdentifiers],
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
    def _get_deltas(cls, start_time: dt.datetime = None, end_time: dt.datetime = None, raw: bool = None,
                    scope: list = None, limit: int = None, offset_key: str = None) -> \
            Iterable[dict]:

        params = {}
        if raw is not None:
            params["raw"] = GsSecurityMasterApi.__stringify_boolean(raw)
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if scope is not None:
            params["scope"] = scope
        if limit is not None:
            params["limit"] = limit
        if offset_key is not None:
            params["offsetKey"] = offset_key

        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        r = GsSession.current._get("/markets/securities/identifiers/updates-feed", payload=payload)
        return r

    @classmethod
    def get_deltas(cls, start_time: dt.datetime = None, end_time: dt.datetime = None, raw: bool = None,
                   scope: list = None, limit: int = None, offset_key: str = None, scroll_all_pages: bool = True) -> \
            Union[dict, Iterable[dict]]:
        """
        Get all identifier changes between two time stamps
        @param scroll_all_pages:
        @param start_time: start time
        @param end_time: end time
        @param limit: page size of returned matches
        @param scope: narrow down the search to a specific set of events
        @param offset_key: offset key to fetch next page
        @param raw: flag, if true (default) aggregates data to more readable form, if false shows unprocessed results.
        @return: list of dict
        """
        if scroll_all_pages:
            fn = partial(cls._get_deltas, start_time, end_time, raw, scope, limit)
            results = cls.__fetch_all(fn, offset_key, extract_results=False)
            latest_update_time = max(result['lastUpdateTime'] for result in results)
            res = [item for result in results for item in result["results"]]
            request_id = results[0]["requestId"] if results else None
            return {"results": res, "lastUpdateTime": latest_update_time, "requestId": request_id}
        else:
            results = cls._get_deltas(start_time, end_time, raw, scope, limit, offset_key)
        return results

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

    @classmethod
    def _prepare_string_or_list_param(cls, value: Union[str, list], param_name: str):
        if isinstance(value, str):
            return [value]  # Wrap single string in a list
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            return value  # Use the list directly
        else:
            raise ValueError(f"{param_name} must be a string or a list of strings")

    @classmethod
    def _prepare_underlyers_params(cls, params, id_value, offset_key=None, type_=None, effective_date=None,
                                   country_code=None, currency=None, include_inactive=None):
        if id_value is not None:
            params["id"] = cls._prepare_string_or_list_param(id_value, "id_value")
        else:
            raise ValueError("id_value must be defined")

        if type_ is not None:
            if isinstance(type_, list):
                if all(isinstance(t, SecMasterAssetType) for t in type_):
                    params["type"] = [t.value for t in type_]
                else:
                    raise ValueError("All elements in the type_ list must be instances of SecMasterAssetType")
            elif isinstance(type_, SecMasterAssetType):
                params["type"] = type_.value
            else:
                raise ValueError("type_ must be either a SecMasterAssetType or a list of SecMasterAssetType")

        if country_code is not None:
            params["countryCode"] = cls._prepare_string_or_list_param(country_code, "country_code")
        if currency is not None:
            params["currency"] = cls._prepare_string_or_list_param(currency, "currency")
        if offset_key is not None:
            params["offsetKey"] = offset_key
        if effective_date is not None:
            params["effectiveDate"] = effective_date
        if include_inactive is not None:
            params["includeInactive"] = include_inactive

    @classmethod
    def _get_securities_by_underlyers(cls,
                                      id_value: Union[str, list],
                                      type_: Union[SecMasterAssetType, list] = None,
                                      effective_date: dt.date = None,
                                      limit: int = 100,
                                      country_code: Union[str, list] = None,
                                      currency: Union[str, list] = None,
                                      include_inactive: bool = False,
                                      offset_key: str = None) \
            -> Optional[dict]:
        params = {
            "limit": limit
        }

        cls._prepare_underlyers_params(
            params=params,
            id_value=id_value,
            offset_key=offset_key,
            type_=type_,
            effective_date=effective_date,
            country_code=country_code,
            currency=currency,
            include_inactive=include_inactive
        )

        payload = json.loads(json.dumps(params, cls=JSONEncoder))

        r = GsSession.current._get('/markets/securities/underlyers', payload=payload)
        if r['totalResults'] == 0:
            return None
        return r

    @classmethod
    def get_securities_by_underlyers(cls,
                                     id_value: Union[str, list],
                                     type_: Union[SecMasterAssetType, list] = None,
                                     effective_date: dt.date = None,
                                     limit: int = None,
                                     offset_key: str = None,
                                     country_code: Union[str, list] = None,
                                     currency: Union[str, list] = None,
                                     include_inactive: bool = False,
                                     scroll_all_pages: bool = False) \
            -> Optional[dict]:
        """
        Retrieve reference data for listed derivatives based on their underlyers.

        This method retrieves securities linked to specific underlyers, with optional filters for asset type, effective
        date, country code and currency. The results can be paginated, and the method supports fetching either
        a single page or all pages of results.

        Args:
            id_value (Union[str, list]): Identifier(s) of the underlyers. Can be a single string or a list of strings.
                                          Example: 'GSPD100E0' or ['GSPD100E0'].
            type_ (Union[SecMasterAssetType, list], optional): Asset type(s) to filter the results. Can be a single
                                                               `SecMasterAssetType` or a list of `SecMasterAssetType`.
                                                               Defaults to None.
            effective_date (dt.date, optional): Effective date for the query. Defaults to None.
            limit (int, optional): Maximum number of results to return per page. Defaults to None.
            offset_key (str, optional): String indicating where the page ends, used for pagination. Defaults to None.
            country_code (Union[str, list], optional): Country code(s) to filter the results. Can be a single string
                                                       or a list of strings. Defaults to None.
            currency (Union[str, list], optional): Currency code(s) to filter the results. Can be a single string
                                                   or a list of strings. Defaults to None.
            include_inactive (bool, optional): Whether to include inactive listed derivatives in the results.
                                               Defaults to False.
            scroll_all_pages (bool, optional): Whether to fetch all pages of results. If True, retrieves all pages.
                                               Defaults to False.

        Returns:
            Optional[dict]: A dictionary containing the results for the requested page(s), or None if no results are
                            found.
                            Example:
                            {
                                "totalResults": 10,
                                "offsetKey": "ABCD=",
                                "results": [...],
                                "asOfTime": "2025-01-11T11:22:33.740Z",
                                "requestId": "abc123"
                            }

        Raises:
            ValueError: If `id_value` is not provided or is invalid.
            ValueError: If `type_` is not a valid `SecMasterAssetType` or a list of valid `SecMasterAssetType`.
            ValueError: If `country_code` or `currency` is not a string or a list of strings.
            ValueError: If `effective_date` is not in the format 'YYYY-MM-DD' when provided as a string.
            TypeError: If `effective_date` is not of type `datetime.date` or `str`.

        Note:
            - This method fetches a single page of results by default. To fetch all pages, set `scroll_all_pages=True`.
            - The `effective_date` parameter is used to query securities as of a specific date.
            - The `offset_key` parameter is used for pagination to fetch subsequent pages of results.

        Example:
            >>> result = GsSecurityMasterApi.get_securities_by_underlyers(
            ...     id_value="GSPD100E0",
            ...     type_=SecMasterAssetType.Equity_Option,
            ...     effective_date="2023-10-01",
            ...     country_code="US",
            ...     currency="USD",
            ...     include_inactive=False,
            ...     scroll_all_pages=True
            ... )
            >>> print(result["results"])
        """

        supported_types = [SecMasterAssetType.Equity_Option, SecMasterAssetType.Future,
                           SecMasterAssetType.Future_Option]
        if type_ is not None:
            if isinstance(type_, SecMasterAssetType):
                if type_ not in supported_types:
                    raise ValueError(f"Unsupported type {type_}. Supported types are {supported_types}")
            elif isinstance(type_, list):
                for t in type_:
                    if t not in supported_types:
                        raise ValueError(f"Unsupported type {t}. Supported types are {supported_types}")

        if scroll_all_pages:
            if limit is None:
                limit = 500
            fn = partial(cls._get_securities_by_underlyers,
                         id_value=id_value,
                         type_=type_,
                         effective_date=effective_date,
                         limit=limit,
                         country_code=country_code,
                         currency=currency,
                         include_inactive=include_inactive)
            results = cls.__fetch_all(fn, offset_key, extract_results=False)
            as_of_time = max(result['asOfTime'] for result in results)
            res = [item for result in results for item in result["results"]]
            request_id = results[0]["requestId"] if results else None
            total_results = len(res)
            return {"totalResults": total_results, "results": res, "asOfTime": as_of_time, "requestId": request_id}

        else:
            return cls._get_securities_by_underlyers(
                id_value=id_value,
                type_=type_,
                effective_date=effective_date,
                limit=limit,
                offset_key=offset_key,
                country_code=country_code,
                currency=currency,
                include_inactive=include_inactive
            )
