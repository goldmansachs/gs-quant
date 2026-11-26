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
from enum import Enum


class ReportGenerateTemplateId(EnumBase, Enum):    
    
    """The Report Template ID to generate the report from."""

    analytics_factor_attribution_pdf = 'analytics-factor-attribution-pdf'
    analytics_factor_risk_pdf = 'analytics-factor-risk-pdf'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AumTimeseriesDataPoint(Base):
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    aum: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AumTimeseries(Base):
    data: Optional[tuple[AumTimeseriesDataPoint, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ParametersOverrides(Base):
    csa_term: Optional[str] = field(default=None, metadata=field_metadata)
    pricing_location: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportGenerateRequest(Base):
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    report_id: Optional[str] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    template_id: Optional[ReportGenerateTemplateId] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportRescheduleRequest(Base):
    report_ids: Optional[tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportWithParametersOverrides(Base):
    report_id: Optional[str] = field(default=None, metadata=field_metadata)
    parameters: Optional[ParametersOverrides] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportToggleEntityRequest(Base):
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    user: Optional[User] = field(default=None, metadata=field_metadata)
    is_delete: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportBatchScheduleRequest(Base):
    reports: Optional[tuple[str, ...]] = field(default=None, metadata=field_metadata)
    reports_with_parameters_overrides: Optional[tuple[ReportWithParametersOverrides, ...]] = field(default=None, metadata=field_metadata)
    time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    use_close_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    parameters: Optional[ReportParameters] = field(default=None, metadata=field_metadata)
    priority: Optional[ReportJobPriority] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportJob(Base):
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    use_close_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    elapsed_time: Optional[float] = field(default=None, metadata=field_metadata)
    percentage_complete: Optional[float] = field(default=None, metadata=field_metadata)
    execution_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    measures: Optional[tuple[ReportMeasures, ...]] = field(default=None, metadata=field_metadata)
    parameters: Optional[ReportParameters] = field(default=None, metadata=field_metadata)
    parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    position_source_id: Optional[str] = field(default=None, metadata=field_metadata)
    position_source_type: Optional[PositionSourceType] = field(default=None, metadata=field_metadata)
    report_id: Optional[str] = field(default=None, metadata=field_metadata)
    report_type: Optional[ReportType] = field(default=None, metadata=field_metadata)
    status: Optional[ReportStatus] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    report_ids: Optional[tuple[str, ...]] = field(default=None, metadata=field_metadata)
    priority: Optional[ReportJobPriority] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
