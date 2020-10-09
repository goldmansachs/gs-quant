"""
Copyright 2020 Goldman Sachs.
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
from typing import Tuple

from gs_quant.session import GsSession
from gs_quant.target.countries import Country, Subdivision


class GsCountryApi:
    """GS Country API client implementation"""

    @classmethod
    def get_many_countries(cls, limit: int = 100) -> Tuple[Country, ...]:
        return GsSession.current._get('/countries?limit={limit}'.format(limit=limit), cls=Country)['results']

    @classmethod
    def get_country(cls, country_id: str) -> Country:
        return GsSession.current._get('/countries/{id}'.format(id=country_id), cls=Country)

    @classmethod
    def create_country(cls, country: Country) -> Country:
        return GsSession.current._post('/countries', country, cls=Country)

    @classmethod
    def update_country(cls, country: Country):
        return GsSession.current._put('/countries/{id}'.format(id=country.id), country, cls=Country)

    @classmethod
    def delete_country(cls, country_id: str) -> dict:
        return GsSession.current._delete('/countries/{id}'.format(id=country_id))

    @classmethod
    def get_many_subdivisions(cls, limit: int = 100) -> Tuple[Subdivision, ...]:
        return GsSession.current._get('/countries/subdivisions?limit={limit}'.format(limit=limit),
                                      cls=Subdivision)['results']

    @classmethod
    def get_subdivision(cls, subdivision_id: str) -> Subdivision:
        return GsSession.current._get('/countries/subdivisions/{id}'.format(id=subdivision_id), cls=Subdivision)

    @classmethod
    def create_subdivision(cls, subdivision: Subdivision) -> Subdivision:
        return GsSession.current._post('/countries/subdivisions', subdivision, cls=Subdivision)

    @classmethod
    def update_subdivision(cls, subdivision: Subdivision):
        return GsSession.current._put('/countries/subdivisions/{id}'.format(id=subdivision.id), subdivision,
                                      cls=Subdivision)

    @classmethod
    def delete_subdivision(cls, subdivision_id: str) -> dict:
        return GsSession.current._delete('/countries/subdivisions/{id}'.format(id=subdivision_id))
