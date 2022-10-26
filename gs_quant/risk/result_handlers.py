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

from gs_quant.base import InstrumentBase, RiskKey
from gs_quant.risk.measures import PnlExplain

from .core import DataFrameWithInfo, ErrorValue, UnsupportedValue, FloatWithInfo, SeriesWithInfo, StringWithInfo, \
    sort_values, MQVSValidatorDefnsWithInfo, MQVSValidatorDefn

_logger = logging.getLogger(__name__)
__scalar_risk_measures = ('EqDelta', 'EqGamma', 'EqVega')


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


def __dataframe_handler_unsorted(result: Iterable, mappings: tuple, date_cols: tuple, risk_key: RiskKey,
                                 request_id: Optional[str] = None) -> DataFrameWithInfo:
    first_row = next(iter(result), None)
    if first_row is None:
        return DataFrameWithInfo(risk_key=risk_key, request_id=request_id)

    records = ([row.get(field_from) for field_to, field_from in mappings] for row in result)
    df = DataFrameWithInfo(records, risk_key=risk_key, request_id=request_id)
    df.columns = [m[0] for m in mappings]
    for dt_col in date_cols:
        df[dt_col] = df[dt_col].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').date() if isinstance(x, str) else x)

    return df


def cashflows_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase, request_id: Optional[str] = None) \
        -> DataFrameWithInfo:
    mappings = (
        ('currency', 'currency'),
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
    date_cols = ('payment_date', 'set_date', 'accrual_start_date', 'accrual_end_date')
    return __dataframe_handler_unsorted(result['cashflows'], mappings, date_cols, risk_key, request_id=request_id)


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
        -> Union[StringWithInfo, ErrorValue]:
    message = result.get('message')
    if message is None:
        return ErrorValue(risk_key, "No result returned", request_id=request_id)
    else:
        return StringWithInfo(risk_key, message, request_id=request_id)


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
    if str(risk_key.risk_measure.name) in external_risk_by_class_val and len(types) <= 2 and len(set(types)) == 1:
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

        if isinstance(risk_key.risk_measure, PnlExplain):
            return __dataframe_handler_unsorted(classes, mappings, (), risk_key, request_id=request_id)
        else:
            return __dataframe_handler(classes, mappings, risk_key, request_id=request_id)


def risk_vector_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                        request_id: Optional[str] = None) -> DataFrameWithInfo:
    assets = result['asset']
    # Handle equity risk measures which are really scalars
    if len(assets) == 1 and risk_key.risk_measure.name in __scalar_risk_measures:
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


def fixing_table_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                         request_id: Optional[str] = None) -> SeriesWithInfo:
    rows = result['fixingTableRows']

    dates = []
    values = []
    for row in rows:
        dates.append(dt.date.fromisoformat(row["fixingDate"]))
        values.append(row["fixing"])

    return SeriesWithInfo(values, index=dates, risk_key=risk_key, request_id=request_id)


def simple_valtable_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                            request_id: Optional[str] = None) -> DataFrameWithInfo:
    raw_res = result['rows']
    # simplevaltable's values contain all the information on units which needs to be extracted into the dataframe
    df = DataFrameWithInfo([(res['label'], res['value']['val']) for res in raw_res], risk_key=risk_key,
                           request_id=request_id, unit=raw_res[0]['value'].get('unit'))
    df.columns = ['label', 'value']
    return df


def canonical_projection_table_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                                       request_id: Optional[str] = None) -> DataFrameWithInfo:
    mappings = (
        ('asset_class', 'assetClass'),
        ('asset', 'asset'),
        ('asset_family', 'assetFamily'),
        ('asset_sub_family', 'assetSubFamily'),
        ('product', 'product'),
        ('product_family', 'productFamily'),
        ('product_sub_family', 'productSubFamily'),
        ('side', 'side'),
        ('size', 'size'),
        ('size_unit', 'sizeUnit'),
        ('quote_level', 'quoteLevel'),
        ('quote_unit', 'quoteUnit'),
        ('start_date', 'startDate'),
        ('end_date', 'endDate'),
        ('expiration_date', 'expiryDate'),
        ('strike', 'strike'),
        ('strike_unit', 'strikeUnit'),
        ('option_type', 'optionType'),
        ('option_style', 'optionStyle'),
        ('tenor', 'tenor'),
        ('tenor_unit', 'tenorUnit'),
        ('premium_currency', 'premiumCcy'),
        ('currency', 'currency')
    )
    date_cols = ('start_date', 'end_date', 'expiration_date')
    return __dataframe_handler_unsorted(result['rows'], mappings, date_cols, risk_key, request_id)


def risk_float_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                       request_id: Optional[str] = None) -> FloatWithInfo:
    return FloatWithInfo(risk_key, result['values'][0], request_id=request_id)


def mdapi_table_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                        request_id: Optional[str] = None) -> DataFrameWithInfo:
    coordinates = []
    for r in result['rows']:
        raw_point = r['coordinate'].get('point', '')
        point = ';'.join(raw_point) if isinstance(raw_point, list) else raw_point
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


def mmapi_table_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                        request_id: Optional[str] = None) -> DataFrameWithInfo:
    coordinates = []
    for r in result['rows']:
        raw_point = r['modelCoordinate'].get('point', '')
        point = ';'.join(raw_point) if isinstance(raw_point, list) else raw_point
        r['modelCoordinate'].update({'point': point})
        raw_tags = r['modelCoordinate'].get('tags', '')
        tags = ';'.join(raw_tags) if isinstance(raw_tags, list) else raw_tags
        r['modelCoordinate'].update({'tags': tags})
        rows = r['value'].get('value', '')
        DataPoints = []
        for row in rows:
            DataPoints.append([dt.date.fromisoformat(row["date"]), row["value"]])
        r['modelCoordinate'].update({'value': DataPoints})
        coordinates.append(r['modelCoordinate'])

    mappings = (('mkt_type', 'type'),
                ('mkt_asset', 'asset'),
                ('mkt_point', 'point'),
                ('mkt_tags', 'tags'),
                ('mkt_quoting_style', 'quotingStyle'),
                ('value', 'value'))

    return __dataframe_handler(coordinates, mappings, risk_key, request_id=request_id)


def mqvs_validators_handler(result: dict, risk_key: RiskKey, _instrument: InstrumentBase,
                            request_id: Optional[str] = None) -> MQVSValidatorDefnsWithInfo:
    validators = [MQVSValidatorDefn.from_dict(r) for r in result['validators']]
    return MQVSValidatorDefnsWithInfo(risk_key, tuple(validators), request_id=request_id)


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
    'MMAPITable': mmapi_table_handler,
    'MQVSValidators': mqvs_validators_handler,
    'NumberAndUnit': number_and_unit_handler,
    'RequireAssets': required_assets_handler,
    'Risk': risk_handler,
    'RiskByClass': risk_by_class_handler,
    'RiskVector': risk_vector_handler,
    'FixingTable': fixing_table_handler,
    'Table': simple_valtable_handler,
    'CanonicalProjectionTable': canonical_projection_table_handler,
    'RiskSecondOrderVector': risk_float_handler,
    'RiskTheta': risk_float_handler,
    'Market': market_handler,
    'Unsupported': unsupported_handler
}
