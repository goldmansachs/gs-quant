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

import urllib.parse
from typing import Tuple, Dict

from pydash import get

from gs_quant.session import GsSession
from gs_quant.target.workspaces_markets import Workspace

import webbrowser

API = '/workspaces/markets'
WORKSPACES_MARKETS_HEADERS: Dict[str, str] = {'Content-Type': 'application/json;charset=utf-8'}


class GsWorkspacesMarketsApi:
    """GS Workspaces Markets API implementation"""

    @classmethod
    def get_workspaces(cls, limit: int = 10, **kwargs) -> Tuple[Workspace, ...]:
        return GsSession.current._get(f'{API}?limit={limit}&{urllib.parse.urlencode(kwargs)}', cls=Workspace)['results']

    @classmethod
    def get_workspace(cls, workspace_id: str):
        return GsSession.current._get(f'{API}/{workspace_id}', cls=Workspace)

    @classmethod
    def get_workspace_by_alias(cls, alias: str) -> Workspace:
        workspace = get(GsSession.current._get(f'{API}?alias={alias}', cls=Workspace), 'results.0')
        if not workspace:
            raise ValueError(f'Workspace with alias {alias} not found')
        return workspace

    @classmethod
    def create_workspace(cls, workspace: Workspace) -> Workspace:
        return GsSession.current._post(f'{API}', workspace, cls=Workspace, request_headers=WORKSPACES_MARKETS_HEADERS)

    @classmethod
    def update_workspace(cls, workspace: Workspace):
        return GsSession.current._put(f'{API}/{workspace.id}', workspace, cls=Workspace,
                                      request_headers=WORKSPACES_MARKETS_HEADERS)

    @classmethod
    def delete_workspace(cls, workspace_id: str) -> Dict:
        return GsSession.current._delete(f'{API}/{workspace_id}')

    @classmethod
    def open_workspace(cls, workspace: Workspace):
        if workspace.alias:
            webbrowser.open(f'{GsSession.current.domain.replace(".web", "")}/s/markets/{workspace.alias}')
        else:
            webbrowser.open(f'{GsSession.current.domain.replace(".web", "")}/s/markets/{workspace.id}')
