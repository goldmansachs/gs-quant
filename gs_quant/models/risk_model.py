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
from enum import auto, Enum
from typing import List, Dict, Tuple, Union

import pandas as pd

from gs_quant.api.gs.data import GsDataApi
from gs_quant.api.gs.risk_models import GsFactorRiskModelApi, GsRiskModelApi
from gs_quant.errors import MqValueError, MqRequestError
from gs_quant.markets.factor import Factor
from gs_quant.models.factor_risk_model_utils import build_asset_data_map, build_factor_data_map, \
    build_factor_data_dataframe, build_pfp_data_dataframe, get_isc_dataframe, get_covariance_matrix_dataframe, \
    get_closest_date_index, divide_request, batch_and_upload_partial_data, risk_model_data_to_json, get_universe_size
from gs_quant.target.risk_models import RiskModel as RiskModelBuilder, RiskModelEventType
from gs_quant.target.risk_models import RiskModelData, RiskModelCalendar, RiskModelFactor, \
    DataAssetsRequest, Measure, CoverageType, UniverseIdentifier, Entitlements, Term, \
    RiskModelUniverseIdentifierRequest, FactorType


class ReturnFormat(Enum):
    """Alternative format for data to be returned from get_data functions"""
    JSON = auto()
    DATA_FRAME = auto()


class RiskModel:
    """ Risk Model Class """

    def __init__(self,
                 id_: str,
                 name: str,
                 entitlements: Union[Dict, Entitlements] = None,
                 description: str = None):
        self.__id: str = id_
        self.__name: str = name
        self.__description: str = description
        self.__entitlements: Entitlements = entitlements if entitlements and isinstance(entitlements, Entitlements) \
            else Entitlements.from_dict(entitlements) if entitlements and isinstance(entitlements, Dict) else None

    @property
    def id(self) -> str:
        """ Get risk model id """
        return self.__id

    @property
    def name(self) -> str:
        """ Get risk model name """
        return self.__name

    @name.setter
    def name(self, name: str):
        """ Set risk model name """
        self.__name = name

    @property
    def description(self) -> str:
        """ Get risk model description """
        return self.__description

    @description.setter
    def description(self, description: str):
        """ Set risk model description """
        self.__description = description

    @property
    def entitlements(self) -> Entitlements:
        """ Get risk model entitlements """
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, entitlements: Union[Entitlements, Dict]):
        """ Set risk model entitlements """
        self.__entitlements = entitlements

    def delete(self):
        """ Delete existing risk model object from Marquee """
        return GsRiskModelApi.delete_risk_model(self.id)

    def get_dates(self, start_date: dt.date = None, end_date: dt.date = None, event_type: RiskModelEventType = None) \
            -> List[dt.date]:
        """ Get risk model dates for existing risk model

        :param start_date: list returned including and after start_date
        :param end_date: list returned up to and including end_date
        :param event_type: which event type to retrieve

        :return: list of dates where risk model data is present
        """
        return [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in
                GsRiskModelApi.get_risk_model_dates(self.id, start_date, end_date, event_type=event_type)]

    def get_calendar(self, start_date: dt.date = None, end_date: dt.date = None) -> RiskModelCalendar:
        """ Get risk model calendar for existing risk model between start and end date

        :param start_date: list returned including and after start_date
        :param end_date: list returned up to and including end_date

        :return: RiskModelCalendar for model
        """
        calendar = GsRiskModelApi.get_risk_model_calendar(self.id)
        if not start_date and not end_date:
            return calendar
        start_idx = get_closest_date_index(start_date, calendar.business_dates, 'after') if start_date else 0
        end_idx = get_closest_date_index(end_date, calendar.business_dates, 'before') if end_date else len(
            calendar.business_dates)
        return RiskModelCalendar(calendar.business_dates[start_idx:end_idx + 1])

    def upload_calendar(self, calendar: RiskModelCalendar):
        """ Upload risk model calendar to existing risk model

        :param calendar: RiskModelCalendar containing list of dates where model data is expected
        """
        return GsRiskModelApi.upload_risk_model_calendar(self.id, calendar)

    def get_missing_dates(self, start_date: dt.date = None, end_date: dt.date = None) -> List[dt.date]:
        """ Get any dates where data is not published according to expected days returned from the risk model calendar

        :param end_date: date to truncate missing dates at

            If no end_date is provided, end_date defaults to T-1 date according
                to the risk model calendar
        """

        posted_dates = self.get_dates()
        if not start_date:
            start_date = posted_dates[0]
        if not end_date:
            end_date = dt.date.today() - dt.timedelta(days=1)
        calendar = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in self.get_calendar(
            start_date=start_date,
            end_date=end_date).business_dates]
        return [date for date in calendar if date not in posted_dates]

    def get_most_recent_date_from_calendar(self) -> dt.date:
        """ Get T-1 date according to risk model calendar """
        yesterday = dt.date.today() - dt.timedelta(1)
        calendar = self.get_calendar(end_date=yesterday).business_dates
        return dt.datetime.strptime(calendar[len(calendar) - 1], '%Y-%m-%d').date()

    def __str__(self):
        return self.id

    def __repr__(self):
        s = "{}('{}','{}'".format(self.__class__.__name__, self.id, self.name)
        if self.entitlements is not None:
            s += ", entitlements={}".format(self)
        if self.description is not None:
            s += ", description={}".format(self)

        s += ")"
        return s


class FactorRiskModel(RiskModel):
    """ Factor Risk Model used for calculating asset level factor risk"""

    def __init__(self,
                 id_: str,
                 name: str,
                 coverage: CoverageType,
                 term: Term,
                 universe_identifier: UniverseIdentifier,
                 vendor: str,
                 version: float,
                 entitlements: Union[Dict, Entitlements] = None,
                 description: str = None):
        """ Create new factor risk model object

        :param id_: risk model id (cannot be changed)
        :param name: risk model name
        :param coverage: coverage of risk model asset universe
        :param term: horizon term
        :param universe_identifier: identifier used in asset universe upload (cannot be changed)
        :param vendor: risk model vendor
        :param version: version of model
        :param entitlements: entitlements associated with risk model
        :param description: risk model description

        :return: FactorRiskModel object
        """
        super().__init__(id_, name, entitlements=entitlements, description=description)
        self.__coverage = coverage
        self.__term = term
        self.__universe_identifier = universe_identifier
        self.__vendor = vendor
        self.__version = version

    @property
    def vendor(self) -> str:
        """ Get risk model vendor """
        return self.__vendor

    @vendor.setter
    def vendor(self, vendor):
        """ Set risk model vendor """
        self.__vendor = vendor

    @property
    def universe_identifier(self) -> UniverseIdentifier:
        """ Get risk model universe identifier """
        return self.__universe_identifier

    @property
    def term(self) -> Term:
        """ Get risk model term """
        return self.__term

    @term.setter
    def term(self, term: Term):
        """ Set risk model term """
        self.__term = term

    @property
    def version(self) -> float:
        """ Get risk model version """
        return self.__version

    @version.setter
    def version(self, version: float):
        """ Set risk model version """
        self.__version = version

    @property
    def coverage(self) -> CoverageType:
        """ Get risk model coverage """
        return self.__coverage

    @coverage.setter
    def coverage(self, coverage: CoverageType):
        """ Set risk model coverage """
        self.__coverage = coverage

    @classmethod
    def from_target(cls, model: RiskModelBuilder):
        uid = model.universe_identifier
        return FactorRiskModel(
            model.id,
            model.name,
            model.coverage if isinstance(model.coverage, CoverageType) else CoverageType(model.coverage),
            model.term if isinstance(model.term, Term) else Term(model.term),
            uid if isinstance(uid, UniverseIdentifier) else UniverseIdentifier(uid) if uid else None,
            model.vendor,
            model.version,
            entitlements=model.entitlements,
            description=model.description
        )

    @classmethod
    def from_many_targets(cls, models: Tuple[RiskModelBuilder, ...]):
        return [cls.from_target(model) for model in models]

    @classmethod
    def get(cls, model_id: str):
        """ Get a factor risk model from Marquee
            :param model_id: risk model id corresponding to Marquee Factor Risk Model
            :return: Factor Risk Model object  """
        model = GsRiskModelApi.get_risk_model(model_id)
        return cls.from_target(model)

    @classmethod
    def get_many(cls,
                 ids: List[str] = None,
                 terms: List[str] = None,
                 vendors: List[str] = None,
                 names: List[str] = None,
                 coverages: List[str] = None,
                 limit: int = None):
        """ Get a factor risk model from Marquee

        :param ids: list of model identifiers in Marquee
        :param terms: list of model terms
        :param vendors: list of model vendors
        :param names: list of model names
        :param coverages: list of model coverages
        :param limit: limit of number of models in response

        :return: Factor Risk Model object
        """
        models = GsRiskModelApi.get_risk_models(ids=ids,
                                                terms=terms,
                                                vendors=vendors,
                                                names=names,
                                                coverages=coverages,
                                                limit=limit)
        return cls.from_many_targets(models)

    def save(self):
        """ Upload current Factor Risk Model object to Marquee """
        new_model = RiskModelBuilder(self.coverage,
                                     self.id,
                                     self.name,
                                     self.term,
                                     self.universe_identifier,
                                     self.vendor,
                                     self.version,
                                     description=self.description,
                                     entitlements=self.entitlements)
        GsRiskModelApi.create_risk_model(new_model)

    def update(self):
        """ Update factor risk model object on Marquee """
        updated_model = RiskModelBuilder(self.coverage,
                                         self.id,
                                         self.name,
                                         self.term,
                                         self.universe_identifier,
                                         self.vendor,
                                         self.version,
                                         description=self.description,
                                         entitlements=self.entitlements)
        GsRiskModelApi.update_risk_model(updated_model)

    def get_factor(self, name: str) -> Factor:
        """ Get risk model factor from its name

        :param name: factor name associated with risk model

        :return: Factor object
        """
        name_matches = [f for f in self.get_factor_data(format=ReturnFormat.JSON) if f['name'] == name]

        if not name_matches:
            raise MqValueError(f'Factor with name {name} does not in exist in risk model {self.id}')

        factor = name_matches.pop()
        return Factor(risk_model_id=self.id,
                      id_=factor['identifier'],
                      type_=factor['type'],
                      name=factor.get('name'),
                      category=factor.get('factorCategory'),
                      tooltip=factor.get('tooltip'),
                      description=factor.get('description'),
                      glossary_description=factor.get('glossaryDescription'))

    def get_many_factors(self):
        factors = self.get_factor_data(format=ReturnFormat.JSON)
        return [Factor(risk_model_id=self.id,
                       id_=f['identifier'],
                       type_=f['type'],
                       name=f.get('name'),
                       category=f.get('factorCategory'),
                       tooltip=f.get('tooltip'),
                       description=f.get('description'),
                       glossary_description=f.get('glossaryDescription')) for f in factors]

    def save_factor_metadata(self, factor_metadata: RiskModelFactor):
        """ Add metadata to a factor in a risk model

        :param factor_metadata: factor metadata object
        """
        try:
            GsFactorRiskModelApi.get_risk_model_factor(self.id, factor_id=factor_metadata.identifier)
        except MqRequestError:
            GsFactorRiskModelApi.create_risk_model_factor(self.id, factor_metadata)
        GsFactorRiskModelApi.update_risk_model_factor(self.id, factor_metadata)

    def delete_factor_metadata(self, factor_id: str):
        """ Delete a factor's metadata from a risk model

        :param factor_id: factor id associated with risk model's factor
        """
        GsFactorRiskModelApi.delete_risk_model_factor(self.id, factor_id)

    def get_factor_data(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        identifiers: List[str] = None,
                        include_performance_curve: bool = False,
                        category_filter: List[str] = None,
                        factor_type: FactorType = None,
                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get factor data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param identifiers: list of factor ids associated with risk model
        :param include_performance_curve: request to include the performance curve of the factors
        :param category_filter: filter the results to those having one of the specified categories. \
            Default is to return all results
        :param factor_type:
        :param format: which format to return the results in

        :return: risk model factor data
        """
        factor_data = GsFactorRiskModelApi.get_risk_model_factor_data(
            self.id,
            start_date,
            end_date,
            identifiers,
            include_performance_curve
        )
        if factor_type:
            factor_data = [factor for factor in factor_data if factor['type'] == factor_type.value]
        if category_filter:
            if factor_type == FactorType.Category:
                print('Category Filter is not applicable for the Category FactorType')
            else:
                factor_data = [factor for factor in factor_data if factor['factorCategory'] in category_filter]
        if format == ReturnFormat.DATA_FRAME:
            factor_data = pd.DataFrame(factor_data)
        return factor_data

    def get_asset_universe(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get asset universe data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: risk model universe
        """
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
                            assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                            format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get historical beta data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: historical beta for assets requested
        """
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
                       assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                       format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get total risk data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: total risk for assets requested
        """
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
                          assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                          format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get specific risk data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: specific risk for assets requested
        """
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
                              assets: DataAssetsRequest = DataAssetsRequest(
                                  RiskModelUniverseIdentifierRequest.gsid, []),
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get residual variance data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: residual variance for assets requested
         """
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

    def get_specific_return(self,
                            start_date: dt.date,
                            end_date: dt.date = None,
                            assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                            format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get specific return data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: specific returns for assets requested
        """
        results = GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Specific_Return, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
        specific_return = build_asset_data_map(results, universe, 'specificReturn')
        if format == ReturnFormat.DATA_FRAME:
            specific_return = pd.DataFrame(specific_return)
        return specific_return

    def get_universe_factor_exposure(self,
                                     start_date: dt.date,
                                     end_date: dt.date = None,
                                     assets: DataAssetsRequest = DataAssetsRequest(
                                         RiskModelUniverseIdentifierRequest.gsid, []),
                                     format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe factor exposure data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: factor exposure for assets requested
        """
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
        """ Get factor return data for existing risk model keyed by name

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param format: which format to return the results in

        :return: factor returns by name
        """
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
        """ Get factor return data for existing risk model keyed by factor id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param format: which format to return the results in

        :return: factor returns by factor id
        """
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
        """ Get covariance matrix data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param format: which format to return the results in

        :return: covariance matrix of daily factor returns
        """
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
                                       assets: DataAssetsRequest = DataAssetsRequest(
                                           RiskModelUniverseIdentifierRequest.gsid, []),
                                       format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get issuer specific covariance data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: issuer specific covariance matrix (covariance of assets with the same issuer)
        """
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
                              assets: DataAssetsRequest = DataAssetsRequest(
                                  RiskModelUniverseIdentifierRequest.gsid, []),
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get factor portfolios data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: factor portfolios data
        """
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
                 assets: DataAssetsRequest = DataAssetsRequest(
                     RiskModelUniverseIdentifierRequest.gsid, []),
                 limit_factors: bool = True) -> Dict:
        """ Get data for multiple measures for existing risk model

        :param measures: list of measures for general risk model data request
        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param limit_factors: limit factors included in factorData and covariance matrix to only include factors
                which the input universe has non-zero exposure to

        :return: factor portfolios data
        """
        return GsFactorRiskModelApi.get_risk_model_data(
            model_id=self.id,
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
        )

    def upload_data(self, data: Union[RiskModelData, Dict], max_asset_batch_size: int = 20000):
        """ Upload risk model data to existing risk model in Marquee

        :param data: complete risk model data for uploading on given date
            includes: date, factorData, assetData, covarianceMatrix with optional inputs:
            issuerSpecificCovariance and factorPortfolios
        :param max_asset_batch_size: size of payload to batch with. Defaults to 20000 assets

        If upload universe is over 20000 max_asset_batch_size, will batch and upload data in chunks of 20000 assets
        """

        data = risk_model_data_to_json(data) if type(data) == RiskModelData else data
        target_universe_size = get_universe_size(data)
        print(target_universe_size)
        if target_universe_size > max_asset_batch_size:
            print('Batching uploads due to universe size')
            batch_and_upload_partial_data(self.id, data, max_asset_batch_size)
        else:
            print(GsFactorRiskModelApi.upload_risk_model_data(self.id, data))

    def upload_partial_data(self, data: RiskModelData, target_universe_size: float = None):
        """ Upload partial risk model data to existing risk model in Marquee

        :param data: partial risk model data for uploading on given date
        :param target_universe_size: the size of the complete universe on date

        The models factorData and covarianceMatrix must be uploaded first on given date if repeats in partial
            upload, newer posted data will replace existing data on upload day
        """
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
            Marquee UI dropdown for users with "execute" capabilities
        """
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

    def __repr__(self):
        s = "{}('{}','{}','{}','{}','{}','{}','{}'".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.coverage,
            self.term,
            self.universe_identifier,
            self.vendor,
            self.version
        )
        if self.entitlements is not None:
            s += ", entitlements={}".format(self)
        if self.description is not None:
            s += ", description={}".format(self)

        s += ")"
        return s
