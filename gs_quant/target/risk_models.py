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


class Currency(EnumBase, Enum):    
    
    """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""

    _ = ''
    ACU = 'ACU'
    ADP = 'ADP'
    AED = 'AED'
    AFA = 'AFA'
    ALL = 'ALL'
    AMD = 'AMD'
    ANG = 'ANG'
    AOA = 'AOA'
    AOK = 'AOK'
    AON = 'AON'
    ARA = 'ARA'
    ARS = 'ARS'
    ARZ = 'ARZ'
    ATS = 'ATS'
    AUD = 'AUD'
    AUZ = 'AUZ'
    AZM = 'AZM'
    AZN = 'AZN'
    B03 = 'B03'
    BAD = 'BAD'
    BAK = 'BAK'
    BAM = 'BAM'
    BBD = 'BBD'
    BDN = 'BDN'
    BDT = 'BDT'
    BEF = 'BEF'
    BGL = 'BGL'
    BGN = 'BGN'
    BHD = 'BHD'
    BIF = 'BIF'
    BMD = 'BMD'
    BND = 'BND'
    BOB = 'BOB'
    BR6 = 'BR6'
    BRE = 'BRE'
    BRF = 'BRF'
    BRL = 'BRL'
    BRR = 'BRR'
    BSD = 'BSD'
    BTC = 'BTC'
    BTN = 'BTN'
    BTR = 'BTR'
    BWP = 'BWP'
    BYR = 'BYR'
    BZD = 'BZD'
    C23 = 'C23'
    CAC = 'CAC'
    CAD = 'CAD'
    CAZ = 'CAZ'
    CCI = 'CCI'
    CDF = 'CDF'
    CFA = 'CFA'
    CHF = 'CHF'
    CHZ = 'CHZ'
    CLF = 'CLF'
    CLP = 'CLP'
    CLZ = 'CLZ'
    CNH = 'CNH'
    CNO = 'CNO'
    CNY = 'CNY'
    CNZ = 'CNZ'
    COP = 'COP'
    COZ = 'COZ'
    CPB = 'CPB'
    CPI = 'CPI'
    CRC = 'CRC'
    CUP = 'CUP'
    CVE = 'CVE'
    CYP = 'CYP'
    CZH = 'CZH'
    CZK = 'CZK'
    DAX = 'DAX'
    DEM = 'DEM'
    DIJ = 'DIJ'
    DJF = 'DJF'
    DJE = 'DJE'
    DKK = 'DKK'
    DOP = 'DOP'
    DZD = 'DZD'
    E51 = 'E51'
    E52 = 'E52'
    E53 = 'E53'
    E54 = 'E54'
    ECI = 'ECI'
    ECS = 'ECS'
    ECU = 'ECU'
    EEK = 'EEK'
    EF0 = 'EF0'
    EGP = 'EGP'
    ESP = 'ESP'
    ETB = 'ETB'
    ETH = 'ETH'
    EUR = 'EUR'
    EUZ = 'EUZ'
    F06 = 'F06'
    FED = 'FED'
    FIM = 'FIM'
    FJD = 'FJD'
    FKP = 'FKP'
    FRF = 'FRF'
    FT1 = 'FT1'
    GBP = 'GBP'
    GBZ = 'GBZ'
    GEK = 'GEK'
    GEL = 'GEL'
    GHC = 'GHC'
    GHS = 'GHS'
    GHY = 'GHY'
    GIP = 'GIP'
    GLD = 'GLD'
    GLR = 'GLR'
    GMD = 'GMD'
    GNF = 'GNF'
    GQE = 'GQE'
    GRD = 'GRD'
    GTQ = 'GTQ'
    GWP = 'GWP'
    GYD = 'GYD'
    HKB = 'HKB'
    HKD = 'HKD'
    HNL = 'HNL'
    HRK = 'HRK'
    HSI = 'HSI'
    HTG = 'HTG'
    HUF = 'HUF'
    IDB = 'IDB'
    IDO = 'IDO'
    IDR = 'IDR'
    IEP = 'IEP'
    IGP = 'IGP'
    ILS = 'ILS'
    INO = 'INO'
    INP = 'INP'
    INR = 'INR'
    IPA = 'IPA'
    IPX = 'IPX'
    IQD = 'IQD'
    IRR = 'IRR'
    IRS = 'IRS'
    ISI = 'ISI'
    ISK = 'ISK'
    ISO = 'ISO'
    ITL = 'ITL'
    J05 = 'J05'
    JMD = 'JMD'
    JNI = 'JNI'
    JOD = 'JOD'
    JPY = 'JPY'
    JPZ = 'JPZ'
    JZ9 = 'JZ9'
    KES = 'KES'
    KGS = 'KGS'
    KHR = 'KHR'
    KMF = 'KMF'
    KOR = 'KOR'
    KPW = 'KPW'
    KRW = 'KRW'
    KWD = 'KWD'
    KYD = 'KYD'
    KZT = 'KZT'
    LAK = 'LAK'
    LBA = 'LBA'
    LBP = 'LBP'
    LHY = 'LHY'
    LKR = 'LKR'
    LRD = 'LRD'
    LSL = 'LSL'
    LSM = 'LSM'
    LTL = 'LTL'
    LUF = 'LUF'
    LVL = 'LVL'
    LYD = 'LYD'
    MAD = 'MAD'
    MDL = 'MDL'
    MGF = 'MGF'
    MKD = 'MKD'
    MMK = 'MMK'
    MNT = 'MNT'
    MOP = 'MOP'
    MRO = 'MRO'
    MTL = 'MTL'
    MTP = 'MTP'
    MUR = 'MUR'
    MVR = 'MVR'
    MWK = 'MWK'
    MXB = 'MXB'
    MXN = 'MXN'
    MXP = 'MXP'
    MXW = 'MXW'
    MXZ = 'MXZ'
    MYO = 'MYO'
    MYR = 'MYR'
    MZM = 'MZM'
    MZN = 'MZN'
    NAD = 'NAD'
    ND3 = 'ND3'
    NGF = 'NGF'
    NGI = 'NGI'
    NGN = 'NGN'
    NIC = 'NIC'
    NIO = 'NIO'
    NLG = 'NLG'
    NOK = 'NOK'
    NOZ = 'NOZ'
    NPR = 'NPR'
    NZD = 'NZD'
    NZZ = 'NZZ'
    O08 = 'O08'
    OMR = 'OMR'
    PAB = 'PAB'
    PEI = 'PEI'
    PEN = 'PEN'
    PEZ = 'PEZ'
    PGK = 'PGK'
    PHP = 'PHP'
    PKR = 'PKR'
    PLN = 'PLN'
    PLZ = 'PLZ'
    PSI = 'PSI'
    PTE = 'PTE'
    PYG = 'PYG'
    QAR = 'QAR'
    R2K = 'R2K'
    ROL = 'ROL'
    RON = 'RON'
    RSD = 'RSD'
    RUB = 'RUB'
    RUF = 'RUF'
    RUR = 'RUR'
    RWF = 'RWF'
    SAR = 'SAR'
    SBD = 'SBD'
    SCR = 'SCR'
    SDP = 'SDP'
    SDR = 'SDR'
    SEK = 'SEK'
    SET = 'SET'
    SGD = 'SGD'
    SGS = 'SGS'
    SHP = 'SHP'
    SIL = 'SIL'
    SIT = 'SIT'
    SKK = 'SKK'
    SLL = 'SLL'
    SRG = 'SRG'
    SSI = 'SSI'
    STD = 'STD'
    SUR = 'SUR'
    SVC = 'SVC'
    SVT = 'SVT'
    SYP = 'SYP'
    SZL = 'SZL'
    T21 = 'T21'
    T51 = 'T51'
    T52 = 'T52'
    T53 = 'T53'
    T54 = 'T54'
    T55 = 'T55'
    T71 = 'T71'
    TE0 = 'TE0'
    TED = 'TED'
    TF9 = 'TF9'
    THB = 'THB'
    THO = 'THO'
    TMM = 'TMM'
    TND = 'TND'
    TNT = 'TNT'
    TOP = 'TOP'
    TPE = 'TPE'
    TPX = 'TPX'
    TRB = 'TRB'
    TRL = 'TRL'
    TRY = 'TRY'
    TRZ = 'TRZ'
    TTD = 'TTD'
    TWD = 'TWD'
    TZS = 'TZS'
    UAH = 'UAH'
    UCB = 'UCB'
    UDI = 'UDI'
    UFC = 'UFC'
    UFZ = 'UFZ'
    UGS = 'UGS'
    UGX = 'UGX'
    USB = 'USB'
    USD = 'USD'
    UVR = 'UVR'
    UYP = 'UYP'
    UYU = 'UYU'
    UZS = 'UZS'
    VAC = 'VAC'
    VEB = 'VEB'
    VEF = 'VEF'
    VES = 'VES'
    VND = 'VND'
    VUV = 'VUV'
    WST = 'WST'
    XAF = 'XAF'
    XAG = 'XAG'
    XAU = 'XAU'
    XPD = 'XPD'
    XPT = 'XPT'
    XCD = 'XCD'
    XDR = 'XDR'
    XEU = 'XEU'
    XOF = 'XOF'
    XPF = 'XPF'
    YDD = 'YDD'
    YER = 'YER'
    YUD = 'YUD'
    YUN = 'YUN'
    ZAL = 'ZAL'
    ZAR = 'ZAR'
    ZAZ = 'ZAZ'
    ZMK = 'ZMK'
    ZMW = 'ZMW'
    ZRN = 'ZRN'
    ZRZ = 'ZRZ'
    ZWD = 'ZWD'
    ZWL = 'ZWL'
    AUd = 'AUd'
    BWp = 'BWp'
    EUr = 'EUr'
    GBp = 'GBp'
    ILs = 'ILs'
    KWd = 'KWd'
    MWk = 'MWk'
    SGd = 'SGd'
    SZl = 'SZl'
    USd = 'USd'
    ZAr = 'ZAr'    


class RiskModelCoverage(EnumBase, Enum):    
    
    """Allowed risk model coverages"""

    Country = 'Country'
    Global = 'Global'
    Market_Type = 'Market Type'
    Region = 'Region'    


class RiskModelDataMeasure(EnumBase, Enum):    
    
    """A list of the different risk model data measures to choose from."""

    Asset_Universe = 'Asset Universe'
    Historical_Beta = 'Historical Beta'
    Total_Risk = 'Total Risk'
    Specific_Risk = 'Specific Risk'
    Specific_Return = 'Specific Return'
    Daily_Return = 'Daily Return'
    Estimation_Universe_Weight = 'Estimation Universe Weight'
    Residual_Variance = 'Residual Variance'
    Predicted_Beta = 'Predicted Beta'
    Global_Predicted_Beta = 'Global Predicted Beta'
    Universe_Factor_Exposure = 'Universe Factor Exposure'
    R_Squared = 'R Squared'
    Fair_Value_Gap_Percent = 'Fair Value Gap Percent'
    Fair_Value_Gap_Standard_Deviation = 'Fair Value Gap Standard Deviation'
    Factor_Id = 'Factor Id'
    Factor_Name = 'Factor Name'
    Factor_Category_Id = 'Factor Category Id'
    Factor_Category = 'Factor Category'
    Factor_Return = 'Factor Return'
    Factor_Standard_Deviation = 'Factor Standard Deviation'
    Factor_Z_Score = 'Factor Z Score'
    Factor_Volatility = 'Factor Volatility'
    Covariance_Matrix = 'Covariance Matrix'
    Issuer_Specific_Covariance = 'Issuer Specific Covariance'
    Factor_Portfolios = 'Factor Portfolios'
    Bid_Ask_Spread = 'Bid Ask Spread'
    Bid_Ask_Spread_30d = 'Bid Ask Spread 30d'
    Bid_Ask_Spread_60d = 'Bid Ask Spread 60d'
    Bid_Ask_Spread_90d = 'Bid Ask Spread 90d'
    Trading_Volume = 'Trading Volume'
    Trading_Volume_30d = 'Trading Volume 30d'
    Trading_Volume_60d = 'Trading Volume 60d'
    Trading_Volume_90d = 'Trading Volume 90d'
    Traded_Value_30d = 'Traded Value 30d'
    Composite_Volume = 'Composite Volume'
    Composite_Volume_30d = 'Composite Volume 30d'
    Composite_Volume_60d = 'Composite Volume 60d'
    Composite_Volume_90d = 'Composite Volume 90d'
    Composite_Value_30d = 'Composite Value 30d'
    Issuer_Market_Cap = 'Issuer Market Cap'
    Price = 'Price'
    Model_Price = 'Model Price'
    Capitalization = 'Capitalization'
    Currency = 'Currency'
    Unadjusted_Specific_Risk = 'Unadjusted Specific Risk'
    Dividend_Yield = 'Dividend Yield'
    Pre_VRA_Covariance_Matrix = 'Pre VRA Covariance Matrix'
    Unadjusted_Covariance_Matrix = 'Unadjusted Covariance Matrix'    


class RiskModelEventType(EnumBase, Enum):    
    
    """Event type for risk model class."""

    Risk_Model = 'Risk Model'
    Risk_Model_PFP_Data = 'Risk Model PFP Data'
    Risk_Model_ISC_Data = 'Risk Model ISC Data'
    Risk_Model_AWS = 'Risk Model AWS'
    Risk_Model_PFP_Data_AWS = 'Risk Model PFP Data AWS'
    Risk_Model_ISC_Data_AWS = 'Risk Model ISC Data AWS'    


class RiskModelLogicalDb(EnumBase, Enum):    
    
    QSAR_AX_NYC = 'QSAR_AX_NYC'
    STUDIO_DAILY = 'STUDIO_DAILY'    


class RiskModelTerm(EnumBase, Enum):    
    
    """Allowed risk model terms"""

    Trading = 'Trading'
    Daily = 'Daily'
    Short = 'Short'
    Medium = 'Medium'
    Long = 'Long'    


class RiskModelType(EnumBase, Enum):    
    
    """Marquee risk model type"""

    Factor = 'Factor'
    Macro = 'Macro'
    Thematic = 'Thematic'    


class RiskModelUniverseIdentifier(EnumBase, Enum):    
    
    """The identifier which the risk model is uploaded by."""

    sedol = 'sedol'
    bcid = 'bcid'
    cusip = 'cusip'
    gsid = 'gsid'
    isin = 'isin'    


class RiskModelUniverseIdentifierRequest(EnumBase, Enum):    
    
    """The identifier which the risk model is queried by."""

    gsid = 'gsid'
    bbid = 'bbid'
    bcid = 'bcid'
    cusip = 'cusip'
    sedol = 'sedol'
    ric = 'ric'
    ticker = 'ticker'
    primeId = 'primeId'
    isin = 'isin'    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Factor(Base):
    identifier: str = field(default=None, metadata=field_metadata)
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    description: Optional[str] = field(default=None, metadata=field_metadata)
    glossary_description: Optional[str] = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelCalendar(Base):
    business_dates: Tuple[datetime.date, ...] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelFactorData(Base):
    factor_id: str = field(default=None, metadata=field_metadata)
    factor_name: str = field(default=None, metadata=field_metadata)
    factor_category_id: str = field(default=None, metadata=field_metadata)
    factor_category: str = field(default=None, metadata=field_metadata)
    factor_return: float = field(default=None, metadata=field_metadata)
    factor_standard_deviation: Optional[float] = field(default=None, metadata=field_metadata)
    factor_z_score: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


RiskModelFactorExposure = Dict[str, float]


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelFactorPortfolio(Base):
    factor_id: str = field(default=None, metadata=field_metadata)
    weights: Tuple[float, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelIssuerSpecificCovarianceData(Base):
    universe_id1: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    universe_id2: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    covariance: Tuple[float, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)

@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Entitlements(Base):
    view: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    edit: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    admin: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    rebalance: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    execute: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    trade: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    upload: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    query: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    performance_details: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    plot: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    delete: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    display: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelAssetData(Base):
    universe: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    specific_risk: Tuple[float, ...] = field(default=None, metadata=field_metadata)
    factor_exposure: Tuple[RiskModelFactorExposure, ...] = field(default=None, metadata=field_metadata)
    unadjusted_specific_risk: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    specific_return: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    daily_return: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    estimation_universe_weight: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    residual_variance: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    historical_beta: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    predicted_beta: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    global_predicted_beta: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    total_risk: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    bid_ask_spread: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    bid_ask_spread30d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    bid_ask_spread60d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    bid_ask_spread90d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    trading_volume: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    trading_volume30d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    trading_volume60d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    trading_volume90d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    traded_value30d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    composite_volume: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    composite_volume30d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    composite_volume60d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    composite_volume90d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    composite_value30d: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    issuer_market_cap: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    price: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    capitalization: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    currency: Optional[Tuple[Currency, ...]] = field(default=None, metadata=field_metadata)
    dividend_yield: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    r_squared: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    fair_value_gap_percent: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    fair_value_gap_standard_deviation: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    model_price: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelCoverageRequest(Base):
    asset_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    as_of_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    sort_by_term: Optional[RiskModelTerm] = field(default=None, metadata=field_metadata)
    vendor: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelDataAssetsRequest(Base):
    identifier: RiskModelUniverseIdentifierRequest = field(default=None, metadata=field_metadata)
    universe: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelFactorPortfoliosData(Base):
    universe: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    portfolio: Tuple[RiskModelFactorPortfolio, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModel(Base):
    coverage: RiskModelCoverage = field(default=None, metadata=field_metadata)
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    term: RiskModelTerm = field(default=None, metadata=field_metadata)
    universe_identifier: RiskModelUniverseIdentifier = field(default=None, metadata=field_metadata)
    vendor: str = field(default=None, metadata=field_metadata)
    version: float = field(default=None, metadata=field_metadata)
    type_: RiskModelType = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    expected_update_time: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    universe_size: Optional[float] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelData(Base):
    date: datetime.date = field(default=None, metadata=field_metadata)
    asset_data: Optional[RiskModelAssetData] = field(default=None, metadata=field_metadata)
    factor_data: Optional[Tuple[RiskModelFactorData, ...]] = field(default=None, metadata=field_metadata)
    covariance_matrix: Optional[Tuple[Tuple[float, ...], ...]] = field(default=None, metadata=field_metadata)
    pre_vra_covariance_matrix: Optional[Tuple[Tuple[float, ...], ...]] = field(default=None, metadata=config(field_name='preVRACovarianceMatrix', exclude=exclude_none))
    unadjusted_covariance_matrix: Optional[Tuple[Tuple[float, ...], ...]] = field(default=None, metadata=field_metadata)
    issuer_specific_covariance: Optional[RiskModelIssuerSpecificCovarianceData] = field(default=None, metadata=field_metadata)
    factor_portfolios: Optional[RiskModelFactorPortfoliosData] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelDataRequest(Base):
    start_date: datetime.date = field(default=None, metadata=field_metadata)
    end_date: datetime.date = field(default=None, metadata=field_metadata)
    measures: Tuple[RiskModelDataMeasure, ...] = field(default=None, metadata=field_metadata)
    assets: Optional[RiskModelDataAssetsRequest] = field(default=None, metadata=field_metadata)
    limit_factors: Optional[bool] = field(default=True, metadata=field_metadata)
    base_currency_factor: Optional[str] = field(default=None, metadata=field_metadata)
    format_: Optional[str] = field(default='Json', metadata=config(field_name='format', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskModelDataResponse(Base):
    results: Tuple[RiskModelData, ...] = field(default=None, metadata=field_metadata)
    total_results: int = field(default=None, metadata=field_metadata)
    missing_dates: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
