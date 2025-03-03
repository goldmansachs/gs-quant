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
import math
from enum import Enum, auto
from typing import List, Dict, Tuple, Union
import pandas as pd
import numpy as np
import logging
import deprecation
from gs_quant.target.common import Currency

from gs_quant.api.gs.risk_models import GsFactorRiskModelApi, GsRiskModelApi
from gs_quant.base import EnumBase
from gs_quant.data import DataMeasure
from gs_quant.errors import MqValueError, MqRequestError
from gs_quant.markets.factor import Factor
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier
from gs_quant.models.risk_model_utils import *
from gs_quant.target.risk_models import RiskModel as RiskModelBuilder, RiskModelEventType, RiskModelData, \
    RiskModelCalendar, RiskModelDataAssetsRequest as DataAssetsRequest, RiskModelDataMeasure as Measure, \
    RiskModelCoverage as CoverageType, RiskModelUniverseIdentifier as UniverseIdentifier, Entitlements, \
    RiskModelTerm as Term, RiskModelUniverseIdentifierRequest, Factor as RiskModelFactor, RiskModelType, \
    RiskModelDataMeasure, RiskModelDataAssetsRequest


class ReturnFormat(Enum):
    """Alternative format for data to be returned from get_data functions"""
    JSON = auto()
    DATA_FRAME = auto()


class Unit(Enum):
    """Units in which to return a risk model data measure"""
    PERCENT = auto()
    STANDARD_DEVIATION = auto()


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
                 universe_size: int = None,
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
        self.__universe_size = universe_size
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
    def universe_size(self) -> int:
        """ Get risk model universe size """
        return self.__universe_size

    @universe_size.setter
    def universe_size(self, universe_size: int):
        """ Set risk model universe size """
        self.__universe_size = universe_size

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
        """ Get dates between start_date and end_date for which risk model data is present

        :param start_date: List returned including and after start_date
        :param end_date: List returned up to and including end_date
        :param event_type: Which event type to retrieve dates for

        :return: A list of dates where risk model data is present

        **Usage**

        Get all the dates for which risk model data is present over start_date and end_date (inclusive).

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel, RiskModelEventType
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> dates = model.get_dates(start_date, end_date)

        **See also**

        :func:`get_missing_dates` :func:`get_calendar` :func:`get_most_recent_date_from_calendar`
        """
        return [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in
                GsRiskModelApi.get_risk_model_dates(self.id, start_date, end_date, event_type=event_type)]

    def get_calendar(self, start_date: dt.date = None, end_date: dt.date = None) -> RiskModelCalendar:
        """ Get risk model calendar for existing risk model between start and end date

        :param start_date: List returned including and after start_date
        :param end_date: List returned up to and including end_date

        :return: RiskModelCalendar for model

        **Usage**

        Get the risk model calendar.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> model_calendar = model.get_calendar(start_date, end_date)

        **See also**

        :func:`get_most_recent_date_from_calendar` :func:`get_dates` :func:`get_missing_dates`
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

        :param start_date: Date to truncate missing dates at
        :param end_date: Date to truncate missing dates at

            If no end_date is provided, end_date defaults to T-1 date according
                to the risk model calendar

        **Usage**

        Get dates with missing data between start date and end date.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> dates = model.get_missing_dates(start_date, end_date)

        **See also**

        :func:`get_dates` :func:`get_calendar`
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
                                 universe_size=self.universe_size,
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

        :param start_date: Start date for data request. Must be equal to end_date if universe array
                           in DataAssetsRequest is empty.
        :param end_date: End date for data request. Must be equal to start_date if universe array
                         in DataAssetsRequest is empty.
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Risk model universe data in a pandas dataframe or dict

        **Usage**

        Get the assets covered by the model between start date and end date.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier, ReturnFormat
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> universe = ['GS UN']
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> asset_universe = model.get_asset_universe(start_date, end_date,
        ...                                           DataAssetsRequest(UniverseIdentifier.bbid, universe))

        **See also**

        :func:`get_specific_risk` :func:`get_universe_factor_exposure` :func:`get_total_risk`
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
            return pd.DataFrame.from_dict(dates_to_universe, orient='index').T
        return dates_to_universe

    def get_factor(self, name: str, start_date: dt.date = None, end_date: dt.date = None) -> Factor:
        """ Get risk model factor from its name

        :param name: Factor name associated with risk model
        :param start_date: Start date of when to search for factor (optional, default to last month)
        :param end_date: End date of when to search for factor (optional, default to today)

        :return: Factor object
        """
        name_matches = [f for f in self.get_factor_data(start_date=start_date, end_date=end_date,
                                                        format=ReturnFormat.JSON) if f['name'] == name]

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

    def get_many_factors(self,
                         start_date: dt.date = None,
                         end_date: dt.date = None,
                         factor_names: List[str] = None,
                         factor_ids: List[str] = None,
                         factor_type: FactorType = None) -> List[Factor]:
        """ Get risk model factors
        :param start_date: Start date of when to search for factors (optional, default to last month)
        :param end_date: End date of when to search for factors
        :param factor_names: The list of names of factors to get. All names must be valid factor names. If both
                             factor_names and factor_ids are empty, all the factors will be returned.
        :param factor_ids: The list of ids of factors to get. All ids must be valid factor ids. If both factor_names and
                          factor_ids are empty, all the factors will be returned
        :param factor_type: Whether to return factors or factor categories. If unspecified, all the factors of all types
                            will be returned

        :return: A list of Factor objects

        **Usage**

        Given a list of factor names and/or ids, return the factor objects that represent the factor requested. If no
        factor names or ids are provided, all the factors will be returned.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel, FactorType
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> many_factors = model.get_many_factors(start_date, end_date, factor_names=["factor1", "factor2"],
        ...                                       factor_type=FactorType.Factor)
        >>>

        **See also**

        :func:`get_factor` :func:`get_factor_data`
        """
        factors_from_model = self.get_factor_data(start_date=start_date, end_date=end_date,
                                                  factor_type=factor_type, format=ReturnFormat.JSON)
        name_matches = []
        if not factor_names and not factor_ids:
            name_matches = factors_from_model
        else:
            for f in factors_from_model:
                if factor_names:
                    if f["name"] in factor_names:
                        name_matches.append(f)
                        factor_names.remove(f["name"])
                if factor_ids:
                    if f["identifier"] in factor_ids:
                        name_matches.append(f)
                        factor_ids.remove(f["identifier"])

        if factor_names or factor_ids:
            raise MqValueError(f'Factor names: {factor_names} and factor ids: {factor_ids} not in model'
                               f' {self.id} for date range requested')

        return [Factor(risk_model_id=self.id,
                       id_=f['identifier'],
                       type_=f['type'],
                       name=f.get('name'),
                       category=f.get('factorCategory'),
                       tooltip=f.get('tooltip'),
                       description=f.get('description'),
                       glossary_description=f.get('glossaryDescription')) for f in name_matches]

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
                        name_filter: List[str] = None,
                        factor_type: FactorType = None,
                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get factor data for existing risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param identifiers: List of factor ids associated with risk model
        :param include_performance_curve: Include the performance curve of the factors
        :param category_filter: Filter the results to those having one of the specified categories. \
            Default is to return all results
        :param factor_type: The type of factor.
        :param format: which format to return the results in
        :param name_filter: Filter the results based on factor name.
        :return: Risk model factor data

        **Usage**

        Get factor data for factors whose ids are specified in identifiers.

        **Examples**

        This will get the factor data for the past 1 month.

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data()

        This will get the factor data within the range start_date and end_date

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data(start_date=dt.date("2023-01-01"), end_date=dt.date("2023-02-03"))

        This will return factor data for factors with the specified identifiers

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data(identifiers=["1", "2", "3"])

        This will filter factor data based on factor names

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data(name_filter=["Factor name a", "Factor name b", "Factor name c"])

        This will return factor data for factors in the specified factor categories

         >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data(category_filter=["Factor category 1", "Factor category 2"])

        This will return all the factors of type "Factor" (won't return data on factor categories)

         >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data(factor_type=FactorType.Factor)

        This will only return higher level factor category data.

         >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_data = model.get_factor_data(factor_type=FactorType.Category)

        **See also**

        :func:`get_many_factors :func:`get_factor_returns_by_name`
        """
        factor_categories = category_filter if category_filter else []
        if factor_type == FactorType.Category:
            if factor_categories:
                raise ValueError('Category filter is not applicable while requesting the FactorType as Category')
            factor_categories = ['Aggregations']
        factor_data = GsFactorRiskModelApi.get_risk_model_factor_data(
            self.id,
            start_date,
            end_date,
            identifiers,
            include_performance_curve,
            factor_categories,
            name_filter,
        )
        if factor_type == FactorType.Factor:
            if 'Aggregations' in factor_categories:
                raise ValueError("Aggregations should not be passed while requesting the FactorType as Factor")
            factor_data = [factor for factor in factor_data if factor['type'] == factor_type.value]
        if format == ReturnFormat.DATA_FRAME:
            factor_data = pd.DataFrame(factor_data)
        return factor_data

    def get_factor_returns_by_name(self,
                                   start_date: dt.date,
                                   end_date: dt.date = None,
                                   assets: DataAssetsRequest = None,
                                   factors: List[str] = [],
                                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get factor return data for existing risk model keyed by name

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: The factors to get factor return data for. If empty, the data for all factors is returned
        :param format: Which format to return the results in

        :return: Factor returns by name

        **Usage**

        Get factor returns between start date and end date.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_returns = model.get_factor_returns_by_name(start_date, end_date)

        **See also**

        :func:`get_factor_returns_by_id` :func:`get_factor_data`
        """

        return self._get_factor_data_measure(Measure.Factor_Return,
                                             start_date,
                                             end_date,
                                             assets,
                                             True,
                                             factors,
                                             format)

    def get_factor_returns_by_id(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 assets: DataAssetsRequest = None,
                                 factors: List[str] = [],
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get factor return data for existing risk model keyed by factor id

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: The factors to get factor return data for. If empty, the data for all factors is returned
        :param format: Which format to return the results in

        :return: Factor returns by factor id

        **Usage**

        Get factor returns between start date and end date.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_returns = model.get_factor_returns_by_id(start_date, end_date)


        **See also**

        :func:`get_factor_returns_by_name` :func:`get_factor_data`
        """

        return self._get_factor_data_measure(Measure.Factor_Return,
                                             start_date,
                                             end_date,
                                             assets,
                                             False,
                                             factors,
                                             format)

    def _get_factor_data_measure(self,
                                 requested_measure: RiskModelDataMeasure,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 assets: DataAssetsRequest = None,
                                 factors_by_name=True,
                                 factors: List[str] = [],
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:

        limit_factors = False
        measures = [requested_measure, Measure.Factor_Name, Measure.Factor_Id]
        if assets:
            measures += [Measure.Universe_Factor_Exposure, Measure.Asset_Universe]
            limit_factors = True
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
        ).get('results')
        identifier = 'factorName' if factors_by_name else 'factorId'
        factor_data_df = build_factor_data_map(results, identifier, self.id, requested_measure, factors=factors)
        return factor_data_df if format == ReturnFormat.DATA_FRAME else factor_data_df.to_dict()

    def _get_asset_data_measure(self,
                                requested_measure: RiskModelDataMeasure,
                                start_date: dt.date,
                                end_date: dt.date = None,
                                assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                              []),
                                format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[requested_measure, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        measure_data = build_asset_data_map(results, assets.universe, requested_measure, {})
        if format == ReturnFormat.DATA_FRAME:
            measure_data = pd.DataFrame(measure_data)
        return measure_data

    def get_universe_exposure(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = DataAssetsRequest(
                                  RiskModelUniverseIdentifierRequest.gsid, []),
                              get_factors_by_name: bool = False,
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe factor exposure data for existing risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param get_factors_by_name: Return results keyed by factor name instead of ID
        :param format: Which format to return the results in

        :return: Factor exposure for assets requested

        **Usage**

        Given a list of assets, return their exposure to factor between start date and end date.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> universe = ['GS UN']
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> universe_exposure = model.get_universe_exposure(start_date, end_date,
        ...                                                 DataAssetsRequest(UniverseIdentifier.bbid, universe))

        **See also**

        :func:`get_asset_universe` :func:`get_factor_returns_by_name` :func:`get_covariance_matrix`
        """
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Factor_Name, Measure.Factor_Id, Measure.Universe_Factor_Exposure, Measure.Asset_Universe],
            limit_factors=False
        ).get('results')
        factor_map = {}
        if get_factors_by_name:
            factor_map = build_factor_id_to_name_map(results)
        factor_exposure = build_asset_data_map(results, assets.universe, Measure.Universe_Factor_Exposure, factor_map)
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

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Specific risk for assets requested

        **Usage**

        Get specific risk data for assets specified in `assets` between `start_date` and `end_date`

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> specific_risk = model.get_specific_risk(start_date, end_date,
        ...                                         DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_specific_return` :func:`get_total_risk`
        """
        return self._get_asset_data_measure(Measure.Specific_Risk, start_date, end_date, assets, format)

    def get_factor_standard_deviation(self,
                                      start_date: dt.date,
                                      end_date: dt.date = None,
                                      assets: DataAssetsRequest = None,
                                      factors: List[str] = [],
                                      factors_by_name: bool = True,
                                      format: ReturnFormat =
                                      ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get factor standard deviation data for existing risk model keyed by name or id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: the factors to get standard deviation for. If empty, the data for all factors is returned
        :param factors_by_name: whether to identify factors by their name or id. If true, the list of factors must \
         be a list of factor names. Otherwise, it should be a list of factor ids
        :param format: which format to return the results in

        :return: factor standard deviation

        **Usage**

        Get the value of one standard deviation of the factors specified in `factors`

        **Examples**

        >>> from gs_quant.models.risk_model import MarqueeRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MarqueeRiskModel.get("MODEL_ID")
        >>> factor_standard_deviation = model.get_factor_standard_deviation(start_date, end_date,
        ...                                                                 factors=['factor1', 'factor2'])

        **See also**

        :func:`get_specific_risk` :func:`get_factor_mean`
        """

        return self._get_factor_data_measure(Measure.Factor_Standard_Deviation,
                                             start_date,
                                             end_date,
                                             assets,
                                             factors_by_name,
                                             factors,
                                             format)

    def get_factor_mean(self,
                        start_date: dt.date,
                        end_date: dt.date = None,
                        assets: DataAssetsRequest = None,
                        factors: List[str] = [],
                        factors_by_name: bool = True,
                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get factor mean data for existing risk model keyed by name or id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: the factors to get standard deviation for. If empty, the data for all factors is returned
        :param factors_by_name: whether to identify factors by their name or id. If true, the list of factors must \
         be a list of factor names. Otherwise, it should be a list of factor ids
        :param format: which format to return the results in

        :return: factor mean

        **Usage**

        Get the value of one mean of the factors specified in `factors`

        **Examples**

        >>> from gs_quant.models.risk_model import MarqueeRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MarqueeRiskModel.get("MODEL_ID")
        >>> factor_mean = model.get_factor_mean(start_date, end_date, factors=['factor1', 'factor2'])

        **See also**

        :func:`get_specific_risk` :func:`get_factor_standard_deviation`
        """

        return self._get_factor_data_measure(Measure.Factor_Mean,
                                             start_date,
                                             end_date,
                                             assets,
                                             factors_by_name,
                                             factors,
                                             format)

    def get_factor_cross_sectional_mean(self,
                                        start_date: dt.date,
                                        end_date: dt.date = None,
                                        assets: DataAssetsRequest = None,
                                        factors: List[str] = [],
                                        factors_by_name: bool = True,
                                        format: ReturnFormat = ReturnFormat.DATA_FRAME
                                        ) -> (Union)[List[Dict], pd.DataFrame]:
        """ Get factor cross-sectional mean data for existing risk model keyed by name or id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: the factors to get standard deviation for. If empty, the data for all factors is returned
        :param factors_by_name: whether to identify factors by their name or id. If true, the list of factors must \
         be a list of factor names. Otherwise, it should be a list of factor ids
        :param format: which format to return the results in

        :return: factor cross-sectional mean

        **Usage**

        Get the value of one cross-sectional mean of the factors specified in `factors`

        **Examples**

        >>> from gs_quant.models.risk_model import MarqueeRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MarqueeRiskModel.get("MODEL_ID")
        >>> factor_cross_sectional_mean = model.get_factor_cross_sectional_mean(start_date, end_date,
                                                                                factors=['factor1', 'factor2'])

        **See also**

        :func:`get_factor_mean` :func:`get_factor_cross_sectional_standard_deviation`
        """

        return self._get_factor_data_measure(Measure.Factor_Cross_Sectional_Mean,
                                             start_date,
                                             end_date,
                                             assets,
                                             factors_by_name,
                                             factors,
                                             format)

    def get_factor_cross_sectional_standard_deviation(self,
                                                      start_date: dt.date,
                                                      end_date: dt.date = None,
                                                      assets: DataAssetsRequest = None,
                                                      factors: List[str] = [],
                                                      factors_by_name: bool = True,
                                                      format: ReturnFormat = ReturnFormat.DATA_FRAME
                                                      ) -> Union[List[Dict], pd.DataFrame]:
        """ Get factor cross-sectional standard deviation data for existing risk model keyed by name or id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: the factors to get standard deviation for. If empty, the data for all factors is returned
        :param factors_by_name: whether to identify factors by their name or id. If true, the list of factors must \
         be a list of factor names. Otherwise, it should be a list of factor ids
        :param format: which format to return the results in

        :return: factor cross-sectional standard deviation

        **Usage**

        Get the value of one cross-sectional standard deviation of the factors specified in `factors`

        **Examples**

        >>> from gs_quant.models.risk_model import MarqueeRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MarqueeRiskModel.get("MODEL_ID")
        >>> factor_cross_sectional_sd = model.get_factor_cross_sectional_standard_deviation(start_date, end_date,
                                                                                            factors=['factor1',
                                                                                                    'factor2'])

        **See also**

        :func:`get_factor_standard_deviation` :func:`get_factor_cross_sectional_mean`
        """

        return self._get_factor_data_measure(Measure.Factor_Cross_Sectional_Standard_Deviation,
                                             start_date,
                                             end_date,
                                             assets,
                                             factors_by_name,
                                             factors,
                                             format)

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

        :return: risk model data or MqRequestError if query is too large for the service
        """
        try:
            return GsFactorRiskModelApi.get_risk_model_data(
                model_id=self.id,
                start_date=start_date,
                end_date=end_date,
                assets=assets,
                measures=measures,
                limit_factors=limit_factors
            )
        except MqRequestError as e:
            if e.status > 499:
                logging.warning(f"Potential timeout in request for model {self.id}. Consider adding a retry or"
                                f" batching request if error persists")
                raise MqRequestError(e.status, f"timeout while getting model data between {start_date} and {end_date} "
                                               f" for {self.id}, consider batching request")
            raise e

    def upload_data(self,
                    data: Union[RiskModelData, Dict],
                    max_asset_batch_size: int = 20000,
                    aws_upload: bool = True):
        """ Upload risk model data to existing risk model in Marquee

        :param data: complete or partial risk model data for uploading on given date
            includes: date, and one or more of: factorData, assetData, covarianceMatrix,
                issuerSpecificCovariance, factorPortfolios and currencyRatesData. Look at risk model upload
                documentation for further information on what data can be grouped together if asset data size is above
                the max asset batch size
        :param max_asset_batch_size: size of payload to batch with. Defaults to 20000 assets which works well for
            models that have factor ids ranging from 1- 3 characters in length. For models with longer factor ids,
            consider batching with a smaller max asset batch size
        If upload universe is over max_asset_batch_size, will batch data in chunks of max_asset_batch_size assets
        :param aws_upload: If true, uploads risk model data to AWS
        This function takes risk model data, and if partial requests are necessary, will upload data by
            1. factor data (includes covariance matrix if factor model)
            2. asset data in batches of max_asset_batch_size
            3. issuer specific covariance data in batches of max_asset_batch_size / 2 due to the structure of this data
            4. factor portfolio data in batches of max_asset_batch_size / 2 due to the structure of this data

        In the case of repeat identifiers on a given data, the repeated data will replace existing data
        """

        data = data.as_dict() if type(data) is RiskModelData else data
        full_data_present = 'factorData' in data.keys() and 'assetData' in data.keys()
        only_factor_data_present = only_factor_data_is_present(self.type, data)
        target_universe_size = 0 if only_factor_data_present else get_universe_size(data)
        make_partial_request = target_universe_size > max_asset_batch_size or not full_data_present
        if target_universe_size:
            logging.info(f'Target universe size for upload: {target_universe_size}')
        if make_partial_request:
            batch_and_upload_partial_data(self.id, data, max_asset_batch_size, aws_upload=aws_upload)
        else:
            logging.info('Uploading model data in one request')
            upload_model_data(self.id, data, aws_upload=aws_upload)

    @deprecation.deprecated(deprecated_in="0.9.42", details="Please use upload_data instead")
    def upload_partial_data(self,
                            data: Union[RiskModelData, dict],
                            final_upload: bool = None):
        """ Upload partial risk model data to existing risk model in Marquee

        :param data: partial risk model data for uploading on given date
        :param final_upload: if this is the last upload for the batched subset of data

        The models factorData and covarianceMatrix must be uploaded first on given date if repeats in partial
            upload, newer posted data will replace existing data on upload day

        """
        upload_model_data(self.id, data, partial_upload=True, final_upload=final_upload)

    def upload_asset_coverage_data(self, date: dt.date = None, batch_size: int = 100):
        """ Upload to the coverage dataset for given risk model and date

        :param date: Date to upload coverage data for, default date is last date from risk model calendar
        :param batch_size: Number of assets to upload in one request

        Posting to the coverage dataset within the last 5 days will enable the risk model to be seen in the
        Marquee UI dropdown for users with "execute" capabilities
        """
        if not date:
            date = self.get_dates()[-1]
        gsid_list = self.get_asset_universe(date,
                                            assets=DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                                            format=ReturnFormat.JSON).get(date)
        if not gsid_list:
            raise MqRequestError(404, f'No asset data found on {date}')
        batch_and_upload_coverage_data(date, gsid_list, self.id, batch_size)

    @classmethod
    def from_target(cls, model):
        uid = model.universe_identifier
        return MarqueeRiskModel(
            id_=model.id,
            name=model.name,
            coverage=model.coverage if isinstance(model.coverage, CoverageType) else CoverageType(model.coverage),
            term=model.term if isinstance(model.term, Term) else Term(model.term),
            universe_identifier=uid if isinstance(uid, UniverseIdentifier) else
            UniverseIdentifier(uid) if uid else None,
            vendor=model.vendor,
            version=model.version,
            type_=model.type_ if not model.type_ or isinstance(model.type_, RiskModelType)
            else RiskModelType(model.type_),
            entitlements=model.entitlements,
            description=model.description,
            expected_update_time=dt.datetime.strptime(
                model.expected_update_time, "%H:%M:%S").time() if model.expected_update_time else None
        )

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
        if self.universe_size:
            s += ", universe_size={}".format(self)
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
                 universe_size: int = None,
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
        :param universe_size: total rough expected universe size (rounding up to nearest 1k)
        :param entitlements: entitlements associated with risk model
        :param description: risk model description
        :param expected_update_time: time when risk model daily data is expected to be uploaded

        :return: FactorRiskModel object
        """
        super().__init__(id_, name, RiskModelType.Factor, vendor, version, coverage, universe_identifier, term,
                         universe_size=universe_size, entitlements=entitlements, description=description,
                         expected_update_time=expected_update_time)

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
            universe_size=model.universe_size,
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
        """ Get many factor risk models from Marquee

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

        **Usage**

        Get total risk data for assets specified in `assets` between `start_date` and `end_date`

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier, ReturnFormat
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> total_risk = model.get_total_risk(start_date, end_date,
    ...                                       DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_specific_risk` :func:`get_specific_return` :func:`get_historical_beta`
        """
        return self._get_asset_data_measure(Measure.Total_Risk, start_date, end_date, assets, format)

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

        **Usage**

        Get historical beta data for assets specified in `assets` between `start_date` and `end_date`

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier, ReturnFormat
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> historical_beta = model.get_historical_beta(start_date, end_date,
        ...                                             DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_predicted_beta` :func:`get_global_predicted_beta`
        """
        return self._get_asset_data_measure(Measure.Historical_Beta, start_date, end_date, assets, format)

    def get_predicted_beta(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get predicted beta data for an existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: predicted beta for assets requested

        **Usage**

        Get predicted beta data for assets specified in `assets` between `start_date` and `end_date`

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MacroRiskModel.get("MODEL_ID")
        >>> predicted_beta = model.get_predicted_beta(start_date, end_date,
        ...                                           DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_historical_beta` :func:`get_global_predicted_beta`
        """
        return self._get_asset_data_measure(Measure.Predicted_Beta, start_date, end_date, assets, format)

    def get_global_predicted_beta(self,
                                  start_date: dt.date,
                                  end_date: dt.date = None,
                                  assets: DataAssetsRequest = DataAssetsRequest(
                                      RiskModelUniverseIdentifierRequest.gsid, []),
                                  format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get global predicted beta data for an existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: which format to return the results in

        :return: global predicted beta for assets requested

        **Usage**

        Get global predicted beta for assets specified in `assets` between `start_date` and `end_date`

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> global_predicted_beta = model.get_global_predicted_beta(start_date, end_date,
        ...                                                       DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_predicted_beta` :func:`get_historical_beta`
        """
        return self._get_asset_data_measure(Measure.Global_Predicted_Beta, start_date, end_date, assets, format)

    def get_daily_return(self,
                         start_date: dt.date,
                         end_date: dt.date = None,
                         assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                         format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get daily asset total return data

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Daily asset total return data

        **Usage**

        Get daily return data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> daily_returns = model.get_daily_return(start_date, end_date,
        ...                                        DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_specific_risk` :func:`get_universe_factor_exposure` :func: `get_specific_return`

        """
        return self._get_asset_data_measure(Measure.Daily_Return, start_date, end_date, assets, format)

    def get_specific_return(self,
                            start_date: dt.date,
                            end_date: dt.date = None,
                            assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                            format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get specific return data for existing risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Specific return data

        **Usage**

        Get specific return data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> specific_returns = model.get_specific_return(start_date, end_date,
        ...                                              DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_specific_risk` :func:`get_universe_factor_exposure`

        """
        return self._get_asset_data_measure(Measure.Specific_Return, start_date, end_date, assets, format)

    def get_bid_ask_spread(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           days: int = 0,
                           assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get bid ask spread data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param days: Get bid ask spread for a past average of specific days
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Bid Ask Spread Data

        **Usage**

        Get Bid Ask Spread data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> bid_ask_spread_30d = model.get_bid_ask_spread(start_date, end_date, 30, \
        ...                                               DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_composite_volume` :func:`get_trading_volume`

        """
        try:
            requested_measure = Measure.Bid_Ask_Spread if not days else Measure[f'Bid_Ask_Spread_{days}d']
            return super()._get_asset_data_measure(requested_measure, start_date, end_date, assets, format)
        except KeyError:
            raise ValueError(f'Bid Ask Spread data is not available for the requested days: {days}')

    def get_trading_volume(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           days: int = 0,
                           assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get trading volume data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param days: Get trading volume for a past average of specific days
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Trading Volume data

        **Usage**

        Get trading volume data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> trading_volume_60d = model.get_trading_volume(start_date, end_date, 60,
        ...                                               DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_composite_volume` :func:`get_traded_value`

        """
        try:
            requested_measure = Measure.Trading_Volume if not days else Measure[f'Trading_Volume_{days}d']
            return super()._get_asset_data_measure(requested_measure, start_date, end_date, assets, format)
        except KeyError:
            raise ValueError(f'Trading volume data is not available for the requested days: {days}')

    def get_traded_value(self,
                         start_date: dt.date,
                         end_date: dt.date = None,
                         days: int = 30,
                         assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                       []),
                         format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get traded value data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param days: Get traded value for a past average of specific days
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Traded Value Data

        **Usage**

        Get traded value data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> traded_value_30d = model.get_traded_value(start_date, end_date,
        ...                                           assets = DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_composite_value` :func:`get_trading_volume`

        """
        try:
            requested_measure = Measure.Traded_Value_30d if not days else Measure[f'Traded_Value_{days}d']
            return super()._get_asset_data_measure(requested_measure, start_date, end_date, assets, format)
        except KeyError:
            raise ValueError(f'Traded Value data is not available for the requested days: {days}')

    def get_composite_volume(self,
                             start_date: dt.date,
                             end_date: dt.date = None,
                             days: int = 0,
                             assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                           []),
                             format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get composite volume data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param days: Get composite volume for a past average of specific days
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Composite volume data

        **Usage**

        Get composite volume data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> composite_volume_30d = model.get_composite_volume(start_date, end_date, 30,
        ...                                                   DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_composite_value` :func:`get_traded_value`

        """
        try:
            requested_measure = Measure.Composite_Volume if not days else Measure[f'Composite_Volume_{days}d']
            return super()._get_asset_data_measure(requested_measure, start_date, end_date, assets, format)
        except KeyError:
            raise ValueError(f'Composite Volume data is not available for the requested days: {days}')

    def get_composite_value(self,
                            start_date: dt.date,
                            end_date: dt.date = None,
                            days: int = 30,
                            assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                          []),
                            format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get composite value data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param days: Get composite value for a past average of specific days
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Composite Value data

        **Usage**

        Get composite value data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> composite_value_30d = model.get_composite_value(start_date, end_date,
        ...                                                assets=DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_traded_value` :func:`get_composite_volume`

        """
        try:
            requested_measure = Measure.Composite_Value_30d if not days else Measure[f'Composite_Value_{days}d']
            return super()._get_asset_data_measure(requested_measure, start_date, end_date, assets, format)
        except KeyError:
            raise ValueError(f'Composite Value data is not available for the requested days: {days}')

    def get_issuer_market_cap(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                            []),
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get issuer market capitalization for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Issue Market cap data

        **Usage**

        Get issuer market capitalization for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> issuer_market_cap = model.get_issuer_market_cap(start_date, end_date,
        ...                                                  DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_asset_price` :func:`get_asset_capitalization` :func:`get_currency`

        """
        return super()._get_asset_data_measure(Measure.Issuer_Market_Cap, start_date, end_date, assets, format)

    def get_asset_price(self,
                        start_date: dt.date,
                        end_date: dt.date = None,
                        assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get asset price data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Asset price data

        **Usage**

        Get prices for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> asset_price = model.get_asset_price(start_date, end_date,
        ...                                                  DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_asset_capitalization` :func:`get_currency`

        """
        return super()._get_asset_data_measure(Measure.Price, start_date, end_date, assets, format)

    def get_asset_capitalization(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid,
                                                                               []),
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get asset capitalization data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Asset Capitalization data

        **Usage**

        Get asset capitalization data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> asset_capitalization = model.get_asset_capitalization(start_date, end_date,
        ...                                                  DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_issuer_market_cap` :func:`get_currency`

        """
        return super()._get_asset_data_measure(Measure.Capitalization, start_date, end_date, assets, format)

    def get_currency(self,
                     start_date: dt.date,
                     end_date: dt.date = None,
                     assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                     format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get currency data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Currency data

        **Usage**

        Get currency data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> currency = model.get_currency(start_date, end_date,
        ...                               DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_asset_price` :func:`get_issuer_market_cap`

        """
        return super()._get_asset_data_measure(Measure.Currency, start_date, end_date, assets, format)

    def get_unadjusted_specific_risk(self,
                                     start_date: dt.date,
                                     end_date: dt.date = None,
                                     assets: DataAssetsRequest = DataAssetsRequest(
                                         RiskModelUniverseIdentifierRequest.gsid, []),
                                     format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get asset unadjusted specific risk data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Unadjusted Specific Risk data

        **Usage**

        Get unadjusted specific risk data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> unadjusted_specific_risk = model.get_unadjusted_specific_risk(start_date, end_date,
        ...                                                  DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_specific_risk` :func:`get_total_risk`

        """
        return super()._get_asset_data_measure(Measure.Unadjusted_Specific_Risk, start_date, end_date, assets, format)

    def get_dividend_yield(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = DataAssetsRequest(
                               RiskModelUniverseIdentifierRequest.gsid, []),
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get dividend yield data for assets covered by the risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Asset Divident Yield

        **Usage**

        Get dividend yield data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> dividend_yield = model.get_dividend_yield(start_date, end_date,
        ...                                           DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_asset_capitalization` :func:`get_issuer_market_cap`

        """
        return super()._get_asset_data_measure(Measure.Dividend_Yield, start_date, end_date, assets, format)

    def get_universe_factor_exposure(self,
                                     start_date: dt.date,
                                     end_date: dt.date = None,
                                     assets: DataAssetsRequest = DataAssetsRequest(
                                         RiskModelUniverseIdentifierRequest.gsid, []),
                                     get_factors_by_name: bool = False,
                                     format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe factor exposure data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param get_factors_by_name: return results keyed by factor name instead of ID
        :param format: which format to return the results in

        :return: factor exposure for assets requested

        **Usage**

        Given a list of assets, return their exposure to factors between start date and end date.

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> universe = ['GS UN']
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> universe_exposure = model.get_universe_factor_exposure(start_date, end_date,
        ...                                                 DataAssetsRequest(UniverseIdentifier.bbid, universe))

        **See also**

        :func:`get_asset_universe` :func:`get_specific_risk`
        """
        return super().get_universe_exposure(start_date, end_date, assets,
                                             get_factors_by_name=get_factors_by_name, format=format)

    def _build_covariance_matrix_measure(self,
                                         covariance_matrix_type: Measure,
                                         start_date: dt.date,
                                         end_date: dt.date = None,
                                         assets: DataAssetsRequest = None,
                                         format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        measure_to_field_name_map = {
            Measure.Covariance_Matrix: 'covarianceMatrix',
            Measure.Unadjusted_Covariance_Matrix: 'unadjustedCovarianceMatrix',
            Measure.Pre_VRA_Covariance_Matrix: 'preVRACovarianceMatrix'
        }
        limit_factors = True if assets else False
        measures = [covariance_matrix_type, Measure.Factor_Name, Measure.Factor_Id]
        if assets:
            measures += [Measure.Universe_Factor_Exposure, Measure.Asset_Universe]
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=measures,
            limit_factors=limit_factors
        ).get('results')
        covariance_data = results if format == ReturnFormat.JSON else get_covariance_matrix_dataframe(
            results, covariance_matrix_key=measure_to_field_name_map[covariance_matrix_type]
        )
        return covariance_data

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

        **Usage**

        Get the covariance matrix of daily factor returns

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> covariance_matrix = model.get_covariance_matrix(start_date, end_date,
        ...                                                 DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_factor_returns_by_name` :func:`get_factor_returns_by_id`
        """
        return self._build_covariance_matrix_measure(Measure.Covariance_Matrix, start_date, end_date, assets, format)

    def get_unadjusted_covariance_matrix(self,
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

        **Usage**

        Get the covariance matrix of daily factor returns

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> covariance_matrix = model.get_unadjusted_covariance_matrix(start_date, end_date,
        ...                                                 DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_factor_returns_by_name` :func:`get_factor_returns_by_id`
        """
        return self._build_covariance_matrix_measure(Measure.Unadjusted_Covariance_Matrix, start_date, end_date, assets,
                                                     format)

    def get_pre_vra_covariance_matrix(self,
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

        **Usage**

        Get the covariance matrix of daily factor returns

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> covariance_matrix = model.get_covariance_matrix(start_date, end_date,
        ...                                                 DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_factor_returns_by_name` :func:`get_factor_returns_by_id`
        """
        return self._build_covariance_matrix_measure(Measure.Pre_VRA_Covariance_Matrix, start_date, end_date, assets,
                                                     format)

    def _build_currency_rates_data(self, rows: List[Dict], currencies: List[Currency], rates_key: str,
                                   format: ReturnFormat) -> Union[Dict, pd.DataFrame]:
        currency_rates_key = "currencyRatesData"
        currency_rates_df = get_optional_data_as_dataframe(rows, currency_rates_key)
        if currencies:
            currency_rates_df = currency_rates_df.loc[currency_rates_df['currency'].isin([cur.value
                                                                                          for cur in currencies])]
        if format == ReturnFormat.DATA_FRAME:
            return currency_rates_df
        return currency_rates_df.to_dict()

    def get_risk_free_rate(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           currencies: List[Currency] = [],
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get risk-free rates for existing risk model

       :param start_date: start date for data request
       :param end_date: end date for data request
       :param currencies: return risk-free rates for these currencies. If empty returns data for all currencies
       :param format: which format to return the results in

       :return: risk-free rates data

       **Usage**

       Get risk-free rates data between `start_date` and `end_date`

       **Examples**

       >>> from gs_quant.models.risk_model import FactorRiskModel
       >>> import datetime as dt
       >>>
       >>> start_date = dt.date(2022, 1, 1)
       >>> end_date = dt.date(2022, 5, 2)
       >>> model = FactorRiskModel.get("MODEL_ID")
       >>> risk_free_rates = model.get_risk_free_rate(start_date, end_date))

       **See also**

       :func:`get_currency_exchange_rate`
        """
        results = self.get_data(measures=[RiskModelDataMeasure.Risk_Free_Rate], start_date=start_date,
                                end_date=end_date, limit_factors=False).get('results')
        return self._build_currency_rates_data(results, rates_key="riskFreeRate", currencies=currencies, format=format)

    def get_currency_exchange_rate(self,
                                   start_date: dt.date,
                                   end_date: dt.date = None,
                                   currencies: List[Currency] = [],
                                   format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get currency exchange rates for existing risk model

       :param start_date: start date for data request
       :param end_date: end date for data request
       :param currencies: return currency exchange rates for these currencies. If empty returns data for all currencies
       :param format: which format to return the results in

       :return: currency exchange rates data

       **Usage**

       Get currency exchange rates data between `start_date` and `end_date`

       **Examples**

       >>> from gs_quant.models.risk_model import FactorRiskModel
       >>> import datetime as dt
       >>>
       >>> start_date = dt.date(2022, 1, 1)
       >>> end_date = dt.date(2022, 5, 2)
       >>> model = FactorRiskModel.get("MODEL_ID")
       >>> currency_exchange_rates = model.get_currency_exchange_rate(start_date, end_date))

       **See also**

       :func:`get_risk_free_rate`
        """
        results = self.get_data(measures=[RiskModelDataMeasure.Currency_Exchange_Rate], start_date=start_date,
                                end_date=end_date, limit_factors=False).get('results')
        return self._build_currency_rates_data(results, rates_key="exchangeRate", currencies=currencies, format=format)

    def get_factor_volatility(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              factors: List[str] = None,
                              get_factors_by_name: bool = True,
                              format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get factor volatility data for existing risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param factors: The factors to get factor return data for. If empty, the data for all factors is returned
        :param get_factors_by_name: get results keyed by factor name instead of ID
        :param format: which format to return the results in

        :return: factor volatility data

        **Usage**

        Get the factor volatility data for daily factor returns

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_volatility_by_name = model.get_factor_volatility(start_date, end_date,
        ...                                                         factors=["factor1", "factor2"])
        >>> factor_volatility_by_id = model.get_factor_volatility(start_date=start_date, end_date=end_date,
        ...                                                       factors=["1", "2", "3"], get_factors_by_name=False)

        **See also**

        :func:`get_factor_returns_by_name` :func:`get_factor_returns_by_id`
        """
        if factors is None:
            factors = []
        measures = [Measure.Factor_Volatility, Measure.Factor_Name, Measure.Factor_Id]
        results = self.get_data(
            start_date=start_date,
            end_date=end_date,
            measures=measures,
            limit_factors=False
        ).get('results')
        if format == ReturnFormat.JSON and not get_factors_by_name and not factors:
            return results
        else:
            factor_volatility_df = build_factor_volatility_dataframe(results, get_factors_by_name, factors)
            return factor_volatility_df if format == ReturnFormat.DATA_FRAME else factor_volatility_df.to_dict()

    def get_estimation_universe_weights(self,
                                        start_date: dt.date,
                                        end_date: dt.date = None,
                                        assets: DataAssetsRequest = DataAssetsRequest(
                                            RiskModelUniverseIdentifierRequest.gsid, []),
                                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[Dict, pd.DataFrame]:
        """ Get estimation universe data for existing risk model

           :param start_date: Start date for data request. Must be equal to end_date if universe array
                              in DataAssetsRequest is empty.
           :param end_date: End date for data request. Must be equal to start_date if universe array
                            in DataAssetsRequest is empty.
           :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
           :param format: Which format to return the results in

           :return: Estimation Universe data in a pandas dataframe or dict

           **Usage**

           Get the assets that are in the estimation universe of the model and their weights.

           **Examples**

           >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
           ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
           >>> import datetime as dt
           >>>
           >>> start_date = dt.date(2022, 1, 1)
           >>> end_date = dt.date(2022, 5, 2)
           >>> universe = ['GS UN']
           >>> model = FactorRiskModel.get("MODEL_ID")
           >>> estimation_universe_weights = model.get_estimation_universe_weights(start_date, end_date,
           ...                                           DataAssetsRequest(UniverseIdentifier.bbid, universe))

           **See also**

           :func:`get_asset_universe` :func:`get_specific_risk`
           """
        return self._get_asset_data_measure(Measure.Estimation_Universe_Weight, start_date, end_date, assets, format)

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

        **Usage**

        Get the covariance of assets with the same issuer.

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> issuer_specific_covariance = model.get_issuer_specific_covariance(start_date, end_date,
        ...                                   DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_factor_portfolios`
        """
        isc = self.get_data(
            start_date=start_date,
            end_date=end_date,
            assets=assets,
            measures=[Measure.Issuer_Specific_Covariance],
            limit_factors=False
        ).get('results')
        isc_data = isc if format == ReturnFormat.JSON else get_optional_data_as_dataframe(isc,
                                                                                          'issuerSpecificCovariance')
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

        **Usage**

        Get the factor portfolios data between `start_date` and `end_date`

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> factor_portfolios = model.get_factor_portfolios(start_date, end_date,
        ...                                                 DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_issuer_specific_covariance`
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

    def get_asset_contribution_to_risk(self,
                                       asset_identifier: str,
                                       date: dt.date,
                                       asset_identifier_type=RiskModelUniverseIdentifierRequest.bbid,
                                       get_factors_by_name: bool = True,
                                       format: ReturnFormat = ReturnFormat.DATA_FRAME):
        """
        Get factor proportion of risk and marginal contribution to risk for each factor in the model

        :param asset_identifier: asset identifier
        :param date: date
        :param asset_identifier_type: type corresponding to the identifier passed in
        :param get_factors_by_name: whether to denote the results by factor name (True) or ID (False)
        :param format: which format to return the results in

        :return: factor proportion of risk and marginal contribution to risk breakdown

        **Usage**

        Get the factor contribution breakdown for any asset covered by the risk model

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> mctr_breakdown = model.get_asset_contribution_to_risk('AAPL UW', date)
        """
        # Get spot price for the asset as of date
        security = SecurityMaster.get_asset(asset_identifier, AssetIdentifier(asset_identifier_type.value.upper()))
        spot_data_coordinate = security.get_data_coordinate(DataMeasure.SPOT_PRICE)
        series = spot_data_coordinate.get_series(start=date, end=date)
        if len(series) == 0:
            raise MqValueError(f'{asset_identifier} has no end of day price available on {date.strftime("%Y-%m-%d")}')
        spot_price = series.iloc[0]

        # Get risk model data for the asset as of date
        data_measures = [RiskModelDataMeasure.Asset_Universe,
                         RiskModelDataMeasure.Total_Risk,
                         RiskModelDataMeasure.Universe_Factor_Exposure,
                         RiskModelDataMeasure.Covariance_Matrix,
                         RiskModelDataMeasure.Factor_Name,
                         RiskModelDataMeasure.Factor_Id,
                         RiskModelDataMeasure.Factor_Category]
        risk_results = self.get_data(data_measures, date, date,
                                     RiskModelDataAssetsRequest(identifier=asset_identifier_type,
                                                                universe=[asset_identifier]),
                                     limit_factors=True)
        if len(risk_results['results'][0]['assetData']['totalRisk']) == 0:
            raise MqValueError(f'{asset_identifier} is not covered by {self.id} on {date.strftime("%Y-%m-%d")}')
        total_risk = risk_results['results'][0]['assetData']['totalRisk'][0]
        var = total_risk / 100 * spot_price / math.sqrt(252)
        covariance_matrix = np.array(risk_results['results'][0]['covarianceMatrix'])
        factor_z_scores = risk_results['results'][0]['assetData']['factorExposure'][0]

        # Calculate results
        factors = risk_results['results'][0]['factorData']
        factor_ids_in_order = [f['factorId'] for f in factors]
        exp = np.array([factor_z_scores[key] * spot_price for key in factor_ids_in_order])
        cov_x_exp = np.dot(covariance_matrix, exp)
        mctr = np.divide(cov_x_exp, var)
        rmctr = np.multiply(exp, mctr)
        annualized_rmctr = np.multiply(rmctr, math.sqrt(252) / spot_price * 100)
        annualized_factor_rmctr_sum = np.sum(annualized_rmctr)

        final_results = []
        for i in range(0, len(mctr)):
            final_results.append({
                'Factor': factors[i]['factorName'] if get_factors_by_name else factors[i]['factorId'],
                'Factor Category': factors[i]['factorCategory'],
                'Proportion of Risk (%)': annualized_rmctr[i] / total_risk * 100,
                'MCTR (%)': annualized_rmctr[i]
            })
        final_results.append({
            'Factor': 'Specific' if get_factors_by_name else 'SPC',
            'Factor Category': 'Specific',
            'Proportion of Risk (%)': (total_risk - annualized_factor_rmctr_sum) / total_risk * 100,
            'MCTR (%)': total_risk - annualized_factor_rmctr_sum
        })

        return pd.DataFrame(final_results) if format == ReturnFormat.DATA_FRAME else final_results

    def get_asset_factor_attribution(self,
                                     asset_identifier: str,
                                     start_date: dt.date,
                                     end_date: dt.date,
                                     asset_identifier_type=RiskModelUniverseIdentifierRequest.bbid,
                                     get_factors_by_name: bool = True,
                                     format: ReturnFormat = ReturnFormat.DATA_FRAME):
        """
        Get attribution by factor for an asset for a desired date range

        :param asset_identifier: asset identifier
        :param start_date: start date
        :param end_date: end date
        :param asset_identifier_type: type corresponding to the identifier passed in
        :param get_factors_by_name: whether to denote the results by factor name (True) or ID (False)
        :param format: which format to return the results in

        :return: factor attribution breakdown

        **Usage**

        Get the factor attribution (in percent) breakdown for any asset covered by the risk model

        **Examples**

        >>> from gs_quant.models.risk_model import FactorRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 5, 2)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = FactorRiskModel.get("MODEL_ID")
        >>> attribution_breakdown = model.get_asset_factor_attribution('AAPL UW', start_date, end_date)
        """

        # Get risk model data for the asset
        data_measures = [RiskModelDataMeasure.Asset_Universe,
                         RiskModelDataMeasure.Universe_Factor_Exposure,
                         RiskModelDataMeasure.Factor_Volatility,
                         RiskModelDataMeasure.Factor_Return,
                         RiskModelDataMeasure.Factor_Name,
                         RiskModelDataMeasure.Factor_Id,
                         RiskModelDataMeasure.Factor_Category]
        risk_results = self.get_data(data_measures, start_date, end_date,
                                     RiskModelDataAssetsRequest(identifier=asset_identifier_type,
                                                                universe=[asset_identifier]),
                                     limit_factors=True)['results']
        if len(risk_results) == 0:
            raise MqValueError(f'{asset_identifier} is not covered by {self.id}')
        if len(risk_results) < 2:
            raise MqValueError('Attribution cannot be calculated with only one day of risk data')
        factor_id_to_name_map = {}
        factor_attribution = []
        for i in range(1, len(risk_results)):
            attribution_on_date = {'Date': risk_results[i]['date']}
            for factor_data in risk_results[i]['factorData']:
                factor = factor_data['factorName'] if get_factors_by_name else factor_data['factorId']
                attribution_on_date[factor] = factor_data['factorReturn']
                factor_id_to_name_map[factor_data['factorId']] = factor_data['factorName']

            previous_factor_exposures = risk_results[i - 1]['assetData']['factorExposure'][0]
            for factor_id in previous_factor_exposures:
                factor = factor_id_to_name_map[factor_id] if get_factors_by_name else factor_id
                factor_exposure = previous_factor_exposures[factor_id]
                attribution_on_date[factor] *= factor_exposure
            factor_attribution.append(attribution_on_date)

        return pd.DataFrame(factor_attribution) if format == ReturnFormat.DATA_FRAME else factor_attribution

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
        if self.universe_size:
            s += ", universe_size={}".format(self)
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
                 universe_size: int = None,
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
        :param universe_size: total rough expected universe size (rounding up to nearest 1k)
        :param entitlements: entitlements associated with risk model
        :param description: risk model description
        :param expected_update_time: time when risk model daily data is expected to be uploaded

        :return: MacroRiskModel object
        """
        super().__init__(id_, name, RiskModelType.Macro, vendor, version, coverage, universe_identifier, term,
                         universe_size=universe_size, entitlements=entitlements, description=description,
                         expected_update_time=expected_update_time)

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
            universe_size=model.universe_size,
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
        """ Get many Macro risk models from Marquee

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
                                 assets: DataAssetsRequest = DataAssetsRequest(
                                     RiskModelUniverseIdentifierRequest.gsid, []),
                                 factor_type: FactorType = FactorType.Factor,
                                 get_factors_by_name: bool = False,
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME
                                 ) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe factor or factor category sensitivity data for existing macro risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param factor_type: If factor type is factor, return factor sensitivity. Otherwise, return factor category
        sensitivity.
        :param get_factors_by_name: return results keyed by factor name instead of ID
        :param format: which format to return the results in

        :return: Factor or Factor Category sensitivity for assets requested

        **Usage**

        Given a list of assets, return their sensitivity to macro factors (when the factor_type is `Factor`)
         or macro factor categories (when the factor_type is Category).

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MacroRiskModel.get("MODEL_ID")
        >>> sensitivity = model.get_universe_sensitivity(start_date, end_date,
        ...                                              DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**

        :func:`get_r_squared` :func:`factor_standard_deviation` :func:`factor_z_score`
        """

        sensitivity_df = super().get_universe_exposure(start_date, end_date, assets,
                                                       get_factors_by_name=get_factors_by_name, format=format) \
            if factor_type == FactorType.Factor else \
            super().get_universe_exposure(start_date, end_date, assets, get_factors_by_name=get_factors_by_name)

        if factor_type == FactorType.Factor or sensitivity_df.empty:
            return sensitivity_df

        factor_data = self.get_factor_data(start_date, end_date)
        factor_data = factor_data.set_index("name") if get_factors_by_name else factor_data.set_index("identifier")
        columns = [(factor_data.loc[f, "factorCategory"], f) for f in sensitivity_df.columns.values] \
            if get_factors_by_name else \
            [(factor_data.loc[f, "factorCategoryId"], f) for f in sensitivity_df.columns.values]
        sensitivity_df = sensitivity_df.set_axis(pd.MultiIndex.from_tuples(columns), axis=1)

        factor_categories = list(set(sensitivity_df.columns.get_level_values(0).values))
        factor_category_sens_df = pd.concat(
            [sensitivity_df[factor_category].agg(np.sum, axis=1).to_frame().rename(columns={0: factor_category})
             for factor_category in factor_categories], axis=1
        )

        if format == ReturnFormat.JSON:
            factor_category_sens_df = factor_category_sens_df.to_dict(orient='index')
            factor_category_sens_dict = {}

            for key, value in factor_category_sens_df.items():
                temp_dict = factor_category_sens_dict.get(key[0], {})
                temp_dict[key[1]] = value
                factor_category_sens_dict[key[0]] = temp_dict

            return factor_category_sens_dict

        return factor_category_sens_df

    def get_r_squared(self,
                      start_date: dt.date,
                      end_date: dt.date = None,
                      assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                      format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get R Squared data for existing macro risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: The format to return the results in (Dataframe or Dict)
        :return: R Squared for assets requested

        **Usage**

        Given a list of assets, return the r squared for each asset between `start_date` and `end_date`.

        **Examples**

        >>> start = dt.date(2022, 1, 1)
        >>> end = dt.date(2022, 5, 2)
        >>> model = MacroRiskModel.get("MODEL_ID")
        >>> r_squared_df = model.get_r_squared(start, end, DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        To get the data in dict format, specify the return format to JSON

        >>> r_squared_dict = model.get_r_squared(start, end,
        ...                                      DataAssetsRequest(RiskModelUniverseIdentifierRequest.bbid, ['GS UN'],
        ...                                      ReturnFormat.JSON)

        **See also**

        :func:`get_fair_value_gap` :func:`factor_standard_deviation` :func:`factor_z_score`
        """

        return self._get_asset_data_measure(Measure.R_Squared, start_date, end_date, assets, format)

    def get_fair_value_gap(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = DataAssetsRequest(RiskModelUniverseIdentifierRequest.gsid, []),
                           fair_value_gap_unit: Unit = Unit.STANDARD_DEVIATION,
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:

        """ Get fair value gap data for a list of assets between start date and end date

        :param start_date: The start date for data request.
        :param end_date: The end date for data request.
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request.
        :param fair_value_gap_unit: Return the fair value gap value expressed in this unit. The default is
                                    standard deviation.
        :param format: The format to return the data in. The default is pandas Dataframe.

        :return: Fair Value Gap for the assets requested

        **Usage**

        Given a list of assets, return the fair value gap for each asset between `start_date`
        and `end_date`. The data can be returned as a pandas DataFrame or as a dict.

        **Examples**

        Get the fair value gap data in a dataframe format between start and end.
        >>> from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, \
        ...                      RiskModelUniverseIdentifierRequest as UniverseIdentifier, ReturnFormat
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MacroRiskModel.get("MODEL_ID")
        >>> fvg_df = model.get_fair_value_gap(start_date, end_date,
        ...                                   DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        To get the data in percentage, specify the fair_value_gap_unit to PERCENT.

        >>> fvg_df = model.get_fair_value_gap(start_date, end_date,
        ...                                   DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']), Unit.PERCENT)

        **See also**

        :func:`get_r_squared` :func:`factor_standard_deviation` :func:`factor_z_score`
        """

        return self._get_asset_data_measure(
            Measure.Fair_Value_Gap_Standard_Deviation
            if fair_value_gap_unit == Unit.STANDARD_DEVIATION
            else Measure.Fair_Value_Gap_Percent,
            start_date,
            end_date,
            assets,
            format)

    def get_factor_z_score(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = None,
                           factors: List[str] = [],
                           factors_by_name: bool = True,
                           format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get factor z score data for existing risk model keyed by name or id

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to limit the factors by
        :param factors: the factors to get z score data for. If empty, the data for all factors is returned
        :param factors_by_name: whether to identify factors by their name or id. If true, the list of factors must \
         be a list of factor names. Otherwise, it should be a list of factor ids
        :param format: which format to return the results in

        :return: factor z score

        **Usage**

        Get the z score of the factors specified in `factors`

        **Examples**

        >>> from gs_quant.models.risk_model import MacroRiskModel
        >>> import datetime as dt
        >>>
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MacroRiskModel.get("MODEL_ID")
        >>> factor_z_score = model.get_factor_z_score(start_date, end_date, factors=['factor1', 'factor2'])

        **See also**

        :func:`get_r_squared` :func:`factor_standard_deviation` :func:`factor_z_score`
        """

        return self._get_factor_data_measure(Measure.Factor_Z_Score,
                                             start_date,
                                             end_date,
                                             assets,
                                             factors_by_name,
                                             factors,
                                             format)

    def get_model_price(self,
                        start_date: dt.date,
                        end_date: dt.date = None,
                        assets: DataAssetsRequest = DataAssetsRequest(
                            RiskModelUniverseIdentifierRequest.gsid, []),
                        format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get model price data for existing risk model

        :param start_date: Start date for data request
        :param end_date: End date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param format: Which format to return the results in

        :return: Model price data

        **Usage**

        Get model price data for assets specified in `assets` between `start_date` and `end_date`

        **Example**
        >>> from gs_quant.models.risk_model import FactorRiskModel, DataAssetsRequest, \
        ...                                        RiskModelUniverseIdentifierRequest as UniverseIdentifier
        >>> import datetime as dt
        >>> start_date = dt.date(2022, 1, 1)
        >>> end_date = dt.date(2022, 5, 2)
        >>> model = MacroRiskModel.get("MODEL_ID")
        >>> model_price = model.get_model_price(start_date, end_date,
        ...                                                  DataAssetsRequest(UniverseIdentifier.bbid, ['GS UN']))

        **See also**
        :func:`get_r_squared` :func:`get_fair_value_gap`

        """
        return super()._get_asset_data_measure(Measure.Model_Price, start_date, end_date, assets, format)

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
        if self.universe_size:
            s += ", universe_size={}".format(self)
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
                 universe_size: int = None,
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
        :param universe_size: total rough expected universe size (rounding up to nearest 1k)
        :param entitlements: entitlements associated with risk model
        :param description: risk model description
        :param expected_update_time: time when risk model daily data is expected to be uploaded

        :return: Thematic Risk Model object
        """
        super().__init__(id_, name, RiskModelType.Thematic, vendor, version, coverage, universe_identifier, term,
                         universe_size=universe_size, entitlements=entitlements, description=description,
                         expected_update_time=expected_update_time)

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
            universe_size=model.universe_size,
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
                                 get_factors_by_name: bool = False,
                                 format: ReturnFormat = ReturnFormat.DATA_FRAME) -> Union[List[Dict], pd.DataFrame]:
        """ Get universe sensitivity data for existing thematic risk model

        :param start_date: start date for data request
        :param end_date: end date for data request
        :param assets: DataAssetsRequest object with identifier and list of assets to retrieve for request
        :param get_factors_by_name: return results keyed by factor name instead of ID
        :param format: which format to return the results in

        :return: basket sensitivity for assets requested
        """
        return super().get_universe_exposure(start_date, end_date, assets,
                                             get_factors_by_name=get_factors_by_name, format=format)

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
        if self.universe_size:
            s += ", universe_size={}".format(self)
        if self.entitlements:
            s += ", entitlements={}".format(self)
        if self.description:
            s += ", description={}".format(self)
        if self.expected_update_time:
            s += ", expected_update_time={}".format(self)

        s += ")"
        return s
