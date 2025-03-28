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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ByAssetPnlResult(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    bbid: Optional[str] = field(default=None, metadata=field_metadata)
    sector: Optional[str] = field(default=None, metadata=field_metadata)
    industry: Optional[str] = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    direction: Optional[str] = field(default=None, metadata=field_metadata)
    exposure: Optional[float] = field(default=None, metadata=field_metadata)
    estimated_pnl: Optional[float] = field(default=None, metadata=field_metadata)
    estimated_performance: Optional[float] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ErroredScenario(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    error_message: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SummaryResult(Base):
    estimated_pnl: float = field(default=None, metadata=field_metadata)
    estimated_performance: Optional[float] = field(default=None, metadata=field_metadata)
    stressed_market_value: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PnlResult(Base):
    name: str = field(default=None, metadata=field_metadata)
    estimated_pnl: float = field(default=None, metadata=field_metadata)
    factor_exposure: Optional[float] = field(default=None, metadata=field_metadata)
    exposure: Optional[float] = field(default=None, metadata=field_metadata)
    factor_shock: Optional[float] = field(default=None, metadata=field_metadata)
    by_asset: Optional[ByAssetPnlResult] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScenarioResponse(Base):
    summary: Optional[SummaryResult] = field(default=None, metadata=field_metadata)
    factor_pnl: Optional[PnlResult] = field(default=None, metadata=field_metadata)
    by_sector_aggregations: Optional[PnlResult] = field(default=None, metadata=field_metadata)
    by_region_aggregations: Optional[PnlResult] = field(default=None, metadata=field_metadata)
    by_direction_aggregations: Optional[PnlResult] = field(default=None, metadata=field_metadata)
    by_asset: Optional[ByAssetPnlResult] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScenarioCalculationResponse(Base):
    scenarios: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    errored_scenarios: Optional[Tuple[ErroredScenario, ...]] = field(default=None, metadata=field_metadata)
    results: Optional[Tuple[ScenarioResponse, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScenarioCalculationAPIRequest(Base):
    scenario_ids: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    measures: tuple = field(default=None, metadata=field_metadata)
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    risk_model: Optional[str] = field(default=None, metadata=field_metadata)
    entity_id: Optional[str] = field(default=None, metadata=field_metadata)
    position_set: Optional[PositionSetRequest] = field(default=None, metadata=field_metadata)
    report_id: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(init=False, default='Factor Scenario', metadata=config(field_name='type', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)
