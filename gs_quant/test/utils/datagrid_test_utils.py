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

from gs_quant.markets.securities import Stock
from gs_quant.target.common import Currency


def _read_entity(entity):
    with open(pathlib.Path(__file__).parents[1] / f'resources/{entity}.json') as entity:
        return json.loads(entity.read())


def get_test_entity(entity_id: str):
    entity = _read_entity(entity_id)
    return Stock(id_=entity_id,
                 name=entity['name'],
                 currency=Currency.USD,
                 entity=entity)
