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
import time
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
from pydash import get

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.common import DateLimit, PositionType
from gs_quant.data import DataCoordinate, DataFrequency, DataMeasure
from gs_quant.data.coordinate import DataDimensions
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqError
from gs_quant.markets.position_set import PositionSet
from gs_quant.markets.report import PerformanceReport, FactorRiskReport, Report
from gs_quant.session import GsSession
from gs_quant.target.reports import ReportStatus, ReportType

_logger = logging.getLogger(__name__)


class EntityType(Enum):
    ASSET = 'asset'
    BACKTEST = 'backtest'
    COUNTRY = 'country'
    HEDGE = 'hedge'
    KPI = 'kpi'
    PORTFOLIO = 'portfolio'
    REPORT = 'report'
    RISK_MODEL = 'risk_model'
    SUBDIVISION = 'subdivision'


@dataclass
class EntityKey:
    id_: str
    entity_type: EntityType


class EntityIdentifier(Enum):
    pass


class Entity(metaclass=ABCMeta):
    """Base class for any first-class entity"""
    _entity_to_endpoint = {
        EntityType.ASSET: 'assets',
        EntityType.COUNTRY: 'countries',
        EntityType.SUBDIVISION: 'countries/subdivisions',
        EntityType.KPI: 'kpis',
        EntityType.PORTFOLIO: 'portfolios',
        EntityType.RISK_MODEL: 'risk/models'
    }

    def __init__(self,
                 id_: str,
                 entity_type: EntityType,
                 entity: Optional[Dict] = None):
        self.__id: str = id_
        self.__entity_type: EntityType = entity_type
        self.__entity: Dict = entity

    @property
    @abstractmethod
    def data_dimension(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def entity_type(cls) -> EntityType:
        pass

    @classmethod
    def get(cls,
            id_value: str,
            id_type: Union[EntityIdentifier, str],
            entity_type: Optional[Union[EntityType, str]] = None):
        id_type = id_type.value if isinstance(id_type, Enum) else id_type

        if entity_type is None:
            entity_type = cls.entity_type()
            endpoint = cls._entity_to_endpoint[entity_type]
        else:
            entity_type = entity_type.value if isinstance(entity_type, Enum) else entity_type
            endpoint = cls._entity_to_endpoint[EntityType(entity_type)]

        if entity_type == 'asset':
            from gs_quant.markets.securities import SecurityMaster, AssetIdentifier
            return SecurityMaster.get_asset(id_value, AssetIdentifier.MARQUEE_ID)

        if id_type == 'MQID':
            result = GsSession.current._get(f'/{endpoint}/{id_value}')
        else:
            result = get(GsSession.current._get(f'/{endpoint}?{id_type.lower()}={id_value}'), 'results.0')
        if result:
            return cls._get_entity_from_type(result, EntityType(entity_type))

    @classmethod
    def _get_entity_from_type(cls,
                              entity: Dict,
                              entity_type: EntityType = None):
        id_ = entity.get('id')
        entity_type = entity_type or cls.entity_type()
        if entity_type == EntityType.COUNTRY:
            return Country(id_, entity=entity)
        if entity_type == EntityType.KPI:
            return KPI(id_, entity=entity)
        if entity_type == EntityType.SUBDIVISION:
            return Subdivision(id_, entity=entity)
        if entity_type == EntityType.RISK_MODEL:
            return RiskModelEntity(id_, entity=entity)

    def get_marquee_id(self) -> str:
        return self.__id

    def get_entity(self) -> Optional[Dict]:
        return self.__entity

    def get_unique_entity_key(self) -> EntityKey:
        return EntityKey(self.__id, self.__entity_type)

    def get_data_coordinate(self,
                            measure: Union[DataMeasure, str],
                            dimensions: Optional[DataDimensions] = None,
                            frequency: DataFrequency = DataFrequency.DAILY,
                            availability=None) -> DataCoordinate:
        id_ = self.get_marquee_id()
        dimensions = dimensions or {}
        dimensions[self.data_dimension] = id_
        measure = measure if isinstance(measure, str) else measure.value
        available: Dict = GsDataApi.get_data_providers(id_, availability).get(measure, {})

        if frequency == DataFrequency.DAILY:
            daily_dataset_id = available.get(DataFrequency.DAILY)
            return DataCoordinate(dataset_id=daily_dataset_id, measure=measure, dimensions=dimensions,
                                  frequency=frequency)
        if frequency == DataFrequency.REAL_TIME:
            rt_dataset_id = available.get(DataFrequency.REAL_TIME)
            return DataCoordinate(dataset_id=rt_dataset_id, measure=measure, dimensions=dimensions, frequency=frequency)

    def get_entitlements(self):
        entitlements_dict = self.get_entity().get('entitlements')
        if entitlements_dict is None:
            raise ValueError('This entity does not have entitlements.')
        return Entitlements.from_dict(entitlements_dict)


class Country(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = 'MQID'
        NAME = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.COUNTRY, entity)

    @property
    def data_dimension(self) -> str:
        return 'countryId'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.COUNTRY

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')

    def get_region(self) -> Optional[str]:
        return get(self.get_entity(), 'region')

    def get_sub_region(self):
        return get(self.get_entity(), 'subRegion')

    def get_region_code(self):
        return get(self.get_entity(), 'regionCode')

    def get_sub_region_code(self):
        return get(self.get_entity(), 'subRegionCode')

    def get_alpha3(self):
        return get(self.get_entity(), 'xref.alpha3')

    def get_bbid(self):
        return get(self.get_entity(), 'xref.bbid')

    def get_alpha2(self):
        return get(self.get_entity(), 'xref.alpha2')

    def get_country_code(self):
        return get(self.get_entity(), 'xref.countryCode')


class Subdivision(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = 'MQID'
        name = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.SUBDIVISION, entity)

    @property
    def data_dimension(self) -> str:
        return 'subdivisionId'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.SUBDIVISION

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')


class KPI(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = "MQID"
        name = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.KPI, entity)

    @property
    def data_dimension(self) -> str:
        return 'kpiId'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.KPI

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')

    def get_category(self) -> Optional[str]:
        return get(self.get_entity(), 'category')

    def get_sub_category(self):
        return get(self.get_entity(), 'subCategory')


class RiskModelEntity(Entity):
    class Identifier(EntityIdentifier):
        MARQUEE_ID = "MQID"
        name = 'name'

    def __init__(self,
                 id_: str,
                 entity: Optional[Dict] = None):
        super().__init__(id_, EntityType.RISK_MODEL, entity)

    @property
    def data_dimension(self) -> str:
        return 'riskModel'

    @classmethod
    def entity_type(cls) -> EntityType:
        return EntityType.RISK_MODEL

    @classmethod
    def get_by_identifier(cls,
                          id_value: str,
                          id_type: Identifier) -> Optional['Entity']:
        super().get(id_value, id_type)

    def get_name(self) -> Optional[str]:
        return get(self.get_entity(), 'name')

    def get_coverage(self) -> Optional[str]:
        return get(self.get_entity(), 'coverage')

    def get_term(self) -> Optional[str]:
        return get(self.get_entity(), 'term')

    def get_vendor(self) -> Optional[str]:
        return get(self.get_entity(), 'vendor')


class PositionedEntity(metaclass=ABCMeta):
    def __init__(self, id_: str, entity_type: EntityType):
        self.__id: str = id_
        self.__entity_type: EntityType = entity_type

    @property
    def id(self) -> str:
        return self.__id

    @property
    def positioned_entity_type(self) -> EntityType:
        return self.__entity_type

    def get_latest_position_set(self,
                                position_type: PositionType = PositionType.CLOSE) -> PositionSet:
        if self.positioned_entity_type == EntityType.ASSET:
            response = GsAssetApi.get_latest_positions(self.id, position_type)
            return PositionSet.from_target(response)
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            response = GsPortfolioApi.get_latest_positions(portfolio_id=self.id,
                                                           position_type=position_type.value)
            return PositionSet.from_target(response)
        raise NotImplementedError

    def get_position_set_for_date(self,
                                  date: dt.date,
                                  position_type: PositionType = PositionType.CLOSE) -> PositionSet:
        if self.positioned_entity_type == EntityType.ASSET:
            response = GsAssetApi.get_asset_positions_for_date(self.id, date, position_type)[0]
            return PositionSet.from_target(response)
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            response = GsPortfolioApi.get_positions_for_date(portfolio_id=self.id,
                                                             position_date=date,
                                                             position_type=position_type.value)
            return PositionSet.from_target(response) if response else None
        raise NotImplementedError

    def get_position_sets(self,
                          start: dt.date = DateLimit.LOW_LIMIT.value,
                          end: dt.date = dt.date.today(),
                          position_type: PositionType = PositionType.CLOSE) -> List[PositionSet]:
        if self.positioned_entity_type == EntityType.ASSET:
            response = GsAssetApi.get_asset_positions_for_dates(self.id, start, end, position_type)
            return [PositionSet.from_target(position_set) for position_set in response]
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            response = GsPortfolioApi.get_positions(portfolio_id=self.id,
                                                    start_date=start,
                                                    end_date=end)
            return [PositionSet.from_target(position_set) for position_set in response]
        raise NotImplementedError

    def update_positions(self,
                         position_sets: List[PositionSet],
                         schedule_reports: bool = True):
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            if not position_sets:
                return
            existing_positions_dates = self.get_position_dates()
            new_position_dates = [p.date for p in position_sets] if position_sets else []
            reports = [r.latest_end_date for r in self.get_reports() if r.latest_end_date]
            latest_date_covered_by_reports = min(reports) if reports else None
            latest_position_date_in_reports = max([d for d in existing_positions_dates
                                                   if d <= latest_date_covered_by_reports]) \
                if latest_date_covered_by_reports else min(new_position_dates)
            start_date = min(latest_position_date_in_reports, min(new_position_dates))
            end_date = max(new_position_dates)
            GsPortfolioApi.update_positions(portfolio_id=self.id, position_sets=[p.to_target() for p in position_sets])
            if schedule_reports:
                self._schedule_reports(start_date=start_date,
                                       end_date=end_date)
        else:
            raise NotImplementedError

    def get_positions_data(self,
                           start: dt.date = DateLimit.LOW_LIMIT.value,
                           end: dt.date = dt.date.today(),
                           fields: [str] = None,
                           position_type: PositionType = PositionType.CLOSE) -> List[Dict]:
        if self.positioned_entity_type == EntityType.ASSET:
            return GsAssetApi.get_asset_positions_data(self.id, start, end, fields, position_type)
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            return GsPortfolioApi.get_positions_data(self.id, start, end, fields, position_type)
        raise NotImplementedError

    def get_position_dates(self) -> Tuple[dt.date, ...]:
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            return GsPortfolioApi.get_position_dates(portfolio_id=self.id)
        if self.positioned_entity_type == EntityType.ASSET:
            return GsAssetApi.get_position_dates(asset_id=self.id)
        raise NotImplementedError

    def get_reports(self) -> List[Report]:
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            reports_as_target = GsPortfolioApi.get_reports(portfolio_id=self.id)
        elif self.positioned_entity_type == EntityType.ASSET:
            reports_as_target = GsAssetApi.get_reports(asset_id=self.id)
        else:
            raise NotImplementedError
        report_objects = []
        for report in reports_as_target:
            if report.type == ReportType.Portfolio_Performance_Analytics:
                report_objects.append(PerformanceReport.from_target(report))
            elif report.type in [ReportType.Portfolio_Factor_Risk, ReportType.Asset_Factor_Risk]:
                report_objects.append(FactorRiskReport.from_target(report))
            else:
                report_objects.append(Report.from_target(report))
        return report_objects

    def get_status_of_reports(self) -> pd.DataFrame:
        reports = self.get_reports()
        reports_dict = {
            'Name': [r.name for r in reports],
            'ID': [r.id for r in reports],
            'Latest Execution Time': [r.latest_execution_time for r in reports],
            'Latest End Date': [r.latest_end_date for r in reports],
            "Status": [r.status for r in reports],
            'Percentage Complete': [r.percentage_complete for r in reports]
        }

        return pd.DataFrame.from_dict(reports_dict)

    def get_factor_risk_report(self,
                               risk_model_id: str = None,
                               fx_hedged: bool = None) -> FactorRiskReport:
        if self.positioned_entity_type in [EntityType.PORTFOLIO, EntityType.ASSET]:
            position_source_type = self.positioned_entity_type.value.capitalize()
            reports = GsReportApi.get_reports(limit=100,
                                              position_source_type=position_source_type,
                                              position_source_id=self.id,
                                              report_type=f'{position_source_type} Factor Risk')
            if fx_hedged:
                reports = [report for report in reports if report.parameters.fx_hedged == fx_hedged]
            if risk_model_id:
                reports = [report for report in reports if report.parameters.risk_model == risk_model_id]
            if len(reports) > 1:
                raise MqError(f'This {position_source_type} has more than one factor risk report that matches '
                              'your parameters. Please specify the risk model ID and fxHedged value in the '
                              'function parameters.')
            if len(reports) == 0:
                raise MqError(f'This {position_source_type} has no factor risk reports that match your parameters.')
            return FactorRiskReport.from_target(reports[0])
        raise NotImplementedError

    def create_report(self, report: Report):
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            report.set_position_source(self.id)
            report.save()
            self._schedule_first_reports([pos_set.date for pos_set in self.get_position_sets()])
            return report
        raise NotImplementedError

    def poll_report(self, report_id: str, timeout: int = 600, step: int = 30) -> ReportStatus:
        poll = True
        timeout = 1800 if timeout > 1800 else timeout
        step = 15 if step < 15 else step
        end = dt.datetime.now() + dt.timedelta(seconds=timeout)

        while poll and dt.datetime.now() <= end:
            try:
                status = Report.get(report_id).status
                if status not in {ReportStatus.error, ReportStatus.cancelled, ReportStatus.done}:
                    _logger.info(f'Report is {status} as of {dt.datetime.now().isoformat()}')
                    time.sleep(step)
                else:
                    poll = False
                    if status == ReportStatus.error:
                        raise MqError(f'Report {report_id} has failed for {self.id}. \
                                        Please reach out to the Marquee team for assistance.')
                    elif status == ReportStatus.cancelled:
                        _logger.info(f'Report {report_id} has been cancelled. Please reach out to the \
                                       Marquee team if you believe this is a mistake.')
                        return status
                    else:
                        _logger.info(f'Report {report_id} is now complete')
                        return status
            except Exception as err:
                raise MqError(f'Could not fetch report status with error {err}')

        raise MqError('The report is taking longer than expected to complete. \
                       Please check again later or reach out to the Marquee team for assistance.')
