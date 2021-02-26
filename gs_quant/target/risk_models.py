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
from typing import List

from gs_quant.target.common import *


class CoverageType(EnumBase, Enum):
    """Coverage for risk model"""

    Global = 'Global'
    Region = 'Region'
    Region_Excluding_Countries = 'Region Excluding Countries'
    Country = 'Country'

    def __repr__(self):
        return self.value


class Term(EnumBase, Enum):
    """Allowed risk model terms"""

    Short = 'Short'
    Medium = 'Medium'
    Long = 'Long'

    def __repr__(self):
        return self.value


class UniverseIdentifier(EnumBase, Enum):
    """Identifier by which risk model is uploaded"""

    sedol = 'sedol'
    bcid = 'bcid'
    cusip = 'cusip'
    gsid = 'gsid'

    def __repr__(self):
        return self.value


class FactorType(EnumBase, Enum):
    """Factor represents a risk factor and Category represents a risk factor category"""

    Factor = 'Factor'
    Category = 'Category'

    def __repr__(self):
        return self.value


class Measure(EnumBase, Enum):
    """Different risk model data measures to choose from"""

    Asset_Universe = 'Asset Universe'
    Historical_Beta = 'Historical Beta'
    Total_Risk = 'Total Risk'
    Specific_Risk = 'Specific Risk'
    Residual_Variance = 'Residual Variance'
    Universe_Factor_Exposure = 'Universe Factor Exposure'
    Factor_Id = 'Factor Id'
    Factor_Name = 'Factor Name'
    Factor_Category_Id = 'Factor Category Id'
    Factor_Category = 'Factor Category'
    Factor_Return = 'Factor Return'
    Covariance_Matrix = 'Covariance Matrix'
    Issuer_Specific_Covariance = 'Issuer Specific Covariance'
    Factor_Portfolios = 'Factor Portfolios'

    def __repr__(self):
        return self.value


class Format(EnumBase, Enum):
    """Alternative format for data to be returned"""

    Json = 'Json'
    Message_pack = 'Message Pack'

    def __repr__(self):
        return self.value


class AssetData(Base):

    @camel_case_translate
    def __init__(
            self,
            universe: List[str],
            specific_risk: List[float],
            factor_exposure: List,
            historical_beta: List[float] = None,
            total_risk: List[float] = None
    ):
        super().__init__()
        self.universe = universe
        self.specific_risk = specific_risk
        self.factor_exposure = factor_exposure
        self.historical_beta = historical_beta
        self.total_risk = total_risk

    @property
    def universe(self) -> List[str]:
        """Model universe uploaded as an array of identifiers"""
        return self.__universe

    @universe.setter
    def universe(self, value: List[str]):
        self._property_changed('universe')
        self.__universe = value

    @property
    def specific_risk(self) -> List[float]:
        """Asset annualized specific risk in percent units"""
        return self.__specific_risk

    @specific_risk.setter
    def specific_risk(self, value: List[float]):
        self._property_changed('specific_risk')
        self.__specific_risk = value

    @property
    def factor_exposure(self) -> List:
        """Asset factor exposure"""
        return self.__factor_exposure

    @factor_exposure.setter
    def factor_exposure(self, value: List):
        self._property_changed('factor_exposure')
        self.__factor_exposure = value

    @property
    def historical_beta(self) -> List[float]:
        """Asset historical beta"""
        return self.__historical_beta

    @historical_beta.setter
    def historical_beta(self, value: List[float]):
        self._property_changed('historical_beta')
        self.__historical_beta = value

    @property
    def total_risk(self) -> List[float]:
        """Asset total risk in percent units"""
        return self.__total_risk

    @total_risk.setter
    def total_risk(self, value: List[float]):
        self._property_changed('total_risk')
        self.__total_risk = value


class FactorData(Base):

    @camel_case_translate
    def __init__(
            self,
            factor_id: str,
            factor_name: str,
            factor_category_id: str,
            factor_category: str,
            factor_return: float
    ):
        super().__init__()
        self.factor_id = factor_id
        self.factor_name = factor_name
        self.factor_category_id = factor_category_id
        self.factor_category = factor_category
        self.factor_return = factor_return

    @property
    def factor_id(self) -> str:
        """Identifier associated with the factor"""
        return self.__factor_id

    @factor_id.setter
    def factor_id(self, value: str):
        self._property_changed('factor_id')
        self.__factor_id = value

    @property
    def factor_name(self) -> str:
        """Text to display when representing the factor"""
        return self.factor_name

    @factor_name.setter
    def factor_name(self, value: str):
        self._property_changed('factor_name')
        self.__factor_name = value

    @property
    def factor_category_id(self) -> str:
        """ID for factor categories"""
        return self.__factor_category_id

    @factor_category_id.setter
    def factor_category_id(self, value: str):
        self._property_changed('factor_category_id')
        self.__factor_category_id = value

    @property
    def factor_category(self) -> str:
        """ID for factor categories"""
        return self.__factor_category

    @factor_category.setter
    def factor_category(self, value: str):
        self._property_changed('factor_category')
        self.__factor_category = value

    @property
    def factor_return(self) -> float:
        """ID for factor categories"""
        return self.__factor_return

    @factor_return.setter
    def factor_return(self, value: float):
        self._property_changed('factor_return')
        self.__factor_return = value


class CovarianceData(Base):

    @camel_case_translate
    def __init__(
            self,
            universe_id_1: List[str],
            universe_id_2: List[str],
            covariance: List[float]
    ):
        super().__init__()
        self.universe_id_1 = universe_id_1
        self.universe_id_2 = universe_id_2
        self.covariance = covariance

    @property
    def universe_id_1(self) -> List[str]:
        """First universe identifier for which variance value is attributed"""
        return self.__universe_id_1

    @universe_id_1.setter
    def universe_id_1(self, value: List[str]):
        self._property_changed('universe_id_1')
        self.__universe_id_1 = value

    @property
    def universe_id_2(self) -> List[str]:
        """Second universe identifier for which variance value is attributed"""
        return self.__universe_id_2

    @universe_id_2.setter
    def universe_id_2(self, value: List[str]):
        self._property_changed('universe_id_2')
        self.__universe_id_2 = value

    @property
    def covariance(self) -> List[float]:
        """Covariance of assets in daily variance units"""
        return self.__covariance

    @covariance.setter
    def covariance(self, value: List[float]):
        self._property_changed('covariance')
        self.__covariance = value


class FactorPortfolio(Base):

    @camel_case_translate
    def __init__(
            self,
            factor_id: str,
            weight: List[float]
    ):
        super().__init__()
        self.factor_id = factor_id
        self.weight = weight

    @property
    def factor_id(self) -> str:
        """Factor identifier for which portfolio is behind"""
        return self.__factor_id

    @factor_id.setter
    def factor_id(self, value: str):
        self._property_changed('factor_id')
        self.__factor_id = value

    @property
    def weight(self) -> List[float]:
        """Weights for each asset in the portfolio"""
        return self.__weight

    @weight.setter
    def weight(self, value: List[float]):
        self._property_changed('weight')
        self.__weight = value


class FactorPortfolioData(Base):

    @camel_case_translate
    def __init__(
            self,
            universe: List[str],
            portfolio: List[FactorPortfolio]
    ):
        super().__init__()
        self.universe = universe
        self.portfolio = portfolio

    @property
    def universe(self) -> List[str]:
        """Universe of the portfolio"""
        return self.__universe

    @universe.setter
    def universe(self, value: List[str]):
        self._property_changed('universe')
        self.__universe = value

    @property
    def portfolio(self) -> List[FactorPortfolio]:
        """Array of factor and portfolio weights"""
        return self.__portfolio

    @portfolio.setter
    def portfolio(self, value: List[FactorPortfolio]):
        self._property_changed('portfolio')
        self.__portfolio = value


class DataAssetsRequest(Base):

    @camel_case_translate
    def __init__(
            self,
            identifier: Union[UniverseIdentifier, str],
            universe: List[str]
    ):
        super().__init__()
        self.identifier = get_enum_value(UniverseIdentifier, identifier)
        self.universe = universe

    @property
    def identifier(self) -> Union[UniverseIdentifier, str]:
        """The identifier by which the risk model is queried"""
        return self.__identifier

    @identifier.setter
    def identifier(self, value: Union[UniverseIdentifier, str]):
        self._property_changed('identifier')
        self.__identifier = get_enum_value(UniverseIdentifier, value)

    @property
    def universe(self) -> List[str]:
        """Set of asset identifiers for which to get model data"""
        return self.__universe

    @universe.setter
    def universe(self, value: List[str]):
        self._property_changed('universe')
        self.__universe = value


class RiskModelData(Base):

    @camel_case_translate
    def __init__(
            self,
            date: datetime.date,
            asset_data: AssetData = None,
            factor_data: List[FactorData] = None,
            covariance_matrix: List = None,
            issuer_specific_covariance: CovarianceData = None,
            factor_portfolios: FactorPortfolioData = None
    ):
        super().__init__()
        self.date = date.strftime('%Y-%m-%d')
        self.asset_data = asset_data
        self.factor_data = factor_data
        self.covariance_matrix = covariance_matrix
        self.issuer_specific_covariance = issuer_specific_covariance
        self.factor_portfolios = factor_portfolios

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.datetime):
        self._property_changed('date')
        self.__date = value

    @property
    def asset_data(self) -> AssetData:
        """Asset data of the risk model on a specific date"""
        return self.__asset_data

    @asset_data.setter
    def asset_data(self, value: AssetData):
        self._property_changed('asset_data')
        self.__asset_data = value

    @property
    def factor_data(self) -> List[FactorData]:
        """Factor data of the risk model on a specific date"""
        return self.__factor_data

    @factor_data.setter
    def factor_data(self, value: List[FactorData]):
        self._property_changed('factor_data')
        self.__factor_data = value

    @property
    def covariance_matrix(self) -> List:
        """Covariance matrix of the risk model on a specific date, in daily variance units"""
        return self.__covariance_matrix

    @covariance_matrix.setter
    def covariance_matrix(self, value: List):
        self._property_changed('covariance_matrix')
        self.__covariance_matrix = value

    @property
    def issuer_specific_covariance(self) -> CovarianceData:
        """Covariance between two assets"""
        return self.__issuer_specific_covariance

    @issuer_specific_covariance.setter
    def issuer_specific_covariance(self, value: CovarianceData):
        self._property_changed('issuer_specific_covariance')
        self.__issuer_specific_covariance = value

    @property
    def factor_portfolios(self) -> FactorPortfolioData:
        """Portfolios behind each factor"""
        return self.__factor_portfolios

    @factor_portfolios.setter
    def factor_portfolios(self, value: FactorPortfolioData):
        self._property_changed('factor_portfolios')
        self.__factor_portfolios = value


class RiskModel(Base):

    @camel_case_translate
    def __init__(
            self,
            coverage: Union[CoverageType, str],
            id_: str,
            name: str,
            term: Union[Term, str],
            universe_identifier: Union[UniverseIdentifier, str],
            vendor: str,
            version: float,
            created_by_id: str = None,
            created_time: datetime.datetime = None,
            last_updated_by_id: str = None,
            last_updated_time: datetime.datetime = None,
            description: str = None,
            entitlements: Entitlements = None,
            owner_id: str = None,
    ):
        super().__init__()
        self.coverage = get_enum_value(CoverageType, coverage)
        self.__id = id_
        self.name = name
        self.term = get_enum_value(Term, term)
        self.universe_identifier = get_enum_value(UniverseIdentifier, universe_identifier)
        self.vendor = vendor
        self.version = version
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.description = description
        self.entitlements = entitlements
        self.owner_id = owner_id

    @property
    def coverage(self) -> Union[CoverageType, str]:
        """Allowed risk model coverages"""
        return self.__coverage

    @coverage.setter
    def coverage(self, value: Union[CoverageType, str]):
        self._property_changed('coverage')
        self.__coverage = get_enum_value(CoverageType, value)

    @property
    def id(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value

    @property
    def name(self) -> str:
        """Risk model name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value

    @property
    def term(self) -> Union[Term, str]:
        """Allowed risk model terms"""
        return self.__term

    @term.setter
    def term(self, value: Union[Term, str]):
        self._property_changed('term')
        self.__term = get_enum_value(Term, value)

    @property
    def universe_identifier(self) -> Union[UniverseIdentifier, str]:
        """The identifier by which the risk model is uploaded"""
        return self.__universe_identifier

    @universe_identifier.setter
    def universe_identifier(self, value: Union[UniverseIdentifier, str]):
        self._property_changed('universe_identifier')
        self.__universe_identifier = get_enum_value(UniverseIdentifier, value)

    @property
    def vendor(self) -> str:
        """Risk model vendor name"""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self._property_changed('vendor')
        self.__vendor = value

    @property
    def version(self) -> float:
        """Version number"""
        return self.__version

    @version.setter
    def version(self, value: float):
        self._property_changed('version')
        self.__version = value

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
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
    def description(self) -> str:
        """Description of risk model"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier of who owns risk model"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value


class RiskModelFactor(Base):

    @camel_case_translate
    def __init__(
            self,
            identifier: str,
            type_: Union[FactorType, str],
            name: str = None,
            description: str = None,
            glossary_description: str = None,
            tooltip: str = None,
            created_by_id: str = None,
            created_time: datetime.datetime = None,
            last_updated_by_id: str = None,
            last_updated_time: datetime.datetime = None,
    ):
        super().__init__()
        self.identifier = identifier
        self.__type = get_enum_value(FactorType, type_)
        self.name = name
        self.description = description
        self.glossary_description = glossary_description
        self.tooltip = tooltip
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time

    @property
    def identifier(self) -> str:
        """The corresponding factorId or factorCategoryId, depending on factor type"""
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str):
        self._property_changed('identifier')
        self.__identifier = value

    @property
    def type(self) -> Union[FactorType, str]:
        """Factor type"""
        return self.__type

    @type.setter
    def type(self, value: Union[FactorType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(FactorType, value)

    @property
    def name(self) -> str:
        """Factor name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value

    @property
    def description(self) -> str:
        """Description of the factor to be displayed on the factor break down page"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value

    @property
    def glossary_description(self) -> str:
        """A more in depth factor description to be displayed on the glossary page"""
        return self.__glossary_description

    @glossary_description.setter
    def glossary_description(self, value: str):
        self._property_changed('glossary_description')
        self.__glossary_description = value

    @property
    def tooltip(self) -> str:
        """A short description of the factor to be displayed in a tooltip"""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
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


class RiskModelCalendar(Base):

    @camel_case_translate
    def __init__(
            self,
            business_dates: List[str],
            created_by_id: str = None,
            created_time: datetime.datetime = None,
            last_updated_by_id: str = None,
            last_updated_time: datetime.datetime = None,
    ):
        super().__init__()
        self.business_dates = business_dates
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time

    @property
    def business_dates(self) -> List[str]:
        """Array of quantity position objects"""
        return self.__business_dates

    @business_dates.setter
    def business_dates(self, value: List[str]):
        self._property_changed('business_dates')
        self.__business_dates = value

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
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
