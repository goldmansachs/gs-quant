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
from typing import Union

from .core import DataFrameWithInfo, ErrorValue, FloatWithInfo, StringWithInfo, sort_risk
from gs_quant.base import InstrumentBase, RiskKey


_logger = logging.getLogger(__name__)


def __dataframe_handler(field: str, mappings: tuple, result: dict, risk_key: RiskKey) -> DataFrameWithInfo:
    records = [{k: datum[v] for k, v in mappings} for datum in result[field]]
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
            date = dt.date.fromisoformat(value) if value else dt.date.max
            cashflow[field] = date

    return __dataframe_handler('cashflows', mappings, result, risk_key)


def error_handler(result: dict, risk_key: RiskKey, instrument: InstrumentBase) -> ErrorValue:
    error = result.get('errorString', 'Unknown error')
    _logger.error(f'Error while computing {risk_key.risk_measure} on {instrument} for {risk_key.date}: {error}')
    return ErrorValue(risk_key, error)


def leg_definition_handler(result: dict, risk_key: RiskKey, instrument: InstrumentBase) -> InstrumentBase:
    new_instrument = instrument.from_dict(result)
    new_instrument.unresolved = instrument
    new_instrument.name = instrument.name
    new_instrument.resolution_key = risk_key
    return new_instrument


def message_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> StringWithInfo:
    return StringWithInfo(risk_key, result.get('message'))


def number_and_unit_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result.get('value', float('nan')), unit=result.get('unit'))


def required_assets_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase):
    mappings = (('mkt_type', 'type'), ('mkt_asset', 'asset'))
    return __dataframe_handler('requiredAssets', mappings, result, risk_key)


def risk_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result.get('val', float('nan')), unit=result.get('unit'))


def risk_by_class_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase)\
        -> Union[DataFrameWithInfo, FloatWithInfo]:
    # TODO Remove this once we migrate parallel USD IRDelta measures
    types = [c['type'] for c in result['classes']]
    if len(types) <= 2 and all(t == 'IR' for t in types):
        return FloatWithInfo(risk_key, sum(result.get('values', (float('nan'),))), unit=result.get('unit'))
    else:
        for clazz, value in zip(result['classes'], result['values']):
            mkt_type = clazz['type']
            if 'SPIKE' in mkt_type or 'JUMP' in mkt_type:
                clazz['type'] = 'OTHER'

            clazz.update({'value': value})

        mappings = (
            ('mkt_type', 'type'),
            ('mkt_asset', 'asset'),
            ('value', 'value')
        )

        return __dataframe_handler('classes', mappings, result, risk_key)


def risk_vector_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase) -> DataFrameWithInfo:
    for points, value in zip(result['points'], result['asset']):
        points.update({'value': value})

    mappings = (
        ('mkt_type', 'type'),
        ('mkt_asset', 'asset'),
        ('mkt_class', 'class_'),
        ('mkt_point', 'point'),
        ('value', 'value')
    )

    return __dataframe_handler('points', mappings, result, risk_key)


result_handlers = {
    'Error': error_handler,
    'IRPCashflowTable': cashflows_handler,
    'LegDefinition': leg_definition_handler,
    'Message': message_handler,
    'NumberAndUnit': number_and_unit_handler,
    'RequireAssets': required_assets_handler,
    'Risk': risk_handler,
    'RiskByClass': risk_by_class_handler,
    'RiskVector': risk_vector_handler
}
