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
import traceback
from time import sleep
from typing import List, Union, Dict

import deprecation
import numpy as np
import pandas
import pandas as pd

from gs_quant.common import PositionType
from gs_quant.target.risk_models import RiskModelDataAssetsRequest, RiskModelUniverseIdentifierRequest

from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.entities.entitlements import Entitlements, EntitlementBlock, User
from gs_quant.entities.entity import PositionedEntity, EntityType, ScenarioCalculationMeasure
from gs_quant.errors import MqError
from gs_quant.errors import MqValueError
from gs_quant.markets.factor import Factor
from gs_quant.markets.scenario import FactorScenario
from gs_quant.markets.portfolio_manager_utils import build_exposure_df, build_portfolio_constituents_df, \
    build_sensitivity_df, get_batched_dates
from gs_quant.markets.report import PerformanceReport, ReportJobFuture
from gs_quant.models.risk_model import MacroRiskModel, ReturnFormat, FactorType, FactorRiskModel
from gs_quant.target.common import Currency
from gs_quant.target.portfolios import RiskAumSource, PortfolioTree

_logger = logging.getLogger(__name__)


@deprecation.deprecated(deprecated_in='1.0.10',
                        details='portfolio_manager.CustomAUMDataPoint is now deprecated, please use '
                                'report.CustomAUMDataPoint instead.')
class CustomAUMDataPoint:
    """

    Custom AUM Data Point represents a portfolio's AUM value for a specific date

    """

    def __init__(self,
                 date: dt.date,
                 aum: float):
        self.__date = date
        self.__aum = aum

    @property
    def date(self) -> dt.date:
        return self.__date

    @date.setter
    def date(self, value: dt.date):
        self.__date = value

    @property
    def aum(self) -> float:
        return self.__aum

    @aum.setter
    def aum(self, value: float):
        self.__aum = value


class PortfolioManager(PositionedEntity):
    """
    Portfolio Manager is used to manage Marquee portfolios (setting entitlements, running and retrieving reports, etc)
    """

    def __init__(self,
                 portfolio_id: str):
        """
        Initialize a Portfolio Manager

        :param portfolio_id: Portfolio ID
        """
        self.__portfolio_id = portfolio_id
        PositionedEntity.__init__(self, portfolio_id, EntityType.PORTFOLIO)

    @property
    def portfolio_id(self) -> str:
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: str):
        self.__portfolio_id = value

    def get_performance_report(self, tags: Dict = None) -> PerformanceReport:
        """
        Get performance report associated with a portfolio

        :param tags: If the portfolio is a fund of funds, pass in a dictionary corresponding to the tag values
        to retrieve results for a sub-portfolio

        :return: returns the PerformanceReport associated with portfolio if one exists
        """
        reports = GsReportApi.get_reports(limit=100,
                                          position_source_type='Portfolio',
                                          position_source_id=self.id,
                                          report_type='Portfolio Performance Analytics',
                                          tags=tags)

        # If tags is set to None, it returns all PPA reports for the portfolio,
        # and returning reports[0] can return any one PPA, so specifically if tags is None it means we are
        # looking for the root PPA, we need to explicitly filter out and get the one report where tags is None
        if tags is None:
            reports = [report for report in reports if report.parameters.tags is None]
        if len(reports) == 0:
            raise MqError('No performance report found.')
        return PerformanceReport.from_target(reports[0])

    def schedule_reports(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None,
                         backcast: bool = False,
                         months_per_batch: int = None):
        """
        Schedule all reports associated with a portfolio. If months_per_batch is passed and reports are historical, then
        schedule them in batches of bathc_period months. Backcasted reported can't be batched.

        :param start_date: start date of report job (optional)
        :param end_date: end date of report job (optional)
        :param backcast: true if reports should be backcasted; defaults to false
        :param months_per_batch: batch size of historical report job schedules in number of months; defaults to false
        if set, historical reports are scheduled in batches of size less than or equal to the given number of months

        **Examples**

        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> pm.schedule_reports(backcast=False)

        for a portfolio having hisotry greater than 1 yr, use months_per_batch to schedule reports in batches of
        6 months
        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> pm.schedule_reports(backcast=False, months_per_batch=6)
        """
        if months_per_batch is None or backcast:
            if backcast:
                print('Batching of schedule reports is only supported for historical reports. '
                      'Backcasted reports will be scheduled for the full date range')
            GsPortfolioApi.schedule_reports(self.__portfolio_id, start_date, end_date, backcast=backcast)
        else:
            # Process input
            if months_per_batch <= 0:
                raise MqValueError(f'Invalid input, months_per_batch {months_per_batch} should be greater than 0')

            if end_date is None or start_date is None:
                hints = self.get_schedule_dates(backcast=backcast)
                start_date = hints[0] if start_date is None else start_date
                end_date = hints[1] if end_date is None else end_date

            if start_date >= end_date:
                raise MqValueError(f'Invalid input, start date {start_date} should be before end date {end_date}')

            # Validate input date range against position dates
            position_dates = self.get_position_dates()
            position_dates = [p for p in position_dates if end_date >= p >= start_date]

            if len(position_dates) == 0:
                raise MqValueError('Portfolio does not have any positions in the given date range')

            if start_date not in position_dates:
                # There should be positions on the start date for historical reports
                raise MqError('Cannot schedule historical report because the first set of positions within the '
                              f'scheduling date range need to be on this date {start_date}')
            else:
                # preparation for the first batch
                position_dates.remove(start_date)

            if end_date not in position_dates:
                # make sure to process the last batch
                position_dates.append(end_date)

            # Create batches using sliding window
            batch_boundaries = [start_date]
            prev_date = start_date
            for i, d in enumerate(position_dates):
                current_batch = d - prev_date
                if current_batch.days > months_per_batch * 30 and i > 0:
                    # split the current window at the previous date
                    prev_date = position_dates[i - 1]
                    batch_boundaries.append(prev_date)

            batch_boundaries.append(end_date)

            # Schedule reports in batches
            print(f'Scheduling reports from {start_date} to {end_date} in {len(batch_boundaries) - 1} batches')

            for i in range(len(batch_boundaries) - 1):
                print(f'Scheduling for {batch_boundaries[i]} to {batch_boundaries[i + 1]}')
                GsPortfolioApi.schedule_reports(self.__portfolio_id,
                                                batch_boundaries[i],
                                                batch_boundaries[i + 1],
                                                backcast=backcast)
                if i > 0 and i % 10 == 0:
                    sleep(6)

    def run_reports(self,
                    start_date: dt.date = None,
                    end_date: dt.date = None,
                    backcast: bool = False,
                    is_async: bool = True,
                    months_per_batch: int = None) -> List[Union[pd.DataFrame, ReportJobFuture]]:
        """
        Run all reports associated with a portfolio

        :param start_date: start date of report job
        :param end_date: end date of report job
        :param backcast: true if reports should be backcasted; defaults to false
        :param is_async: true if reports should run asynchronously; defaults to true
        :param months_per_batch: batch size of historical report job schedules in number of months; defaults to false
        if set, historical reports are scheduled in batches of size less than or equal to the given number of months
        :return: if is_async is true, returns a list of ReportJobFuture objects; if is_async is false, returns a list
        of dataframe objects containing report results for all portfolio results

        **Examples**

        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> report_results = pm.run_reports(backcast=True)

        for longer hisotry, use months_per_batch to schedule reports in batches of 6 months
        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> pm.schedule_reports(backcast=False, months_per_batch=6)
        """
        self.schedule_reports(start_date, end_date, backcast, months_per_batch)
        reports = self.get_reports()
        report_futures = [report.get_most_recent_job() for report in reports]
        if is_async:
            return report_futures
        counter = 100
        while counter > 0:
            is_done = [future.done() for future in report_futures]
            if False not in is_done:
                return [job_future.result() for job_future in report_futures]
            sleep(6)
        raise MqValueError(f'Your reports for Portfolio {self.__portfolio_id} are taking longer than expected '
                           f'to finish. Please contact the Marquee Analytics team at '
                           f'gs-marquee-analytics-support@gs.com')

    def set_entitlements(self,
                         entitlements: Entitlements):
        """
        Set the entitlements of a portfolio

        :param entitlements: Entitlements object

        **Examples**

        >>> portfolio_admin_emails = ['LIST OF ADMIN EMAILS']
        >>> portfolio_viewer_emails = ['LIST OF VIEWER EMAILS']
        >>> admin_entitlements = EntitlementBlock(users=User.get_many(emails=portfolio_admin_emails))
        >>> view_entitlements = EntitlementBlock(users=User.get_many(emails=portfolio_viewer_emails))
        >>>
        >>> entitlements = Entitlements(
        >>>    view=view_entitlements,
        >>>    admin=admin_entitlements
        >>> )
        >>>
        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> pm.set_entitlements(entitlements)

        **See Also**
        :func: PortfolioManager.share
        :func: PortfolioManager.get_entitlements
        """
        entitlements_as_target = entitlements.to_target()
        portfolio_as_target = GsPortfolioApi.get_portfolio(self.__portfolio_id)
        portfolio_as_target.entitlements = entitlements_as_target
        GsPortfolioApi.update_portfolio(portfolio_as_target)

    def share(self, emails: List[str], admin: bool = False):
        """
        Share a portfolio with a list of emails

        :param emails: list of emails to share the portfolio with
        :param admin: true if the users should have admin access; defaults to false

        **Examples**

        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> pm.share(['EMAIL1', 'EMAIL2'])
        """
        current_entitlements = self.get_entitlements()
        users = User.get_many(emails=emails)
        found_emails = [user.email for user in users]
        if len(found_emails) != len(emails):
            missing_emails = [email for email in emails if email not in found_emails]
            raise MqValueError(f'Users with emails {missing_emails} not found')
        if admin:
            current_entitlements.admin = EntitlementBlock(users=set(current_entitlements.admin.users + users))
        current_entitlements.view = EntitlementBlock(users=set(current_entitlements.view.users + users))
        self.set_entitlements(current_entitlements)

    def set_currency(self, currency: Currency):
        """
        Set the currency of a portfolio

        :param currency: Currency
        """
        portfolio_as_target = GsPortfolioApi.get_portfolio(self.__portfolio_id)
        portfolio_as_target.currency = currency
        GsPortfolioApi.update_portfolio(portfolio_as_target)

    def get_tag_name_hierarchy(self) -> List:
        """
        Get the list of tags by name by which a portfolio's fund of funds are structured in that order

        :return: a list of tag names
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        return list(portfolio.tag_name_hierarchy) if portfolio.tag_name_hierarchy else None

    def set_tag_name_hierarchy(self, tag_names: List):
        """
        Set the list of tags by name by which a portfolio's fund of funds are structured in that order

        :param tag_names: a list of tag names in order of the new fund of funds structure
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        portfolio.tag_name_hierarchy = tag_names
        GsPortfolioApi.update_portfolio(portfolio)

    def update_portfolio_tree(self):
        """
        After a modification is made on your portfolio (reports are added/modified, the tag name hierarchy is changed,
        etc), run this function so those changes reflect across all the portfolio's sub-portfolios
        """
        GsPortfolioApi.update_portfolio_tree(self.portfolio_id)

    def get_portfolio_tree(self) -> PortfolioTree:
        """
        Get the portfolio tree of a fund of funds portfolio
        """
        return GsPortfolioApi.get_portfolio_tree(self.portfolio_id)

    def get_all_fund_of_fund_tags(self) -> List:
        """
        If the portfolio is a fund of funds, this function will retrieve a list of dictionaries of all the tag sets
        associated with the sub-portfolios in the portfolio.

        :return: a list of tags as dictionaries
        """
        tag_dicts = []
        for r in self.get_reports():
            if r.parameters.tags is not None:
                tags_as_dict = {tag.name: tag.value for tag in r.parameters.tags}
                if tags_as_dict not in tag_dicts:
                    tag_dicts.append(tags_as_dict)
        tag_dicts.sort(key=lambda dictionary: len(dictionary.keys()))
        return tag_dicts

    def get_schedule_dates(self,
                           backcast: bool = False) -> List[dt.date]:
        """
        Get recommended start and end dates for a portfolio report scheduling job

        :param backcast: true if reports should be backcasted
        :return: a list of two dates, the first is the suggested start date and the second is the suggested end date
        """
        return GsPortfolioApi.get_schedule_dates(self.id, backcast)

    @deprecation.deprecated(deprecated_in='1.0.10',
                            details='PortfolioManager.get_aum_source is now deprecated, please use '
                                    'PerformanceReport.get_aum_source instead.')
    def get_aum_source(self) -> RiskAumSource:
        """
        Get portfolio AUM Source

        :return: aum source
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        return portfolio.aum_source if portfolio.aum_source is not None else RiskAumSource.Long

    @deprecation.deprecated(deprecated_in='1.0.10',
                            details='PortfolioManager.set_aum_source is now deprecated, please use '
                                    'PerformanceReport.set_aum_source instead.')
    def set_aum_source(self,
                       aum_source: RiskAumSource):
        """
        Set portfolio AUM Source

        :param aum_source: aum source for portfolio
        :return: aum source
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        portfolio.aum_source = aum_source
        GsPortfolioApi.update_portfolio(portfolio)

    @deprecation.deprecated(deprecated_in='1.0.10',
                            details='PortfolioManager.get_custom_aum is now deprecated, please use '
                                    'PerformanceReport.get_custom_aum instead.')
    def get_custom_aum(self,
                       start_date: dt.date = None,
                       end_date: dt.date = None) -> List[CustomAUMDataPoint]:
        """
        Get AUM data for portfolio

        :param start_date: start date
        :param end_date: end date
        :return: list of AUM data between the specified range
        """
        aum_data = GsPortfolioApi.get_custom_aum(self.portfolio_id, start_date, end_date)
        return [CustomAUMDataPoint(date=dt.datetime.strptime(data['date'], '%Y-%m-%d'),
                                   aum=data['aum']) for data in aum_data]

    @deprecation.deprecated(deprecated_in='1.0.10',
                            details='PortfolioManager.get_aum is now deprecated, please use '
                                    'PerformanceReport.get_aum instead.')
    def get_aum(self,
                start_date: dt.date,
                end_date: dt.date):
        """
        Get AUM data for portfolio

        :param start_date: start date
        :param end_date: end date
        :return: dictionary of dates with corresponding AUM values
        """
        aum_source = self.get_aum_source()
        if aum_source == RiskAumSource.Custom_AUM:
            aum = self.get_custom_aum(start_date=start_date, end_date=end_date)
            return {aum_point.date.strftime('%Y-%m-%d'): aum_point.aum for aum_point in aum}
        if aum_source == RiskAumSource.Long:
            aum = self.get_performance_report().get_long_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['longExposure'] for index, row in aum.iterrows()}
        if aum_source == RiskAumSource.Short:
            aum = self.get_performance_report().get_short_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['shortExposure'] for index, row in aum.iterrows()}
        if aum_source == RiskAumSource.Gross:
            aum = self.get_performance_report().get_gross_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['grossExposure'] for index, row in aum.iterrows()}
        if aum_source == RiskAumSource.Net:
            aum = self.get_performance_report().get_net_exposure(start_date=start_date, end_date=end_date)
            return {row['date']: row['netExposure'] for index, row in aum.iterrows()}

    @deprecation.deprecated(deprecated_in='1.0.10',
                            details='PortfolioManager.upload_custom_aum is now deprecated, please use '
                                    'PerformanceReport.upload_custom_aum instead.')
    def upload_custom_aum(self,
                          aum_data: List[CustomAUMDataPoint],
                          clear_existing_data: bool = None):
        """
        Add AUM data for portfolio

        :param aum_data: list of AUM data to upload
        :param clear_existing_data: delete all previously uploaded AUM data for the portfolio (defaults to false)
        """
        formatted_aum_data = [{'date': data.date.strftime('%Y-%m-%d'), 'aum': data.aum} for data in aum_data]
        GsPortfolioApi.upload_custom_aum(self.portfolio_id, formatted_aum_data, clear_existing_data)

    @deprecation.deprecated(deprecated_in="0.9.110",
                            details="Please use the get_pnl_contribution on your portfolio's performance report using"
                                    "the PerformanceReport class")
    def get_pnl_contribution(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None,
                             currency: Currency = None,
                             tags: Dict = None) -> pd.DataFrame:
        """
        Get PnL Contribution of your portfolio broken down by constituents

        :param start_date: optional start date
        :param end_date: optional end date
        :param currency: optional currency; defaults to your portfolio's currency
        :param tags: If the portfolio is a fund of funds, pass in a dictionary corresponding to the tag values
        to retrieve results for a sub-portfolio
        :return: a Pandas DataFrame of results
        """
        performance_report_id = None if tags is None else self.get_performance_report(tags).id
        return pd.DataFrame(GsPortfolioApi.get_attribution(self.portfolio_id, start_date, end_date,
                                                           currency, performance_report_id))

    def get_macro_exposure(self,
                           model: MacroRiskModel,
                           date: dt.date,
                           factor_type: FactorType,
                           factor_categories: List[Factor] = [],
                           get_factors_by_name: bool = True,
                           tags: Dict = None,
                           return_format: ReturnFormat = ReturnFormat.DATA_FRAME
                           ) -> Union[Dict, pd.DataFrame]:
        """
        Get portfolio and asset exposure to macro factors or macro factor categories

        :param model: the macro risk model
        :param date: date for which to get exposure
        :param factor_type: whether to get exposure to factor categories or factors.
        :param factor_categories: Get portfolio exposure to these factor categories. Must be valid Factor Categories.
        If factor_type is Factor, get exposure to factors that are grouped in these factor categories.
        If empty, return exposure to all factor categories/factors.
        :param get_factors_by_name: whether to identify factors by their name or identifier
        :param tags: If the portfolio is a fund of funds, pass in a dictionary corresponding to the tag values
        to retrieve results for a sub-portfolio
        :param return_format: whether to return a dict or a pandas dataframe

        :return: a Pandas Dataframe or a Dict of portfolio exposure to macro factors

        **Examples**

        >>> model = MacroRiskModel.get(\"MODEL\")
        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> exposure_dataframe = pm.get_macro_exposure(
        >>>     model=model,
        >>>     date=dt.date(2022, 1, 1),
        >>>     factor_type=FactorType.Factor
        >>> ).sort_values(
        >>>     by=[\"Total Factor Exposure\"],
        >>>     axis=1,
        >>>     ascending=False
        >>> )
        """
        performance_report = self.get_performance_report(tags)

        # Get portfolio constituents
        constituents_and_notional_df = build_portfolio_constituents_df(performance_report, date). \
            rename(columns={"name": "Asset Name", "netExposure": "Notional"})

        # Query universe sensitivity
        universe = constituents_and_notional_df.index.dropna().tolist()
        universe_sensitivities_df = build_sensitivity_df(universe, model, date, factor_type, get_factors_by_name)

        # Remove assets without exposure
        assets_with_exposure = list(universe_sensitivities_df.index.values)
        if not assets_with_exposure:
            logging.warning("The Portfolio is not exposed to any of the requested macro factors")
            return pd.DataFrame()

        constituents_and_notional_df = constituents_and_notional_df.loc[assets_with_exposure]

        factor_data = model.get_factor_data(date, date, factor_type=FactorType.Factor) \
            if factor_type == FactorType.Factor else pd.DataFrame()
        exposure_df = build_exposure_df(constituents_and_notional_df, universe_sensitivities_df,
                                        factor_categories, factor_data, get_factors_by_name)

        if return_format == ReturnFormat.JSON:
            return exposure_df.to_dict()

        return exposure_df

    def get_factor_scenario_analytics(self,
                                      scenarios: List[FactorScenario],
                                      date: dt.date,
                                      measures: List[ScenarioCalculationMeasure],
                                      risk_model: str = None,
                                      return_format: ReturnFormat = ReturnFormat.DATA_FRAME) -> \
            Union[Dict, Union[Dict, pd.DataFrame]]:
        """Given a list of factor scenarios (historical simulation and/or custom shocks), return the estimated pnl
         of the given positioned entity.
         :param scenarios: List of factor-based scenarios
         :param date: date to run scenarios.
         :param measures: which metrics to return
         :param risk_model: valid risk model ID
         :param return_format: whether to return data formatted in a dataframe or as a dict

          **Examples**

            >>> from gs_quant.session import GsSession, Environment
            >>> from gs_quant.markets.portfolio_manager import PortfolioManager, ReturnFormat
            >>> from gs_quant.entities.entity import ScenarioCalculationMeasure, PositionedEntity
            >>> from gs_quant.markets.scenario import Scenario

          Get scenarios
            >>> covid_19_omicron = Scenario.get_by_name("Covid 19 Omicron (v2)") # historical simulation
            >>> custom_shock = Scenario.get_by_name("Shocking factor by x% (Propagated)") # custom shock
            >>> risk_model = "RISK_MODEL_ID" # valid risk model ID

          Instantiate your positionedEntity. Here, we are using one of its subclasses, PortfolioManager

            >>> pm = PortfolioManager(portfolio_id="PORTFOLIO_ID")

          Set the date you wish to run your scenario on

           >>> date = dt.date(2023, 3, 7)

          Run scenario and get estimated impact on your positioned entity

          >>> scenario_analytics = pm.get_factor_scenario_analytics(
          ...     scenarios=[covid_19_omicron, beta_propagated],
          ...     date=date,
          ...     measures=[ScenarioCalculationMeasure.SUMMARY,
          ...               ScenarioCalculationMeasure.ESTIMATED_FACTOR_PNL,
          ...               ScenarioCalculationMeasure.ESTIMATED_PNL_BY_SECTOR,
          ...               ScenarioCalculationMeasure.ESTIMATED_PNL_BY_REGION,
          ...               ScenarioCalculationMeasure.ESTIMATED_PNL_BY_DIRECTION,
          ...               ScenarioCalculationMeasure.ESTIMATED_PNL_BY_ASSET],
          ...     risk_model=risk_model)

          By default, the result will be returned in a dict with keys as the measures/metrics requested and values as
          the scenario calculation results formatted in a dataframe. To get the results in a dict, specify the return
          format as JSON
         """

        return super().get_factor_scenario_analytics(scenarios, date, measures, risk_model, return_format)

    def get_risk_model_predicted_beta(self, start_date: dt.date, end_date: dt.date, risk_model_id: str,
                                      default_beta_value: int = 1, tags: Dict = None) -> pd.DataFrame:
        """
        Get the predicted beta of a portfolio as estimated by the provided risk model.
        The beta is calculated using the factor risk model data. The function retrieves the factor risk report
        associated with the portfolio and the risk model ID, and then calculates the predicted beta for each date
        in the specified range.

        :param start_date: Start date for the beta calculation
        :param end_date: End date for the beta calculation
        :param risk_model_id: Risk model ID to be used for the calculation
        :param default_beta_value: Default beta value to be used if no data is available for a specific date
        :param tags: If the portfolio is a fund of funds, pass in a dictionary corresponding to the tag values
        to retrieve results for a sub-portfolio

        :return: A DataFrame containing the predicted beta for each date in the specified range

        **Examples**
        >>> pm = PortfolioManager("PORTFOLIO ID")
        >>> beta_df = pm.get_risk_model_predicted_beta(start_date=dt.date(2023, 1, 1),
        ... end_date=dt.date(2023, 12, 31), risk_model_id="RISK_MODEL_ID")
        >>> print(beta_df)
        >>> # Output:

        date        beta
        2023-01-01  1.05
        2023-01-02  1.10
        2023-01-03  1.02
        """
        performance_report = self.get_performance_report(tags=tags)
        risk_model = FactorRiskModel.get(risk_model_id)
        risk_model_dates: List[dt.date] = risk_model.get_dates(start_date=start_date, end_date=end_date)
        batched_dates = get_batched_dates(risk_model_dates, batch_size=10)
        risk_model_predicted_beta_timeseries = pd.DataFrame()
        asset_level_betas = pd.DataFrame()
        portfolio_position_net_weights = pd.DataFrame()
        for batch in batched_dates:
            start_date, end_date = batch[0], batch[-1]
            try:
                date_wise_net_weight = performance_report.get_position_net_weights(start_date=start_date,
                                                                                   end_date=end_date,
                                                                                   asset_metadata_fields=["gsid"],
                                                                                   include_all_business_days=True,
                                                                                   position_type=PositionType.CLOSE)
                date_wise_net_weight = date_wise_net_weight.dropna().pivot_table(index='positionDate', columns='gsid',
                                                                                 values='netWeight', aggfunc='sum')
                portfolio_position_gsids = [gsid for gsid in date_wise_net_weight.columns.tolist() if gsid is not None]
                asset_level_betas_batch = (risk_model
                                           .get_predicted_beta(start_date=start_date, end_date=end_date,
                                                               assets=RiskModelDataAssetsRequest(
                                                                   identifier=RiskModelUniverseIdentifierRequest.gsid,
                                                                   universe=tuple(portfolio_position_gsids))))
                if asset_level_betas_batch.isna().all().all():
                    logging.warning(
                        f"Risk model predicted beta not available for risk model {risk_model_id} for dates: {batch}")
                    continue
                else:
                    asset_level_betas = pd.concat([asset_level_betas, asset_level_betas_batch], axis=0)
                    portfolio_position_net_weights = pd.concat([portfolio_position_net_weights,
                                                                date_wise_net_weight], axis=0)
            except Exception as ex:
                raise MqError(
                    f"Risk model predicted beta cannot be calculated for risk model {risk_model_id} "
                    f"from {start_date} to {end_date} because of exception: {ex}, traceback: {traceback.format_exc()}")
        if asset_level_betas.empty:
            return pd.DataFrame()
        asset_level_betas.fillna(default_beta_value, inplace=True)
        risk_model_predicted_beta_timeseries = asset_level_betas * portfolio_position_net_weights
        risk_model_predicted_beta_timeseries = (risk_model_predicted_beta_timeseries.sum(axis=1).rename('beta').
                                                replace({0: np.nan}).ffill())
        return risk_model_predicted_beta_timeseries.reset_index().rename(columns={'index': 'date', 0: 'beta'})
