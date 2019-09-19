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
import pathlib
from typing import Union

from gs_quant.base import Base


def __unpack(results: Union[dict, list], cls: type) -> Union[Base, tuple, dict]:
    if issubclass(cls, Base):
        if isinstance(results, list):
            return tuple(None if r is None else cls.from_dict(r) for r in results)
        else:
            return None if results is None else cls.from_dict(results)
    else:
        if isinstance(results, list):
            return tuple(cls(**r) for r in results)
        else:
            return cls(**results)


def handle_response(res, cls=None):
    if cls:
        if isinstance(res, dict) and 'results' in res:
            res['results'] = __unpack(res['results'], cls)
        else:
            res = __unpack(res, cls)

    return res


def mock_request(path, payload=None, cls=None):
    response = {}
    "/assets/{id}/xrefs"
    if '/assets' in path:
        if path == "/assets/query":
            bbid = payload.where.bbid
            with open(pathlib.Path(__file__).parents[1] / f'resources/asset-query-{bbid}.json') as response:
                response = handle_response(json.load(response), cls)
        else:
            split = path.split("/")
            asset_id = split[2]
            if len(split) == 3:
                with open(pathlib.Path(__file__).parents[1] / f'resources/{asset_id}.json') as response:
                    response = handle_response(json.load(response), cls)
            else:
                if "xrefs" in path:
                    with open(pathlib.Path(__file__).parents[1] / f'resources/{asset_id}-xrefs.json') as response:
                        response = handle_response(json.load(response), cls)
    return response
