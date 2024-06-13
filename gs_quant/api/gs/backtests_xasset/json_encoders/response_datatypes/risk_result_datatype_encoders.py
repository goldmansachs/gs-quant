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
import pandas as pd
from typing import Dict


def encode_series_result(s: pd.Series) -> Dict:
    return {'index': tuple(s.index), 'name': s.name, 'values': tuple(s.values)}


def encode_dataframe_result(df: pd.DataFrame) -> Dict:
    return {'index': tuple(df.index), 'columns': tuple(df.columns), 'values': tuple(tuple(v) for v in df.values)}


def _convert_list_to_dates(lst: list):
    if not (lst and isinstance(lst[0], str)):
        return lst
    try:
        lst = tuple(dt.date.fromisoformat(v) for v in lst)
    except ValueError:
        pass
    return lst


def decode_series_result(s: dict) -> pd.Series:
    return pd.Series(s['values'], index=_convert_list_to_dates(s['index']), name=s['name'])


def decode_dataframe_result(s: dict) -> pd.DataFrame:
    return pd.DataFrame(s['values'], index=_convert_list_to_dates(s['index']), columns=s['columns'])
