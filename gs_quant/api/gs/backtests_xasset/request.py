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

from gs_quant.api.gs.backtests_xasset.json_encoders.request_encoders import legs_encoder, legs_decoder
from gs_quant.api.gs.backtests_xasset.response_datatypes.backtest_datatypes import DateConfig, Trade, Configuration, \
    TransactionCostConfig
from gs_quant.api.gs.backtests_xasset.response_datatypes.generic_backtest_datatypes import Strategy
from gs_quant.common import RiskMeasure
from gs_quant.json_convertors import decode_optional_date, decode_date_tuple, encode_date_tuple
from gs_quant.json_convertors_common import encode_risk_measure_tuple, decode_risk_measure_tuple
from gs_quant.priceable import PriceableImpl
from gs_quant.target.backtests import FlowVolBacktestMeasure


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskRequest:
    start_date: Optional[dt.date] = field(default=None, metadata=config(decoder=decode_optional_date))
    end_date: Optional[dt.date] = field(default=None, metadata=config(decoder=decode_optional_date))
    additional_dates: Optional[Tuple[dt.date, ...]] = field(default=None, metadata=config(encoder=encode_date_tuple,
                                                                                          decoder=decode_date_tuple))
    legs: Optional[Tuple[PriceableImpl, ...]] = field(default=None, metadata=config(encoder=legs_encoder,
                                                                                    decoder=legs_decoder))
    measures: Optional[Tuple[RiskMeasure, ...]] = field(default=None,
                                                        metadata=config(encoder=encode_risk_measure_tuple,
                                                                        decoder=decode_risk_measure_tuple))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BasicBacktestRequest:
    dates: DateConfig
    trades: Tuple[Trade, ...]
    measures: Tuple[FlowVolBacktestMeasure, ...]
    delta_hedge_frequency: Optional[str] = None
    transaction_costs: Optional[TransactionCostConfig] = None
    configuration: Optional[Configuration] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GenericBacktestRequest:
    strategy: Strategy
    dates: Union[DateConfig, Tuple[dt.date, ...]]
    configuration: Optional[Configuration] = None
