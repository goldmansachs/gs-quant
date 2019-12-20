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

import socket
import requests


def handle_proxy(url, params):
    if socket.getfqdn().split('.')[-2:] == ['gs', 'com']:
        try:
            import gs_quant_internal
            proxies = gs_quant_internal.__proxies__
            response = requests.get(url, params=params, proxies=proxies)
        except ModuleNotFoundError:
            raise RuntimeError('You must install gs_quant_internal to be able to use this endpoint')
    else:
        response = requests.get(url, params=params)
    return response
