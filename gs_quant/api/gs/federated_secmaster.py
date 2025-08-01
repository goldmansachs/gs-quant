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

from enum import Enum
from gs_quant.target.secmaster import SecMasterAssetType
from gs_quant.common import AssetType, AssetClass
from typing import Union, Iterable, Dict, Optional
from gs_quant.json_encoder import JSONEncoder
from gs_quant.session import GsSession
import json
import datetime as dt

SECURITIES_FEDERATED = '/markets/securities/federated'


class FederatedIdentifiers(Enum):
    IDENTIFIER = 'identifier'
    ID = 'id'
    ASSET_ID = 'assetId'
    GSID = 'gsid'
    TICKER = 'ticker'
    BBID = 'bbid'
    BCID = 'bcid'
    RIC = 'ric'
    RCIC = 'rcic'
    CUSIP = 'cusip'
    CINS = 'cins'
    SEDOL = 'sedol'
    ISIN = 'isin'
    PRIMEID = 'primeId'


class GsSecurityMasterFederatedApi:

    @classmethod
    def get_a_security(cls, id: str, effective_date: dt.date = None) -> Optional[dict]:
        """
        Get security or asset for given security id or asset id.
        @param id: secmaster id(e.g. 'GSPD111E123') or asset id(e.g. 'MANYS1FCCWWV45P7')
        @param effective_date: As of date for query
        @return: dict
        """

        if not id.startswith("GS") and not id.startswith("MA"):
            raise ValueError(f"Invalid id: {id}. Security id starts with 'GS' and Asset id starts with 'MA'")

        params = {
        }
        if effective_date is not None:
            params["effectiveDate"] = effective_date
        payload = json.loads(json.dumps(params, cls=JSONEncoder))

        return GsSession.current._get(f'{SECURITIES_FEDERATED}/{id}', payload=payload)

    @classmethod
    def get_security_identifiers(cls, id: str) -> Optional[dict]:
        """
        Get identifiers history for given security id or asset id.
        @param id: secmaster id(e.g. 'GSPD111E123') or asset id(e.g. 'MANYS1FCCWWV45P7')
        @return: dict
        """

        if not id.startswith("GS") and not id.startswith("MA"):
            raise ValueError(f"Invalid id: {id}. Security id starts with 'GS' and Asset id starts with 'MA'")

        return GsSession.current._get(f'{SECURITIES_FEDERATED}/{id}/identifiers')

    @classmethod
    def get_many_securities(cls,
                            type_: Union[SecMasterAssetType, AssetType] = None,
                            effective_date: dt.date = None,
                            limit: int = 50,
                            is_primary=None,
                            offset_key: str = None,
                            **query_params: Dict[FederatedIdentifiers, Union[str, Iterable[str]]]) -> Optional[dict]:
        """
        Get reference data for a single page. Use returned offsetKey to fetch next page.
        @param is_primary:
        @param type_: security or asset type
        @param effective_date: As of date for query
        @param limit: integer of individual page
        @param offset_key: string, an offset indicating where the page ends
        @return: dict
        """

        return cls.__query_securities(type_=type_,
                                      effective_date=effective_date,
                                      limit=limit,
                                      flatten=False,
                                      is_primary=is_primary,
                                      offset_key=offset_key,
                                      **query_params)

    @classmethod
    def get_securities_data(cls,
                            type_: Union[SecMasterAssetType, AssetType] = None,
                            effective_date: dt.date = None,
                            limit: int = 50,
                            is_primary=None,
                            offset_key: str = None,
                            **query_params: Dict[FederatedIdentifiers, Union[str, Iterable[str]]]) -> Optional[dict]:
        """
        Get flattened reference data for a single page. Use returned offsetKey to fetch next page.
        @param is_primary:
        @param type_: security or asset type
        @param effective_date: As of date for query
        @param limit: integer of individual page
        @param offset_key: string, an offset indicating where the page ends
        @return: dict
        """

        return cls.__query_securities(type_=type_,
                                      effective_date=effective_date,
                                      limit=limit,
                                      flatten=True,
                                      is_primary=is_primary,
                                      offset_key=offset_key,
                                      **query_params)

    @classmethod
    def search_many_securities(cls,
                               q: str = None,
                               limit: int = 10,
                               offset_key: str = None,
                               asset_class: AssetClass = None,
                               type_: Union[SecMasterAssetType, AssetType] = None,
                               is_primary: bool = None) -> Optional[dict]:
        """
        Search reference data by a query string. It does a full text search among names, identifiers, company.
        @param q: query string
        @param limit: number of returned matches
        @param offset_key: string, an offset indicating where the page ends
        @param asset_class: filter restricting the class of results
        @param type_: filter restricting the type of results
        @param is_primary: filter restricting the matches to primary listings
        @return: dict
        """

        return cls.__search_securities(q=q,
                                       limit=limit,
                                       offset_key=offset_key,
                                       flatten=False,
                                       asset_class=asset_class,
                                       type_=type_,
                                       is_primary=is_primary)

    @classmethod
    def search_securities_data(cls,
                               q: str = None,
                               limit: int = 10,
                               offset_key: str = None,
                               asset_class: AssetClass = None,
                               type_: Union[SecMasterAssetType, AssetType] = None,
                               is_primary: bool = None) -> Optional[dict]:
        """
        Search flattened reference data by a query string. It does a full text search among names, identifiers, company.
        @param q: query string
        @param limit: number of returned matches
        @param offset_key: string, an offset indicating where the page ends
        @param asset_class: filter restricting the class of results
        @param type_: filter restricting the type of results
        @param is_primary: filter restricting the matches to primary listings
        @return: dict
        """

        return cls.__search_securities(q=q,
                                       limit=limit,
                                       offset_key=offset_key,
                                       flatten=True,
                                       asset_class=asset_class,
                                       type_=type_,
                                       is_primary=is_primary)

    @classmethod
    def __query_securities(cls,
                           type_: Union[SecMasterAssetType, AssetType] = None,
                           effective_date: dt.date = None,
                           limit: int = 50,
                           flatten=False,
                           is_primary=None,
                           offset_key: str = None,
                           **query_params: Dict[FederatedIdentifiers, Union[str, Iterable[str]]]
                           ) -> Optional[dict]:
        if (query_params is None or len(query_params) == 0) and type_ is None:
            raise ValueError("Neither '_type' nor 'query_params' are provided")

        params = {
            "limit": limit
        }
        cls.__prepare_params(params, effective_date, offset_key, is_primary, type_, None)
        params = {**params, **query_params}
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        if flatten:
            return GsSession.current._get(f'{SECURITIES_FEDERATED}/data', payload=payload)
        return GsSession.current._get(f'{SECURITIES_FEDERATED}', payload=payload)

    @classmethod
    def __search_securities(cls,
                            q: str = None,
                            limit: int = 10,
                            offset_key: str = None,
                            flatten=False,
                            asset_class: AssetClass = None,
                            type_: Union[SecMasterAssetType, AssetType] = None,
                            is_primary: bool = None) -> Optional[dict]:
        if (q is None):
            raise ValueError("No search query provided")

        params = {
            "q": q,
            "limit": limit
        }
        cls.__prepare_params(params, None, offset_key, is_primary, type_, asset_class)
        payload = json.loads(json.dumps(params, cls=JSONEncoder))
        if flatten:
            return GsSession.current._get(f'{SECURITIES_FEDERATED}/search/data', payload=payload)
        return GsSession.current._get(f'{SECURITIES_FEDERATED}/search', payload=payload)

    @classmethod
    def __prepare_params(cls, params, effective_date, offset_key, is_primary, type_, asset_class):
        if effective_date is not None:
            params["effectiveDate"] = effective_date
        if offset_key is not None:
            params["offsetKey"] = offset_key
        if is_primary is not None:
            params["isPrimary"] = is_primary
        if type_ is not None:
            params["type"] = type_.value
        if asset_class is not None:
            params["assetClass"] = asset_class.value
