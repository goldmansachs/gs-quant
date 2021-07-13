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
from typing import Iterable, Optional, Union

from .core import DataFrameWithInfo, ErrorValue, UnsupportedValue, FloatWithInfo, StringWithInfo, sort_values
from .measures import EqDelta, EqGamma, EqVega
from gs_quant.base import InstrumentBase, RiskKey

_logger = logging.getLogger(__name__)
__scalar_risk_measures = (EqDelta, EqGamma, EqVega)


def __dataframe_handler(result: Iterable, mappings: tuple, risk_key: RiskKey, request_id: Optional[str] = None) \
        -> DataFrameWithInfo:
    first_row = next(iter(result), None)
    if first_row is None:
        return DataFrameWithInfo(risk_key=risk_key, request_id=request_id)

    columns = ()
    indices = [False] * len(first_row.keys())
    mappings_lookup = {v: k for k, v in mappings}

    for idx, src in enumerate(first_row.keys()):
        if src in mappings_lookup:
            indices[idx] = True
            columns += ((mappings_lookup[src]),)

    records = tuple(
        sort_values((tuple(v for i, v in enumerate(r.values()) if indices[i]) for r in result), columns, columns)
    )

    df = DataFrameWithInfo(records, risk_key=risk_key, request_id=request_id)
    df.columns = columns

    return df


def cashflows_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase, request_id: Optional[str] = None) \
        -> DataFrameWithInfo:
    mappings = (
        ('payment_date', 'payDate'),
        ('set_date', 'setDate'),
        ('accrual_start_date', 'accStart'),
        ('accrual_end_date', 'accEnd'),
        ('payment_amount', 'payAmount'),
        ('notional', 'notional'),
        ('payment_type', 'paymentType'),
        ('floating_rate_option', 'index'),
        ('floating_rate_designated_maturity', 'indexTerm'),
        ('day_count_fraction', 'dayCountFraction'),
        ('spread', 'spread'),
        ('rate', 'rate'),
        ('discount_factor', 'discountFactor')
    )

    for cashflow in result['cashflows']:
        for field in ('payDate', 'setDate', 'accStart', 'accEnd'):
            value = cashflow.get(field)
            date = dt.datetime.strptime(value, '%Y-%m-%d').date() if value else dt.date.max
            cashflow[field] = date

    return __dataframe_handler(result['cashflows'], mappings, risk_key, request_id=request_id)


def error_handler(result: dict, risk_key: RiskKey, instrument: InstrumentBase, request_id: Optional[str] = None) \
        -> ErrorValue:
    error = result.get('errorString', 'Unknown error')
    if request_id:
        error += f'. request Id={request_id}'

    _logger.error(f'Error while computing {risk_key.risk_measure} on {instrument} for {risk_key.date}: {error}')
    return ErrorValue(risk_key, error, request_id=request_id)


def leg_definition_handler(result: dict, risk_key: RiskKey, instrument: InstrumentBase,
                           request_id: Optional[str] = None) -> InstrumentBase:
    return instrument.resolved(result, risk_key)


def message_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase, request_id: Optional[str] = None) \
        -> StringWithInfo:
    return StringWithInfo(risk_key, result.get('message'), request_id=request_id)


def number_and_unit_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                            request_id: Optional[str] = None) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result.get('value', float('nan')), unit=result.get('unit'), request_id=request_id)


def required_assets_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                            request_id: Optional[str] = None) -> DataFrameWithInfo:
    mappings = (('mkt_type', 'type'), ('mkt_asset', 'asset'))
    return __dataframe_handler(result['requiredAssets'], mappings, risk_key, request_id=request_id)


def risk_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase, request_id: Optional[str] = None) \
        -> Union[DataFrameWithInfo, FloatWithInfo]:
    if result.get('children'):
        # result with leg valuations
        classes = []
        if result.get('val'):
            classes.append({'path': 'parent', 'value': result.get('val')})

        for key, val in result.get('children').items():
            classes.append({'path': key, 'value': val})
        mappings = (
            ('path', 'path'),
            ('value', 'value')
        )
        return __dataframe_handler(classes, mappings, risk_key, request_id=request_id)
    else:
        return FloatWithInfo(risk_key, result.get('val', float('nan')), unit=result.get('unit'), request_id=request_id)


def risk_by_class_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                          request_id: Optional[str] = None) -> Union[DataFrameWithInfo, FloatWithInfo]:
    # TODO Remove this once we migrate parallel USD IRDelta measures
    types = [c['type'] for c in result['classes']]
    # list of risk by class measures exposed in gs-quant
    external_risk_by_class_val = ['IRBasisParallel', 'IRDeltaParallel', 'IRVegaParallel', 'PnlExplain']
    if str(risk_key.risk_measure) in external_risk_by_class_val and len(types) <= 2 and len(set(types)) == 1:
        return FloatWithInfo(risk_key, sum(result.get('values', (float('nan'),))), unit=result.get('unit'),
                             request_id=request_id)
    else:
        classes = []
        skip = []

        crosses_idx = next((i for i, c in enumerate(result['classes']) if c['type'] == 'CROSSES'), None)
        for idx, (clazz, value) in enumerate(zip(result['classes'], result['values'])):
            mkt_type = clazz['type']
            if 'SPIKE' in mkt_type or 'JUMP' in mkt_type:
                skip.append(idx)

                if crosses_idx is not None:
                    result['classes'][crosses_idx]['value'] += value

            clazz.update({'value': value})

        for idx, clazz in enumerate(result['classes']):
            if idx not in skip:
                classes.append(clazz)

        mappings = (
            ('mkt_type', 'type'),
            ('mkt_asset', 'asset'),
            ('value', 'value')
        )

        return __dataframe_handler(classes, mappings, risk_key, request_id=request_id)


def risk_vector_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                        request_id: Optional[str] = None) -> DataFrameWithInfo:
    assets = result['asset']
    # Handle equity risk measures which are really scalars
    if len(assets) == 1 and risk_key.risk_measure in __scalar_risk_measures:
        return FloatWithInfo(risk_key, assets[0], request_id=request_id)

    for points, value in zip(result['points'], assets):
        points.update({'value': value})

    mappings = (
        ('mkt_type', 'type'),
        ('mkt_asset', 'asset'),
        ('mkt_class', 'class_'),
        ('mkt_point', 'point'),
        ('mkt_quoting_style', 'quoteStyle'),
        ('value', 'value')
    )

    return __dataframe_handler(result['points'], mappings, risk_key, request_id=request_id)


def risk_theta_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                       request_id: Optional[str] = None) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result['values'][0], request_id=request_id)


def mdapi_table_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                        request_id: Optional[str] = None) -> DataFrameWithInfo:
    coordinates = []
    for r in result['rows']:
        point = ';'.join(r['coordinate']['point']) if isinstance(r['coordinate']['point'], list) else ""
        r['coordinate'].update({'point': point})
        r['coordinate'].update({'value': r['value']})
        r['coordinate'].update({'permissions': r['permissions']})
        coordinates.append(r['coordinate'])

    mappings = (('mkt_type', 'type'),
                ('mkt_asset', 'asset'),
                ('mkt_class', 'assetClass'),
                ('mkt_point', 'point'),
                ('mkt_quoting_style', 'quotingStyle'),
                ('value', 'value'),
                ('permissions', 'permissions'))

    return __dataframe_handler(coordinates, mappings, risk_key, request_id=request_id)


def market_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                   request_id: Optional[str] = None) -> StringWithInfo:
    return StringWithInfo(risk_key, result.get('marketRef'), request_id=request_id)


def unsupported_handler(_result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                        request_id: Optional[str] = None) -> UnsupportedValue:
    return UnsupportedValue(risk_key, request_id=request_id)


result_handlers = {
    'Error': error_handler,
    'IRPCashflowTable': cashflows_handler,
    'LegDefinition': leg_definition_handler,
    'Message': message_handler,
    'MDAPITable': mdapi_table_handler,
    'NumberAndUnit': number_and_unit_handler,
    'RequireAssets': required_assets_handler,
    'Risk': risk_handler,
    'RiskByClass': risk_by_class_handler,
    'RiskVector': risk_vector_handler,
    'RiskTheta': risk_theta_handler,
    'Market': market_handler,
    'Unsupported': unsupported_handler
}
