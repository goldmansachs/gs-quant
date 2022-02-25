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


class PositionSourceType(EnumBase, Enum):    
    
    """Source object for position data"""

    Portfolio = 'Portfolio'
    Asset = 'Asset'
    Backtest = 'Backtest'
    RiskRequest = 'RiskRequest'
    Hedge = 'Hedge'    


class ReportGenerateTemplateId(EnumBase, Enum):    
    
    """The Report Template ID to generate the report from."""

    analytics_factor_attribution_pdf = 'analytics-factor-attribution-pdf'
    analytics_factor_risk_pdf = 'analytics-factor-risk-pdf'    


class ReportMeasures(EnumBase, Enum):    
    
    """Enums for measures to be outputted for the report"""

    _ = ''
    pnl = 'pnl'
    longExposure = 'longExposure'
    shortExposure = 'shortExposure'
    assetCount = 'assetCount'
    turnover = 'turnover'
    assetCountLong = 'assetCountLong'
    assetCountShort = 'assetCountShort'
    netExposure = 'netExposure'
    grossExposure = 'grossExposure'
    tradingPnl = 'tradingPnl'
    tradingCostPnl = 'tradingCostPnl'
    servicingCostLongPnl = 'servicingCostLongPnl'
    servicingCostShortPnl = 'servicingCostShortPnl'
    exposure = 'exposure'
    sensitivity = 'sensitivity'
    mctr = 'mctr'
    annualizedMCTRisk = 'annualizedMCTRisk'
    annualizedRMCTRisk = 'annualizedRMCTRisk'
    poRisk = 'poRisk'
    price = 'price'
    basePrice = 'basePrice'    


class ReportStatus(EnumBase, Enum):    
    
    """Status of report run"""

    new = 'new'
    ready = 'ready'
    executing = 'executing'
    calculating = 'calculating'
    done = 'done'
    error = 'error'
    cancelled = 'cancelled'
    waiting = 'waiting'    


class ReportType(EnumBase, Enum):    
    
    """Type of report to execute"""

    Portfolio_Performance_Analytics = 'Portfolio Performance Analytics'
    Portfolio_Factor_Risk = 'Portfolio Factor Risk'
    Portfolio_Aging = 'Portfolio Aging'
    Portfolio_Thematic_Analytics = 'Portfolio Thematic Analytics'
    Asset_Factor_Risk = 'Asset Factor Risk'
    Asset_Thematic_Analytics = 'Asset Thematic Analytics'
    Basket_Create = 'Basket Create'
    Basket_Backcast = 'Basket Backcast'
    Basket_Rebalance_Auto_Approval = 'Basket Rebalance Auto Approval'
    Scenario = 'Scenario'
    Iselect_Backtest = 'Iselect Backtest'
    Backtest_Run = 'Backtest Run'
    Analytics = 'Analytics'
    Risk_Calculation = 'Risk Calculation'
    PCO = 'PCO'    


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Report(Base):
    position_source_id: str = None
    position_source_type: PositionSourceType = None
    type_: ReportType = field(default=None, metadata=config(field_name='type'))
    parameters: ReportParameters = None
    calculation_time: Optional[float] = None
    data_set_id: Optional[str] = None
    asset_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    entitlements: Optional[Entitlements] = None
    earliest_start_date: Optional[datetime.date] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    measures: Optional[Tuple[ReportMeasures, ...]] = None
    name: Optional[str] = None
    owner_id: Optional[str] = None
    status: Optional[ReportStatus] = None
    latest_execution_time: Optional[datetime.datetime] = None
    latest_end_date: Optional[datetime.date] = None
    percentage_complete: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ParametersOverrides(Base):
    csa_term: Optional[str] = None
    pricing_location: Optional[PricingLocation] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportGenerateRequest(Base):
    end_date: Optional[datetime.date] = None
    report_id: Optional[str] = None
    start_date: Optional[datetime.date] = None
    template_id: Optional[ReportGenerateTemplateId] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportRescheduleRequest(Base):
    report_ids: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportWithParametersOverrides(Base):
    report_id: Optional[str] = None
    parameters: Optional[ParametersOverrides] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportToggleEntityRequest(Base):
    type_: Optional[str] = field(default=None, metadata=config(field_name='type'))
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    user: Optional[User] = None
    is_delete: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportBatchScheduleRequest(Base):
    reports: Optional[Tuple[str, ...]] = None
    reports_with_parameters_overrides: Optional[Tuple[ReportWithParametersOverrides, ...]] = None
    time: Optional[datetime.datetime] = None
    end_date: Optional[datetime.date] = None
    use_close_date: Optional[datetime.date] = None
    start_date: Optional[datetime.date] = None
    parameters: Optional[ReportParameters] = None
    priority: Optional[ReportJobPriority] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportJob(Base):
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    time: Optional[datetime.datetime] = None
    use_close_date: Optional[datetime.date] = None
    elapsed_time: Optional[float] = None
    percentage_complete: Optional[float] = None
    execution_time: Optional[datetime.datetime] = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    measures: Optional[Tuple[ReportMeasures, ...]] = None
    parameters: Optional[ReportParameters] = None
    parent_id: Optional[str] = None
    position_source_id: Optional[str] = None
    position_source_type: Optional[PositionSourceType] = None
    report_id: Optional[str] = None
    report_type: Optional[ReportType] = None
    status: Optional[ReportStatus] = None
    owner_id: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    report_ids: Optional[Tuple[str, ...]] = None
    priority: Optional[ReportJobPriority] = None
