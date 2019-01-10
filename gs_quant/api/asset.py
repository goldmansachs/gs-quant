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

from datetime import datetime
from enum import auto, Enum
from typing import List, Union
from gs_quant.target.assets import *
from gs_quant.session import GsSession


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


class Asset:

    @staticmethod
    def get_many_assets(
            where: dict = None,
            fields: list = None,
            as_of=None
    ):
        query = {'where': where, 'fields': fields, 'asOfTime': as_of or datetime.now()}
        response = GsSession.current._post('/assets/query', payload=query)

        return response

    @staticmethod
    def map_identifiers(
            input_type: Union[IdType, str],
            output_type: Union[IdType, str],
            ids: List[str],
            as_of=None
    ):
        if isinstance(input_type, IdType):
            input_type = input_type.name
        elif not isinstance(input_type, str):
            raise ValueError('input_type must be of type str or IdType')

        if isinstance(output_type, IdType):
            output_type = output_type.name
        elif not isinstance(output_type, str):
            raise ValueError('output_type must be of type str or IdType')

        query = {'where': {input_type: ids}, 'fields': (input_type, output_type), 'asOfTime': as_of or datetime.now()}
        response = GsSession.current._post('/assets/data/query', payload=query)
        return {entry.pop(input_type): entry.get(output_type) for entry in response['results']}

