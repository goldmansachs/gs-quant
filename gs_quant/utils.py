"""
Copyright 2018 Goldman Sachs.
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

import cachetools.func
import inflection
import typing as ty
from .errors import *
from .mqapi import MqSession
from future.utils import bind_method

ENABLED_IDENTIFIERS = {'assetId', 'bbid', 'bcid', 'cross', 'gsid', 'ric', 'sedol', 'isin'}


def _build_getter(key, doc=None):
    def get_value(self):
        return self.store.get(key)

    get_value.__doc__ = doc
    return get_value


def _build_setter(key, doc=None):
    def set_value(self, value):
        if value:
            self.store[key] = value
        else:
            del self.store[key]
        return self

    set_value.__doc__ = doc
    return set_value


def _get_identifier(self):
    """Get identifier type and value."""
    return (self.id_type, self.store[self.id_type]) if self.id_type else None


def _build_id_setter(listed_types):
    def set_identifier(self, id_type, value):
        if id_type not in ENABLED_IDENTIFIERS:
            raise MqValueError('unknown identifier type ' + id_type)
        if self.id_type:
            del self.store[self.id_type]
        self.id_type = id_type
        self.store[id_type] = value
        return self

    set_identifier.__doc__ = 'Set identifier(s) for query. Type must be one of: {}.' \
        .format(', '.join(sorted(listed_types)))
    return set_identifier


@cachetools.func.ttl_cache()
def _generate_query_builder(session, dataset_id):
    # type: (MqSession, ty.AnyStr) -> ty.Tuple[ty.Type[DataQueryBuilder], ty.Dict[ty.AnyStr, ty.AnyStr]]
    clazz = type(inflection.camelize(dataset_id, True) + 'QueryBuilder', (DataQueryBuilder,), {})
    ce = session.get_data_catalog(dataset_id)
    time_field = ce['timeField']

    field_map = {}
    for field, spec in ce['fields'].items():
        if field == time_field or spec.get('format', '').find('date') != -1:
            continue
        if field in ENABLED_IDENTIFIERS and field in ce.get('symbolDimensions', []):
            for ei in ENABLED_IDENTIFIERS:
                field_map[inflection.underscore(ei)] = ei
            listed_types = ENABLED_IDENTIFIERS if field == 'gsid' else ENABLED_IDENTIFIERS - {'gsid'}
            bind_method(clazz, 'set_identifier', _build_id_setter(listed_types))
            bind_method(clazz, 'get_identifier', _get_identifier)
        else:
            normalized = inflection.underscore(field)
            field_map[normalized] = field
            bind_method(clazz, 'set_' + normalized,
                        _build_setter(normalized, '(list of) {}: {}'.format(spec['type'], spec.get('description'))))
            bind_method(clazz, 'get_' + normalized,
                        _build_getter(normalized, 'retrieve {}: {}'.format(normalized, spec.get('description'))))
    return clazz, field_map


def get_query_builder(session, dataset_id):
    """
    Get a query builder object to be used in querying the Marquee Data Service.

    :param session: an active session
    :param dataset_id: id of dataset to be queried
    :return: a new query builder
    """
    clazz, field_map = _generate_query_builder(session, dataset_id)
    return clazz(field_map)


class DataQueryBuilder:
    """
    Helper class to construct data service queries. Setter methods return self to allow method chaining
    (fluent pattern).
    """

    def __init__(self, field_map):
        self.store = dict()
        self.field_map = field_map
        self.id_type = None

    def build(self):
        """Build a query object that can be passed to a get_data* method"""
        return {self.field_map[k]: v for k, v in self.store.items()}

    def __str__(self):
        return self.store.__str__()

    def __repr__(self):
        return self.store.__repr__()
