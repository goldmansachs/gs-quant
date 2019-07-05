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
from urllib.parse import urlencode
from typing import Tuple

from gs_quant.session import GsSession
from gs_quant.target.monitor import Monitor, MonitorResponseData

_logger = logging.getLogger(__name__)


class GsMonitorApi:
    """GS Monitor API client implementation"""

    @classmethod
    def get_monitors(cls,
                     limit: int = 100,
                     monitor_id: str = None,
                     owner_id: str = None,
                     name: str = None,
                     folder_name: str = None,
                     monitor_type: str = None) -> Tuple[Monitor, ...]:
        query_string = urlencode(dict(filter(lambda item: item[1] is not None,
                                             dict(id=monitor_id, ownerId=owner_id, name=name, folderName=folder_name,
                                                  type=monitor_type, limit=limit).items())))
        return GsSession.current._get('/monitors?{query}'.format(query=query_string), cls=Monitor)['results']

    @classmethod
    def get_monitor(cls, monitor_id: str) -> Monitor:
        return GsSession.current._get('/monitors/{id}'.format(id=monitor_id), cls=Monitor)

    @classmethod
    def create_monitor(cls, monitor: Monitor) -> Monitor:
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/monitors', monitor, request_headers=request_headers, cls=Monitor)

    @classmethod
    def update_monitor(cls, monitor: Monitor):
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._put('/monitors/{id}'.format(id=monitor.id), monitor, request_headers=request_headers,
                                      cls=Monitor)

    @classmethod
    def delete_monitor(cls, monitor_id: str) -> dict:
        return GsSession.current._delete('/monitors/{id}'.format(id=monitor_id))

    @classmethod
    def calculate_monitor(cls, monitor_id) -> MonitorResponseData:
        return GsSession.current._get('/monitors/{id}/data'.format(id=monitor_id), cls=MonitorResponseData)
