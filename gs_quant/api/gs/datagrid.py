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

import json
import urllib.parse
from typing import List

from pydash import get

from gs_quant.analytics.datagrid import DataGrid
from gs_quant.analytics.datagrid.datagrid import API, DATAGRID_HEADERS
from gs_quant.session import GsSession


class GsDataGridApi:
    """GS DataGrids API implementation"""

    @classmethod
    def get_datagrids(cls, limit: int = 10, **kwargs) -> List[DataGrid]:
        raw_datagrids = get(
            GsSession.current._get(f'{API}?limit={limit}&orderBy=>lastUpdatedTime&{urllib.parse.urlencode(kwargs)}'),
            'results', [])
        return [DataGrid.from_dict(raw_datagrid) for raw_datagrid in raw_datagrids]

    @classmethod
    def get_my_datagrids(cls, limit: int = 10, **kwargs) -> List[DataGrid]:
        user_id = GsSession.current._get('/users/self')['id']
        raw_datagrids = get(
            GsSession.current._get(
                f'{API}?limit={limit}&ownerId={user_id}&orderBy=>lastUpdatedTime&{urllib.parse.urlencode(kwargs)}'),
            'results', [])
        return [DataGrid.from_dict(raw_datagrid) for raw_datagrid in raw_datagrids]

    @classmethod
    def get_datagrid(cls, datagrid_id: str) -> DataGrid:
        raw_datagrid = GsSession.current._get(f'{API}/{datagrid_id}')
        return DataGrid.from_dict(raw_datagrid)

    @classmethod
    def create_datagrid(cls, datagrid: DataGrid) -> DataGrid:
        datagrid_json = json.dumps(datagrid.as_dict())
        response = GsSession.current._post(f'{API}', datagrid_json, request_headers=DATAGRID_HEADERS)
        return DataGrid.from_dict(response)

    @classmethod
    def update_datagrid(cls, datagrid: DataGrid):
        datagrid_json = json.dumps(datagrid.as_dict())
        datagrid = GsSession.current._put(f'{API}/{datagrid.id_}', datagrid_json, request_headers=DATAGRID_HEADERS)
        return DataGrid.from_dict(datagrid)

    @classmethod
    def delete_datagrid(cls, datagrid: DataGrid):
        return GsSession.current._delete(f'{API}/{datagrid.id_}')
