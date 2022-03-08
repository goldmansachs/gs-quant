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
from enum import Enum, auto
from typing import List, Dict, Tuple, Union
import pandas as pd
import logging
import pydash

from gs_quant.api.gs.risk_models import GsFactorRiskModelApi, GsRiskModelApi
from gs_quant.base import EnumBase
from gs_quant.errors import MqValueError, MqRequestError
from gs_quant.markets.factor import Factor
from gs_quant.models.risk_model_utils import build_asset_data_map, build_factor_data_map, \
    build_pfp_data_dataframe, get_isc_dataframe, get_covariance_matrix_dataframe, get_closest_date_index, \
    batch_and_upload_partial_data, risk_model_data_to_json, get_universe_size, batch_and_upload_coverage_data, \
    upload_model_data
from gs_quant.target.risk_models import RiskModel as RiskModelBuilder, RiskModelEventType, RiskModelData, \
    RiskModelCalendar, RiskModelDataAssetsRequest as DataAssetsRequest, RiskModelDataMeasure as Measure, \
    RiskModelCoverage as CoverageType, RiskModelUniverseIdentifier as UniverseIdentifier, Entitlements, \
    RiskModelTerm as Term, RiskModelUniverseIdentifierRequest, Factor as RiskModelFactor, RiskModelType


class ReturnFormat(Enum):
    """Alternative format for data to be returned from get_data functions"""
    JSON = auto()
    DATA_FRAME = auto()


class FactorType(EnumBase, Enum):
    """Factor represents a risk factor and Category represents a risk factor category"""

    Factor = 'Factor'
    Category = 'Category'

    def __repr__(self):
        return self.value


class RiskModel:
    """ Risk Model Class """

    def __init__(self,
                 id_: str,
                 name: str):
        self.__id: str = id_
        self.__name: str = name

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

    def __str__(self):
        return self.id

    def __repr__(self):
        s = "{}('{}','{}'".format(self.__class__.__name__, self.id, self.name)

        s += ")"
        return s


class MarqueeRiskModel(RiskModel):
    """ Marquee Risk Model Class """

    def __init__(self,
                 id_: str,
                 name: str,
                 type_: Union[str, RiskModelType],
                 vendor: str,
                 version: float,
                 coverage: CoverageType,
                 universe_identifier: UniverseIdentifier,
                 term: Term,
                 entitlements: Union[Dict, Entitlements] = None,
                 description: str = None,
                 expected_update_time: dt.time = None):
        super().__init__(id_, name)
        self.__type: RiskModelType = type_ if type_ and isinstance(type_, RiskModelType) else RiskModelType(type_)
        self.__vendor = vendor
        self.__version = version
        self.__coverage = coverage
        self.__universe_identifier = universe_identifier
        self.__term = term
        self.__entitlements: Entitlements = entitlements if entitlements and isinstance(entitlements, Entitlements) \
            else Entitlements.from_dict(entitlements) if entitlements and isinstance(entitlements, Dict) else None
        self.__description: str = description
        self.__expected_update_time = expected_update_time

    @property
    def type(self) -> RiskModelType:
        """ Get risk model type"""
        return self.__type

    @type.setter
    def type(self, type_: RiskModelType):
        """ Set risk model type """
        self.__type = type_

    @property
    def vendor(self) -> str:
        """ Get risk model vendor """
        return self.__vendor

    @vendor.setter
    def vendor(self, vendor):
        """ Set risk model vendor """
        self.__vendor = vendor

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

    @property
    def expected_update_time(self) -> dt.time:
        """ Get risk model expected update time """
        return self.__expected_update_time

    @expected_update_time.setter
    def expected_update_time(self, expected_update_time: dt.time):
        """ Set expected update time """
        self.__expected_update_time = expected_update_time

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

        :param start_date: date to truncate missing dates at
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

    def save(self):
        """ Upload current Risk Model object to Marquee """
        model = RiskModelBuilder(self.coverage,
                                 self.id,
                                 self.name,
                                 self.term,
                                 self.universe_identifier,
                                 self.vendor,
                                 self.version,
                                 type_=self.type,
                                 description=self.description,
                                 entitlements=self.entitlements,
                                 expected_update_time=self.expected_update_time.strftime('%H:%M:%S') if
                                 self.expected_update_time else None)
        try:
            GsRiskModelApi.create_risk_model(model)
        except MqRequestError:
            GsRiskModelApi.update_risk_model(model)

    @classmethod
    def get(cls, model_id: str):
        """ Get a risk model from Marquee
        :param model_id: risk model id corresponding to Marquee Risk Model
        :return: Risk Model object
        """
        model = GsRiskModelApi.get_risk_model(model_id)
        return cls.from_target(model)

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
        results = self.get_data(
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

    def get_many_factors(self) -> List[Factor]:
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
            GsFactorRiskModelApi.update_risk_model_factor(self.id, factor_metadata)
        except MqRequestError:
            GsFactorRiskModelApi.create_risk_model_factor(self.id, factor_metadata)

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
                print('Category filter is not applicable for the Category FactorType')
            else:
                factor_data = [factor for factor in factor_data if factor['factorCategory'] in category_filter]
        if format == ReturnFormat.DATA_FRAME:
            factor_data = pd.DataFrame(factor_data)
        return factor_data

    def get_factor_returns_by_name(self,
                                   start_date: dt.date,
                                   end_date: dt.date = None,
                                   assets: DataAssetsRequest = None,
                                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get factor return data for existing risk model keyed by name

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param format: which format to return the results in

        :return: factor returns by name
        """
        limit_factors = True if assets else False
        measures = [Measure.Factor_Return, Measure.Factor_Name, Measure.Factor_Id]
        if assets:
            measures += [Measure.Universe_Factor_Exposure, Measure.Asset_Universe]
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
        ).get('results')
        factor_data = build_factor_data_map(results, 'factorName')
        if format == ReturnFormat.DATA_FRAME:
            factor_data = pd.DataFrame(factor_data)
        return factor_data

    def get_factor_returns_by_id(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 assets: DataAssetsRequest = None,
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get factor return data for existing risk model keyed by factor id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param format: which format to return the results in
        :return: factor returns by factor id
        """

        limit_factors = True if assets else False
        measures = [Measure.Factor_Return, Measure.Factor_Name, Measure.Factor_Id]
        if assets:
            measures += [Measure.Universe_Factor_Exposure, Measure.Asset_Universe]
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
        ).get('results')
        factor_data = build_factor_data_map(results, 'id')
        if format == ReturnFormat.DATA_FRAME:
            factor_data = pd.DataFrame(factor_data)
        return factor_data

    def get_universe_exposure(self,
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
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = pydash.get(results, '0.assetData.universe', [])
        factor_exposure = build_asset_data_map(results, universe, 'factorExposure')
        if format == ReturnFormat.DATA_FRAME:
            factor_exposure = pd.DataFrame.from_dict(
                {(i, j): factor_exposure[i][j]
                 for i in factor_exposure.keys()
                 for j in factor_exposure[i].keys()},
                orient='index'
            )
        return factor_exposure

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
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Specific_Risk, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = pydash.get(results, '0.assetData.universe', [])
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
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Residual_Variance, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = pydash.get(results, '0.assetData.universe', [])
        residual_variance = build_asset_data_map(results, universe, 'residualVariance')
        if format == ReturnFormat.DATA_FRAME:
            residual_variance = pd.DataFrame(residual_variance)
        return residual_variance

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

        :return: risk model data
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

        If upload universe is over max_asset_batch_size, will batch data in chunks of max_asset_batch_size assets
        """

        data = risk_model_data_to_json(data) if type(data) == RiskModelData else data
        target_universe_size = get_universe_size(data)
        logging.info(f'Target universe size for upload: {target_universe_size}')
        if target_universe_size > max_asset_batch_size:
            logging.info('Batching uploads due to universe size')
            batch_and_upload_partial_data(self.id, data, max_asset_batch_size)
        else:
            upload_model_data(self.id, data)

    def upload_partial_data(self, data: Union[RiskModelData, dict], target_universe_size: float = None):
        """ Upload partial risk model data to existing risk model in Marquee

        :param data: partial risk model data for uploading on given date
        :param target_universe_size: the size of the complete universe on date

        The models factorData and covarianceMatrix must be uploaded first on given date if repeats in partial
            upload, newer posted data will replace existing data on upload day
        """
        upload_model_data(self.id, data, partial_upload=True, target_universe_size=target_universe_size)

    def upload_asset_coverage_data(self, date: dt.date = None):
        """ Upload to the coverage dataset for given risk model and date

        :param date: date to upload coverage data for, default date is last date from risk model calendar

        Posting to the coverage dataset within in the last 5 days will enable the risk model to be seen in the
            Marquee UI dropdown for users with "execute" capabilities
        """
        if not date:
            date = self.get_dates()[-1]
        gsid_list = self.get_asset_universe(
            date, assets=DataAssetsRequest('gsid', []), format=ReturnFormat.JSON).get(date)
        if not gsid_list:
            raise MqRequestError(404, f'No asset data found on {date}')
        batch_and_upload_coverage_data(date, gsid_list, self.id)

    @classmethod
    def from_target(cls, model):
        pass

    @classmethod
    def from_many_targets(cls, models: Tuple[RiskModelBuilder, ...]):
        return [cls.from_target(model) for model in models]

    def __str__(self):
        return self.id

    def __repr__(self):
        s = "{}('{}','{}','{}','{}','{}','{}','{}', '{}".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.coverage,
            self.term,
            self.universe_identifier,
            self.vendor,
            self.version,
            self.type
        )
        if self.entitlements:
            s += ", entitlements={}".format(self)
        if self.description:
            s += ", description={}".format(self)
        if self.expected_update_time:
            s += ", expected_update_time={}".format(self)

        s += ")"
        return s


class FactorRiskModel(MarqueeRiskModel):
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
                 description: str = None,
                 expected_update_time: dt.time = None):
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
        :param expected_update_time: time when risk model daily data is expected to be uploaded

        :return: FactorRiskModel object
        """
        super().__init__(id_, name, RiskModelType.Factor, vendor, version, coverage, universe_identifier, term,
                         entitlements=entitlements, description=description, expected_update_time=expected_update_time)

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
            description=model.description,
            expected_update_time=dt.datetime.strptime(
                model.expected_update_time, "%H:%M:%S").time() if model.expected_update_time else None
        )

    @classmethod
    def get_many(cls,
                 ids: List[str] = None,
                 terms: List[str] = None,
                 vendors: List[str] = None,
                 names: List[str] = None,
                 coverages: List[str] = None,
                 limit: int = None) -> list:
        """ Get a factor risk model from Marquee

        :param ids: list of model identifiers in Marquee
        :param terms: list of model terms
        :param vendors: list of model vendors
        :param names: list of model names
        :param coverages: list of model coverages
        :param limit: limit of number of models in response

        :return: list of Factor Risk Model object
        """
        models = GsRiskModelApi.get_risk_models(ids=ids,
                                                terms=terms,
                                                vendors=vendors,
                                                names=names,
                                                coverages=coverages,
                                                limit=limit,
                                                types=[RiskModelType.Factor.value]
                                                )
        return cls.from_many_targets(models)

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
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Total_Risk, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = pydash.get(results, '0.assetData.universe', [])
        total_risk = build_asset_data_map(results, universe, 'totalRisk')
        if format == ReturnFormat.DATA_FRAME:
            total_risk = pd.DataFrame(total_risk)
        return total_risk

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
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Historical_Beta, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        universe = pydash.get(results, '0.assetData.universe', [])
        historical_beta = build_asset_data_map(results, universe, 'historicalBeta')
        if format == ReturnFormat.DATA_FRAME:
            historical_beta = pd.DataFrame(historical_beta)
        return historical_beta

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
        return super().get_universe_exposure(start_date, end_date, assets, format)

    def get_covariance_matrix(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = None,
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get covariance matrix data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the covariance matrix by
        :param format: which format to return the results in

        :return: covariance matrix of daily factor returns
        """

        limit_factors = True if assets else False
        measures = [Measure.Covariance_Matrix, Measure.Factor_Name, Measure.Factor_Id]
        if assets:
            measures += [Measure.Universe_Factor_Exposure, Measure.Asset_Universe]
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
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
        isc = self.get_data(
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
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Factor_Portfolios],
            limit_factors=False
        ).get('results')
        pfp_data = results if format == ReturnFormat.JSON else build_pfp_data_dataframe(results)
        return pfp_data

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
        if self.entitlements:
            s += ", entitlements={}".format(self)
        if self.description:
            s += ", description={}".format(self)
        if self.expected_update_time:
            s += ", expected_update_time={}".format(self)

        s += ")"
        return s


class MacroRiskModel(MarqueeRiskModel):
    """ Macro Risk Model used for sensitivity analysis"""

    def __init__(self,
                 id_: str,
                 name: str,
                 coverage: CoverageType,
                 term: Term,
                 universe_identifier: UniverseIdentifier,
                 vendor: str,
                 version: float,
                 entitlements: Union[Dict, Entitlements] = None,
                 description: str = None,
                 expected_update_time: dt.time = None):
        """ Create new Macro risk model object

        :param id_: risk model id (cannot be changed)
        :param name: risk model name
        :param coverage: coverage of risk model asset universe
        :param universe_identifier: identifier used in asset universe upload (cannot be changed)
        :param vendor: risk model vendor
        :param version: version of model
        :param entitlements: entitlements associated with risk model
        :param description: risk model description
        :param expected_update_time: time when risk model daily data is expected to be uploaded

        :return: MacroRiskModel object
        """
        super().__init__(id_, name, RiskModelType.Macro, vendor, version, coverage, universe_identifier, term,
                         entitlements=entitlements, description=description, expected_update_time=expected_update_time)

    @classmethod
    def from_target(cls, model: RiskModelBuilder):
        uid = model.universe_identifier
        return MacroRiskModel(
            model.id,
            model.name,
            model.coverage if isinstance(model.coverage, CoverageType) else CoverageType(model.coverage),
            model.term if isinstance(model.term, Term) else Term(model.term),
            uid if isinstance(uid, UniverseIdentifier) else UniverseIdentifier(uid) if uid else None,
            model.vendor,
            model.version,
            entitlements=model.entitlements,
            description=model.description,
            expected_update_time=dt.datetime.strptime(
                model.expected_update_time, "%H:%M:%S").time() if model.expected_update_time else None
        )

    @classmethod
    def get_many(cls,
                 ids: List[str] = None,
                 terms: List[str] = None,
                 vendors: List[str] = None,
                 names: List[str] = None,
                 coverages: List[str] = None,
                 limit: int = None):
        """ Get a Macro risk model from Marquee

        :param ids: list of model identifiers in Marquee
        :param terms: list of model terms
        :param vendors: list of model vendors
        :param names: list of model names
        :param coverages: list of model coverages
        :param limit: limit of number of models in response

        :return: list of Macro Risk Model object
        """
        models = GsRiskModelApi.get_risk_models(ids=ids,
                                                terms=terms,
                                                vendors=vendors,
                                                names=names,
                                                coverages=coverages,
                                                types=[RiskModelType.Macro.value],
                                                limit=limit)
        return cls.from_many_targets(models)

    def get_universe_sensitivity(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                               []),
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe sensitivity data for existing macro risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: sensitivity for assets requested
        """
        return super().get_universe_exposure(start_date, end_date, assets, format)

    def __repr__(self):
        s = "{}('{}','{}','{}','{}','{}','{}'".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.coverage,
            self.universe_identifier,
            self.vendor,
            self.version
        )
        if self.entitlements:
            s += ", entitlements={}".format(self)
        if self.description:
            s += ", description={}".format(self)
        if self.expected_update_time:
            s += ", expected_update_time={}".format(self)

        s += ")"
        return s


class ThematicRiskModel(MarqueeRiskModel):
    """ Thematic Risk Model used for calculating exposure to thematic flagship baskets """

    def __init__(self,
                 id_: str,
                 name: str,
                 coverage: CoverageType,
                 term: Term,
                 universe_identifier: UniverseIdentifier,
                 vendor: str,
                 version: float,
                 entitlements: Union[Dict, Entitlements] = None,
                 description: str = None,
                 expected_update_time: dt.time = None):
        """ Create new Thematic risk model object

        :param id_: risk model id (cannot be changed)
        :param name: risk model name
        :param coverage: coverage of risk model asset universe
        :param term: horizon term
        :param universe_identifier: identifier used in asset universe upload (cannot be changed)
        :param vendor: risk model vendor
        :param version: version of model
        :param entitlements: entitlements associated with risk model
        :param description: risk model description
        :param expected_update_time: time when risk model daily data is expected to be uploaded

        :return: Thematic Risk Model object
        """
        super().__init__(id_, name, RiskModelType.Thematic, vendor, version, coverage, universe_identifier, term,
                         entitlements=entitlements, description=description, expected_update_time=expected_update_time)

    @classmethod
    def from_target(cls, model: RiskModelBuilder):
        uid = model.universe_identifier
        return ThematicRiskModel(
            model.id,
            model.name,
            model.coverage if isinstance(model.coverage, CoverageType) else CoverageType(model.coverage),
            model.term if isinstance(model.term, Term) else Term(model.term),
            uid if isinstance(uid, UniverseIdentifier) else UniverseIdentifier(uid) if uid else None,
            model.vendor,
            model.version,
            entitlements=model.entitlements,
            description=model.description,
            expected_update_time=dt.datetime.strptime(
                model.expected_update_time, "%H:%M:%S").time() if model.expected_update_time else None
        )

    @classmethod
    def get_many(cls,
                 ids: List[str] = None,
                 terms: List[str] = None,
                 vendors: List[str] = None,
                 names: List[str] = None,
                 coverages: List[str] = None,
                 limit: int = None):
        """ Get a Thematic risk model from Marquee

        :param ids: list of model identifiers in Marquee
        :param terms: list of model terms
        :param vendors: list of model vendors
        :param names: list of model names
        :param coverages: list of model coverages
        :param limit: limit of number of models in response

        :return: Macro Risk Model object
        """
        models = GsRiskModelApi.get_risk_models(ids=ids,
                                                terms=terms,
                                                vendors=vendors,
                                                names=names,
                                                coverages=coverages,
                                                types=[RiskModelType.Thematic.value],
                                                limit=limit)
        return cls.from_many_targets(models)

    def get_universe_sensitivity(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                               []),
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe sensitivity data for existing thematic risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: basket sensitivity for assets requested
        """
        return super().get_universe_exposure(start_date, end_date, assets, format)

    def __repr__(self):
        s = "{}('{}','{}','{}','{}','{}','{}'".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.coverage,
            self.universe_identifier,
            self.vendor,
            self.version
        )
        if self.entitlements:
            s += ", entitlements={}".format(self)
        if self.description:
            s += ", description={}".format(self)
        if self.expected_update_time:
            s += ", expected_update_time={}".format(self)

        s += ")"
        return s
