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
import logging
from enum import auto, Enum
from typing import List, Tuple, Union
from gs_quant.target.assets import EntityQuery
from gs_quant.common import FieldFilterMap
from gs_quant.errors import MqValueError
from gs_quant.session import GsSession
from gs_quant.target.assets import Asset as __Asset, Asset

_logger = logging.getLogger(__name__)
IdList = Union[List, Tuple]


class GsIdType(Enum):
    ric = auto()
    bbid = auto()
    bcid = auto()
    cusip = auto()
    isin = auto()
    sedol = auto()
    mdapi = auto()
    primeId = auto()
    id = auto()


class GsAsset(__Asset):

    pass


class GsAssetApi:

    @classmethod
    def __create_query(
        cls,
        fields: Union[List, Tuple],
        as_of: dt.datetime=None,
        limit: int=None,
        **kwargs
    ) -> EntityQuery:
        keys = set(kwargs.keys())
        valid = keys.intersection(i for i in dir(FieldFilterMap) if isinstance(getattr(FieldFilterMap, i), property))
        invalid = keys.difference(valid)

        if invalid:
            bad_args = ['{}={}'.format(k, kwargs[k]) for k in invalid]
            raise KeyError('Invalid asset query argument(s): {}'.format(', '.join(bad_args)))

        return EntityQuery(
            where=FieldFilterMap(**kwargs),
            fields=fields,
            asOfTime=as_of or dt.datetime.now(),
            limit=limit
        )


    @classmethod
    def get_many_assets(
            cls,
            fields: IdList = None,
            as_of: dt.datetime = None,
            limit: int = None,
            **kwargs
    ) -> List[GsAsset]:
        query = cls.__create_query(fields, as_of, limit, **kwargs)
        response = GsSession.current._post('/assets/query', payload=query)

        results = []
        for result in response.get('results', ()):
            results.append(GsAsset(**result))

        return results

    @staticmethod
    def get_asset(
            asset_id: str,
    ) -> GsAsset:
        response = GsSession.current._get('/assets/{id}'.format(id=asset_id), cls=GsAsset)

        return response

    @classmethod
    def map_identifiers(
            cls,
            input_type: Union[GsIdType, str],
            output_type: Union[GsIdType, str],
            ids: IdList,
            as_of: dt.datetime = None,
            multimap: bool = False,
            limit: int = None,
            **kwargs
    ) -> dict:
        if isinstance(input_type, GsIdType):
            input_type = input_type.name
        elif not isinstance(input_type, str):
            raise ValueError('input_type must be of type str or IdType')

        if isinstance(output_type, GsIdType):
            output_type = output_type.name
        elif not isinstance(output_type, str):
            raise ValueError('output_type must be of type str or IdType')

        the_args = kwargs
        the_args[input_type] = ids

        query = cls.__create_query((input_type, output_type), as_of, limit, **the_args)
        response = GsSession.current._post('/assets/data/query', payload=query)

        results = response['results']
        if response['totalResults'] > len(results):
            raise MqValueError('number of results exceeded capacity')

        out = {}
        for entry in response['results']:
            key = entry.get(input_type)
            value = entry.get(output_type)
            if multimap:
                bunch = out.setdefault(key, [])
                bunch.append(value)
            else:
                if key in out:
                    _logger.warning('%s: more than one mapping for %s', GsAssetApi.map_identifiers.__name__, key)
                out[key] = value
        return out
