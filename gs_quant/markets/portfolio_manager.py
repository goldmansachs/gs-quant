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
from time import sleep
from typing import List, Union, Dict

import pandas as pd

from gs_quant.api.gs.portfolios import GsPortfolioApi
from gs_quant.api.gs.reports import GsReportApi
from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.entities.entitlements import Entitlements
from gs_quant.entities.entity import PositionedEntity, EntityType
from gs_quant.errors import MqError
from gs_quant.errors import MqValueError
from gs_quant.markets.factor import Factor
from gs_quant.markets.report import PerformanceReport
from gs_quant.markets.report import ReportJobFuture
from gs_quant.markets.portfolio_manager_utils import build_exposure_df, build_portfolio_constituents_df, \
    build_sensitivity_df, build_macro_portfolio_exposure_df
from gs_quant.models.risk_model import MacroRiskModel, ReturnFormat, FactorType, DataAssetsRequest, \
    RiskModelUniverseIdentifierRequest as UniverseIdentifierRequest
from gs_quant.target.common import Currency
from gs_quant.target.portfolios import RiskAumSource
import deprecation

_logger = logging.getLogger(__name__)


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

    def get_performance_report(self) -> PerformanceReport:
        """
        Get performance report associated with a portfolio

        :return: returns the PerformanceReport associated with portfolio if one exists
        """
        reports = GsReportApi.get_reports(limit=100,
                                          position_source_type='Portfolio',
                                          position_source_id=self.id,
                                          report_type='Portfolio Performance Analytics')
        if len(reports) == 0:
            raise MqError('This portfolio has no performance report.')
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
                print(f'Scheduling for {batch_boundaries[i]} to {batch_boundaries[i+1]}')
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
        """
        entitlements_as_target = entitlements.to_target()
        portfolio_as_target = GsPortfolioApi.get_portfolio(self.__portfolio_id)
        portfolio_as_target.entitlements = entitlements_as_target
        GsPortfolioApi.update_portfolio(portfolio_as_target)

    def get_schedule_dates(self,
                           backcast: bool = False) -> List[dt.date]:
        """
        Get recommended start and end dates for a portfolio report scheduling job

        :param backcast: true if reports should be backcasted
        :return: a list of two dates, the first is the suggested start date and the second is the suggested end date
        """
        return GsPortfolioApi.get_schedule_dates(self.id, backcast)

    def get_aum_source(self) -> RiskAumSource:
        """
        Get portfolio AUM Source

        :return: aum source
        """
        portfolio = GsPortfolioApi.get_portfolio(self.portfolio_id)
        return portfolio.aum_source if portfolio.aum_source is not None else RiskAumSource.Long

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

    def get_pnl_contribution(self,
                             start_date: dt.date = None,
                             end_date: dt.date = None,
                             currency: Currency = None) -> pd.DataFrame:
        """
        Get PnL Contribution of your portfolio broken down by constituents

        :param start_date: optional start date
        :param end_date: optional end date
        :param currency: optional currency; defaults to your portfolio's currency
        :return: a Pandas DataFrame of results
        """
        return pd.DataFrame(GsPortfolioApi.get_attribution(self.portfolio_id, start_date, end_date, currency))

    @deprecation.deprecated(deprecated_in="0.9.39",
                            details="Please use get_macro_exposure instead")
    def get_macro_exposure_table(self,
                                 macro_risk_model: MacroRiskModel,
                                 date: dt.date,
                                 factors: List[str] = [],
                                 factors_by_name: bool = True,
                                 group_by_factor_category: bool = False,
                                 return_format: ReturnFormat = ReturnFormat.DATA_FRAME
                                 ) -> Union[Dict, pd.DataFrame]:
        """
        Get portfolio and asset exposure to macro factors

        :param macro_risk_model: the macro risk model
        :param date: date for which to get exposure
        :param factors: macro factors to get portfolio and asset exposure for.
        If empty, return exposure for all factors in the macro risk model
        :param factors_by_name: whether to identify factors by their name or identifier
        :param group_by_factor_category: whether to return results with factors grouped within their respective
        categories.
        :param return_format: whether to return a dict or a pandas dataframe
        :return: a Pandas Dataframe or a Dict of portfolio exposure to macro factors
        """

        performance_report = self.get_performance_report()

        constituents_df = performance_report.get_portfolio_constituents(fields=['netExposure'],
                                                                        start_date=date,
                                                                        end_date=date)
        if constituents_df.empty:
            raise MqValueError(f"Macro Exposure can't be calculated as the portfolio constituents could not be found on"
                               f" the requested date {date}. Make sure the portfolio performance report is up-to-date.")
        constituents_df = constituents_df.dropna()
        constituents_df = constituents_df.loc[:, ["assetId", "netExposure"]]
        constituents_df = constituents_df.set_index("assetId")
        constituents_df.index.name = "Asset Identifier"

        assets_data = GsAssetApi.get_many_assets_data_scroll(fields=['name', 'gsid', 'id'],
                                                             as_of=dt.datetime(date.year, date.month, date.day),
                                                             limit=1000,
                                                             id=constituents_df.index.tolist())
        df_assets_data = pd.DataFrame.from_records(assets_data).set_index("id"). \
            fillna(value={"name": "Name not available"})
        df_assets_data.index.name = "Asset Identifier"

        # Merge the constituents dataframe and asset data dataframe to get gsid, name, notional
        constituents_and_notional_df = df_assets_data.merge(constituents_df, on='Asset Identifier')
        constituents_and_notional_df = constituents_and_notional_df.reset_index(drop=True).set_index("gsid")
        universe = constituents_and_notional_df.index.dropna().tolist()
        constituents_and_notional_df.index.name = 'Asset Identifier'
        constituents_and_notional_df = constituents_and_notional_df.sort_index()

        # Query universe sensitivity
        universe_sensitivities_df = macro_risk_model.get_universe_sensitivity(start_date=date,
                                                                              end_date=date,
                                                                              assets=DataAssetsRequest(
                                                                                  UniverseIdentifierRequest.gsid,
                                                                                  universe),
                                                                              factor_type=FactorType.Factor)
        if universe_sensitivities_df.empty:
            print(f"None of the assets in the portfolio are exposed to the macro factors in model "
                  f"{macro_risk_model.id} ")
            return pd.DataFrame()
        universe_sensitivities_df = universe_sensitivities_df.reset_index(level=1, drop=True)
        universe_sensitivities_df.index.name = 'Asset Identifier'
        universe_sensitivities_df = universe_sensitivities_df.sort_index()

        factors_in_model = macro_risk_model.get_many_factors()
        if factors:
            factor_dict = {f.id: f.name for f in factors_in_model if f.name in factors} \
                if factors_by_name else {f.id: f.name for f in factors_in_model if f.id in factors}
            wrong_factors = list(set(factors) - set(factor_dict.values())) if factors_by_name else \
                list(set(factors) - set(factor_dict.keys()))
            if wrong_factors:
                identifier = "name" if factors_by_name else "identifier"
                print(f"The following factors with {identifier}(s) {', '.join(wrong_factors)} could not be found")
        else:
            factor_dict = {f.id: f.name for f in factors_in_model}

        factor_category_dict = {}
        if group_by_factor_category:
            factor_category_dict = {f.name: f.category for f in factors_in_model} if factors_by_name else \
                {f.id: f.category for f in factors_in_model}

        exposure_df = build_macro_portfolio_exposure_df(
            constituents_and_notional_df, universe_sensitivities_df, factor_dict, factor_category_dict, factors_by_name)

        if return_format == ReturnFormat.JSON:
            return exposure_df.to_dict()

        return exposure_df

    def get_macro_exposure(self,
                           model: MacroRiskModel,
                           date: dt.date,
                           factor_type: FactorType,
                           factor_categories: List[Factor] = [],
                           get_factors_by_name: bool = True,
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
        performance_report = self.get_performance_report()

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
