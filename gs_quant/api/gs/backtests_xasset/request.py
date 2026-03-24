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
from enum import Enum
from typing import Optional, Union, Tuple

from dataclasses_json import dataclass_json, LetterCase, config

from gs_quant.api.gs.backtests_xasset.json_encoders.request_encoders import legs_encoder, legs_decoder, enum_decode
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import (
    DateConfig,
    Trade,
    Configuration,
    TransactionCostConfig,
    StrategyHedge,
)
from gs_quant.api.gs.backtests_xasset.response_datatypes.generic_backtest_datatypes import decode_strategy
from gs_quant.base import EnumBase
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


class RiskProviderEnum(EnumBase, Enum):
    Default = "Default"
    DataSetProvider = "DataSetProvider"
    EqVolRiskProvider = "EqVolRiskProvider"


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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskRequest:
    start_date: Optional[Union[dt.date, dt.datetime]] = field(
        default=None, metadata=config(decoder=decode_optional_date_or_time)
    )
    end_date: Optional[Union[dt.date, dt.datetime]] = field(
        default=None, metadata=config(decoder=decode_optional_date_or_time)
    )
    frequency: Optional[Union[str, dt.timedelta]] = field(
        default=None, metadata=config(encoder=encode_timedelta, decoder=decode_timedelta)
    )
    additional_dates: Optional[Tuple[Union[dt.date, dt.datetime], ...]] = field(
        default=None, metadata=config(encoder=encode_date_or_time_tuple, decoder=decode_date_or_time_tuple)
    )
    legs: Optional[Tuple[PriceableImpl, ...]] = field(
        default=None, metadata=config(encoder=legs_encoder, decoder=legs_decoder)
    )
    measures: Optional[Tuple[RiskMeasure, ...]] = field(
        default=None, metadata=config(encoder=encode_risk_measure_tuple, decoder=decode_risk_measure_tuple)
    )
    risk_provider: Optional[RiskProviderEnum] = field(
        default=None, metadata=config(decoder=enum_decode(RiskProviderEnum))
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasicBacktestRequest:
    dates: DateConfig
    trades: Tuple[Trade, ...]
    measures: Tuple[FlowVolBacktestMeasure, ...]
    delta_hedge_frequency: Optional[str] = None
    transaction_costs: Optional[TransactionCostConfig] = None
    configuration: Optional[Configuration] = None
    hedge: Optional[StrategyHedge] = None
    risk_provider: Optional[RiskProviderEnum] = field(
        default=None, metadata=config(decoder=enum_decode(RiskProviderEnum))
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GenericBacktestRequest:
    strategy: object = field(default=None, metadata=config(decoder=decode_strategy))
    dates: Union[DateConfig, Tuple[dt.date, ...]] = field(default=None, metadata=config(decoder=_decode_dates))
    configuration: Optional[Configuration] = field(default=None, metadata=config(decoder=_decode_configuration))
