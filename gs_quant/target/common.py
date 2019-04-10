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

from enum import Enum
from gs_quant.base import Base, EnumBase, Priceable, get_enum_value
from typing import Tuple, Union
import datetime


class AssetClass(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""

    Cash = 'Cash'
    Commod = 'Commod'
    Credit = 'Credit'
    Cross_Asset = 'Cross Asset'
    Equity = 'Equity'
    Fund = 'Fund'
    FX = 'FX'
    Mortgage = 'Mortgage'
    Rates = 'Rates'
    Loan = 'Loan'
    
    def __repr__(self):
        return self.value


class AssetType(EnumBase, Enum):    
    
    """Asset type differentiates the product categorization or contract type"""

    Access = 'Access'
    Basis = 'Basis'
    BasisSwap = 'BasisSwap'
    Benchmark = 'Benchmark'
    Benchmark_Rate = 'Benchmark Rate'
    Bond = 'Bond'
    Calendar_Spread = 'Calendar Spread'
    Cap = 'Cap'
    Cash = 'Cash'
    Certificate = 'Certificate'
    CD = 'CD'
    Commodity = 'Commodity'
    Company = 'Company'
    Convertible = 'Convertible'
    Credit_Basket = 'Credit Basket'
    Cross = 'Cross'
    Crypto_Currency = 'Crypto Currency'
    Currency = 'Currency'
    Custom_Basket = 'Custom Basket'
    Default_Swap = 'Default Swap'
    Economic = 'Economic'
    Endowment = 'Endowment'
    Equity_Basket = 'Equity Basket'
    ETF = 'ETF'
    ETN = 'ETN'
    Event = 'Event'
    Fixing = 'Fixing'
    Floor = 'Floor'
    Forward = 'Forward'
    Future = 'Future'
    Hedge_Fund = 'Hedge Fund'
    Index = 'Index'
    Inter_Commodity_Spread = 'Inter-Commodity Spread'
    Market_Location = 'Market Location'
    Multi_Asset_Allocation = 'Multi-Asset Allocation'
    Mutual_Fund = 'Mutual Fund'
    Note = 'Note'
    Option = 'Option'
    Pension_Fund = 'Pension Fund'
    Preferred_Stock = 'Preferred Stock'
    Physical = 'Physical'
    Reference_Entity = 'Reference Entity'
    Research_Basket = 'Research Basket'
    Rate = 'Rate'
    Risk_Premia = 'Risk Premia'
    Securities_Lending_Loan = 'Securities Lending Loan'
    Share_Class = 'Share Class'
    Single_Stock = 'Single Stock'
    Swap = 'Swap'
    Swaption = 'Swaption'
    Systematic_Hedging = 'Systematic Hedging'
    
    def __repr__(self):
        return self.value


class BusinessDayConvention(EnumBase, Enum):    
    
    """Business Day Convention."""

    Following = 'Following'
    Modified_Following = 'Modified Following'
    Previous = 'Previous'
    Unadjusted = 'Unadjusted'
    
    def __repr__(self):
        return self.value


class Commodities(EnumBase, Enum):    
    
    """Commodity asset"""

    Aluminium = 'Aluminium'
    Aluminium_Alloy = 'Aluminium Alloy'
    Chicago_Ethanol = 'Chicago Ethanol'
    Coal = 'Coal'
    Coffee = 'Coffee'
    Copper = 'Copper'
    Corn = 'Corn'
    Cotton = 'Cotton'
    Crude_Palm_Oil = 'Crude Palm Oil'
    Diesel_Fuel = 'Diesel Fuel'
    Electricity = 'Electricity'
    Emissions = 'Emissions'
    Ethylene = 'Ethylene'
    Freight = 'Freight'
    Fuel_Oil = 'Fuel Oil'
    Gas_Oil = 'Gas Oil'
    Gasoline = 'Gasoline'
    Gold = 'Gold'
    Heating_Oil = 'Heating Oil'
    Iron_Ore = 'Iron Ore'
    Jet_Fuel = 'Jet Fuel'
    Lead = 'Lead'
    Lean_Hogs = 'Lean Hogs'
    NGL = 'NGL'
    Naphtha = 'Naphtha'
    Natural_Gas = 'Natural Gas'
    Nickel = 'Nickel'
    Oil = 'Oil'
    Palladium = 'Palladium'
    Platinum = 'Platinum'
    Polypropylene = 'Polypropylene'
    Primary_Aluminium = 'Primary Aluminium'
    Silver = 'Silver'
    Soybean_Meal = 'Soybean Meal'
    Soybean_Oil = 'Soybean Oil'
    Soybeans = 'Soybeans'
    Sugar = 'Sugar'
    Tin = 'Tin'
    Ultra_Low_Sulphur_Diesel = 'Ultra Low Sulphur Diesel'
    Wheat = 'Wheat'
    White_Sugar = 'White Sugar'
    Zinc = 'Zinc'
    
    def __repr__(self):
        return self.value


class CountryCode(EnumBase, Enum):    
    
    """ISO Country code"""

    AU = 'AU'
    CX = 'CX'
    CC = 'CC'
    HM = 'HM'
    NF = 'NF'
    NZ = 'NZ'
    CK = 'CK'
    NU = 'NU'
    TK = 'TK'
    JP = 'JP'
    JN = 'JN'
    EU = 'EU'
    ER = 'ER'
    EZ = 'EZ'
    AT = 'AT'
    BE = 'BE'
    FI = 'FI'
    FR = 'FR'
    GF = 'GF'
    PF = 'PF'
    TF = 'TF'
    GP = 'GP'
    MQ = 'MQ'
    YT = 'YT'
    NC = 'NC'
    RE = 'RE'
    SH = 'SH'
    PM = 'PM'
    WF = 'WF'
    DE = 'DE'
    GE = 'GE'
    GR = 'GR'
    IE = 'IE'
    IT = 'IT'
    LU = 'LU'
    NL = 'NL'
    AW = 'AW'
    AN = 'AN'
    PT = 'PT'
    ES = 'ES'
    BY = 'BY'
    CH = 'CH'
    SE = 'SE'
    SW = 'SW'
    DK = 'DK'
    FO = 'FO'
    NO = 'NO'
    BV = 'BV'
    SJ = 'SJ'
    LI = 'LI'
    GB = 'GB'
    UK = 'UK'
    AI = 'AI'
    IO = 'IO'
    KY = 'KY'
    FK = 'FK'
    GI = 'GI'
    MS = 'MS'
    PN = 'PN'
    GS = 'GS'
    TC = 'TC'
    VG = 'VG'
    JE = 'JE'
    _02 = '02'
    US = 'US'
    AS = 'AS'
    GU = 'GU'
    MP = 'MP'
    PR = 'PR'
    UM = 'UM'
    VI = 'VI'
    CA = 'CA'
    AR = 'AR'
    BA = 'BA'
    BD = 'BD'
    BG = 'BG'
    BS = 'BS'
    BM = 'BM'
    BO = 'BO'
    BR = 'BR'
    CL = 'CL'
    CN = 'CN'
    CO = 'CO'
    CR = 'CR'
    CZ = 'CZ'
    DO = 'DO'
    EC = 'EC'
    EG = 'EG'
    GA = 'GA'
    GT = 'GT'
    HK = 'HK'
    HR = 'HR'
    HU = 'HU'
    IL = 'IL'
    IM = 'IM'
    IR = 'IR'
    IS = 'IS'
    JO = 'JO'
    KE = 'KE'
    KR = 'KR'
    KZ = 'KZ'
    LB = 'LB'
    LK = 'LK'
    LT = 'LT'
    MA = 'MA'
    MH = 'MH'
    ML = 'ML'
    MO = 'MO'
    MT = 'MT'
    MX = 'MX'
    MY = 'MY'
    NI = 'NI'
    OM = 'OM'
    PA = 'PA'
    PD = 'PD'
    PE = 'PE'
    PH = 'PH'
    PK = 'PK'
    PL = 'PL'
    QA = 'QA'
    RO = 'RO'
    RU = 'RU'
    SA = 'SA'
    SG = 'SG'
    SI = 'SI'
    SK = 'SK'
    SV = 'SV'
    TH = 'TH'
    TN = 'TN'
    TP = 'TP'
    TR = 'TR'
    TW = 'TW'
    UA = 'UA'
    UY = 'UY'
    VE = 'VE'
    VN = 'VN'
    ZA = 'ZA'
    BH = 'BH'
    EE = 'EE'
    GH = 'GH'
    ME = 'ME'
    RS = 'RS'
    ZM = 'ZM'
    ZW = 'ZW'
    TT = 'TT'
    AE = 'AE'
    KW = 'KW'
    BB = 'BB'
    LV = 'LV'
    GG = 'GG'
    CY = 'CY'
    CI = 'CI'
    MU = 'MU'
    PY = 'PY'
    HN = 'HN'
    BZ = 'BZ'
    NA = 'NA'
    FJ = 'FJ'
    BW = 'BW'
    DZ = 'DZ'
    MN = 'MN'
    SN = 'SN'
    TZ = 'TZ'
    AD = 'AD'
    AG = 'AG'
    AL = 'AL'
    AM = 'AM'
    AO = 'AO'
    AZ = 'AZ'
    BF = 'BF'
    BI = 'BI'
    BJ = 'BJ'
    BN = 'BN'
    BT = 'BT'
    CD = 'CD'
    CF = 'CF'
    CG = 'CG'
    CM = 'CM'
    CU = 'CU'
    CV = 'CV'
    CS = 'CS'
    DJ = 'DJ'
    DM = 'DM'
    EH = 'EH'
    ET = 'ET'
    FM = 'FM'
    GD = 'GD'
    GL = 'GL'
    GM = 'GM'
    GN = 'GN'
    GQ = 'GQ'
    GW = 'GW'
    GY = 'GY'
    HT = 'HT'
    ID = 'ID'
    IN = 'IN'
    IQ = 'IQ'
    JM = 'JM'
    KG = 'KG'
    KH = 'KH'
    KI = 'KI'
    KM = 'KM'
    KN = 'KN'
    KP = 'KP'
    LA = 'LA'
    LC = 'LC'
    LR = 'LR'
    LS = 'LS'
    LY = 'LY'
    MC = 'MC'
    MD = 'MD'
    MG = 'MG'
    MK = 'MK'
    MM = 'MM'
    MR = 'MR'
    MV = 'MV'
    MW = 'MW'
    MZ = 'MZ'
    NE = 'NE'
    NG = 'NG'
    NP = 'NP'
    NR = 'NR'
    PG = 'PG'
    PW = 'PW'
    RW = 'RW'
    SB = 'SB'
    SC = 'SC'
    SD = 'SD'
    SL = 'SL'
    SM = 'SM'
    SO = 'SO'
    SR = 'SR'
    ST = 'ST'
    SY = 'SY'
    SZ = 'SZ'
    TD = 'TD'
    TG = 'TG'
    TJ = 'TJ'
    TL = 'TL'
    TM = 'TM'
    TO = 'TO'
    TV = 'TV'
    UG = 'UG'
    UZ = 'UZ'
    VA = 'VA'
    VC = 'VC'
    VU = 'VU'
    WS = 'WS'
    YE = 'YE'
    
    def __repr__(self):
        return self.value


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
    GHC = 'GHC'
    GHS = 'GHS'
    GHY = 'GHY'
    GIP = 'GIP'
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
    SHP = 'SHP'
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
    
    def __repr__(self):
        return self.value


class DayCountFraction(EnumBase, Enum):    
    
    """Day Count Fraction."""

    ACT_OVER_360 = 'ACT/360'
    ACT_OVER_365_Fixed = 'ACT/365 (Fixed)'
    ACT_OVER_365_ISDA = 'ACT/365 ISDA'
    ACT_OVER_ACT_ISDA = 'ACT/ACT ISDA'
    _30_OVER_360 = '30/360'
    _30E_OVER_360 = '30E/360'
    
    def __repr__(self):
        return self.value


class Field(EnumBase, Enum):    
    
    """Field to be returned"""

    queueClockTimeLabel = 'queueClockTimeLabel'
    marketPnl = 'marketPnl'
    year = 'year'
    sustainAsiaExJapan = 'sustainAsiaExJapan'
    investmentRate = 'investmentRate'
    assetClassificationsGicsSubIndustry = 'assetClassificationsGicsSubIndustry'
    bidUnadjusted = 'bidUnadjusted'
    economicTermsHash = 'economicTermsHash'
    neighbourAssetId = 'neighbourAssetId'
    simonIntlAssetTags = 'simonIntlAssetTags'
    path = 'path'
    availableInventory = 'availableInventory'
    clientContact = 'clientContact'
    est1DayCompletePct = 'est1DayCompletePct'
    rank = 'rank'
    dataSetCategory = 'dataSetCategory'
    createdById = 'createdById'
    vehicleType = 'vehicleType'
    dailyRisk = 'dailyRisk'
    bosInBpsLabel = 'bosInBpsLabel'
    marketDataType = 'marketDataType'
    sentimentScore = 'sentimentScore'
    bosInBps = 'bosInBps'
    pointClass = 'pointClass'
    fxSpot = 'fxSpot'
    bidLow = 'bidLow'
    valuePrevious = 'valuePrevious'
    fairVarianceVolatility = 'fairVarianceVolatility'
    avgTradeRate = 'avgTradeRate'
    shortLevel = 'shortLevel'
    hedgeVolatility = 'hedgeVolatility'
    version = 'version'
    tags = 'tags'
    underlyingAssetId = 'underlyingAssetId'
    clientExposure = 'clientExposure'
    correlation = 'correlation'
    exposure = 'exposure'
    gsSustainSubSector = 'gsSustainSubSector'
    domain = 'domain'
    marketDataAsset = 'marketDataAsset'
    forwardTenor = 'forwardTenor'
    unadjustedHigh = 'unadjustedHigh'
    sourceImportance = 'sourceImportance'
    eid = 'eid'
    jsn = 'jsn'
    relativeReturnQtd = 'relativeReturnQtd'
    displayName = 'displayName'
    minutesToTrade100Pct = 'minutesToTrade100Pct'
    marketModelId = 'marketModelId'
    quoteType = 'quoteType'
    tenor = 'tenor'
    esPolicyPercentile = 'esPolicyPercentile'
    tcmCostParticipationRate75Pct = 'tcmCostParticipationRate75Pct'
    close = 'close'
    tcmCostParticipationRate100Pct = 'tcmCostParticipationRate100Pct'
    disclaimer = 'disclaimer'
    measureIdx = 'measureIdx'
    a = 'a'
    b = 'b'
    loanFee = 'loanFee'
    c = 'c'
    equityVega = 'equityVega'
    deploymentVersion = 'deploymentVersion'
    fiveDayMove = 'fiveDayMove'
    borrower = 'borrower'
    performanceContribution = 'performanceContribution'
    targetNotional = 'targetNotional'
    fillLegId = 'fillLegId'
    delisted = 'delisted'
    rationale = 'rationale'
    regionalFocus = 'regionalFocus'
    volumePrimary = 'volumePrimary'
    series = 'series'
    simonId = 'simonId'
    newIdeasQtd = 'newIdeasQtd'
    adjustedAskPrice = 'adjustedAskPrice'
    quarter = 'quarter'
    factorUniverse = 'factorUniverse'
    eventCategory = 'eventCategory'
    impliedNormalVolatility = 'impliedNormalVolatility'
    unadjustedOpen = 'unadjustedOpen'
    arrivalRt = 'arrivalRt'
    transactionCost = 'transactionCost'
    servicingCostShortPnl = 'servicingCostShortPnl'
    bidAskSpread = 'bidAskSpread'
    optionType = 'optionType'
    tcmCostHorizon3Hour = 'tcmCostHorizon3Hour'
    clusterDescription = 'clusterDescription'
    positionAmount = 'positionAmount'
    numberOfPositions = 'numberOfPositions'
    windSpeed = 'windSpeed'
    openUnadjusted = 'openUnadjusted'
    maRank = 'maRank'
    eventStartDateTime = 'eventStartDateTime'
    askPrice = 'askPrice'
    eventId = 'eventId'
    dataProduct = 'dataProduct'
    sectors = 'sectors'
    annualizedTrackingError = 'annualizedTrackingError'
    volSwap = 'volSwap'
    annualizedRisk = 'annualizedRisk'
    corporateAction = 'corporateAction'
    conviction = 'conviction'
    grossExposure = 'grossExposure'
    benchmarkMaturity = 'benchmarkMaturity'
    volumeComposite = 'volumeComposite'
    volume = 'volume'
    adv = 'adv'
    stsFxCurrency = 'stsFxCurrency'
    wpk = 'wpk'
    shortConvictionMedium = 'shortConvictionMedium'
    bidChange = 'bidChange'
    exchange = 'exchange'
    expiration = 'expiration'
    tradePrice = 'tradePrice'
    esPolicyScore = 'esPolicyScore'
    loanId = 'loanId'
    cid = 'cid'
    liquidityScore = 'liquidityScore'
    importance = 'importance'
    sourceDateSpan = 'sourceDateSpan'
    assetClassificationsGicsSector = 'assetClassificationsGicsSector'
    underlyingDataSetId = 'underlyingDataSetId'
    stsAssetName = 'stsAssetName'
    closeUnadjusted = 'closeUnadjusted'
    valueUnit = 'valueUnit'
    bidHigh = 'bidHigh'
    adjustedLowPrice = 'adjustedLowPrice'
    netExposureClassification = 'netExposureClassification'
    longConvictionLarge = 'longConvictionLarge'
    fairVariance = 'fairVariance'
    hitRateWtd = 'hitRateWtd'
    oad = 'oad'
    bosInBpsDescription = 'bosInBpsDescription'
    lowPrice = 'lowPrice'
    realizedVolatility = 'realizedVolatility'
    rate = 'rate'
    adv22DayPct = 'adv22DayPct'
    alpha = 'alpha'
    client = 'client'
    company = 'company'
    convictionList = 'convictionList'
    priceRangeInTicksLabel = 'priceRangeInTicksLabel'
    ticker = 'ticker'
    inRiskModel = 'inRiskModel'
    tcmCostHorizon1Day = 'tcmCostHorizon1Day'
    servicingCostLongPnl = 'servicingCostLongPnl'
    stsRatesCountry = 'stsRatesCountry'
    meetingNumber = 'meetingNumber'
    exchangeId = 'exchangeId'
    horizon = 'horizon'
    tcmCostHorizon20Day = 'tcmCostHorizon20Day'
    longLevel = 'longLevel'
    sourceValueForecast = 'sourceValueForecast'
    shortConvictionLarge = 'shortConvictionLarge'
    realm = 'realm'
    bid = 'bid'
    dataDescription = 'dataDescription'
    composite22DayAdv = 'composite22DayAdv'
    gsn = 'gsn'
    isAggressive = 'isAggressive'
    orderId = 'orderId'
    gss = 'gss'
    percentOfMediandv1m = 'percentOfMediandv1m'
    lendables = 'lendables'
    assetClass = 'assetClass'
    gsideid = 'gsideid'
    bosInTicksLabel = 'bosInTicksLabel'
    ric = 'ric'
    positionSourceId = 'positionSourceId'
    division = 'division'
    marketCapUSD = 'marketCapUSD'
    deploymentId = 'deploymentId'
    highPrice = 'highPrice'
    shortWeight = 'shortWeight'
    absoluteShares = 'absoluteShares'
    action = 'action'
    model = 'model'
    id = 'id'
    arrivalHaircutVwapNormalized = 'arrivalHaircutVwapNormalized'
    queueClockTimeDescription = 'queueClockTimeDescription'
    period = 'period'
    indexCreateSource = 'indexCreateSource'
    fiscalQuarter = 'fiscalQuarter'
    deltaStrike = 'deltaStrike'
    marketImpact = 'marketImpact'
    eventType = 'eventType'
    assetCountLong = 'assetCountLong'
    valueActual = 'valueActual'
    bcid = 'bcid'
    originalCountry = 'originalCountry'
    touchLiquidityScore = 'touchLiquidityScore'
    field = 'field'
    spot = 'spot'
    expectedCompletionDate = 'expectedCompletionDate'
    loanValue = 'loanValue'
    skew = 'skew'
    status = 'status'
    sustainEmergingMarkets = 'sustainEmergingMarkets'
    eventDateTime = 'eventDateTime'
    totalReturnPrice = 'totalReturnPrice'
    city = 'city'
    eventSource = 'eventSource'
    qisPermNo = 'qisPermNo'
    hitRateYtd = 'hitRateYtd'
    stsCommodity = 'stsCommodity'
    stsCommoditySector = 'stsCommoditySector'
    salesCoverage = 'salesCoverage'
    shortExposure = 'shortExposure'
    esScore = 'esScore'
    tcmCostParticipationRate10Pct = 'tcmCostParticipationRate10Pct'
    eventTime = 'eventTime'
    positionSourceName = 'positionSourceName'
    priceRangeInTicks = 'priceRangeInTicks'
    deliveryDate = 'deliveryDate'
    arrivalHaircutVwap = 'arrivalHaircutVwap'
    interestRate = 'interestRate'
    executionDays = 'executionDays'
    pctChange = 'pctChange'
    side = 'side'
    numberOfRolls = 'numberOfRolls'
    agentLenderFee = 'agentLenderFee'
    complianceRestrictedStatus = 'complianceRestrictedStatus'
    forward = 'forward'
    borrowFee = 'borrowFee'
    strike = 'strike'
    updateTime = 'updateTime'
    loanSpread = 'loanSpread'
    tcmCostHorizon12Hour = 'tcmCostHorizon12Hour'
    dewPoint = 'dewPoint'
    researchCommission = 'researchCommission'
    bbid = 'bbid'
    assetClassificationsRiskCountryCode = 'assetClassificationsRiskCountryCode'
    eventStatus = 'eventStatus'
    effectiveDate = 'effectiveDate'
    _return = 'return'
    maxTemperature = 'maxTemperature'
    acquirerShareholderMeetingDate = 'acquirerShareholderMeetingDate'
    arrivalMidNormalized = 'arrivalMidNormalized'
    rating = 'rating'
    arrivalRtNormalized = 'arrivalRtNormalized'
    performanceFee = 'performanceFee'
    reportType = 'reportType'
    sourceURL = 'sourceURL'
    estimatedReturn = 'estimatedReturn'
    underlyingAssetIds = 'underlyingAssetIds'
    high = 'high'
    sourceLastUpdate = 'sourceLastUpdate'
    queueInLotsLabel = 'queueInLotsLabel'
    adv10DayPct = 'adv10DayPct'
    longConvictionMedium = 'longConvictionMedium'
    eventName = 'eventName'
    annualRisk = 'annualRisk'
    dailyTrackingError = 'dailyTrackingError'
    unadjustedBid = 'unadjustedBid'
    gsdeer = 'gsdeer'
    marketCap = 'marketCap'
    clusterRegion = 'clusterRegion'
    bbidEquivalent = 'bbidEquivalent'
    prevCloseAsk = 'prevCloseAsk'
    level = 'level'
    valoren = 'valoren'
    pressure = 'pressure'
    shortDescription = 'shortDescription'
    basis = 'basis'
    netWeight = 'netWeight'
    hedgeId = 'hedgeId'
    portfolioManagers = 'portfolioManagers'
    assetParametersCommoditySector = 'assetParametersCommoditySector'
    bosInTicks = 'bosInTicks'
    tcmCostHorizon8Day = 'tcmCostHorizon8Day'
    supraStrategy = 'supraStrategy'
    adv5DayPct = 'adv5DayPct'
    factorSource = 'factorSource'
    leverage = 'leverage'
    submitter = 'submitter'
    notional = 'notional'
    esDisclosurePercentage = 'esDisclosurePercentage'
    clientShortName = 'clientShortName'
    fwdPoints = 'fwdPoints'
    groupCategory = 'groupCategory'
    kpiId = 'kpiId'
    relativeReturnWtd = 'relativeReturnWtd'
    bidPlusAsk = 'bidPlusAsk'
    assetClassificationsRiskCountryName = 'assetClassificationsRiskCountryName'
    total = 'total'
    riskModel = 'riskModel'
    assetId = 'assetId'
    lastUpdatedTime = 'lastUpdatedTime'
    fairValue = 'fairValue'
    adjustedHighPrice = 'adjustedHighPrice'
    openTime = 'openTime'
    beta = 'beta'
    direction = 'direction'
    valueForecast = 'valueForecast'
    longExposure = 'longExposure'
    positionSourceType = 'positionSourceType'
    tcmCostParticipationRate20Pct = 'tcmCostParticipationRate20Pct'
    adjustedClosePrice = 'adjustedClosePrice'
    cross = 'cross'
    lmsId = 'lmsId'
    rebateRate = 'rebateRate'
    ideaStatus = 'ideaStatus'
    participationRate = 'participationRate'
    obfr = 'obfr'
    fxForecast = 'fxForecast'
    fixingTimeLabel = 'fixingTimeLabel'
    fillId = 'fillId'
    esNumericScore = 'esNumericScore'
    inBenchmark = 'inBenchmark'
    strategy = 'strategy'
    shortInterest = 'shortInterest'
    referencePeriod = 'referencePeriod'
    adjustedVolume = 'adjustedVolume'
    queueInLotsDescription = 'queueInLotsDescription'
    pbClientId = 'pbClientId'
    ownerId = 'ownerId'
    secDB = 'secDB'
    composite10DayAdv = 'composite10DayAdv'
    objective = 'objective'
    navPrice = 'navPrice'
    ideaActivityType = 'ideaActivityType'
    precipitation = 'precipitation'
    ideaSource = 'ideaSource'
    hedgeNotional = 'hedgeNotional'
    askLow = 'askLow'
    unadjustedAsk = 'unadjustedAsk'
    betaAdjustedNetExposure = 'betaAdjustedNetExposure'
    expiry = 'expiry'
    tradingPnl = 'tradingPnl'
    strikePercentage = 'strikePercentage'
    excessReturnPrice = 'excessReturnPrice'
    givenPlusPaid = 'givenPlusPaid'
    shortConvictionSmall = 'shortConvictionSmall'
    prevCloseBid = 'prevCloseBid'
    fxPnl = 'fxPnl'
    forecast = 'forecast'
    tcmCostHorizon16Day = 'tcmCostHorizon16Day'
    pnl = 'pnl'
    assetClassificationsGicsIndustryGroup = 'assetClassificationsGicsIndustryGroup'
    unadjustedClose = 'unadjustedClose'
    tcmCostHorizon4Day = 'tcmCostHorizon4Day'
    assetClassificationsIsPrimary = 'assetClassificationsIsPrimary'
    styles = 'styles'
    lendingSecId = 'lendingSecId'
    shortName = 'shortName'
    equityTheta = 'equityTheta'
    averageFillPrice = 'averageFillPrice'
    snowfall = 'snowfall'
    mic = 'mic'
    openPrice = 'openPrice'
    autoExecState = 'autoExecState'
    depthSpreadScore = 'depthSpreadScore'
    relativeReturnYtd = 'relativeReturnYtd'
    long = 'long'
    fairVolatility = 'fairVolatility'
    dollarCross = 'dollarCross'
    longWeight = 'longWeight'
    vendor = 'vendor'
    currency = 'currency'
    clusterClass = 'clusterClass'
    financialReturnsScore = 'financialReturnsScore'
    netChange = 'netChange'
    nonSymbolDimensions = 'nonSymbolDimensions'
    bidSize = 'bidSize'
    arrivalMid = 'arrivalMid'
    assetParametersExchangeCurrency = 'assetParametersExchangeCurrency'
    unexplained = 'unexplained'
    assetClassificationsCountryName = 'assetClassificationsCountryName'
    metric = 'metric'
    newIdeasYtd = 'newIdeasYtd'
    managementFee = 'managementFee'
    ask = 'ask'
    impliedLognormalVolatility = 'impliedLognormalVolatility'
    closePrice = 'closePrice'
    endTime = 'endTime'
    open = 'open'
    sourceId = 'sourceId'
    country = 'country'
    cusip = 'cusip'
    ideaActivityTime = 'ideaActivityTime'
    touchSpreadScore = 'touchSpreadScore'
    absoluteStrike = 'absoluteStrike'
    netExposure = 'netExposure'
    source = 'source'
    assetClassificationsCountryCode = 'assetClassificationsCountryCode'
    frequency = 'frequency'
    activityId = 'activityId'
    estimatedImpact = 'estimatedImpact'
    dataSetSubCategory = 'dataSetSubCategory'
    assetParametersPricingLocation = 'assetParametersPricingLocation'
    eventDescription = 'eventDescription'
    strikeReference = 'strikeReference'
    details = 'details'
    assetCount = 'assetCount'
    given = 'given'
    absoluteValue = 'absoluteValue'
    delistingDate = 'delistingDate'
    longTenor = 'longTenor'
    mctr = 'mctr'
    weight = 'weight'
    historicalClose = 'historicalClose'
    assetCountPriced = 'assetCountPriced'
    marketDataPoint = 'marketDataPoint'
    ideaId = 'ideaId'
    commentStatus = 'commentStatus'
    marginalCost = 'marginalCost'
    absoluteWeight = 'absoluteWeight'
    tradeTime = 'tradeTime'
    measure = 'measure'
    clientWeight = 'clientWeight'
    hedgeAnnualizedVolatility = 'hedgeAnnualizedVolatility'
    benchmarkCurrency = 'benchmarkCurrency'
    name = 'name'
    aum = 'aum'
    folderName = 'folderName'
    lendingPartnerFee = 'lendingPartnerFee'
    region = 'region'
    liveDate = 'liveDate'
    askHigh = 'askHigh'
    corporateActionType = 'corporateActionType'
    primeId = 'primeId'
    tenor2 = 'tenor2'
    description = 'description'
    valueRevised = 'valueRevised'
    ownerName = 'ownerName'
    adjustedTradePrice = 'adjustedTradePrice'
    lastUpdatedById = 'lastUpdatedById'
    zScore = 'zScore'
    targetShareholderMeetingDate = 'targetShareholderMeetingDate'
    isADR = 'isADR'
    eventStartTime = 'eventStartTime'
    factor = 'factor'
    longConvictionSmall = 'longConvictionSmall'
    serviceId = 'serviceId'
    turnover = 'turnover'
    complianceEffectiveTime = 'complianceEffectiveTime'
    expirationDate = 'expirationDate'
    gsfeer = 'gsfeer'
    coverage = 'coverage'
    backtestId = 'backtestId'
    gPercentile = 'gPercentile'
    gScore = 'gScore'
    marketValue = 'marketValue'
    multipleScore = 'multipleScore'
    lendingFundNav = 'lendingFundNav'
    sourceOriginalCategory = 'sourceOriginalCategory'
    betaAdjustedExposure = 'betaAdjustedExposure'
    composite5DayAdv = 'composite5DayAdv'
    latestExecutionTime = 'latestExecutionTime'
    dividendPoints = 'dividendPoints'
    newIdeasWtd = 'newIdeasWtd'
    paid = 'paid'
    short = 'short'
    location = 'location'
    comment = 'comment'
    bosInTicksDescription = 'bosInTicksDescription'
    sourceSymbol = 'sourceSymbol'
    time = 'time'
    scenarioId = 'scenarioId'
    askUnadjusted = 'askUnadjusted'
    queueClockTime = 'queueClockTime'
    askChange = 'askChange'
    tcmCostParticipationRate50Pct = 'tcmCostParticipationRate50Pct'
    normalizedPerformance = 'normalizedPerformance'
    cmId = 'cmId'
    type = 'type'
    mdapi = 'mdapi'
    dividendYield = 'dividendYield'
    cumulativePnl = 'cumulativePnl'
    sourceOrigin = 'sourceOrigin'
    shortTenor = 'shortTenor'
    unadjustedVolume = 'unadjustedVolume'
    measures = 'measures'
    tradingCostPnl = 'tradingCostPnl'
    internalUser = 'internalUser'
    price = 'price'
    paymentQuantity = 'paymentQuantity'
    underlyer = 'underlyer'
    createdTime = 'createdTime'
    positionIdx = 'positionIdx'
    secName = 'secName'
    percentADV = 'percentADV'
    unadjustedLow = 'unadjustedLow'
    contract = 'contract'
    sedol = 'sedol'
    roundingCostPnl = 'roundingCostPnl'
    sustainGlobal = 'sustainGlobal'
    sourceTicker = 'sourceTicker'
    portfolioId = 'portfolioId'
    gsid = 'gsid'
    esPercentile = 'esPercentile'
    lendingFund = 'lendingFund'
    tcmCostParticipationRate15Pct = 'tcmCostParticipationRate15Pct'
    sensitivity = 'sensitivity'
    fiscalYear = 'fiscalYear'
    rcic = 'rcic'
    simonAssetTags = 'simonAssetTags'
    internal = 'internal'
    forwardPoint = 'forwardPoint'
    assetClassificationsGicsIndustry = 'assetClassificationsGicsIndustry'
    adjustedBidPrice = 'adjustedBidPrice'
    hitRateQtd = 'hitRateQtd'
    varSwap = 'varSwap'
    lowUnadjusted = 'lowUnadjusted'
    sectorsRaw = 'sectorsRaw'
    low = 'low'
    crossGroup = 'crossGroup'
    integratedScore = 'integratedScore'
    reportRunTime = 'reportRunTime'
    fiveDayPriceChangeBps = 'fiveDayPriceChangeBps'
    tradeSize = 'tradeSize'
    symbolDimensions = 'symbolDimensions'
    quotingStyle = 'quotingStyle'
    scenarioGroupId = 'scenarioGroupId'
    errorMessage = 'errorMessage'
    avgTradeRateDescription = 'avgTradeRateDescription'
    midPrice = 'midPrice'
    fraction = 'fraction'
    stsCreditMarket = 'stsCreditMarket'
    assetCountShort = 'assetCountShort'
    stsEmDm = 'stsEmDm'
    tcmCostHorizon2Day = 'tcmCostHorizon2Day'
    queueInLots = 'queueInLots'
    priceRangeInTicksDescription = 'priceRangeInTicksDescription'
    date = 'date'
    tenderOfferExpirationDate = 'tenderOfferExpirationDate'
    highUnadjusted = 'highUnadjusted'
    sourceCategory = 'sourceCategory'
    volumeUnadjusted = 'volumeUnadjusted'
    avgTradeRateLabel = 'avgTradeRateLabel'
    tcmCostParticipationRate5Pct = 'tcmCostParticipationRate5Pct'
    isActive = 'isActive'
    growthScore = 'growthScore'
    encodedStats = 'encodedStats'
    adjustedShortInterest = 'adjustedShortInterest'
    askSize = 'askSize'
    mdapiType = 'mdapiType'
    group = 'group'
    estimatedSpread = 'estimatedSpread'
    resource = 'resource'
    created = 'created'
    tcmCost = 'tcmCost'
    sustainJapan = 'sustainJapan'
    navSpread = 'navSpread'
    bidPrice = 'bidPrice'
    hedgeTrackingError = 'hedgeTrackingError'
    marketCapCategory = 'marketCapCategory'
    historicalVolume = 'historicalVolume'
    esNumericPercentile = 'esNumericPercentile'
    strikePrice = 'strikePrice'
    eventStartDate = 'eventStartDate'
    calSpreadMisPricing = 'calSpreadMisPricing'
    equityGamma = 'equityGamma'
    grossIncome = 'grossIncome'
    emId = 'emId'
    adjustedOpenPrice = 'adjustedOpenPrice'
    assetCountInModel = 'assetCountInModel'
    stsCreditRegion = 'stsCreditRegion'
    point = 'point'
    lender = 'lender'
    minTemperature = 'minTemperature'
    closeTime = 'closeTime'
    value = 'value'
    relativeStrike = 'relativeStrike'
    amount = 'amount'
    quantity = 'quantity'
    lendingFundAcct = 'lendingFundAcct'
    reportId = 'reportId'
    indexWeight = 'indexWeight'
    rebate = 'rebate'
    trader = 'trader'
    factorCategory = 'factorCategory'
    impliedVolatility = 'impliedVolatility'
    spread = 'spread'
    stsRatesMaturity = 'stsRatesMaturity'
    equityDelta = 'equityDelta'
    grossWeight = 'grossWeight'
    listed = 'listed'
    tcmCostHorizon6Hour = 'tcmCostHorizon6Hour'
    g10Currency = 'g10Currency'
    shockStyle = 'shockStyle'
    relativePeriod = 'relativePeriod'
    isin = 'isin'
    methodology = 'methodology'
    adjustedClose = 'adjustedClose'
    averageValue = 'averageValue'
    avgInterestRate = 'avgInterestRate'
    basisDuration = 'basisDuration'
    bestMonthDate = 'bestMonthDate'
    bloombergTicker = 'bloombergTicker'
    capexDepreciation = 'capexDepreciation'
    capexSales = 'capexSales'
    carry = 'carry'
    cashConversion = 'cashConversion'
    category = 'category'
    convexity = 'convexity'
    countryCode = 'countryCode'
    croci = 'croci'
    currentValue = 'currentValue'
    dacf = 'dacf'
    dailyVolatility = 'dailyVolatility'
    divYield = 'divYield'
    dollarDuration = 'dollarDuration'
    dpsGrowth = 'dpsGrowth'
    drawdownOverReturn = 'drawdownOverReturn'
    ebitdaGrowth = 'ebitdaGrowth'
    ebitdaMargin = 'ebitdaMargin'
    ebitGrowth = 'ebitGrowth'
    ebitMargin = 'ebitMargin'
    evGci = 'evGci'
    fcfConversion = 'fcfConversion'
    fcfYield = 'fcfYield'
    gci = 'gci'
    grossProfTotAssets = 'grossProfTotAssets'
    historicCPR = 'historicCPR'
    incrementalMargin = 'incrementalMargin'
    industry = 'industry'
    informationRatio = 'informationRatio'
    interestCover = 'interestCover'
    lastChange = 'lastChange'
    lastChangePct = 'lastChangePct'
    lastDate = 'lastDate'
    lastValue = 'lastValue'
    liborMatchedMaturitySwap = 'liborMatchedMaturitySwap'
    liborOAS = 'liborOAS'
    liborProceedsASW = 'liborProceedsASW'
    liborzSpread = 'liborzSpread'
    manEarningGrowthMeas = 'manEarningGrowthMeas'
    marginalRiskContribution = 'marginalRiskContribution'
    maxDrawdown = 'maxDrawdown'
    modifiedDuration = 'modifiedDuration'
    netDebtEbitda = 'netDebtEbitda'
    netDebtEquity = 'netDebtEquity'
    niGrowth = 'niGrowth'
    niMargin = 'niMargin'
    oisMatchedMaturitySwap = 'oisMatchedMaturitySwap'
    oisProceedsASW = 'oisProceedsASW'
    oiszSpread = 'oiszSpread'
    optionStyle = 'optionStyle'
    payup = 'payup'
    positionDate = 'positionDate'
    preTaxProfitGrowth = 'preTaxProfitGrowth'
    riskPremiaStyles = 'riskPremiaStyles'
    roce = 'roce'
    rolldown = 'rolldown'
    salesGrowth = 'salesGrowth'
    sector = 'sector'
    sharpeRatio = 'sharpeRatio'
    totalDebtCapital = 'totalDebtCapital'
    totalDebtTotalAsset = 'totalDebtTotalAsset'
    totalReturn = 'totalReturn'
    unleveredFcfYield = 'unleveredFcfYield'
    worstMonthDate = 'worstMonthDate'
    _yield = 'yield'
    
    def __repr__(self):
        return self.value


class Format(EnumBase, Enum):    
    
    """Alternative format for data to be returned in"""

    Json = 'Json'
    Excel = 'Excel'
    MessagePack = 'MessagePack'
    Pdf = 'Pdf'
    
    def __repr__(self):
        return self.value


class Frequency(EnumBase, Enum):    
    
    """Payment frequency"""

    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthly = 'Monthly'
    Quarterly = 'Quarterly'
    Annually = 'Annually'
    
    def __repr__(self):
        return self.value


class MarketDataVendor(EnumBase, Enum):    
    
    Goldman_Sachs = 'Goldman Sachs'
    Thomson_Reuters = 'Thomson Reuters'
    Solactive = 'Solactive'
    WM = 'WM'
    
    def __repr__(self):
        return self.value


class OptionStyle(EnumBase, Enum):    
    
    """Option Style"""

    European = 'European'
    American = 'American'
    Bermudan = 'Bermudan'
    
    def __repr__(self):
        return self.value


class OptionType(EnumBase, Enum):    
    
    Call = 'Call'
    Put = 'Put'
    
    def __repr__(self):
        return self.value


class PayReceive(EnumBase, Enum):    
    
    """Pay or receive fixed"""

    Pay = 'Pay'
    Receive = 'Receive'
    
    def __repr__(self):
        return self.value


class PricingLocation(EnumBase, Enum):    
    
    """Based on the location of the exchange. Called 'Native Region' in SecDB"""

    NYC = 'NYC'
    LDN = 'LDN'
    TKO = 'TKO'
    HKG = 'HKG'
    
    def __repr__(self):
        return self.value


class Region(EnumBase, Enum):    
    
    """Regional classification for the asset"""

    _ = ''
    Americas = 'Americas'
    Asia = 'Asia'
    EM = 'EM'
    Europe = 'Europe'
    Global = 'Global'
    
    def __repr__(self):
        return self.value


class SwapClearingHouse(EnumBase, Enum):    
    
    """Swap Clearing House"""

    LCH = 'LCH'
    EUREX = 'EUREX'
    JSCC = 'JSCC'
    CME = 'CME'
    
    def __repr__(self):
        return self.value


class SwapSettlement(EnumBase, Enum):    
    
    """Swap Settlement Type"""

    Phys_CLEARED = 'Phys.CLEARED'
    Physical = 'Physical'
    Cash_CollatCash = 'Cash.CollatCash'
    Cash_PYU = 'Cash.PYU'
    
    def __repr__(self):
        return self.value


class Entitlements(Base):
        
    """Defines the entitlements of a given resource"""
       
    def __init__(self, view: Tuple[str, ...] = None, edit: Tuple[str, ...] = None, admin: Tuple[str, ...] = None, rebalance: Tuple[str, ...] = None, trade: Tuple[str, ...] = None, upload: Tuple[str, ...] = None, query: Tuple[str, ...] = None, performanceDetails: Tuple[str, ...] = None, plot: Tuple[str, ...] = None):
        super().__init__()
        self.__view = view
        self.__edit = edit
        self.__admin = admin
        self.__rebalance = rebalance
        self.__trade = trade
        self.__upload = upload
        self.__query = query
        self.__performanceDetails = performanceDetails
        self.__plot = plot

    @property
    def view(self) -> Tuple[str, ...]:
        """Permission to view the resource and its contents"""
        return self.__view

    @view.setter
    def view(self, value: Tuple[str, ...]):
        self.__view = value
        self._property_changed('view')        

    @property
    def edit(self) -> Tuple[str, ...]:
        """Permission to edit details about the resource content, excluding entitlements. Can also delete the resource"""
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[str, ...]):
        self.__edit = value
        self._property_changed('edit')        

    @property
    def admin(self) -> Tuple[str, ...]:
        """Permission to edit all details of the resource, including entitlements. Can also delete the resource"""
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[str, ...]):
        self.__admin = value
        self._property_changed('admin')        

    @property
    def rebalance(self) -> Tuple[str, ...]:
        """Permission to rebalance the constituent weights of the resource"""
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value: Tuple[str, ...]):
        self.__rebalance = value
        self._property_changed('rebalance')        

    @property
    def trade(self) -> Tuple[str, ...]:
        """Permission to trade the resource"""
        return self.__trade

    @trade.setter
    def trade(self, value: Tuple[str, ...]):
        self.__trade = value
        self._property_changed('trade')        

    @property
    def upload(self) -> Tuple[str, ...]:
        """Permission to upload data to the given resource"""
        return self.__upload

    @upload.setter
    def upload(self, value: Tuple[str, ...]):
        self.__upload = value
        self._property_changed('upload')        

    @property
    def query(self) -> Tuple[str, ...]:
        """Permission to query data from the given resource"""
        return self.__query

    @query.setter
    def query(self, value: Tuple[str, ...]):
        self.__query = value
        self._property_changed('query')        

    @property
    def performanceDetails(self) -> Tuple[str, ...]:
        """Permission to view the resource, it's entire contents, and related data"""
        return self.__performanceDetails

    @performanceDetails.setter
    def performanceDetails(self, value: Tuple[str, ...]):
        self.__performanceDetails = value
        self._property_changed('performanceDetails')        

    @property
    def plot(self) -> Tuple[str, ...]:
        """Permission to plot data from the given resource"""
        return self.__plot

    @plot.setter
    def plot(self, value: Tuple[str, ...]):
        self.__plot = value
        self._property_changed('plot')        


class Link(Base):
        
    """Hyperlink"""
       
    def __init__(self, title: str = None, source: str = None):
        super().__init__()
        self.__title = title
        self.__source = source

    @property
    def title(self) -> str:
        """display text"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value
        self._property_changed('title')        

    @property
    def source(self) -> str:
        """link"""
        return self.__source

    @source.setter
    def source(self, value: str):
        self.__source = value
        self._property_changed('source')        


class MarketDataCoordinate(Base):
        
    """Object representation of a market data coordinate"""
       
    def __init__(self, marketDataType: str, assetId: str = None, marketDataAsset: str = None, pointClass: str = None, marketDataPoint: Tuple[str, ...] = None, field: str = None, quotingStyle: str = None):
        super().__init__()
        self.__marketDataType = marketDataType
        self.__assetId = assetId
        self.__marketDataAsset = marketDataAsset
        self.__pointClass = pointClass
        self.__marketDataPoint = marketDataPoint
        self.__field = field
        self.__quotingStyle = quotingStyle

    @property
    def marketDataType(self) -> str:
        """The Market Data Type, e.g. IR, IR_BASIS, FX, FX_Vol"""
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value: str):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def marketDataAsset(self) -> str:
        """The specific aaset, e.g. USD, EUR-EURIBOR-Telerate, WTI"""
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value: str):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def pointClass(self) -> str:
        """The market data pointClass, e.g. Swap, Cash."""
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value: str):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def marketDataPoint(self) -> Tuple[str, ...]:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value: Tuple[str, ...]):
        self.__marketDataPoint = value
        self._property_changed('marketDataPoint')        

    @property
    def field(self) -> str:
        """The specific field: bid, mid, rate etc"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        

    @property
    def quotingStyle(self) -> str:
        return self.__quotingStyle

    @quotingStyle.setter
    def quotingStyle(self, value: str):
        self.__quotingStyle = value
        self._property_changed('quotingStyle')        


class Op(Base):
        
    """Operations for searches."""
       
    def __init__(self, gte: Union[datetime.date, float] = None, lte: Union[datetime.date, float] = None, lt: Union[datetime.date, float] = None, gt: Union[datetime.date, float] = None):
        super().__init__()
        self.__gte = gte
        self.__lte = lte
        self.__lt = lt
        self.__gt = gt

    @property
    def gte(self) -> Union[datetime.date, float]:
        """search for values greater than or equal."""
        return self.__gte

    @gte.setter
    def gte(self, value: Union[datetime.date, float]):
        self.__gte = value
        self._property_changed('gte')        

    @property
    def lte(self) -> Union[datetime.date, float]:
        """search for values less than or equal to."""
        return self.__lte

    @lte.setter
    def lte(self, value: Union[datetime.date, float]):
        self.__lte = value
        self._property_changed('lte')        

    @property
    def lt(self) -> Union[datetime.date, float]:
        """search for values less than."""
        return self.__lt

    @lt.setter
    def lt(self, value: Union[datetime.date, float]):
        self.__lt = value
        self._property_changed('lt')        

    @property
    def gt(self) -> Union[datetime.date, float]:
        """search for values greater than."""
        return self.__gt

    @gt.setter
    def gt(self, value: Union[datetime.date, float]):
        self.__gt = value
        self._property_changed('gt')        


class Position(Base):
               
    def __init__(self, assetId: str = None, quantity: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__quantity = quantity

    @property
    def assetId(self) -> str:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def quantity(self) -> float:
        """Quantity of position"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        


class XRef(Priceable):
               
    def __init__(self, ric: str = None, rcic: str = None, eid: str = None, gsideid: str = None, gsid: str = None, cid: str = None, bbid: str = None, bcid: str = None, delisted: str = None, bbidEquivalent: str = None, cusip: str = None, gss: str = None, isin: str = None, jsn: str = None, primeId: str = None, sedol: str = None, ticker: str = None, valoren: str = None, wpk: str = None, gsn: str = None, secName: str = None, cross: str = None, simonId: str = None, emId: str = None, cmId: str = None, lmsId: str = None, mdapi: str = None, mic: str = None, sfId: str = None, dollarCross: str = None):
        super().__init__()
        self.__ric = ric
        self.__rcic = rcic
        self.__eid = eid
        self.__gsideid = gsideid
        self.__gsid = gsid
        self.__cid = cid
        self.__bbid = bbid
        self.__bcid = bcid
        self.__delisted = delisted
        self.__bbidEquivalent = bbidEquivalent
        self.__cusip = cusip
        self.__gss = gss
        self.__isin = isin
        self.__jsn = jsn
        self.__primeId = primeId
        self.__sedol = sedol
        self.__ticker = ticker
        self.__valoren = valoren
        self.__wpk = wpk
        self.__gsn = gsn
        self.__secName = secName
        self.__cross = cross
        self.__simonId = simonId
        self.__emId = emId
        self.__cmId = cmId
        self.__lmsId = lmsId
        self.__mdapi = mdapi
        self.__mic = mic
        self.__sfId = sfId
        self.__dollarCross = dollarCross

    @property
    def ric(self) -> str:
        """Reuters Instrument Code identifier"""
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self.__ric = value
        self._property_changed('ric')        

    @property
    def rcic(self) -> str:
        """Reuters Composite Instrument Code Identifier"""
        return self.__rcic

    @rcic.setter
    def rcic(self, value: str):
        self.__rcic = value
        self._property_changed('rcic')        

    @property
    def eid(self) -> str:
        """EID Identifier"""
        return self.__eid

    @eid.setter
    def eid(self, value: str):
        self.__eid = value
        self._property_changed('eid')        

    @property
    def gsideid(self) -> str:
        """GSID_EID Identifier"""
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: str):
        self.__gsideid = value
        self._property_changed('gsideid')        

    @property
    def gsid(self) -> str:
        """GSID Identifier"""
        return self.__gsid

    @gsid.setter
    def gsid(self, value: str):
        self.__gsid = value
        self._property_changed('gsid')        

    @property
    def cid(self) -> str:
        """Company Id Identifier"""
        return self.__cid

    @cid.setter
    def cid(self, value: str):
        self.__cid = value
        self._property_changed('cid')        

    @property
    def bbid(self) -> str:
        """Bloomberg Id Identifier"""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self.__bbid = value
        self._property_changed('bbid')        

    @property
    def bcid(self) -> str:
        """Bloomberg Composite Identifier"""
        return self.__bcid

    @bcid.setter
    def bcid(self, value: str):
        self.__bcid = value
        self._property_changed('bcid')        

    @property
    def delisted(self) -> str:
        """Whether an asset has been delisted"""
        return self.__delisted

    @delisted.setter
    def delisted(self, value: str):
        self.__delisted = value
        self._property_changed('delisted')        

    @property
    def bbidEquivalent(self) -> str:
        """Bloomberg Equivalent Identifier"""
        return self.__bbidEquivalent

    @bbidEquivalent.setter
    def bbidEquivalent(self, value: str):
        self.__bbidEquivalent = value
        self._property_changed('bbidEquivalent')        

    @property
    def cusip(self) -> str:
        """Cusip Identifier"""
        return self.__cusip

    @cusip.setter
    def cusip(self, value: str):
        self.__cusip = value
        self._property_changed('cusip')        

    @property
    def gss(self) -> str:
        """GS Symbol identifier"""
        return self.__gss

    @gss.setter
    def gss(self, value: str):
        self.__gss = value
        self._property_changed('gss')        

    @property
    def isin(self) -> str:
        """International Security Number"""
        return self.__isin

    @isin.setter
    def isin(self, value: str):
        self.__isin = value
        self._property_changed('isin')        

    @property
    def jsn(self) -> str:
        """Japan Security Number"""
        return self.__jsn

    @jsn.setter
    def jsn(self, value: str):
        self.__jsn = value
        self._property_changed('jsn')        

    @property
    def primeId(self) -> str:
        """PrimeID Identifier"""
        return self.__primeId

    @primeId.setter
    def primeId(self, value: str):
        self.__primeId = value
        self._property_changed('primeId')        

    @property
    def sedol(self) -> str:
        """Sedol Identifier"""
        return self.__sedol

    @sedol.setter
    def sedol(self, value: str):
        self.__sedol = value
        self._property_changed('sedol')        

    @property
    def ticker(self) -> str:
        """Ticker Identifier"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self.__ticker = value
        self._property_changed('ticker')        

    @property
    def valoren(self) -> str:
        """Valoren Identifier"""
        return self.__valoren

    @valoren.setter
    def valoren(self, value: str):
        self.__valoren = value
        self._property_changed('valoren')        

    @property
    def wpk(self) -> str:
        """Wertpapier Kenn-Nummer"""
        return self.__wpk

    @wpk.setter
    def wpk(self, value: str):
        self.__wpk = value
        self._property_changed('wpk')        

    @property
    def gsn(self) -> str:
        """Goldman Sachs internal product number"""
        return self.__gsn

    @gsn.setter
    def gsn(self, value: str):
        self.__gsn = value
        self._property_changed('gsn')        

    @property
    def secName(self) -> str:
        """Internal Goldman Sachs security name"""
        return self.__secName

    @secName.setter
    def secName(self, value: str):
        self.__secName = value
        self._property_changed('secName')        

    @property
    def cross(self) -> str:
        """Cross identifier"""
        return self.__cross

    @cross.setter
    def cross(self, value: str):
        self.__cross = value
        self._property_changed('cross')        

    @property
    def simonId(self) -> str:
        """SIMON product identifier"""
        return self.__simonId

    @simonId.setter
    def simonId(self, value: str):
        self.__simonId = value
        self._property_changed('simonId')        

    @property
    def emId(self) -> str:
        """Entity Master Identifier"""
        return self.__emId

    @emId.setter
    def emId(self, value: str):
        self.__emId = value
        self._property_changed('emId')        

    @property
    def cmId(self) -> str:
        """Client Master Party Id"""
        return self.__cmId

    @cmId.setter
    def cmId(self, value: str):
        self.__cmId = value
        self._property_changed('cmId')        

    @property
    def lmsId(self) -> str:
        """Listed Market Symbol"""
        return self.__lmsId

    @lmsId.setter
    def lmsId(self, value: str):
        self.__lmsId = value
        self._property_changed('lmsId')        

    @property
    def mdapi(self) -> str:
        """MDAPI Asset"""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: str):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def mic(self) -> str:
        """Market Identifier Code"""
        return self.__mic

    @mic.setter
    def mic(self, value: str):
        self.__mic = value
        self._property_changed('mic')        

    @property
    def sfId(self) -> str:
        """SalesForce ID"""
        return self.__sfId

    @sfId.setter
    def sfId(self, value: str):
        self.__sfId = value
        self._property_changed('sfId')        

    @property
    def dollarCross(self) -> str:
        """USD cross identifier for a particular currency"""
        return self.__dollarCross

    @dollarCross.setter
    def dollarCross(self, value: str):
        self.__dollarCross = value
        self._property_changed('dollarCross')        


class GIRDomain(Base):
               
    def __init__(self, documentLinks: Tuple[Link, ...] = None):
        super().__init__()
        self.__documentLinks = documentLinks

    @property
    def documentLinks(self) -> Tuple[Link, ...]:
        """Documents related to this asset"""
        return self.__documentLinks

    @documentLinks.setter
    def documentLinks(self, value: Tuple[Link, ...]):
        self.__documentLinks = value
        self._property_changed('documentLinks')        


class FieldFilterMap(Base):
               
    def __init__(self, **kwargs):
        super().__init__()
        self.__queueClockTimeLabel = kwargs.get('queueClockTimeLabel')
        self.__marketPnl = kwargs.get('marketPnl')
        self.__year = kwargs.get('year')
        self.__sustainAsiaExJapan = kwargs.get('sustainAsiaExJapan')
        self.__investmentRate = kwargs.get('investmentRate')
        self.__assetClassificationsGicsSubIndustry = kwargs.get('assetClassificationsGicsSubIndustry')
        self.__bidUnadjusted = kwargs.get('bidUnadjusted')
        self.__economicTermsHash = kwargs.get('economicTermsHash')
        self.__neighbourAssetId = kwargs.get('neighbourAssetId')
        self.__simonIntlAssetTags = kwargs.get('simonIntlAssetTags')
        self.__path = kwargs.get('path')
        self.__availableInventory = kwargs.get('availableInventory')
        self.__clientContact = kwargs.get('clientContact')
        self.__est1DayCompletePct = kwargs.get('est1DayCompletePct')
        self.__rank = kwargs.get('rank')
        self.__dataSetCategory = kwargs.get('dataSetCategory')
        self.__createdById = kwargs.get('createdById')
        self.__vehicleType = kwargs.get('vehicleType')
        self.__dailyRisk = kwargs.get('dailyRisk')
        self.__bosInBpsLabel = kwargs.get('bosInBpsLabel')
        self.__marketDataType = kwargs.get('marketDataType')
        self.__sentimentScore = kwargs.get('sentimentScore')
        self.__bosInBps = kwargs.get('bosInBps')
        self.__pointClass = kwargs.get('pointClass')
        self.__fxSpot = kwargs.get('fxSpot')
        self.__bidLow = kwargs.get('bidLow')
        self.__valuePrevious = kwargs.get('valuePrevious')
        self.__fairVarianceVolatility = kwargs.get('fairVarianceVolatility')
        self.__avgTradeRate = kwargs.get('avgTradeRate')
        self.__shortLevel = kwargs.get('shortLevel')
        self.__hedgeVolatility = kwargs.get('hedgeVolatility')
        self.__version = kwargs.get('version')
        self.__tags = kwargs.get('tags')
        self.__underlyingAssetId = kwargs.get('underlyingAssetId')
        self.__clientExposure = kwargs.get('clientExposure')
        self.__correlation = kwargs.get('correlation')
        self.__exposure = kwargs.get('exposure')
        self.__gsSustainSubSector = kwargs.get('gsSustainSubSector')
        self.__domain = kwargs.get('domain')
        self.__marketDataAsset = kwargs.get('marketDataAsset')
        self.__forwardTenor = kwargs.get('forwardTenor')
        self.__unadjustedHigh = kwargs.get('unadjustedHigh')
        self.__sourceImportance = kwargs.get('sourceImportance')
        self.__eid = kwargs.get('eid')
        self.__jsn = kwargs.get('jsn')
        self.__relativeReturnQtd = kwargs.get('relativeReturnQtd')
        self.__displayName = kwargs.get('displayName')
        self.__minutesToTrade100Pct = kwargs.get('minutesToTrade100Pct')
        self.__marketModelId = kwargs.get('marketModelId')
        self.__quoteType = kwargs.get('quoteType')
        self.__tenor = kwargs.get('tenor')
        self.__esPolicyPercentile = kwargs.get('esPolicyPercentile')
        self.__tcmCostParticipationRate75Pct = kwargs.get('tcmCostParticipationRate75Pct')
        self.__close = kwargs.get('close')
        self.__tcmCostParticipationRate100Pct = kwargs.get('tcmCostParticipationRate100Pct')
        self.__disclaimer = kwargs.get('disclaimer')
        self.__measureIdx = kwargs.get('measureIdx')
        self.__a = kwargs.get('a')
        self.__b = kwargs.get('b')
        self.__loanFee = kwargs.get('loanFee')
        self.__c = kwargs.get('c')
        self.__equityVega = kwargs.get('equityVega')
        self.__deploymentVersion = kwargs.get('deploymentVersion')
        self.__fiveDayMove = kwargs.get('fiveDayMove')
        self.__borrower = kwargs.get('borrower')
        self.__performanceContribution = kwargs.get('performanceContribution')
        self.__targetNotional = kwargs.get('targetNotional')
        self.__fillLegId = kwargs.get('fillLegId')
        self.__delisted = kwargs.get('delisted')
        self.__rationale = kwargs.get('rationale')
        self.__regionalFocus = kwargs.get('regionalFocus')
        self.__volumePrimary = kwargs.get('volumePrimary')
        self.__series = kwargs.get('series')
        self.__simonId = kwargs.get('simonId')
        self.__newIdeasQtd = kwargs.get('newIdeasQtd')
        self.__adjustedAskPrice = kwargs.get('adjustedAskPrice')
        self.__quarter = kwargs.get('quarter')
        self.__factorUniverse = kwargs.get('factorUniverse')
        self.__eventCategory = kwargs.get('eventCategory')
        self.__impliedNormalVolatility = kwargs.get('impliedNormalVolatility')
        self.__unadjustedOpen = kwargs.get('unadjustedOpen')
        self.__arrivalRt = kwargs.get('arrivalRt')
        self.__transactionCost = kwargs.get('transactionCost')
        self.__servicingCostShortPnl = kwargs.get('servicingCostShortPnl')
        self.__bidAskSpread = kwargs.get('bidAskSpread')
        self.__optionType = kwargs.get('optionType')
        self.__tcmCostHorizon3Hour = kwargs.get('tcmCostHorizon3Hour')
        self.__clusterDescription = kwargs.get('clusterDescription')
        self.__positionAmount = kwargs.get('positionAmount')
        self.__numberOfPositions = kwargs.get('numberOfPositions')
        self.__windSpeed = kwargs.get('windSpeed')
        self.__openUnadjusted = kwargs.get('openUnadjusted')
        self.__maRank = kwargs.get('maRank')
        self.__askPrice = kwargs.get('askPrice')
        self.__eventId = kwargs.get('eventId')
        self.__dataProduct = kwargs.get('dataProduct')
        self.__sectors = kwargs.get('sectors')
        self.__annualizedTrackingError = kwargs.get('annualizedTrackingError')
        self.__volSwap = kwargs.get('volSwap')
        self.__annualizedRisk = kwargs.get('annualizedRisk')
        self.__corporateAction = kwargs.get('corporateAction')
        self.__conviction = kwargs.get('conviction')
        self.__grossExposure = kwargs.get('grossExposure')
        self.__benchmarkMaturity = kwargs.get('benchmarkMaturity')
        self.__volumeComposite = kwargs.get('volumeComposite')
        self.__volume = kwargs.get('volume')
        self.__adv = kwargs.get('adv')
        self.__stsFxCurrency = kwargs.get('stsFxCurrency')
        self.__wpk = kwargs.get('wpk')
        self.__shortConvictionMedium = kwargs.get('shortConvictionMedium')
        self.__bidChange = kwargs.get('bidChange')
        self.__exchange = kwargs.get('exchange')
        self.__expiration = kwargs.get('expiration')
        self.__tradePrice = kwargs.get('tradePrice')
        self.__esPolicyScore = kwargs.get('esPolicyScore')
        self.__loanId = kwargs.get('loanId')
        self.__cid = kwargs.get('cid')
        self.__liquidityScore = kwargs.get('liquidityScore')
        self.__importance = kwargs.get('importance')
        self.__sourceDateSpan = kwargs.get('sourceDateSpan')
        self.__assetClassificationsGicsSector = kwargs.get('assetClassificationsGicsSector')
        self.__underlyingDataSetId = kwargs.get('underlyingDataSetId')
        self.__stsAssetName = kwargs.get('stsAssetName')
        self.__closeUnadjusted = kwargs.get('closeUnadjusted')
        self.__valueUnit = kwargs.get('valueUnit')
        self.__bidHigh = kwargs.get('bidHigh')
        self.__adjustedLowPrice = kwargs.get('adjustedLowPrice')
        self.__netExposureClassification = kwargs.get('netExposureClassification')
        self.__longConvictionLarge = kwargs.get('longConvictionLarge')
        self.__fairVariance = kwargs.get('fairVariance')
        self.__hitRateWtd = kwargs.get('hitRateWtd')
        self.__oad = kwargs.get('oad')
        self.__bosInBpsDescription = kwargs.get('bosInBpsDescription')
        self.__lowPrice = kwargs.get('lowPrice')
        self.__realizedVolatility = kwargs.get('realizedVolatility')
        self.__rate = kwargs.get('rate')
        self.__adv22DayPct = kwargs.get('adv22DayPct')
        self.__alpha = kwargs.get('alpha')
        self.__client = kwargs.get('client')
        self.__company = kwargs.get('company')
        self.__convictionList = kwargs.get('convictionList')
        self.__priceRangeInTicksLabel = kwargs.get('priceRangeInTicksLabel')
        self.__ticker = kwargs.get('ticker')
        self.__inRiskModel = kwargs.get('inRiskModel')
        self.__tcmCostHorizon1Day = kwargs.get('tcmCostHorizon1Day')
        self.__servicingCostLongPnl = kwargs.get('servicingCostLongPnl')
        self.__stsRatesCountry = kwargs.get('stsRatesCountry')
        self.__meetingNumber = kwargs.get('meetingNumber')
        self.__exchangeId = kwargs.get('exchangeId')
        self.__horizon = kwargs.get('horizon')
        self.__tcmCostHorizon20Day = kwargs.get('tcmCostHorizon20Day')
        self.__longLevel = kwargs.get('longLevel')
        self.__sourceValueForecast = kwargs.get('sourceValueForecast')
        self.__shortConvictionLarge = kwargs.get('shortConvictionLarge')
        self.__realm = kwargs.get('realm')
        self.__bid = kwargs.get('bid')
        self.__dataDescription = kwargs.get('dataDescription')
        self.__composite22DayAdv = kwargs.get('composite22DayAdv')
        self.__gsn = kwargs.get('gsn')
        self.__isAggressive = kwargs.get('isAggressive')
        self.__orderId = kwargs.get('orderId')
        self.__gss = kwargs.get('gss')
        self.__percentOfMediandv1m = kwargs.get('percentOfMediandv1m')
        self.__lendables = kwargs.get('lendables')
        self.__assetClass = kwargs.get('assetClass')
        self.__gsideid = kwargs.get('gsideid')
        self.__bosInTicksLabel = kwargs.get('bosInTicksLabel')
        self.__ric = kwargs.get('ric')
        self.__positionSourceId = kwargs.get('positionSourceId')
        self.__division = kwargs.get('division')
        self.__marketCapUSD = kwargs.get('marketCapUSD')
        self.__deploymentId = kwargs.get('deploymentId')
        self.__highPrice = kwargs.get('highPrice')
        self.__shortWeight = kwargs.get('shortWeight')
        self.__absoluteShares = kwargs.get('absoluteShares')
        self.__action = kwargs.get('action')
        self.__model = kwargs.get('model')
        self.__id = kwargs.get('id')
        self.__arrivalHaircutVwapNormalized = kwargs.get('arrivalHaircutVwapNormalized')
        self.__queueClockTimeDescription = kwargs.get('queueClockTimeDescription')
        self.__period = kwargs.get('period')
        self.__indexCreateSource = kwargs.get('indexCreateSource')
        self.__fiscalQuarter = kwargs.get('fiscalQuarter')
        self.__deltaStrike = kwargs.get('deltaStrike')
        self.__marketImpact = kwargs.get('marketImpact')
        self.__eventType = kwargs.get('eventType')
        self.__assetCountLong = kwargs.get('assetCountLong')
        self.__valueActual = kwargs.get('valueActual')
        self.__bcid = kwargs.get('bcid')
        self.__originalCountry = kwargs.get('originalCountry')
        self.__touchLiquidityScore = kwargs.get('touchLiquidityScore')
        self.__field = kwargs.get('field')
        self.__spot = kwargs.get('spot')
        self.__expectedCompletionDate = kwargs.get('expectedCompletionDate')
        self.__loanValue = kwargs.get('loanValue')
        self.__skew = kwargs.get('skew')
        self.__status = kwargs.get('status')
        self.__sustainEmergingMarkets = kwargs.get('sustainEmergingMarkets')
        self.__totalReturnPrice = kwargs.get('totalReturnPrice')
        self.__city = kwargs.get('city')
        self.__eventSource = kwargs.get('eventSource')
        self.__qisPermNo = kwargs.get('qisPermNo')
        self.__hitRateYtd = kwargs.get('hitRateYtd')
        self.__stsCommodity = kwargs.get('stsCommodity')
        self.__stsCommoditySector = kwargs.get('stsCommoditySector')
        self.__salesCoverage = kwargs.get('salesCoverage')
        self.__shortExposure = kwargs.get('shortExposure')
        self.__esScore = kwargs.get('esScore')
        self.__tcmCostParticipationRate10Pct = kwargs.get('tcmCostParticipationRate10Pct')
        self.__eventTime = kwargs.get('eventTime')
        self.__positionSourceName = kwargs.get('positionSourceName')
        self.__priceRangeInTicks = kwargs.get('priceRangeInTicks')
        self.__arrivalHaircutVwap = kwargs.get('arrivalHaircutVwap')
        self.__interestRate = kwargs.get('interestRate')
        self.__executionDays = kwargs.get('executionDays')
        self.__pctChange = kwargs.get('pctChange')
        self.__side = kwargs.get('side')
        self.__numberOfRolls = kwargs.get('numberOfRolls')
        self.__agentLenderFee = kwargs.get('agentLenderFee')
        self.__complianceRestrictedStatus = kwargs.get('complianceRestrictedStatus')
        self.__forward = kwargs.get('forward')
        self.__borrowFee = kwargs.get('borrowFee')
        self.__strike = kwargs.get('strike')
        self.__loanSpread = kwargs.get('loanSpread')
        self.__tcmCostHorizon12Hour = kwargs.get('tcmCostHorizon12Hour')
        self.__dewPoint = kwargs.get('dewPoint')
        self.__researchCommission = kwargs.get('researchCommission')
        self.__bbid = kwargs.get('bbid')
        self.__assetClassificationsRiskCountryCode = kwargs.get('assetClassificationsRiskCountryCode')
        self.__eventStatus = kwargs.get('eventStatus')
        self.__return = kwargs.get('return_')
        self.__maxTemperature = kwargs.get('maxTemperature')
        self.__acquirerShareholderMeetingDate = kwargs.get('acquirerShareholderMeetingDate')
        self.__arrivalMidNormalized = kwargs.get('arrivalMidNormalized')
        self.__rating = kwargs.get('rating')
        self.__arrivalRtNormalized = kwargs.get('arrivalRtNormalized')
        self.__performanceFee = kwargs.get('performanceFee')
        self.__reportType = kwargs.get('reportType')
        self.__sourceURL = kwargs.get('sourceURL')
        self.__estimatedReturn = kwargs.get('estimatedReturn')
        self.__underlyingAssetIds = kwargs.get('underlyingAssetIds')
        self.__high = kwargs.get('high')
        self.__sourceLastUpdate = kwargs.get('sourceLastUpdate')
        self.__queueInLotsLabel = kwargs.get('queueInLotsLabel')
        self.__adv10DayPct = kwargs.get('adv10DayPct')
        self.__longConvictionMedium = kwargs.get('longConvictionMedium')
        self.__eventName = kwargs.get('eventName')
        self.__annualRisk = kwargs.get('annualRisk')
        self.__dailyTrackingError = kwargs.get('dailyTrackingError')
        self.__unadjustedBid = kwargs.get('unadjustedBid')
        self.__gsdeer = kwargs.get('gsdeer')
        self.__marketCap = kwargs.get('marketCap')
        self.__clusterRegion = kwargs.get('clusterRegion')
        self.__bbidEquivalent = kwargs.get('bbidEquivalent')
        self.__prevCloseAsk = kwargs.get('prevCloseAsk')
        self.__level = kwargs.get('level')
        self.__valoren = kwargs.get('valoren')
        self.__pressure = kwargs.get('pressure')
        self.__shortDescription = kwargs.get('shortDescription')
        self.__basis = kwargs.get('basis')
        self.__netWeight = kwargs.get('netWeight')
        self.__hedgeId = kwargs.get('hedgeId')
        self.__portfolioManagers = kwargs.get('portfolioManagers')
        self.__assetParametersCommoditySector = kwargs.get('assetParametersCommoditySector')
        self.__bosInTicks = kwargs.get('bosInTicks')
        self.__tcmCostHorizon8Day = kwargs.get('tcmCostHorizon8Day')
        self.__supraStrategy = kwargs.get('supraStrategy')
        self.__adv5DayPct = kwargs.get('adv5DayPct')
        self.__factorSource = kwargs.get('factorSource')
        self.__leverage = kwargs.get('leverage')
        self.__submitter = kwargs.get('submitter')
        self.__notional = kwargs.get('notional')
        self.__esDisclosurePercentage = kwargs.get('esDisclosurePercentage')
        self.__clientShortName = kwargs.get('clientShortName')
        self.__fwdPoints = kwargs.get('fwdPoints')
        self.__groupCategory = kwargs.get('groupCategory')
        self.__kpiId = kwargs.get('kpiId')
        self.__relativeReturnWtd = kwargs.get('relativeReturnWtd')
        self.__bidPlusAsk = kwargs.get('bidPlusAsk')
        self.__assetClassificationsRiskCountryName = kwargs.get('assetClassificationsRiskCountryName')
        self.__total = kwargs.get('total')
        self.__riskModel = kwargs.get('riskModel')
        self.__assetId = kwargs.get('assetId')
        self.__fairValue = kwargs.get('fairValue')
        self.__adjustedHighPrice = kwargs.get('adjustedHighPrice')
        self.__beta = kwargs.get('beta')
        self.__direction = kwargs.get('direction')
        self.__valueForecast = kwargs.get('valueForecast')
        self.__longExposure = kwargs.get('longExposure')
        self.__positionSourceType = kwargs.get('positionSourceType')
        self.__tcmCostParticipationRate20Pct = kwargs.get('tcmCostParticipationRate20Pct')
        self.__adjustedClosePrice = kwargs.get('adjustedClosePrice')
        self.__cross = kwargs.get('cross')
        self.__lmsId = kwargs.get('lmsId')
        self.__rebateRate = kwargs.get('rebateRate')
        self.__ideaStatus = kwargs.get('ideaStatus')
        self.__participationRate = kwargs.get('participationRate')
        self.__obfr = kwargs.get('obfr')
        self.__fxForecast = kwargs.get('fxForecast')
        self.__fixingTimeLabel = kwargs.get('fixingTimeLabel')
        self.__fillId = kwargs.get('fillId')
        self.__esNumericScore = kwargs.get('esNumericScore')
        self.__inBenchmark = kwargs.get('inBenchmark')
        self.__strategy = kwargs.get('strategy')
        self.__shortInterest = kwargs.get('shortInterest')
        self.__referencePeriod = kwargs.get('referencePeriod')
        self.__adjustedVolume = kwargs.get('adjustedVolume')
        self.__queueInLotsDescription = kwargs.get('queueInLotsDescription')
        self.__pbClientId = kwargs.get('pbClientId')
        self.__ownerId = kwargs.get('ownerId')
        self.__secDB = kwargs.get('secDB')
        self.__composite10DayAdv = kwargs.get('composite10DayAdv')
        self.__objective = kwargs.get('objective')
        self.__navPrice = kwargs.get('navPrice')
        self.__ideaActivityType = kwargs.get('ideaActivityType')
        self.__precipitation = kwargs.get('precipitation')
        self.__ideaSource = kwargs.get('ideaSource')
        self.__hedgeNotional = kwargs.get('hedgeNotional')
        self.__askLow = kwargs.get('askLow')
        self.__unadjustedAsk = kwargs.get('unadjustedAsk')
        self.__betaAdjustedNetExposure = kwargs.get('betaAdjustedNetExposure')
        self.__expiry = kwargs.get('expiry')
        self.__tradingPnl = kwargs.get('tradingPnl')
        self.__strikePercentage = kwargs.get('strikePercentage')
        self.__excessReturnPrice = kwargs.get('excessReturnPrice')
        self.__givenPlusPaid = kwargs.get('givenPlusPaid')
        self.__shortConvictionSmall = kwargs.get('shortConvictionSmall')
        self.__prevCloseBid = kwargs.get('prevCloseBid')
        self.__fxPnl = kwargs.get('fxPnl')
        self.__forecast = kwargs.get('forecast')
        self.__tcmCostHorizon16Day = kwargs.get('tcmCostHorizon16Day')
        self.__pnl = kwargs.get('pnl')
        self.__assetClassificationsGicsIndustryGroup = kwargs.get('assetClassificationsGicsIndustryGroup')
        self.__unadjustedClose = kwargs.get('unadjustedClose')
        self.__tcmCostHorizon4Day = kwargs.get('tcmCostHorizon4Day')
        self.__assetClassificationsIsPrimary = kwargs.get('assetClassificationsIsPrimary')
        self.__styles = kwargs.get('styles')
        self.__lendingSecId = kwargs.get('lendingSecId')
        self.__shortName = kwargs.get('shortName')
        self.__equityTheta = kwargs.get('equityTheta')
        self.__averageFillPrice = kwargs.get('averageFillPrice')
        self.__snowfall = kwargs.get('snowfall')
        self.__mic = kwargs.get('mic')
        self.__openPrice = kwargs.get('openPrice')
        self.__autoExecState = kwargs.get('autoExecState')
        self.__depthSpreadScore = kwargs.get('depthSpreadScore')
        self.__relativeReturnYtd = kwargs.get('relativeReturnYtd')
        self.__long = kwargs.get('long')
        self.__fairVolatility = kwargs.get('fairVolatility')
        self.__dollarCross = kwargs.get('dollarCross')
        self.__longWeight = kwargs.get('longWeight')
        self.__vendor = kwargs.get('vendor')
        self.__currency = kwargs.get('currency')
        self.__clusterClass = kwargs.get('clusterClass')
        self.__financialReturnsScore = kwargs.get('financialReturnsScore')
        self.__netChange = kwargs.get('netChange')
        self.__nonSymbolDimensions = kwargs.get('nonSymbolDimensions')
        self.__bidSize = kwargs.get('bidSize')
        self.__arrivalMid = kwargs.get('arrivalMid')
        self.__assetParametersExchangeCurrency = kwargs.get('assetParametersExchangeCurrency')
        self.__unexplained = kwargs.get('unexplained')
        self.__assetClassificationsCountryName = kwargs.get('assetClassificationsCountryName')
        self.__metric = kwargs.get('metric')
        self.__newIdeasYtd = kwargs.get('newIdeasYtd')
        self.__managementFee = kwargs.get('managementFee')
        self.__ask = kwargs.get('ask')
        self.__impliedLognormalVolatility = kwargs.get('impliedLognormalVolatility')
        self.__closePrice = kwargs.get('closePrice')
        self.__open = kwargs.get('open')
        self.__sourceId = kwargs.get('sourceId')
        self.__country = kwargs.get('country')
        self.__cusip = kwargs.get('cusip')
        self.__touchSpreadScore = kwargs.get('touchSpreadScore')
        self.__absoluteStrike = kwargs.get('absoluteStrike')
        self.__netExposure = kwargs.get('netExposure')
        self.__source = kwargs.get('source')
        self.__assetClassificationsCountryCode = kwargs.get('assetClassificationsCountryCode')
        self.__frequency = kwargs.get('frequency')
        self.__activityId = kwargs.get('activityId')
        self.__estimatedImpact = kwargs.get('estimatedImpact')
        self.__dataSetSubCategory = kwargs.get('dataSetSubCategory')
        self.__assetParametersPricingLocation = kwargs.get('assetParametersPricingLocation')
        self.__eventDescription = kwargs.get('eventDescription')
        self.__strikeReference = kwargs.get('strikeReference')
        self.__details = kwargs.get('details')
        self.__assetCount = kwargs.get('assetCount')
        self.__given = kwargs.get('given')
        self.__absoluteValue = kwargs.get('absoluteValue')
        self.__delistingDate = kwargs.get('delistingDate')
        self.__longTenor = kwargs.get('longTenor')
        self.__mctr = kwargs.get('mctr')
        self.__weight = kwargs.get('weight')
        self.__historicalClose = kwargs.get('historicalClose')
        self.__assetCountPriced = kwargs.get('assetCountPriced')
        self.__marketDataPoint = kwargs.get('marketDataPoint')
        self.__ideaId = kwargs.get('ideaId')
        self.__commentStatus = kwargs.get('commentStatus')
        self.__marginalCost = kwargs.get('marginalCost')
        self.__absoluteWeight = kwargs.get('absoluteWeight')
        self.__measure = kwargs.get('measure')
        self.__clientWeight = kwargs.get('clientWeight')
        self.__hedgeAnnualizedVolatility = kwargs.get('hedgeAnnualizedVolatility')
        self.__benchmarkCurrency = kwargs.get('benchmarkCurrency')
        self.__name = kwargs.get('name')
        self.__aum = kwargs.get('aum')
        self.__folderName = kwargs.get('folderName')
        self.__lendingPartnerFee = kwargs.get('lendingPartnerFee')
        self.__region = kwargs.get('region')
        self.__liveDate = kwargs.get('liveDate')
        self.__askHigh = kwargs.get('askHigh')
        self.__corporateActionType = kwargs.get('corporateActionType')
        self.__primeId = kwargs.get('primeId')
        self.__tenor2 = kwargs.get('tenor2')
        self.__description = kwargs.get('description')
        self.__valueRevised = kwargs.get('valueRevised')
        self.__ownerName = kwargs.get('ownerName')
        self.__adjustedTradePrice = kwargs.get('adjustedTradePrice')
        self.__lastUpdatedById = kwargs.get('lastUpdatedById')
        self.__zScore = kwargs.get('zScore')
        self.__targetShareholderMeetingDate = kwargs.get('targetShareholderMeetingDate')
        self.__isADR = kwargs.get('isADR')
        self.__eventStartTime = kwargs.get('eventStartTime')
        self.__factor = kwargs.get('factor')
        self.__longConvictionSmall = kwargs.get('longConvictionSmall')
        self.__serviceId = kwargs.get('serviceId')
        self.__turnover = kwargs.get('turnover')
        self.__gsfeer = kwargs.get('gsfeer')
        self.__coverage = kwargs.get('coverage')
        self.__backtestId = kwargs.get('backtestId')
        self.__gPercentile = kwargs.get('gPercentile')
        self.__gScore = kwargs.get('gScore')
        self.__marketValue = kwargs.get('marketValue')
        self.__multipleScore = kwargs.get('multipleScore')
        self.__lendingFundNav = kwargs.get('lendingFundNav')
        self.__sourceOriginalCategory = kwargs.get('sourceOriginalCategory')
        self.__betaAdjustedExposure = kwargs.get('betaAdjustedExposure')
        self.__composite5DayAdv = kwargs.get('composite5DayAdv')
        self.__dividendPoints = kwargs.get('dividendPoints')
        self.__newIdeasWtd = kwargs.get('newIdeasWtd')
        self.__paid = kwargs.get('paid')
        self.__short = kwargs.get('short')
        self.__location = kwargs.get('location')
        self.__comment = kwargs.get('comment')
        self.__bosInTicksDescription = kwargs.get('bosInTicksDescription')
        self.__sourceSymbol = kwargs.get('sourceSymbol')
        self.__scenarioId = kwargs.get('scenarioId')
        self.__askUnadjusted = kwargs.get('askUnadjusted')
        self.__queueClockTime = kwargs.get('queueClockTime')
        self.__askChange = kwargs.get('askChange')
        self.__tcmCostParticipationRate50Pct = kwargs.get('tcmCostParticipationRate50Pct')
        self.__normalizedPerformance = kwargs.get('normalizedPerformance')
        self.__cmId = kwargs.get('cmId')
        self.__type = kwargs.get('type')
        self.__mdapi = kwargs.get('mdapi')
        self.__dividendYield = kwargs.get('dividendYield')
        self.__cumulativePnl = kwargs.get('cumulativePnl')
        self.__sourceOrigin = kwargs.get('sourceOrigin')
        self.__shortTenor = kwargs.get('shortTenor')
        self.__unadjustedVolume = kwargs.get('unadjustedVolume')
        self.__measures = kwargs.get('measures')
        self.__tradingCostPnl = kwargs.get('tradingCostPnl')
        self.__internalUser = kwargs.get('internalUser')
        self.__price = kwargs.get('price')
        self.__paymentQuantity = kwargs.get('paymentQuantity')
        self.__underlyer = kwargs.get('underlyer')
        self.__positionIdx = kwargs.get('positionIdx')
        self.__secName = kwargs.get('secName')
        self.__percentADV = kwargs.get('percentADV')
        self.__unadjustedLow = kwargs.get('unadjustedLow')
        self.__contract = kwargs.get('contract')
        self.__sedol = kwargs.get('sedol')
        self.__roundingCostPnl = kwargs.get('roundingCostPnl')
        self.__sustainGlobal = kwargs.get('sustainGlobal')
        self.__sourceTicker = kwargs.get('sourceTicker')
        self.__portfolioId = kwargs.get('portfolioId')
        self.__gsid = kwargs.get('gsid')
        self.__esPercentile = kwargs.get('esPercentile')
        self.__lendingFund = kwargs.get('lendingFund')
        self.__tcmCostParticipationRate15Pct = kwargs.get('tcmCostParticipationRate15Pct')
        self.__sensitivity = kwargs.get('sensitivity')
        self.__fiscalYear = kwargs.get('fiscalYear')
        self.__rcic = kwargs.get('rcic')
        self.__simonAssetTags = kwargs.get('simonAssetTags')
        self.__internal = kwargs.get('internal')
        self.__forwardPoint = kwargs.get('forwardPoint')
        self.__assetClassificationsGicsIndustry = kwargs.get('assetClassificationsGicsIndustry')
        self.__adjustedBidPrice = kwargs.get('adjustedBidPrice')
        self.__hitRateQtd = kwargs.get('hitRateQtd')
        self.__varSwap = kwargs.get('varSwap')
        self.__lowUnadjusted = kwargs.get('lowUnadjusted')
        self.__sectorsRaw = kwargs.get('sectorsRaw')
        self.__low = kwargs.get('low')
        self.__crossGroup = kwargs.get('crossGroup')
        self.__integratedScore = kwargs.get('integratedScore')
        self.__fiveDayPriceChangeBps = kwargs.get('fiveDayPriceChangeBps')
        self.__tradeSize = kwargs.get('tradeSize')
        self.__symbolDimensions = kwargs.get('symbolDimensions')
        self.__quotingStyle = kwargs.get('quotingStyle')
        self.__scenarioGroupId = kwargs.get('scenarioGroupId')
        self.__errorMessage = kwargs.get('errorMessage')
        self.__avgTradeRateDescription = kwargs.get('avgTradeRateDescription')
        self.__midPrice = kwargs.get('midPrice')
        self.__fraction = kwargs.get('fraction')
        self.__stsCreditMarket = kwargs.get('stsCreditMarket')
        self.__assetCountShort = kwargs.get('assetCountShort')
        self.__stsEmDm = kwargs.get('stsEmDm')
        self.__tcmCostHorizon2Day = kwargs.get('tcmCostHorizon2Day')
        self.__queueInLots = kwargs.get('queueInLots')
        self.__priceRangeInTicksDescription = kwargs.get('priceRangeInTicksDescription')
        self.__tenderOfferExpirationDate = kwargs.get('tenderOfferExpirationDate')
        self.__highUnadjusted = kwargs.get('highUnadjusted')
        self.__sourceCategory = kwargs.get('sourceCategory')
        self.__volumeUnadjusted = kwargs.get('volumeUnadjusted')
        self.__avgTradeRateLabel = kwargs.get('avgTradeRateLabel')
        self.__tcmCostParticipationRate5Pct = kwargs.get('tcmCostParticipationRate5Pct')
        self.__isActive = kwargs.get('isActive')
        self.__growthScore = kwargs.get('growthScore')
        self.__encodedStats = kwargs.get('encodedStats')
        self.__adjustedShortInterest = kwargs.get('adjustedShortInterest')
        self.__askSize = kwargs.get('askSize')
        self.__mdapiType = kwargs.get('mdapiType')
        self.__group = kwargs.get('group')
        self.__estimatedSpread = kwargs.get('estimatedSpread')
        self.__resource = kwargs.get('resource')
        self.__tcmCost = kwargs.get('tcmCost')
        self.__sustainJapan = kwargs.get('sustainJapan')
        self.__navSpread = kwargs.get('navSpread')
        self.__bidPrice = kwargs.get('bidPrice')
        self.__hedgeTrackingError = kwargs.get('hedgeTrackingError')
        self.__marketCapCategory = kwargs.get('marketCapCategory')
        self.__historicalVolume = kwargs.get('historicalVolume')
        self.__esNumericPercentile = kwargs.get('esNumericPercentile')
        self.__strikePrice = kwargs.get('strikePrice')
        self.__calSpreadMisPricing = kwargs.get('calSpreadMisPricing')
        self.__equityGamma = kwargs.get('equityGamma')
        self.__grossIncome = kwargs.get('grossIncome')
        self.__emId = kwargs.get('emId')
        self.__adjustedOpenPrice = kwargs.get('adjustedOpenPrice')
        self.__assetCountInModel = kwargs.get('assetCountInModel')
        self.__stsCreditRegion = kwargs.get('stsCreditRegion')
        self.__point = kwargs.get('point')
        self.__lender = kwargs.get('lender')
        self.__minTemperature = kwargs.get('minTemperature')
        self.__value = kwargs.get('value')
        self.__relativeStrike = kwargs.get('relativeStrike')
        self.__amount = kwargs.get('amount')
        self.__quantity = kwargs.get('quantity')
        self.__lendingFundAcct = kwargs.get('lendingFundAcct')
        self.__reportId = kwargs.get('reportId')
        self.__indexWeight = kwargs.get('indexWeight')
        self.__rebate = kwargs.get('rebate')
        self.__trader = kwargs.get('trader')
        self.__factorCategory = kwargs.get('factorCategory')
        self.__impliedVolatility = kwargs.get('impliedVolatility')
        self.__spread = kwargs.get('spread')
        self.__stsRatesMaturity = kwargs.get('stsRatesMaturity')
        self.__equityDelta = kwargs.get('equityDelta')
        self.__grossWeight = kwargs.get('grossWeight')
        self.__listed = kwargs.get('listed')
        self.__tcmCostHorizon6Hour = kwargs.get('tcmCostHorizon6Hour')
        self.__g10Currency = kwargs.get('g10Currency')
        self.__shockStyle = kwargs.get('shockStyle')
        self.__relativePeriod = kwargs.get('relativePeriod')
        self.__isin = kwargs.get('isin')
        self.__methodology = kwargs.get('methodology')

    @property
    def queueClockTimeLabel(self) -> tuple:
        return self.__queueClockTimeLabel

    @queueClockTimeLabel.setter
    def queueClockTimeLabel(self, value: tuple):
        self.__queueClockTimeLabel = value
        self._property_changed('queueClockTimeLabel')        

    @property
    def marketPnl(self) -> dict:
        return self.__marketPnl

    @marketPnl.setter
    def marketPnl(self, value: dict):
        self.__marketPnl = value
        self._property_changed('marketPnl')        

    @property
    def year(self) -> dict:
        return self.__year

    @year.setter
    def year(self, value: dict):
        self.__year = value
        self._property_changed('year')        

    @property
    def sustainAsiaExJapan(self) -> dict:
        return self.__sustainAsiaExJapan

    @sustainAsiaExJapan.setter
    def sustainAsiaExJapan(self, value: dict):
        self.__sustainAsiaExJapan = value
        self._property_changed('sustainAsiaExJapan')        

    @property
    def investmentRate(self) -> dict:
        return self.__investmentRate

    @investmentRate.setter
    def investmentRate(self, value: dict):
        self.__investmentRate = value
        self._property_changed('investmentRate')        

    @property
    def assetClassificationsGicsSubIndustry(self) -> dict:
        return self.__assetClassificationsGicsSubIndustry

    @assetClassificationsGicsSubIndustry.setter
    def assetClassificationsGicsSubIndustry(self, value: dict):
        self.__assetClassificationsGicsSubIndustry = value
        self._property_changed('assetClassificationsGicsSubIndustry')        

    @property
    def bidUnadjusted(self) -> dict:
        return self.__bidUnadjusted

    @bidUnadjusted.setter
    def bidUnadjusted(self, value: dict):
        self.__bidUnadjusted = value
        self._property_changed('bidUnadjusted')        

    @property
    def economicTermsHash(self) -> dict:
        return self.__economicTermsHash

    @economicTermsHash.setter
    def economicTermsHash(self, value: dict):
        self.__economicTermsHash = value
        self._property_changed('economicTermsHash')        

    @property
    def neighbourAssetId(self) -> dict:
        return self.__neighbourAssetId

    @neighbourAssetId.setter
    def neighbourAssetId(self, value: dict):
        self.__neighbourAssetId = value
        self._property_changed('neighbourAssetId')        

    @property
    def simonIntlAssetTags(self) -> dict:
        return self.__simonIntlAssetTags

    @simonIntlAssetTags.setter
    def simonIntlAssetTags(self, value: dict):
        self.__simonIntlAssetTags = value
        self._property_changed('simonIntlAssetTags')        

    @property
    def path(self) -> dict:
        return self.__path

    @path.setter
    def path(self, value: dict):
        self.__path = value
        self._property_changed('path')        

    @property
    def availableInventory(self) -> dict:
        return self.__availableInventory

    @availableInventory.setter
    def availableInventory(self, value: dict):
        self.__availableInventory = value
        self._property_changed('availableInventory')        

    @property
    def clientContact(self) -> dict:
        return self.__clientContact

    @clientContact.setter
    def clientContact(self, value: dict):
        self.__clientContact = value
        self._property_changed('clientContact')        

    @property
    def est1DayCompletePct(self) -> dict:
        return self.__est1DayCompletePct

    @est1DayCompletePct.setter
    def est1DayCompletePct(self, value: dict):
        self.__est1DayCompletePct = value
        self._property_changed('est1DayCompletePct')        

    @property
    def rank(self) -> dict:
        return self.__rank

    @rank.setter
    def rank(self, value: dict):
        self.__rank = value
        self._property_changed('rank')        

    @property
    def dataSetCategory(self) -> dict:
        return self.__dataSetCategory

    @dataSetCategory.setter
    def dataSetCategory(self, value: dict):
        self.__dataSetCategory = value
        self._property_changed('dataSetCategory')        

    @property
    def createdById(self) -> dict:
        return self.__createdById

    @createdById.setter
    def createdById(self, value: dict):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def vehicleType(self) -> dict:
        return self.__vehicleType

    @vehicleType.setter
    def vehicleType(self, value: dict):
        self.__vehicleType = value
        self._property_changed('vehicleType')        

    @property
    def dailyRisk(self) -> dict:
        return self.__dailyRisk

    @dailyRisk.setter
    def dailyRisk(self, value: dict):
        self.__dailyRisk = value
        self._property_changed('dailyRisk')        

    @property
    def bosInBpsLabel(self) -> tuple:
        return self.__bosInBpsLabel

    @bosInBpsLabel.setter
    def bosInBpsLabel(self, value: tuple):
        self.__bosInBpsLabel = value
        self._property_changed('bosInBpsLabel')        

    @property
    def marketDataType(self) -> dict:
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value: dict):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def sentimentScore(self) -> dict:
        return self.__sentimentScore

    @sentimentScore.setter
    def sentimentScore(self, value: dict):
        self.__sentimentScore = value
        self._property_changed('sentimentScore')        

    @property
    def bosInBps(self) -> dict:
        return self.__bosInBps

    @bosInBps.setter
    def bosInBps(self, value: dict):
        self.__bosInBps = value
        self._property_changed('bosInBps')        

    @property
    def pointClass(self) -> dict:
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value: dict):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def fxSpot(self) -> dict:
        return self.__fxSpot

    @fxSpot.setter
    def fxSpot(self, value: dict):
        self.__fxSpot = value
        self._property_changed('fxSpot')        

    @property
    def bidLow(self) -> dict:
        return self.__bidLow

    @bidLow.setter
    def bidLow(self, value: dict):
        self.__bidLow = value
        self._property_changed('bidLow')        

    @property
    def valuePrevious(self) -> dict:
        return self.__valuePrevious

    @valuePrevious.setter
    def valuePrevious(self, value: dict):
        self.__valuePrevious = value
        self._property_changed('valuePrevious')        

    @property
    def fairVarianceVolatility(self) -> dict:
        return self.__fairVarianceVolatility

    @fairVarianceVolatility.setter
    def fairVarianceVolatility(self, value: dict):
        self.__fairVarianceVolatility = value
        self._property_changed('fairVarianceVolatility')        

    @property
    def avgTradeRate(self) -> dict:
        return self.__avgTradeRate

    @avgTradeRate.setter
    def avgTradeRate(self, value: dict):
        self.__avgTradeRate = value
        self._property_changed('avgTradeRate')        

    @property
    def shortLevel(self) -> dict:
        return self.__shortLevel

    @shortLevel.setter
    def shortLevel(self, value: dict):
        self.__shortLevel = value
        self._property_changed('shortLevel')        

    @property
    def hedgeVolatility(self) -> dict:
        return self.__hedgeVolatility

    @hedgeVolatility.setter
    def hedgeVolatility(self, value: dict):
        self.__hedgeVolatility = value
        self._property_changed('hedgeVolatility')        

    @property
    def version(self) -> dict:
        return self.__version

    @version.setter
    def version(self, value: dict):
        self.__version = value
        self._property_changed('version')        

    @property
    def tags(self) -> dict:
        return self.__tags

    @tags.setter
    def tags(self, value: dict):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def underlyingAssetId(self) -> dict:
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value: dict):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        

    @property
    def clientExposure(self) -> dict:
        return self.__clientExposure

    @clientExposure.setter
    def clientExposure(self, value: dict):
        self.__clientExposure = value
        self._property_changed('clientExposure')        

    @property
    def correlation(self) -> dict:
        return self.__correlation

    @correlation.setter
    def correlation(self, value: dict):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def exposure(self) -> dict:
        return self.__exposure

    @exposure.setter
    def exposure(self, value: dict):
        self.__exposure = value
        self._property_changed('exposure')        

    @property
    def gsSustainSubSector(self) -> dict:
        return self.__gsSustainSubSector

    @gsSustainSubSector.setter
    def gsSustainSubSector(self, value: dict):
        self.__gsSustainSubSector = value
        self._property_changed('gsSustainSubSector')        

    @property
    def domain(self) -> dict:
        return self.__domain

    @domain.setter
    def domain(self, value: dict):
        self.__domain = value
        self._property_changed('domain')        

    @property
    def marketDataAsset(self) -> dict:
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value: dict):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def forwardTenor(self) -> dict:
        return self.__forwardTenor

    @forwardTenor.setter
    def forwardTenor(self, value: dict):
        self.__forwardTenor = value
        self._property_changed('forwardTenor')        

    @property
    def unadjustedHigh(self) -> dict:
        return self.__unadjustedHigh

    @unadjustedHigh.setter
    def unadjustedHigh(self, value: dict):
        self.__unadjustedHigh = value
        self._property_changed('unadjustedHigh')        

    @property
    def sourceImportance(self) -> dict:
        return self.__sourceImportance

    @sourceImportance.setter
    def sourceImportance(self, value: dict):
        self.__sourceImportance = value
        self._property_changed('sourceImportance')        

    @property
    def eid(self) -> dict:
        return self.__eid

    @eid.setter
    def eid(self, value: dict):
        self.__eid = value
        self._property_changed('eid')        

    @property
    def jsn(self) -> dict:
        return self.__jsn

    @jsn.setter
    def jsn(self, value: dict):
        self.__jsn = value
        self._property_changed('jsn')        

    @property
    def relativeReturnQtd(self) -> dict:
        return self.__relativeReturnQtd

    @relativeReturnQtd.setter
    def relativeReturnQtd(self, value: dict):
        self.__relativeReturnQtd = value
        self._property_changed('relativeReturnQtd')        

    @property
    def displayName(self) -> dict:
        return self.__displayName

    @displayName.setter
    def displayName(self, value: dict):
        self.__displayName = value
        self._property_changed('displayName')        

    @property
    def minutesToTrade100Pct(self) -> dict:
        return self.__minutesToTrade100Pct

    @minutesToTrade100Pct.setter
    def minutesToTrade100Pct(self, value: dict):
        self.__minutesToTrade100Pct = value
        self._property_changed('minutesToTrade100Pct')        

    @property
    def marketModelId(self) -> dict:
        return self.__marketModelId

    @marketModelId.setter
    def marketModelId(self, value: dict):
        self.__marketModelId = value
        self._property_changed('marketModelId')        

    @property
    def quoteType(self) -> dict:
        return self.__quoteType

    @quoteType.setter
    def quoteType(self, value: dict):
        self.__quoteType = value
        self._property_changed('quoteType')        

    @property
    def tenor(self) -> dict:
        return self.__tenor

    @tenor.setter
    def tenor(self, value: dict):
        self.__tenor = value
        self._property_changed('tenor')        

    @property
    def esPolicyPercentile(self) -> dict:
        return self.__esPolicyPercentile

    @esPolicyPercentile.setter
    def esPolicyPercentile(self, value: dict):
        self.__esPolicyPercentile = value
        self._property_changed('esPolicyPercentile')        

    @property
    def tcmCostParticipationRate75Pct(self) -> dict:
        return self.__tcmCostParticipationRate75Pct

    @tcmCostParticipationRate75Pct.setter
    def tcmCostParticipationRate75Pct(self, value: dict):
        self.__tcmCostParticipationRate75Pct = value
        self._property_changed('tcmCostParticipationRate75Pct')        

    @property
    def close(self) -> dict:
        return self.__close

    @close.setter
    def close(self, value: dict):
        self.__close = value
        self._property_changed('close')        

    @property
    def tcmCostParticipationRate100Pct(self) -> dict:
        return self.__tcmCostParticipationRate100Pct

    @tcmCostParticipationRate100Pct.setter
    def tcmCostParticipationRate100Pct(self, value: dict):
        self.__tcmCostParticipationRate100Pct = value
        self._property_changed('tcmCostParticipationRate100Pct')        

    @property
    def disclaimer(self) -> dict:
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: dict):
        self.__disclaimer = value
        self._property_changed('disclaimer')        

    @property
    def measureIdx(self) -> dict:
        return self.__measureIdx

    @measureIdx.setter
    def measureIdx(self, value: dict):
        self.__measureIdx = value
        self._property_changed('measureIdx')        

    @property
    def a(self) -> dict:
        return self.__a

    @a.setter
    def a(self, value: dict):
        self.__a = value
        self._property_changed('a')        

    @property
    def b(self) -> dict:
        return self.__b

    @b.setter
    def b(self, value: dict):
        self.__b = value
        self._property_changed('b')        

    @property
    def loanFee(self) -> dict:
        return self.__loanFee

    @loanFee.setter
    def loanFee(self, value: dict):
        self.__loanFee = value
        self._property_changed('loanFee')        

    @property
    def c(self) -> dict:
        return self.__c

    @c.setter
    def c(self, value: dict):
        self.__c = value
        self._property_changed('c')        

    @property
    def equityVega(self) -> dict:
        return self.__equityVega

    @equityVega.setter
    def equityVega(self, value: dict):
        self.__equityVega = value
        self._property_changed('equityVega')        

    @property
    def deploymentVersion(self) -> dict:
        return self.__deploymentVersion

    @deploymentVersion.setter
    def deploymentVersion(self, value: dict):
        self.__deploymentVersion = value
        self._property_changed('deploymentVersion')        

    @property
    def fiveDayMove(self) -> dict:
        return self.__fiveDayMove

    @fiveDayMove.setter
    def fiveDayMove(self, value: dict):
        self.__fiveDayMove = value
        self._property_changed('fiveDayMove')        

    @property
    def borrower(self) -> dict:
        return self.__borrower

    @borrower.setter
    def borrower(self, value: dict):
        self.__borrower = value
        self._property_changed('borrower')        

    @property
    def performanceContribution(self) -> dict:
        return self.__performanceContribution

    @performanceContribution.setter
    def performanceContribution(self, value: dict):
        self.__performanceContribution = value
        self._property_changed('performanceContribution')        

    @property
    def targetNotional(self) -> dict:
        return self.__targetNotional

    @targetNotional.setter
    def targetNotional(self, value: dict):
        self.__targetNotional = value
        self._property_changed('targetNotional')        

    @property
    def fillLegId(self) -> dict:
        return self.__fillLegId

    @fillLegId.setter
    def fillLegId(self, value: dict):
        self.__fillLegId = value
        self._property_changed('fillLegId')        

    @property
    def delisted(self) -> dict:
        return self.__delisted

    @delisted.setter
    def delisted(self, value: dict):
        self.__delisted = value
        self._property_changed('delisted')        

    @property
    def rationale(self) -> dict:
        return self.__rationale

    @rationale.setter
    def rationale(self, value: dict):
        self.__rationale = value
        self._property_changed('rationale')        

    @property
    def regionalFocus(self) -> dict:
        return self.__regionalFocus

    @regionalFocus.setter
    def regionalFocus(self, value: dict):
        self.__regionalFocus = value
        self._property_changed('regionalFocus')        

    @property
    def volumePrimary(self) -> dict:
        return self.__volumePrimary

    @volumePrimary.setter
    def volumePrimary(self, value: dict):
        self.__volumePrimary = value
        self._property_changed('volumePrimary')        

    @property
    def series(self) -> dict:
        return self.__series

    @series.setter
    def series(self, value: dict):
        self.__series = value
        self._property_changed('series')        

    @property
    def simonId(self) -> dict:
        return self.__simonId

    @simonId.setter
    def simonId(self, value: dict):
        self.__simonId = value
        self._property_changed('simonId')        

    @property
    def newIdeasQtd(self) -> dict:
        return self.__newIdeasQtd

    @newIdeasQtd.setter
    def newIdeasQtd(self, value: dict):
        self.__newIdeasQtd = value
        self._property_changed('newIdeasQtd')        

    @property
    def adjustedAskPrice(self) -> dict:
        return self.__adjustedAskPrice

    @adjustedAskPrice.setter
    def adjustedAskPrice(self, value: dict):
        self.__adjustedAskPrice = value
        self._property_changed('adjustedAskPrice')        

    @property
    def quarter(self) -> dict:
        return self.__quarter

    @quarter.setter
    def quarter(self, value: dict):
        self.__quarter = value
        self._property_changed('quarter')        

    @property
    def factorUniverse(self) -> dict:
        return self.__factorUniverse

    @factorUniverse.setter
    def factorUniverse(self, value: dict):
        self.__factorUniverse = value
        self._property_changed('factorUniverse')        

    @property
    def eventCategory(self) -> dict:
        return self.__eventCategory

    @eventCategory.setter
    def eventCategory(self, value: dict):
        self.__eventCategory = value
        self._property_changed('eventCategory')        

    @property
    def impliedNormalVolatility(self) -> dict:
        return self.__impliedNormalVolatility

    @impliedNormalVolatility.setter
    def impliedNormalVolatility(self, value: dict):
        self.__impliedNormalVolatility = value
        self._property_changed('impliedNormalVolatility')        

    @property
    def unadjustedOpen(self) -> dict:
        return self.__unadjustedOpen

    @unadjustedOpen.setter
    def unadjustedOpen(self, value: dict):
        self.__unadjustedOpen = value
        self._property_changed('unadjustedOpen')        

    @property
    def arrivalRt(self) -> dict:
        return self.__arrivalRt

    @arrivalRt.setter
    def arrivalRt(self, value: dict):
        self.__arrivalRt = value
        self._property_changed('arrivalRt')        

    @property
    def transactionCost(self) -> dict:
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value: dict):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def servicingCostShortPnl(self) -> dict:
        return self.__servicingCostShortPnl

    @servicingCostShortPnl.setter
    def servicingCostShortPnl(self, value: dict):
        self.__servicingCostShortPnl = value
        self._property_changed('servicingCostShortPnl')        

    @property
    def bidAskSpread(self) -> dict:
        return self.__bidAskSpread

    @bidAskSpread.setter
    def bidAskSpread(self, value: dict):
        self.__bidAskSpread = value
        self._property_changed('bidAskSpread')        

    @property
    def optionType(self) -> dict:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: dict):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def tcmCostHorizon3Hour(self) -> dict:
        return self.__tcmCostHorizon3Hour

    @tcmCostHorizon3Hour.setter
    def tcmCostHorizon3Hour(self, value: dict):
        self.__tcmCostHorizon3Hour = value
        self._property_changed('tcmCostHorizon3Hour')        

    @property
    def clusterDescription(self) -> dict:
        return self.__clusterDescription

    @clusterDescription.setter
    def clusterDescription(self, value: dict):
        self.__clusterDescription = value
        self._property_changed('clusterDescription')        

    @property
    def positionAmount(self) -> dict:
        return self.__positionAmount

    @positionAmount.setter
    def positionAmount(self, value: dict):
        self.__positionAmount = value
        self._property_changed('positionAmount')        

    @property
    def numberOfPositions(self) -> dict:
        return self.__numberOfPositions

    @numberOfPositions.setter
    def numberOfPositions(self, value: dict):
        self.__numberOfPositions = value
        self._property_changed('numberOfPositions')        

    @property
    def windSpeed(self) -> dict:
        return self.__windSpeed

    @windSpeed.setter
    def windSpeed(self, value: dict):
        self.__windSpeed = value
        self._property_changed('windSpeed')        

    @property
    def openUnadjusted(self) -> dict:
        return self.__openUnadjusted

    @openUnadjusted.setter
    def openUnadjusted(self, value: dict):
        self.__openUnadjusted = value
        self._property_changed('openUnadjusted')        

    @property
    def maRank(self) -> dict:
        return self.__maRank

    @maRank.setter
    def maRank(self, value: dict):
        self.__maRank = value
        self._property_changed('maRank')        

    @property
    def askPrice(self) -> dict:
        return self.__askPrice

    @askPrice.setter
    def askPrice(self, value: dict):
        self.__askPrice = value
        self._property_changed('askPrice')        

    @property
    def eventId(self) -> dict:
        return self.__eventId

    @eventId.setter
    def eventId(self, value: dict):
        self.__eventId = value
        self._property_changed('eventId')        

    @property
    def dataProduct(self) -> dict:
        return self.__dataProduct

    @dataProduct.setter
    def dataProduct(self, value: dict):
        self.__dataProduct = value
        self._property_changed('dataProduct')        

    @property
    def sectors(self) -> dict:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: dict):
        self.__sectors = value
        self._property_changed('sectors')        

    @property
    def annualizedTrackingError(self) -> dict:
        return self.__annualizedTrackingError

    @annualizedTrackingError.setter
    def annualizedTrackingError(self, value: dict):
        self.__annualizedTrackingError = value
        self._property_changed('annualizedTrackingError')        

    @property
    def volSwap(self) -> dict:
        return self.__volSwap

    @volSwap.setter
    def volSwap(self, value: dict):
        self.__volSwap = value
        self._property_changed('volSwap')        

    @property
    def annualizedRisk(self) -> dict:
        return self.__annualizedRisk

    @annualizedRisk.setter
    def annualizedRisk(self, value: dict):
        self.__annualizedRisk = value
        self._property_changed('annualizedRisk')        

    @property
    def corporateAction(self) -> dict:
        return self.__corporateAction

    @corporateAction.setter
    def corporateAction(self, value: dict):
        self.__corporateAction = value
        self._property_changed('corporateAction')        

    @property
    def conviction(self) -> dict:
        return self.__conviction

    @conviction.setter
    def conviction(self, value: dict):
        self.__conviction = value
        self._property_changed('conviction')        

    @property
    def grossExposure(self) -> dict:
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value: dict):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def benchmarkMaturity(self) -> dict:
        return self.__benchmarkMaturity

    @benchmarkMaturity.setter
    def benchmarkMaturity(self, value: dict):
        self.__benchmarkMaturity = value
        self._property_changed('benchmarkMaturity')        

    @property
    def volumeComposite(self) -> dict:
        return self.__volumeComposite

    @volumeComposite.setter
    def volumeComposite(self, value: dict):
        self.__volumeComposite = value
        self._property_changed('volumeComposite')        

    @property
    def volume(self) -> dict:
        return self.__volume

    @volume.setter
    def volume(self, value: dict):
        self.__volume = value
        self._property_changed('volume')        

    @property
    def adv(self) -> dict:
        return self.__adv

    @adv.setter
    def adv(self, value: dict):
        self.__adv = value
        self._property_changed('adv')        

    @property
    def stsFxCurrency(self) -> dict:
        return self.__stsFxCurrency

    @stsFxCurrency.setter
    def stsFxCurrency(self, value: dict):
        self.__stsFxCurrency = value
        self._property_changed('stsFxCurrency')        

    @property
    def wpk(self) -> dict:
        return self.__wpk

    @wpk.setter
    def wpk(self, value: dict):
        self.__wpk = value
        self._property_changed('wpk')        

    @property
    def shortConvictionMedium(self) -> dict:
        return self.__shortConvictionMedium

    @shortConvictionMedium.setter
    def shortConvictionMedium(self, value: dict):
        self.__shortConvictionMedium = value
        self._property_changed('shortConvictionMedium')        

    @property
    def bidChange(self) -> dict:
        return self.__bidChange

    @bidChange.setter
    def bidChange(self, value: dict):
        self.__bidChange = value
        self._property_changed('bidChange')        

    @property
    def exchange(self) -> dict:
        return self.__exchange

    @exchange.setter
    def exchange(self, value: dict):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expiration(self) -> dict:
        return self.__expiration

    @expiration.setter
    def expiration(self, value: dict):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def tradePrice(self) -> dict:
        return self.__tradePrice

    @tradePrice.setter
    def tradePrice(self, value: dict):
        self.__tradePrice = value
        self._property_changed('tradePrice')        

    @property
    def esPolicyScore(self) -> dict:
        return self.__esPolicyScore

    @esPolicyScore.setter
    def esPolicyScore(self, value: dict):
        self.__esPolicyScore = value
        self._property_changed('esPolicyScore')        

    @property
    def loanId(self) -> dict:
        return self.__loanId

    @loanId.setter
    def loanId(self, value: dict):
        self.__loanId = value
        self._property_changed('loanId')        

    @property
    def cid(self) -> dict:
        return self.__cid

    @cid.setter
    def cid(self, value: dict):
        self.__cid = value
        self._property_changed('cid')        

    @property
    def liquidityScore(self) -> dict:
        return self.__liquidityScore

    @liquidityScore.setter
    def liquidityScore(self, value: dict):
        self.__liquidityScore = value
        self._property_changed('liquidityScore')        

    @property
    def importance(self) -> dict:
        return self.__importance

    @importance.setter
    def importance(self, value: dict):
        self.__importance = value
        self._property_changed('importance')        

    @property
    def sourceDateSpan(self) -> dict:
        return self.__sourceDateSpan

    @sourceDateSpan.setter
    def sourceDateSpan(self, value: dict):
        self.__sourceDateSpan = value
        self._property_changed('sourceDateSpan')        

    @property
    def assetClassificationsGicsSector(self) -> dict:
        return self.__assetClassificationsGicsSector

    @assetClassificationsGicsSector.setter
    def assetClassificationsGicsSector(self, value: dict):
        self.__assetClassificationsGicsSector = value
        self._property_changed('assetClassificationsGicsSector')        

    @property
    def underlyingDataSetId(self) -> dict:
        return self.__underlyingDataSetId

    @underlyingDataSetId.setter
    def underlyingDataSetId(self, value: dict):
        self.__underlyingDataSetId = value
        self._property_changed('underlyingDataSetId')        

    @property
    def stsAssetName(self) -> dict:
        return self.__stsAssetName

    @stsAssetName.setter
    def stsAssetName(self, value: dict):
        self.__stsAssetName = value
        self._property_changed('stsAssetName')        

    @property
    def closeUnadjusted(self) -> dict:
        return self.__closeUnadjusted

    @closeUnadjusted.setter
    def closeUnadjusted(self, value: dict):
        self.__closeUnadjusted = value
        self._property_changed('closeUnadjusted')        

    @property
    def valueUnit(self) -> dict:
        return self.__valueUnit

    @valueUnit.setter
    def valueUnit(self, value: dict):
        self.__valueUnit = value
        self._property_changed('valueUnit')        

    @property
    def bidHigh(self) -> dict:
        return self.__bidHigh

    @bidHigh.setter
    def bidHigh(self, value: dict):
        self.__bidHigh = value
        self._property_changed('bidHigh')        

    @property
    def adjustedLowPrice(self) -> dict:
        return self.__adjustedLowPrice

    @adjustedLowPrice.setter
    def adjustedLowPrice(self, value: dict):
        self.__adjustedLowPrice = value
        self._property_changed('adjustedLowPrice')        

    @property
    def netExposureClassification(self) -> dict:
        return self.__netExposureClassification

    @netExposureClassification.setter
    def netExposureClassification(self, value: dict):
        self.__netExposureClassification = value
        self._property_changed('netExposureClassification')        

    @property
    def longConvictionLarge(self) -> dict:
        return self.__longConvictionLarge

    @longConvictionLarge.setter
    def longConvictionLarge(self, value: dict):
        self.__longConvictionLarge = value
        self._property_changed('longConvictionLarge')        

    @property
    def fairVariance(self) -> dict:
        return self.__fairVariance

    @fairVariance.setter
    def fairVariance(self, value: dict):
        self.__fairVariance = value
        self._property_changed('fairVariance')        

    @property
    def hitRateWtd(self) -> dict:
        return self.__hitRateWtd

    @hitRateWtd.setter
    def hitRateWtd(self, value: dict):
        self.__hitRateWtd = value
        self._property_changed('hitRateWtd')        

    @property
    def oad(self) -> dict:
        return self.__oad

    @oad.setter
    def oad(self, value: dict):
        self.__oad = value
        self._property_changed('oad')        

    @property
    def bosInBpsDescription(self) -> dict:
        return self.__bosInBpsDescription

    @bosInBpsDescription.setter
    def bosInBpsDescription(self, value: dict):
        self.__bosInBpsDescription = value
        self._property_changed('bosInBpsDescription')        

    @property
    def lowPrice(self) -> dict:
        return self.__lowPrice

    @lowPrice.setter
    def lowPrice(self, value: dict):
        self.__lowPrice = value
        self._property_changed('lowPrice')        

    @property
    def realizedVolatility(self) -> dict:
        return self.__realizedVolatility

    @realizedVolatility.setter
    def realizedVolatility(self, value: dict):
        self.__realizedVolatility = value
        self._property_changed('realizedVolatility')        

    @property
    def rate(self) -> dict:
        return self.__rate

    @rate.setter
    def rate(self, value: dict):
        self.__rate = value
        self._property_changed('rate')        

    @property
    def adv22DayPct(self) -> dict:
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value: dict):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def alpha(self) -> dict:
        return self.__alpha

    @alpha.setter
    def alpha(self, value: dict):
        self.__alpha = value
        self._property_changed('alpha')        

    @property
    def client(self) -> dict:
        return self.__client

    @client.setter
    def client(self, value: dict):
        self.__client = value
        self._property_changed('client')        

    @property
    def company(self) -> dict:
        return self.__company

    @company.setter
    def company(self, value: dict):
        self.__company = value
        self._property_changed('company')        

    @property
    def convictionList(self) -> dict:
        return self.__convictionList

    @convictionList.setter
    def convictionList(self, value: dict):
        self.__convictionList = value
        self._property_changed('convictionList')        

    @property
    def priceRangeInTicksLabel(self) -> tuple:
        return self.__priceRangeInTicksLabel

    @priceRangeInTicksLabel.setter
    def priceRangeInTicksLabel(self, value: tuple):
        self.__priceRangeInTicksLabel = value
        self._property_changed('priceRangeInTicksLabel')        

    @property
    def ticker(self) -> dict:
        return self.__ticker

    @ticker.setter
    def ticker(self, value: dict):
        self.__ticker = value
        self._property_changed('ticker')        

    @property
    def inRiskModel(self) -> dict:
        return self.__inRiskModel

    @inRiskModel.setter
    def inRiskModel(self, value: dict):
        self.__inRiskModel = value
        self._property_changed('inRiskModel')        

    @property
    def tcmCostHorizon1Day(self) -> dict:
        return self.__tcmCostHorizon1Day

    @tcmCostHorizon1Day.setter
    def tcmCostHorizon1Day(self, value: dict):
        self.__tcmCostHorizon1Day = value
        self._property_changed('tcmCostHorizon1Day')        

    @property
    def servicingCostLongPnl(self) -> dict:
        return self.__servicingCostLongPnl

    @servicingCostLongPnl.setter
    def servicingCostLongPnl(self, value: dict):
        self.__servicingCostLongPnl = value
        self._property_changed('servicingCostLongPnl')        

    @property
    def stsRatesCountry(self) -> dict:
        return self.__stsRatesCountry

    @stsRatesCountry.setter
    def stsRatesCountry(self, value: dict):
        self.__stsRatesCountry = value
        self._property_changed('stsRatesCountry')        

    @property
    def meetingNumber(self) -> dict:
        return self.__meetingNumber

    @meetingNumber.setter
    def meetingNumber(self, value: dict):
        self.__meetingNumber = value
        self._property_changed('meetingNumber')        

    @property
    def exchangeId(self) -> dict:
        return self.__exchangeId

    @exchangeId.setter
    def exchangeId(self, value: dict):
        self.__exchangeId = value
        self._property_changed('exchangeId')        

    @property
    def horizon(self) -> dict:
        return self.__horizon

    @horizon.setter
    def horizon(self, value: dict):
        self.__horizon = value
        self._property_changed('horizon')        

    @property
    def tcmCostHorizon20Day(self) -> dict:
        return self.__tcmCostHorizon20Day

    @tcmCostHorizon20Day.setter
    def tcmCostHorizon20Day(self, value: dict):
        self.__tcmCostHorizon20Day = value
        self._property_changed('tcmCostHorizon20Day')        

    @property
    def longLevel(self) -> dict:
        return self.__longLevel

    @longLevel.setter
    def longLevel(self, value: dict):
        self.__longLevel = value
        self._property_changed('longLevel')        

    @property
    def sourceValueForecast(self) -> dict:
        return self.__sourceValueForecast

    @sourceValueForecast.setter
    def sourceValueForecast(self, value: dict):
        self.__sourceValueForecast = value
        self._property_changed('sourceValueForecast')        

    @property
    def shortConvictionLarge(self) -> dict:
        return self.__shortConvictionLarge

    @shortConvictionLarge.setter
    def shortConvictionLarge(self, value: dict):
        self.__shortConvictionLarge = value
        self._property_changed('shortConvictionLarge')        

    @property
    def realm(self) -> dict:
        return self.__realm

    @realm.setter
    def realm(self, value: dict):
        self.__realm = value
        self._property_changed('realm')        

    @property
    def bid(self) -> dict:
        return self.__bid

    @bid.setter
    def bid(self, value: dict):
        self.__bid = value
        self._property_changed('bid')        

    @property
    def dataDescription(self) -> dict:
        return self.__dataDescription

    @dataDescription.setter
    def dataDescription(self, value: dict):
        self.__dataDescription = value
        self._property_changed('dataDescription')        

    @property
    def composite22DayAdv(self) -> dict:
        return self.__composite22DayAdv

    @composite22DayAdv.setter
    def composite22DayAdv(self, value: dict):
        self.__composite22DayAdv = value
        self._property_changed('composite22DayAdv')        

    @property
    def gsn(self) -> dict:
        return self.__gsn

    @gsn.setter
    def gsn(self, value: dict):
        self.__gsn = value
        self._property_changed('gsn')        

    @property
    def isAggressive(self) -> dict:
        return self.__isAggressive

    @isAggressive.setter
    def isAggressive(self, value: dict):
        self.__isAggressive = value
        self._property_changed('isAggressive')        

    @property
    def orderId(self) -> dict:
        return self.__orderId

    @orderId.setter
    def orderId(self, value: dict):
        self.__orderId = value
        self._property_changed('orderId')        

    @property
    def gss(self) -> dict:
        return self.__gss

    @gss.setter
    def gss(self, value: dict):
        self.__gss = value
        self._property_changed('gss')        

    @property
    def percentOfMediandv1m(self) -> dict:
        return self.__percentOfMediandv1m

    @percentOfMediandv1m.setter
    def percentOfMediandv1m(self, value: dict):
        self.__percentOfMediandv1m = value
        self._property_changed('percentOfMediandv1m')        

    @property
    def lendables(self) -> dict:
        return self.__lendables

    @lendables.setter
    def lendables(self, value: dict):
        self.__lendables = value
        self._property_changed('lendables')        

    @property
    def assetClass(self) -> dict:
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: dict):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def gsideid(self) -> dict:
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: dict):
        self.__gsideid = value
        self._property_changed('gsideid')        

    @property
    def bosInTicksLabel(self) -> tuple:
        return self.__bosInTicksLabel

    @bosInTicksLabel.setter
    def bosInTicksLabel(self, value: tuple):
        self.__bosInTicksLabel = value
        self._property_changed('bosInTicksLabel')        

    @property
    def ric(self) -> dict:
        return self.__ric

    @ric.setter
    def ric(self, value: dict):
        self.__ric = value
        self._property_changed('ric')        

    @property
    def positionSourceId(self) -> dict:
        return self.__positionSourceId

    @positionSourceId.setter
    def positionSourceId(self, value: dict):
        self.__positionSourceId = value
        self._property_changed('positionSourceId')        

    @property
    def division(self) -> dict:
        return self.__division

    @division.setter
    def division(self, value: dict):
        self.__division = value
        self._property_changed('division')        

    @property
    def marketCapUSD(self) -> dict:
        return self.__marketCapUSD

    @marketCapUSD.setter
    def marketCapUSD(self, value: dict):
        self.__marketCapUSD = value
        self._property_changed('marketCapUSD')        

    @property
    def deploymentId(self) -> dict:
        return self.__deploymentId

    @deploymentId.setter
    def deploymentId(self, value: dict):
        self.__deploymentId = value
        self._property_changed('deploymentId')        

    @property
    def highPrice(self) -> dict:
        return self.__highPrice

    @highPrice.setter
    def highPrice(self, value: dict):
        self.__highPrice = value
        self._property_changed('highPrice')        

    @property
    def shortWeight(self) -> dict:
        return self.__shortWeight

    @shortWeight.setter
    def shortWeight(self, value: dict):
        self.__shortWeight = value
        self._property_changed('shortWeight')        

    @property
    def absoluteShares(self) -> dict:
        return self.__absoluteShares

    @absoluteShares.setter
    def absoluteShares(self, value: dict):
        self.__absoluteShares = value
        self._property_changed('absoluteShares')        

    @property
    def action(self) -> dict:
        return self.__action

    @action.setter
    def action(self, value: dict):
        self.__action = value
        self._property_changed('action')        

    @property
    def model(self) -> dict:
        return self.__model

    @model.setter
    def model(self, value: dict):
        self.__model = value
        self._property_changed('model')        

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self.__id = value
        self._property_changed('id')        

    @property
    def arrivalHaircutVwapNormalized(self) -> dict:
        return self.__arrivalHaircutVwapNormalized

    @arrivalHaircutVwapNormalized.setter
    def arrivalHaircutVwapNormalized(self, value: dict):
        self.__arrivalHaircutVwapNormalized = value
        self._property_changed('arrivalHaircutVwapNormalized')        

    @property
    def queueClockTimeDescription(self) -> dict:
        return self.__queueClockTimeDescription

    @queueClockTimeDescription.setter
    def queueClockTimeDescription(self, value: dict):
        self.__queueClockTimeDescription = value
        self._property_changed('queueClockTimeDescription')        

    @property
    def period(self) -> dict:
        return self.__period

    @period.setter
    def period(self, value: dict):
        self.__period = value
        self._property_changed('period')        

    @property
    def indexCreateSource(self) -> dict:
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value: dict):
        self.__indexCreateSource = value
        self._property_changed('indexCreateSource')        

    @property
    def fiscalQuarter(self) -> dict:
        return self.__fiscalQuarter

    @fiscalQuarter.setter
    def fiscalQuarter(self, value: dict):
        self.__fiscalQuarter = value
        self._property_changed('fiscalQuarter')        

    @property
    def deltaStrike(self) -> dict:
        return self.__deltaStrike

    @deltaStrike.setter
    def deltaStrike(self, value: dict):
        self.__deltaStrike = value
        self._property_changed('deltaStrike')        

    @property
    def marketImpact(self) -> dict:
        return self.__marketImpact

    @marketImpact.setter
    def marketImpact(self, value: dict):
        self.__marketImpact = value
        self._property_changed('marketImpact')        

    @property
    def eventType(self) -> dict:
        return self.__eventType

    @eventType.setter
    def eventType(self, value: dict):
        self.__eventType = value
        self._property_changed('eventType')        

    @property
    def assetCountLong(self) -> dict:
        return self.__assetCountLong

    @assetCountLong.setter
    def assetCountLong(self, value: dict):
        self.__assetCountLong = value
        self._property_changed('assetCountLong')        

    @property
    def valueActual(self) -> dict:
        return self.__valueActual

    @valueActual.setter
    def valueActual(self, value: dict):
        self.__valueActual = value
        self._property_changed('valueActual')        

    @property
    def bcid(self) -> dict:
        return self.__bcid

    @bcid.setter
    def bcid(self, value: dict):
        self.__bcid = value
        self._property_changed('bcid')        

    @property
    def originalCountry(self) -> dict:
        return self.__originalCountry

    @originalCountry.setter
    def originalCountry(self, value: dict):
        self.__originalCountry = value
        self._property_changed('originalCountry')        

    @property
    def touchLiquidityScore(self) -> dict:
        return self.__touchLiquidityScore

    @touchLiquidityScore.setter
    def touchLiquidityScore(self, value: dict):
        self.__touchLiquidityScore = value
        self._property_changed('touchLiquidityScore')        

    @property
    def field(self) -> dict:
        return self.__field

    @field.setter
    def field(self, value: dict):
        self.__field = value
        self._property_changed('field')        

    @property
    def spot(self) -> dict:
        return self.__spot

    @spot.setter
    def spot(self, value: dict):
        self.__spot = value
        self._property_changed('spot')        

    @property
    def expectedCompletionDate(self) -> dict:
        return self.__expectedCompletionDate

    @expectedCompletionDate.setter
    def expectedCompletionDate(self, value: dict):
        self.__expectedCompletionDate = value
        self._property_changed('expectedCompletionDate')        

    @property
    def loanValue(self) -> dict:
        return self.__loanValue

    @loanValue.setter
    def loanValue(self, value: dict):
        self.__loanValue = value
        self._property_changed('loanValue')        

    @property
    def skew(self) -> dict:
        return self.__skew

    @skew.setter
    def skew(self, value: dict):
        self.__skew = value
        self._property_changed('skew')        

    @property
    def status(self) -> dict:
        return self.__status

    @status.setter
    def status(self, value: dict):
        self.__status = value
        self._property_changed('status')        

    @property
    def sustainEmergingMarkets(self) -> dict:
        return self.__sustainEmergingMarkets

    @sustainEmergingMarkets.setter
    def sustainEmergingMarkets(self, value: dict):
        self.__sustainEmergingMarkets = value
        self._property_changed('sustainEmergingMarkets')        

    @property
    def totalReturnPrice(self) -> dict:
        return self.__totalReturnPrice

    @totalReturnPrice.setter
    def totalReturnPrice(self, value: dict):
        self.__totalReturnPrice = value
        self._property_changed('totalReturnPrice')        

    @property
    def city(self) -> dict:
        return self.__city

    @city.setter
    def city(self, value: dict):
        self.__city = value
        self._property_changed('city')        

    @property
    def eventSource(self) -> dict:
        return self.__eventSource

    @eventSource.setter
    def eventSource(self, value: dict):
        self.__eventSource = value
        self._property_changed('eventSource')        

    @property
    def qisPermNo(self) -> dict:
        return self.__qisPermNo

    @qisPermNo.setter
    def qisPermNo(self, value: dict):
        self.__qisPermNo = value
        self._property_changed('qisPermNo')        

    @property
    def hitRateYtd(self) -> dict:
        return self.__hitRateYtd

    @hitRateYtd.setter
    def hitRateYtd(self, value: dict):
        self.__hitRateYtd = value
        self._property_changed('hitRateYtd')        

    @property
    def stsCommodity(self) -> dict:
        return self.__stsCommodity

    @stsCommodity.setter
    def stsCommodity(self, value: dict):
        self.__stsCommodity = value
        self._property_changed('stsCommodity')        

    @property
    def stsCommoditySector(self) -> dict:
        return self.__stsCommoditySector

    @stsCommoditySector.setter
    def stsCommoditySector(self, value: dict):
        self.__stsCommoditySector = value
        self._property_changed('stsCommoditySector')        

    @property
    def salesCoverage(self) -> dict:
        return self.__salesCoverage

    @salesCoverage.setter
    def salesCoverage(self, value: dict):
        self.__salesCoverage = value
        self._property_changed('salesCoverage')        

    @property
    def shortExposure(self) -> dict:
        return self.__shortExposure

    @shortExposure.setter
    def shortExposure(self, value: dict):
        self.__shortExposure = value
        self._property_changed('shortExposure')        

    @property
    def esScore(self) -> dict:
        return self.__esScore

    @esScore.setter
    def esScore(self, value: dict):
        self.__esScore = value
        self._property_changed('esScore')        

    @property
    def tcmCostParticipationRate10Pct(self) -> dict:
        return self.__tcmCostParticipationRate10Pct

    @tcmCostParticipationRate10Pct.setter
    def tcmCostParticipationRate10Pct(self, value: dict):
        self.__tcmCostParticipationRate10Pct = value
        self._property_changed('tcmCostParticipationRate10Pct')        

    @property
    def eventTime(self) -> dict:
        return self.__eventTime

    @eventTime.setter
    def eventTime(self, value: dict):
        self.__eventTime = value
        self._property_changed('eventTime')        

    @property
    def positionSourceName(self) -> dict:
        return self.__positionSourceName

    @positionSourceName.setter
    def positionSourceName(self, value: dict):
        self.__positionSourceName = value
        self._property_changed('positionSourceName')        

    @property
    def priceRangeInTicks(self) -> dict:
        return self.__priceRangeInTicks

    @priceRangeInTicks.setter
    def priceRangeInTicks(self, value: dict):
        self.__priceRangeInTicks = value
        self._property_changed('priceRangeInTicks')        

    @property
    def arrivalHaircutVwap(self) -> dict:
        return self.__arrivalHaircutVwap

    @arrivalHaircutVwap.setter
    def arrivalHaircutVwap(self, value: dict):
        self.__arrivalHaircutVwap = value
        self._property_changed('arrivalHaircutVwap')        

    @property
    def interestRate(self) -> dict:
        return self.__interestRate

    @interestRate.setter
    def interestRate(self, value: dict):
        self.__interestRate = value
        self._property_changed('interestRate')        

    @property
    def executionDays(self) -> dict:
        return self.__executionDays

    @executionDays.setter
    def executionDays(self, value: dict):
        self.__executionDays = value
        self._property_changed('executionDays')        

    @property
    def pctChange(self) -> dict:
        return self.__pctChange

    @pctChange.setter
    def pctChange(self, value: dict):
        self.__pctChange = value
        self._property_changed('pctChange')        

    @property
    def side(self) -> dict:
        return self.__side

    @side.setter
    def side(self, value: dict):
        self.__side = value
        self._property_changed('side')        

    @property
    def numberOfRolls(self) -> dict:
        return self.__numberOfRolls

    @numberOfRolls.setter
    def numberOfRolls(self, value: dict):
        self.__numberOfRolls = value
        self._property_changed('numberOfRolls')        

    @property
    def agentLenderFee(self) -> dict:
        return self.__agentLenderFee

    @agentLenderFee.setter
    def agentLenderFee(self, value: dict):
        self.__agentLenderFee = value
        self._property_changed('agentLenderFee')        

    @property
    def complianceRestrictedStatus(self) -> dict:
        return self.__complianceRestrictedStatus

    @complianceRestrictedStatus.setter
    def complianceRestrictedStatus(self, value: dict):
        self.__complianceRestrictedStatus = value
        self._property_changed('complianceRestrictedStatus')        

    @property
    def forward(self) -> dict:
        return self.__forward

    @forward.setter
    def forward(self, value: dict):
        self.__forward = value
        self._property_changed('forward')        

    @property
    def borrowFee(self) -> dict:
        return self.__borrowFee

    @borrowFee.setter
    def borrowFee(self, value: dict):
        self.__borrowFee = value
        self._property_changed('borrowFee')        

    @property
    def strike(self) -> dict:
        return self.__strike

    @strike.setter
    def strike(self, value: dict):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def loanSpread(self) -> dict:
        return self.__loanSpread

    @loanSpread.setter
    def loanSpread(self, value: dict):
        self.__loanSpread = value
        self._property_changed('loanSpread')        

    @property
    def tcmCostHorizon12Hour(self) -> dict:
        return self.__tcmCostHorizon12Hour

    @tcmCostHorizon12Hour.setter
    def tcmCostHorizon12Hour(self, value: dict):
        self.__tcmCostHorizon12Hour = value
        self._property_changed('tcmCostHorizon12Hour')        

    @property
    def dewPoint(self) -> dict:
        return self.__dewPoint

    @dewPoint.setter
    def dewPoint(self, value: dict):
        self.__dewPoint = value
        self._property_changed('dewPoint')        

    @property
    def researchCommission(self) -> dict:
        return self.__researchCommission

    @researchCommission.setter
    def researchCommission(self, value: dict):
        self.__researchCommission = value
        self._property_changed('researchCommission')        

    @property
    def bbid(self) -> dict:
        return self.__bbid

    @bbid.setter
    def bbid(self, value: dict):
        self.__bbid = value
        self._property_changed('bbid')        

    @property
    def assetClassificationsRiskCountryCode(self) -> dict:
        return self.__assetClassificationsRiskCountryCode

    @assetClassificationsRiskCountryCode.setter
    def assetClassificationsRiskCountryCode(self, value: dict):
        self.__assetClassificationsRiskCountryCode = value
        self._property_changed('assetClassificationsRiskCountryCode')        

    @property
    def eventStatus(self) -> dict:
        return self.__eventStatus

    @eventStatus.setter
    def eventStatus(self, value: dict):
        self.__eventStatus = value
        self._property_changed('eventStatus')        

    @property
    def return_(self) -> dict:
        return self.__return

    @return_.setter
    def return_(self, value: dict):
        self.__return = value
        self._property_changed('return')        

    @property
    def maxTemperature(self) -> dict:
        return self.__maxTemperature

    @maxTemperature.setter
    def maxTemperature(self, value: dict):
        self.__maxTemperature = value
        self._property_changed('maxTemperature')        

    @property
    def acquirerShareholderMeetingDate(self) -> dict:
        return self.__acquirerShareholderMeetingDate

    @acquirerShareholderMeetingDate.setter
    def acquirerShareholderMeetingDate(self, value: dict):
        self.__acquirerShareholderMeetingDate = value
        self._property_changed('acquirerShareholderMeetingDate')        

    @property
    def arrivalMidNormalized(self) -> dict:
        return self.__arrivalMidNormalized

    @arrivalMidNormalized.setter
    def arrivalMidNormalized(self, value: dict):
        self.__arrivalMidNormalized = value
        self._property_changed('arrivalMidNormalized')        

    @property
    def rating(self) -> dict:
        return self.__rating

    @rating.setter
    def rating(self, value: dict):
        self.__rating = value
        self._property_changed('rating')        

    @property
    def arrivalRtNormalized(self) -> dict:
        return self.__arrivalRtNormalized

    @arrivalRtNormalized.setter
    def arrivalRtNormalized(self, value: dict):
        self.__arrivalRtNormalized = value
        self._property_changed('arrivalRtNormalized')        

    @property
    def performanceFee(self) -> dict:
        return self.__performanceFee

    @performanceFee.setter
    def performanceFee(self, value: dict):
        self.__performanceFee = value
        self._property_changed('performanceFee')        

    @property
    def reportType(self) -> dict:
        return self.__reportType

    @reportType.setter
    def reportType(self, value: dict):
        self.__reportType = value
        self._property_changed('reportType')        

    @property
    def sourceURL(self) -> dict:
        return self.__sourceURL

    @sourceURL.setter
    def sourceURL(self, value: dict):
        self.__sourceURL = value
        self._property_changed('sourceURL')        

    @property
    def estimatedReturn(self) -> dict:
        return self.__estimatedReturn

    @estimatedReturn.setter
    def estimatedReturn(self, value: dict):
        self.__estimatedReturn = value
        self._property_changed('estimatedReturn')        

    @property
    def underlyingAssetIds(self) -> dict:
        return self.__underlyingAssetIds

    @underlyingAssetIds.setter
    def underlyingAssetIds(self, value: dict):
        self.__underlyingAssetIds = value
        self._property_changed('underlyingAssetIds')        

    @property
    def high(self) -> dict:
        return self.__high

    @high.setter
    def high(self, value: dict):
        self.__high = value
        self._property_changed('high')        

    @property
    def sourceLastUpdate(self) -> dict:
        return self.__sourceLastUpdate

    @sourceLastUpdate.setter
    def sourceLastUpdate(self, value: dict):
        self.__sourceLastUpdate = value
        self._property_changed('sourceLastUpdate')        

    @property
    def queueInLotsLabel(self) -> tuple:
        return self.__queueInLotsLabel

    @queueInLotsLabel.setter
    def queueInLotsLabel(self, value: tuple):
        self.__queueInLotsLabel = value
        self._property_changed('queueInLotsLabel')        

    @property
    def adv10DayPct(self) -> dict:
        return self.__adv10DayPct

    @adv10DayPct.setter
    def adv10DayPct(self, value: dict):
        self.__adv10DayPct = value
        self._property_changed('adv10DayPct')        

    @property
    def longConvictionMedium(self) -> dict:
        return self.__longConvictionMedium

    @longConvictionMedium.setter
    def longConvictionMedium(self, value: dict):
        self.__longConvictionMedium = value
        self._property_changed('longConvictionMedium')        

    @property
    def eventName(self) -> dict:
        return self.__eventName

    @eventName.setter
    def eventName(self, value: dict):
        self.__eventName = value
        self._property_changed('eventName')        

    @property
    def annualRisk(self) -> dict:
        return self.__annualRisk

    @annualRisk.setter
    def annualRisk(self, value: dict):
        self.__annualRisk = value
        self._property_changed('annualRisk')        

    @property
    def dailyTrackingError(self) -> dict:
        return self.__dailyTrackingError

    @dailyTrackingError.setter
    def dailyTrackingError(self, value: dict):
        self.__dailyTrackingError = value
        self._property_changed('dailyTrackingError')        

    @property
    def unadjustedBid(self) -> dict:
        return self.__unadjustedBid

    @unadjustedBid.setter
    def unadjustedBid(self, value: dict):
        self.__unadjustedBid = value
        self._property_changed('unadjustedBid')        

    @property
    def gsdeer(self) -> dict:
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value: dict):
        self.__gsdeer = value
        self._property_changed('gsdeer')        

    @property
    def marketCap(self) -> dict:
        return self.__marketCap

    @marketCap.setter
    def marketCap(self, value: dict):
        self.__marketCap = value
        self._property_changed('marketCap')        

    @property
    def clusterRegion(self) -> tuple:
        return self.__clusterRegion

    @clusterRegion.setter
    def clusterRegion(self, value: tuple):
        self.__clusterRegion = value
        self._property_changed('clusterRegion')        

    @property
    def bbidEquivalent(self) -> dict:
        return self.__bbidEquivalent

    @bbidEquivalent.setter
    def bbidEquivalent(self, value: dict):
        self.__bbidEquivalent = value
        self._property_changed('bbidEquivalent')        

    @property
    def prevCloseAsk(self) -> dict:
        return self.__prevCloseAsk

    @prevCloseAsk.setter
    def prevCloseAsk(self, value: dict):
        self.__prevCloseAsk = value
        self._property_changed('prevCloseAsk')        

    @property
    def level(self) -> dict:
        return self.__level

    @level.setter
    def level(self, value: dict):
        self.__level = value
        self._property_changed('level')        

    @property
    def valoren(self) -> dict:
        return self.__valoren

    @valoren.setter
    def valoren(self, value: dict):
        self.__valoren = value
        self._property_changed('valoren')        

    @property
    def pressure(self) -> dict:
        return self.__pressure

    @pressure.setter
    def pressure(self, value: dict):
        self.__pressure = value
        self._property_changed('pressure')        

    @property
    def shortDescription(self) -> dict:
        return self.__shortDescription

    @shortDescription.setter
    def shortDescription(self, value: dict):
        self.__shortDescription = value
        self._property_changed('shortDescription')        

    @property
    def basis(self) -> dict:
        return self.__basis

    @basis.setter
    def basis(self, value: dict):
        self.__basis = value
        self._property_changed('basis')        

    @property
    def netWeight(self) -> dict:
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value: dict):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def hedgeId(self) -> dict:
        return self.__hedgeId

    @hedgeId.setter
    def hedgeId(self, value: dict):
        self.__hedgeId = value
        self._property_changed('hedgeId')        

    @property
    def portfolioManagers(self) -> dict:
        return self.__portfolioManagers

    @portfolioManagers.setter
    def portfolioManagers(self, value: dict):
        self.__portfolioManagers = value
        self._property_changed('portfolioManagers')        

    @property
    def assetParametersCommoditySector(self) -> dict:
        return self.__assetParametersCommoditySector

    @assetParametersCommoditySector.setter
    def assetParametersCommoditySector(self, value: dict):
        self.__assetParametersCommoditySector = value
        self._property_changed('assetParametersCommoditySector')        

    @property
    def bosInTicks(self) -> dict:
        return self.__bosInTicks

    @bosInTicks.setter
    def bosInTicks(self, value: dict):
        self.__bosInTicks = value
        self._property_changed('bosInTicks')        

    @property
    def tcmCostHorizon8Day(self) -> dict:
        return self.__tcmCostHorizon8Day

    @tcmCostHorizon8Day.setter
    def tcmCostHorizon8Day(self, value: dict):
        self.__tcmCostHorizon8Day = value
        self._property_changed('tcmCostHorizon8Day')        

    @property
    def supraStrategy(self) -> dict:
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value: dict):
        self.__supraStrategy = value
        self._property_changed('supraStrategy')        

    @property
    def adv5DayPct(self) -> dict:
        return self.__adv5DayPct

    @adv5DayPct.setter
    def adv5DayPct(self, value: dict):
        self.__adv5DayPct = value
        self._property_changed('adv5DayPct')        

    @property
    def factorSource(self) -> dict:
        return self.__factorSource

    @factorSource.setter
    def factorSource(self, value: dict):
        self.__factorSource = value
        self._property_changed('factorSource')        

    @property
    def leverage(self) -> dict:
        return self.__leverage

    @leverage.setter
    def leverage(self, value: dict):
        self.__leverage = value
        self._property_changed('leverage')        

    @property
    def submitter(self) -> dict:
        return self.__submitter

    @submitter.setter
    def submitter(self, value: dict):
        self.__submitter = value
        self._property_changed('submitter')        

    @property
    def notional(self) -> dict:
        return self.__notional

    @notional.setter
    def notional(self, value: dict):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def esDisclosurePercentage(self) -> dict:
        return self.__esDisclosurePercentage

    @esDisclosurePercentage.setter
    def esDisclosurePercentage(self, value: dict):
        self.__esDisclosurePercentage = value
        self._property_changed('esDisclosurePercentage')        

    @property
    def clientShortName(self) -> dict:
        return self.__clientShortName

    @clientShortName.setter
    def clientShortName(self, value: dict):
        self.__clientShortName = value
        self._property_changed('clientShortName')        

    @property
    def fwdPoints(self) -> dict:
        return self.__fwdPoints

    @fwdPoints.setter
    def fwdPoints(self, value: dict):
        self.__fwdPoints = value
        self._property_changed('fwdPoints')        

    @property
    def groupCategory(self) -> dict:
        return self.__groupCategory

    @groupCategory.setter
    def groupCategory(self, value: dict):
        self.__groupCategory = value
        self._property_changed('groupCategory')        

    @property
    def kpiId(self) -> dict:
        return self.__kpiId

    @kpiId.setter
    def kpiId(self, value: dict):
        self.__kpiId = value
        self._property_changed('kpiId')        

    @property
    def relativeReturnWtd(self) -> dict:
        return self.__relativeReturnWtd

    @relativeReturnWtd.setter
    def relativeReturnWtd(self, value: dict):
        self.__relativeReturnWtd = value
        self._property_changed('relativeReturnWtd')        

    @property
    def bidPlusAsk(self) -> dict:
        return self.__bidPlusAsk

    @bidPlusAsk.setter
    def bidPlusAsk(self, value: dict):
        self.__bidPlusAsk = value
        self._property_changed('bidPlusAsk')        

    @property
    def assetClassificationsRiskCountryName(self) -> dict:
        return self.__assetClassificationsRiskCountryName

    @assetClassificationsRiskCountryName.setter
    def assetClassificationsRiskCountryName(self, value: dict):
        self.__assetClassificationsRiskCountryName = value
        self._property_changed('assetClassificationsRiskCountryName')        

    @property
    def total(self) -> dict:
        return self.__total

    @total.setter
    def total(self, value: dict):
        self.__total = value
        self._property_changed('total')        

    @property
    def riskModel(self) -> dict:
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value: dict):
        self.__riskModel = value
        self._property_changed('riskModel')        

    @property
    def assetId(self) -> dict:
        return self.__assetId

    @assetId.setter
    def assetId(self, value: dict):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def fairValue(self) -> dict:
        return self.__fairValue

    @fairValue.setter
    def fairValue(self, value: dict):
        self.__fairValue = value
        self._property_changed('fairValue')        

    @property
    def adjustedHighPrice(self) -> dict:
        return self.__adjustedHighPrice

    @adjustedHighPrice.setter
    def adjustedHighPrice(self, value: dict):
        self.__adjustedHighPrice = value
        self._property_changed('adjustedHighPrice')        

    @property
    def beta(self) -> dict:
        return self.__beta

    @beta.setter
    def beta(self, value: dict):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def direction(self) -> dict:
        return self.__direction

    @direction.setter
    def direction(self, value: dict):
        self.__direction = value
        self._property_changed('direction')        

    @property
    def valueForecast(self) -> dict:
        return self.__valueForecast

    @valueForecast.setter
    def valueForecast(self, value: dict):
        self.__valueForecast = value
        self._property_changed('valueForecast')        

    @property
    def longExposure(self) -> dict:
        return self.__longExposure

    @longExposure.setter
    def longExposure(self, value: dict):
        self.__longExposure = value
        self._property_changed('longExposure')        

    @property
    def positionSourceType(self) -> dict:
        return self.__positionSourceType

    @positionSourceType.setter
    def positionSourceType(self, value: dict):
        self.__positionSourceType = value
        self._property_changed('positionSourceType')        

    @property
    def tcmCostParticipationRate20Pct(self) -> dict:
        return self.__tcmCostParticipationRate20Pct

    @tcmCostParticipationRate20Pct.setter
    def tcmCostParticipationRate20Pct(self, value: dict):
        self.__tcmCostParticipationRate20Pct = value
        self._property_changed('tcmCostParticipationRate20Pct')        

    @property
    def adjustedClosePrice(self) -> dict:
        return self.__adjustedClosePrice

    @adjustedClosePrice.setter
    def adjustedClosePrice(self, value: dict):
        self.__adjustedClosePrice = value
        self._property_changed('adjustedClosePrice')        

    @property
    def cross(self) -> dict:
        return self.__cross

    @cross.setter
    def cross(self, value: dict):
        self.__cross = value
        self._property_changed('cross')        

    @property
    def lmsId(self) -> dict:
        return self.__lmsId

    @lmsId.setter
    def lmsId(self, value: dict):
        self.__lmsId = value
        self._property_changed('lmsId')        

    @property
    def rebateRate(self) -> dict:
        return self.__rebateRate

    @rebateRate.setter
    def rebateRate(self, value: dict):
        self.__rebateRate = value
        self._property_changed('rebateRate')        

    @property
    def ideaStatus(self) -> dict:
        return self.__ideaStatus

    @ideaStatus.setter
    def ideaStatus(self, value: dict):
        self.__ideaStatus = value
        self._property_changed('ideaStatus')        

    @property
    def participationRate(self) -> dict:
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value: dict):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def obfr(self) -> dict:
        return self.__obfr

    @obfr.setter
    def obfr(self, value: dict):
        self.__obfr = value
        self._property_changed('obfr')        

    @property
    def fxForecast(self) -> dict:
        return self.__fxForecast

    @fxForecast.setter
    def fxForecast(self, value: dict):
        self.__fxForecast = value
        self._property_changed('fxForecast')        

    @property
    def fixingTimeLabel(self) -> dict:
        return self.__fixingTimeLabel

    @fixingTimeLabel.setter
    def fixingTimeLabel(self, value: dict):
        self.__fixingTimeLabel = value
        self._property_changed('fixingTimeLabel')        

    @property
    def fillId(self) -> dict:
        return self.__fillId

    @fillId.setter
    def fillId(self, value: dict):
        self.__fillId = value
        self._property_changed('fillId')        

    @property
    def esNumericScore(self) -> dict:
        return self.__esNumericScore

    @esNumericScore.setter
    def esNumericScore(self, value: dict):
        self.__esNumericScore = value
        self._property_changed('esNumericScore')        

    @property
    def inBenchmark(self) -> dict:
        return self.__inBenchmark

    @inBenchmark.setter
    def inBenchmark(self, value: dict):
        self.__inBenchmark = value
        self._property_changed('inBenchmark')        

    @property
    def strategy(self) -> dict:
        return self.__strategy

    @strategy.setter
    def strategy(self, value: dict):
        self.__strategy = value
        self._property_changed('strategy')        

    @property
    def shortInterest(self) -> dict:
        return self.__shortInterest

    @shortInterest.setter
    def shortInterest(self, value: dict):
        self.__shortInterest = value
        self._property_changed('shortInterest')        

    @property
    def referencePeriod(self) -> dict:
        return self.__referencePeriod

    @referencePeriod.setter
    def referencePeriod(self, value: dict):
        self.__referencePeriod = value
        self._property_changed('referencePeriod')        

    @property
    def adjustedVolume(self) -> dict:
        return self.__adjustedVolume

    @adjustedVolume.setter
    def adjustedVolume(self, value: dict):
        self.__adjustedVolume = value
        self._property_changed('adjustedVolume')        

    @property
    def queueInLotsDescription(self) -> dict:
        return self.__queueInLotsDescription

    @queueInLotsDescription.setter
    def queueInLotsDescription(self, value: dict):
        self.__queueInLotsDescription = value
        self._property_changed('queueInLotsDescription')        

    @property
    def pbClientId(self) -> dict:
        return self.__pbClientId

    @pbClientId.setter
    def pbClientId(self, value: dict):
        self.__pbClientId = value
        self._property_changed('pbClientId')        

    @property
    def ownerId(self) -> dict:
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: dict):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def secDB(self) -> dict:
        return self.__secDB

    @secDB.setter
    def secDB(self, value: dict):
        self.__secDB = value
        self._property_changed('secDB')        

    @property
    def composite10DayAdv(self) -> dict:
        return self.__composite10DayAdv

    @composite10DayAdv.setter
    def composite10DayAdv(self, value: dict):
        self.__composite10DayAdv = value
        self._property_changed('composite10DayAdv')        

    @property
    def objective(self) -> dict:
        return self.__objective

    @objective.setter
    def objective(self, value: dict):
        self.__objective = value
        self._property_changed('objective')        

    @property
    def navPrice(self) -> dict:
        return self.__navPrice

    @navPrice.setter
    def navPrice(self, value: dict):
        self.__navPrice = value
        self._property_changed('navPrice')        

    @property
    def ideaActivityType(self) -> dict:
        return self.__ideaActivityType

    @ideaActivityType.setter
    def ideaActivityType(self, value: dict):
        self.__ideaActivityType = value
        self._property_changed('ideaActivityType')        

    @property
    def precipitation(self) -> dict:
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value: dict):
        self.__precipitation = value
        self._property_changed('precipitation')        

    @property
    def ideaSource(self) -> dict:
        return self.__ideaSource

    @ideaSource.setter
    def ideaSource(self, value: dict):
        self.__ideaSource = value
        self._property_changed('ideaSource')        

    @property
    def hedgeNotional(self) -> dict:
        return self.__hedgeNotional

    @hedgeNotional.setter
    def hedgeNotional(self, value: dict):
        self.__hedgeNotional = value
        self._property_changed('hedgeNotional')        

    @property
    def askLow(self) -> dict:
        return self.__askLow

    @askLow.setter
    def askLow(self, value: dict):
        self.__askLow = value
        self._property_changed('askLow')        

    @property
    def unadjustedAsk(self) -> dict:
        return self.__unadjustedAsk

    @unadjustedAsk.setter
    def unadjustedAsk(self, value: dict):
        self.__unadjustedAsk = value
        self._property_changed('unadjustedAsk')        

    @property
    def betaAdjustedNetExposure(self) -> dict:
        return self.__betaAdjustedNetExposure

    @betaAdjustedNetExposure.setter
    def betaAdjustedNetExposure(self, value: dict):
        self.__betaAdjustedNetExposure = value
        self._property_changed('betaAdjustedNetExposure')        

    @property
    def expiry(self) -> dict:
        return self.__expiry

    @expiry.setter
    def expiry(self, value: dict):
        self.__expiry = value
        self._property_changed('expiry')        

    @property
    def tradingPnl(self) -> dict:
        return self.__tradingPnl

    @tradingPnl.setter
    def tradingPnl(self, value: dict):
        self.__tradingPnl = value
        self._property_changed('tradingPnl')        

    @property
    def strikePercentage(self) -> dict:
        return self.__strikePercentage

    @strikePercentage.setter
    def strikePercentage(self, value: dict):
        self.__strikePercentage = value
        self._property_changed('strikePercentage')        

    @property
    def excessReturnPrice(self) -> dict:
        return self.__excessReturnPrice

    @excessReturnPrice.setter
    def excessReturnPrice(self, value: dict):
        self.__excessReturnPrice = value
        self._property_changed('excessReturnPrice')        

    @property
    def givenPlusPaid(self) -> dict:
        return self.__givenPlusPaid

    @givenPlusPaid.setter
    def givenPlusPaid(self, value: dict):
        self.__givenPlusPaid = value
        self._property_changed('givenPlusPaid')        

    @property
    def shortConvictionSmall(self) -> dict:
        return self.__shortConvictionSmall

    @shortConvictionSmall.setter
    def shortConvictionSmall(self, value: dict):
        self.__shortConvictionSmall = value
        self._property_changed('shortConvictionSmall')        

    @property
    def prevCloseBid(self) -> dict:
        return self.__prevCloseBid

    @prevCloseBid.setter
    def prevCloseBid(self, value: dict):
        self.__prevCloseBid = value
        self._property_changed('prevCloseBid')        

    @property
    def fxPnl(self) -> dict:
        return self.__fxPnl

    @fxPnl.setter
    def fxPnl(self, value: dict):
        self.__fxPnl = value
        self._property_changed('fxPnl')        

    @property
    def forecast(self) -> dict:
        return self.__forecast

    @forecast.setter
    def forecast(self, value: dict):
        self.__forecast = value
        self._property_changed('forecast')        

    @property
    def tcmCostHorizon16Day(self) -> dict:
        return self.__tcmCostHorizon16Day

    @tcmCostHorizon16Day.setter
    def tcmCostHorizon16Day(self, value: dict):
        self.__tcmCostHorizon16Day = value
        self._property_changed('tcmCostHorizon16Day')        

    @property
    def pnl(self) -> dict:
        return self.__pnl

    @pnl.setter
    def pnl(self, value: dict):
        self.__pnl = value
        self._property_changed('pnl')        

    @property
    def assetClassificationsGicsIndustryGroup(self) -> dict:
        return self.__assetClassificationsGicsIndustryGroup

    @assetClassificationsGicsIndustryGroup.setter
    def assetClassificationsGicsIndustryGroup(self, value: dict):
        self.__assetClassificationsGicsIndustryGroup = value
        self._property_changed('assetClassificationsGicsIndustryGroup')        

    @property
    def unadjustedClose(self) -> dict:
        return self.__unadjustedClose

    @unadjustedClose.setter
    def unadjustedClose(self, value: dict):
        self.__unadjustedClose = value
        self._property_changed('unadjustedClose')        

    @property
    def tcmCostHorizon4Day(self) -> dict:
        return self.__tcmCostHorizon4Day

    @tcmCostHorizon4Day.setter
    def tcmCostHorizon4Day(self, value: dict):
        self.__tcmCostHorizon4Day = value
        self._property_changed('tcmCostHorizon4Day')        

    @property
    def assetClassificationsIsPrimary(self) -> dict:
        return self.__assetClassificationsIsPrimary

    @assetClassificationsIsPrimary.setter
    def assetClassificationsIsPrimary(self, value: dict):
        self.__assetClassificationsIsPrimary = value
        self._property_changed('assetClassificationsIsPrimary')        

    @property
    def styles(self) -> dict:
        return self.__styles

    @styles.setter
    def styles(self, value: dict):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def lendingSecId(self) -> dict:
        return self.__lendingSecId

    @lendingSecId.setter
    def lendingSecId(self, value: dict):
        self.__lendingSecId = value
        self._property_changed('lendingSecId')        

    @property
    def shortName(self) -> dict:
        return self.__shortName

    @shortName.setter
    def shortName(self, value: dict):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def equityTheta(self) -> dict:
        return self.__equityTheta

    @equityTheta.setter
    def equityTheta(self, value: dict):
        self.__equityTheta = value
        self._property_changed('equityTheta')        

    @property
    def averageFillPrice(self) -> dict:
        return self.__averageFillPrice

    @averageFillPrice.setter
    def averageFillPrice(self, value: dict):
        self.__averageFillPrice = value
        self._property_changed('averageFillPrice')        

    @property
    def snowfall(self) -> dict:
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value: dict):
        self.__snowfall = value
        self._property_changed('snowfall')        

    @property
    def mic(self) -> dict:
        return self.__mic

    @mic.setter
    def mic(self, value: dict):
        self.__mic = value
        self._property_changed('mic')        

    @property
    def openPrice(self) -> dict:
        return self.__openPrice

    @openPrice.setter
    def openPrice(self, value: dict):
        self.__openPrice = value
        self._property_changed('openPrice')        

    @property
    def autoExecState(self) -> dict:
        return self.__autoExecState

    @autoExecState.setter
    def autoExecState(self, value: dict):
        self.__autoExecState = value
        self._property_changed('autoExecState')        

    @property
    def depthSpreadScore(self) -> dict:
        return self.__depthSpreadScore

    @depthSpreadScore.setter
    def depthSpreadScore(self, value: dict):
        self.__depthSpreadScore = value
        self._property_changed('depthSpreadScore')        

    @property
    def relativeReturnYtd(self) -> dict:
        return self.__relativeReturnYtd

    @relativeReturnYtd.setter
    def relativeReturnYtd(self, value: dict):
        self.__relativeReturnYtd = value
        self._property_changed('relativeReturnYtd')        

    @property
    def long(self) -> dict:
        return self.__long

    @long.setter
    def long(self, value: dict):
        self.__long = value
        self._property_changed('long')        

    @property
    def fairVolatility(self) -> dict:
        return self.__fairVolatility

    @fairVolatility.setter
    def fairVolatility(self, value: dict):
        self.__fairVolatility = value
        self._property_changed('fairVolatility')        

    @property
    def dollarCross(self) -> dict:
        return self.__dollarCross

    @dollarCross.setter
    def dollarCross(self, value: dict):
        self.__dollarCross = value
        self._property_changed('dollarCross')        

    @property
    def longWeight(self) -> dict:
        return self.__longWeight

    @longWeight.setter
    def longWeight(self, value: dict):
        self.__longWeight = value
        self._property_changed('longWeight')        

    @property
    def vendor(self) -> dict:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: dict):
        self.__vendor = value
        self._property_changed('vendor')        

    @property
    def currency(self) -> dict:
        return self.__currency

    @currency.setter
    def currency(self, value: dict):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def clusterClass(self) -> dict:
        return self.__clusterClass

    @clusterClass.setter
    def clusterClass(self, value: dict):
        self.__clusterClass = value
        self._property_changed('clusterClass')        

    @property
    def financialReturnsScore(self) -> dict:
        return self.__financialReturnsScore

    @financialReturnsScore.setter
    def financialReturnsScore(self, value: dict):
        self.__financialReturnsScore = value
        self._property_changed('financialReturnsScore')        

    @property
    def netChange(self) -> dict:
        return self.__netChange

    @netChange.setter
    def netChange(self, value: dict):
        self.__netChange = value
        self._property_changed('netChange')        

    @property
    def nonSymbolDimensions(self) -> dict:
        return self.__nonSymbolDimensions

    @nonSymbolDimensions.setter
    def nonSymbolDimensions(self, value: dict):
        self.__nonSymbolDimensions = value
        self._property_changed('nonSymbolDimensions')        

    @property
    def bidSize(self) -> dict:
        return self.__bidSize

    @bidSize.setter
    def bidSize(self, value: dict):
        self.__bidSize = value
        self._property_changed('bidSize')        

    @property
    def arrivalMid(self) -> dict:
        return self.__arrivalMid

    @arrivalMid.setter
    def arrivalMid(self, value: dict):
        self.__arrivalMid = value
        self._property_changed('arrivalMid')        

    @property
    def assetParametersExchangeCurrency(self) -> dict:
        return self.__assetParametersExchangeCurrency

    @assetParametersExchangeCurrency.setter
    def assetParametersExchangeCurrency(self, value: dict):
        self.__assetParametersExchangeCurrency = value
        self._property_changed('assetParametersExchangeCurrency')        

    @property
    def unexplained(self) -> dict:
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value: dict):
        self.__unexplained = value
        self._property_changed('unexplained')        

    @property
    def assetClassificationsCountryName(self) -> dict:
        return self.__assetClassificationsCountryName

    @assetClassificationsCountryName.setter
    def assetClassificationsCountryName(self, value: dict):
        self.__assetClassificationsCountryName = value
        self._property_changed('assetClassificationsCountryName')        

    @property
    def metric(self) -> dict:
        return self.__metric

    @metric.setter
    def metric(self, value: dict):
        self.__metric = value
        self._property_changed('metric')        

    @property
    def newIdeasYtd(self) -> dict:
        return self.__newIdeasYtd

    @newIdeasYtd.setter
    def newIdeasYtd(self, value: dict):
        self.__newIdeasYtd = value
        self._property_changed('newIdeasYtd')        

    @property
    def managementFee(self) -> dict:
        return self.__managementFee

    @managementFee.setter
    def managementFee(self, value: dict):
        self.__managementFee = value
        self._property_changed('managementFee')        

    @property
    def ask(self) -> dict:
        return self.__ask

    @ask.setter
    def ask(self, value: dict):
        self.__ask = value
        self._property_changed('ask')        

    @property
    def impliedLognormalVolatility(self) -> dict:
        return self.__impliedLognormalVolatility

    @impliedLognormalVolatility.setter
    def impliedLognormalVolatility(self, value: dict):
        self.__impliedLognormalVolatility = value
        self._property_changed('impliedLognormalVolatility')        

    @property
    def closePrice(self) -> dict:
        return self.__closePrice

    @closePrice.setter
    def closePrice(self, value: dict):
        self.__closePrice = value
        self._property_changed('closePrice')        

    @property
    def open(self) -> dict:
        return self.__open

    @open.setter
    def open(self, value: dict):
        self.__open = value
        self._property_changed('open')        

    @property
    def sourceId(self) -> dict:
        return self.__sourceId

    @sourceId.setter
    def sourceId(self, value: dict):
        self.__sourceId = value
        self._property_changed('sourceId')        

    @property
    def country(self) -> dict:
        return self.__country

    @country.setter
    def country(self, value: dict):
        self.__country = value
        self._property_changed('country')        

    @property
    def cusip(self) -> dict:
        return self.__cusip

    @cusip.setter
    def cusip(self, value: dict):
        self.__cusip = value
        self._property_changed('cusip')        

    @property
    def touchSpreadScore(self) -> dict:
        return self.__touchSpreadScore

    @touchSpreadScore.setter
    def touchSpreadScore(self, value: dict):
        self.__touchSpreadScore = value
        self._property_changed('touchSpreadScore')        

    @property
    def absoluteStrike(self) -> dict:
        return self.__absoluteStrike

    @absoluteStrike.setter
    def absoluteStrike(self, value: dict):
        self.__absoluteStrike = value
        self._property_changed('absoluteStrike')        

    @property
    def netExposure(self) -> dict:
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: dict):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def source(self) -> dict:
        return self.__source

    @source.setter
    def source(self, value: dict):
        self.__source = value
        self._property_changed('source')        

    @property
    def assetClassificationsCountryCode(self) -> dict:
        return self.__assetClassificationsCountryCode

    @assetClassificationsCountryCode.setter
    def assetClassificationsCountryCode(self, value: dict):
        self.__assetClassificationsCountryCode = value
        self._property_changed('assetClassificationsCountryCode')        

    @property
    def frequency(self) -> dict:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: dict):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def activityId(self) -> dict:
        return self.__activityId

    @activityId.setter
    def activityId(self, value: dict):
        self.__activityId = value
        self._property_changed('activityId')        

    @property
    def estimatedImpact(self) -> dict:
        return self.__estimatedImpact

    @estimatedImpact.setter
    def estimatedImpact(self, value: dict):
        self.__estimatedImpact = value
        self._property_changed('estimatedImpact')        

    @property
    def dataSetSubCategory(self) -> dict:
        return self.__dataSetSubCategory

    @dataSetSubCategory.setter
    def dataSetSubCategory(self, value: dict):
        self.__dataSetSubCategory = value
        self._property_changed('dataSetSubCategory')        

    @property
    def assetParametersPricingLocation(self) -> dict:
        return self.__assetParametersPricingLocation

    @assetParametersPricingLocation.setter
    def assetParametersPricingLocation(self, value: dict):
        self.__assetParametersPricingLocation = value
        self._property_changed('assetParametersPricingLocation')        

    @property
    def eventDescription(self) -> dict:
        return self.__eventDescription

    @eventDescription.setter
    def eventDescription(self, value: dict):
        self.__eventDescription = value
        self._property_changed('eventDescription')        

    @property
    def strikeReference(self) -> dict:
        return self.__strikeReference

    @strikeReference.setter
    def strikeReference(self, value: dict):
        self.__strikeReference = value
        self._property_changed('strikeReference')        

    @property
    def details(self) -> dict:
        return self.__details

    @details.setter
    def details(self, value: dict):
        self.__details = value
        self._property_changed('details')        

    @property
    def assetCount(self) -> dict:
        return self.__assetCount

    @assetCount.setter
    def assetCount(self, value: dict):
        self.__assetCount = value
        self._property_changed('assetCount')        

    @property
    def given(self) -> dict:
        return self.__given

    @given.setter
    def given(self, value: dict):
        self.__given = value
        self._property_changed('given')        

    @property
    def absoluteValue(self) -> dict:
        return self.__absoluteValue

    @absoluteValue.setter
    def absoluteValue(self, value: dict):
        self.__absoluteValue = value
        self._property_changed('absoluteValue')        

    @property
    def delistingDate(self) -> dict:
        return self.__delistingDate

    @delistingDate.setter
    def delistingDate(self, value: dict):
        self.__delistingDate = value
        self._property_changed('delistingDate')        

    @property
    def longTenor(self) -> dict:
        return self.__longTenor

    @longTenor.setter
    def longTenor(self, value: dict):
        self.__longTenor = value
        self._property_changed('longTenor')        

    @property
    def mctr(self) -> dict:
        return self.__mctr

    @mctr.setter
    def mctr(self, value: dict):
        self.__mctr = value
        self._property_changed('mctr')        

    @property
    def weight(self) -> dict:
        return self.__weight

    @weight.setter
    def weight(self, value: dict):
        self.__weight = value
        self._property_changed('weight')        

    @property
    def historicalClose(self) -> dict:
        return self.__historicalClose

    @historicalClose.setter
    def historicalClose(self, value: dict):
        self.__historicalClose = value
        self._property_changed('historicalClose')        

    @property
    def assetCountPriced(self) -> dict:
        return self.__assetCountPriced

    @assetCountPriced.setter
    def assetCountPriced(self, value: dict):
        self.__assetCountPriced = value
        self._property_changed('assetCountPriced')        

    @property
    def marketDataPoint(self) -> dict:
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value: dict):
        self.__marketDataPoint = value
        self._property_changed('marketDataPoint')        

    @property
    def ideaId(self) -> dict:
        return self.__ideaId

    @ideaId.setter
    def ideaId(self, value: dict):
        self.__ideaId = value
        self._property_changed('ideaId')        

    @property
    def commentStatus(self) -> dict:
        return self.__commentStatus

    @commentStatus.setter
    def commentStatus(self, value: dict):
        self.__commentStatus = value
        self._property_changed('commentStatus')        

    @property
    def marginalCost(self) -> dict:
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value: dict):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def absoluteWeight(self) -> dict:
        return self.__absoluteWeight

    @absoluteWeight.setter
    def absoluteWeight(self, value: dict):
        self.__absoluteWeight = value
        self._property_changed('absoluteWeight')        

    @property
    def measure(self) -> dict:
        return self.__measure

    @measure.setter
    def measure(self, value: dict):
        self.__measure = value
        self._property_changed('measure')        

    @property
    def clientWeight(self) -> dict:
        return self.__clientWeight

    @clientWeight.setter
    def clientWeight(self, value: dict):
        self.__clientWeight = value
        self._property_changed('clientWeight')        

    @property
    def hedgeAnnualizedVolatility(self) -> dict:
        return self.__hedgeAnnualizedVolatility

    @hedgeAnnualizedVolatility.setter
    def hedgeAnnualizedVolatility(self, value: dict):
        self.__hedgeAnnualizedVolatility = value
        self._property_changed('hedgeAnnualizedVolatility')        

    @property
    def benchmarkCurrency(self) -> dict:
        return self.__benchmarkCurrency

    @benchmarkCurrency.setter
    def benchmarkCurrency(self, value: dict):
        self.__benchmarkCurrency = value
        self._property_changed('benchmarkCurrency')        

    @property
    def name(self) -> dict:
        return self.__name

    @name.setter
    def name(self, value: dict):
        self.__name = value
        self._property_changed('name')        

    @property
    def aum(self) -> dict:
        return self.__aum

    @aum.setter
    def aum(self, value: dict):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def folderName(self) -> dict:
        return self.__folderName

    @folderName.setter
    def folderName(self, value: dict):
        self.__folderName = value
        self._property_changed('folderName')        

    @property
    def lendingPartnerFee(self) -> dict:
        return self.__lendingPartnerFee

    @lendingPartnerFee.setter
    def lendingPartnerFee(self, value: dict):
        self.__lendingPartnerFee = value
        self._property_changed('lendingPartnerFee')        

    @property
    def region(self) -> dict:
        return self.__region

    @region.setter
    def region(self, value: dict):
        self.__region = value
        self._property_changed('region')        

    @property
    def liveDate(self) -> dict:
        return self.__liveDate

    @liveDate.setter
    def liveDate(self, value: dict):
        self.__liveDate = value
        self._property_changed('liveDate')        

    @property
    def askHigh(self) -> dict:
        return self.__askHigh

    @askHigh.setter
    def askHigh(self, value: dict):
        self.__askHigh = value
        self._property_changed('askHigh')        

    @property
    def corporateActionType(self) -> dict:
        return self.__corporateActionType

    @corporateActionType.setter
    def corporateActionType(self, value: dict):
        self.__corporateActionType = value
        self._property_changed('corporateActionType')        

    @property
    def primeId(self) -> dict:
        return self.__primeId

    @primeId.setter
    def primeId(self, value: dict):
        self.__primeId = value
        self._property_changed('primeId')        

    @property
    def tenor2(self) -> dict:
        return self.__tenor2

    @tenor2.setter
    def tenor2(self, value: dict):
        self.__tenor2 = value
        self._property_changed('tenor2')        

    @property
    def description(self) -> dict:
        return self.__description

    @description.setter
    def description(self, value: dict):
        self.__description = value
        self._property_changed('description')        

    @property
    def valueRevised(self) -> dict:
        return self.__valueRevised

    @valueRevised.setter
    def valueRevised(self, value: dict):
        self.__valueRevised = value
        self._property_changed('valueRevised')        

    @property
    def ownerName(self) -> dict:
        return self.__ownerName

    @ownerName.setter
    def ownerName(self, value: dict):
        self.__ownerName = value
        self._property_changed('ownerName')        

    @property
    def adjustedTradePrice(self) -> dict:
        return self.__adjustedTradePrice

    @adjustedTradePrice.setter
    def adjustedTradePrice(self, value: dict):
        self.__adjustedTradePrice = value
        self._property_changed('adjustedTradePrice')        

    @property
    def lastUpdatedById(self) -> dict:
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: dict):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def zScore(self) -> dict:
        return self.__zScore

    @zScore.setter
    def zScore(self, value: dict):
        self.__zScore = value
        self._property_changed('zScore')        

    @property
    def targetShareholderMeetingDate(self) -> dict:
        return self.__targetShareholderMeetingDate

    @targetShareholderMeetingDate.setter
    def targetShareholderMeetingDate(self, value: dict):
        self.__targetShareholderMeetingDate = value
        self._property_changed('targetShareholderMeetingDate')        

    @property
    def isADR(self) -> dict:
        return self.__isADR

    @isADR.setter
    def isADR(self, value: dict):
        self.__isADR = value
        self._property_changed('isADR')        

    @property
    def eventStartTime(self) -> dict:
        return self.__eventStartTime

    @eventStartTime.setter
    def eventStartTime(self, value: dict):
        self.__eventStartTime = value
        self._property_changed('eventStartTime')        

    @property
    def factor(self) -> dict:
        return self.__factor

    @factor.setter
    def factor(self, value: dict):
        self.__factor = value
        self._property_changed('factor')        

    @property
    def longConvictionSmall(self) -> dict:
        return self.__longConvictionSmall

    @longConvictionSmall.setter
    def longConvictionSmall(self, value: dict):
        self.__longConvictionSmall = value
        self._property_changed('longConvictionSmall')        

    @property
    def serviceId(self) -> dict:
        return self.__serviceId

    @serviceId.setter
    def serviceId(self, value: dict):
        self.__serviceId = value
        self._property_changed('serviceId')        

    @property
    def turnover(self) -> dict:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: dict):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def gsfeer(self) -> dict:
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value: dict):
        self.__gsfeer = value
        self._property_changed('gsfeer')        

    @property
    def coverage(self) -> dict:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: dict):
        self.__coverage = value
        self._property_changed('coverage')        

    @property
    def backtestId(self) -> dict:
        return self.__backtestId

    @backtestId.setter
    def backtestId(self, value: dict):
        self.__backtestId = value
        self._property_changed('backtestId')        

    @property
    def gPercentile(self) -> dict:
        return self.__gPercentile

    @gPercentile.setter
    def gPercentile(self, value: dict):
        self.__gPercentile = value
        self._property_changed('gPercentile')        

    @property
    def gScore(self) -> dict:
        return self.__gScore

    @gScore.setter
    def gScore(self, value: dict):
        self.__gScore = value
        self._property_changed('gScore')        

    @property
    def marketValue(self) -> dict:
        return self.__marketValue

    @marketValue.setter
    def marketValue(self, value: dict):
        self.__marketValue = value
        self._property_changed('marketValue')        

    @property
    def multipleScore(self) -> dict:
        return self.__multipleScore

    @multipleScore.setter
    def multipleScore(self, value: dict):
        self.__multipleScore = value
        self._property_changed('multipleScore')        

    @property
    def lendingFundNav(self) -> dict:
        return self.__lendingFundNav

    @lendingFundNav.setter
    def lendingFundNav(self, value: dict):
        self.__lendingFundNav = value
        self._property_changed('lendingFundNav')        

    @property
    def sourceOriginalCategory(self) -> dict:
        return self.__sourceOriginalCategory

    @sourceOriginalCategory.setter
    def sourceOriginalCategory(self, value: dict):
        self.__sourceOriginalCategory = value
        self._property_changed('sourceOriginalCategory')        

    @property
    def betaAdjustedExposure(self) -> dict:
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value: dict):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def composite5DayAdv(self) -> dict:
        return self.__composite5DayAdv

    @composite5DayAdv.setter
    def composite5DayAdv(self, value: dict):
        self.__composite5DayAdv = value
        self._property_changed('composite5DayAdv')        

    @property
    def dividendPoints(self) -> dict:
        return self.__dividendPoints

    @dividendPoints.setter
    def dividendPoints(self, value: dict):
        self.__dividendPoints = value
        self._property_changed('dividendPoints')        

    @property
    def newIdeasWtd(self) -> dict:
        return self.__newIdeasWtd

    @newIdeasWtd.setter
    def newIdeasWtd(self, value: dict):
        self.__newIdeasWtd = value
        self._property_changed('newIdeasWtd')        

    @property
    def paid(self) -> dict:
        return self.__paid

    @paid.setter
    def paid(self, value: dict):
        self.__paid = value
        self._property_changed('paid')        

    @property
    def short(self) -> dict:
        return self.__short

    @short.setter
    def short(self, value: dict):
        self.__short = value
        self._property_changed('short')        

    @property
    def location(self) -> dict:
        return self.__location

    @location.setter
    def location(self, value: dict):
        self.__location = value
        self._property_changed('location')        

    @property
    def comment(self) -> dict:
        return self.__comment

    @comment.setter
    def comment(self, value: dict):
        self.__comment = value
        self._property_changed('comment')        

    @property
    def bosInTicksDescription(self) -> dict:
        return self.__bosInTicksDescription

    @bosInTicksDescription.setter
    def bosInTicksDescription(self, value: dict):
        self.__bosInTicksDescription = value
        self._property_changed('bosInTicksDescription')        

    @property
    def sourceSymbol(self) -> dict:
        return self.__sourceSymbol

    @sourceSymbol.setter
    def sourceSymbol(self, value: dict):
        self.__sourceSymbol = value
        self._property_changed('sourceSymbol')        

    @property
    def scenarioId(self) -> dict:
        return self.__scenarioId

    @scenarioId.setter
    def scenarioId(self, value: dict):
        self.__scenarioId = value
        self._property_changed('scenarioId')        

    @property
    def askUnadjusted(self) -> dict:
        return self.__askUnadjusted

    @askUnadjusted.setter
    def askUnadjusted(self, value: dict):
        self.__askUnadjusted = value
        self._property_changed('askUnadjusted')        

    @property
    def queueClockTime(self) -> dict:
        return self.__queueClockTime

    @queueClockTime.setter
    def queueClockTime(self, value: dict):
        self.__queueClockTime = value
        self._property_changed('queueClockTime')        

    @property
    def askChange(self) -> dict:
        return self.__askChange

    @askChange.setter
    def askChange(self, value: dict):
        self.__askChange = value
        self._property_changed('askChange')        

    @property
    def tcmCostParticipationRate50Pct(self) -> dict:
        return self.__tcmCostParticipationRate50Pct

    @tcmCostParticipationRate50Pct.setter
    def tcmCostParticipationRate50Pct(self, value: dict):
        self.__tcmCostParticipationRate50Pct = value
        self._property_changed('tcmCostParticipationRate50Pct')        

    @property
    def normalizedPerformance(self) -> dict:
        return self.__normalizedPerformance

    @normalizedPerformance.setter
    def normalizedPerformance(self, value: dict):
        self.__normalizedPerformance = value
        self._property_changed('normalizedPerformance')        

    @property
    def cmId(self) -> dict:
        return self.__cmId

    @cmId.setter
    def cmId(self, value: dict):
        self.__cmId = value
        self._property_changed('cmId')        

    @property
    def type(self) -> dict:
        return self.__type

    @type.setter
    def type(self, value: dict):
        self.__type = value
        self._property_changed('type')        

    @property
    def mdapi(self) -> dict:
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: dict):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def dividendYield(self) -> dict:
        return self.__dividendYield

    @dividendYield.setter
    def dividendYield(self, value: dict):
        self.__dividendYield = value
        self._property_changed('dividendYield')        

    @property
    def cumulativePnl(self) -> dict:
        return self.__cumulativePnl

    @cumulativePnl.setter
    def cumulativePnl(self, value: dict):
        self.__cumulativePnl = value
        self._property_changed('cumulativePnl')        

    @property
    def sourceOrigin(self) -> dict:
        return self.__sourceOrigin

    @sourceOrigin.setter
    def sourceOrigin(self, value: dict):
        self.__sourceOrigin = value
        self._property_changed('sourceOrigin')        

    @property
    def shortTenor(self) -> dict:
        return self.__shortTenor

    @shortTenor.setter
    def shortTenor(self, value: dict):
        self.__shortTenor = value
        self._property_changed('shortTenor')        

    @property
    def unadjustedVolume(self) -> dict:
        return self.__unadjustedVolume

    @unadjustedVolume.setter
    def unadjustedVolume(self, value: dict):
        self.__unadjustedVolume = value
        self._property_changed('unadjustedVolume')        

    @property
    def measures(self) -> dict:
        return self.__measures

    @measures.setter
    def measures(self, value: dict):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def tradingCostPnl(self) -> dict:
        return self.__tradingCostPnl

    @tradingCostPnl.setter
    def tradingCostPnl(self, value: dict):
        self.__tradingCostPnl = value
        self._property_changed('tradingCostPnl')        

    @property
    def internalUser(self) -> dict:
        return self.__internalUser

    @internalUser.setter
    def internalUser(self, value: dict):
        self.__internalUser = value
        self._property_changed('internalUser')        

    @property
    def price(self) -> dict:
        return self.__price

    @price.setter
    def price(self, value: dict):
        self.__price = value
        self._property_changed('price')        

    @property
    def paymentQuantity(self) -> dict:
        return self.__paymentQuantity

    @paymentQuantity.setter
    def paymentQuantity(self, value: dict):
        self.__paymentQuantity = value
        self._property_changed('paymentQuantity')        

    @property
    def underlyer(self) -> dict:
        return self.__underlyer

    @underlyer.setter
    def underlyer(self, value: dict):
        self.__underlyer = value
        self._property_changed('underlyer')        

    @property
    def positionIdx(self) -> dict:
        return self.__positionIdx

    @positionIdx.setter
    def positionIdx(self, value: dict):
        self.__positionIdx = value
        self._property_changed('positionIdx')        

    @property
    def secName(self) -> dict:
        return self.__secName

    @secName.setter
    def secName(self, value: dict):
        self.__secName = value
        self._property_changed('secName')        

    @property
    def percentADV(self) -> dict:
        return self.__percentADV

    @percentADV.setter
    def percentADV(self, value: dict):
        self.__percentADV = value
        self._property_changed('percentADV')        

    @property
    def unadjustedLow(self) -> dict:
        return self.__unadjustedLow

    @unadjustedLow.setter
    def unadjustedLow(self, value: dict):
        self.__unadjustedLow = value
        self._property_changed('unadjustedLow')        

    @property
    def contract(self) -> dict:
        return self.__contract

    @contract.setter
    def contract(self, value: dict):
        self.__contract = value
        self._property_changed('contract')        

    @property
    def sedol(self) -> dict:
        return self.__sedol

    @sedol.setter
    def sedol(self, value: dict):
        self.__sedol = value
        self._property_changed('sedol')        

    @property
    def roundingCostPnl(self) -> dict:
        return self.__roundingCostPnl

    @roundingCostPnl.setter
    def roundingCostPnl(self, value: dict):
        self.__roundingCostPnl = value
        self._property_changed('roundingCostPnl')        

    @property
    def sustainGlobal(self) -> dict:
        return self.__sustainGlobal

    @sustainGlobal.setter
    def sustainGlobal(self, value: dict):
        self.__sustainGlobal = value
        self._property_changed('sustainGlobal')        

    @property
    def sourceTicker(self) -> dict:
        return self.__sourceTicker

    @sourceTicker.setter
    def sourceTicker(self, value: dict):
        self.__sourceTicker = value
        self._property_changed('sourceTicker')        

    @property
    def portfolioId(self) -> dict:
        return self.__portfolioId

    @portfolioId.setter
    def portfolioId(self, value: dict):
        self.__portfolioId = value
        self._property_changed('portfolioId')        

    @property
    def gsid(self) -> dict:
        return self.__gsid

    @gsid.setter
    def gsid(self, value: dict):
        self.__gsid = value
        self._property_changed('gsid')        

    @property
    def esPercentile(self) -> dict:
        return self.__esPercentile

    @esPercentile.setter
    def esPercentile(self, value: dict):
        self.__esPercentile = value
        self._property_changed('esPercentile')        

    @property
    def lendingFund(self) -> dict:
        return self.__lendingFund

    @lendingFund.setter
    def lendingFund(self, value: dict):
        self.__lendingFund = value
        self._property_changed('lendingFund')        

    @property
    def tcmCostParticipationRate15Pct(self) -> dict:
        return self.__tcmCostParticipationRate15Pct

    @tcmCostParticipationRate15Pct.setter
    def tcmCostParticipationRate15Pct(self, value: dict):
        self.__tcmCostParticipationRate15Pct = value
        self._property_changed('tcmCostParticipationRate15Pct')        

    @property
    def sensitivity(self) -> dict:
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value: dict):
        self.__sensitivity = value
        self._property_changed('sensitivity')        

    @property
    def fiscalYear(self) -> dict:
        return self.__fiscalYear

    @fiscalYear.setter
    def fiscalYear(self, value: dict):
        self.__fiscalYear = value
        self._property_changed('fiscalYear')        

    @property
    def rcic(self) -> dict:
        return self.__rcic

    @rcic.setter
    def rcic(self, value: dict):
        self.__rcic = value
        self._property_changed('rcic')        

    @property
    def simonAssetTags(self) -> dict:
        return self.__simonAssetTags

    @simonAssetTags.setter
    def simonAssetTags(self, value: dict):
        self.__simonAssetTags = value
        self._property_changed('simonAssetTags')        

    @property
    def internal(self) -> dict:
        return self.__internal

    @internal.setter
    def internal(self, value: dict):
        self.__internal = value
        self._property_changed('internal')        

    @property
    def forwardPoint(self) -> dict:
        return self.__forwardPoint

    @forwardPoint.setter
    def forwardPoint(self, value: dict):
        self.__forwardPoint = value
        self._property_changed('forwardPoint')        

    @property
    def assetClassificationsGicsIndustry(self) -> dict:
        return self.__assetClassificationsGicsIndustry

    @assetClassificationsGicsIndustry.setter
    def assetClassificationsGicsIndustry(self, value: dict):
        self.__assetClassificationsGicsIndustry = value
        self._property_changed('assetClassificationsGicsIndustry')        

    @property
    def adjustedBidPrice(self) -> dict:
        return self.__adjustedBidPrice

    @adjustedBidPrice.setter
    def adjustedBidPrice(self, value: dict):
        self.__adjustedBidPrice = value
        self._property_changed('adjustedBidPrice')        

    @property
    def hitRateQtd(self) -> dict:
        return self.__hitRateQtd

    @hitRateQtd.setter
    def hitRateQtd(self, value: dict):
        self.__hitRateQtd = value
        self._property_changed('hitRateQtd')        

    @property
    def varSwap(self) -> dict:
        return self.__varSwap

    @varSwap.setter
    def varSwap(self, value: dict):
        self.__varSwap = value
        self._property_changed('varSwap')        

    @property
    def lowUnadjusted(self) -> dict:
        return self.__lowUnadjusted

    @lowUnadjusted.setter
    def lowUnadjusted(self, value: dict):
        self.__lowUnadjusted = value
        self._property_changed('lowUnadjusted')        

    @property
    def sectorsRaw(self) -> dict:
        return self.__sectorsRaw

    @sectorsRaw.setter
    def sectorsRaw(self, value: dict):
        self.__sectorsRaw = value
        self._property_changed('sectorsRaw')        

    @property
    def low(self) -> dict:
        return self.__low

    @low.setter
    def low(self, value: dict):
        self.__low = value
        self._property_changed('low')        

    @property
    def crossGroup(self) -> dict:
        return self.__crossGroup

    @crossGroup.setter
    def crossGroup(self, value: dict):
        self.__crossGroup = value
        self._property_changed('crossGroup')        

    @property
    def integratedScore(self) -> dict:
        return self.__integratedScore

    @integratedScore.setter
    def integratedScore(self, value: dict):
        self.__integratedScore = value
        self._property_changed('integratedScore')        

    @property
    def fiveDayPriceChangeBps(self) -> dict:
        return self.__fiveDayPriceChangeBps

    @fiveDayPriceChangeBps.setter
    def fiveDayPriceChangeBps(self, value: dict):
        self.__fiveDayPriceChangeBps = value
        self._property_changed('fiveDayPriceChangeBps')        

    @property
    def tradeSize(self) -> dict:
        return self.__tradeSize

    @tradeSize.setter
    def tradeSize(self, value: dict):
        self.__tradeSize = value
        self._property_changed('tradeSize')        

    @property
    def symbolDimensions(self) -> dict:
        return self.__symbolDimensions

    @symbolDimensions.setter
    def symbolDimensions(self, value: dict):
        self.__symbolDimensions = value
        self._property_changed('symbolDimensions')        

    @property
    def quotingStyle(self) -> dict:
        return self.__quotingStyle

    @quotingStyle.setter
    def quotingStyle(self, value: dict):
        self.__quotingStyle = value
        self._property_changed('quotingStyle')        

    @property
    def scenarioGroupId(self) -> dict:
        return self.__scenarioGroupId

    @scenarioGroupId.setter
    def scenarioGroupId(self, value: dict):
        self.__scenarioGroupId = value
        self._property_changed('scenarioGroupId')        

    @property
    def errorMessage(self) -> dict:
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, value: dict):
        self.__errorMessage = value
        self._property_changed('errorMessage')        

    @property
    def avgTradeRateDescription(self) -> dict:
        return self.__avgTradeRateDescription

    @avgTradeRateDescription.setter
    def avgTradeRateDescription(self, value: dict):
        self.__avgTradeRateDescription = value
        self._property_changed('avgTradeRateDescription')        

    @property
    def midPrice(self) -> dict:
        return self.__midPrice

    @midPrice.setter
    def midPrice(self, value: dict):
        self.__midPrice = value
        self._property_changed('midPrice')        

    @property
    def fraction(self) -> dict:
        return self.__fraction

    @fraction.setter
    def fraction(self, value: dict):
        self.__fraction = value
        self._property_changed('fraction')        

    @property
    def stsCreditMarket(self) -> dict:
        return self.__stsCreditMarket

    @stsCreditMarket.setter
    def stsCreditMarket(self, value: dict):
        self.__stsCreditMarket = value
        self._property_changed('stsCreditMarket')        

    @property
    def assetCountShort(self) -> dict:
        return self.__assetCountShort

    @assetCountShort.setter
    def assetCountShort(self, value: dict):
        self.__assetCountShort = value
        self._property_changed('assetCountShort')        

    @property
    def stsEmDm(self) -> dict:
        return self.__stsEmDm

    @stsEmDm.setter
    def stsEmDm(self, value: dict):
        self.__stsEmDm = value
        self._property_changed('stsEmDm')        

    @property
    def tcmCostHorizon2Day(self) -> dict:
        return self.__tcmCostHorizon2Day

    @tcmCostHorizon2Day.setter
    def tcmCostHorizon2Day(self, value: dict):
        self.__tcmCostHorizon2Day = value
        self._property_changed('tcmCostHorizon2Day')        

    @property
    def queueInLots(self) -> dict:
        return self.__queueInLots

    @queueInLots.setter
    def queueInLots(self, value: dict):
        self.__queueInLots = value
        self._property_changed('queueInLots')        

    @property
    def priceRangeInTicksDescription(self) -> dict:
        return self.__priceRangeInTicksDescription

    @priceRangeInTicksDescription.setter
    def priceRangeInTicksDescription(self, value: dict):
        self.__priceRangeInTicksDescription = value
        self._property_changed('priceRangeInTicksDescription')        

    @property
    def tenderOfferExpirationDate(self) -> dict:
        return self.__tenderOfferExpirationDate

    @tenderOfferExpirationDate.setter
    def tenderOfferExpirationDate(self, value: dict):
        self.__tenderOfferExpirationDate = value
        self._property_changed('tenderOfferExpirationDate')        

    @property
    def highUnadjusted(self) -> dict:
        return self.__highUnadjusted

    @highUnadjusted.setter
    def highUnadjusted(self, value: dict):
        self.__highUnadjusted = value
        self._property_changed('highUnadjusted')        

    @property
    def sourceCategory(self) -> dict:
        return self.__sourceCategory

    @sourceCategory.setter
    def sourceCategory(self, value: dict):
        self.__sourceCategory = value
        self._property_changed('sourceCategory')        

    @property
    def volumeUnadjusted(self) -> dict:
        return self.__volumeUnadjusted

    @volumeUnadjusted.setter
    def volumeUnadjusted(self, value: dict):
        self.__volumeUnadjusted = value
        self._property_changed('volumeUnadjusted')        

    @property
    def avgTradeRateLabel(self) -> tuple:
        return self.__avgTradeRateLabel

    @avgTradeRateLabel.setter
    def avgTradeRateLabel(self, value: tuple):
        self.__avgTradeRateLabel = value
        self._property_changed('avgTradeRateLabel')        

    @property
    def tcmCostParticipationRate5Pct(self) -> dict:
        return self.__tcmCostParticipationRate5Pct

    @tcmCostParticipationRate5Pct.setter
    def tcmCostParticipationRate5Pct(self, value: dict):
        self.__tcmCostParticipationRate5Pct = value
        self._property_changed('tcmCostParticipationRate5Pct')        

    @property
    def isActive(self) -> dict:
        return self.__isActive

    @isActive.setter
    def isActive(self, value: dict):
        self.__isActive = value
        self._property_changed('isActive')        

    @property
    def growthScore(self) -> dict:
        return self.__growthScore

    @growthScore.setter
    def growthScore(self, value: dict):
        self.__growthScore = value
        self._property_changed('growthScore')        

    @property
    def encodedStats(self) -> dict:
        return self.__encodedStats

    @encodedStats.setter
    def encodedStats(self, value: dict):
        self.__encodedStats = value
        self._property_changed('encodedStats')        

    @property
    def adjustedShortInterest(self) -> dict:
        return self.__adjustedShortInterest

    @adjustedShortInterest.setter
    def adjustedShortInterest(self, value: dict):
        self.__adjustedShortInterest = value
        self._property_changed('adjustedShortInterest')        

    @property
    def askSize(self) -> dict:
        return self.__askSize

    @askSize.setter
    def askSize(self, value: dict):
        self.__askSize = value
        self._property_changed('askSize')        

    @property
    def mdapiType(self) -> dict:
        return self.__mdapiType

    @mdapiType.setter
    def mdapiType(self, value: dict):
        self.__mdapiType = value
        self._property_changed('mdapiType')        

    @property
    def group(self) -> dict:
        return self.__group

    @group.setter
    def group(self, value: dict):
        self.__group = value
        self._property_changed('group')        

    @property
    def estimatedSpread(self) -> dict:
        return self.__estimatedSpread

    @estimatedSpread.setter
    def estimatedSpread(self, value: dict):
        self.__estimatedSpread = value
        self._property_changed('estimatedSpread')        

    @property
    def resource(self) -> dict:
        return self.__resource

    @resource.setter
    def resource(self, value: dict):
        self.__resource = value
        self._property_changed('resource')        

    @property
    def tcmCost(self) -> dict:
        return self.__tcmCost

    @tcmCost.setter
    def tcmCost(self, value: dict):
        self.__tcmCost = value
        self._property_changed('tcmCost')        

    @property
    def sustainJapan(self) -> dict:
        return self.__sustainJapan

    @sustainJapan.setter
    def sustainJapan(self, value: dict):
        self.__sustainJapan = value
        self._property_changed('sustainJapan')        

    @property
    def navSpread(self) -> dict:
        return self.__navSpread

    @navSpread.setter
    def navSpread(self, value: dict):
        self.__navSpread = value
        self._property_changed('navSpread')        

    @property
    def bidPrice(self) -> dict:
        return self.__bidPrice

    @bidPrice.setter
    def bidPrice(self, value: dict):
        self.__bidPrice = value
        self._property_changed('bidPrice')        

    @property
    def hedgeTrackingError(self) -> dict:
        return self.__hedgeTrackingError

    @hedgeTrackingError.setter
    def hedgeTrackingError(self, value: dict):
        self.__hedgeTrackingError = value
        self._property_changed('hedgeTrackingError')        

    @property
    def marketCapCategory(self) -> dict:
        return self.__marketCapCategory

    @marketCapCategory.setter
    def marketCapCategory(self, value: dict):
        self.__marketCapCategory = value
        self._property_changed('marketCapCategory')        

    @property
    def historicalVolume(self) -> dict:
        return self.__historicalVolume

    @historicalVolume.setter
    def historicalVolume(self, value: dict):
        self.__historicalVolume = value
        self._property_changed('historicalVolume')        

    @property
    def esNumericPercentile(self) -> dict:
        return self.__esNumericPercentile

    @esNumericPercentile.setter
    def esNumericPercentile(self, value: dict):
        self.__esNumericPercentile = value
        self._property_changed('esNumericPercentile')        

    @property
    def strikePrice(self) -> dict:
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: dict):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def calSpreadMisPricing(self) -> dict:
        return self.__calSpreadMisPricing

    @calSpreadMisPricing.setter
    def calSpreadMisPricing(self, value: dict):
        self.__calSpreadMisPricing = value
        self._property_changed('calSpreadMisPricing')        

    @property
    def equityGamma(self) -> dict:
        return self.__equityGamma

    @equityGamma.setter
    def equityGamma(self, value: dict):
        self.__equityGamma = value
        self._property_changed('equityGamma')        

    @property
    def grossIncome(self) -> dict:
        return self.__grossIncome

    @grossIncome.setter
    def grossIncome(self, value: dict):
        self.__grossIncome = value
        self._property_changed('grossIncome')        

    @property
    def emId(self) -> dict:
        return self.__emId

    @emId.setter
    def emId(self, value: dict):
        self.__emId = value
        self._property_changed('emId')        

    @property
    def adjustedOpenPrice(self) -> dict:
        return self.__adjustedOpenPrice

    @adjustedOpenPrice.setter
    def adjustedOpenPrice(self, value: dict):
        self.__adjustedOpenPrice = value
        self._property_changed('adjustedOpenPrice')        

    @property
    def assetCountInModel(self) -> dict:
        return self.__assetCountInModel

    @assetCountInModel.setter
    def assetCountInModel(self, value: dict):
        self.__assetCountInModel = value
        self._property_changed('assetCountInModel')        

    @property
    def stsCreditRegion(self) -> dict:
        return self.__stsCreditRegion

    @stsCreditRegion.setter
    def stsCreditRegion(self, value: dict):
        self.__stsCreditRegion = value
        self._property_changed('stsCreditRegion')        

    @property
    def point(self) -> dict:
        return self.__point

    @point.setter
    def point(self, value: dict):
        self.__point = value
        self._property_changed('point')        

    @property
    def lender(self) -> dict:
        return self.__lender

    @lender.setter
    def lender(self, value: dict):
        self.__lender = value
        self._property_changed('lender')        

    @property
    def minTemperature(self) -> dict:
        return self.__minTemperature

    @minTemperature.setter
    def minTemperature(self, value: dict):
        self.__minTemperature = value
        self._property_changed('minTemperature')        

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: dict):
        self.__value = value
        self._property_changed('value')        

    @property
    def relativeStrike(self) -> dict:
        return self.__relativeStrike

    @relativeStrike.setter
    def relativeStrike(self, value: dict):
        self.__relativeStrike = value
        self._property_changed('relativeStrike')        

    @property
    def amount(self) -> dict:
        return self.__amount

    @amount.setter
    def amount(self, value: dict):
        self.__amount = value
        self._property_changed('amount')        

    @property
    def quantity(self) -> dict:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: dict):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def lendingFundAcct(self) -> dict:
        return self.__lendingFundAcct

    @lendingFundAcct.setter
    def lendingFundAcct(self, value: dict):
        self.__lendingFundAcct = value
        self._property_changed('lendingFundAcct')        

    @property
    def reportId(self) -> dict:
        return self.__reportId

    @reportId.setter
    def reportId(self, value: dict):
        self.__reportId = value
        self._property_changed('reportId')        

    @property
    def indexWeight(self) -> dict:
        return self.__indexWeight

    @indexWeight.setter
    def indexWeight(self, value: dict):
        self.__indexWeight = value
        self._property_changed('indexWeight')        

    @property
    def rebate(self) -> dict:
        return self.__rebate

    @rebate.setter
    def rebate(self, value: dict):
        self.__rebate = value
        self._property_changed('rebate')        

    @property
    def trader(self) -> dict:
        return self.__trader

    @trader.setter
    def trader(self, value: dict):
        self.__trader = value
        self._property_changed('trader')        

    @property
    def factorCategory(self) -> dict:
        return self.__factorCategory

    @factorCategory.setter
    def factorCategory(self, value: dict):
        self.__factorCategory = value
        self._property_changed('factorCategory')        

    @property
    def impliedVolatility(self) -> dict:
        return self.__impliedVolatility

    @impliedVolatility.setter
    def impliedVolatility(self, value: dict):
        self.__impliedVolatility = value
        self._property_changed('impliedVolatility')        

    @property
    def spread(self) -> dict:
        return self.__spread

    @spread.setter
    def spread(self, value: dict):
        self.__spread = value
        self._property_changed('spread')        

    @property
    def stsRatesMaturity(self) -> dict:
        return self.__stsRatesMaturity

    @stsRatesMaturity.setter
    def stsRatesMaturity(self, value: dict):
        self.__stsRatesMaturity = value
        self._property_changed('stsRatesMaturity')        

    @property
    def equityDelta(self) -> dict:
        return self.__equityDelta

    @equityDelta.setter
    def equityDelta(self, value: dict):
        self.__equityDelta = value
        self._property_changed('equityDelta')        

    @property
    def grossWeight(self) -> dict:
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value: dict):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def listed(self) -> dict:
        return self.__listed

    @listed.setter
    def listed(self, value: dict):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def tcmCostHorizon6Hour(self) -> dict:
        return self.__tcmCostHorizon6Hour

    @tcmCostHorizon6Hour.setter
    def tcmCostHorizon6Hour(self, value: dict):
        self.__tcmCostHorizon6Hour = value
        self._property_changed('tcmCostHorizon6Hour')        

    @property
    def g10Currency(self) -> dict:
        return self.__g10Currency

    @g10Currency.setter
    def g10Currency(self, value: dict):
        self.__g10Currency = value
        self._property_changed('g10Currency')        

    @property
    def shockStyle(self) -> dict:
        return self.__shockStyle

    @shockStyle.setter
    def shockStyle(self, value: dict):
        self.__shockStyle = value
        self._property_changed('shockStyle')        

    @property
    def relativePeriod(self) -> dict:
        return self.__relativePeriod

    @relativePeriod.setter
    def relativePeriod(self, value: dict):
        self.__relativePeriod = value
        self._property_changed('relativePeriod')        

    @property
    def isin(self) -> dict:
        return self.__isin

    @isin.setter
    def isin(self, value: dict):
        self.__isin = value
        self._property_changed('isin')        

    @property
    def methodology(self) -> dict:
        return self.__methodology

    @methodology.setter
    def methodology(self, value: dict):
        self.__methodology = value
        self._property_changed('methodology')        


class FieldValueMap(Base):
               
    def __init__(self, **kwargs):
        super().__init__()
        self.__queueClockTimeLabel = kwargs.get('queueClockTimeLabel')
        self.__marketPnl = kwargs.get('marketPnl')
        self.__year = kwargs.get('year')
        self.__sustainAsiaExJapan = kwargs.get('sustainAsiaExJapan')
        self.__investmentRate = kwargs.get('investmentRate')
        self.__assetClassificationsGicsSubIndustry = kwargs.get('assetClassificationsGicsSubIndustry')
        self.__bidUnadjusted = kwargs.get('bidUnadjusted')
        self.__economicTermsHash = kwargs.get('economicTermsHash')
        self.__neighbourAssetId = kwargs.get('neighbourAssetId')
        self.__simonIntlAssetTags = kwargs.get('simonIntlAssetTags')
        self.__path = kwargs.get('path')
        self.__availableInventory = kwargs.get('availableInventory')
        self.__clientContact = kwargs.get('clientContact')
        self.__est1DayCompletePct = kwargs.get('est1DayCompletePct')
        self.__rank = kwargs.get('rank')
        self.__dataSetCategory = kwargs.get('dataSetCategory')
        self.__createdById = kwargs.get('createdById')
        self.__vehicleType = kwargs.get('vehicleType')
        self.__dailyRisk = kwargs.get('dailyRisk')
        self.__bosInBpsLabel = kwargs.get('bosInBpsLabel')
        self.__marketDataType = kwargs.get('marketDataType')
        self.__sentimentScore = kwargs.get('sentimentScore')
        self.__bosInBps = kwargs.get('bosInBps')
        self.__pointClass = kwargs.get('pointClass')
        self.__fxSpot = kwargs.get('fxSpot')
        self.__bidLow = kwargs.get('bidLow')
        self.__valuePrevious = kwargs.get('valuePrevious')
        self.__fairVarianceVolatility = kwargs.get('fairVarianceVolatility')
        self.__avgTradeRate = kwargs.get('avgTradeRate')
        self.__shortLevel = kwargs.get('shortLevel')
        self.__hedgeVolatility = kwargs.get('hedgeVolatility')
        self.__version = kwargs.get('version')
        self.__tags = kwargs.get('tags')
        self.__underlyingAssetId = kwargs.get('underlyingAssetId')
        self.__clientExposure = kwargs.get('clientExposure')
        self.__correlation = kwargs.get('correlation')
        self.__exposure = kwargs.get('exposure')
        self.__gsSustainSubSector = kwargs.get('gsSustainSubSector')
        self.__domain = kwargs.get('domain')
        self.__marketDataAsset = kwargs.get('marketDataAsset')
        self.__forwardTenor = kwargs.get('forwardTenor')
        self.__unadjustedHigh = kwargs.get('unadjustedHigh')
        self.__sourceImportance = kwargs.get('sourceImportance')
        self.__eid = kwargs.get('eid')
        self.__jsn = kwargs.get('jsn')
        self.__relativeReturnQtd = kwargs.get('relativeReturnQtd')
        self.__displayName = kwargs.get('displayName')
        self.__minutesToTrade100Pct = kwargs.get('minutesToTrade100Pct')
        self.__marketModelId = kwargs.get('marketModelId')
        self.__quoteType = kwargs.get('quoteType')
        self.__tenor = kwargs.get('tenor')
        self.__esPolicyPercentile = kwargs.get('esPolicyPercentile')
        self.__tcmCostParticipationRate75Pct = kwargs.get('tcmCostParticipationRate75Pct')
        self.__close = kwargs.get('close')
        self.__tcmCostParticipationRate100Pct = kwargs.get('tcmCostParticipationRate100Pct')
        self.__disclaimer = kwargs.get('disclaimer')
        self.__measureIdx = kwargs.get('measureIdx')
        self.__a = kwargs.get('a')
        self.__b = kwargs.get('b')
        self.__loanFee = kwargs.get('loanFee')
        self.__c = kwargs.get('c')
        self.__equityVega = kwargs.get('equityVega')
        self.__deploymentVersion = kwargs.get('deploymentVersion')
        self.__fiveDayMove = kwargs.get('fiveDayMove')
        self.__borrower = kwargs.get('borrower')
        self.__performanceContribution = kwargs.get('performanceContribution')
        self.__targetNotional = kwargs.get('targetNotional')
        self.__fillLegId = kwargs.get('fillLegId')
        self.__delisted = kwargs.get('delisted')
        self.__rationale = kwargs.get('rationale')
        self.__regionalFocus = kwargs.get('regionalFocus')
        self.__volumePrimary = kwargs.get('volumePrimary')
        self.__series = kwargs.get('series')
        self.__simonId = kwargs.get('simonId')
        self.__newIdeasQtd = kwargs.get('newIdeasQtd')
        self.__adjustedAskPrice = kwargs.get('adjustedAskPrice')
        self.__quarter = kwargs.get('quarter')
        self.__factorUniverse = kwargs.get('factorUniverse')
        self.__eventCategory = kwargs.get('eventCategory')
        self.__impliedNormalVolatility = kwargs.get('impliedNormalVolatility')
        self.__unadjustedOpen = kwargs.get('unadjustedOpen')
        self.__arrivalRt = kwargs.get('arrivalRt')
        self.__transactionCost = kwargs.get('transactionCost')
        self.__servicingCostShortPnl = kwargs.get('servicingCostShortPnl')
        self.__bidAskSpread = kwargs.get('bidAskSpread')
        self.__optionType = kwargs.get('optionType')
        self.__tcmCostHorizon3Hour = kwargs.get('tcmCostHorizon3Hour')
        self.__clusterDescription = kwargs.get('clusterDescription')
        self.__positionAmount = kwargs.get('positionAmount')
        self.__numberOfPositions = kwargs.get('numberOfPositions')
        self.__windSpeed = kwargs.get('windSpeed')
        self.__openUnadjusted = kwargs.get('openUnadjusted')
        self.__maRank = kwargs.get('maRank')
        self.__eventStartDateTime = kwargs.get('eventStartDateTime')
        self.__askPrice = kwargs.get('askPrice')
        self.__eventId = kwargs.get('eventId')
        self.__dataProduct = kwargs.get('dataProduct')
        self.__sectors = kwargs.get('sectors')
        self.__annualizedTrackingError = kwargs.get('annualizedTrackingError')
        self.__volSwap = kwargs.get('volSwap')
        self.__annualizedRisk = kwargs.get('annualizedRisk')
        self.__corporateAction = kwargs.get('corporateAction')
        self.__conviction = kwargs.get('conviction')
        self.__grossExposure = kwargs.get('grossExposure')
        self.__benchmarkMaturity = kwargs.get('benchmarkMaturity')
        self.__volumeComposite = kwargs.get('volumeComposite')
        self.__volume = kwargs.get('volume')
        self.__adv = kwargs.get('adv')
        self.__stsFxCurrency = kwargs.get('stsFxCurrency')
        self.__wpk = kwargs.get('wpk')
        self.__shortConvictionMedium = kwargs.get('shortConvictionMedium')
        self.__bidChange = kwargs.get('bidChange')
        self.__exchange = kwargs.get('exchange')
        self.__expiration = kwargs.get('expiration')
        self.__tradePrice = kwargs.get('tradePrice')
        self.__esPolicyScore = kwargs.get('esPolicyScore')
        self.__loanId = kwargs.get('loanId')
        self.__cid = kwargs.get('cid')
        self.__liquidityScore = kwargs.get('liquidityScore')
        self.__importance = kwargs.get('importance')
        self.__sourceDateSpan = kwargs.get('sourceDateSpan')
        self.__assetClassificationsGicsSector = kwargs.get('assetClassificationsGicsSector')
        self.__underlyingDataSetId = kwargs.get('underlyingDataSetId')
        self.__stsAssetName = kwargs.get('stsAssetName')
        self.__closeUnadjusted = kwargs.get('closeUnadjusted')
        self.__valueUnit = kwargs.get('valueUnit')
        self.__bidHigh = kwargs.get('bidHigh')
        self.__adjustedLowPrice = kwargs.get('adjustedLowPrice')
        self.__netExposureClassification = kwargs.get('netExposureClassification')
        self.__longConvictionLarge = kwargs.get('longConvictionLarge')
        self.__fairVariance = kwargs.get('fairVariance')
        self.__hitRateWtd = kwargs.get('hitRateWtd')
        self.__oad = kwargs.get('oad')
        self.__bosInBpsDescription = kwargs.get('bosInBpsDescription')
        self.__lowPrice = kwargs.get('lowPrice')
        self.__realizedVolatility = kwargs.get('realizedVolatility')
        self.__rate = kwargs.get('rate')
        self.__adv22DayPct = kwargs.get('adv22DayPct')
        self.__alpha = kwargs.get('alpha')
        self.__client = kwargs.get('client')
        self.__company = kwargs.get('company')
        self.__convictionList = kwargs.get('convictionList')
        self.__priceRangeInTicksLabel = kwargs.get('priceRangeInTicksLabel')
        self.__ticker = kwargs.get('ticker')
        self.__inRiskModel = kwargs.get('inRiskModel')
        self.__tcmCostHorizon1Day = kwargs.get('tcmCostHorizon1Day')
        self.__servicingCostLongPnl = kwargs.get('servicingCostLongPnl')
        self.__stsRatesCountry = kwargs.get('stsRatesCountry')
        self.__meetingNumber = kwargs.get('meetingNumber')
        self.__exchangeId = kwargs.get('exchangeId')
        self.__horizon = kwargs.get('horizon')
        self.__tcmCostHorizon20Day = kwargs.get('tcmCostHorizon20Day')
        self.__longLevel = kwargs.get('longLevel')
        self.__sourceValueForecast = kwargs.get('sourceValueForecast')
        self.__shortConvictionLarge = kwargs.get('shortConvictionLarge')
        self.__realm = kwargs.get('realm')
        self.__bid = kwargs.get('bid')
        self.__dataDescription = kwargs.get('dataDescription')
        self.__composite22DayAdv = kwargs.get('composite22DayAdv')
        self.__gsn = kwargs.get('gsn')
        self.__isAggressive = kwargs.get('isAggressive')
        self.__orderId = kwargs.get('orderId')
        self.__gss = kwargs.get('gss')
        self.__percentOfMediandv1m = kwargs.get('percentOfMediandv1m')
        self.__lendables = kwargs.get('lendables')
        self.__assetClass = kwargs.get('assetClass')
        self.__gsideid = kwargs.get('gsideid')
        self.__bosInTicksLabel = kwargs.get('bosInTicksLabel')
        self.__ric = kwargs.get('ric')
        self.__positionSourceId = kwargs.get('positionSourceId')
        self.__division = kwargs.get('division')
        self.__marketCapUSD = kwargs.get('marketCapUSD')
        self.__deploymentId = kwargs.get('deploymentId')
        self.__highPrice = kwargs.get('highPrice')
        self.__shortWeight = kwargs.get('shortWeight')
        self.__absoluteShares = kwargs.get('absoluteShares')
        self.__action = kwargs.get('action')
        self.__model = kwargs.get('model')
        self.__id = kwargs.get('id')
        self.__arrivalHaircutVwapNormalized = kwargs.get('arrivalHaircutVwapNormalized')
        self.__queueClockTimeDescription = kwargs.get('queueClockTimeDescription')
        self.__period = kwargs.get('period')
        self.__indexCreateSource = kwargs.get('indexCreateSource')
        self.__fiscalQuarter = kwargs.get('fiscalQuarter')
        self.__deltaStrike = kwargs.get('deltaStrike')
        self.__marketImpact = kwargs.get('marketImpact')
        self.__eventType = kwargs.get('eventType')
        self.__assetCountLong = kwargs.get('assetCountLong')
        self.__valueActual = kwargs.get('valueActual')
        self.__bcid = kwargs.get('bcid')
        self.__originalCountry = kwargs.get('originalCountry')
        self.__touchLiquidityScore = kwargs.get('touchLiquidityScore')
        self.__field = kwargs.get('field')
        self.__spot = kwargs.get('spot')
        self.__expectedCompletionDate = kwargs.get('expectedCompletionDate')
        self.__loanValue = kwargs.get('loanValue')
        self.__skew = kwargs.get('skew')
        self.__status = kwargs.get('status')
        self.__sustainEmergingMarkets = kwargs.get('sustainEmergingMarkets')
        self.__eventDateTime = kwargs.get('eventDateTime')
        self.__totalReturnPrice = kwargs.get('totalReturnPrice')
        self.__city = kwargs.get('city')
        self.__eventSource = kwargs.get('eventSource')
        self.__qisPermNo = kwargs.get('qisPermNo')
        self.__hitRateYtd = kwargs.get('hitRateYtd')
        self.__stsCommodity = kwargs.get('stsCommodity')
        self.__stsCommoditySector = kwargs.get('stsCommoditySector')
        self.__salesCoverage = kwargs.get('salesCoverage')
        self.__shortExposure = kwargs.get('shortExposure')
        self.__esScore = kwargs.get('esScore')
        self.__tcmCostParticipationRate10Pct = kwargs.get('tcmCostParticipationRate10Pct')
        self.__eventTime = kwargs.get('eventTime')
        self.__positionSourceName = kwargs.get('positionSourceName')
        self.__priceRangeInTicks = kwargs.get('priceRangeInTicks')
        self.__deliveryDate = kwargs.get('deliveryDate')
        self.__arrivalHaircutVwap = kwargs.get('arrivalHaircutVwap')
        self.__interestRate = kwargs.get('interestRate')
        self.__executionDays = kwargs.get('executionDays')
        self.__pctChange = kwargs.get('pctChange')
        self.__side = kwargs.get('side')
        self.__numberOfRolls = kwargs.get('numberOfRolls')
        self.__agentLenderFee = kwargs.get('agentLenderFee')
        self.__complianceRestrictedStatus = kwargs.get('complianceRestrictedStatus')
        self.__forward = kwargs.get('forward')
        self.__borrowFee = kwargs.get('borrowFee')
        self.__strike = kwargs.get('strike')
        self.__updateTime = kwargs.get('updateTime')
        self.__loanSpread = kwargs.get('loanSpread')
        self.__tcmCostHorizon12Hour = kwargs.get('tcmCostHorizon12Hour')
        self.__dewPoint = kwargs.get('dewPoint')
        self.__researchCommission = kwargs.get('researchCommission')
        self.__bbid = kwargs.get('bbid')
        self.__assetClassificationsRiskCountryCode = kwargs.get('assetClassificationsRiskCountryCode')
        self.__eventStatus = kwargs.get('eventStatus')
        self.__effectiveDate = kwargs.get('effectiveDate')
        self.__return = kwargs.get('return_')
        self.__maxTemperature = kwargs.get('maxTemperature')
        self.__acquirerShareholderMeetingDate = kwargs.get('acquirerShareholderMeetingDate')
        self.__arrivalMidNormalized = kwargs.get('arrivalMidNormalized')
        self.__rating = kwargs.get('rating')
        self.__arrivalRtNormalized = kwargs.get('arrivalRtNormalized')
        self.__performanceFee = kwargs.get('performanceFee')
        self.__reportType = kwargs.get('reportType')
        self.__sourceURL = kwargs.get('sourceURL')
        self.__estimatedReturn = kwargs.get('estimatedReturn')
        self.__underlyingAssetIds = kwargs.get('underlyingAssetIds')
        self.__high = kwargs.get('high')
        self.__sourceLastUpdate = kwargs.get('sourceLastUpdate')
        self.__queueInLotsLabel = kwargs.get('queueInLotsLabel')
        self.__adv10DayPct = kwargs.get('adv10DayPct')
        self.__longConvictionMedium = kwargs.get('longConvictionMedium')
        self.__eventName = kwargs.get('eventName')
        self.__annualRisk = kwargs.get('annualRisk')
        self.__dailyTrackingError = kwargs.get('dailyTrackingError')
        self.__unadjustedBid = kwargs.get('unadjustedBid')
        self.__gsdeer = kwargs.get('gsdeer')
        self.__marketCap = kwargs.get('marketCap')
        self.__clusterRegion = kwargs.get('clusterRegion')
        self.__bbidEquivalent = kwargs.get('bbidEquivalent')
        self.__prevCloseAsk = kwargs.get('prevCloseAsk')
        self.__level = kwargs.get('level')
        self.__valoren = kwargs.get('valoren')
        self.__pressure = kwargs.get('pressure')
        self.__shortDescription = kwargs.get('shortDescription')
        self.__basis = kwargs.get('basis')
        self.__netWeight = kwargs.get('netWeight')
        self.__hedgeId = kwargs.get('hedgeId')
        self.__portfolioManagers = kwargs.get('portfolioManagers')
        self.__assetParametersCommoditySector = kwargs.get('assetParametersCommoditySector')
        self.__bosInTicks = kwargs.get('bosInTicks')
        self.__tcmCostHorizon8Day = kwargs.get('tcmCostHorizon8Day')
        self.__supraStrategy = kwargs.get('supraStrategy')
        self.__adv5DayPct = kwargs.get('adv5DayPct')
        self.__factorSource = kwargs.get('factorSource')
        self.__leverage = kwargs.get('leverage')
        self.__submitter = kwargs.get('submitter')
        self.__notional = kwargs.get('notional')
        self.__esDisclosurePercentage = kwargs.get('esDisclosurePercentage')
        self.__clientShortName = kwargs.get('clientShortName')
        self.__fwdPoints = kwargs.get('fwdPoints')
        self.__groupCategory = kwargs.get('groupCategory')
        self.__kpiId = kwargs.get('kpiId')
        self.__relativeReturnWtd = kwargs.get('relativeReturnWtd')
        self.__bidPlusAsk = kwargs.get('bidPlusAsk')
        self.__assetClassificationsRiskCountryName = kwargs.get('assetClassificationsRiskCountryName')
        self.__total = kwargs.get('total')
        self.__riskModel = kwargs.get('riskModel')
        self.__assetId = kwargs.get('assetId')
        self.__lastUpdatedTime = kwargs.get('lastUpdatedTime')
        self.__fairValue = kwargs.get('fairValue')
        self.__adjustedHighPrice = kwargs.get('adjustedHighPrice')
        self.__openTime = kwargs.get('openTime')
        self.__beta = kwargs.get('beta')
        self.__direction = kwargs.get('direction')
        self.__valueForecast = kwargs.get('valueForecast')
        self.__longExposure = kwargs.get('longExposure')
        self.__positionSourceType = kwargs.get('positionSourceType')
        self.__tcmCostParticipationRate20Pct = kwargs.get('tcmCostParticipationRate20Pct')
        self.__adjustedClosePrice = kwargs.get('adjustedClosePrice')
        self.__cross = kwargs.get('cross')
        self.__lmsId = kwargs.get('lmsId')
        self.__rebateRate = kwargs.get('rebateRate')
        self.__ideaStatus = kwargs.get('ideaStatus')
        self.__participationRate = kwargs.get('participationRate')
        self.__obfr = kwargs.get('obfr')
        self.__fxForecast = kwargs.get('fxForecast')
        self.__fixingTimeLabel = kwargs.get('fixingTimeLabel')
        self.__fillId = kwargs.get('fillId')
        self.__esNumericScore = kwargs.get('esNumericScore')
        self.__inBenchmark = kwargs.get('inBenchmark')
        self.__strategy = kwargs.get('strategy')
        self.__shortInterest = kwargs.get('shortInterest')
        self.__referencePeriod = kwargs.get('referencePeriod')
        self.__adjustedVolume = kwargs.get('adjustedVolume')
        self.__queueInLotsDescription = kwargs.get('queueInLotsDescription')
        self.__pbClientId = kwargs.get('pbClientId')
        self.__ownerId = kwargs.get('ownerId')
        self.__secDB = kwargs.get('secDB')
        self.__composite10DayAdv = kwargs.get('composite10DayAdv')
        self.__objective = kwargs.get('objective')
        self.__navPrice = kwargs.get('navPrice')
        self.__ideaActivityType = kwargs.get('ideaActivityType')
        self.__precipitation = kwargs.get('precipitation')
        self.__ideaSource = kwargs.get('ideaSource')
        self.__hedgeNotional = kwargs.get('hedgeNotional')
        self.__askLow = kwargs.get('askLow')
        self.__unadjustedAsk = kwargs.get('unadjustedAsk')
        self.__betaAdjustedNetExposure = kwargs.get('betaAdjustedNetExposure')
        self.__expiry = kwargs.get('expiry')
        self.__tradingPnl = kwargs.get('tradingPnl')
        self.__strikePercentage = kwargs.get('strikePercentage')
        self.__excessReturnPrice = kwargs.get('excessReturnPrice')
        self.__givenPlusPaid = kwargs.get('givenPlusPaid')
        self.__shortConvictionSmall = kwargs.get('shortConvictionSmall')
        self.__prevCloseBid = kwargs.get('prevCloseBid')
        self.__fxPnl = kwargs.get('fxPnl')
        self.__forecast = kwargs.get('forecast')
        self.__tcmCostHorizon16Day = kwargs.get('tcmCostHorizon16Day')
        self.__pnl = kwargs.get('pnl')
        self.__assetClassificationsGicsIndustryGroup = kwargs.get('assetClassificationsGicsIndustryGroup')
        self.__unadjustedClose = kwargs.get('unadjustedClose')
        self.__tcmCostHorizon4Day = kwargs.get('tcmCostHorizon4Day')
        self.__assetClassificationsIsPrimary = kwargs.get('assetClassificationsIsPrimary')
        self.__styles = kwargs.get('styles')
        self.__lendingSecId = kwargs.get('lendingSecId')
        self.__shortName = kwargs.get('shortName')
        self.__equityTheta = kwargs.get('equityTheta')
        self.__averageFillPrice = kwargs.get('averageFillPrice')
        self.__snowfall = kwargs.get('snowfall')
        self.__mic = kwargs.get('mic')
        self.__openPrice = kwargs.get('openPrice')
        self.__autoExecState = kwargs.get('autoExecState')
        self.__depthSpreadScore = kwargs.get('depthSpreadScore')
        self.__relativeReturnYtd = kwargs.get('relativeReturnYtd')
        self.__long = kwargs.get('long')
        self.__fairVolatility = kwargs.get('fairVolatility')
        self.__dollarCross = kwargs.get('dollarCross')
        self.__longWeight = kwargs.get('longWeight')
        self.__vendor = kwargs.get('vendor')
        self.__currency = kwargs.get('currency')
        self.__clusterClass = kwargs.get('clusterClass')
        self.__financialReturnsScore = kwargs.get('financialReturnsScore')
        self.__netChange = kwargs.get('netChange')
        self.__nonSymbolDimensions = kwargs.get('nonSymbolDimensions')
        self.__bidSize = kwargs.get('bidSize')
        self.__arrivalMid = kwargs.get('arrivalMid')
        self.__assetParametersExchangeCurrency = kwargs.get('assetParametersExchangeCurrency')
        self.__unexplained = kwargs.get('unexplained')
        self.__assetClassificationsCountryName = kwargs.get('assetClassificationsCountryName')
        self.__metric = kwargs.get('metric')
        self.__newIdeasYtd = kwargs.get('newIdeasYtd')
        self.__managementFee = kwargs.get('managementFee')
        self.__ask = kwargs.get('ask')
        self.__impliedLognormalVolatility = kwargs.get('impliedLognormalVolatility')
        self.__closePrice = kwargs.get('closePrice')
        self.__endTime = kwargs.get('endTime')
        self.__open = kwargs.get('open')
        self.__sourceId = kwargs.get('sourceId')
        self.__country = kwargs.get('country')
        self.__cusip = kwargs.get('cusip')
        self.__ideaActivityTime = kwargs.get('ideaActivityTime')
        self.__touchSpreadScore = kwargs.get('touchSpreadScore')
        self.__absoluteStrike = kwargs.get('absoluteStrike')
        self.__netExposure = kwargs.get('netExposure')
        self.__source = kwargs.get('source')
        self.__assetClassificationsCountryCode = kwargs.get('assetClassificationsCountryCode')
        self.__frequency = kwargs.get('frequency')
        self.__activityId = kwargs.get('activityId')
        self.__estimatedImpact = kwargs.get('estimatedImpact')
        self.__dataSetSubCategory = kwargs.get('dataSetSubCategory')
        self.__assetParametersPricingLocation = kwargs.get('assetParametersPricingLocation')
        self.__eventDescription = kwargs.get('eventDescription')
        self.__strikeReference = kwargs.get('strikeReference')
        self.__details = kwargs.get('details')
        self.__assetCount = kwargs.get('assetCount')
        self.__given = kwargs.get('given')
        self.__absoluteValue = kwargs.get('absoluteValue')
        self.__delistingDate = kwargs.get('delistingDate')
        self.__longTenor = kwargs.get('longTenor')
        self.__mctr = kwargs.get('mctr')
        self.__weight = kwargs.get('weight')
        self.__historicalClose = kwargs.get('historicalClose')
        self.__assetCountPriced = kwargs.get('assetCountPriced')
        self.__marketDataPoint = kwargs.get('marketDataPoint')
        self.__ideaId = kwargs.get('ideaId')
        self.__commentStatus = kwargs.get('commentStatus')
        self.__marginalCost = kwargs.get('marginalCost')
        self.__absoluteWeight = kwargs.get('absoluteWeight')
        self.__tradeTime = kwargs.get('tradeTime')
        self.__measure = kwargs.get('measure')
        self.__clientWeight = kwargs.get('clientWeight')
        self.__hedgeAnnualizedVolatility = kwargs.get('hedgeAnnualizedVolatility')
        self.__benchmarkCurrency = kwargs.get('benchmarkCurrency')
        self.__name = kwargs.get('name')
        self.__aum = kwargs.get('aum')
        self.__folderName = kwargs.get('folderName')
        self.__lendingPartnerFee = kwargs.get('lendingPartnerFee')
        self.__region = kwargs.get('region')
        self.__liveDate = kwargs.get('liveDate')
        self.__askHigh = kwargs.get('askHigh')
        self.__corporateActionType = kwargs.get('corporateActionType')
        self.__primeId = kwargs.get('primeId')
        self.__tenor2 = kwargs.get('tenor2')
        self.__description = kwargs.get('description')
        self.__valueRevised = kwargs.get('valueRevised')
        self.__ownerName = kwargs.get('ownerName')
        self.__adjustedTradePrice = kwargs.get('adjustedTradePrice')
        self.__lastUpdatedById = kwargs.get('lastUpdatedById')
        self.__zScore = kwargs.get('zScore')
        self.__targetShareholderMeetingDate = kwargs.get('targetShareholderMeetingDate')
        self.__isADR = kwargs.get('isADR')
        self.__eventStartTime = kwargs.get('eventStartTime')
        self.__factor = kwargs.get('factor')
        self.__longConvictionSmall = kwargs.get('longConvictionSmall')
        self.__serviceId = kwargs.get('serviceId')
        self.__turnover = kwargs.get('turnover')
        self.__complianceEffectiveTime = kwargs.get('complianceEffectiveTime')
        self.__expirationDate = kwargs.get('expirationDate')
        self.__gsfeer = kwargs.get('gsfeer')
        self.__coverage = kwargs.get('coverage')
        self.__backtestId = kwargs.get('backtestId')
        self.__gPercentile = kwargs.get('gPercentile')
        self.__gScore = kwargs.get('gScore')
        self.__marketValue = kwargs.get('marketValue')
        self.__multipleScore = kwargs.get('multipleScore')
        self.__lendingFundNav = kwargs.get('lendingFundNav')
        self.__sourceOriginalCategory = kwargs.get('sourceOriginalCategory')
        self.__betaAdjustedExposure = kwargs.get('betaAdjustedExposure')
        self.__composite5DayAdv = kwargs.get('composite5DayAdv')
        self.__latestExecutionTime = kwargs.get('latestExecutionTime')
        self.__dividendPoints = kwargs.get('dividendPoints')
        self.__newIdeasWtd = kwargs.get('newIdeasWtd')
        self.__paid = kwargs.get('paid')
        self.__short = kwargs.get('short')
        self.__location = kwargs.get('location')
        self.__comment = kwargs.get('comment')
        self.__bosInTicksDescription = kwargs.get('bosInTicksDescription')
        self.__sourceSymbol = kwargs.get('sourceSymbol')
        self.__time = kwargs.get('time')
        self.__scenarioId = kwargs.get('scenarioId')
        self.__askUnadjusted = kwargs.get('askUnadjusted')
        self.__queueClockTime = kwargs.get('queueClockTime')
        self.__askChange = kwargs.get('askChange')
        self.__tcmCostParticipationRate50Pct = kwargs.get('tcmCostParticipationRate50Pct')
        self.__normalizedPerformance = kwargs.get('normalizedPerformance')
        self.__cmId = kwargs.get('cmId')
        self.__type = kwargs.get('type')
        self.__mdapi = kwargs.get('mdapi')
        self.__dividendYield = kwargs.get('dividendYield')
        self.__cumulativePnl = kwargs.get('cumulativePnl')
        self.__sourceOrigin = kwargs.get('sourceOrigin')
        self.__shortTenor = kwargs.get('shortTenor')
        self.__unadjustedVolume = kwargs.get('unadjustedVolume')
        self.__measures = kwargs.get('measures')
        self.__tradingCostPnl = kwargs.get('tradingCostPnl')
        self.__internalUser = kwargs.get('internalUser')
        self.__price = kwargs.get('price')
        self.__paymentQuantity = kwargs.get('paymentQuantity')
        self.__underlyer = kwargs.get('underlyer')
        self.__createdTime = kwargs.get('createdTime')
        self.__positionIdx = kwargs.get('positionIdx')
        self.__secName = kwargs.get('secName')
        self.__percentADV = kwargs.get('percentADV')
        self.__unadjustedLow = kwargs.get('unadjustedLow')
        self.__contract = kwargs.get('contract')
        self.__sedol = kwargs.get('sedol')
        self.__roundingCostPnl = kwargs.get('roundingCostPnl')
        self.__sustainGlobal = kwargs.get('sustainGlobal')
        self.__sourceTicker = kwargs.get('sourceTicker')
        self.__portfolioId = kwargs.get('portfolioId')
        self.__gsid = kwargs.get('gsid')
        self.__esPercentile = kwargs.get('esPercentile')
        self.__lendingFund = kwargs.get('lendingFund')
        self.__tcmCostParticipationRate15Pct = kwargs.get('tcmCostParticipationRate15Pct')
        self.__sensitivity = kwargs.get('sensitivity')
        self.__fiscalYear = kwargs.get('fiscalYear')
        self.__rcic = kwargs.get('rcic')
        self.__simonAssetTags = kwargs.get('simonAssetTags')
        self.__internal = kwargs.get('internal')
        self.__forwardPoint = kwargs.get('forwardPoint')
        self.__assetClassificationsGicsIndustry = kwargs.get('assetClassificationsGicsIndustry')
        self.__adjustedBidPrice = kwargs.get('adjustedBidPrice')
        self.__hitRateQtd = kwargs.get('hitRateQtd')
        self.__varSwap = kwargs.get('varSwap')
        self.__lowUnadjusted = kwargs.get('lowUnadjusted')
        self.__sectorsRaw = kwargs.get('sectorsRaw')
        self.__low = kwargs.get('low')
        self.__crossGroup = kwargs.get('crossGroup')
        self.__integratedScore = kwargs.get('integratedScore')
        self.__reportRunTime = kwargs.get('reportRunTime')
        self.__fiveDayPriceChangeBps = kwargs.get('fiveDayPriceChangeBps')
        self.__tradeSize = kwargs.get('tradeSize')
        self.__symbolDimensions = kwargs.get('symbolDimensions')
        self.__quotingStyle = kwargs.get('quotingStyle')
        self.__scenarioGroupId = kwargs.get('scenarioGroupId')
        self.__errorMessage = kwargs.get('errorMessage')
        self.__avgTradeRateDescription = kwargs.get('avgTradeRateDescription')
        self.__midPrice = kwargs.get('midPrice')
        self.__fraction = kwargs.get('fraction')
        self.__stsCreditMarket = kwargs.get('stsCreditMarket')
        self.__assetCountShort = kwargs.get('assetCountShort')
        self.__stsEmDm = kwargs.get('stsEmDm')
        self.__tcmCostHorizon2Day = kwargs.get('tcmCostHorizon2Day')
        self.__queueInLots = kwargs.get('queueInLots')
        self.__priceRangeInTicksDescription = kwargs.get('priceRangeInTicksDescription')
        self.__date = kwargs.get('date')
        self.__tenderOfferExpirationDate = kwargs.get('tenderOfferExpirationDate')
        self.__highUnadjusted = kwargs.get('highUnadjusted')
        self.__sourceCategory = kwargs.get('sourceCategory')
        self.__volumeUnadjusted = kwargs.get('volumeUnadjusted')
        self.__avgTradeRateLabel = kwargs.get('avgTradeRateLabel')
        self.__tcmCostParticipationRate5Pct = kwargs.get('tcmCostParticipationRate5Pct')
        self.__isActive = kwargs.get('isActive')
        self.__growthScore = kwargs.get('growthScore')
        self.__encodedStats = kwargs.get('encodedStats')
        self.__adjustedShortInterest = kwargs.get('adjustedShortInterest')
        self.__askSize = kwargs.get('askSize')
        self.__mdapiType = kwargs.get('mdapiType')
        self.__group = kwargs.get('group')
        self.__estimatedSpread = kwargs.get('estimatedSpread')
        self.__resource = kwargs.get('resource')
        self.__created = kwargs.get('created')
        self.__tcmCost = kwargs.get('tcmCost')
        self.__sustainJapan = kwargs.get('sustainJapan')
        self.__navSpread = kwargs.get('navSpread')
        self.__bidPrice = kwargs.get('bidPrice')
        self.__hedgeTrackingError = kwargs.get('hedgeTrackingError')
        self.__marketCapCategory = kwargs.get('marketCapCategory')
        self.__historicalVolume = kwargs.get('historicalVolume')
        self.__esNumericPercentile = kwargs.get('esNumericPercentile')
        self.__strikePrice = kwargs.get('strikePrice')
        self.__eventStartDate = kwargs.get('eventStartDate')
        self.__calSpreadMisPricing = kwargs.get('calSpreadMisPricing')
        self.__equityGamma = kwargs.get('equityGamma')
        self.__grossIncome = kwargs.get('grossIncome')
        self.__emId = kwargs.get('emId')
        self.__adjustedOpenPrice = kwargs.get('adjustedOpenPrice')
        self.__assetCountInModel = kwargs.get('assetCountInModel')
        self.__stsCreditRegion = kwargs.get('stsCreditRegion')
        self.__point = kwargs.get('point')
        self.__lender = kwargs.get('lender')
        self.__minTemperature = kwargs.get('minTemperature')
        self.__closeTime = kwargs.get('closeTime')
        self.__value = kwargs.get('value')
        self.__relativeStrike = kwargs.get('relativeStrike')
        self.__amount = kwargs.get('amount')
        self.__quantity = kwargs.get('quantity')
        self.__lendingFundAcct = kwargs.get('lendingFundAcct')
        self.__reportId = kwargs.get('reportId')
        self.__indexWeight = kwargs.get('indexWeight')
        self.__rebate = kwargs.get('rebate')
        self.__trader = kwargs.get('trader')
        self.__factorCategory = kwargs.get('factorCategory')
        self.__impliedVolatility = kwargs.get('impliedVolatility')
        self.__spread = kwargs.get('spread')
        self.__stsRatesMaturity = kwargs.get('stsRatesMaturity')
        self.__equityDelta = kwargs.get('equityDelta')
        self.__grossWeight = kwargs.get('grossWeight')
        self.__listed = kwargs.get('listed')
        self.__tcmCostHorizon6Hour = kwargs.get('tcmCostHorizon6Hour')
        self.__g10Currency = kwargs.get('g10Currency')
        self.__shockStyle = kwargs.get('shockStyle')
        self.__relativePeriod = kwargs.get('relativePeriod')
        self.__isin = kwargs.get('isin')
        self.__methodology = kwargs.get('methodology')

    @property
    def queueClockTimeLabel(self):
        return self.__queueClockTimeLabel

    @queueClockTimeLabel.setter
    def queueClockTimeLabel(self, value):
        self.__queueClockTimeLabel = value
        self._property_changed('queueClockTimeLabel')        

    @property
    def marketPnl(self) -> float:
        return self.__marketPnl

    @marketPnl.setter
    def marketPnl(self, value: float):
        self.__marketPnl = value
        self._property_changed('marketPnl')        

    @property
    def year(self) -> str:
        return self.__year

    @year.setter
    def year(self, value: str):
        self.__year = value
        self._property_changed('year')        

    @property
    def sustainAsiaExJapan(self) -> bool:
        return self.__sustainAsiaExJapan

    @sustainAsiaExJapan.setter
    def sustainAsiaExJapan(self, value: bool):
        self.__sustainAsiaExJapan = value
        self._property_changed('sustainAsiaExJapan')        

    @property
    def investmentRate(self) -> float:
        return self.__investmentRate

    @investmentRate.setter
    def investmentRate(self, value: float):
        self.__investmentRate = value
        self._property_changed('investmentRate')        

    @property
    def assetClassificationsGicsSubIndustry(self) -> str:
        return self.__assetClassificationsGicsSubIndustry

    @assetClassificationsGicsSubIndustry.setter
    def assetClassificationsGicsSubIndustry(self, value: str):
        self.__assetClassificationsGicsSubIndustry = value
        self._property_changed('assetClassificationsGicsSubIndustry')        

    @property
    def bidUnadjusted(self) -> float:
        return self.__bidUnadjusted

    @bidUnadjusted.setter
    def bidUnadjusted(self, value: float):
        self.__bidUnadjusted = value
        self._property_changed('bidUnadjusted')        

    @property
    def economicTermsHash(self) -> str:
        return self.__economicTermsHash

    @economicTermsHash.setter
    def economicTermsHash(self, value: str):
        self.__economicTermsHash = value
        self._property_changed('economicTermsHash')        

    @property
    def neighbourAssetId(self) -> str:
        return self.__neighbourAssetId

    @neighbourAssetId.setter
    def neighbourAssetId(self, value: str):
        self.__neighbourAssetId = value
        self._property_changed('neighbourAssetId')        

    @property
    def simonIntlAssetTags(self) -> Tuple[str, ...]:
        return self.__simonIntlAssetTags

    @simonIntlAssetTags.setter
    def simonIntlAssetTags(self, value: Tuple[str, ...]):
        self.__simonIntlAssetTags = value
        self._property_changed('simonIntlAssetTags')        

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value
        self._property_changed('path')        

    @property
    def availableInventory(self) -> float:
        return self.__availableInventory

    @availableInventory.setter
    def availableInventory(self, value: float):
        self.__availableInventory = value
        self._property_changed('availableInventory')        

    @property
    def clientContact(self) -> str:
        return self.__clientContact

    @clientContact.setter
    def clientContact(self, value: str):
        self.__clientContact = value
        self._property_changed('clientContact')        

    @property
    def est1DayCompletePct(self) -> float:
        return self.__est1DayCompletePct

    @est1DayCompletePct.setter
    def est1DayCompletePct(self, value: float):
        self.__est1DayCompletePct = value
        self._property_changed('est1DayCompletePct')        

    @property
    def rank(self) -> float:
        return self.__rank

    @rank.setter
    def rank(self, value: float):
        self.__rank = value
        self._property_changed('rank')        

    @property
    def dataSetCategory(self) -> str:
        return self.__dataSetCategory

    @dataSetCategory.setter
    def dataSetCategory(self, value: str):
        self.__dataSetCategory = value
        self._property_changed('dataSetCategory')        

    @property
    def createdById(self) -> str:
        return self.__createdById

    @createdById.setter
    def createdById(self, value: str):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def vehicleType(self) -> str:
        return self.__vehicleType

    @vehicleType.setter
    def vehicleType(self, value: str):
        self.__vehicleType = value
        self._property_changed('vehicleType')        

    @property
    def dailyRisk(self) -> float:
        return self.__dailyRisk

    @dailyRisk.setter
    def dailyRisk(self, value: float):
        self.__dailyRisk = value
        self._property_changed('dailyRisk')        

    @property
    def bosInBpsLabel(self):
        return self.__bosInBpsLabel

    @bosInBpsLabel.setter
    def bosInBpsLabel(self, value):
        self.__bosInBpsLabel = value
        self._property_changed('bosInBpsLabel')        

    @property
    def marketDataType(self) -> str:
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value: str):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def sentimentScore(self) -> float:
        return self.__sentimentScore

    @sentimentScore.setter
    def sentimentScore(self, value: float):
        self.__sentimentScore = value
        self._property_changed('sentimentScore')        

    @property
    def bosInBps(self) -> float:
        return self.__bosInBps

    @bosInBps.setter
    def bosInBps(self, value: float):
        self.__bosInBps = value
        self._property_changed('bosInBps')        

    @property
    def pointClass(self) -> str:
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value: str):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def fxSpot(self) -> float:
        return self.__fxSpot

    @fxSpot.setter
    def fxSpot(self, value: float):
        self.__fxSpot = value
        self._property_changed('fxSpot')        

    @property
    def bidLow(self) -> float:
        return self.__bidLow

    @bidLow.setter
    def bidLow(self, value: float):
        self.__bidLow = value
        self._property_changed('bidLow')        

    @property
    def valuePrevious(self) -> str:
        return self.__valuePrevious

    @valuePrevious.setter
    def valuePrevious(self, value: str):
        self.__valuePrevious = value
        self._property_changed('valuePrevious')        

    @property
    def fairVarianceVolatility(self) -> float:
        return self.__fairVarianceVolatility

    @fairVarianceVolatility.setter
    def fairVarianceVolatility(self, value: float):
        self.__fairVarianceVolatility = value
        self._property_changed('fairVarianceVolatility')        

    @property
    def avgTradeRate(self) -> float:
        return self.__avgTradeRate

    @avgTradeRate.setter
    def avgTradeRate(self, value: float):
        self.__avgTradeRate = value
        self._property_changed('avgTradeRate')        

    @property
    def shortLevel(self) -> float:
        return self.__shortLevel

    @shortLevel.setter
    def shortLevel(self, value: float):
        self.__shortLevel = value
        self._property_changed('shortLevel')        

    @property
    def hedgeVolatility(self) -> float:
        return self.__hedgeVolatility

    @hedgeVolatility.setter
    def hedgeVolatility(self, value: float):
        self.__hedgeVolatility = value
        self._property_changed('hedgeVolatility')        

    @property
    def version(self) -> float:
        return self.__version

    @version.setter
    def version(self, value: float):
        self.__version = value
        self._property_changed('version')        

    @property
    def tags(self) -> Tuple[str, ...]:
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def underlyingAssetId(self) -> str:
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value: str):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        

    @property
    def clientExposure(self) -> float:
        return self.__clientExposure

    @clientExposure.setter
    def clientExposure(self, value: float):
        self.__clientExposure = value
        self._property_changed('clientExposure')        

    @property
    def correlation(self) -> float:
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def exposure(self) -> float:
        return self.__exposure

    @exposure.setter
    def exposure(self, value: float):
        self.__exposure = value
        self._property_changed('exposure')        

    @property
    def gsSustainSubSector(self) -> str:
        return self.__gsSustainSubSector

    @gsSustainSubSector.setter
    def gsSustainSubSector(self, value: str):
        self.__gsSustainSubSector = value
        self._property_changed('gsSustainSubSector')        

    @property
    def domain(self) -> str:
        return self.__domain

    @domain.setter
    def domain(self, value: str):
        self.__domain = value
        self._property_changed('domain')        

    @property
    def marketDataAsset(self) -> str:
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value: str):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def forwardTenor(self) -> str:
        return self.__forwardTenor

    @forwardTenor.setter
    def forwardTenor(self, value: str):
        self.__forwardTenor = value
        self._property_changed('forwardTenor')        

    @property
    def unadjustedHigh(self) -> float:
        return self.__unadjustedHigh

    @unadjustedHigh.setter
    def unadjustedHigh(self, value: float):
        self.__unadjustedHigh = value
        self._property_changed('unadjustedHigh')        

    @property
    def sourceImportance(self) -> float:
        return self.__sourceImportance

    @sourceImportance.setter
    def sourceImportance(self, value: float):
        self.__sourceImportance = value
        self._property_changed('sourceImportance')        

    @property
    def eid(self) -> str:
        return self.__eid

    @eid.setter
    def eid(self, value: str):
        self.__eid = value
        self._property_changed('eid')        

    @property
    def jsn(self) -> str:
        return self.__jsn

    @jsn.setter
    def jsn(self, value: str):
        self.__jsn = value
        self._property_changed('jsn')        

    @property
    def relativeReturnQtd(self) -> float:
        return self.__relativeReturnQtd

    @relativeReturnQtd.setter
    def relativeReturnQtd(self, value: float):
        self.__relativeReturnQtd = value
        self._property_changed('relativeReturnQtd')        

    @property
    def displayName(self) -> str:
        return self.__displayName

    @displayName.setter
    def displayName(self, value: str):
        self.__displayName = value
        self._property_changed('displayName')        

    @property
    def minutesToTrade100Pct(self) -> float:
        return self.__minutesToTrade100Pct

    @minutesToTrade100Pct.setter
    def minutesToTrade100Pct(self, value: float):
        self.__minutesToTrade100Pct = value
        self._property_changed('minutesToTrade100Pct')        

    @property
    def marketModelId(self) -> str:
        return self.__marketModelId

    @marketModelId.setter
    def marketModelId(self, value: str):
        self.__marketModelId = value
        self._property_changed('marketModelId')        

    @property
    def quoteType(self) -> str:
        return self.__quoteType

    @quoteType.setter
    def quoteType(self, value: str):
        self.__quoteType = value
        self._property_changed('quoteType')        

    @property
    def tenor(self) -> str:
        return self.__tenor

    @tenor.setter
    def tenor(self, value: str):
        self.__tenor = value
        self._property_changed('tenor')        

    @property
    def esPolicyPercentile(self) -> float:
        return self.__esPolicyPercentile

    @esPolicyPercentile.setter
    def esPolicyPercentile(self, value: float):
        self.__esPolicyPercentile = value
        self._property_changed('esPolicyPercentile')        

    @property
    def tcmCostParticipationRate75Pct(self) -> float:
        return self.__tcmCostParticipationRate75Pct

    @tcmCostParticipationRate75Pct.setter
    def tcmCostParticipationRate75Pct(self, value: float):
        self.__tcmCostParticipationRate75Pct = value
        self._property_changed('tcmCostParticipationRate75Pct')        

    @property
    def close(self) -> float:
        return self.__close

    @close.setter
    def close(self, value: float):
        self.__close = value
        self._property_changed('close')        

    @property
    def tcmCostParticipationRate100Pct(self) -> float:
        return self.__tcmCostParticipationRate100Pct

    @tcmCostParticipationRate100Pct.setter
    def tcmCostParticipationRate100Pct(self, value: float):
        self.__tcmCostParticipationRate100Pct = value
        self._property_changed('tcmCostParticipationRate100Pct')        

    @property
    def disclaimer(self) -> str:
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: str):
        self.__disclaimer = value
        self._property_changed('disclaimer')        

    @property
    def measureIdx(self) -> int:
        return self.__measureIdx

    @measureIdx.setter
    def measureIdx(self, value: int):
        self.__measureIdx = value
        self._property_changed('measureIdx')        

    @property
    def a(self) -> float:
        return self.__a

    @a.setter
    def a(self, value: float):
        self.__a = value
        self._property_changed('a')        

    @property
    def b(self) -> float:
        return self.__b

    @b.setter
    def b(self, value: float):
        self.__b = value
        self._property_changed('b')        

    @property
    def loanFee(self) -> float:
        return self.__loanFee

    @loanFee.setter
    def loanFee(self, value: float):
        self.__loanFee = value
        self._property_changed('loanFee')        

    @property
    def c(self) -> float:
        return self.__c

    @c.setter
    def c(self, value: float):
        self.__c = value
        self._property_changed('c')        

    @property
    def equityVega(self) -> float:
        return self.__equityVega

    @equityVega.setter
    def equityVega(self, value: float):
        self.__equityVega = value
        self._property_changed('equityVega')        

    @property
    def deploymentVersion(self) -> str:
        return self.__deploymentVersion

    @deploymentVersion.setter
    def deploymentVersion(self, value: str):
        self.__deploymentVersion = value
        self._property_changed('deploymentVersion')        

    @property
    def fiveDayMove(self) -> float:
        return self.__fiveDayMove

    @fiveDayMove.setter
    def fiveDayMove(self, value: float):
        self.__fiveDayMove = value
        self._property_changed('fiveDayMove')        

    @property
    def borrower(self) -> str:
        return self.__borrower

    @borrower.setter
    def borrower(self, value: str):
        self.__borrower = value
        self._property_changed('borrower')        

    @property
    def performanceContribution(self) -> float:
        return self.__performanceContribution

    @performanceContribution.setter
    def performanceContribution(self, value: float):
        self.__performanceContribution = value
        self._property_changed('performanceContribution')        

    @property
    def targetNotional(self) -> float:
        return self.__targetNotional

    @targetNotional.setter
    def targetNotional(self, value: float):
        self.__targetNotional = value
        self._property_changed('targetNotional')        

    @property
    def fillLegId(self) -> str:
        return self.__fillLegId

    @fillLegId.setter
    def fillLegId(self, value: str):
        self.__fillLegId = value
        self._property_changed('fillLegId')        

    @property
    def delisted(self) -> str:
        return self.__delisted

    @delisted.setter
    def delisted(self, value: str):
        self.__delisted = value
        self._property_changed('delisted')        

    @property
    def rationale(self) -> str:
        return self.__rationale

    @rationale.setter
    def rationale(self, value: str):
        self.__rationale = value
        self._property_changed('rationale')        

    @property
    def regionalFocus(self) -> str:
        return self.__regionalFocus

    @regionalFocus.setter
    def regionalFocus(self, value: str):
        self.__regionalFocus = value
        self._property_changed('regionalFocus')        

    @property
    def volumePrimary(self) -> float:
        return self.__volumePrimary

    @volumePrimary.setter
    def volumePrimary(self, value: float):
        self.__volumePrimary = value
        self._property_changed('volumePrimary')        

    @property
    def series(self) -> str:
        return self.__series

    @series.setter
    def series(self, value: str):
        self.__series = value
        self._property_changed('series')        

    @property
    def simonId(self) -> str:
        return self.__simonId

    @simonId.setter
    def simonId(self, value: str):
        self.__simonId = value
        self._property_changed('simonId')        

    @property
    def newIdeasQtd(self) -> float:
        return self.__newIdeasQtd

    @newIdeasQtd.setter
    def newIdeasQtd(self, value: float):
        self.__newIdeasQtd = value
        self._property_changed('newIdeasQtd')        

    @property
    def adjustedAskPrice(self) -> float:
        return self.__adjustedAskPrice

    @adjustedAskPrice.setter
    def adjustedAskPrice(self, value: float):
        self.__adjustedAskPrice = value
        self._property_changed('adjustedAskPrice')        

    @property
    def quarter(self) -> str:
        return self.__quarter

    @quarter.setter
    def quarter(self, value: str):
        self.__quarter = value
        self._property_changed('quarter')        

    @property
    def factorUniverse(self) -> str:
        return self.__factorUniverse

    @factorUniverse.setter
    def factorUniverse(self, value: str):
        self.__factorUniverse = value
        self._property_changed('factorUniverse')        

    @property
    def eventCategory(self) -> str:
        return self.__eventCategory

    @eventCategory.setter
    def eventCategory(self, value: str):
        self.__eventCategory = value
        self._property_changed('eventCategory')        

    @property
    def impliedNormalVolatility(self) -> float:
        return self.__impliedNormalVolatility

    @impliedNormalVolatility.setter
    def impliedNormalVolatility(self, value: float):
        self.__impliedNormalVolatility = value
        self._property_changed('impliedNormalVolatility')        

    @property
    def unadjustedOpen(self) -> float:
        return self.__unadjustedOpen

    @unadjustedOpen.setter
    def unadjustedOpen(self, value: float):
        self.__unadjustedOpen = value
        self._property_changed('unadjustedOpen')        

    @property
    def arrivalRt(self) -> float:
        return self.__arrivalRt

    @arrivalRt.setter
    def arrivalRt(self, value: float):
        self.__arrivalRt = value
        self._property_changed('arrivalRt')        

    @property
    def transactionCost(self) -> float:
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value: float):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def servicingCostShortPnl(self) -> float:
        return self.__servicingCostShortPnl

    @servicingCostShortPnl.setter
    def servicingCostShortPnl(self, value: float):
        self.__servicingCostShortPnl = value
        self._property_changed('servicingCostShortPnl')        

    @property
    def bidAskSpread(self) -> float:
        return self.__bidAskSpread

    @bidAskSpread.setter
    def bidAskSpread(self, value: float):
        self.__bidAskSpread = value
        self._property_changed('bidAskSpread')        

    @property
    def optionType(self) -> str:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: str):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def tcmCostHorizon3Hour(self) -> float:
        return self.__tcmCostHorizon3Hour

    @tcmCostHorizon3Hour.setter
    def tcmCostHorizon3Hour(self, value: float):
        self.__tcmCostHorizon3Hour = value
        self._property_changed('tcmCostHorizon3Hour')        

    @property
    def clusterDescription(self) -> str:
        return self.__clusterDescription

    @clusterDescription.setter
    def clusterDescription(self, value: str):
        self.__clusterDescription = value
        self._property_changed('clusterDescription')        

    @property
    def positionAmount(self) -> float:
        return self.__positionAmount

    @positionAmount.setter
    def positionAmount(self, value: float):
        self.__positionAmount = value
        self._property_changed('positionAmount')        

    @property
    def numberOfPositions(self) -> float:
        return self.__numberOfPositions

    @numberOfPositions.setter
    def numberOfPositions(self, value: float):
        self.__numberOfPositions = value
        self._property_changed('numberOfPositions')        

    @property
    def windSpeed(self) -> float:
        return self.__windSpeed

    @windSpeed.setter
    def windSpeed(self, value: float):
        self.__windSpeed = value
        self._property_changed('windSpeed')        

    @property
    def openUnadjusted(self) -> float:
        return self.__openUnadjusted

    @openUnadjusted.setter
    def openUnadjusted(self, value: float):
        self.__openUnadjusted = value
        self._property_changed('openUnadjusted')        

    @property
    def maRank(self) -> float:
        return self.__maRank

    @maRank.setter
    def maRank(self, value: float):
        self.__maRank = value
        self._property_changed('maRank')        

    @property
    def eventStartDateTime(self) -> datetime.datetime:
        return self.__eventStartDateTime

    @eventStartDateTime.setter
    def eventStartDateTime(self, value: datetime.datetime):
        self.__eventStartDateTime = value
        self._property_changed('eventStartDateTime')        

    @property
    def askPrice(self) -> float:
        return self.__askPrice

    @askPrice.setter
    def askPrice(self, value: float):
        self.__askPrice = value
        self._property_changed('askPrice')        

    @property
    def eventId(self) -> str:
        return self.__eventId

    @eventId.setter
    def eventId(self, value: str):
        self.__eventId = value
        self._property_changed('eventId')        

    @property
    def dataProduct(self) -> str:
        return self.__dataProduct

    @dataProduct.setter
    def dataProduct(self, value: str):
        self.__dataProduct = value
        self._property_changed('dataProduct')        

    @property
    def sectors(self) -> Tuple[str, ...]:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: Tuple[str, ...]):
        self.__sectors = value
        self._property_changed('sectors')        

    @property
    def annualizedTrackingError(self) -> float:
        return self.__annualizedTrackingError

    @annualizedTrackingError.setter
    def annualizedTrackingError(self, value: float):
        self.__annualizedTrackingError = value
        self._property_changed('annualizedTrackingError')        

    @property
    def volSwap(self) -> float:
        return self.__volSwap

    @volSwap.setter
    def volSwap(self, value: float):
        self.__volSwap = value
        self._property_changed('volSwap')        

    @property
    def annualizedRisk(self) -> float:
        return self.__annualizedRisk

    @annualizedRisk.setter
    def annualizedRisk(self, value: float):
        self.__annualizedRisk = value
        self._property_changed('annualizedRisk')        

    @property
    def corporateAction(self) -> bool:
        return self.__corporateAction

    @corporateAction.setter
    def corporateAction(self, value: bool):
        self.__corporateAction = value
        self._property_changed('corporateAction')        

    @property
    def conviction(self) -> str:
        return self.__conviction

    @conviction.setter
    def conviction(self, value: str):
        self.__conviction = value
        self._property_changed('conviction')        

    @property
    def grossExposure(self) -> float:
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value: float):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def benchmarkMaturity(self) -> str:
        return self.__benchmarkMaturity

    @benchmarkMaturity.setter
    def benchmarkMaturity(self, value: str):
        self.__benchmarkMaturity = value
        self._property_changed('benchmarkMaturity')        

    @property
    def volumeComposite(self) -> float:
        return self.__volumeComposite

    @volumeComposite.setter
    def volumeComposite(self, value: float):
        self.__volumeComposite = value
        self._property_changed('volumeComposite')        

    @property
    def volume(self) -> float:
        return self.__volume

    @volume.setter
    def volume(self, value: float):
        self.__volume = value
        self._property_changed('volume')        

    @property
    def adv(self) -> float:
        return self.__adv

    @adv.setter
    def adv(self, value: float):
        self.__adv = value
        self._property_changed('adv')        

    @property
    def stsFxCurrency(self) -> str:
        return self.__stsFxCurrency

    @stsFxCurrency.setter
    def stsFxCurrency(self, value: str):
        self.__stsFxCurrency = value
        self._property_changed('stsFxCurrency')        

    @property
    def wpk(self) -> str:
        return self.__wpk

    @wpk.setter
    def wpk(self, value: str):
        self.__wpk = value
        self._property_changed('wpk')        

    @property
    def shortConvictionMedium(self) -> float:
        return self.__shortConvictionMedium

    @shortConvictionMedium.setter
    def shortConvictionMedium(self, value: float):
        self.__shortConvictionMedium = value
        self._property_changed('shortConvictionMedium')        

    @property
    def bidChange(self) -> float:
        return self.__bidChange

    @bidChange.setter
    def bidChange(self, value: float):
        self.__bidChange = value
        self._property_changed('bidChange')        

    @property
    def exchange(self) -> str:
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expiration(self) -> str:
        return self.__expiration

    @expiration.setter
    def expiration(self, value: str):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def tradePrice(self) -> float:
        return self.__tradePrice

    @tradePrice.setter
    def tradePrice(self, value: float):
        self.__tradePrice = value
        self._property_changed('tradePrice')        

    @property
    def esPolicyScore(self) -> float:
        return self.__esPolicyScore

    @esPolicyScore.setter
    def esPolicyScore(self, value: float):
        self.__esPolicyScore = value
        self._property_changed('esPolicyScore')        

    @property
    def loanId(self) -> str:
        return self.__loanId

    @loanId.setter
    def loanId(self, value: str):
        self.__loanId = value
        self._property_changed('loanId')        

    @property
    def cid(self) -> str:
        return self.__cid

    @cid.setter
    def cid(self, value: str):
        self.__cid = value
        self._property_changed('cid')        

    @property
    def liquidityScore(self) -> float:
        return self.__liquidityScore

    @liquidityScore.setter
    def liquidityScore(self, value: float):
        self.__liquidityScore = value
        self._property_changed('liquidityScore')        

    @property
    def importance(self) -> float:
        return self.__importance

    @importance.setter
    def importance(self, value: float):
        self.__importance = value
        self._property_changed('importance')        

    @property
    def sourceDateSpan(self) -> float:
        return self.__sourceDateSpan

    @sourceDateSpan.setter
    def sourceDateSpan(self, value: float):
        self.__sourceDateSpan = value
        self._property_changed('sourceDateSpan')        

    @property
    def assetClassificationsGicsSector(self) -> str:
        return self.__assetClassificationsGicsSector

    @assetClassificationsGicsSector.setter
    def assetClassificationsGicsSector(self, value: str):
        self.__assetClassificationsGicsSector = value
        self._property_changed('assetClassificationsGicsSector')        

    @property
    def underlyingDataSetId(self) -> str:
        return self.__underlyingDataSetId

    @underlyingDataSetId.setter
    def underlyingDataSetId(self, value: str):
        self.__underlyingDataSetId = value
        self._property_changed('underlyingDataSetId')        

    @property
    def stsAssetName(self) -> str:
        return self.__stsAssetName

    @stsAssetName.setter
    def stsAssetName(self, value: str):
        self.__stsAssetName = value
        self._property_changed('stsAssetName')        

    @property
    def closeUnadjusted(self) -> float:
        return self.__closeUnadjusted

    @closeUnadjusted.setter
    def closeUnadjusted(self, value: float):
        self.__closeUnadjusted = value
        self._property_changed('closeUnadjusted')        

    @property
    def valueUnit(self) -> str:
        return self.__valueUnit

    @valueUnit.setter
    def valueUnit(self, value: str):
        self.__valueUnit = value
        self._property_changed('valueUnit')        

    @property
    def bidHigh(self) -> float:
        return self.__bidHigh

    @bidHigh.setter
    def bidHigh(self, value: float):
        self.__bidHigh = value
        self._property_changed('bidHigh')        

    @property
    def adjustedLowPrice(self) -> float:
        return self.__adjustedLowPrice

    @adjustedLowPrice.setter
    def adjustedLowPrice(self, value: float):
        self.__adjustedLowPrice = value
        self._property_changed('adjustedLowPrice')        

    @property
    def netExposureClassification(self) -> str:
        return self.__netExposureClassification

    @netExposureClassification.setter
    def netExposureClassification(self, value: str):
        self.__netExposureClassification = value
        self._property_changed('netExposureClassification')        

    @property
    def longConvictionLarge(self) -> float:
        return self.__longConvictionLarge

    @longConvictionLarge.setter
    def longConvictionLarge(self, value: float):
        self.__longConvictionLarge = value
        self._property_changed('longConvictionLarge')        

    @property
    def fairVariance(self) -> float:
        return self.__fairVariance

    @fairVariance.setter
    def fairVariance(self, value: float):
        self.__fairVariance = value
        self._property_changed('fairVariance')        

    @property
    def hitRateWtd(self) -> float:
        return self.__hitRateWtd

    @hitRateWtd.setter
    def hitRateWtd(self, value: float):
        self.__hitRateWtd = value
        self._property_changed('hitRateWtd')        

    @property
    def oad(self) -> float:
        return self.__oad

    @oad.setter
    def oad(self, value: float):
        self.__oad = value
        self._property_changed('oad')        

    @property
    def bosInBpsDescription(self) -> str:
        return self.__bosInBpsDescription

    @bosInBpsDescription.setter
    def bosInBpsDescription(self, value: str):
        self.__bosInBpsDescription = value
        self._property_changed('bosInBpsDescription')        

    @property
    def lowPrice(self) -> float:
        return self.__lowPrice

    @lowPrice.setter
    def lowPrice(self, value: float):
        self.__lowPrice = value
        self._property_changed('lowPrice')        

    @property
    def realizedVolatility(self) -> float:
        return self.__realizedVolatility

    @realizedVolatility.setter
    def realizedVolatility(self, value: float):
        self.__realizedVolatility = value
        self._property_changed('realizedVolatility')        

    @property
    def rate(self) -> float:
        return self.__rate

    @rate.setter
    def rate(self, value: float):
        self.__rate = value
        self._property_changed('rate')        

    @property
    def adv22DayPct(self) -> float:
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value: float):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def alpha(self) -> float:
        return self.__alpha

    @alpha.setter
    def alpha(self, value: float):
        self.__alpha = value
        self._property_changed('alpha')        

    @property
    def client(self) -> str:
        return self.__client

    @client.setter
    def client(self, value: str):
        self.__client = value
        self._property_changed('client')        

    @property
    def company(self) -> str:
        return self.__company

    @company.setter
    def company(self, value: str):
        self.__company = value
        self._property_changed('company')        

    @property
    def convictionList(self) -> bool:
        return self.__convictionList

    @convictionList.setter
    def convictionList(self, value: bool):
        self.__convictionList = value
        self._property_changed('convictionList')        

    @property
    def priceRangeInTicksLabel(self):
        return self.__priceRangeInTicksLabel

    @priceRangeInTicksLabel.setter
    def priceRangeInTicksLabel(self, value):
        self.__priceRangeInTicksLabel = value
        self._property_changed('priceRangeInTicksLabel')        

    @property
    def ticker(self) -> str:
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self.__ticker = value
        self._property_changed('ticker')        

    @property
    def inRiskModel(self) -> bool:
        return self.__inRiskModel

    @inRiskModel.setter
    def inRiskModel(self, value: bool):
        self.__inRiskModel = value
        self._property_changed('inRiskModel')        

    @property
    def tcmCostHorizon1Day(self) -> float:
        return self.__tcmCostHorizon1Day

    @tcmCostHorizon1Day.setter
    def tcmCostHorizon1Day(self, value: float):
        self.__tcmCostHorizon1Day = value
        self._property_changed('tcmCostHorizon1Day')        

    @property
    def servicingCostLongPnl(self) -> float:
        return self.__servicingCostLongPnl

    @servicingCostLongPnl.setter
    def servicingCostLongPnl(self, value: float):
        self.__servicingCostLongPnl = value
        self._property_changed('servicingCostLongPnl')        

    @property
    def stsRatesCountry(self) -> str:
        return self.__stsRatesCountry

    @stsRatesCountry.setter
    def stsRatesCountry(self, value: str):
        self.__stsRatesCountry = value
        self._property_changed('stsRatesCountry')        

    @property
    def meetingNumber(self) -> int:
        return self.__meetingNumber

    @meetingNumber.setter
    def meetingNumber(self, value: int):
        self.__meetingNumber = value
        self._property_changed('meetingNumber')        

    @property
    def exchangeId(self) -> str:
        return self.__exchangeId

    @exchangeId.setter
    def exchangeId(self, value: str):
        self.__exchangeId = value
        self._property_changed('exchangeId')        

    @property
    def horizon(self) -> str:
        return self.__horizon

    @horizon.setter
    def horizon(self, value: str):
        self.__horizon = value
        self._property_changed('horizon')        

    @property
    def tcmCostHorizon20Day(self) -> float:
        return self.__tcmCostHorizon20Day

    @tcmCostHorizon20Day.setter
    def tcmCostHorizon20Day(self, value: float):
        self.__tcmCostHorizon20Day = value
        self._property_changed('tcmCostHorizon20Day')        

    @property
    def longLevel(self) -> float:
        return self.__longLevel

    @longLevel.setter
    def longLevel(self, value: float):
        self.__longLevel = value
        self._property_changed('longLevel')        

    @property
    def sourceValueForecast(self) -> str:
        return self.__sourceValueForecast

    @sourceValueForecast.setter
    def sourceValueForecast(self, value: str):
        self.__sourceValueForecast = value
        self._property_changed('sourceValueForecast')        

    @property
    def shortConvictionLarge(self) -> float:
        return self.__shortConvictionLarge

    @shortConvictionLarge.setter
    def shortConvictionLarge(self, value: float):
        self.__shortConvictionLarge = value
        self._property_changed('shortConvictionLarge')        

    @property
    def realm(self) -> str:
        return self.__realm

    @realm.setter
    def realm(self, value: str):
        self.__realm = value
        self._property_changed('realm')        

    @property
    def bid(self) -> float:
        return self.__bid

    @bid.setter
    def bid(self, value: float):
        self.__bid = value
        self._property_changed('bid')        

    @property
    def dataDescription(self) -> str:
        return self.__dataDescription

    @dataDescription.setter
    def dataDescription(self, value: str):
        self.__dataDescription = value
        self._property_changed('dataDescription')        

    @property
    def composite22DayAdv(self) -> float:
        return self.__composite22DayAdv

    @composite22DayAdv.setter
    def composite22DayAdv(self, value: float):
        self.__composite22DayAdv = value
        self._property_changed('composite22DayAdv')        

    @property
    def gsn(self) -> str:
        return self.__gsn

    @gsn.setter
    def gsn(self, value: str):
        self.__gsn = value
        self._property_changed('gsn')        

    @property
    def isAggressive(self) -> float:
        return self.__isAggressive

    @isAggressive.setter
    def isAggressive(self, value: float):
        self.__isAggressive = value
        self._property_changed('isAggressive')        

    @property
    def orderId(self) -> str:
        return self.__orderId

    @orderId.setter
    def orderId(self, value: str):
        self.__orderId = value
        self._property_changed('orderId')        

    @property
    def gss(self) -> str:
        return self.__gss

    @gss.setter
    def gss(self, value: str):
        self.__gss = value
        self._property_changed('gss')        

    @property
    def percentOfMediandv1m(self) -> float:
        return self.__percentOfMediandv1m

    @percentOfMediandv1m.setter
    def percentOfMediandv1m(self, value: float):
        self.__percentOfMediandv1m = value
        self._property_changed('percentOfMediandv1m')        

    @property
    def lendables(self) -> float:
        return self.__lendables

    @lendables.setter
    def lendables(self, value: float):
        self.__lendables = value
        self._property_changed('lendables')        

    @property
    def assetClass(self) -> str:
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: str):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def gsideid(self) -> str:
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: str):
        self.__gsideid = value
        self._property_changed('gsideid')        

    @property
    def bosInTicksLabel(self):
        return self.__bosInTicksLabel

    @bosInTicksLabel.setter
    def bosInTicksLabel(self, value):
        self.__bosInTicksLabel = value
        self._property_changed('bosInTicksLabel')        

    @property
    def ric(self) -> str:
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self.__ric = value
        self._property_changed('ric')        

    @property
    def positionSourceId(self) -> str:
        return self.__positionSourceId

    @positionSourceId.setter
    def positionSourceId(self, value: str):
        self.__positionSourceId = value
        self._property_changed('positionSourceId')        

    @property
    def division(self) -> str:
        return self.__division

    @division.setter
    def division(self, value: str):
        self.__division = value
        self._property_changed('division')        

    @property
    def marketCapUSD(self) -> float:
        return self.__marketCapUSD

    @marketCapUSD.setter
    def marketCapUSD(self, value: float):
        self.__marketCapUSD = value
        self._property_changed('marketCapUSD')        

    @property
    def deploymentId(self) -> float:
        return self.__deploymentId

    @deploymentId.setter
    def deploymentId(self, value: float):
        self.__deploymentId = value
        self._property_changed('deploymentId')        

    @property
    def highPrice(self) -> float:
        return self.__highPrice

    @highPrice.setter
    def highPrice(self, value: float):
        self.__highPrice = value
        self._property_changed('highPrice')        

    @property
    def shortWeight(self) -> float:
        return self.__shortWeight

    @shortWeight.setter
    def shortWeight(self, value: float):
        self.__shortWeight = value
        self._property_changed('shortWeight')        

    @property
    def absoluteShares(self) -> float:
        return self.__absoluteShares

    @absoluteShares.setter
    def absoluteShares(self, value: float):
        self.__absoluteShares = value
        self._property_changed('absoluteShares')        

    @property
    def action(self) -> str:
        return self.__action

    @action.setter
    def action(self, value: str):
        self.__action = value
        self._property_changed('action')        

    @property
    def model(self) -> str:
        return self.__model

    @model.setter
    def model(self, value: str):
        self.__model = value
        self._property_changed('model')        

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def arrivalHaircutVwapNormalized(self) -> float:
        return self.__arrivalHaircutVwapNormalized

    @arrivalHaircutVwapNormalized.setter
    def arrivalHaircutVwapNormalized(self, value: float):
        self.__arrivalHaircutVwapNormalized = value
        self._property_changed('arrivalHaircutVwapNormalized')        

    @property
    def queueClockTimeDescription(self) -> str:
        return self.__queueClockTimeDescription

    @queueClockTimeDescription.setter
    def queueClockTimeDescription(self, value: str):
        self.__queueClockTimeDescription = value
        self._property_changed('queueClockTimeDescription')        

    @property
    def period(self) -> str:
        return self.__period

    @period.setter
    def period(self, value: str):
        self.__period = value
        self._property_changed('period')        

    @property
    def indexCreateSource(self) -> str:
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value: str):
        self.__indexCreateSource = value
        self._property_changed('indexCreateSource')        

    @property
    def fiscalQuarter(self) -> str:
        return self.__fiscalQuarter

    @fiscalQuarter.setter
    def fiscalQuarter(self, value: str):
        self.__fiscalQuarter = value
        self._property_changed('fiscalQuarter')        

    @property
    def deltaStrike(self) -> str:
        return self.__deltaStrike

    @deltaStrike.setter
    def deltaStrike(self, value: str):
        self.__deltaStrike = value
        self._property_changed('deltaStrike')        

    @property
    def marketImpact(self) -> float:
        return self.__marketImpact

    @marketImpact.setter
    def marketImpact(self, value: float):
        self.__marketImpact = value
        self._property_changed('marketImpact')        

    @property
    def eventType(self) -> str:
        return self.__eventType

    @eventType.setter
    def eventType(self, value: str):
        self.__eventType = value
        self._property_changed('eventType')        

    @property
    def assetCountLong(self) -> float:
        return self.__assetCountLong

    @assetCountLong.setter
    def assetCountLong(self, value: float):
        self.__assetCountLong = value
        self._property_changed('assetCountLong')        

    @property
    def valueActual(self) -> str:
        return self.__valueActual

    @valueActual.setter
    def valueActual(self, value: str):
        self.__valueActual = value
        self._property_changed('valueActual')        

    @property
    def bcid(self) -> str:
        return self.__bcid

    @bcid.setter
    def bcid(self, value: str):
        self.__bcid = value
        self._property_changed('bcid')        

    @property
    def originalCountry(self) -> str:
        return self.__originalCountry

    @originalCountry.setter
    def originalCountry(self, value: str):
        self.__originalCountry = value
        self._property_changed('originalCountry')        

    @property
    def touchLiquidityScore(self) -> float:
        return self.__touchLiquidityScore

    @touchLiquidityScore.setter
    def touchLiquidityScore(self, value: float):
        self.__touchLiquidityScore = value
        self._property_changed('touchLiquidityScore')        

    @property
    def field(self) -> str:
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        

    @property
    def spot(self) -> float:
        return self.__spot

    @spot.setter
    def spot(self, value: float):
        self.__spot = value
        self._property_changed('spot')        

    @property
    def expectedCompletionDate(self) -> str:
        return self.__expectedCompletionDate

    @expectedCompletionDate.setter
    def expectedCompletionDate(self, value: str):
        self.__expectedCompletionDate = value
        self._property_changed('expectedCompletionDate')        

    @property
    def loanValue(self) -> float:
        return self.__loanValue

    @loanValue.setter
    def loanValue(self, value: float):
        self.__loanValue = value
        self._property_changed('loanValue')        

    @property
    def skew(self) -> float:
        return self.__skew

    @skew.setter
    def skew(self, value: float):
        self.__skew = value
        self._property_changed('skew')        

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value
        self._property_changed('status')        

    @property
    def sustainEmergingMarkets(self) -> bool:
        return self.__sustainEmergingMarkets

    @sustainEmergingMarkets.setter
    def sustainEmergingMarkets(self, value: bool):
        self.__sustainEmergingMarkets = value
        self._property_changed('sustainEmergingMarkets')        

    @property
    def eventDateTime(self) -> datetime.datetime:
        return self.__eventDateTime

    @eventDateTime.setter
    def eventDateTime(self, value: datetime.datetime):
        self.__eventDateTime = value
        self._property_changed('eventDateTime')        

    @property
    def totalReturnPrice(self) -> float:
        return self.__totalReturnPrice

    @totalReturnPrice.setter
    def totalReturnPrice(self, value: float):
        self.__totalReturnPrice = value
        self._property_changed('totalReturnPrice')        

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, value: str):
        self.__city = value
        self._property_changed('city')        

    @property
    def eventSource(self) -> str:
        return self.__eventSource

    @eventSource.setter
    def eventSource(self, value: str):
        self.__eventSource = value
        self._property_changed('eventSource')        

    @property
    def qisPermNo(self) -> str:
        return self.__qisPermNo

    @qisPermNo.setter
    def qisPermNo(self, value: str):
        self.__qisPermNo = value
        self._property_changed('qisPermNo')        

    @property
    def hitRateYtd(self) -> float:
        return self.__hitRateYtd

    @hitRateYtd.setter
    def hitRateYtd(self, value: float):
        self.__hitRateYtd = value
        self._property_changed('hitRateYtd')        

    @property
    def stsCommodity(self) -> str:
        return self.__stsCommodity

    @stsCommodity.setter
    def stsCommodity(self, value: str):
        self.__stsCommodity = value
        self._property_changed('stsCommodity')        

    @property
    def stsCommoditySector(self) -> str:
        return self.__stsCommoditySector

    @stsCommoditySector.setter
    def stsCommoditySector(self, value: str):
        self.__stsCommoditySector = value
        self._property_changed('stsCommoditySector')        

    @property
    def salesCoverage(self) -> str:
        return self.__salesCoverage

    @salesCoverage.setter
    def salesCoverage(self, value: str):
        self.__salesCoverage = value
        self._property_changed('salesCoverage')        

    @property
    def shortExposure(self) -> float:
        return self.__shortExposure

    @shortExposure.setter
    def shortExposure(self, value: float):
        self.__shortExposure = value
        self._property_changed('shortExposure')        

    @property
    def esScore(self) -> float:
        return self.__esScore

    @esScore.setter
    def esScore(self, value: float):
        self.__esScore = value
        self._property_changed('esScore')        

    @property
    def tcmCostParticipationRate10Pct(self) -> float:
        return self.__tcmCostParticipationRate10Pct

    @tcmCostParticipationRate10Pct.setter
    def tcmCostParticipationRate10Pct(self, value: float):
        self.__tcmCostParticipationRate10Pct = value
        self._property_changed('tcmCostParticipationRate10Pct')        

    @property
    def eventTime(self) -> str:
        return self.__eventTime

    @eventTime.setter
    def eventTime(self, value: str):
        self.__eventTime = value
        self._property_changed('eventTime')        

    @property
    def positionSourceName(self) -> str:
        return self.__positionSourceName

    @positionSourceName.setter
    def positionSourceName(self, value: str):
        self.__positionSourceName = value
        self._property_changed('positionSourceName')        

    @property
    def priceRangeInTicks(self) -> float:
        return self.__priceRangeInTicks

    @priceRangeInTicks.setter
    def priceRangeInTicks(self, value: float):
        self.__priceRangeInTicks = value
        self._property_changed('priceRangeInTicks')        

    @property
    def deliveryDate(self) -> datetime.date:
        return self.__deliveryDate

    @deliveryDate.setter
    def deliveryDate(self, value: datetime.date):
        self.__deliveryDate = value
        self._property_changed('deliveryDate')        

    @property
    def arrivalHaircutVwap(self) -> float:
        return self.__arrivalHaircutVwap

    @arrivalHaircutVwap.setter
    def arrivalHaircutVwap(self, value: float):
        self.__arrivalHaircutVwap = value
        self._property_changed('arrivalHaircutVwap')        

    @property
    def interestRate(self) -> float:
        return self.__interestRate

    @interestRate.setter
    def interestRate(self, value: float):
        self.__interestRate = value
        self._property_changed('interestRate')        

    @property
    def executionDays(self) -> float:
        return self.__executionDays

    @executionDays.setter
    def executionDays(self, value: float):
        self.__executionDays = value
        self._property_changed('executionDays')        

    @property
    def pctChange(self) -> float:
        return self.__pctChange

    @pctChange.setter
    def pctChange(self, value: float):
        self.__pctChange = value
        self._property_changed('pctChange')        

    @property
    def side(self) -> str:
        return self.__side

    @side.setter
    def side(self, value: str):
        self.__side = value
        self._property_changed('side')        

    @property
    def numberOfRolls(self) -> int:
        return self.__numberOfRolls

    @numberOfRolls.setter
    def numberOfRolls(self, value: int):
        self.__numberOfRolls = value
        self._property_changed('numberOfRolls')        

    @property
    def agentLenderFee(self) -> float:
        return self.__agentLenderFee

    @agentLenderFee.setter
    def agentLenderFee(self, value: float):
        self.__agentLenderFee = value
        self._property_changed('agentLenderFee')        

    @property
    def complianceRestrictedStatus(self) -> str:
        return self.__complianceRestrictedStatus

    @complianceRestrictedStatus.setter
    def complianceRestrictedStatus(self, value: str):
        self.__complianceRestrictedStatus = value
        self._property_changed('complianceRestrictedStatus')        

    @property
    def forward(self) -> float:
        return self.__forward

    @forward.setter
    def forward(self, value: float):
        self.__forward = value
        self._property_changed('forward')        

    @property
    def borrowFee(self) -> float:
        return self.__borrowFee

    @borrowFee.setter
    def borrowFee(self, value: float):
        self.__borrowFee = value
        self._property_changed('borrowFee')        

    @property
    def strike(self) -> float:
        return self.__strike

    @strike.setter
    def strike(self, value: float):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def updateTime(self) -> datetime.datetime:
        return self.__updateTime

    @updateTime.setter
    def updateTime(self, value: datetime.datetime):
        self.__updateTime = value
        self._property_changed('updateTime')        

    @property
    def loanSpread(self) -> float:
        return self.__loanSpread

    @loanSpread.setter
    def loanSpread(self, value: float):
        self.__loanSpread = value
        self._property_changed('loanSpread')        

    @property
    def tcmCostHorizon12Hour(self) -> float:
        return self.__tcmCostHorizon12Hour

    @tcmCostHorizon12Hour.setter
    def tcmCostHorizon12Hour(self, value: float):
        self.__tcmCostHorizon12Hour = value
        self._property_changed('tcmCostHorizon12Hour')        

    @property
    def dewPoint(self) -> float:
        return self.__dewPoint

    @dewPoint.setter
    def dewPoint(self, value: float):
        self.__dewPoint = value
        self._property_changed('dewPoint')        

    @property
    def researchCommission(self) -> float:
        return self.__researchCommission

    @researchCommission.setter
    def researchCommission(self, value: float):
        self.__researchCommission = value
        self._property_changed('researchCommission')        

    @property
    def bbid(self) -> str:
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self.__bbid = value
        self._property_changed('bbid')        

    @property
    def assetClassificationsRiskCountryCode(self) -> str:
        return self.__assetClassificationsRiskCountryCode

    @assetClassificationsRiskCountryCode.setter
    def assetClassificationsRiskCountryCode(self, value: str):
        self.__assetClassificationsRiskCountryCode = value
        self._property_changed('assetClassificationsRiskCountryCode')        

    @property
    def eventStatus(self) -> str:
        return self.__eventStatus

    @eventStatus.setter
    def eventStatus(self, value: str):
        self.__eventStatus = value
        self._property_changed('eventStatus')        

    @property
    def effectiveDate(self) -> datetime.date:
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: datetime.date):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def return_(self) -> float:
        return self.__return

    @return_.setter
    def return_(self, value: float):
        self.__return = value
        self._property_changed('return')        

    @property
    def maxTemperature(self) -> float:
        return self.__maxTemperature

    @maxTemperature.setter
    def maxTemperature(self, value: float):
        self.__maxTemperature = value
        self._property_changed('maxTemperature')        

    @property
    def acquirerShareholderMeetingDate(self) -> str:
        return self.__acquirerShareholderMeetingDate

    @acquirerShareholderMeetingDate.setter
    def acquirerShareholderMeetingDate(self, value: str):
        self.__acquirerShareholderMeetingDate = value
        self._property_changed('acquirerShareholderMeetingDate')        

    @property
    def arrivalMidNormalized(self) -> float:
        return self.__arrivalMidNormalized

    @arrivalMidNormalized.setter
    def arrivalMidNormalized(self, value: float):
        self.__arrivalMidNormalized = value
        self._property_changed('arrivalMidNormalized')        

    @property
    def rating(self) -> str:
        return self.__rating

    @rating.setter
    def rating(self, value: str):
        self.__rating = value
        self._property_changed('rating')        

    @property
    def arrivalRtNormalized(self) -> float:
        return self.__arrivalRtNormalized

    @arrivalRtNormalized.setter
    def arrivalRtNormalized(self, value: float):
        self.__arrivalRtNormalized = value
        self._property_changed('arrivalRtNormalized')        

    @property
    def performanceFee(self) -> Union[float, Op]:
        return self.__performanceFee

    @performanceFee.setter
    def performanceFee(self, value: Union[float, Op]):
        self.__performanceFee = value
        self._property_changed('performanceFee')        

    @property
    def reportType(self) -> str:
        return self.__reportType

    @reportType.setter
    def reportType(self, value: str):
        self.__reportType = value
        self._property_changed('reportType')        

    @property
    def sourceURL(self) -> str:
        return self.__sourceURL

    @sourceURL.setter
    def sourceURL(self, value: str):
        self.__sourceURL = value
        self._property_changed('sourceURL')        

    @property
    def estimatedReturn(self) -> float:
        return self.__estimatedReturn

    @estimatedReturn.setter
    def estimatedReturn(self, value: float):
        self.__estimatedReturn = value
        self._property_changed('estimatedReturn')        

    @property
    def underlyingAssetIds(self) -> Tuple[str, ...]:
        return self.__underlyingAssetIds

    @underlyingAssetIds.setter
    def underlyingAssetIds(self, value: Tuple[str, ...]):
        self.__underlyingAssetIds = value
        self._property_changed('underlyingAssetIds')        

    @property
    def high(self) -> float:
        return self.__high

    @high.setter
    def high(self, value: float):
        self.__high = value
        self._property_changed('high')        

    @property
    def sourceLastUpdate(self) -> str:
        return self.__sourceLastUpdate

    @sourceLastUpdate.setter
    def sourceLastUpdate(self, value: str):
        self.__sourceLastUpdate = value
        self._property_changed('sourceLastUpdate')        

    @property
    def queueInLotsLabel(self):
        return self.__queueInLotsLabel

    @queueInLotsLabel.setter
    def queueInLotsLabel(self, value):
        self.__queueInLotsLabel = value
        self._property_changed('queueInLotsLabel')        

    @property
    def adv10DayPct(self) -> float:
        return self.__adv10DayPct

    @adv10DayPct.setter
    def adv10DayPct(self, value: float):
        self.__adv10DayPct = value
        self._property_changed('adv10DayPct')        

    @property
    def longConvictionMedium(self) -> float:
        return self.__longConvictionMedium

    @longConvictionMedium.setter
    def longConvictionMedium(self, value: float):
        self.__longConvictionMedium = value
        self._property_changed('longConvictionMedium')        

    @property
    def eventName(self) -> str:
        return self.__eventName

    @eventName.setter
    def eventName(self, value: str):
        self.__eventName = value
        self._property_changed('eventName')        

    @property
    def annualRisk(self) -> float:
        return self.__annualRisk

    @annualRisk.setter
    def annualRisk(self, value: float):
        self.__annualRisk = value
        self._property_changed('annualRisk')        

    @property
    def dailyTrackingError(self) -> float:
        return self.__dailyTrackingError

    @dailyTrackingError.setter
    def dailyTrackingError(self, value: float):
        self.__dailyTrackingError = value
        self._property_changed('dailyTrackingError')        

    @property
    def unadjustedBid(self) -> float:
        return self.__unadjustedBid

    @unadjustedBid.setter
    def unadjustedBid(self, value: float):
        self.__unadjustedBid = value
        self._property_changed('unadjustedBid')        

    @property
    def gsdeer(self) -> float:
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value: float):
        self.__gsdeer = value
        self._property_changed('gsdeer')        

    @property
    def marketCap(self) -> float:
        return self.__marketCap

    @marketCap.setter
    def marketCap(self, value: float):
        self.__marketCap = value
        self._property_changed('marketCap')        

    @property
    def clusterRegion(self):
        return self.__clusterRegion

    @clusterRegion.setter
    def clusterRegion(self, value):
        self.__clusterRegion = value
        self._property_changed('clusterRegion')        

    @property
    def bbidEquivalent(self) -> str:
        return self.__bbidEquivalent

    @bbidEquivalent.setter
    def bbidEquivalent(self, value: str):
        self.__bbidEquivalent = value
        self._property_changed('bbidEquivalent')        

    @property
    def prevCloseAsk(self) -> float:
        return self.__prevCloseAsk

    @prevCloseAsk.setter
    def prevCloseAsk(self, value: float):
        self.__prevCloseAsk = value
        self._property_changed('prevCloseAsk')        

    @property
    def level(self) -> float:
        return self.__level

    @level.setter
    def level(self, value: float):
        self.__level = value
        self._property_changed('level')        

    @property
    def valoren(self) -> str:
        return self.__valoren

    @valoren.setter
    def valoren(self, value: str):
        self.__valoren = value
        self._property_changed('valoren')        

    @property
    def pressure(self) -> float:
        return self.__pressure

    @pressure.setter
    def pressure(self, value: float):
        self.__pressure = value
        self._property_changed('pressure')        

    @property
    def shortDescription(self) -> str:
        return self.__shortDescription

    @shortDescription.setter
    def shortDescription(self, value: str):
        self.__shortDescription = value
        self._property_changed('shortDescription')        

    @property
    def basis(self) -> float:
        return self.__basis

    @basis.setter
    def basis(self, value: float):
        self.__basis = value
        self._property_changed('basis')        

    @property
    def netWeight(self) -> float:
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value: float):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def hedgeId(self) -> str:
        return self.__hedgeId

    @hedgeId.setter
    def hedgeId(self, value: str):
        self.__hedgeId = value
        self._property_changed('hedgeId')        

    @property
    def portfolioManagers(self) -> Tuple[str, ...]:
        return self.__portfolioManagers

    @portfolioManagers.setter
    def portfolioManagers(self, value: Tuple[str, ...]):
        self.__portfolioManagers = value
        self._property_changed('portfolioManagers')        

    @property
    def assetParametersCommoditySector(self) -> str:
        return self.__assetParametersCommoditySector

    @assetParametersCommoditySector.setter
    def assetParametersCommoditySector(self, value: str):
        self.__assetParametersCommoditySector = value
        self._property_changed('assetParametersCommoditySector')        

    @property
    def bosInTicks(self) -> float:
        return self.__bosInTicks

    @bosInTicks.setter
    def bosInTicks(self, value: float):
        self.__bosInTicks = value
        self._property_changed('bosInTicks')        

    @property
    def tcmCostHorizon8Day(self) -> float:
        return self.__tcmCostHorizon8Day

    @tcmCostHorizon8Day.setter
    def tcmCostHorizon8Day(self, value: float):
        self.__tcmCostHorizon8Day = value
        self._property_changed('tcmCostHorizon8Day')        

    @property
    def supraStrategy(self) -> str:
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value: str):
        self.__supraStrategy = value
        self._property_changed('supraStrategy')        

    @property
    def adv5DayPct(self) -> float:
        return self.__adv5DayPct

    @adv5DayPct.setter
    def adv5DayPct(self, value: float):
        self.__adv5DayPct = value
        self._property_changed('adv5DayPct')        

    @property
    def factorSource(self) -> str:
        return self.__factorSource

    @factorSource.setter
    def factorSource(self, value: str):
        self.__factorSource = value
        self._property_changed('factorSource')        

    @property
    def leverage(self) -> float:
        return self.__leverage

    @leverage.setter
    def leverage(self, value: float):
        self.__leverage = value
        self._property_changed('leverage')        

    @property
    def submitter(self) -> str:
        return self.__submitter

    @submitter.setter
    def submitter(self, value: str):
        self.__submitter = value
        self._property_changed('submitter')        

    @property
    def notional(self) -> float:
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def esDisclosurePercentage(self) -> float:
        return self.__esDisclosurePercentage

    @esDisclosurePercentage.setter
    def esDisclosurePercentage(self, value: float):
        self.__esDisclosurePercentage = value
        self._property_changed('esDisclosurePercentage')        

    @property
    def clientShortName(self) -> str:
        return self.__clientShortName

    @clientShortName.setter
    def clientShortName(self, value: str):
        self.__clientShortName = value
        self._property_changed('clientShortName')        

    @property
    def fwdPoints(self) -> float:
        return self.__fwdPoints

    @fwdPoints.setter
    def fwdPoints(self, value: float):
        self.__fwdPoints = value
        self._property_changed('fwdPoints')        

    @property
    def groupCategory(self) -> str:
        return self.__groupCategory

    @groupCategory.setter
    def groupCategory(self, value: str):
        self.__groupCategory = value
        self._property_changed('groupCategory')        

    @property
    def kpiId(self) -> str:
        return self.__kpiId

    @kpiId.setter
    def kpiId(self, value: str):
        self.__kpiId = value
        self._property_changed('kpiId')        

    @property
    def relativeReturnWtd(self) -> float:
        return self.__relativeReturnWtd

    @relativeReturnWtd.setter
    def relativeReturnWtd(self, value: float):
        self.__relativeReturnWtd = value
        self._property_changed('relativeReturnWtd')        

    @property
    def bidPlusAsk(self) -> float:
        return self.__bidPlusAsk

    @bidPlusAsk.setter
    def bidPlusAsk(self, value: float):
        self.__bidPlusAsk = value
        self._property_changed('bidPlusAsk')        

    @property
    def assetClassificationsRiskCountryName(self) -> str:
        return self.__assetClassificationsRiskCountryName

    @assetClassificationsRiskCountryName.setter
    def assetClassificationsRiskCountryName(self, value: str):
        self.__assetClassificationsRiskCountryName = value
        self._property_changed('assetClassificationsRiskCountryName')        

    @property
    def total(self) -> float:
        return self.__total

    @total.setter
    def total(self, value: float):
        self.__total = value
        self._property_changed('total')        

    @property
    def riskModel(self) -> str:
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value: str):
        self.__riskModel = value
        self._property_changed('riskModel')        

    @property
    def assetId(self) -> str:
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def fairValue(self) -> float:
        return self.__fairValue

    @fairValue.setter
    def fairValue(self, value: float):
        self.__fairValue = value
        self._property_changed('fairValue')        

    @property
    def adjustedHighPrice(self) -> float:
        return self.__adjustedHighPrice

    @adjustedHighPrice.setter
    def adjustedHighPrice(self, value: float):
        self.__adjustedHighPrice = value
        self._property_changed('adjustedHighPrice')        

    @property
    def openTime(self) -> datetime.datetime:
        return self.__openTime

    @openTime.setter
    def openTime(self, value: datetime.datetime):
        self.__openTime = value
        self._property_changed('openTime')        

    @property
    def beta(self) -> float:
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def direction(self) -> str:
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self.__direction = value
        self._property_changed('direction')        

    @property
    def valueForecast(self) -> str:
        return self.__valueForecast

    @valueForecast.setter
    def valueForecast(self, value: str):
        self.__valueForecast = value
        self._property_changed('valueForecast')        

    @property
    def longExposure(self) -> float:
        return self.__longExposure

    @longExposure.setter
    def longExposure(self, value: float):
        self.__longExposure = value
        self._property_changed('longExposure')        

    @property
    def positionSourceType(self) -> str:
        return self.__positionSourceType

    @positionSourceType.setter
    def positionSourceType(self, value: str):
        self.__positionSourceType = value
        self._property_changed('positionSourceType')        

    @property
    def tcmCostParticipationRate20Pct(self) -> float:
        return self.__tcmCostParticipationRate20Pct

    @tcmCostParticipationRate20Pct.setter
    def tcmCostParticipationRate20Pct(self, value: float):
        self.__tcmCostParticipationRate20Pct = value
        self._property_changed('tcmCostParticipationRate20Pct')        

    @property
    def adjustedClosePrice(self) -> float:
        return self.__adjustedClosePrice

    @adjustedClosePrice.setter
    def adjustedClosePrice(self, value: float):
        self.__adjustedClosePrice = value
        self._property_changed('adjustedClosePrice')        

    @property
    def cross(self) -> str:
        return self.__cross

    @cross.setter
    def cross(self, value: str):
        self.__cross = value
        self._property_changed('cross')        

    @property
    def lmsId(self) -> str:
        return self.__lmsId

    @lmsId.setter
    def lmsId(self, value: str):
        self.__lmsId = value
        self._property_changed('lmsId')        

    @property
    def rebateRate(self) -> float:
        return self.__rebateRate

    @rebateRate.setter
    def rebateRate(self, value: float):
        self.__rebateRate = value
        self._property_changed('rebateRate')        

    @property
    def ideaStatus(self) -> str:
        return self.__ideaStatus

    @ideaStatus.setter
    def ideaStatus(self, value: str):
        self.__ideaStatus = value
        self._property_changed('ideaStatus')        

    @property
    def participationRate(self) -> float:
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value: float):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def obfr(self) -> float:
        return self.__obfr

    @obfr.setter
    def obfr(self, value: float):
        self.__obfr = value
        self._property_changed('obfr')        

    @property
    def fxForecast(self) -> float:
        return self.__fxForecast

    @fxForecast.setter
    def fxForecast(self, value: float):
        self.__fxForecast = value
        self._property_changed('fxForecast')        

    @property
    def fixingTimeLabel(self) -> str:
        return self.__fixingTimeLabel

    @fixingTimeLabel.setter
    def fixingTimeLabel(self, value: str):
        self.__fixingTimeLabel = value
        self._property_changed('fixingTimeLabel')        

    @property
    def fillId(self) -> str:
        return self.__fillId

    @fillId.setter
    def fillId(self, value: str):
        self.__fillId = value
        self._property_changed('fillId')        

    @property
    def esNumericScore(self) -> float:
        return self.__esNumericScore

    @esNumericScore.setter
    def esNumericScore(self, value: float):
        self.__esNumericScore = value
        self._property_changed('esNumericScore')        

    @property
    def inBenchmark(self) -> bool:
        return self.__inBenchmark

    @inBenchmark.setter
    def inBenchmark(self, value: bool):
        self.__inBenchmark = value
        self._property_changed('inBenchmark')        

    @property
    def strategy(self) -> str:
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self.__strategy = value
        self._property_changed('strategy')        

    @property
    def shortInterest(self) -> float:
        return self.__shortInterest

    @shortInterest.setter
    def shortInterest(self, value: float):
        self.__shortInterest = value
        self._property_changed('shortInterest')        

    @property
    def referencePeriod(self) -> str:
        return self.__referencePeriod

    @referencePeriod.setter
    def referencePeriod(self, value: str):
        self.__referencePeriod = value
        self._property_changed('referencePeriod')        

    @property
    def adjustedVolume(self) -> float:
        return self.__adjustedVolume

    @adjustedVolume.setter
    def adjustedVolume(self, value: float):
        self.__adjustedVolume = value
        self._property_changed('adjustedVolume')        

    @property
    def queueInLotsDescription(self) -> str:
        return self.__queueInLotsDescription

    @queueInLotsDescription.setter
    def queueInLotsDescription(self, value: str):
        self.__queueInLotsDescription = value
        self._property_changed('queueInLotsDescription')        

    @property
    def pbClientId(self) -> str:
        return self.__pbClientId

    @pbClientId.setter
    def pbClientId(self, value: str):
        self.__pbClientId = value
        self._property_changed('pbClientId')        

    @property
    def ownerId(self) -> str:
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: str):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def secDB(self) -> str:
        return self.__secDB

    @secDB.setter
    def secDB(self, value: str):
        self.__secDB = value
        self._property_changed('secDB')        

    @property
    def composite10DayAdv(self) -> float:
        return self.__composite10DayAdv

    @composite10DayAdv.setter
    def composite10DayAdv(self, value: float):
        self.__composite10DayAdv = value
        self._property_changed('composite10DayAdv')        

    @property
    def objective(self) -> str:
        return self.__objective

    @objective.setter
    def objective(self, value: str):
        self.__objective = value
        self._property_changed('objective')        

    @property
    def navPrice(self) -> float:
        return self.__navPrice

    @navPrice.setter
    def navPrice(self, value: float):
        self.__navPrice = value
        self._property_changed('navPrice')        

    @property
    def ideaActivityType(self) -> str:
        return self.__ideaActivityType

    @ideaActivityType.setter
    def ideaActivityType(self, value: str):
        self.__ideaActivityType = value
        self._property_changed('ideaActivityType')        

    @property
    def precipitation(self) -> float:
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value: float):
        self.__precipitation = value
        self._property_changed('precipitation')        

    @property
    def ideaSource(self) -> str:
        return self.__ideaSource

    @ideaSource.setter
    def ideaSource(self, value: str):
        self.__ideaSource = value
        self._property_changed('ideaSource')        

    @property
    def hedgeNotional(self) -> float:
        return self.__hedgeNotional

    @hedgeNotional.setter
    def hedgeNotional(self, value: float):
        self.__hedgeNotional = value
        self._property_changed('hedgeNotional')        

    @property
    def askLow(self) -> float:
        return self.__askLow

    @askLow.setter
    def askLow(self, value: float):
        self.__askLow = value
        self._property_changed('askLow')        

    @property
    def unadjustedAsk(self) -> float:
        return self.__unadjustedAsk

    @unadjustedAsk.setter
    def unadjustedAsk(self, value: float):
        self.__unadjustedAsk = value
        self._property_changed('unadjustedAsk')        

    @property
    def betaAdjustedNetExposure(self) -> float:
        return self.__betaAdjustedNetExposure

    @betaAdjustedNetExposure.setter
    def betaAdjustedNetExposure(self, value: float):
        self.__betaAdjustedNetExposure = value
        self._property_changed('betaAdjustedNetExposure')        

    @property
    def expiry(self) -> str:
        return self.__expiry

    @expiry.setter
    def expiry(self, value: str):
        self.__expiry = value
        self._property_changed('expiry')        

    @property
    def tradingPnl(self) -> float:
        return self.__tradingPnl

    @tradingPnl.setter
    def tradingPnl(self, value: float):
        self.__tradingPnl = value
        self._property_changed('tradingPnl')        

    @property
    def strikePercentage(self) -> float:
        return self.__strikePercentage

    @strikePercentage.setter
    def strikePercentage(self, value: float):
        self.__strikePercentage = value
        self._property_changed('strikePercentage')        

    @property
    def excessReturnPrice(self) -> float:
        return self.__excessReturnPrice

    @excessReturnPrice.setter
    def excessReturnPrice(self, value: float):
        self.__excessReturnPrice = value
        self._property_changed('excessReturnPrice')        

    @property
    def givenPlusPaid(self) -> float:
        return self.__givenPlusPaid

    @givenPlusPaid.setter
    def givenPlusPaid(self, value: float):
        self.__givenPlusPaid = value
        self._property_changed('givenPlusPaid')        

    @property
    def shortConvictionSmall(self) -> float:
        return self.__shortConvictionSmall

    @shortConvictionSmall.setter
    def shortConvictionSmall(self, value: float):
        self.__shortConvictionSmall = value
        self._property_changed('shortConvictionSmall')        

    @property
    def prevCloseBid(self) -> float:
        return self.__prevCloseBid

    @prevCloseBid.setter
    def prevCloseBid(self, value: float):
        self.__prevCloseBid = value
        self._property_changed('prevCloseBid')        

    @property
    def fxPnl(self) -> float:
        return self.__fxPnl

    @fxPnl.setter
    def fxPnl(self, value: float):
        self.__fxPnl = value
        self._property_changed('fxPnl')        

    @property
    def forecast(self) -> float:
        return self.__forecast

    @forecast.setter
    def forecast(self, value: float):
        self.__forecast = value
        self._property_changed('forecast')        

    @property
    def tcmCostHorizon16Day(self) -> float:
        return self.__tcmCostHorizon16Day

    @tcmCostHorizon16Day.setter
    def tcmCostHorizon16Day(self, value: float):
        self.__tcmCostHorizon16Day = value
        self._property_changed('tcmCostHorizon16Day')        

    @property
    def pnl(self) -> float:
        return self.__pnl

    @pnl.setter
    def pnl(self, value: float):
        self.__pnl = value
        self._property_changed('pnl')        

    @property
    def assetClassificationsGicsIndustryGroup(self) -> str:
        return self.__assetClassificationsGicsIndustryGroup

    @assetClassificationsGicsIndustryGroup.setter
    def assetClassificationsGicsIndustryGroup(self, value: str):
        self.__assetClassificationsGicsIndustryGroup = value
        self._property_changed('assetClassificationsGicsIndustryGroup')        

    @property
    def unadjustedClose(self) -> float:
        return self.__unadjustedClose

    @unadjustedClose.setter
    def unadjustedClose(self, value: float):
        self.__unadjustedClose = value
        self._property_changed('unadjustedClose')        

    @property
    def tcmCostHorizon4Day(self) -> float:
        return self.__tcmCostHorizon4Day

    @tcmCostHorizon4Day.setter
    def tcmCostHorizon4Day(self, value: float):
        self.__tcmCostHorizon4Day = value
        self._property_changed('tcmCostHorizon4Day')        

    @property
    def assetClassificationsIsPrimary(self) -> bool:
        return self.__assetClassificationsIsPrimary

    @assetClassificationsIsPrimary.setter
    def assetClassificationsIsPrimary(self, value: bool):
        self.__assetClassificationsIsPrimary = value
        self._property_changed('assetClassificationsIsPrimary')        

    @property
    def styles(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[Tuple[str, ...], ...]):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def lendingSecId(self) -> str:
        return self.__lendingSecId

    @lendingSecId.setter
    def lendingSecId(self, value: str):
        self.__lendingSecId = value
        self._property_changed('lendingSecId')        

    @property
    def shortName(self) -> str:
        return self.__shortName

    @shortName.setter
    def shortName(self, value: str):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def equityTheta(self) -> float:
        return self.__equityTheta

    @equityTheta.setter
    def equityTheta(self, value: float):
        self.__equityTheta = value
        self._property_changed('equityTheta')        

    @property
    def averageFillPrice(self) -> float:
        return self.__averageFillPrice

    @averageFillPrice.setter
    def averageFillPrice(self, value: float):
        self.__averageFillPrice = value
        self._property_changed('averageFillPrice')        

    @property
    def snowfall(self) -> float:
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value: float):
        self.__snowfall = value
        self._property_changed('snowfall')        

    @property
    def mic(self) -> str:
        return self.__mic

    @mic.setter
    def mic(self, value: str):
        self.__mic = value
        self._property_changed('mic')        

    @property
    def openPrice(self) -> float:
        return self.__openPrice

    @openPrice.setter
    def openPrice(self, value: float):
        self.__openPrice = value
        self._property_changed('openPrice')        

    @property
    def autoExecState(self) -> str:
        return self.__autoExecState

    @autoExecState.setter
    def autoExecState(self, value: str):
        self.__autoExecState = value
        self._property_changed('autoExecState')        

    @property
    def depthSpreadScore(self) -> float:
        return self.__depthSpreadScore

    @depthSpreadScore.setter
    def depthSpreadScore(self, value: float):
        self.__depthSpreadScore = value
        self._property_changed('depthSpreadScore')        

    @property
    def relativeReturnYtd(self) -> float:
        return self.__relativeReturnYtd

    @relativeReturnYtd.setter
    def relativeReturnYtd(self, value: float):
        self.__relativeReturnYtd = value
        self._property_changed('relativeReturnYtd')        

    @property
    def long(self) -> float:
        return self.__long

    @long.setter
    def long(self, value: float):
        self.__long = value
        self._property_changed('long')        

    @property
    def fairVolatility(self) -> float:
        return self.__fairVolatility

    @fairVolatility.setter
    def fairVolatility(self, value: float):
        self.__fairVolatility = value
        self._property_changed('fairVolatility')        

    @property
    def dollarCross(self) -> str:
        return self.__dollarCross

    @dollarCross.setter
    def dollarCross(self, value: str):
        self.__dollarCross = value
        self._property_changed('dollarCross')        

    @property
    def longWeight(self) -> float:
        return self.__longWeight

    @longWeight.setter
    def longWeight(self, value: float):
        self.__longWeight = value
        self._property_changed('longWeight')        

    @property
    def vendor(self) -> str:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self.__vendor = value
        self._property_changed('vendor')        

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def clusterClass(self) -> str:
        return self.__clusterClass

    @clusterClass.setter
    def clusterClass(self, value: str):
        self.__clusterClass = value
        self._property_changed('clusterClass')        

    @property
    def financialReturnsScore(self) -> float:
        return self.__financialReturnsScore

    @financialReturnsScore.setter
    def financialReturnsScore(self, value: float):
        self.__financialReturnsScore = value
        self._property_changed('financialReturnsScore')        

    @property
    def netChange(self) -> float:
        return self.__netChange

    @netChange.setter
    def netChange(self, value: float):
        self.__netChange = value
        self._property_changed('netChange')        

    @property
    def nonSymbolDimensions(self) -> Tuple[str, ...]:
        return self.__nonSymbolDimensions

    @nonSymbolDimensions.setter
    def nonSymbolDimensions(self, value: Tuple[str, ...]):
        self.__nonSymbolDimensions = value
        self._property_changed('nonSymbolDimensions')        

    @property
    def bidSize(self) -> float:
        return self.__bidSize

    @bidSize.setter
    def bidSize(self, value: float):
        self.__bidSize = value
        self._property_changed('bidSize')        

    @property
    def arrivalMid(self) -> float:
        return self.__arrivalMid

    @arrivalMid.setter
    def arrivalMid(self, value: float):
        self.__arrivalMid = value
        self._property_changed('arrivalMid')        

    @property
    def assetParametersExchangeCurrency(self) -> str:
        return self.__assetParametersExchangeCurrency

    @assetParametersExchangeCurrency.setter
    def assetParametersExchangeCurrency(self, value: str):
        self.__assetParametersExchangeCurrency = value
        self._property_changed('assetParametersExchangeCurrency')        

    @property
    def unexplained(self) -> float:
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value: float):
        self.__unexplained = value
        self._property_changed('unexplained')        

    @property
    def assetClassificationsCountryName(self) -> str:
        return self.__assetClassificationsCountryName

    @assetClassificationsCountryName.setter
    def assetClassificationsCountryName(self, value: str):
        self.__assetClassificationsCountryName = value
        self._property_changed('assetClassificationsCountryName')        

    @property
    def metric(self) -> str:
        return self.__metric

    @metric.setter
    def metric(self, value: str):
        self.__metric = value
        self._property_changed('metric')        

    @property
    def newIdeasYtd(self) -> float:
        return self.__newIdeasYtd

    @newIdeasYtd.setter
    def newIdeasYtd(self, value: float):
        self.__newIdeasYtd = value
        self._property_changed('newIdeasYtd')        

    @property
    def managementFee(self) -> Union[float, Op]:
        return self.__managementFee

    @managementFee.setter
    def managementFee(self, value: Union[float, Op]):
        self.__managementFee = value
        self._property_changed('managementFee')        

    @property
    def ask(self) -> float:
        return self.__ask

    @ask.setter
    def ask(self, value: float):
        self.__ask = value
        self._property_changed('ask')        

    @property
    def impliedLognormalVolatility(self) -> float:
        return self.__impliedLognormalVolatility

    @impliedLognormalVolatility.setter
    def impliedLognormalVolatility(self, value: float):
        self.__impliedLognormalVolatility = value
        self._property_changed('impliedLognormalVolatility')        

    @property
    def closePrice(self) -> float:
        return self.__closePrice

    @closePrice.setter
    def closePrice(self, value: float):
        self.__closePrice = value
        self._property_changed('closePrice')        

    @property
    def endTime(self) -> datetime.datetime:
        return self.__endTime

    @endTime.setter
    def endTime(self, value: datetime.datetime):
        self.__endTime = value
        self._property_changed('endTime')        

    @property
    def open(self) -> float:
        return self.__open

    @open.setter
    def open(self, value: float):
        self.__open = value
        self._property_changed('open')        

    @property
    def sourceId(self) -> str:
        return self.__sourceId

    @sourceId.setter
    def sourceId(self, value: str):
        self.__sourceId = value
        self._property_changed('sourceId')        

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str):
        self.__country = value
        self._property_changed('country')        

    @property
    def cusip(self) -> str:
        return self.__cusip

    @cusip.setter
    def cusip(self, value: str):
        self.__cusip = value
        self._property_changed('cusip')        

    @property
    def ideaActivityTime(self) -> datetime.datetime:
        return self.__ideaActivityTime

    @ideaActivityTime.setter
    def ideaActivityTime(self, value: datetime.datetime):
        self.__ideaActivityTime = value
        self._property_changed('ideaActivityTime')        

    @property
    def touchSpreadScore(self) -> float:
        return self.__touchSpreadScore

    @touchSpreadScore.setter
    def touchSpreadScore(self, value: float):
        self.__touchSpreadScore = value
        self._property_changed('touchSpreadScore')        

    @property
    def absoluteStrike(self) -> float:
        return self.__absoluteStrike

    @absoluteStrike.setter
    def absoluteStrike(self, value: float):
        self.__absoluteStrike = value
        self._property_changed('absoluteStrike')        

    @property
    def netExposure(self) -> float:
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value: float):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def source(self) -> str:
        return self.__source

    @source.setter
    def source(self, value: str):
        self.__source = value
        self._property_changed('source')        

    @property
    def assetClassificationsCountryCode(self) -> str:
        return self.__assetClassificationsCountryCode

    @assetClassificationsCountryCode.setter
    def assetClassificationsCountryCode(self, value: str):
        self.__assetClassificationsCountryCode = value
        self._property_changed('assetClassificationsCountryCode')        

    @property
    def frequency(self) -> str:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def activityId(self) -> str:
        return self.__activityId

    @activityId.setter
    def activityId(self, value: str):
        self.__activityId = value
        self._property_changed('activityId')        

    @property
    def estimatedImpact(self) -> float:
        return self.__estimatedImpact

    @estimatedImpact.setter
    def estimatedImpact(self, value: float):
        self.__estimatedImpact = value
        self._property_changed('estimatedImpact')        

    @property
    def dataSetSubCategory(self) -> str:
        return self.__dataSetSubCategory

    @dataSetSubCategory.setter
    def dataSetSubCategory(self, value: str):
        self.__dataSetSubCategory = value
        self._property_changed('dataSetSubCategory')        

    @property
    def assetParametersPricingLocation(self) -> str:
        return self.__assetParametersPricingLocation

    @assetParametersPricingLocation.setter
    def assetParametersPricingLocation(self, value: str):
        self.__assetParametersPricingLocation = value
        self._property_changed('assetParametersPricingLocation')        

    @property
    def eventDescription(self) -> str:
        return self.__eventDescription

    @eventDescription.setter
    def eventDescription(self, value: str):
        self.__eventDescription = value
        self._property_changed('eventDescription')        

    @property
    def strikeReference(self) -> str:
        return self.__strikeReference

    @strikeReference.setter
    def strikeReference(self, value: str):
        self.__strikeReference = value
        self._property_changed('strikeReference')        

    @property
    def details(self) -> str:
        return self.__details

    @details.setter
    def details(self, value: str):
        self.__details = value
        self._property_changed('details')        

    @property
    def assetCount(self) -> float:
        return self.__assetCount

    @assetCount.setter
    def assetCount(self, value: float):
        self.__assetCount = value
        self._property_changed('assetCount')        

    @property
    def given(self) -> float:
        return self.__given

    @given.setter
    def given(self, value: float):
        self.__given = value
        self._property_changed('given')        

    @property
    def absoluteValue(self) -> float:
        return self.__absoluteValue

    @absoluteValue.setter
    def absoluteValue(self, value: float):
        self.__absoluteValue = value
        self._property_changed('absoluteValue')        

    @property
    def delistingDate(self) -> str:
        return self.__delistingDate

    @delistingDate.setter
    def delistingDate(self, value: str):
        self.__delistingDate = value
        self._property_changed('delistingDate')        

    @property
    def longTenor(self) -> str:
        return self.__longTenor

    @longTenor.setter
    def longTenor(self, value: str):
        self.__longTenor = value
        self._property_changed('longTenor')        

    @property
    def mctr(self) -> float:
        return self.__mctr

    @mctr.setter
    def mctr(self, value: float):
        self.__mctr = value
        self._property_changed('mctr')        

    @property
    def weight(self) -> float:
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value
        self._property_changed('weight')        

    @property
    def historicalClose(self) -> float:
        return self.__historicalClose

    @historicalClose.setter
    def historicalClose(self, value: float):
        self.__historicalClose = value
        self._property_changed('historicalClose')        

    @property
    def assetCountPriced(self) -> float:
        return self.__assetCountPriced

    @assetCountPriced.setter
    def assetCountPriced(self, value: float):
        self.__assetCountPriced = value
        self._property_changed('assetCountPriced')        

    @property
    def marketDataPoint(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value: Tuple[Tuple[str, ...], ...]):
        self.__marketDataPoint = value
        self._property_changed('marketDataPoint')        

    @property
    def ideaId(self) -> str:
        return self.__ideaId

    @ideaId.setter
    def ideaId(self, value: str):
        self.__ideaId = value
        self._property_changed('ideaId')        

    @property
    def commentStatus(self) -> str:
        return self.__commentStatus

    @commentStatus.setter
    def commentStatus(self, value: str):
        self.__commentStatus = value
        self._property_changed('commentStatus')        

    @property
    def marginalCost(self) -> float:
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value: float):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def absoluteWeight(self) -> float:
        return self.__absoluteWeight

    @absoluteWeight.setter
    def absoluteWeight(self, value: float):
        self.__absoluteWeight = value
        self._property_changed('absoluteWeight')        

    @property
    def tradeTime(self) -> datetime.datetime:
        return self.__tradeTime

    @tradeTime.setter
    def tradeTime(self, value: datetime.datetime):
        self.__tradeTime = value
        self._property_changed('tradeTime')        

    @property
    def measure(self) -> str:
        return self.__measure

    @measure.setter
    def measure(self, value: str):
        self.__measure = value
        self._property_changed('measure')        

    @property
    def clientWeight(self) -> float:
        return self.__clientWeight

    @clientWeight.setter
    def clientWeight(self, value: float):
        self.__clientWeight = value
        self._property_changed('clientWeight')        

    @property
    def hedgeAnnualizedVolatility(self) -> float:
        return self.__hedgeAnnualizedVolatility

    @hedgeAnnualizedVolatility.setter
    def hedgeAnnualizedVolatility(self, value: float):
        self.__hedgeAnnualizedVolatility = value
        self._property_changed('hedgeAnnualizedVolatility')        

    @property
    def benchmarkCurrency(self) -> str:
        return self.__benchmarkCurrency

    @benchmarkCurrency.setter
    def benchmarkCurrency(self, value: str):
        self.__benchmarkCurrency = value
        self._property_changed('benchmarkCurrency')        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def aum(self) -> Union[float, Op]:
        return self.__aum

    @aum.setter
    def aum(self, value: Union[float, Op]):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def folderName(self) -> str:
        return self.__folderName

    @folderName.setter
    def folderName(self, value: str):
        self.__folderName = value
        self._property_changed('folderName')        

    @property
    def lendingPartnerFee(self) -> float:
        return self.__lendingPartnerFee

    @lendingPartnerFee.setter
    def lendingPartnerFee(self, value: float):
        self.__lendingPartnerFee = value
        self._property_changed('lendingPartnerFee')        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self.__region = value
        self._property_changed('region')        

    @property
    def liveDate(self) -> Union[datetime.date, Op]:
        return self.__liveDate

    @liveDate.setter
    def liveDate(self, value: Union[datetime.date, Op]):
        self.__liveDate = value
        self._property_changed('liveDate')        

    @property
    def askHigh(self) -> float:
        return self.__askHigh

    @askHigh.setter
    def askHigh(self, value: float):
        self.__askHigh = value
        self._property_changed('askHigh')        

    @property
    def corporateActionType(self) -> str:
        return self.__corporateActionType

    @corporateActionType.setter
    def corporateActionType(self, value: str):
        self.__corporateActionType = value
        self._property_changed('corporateActionType')        

    @property
    def primeId(self) -> str:
        return self.__primeId

    @primeId.setter
    def primeId(self, value: str):
        self.__primeId = value
        self._property_changed('primeId')        

    @property
    def tenor2(self) -> str:
        return self.__tenor2

    @tenor2.setter
    def tenor2(self, value: str):
        self.__tenor2 = value
        self._property_changed('tenor2')        

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def valueRevised(self) -> str:
        return self.__valueRevised

    @valueRevised.setter
    def valueRevised(self, value: str):
        self.__valueRevised = value
        self._property_changed('valueRevised')        

    @property
    def ownerName(self) -> str:
        return self.__ownerName

    @ownerName.setter
    def ownerName(self, value: str):
        self.__ownerName = value
        self._property_changed('ownerName')        

    @property
    def adjustedTradePrice(self) -> float:
        return self.__adjustedTradePrice

    @adjustedTradePrice.setter
    def adjustedTradePrice(self, value: float):
        self.__adjustedTradePrice = value
        self._property_changed('adjustedTradePrice')        

    @property
    def lastUpdatedById(self) -> str:
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: str):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def zScore(self) -> float:
        return self.__zScore

    @zScore.setter
    def zScore(self, value: float):
        self.__zScore = value
        self._property_changed('zScore')        

    @property
    def targetShareholderMeetingDate(self) -> str:
        return self.__targetShareholderMeetingDate

    @targetShareholderMeetingDate.setter
    def targetShareholderMeetingDate(self, value: str):
        self.__targetShareholderMeetingDate = value
        self._property_changed('targetShareholderMeetingDate')        

    @property
    def isADR(self) -> bool:
        return self.__isADR

    @isADR.setter
    def isADR(self, value: bool):
        self.__isADR = value
        self._property_changed('isADR')        

    @property
    def eventStartTime(self) -> str:
        return self.__eventStartTime

    @eventStartTime.setter
    def eventStartTime(self, value: str):
        self.__eventStartTime = value
        self._property_changed('eventStartTime')        

    @property
    def factor(self) -> str:
        return self.__factor

    @factor.setter
    def factor(self, value: str):
        self.__factor = value
        self._property_changed('factor')        

    @property
    def longConvictionSmall(self) -> float:
        return self.__longConvictionSmall

    @longConvictionSmall.setter
    def longConvictionSmall(self, value: float):
        self.__longConvictionSmall = value
        self._property_changed('longConvictionSmall')        

    @property
    def serviceId(self) -> str:
        return self.__serviceId

    @serviceId.setter
    def serviceId(self, value: str):
        self.__serviceId = value
        self._property_changed('serviceId')        

    @property
    def turnover(self) -> float:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def complianceEffectiveTime(self) -> datetime.datetime:
        return self.__complianceEffectiveTime

    @complianceEffectiveTime.setter
    def complianceEffectiveTime(self, value: datetime.datetime):
        self.__complianceEffectiveTime = value
        self._property_changed('complianceEffectiveTime')        

    @property
    def expirationDate(self) -> datetime.date:
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: datetime.date):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def gsfeer(self) -> float:
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value: float):
        self.__gsfeer = value
        self._property_changed('gsfeer')        

    @property
    def coverage(self) -> str:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: str):
        self.__coverage = value
        self._property_changed('coverage')        

    @property
    def backtestId(self) -> str:
        return self.__backtestId

    @backtestId.setter
    def backtestId(self, value: str):
        self.__backtestId = value
        self._property_changed('backtestId')        

    @property
    def gPercentile(self) -> float:
        return self.__gPercentile

    @gPercentile.setter
    def gPercentile(self, value: float):
        self.__gPercentile = value
        self._property_changed('gPercentile')        

    @property
    def gScore(self) -> float:
        return self.__gScore

    @gScore.setter
    def gScore(self, value: float):
        self.__gScore = value
        self._property_changed('gScore')        

    @property
    def marketValue(self) -> float:
        return self.__marketValue

    @marketValue.setter
    def marketValue(self, value: float):
        self.__marketValue = value
        self._property_changed('marketValue')        

    @property
    def multipleScore(self) -> float:
        return self.__multipleScore

    @multipleScore.setter
    def multipleScore(self, value: float):
        self.__multipleScore = value
        self._property_changed('multipleScore')        

    @property
    def lendingFundNav(self) -> float:
        return self.__lendingFundNav

    @lendingFundNav.setter
    def lendingFundNav(self, value: float):
        self.__lendingFundNav = value
        self._property_changed('lendingFundNav')        

    @property
    def sourceOriginalCategory(self) -> str:
        return self.__sourceOriginalCategory

    @sourceOriginalCategory.setter
    def sourceOriginalCategory(self, value: str):
        self.__sourceOriginalCategory = value
        self._property_changed('sourceOriginalCategory')        

    @property
    def betaAdjustedExposure(self) -> float:
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value: float):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def composite5DayAdv(self) -> float:
        return self.__composite5DayAdv

    @composite5DayAdv.setter
    def composite5DayAdv(self, value: float):
        self.__composite5DayAdv = value
        self._property_changed('composite5DayAdv')        

    @property
    def latestExecutionTime(self) -> datetime.datetime:
        return self.__latestExecutionTime

    @latestExecutionTime.setter
    def latestExecutionTime(self, value: datetime.datetime):
        self.__latestExecutionTime = value
        self._property_changed('latestExecutionTime')        

    @property
    def dividendPoints(self) -> float:
        return self.__dividendPoints

    @dividendPoints.setter
    def dividendPoints(self, value: float):
        self.__dividendPoints = value
        self._property_changed('dividendPoints')        

    @property
    def newIdeasWtd(self) -> float:
        return self.__newIdeasWtd

    @newIdeasWtd.setter
    def newIdeasWtd(self, value: float):
        self.__newIdeasWtd = value
        self._property_changed('newIdeasWtd')        

    @property
    def paid(self) -> float:
        return self.__paid

    @paid.setter
    def paid(self, value: float):
        self.__paid = value
        self._property_changed('paid')        

    @property
    def short(self) -> float:
        return self.__short

    @short.setter
    def short(self, value: float):
        self.__short = value
        self._property_changed('short')        

    @property
    def location(self) -> str:
        return self.__location

    @location.setter
    def location(self, value: str):
        self.__location = value
        self._property_changed('location')        

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self.__comment = value
        self._property_changed('comment')        

    @property
    def bosInTicksDescription(self) -> str:
        return self.__bosInTicksDescription

    @bosInTicksDescription.setter
    def bosInTicksDescription(self, value: str):
        self.__bosInTicksDescription = value
        self._property_changed('bosInTicksDescription')        

    @property
    def sourceSymbol(self) -> str:
        return self.__sourceSymbol

    @sourceSymbol.setter
    def sourceSymbol(self, value: str):
        self.__sourceSymbol = value
        self._property_changed('sourceSymbol')        

    @property
    def time(self) -> datetime.datetime:
        return self.__time

    @time.setter
    def time(self, value: datetime.datetime):
        self.__time = value
        self._property_changed('time')        

    @property
    def scenarioId(self) -> str:
        return self.__scenarioId

    @scenarioId.setter
    def scenarioId(self, value: str):
        self.__scenarioId = value
        self._property_changed('scenarioId')        

    @property
    def askUnadjusted(self) -> float:
        return self.__askUnadjusted

    @askUnadjusted.setter
    def askUnadjusted(self, value: float):
        self.__askUnadjusted = value
        self._property_changed('askUnadjusted')        

    @property
    def queueClockTime(self) -> float:
        return self.__queueClockTime

    @queueClockTime.setter
    def queueClockTime(self, value: float):
        self.__queueClockTime = value
        self._property_changed('queueClockTime')        

    @property
    def askChange(self) -> float:
        return self.__askChange

    @askChange.setter
    def askChange(self, value: float):
        self.__askChange = value
        self._property_changed('askChange')        

    @property
    def tcmCostParticipationRate50Pct(self) -> float:
        return self.__tcmCostParticipationRate50Pct

    @tcmCostParticipationRate50Pct.setter
    def tcmCostParticipationRate50Pct(self, value: float):
        self.__tcmCostParticipationRate50Pct = value
        self._property_changed('tcmCostParticipationRate50Pct')        

    @property
    def normalizedPerformance(self) -> float:
        return self.__normalizedPerformance

    @normalizedPerformance.setter
    def normalizedPerformance(self, value: float):
        self.__normalizedPerformance = value
        self._property_changed('normalizedPerformance')        

    @property
    def cmId(self) -> str:
        return self.__cmId

    @cmId.setter
    def cmId(self, value: str):
        self.__cmId = value
        self._property_changed('cmId')        

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def mdapi(self) -> str:
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: str):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def dividendYield(self) -> float:
        return self.__dividendYield

    @dividendYield.setter
    def dividendYield(self, value: float):
        self.__dividendYield = value
        self._property_changed('dividendYield')        

    @property
    def cumulativePnl(self) -> float:
        return self.__cumulativePnl

    @cumulativePnl.setter
    def cumulativePnl(self, value: float):
        self.__cumulativePnl = value
        self._property_changed('cumulativePnl')        

    @property
    def sourceOrigin(self) -> str:
        return self.__sourceOrigin

    @sourceOrigin.setter
    def sourceOrigin(self, value: str):
        self.__sourceOrigin = value
        self._property_changed('sourceOrigin')        

    @property
    def shortTenor(self) -> str:
        return self.__shortTenor

    @shortTenor.setter
    def shortTenor(self, value: str):
        self.__shortTenor = value
        self._property_changed('shortTenor')        

    @property
    def unadjustedVolume(self) -> float:
        return self.__unadjustedVolume

    @unadjustedVolume.setter
    def unadjustedVolume(self, value: float):
        self.__unadjustedVolume = value
        self._property_changed('unadjustedVolume')        

    @property
    def measures(self) -> Tuple[str, ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[str, ...]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def tradingCostPnl(self) -> float:
        return self.__tradingCostPnl

    @tradingCostPnl.setter
    def tradingCostPnl(self, value: float):
        self.__tradingCostPnl = value
        self._property_changed('tradingCostPnl')        

    @property
    def internalUser(self) -> bool:
        return self.__internalUser

    @internalUser.setter
    def internalUser(self, value: bool):
        self.__internalUser = value
        self._property_changed('internalUser')        

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        self.__price = value
        self._property_changed('price')        

    @property
    def paymentQuantity(self) -> float:
        return self.__paymentQuantity

    @paymentQuantity.setter
    def paymentQuantity(self, value: float):
        self.__paymentQuantity = value
        self._property_changed('paymentQuantity')        

    @property
    def underlyer(self) -> str:
        return self.__underlyer

    @underlyer.setter
    def underlyer(self, value: str):
        self.__underlyer = value
        self._property_changed('underlyer')        

    @property
    def createdTime(self) -> datetime.datetime:
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: datetime.datetime):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def positionIdx(self) -> int:
        return self.__positionIdx

    @positionIdx.setter
    def positionIdx(self, value: int):
        self.__positionIdx = value
        self._property_changed('positionIdx')        

    @property
    def secName(self) -> str:
        return self.__secName

    @secName.setter
    def secName(self, value: str):
        self.__secName = value
        self._property_changed('secName')        

    @property
    def percentADV(self) -> float:
        return self.__percentADV

    @percentADV.setter
    def percentADV(self, value: float):
        self.__percentADV = value
        self._property_changed('percentADV')        

    @property
    def unadjustedLow(self) -> float:
        return self.__unadjustedLow

    @unadjustedLow.setter
    def unadjustedLow(self, value: float):
        self.__unadjustedLow = value
        self._property_changed('unadjustedLow')        

    @property
    def contract(self) -> str:
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self.__contract = value
        self._property_changed('contract')        

    @property
    def sedol(self) -> str:
        return self.__sedol

    @sedol.setter
    def sedol(self, value: str):
        self.__sedol = value
        self._property_changed('sedol')        

    @property
    def roundingCostPnl(self) -> float:
        return self.__roundingCostPnl

    @roundingCostPnl.setter
    def roundingCostPnl(self, value: float):
        self.__roundingCostPnl = value
        self._property_changed('roundingCostPnl')        

    @property
    def sustainGlobal(self) -> bool:
        return self.__sustainGlobal

    @sustainGlobal.setter
    def sustainGlobal(self, value: bool):
        self.__sustainGlobal = value
        self._property_changed('sustainGlobal')        

    @property
    def sourceTicker(self) -> str:
        return self.__sourceTicker

    @sourceTicker.setter
    def sourceTicker(self, value: str):
        self.__sourceTicker = value
        self._property_changed('sourceTicker')        

    @property
    def portfolioId(self) -> str:
        return self.__portfolioId

    @portfolioId.setter
    def portfolioId(self, value: str):
        self.__portfolioId = value
        self._property_changed('portfolioId')        

    @property
    def gsid(self) -> str:
        return self.__gsid

    @gsid.setter
    def gsid(self, value: str):
        self.__gsid = value
        self._property_changed('gsid')        

    @property
    def esPercentile(self) -> float:
        return self.__esPercentile

    @esPercentile.setter
    def esPercentile(self, value: float):
        self.__esPercentile = value
        self._property_changed('esPercentile')        

    @property
    def lendingFund(self) -> str:
        return self.__lendingFund

    @lendingFund.setter
    def lendingFund(self, value: str):
        self.__lendingFund = value
        self._property_changed('lendingFund')        

    @property
    def tcmCostParticipationRate15Pct(self) -> float:
        return self.__tcmCostParticipationRate15Pct

    @tcmCostParticipationRate15Pct.setter
    def tcmCostParticipationRate15Pct(self, value: float):
        self.__tcmCostParticipationRate15Pct = value
        self._property_changed('tcmCostParticipationRate15Pct')        

    @property
    def sensitivity(self) -> float:
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value: float):
        self.__sensitivity = value
        self._property_changed('sensitivity')        

    @property
    def fiscalYear(self) -> str:
        return self.__fiscalYear

    @fiscalYear.setter
    def fiscalYear(self, value: str):
        self.__fiscalYear = value
        self._property_changed('fiscalYear')        

    @property
    def rcic(self) -> str:
        return self.__rcic

    @rcic.setter
    def rcic(self, value: str):
        self.__rcic = value
        self._property_changed('rcic')        

    @property
    def simonAssetTags(self) -> Tuple[str, ...]:
        return self.__simonAssetTags

    @simonAssetTags.setter
    def simonAssetTags(self, value: Tuple[str, ...]):
        self.__simonAssetTags = value
        self._property_changed('simonAssetTags')        

    @property
    def internal(self) -> bool:
        return self.__internal

    @internal.setter
    def internal(self, value: bool):
        self.__internal = value
        self._property_changed('internal')        

    @property
    def forwardPoint(self) -> float:
        return self.__forwardPoint

    @forwardPoint.setter
    def forwardPoint(self, value: float):
        self.__forwardPoint = value
        self._property_changed('forwardPoint')        

    @property
    def assetClassificationsGicsIndustry(self) -> str:
        return self.__assetClassificationsGicsIndustry

    @assetClassificationsGicsIndustry.setter
    def assetClassificationsGicsIndustry(self, value: str):
        self.__assetClassificationsGicsIndustry = value
        self._property_changed('assetClassificationsGicsIndustry')        

    @property
    def adjustedBidPrice(self) -> float:
        return self.__adjustedBidPrice

    @adjustedBidPrice.setter
    def adjustedBidPrice(self, value: float):
        self.__adjustedBidPrice = value
        self._property_changed('adjustedBidPrice')        

    @property
    def hitRateQtd(self) -> float:
        return self.__hitRateQtd

    @hitRateQtd.setter
    def hitRateQtd(self, value: float):
        self.__hitRateQtd = value
        self._property_changed('hitRateQtd')        

    @property
    def varSwap(self) -> float:
        return self.__varSwap

    @varSwap.setter
    def varSwap(self, value: float):
        self.__varSwap = value
        self._property_changed('varSwap')        

    @property
    def lowUnadjusted(self) -> float:
        return self.__lowUnadjusted

    @lowUnadjusted.setter
    def lowUnadjusted(self, value: float):
        self.__lowUnadjusted = value
        self._property_changed('lowUnadjusted')        

    @property
    def sectorsRaw(self) -> Tuple[str, ...]:
        return self.__sectorsRaw

    @sectorsRaw.setter
    def sectorsRaw(self, value: Tuple[str, ...]):
        self.__sectorsRaw = value
        self._property_changed('sectorsRaw')        

    @property
    def low(self) -> float:
        return self.__low

    @low.setter
    def low(self, value: float):
        self.__low = value
        self._property_changed('low')        

    @property
    def crossGroup(self) -> str:
        return self.__crossGroup

    @crossGroup.setter
    def crossGroup(self, value: str):
        self.__crossGroup = value
        self._property_changed('crossGroup')        

    @property
    def integratedScore(self) -> float:
        return self.__integratedScore

    @integratedScore.setter
    def integratedScore(self, value: float):
        self.__integratedScore = value
        self._property_changed('integratedScore')        

    @property
    def reportRunTime(self) -> datetime.datetime:
        return self.__reportRunTime

    @reportRunTime.setter
    def reportRunTime(self, value: datetime.datetime):
        self.__reportRunTime = value
        self._property_changed('reportRunTime')        

    @property
    def fiveDayPriceChangeBps(self) -> float:
        return self.__fiveDayPriceChangeBps

    @fiveDayPriceChangeBps.setter
    def fiveDayPriceChangeBps(self, value: float):
        self.__fiveDayPriceChangeBps = value
        self._property_changed('fiveDayPriceChangeBps')        

    @property
    def tradeSize(self) -> float:
        return self.__tradeSize

    @tradeSize.setter
    def tradeSize(self, value: float):
        self.__tradeSize = value
        self._property_changed('tradeSize')        

    @property
    def symbolDimensions(self) -> Tuple[str, ...]:
        return self.__symbolDimensions

    @symbolDimensions.setter
    def symbolDimensions(self, value: Tuple[str, ...]):
        self.__symbolDimensions = value
        self._property_changed('symbolDimensions')        

    @property
    def quotingStyle(self) -> str:
        return self.__quotingStyle

    @quotingStyle.setter
    def quotingStyle(self, value: str):
        self.__quotingStyle = value
        self._property_changed('quotingStyle')        

    @property
    def scenarioGroupId(self) -> str:
        return self.__scenarioGroupId

    @scenarioGroupId.setter
    def scenarioGroupId(self, value: str):
        self.__scenarioGroupId = value
        self._property_changed('scenarioGroupId')        

    @property
    def errorMessage(self) -> str:
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, value: str):
        self.__errorMessage = value
        self._property_changed('errorMessage')        

    @property
    def avgTradeRateDescription(self) -> str:
        return self.__avgTradeRateDescription

    @avgTradeRateDescription.setter
    def avgTradeRateDescription(self, value: str):
        self.__avgTradeRateDescription = value
        self._property_changed('avgTradeRateDescription')        

    @property
    def midPrice(self) -> float:
        return self.__midPrice

    @midPrice.setter
    def midPrice(self, value: float):
        self.__midPrice = value
        self._property_changed('midPrice')        

    @property
    def fraction(self) -> float:
        return self.__fraction

    @fraction.setter
    def fraction(self, value: float):
        self.__fraction = value
        self._property_changed('fraction')        

    @property
    def stsCreditMarket(self) -> str:
        return self.__stsCreditMarket

    @stsCreditMarket.setter
    def stsCreditMarket(self, value: str):
        self.__stsCreditMarket = value
        self._property_changed('stsCreditMarket')        

    @property
    def assetCountShort(self) -> float:
        return self.__assetCountShort

    @assetCountShort.setter
    def assetCountShort(self, value: float):
        self.__assetCountShort = value
        self._property_changed('assetCountShort')        

    @property
    def stsEmDm(self) -> str:
        return self.__stsEmDm

    @stsEmDm.setter
    def stsEmDm(self, value: str):
        self.__stsEmDm = value
        self._property_changed('stsEmDm')        

    @property
    def tcmCostHorizon2Day(self) -> float:
        return self.__tcmCostHorizon2Day

    @tcmCostHorizon2Day.setter
    def tcmCostHorizon2Day(self, value: float):
        self.__tcmCostHorizon2Day = value
        self._property_changed('tcmCostHorizon2Day')        

    @property
    def queueInLots(self) -> float:
        return self.__queueInLots

    @queueInLots.setter
    def queueInLots(self, value: float):
        self.__queueInLots = value
        self._property_changed('queueInLots')        

    @property
    def priceRangeInTicksDescription(self) -> str:
        return self.__priceRangeInTicksDescription

    @priceRangeInTicksDescription.setter
    def priceRangeInTicksDescription(self, value: str):
        self.__priceRangeInTicksDescription = value
        self._property_changed('priceRangeInTicksDescription')        

    @property
    def date(self) -> datetime.date:
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self.__date = value
        self._property_changed('date')        

    @property
    def tenderOfferExpirationDate(self) -> str:
        return self.__tenderOfferExpirationDate

    @tenderOfferExpirationDate.setter
    def tenderOfferExpirationDate(self, value: str):
        self.__tenderOfferExpirationDate = value
        self._property_changed('tenderOfferExpirationDate')        

    @property
    def highUnadjusted(self) -> float:
        return self.__highUnadjusted

    @highUnadjusted.setter
    def highUnadjusted(self, value: float):
        self.__highUnadjusted = value
        self._property_changed('highUnadjusted')        

    @property
    def sourceCategory(self) -> str:
        return self.__sourceCategory

    @sourceCategory.setter
    def sourceCategory(self, value: str):
        self.__sourceCategory = value
        self._property_changed('sourceCategory')        

    @property
    def volumeUnadjusted(self) -> float:
        return self.__volumeUnadjusted

    @volumeUnadjusted.setter
    def volumeUnadjusted(self, value: float):
        self.__volumeUnadjusted = value
        self._property_changed('volumeUnadjusted')        

    @property
    def avgTradeRateLabel(self):
        return self.__avgTradeRateLabel

    @avgTradeRateLabel.setter
    def avgTradeRateLabel(self, value):
        self.__avgTradeRateLabel = value
        self._property_changed('avgTradeRateLabel')        

    @property
    def tcmCostParticipationRate5Pct(self) -> float:
        return self.__tcmCostParticipationRate5Pct

    @tcmCostParticipationRate5Pct.setter
    def tcmCostParticipationRate5Pct(self, value: float):
        self.__tcmCostParticipationRate5Pct = value
        self._property_changed('tcmCostParticipationRate5Pct')        

    @property
    def isActive(self) -> bool:
        return self.__isActive

    @isActive.setter
    def isActive(self, value: bool):
        self.__isActive = value
        self._property_changed('isActive')        

    @property
    def growthScore(self) -> float:
        return self.__growthScore

    @growthScore.setter
    def growthScore(self, value: float):
        self.__growthScore = value
        self._property_changed('growthScore')        

    @property
    def encodedStats(self) -> str:
        return self.__encodedStats

    @encodedStats.setter
    def encodedStats(self, value: str):
        self.__encodedStats = value
        self._property_changed('encodedStats')        

    @property
    def adjustedShortInterest(self) -> float:
        return self.__adjustedShortInterest

    @adjustedShortInterest.setter
    def adjustedShortInterest(self, value: float):
        self.__adjustedShortInterest = value
        self._property_changed('adjustedShortInterest')        

    @property
    def askSize(self) -> float:
        return self.__askSize

    @askSize.setter
    def askSize(self, value: float):
        self.__askSize = value
        self._property_changed('askSize')        

    @property
    def mdapiType(self) -> str:
        return self.__mdapiType

    @mdapiType.setter
    def mdapiType(self, value: str):
        self.__mdapiType = value
        self._property_changed('mdapiType')        

    @property
    def group(self) -> str:
        return self.__group

    @group.setter
    def group(self, value: str):
        self.__group = value
        self._property_changed('group')        

    @property
    def estimatedSpread(self) -> float:
        return self.__estimatedSpread

    @estimatedSpread.setter
    def estimatedSpread(self, value: float):
        self.__estimatedSpread = value
        self._property_changed('estimatedSpread')        

    @property
    def resource(self) -> str:
        return self.__resource

    @resource.setter
    def resource(self, value: str):
        self.__resource = value
        self._property_changed('resource')        

    @property
    def created(self) -> datetime.datetime:
        return self.__created

    @created.setter
    def created(self, value: datetime.datetime):
        self.__created = value
        self._property_changed('created')        

    @property
    def tcmCost(self) -> float:
        return self.__tcmCost

    @tcmCost.setter
    def tcmCost(self, value: float):
        self.__tcmCost = value
        self._property_changed('tcmCost')        

    @property
    def sustainJapan(self) -> bool:
        return self.__sustainJapan

    @sustainJapan.setter
    def sustainJapan(self, value: bool):
        self.__sustainJapan = value
        self._property_changed('sustainJapan')        

    @property
    def navSpread(self) -> float:
        return self.__navSpread

    @navSpread.setter
    def navSpread(self, value: float):
        self.__navSpread = value
        self._property_changed('navSpread')        

    @property
    def bidPrice(self) -> float:
        return self.__bidPrice

    @bidPrice.setter
    def bidPrice(self, value: float):
        self.__bidPrice = value
        self._property_changed('bidPrice')        

    @property
    def hedgeTrackingError(self) -> float:
        return self.__hedgeTrackingError

    @hedgeTrackingError.setter
    def hedgeTrackingError(self, value: float):
        self.__hedgeTrackingError = value
        self._property_changed('hedgeTrackingError')        

    @property
    def marketCapCategory(self) -> str:
        return self.__marketCapCategory

    @marketCapCategory.setter
    def marketCapCategory(self, value: str):
        self.__marketCapCategory = value
        self._property_changed('marketCapCategory')        

    @property
    def historicalVolume(self) -> float:
        return self.__historicalVolume

    @historicalVolume.setter
    def historicalVolume(self, value: float):
        self.__historicalVolume = value
        self._property_changed('historicalVolume')        

    @property
    def esNumericPercentile(self) -> float:
        return self.__esNumericPercentile

    @esNumericPercentile.setter
    def esNumericPercentile(self, value: float):
        self.__esNumericPercentile = value
        self._property_changed('esNumericPercentile')        

    @property
    def strikePrice(self) -> float:
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: float):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def eventStartDate(self) -> datetime.date:
        return self.__eventStartDate

    @eventStartDate.setter
    def eventStartDate(self, value: datetime.date):
        self.__eventStartDate = value
        self._property_changed('eventStartDate')        

    @property
    def calSpreadMisPricing(self) -> float:
        return self.__calSpreadMisPricing

    @calSpreadMisPricing.setter
    def calSpreadMisPricing(self, value: float):
        self.__calSpreadMisPricing = value
        self._property_changed('calSpreadMisPricing')        

    @property
    def equityGamma(self) -> float:
        return self.__equityGamma

    @equityGamma.setter
    def equityGamma(self, value: float):
        self.__equityGamma = value
        self._property_changed('equityGamma')        

    @property
    def grossIncome(self) -> float:
        return self.__grossIncome

    @grossIncome.setter
    def grossIncome(self, value: float):
        self.__grossIncome = value
        self._property_changed('grossIncome')        

    @property
    def emId(self) -> str:
        return self.__emId

    @emId.setter
    def emId(self, value: str):
        self.__emId = value
        self._property_changed('emId')        

    @property
    def adjustedOpenPrice(self) -> float:
        return self.__adjustedOpenPrice

    @adjustedOpenPrice.setter
    def adjustedOpenPrice(self, value: float):
        self.__adjustedOpenPrice = value
        self._property_changed('adjustedOpenPrice')        

    @property
    def assetCountInModel(self) -> float:
        return self.__assetCountInModel

    @assetCountInModel.setter
    def assetCountInModel(self, value: float):
        self.__assetCountInModel = value
        self._property_changed('assetCountInModel')        

    @property
    def stsCreditRegion(self) -> str:
        return self.__stsCreditRegion

    @stsCreditRegion.setter
    def stsCreditRegion(self, value: str):
        self.__stsCreditRegion = value
        self._property_changed('stsCreditRegion')        

    @property
    def point(self) -> str:
        return self.__point

    @point.setter
    def point(self, value: str):
        self.__point = value
        self._property_changed('point')        

    @property
    def lender(self) -> str:
        return self.__lender

    @lender.setter
    def lender(self, value: str):
        self.__lender = value
        self._property_changed('lender')        

    @property
    def minTemperature(self) -> float:
        return self.__minTemperature

    @minTemperature.setter
    def minTemperature(self, value: float):
        self.__minTemperature = value
        self._property_changed('minTemperature')        

    @property
    def closeTime(self) -> datetime.datetime:
        return self.__closeTime

    @closeTime.setter
    def closeTime(self, value: datetime.datetime):
        self.__closeTime = value
        self._property_changed('closeTime')        

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        

    @property
    def relativeStrike(self) -> float:
        return self.__relativeStrike

    @relativeStrike.setter
    def relativeStrike(self, value: float):
        self.__relativeStrike = value
        self._property_changed('relativeStrike')        

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        self.__amount = value
        self._property_changed('amount')        

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def lendingFundAcct(self) -> str:
        return self.__lendingFundAcct

    @lendingFundAcct.setter
    def lendingFundAcct(self, value: str):
        self.__lendingFundAcct = value
        self._property_changed('lendingFundAcct')        

    @property
    def reportId(self) -> str:
        return self.__reportId

    @reportId.setter
    def reportId(self, value: str):
        self.__reportId = value
        self._property_changed('reportId')        

    @property
    def indexWeight(self) -> float:
        return self.__indexWeight

    @indexWeight.setter
    def indexWeight(self, value: float):
        self.__indexWeight = value
        self._property_changed('indexWeight')        

    @property
    def rebate(self) -> float:
        return self.__rebate

    @rebate.setter
    def rebate(self, value: float):
        self.__rebate = value
        self._property_changed('rebate')        

    @property
    def trader(self) -> str:
        return self.__trader

    @trader.setter
    def trader(self, value: str):
        self.__trader = value
        self._property_changed('trader')        

    @property
    def factorCategory(self) -> str:
        return self.__factorCategory

    @factorCategory.setter
    def factorCategory(self, value: str):
        self.__factorCategory = value
        self._property_changed('factorCategory')        

    @property
    def impliedVolatility(self) -> float:
        return self.__impliedVolatility

    @impliedVolatility.setter
    def impliedVolatility(self, value: float):
        self.__impliedVolatility = value
        self._property_changed('impliedVolatility')        

    @property
    def spread(self) -> float:
        return self.__spread

    @spread.setter
    def spread(self, value: float):
        self.__spread = value
        self._property_changed('spread')        

    @property
    def stsRatesMaturity(self) -> str:
        return self.__stsRatesMaturity

    @stsRatesMaturity.setter
    def stsRatesMaturity(self, value: str):
        self.__stsRatesMaturity = value
        self._property_changed('stsRatesMaturity')        

    @property
    def equityDelta(self) -> float:
        return self.__equityDelta

    @equityDelta.setter
    def equityDelta(self, value: float):
        self.__equityDelta = value
        self._property_changed('equityDelta')        

    @property
    def grossWeight(self) -> float:
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value: float):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def listed(self) -> bool:
        return self.__listed

    @listed.setter
    def listed(self, value: bool):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def tcmCostHorizon6Hour(self) -> float:
        return self.__tcmCostHorizon6Hour

    @tcmCostHorizon6Hour.setter
    def tcmCostHorizon6Hour(self, value: float):
        self.__tcmCostHorizon6Hour = value
        self._property_changed('tcmCostHorizon6Hour')        

    @property
    def g10Currency(self) -> bool:
        return self.__g10Currency

    @g10Currency.setter
    def g10Currency(self, value: bool):
        self.__g10Currency = value
        self._property_changed('g10Currency')        

    @property
    def shockStyle(self) -> str:
        return self.__shockStyle

    @shockStyle.setter
    def shockStyle(self, value: str):
        self.__shockStyle = value
        self._property_changed('shockStyle')        

    @property
    def relativePeriod(self) -> str:
        return self.__relativePeriod

    @relativePeriod.setter
    def relativePeriod(self, value: str):
        self.__relativePeriod = value
        self._property_changed('relativePeriod')        

    @property
    def isin(self) -> str:
        return self.__isin

    @isin.setter
    def isin(self, value: str):
        self.__isin = value
        self._property_changed('isin')        

    @property
    def methodology(self) -> str:
        return self.__methodology

    @methodology.setter
    def methodology(self, value: str):
        self.__methodology = value
        self._property_changed('methodology')        
