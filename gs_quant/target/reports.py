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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


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
    mctRisk = 'mctRisk'
    rmctRisk = 'rmctRisk'
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
    Basket_Create = 'Basket Create'
    Basket_Backcast = 'Basket Backcast'
    Basket_Rebalance_Auto_Approval = 'Basket Rebalance Auto Approval'
    Scenario = 'Scenario'
    Iselect_Backtest = 'Iselect Backtest'
    Backtest_Run = 'Backtest Run'
    Analytics = 'Analytics'
    Risk_Calculation = 'Risk Calculation'
    PCO = 'PCO'    


class ParametersOverrides(Base):
        
    """Overriding parameters specific to the report type"""

    @camel_case_translate
    def __init__(
        self,
        csa_term: str = None,
        name: str = None
    ):        
        super().__init__()
        self.csa_term = csa_term
        self.name = name

    @property
    def csa_term(self) -> str:
        """The CSA Term for CSA specific discounting, e.g. EUR-1"""
        return self.__csa_term

    @csa_term.setter
    def csa_term(self, value: str):
        self._property_changed('csa_term')
        self.__csa_term = value        


class Report(Base):
        
    @camel_case_translate
    def __init__(
        self,
        position_source_id: str,
        position_source_type: Union[PositionSourceType, str],
        type_: Union[ReportType, str],
        parameters: ReportParameters,
        calculation_time: float = None,
        data_set_id: str = None,
        asset_id: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        id_: str = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        measures: Tuple[Union[ReportMeasures, str], ...] = None,
        name: str = None,
        owner_id: str = None,
        status: Union[ReportStatus, str] = None,
        latest_execution_time: datetime.datetime = None,
        latest_end_date: datetime.date = None,
        percentage_complete: float = None
    ):        
        super().__init__()
        self.calculation_time = calculation_time
        self.data_set_id = data_set_id
        self.asset_id = asset_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.__id = id_
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.measures = measures
        self.name = name
        self.owner_id = owner_id
        self.parameters = parameters
        self.position_source_id = position_source_id
        self.position_source_type = position_source_type
        self.__type = get_enum_value(ReportType, type_)
        self.status = status
        self.latest_execution_time = latest_execution_time
        self.latest_end_date = latest_end_date
        self.percentage_complete = percentage_complete

    @property
    def calculation_time(self) -> float:
        """The calculation time between request to and response from Boltweb"""
        return self.__calculation_time

    @calculation_time.setter
    def calculation_time(self, value: float):
        self._property_changed('calculation_time')
        self.__calculation_time = value        

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def created_by_id(self) -> str:
        """Marquee unique identifier"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Marquee unique identifier"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def measures(self) -> Tuple[Union[ReportMeasures, str], ...]:
        """measures to be outputted for the report"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[ReportMeasures, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def name(self) -> str:
        """Report name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def parameters(self) -> ReportParameters:
        """Parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def position_source_id(self) -> str:
        """Marquee unique identifier"""
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: str):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def position_source_type(self) -> Union[PositionSourceType, str]:
        """Source object for position data"""
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: Union[PositionSourceType, str]):
        self._property_changed('position_source_type')
        self.__position_source_type = get_enum_value(PositionSourceType, value)        

    @property
    def type(self) -> Union[ReportType, str]:
        """Type of report to execute"""
        return self.__type

    @type.setter
    def type(self, value: Union[ReportType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ReportType, value)        

    @property
    def status(self) -> Union[ReportStatus, str]:
        """Status of report run"""
        return self.__status

    @status.setter
    def status(self, value: Union[ReportStatus, str]):
        self._property_changed('status')
        self.__status = get_enum_value(ReportStatus, value)        

    @property
    def latest_execution_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__latest_execution_time

    @latest_execution_time.setter
    def latest_execution_time(self, value: datetime.datetime):
        self._property_changed('latest_execution_time')
        self.__latest_execution_time = value        

    @property
    def latest_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__latest_end_date

    @latest_end_date.setter
    def latest_end_date(self, value: datetime.date):
        self._property_changed('latest_end_date')
        self.__latest_end_date = value        

    @property
    def percentage_complete(self) -> float:
        """Percentage that the report has been completed so far"""
        return self.__percentage_complete

    @percentage_complete.setter
    def percentage_complete(self, value: float):
        self._property_changed('percentage_complete')
        self.__percentage_complete = value        


class ReportGenerateRequest(Base):
        
    """Request body to synchronously generate a report file."""

    @camel_case_translate
    def __init__(
        self,
        end_date: datetime.date = None,
        report_id: str = None,
        start_date: datetime.date = None,
        template_id: Union[ReportGenerateTemplateId, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.end_date = end_date
        self.report_id = report_id
        self.start_date = start_date
        self.template_id = template_id
        self.name = name

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def report_id(self) -> str:
        """Report ID to generate the report file for."""
        return self.__report_id

    @report_id.setter
    def report_id(self, value: str):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def template_id(self) -> Union[ReportGenerateTemplateId, str]:
        """The Report Template ID to generate the report from."""
        return self.__template_id

    @template_id.setter
    def template_id(self, value: Union[ReportGenerateTemplateId, str]):
        self._property_changed('template_id')
        self.__template_id = get_enum_value(ReportGenerateTemplateId, value)        


class ReportRescheduleRequest(Base):
        
    """Parameters in order to re-schedule a report"""

    @camel_case_translate
    def __init__(
        self,
        report_ids: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.report_ids = report_ids
        self.name = name

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self._property_changed('report_ids')
        self.__report_ids = value        


class ReportWithParametersOverrides(Base):
        
    """Reports with their parameters to be overridden"""

    @camel_case_translate
    def __init__(
        self,
        report_id: str = None,
        parameters: ParametersOverrides = None,
        name: str = None
    ):        
        super().__init__()
        self.report_id = report_id
        self.parameters = parameters
        self.name = name

    @property
    def report_id(self) -> str:
        """Marquee unique identifier"""
        return self.__report_id

    @report_id.setter
    def report_id(self, value: str):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def parameters(self) -> ParametersOverrides:
        """Overriding parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ParametersOverrides):
        self._property_changed('parameters')
        self.__parameters = value        


class ReportToggleEntityRequest(Base):
        
    """Toggle entity"""

    @camel_case_translate
    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        user: User = None,
        is_delete: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.__id = id_
        self.user = user
        self.is_delete = is_delete
        self.name = name

    @property
    def type(self) -> str:
        """type"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def user(self) -> User:
        return self.__user

    @user.setter
    def user(self, value: User):
        self._property_changed('user')
        self.__user = value        

    @property
    def is_delete(self) -> bool:
        return self.__is_delete

    @is_delete.setter
    def is_delete(self, value: bool):
        self._property_changed('is_delete')
        self.__is_delete = value        


class ReportBatchScheduleRequest(Base):
        
    """Parameters in order to schedule a batch of reports"""

    @camel_case_translate
    def __init__(
        self,
        reports: Tuple[str, ...] = None,
        reports_with_parameters_overrides: Tuple[ReportWithParametersOverrides, ...] = None,
        end_date: datetime.date = None,
        start_date: datetime.date = None,
        parameters: ReportParameters = None,
        priority: Union[ReportJobPriority, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.reports = reports
        self.reports_with_parameters_overrides = reports_with_parameters_overrides
        self.end_date = end_date
        self.start_date = start_date
        self.parameters = parameters
        self.priority = priority
        self.name = name

    @property
    def reports(self) -> Tuple[str, ...]:
        """Marquee unique identifier"""
        return self.__reports

    @reports.setter
    def reports(self, value: Tuple[str, ...]):
        self._property_changed('reports')
        self.__reports = value        

    @property
    def reports_with_parameters_overrides(self) -> Tuple[ReportWithParametersOverrides, ...]:
        """Reports with their parameters to be overridden"""
        return self.__reports_with_parameters_overrides

    @reports_with_parameters_overrides.setter
    def reports_with_parameters_overrides(self, value: Tuple[ReportWithParametersOverrides, ...]):
        self._property_changed('reports_with_parameters_overrides')
        self.__reports_with_parameters_overrides = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def parameters(self) -> ReportParameters:
        """Parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def priority(self) -> Union[ReportJobPriority, str]:
        """Report job priority."""
        return self.__priority

    @priority.setter
    def priority(self, value: Union[ReportJobPriority, str]):
        self._property_changed('priority')
        self.__priority = get_enum_value(ReportJobPriority, value)        


class ReportJob(Base):
        
    @camel_case_translate
    def __init__(
        self,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        elapsed_time: float = None,
        percentage_complete: float = None,
        execution_time: datetime.datetime = None,
        id_: str = None,
        measures: Tuple[Union[ReportMeasures, str], ...] = None,
        parameters: ReportParameters = None,
        parent_id: str = None,
        position_source_id: str = None,
        position_source_type: Union[PositionSourceType, str] = None,
        report_id: str = None,
        report_type: Union[ReportType, str] = None,
        status: Union[ReportStatus, str] = None,
        owner_id: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        report_ids: Tuple[str, ...] = None,
        priority: Union[ReportJobPriority, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.elapsed_time = elapsed_time
        self.percentage_complete = percentage_complete
        self.execution_time = execution_time
        self.__id = id_
        self.measures = measures
        self.parameters = parameters
        self.parent_id = parent_id
        self.position_source_id = position_source_id
        self.position_source_type = position_source_type
        self.report_id = report_id
        self.report_type = report_type
        self.status = status
        self.owner_id = owner_id
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.report_ids = report_ids
        self.priority = priority
        self.name = name

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def elapsed_time(self) -> float:
        """Time taken to execute report (in milliseconds)"""
        return self.__elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value: float):
        self._property_changed('elapsed_time')
        self.__elapsed_time = value        

    @property
    def percentage_complete(self) -> float:
        """Percentage that the job has been completed so far"""
        return self.__percentage_complete

    @percentage_complete.setter
    def percentage_complete(self, value: float):
        self._property_changed('percentage_complete')
        self.__percentage_complete = value        

    @property
    def execution_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_time

    @execution_time.setter
    def execution_time(self, value: datetime.datetime):
        self._property_changed('execution_time')
        self.__execution_time = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def measures(self) -> Tuple[Union[ReportMeasures, str], ...]:
        """measures to be outputted for the report"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[ReportMeasures, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def parameters(self) -> ReportParameters:
        """Parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def parent_id(self) -> str:
        """Marquee unique identifier"""
        return self.__parent_id

    @parent_id.setter
    def parent_id(self, value: str):
        self._property_changed('parent_id')
        self.__parent_id = value        

    @property
    def position_source_id(self) -> str:
        """Marquee unique identifier"""
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: str):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def position_source_type(self) -> Union[PositionSourceType, str]:
        """Source object for position data"""
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: Union[PositionSourceType, str]):
        self._property_changed('position_source_type')
        self.__position_source_type = get_enum_value(PositionSourceType, value)        

    @property
    def report_id(self) -> str:
        """Marquee unique identifier"""
        return self.__report_id

    @report_id.setter
    def report_id(self, value: str):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def report_type(self) -> Union[ReportType, str]:
        """Type of report to execute"""
        return self.__report_type

    @report_type.setter
    def report_type(self, value: Union[ReportType, str]):
        self._property_changed('report_type')
        self.__report_type = get_enum_value(ReportType, value)        

    @property
    def status(self) -> Union[ReportStatus, str]:
        """Status of report run"""
        return self.__status

    @status.setter
    def status(self, value: Union[ReportStatus, str]):
        self._property_changed('status')
        self.__status = get_enum_value(ReportStatus, value)        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def created_by_id(self) -> str:
        """Marquee unique identifier"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Report that are covered by job. When provided it means its a batched job."""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self._property_changed('report_ids')
        self.__report_ids = value        

    @property
    def priority(self) -> Union[ReportJobPriority, str]:
        """Report job priority."""
        return self.__priority

    @priority.setter
    def priority(self, value: Union[ReportJobPriority, str]):
        self._property_changed('priority')
        self.__priority = get_enum_value(ReportJobPriority, value)        
