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
from dataclasses import dataclass, field
from typing import Optional, Union, Tuple

from dataclasses_json import dataclass_json, LetterCase, config

from gs_quant.api.gs.backtests_xasset.json_encoders.request_encoders import legs_encoder, legs_decoder, enum_decode
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import (
    DateConfig,
    Trade,
    Configuration,
    TransactionCostConfig,
    StrategyHedge,
    RiskRequestParameters,
    RiskProviderEnum,
)
from gs_quant.api.gs.backtests_xasset.response_datatypes.generic_backtest_datatypes import decode_strategy
from gs_quant.base import exclude_none
from gs_quant.common import RiskMeasure
from gs_quant.json_convertors import (
    decode_timedelta,
    encode_timedelta,
    decode_optional_date_or_time,
    decode_date_or_time_tuple,
    encode_date_or_time_tuple,
)
from gs_quant.json_convertors_common import encode_risk_measure_tuple, decode_risk_measure_tuple
from gs_quant.priceable import PriceableImpl
from gs_quant.target.backtests import FlowVolBacktestMeasure


def _decode_dates(data):
    """Decode dates as either a DateConfig dict or a tuple of date strings."""
    if data is None:
        return None
    if isinstance(data, DateConfig):
        return data
    if isinstance(data, dict):
        return DateConfig.from_dict(data)
    if isinstance(data, (list, tuple)):
        return tuple(dt.date.fromisoformat(d) if isinstance(d, str) else d for d in data)
    return data


def _decode_configuration(data):
    """Decode configuration from a camelCase dict into a Configuration object."""
    if data is None:
        return None
    if isinstance(data, Configuration):
        return data
    if isinstance(data, dict):
        return Configuration.from_dict(data)
    return data


def _decode_measures(data):
    """Decode measures as an optional tuple of RiskMeasure objects."""
    if data is None:
        return None
    return decode_risk_measure_tuple(data)


def _encode_measures(data):
    """Encode measures, handling None for optional field."""
    if data is None:
        return None
    return encode_risk_measure_tuple(data)


def _decode_pnl_attribute(data):
    """Decode a single PnlAttribute from a dict, handling nested RiskMeasure fields."""

    from gs_quant.backtests.backtest_objects import PnlAttribute
    from gs_quant.json_convertors_common import decode_risk_measure

    if isinstance(data, PnlAttribute):
        return data
    if isinstance(data, dict):
        attr_metric = data.get('attribute_metric')
        mkt_metric = data.get('market_data_metric')
        return PnlAttribute(
            attribute_name=data['attribute_name'],
            attribute_metric=decode_risk_measure(attr_metric) if isinstance(attr_metric, dict) else attr_metric,
            market_data_metric=decode_risk_measure(mkt_metric) if isinstance(mkt_metric, dict) else mkt_metric,
            scaling_factor=data['scaling_factor'],
            second_order=data.get('second_order', False),
        )
    return data


def _decode_pnl_definition(data):
    """Decode pnl_explain_def from a dict into a PnlDefinition object."""
    if data is None:
        return None
    from gs_quant.backtests.backtest_objects import PnlDefinition

    if isinstance(data, PnlDefinition):
        return data
    if isinstance(data, dict):
        attrs = data.get('attributes', [])
        decoded_attrs = [_decode_pnl_attribute(a) for a in attrs]
        return PnlDefinition(attributes=decoded_attrs)
    return data


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskRequest:
    start_date: Optional[Union[dt.date, dt.datetime]] = field(
        default=None, metadata=config(decoder=decode_optional_date_or_time, exclude=exclude_none)
    )
    end_date: Optional[Union[dt.date, dt.datetime]] = field(
        default=None, metadata=config(decoder=decode_optional_date_or_time, exclude=exclude_none)
    )
    frequency: Optional[Union[str, dt.timedelta]] = field(
        default=None, metadata=config(encoder=encode_timedelta, decoder=decode_timedelta, exclude=exclude_none)
    )
    additional_dates: Optional[Tuple[Union[dt.date, dt.datetime], ...]] = field(
        default=None,
        metadata=config(encoder=encode_date_or_time_tuple, decoder=decode_date_or_time_tuple, exclude=exclude_none),
    )
    legs: Optional[Tuple[PriceableImpl, ...]] = field(
        default=None, metadata=config(encoder=legs_encoder, decoder=legs_decoder, exclude=exclude_none)
    )
    measures: Optional[Tuple[RiskMeasure, ...]] = field(
        default=None,
        metadata=config(encoder=encode_risk_measure_tuple, decoder=decode_risk_measure_tuple, exclude=exclude_none),
    )
    risk_provider: Optional[RiskProviderEnum] = field(
        default=None, metadata=config(decoder=enum_decode(RiskProviderEnum), exclude=exclude_none)
    )
    parameters: Optional[RiskRequestParameters] = field(default=None, metadata=config(exclude=exclude_none))
    something_new: str = field(default=None, metadata=config(exclude=exclude_none))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasicBacktestRequest:
    dates: DateConfig
    trades: Tuple[Trade, ...]
    measures: Tuple[FlowVolBacktestMeasure, ...]
    delta_hedge_frequency: Optional[str] = field(default=None, metadata=config(exclude=exclude_none))
    transaction_costs: Optional[TransactionCostConfig] = field(default=None, metadata=config(exclude=exclude_none))
    configuration: Optional[Configuration] = field(default=None, metadata=config(exclude=exclude_none))
    hedge: Optional[StrategyHedge] = field(default=None, metadata=config(exclude=exclude_none))
    risk_provider: Optional[RiskProviderEnum] = field(
        default=None, metadata=config(decoder=enum_decode(RiskProviderEnum), exclude=exclude_none)
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GenericBacktestRequest:
    strategy: object = field(default=None, metadata=config(decoder=decode_strategy, exclude=exclude_none))
    dates: Union[DateConfig, Tuple[dt.date, ...]] = field(
        default=None, metadata=config(decoder=_decode_dates, exclude=exclude_none)
    )
    configuration: Optional[Configuration] = field(
        default=None, metadata=config(decoder=_decode_configuration, exclude=exclude_none)
    )
    measures: Optional[Tuple[RiskMeasure, ...]] = field(
        default=None, metadata=config(encoder=_encode_measures, decoder=_decode_measures, exclude=exclude_none)
    )
    pnl_explain_def: Optional[object] = field(
        default=None, metadata=config(decoder=_decode_pnl_definition, exclude=exclude_none)
    )
