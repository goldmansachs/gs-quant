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

from gs_quant.target.assets import *
from gs_quant.target.assets import Asset as __Asset
from gs_quant.api.common import FieldFilterMap
from gs_quant.session import GsSession

from datetime import datetime
from enum import auto, Enum
from typing import List, Tuple, Union

IdList = Union[List[str], Tuple[str]]


class IdType(Enum):
    ric = auto()
    bbid = auto()
    bcid = auto()
    cusip = auto()
    isin = auto()
    sedol = auto()
    mdapi = auto()
    id = auto(),
    name = auto()


class Asset(__Asset):

    @staticmethod
    def __check_kwargs_valid_for_where(**kwargs):
        keys = set(kwargs.keys())
        valid = keys.intersection(i for i in dir(FieldFilterMap) if isinstance(getattr(FieldFilterMap, i), property))
        invalid = keys.difference(valid)

        if invalid:
            bad_args = ['{}={}'.format(k, kwargs[k]) for k in invalid]
            raise KeyError('Invalid asset query argument(s): {}'.format(', '.join(bad_args)))

    @staticmethod
    def get_many_assets(
            fields: IdList=None,
            as_of: datetime=None,
            limit: int=None,
            **kwargs
    ) -> List[Asset]:
        Asset.__check_kwargs_valid_for_where(**kwargs)

        query = EntityQuery(
            where=FieldFilterMap(**kwargs),
            fields=fields,
            asOfTime=as_of or datetime.now(),
            limit=limit
        )
        response = GsSession.current._post('/assets/query', payload=query)

        results = []
        for result in response.get('results', ()):
            results.append(Asset(**result))

        return results

    @staticmethod
    def map_identifiers(
            input_type: Union[IdType, str],
            output_type: Union[IdType, str],
            ids: IdList,
            as_of: datetime=None,
            **kwargs
    ) -> dict:
        if isinstance(input_type, IdType):
            input_type = input_type.name
        elif not isinstance(input_type, str):
            raise ValueError('input_type must be of type str or IdType')

        if isinstance(output_type, IdType):
            output_type = output_type.name
        elif not isinstance(output_type, str):
            raise ValueError('output_type must be of type str or IdType')

        Asset.__check_kwargs_valid_for_where(**kwargs)

        where = FieldFilterMap(**kwargs)
        setattr(where, input_type, ids)

        query = EntityQuery(
            where=where,
            fields=(input_type, output_type),
            asOfTime=as_of or datetime.now()
        )
        response = GsSession.current._post('/assets/data/query', payload=query)
        return {entry.pop(input_type): entry.get(output_type) for entry in response['results']}
