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
import re
from typing import Optional, Union, Iterable, Dict, Tuple, Any

from dataclasses_json import config
from dataclasses import MISSING, fields
from dateutil.parser import isoparse


__valid_date_formats = ('%Y-%m-%d',  # '2020-07-28'
                        '%d%b%y',  # '28Jul20'
                        '%d-%b-%y',  # '28-Jul-20'
                        '%d/%m/%Y')  # '28/07/2020

DateOrDateTime = Union[dt.date, dt.datetime]


def encode_date_or_str(value: Optional[Union[str, dt.date]]) -> Optional[str]:
    return value.isoformat() if isinstance(value, dt.date) else value


def decode_optional_date(value: Optional[str]) -> Optional[dt.date]:
    # from dataclasses-json 0.6.5 onwards the global config for type T will be applied to Optional[T]
    # So this decoder would become redundant, to allow any version we simply return if it's already a date
    if value is None or isinstance(value, dt.date):
        return value
    elif isinstance(value, str):
        return dt.datetime.strptime(value, '%Y-%m-%d').date()

    raise ValueError(f'Cannot convert {value} to date')


def decode_optional_time(value: Optional[str]) -> Optional[dt.time]:
    # from dataclasses-json 0.6.5 onwards the global config for type T will be applied to Optional[T]
    # So this decoder would become redundant, to allow any version we simply return if it's already a time
    if value is None or isinstance(value, dt.time):
        return value
    elif isinstance(value, str):
        return dt.time.fromisoformat(value)

    raise ValueError(f'Cannot convert {value} to date')


def encode_optional_time(value: Optional[Union[str, dt.time]]) -> Optional[str]:
    return value.isoformat() if isinstance(value, dt.time) else value


def decode_date_tuple(blob: Tuple[str, ...]):
    return tuple(decode_optional_date(s) for s in blob) if isinstance(blob, (tuple, list)) else None


def encode_date_tuple(values: Tuple[Optional[Union[str, dt.date]], ...]):
    return tuple(encode_date_or_str(value) if isinstance(value, (str, dt.date)) else None for value in values) if \
        values is not None else None


def decode_iso_date_or_datetime(value: Any) -> Union[Tuple[DateOrDateTime, ...], DateOrDateTime]:
    if isinstance(value, (tuple, list)):
        return tuple(decode_iso_date_or_datetime(v) for v in value)
    if isinstance(value, (dt.date, dt.datetime)):
        return value
    elif isinstance(value, str):
        if len(value) == 10:
            return decode_optional_date(value)
        else:
            return optional_from_isodatetime(value)
    raise TypeError(f'Cannot convert {value} to date or datetime')


def optional_from_isodatetime(datetime: Union[str, dt.datetime, None]) -> Optional[dt.datetime]:
    if datetime is None or isinstance(datetime, dt.datetime):
        return datetime
    return dt.datetime.fromisoformat(datetime.replace('Z', ''))


def optional_to_isodatetime(datetime: Optional[dt.datetime]):
    return f'{dt.datetime.isoformat(datetime, timespec="seconds")}Z' if datetime is not None else None


optional_datetime_config = config(encoder=optional_to_isodatetime, decoder=optional_from_isodatetime)
optional_date_config = config(encoder=encode_date_or_str, decoder=decode_optional_date)


def decode_dict_date_key(value):
    return {dt.date.fromisoformat(d): v for d, v in value.items()} if value is not None else None


def decode_dict_dict_date_key(value):
    return {k: {dt.date.fromisoformat(d): v for d, v in val.items()} if val is not None else None
            for k, val in value.items()} if value is not None else None


def decode_dict_date_value(value):
    return {k: dt.date.fromisoformat(d) for k, d in value.items()} if value is not None else None


def decode_datetime_tuple(blob: Tuple[str, ...]):
    return tuple(optional_from_isodatetime(s) for s in blob) if isinstance(blob, (tuple, list)) else None


def decode_date_or_str(value: Union[dt.date, float, str]) -> Optional[Union[dt.date, str]]:
    if value is None or isinstance(value, dt.date):
        return value
    elif isinstance(value, float):
        # Assume it's an Excel date
        if value > 59:
            value -= 1  # Excel leap year bug, 1900 is not a leap year!
        return (dt.datetime(1899, 12, 31) + dt.timedelta(days=value)).date()
    elif isinstance(value, str):
        # Try the supported string date formats
        for fmt in __valid_date_formats:
            try:
                return dt.datetime.strptime(value, fmt).date()
            except ValueError:
                pass

        # Assume it's a tenor
        return value

    raise TypeError(f'Cannot convert {value} to date')


def encode_datetime(value: Optional[dt.datetime]) -> Optional[str]:
    if value is None:
        return value

    try:
        iso_formatted = value.isoformat(timespec='milliseconds')
    except TypeError:
        # Pandas Timestamp objects don't take timespec, will raise TypeError (as of 1.2.4)
        iso_formatted = value.isoformat()

    return iso_formatted if value.tzinfo else iso_formatted + 'Z'  # Make sure to be explict about timezone


def decode_datetime(value: Optional[Union[int, str]]) -> Optional[dt.datetime]:
    if value is None or isinstance(value, dt.datetime):
        return value
    if isinstance(value, int):
        return dt.datetime.fromtimestamp(value / 1000)
    elif isinstance(value, str):
        matcher = re.search('\\.([0-9]*)Z$', value)
        if matcher:
            sub_seconds = matcher.group(1)
            if len(sub_seconds) > 6:
                value = re.sub(matcher.re, '.{}Z'.format(sub_seconds[:6]), value)

        return isoparse(value)

    raise TypeError(f'Cannot convert {value} to datetime')


def decode_float_or_str(value: Optional[Union[float, int, str]]) -> Optional[Union[float, str]]:
    if value is None:
        return value
    elif isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            # Assume it's a strike or similar, e.g. 'ATM'
            return value

    raise TypeError(f'Cannot convert {value} to float')


def decode_instrument(value: Optional[Dict]):
    from gs_quant.instrument import Instrument
    return Instrument.from_dict(value) if value else None


def decode_named_instrument(value: Optional[Union[Iterable[Dict], dict]]):
    from gs_quant.instrument import Instrument
    if isinstance(value, (list, tuple)):
        return tuple(decode_named_instrument(v) for v in value)
    elif isinstance(value, dict) and 'portfolio_name' in value.keys():
        return decode_named_portfolio(value)
    return Instrument.from_dict(value) if value else None


def decode_named_portfolio(value):
    from gs_quant.markets.portfolio import Portfolio
    return Portfolio([decode_named_instrument(v) for v in value['instruments']],
                     name=value['portfolio_name'])


def encode_named_instrument(obj):
    from gs_quant.markets.portfolio import Portfolio
    if isinstance(obj, (list, tuple)):
        return tuple(encode_named_instrument(o) for o in obj)
    elif isinstance(obj, Portfolio):
        return encode_named_portfolio(obj)
    return obj.as_dict()


def encode_named_portfolio(obj):
    return {'portfolio_name': obj.name,
            'instruments': tuple(encode_named_instrument(o) for o in obj.all_instruments)}


def encode_pandas_series(obj):
    series_dict = pd.Series.to_dict(obj)
    if isinstance(next(iter(series_dict)), (dt.date, dt.datetime)):
        series_dict = {k.isoformat(): v for k, v in series_dict.items()}
    return series_dict


def decode_pandas_series(value: dict):
    dated_dict = {decode_iso_date_or_datetime(k): v for k, v in value.items()}
    return pd.Series(dated_dict)


def decode_quote_report(value: Optional[dict]):
    from gs_quant.quote_reports.core import quote_report_from_dict
    return quote_report_from_dict(value) if value else None


def decode_quote_reports(value: Optional[Iterable[Dict]]):
    from gs_quant.quote_reports.core import quote_reports_from_dicts
    return quote_reports_from_dicts(value) if value else None


def decode_custom_comment(value: Optional[dict]):
    from gs_quant.quote_reports.core import custom_comment_from_dict
    return custom_comment_from_dict(value) if value else None


def decode_custom_comments(value: Optional[Iterable[Dict]]):
    from gs_quant.quote_reports.core import custom_comments_from_dicts
    return custom_comments_from_dicts(value) if value else None


def decode_hedge_type(value: Optional[dict]):
    from gs_quant.quote_reports.core import hedge_type_from_dict
    return hedge_type_from_dict(value) if value else None


def decode_hedge_types(value: Optional[Iterable[Dict]]):
    from gs_quant.quote_reports.core import hedge_type_from_dicts
    return hedge_type_from_dicts(value) if value else None


def encode_dictable(o):
    return o if o is None else o.to_dict()


def encode_named_dictable(o):
    d = encode_dictable(o)
    if d is not None:
        d['type'] = type(o).__name__
    return d


def _get_dc_type(cls, name_field: str, allow_missing: bool):
    type_field = list(filter(lambda f: f.name in (name_field, f'{name_field}_'), fields(cls)))
    if len(type_field) == 0:
        if allow_missing:
            return None
        raise ValueError(f'Class {cls} has no "{name_field}" property')
    def_value = type_field[0].default
    if def_value == MISSING or def_value is None:
        raise ValueError('No default value for "class_type" field on class')
    return def_value


def _value_decoder(type_to_cls_map, explicit_cls=None, str_mapper=None):
    def decode_value(value):
        if value is None or 'null' == value:
            return None
        if isinstance(value, (list, tuple)):
            return tuple(decode_value(v) for v in value)
        if isinstance(value, str):
            return str_mapper(value) if str_mapper is not None else value
        if isinstance(value, (float, int, dt.date)):
            return value
        if not isinstance(value, dict):
            raise TypeError(f'Cannot decode object of type: {type(value)}')
        if explicit_cls is not None:
            return explicit_cls.from_dict(value)
        else:
            if 'class_type' not in value:
                raise ValueError(f'Object has no "class_type" property {value}')
            obj_type = value['class_type']
            if obj_type not in type_to_cls_map:
                raise ValueError(f'No class mapping for object type: "{obj_type}"')
            try:
                return type_to_cls_map[obj_type].from_dict(value)
            except Exception as e:
                raise ValueError(f'Failed to de-serialise {type_to_cls_map[obj_type]} from value {value}') from e

    return decode_value


def dc_decode(*classes, name_field='class_type', allow_missing=False):
    mappings = ((_get_dc_type(cls, name_field, allow_missing), cls) for cls in classes)
    type_to_cls_map = dict((k, v) for k, v in mappings if k is not None)
    return _value_decoder(type_to_cls_map, None)
