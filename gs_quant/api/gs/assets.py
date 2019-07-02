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
import logging
from enum import auto, Enum
from typing import Iterable, List, Tuple, Optional, Union
from gs_quant.target.assets import Asset as __Asset, AssetClass, AssetType, AssetToInstrumentResponse, TemporalXRef,\
    Position, PositionSet, EntityQuery, PositionSet
from gs_quant.target.common import FieldFilterMap
from gs_quant.errors import MqValueError
from gs_quant.instrument import Instrument, Security
from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)
IdList = Union[Tuple[str, ...], List]


class GsIdType(Enum):
    """GS Asset API identifier type enumeration"""

    ric = auto()
    bbid = auto()
    bcid = auto()
    cusip = auto()
    isin = auto()
    sedol = auto()
    mdapi = auto()
    primeId = auto()
    id = auto()


class GsAsset(__Asset):
    """GS Asset API object model for an asset object"""
    pass


class GsTemporalXRef(TemporalXRef):
    pass


class GsAssetApi:
    """GS Asset API client implementation"""

    @classmethod
    def __create_query(
            cls,
            fields: Union[List, Tuple] = None,
            as_of: dt.datetime = None,
            limit: int = None,
            **kwargs
    ) -> EntityQuery:
        keys = set(kwargs.keys())
        valid = keys.intersection(i for i in dir(FieldFilterMap) if isinstance(getattr(FieldFilterMap, i), property))
        invalid = keys.difference(valid)

        if invalid:
            bad_args = ['{}={}'.format(k, kwargs[k]) for k in invalid]
            raise KeyError('Invalid asset query argument(s): {}'.format(', '.join(bad_args)))

        return EntityQuery(
            where=FieldFilterMap(**kwargs),
            fields=fields,
            asOfTime=as_of or dt.datetime.utcnow(),
            limit=limit
        )

    @classmethod
    def get_many_assets(
            cls,
            fields: IdList = None,
            as_of: dt.datetime = None,
            limit: int = 100,
            **kwargs
    ) -> Tuple[GsAsset, ...]:
        query = cls.__create_query(fields, as_of, limit, **kwargs)
        response = GsSession.current._post('/assets/query', payload=query, cls=GsAsset)
        return response['results']

    @classmethod
    def get_many_assets_data(
            cls,
            fields: IdList = None,
            as_of: dt.datetime = None,
            limit: int = None,
            **kwargs
    ) -> dict:
        query = cls.__create_query(fields, as_of, limit, **kwargs)
        response = GsSession.current._post('/assets/data/query', payload=query)
        return response['results']

    @classmethod
    def get_asset_xrefs(
            cls,
            asset_id: str
    ) -> Tuple[GsTemporalXRef, ...]:
        response = GsSession.current._get('/assets/{id}/xrefs'.format(id=asset_id))
        return tuple(GsTemporalXRef.from_dict(x) for x in response.get('xrefs', ()))

    @classmethod
    def get_asset(
            cls,
            asset_id: str,
    ) -> GsAsset:
        return GsSession.current._get('/assets/{id}'.format(id=asset_id), cls=GsAsset)

    @staticmethod
    def get_asset_positions_for_date(
            asset_id: str,
            position_date: dt.date,
            position_type: str = None,
    ) -> Tuple[PositionSet, ...]:
        position_date_str = position_date.isoformat()
        url = '/assets/{id}/positions/{date}'.format(id=asset_id, date=position_date_str)

        if position_type is not None:
            url += '?type=' + position_type

        results = GsSession.current._get(url)['results']
        return tuple(PositionSet.from_dict(r) for r in results)

    @staticmethod
    def get_instruments_for_asset_ids(
            asset_ids: Tuple[str]
    ) -> Tuple[Optional[Union[Instrument, Security]]]:
        instrument_infos = GsSession.current._post('/assets/instruments', asset_ids, cls=AssetToInstrumentResponse)
        instrument_lookup = {i.assetId: i.instrument for i in instrument_infos if i}
        ret: Tuple[Optional[Union[Instrument, Security]]] = tuple(instrument_lookup.get(a) for a in asset_ids)

        return ret

    @staticmethod
    def get_instruments_for_positions(
            positions: Iterable[Position]
    ) -> Tuple[Optional[Union[Instrument, Security]]]:
        instrument_infos = GsSession.current._post('/assets/instruments', [p.assetId for p in positions], cls=AssetToInstrumentResponse)
        instrument_lookup = {i.assetId: (i.instrument, i.sizeField) for i in instrument_infos if i}
        ret = ()

        for position in positions:
            instrument_info = instrument_lookup.get(position.assetId)
            if instrument_info:
                instrument, size_field = instrument_info
                if instrument is not None and size_field is not None and getattr(instrument, size_field, None) is None:
                    setattr(instrument, size_field, position.quantity)
                ret += (instrument,)
            else:
                ret += (None,)

        return tuple(ret)

    @classmethod
    def map_identifiers(
            cls,
            input_type: Union[GsIdType, str],
            output_type: Union[GsIdType, str],
            ids: IdList,
            as_of: dt.datetime = None,
            multimap: bool = False,
            limit: int = None,
            **kwargs
    ) -> dict:
        if isinstance(input_type, GsIdType):
            input_type = input_type.name
        elif not isinstance(input_type, str):
            raise ValueError('input_type must be of type str or IdType')

        if isinstance(output_type, GsIdType):
            output_type = output_type.name
        elif not isinstance(output_type, str):
            raise ValueError('output_type must be of type str or IdType')

        the_args = kwargs
        the_args[input_type] = ids

        limit = limit or 4 * len(ids)
        query = cls.__create_query((input_type, output_type), as_of, limit, **the_args)
        results = GsSession.current._post('/assets/data/query', payload=query)
        if len(results) >= query.limit:
            raise MqValueError('number of results may have exceeded capacity')

        if 'results' in results:
            results = results['results']

        out = {}
        for entry in results:
            key = entry.get(input_type)
            value = entry.get(output_type)
            if multimap:
                bunch = out.setdefault(key, [])
                bunch.append(value)
            else:
                if key in out:
                    _logger.warning('%s: more than one mapping for %s', GsAssetApi.map_identifiers.__name__, key)
                out[key] = value
        return out
