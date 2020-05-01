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
from typing import List, Mapping, Union

from .core import DataFrameWithInfo, FloatWithInfo, SeriesWithInfo, StringWithInfo, sort_risk
from gs_quant.base import InstrumentBase, PricingKey


def __dataframe_handler(field: str, mappings: tuple, result: List, pricing_key: PricingKey) -> DataFrameWithInfo:
    components = []

    for date_key, date_result in zip(pricing_key, result):
        records = [{k: datum[v] for k, v in mappings} for datum in date_result[field]]
        df = pd.DataFrame.from_records(records)
        df = sort_risk(df, tuple(k for k, _ in mappings))
        components.append(DataFrameWithInfo(date_key, df, unit=date_result.get('unit')))

    return DataFrameWithInfo.compose(components, pricing_key) if len(pricing_key) > 1 else components[0]


def __double_handler(field: str, result: List, pricing_key: PricingKey) -> Union[FloatWithInfo, SeriesWithInfo]:
    components = [FloatWithInfo(k, r.get(field, float('nan')), r.get('unit')) for k, r in zip(pricing_key, result)]
    return FloatWithInfo.compose(components, pricing_key) if len(pricing_key) > 1 else components[0]


def __string_handler(field: str, result: List, pricing_key: PricingKey) -> Union[StringWithInfo, SeriesWithInfo]:
    components = [StringWithInfo(k, r.get(field)) for k, r in zip(pricing_key, result)]
    return StringWithInfo.compose(components, pricing_key) if len(pricing_key) > 1 else components[0]


def cashflows_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase) -> DataFrameWithInfo:
    mappings = (
        ('payment_date', 'payDate'),
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

    for r in result:
        for cashflow in r['cashflows']:
            for field in ('payDate', 'setDate', 'accStart', 'accEnd'):
                value = cashflow.get(field)
                date = dt.date.fromisoformat(value) if value else dt.date.max
                cashflow[field] = date

    return __dataframe_handler('cashflows', mappings, result, pricing_key)


def error_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Union[StringWithInfo, SeriesWithInfo]:
    components = [StringWithInfo(k, r.get('errorString')) for k, r in zip(pricing_key, result)]
    return StringWithInfo.compose(components, pricing_key) if len(pricing_key) > 1 else components[0]


def leg_definition_handler(result: List, pricing_key: PricingKey, instrument: InstrumentBase)\
        -> Union[InstrumentBase, Mapping[dt.date, InstrumentBase]]:
    instruments_by_date = {}

    for date_key, field_values in zip(pricing_key, result):
        new_instrument = instrument.from_dict(field_values)
        new_instrument.unresolved = instrument
        new_instrument.name = instrument.name
        new_instrument.resolution_key = date_key
        instruments_by_date[date_key.pricing_market_data_as_of[0].pricing_date] = new_instrument

    return instruments_by_date if len(pricing_key) > 1 else next(iter(instruments_by_date.values()))


def message_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Union[StringWithInfo, SeriesWithInfo]:
    return __string_handler('message', result, pricing_key)


def number_and_unit_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Union[FloatWithInfo, SeriesWithInfo]:
    return __double_handler('value', result, pricing_key)


def required_assets_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase):
    mappings = (('mkt_type', 'type'), ('mkt_asset', 'asset'))
    return __dataframe_handler('requiredAssets', mappings, result, pricing_key)


def risk_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Union[FloatWithInfo, SeriesWithInfo]:
    return __double_handler('val', result, pricing_key)


def risk_by_class_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Union[FloatWithInfo, SeriesWithInfo]:
    sum_result = []
    for date_result in result:
        if date_result['$type'] == 'Error':
            return error_handler(date_result)
        sum_result.append({'unit': date_result.get('unit'), 'val': sum(date_result['values'])})

    return __double_handler('val', sum_result, pricing_key)


def risk_vector_handler(result: List, pricing_key: PricingKey, _instrument: InstrumentBase)\
        -> Union[DataFrameWithInfo, StringWithInfo]:
    for date_result in result:
        if date_result['$type'] == 'Error':
            return error_handler(date_result)

        for points, value in zip(date_result['points'], date_result['asset']):
            points.update({'value': value})

    mappings = (
        ('mkt_type', 'type'),
        ('mkt_asset', 'asset'),
        ('mkt_class', 'class_'),
        ('mkt_point', 'point'),
        ('value', 'value')
    )

    return __dataframe_handler('points', mappings, result, pricing_key)


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
