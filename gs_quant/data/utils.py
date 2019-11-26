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

import logging
from typing import Union

import cachetools
import numpy
import pandas as pd
from cachetools import TTLCache

from gs_quant.base import Base
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)


@cachetools.cached(TTLCache(ttl=3600, maxsize=128))
def get_types(dataset_id: str):
    results = GsSession.current._get(f'/data/catalog/{dataset_id}')
    if results.get("fields"):
        field_types = {}
        for key, value in results.get("fields").items():
            field_type = value.get('type')
            field_format = value.get('format')
            if field_type:
                if field_format:
                    field_types[key] = field_format
                else:
                    field_types[key] = field_type
            else:
                break
        return field_types
    raise RuntimeError(f"Unable to get Dataset schema for {dataset_id}")


def construct_dataframe_with_types(dataset_id: str, data: Union[Base, list, tuple]) -> pd.DataFrame:
    """
    Constructs a dataframe with correct date types.
    :param data: data to convert with correct types
    :return: dataframe with correct types
    """
    if len(data) > 0:
        dataset_types = get_types(dataset_id)
        df = pd.DataFrame(data)

        for field_name, type_name in dataset_types.items():
            if df.get(type_name) is not None and type_name in ('date', 'date-time'):
                df = df.astype({field_name: numpy.datetime64})

        field_names = dataset_types.keys()

        if 'date' in field_names:
            df = df.set_index('date')
        elif 'time' in field_names:
            df = df.set_index('time')

        return df
    else:
        return pd.DataFrame({})
