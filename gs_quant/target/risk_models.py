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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from enum import Enum


class RiskModelCoverage(EnumBase, Enum):    
    
    """Allowed risk model coverages"""

    Global = 'Global'
    Region = 'Region'
    Region_Excluding_Countries = 'Region Excluding Countries'
    Country = 'Country'    


class RiskModelDataMeasure(EnumBase, Enum):    
    
    """A list of the different risk model data measures to choose from."""

    Asset_Universe = 'Asset Universe'
    Historical_Beta = 'Historical Beta'
    Total_Risk = 'Total Risk'
    Specific_Risk = 'Specific Risk'
    Specific_Return = 'Specific Return'
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


class RiskModelEventType(EnumBase, Enum):    
    
    """Event type for risk model class."""

    Risk_Model = 'Risk Model'
    Risk_Model_PFP_Data = 'Risk Model PFP Data'
    Risk_Model_ISC_Data = 'Risk Model ISC Data'    


class RiskModelLogicalDb(EnumBase, Enum):    
    
    QSAR_AX_NYC = 'QSAR_AX_NYC'
    STUDIO_DAILY = 'STUDIO_DAILY'    


class RiskModelTerm(EnumBase, Enum):    
    
    """Allowed risk model terms"""

    Trading = 'Trading'
    Day = 'Day'
    Short = 'Short'
    Medium = 'Medium'
    Long = 'Long'    


class RiskModelUniverseIdentifier(EnumBase, Enum):    
    
    """The identifier which the risk model is uploaded by."""

    sedol = 'sedol'
    bcid = 'bcid'
    cusip = 'cusip'
    gsid = 'gsid'    


class RiskModelUniverseIdentifierRequest(EnumBase, Enum):    
    
    """The identifier which the risk model is queried by."""

    gsid = 'gsid'
    bbid = 'bbid'
    cusip = 'cusip'
    sedol = 'sedol'
    ric = 'ric'
    ticker = 'ticker'
    primeId = 'primeId'    


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Factor(Base):
    identifier: str = None
    type_: str = field(default=None, metadata=config(field_name='type'))
    description: Optional[str] = None
    glossary_description: Optional[str] = None
    tooltip: Optional[str] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelCalendar(Base):
    business_dates: Tuple[datetime.date, ...] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelFactorData(Base):
    factor_id: str = None
    factor_name: str = None
    factor_category_id: str = None
    factor_category: str = None
    factor_return: float = None


RiskModelFactorExposure = Dict[str, float]


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelFactorPortfolio(Base):
    factor_id: str = None
    weights: Tuple[float, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelIssuerSpecificCovarianceData(Base):
    universe_id1: Tuple[str, ...] = None
    universe_id2: Tuple[str, ...] = None
    covariance: Tuple[float, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelAssetData(Base):
    universe: Tuple[str, ...] = None
    specific_risk: Tuple[float, ...] = None
    factor_exposure: Tuple[RiskModelFactorExposure, ...] = None
    specific_return: Optional[Tuple[float, ...]] = None
    residual_variance: Optional[Tuple[float, ...]] = None
    historical_beta: Optional[Tuple[float, ...]] = None
    total_risk: Optional[Tuple[float, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelCoverageRequest(Base):
    asset_ids: Optional[Tuple[str, ...]] = None
    as_of_date: Optional[datetime.date] = None
    sort_by_term: Optional[RiskModelTerm] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelDataAssetsRequest(Base):
    identifier: RiskModelUniverseIdentifierRequest = None
    universe: Tuple[str, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelFactorPortfoliosData(Base):
    universe: Tuple[str, ...] = None
    portfolio: Tuple[RiskModelFactorPortfolio, ...] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModel(Base):
    coverage: RiskModelCoverage = None
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None
    term: RiskModelTerm = None
    universe_identifier: RiskModelUniverseIdentifier = None
    vendor: str = None
    version: float = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    description: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    last_updated_by_id: Optional[str] = None
    last_updated_time: Optional[datetime.datetime] = None
    expected_update_time: Optional[str] = None
    owner_id: Optional[str] = None
    type_: Optional[RiskModelType] = field(default=None, metadata=config(field_name='type'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelData(Base):
    date: datetime.date = None
    asset_data: Optional[RiskModelAssetData] = None
    factor_data: Optional[Tuple[RiskModelFactorData, ...]] = None
    covariance_matrix: Optional[Tuple[Tuple[float, ...], ...]] = None
    issuer_specific_covariance: Optional[RiskModelIssuerSpecificCovarianceData] = None
    factor_portfolios: Optional[RiskModelFactorPortfoliosData] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelDataRequest(Base):
    start_date: datetime.date = None
    end_date: datetime.date = None
    assets: Optional[RiskModelDataAssetsRequest] = None
    measures: Optional[Tuple[RiskModelDataMeasure, ...]] = None
    limit_factors: Optional[bool] = True
    format_: Optional[str] = field(default='Json', metadata=config(field_name='format'))


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelDataResponse(Base):
    results: Tuple[RiskModelData, ...] = None
    total_results: int = None
    missing_dates: Optional[Tuple[datetime.date, ...]] = None
