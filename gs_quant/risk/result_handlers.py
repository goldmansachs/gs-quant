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
import pandas as pd
from typing import Iterable, Union

from .core import DataFrameWithInfo, ErrorValue, FloatWithInfo, StringWithInfo, sort_risk
from .measures import EqDelta, EqGamma, EqVega
from gs_quant.base import InstrumentBase, RiskKey

_logger = logging.getLogger(__name__)
__scalar_risk_measures = (EqDelta, EqGamma, EqVega)


def __dataframe_handler(result: Iterable, mappings: tuple, risk_key: RiskKey) -> DataFrameWithInfo:
    records = [{k: datum.get(v, (None if v == 'value' else '')) for k, v in mappings} for datum in result]
    df = pd.DataFrame.from_records(records)
    return DataFrameWithInfo(sort_risk(df, tuple(k for k, _ in mappings)), risk_key=risk_key)


def cashflows_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> DataFrameWithInfo:
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

    return __dataframe_handler(result['cashflows'], mappings, risk_key)


def error_handler(result: dict, risk_key: RiskKey, instrument: InstrumentBase) -> ErrorValue:
    error = result.get('errorString', 'Unknown error')
    _logger.error(f'Error while computing {risk_key.risk_measure} on {instrument} for {risk_key.date}: {error}')
    return ErrorValue(risk_key, error)


def leg_definition_handler(result: dict, risk_key: RiskKey, instrument: InstrumentBase) -> InstrumentBase:
    return instrument.resolved(result, risk_key)


def message_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> StringWithInfo:
    return StringWithInfo(risk_key, result.get('message'))


def number_and_unit_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result.get('value', float('nan')), unit=result.get('unit'))


def required_assets_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase):
    mappings = (('mkt_type', 'type'), ('mkt_asset', 'asset'))
    return __dataframe_handler(result['requiredAssets'], mappings, risk_key)


def risk_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result.get('val', float('nan')), unit=result.get('unit'))


def risk_by_class_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) \
        -> Union[DataFrameWithInfo, FloatWithInfo]:
    # TODO Remove this once we migrate parallel USD IRDelta measures
    types = [c['type'] for c in result['classes']]
    if len(types) <= 2 and len(set(types)) == 1:
        return FloatWithInfo(risk_key, sum(result.get('values', (float('nan'),))), unit=result.get('unit'))
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

        return __dataframe_handler(classes, mappings, risk_key)


def risk_vector_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> DataFrameWithInfo:
    assets = result['asset']
    # Handle equity risk measures which are really scalars
    if len(assets) == 1 and risk_key.risk_measure in __scalar_risk_measures:
        return FloatWithInfo(risk_key, assets[0])

    for points, value in zip(result['points'], assets):
        points.update({'value': value})

    mappings = (
        ('mkt_type', 'type'),
        ('mkt_asset', 'asset'),
        ('mkt_class', 'class_'),
        ('mkt_point', 'point'),
        ('value', 'value')
    )

    return __dataframe_handler(result['points'], mappings, risk_key)


def unsupported_handler(_result: dict, risk_key: RiskKey, instrument: InstrumentBase) -> ErrorValue:
    return ErrorValue(risk_key, f'{risk_key.risk_measure} not supported for {type(instrument).__name__}')


result_handlers = {
    'Error': error_handler,
    'IRPCashflowTable': cashflows_handler,
    'LegDefinition': leg_definition_handler,
    'Message': message_handler,
    'NumberAndUnit': number_and_unit_handler,
    'RequireAssets': required_assets_handler,
    'Risk': risk_handler,
    'RiskByClass': risk_by_class_handler,
    'RiskVector': risk_vector_handler,
    'Unsupported': unsupported_handler
}
