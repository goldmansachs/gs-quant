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
from enum import auto
from typing import List, Dict, Union
import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.risk_models import GsFactorRiskModelApi, GsRiskModelApi
from gs_quant.models.factor_risk_model_utils import build_asset_data_map, build_factor_data_map, \
    build_factor_data_dataframe, build_pfp_data_dataframe, get_isc_dataframe, get_covariance_matrix_dataframe, \
    get_closest_date_index, divide_request, batch_and_upload_partial_data
from gs_quant.target.common import Enum
from gs_quant.target.risk_models import RiskModel as RiskModelBuilder
from gs_quant.target.risk_models import RiskModelData, RiskModelCalendar, RiskModelFactor, \
    DataAssetsRequest, Measure, CoverageType, UniverseIdentifier, Entitlements, Term


class ReturnFormat(Enum):
    """Alternative format for data to be returned from get_data functions"""
    JSON = auto()
    DATA_FRAME = auto()


class RiskModel:
    """ Risk Model Class """

    def __init__(self, model_id: str):
        model = GsRiskModelApi.get_risk_model(model_id)
        self.__id: str = model.id
        self.__name: str = model.name
        self.__description: str = model.description
        self.__entitlements: Entitlements = model.entitlements if type(model.entitlements) == Entitlements or not \
            model.entitlements else Entitlements.from_dict(model.entitlements)

    @property
    def id(self) -> str:
        """ Retrieve risk model id for existing risk model """
        return self.__id

    @property
    def name(self) -> str:
        """ Retrieve risk model name for existing risk model """
        return self.__name

    @name.setter
    def name(self, name: str):
        """ Set risk model name for existing risk model """
        self.__name = name

    @property
    def description(self) -> str:
        """ Retrieve risk model description for existing risk model """
        return self.__description

    @description.setter
    def description(self, description: str):
        """ Sets description for existing risk model """
        self.__description = description

    @property
    def entitlements(self) -> Entitlements:
        """ Gets entitlements for existing risk model """
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, entitlements: Union[Entitlements, Dict]):
        """ Sets entitlements for existing risk model """
        self.__entitlements = entitlements

    def add_entitlements(self, entitlements: Union[Entitlements, Dict]):
        """ Adds entitlements for existing risk model """
        entitlements = Entitlements.from_dict(entitlements) if type(entitlements) == dict else entitlements
        edit = self.__entitlements.edit
        for user in entitlements.edit:
            if user not in edit:
                edit += user,
        admin = self.__entitlements.admin
        for user in entitlements.admin:
            if user not in edit:
                admin += user,
        query = self.__entitlements.query
        for user in entitlements.query:
            if user not in query:
                query += user,
        upload = self.__entitlements.upload
        for user in entitlements.upload:
            if user not in upload:
                upload += user,
        view = self.__entitlements.view
        for user in entitlements.view:
            if user not in view:
                view += user,
        execute = self.__entitlements.execute
        for user in entitlements.execute:
            if user not in execute:
                execute += user,
        combined_entitlements = Entitlements(
            edit=edit,
            admin=admin,
            query=query,
            upload=upload,
            view=view,
            execute=execute
        )
        self.entitlements = combined_entitlements

    def remove_entitlements(self, entitlements: Union[Entitlements, Dict]):
        """ Removes entitlements for existing risk model """
        entitlements = Entitlements.from_dict(entitlements) if type(entitlements) == dict else entitlements
        model = GsRiskModelApi.get_risk_model(self.__id)
        edit_ls = list(model.entitlements.edit)
        for edit in entitlements.edit:
            edit_ls.remove(edit)
        admin_ls = list(model.entitlements.admin)
        for admin in entitlements.admin:
            admin_ls.remove(admin)
        query_ls = list(model.entitlements.query)
        for query in entitlements.query:
            query_ls.remove(query)
        upload_ls = list(model.entitlements.upload)
        for upload in entitlements.upload:
            upload_ls.remove(upload)
        view_ls = list(model.entitlements.view)
        for view in entitlements.view:
            view_ls.remove(view)
        execute_ls = list(model.entitlements.execute)
        for execute in entitlements.execute:
            execute_ls.remove(execute)
        removed_entitlements = Entitlements(
            edit=tuple(edit_ls),
            admin=tuple(admin_ls),
            query=tuple(query_ls),
            upload=tuple(upload_ls),
            view=tuple(view_ls),
            execute=tuple(execute_ls)
        )
        self.entitlements = removed_entitlements

    def delete(self):
        """ Delete existing risk model """
        return GsRiskModelApi.delete_risk_model(self.id)

    def get_dates(self, start_date: dt.date = None, end_date: dt.date = None) -> List:
        """ Retrieve risk model dates for existing risk model
            :param start_date: list returned including and after start_date
            :param end_date: list returned up to and including end_date """
        return GsRiskModelApi.get_risk_model_dates(self.id, start_date, end_date)

    def get_calendar(self, start_date: dt.date = None, end_date: dt.date = None) -> RiskModelCalendar:
        """ Retrieve risk model calendar for existing risk model between start and end date
            :param start_date: list returned including and after start_date
            :param end_date: list returned up to and including end_date """
        calendar = GsRiskModelApi.get_risk_model_calendar(self.id)
        if not start_date and not end_date:
            return calendar
        start_idx = get_closest_date_index(start_date, calendar.business_dates, 'after') if start_date else 0
        end_idx = get_closest_date_index(end_date, calendar.business_dates, 'before') if end_date else len(
            calendar.business_dates)
        return RiskModelCalendar(calendar.business_dates[start_idx:end_idx + 1])

    def upload_calendar(self, calendar: RiskModelCalendar):
        """ Upload risk model calendar to existing risk model
            :param calendar: RiskModelCalendar containing list of dates where model data is expected"""
        return GsRiskModelApi.upload_risk_model_calendar(self.id, calendar)

    def get_missing_dates(self, end_date: dt.date = None):
        """ Takes in a risk model id and returns any dates where data is not published according to expected days
                returned from the risk model calendar
            :param end_date: date to truncate missing dates at

            If no end_date is provided, end_date defaults to the most recent business date according
                to the risk model calendar """
        posted_results = self.get_dates()
        if not end_date:
            end_date = dt.date.today() - dt.timedelta(days=1)
        calendar = self.get_calendar(
            start_date=dt.datetime.strptime((posted_results[0]), '%Y-%m-%d').date(),
            end_date=end_date).business_dates
        return [date for date in calendar if date not in posted_results]

    def get_most_recent_date_from_calendar(self) -> dt.date:
        """Returns most recent date in calendar from and including yesterday"""
        yesterday = dt.date.today() - dt.timedelta(1)
        calendar = self.get_calendar(end_date=yesterday).business_dates
        return dt.datetime.strptime(calendar[len(calendar) - 1], '%Y-%m-%d').date()


class FactorRiskModel(RiskModel):
    """ Factor Risk Model used for calculating asset level factor risk"""

    def __init__(self, model_id: str):
        super().__init__(model_id)
        model = GsRiskModelApi.get_risk_model(model_id)
        self.__coverage: Union[CoverageType, str] = model.coverage
        self.__term: Union[Term, str] = model.term
        self.__universe_identifier: Union[UniverseIdentifier, str] = model.universe_identifier
        self.__vendor: str = model.vendor
        self.__version: float = model.version

    @property
    def vendor(self) -> str:
        """ Retrieve risk model vendor for existing risk model """
        return self.__vendor

    @vendor.setter
    def vendor(self, vendor):
        """ Sets risk model vendor for existing risk model """
        self.__vendor = vendor

    @property
    def universe_identifier(self) -> str:
        """ Retrieve risk model universe identifier for existing risk model """
        return self.__universe_identifier

    @property
    def term(self) -> str:
        """ Retrieve risk model term for existing risk model """
        return self.__term

    @term.setter
    def term(self, term: Union[Term, str]):
        """ Set term for existing risk model """
        self.__term = term

    @property
    def version(self) -> float:
        """ Retrieve risk model version for existing risk model """
        return self.__version

    @version.setter
    def version(self, version: float):
        """ Set version for existing risk model """
        self.__version = version

    @property
    def coverage(self) -> str:
        """ Retrieve risk model coverage for existing risk model """
        return self.__coverage

    @coverage.setter
    def coverage(self, coverage: Union[CoverageType, str]):
        """ Sets risk model coverage for existing risk model """
        self.__coverage = coverage

    @classmethod
    def create(cls,
               coverage: Union[CoverageType, str],
               id_: str,
               name: str,
               term: Union[Term, str],
               universe_identifier: Union[UniverseIdentifier, str],
               vendor: str,
               version: float,
               entitlements: Union[Entitlements, Dict] = None,
               description: str = None):
        """ Creates new factor risk model and uploads factor risk model object to Marquee
            :param coverage: coverage of risk model asset universe
            :param id_: risk model id (cannot be changed)
            :param name: risk model name
            :param term: horizon term
            :param universe_identifier: identifier used in asset universe upload (cannot be changed)
            :param vendor: risk model vendor
            :param version: version of model
            :param entitlements: entitlements associated with risk model
            :param description: risk model description
            :return: Factor Risk Model object  """
        new_model = RiskModelBuilder(coverage, id_, name, term, universe_identifier, vendor, version,
                                     entitlements=entitlements, description=description)
        GsRiskModelApi.create_risk_model(new_model)
        return FactorRiskModel(id_)

    def update(self):
        """ Updates factor risk model object on Marquee """
        updated_model = RiskModelBuilder(self.coverage, self.id, self.name, self.term, self.universe_identifier,
                                         self.vendor, self.version, description=self.description,
                                         entitlements=self.entitlements)
        GsRiskModelApi.update_risk_model(updated_model)

    def get_factor(self, factor_id: str) -> RiskModelFactor:
        """ Retrieve risk model factor from model and factor ids
            :param factor_id: factor identifier associated with risk model
            :return: Risk Model Factor object """
        return GsFactorRiskModelApi.get_risk_model_factor(self.id, factor_id)

    def create_factor(self, factor: RiskModelFactor) -> RiskModelFactor:
        """ Create a new risk model factor
            :param factor: factor object
            :return: Risk Model Factor object """
        return GsFactorRiskModelApi.create_risk_model_factor(self.id, factor)

    def update_factor(self, factor_id: str, factor: RiskModelFactor) -> RiskModelFactor:
        """ Update existing risk model factor
            :param factor_id: factor identifier associated with risk model to update
            :param factor: factor object associated with risk model
            :return: Risk Model Factor object """
        return GsFactorRiskModelApi.update_risk_model_factor(self.id, factor_id, factor)

    def delete_factor(self, factor_id: str):
        """ Delete a risk model factor
            :param factor_id: factor identifier associated with risk model to delete """
        GsFactorRiskModelApi.delete_risk_model_factor(self.id, factor_id)

    def get_factor_data(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        identifiers: List[str] = None,
                        include_performance_curve: bool = False,
                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve factor data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param identifiers: list of factor ids associated with risk model
            :param include_performance_curve: request to include the performance curve of the factors
            :param format: which format to return the results in
            :return: risk model factor data """
        factor_data = GsFactorRiskModelApi.get_risk_model_factor_data(
            self.id,
            start_date,
            end_date,
            identifiers,
            include_performance_curve
        )
        if format == ReturnFormat.DATA_FRAME:
            factor_data = pd.DataFrame(factor_data)
        return factor_data

    def get_asset_universe(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve asset universe data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: risk model universe """

        if not assets.universe and not end_date:
            end_date = start_date
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        dates = [dt.datetime.strptime((data.get('date')), '%Y-%m-%d').date() for data in results]
        universe = [data.get('assetData').get('universe') for data in results]
        dates_to_universe = dict(zip(dates, universe))
        if format == ReturnFormat.DATA_FRAME:
            dates_to_universe = pd.DataFrame(dates_to_universe)
        return dates_to_universe

    def get_historical_beta(self,
                            start_date: dt.date,
                            end_date: dt.date = None,
                            assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                            format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve historical beta data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: historical beta for assets requested """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Historical_Beta, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
        historical_beta = build_asset_data_map(results, universe, 'historicalBeta')
        if format == ReturnFormat.DATA_FRAME:
            historical_beta = pd.DataFrame(historical_beta)
        return historical_beta

    def get_total_risk(self,
                       start_date: dt.date,
                       end_date: dt.date = None,
                       assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                       format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve total risk data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: total risk for assets requested """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Total_Risk, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
        total_risk = build_asset_data_map(results, universe, 'totalRisk')
        if format == ReturnFormat.DATA_FRAME:
            total_risk = pd.DataFrame(total_risk)
        return total_risk

    def get_specific_risk(self,
                          start_date: dt.date,
                          end_date: dt.date = None,
                          assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                          format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve specific risk data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: specific risk for assets requested """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Specific_Risk, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
        specific_risk = build_asset_data_map(results, universe, 'specificRisk')
        if format == ReturnFormat.DATA_FRAME:
            specific_risk = pd.DataFrame(specific_risk)
        return specific_risk

    def get_residual_variance(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve residual variance data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: residual variance for assets requested """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Residual_Variance, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
        residual_variance = build_asset_data_map(results, universe, 'residualVariance')
        if format == ReturnFormat.DATA_FRAME:
            residual_variance = pd.DataFrame(residual_variance)
        return residual_variance

    def get_universe_factor_exposure(self,
                                     start_date: dt.date,
                                     end_date: dt.date = None,
                                     assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                                     format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Retrieve universe factor exposure data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: factor exposure for assets requested """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
        factor_exposure = build_asset_data_map(results, universe, 'factorExposure')
        if format == ReturnFormat.DATA_FRAME:
            factor_exposure = pd.DataFrame.from_dict(
                {(i, j): factor_exposure[i][j]
                 for i in factor_exposure.keys()
                 for j in factor_exposure[i].keys()},
                orient='index'
            )
        return factor_exposure

    def get_factor_returns_by_name(self,
                                   start_date: dt.date,
                                   end_date: dt.date = None,
                                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve factor return data for existing risk model keyed by name
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param format: which format to return the results in
            :return: factor returns by name """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=None,
            measures=[Measure.Factor_Return, Measure.Factor_Name, Measure.Factor_Id],
            limit_factors=False
        ).get('results')
        factor_data = build_factor_data_dataframe(results, 'factorName') if \
            format == ReturnFormat.DATA_FRAME else build_factor_data_map(results, 'factorName')
        return factor_data

    def get_factor_returns_by_id(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve factor return data for existing risk model keyed by factor id
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param format: which format to return the results in
            :return: factor returns by factor id """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=None,
            measures=[Measure.Factor_Return, Measure.Factor_Name, Measure.Factor_Id],
            limit_factors=False
        ).get('results')
        factor_data = build_factor_data_dataframe(results, 'id') if format == ReturnFormat.DATA_FRAME else \
            build_factor_data_map(results, 'id')
        return factor_data

    def get_covariance_matrix(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve covariance matrix data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param format: which format to return the results in
            :return: covariance matrix of daily factor returns """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=None,
            measures=[Measure.Covariance_Matrix, Measure.Factor_Name, Measure.Factor_Id],
            limit_factors=False
        ).get('results')
        covariance_data = results if format == ReturnFormat.JSON else get_covariance_matrix_dataframe(results)
        return covariance_data

    def get_issuer_specific_covariance(self,
                                       start_date: dt.date,
                                       end_date: dt.date = None,
                                       assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                                       format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve issuer specific covariance data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: issuer specific covariance matrix (covariance of assets with the same issuer) """
        isc = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Issuer_Specific_Covariance],
            limit_factors=False
        ).get('results')
        isc_data = isc if format == ReturnFormat.JSON else get_isc_dataframe(isc)
        return isc_data

    def get_factor_portfolios(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Retrieve factor portfolios data for existing risk model
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param format: which format to return the results in
            :return: factor portfolios data """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Factor_Portfolios],
            limit_factors=False
        ).get('results')
        pfp_data = results if format == ReturnFormat.JSON else build_pfp_data_dataframe(results)
        return pfp_data

    def get_data(self,
                 measures: List[Measure],
                 start_date: dt.date,
                 end_date: dt.date = None,
                 assets: DataAssetsRequest = DataAssetsRequest(UniverseIdentifier.gsid, []),
                 limit_factors: bool = True) -> Dict:
        """ Retrieve data for multiple measures for existing risk model
            :param measures: list of measures for general risk model data request
            :param start_date: start date for data request
            :param end_date: end date for data request
            :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
            :param limit_factors: limit factors included in factorData and covariance matrix to only include factors
                which the input universe has non-zero exposure to
            :return: factor portfolios data """
        return GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
        )

    def upload_data(self, data: Union[RiskModelData, Dict]):
        """ Upload risk model data to existing risk model
            :param data: complete risk model data for uploading on given date
                includes: date, factorData, assetData, covarianceMatrix with optional inputs:
                issuerSpecificCovariance and factorPortfolios

            If upload universe is over 20000 assets, will batch and upload data in chunks of 20000 assets """

        data = data.to_json() if type(data) == RiskModelData else data
        target_universe_size = len(data.get('assetData').get('universe'))
        if target_universe_size > 20000:
            print('Batching uploads due to universe size')
            batch_and_upload_partial_data(self.id, data)
        else:
            print(GsFactorRiskModelApi.upload_risk_model_data(self.id, data))

    def upload_partial_data(self, data: RiskModelData, target_universe_size: float = None):
        """ Upload partial risk model data to existing risk model
            :param data: partial risk model data for uploading on given date
            :param target_universe_size: the size of the complete universe on date

            The models factorData and covarianceMatrix must be uploaded first on given date if repeats in partial
                upload, newer posted data will replace existing data on upload day """
        print(GsFactorRiskModelApi.upload_risk_model_data(
            self.id,
            data,
            partial_upload=True,
            target_universe_size=target_universe_size)
        )

    def upload_asset_coverage_data(self, date: dt.date = None):
        """ Upload to the coverage dataset for given risk model and date
            :param date: date to upload coverage data for, default date is last date from risk model calendar

            Posting to the coverage dataset within in the last 5 days will enable the risk model to be seen in the
                Marquee UI dropdown for users with "execute" capabilities """
        if not date:
            date = self.get_dates()[-1]
        update_time = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        gsid_list = self.get_asset_universe(
            date, assets=DataAssetsRequest('gsid', []), format=ReturnFormat.JSON).get(date)
        request_array = [{'date': date.strftime('%Y-%m-%d'),
                          'gsid': gsid,
                          'riskModel': self.id,
                          'updateTime': update_time} for gsid in set(gsid_list)]
        list_of_requests = list(divide_request(request_array, 1000))
        for request_set in list_of_requests:
            print(GsDataApi.upload_data('RISK_MODEL_ASSET_COVERAGE', request_set))
