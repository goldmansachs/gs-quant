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

import deprecation
import pandas as pd
from pydash import get

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.carbon import CarbonCard, GsCarbonApi, CarbonTargetCoverageCategory, CarbonScope, \
    CarbonEmissionsAllocationCategory, CarbonEmissionsIntensityType, CarbonCoverageCategory, CarbonEntityType, \
    CarbonAnalyticsView
from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.esg import ESGMeasure, GsEsgApi, ESGCard
from gs_quant.api.gs.indices import GsIndexApi
from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.api.gs.thematics import ThematicMeasure, GsThematicApi, Region
from gs_quant.common import DateLimit, PositionType, Currency
from gs_quant.data import DataCoordinate, DataFrequency, DataMeasure
from gs_quant.data.coordinate import DataDimensions
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqError, MqValueError
from gs_quant.markets.indices_utils import BasketType, IndicesDatasets
from gs_quant.markets.position_set import PositionSet
from gs_quant.markets.report import PerformanceReport, FactorRiskReport, Report, ThematicReport, \
    flatten_results_into_df, get_thematic_breakdown_as_df
from gs_quant.session import GsSession
from gs_quant.target.data import DataQuery
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
    DATASET = 'dataset'


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
        EntityType.RISK_MODEL: 'risk/models',
        EntityType.DATASET: 'data/datasets'
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
        return EntityKey(self.get_marquee_id(), self.__entity_type)

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

    def get_entitlements(self) -> Entitlements:
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            response = GsPortfolioApi.get_portfolio(self.id)
        elif self.positioned_entity_type == EntityType.ASSET:
            response = GsAssetApi.get_asset(self.id)
        else:
            raise NotImplementedError
        return Entitlements.from_target(response.entitlements)

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
            response = GsAssetApi.get_asset_positions_for_date(self.id, date, position_type)
            if len(response) == 0:
                _logger.info("No positions available for {}".format(date))
                return PositionSet([], date=date)
            return PositionSet.from_target(response[0])
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
            if len(response) == 0:
                _logger.info("No positions available in the date range {} - {}".format(start, end))
                return []
            return [PositionSet.from_target(position_set) for position_set in response]
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            response = GsPortfolioApi.get_positions(portfolio_id=self.id,
                                                    start_date=start,
                                                    end_date=end)
            return [PositionSet.from_target(position_set) for position_set in response]
        raise NotImplementedError

    def update_positions(self,
                         position_sets: List[PositionSet],
                         net_positions: bool = True):
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            if not position_sets:
                return
            currency = GsPortfolioApi.get_portfolio(self.id).currency
            new_sets = []
            for pos_set in position_sets:
                positions_are_missing_quantities = len([p for p in pos_set.positions if p.quantity is None]) > 0
                if positions_are_missing_quantities:
                    pos_set.price(currency)
                new_sets.append(pos_set)
            GsPortfolioApi.update_positions(portfolio_id=self.id, position_sets=[p.to_target() for p in new_sets],
                                            net_positions=net_positions)
            time.sleep(3)
        else:
            raise NotImplementedError

    def get_positions_data(self,
                           start: dt.date = DateLimit.LOW_LIMIT.value,
                           end: dt.date = dt.date.today(),
                           fields: [str] = None,
                           position_type: PositionType = PositionType.CLOSE) -> List[Dict]:
        if self.positioned_entity_type == EntityType.ASSET:
            return GsIndexApi.get_positions_data(self.id, start, end, fields, position_type)
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            raise MqError('Please use the get_positions_data function on the portfolio performance report using the '
                          'PerformanceReport class')
        raise NotImplementedError

    def get_last_positions_data(self,
                                fields: [str] = None,
                                position_type: PositionType = PositionType.CLOSE) -> List[Dict]:
        if self.positioned_entity_type == EntityType.ASSET:
            return GsIndexApi.get_last_positions_data(self.id, fields, position_type)
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            raise MqError('Please use the get_positions_data function on the portfolio performance report using the '
                          'PerformanceReport class')
        raise NotImplementedError

    def get_position_dates(self) -> Tuple[dt.date, ...]:
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            return GsPortfolioApi.get_position_dates(portfolio_id=self.id)
        if self.positioned_entity_type == EntityType.ASSET:
            return GsAssetApi.get_position_dates(asset_id=self.id)
        raise NotImplementedError

    def get_reports(self, tags: Dict = None) -> List[Report]:
        if self.positioned_entity_type == EntityType.PORTFOLIO:
            reports_as_target = GsPortfolioApi.get_reports(portfolio_id=self.id, tags=tags)
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
            elif report.type in [ReportType.Portfolio_Thematic_Analytics, ReportType.Asset_Thematic_Analytics]:
                report_objects.append(ThematicReport.from_target(report))
            else:
                report_objects.append(Report.from_target(report))
        return report_objects

    def get_status_of_reports(self, tags: Dict = None) -> pd.DataFrame:
        reports = self.get_reports(tags)
        reports_dict = {
            'Name': [r.name for r in reports],
            'ID': [r.id for r in reports],
            'Latest Execution Time': [r.latest_execution_time for r in reports],
            'Latest End Date': [r.latest_end_date for r in reports],
            "Status": [r.status for r in reports],
            'Percentage Complete': [r.percentage_complete for r in reports]
        }

        return pd.DataFrame.from_dict(reports_dict)

    def get_factor_risk_reports(self, fx_hedged: bool = None, tags: Dict = None) -> List[FactorRiskReport]:
        if self.positioned_entity_type in [EntityType.PORTFOLIO, EntityType.ASSET]:
            position_source_type = self.positioned_entity_type.value.capitalize()
            reports = GsReportApi.get_reports(limit=100,
                                              position_source_type=position_source_type,
                                              position_source_id=self.id,
                                              report_type=f'{position_source_type} Factor Risk',
                                              tags=tags)
            if fx_hedged:
                reports = [report for report in reports if report.parameters.fx_hedged == fx_hedged]
            if len(reports) == 0:
                raise MqError(f'This {position_source_type} has no factor risk reports that match your parameters.')
            return [FactorRiskReport.from_target(report) for report in reports]
        raise NotImplementedError

    def get_factor_risk_report(self,
                               risk_model_id: str = None,
                               fx_hedged: bool = None,
                               benchmark_id: str = None,
                               tags: Dict = None) -> FactorRiskReport:
        position_source_type = self.positioned_entity_type.value.capitalize()
        reports = self.get_factor_risk_reports(fx_hedged=fx_hedged, tags=tags)
        if risk_model_id:
            reports = [report for report in reports if report.parameters.risk_model == risk_model_id]
        reports = [report for report in reports if report.parameters.benchmark == benchmark_id]
        if len(reports) == 0:
            raise MqError(f'This {position_source_type} has no factor risk reports that match '
                          'your parameters. Please edit the risk model ID, fxHedged, and/or benchmark value in the '
                          'function parameters.')
        if len(reports) > 1:
            raise MqError(f'This {position_source_type} has more than one factor risk report that matches '
                          'your parameters. Please specify the risk model ID, fxHedged, and/or benchmark value in the '
                          'function parameters.')
        return reports[0]

    def get_thematic_report(self, tags: Dict = None) -> ThematicReport:
        if self.positioned_entity_type in [EntityType.PORTFOLIO, EntityType.ASSET]:
            position_source_type = self.positioned_entity_type.value.capitalize()
            reports = GsReportApi.get_reports(limit=100,
                                              position_source_type=position_source_type,
                                              position_source_id=self.id,
                                              report_type=f'{position_source_type} Thematic Analytics',
                                              tags=tags)
            if len(reports) == 0:
                raise MqError(f'This {position_source_type} has no thematic analytics report.')
            return ThematicReport.from_target(reports[0])
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

    def get_all_esg_data(self,
                         measures: List[ESGMeasure] = None,
                         cards: List[ESGCard] = None,
                         pricing_date: dt.date = None,
                         benchmark_id: str = None) -> Dict:
        """
        Get all ESG Data
        :param measures: list of ESG Measures to include in results
        :param cards: list of ESG Cards to include in results
        :param pricing_date: optional pricing date; defaults to last previous business day
        :param benchmark_id: optional benchmark asset ID to include in results
        :return: a dictionary of results
        """
        return GsEsgApi.get_esg(entity_id=self.id,
                                pricing_date=pricing_date,
                                cards=cards if cards else [c for c in ESGCard],
                                measures=measures if measures else [m for m in ESGMeasure],
                                benchmark_id=benchmark_id)

    def get_esg_summary(self,
                        pricing_date: dt.date = None) -> pd.DataFrame:
        summary_data = GsEsgApi.get_esg(entity_id=self.id,
                                        pricing_date=pricing_date,
                                        cards=[ESGCard.SUMMARY]).get('summary')
        return pd.DataFrame(summary_data)

    def get_esg_quintiles(self,
                          measure: ESGMeasure,
                          pricing_date: dt.date = None) -> pd.DataFrame:
        """
        Get breakdown of entity by weight in each percentile quintile for requested ESG measure
        :param measure: ESG Measure
        :param pricing_date: optional pricing date; defaults to last previous business day
        :return: a Pandas DataFrame with results
        """
        quintile_data = GsEsgApi.get_esg(entity_id=self.id,
                                         pricing_date=pricing_date,
                                         cards=[ESGCard.QUINTILES],
                                         measures=[measure]).get('quintiles')[0].get('results')
        df = pd.DataFrame(quintile_data)
        return df.filter(items=['description', 'gross', 'long', 'short'])

    def get_esg_by_sector(self,
                          measure: ESGMeasure,
                          pricing_date: dt.date = None) -> pd.DataFrame:
        """
        Get breakdown of entity by sector, along with the weighted average score of the compositions in each sector
        :param measure: ESG Measure
        :param pricing_date: optional pricing date; defaults to last previous business day
        :return: a Pandas DataFrame with results
        """
        return self._get_esg_breakdown(ESGCard.MEASURES_BY_SECTOR, measure, pricing_date)

    def get_esg_by_region(self,
                          measure: ESGMeasure,
                          pricing_date: dt.date = None) -> pd.DataFrame:
        """
        Get breakdown of entity by region, along with the weighted average score of the compositions in each region
        :param measure: ESG Measure
        :param pricing_date: optional pricing date; defaults to last previous business day
        :return: a Pandas DataFrame with results
        """
        return self._get_esg_breakdown(ESGCard.MEASURES_BY_REGION, measure, pricing_date)

    def get_esg_top_ten(self,
                        measure: ESGMeasure,
                        pricing_date: dt.date = None):
        """
        Get entity constituents with the ten highest ESG percentile values
        :param measure: ESG Measure
        :param pricing_date: optional pricing date; defaults to last previous business day
        :return: a Pandas DataFrame with results
        """
        return self._get_esg_ranked_card(ESGCard.TOP_TEN_RANKED, measure, pricing_date)

    def get_esg_bottom_ten(self,
                           measure: ESGMeasure,
                           pricing_date: dt.date = None) -> pd.DataFrame:
        """
        Get entity constituents with the ten lowest ESG percentile values
        :param measure: ESG Measure
        :param pricing_date: optional pricing date; defaults to last previous business day
        :return: a Pandas DataFrame with results
        """
        return self._get_esg_ranked_card(ESGCard.BOTTOM_TEN_RANKED, measure, pricing_date)

    def _get_esg_ranked_card(self,
                             card: ESGCard,
                             measure: ESGMeasure,
                             pricing_date: dt.date = None) -> pd.DataFrame:
        data = GsEsgApi.get_esg(entity_id=self.id,
                                pricing_date=pricing_date,
                                cards=[card],
                                measures=[measure]).get(card.value)[0].get('results')
        return pd.DataFrame(data)

    def _get_esg_breakdown(self,
                           card: ESGCard,
                           measure: ESGMeasure,
                           pricing_date: dt.date = None) -> pd.DataFrame:
        sector_data = GsEsgApi.get_esg(entity_id=self.id,
                                       pricing_date=pricing_date,
                                       cards=[card],
                                       measures=[measure]).get(card.value)[0].get('results')
        return pd.DataFrame(sector_data)

    def get_carbon_analytics(self,
                             benchmark_id: str = None,
                             reporting_year: str = 'Latest',
                             currency: Currency = None,
                             include_estimates: bool = False,
                             use_historical_data: bool = False,
                             normalize_emissions: bool = False,
                             cards: List[CarbonCard] = [c for c in CarbonCard],
                             analytics_view: CarbonAnalyticsView = CarbonAnalyticsView.LONG) -> Dict:
        return GsCarbonApi.get_carbon_analytics(entity_id=self.id,
                                                benchmark_id=benchmark_id,
                                                reporting_year=reporting_year,
                                                currency=currency,
                                                include_estimates=include_estimates,
                                                use_historical_data=use_historical_data,
                                                normalize_emissions=normalize_emissions,
                                                cards=cards,
                                                analytics_view=analytics_view)

    def get_carbon_coverage(self,
                            reporting_year: str = 'Latest',
                            include_estimates: bool = False,
                            use_historical_data: bool = False,
                            coverage_category: CarbonCoverageCategory = CarbonCoverageCategory.WEIGHTS,
                            analytics_view: CarbonAnalyticsView = CarbonAnalyticsView.LONG) -> pd.DataFrame:
        coverage = self.get_carbon_analytics(reporting_year=reporting_year,
                                             include_estimates=include_estimates,
                                             use_historical_data=use_historical_data,
                                             cards=[CarbonCard.COVERAGE],
                                             analytics_view=analytics_view).get(CarbonCard.COVERAGE.value).get(
            coverage_category.value, {}).get(CarbonEntityType.PORTFOLIO.value, {})
        return pd.DataFrame(coverage)

    def get_carbon_sbti_netzero_coverage(self,
                                         reporting_year: str = 'Latest',
                                         include_estimates: bool = False,
                                         use_historical_data: bool = False,
                                         target_coverage_category: CarbonTargetCoverageCategory =
                                         CarbonTargetCoverageCategory.PORTFOLIO_EMISSIONS,
                                         analytics_view: CarbonAnalyticsView =
                                         CarbonAnalyticsView.LONG) -> pd.DataFrame:
        coverage = self.get_carbon_analytics(reporting_year=reporting_year,
                                             include_estimates=include_estimates,
                                             use_historical_data=use_historical_data,
                                             cards=[CarbonCard.SBTI_AND_NET_ZERO_TARGETS],
                                             analytics_view=analytics_view).get(
            CarbonCard.SBTI_AND_NET_ZERO_TARGETS.value).get(target_coverage_category.value, {})
        coverage = {target: target_coverage.get(CarbonEntityType.PORTFOLIO.value, {}) for target, target_coverage in
                    coverage.items()}
        return pd.DataFrame(coverage)

    def get_carbon_emissions(self,
                             currency: Currency = None,
                             include_estimates: bool = False,
                             use_historical_data: bool = False,
                             normalize_emissions: bool = False,
                             scope: CarbonScope = CarbonScope.TOTAL_GHG,
                             analytics_view: CarbonAnalyticsView = CarbonAnalyticsView.LONG) -> pd.DataFrame:
        emissions = self.get_carbon_analytics(currency=currency,
                                              include_estimates=include_estimates,
                                              use_historical_data=use_historical_data,
                                              normalize_emissions=normalize_emissions,
                                              cards=[CarbonCard.EMISSIONS],
                                              analytics_view=analytics_view).get(CarbonCard.EMISSIONS.value).get(
            scope.value, {}).get(CarbonEntityType.PORTFOLIO.value, [])
        return pd.DataFrame(emissions)

    def get_carbon_emissions_allocation(self,
                                        reporting_year: str = 'Latest',
                                        currency: Currency = None,
                                        include_estimates: bool = False,
                                        use_historical_data: bool = False,
                                        normalize_emissions: bool = False,
                                        scope: CarbonScope = CarbonScope.TOTAL_GHG,
                                        classification: CarbonEmissionsAllocationCategory =
                                        CarbonEmissionsAllocationCategory.GICS_SECTOR,
                                        analytics_view: CarbonAnalyticsView = CarbonAnalyticsView.LONG) -> pd.DataFrame:
        allocation = self.get_carbon_analytics(reporting_year=reporting_year,
                                               currency=currency,
                                               include_estimates=include_estimates,
                                               use_historical_data=use_historical_data,
                                               normalize_emissions=normalize_emissions,
                                               cards=[CarbonCard.ALLOCATIONS],
                                               analytics_view=analytics_view).get(CarbonCard.ALLOCATIONS.value).get(
            scope.value, {}).get(CarbonEntityType.PORTFOLIO.value, {}).get(classification.value)
        return pd.DataFrame(allocation).rename(columns={'name': classification.value})

    def get_carbon_attribution_table(self,
                                     benchmark_id: str,
                                     reporting_year: str = 'Latest',
                                     currency: Currency = None,
                                     include_estimates: bool = False,
                                     use_historical_data: bool = False,
                                     scope: CarbonScope = CarbonScope.TOTAL_GHG,
                                     intensity_metric: CarbonEmissionsIntensityType =
                                     CarbonEmissionsIntensityType.EI_ENTERPRISE_VALUE,
                                     analytics_view: CarbonAnalyticsView = CarbonAnalyticsView.LONG) -> pd.DataFrame:
        attribution = self.get_carbon_analytics(benchmark_id=benchmark_id,
                                                reporting_year=reporting_year,
                                                currency=currency,
                                                include_estimates=include_estimates,
                                                use_historical_data=use_historical_data,
                                                cards=[CarbonCard.ATTRIBUTION],
                                                analytics_view=analytics_view).get(CarbonCard.ATTRIBUTION.value).get(
            scope.value, [])
        attribution_table = []
        for entry in attribution:
            new_entry = {
                'sector': entry.get('sector'),
                'weightPortfolio': entry.get('weightPortfolio'),
                'weightBenchmark': entry.get('weightBenchmark'),
                'weightComparison': entry.get('weightComparison')
            }
            new_entry.update(entry.get(intensity_metric.value, {}))
            attribution_table.append(new_entry)
        return pd.DataFrame(attribution_table)

    def get_thematic_exposure(self,
                              basket_identifier: str,
                              notional: int = 10000000,
                              start: dt.date = DateLimit.LOW_LIMIT.value,
                              end: dt.date = dt.date.today()) -> pd.DataFrame:
        if not self.positioned_entity_type == EntityType.ASSET:
            raise NotImplementedError
        response = GsAssetApi.resolve_assets(identifier=[basket_identifier],
                                             fields=['id', 'type'], limit=1)[basket_identifier]
        _id, _type = get(response, '0.id'), get(response, '0.type')
        if len(response) == 0 or _id is None:
            raise MqValueError(f'Basket could not be found using identifier {basket_identifier}.')
        if _type not in BasketType.to_list():
            raise MqValueError(f'Asset {basket_identifier} of type {_type} is not a Custom or Research Basket.')
        query = DataQuery(where={'assetId': self.id, 'basketId': _id}, start_date=start, end_date=end)
        response = GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.COMPOSITE_THEMATIC_BETAS.value)
        df = []
        for r in response:
            df.append({'date': r['date'], 'assetId': r['assetId'], 'basketId': r['basketId'],
                       'thematicExposure': r['beta'] * notional})
        df = pd.DataFrame(df)
        return df.set_index('date')

    def get_thematic_beta(self,
                          basket_identifier: str,
                          start: dt.date = DateLimit.LOW_LIMIT.value,
                          end: dt.date = dt.date.today()) -> pd.DataFrame:
        if not self.positioned_entity_type == EntityType.ASSET:
            raise NotImplementedError
        response = GsAssetApi.resolve_assets(identifier=[basket_identifier],
                                             fields=['id', 'type'], limit=1)[basket_identifier]
        _id, _type = get(response, '0.id'), get(response, '0.type')
        if len(response) == 0 or _id is None:
            raise MqValueError(f'Basket could not be found using identifier {basket_identifier}.')
        if _type not in BasketType.to_list():
            raise MqValueError(f'Asset {basket_identifier} of type {_type} is not a Custom or Research Basket.')
        query = DataQuery(where={'assetId': self.id, 'basketId': _id}, start_date=start, end_date=end)
        response = GsDataApi.query_data(query=query, dataset_id=IndicesDatasets.COMPOSITE_THEMATIC_BETAS.value)
        df = []
        for r in response:
            df.append({'date': r['date'], 'assetId': r['assetId'], 'basketId': r['basketId'],
                       'thematicBeta': r['beta']})
        df = pd.DataFrame(df)
        return df.set_index('date')

    @deprecation.deprecated(deprecated_in="0.9.110",
                            details="Please use the same function using the ThematicReport class")
    def get_all_thematic_exposures(self,
                                   start_date: dt.date = None,
                                   end_date: dt.date = None,
                                   basket_ids: List[str] = None,
                                   regions: List[Region] = None) -> pd.DataFrame:
        results = GsThematicApi.get_thematics(entity_id=self.id,
                                              start_date=start_date,
                                              end_date=end_date,
                                              basket_ids=basket_ids,
                                              regions=regions,
                                              measures=[ThematicMeasure.ALL_THEMATIC_EXPOSURES])
        return flatten_results_into_df(results)

    @deprecation.deprecated(deprecated_in="0.9.110",
                            details="Please use the same function using the ThematicReport class")
    def get_top_five_thematic_exposures(self,
                                        start_date: dt.date = None,
                                        end_date: dt.date = None,
                                        basket_ids: List[str] = None,
                                        regions: List[Region] = None) -> pd.DataFrame:
        results = GsThematicApi.get_thematics(entity_id=self.id,
                                              start_date=start_date,
                                              end_date=end_date,
                                              basket_ids=basket_ids,
                                              regions=regions,
                                              measures=[ThematicMeasure.TOP_FIVE_THEMATIC_EXPOSURES])
        return flatten_results_into_df(results)

    @deprecation.deprecated(deprecated_in="0.9.110",
                            details="Please use the same function using the ThematicReport class")
    def get_bottom_five_thematic_exposures(self,
                                           start_date: dt.date = None,
                                           end_date: dt.date = None,
                                           basket_ids: List[str] = None,
                                           regions: List[Region] = None) -> pd.DataFrame:
        results = GsThematicApi.get_thematics(entity_id=self.id,
                                              start_date=start_date,
                                              end_date=end_date,
                                              basket_ids=basket_ids,
                                              regions=regions,
                                              measures=[ThematicMeasure.BOTTOM_FIVE_THEMATIC_EXPOSURES])
        return flatten_results_into_df(results)

    def get_thematic_breakdown(self,
                               date: dt.date,
                               basket_id: str) -> pd.DataFrame:
        """
        Get a by-asset breakdown of a portfolio or basket's thematic exposure to a particular flagship basket on a
        particular date
        :param date: date
        :param basket_id: GS flagship basket's unique Marquee ID
        :return: a Pandas DataFrame with results
        """
        return get_thematic_breakdown_as_df(entity_id=self.id, date=date, basket_id=basket_id)
