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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class PositionSourceType(EnumBase, Enum):    
    
    """Source object for position data"""

    Portfolio = 'Portfolio'
    Asset = 'Asset'
    Backtest = 'Backtest'
    RiskRequest = 'RiskRequest'
    Hedge = 'Hedge'
    
    def __repr__(self):
        return self.value


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
    price = 'price'
    basePrice = 'basePrice'
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


class ReportType(EnumBase, Enum):    
    
    """Type of report to execute"""

    Portfolio_Performance_Analytics = 'Portfolio Performance Analytics'
    Portfolio_Factor_Risk = 'Portfolio Factor Risk'
    Portfolio_Aging = 'Portfolio Aging'
    Asset_Factor_Risk = 'Asset Factor Risk'
    Basket_Create = 'Basket Create'
    Basket_Backcast = 'Basket Backcast'
    Scenario = 'Scenario'
    Iselect_Backtest = 'Iselect Backtest'
    Backtest_Run = 'Backtest Run'
    Analytics = 'Analytics'
    Risk_Calculation = 'Risk Calculation'
    PCO_Generate_Orders = 'PCO Generate Orders'
    PCO_Program_Change = 'PCO Program Change'
    
    def __repr__(self):
        return self.value


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


class User(Base):
        
    @camel_case_translate
    def __init__(
        self,
        company: str,
        id_: str,
        country: str,
        city: str,
        region: str,
        email: str,
        name: str,
        internal: bool = None,
        system_user: bool = None,
        app_user: bool = None,
        analytics_id: str = None,
        eaa_company: str = None,
        root_oe_id: str = None,
        oe_id: str = None,
        root_oe_name: str = None,
        oe_name: str = None,
        oe_alias: int = None,
        coverage: Tuple[dict, ...] = None,
        internal_email: str = None,
        kerberos: str = None,
        first_name: str = None,
        last_name: str = None,
        internal_id: str = None,
        mi_fidii_trade_idea_declined: str = None,
        department_code: str = None,
        department_name: str = None,
        division_name: str = None,
        business_unit: str = None,
        title: str = None,
        pmd: bool = None,
        login: str = None,
        tokens: Tuple[str, ...] = None,
        roles: Tuple[str, ...] = None,
        groups: Tuple[str, ...] = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        entitlements: Entitlements = None,
        app_managers: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.internal = internal
        self.system_user = system_user
        self.app_user = app_user
        self.analytics_id = analytics_id
        self.city = city
        self.company = company
        self.eaa_company = eaa_company
        self.root_oe_id = root_oe_id
        self.oe_id = oe_id
        self.root_oe_name = root_oe_name
        self.oe_name = oe_name
        self.oe_alias = oe_alias
        self.country = country
        self.coverage = coverage
        self.email = email
        self.internal_email = internal_email
        self.kerberos = kerberos
        self.__id = id_
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.internal_id = internal_id
        self.region = region
        self.mi_fidii_trade_idea_declined = mi_fidii_trade_idea_declined
        self.department_code = department_code
        self.department_name = department_name
        self.division_name = division_name
        self.business_unit = business_unit
        self.title = title
        self.pmd = pmd
        self.login = login
        self.tokens = tokens
        self.roles = roles
        self.groups = groups
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.entitlements = entitlements
        self.app_managers = app_managers

    @property
    def internal(self) -> bool:
        """Is internal"""
        return self.__internal

    @internal.setter
    def internal(self, value: bool):
        self._property_changed('internal')
        self.__internal = value        

    @property
    def system_user(self) -> bool:
        """Is system user"""
        return self.__system_user

    @system_user.setter
    def system_user(self, value: bool):
        self._property_changed('system_user')
        self.__system_user = value        

    @property
    def app_user(self) -> bool:
        """Is app user"""
        return self.__app_user

    @app_user.setter
    def app_user(self, value: bool):
        self._property_changed('app_user')
        self.__app_user = value        

    @property
    def analytics_id(self) -> str:
        """Marquee unique identifier"""
        return self.__analytics_id

    @analytics_id.setter
    def analytics_id(self, value: str):
        self._property_changed('analytics_id')
        self.__analytics_id = value        

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, value: str):
        self._property_changed('city')
        self.__city = value        

    @property
    def company(self) -> str:
        return self.__company

    @company.setter
    def company(self, value: str):
        self._property_changed('company')
        self.__company = value        

    @property
    def eaa_company(self) -> str:
        return self.__eaa_company

    @eaa_company.setter
    def eaa_company(self, value: str):
        self._property_changed('eaa_company')
        self.__eaa_company = value        

    @property
    def root_oe_id(self) -> str:
        """Goldman Sachs unique identifier for user's root organization"""
        return self.__root_oe_id

    @root_oe_id.setter
    def root_oe_id(self, value: str):
        self._property_changed('root_oe_id')
        self.__root_oe_id = value        

    @property
    def oe_id(self) -> str:
        """Goldman Sachs unique identifier for user's organization"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def root_oe_name(self) -> str:
        """The name of the company."""
        return self.__root_oe_name

    @root_oe_name.setter
    def root_oe_name(self, value: str):
        self._property_changed('root_oe_name')
        self.__root_oe_name = value        

    @property
    def oe_name(self) -> str:
        """The name of the company."""
        return self.__oe_name

    @oe_name.setter
    def oe_name(self, value: str):
        self._property_changed('oe_name')
        self.__oe_name = value        

    @property
    def oe_alias(self) -> int:
        """Goldman Sachs alias for user's organization"""
        return self.__oe_alias

    @oe_alias.setter
    def oe_alias(self, value: int):
        self._property_changed('oe_alias')
        self.__oe_alias = value        

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str):
        self._property_changed('country')
        self.__country = value        

    @property
    def coverage(self) -> Tuple[dict, ...]:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: Tuple[dict, ...]):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def internal_email(self) -> str:
        return self.__internal_email

    @internal_email.setter
    def internal_email(self, value: str):
        self._property_changed('internal_email')
        self.__internal_email = value        

    @property
    def kerberos(self) -> str:
        return self.__kerberos

    @kerberos.setter
    def kerberos(self, value: str):
        self._property_changed('kerberos')
        self.__kerberos = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self._property_changed('first_name')
        self.__first_name = value        

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self._property_changed('last_name')
        self.__last_name = value        

    @property
    def internal_id(self) -> str:
        return self.__internal_id

    @internal_id.setter
    def internal_id(self, value: str):
        self._property_changed('internal_id')
        self.__internal_id = value        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def mi_fidii_trade_idea_declined(self) -> str:
        return self.__mi_fidii_trade_idea_declined

    @mi_fidii_trade_idea_declined.setter
    def mi_fidii_trade_idea_declined(self, value: str):
        self._property_changed('mi_fidii_trade_idea_declined')
        self.__mi_fidii_trade_idea_declined = value        

    @property
    def department_code(self) -> str:
        return self.__department_code

    @department_code.setter
    def department_code(self, value: str):
        self._property_changed('department_code')
        self.__department_code = value        

    @property
    def department_name(self) -> str:
        return self.__department_name

    @department_name.setter
    def department_name(self, value: str):
        self._property_changed('department_name')
        self.__department_name = value        

    @property
    def division_name(self) -> str:
        return self.__division_name

    @division_name.setter
    def division_name(self, value: str):
        self._property_changed('division_name')
        self.__division_name = value        

    @property
    def business_unit(self) -> str:
        return self.__business_unit

    @business_unit.setter
    def business_unit(self, value: str):
        self._property_changed('business_unit')
        self.__business_unit = value        

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def pmd(self) -> bool:
        """Is a PMD."""
        return self.__pmd

    @pmd.setter
    def pmd(self, value: bool):
        self._property_changed('pmd')
        self.__pmd = value        

    @property
    def login(self) -> str:
        return self.__login

    @login.setter
    def login(self, value: str):
        self._property_changed('login')
        self.__login = value        

    @property
    def tokens(self) -> Tuple[str, ...]:
        return self.__tokens

    @tokens.setter
    def tokens(self, value: Tuple[str, ...]):
        self._property_changed('tokens')
        self.__tokens = value        

    @property
    def roles(self) -> Tuple[str, ...]:
        """Role set used for entitlements"""
        return self.__roles

    @roles.setter
    def roles(self, value: Tuple[str, ...]):
        self._property_changed('roles')
        self.__roles = value        

    @property
    def groups(self) -> Tuple[str, ...]:
        """Group set used for data level entitlements"""
        return self.__groups

    @groups.setter
    def groups(self, value: Tuple[str, ...]):
        self._property_changed('groups')
        self.__groups = value        

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
        """Timestamp of when the user was created"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

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
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def app_managers(self) -> Tuple[str, ...]:
        """Application managers associated with the app user"""
        return self.__app_managers

    @app_managers.setter
    def app_managers(self, value: Tuple[str, ...]):
        self._property_changed('app_managers')
        self.__app_managers = value        


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
