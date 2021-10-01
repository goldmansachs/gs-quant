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

import deprecation
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, Priceable, Scenario, camel_case_translate, get_enum_value


class AggregationLevel(EnumBase, Enum):    
    
    """Aggregation Level"""

    Type = 'Type'
    Asset = 'Asset'
    Class = 'Class'
    Point = 'Point'    


class AssetClass(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which
       exhibit similar characteristics and behave in a consistent way under
       different market conditions"""

    Cash = 'Cash'
    Commod = 'Commod'
    Credit = 'Credit'
    Cross_Asset = 'Cross Asset'
    Econ = 'Econ'
    Equity = 'Equity'
    Fund = 'Fund'
    FX = 'FX'
    Mortgage = 'Mortgage'
    Rates = 'Rates'
    Loan = 'Loan'
    Social = 'Social'
    Cryptocurrency = 'Cryptocurrency'    


class AssetStatsPeriod(EnumBase, Enum):    
    
    """The period used to produce date range."""

    _1y = '1y'
    _3y = '3y'
    _5y = '5y'
    _10y = '10y'    


class AssetStatsType(EnumBase, Enum):    
    
    """Is it rolling, none etc."""

    Rolling = 'Rolling'
    Calendar = 'Calendar'
    YTD = 'YTD'    


class AssetType(EnumBase, Enum):    
    
    """Asset type differentiates the product categorization or contract type"""

    Access = 'Access'
    AssetSwapFxdFlt = 'AssetSwapFxdFlt'
    AssetSwapFxdFxd = 'AssetSwapFxdFxd'
    Any = 'Any'
    Autoroll = 'Autoroll'
    AveragePriceOption = 'AveragePriceOption'
    Basis = 'Basis'
    BasisSwap = 'BasisSwap'
    Benchmark = 'Benchmark'
    Benchmark_Rate = 'Benchmark Rate'
    Binary = 'Binary'
    Bond = 'Bond'
    BondFuture = 'BondFuture'
    BondFutureOption = 'BondFutureOption'
    BondOption = 'BondOption'
    Calendar_Spread = 'Calendar Spread'
    Cap = 'Cap'
    Cash = 'Cash'
    Certificate = 'Certificate'
    CD = 'CD'
    Cliquet = 'Cliquet'
    CMSOption = 'CMSOption'
    CMSOptionStrip = 'CMSOptionStrip'
    CMSSpreadOption = 'CMSSpreadOption'
    CMSSpreadOptionStrip = 'CMSSpreadOptionStrip'
    Commodity = 'Commodity'
    CommodityReferencePrice = 'CommodityReferencePrice'
    CommodVarianceSwap = 'CommodVarianceSwap'
    CommodityPowerNode = 'CommodityPowerNode'
    CommodityPowerAggregatedNodes = 'CommodityPowerAggregatedNodes'
    CommodityEUNaturalGasHub = 'CommodityEUNaturalGasHub'
    CommodityNaturalGasHub = 'CommodityNaturalGasHub'
    Company = 'Company'
    Convertible = 'Convertible'
    Credit_Basket = 'Credit Basket'
    Cross = 'Cross'
    CSL = 'CSL'
    Currency = 'Currency'
    Custom_Basket = 'Custom Basket'
    Cryptocurrency = 'Cryptocurrency'
    Default_Swap = 'Default Swap'
    DoubleKnockout = 'DoubleKnockout'
    DoubleTouch = 'DoubleTouch'
    Economic = 'Economic'
    Endowment = 'Endowment'
    Equity_Basket = 'Equity Basket'
    EuropeanKnockout = 'EuropeanKnockout'
    ETF = 'ETF'
    ETN = 'ETN'
    Event = 'Event'
    FRA = 'FRA'
    FixedLeg = 'FixedLeg'
    Fixing = 'Fixing'
    FloatLeg = 'FloatLeg'
    Floor = 'Floor'
    Forward = 'Forward'
    Fund = 'Fund'
    Future = 'Future'
    FutureContract = 'FutureContract'
    FutureMarket = 'FutureMarket'
    FutureOption = 'FutureOption'
    FutureStrategy = 'FutureStrategy'
    FXForward = 'FXForward'
    Hedge_Fund = 'Hedge Fund'
    Index = 'Index'
    IndexOption = 'IndexOption'
    InflationSwap = 'InflationSwap'
    Inter_Commodity_Spread = 'Inter-Commodity Spread'
    InvoiceSpread = 'InvoiceSpread'
    Knockout = 'Knockout'
    Market_Location = 'Market Location'
    MLF = 'MLF'
    Multi_Asset_Allocation = 'Multi-Asset Allocation'
    MultiCrossBinary = 'MultiCrossBinary'
    MultiCrossBinaryLeg = 'MultiCrossBinaryLeg'
    Mutual_Fund = 'Mutual Fund'
    Note = 'Note'
    OneTouch = 'OneTouch'
    Option = 'Option'
    OptionLeg = 'OptionLeg'
    OptionStrategy = 'OptionStrategy'
    Peer_Group = 'Peer Group'
    Pension_Fund = 'Pension Fund'
    Preferred_Stock = 'Preferred Stock'
    Physical = 'Physical'
    Precious_Metal = 'Precious Metal'
    Precious_Metal_Swap = 'Precious Metal Swap'
    Precious_Metal_RFQ = 'Precious Metal RFQ'
    Reference_Entity = 'Reference Entity'
    Research_Basket = 'Research Basket'
    Rate = 'Rate'
    Risk_Premia = 'Risk Premia'
    Roll = 'Roll'
    Securities_Lending_Loan = 'Securities Lending Loan'
    Share_Class = 'Share Class'
    Single_Stock = 'Single Stock'
    ShiftingBermForward = 'ShiftingBermForward'
    Swap = 'Swap'
    SwapLeg = 'SwapLeg'
    SwapStrategy = 'SwapStrategy'
    Swaption = 'Swaption'
    Synthetic = 'Synthetic'
    Systematic_Hedging = 'Systematic Hedging'
    VarianceSwap = 'VarianceSwap'
    VolatilitySwap = 'VolatilitySwap'
    VolVarSwap = 'VolVarSwap'
    WeatherIndex = 'WeatherIndex'
    XccySwap = 'XccySwap'
    XccySwapFixFix = 'XccySwapFixFix'
    XccySwapFixFlt = 'XccySwapFixFlt'
    XccySwapMTM = 'XccySwapMTM'    


class AswType(EnumBase, Enum):    
    
    """Asset Swap Type"""

    Par = 'Par'
    Proceeds = 'Proceeds'    


class BasketAction(EnumBase, Enum):    
    
    """Indicates what was the action taken on basket - create/edit/rebalance"""

    Create = 'Create'
    Edit = 'Edit'
    Rebalance = 'Rebalance'    


class BondStrikeType(EnumBase, Enum):    
    
    """The type of the bond strike - price, yield etc"""

    Price = 'Price'
    Yield = 'Yield'    


class BusinessDayConvention(EnumBase, Enum):    
    
    """Business Day Convention"""

    Following = 'Following'
    Modified_Following = 'Modified Following'
    Previous = 'Previous'
    Unadjusted = 'Unadjusted'    


class BuySell(EnumBase, Enum):    
    
    """Buy or Sell side of contract"""

    Buy = 'Buy'
    Sell = 'Sell'    


class CommodMeanRule(EnumBase, Enum):    
    
    """Commodity mean rule"""

    Do_Not_Remove = 'Do Not Remove'
    Remove_Calculated = 'Remove Calculated'
    Remove_Fixed = 'Remove Fixed'    


class CommodUnit(EnumBase, Enum):    
    
    """A coding scheme value to identify the unit of measure (e.g. Therms) in which the
       undelryer is denominated."""

    Lot = 'Lot'
    MegaWattHour = 'MegaWattHour'
    Metric_Ton = 'Metric Ton'
    Million_British_Thermal_Units = 'Million British Thermal Units'
    Oil_Barrel = 'Oil Barrel'
    Troy_Pound = 'Troy Pound'
    US_Gallon = 'US Gallon'    


class CommoditySector(EnumBase, Enum):    
    
    """The sector of the commodity"""

    Base_metals = 'Base metals'
    Precious_metals = 'Precious metals'
    Energy = 'Energy'
    Agriculturals = 'Agriculturals'
    Power = 'Power'    


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


class CreditOptionStrikeType(EnumBase, Enum):    
    
    Spread_Adj = 'Spread Adj'
    Delta = 'Delta'    


class CreditOptionType(EnumBase, Enum):    
    
    Payer = 'Payer'
    Receiver = 'Receiver'    


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
    SGS = 'SGS'
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


class CurrencyName(EnumBase, Enum):    
    
    """Currency Names"""

    United_States_Dollar = 'United States Dollar'
    Australian_Dollar = 'Australian Dollar'
    Canadian_Dollar = 'Canadian Dollar'
    Swiss_Franc = 'Swiss Franc'
    Yuan_Renminbi_Hong_Kong = 'Yuan Renminbi (Hong Kong)'
    Czech_Republic_Koruna = 'Czech Republic Koruna'
    Euro = 'Euro'
    Pound_Sterling = 'Pound Sterling'
    Japanese_Yen = 'Japanese Yen'
    South_Korean_Won = 'South Korean Won'
    Malasyan_Ringgit = 'Malasyan Ringgit'
    Norwegian_Krone = 'Norwegian Krone'
    New_Zealand_Dollar = 'New Zealand Dollar'
    Polish_Zloty = 'Polish Zloty'
    Russian_Rouble = 'Russian Rouble'
    Swedish_Krona = 'Swedish Krona'
    South_African_Rand = 'South African Rand'
    Yuan_Renminbi_Onshore = 'Yuan Renminbi (Onshore)'    


class DayCountFraction(EnumBase, Enum):    
    
    """Day Count Fraction"""

    ACT_OVER_360 = 'ACT/360'
    ACT_OVER_360_ISDA = 'ACT/360 ISDA'
    ACT_OVER_365_Fixed = 'ACT/365 (Fixed)'
    ACT_OVER_365_Fixed_ISDA = 'ACT/365 Fixed ISDA'
    ACT_OVER_365L_ISDA = 'ACT/365L ISDA'
    ACT_OVER_ACT_ISDA = 'ACT/ACT ISDA'
    ACT_OVER_ACT_ISMA = 'ACT/ACT ISMA'
    _30_OVER_360 = '30/360'
    _30E_OVER_360 = '30E/360'    


class Field(EnumBase, Enum):    
    
    """Field to be returned"""

    investmentRate = 'investmentRate'
    startingEmmaLegalEntityId = 'startingEmmaLegalEntityId'
    bvalMidPrice = 'bvalMidPrice'
    mdapiClass = 'mdapiClass'
    totalNotionalUSD = 'totalNotionalUSD'
    bidUnadjusted = 'bidUnadjusted'
    poRisk = 'poRisk'
    navTargetQuantity = 'navTargetQuantity'
    invertedCross = 'invertedCross'
    aggressiveFillsPercentage = 'aggressiveFillsPercentage'
    future10yrMarketCap = 'future10yrMarketCap'
    vehicleType = 'vehicleType'
    totalFatalitiesByState = 'totalFatalitiesByState'
    newActive = 'newActive'
    dailyRisk = 'dailyRisk'
    energy = 'energy'
    sunshineDailyForecast = 'sunshineDailyForecast'
    sentimentScore = 'sentimentScore'
    customerBuySell = 'customerBuySell'
    annualizedZCRate = 'annualizedZCRate'
    fxQuotedDeltaNoPremiumAdjustment = 'fxQuotedDeltaNoPremiumAdjustment'
    settlementRequested = 'settlementRequested'
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    correlation = 'correlation'
    exposure = 'exposure'
    size = 'size'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    marketDataAsset = 'marketDataAsset'
    _8 = '8'
    _9 = '9'
    buy75cents = 'buy75cents'
    unadjustedHigh = 'unadjustedHigh'
    sourceImportance = 'sourceImportance'
    closingYield = 'closingYield'
    wind = 'wind'
    sc16 = 'sc16'
    sc15 = 'sc15'
    sc12 = 'sc12'
    sc11 = 'sc11'
    primaryVwapInLimitUnrealizedBps = 'primaryVwapInLimitUnrealizedBps'
    displayName = 'displayName'
    minutesToTrade100Pct = 'minutesToTrade100Pct'
    sc14 = 'sc14'
    cumulativeVolumeInShares = 'cumulativeVolumeInShares'
    sc13 = 'sc13'
    newFatalities = 'newFatalities'
    buy50bps = 'buy50bps'
    numStaffedBeds = 'numStaffedBeds'
    upfrontPayment = 'upfrontPayment'
    annualizedRMCTRisk = 'annualizedRMCTRisk'
    arrivalMidRealizedCash = 'arrivalMidRealizedCash'
    sc10 = 'sc10'
    lowLeverage = 'lowLeverage'
    sc05 = 'sc05'
    lastTradingDateRule = 'lastTradingDateRule'
    a = 'a'
    sc04 = 'sc04'
    manualPricingTrader = 'manualPricingTrader'
    b = 'b'
    sc07 = 'sc07'
    c = 'c'
    yieldToMaturity = 'yieldToMaturity'
    sc06 = 'sc06'
    address = 'address'
    sc01 = 'sc01'
    leg2PaymentFrequency = 'leg2PaymentFrequency'
    sc03 = 'sc03'
    sc02 = 'sc02'
    geographyName = 'geographyName'
    borrower = 'borrower'
    shareClassType = 'shareClassType'
    settlePrice = 'settlePrice'
    assetParametersPutAmount = 'assetParametersPutAmount'
    performanceContribution = 'performanceContribution'
    sc09 = 'sc09'
    mktClass = 'mktClass'
    sc08 = 'sc08'
    collateralization = 'collateralization'
    futureMonthU26 = 'futureMonthU26'
    fxCalcDelta = 'fxCalcDelta'
    futureMonthU25 = 'futureMonthU25'
    futureMonthU24 = 'futureMonthU24'
    futureMonthU23 = 'futureMonthU23'
    futureMonthU22 = 'futureMonthU22'
    statementId = 'statementId'
    futureMonthU21 = 'futureMonthU21'
    assetParametersSettlementDate = 'assetParametersSettlementDate'
    modifiedDuration = 'modifiedDuration'
    impliedRetailSellPctShares = 'impliedRetailSellPctShares'
    vol180d = 'vol180d'
    fxQuotedDelta = 'fxQuotedDelta'
    shortRatesContribution = 'shortRatesContribution'
    impliedNormalVolatility = 'impliedNormalVolatility'
    solarGeneration = 'solarGeneration'
    requestedSide = 'requestedSide'
    mtmPrice = 'mtmPrice'
    swapSpreadChange = 'swapSpreadChange'
    realizedArrivalPerformanceUSD = 'realizedArrivalPerformanceUSD'
    portfolioAssets = 'portfolioAssets'
    tcmCostHorizon3Hour = 'tcmCostHorizon3Hour'
    exchangeRate = 'exchangeRate'
    potentialBedCapInc = 'potentialBedCapInc'
    numberCovered = 'numberCovered'
    numberOfPositions = 'numberOfPositions'
    openUnadjusted = 'openUnadjusted'
    strikeTime = 'strikeTime'
    askPrice = 'askPrice'
    eventId = 'eventId'
    sectors = 'sectors'
    additionalPriceNotationType = 'additionalPriceNotationType'
    grossInvestmentQtd = 'grossInvestmentQtd'
    annualizedRisk = 'annualizedRisk'
    estimatedHoldingTimeShort = 'estimatedHoldingTimeShort'
    impliedRetailBuyShares = 'impliedRetailBuyShares'
    outrightBid = 'outrightBid'
    midcurvePremium = 'midcurvePremium'
    volumeComposite = 'volumeComposite'
    sharpeQtd = 'sharpeQtd'
    clearingExceptionOrExemptionIndicator = 'clearingExceptionOrExemptionIndicator'
    estimatedHoldingTimeLong = 'estimatedHoldingTimeLong'
    external = 'external'
    trackerName = 'trackerName'
    sell50cents = 'sell50cents'
    tradePrice = 'tradePrice'
    cleared = 'cleared'
    primeIdNumeric = 'primeIdNumeric'
    buy8bps = 'buy8bps'
    totalNotionalLocal = 'totalNotionalLocal'
    cid = 'cid'
    totalConfirmedSeniorHome = 'totalConfirmedSeniorHome'
    ctdFwdPrice = 'ctdFwdPrice'
    sinkFactor = 'sinkFactor'
    assetParametersNotionalAmountInOtherCurrency = 'assetParametersNotionalAmountInOtherCurrency'
    assetParametersPair = 'assetParametersPair'
    temperatureForecast = 'temperatureForecast'
    primaryAssetClass = 'primaryAssetClass'
    bidHigh = 'bidHigh'
    pnlQtd = 'pnlQtd'
    buy50cents = 'buy50cents'
    impliedRetailPctNotional = 'impliedRetailPctNotional'
    sell4bps = 'sell4bps'
    receiverDayCountFraction = 'receiverDayCountFraction'
    auctionClosePercentage = 'auctionClosePercentage'
    targetPrice = 'targetPrice'
    bosInBpsDescription = 'bosInBpsDescription'
    lowPrice = 'lowPrice'
    adv22DayPct = 'adv22DayPct'
    contractMonthLetters = 'contractMonthLetters'
    gateType = 'gateType'
    matchedMaturitySwapSpread12m = 'matchedMaturitySwapSpread12m'
    priceRangeInTicksLabel = 'priceRangeInTicksLabel'
    ticker = 'ticker'
    notionalUnit = 'notionalUnit'
    tcmCostHorizon1Day = 'tcmCostHorizon1Day'
    approval = 'approval'
    testMeasure = 'testMeasure'
    fwdSpreadMode = 'fwdSpreadMode'
    optionLockOutPeriod = 'optionLockOutPeriod'
    executionTime = 'executionTime'
    retailActivity = 'retailActivity'
    sourceValueForecast = 'sourceValueForecast'
    leg2Spread = 'leg2Spread'
    annualizedMCTRisk = 'annualizedMCTRisk'
    shortConvictionLarge = 'shortConvictionLarge'
    leg1FloatingRateIndex = 'leg1FloatingRateIndex'
    ccgName = 'ccgName'
    multiTags = 'multiTags'
    bidGSpread = 'bidGSpread'
    dollarExcessReturn = 'dollarExcessReturn'
    gsn = 'gsn'
    tradeEndDate = 'tradeEndDate'
    receiverRateOption = 'receiverRateOption'
    gss = 'gss'
    percentOfMediandv1m = 'percentOfMediandv1m'
    lendables = 'lendables'
    sell75cents = 'sell75cents'
    optionAdjustedSpread = 'optionAdjustedSpread'
    optionAdjustedSwapSpread = 'optionAdjustedSwapSpread'
    bosInTicksLabel = 'bosInTicksLabel'
    positionSourceId = 'positionSourceId'
    buy1bps = 'buy1bps'
    activeIDAtClient = 'activeIDAtClient'
    buy3point5bps = 'buy3point5bps'
    gsSustainRegion = 'gsSustainRegion'
    absoluteReturnWtd = 'absoluteReturnWtd'
    deploymentId = 'deploymentId'
    tradedActiveID = 'tradedActiveID'
    assetParametersSeniority = 'assetParametersSeniority'
    askSpread = 'askSpread'
    flow = 'flow'
    futureMonthH26 = 'futureMonthH26'
    loanRebate = 'loanRebate'
    futureMonthH25 = 'futureMonthH25'
    period = 'period'
    indexCreateSource = 'indexCreateSource'
    futureMonthH24 = 'futureMonthH24'
    futureMonthH23 = 'futureMonthH23'
    futureMonthH22 = 'futureMonthH22'
    futureMonthH21 = 'futureMonthH21'
    nonUsdOis = 'nonUsdOis'
    realTWIContribution = 'realTWIContribution'
    mktAsset = 'mktAsset'
    leg2IndexLocation = 'leg2IndexLocation'
    twapUnrealizedBps = 'twapUnrealizedBps'
    fwdEbookPointSpreadAllInMultBid = 'fwdEbookPointSpreadAllInMultBid'
    quantityUnitOfMeasure = 'quantityUnitOfMeasure'
    lastUpdatedMessage = 'lastUpdatedMessage'
    loanValue = 'loanValue'
    optionAdjustedOISSpread = 'optionAdjustedOISSpread'
    clientFwdSpreadMultiplier = 'clientFwdSpreadMultiplier'
    totalReturnPrice = 'totalReturnPrice'
    valueCurrency = 'valueCurrency'
    weightedPercentInModel = 'weightedPercentInModel'
    initLoanSpreadRequired = 'initLoanSpreadRequired'
    electionPeriod = 'electionPeriod'
    fundingAskPrice = 'fundingAskPrice'
    historicalBeta = 'historicalBeta'
    bondRiskPremiumIndex = 'bondRiskPremiumIndex'
    hitRateYtd = 'hitRateYtd'
    girGsdeerGsfeer = 'girGsdeerGsfeer'
    numUnits = 'numUnits'
    assetParametersReceiverFrequency = 'assetParametersReceiverFrequency'
    expenseRatioGrossBps = 'expenseRatioGrossBps'
    relativePayoffWtd = 'relativePayoffWtd'
    ctdPrice = 'ctdPrice'
    paceOfRollNow = 'paceOfRollNow'
    product = 'product'
    leg2ReturnType = 'leg2ReturnType'
    agentLenderFee = 'agentLenderFee'
    baseUSDFwdRevenue = 'baseUSDFwdRevenue'
    disseminationId = 'disseminationId'
    optionStrikePrice = 'optionStrikePrice'
    precipitationType = 'precipitationType'
    lowerBound = 'lowerBound'
    entity = 'entity'
    active1yrMarketCap = 'active1yrMarketCap'
    arrivalMidNormalized = 'arrivalMidNormalized'
    underlyingAsset2 = 'underlyingAsset2'
    underlyingAsset1 = 'underlyingAsset1'
    legalEntity = 'legalEntity'
    performanceFee = 'performanceFee'
    orderState = 'orderState'
    actualDataQuality = 'actualDataQuality'
    indexRatio = 'indexRatio'
    traderDescription = 'traderDescription'
    queueInLotsLabel = 'queueInLotsLabel'
    adv10DayPct = 'adv10DayPct'
    longConvictionMedium = 'longConvictionMedium'
    relativeHitRateWtd = 'relativeHitRateWtd'
    dailyTrackingError = 'dailyTrackingError'
    sell140cents = 'sell140cents'
    sell10bps = 'sell10bps'
    aggressiveOffsetFromLast = 'aggressiveOffsetFromLast'
    longitude = 'longitude'
    newIcu = 'newIcu'
    marketCap = 'marketCap'
    entryType = 'entryType'
    weightedAverageMid = 'weightedAverageMid'
    clusterRegion = 'clusterRegion'
    valoren = 'valoren'
    indexName = 'indexName'
    averageExecutionPrice = 'averageExecutionPrice'
    usdFwdRevenue = 'usdFwdRevenue'
    proceedsAssetOISSwapSpread1m = 'proceedsAssetOISSwapSpread1m'
    payoffWtd = 'payoffWtd'
    basis = 'basis'
    investmentRateTrend = 'investmentRateTrend'
    grossInvestmentMtd = 'grossInvestmentMtd'
    _200 = '200'
    hedgeId = 'hedgeId'
    _201 = '201'
    sharpeMtd = 'sharpeMtd'
    _202 = '202'
    _203 = '203'
    tcmCostHorizon8Day = 'tcmCostHorizon8Day'
    _204 = '204'
    residualVariance = 'residualVariance'
    _205 = '205'
    restrictInternalDerivedData = 'restrictInternalDerivedData'
    _206 = '206'
    _207 = '207'
    _208 = '208'
    adv5DayPct = 'adv5DayPct'
    _209 = '209'
    midpointFillsPercentage = 'midpointFillsPercentage'
    riskPackages = 'riskPackages'
    openInterest = 'openInterest'
    turnoverCompositeUnadjusted = 'turnoverCompositeUnadjusted'
    fwdPoints = 'fwdPoints'
    relativeReturnWtd = 'relativeReturnWtd'
    units = 'units'
    payerRateOption = 'payerRateOption'
    assetClassificationsRiskCountryName = 'assetClassificationsRiskCountryName'
    extMktPoint3 = 'extMktPoint3'
    _210 = '210'
    _211 = '211'
    matchedMaturitySwapSpread = 'matchedMaturitySwapSpread'
    _212 = '212'
    cityName = 'cityName'
    _213 = '213'
    hourlyBucket = 'hourlyBucket'
    _214 = '214'
    averageImpliedVolatility = 'averageImpliedVolatility'
    totalHospitalizedWithSymptoms = 'totalHospitalizedWithSymptoms'
    _215 = '215'
    _216 = '216'
    _217 = '217'
    daysOpenRealizedCash = 'daysOpenRealizedCash'
    _218 = '218'
    _219 = '219'
    adjustedHighPrice = 'adjustedHighPrice'
    proceedsAssetOISSwapSpread = 'proceedsAssetOISSwapSpread'
    m2RPrice = 'm2RPrice'
    extMktPoint1 = 'extMktPoint1'
    direction = 'direction'
    extMktPoint2 = 'extMktPoint2'
    subRegionCode = 'subRegionCode'
    assetParametersFixedRate = 'assetParametersFixedRate'
    tsdbSyncedSymbol = 'tsdbSyncedSymbol'
    factorProportionOfRisk = 'factorProportionOfRisk'
    isEstimatedReturn = 'isEstimatedReturn'
    valueForecast = 'valueForecast'
    totalIcu = 'totalIcu'
    positionSourceType = 'positionSourceType'
    previousCloseUnrealizedCash = 'previousCloseUnrealizedCash'
    minimumDenomination = 'minimumDenomination'
    assetParametersStrikePriceRelative = 'assetParametersStrikePriceRelative'
    futureValueNotional = 'futureValueNotional'
    participationRate = 'participationRate'
    obfr = 'obfr'
    _220 = '220'
    _221 = '221'
    _222 = '222'
    buy9point5bps = 'buy9point5bps'
    _223 = '223'
    specificReturn = 'specificReturn'
    _224 = '224'
    _225 = '225'
    optionLockPeriod = 'optionLockPeriod'
    _226 = '226'
    esMomentumPercentile = 'esMomentumPercentile'
    _227 = '227'
    _228 = '228'
    advPercentage = 'advPercentage'
    _229 = '229'
    leg1AveragingMethod = 'leg1AveragingMethod'
    activeIDLatest = 'activeIDLatest'
    turnoverComposite = 'turnoverComposite'
    forecastDate = 'forecastDate'
    internalIndexCalcRegion = 'internalIndexCalcRegion'
    positionType = 'positionType'
    subAssetClass = 'subAssetClass'
    shortInterest = 'shortInterest'
    referencePeriod = 'referencePeriod'
    adjustedVolume = 'adjustedVolume'
    underlyingAssetIdType = 'underlyingAssetIdType'
    ctdFwdYield = 'ctdFwdYield'
    assetParametersStart = 'assetParametersStart'
    secDB = 'secDB'
    memoryUsed = 'memoryUsed'
    bpeQualityStars = 'bpeQualityStars'
    leg = 'leg'
    _230 = '230'
    _231 = '231'
    _232 = '232'
    ctd = 'ctd'
    _233 = '233'
    _234 = '234'
    _235 = '235'
    _236 = '236'
    _237 = '237'
    _238 = '238'
    _239 = '239'
    intendedParticipationRate = 'intendedParticipationRate'
    leg1PaymentType = 'leg1PaymentType'
    tradingPnl = 'tradingPnl'
    collateralValueRequired = 'collateralValueRequired'
    buy45bps = 'buy45bps'
    freeFloatMarketCapRatio = 'freeFloatMarketCapRatio'
    priceToEarningsPositive = 'priceToEarningsPositive'
    outrightAsk = 'outrightAsk'
    assetParametersPayerCurrency = 'assetParametersPayerCurrency'
    forecast = 'forecast'
    forecastValue = 'forecastValue'
    meanDailyVolume5d = 'meanDailyVolume5d'
    _240 = '240'
    pnl = 'pnl'
    _241 = '241'
    _242 = '242'
    _243 = '243'
    volumeInLimit = 'volumeInLimit'
    _244 = '244'
    isTerritory = 'isTerritory'
    fwdEbookRiskDirClientSellUnder = 'fwdEbookRiskDirClientSellUnder'
    _245 = '245'
    meanDailyVolume22d = 'meanDailyVolume22d'
    leg2DeliveryPoint = 'leg2DeliveryPoint'
    _246 = '246'
    _247 = '247'
    _248 = '248'
    _249 = '249'
    tcmCostHorizon4Day = 'tcmCostHorizon4Day'
    styles = 'styles'
    shortName = 'shortName'
    resetFrequency1 = 'resetFrequency1'
    buy4bps = 'buy4bps'
    resetFrequency2 = 'resetFrequency2'
    otherPriceTerm = 'otherPriceTerm'
    bidGspread = 'bidGspread'
    tradedMktFwdPointsMid = 'tradedMktFwdPointsMid'
    openPrice = 'openPrice'
    rfqState = 'rfqState'
    psId = 'psId'
    hitRateMtd = 'hitRateMtd'
    fairVolatility = 'fairVolatility'
    dollarCross = 'dollarCross'
    portfolioType = 'portfolioType'
    optionExpirationRule = 'optionExpirationRule'
    currency = 'currency'
    clusterClass = 'clusterClass'
    sell50bps = 'sell50bps'
    futureMonthM21 = 'futureMonthM21'
    bidSize = 'bidSize'
    coordinateId = 'coordinateId'
    arrivalMid = 'arrivalMid'
    marginalContributionToRiskPercent = 'marginalContributionToRiskPercent'
    assetParametersExchangeCurrency = 'assetParametersExchangeCurrency'
    candidateName = 'candidateName'
    positionDate = 'positionDate'
    impliedLognormalVolatility = 'impliedLognormalVolatility'
    vwapInLimitUnrealizedCash = 'vwapInLimitUnrealizedCash'
    ratingMoodys = 'ratingMoodys'
    futureMonthM26 = 'futureMonthM26'
    futureMonthM25 = 'futureMonthM25'
    futureMonthM24 = 'futureMonthM24'
    futureMonthM23 = 'futureMonthM23'
    developmentStatus = 'developmentStatus'
    futureMonthM22 = 'futureMonthM22'
    flowPct = 'flowPct'
    source = 'source'
    assetClassificationsCountryCode = 'assetClassificationsCountryCode'
    settleDrop = 'settleDrop'
    dataSetSubCategory = 'dataSetSubCategory'
    sell9point5bps = 'sell9point5bps'
    quantityBucket = 'quantityBucket'
    optionStyleSDR = 'optionStyleSDR'
    initialIndexLevel = 'initialIndexLevel'
    cvaDollarChargeAsk = 'cvaDollarChargeAsk'
    oeName = 'oeName'
    given = 'given'
    leg2DayCountConvention = 'leg2DayCountConvention'
    liquidityScoreSell = 'liquidityScoreSell'
    delistingDate = 'delistingDate'
    weight = 'weight'
    accruedInterest = 'accruedInterest'
    businessScope = 'businessScope'
    wtdDegreeDays = 'wtdDegreeDays'
    absoluteWeight = 'absoluteWeight'
    measure = 'measure'
    return30d = 'return30d'
    temperatureHourlyForecast = 'temperatureHourlyForecast'
    icebergTipRateType = 'icebergTipRateType'
    sharpeYtd = 'sharpeYtd'
    windSpeedForecast = 'windSpeedForecast'
    grossInvestmentYtd = 'grossInvestmentYtd'
    yieldPrice = 'yieldPrice'
    paymentFrequencyPeriodMultiplier2 = 'paymentFrequencyPeriodMultiplier2'
    paymentFrequencyPeriodMultiplier1 = 'paymentFrequencyPeriodMultiplier1'
    leg1TotalNotionalUnit = 'leg1TotalNotionalUnit'
    absoluteAttribution = 'absoluteAttribution'
    issuePrice = 'issuePrice'
    quantityCcy = 'quantityCcy'
    askHigh = 'askHigh'
    expectedDataQuality = 'expectedDataQuality'
    regionName = 'regionName'
    valueRevised = 'valueRevised'
    discretionUpperBound = 'discretionUpperBound'
    adjustedTradePrice = 'adjustedTradePrice'
    forecastTime = 'forecastTime'
    isoSubdivisionCodeAlpha2 = 'isoSubdivisionCodeAlpha2'
    ctdConversionFactor = 'ctdConversionFactor'
    impliedRetailNotionalw5kFilter = 'impliedRetailNotionalw5kFilter'
    proceedsAssetSwapSpread = 'proceedsAssetSwapSpread'
    isADR = 'isADR'
    issueDate = 'issueDate'
    serviceId = 'serviceId'
    yes = 'yes'
    gScore = 'gScore'
    impliedRetailNotionalw10kFilter = 'impliedRetailNotionalw10kFilter'
    marketValue = 'marketValue'
    entityId = 'entityId'
    notionalCurrency1 = 'notionalCurrency1'
    netDebtToEbitda = 'netDebtToEbitda'
    numUnitsUpper = 'numUnitsUpper'
    notionalCurrency2 = 'notionalCurrency2'
    inLimitParticipationRate = 'inLimitParticipationRate'
    spotMarketBid = 'spotMarketBid'
    pressureForecast = 'pressureForecast'
    paid = 'paid'
    fixedRate = 'fixedRate'
    short = 'short'
    time = 'time'
    buy4point5bps = 'buy4point5bps'
    sell30cents = 'sell30cents'
    eventEndDateTime = 'eventEndDateTime'
    leg1PaymentFrequency = 'leg1PaymentFrequency'
    cmId = 'cmId'
    taxonomy = 'taxonomy'
    buy45cents = 'buy45cents'
    measures = 'measures'
    seasonalAdjustment = 'seasonalAdjustment'
    clientDescription = 'clientDescription'
    assetParametersNotionalAmount = 'assetParametersNotionalAmount'
    rankWtd = 'rankWtd'
    underlyer = 'underlyer'
    createdTime = 'createdTime'
    return1yr = 'return1yr'
    matchingOrderFwdPointBid = 'matchingOrderFwdPointBid'
    identifier = 'identifier'
    priceUnit = 'priceUnit'
    tradeReportRefId = 'tradeReportRefId'
    subdivisionId = 'subdivisionId'
    primaryMarketVolume = 'primaryMarketVolume'
    unadjustedLow = 'unadjustedLow'
    buy160cents = 'buy160cents'
    portfolioId = 'portfolioId'
    zSpread = 'zSpread'
    floatingRateResetFrequencyPeriod2 = 'floatingRateResetFrequencyPeriod2'
    capFloorAtmFwdRate = 'capFloorAtmFwdRate'
    esPercentile = 'esPercentile'
    tdapi = 'tdapi'
    floatingRateResetFrequencyPeriod1 = 'floatingRateResetFrequencyPeriod1'
    locationCode = 'locationCode'
    yieldToConvention = 'yieldToConvention'
    rcic = 'rcic'
    nameRaw = 'nameRaw'
    simonAssetTags = 'simonAssetTags'
    hitRateQtd = 'hitRateQtd'
    primaryVolumeInLimit = 'primaryVolumeInLimit'
    precipitationDailyForecastPercent = 'precipitationDailyForecastPercent'
    aumEnd = 'aumEnd'
    mktFwdPointMid = 'mktFwdPointMid'
    premium = 'premium'
    low = 'low'
    crossGroup = 'crossGroup'
    reportRunTime = 'reportRunTime'
    fiveDayPriceChangeBps = 'fiveDayPriceChangeBps'
    holdings = 'holdings'
    precipitationDailyForecast = 'precipitationDailyForecast'
    fixedRecoveryCDSFinalPrice = 'fixedRecoveryCDSFinalPrice'
    priceMethod = 'priceMethod'
    assetParametersFixedRateFrequency = 'assetParametersFixedRateFrequency'
    oisXccy = 'oisXccy'
    clientFwdPointsBid = 'clientFwdPointsBid'
    daysOpen = 'daysOpen'
    buy110cents = 'buy110cents'
    highInterestCoverage = 'highInterestCoverage'
    averageSpreadBps = 'averageSpreadBps'
    buy55cents = 'buy55cents'
    assetParametersReceiverCurrency = 'assetParametersReceiverCurrency'
    underlyingAssetIdSDR = 'underlyingAssetIdSDR'
    futureMonthQ26 = 'futureMonthQ26'
    issueSize = 'issueSize'
    futureMonthQ25 = 'futureMonthQ25'
    futureMonthQ24 = 'futureMonthQ24'
    futureMonthQ23 = 'futureMonthQ23'
    futureMonthQ22 = 'futureMonthQ22'
    pendingLoanCount = 'pendingLoanCount'
    futureMonthQ21 = 'futureMonthQ21'
    priceSpotStopLossUnit = 'priceSpotStopLossUnit'
    priceRangeInTicksDescription = 'priceRangeInTicksDescription'
    tradeVolume = 'tradeVolume'
    primaryCountryRic = 'primaryCountryRic'
    chargeInBps = 'chargeInBps'
    optionExpirationFrequency = 'optionExpirationFrequency'
    assetParametersIndexVersion = 'assetParametersIndexVersion'
    assetParametersCommodityReferencePrice = 'assetParametersCommodityReferencePrice'
    isActive = 'isActive'
    useMachineLearning = 'useMachineLearning'
    growthScore = 'growthScore'
    bufferThreshold = 'bufferThreshold'
    buy120cents = 'buy120cents'
    matchedMaturitySwapRate = 'matchedMaturitySwapRate'
    underlyingAssetName = 'underlyingAssetName'
    primaryVwap = 'primaryVwap'
    exchangeTypeId = 'exchangeTypeId'
    basisSwapRate = 'basisSwapRate'
    exchangeCode = 'exchangeCode'
    group = 'group'
    assetParametersTerminationDate = 'assetParametersTerminationDate'
    estimatedSpread = 'estimatedSpread'
    yieldChangeOnDay = 'yieldChangeOnDay'
    created = 'created'
    autoTags = 'autoTags'
    tcmCost = 'tcmCost'
    sustainJapan = 'sustainJapan'
    historyStartDate = 'historyStartDate'
    bidSpread = 'bidSpread'
    usdQuantity = 'usdQuantity'
    percentageComplete = 'percentageComplete'
    marketSymbol = 'marketSymbol'
    hedgeTrackingError = 'hedgeTrackingError'
    assetParametersPutCurrency = 'assetParametersPutCurrency'
    termStatus = 'termStatus'
    windSpeedType = 'windSpeedType'
    strikePrice = 'strikePrice'
    lowInterestCoverage = 'lowInterestCoverage'
    parAssetSwapSpread12m = 'parAssetSwapSpread12m'
    tradeReportId = 'tradeReportId'
    adjustedOpenPrice = 'adjustedOpenPrice'
    countryId = 'countryId'
    point = 'point'
    pnlMtd = 'pnlMtd'
    totalReturns = 'totalReturns'
    lender = 'lender'
    annReturn1Year = 'annReturn1Year'
    ctdFwdDv01 = 'ctdFwdDv01'
    effYield7Day = 'effYield7Day'
    meetingDate = 'meetingDate'
    alias = 'alias'
    calendarSpreadMispricing = 'calendarSpreadMispricing'
    buy140cents = 'buy140cents'
    priceNotation2Type = 'priceNotation2Type'
    fundFocus = 'fundFocus'
    relativeStrike = 'relativeStrike'
    fwdEbookRiskDirClientBuyOver = 'fwdEbookRiskDirClientBuyOver'
    flagship = 'flagship'
    additionalPriceNotation = 'additionalPriceNotation'
    factorCategory = 'factorCategory'
    equityDelta = 'equityDelta'
    grossWeight = 'grossWeight'
    listed = 'listed'
    sell7bps = 'sell7bps'
    earningsRecordType = 'earningsRecordType'
    mean = 'mean'
    askYield = 'askYield'
    shockStyle = 'shockStyle'
    impliedRetailShares = 'impliedRetailShares'
    methodology = 'methodology'
    buy25cents = 'buy25cents'
    amountOutstanding = 'amountOutstanding'
    marketPnl = 'marketPnl'
    sustainAsiaExJapan = 'sustainAsiaExJapan'
    sell6point5bps = 'sell6point5bps'
    neighbourAssetId = 'neighbourAssetId'
    countIdeasYtd = 'countIdeasYtd'
    simonIntlAssetTags = 'simonIntlAssetTags'
    path = 'path'
    vwapUnrealizedCash = 'vwapUnrealizedCash'
    payoffMtd = 'payoffMtd'
    spread2 = 'spread2'
    bosInBpsLabel = 'bosInBpsLabel'
    spread1 = 'spread1'
    bosInBps = 'bosInBps'
    pointClass = 'pointClass'
    fxSpot = 'fxSpot'
    restrictNamedIndividuals = 'restrictNamedIndividuals'
    pricedBy = 'pricedBy'
    hedgeVolatility = 'hedgeVolatility'
    tags = 'tags'
    population = 'population'
    underlyingAssetId = 'underlyingAssetId'
    realLongRatesContribution = 'realLongRatesContribution'
    pctprices_return = 'pctprices_return'
    domain = 'domain'
    buy80cents = 'buy80cents'
    forwardTenor = 'forwardTenor'
    averagePrice = 'averagePrice'
    impliedRetailPctShares = 'impliedRetailPctShares'
    expectedUpdateTime = 'expectedUpdateTime'
    targetPriceRealizedBps = 'targetPriceRealizedBps'
    leg2FixedRate = 'leg2FixedRate'
    shareClassAssets = 'shareClassAssets'
    annuity = 'annuity'
    totalCount = 'totalCount'
    quoteType = 'quoteType'
    corporateActionStatus = 'corporateActionStatus'
    peggedTipSize = 'peggedTipSize'
    uid = 'uid'
    esPolicyPercentile = 'esPolicyPercentile'
    usdOis = 'usdOis'
    term = 'term'
    restrictInternalGsNtk = 'restrictInternalGsNtk'
    tcmCostParticipationRate100Pct = 'tcmCostParticipationRate100Pct'
    relativeUniverse = 'relativeUniverse'
    measureIdx = 'measureIdx'
    executedQuantity = 'executedQuantity'
    fredId = 'fredId'
    twiContribution = 'twiContribution'
    cloudCoverType = 'cloudCoverType'
    delisted = 'delisted'
    regionalFocus = 'regionalFocus'
    volumePrimary = 'volumePrimary'
    assetParametersPayerDesignatedMaturity = 'assetParametersPayerDesignatedMaturity'
    buy30cents = 'buy30cents'
    numLegs = 'numLegs'
    fundingBidPrice = 'fundingBidPrice'
    series = 'series'
    sell3bps = 'sell3bps'
    settlementPrice = 'settlementPrice'
    quarter = 'quarter'
    outrightMarketBid = 'outrightMarketBid'
    sell18bps = 'sell18bps'
    assetParametersFloatingRateOption = 'assetParametersFloatingRateOption'
    TRSAskPrice = 'TRSAskPrice'
    realizedVwapPerformanceBps = 'realizedVwapPerformanceBps'
    voteShare = 'voteShare'
    servicingCostShortPnl = 'servicingCostShortPnl'
    totalConfirmed = 'totalConfirmed'
    isLive = 'isLive'
    economicForecast = 'economicForecast'
    plotId = 'plotId'
    clusterDescription = 'clusterDescription'
    concentrationLimit = 'concentrationLimit'
    windSpeed = 'windSpeed'
    observationHour = 'observationHour'
    signal = 'signal'
    borrowerId = 'borrowerId'
    dataProduct = 'dataProduct'
    buy7point5bps = 'buy7point5bps'
    limitPrice = 'limitPrice'
    bmPrimeId = 'bmPrimeId'
    dataType = 'dataType'
    count = 'count'
    conviction = 'conviction'
    benchmarkMaturity = 'benchmarkMaturity'
    grossFlowNormalized = 'grossFlowNormalized'
    buy14bps = 'buy14bps'
    factorId = 'factorId'
    futureMonthV26 = 'futureMonthV26'
    stsFxCurrency = 'stsFxCurrency'
    futureMonthV25 = 'futureMonthV25'
    bidChange = 'bidChange'
    month = 'month'
    futureMonthV24 = 'futureMonthV24'
    investmentWtd = 'investmentWtd'
    futureMonthV23 = 'futureMonthV23'
    futureMonthV22 = 'futureMonthV22'
    futureMonthV21 = 'futureMonthV21'
    expiration = 'expiration'
    leg2ResetFrequency = 'leg2ResetFrequency'
    controversyScore = 'controversyScore'
    proceedAssetSwapSpread = 'proceedAssetSwapSpread'
    concentrationLevel = 'concentrationLevel'
    importance = 'importance'
    assetClassificationsGicsSector = 'assetClassificationsGicsSector'
    stsAssetName = 'stsAssetName'
    netExposureClassification = 'netExposureClassification'
    settlementMethod = 'settlementMethod'
    receiverDesignatedMaturity = 'receiverDesignatedMaturity'
    title = 'title'
    xRefTypeId = 'xRefTypeId'
    duration = 'duration'
    load = 'load'
    highLeverage = 'highLeverage'
    alpha = 'alpha'
    datasetId = 'datasetId'
    company = 'company'
    settlementFrequency = 'settlementFrequency'
    distAvg7Day = 'distAvg7Day'
    inRiskModel = 'inRiskModel'
    dailyNetShareholderFlowsPercent = 'dailyNetShareholderFlowsPercent'
    filledNotionalLocal = 'filledNotionalLocal'
    everHospitalized = 'everHospitalized'
    meetingNumber = 'meetingNumber'
    midGspread = 'midGspread'
    daysOpenUnrealizedBps = 'daysOpenUnrealizedBps'
    longLevel = 'longLevel'
    dataDescription = 'dataDescription'
    temperatureType = 'temperatureType'
    isSpecialDay = 'isSpecialDay'
    tradedUSDDiscountFactor = 'tradedUSDDiscountFactor'
    gsideid = 'gsideid'
    repoRate = 'repoRate'
    division = 'division'
    cloudCoverDailyForecast = 'cloudCoverDailyForecast'
    windSpeedDailyForecast = 'windSpeedDailyForecast'
    executionVenueType = 'executionVenueType'
    assetParametersFloatingRateDayCountFraction = 'assetParametersFloatingRateDayCountFraction'
    tradeAction = 'tradeAction'
    action = 'action'
    ctdYield = 'ctdYield'
    arrivalHaircutVwapNormalized = 'arrivalHaircutVwapNormalized'
    priceComponent = 'priceComponent'
    queueClockTimeDescription = 'queueClockTimeDescription'
    assetParametersReceiverDayCountFraction = 'assetParametersReceiverDayCountFraction'
    percentMidExecutionQuantity = 'percentMidExecutionQuantity'
    deltaStrike = 'deltaStrike'
    cloudCover = 'cloudCover'
    assetParametersNotionalCurrency = 'assetParametersNotionalCurrency'
    buy18bps = 'buy18bps'
    valueActual = 'valueActual'
    upi = 'upi'
    tradeRejectionReason = 'tradeRejectionReason'
    fixedRate1 = 'fixedRate1'
    collateralCurrency = 'collateralCurrency'
    originalCountry = 'originalCountry'
    fixedRate2 = 'fixedRate2'
    field = 'field'
    geographicFocus = 'geographicFocus'
    daysOpenRealizedBps = 'daysOpenRealizedBps'
    fxRiskPremiumIndex = 'fxRiskPremiumIndex'
    skew = 'skew'
    status = 'status'
    notionalCurrency = 'notionalCurrency'
    sustainEmergingMarkets = 'sustainEmergingMarkets'
    eventDateTime = 'eventDateTime'
    leg1DesignatedMaturity = 'leg1DesignatedMaturity'
    clientName = 'clientName'
    totalPrice = 'totalPrice'
    onBehalfOf = 'onBehalfOf'
    testType = 'testType'
    accruedInterestStandard = 'accruedInterestStandard'
    futureMonthZ26 = 'futureMonthZ26'
    futureMonthZ25 = 'futureMonthZ25'
    ccgCode = 'ccgCode'
    shortExposure = 'shortExposure'
    leg1FixedPaymentCurrency = 'leg1FixedPaymentCurrency'
    map = 'map'
    arrivalHaircutVwap = 'arrivalHaircutVwap'
    executionDays = 'executionDays'
    recallDueDate = 'recallDueDate'
    mktFwdSpreadMultiplier = 'mktFwdSpreadMultiplier'
    impliedRetailNotionalw2kFilter = 'impliedRetailNotionalw2kFilter'
    forward = 'forward'
    strike = 'strike'
    spreadLimit = 'spreadLimit'
    sopr = 'sopr'
    otherPaymentAmount = 'otherPaymentAmount'
    productScope = 'productScope'
    redemptionPeriod = 'redemptionPeriod'
    assetParametersIssuerType = 'assetParametersIssuerType'
    currency1 = 'currency1'
    currency2 = 'currency2'
    previousCloseRealizedBps = 'previousCloseRealizedBps'
    daysSinceReported = 'daysSinceReported'
    eventStatus = 'eventStatus'
    vwapInLimit = 'vwapInLimit'
    fwdDuration = 'fwdDuration'
    _return = 'return'
    isPairBasket = 'isPairBasket'
    notionalAmount = 'notionalAmount'
    optionPremiumAmount = 'optionPremiumAmount'
    payOrReceive = 'payOrReceive'
    impliedRetailSellPctNotional = 'impliedRetailSellPctNotional'
    totalSevere = 'totalSevere'
    unexecutedNotionalUSD = 'unexecutedNotionalUSD'
    expectedResidualPercentage = 'expectedResidualPercentage'
    maturityDate = 'maturityDate'
    traceAdvSell = 'traceAdvSell'
    eventName = 'eventName'
    addressLine2 = 'addressLine2'
    indicationOfOtherPriceAffectingTerm = 'indicationOfOtherPriceAffectingTerm'
    unadjustedBid = 'unadjustedBid'
    backtestType = 'backtestType'
    gsdeer = 'gsdeer'
    assetParametersIssuer = 'assetParametersIssuer'
    gRegionalPercentile = 'gRegionalPercentile'
    coverageChecked = 'coverageChecked'
    oisXccyExSpike = 'oisXccyExSpike'
    totalRisk = 'totalRisk'
    mnav = 'mnav'
    marketVolume = 'marketVolume'
    swapAnnuity = 'swapAnnuity'
    parAssetSwapSpread = 'parAssetSwapSpread'
    currYield7Day = 'currYield7Day'
    pressure = 'pressure'
    shortDescription = 'shortDescription'
    factorProfile = 'factorProfile'
    futureMonthZ24 = 'futureMonthZ24'
    feed = 'feed'
    futureMonthZ23 = 'futureMonthZ23'
    mktPoint1 = 'mktPoint1'
    futureMonthZ22 = 'futureMonthZ22'
    futureMonthZ21 = 'futureMonthZ21'
    futureMonthZ20 = 'futureMonthZ20'
    assetParametersCommoditySector = 'assetParametersCommoditySector'
    priceNotation2 = 'priceNotation2'
    marketBufferThreshold = 'marketBufferThreshold'
    priceNotation3 = 'priceNotation3'
    mktPoint3 = 'mktPoint3'
    mktPoint2 = 'mktPoint2'
    leg2Type = 'leg2Type'
    mktPoint4 = 'mktPoint4'
    degreeDaysType = 'degreeDaysType'
    sentiment = 'sentiment'
    investmentIncome = 'investmentIncome'
    groupType = 'groupType'
    forwardPointImm = 'forwardPointImm'
    twap = 'twap'
    clientShortName = 'clientShortName'
    groupCategory = 'groupCategory'
    bidPlusAsk = 'bidPlusAsk'
    foreignCcyRate = 'foreignCcyRate'
    electionOdds = 'electionOdds'
    windDirectionForecast = 'windDirectionForecast'
    commoditiesRelated = 'commoditiesRelated'
    requireAnonClientName = 'requireAnonClientName'
    pricingLocation = 'pricingLocation'
    beta = 'beta'
    lastReturnsEndDate = 'lastReturnsEndDate'
    upfrontPaymentDate = 'upfrontPaymentDate'
    sell1point5bps = 'sell1point5bps'
    longExposure = 'longExposure'
    sell4point5bps = 'sell4point5bps'
    tcmCostParticipationRate20Pct = 'tcmCostParticipationRate20Pct'
    venueType = 'venueType'
    currentActivityIndicator = 'currentActivityIndicator'
    multiAssetClassSwap = 'multiAssetClassSwap'
    tradedPrice = 'tradedPrice'
    medianDailyVolume5d = 'medianDailyVolume5d'
    deltaChangeId = 'deltaChangeId'
    implementationId = 'implementationId'
    leg1FixedPayment = 'leg1FixedPayment'
    esNumericScore = 'esNumericScore'
    inBenchmark = 'inBenchmark'
    actionSDR = 'actionSDR'
    nearbyContractRule = 'nearbyContractRule'
    quantityFrequency = 'quantityFrequency'
    countIdeasQtd = 'countIdeasQtd'
    knockOutPrice = 'knockOutPrice'
    spreadCurrency1 = 'spreadCurrency1'
    spreadCurrency2 = 'spreadCurrency2'
    currentSupply = 'currentSupply'
    ctdAssetId = 'ctdAssetId'
    buy10bps = 'buy10bps'
    precipitation = 'precipitation'
    impliedRetailSellShares = 'impliedRetailSellShares'
    valueType = 'valueType'
    betaAdjustedNetExposure = 'betaAdjustedNetExposure'
    pairCalculation = 'pairCalculation'
    estimatedRodVolume = 'estimatedRodVolume'
    sell14bps = 'sell14bps'
    _10 = '10'
    _11 = '11'
    _12 = '12'
    _13 = '13'
    excessReturnPrice = 'excessReturnPrice'
    _14 = '14'
    _15 = '15'
    _16 = '16'
    _17 = '17'
    _18 = '18'
    _19 = '19'
    fxPnl = 'fxPnl'
    fixingDate = 'fixingDate'
    leg2FloatingRateIndex = 'leg2FloatingRateIndex'
    assetClassificationsGicsIndustryGroup = 'assetClassificationsGicsIndustryGroup'
    meanDailyVolume10d = 'meanDailyVolume10d'
    indexConstituents = 'indexConstituents'
    lendingSecId = 'lendingSecId'
    dollarDuration = 'dollarDuration'
    equityTheta = 'equityTheta'
    dv01 = 'dv01'
    startDate = 'startDate'
    _20 = '20'
    _21 = '21'
    fwdTier = 'fwdTier'
    _22 = '22'
    _23 = '23'
    mixedSwap = 'mixedSwap'
    swaptionPremium = 'swaptionPremium'
    _24 = '24'
    _25 = '25'
    _26 = '26'
    snowfall = 'snowfall'
    liquidityBucketBuy = 'liquidityBucketBuy'
    dayOpen = 'dayOpen'
    _27 = '27'
    mic = 'mic'
    hurdleType = 'hurdleType'
    _28 = '28'
    latitude = 'latitude'
    _29 = '29'
    mid = 'mid'
    impliedRepo = 'impliedRepo'
    long = 'long'
    firstExecutionTime = 'firstExecutionTime'
    shares = 'shares'
    coveredBond = 'coveredBond'
    regionCode = 'regionCode'
    buy20cents = 'buy20cents'
    longWeight = 'longWeight'
    calculationTime = 'calculationTime'
    liquidityBucketSell = 'liquidityBucketSell'
    daysOpenUnrealizedCash = 'daysOpenUnrealizedCash'
    temperature = 'temperature'
    averageRealizedVariance = 'averageRealizedVariance'
    leg1CommodityUnderlyerId = 'leg1CommodityUnderlyerId'
    ratingFitch = 'ratingFitch'
    financialReturnsScore = 'financialReturnsScore'
    yearOrQuarter = 'yearOrQuarter'
    _30 = '30'
    _31 = '31'
    _32 = '32'
    nonSymbolDimensions = 'nonSymbolDimensions'
    _33 = '33'
    commoditiesForecast = 'commoditiesForecast'
    _34 = '34'
    _35 = '35'
    covid19ByState = 'covid19ByState'
    _36 = '36'
    _37 = '37'
    _38 = '38'
    _39 = '39'
    percentageExpectedResidual = 'percentageExpectedResidual'
    hospitalName = 'hospitalName'
    buy90cents = 'buy90cents'
    periodType = 'periodType'
    assetClassificationsCountryName = 'assetClassificationsCountryName'
    totalHospitalized = 'totalHospitalized'
    peggedRefillInterval = 'peggedRefillInterval'
    fatalitiesProbable = 'fatalitiesProbable'
    tenorCurveBucket = 'tenorCurveBucket'
    _40 = '40'
    administrativeRegion = 'administrativeRegion'
    _41 = '41'
    open = 'open'
    _42 = '42'
    _43 = '43'
    _44 = '44'
    _45 = '45'
    cusip = 'cusip'
    totalConfirmedByState = 'totalConfirmedByState'
    _46 = '46'
    ideaActivityTime = 'ideaActivityTime'
    _47 = '47'
    _48 = '48'
    _49 = '49'
    tagsToExclude = 'tagsToExclude'
    windAttribute = 'windAttribute'
    spreadOptionAtmFwdRate = 'spreadOptionAtmFwdRate'
    netExposure = 'netExposure'
    optionEntitlement = 'optionEntitlement'
    isLegacyPairBasket = 'isLegacyPairBasket'
    issuerType = 'issuerType'
    buy70cents = 'buy70cents'
    strikeReference = 'strikeReference'
    assetCount = 'assetCount'
    matchingOrderFwdPointAsk = 'matchingOrderFwdPointAsk'
    _50 = '50'
    _51 = '51'
    isOrderInLimit = 'isOrderInLimit'
    _52 = '52'
    _53 = '53'
    _54 = '54'
    fundamentalMetric = 'fundamentalMetric'
    _55 = '55'
    _56 = '56'
    quoteStatusId = 'quoteStatusId'
    _57 = '57'
    absoluteValue = 'absoluteValue'
    closingReport = 'closingReport'
    redemptionNoticePeriod = 'redemptionNoticePeriod'
    _58 = '58'
    previousTotalConfirmed = 'previousTotalConfirmed'
    _59 = '59'
    longTenor = 'longTenor'
    multiplier = 'multiplier'
    buy40cents = 'buy40cents'
    assetCountPriced = 'assetCountPriced'
    voteDirection = 'voteDirection'
    impliedRepoRate = 'impliedRepoRate'
    settlementCurrency = 'settlementCurrency'
    wtdDegreeDaysForecast = 'wtdDegreeDaysForecast'
    indicationOfCollateralization = 'indicationOfCollateralization'
    futureMonthN26 = 'futureMonthN26'
    _60 = '60'
    lendingPartnerFee = 'lendingPartnerFee'
    futureMonthN25 = 'futureMonthN25'
    _61 = '61'
    futureMonthN24 = 'futureMonthN24'
    _62 = '62'
    primaryVwapRealizedBps = 'primaryVwapRealizedBps'
    futureMonthN23 = 'futureMonthN23'
    _63 = '63'
    futureMonthN22 = 'futureMonthN22'
    _64 = '64'
    futureMonthN21 = 'futureMonthN21'
    _65 = '65'
    _66 = '66'
    _67 = '67'
    _68 = '68'
    _69 = '69'
    breakEvenInflation = 'breakEvenInflation'
    pnlYtd = 'pnlYtd'
    leg1ReturnType = 'leg1ReturnType'
    tenor2 = 'tenor2'
    resetFrequency = 'resetFrequency'
    assetParametersPayerFrequency = 'assetParametersPayerFrequency'
    degreeDaysForecast = 'degreeDaysForecast'
    isManuallySilenced = 'isManuallySilenced'
    buy3bps = 'buy3bps'
    lastUpdatedById = 'lastUpdatedById'
    legalEntityAcct = 'legalEntityAcct'
    targetShareholderMeetingDate = 'targetShareholderMeetingDate'
    _70 = '70'
    _71 = '71'
    _72 = '72'
    paceOfRollp0 = 'paceOfRollp0'
    _73 = '73'
    _74 = '74'
    controversyPercentile = 'controversyPercentile'
    leg1NotionalCurrency = 'leg1NotionalCurrency'
    _75 = '75'
    complianceEffectiveTime = 'complianceEffectiveTime'
    expirationDate = 'expirationDate'
    _76 = '76'
    _77 = '77'
    _78 = '78'
    _79 = '79'
    floatingRateDayCountFraction = 'floatingRateDayCountFraction'
    callLastDate = 'callLastDate'
    factorReturn = 'factorReturn'
    passiveFlowRatio = 'passiveFlowRatio'
    composite5DayAdv = 'composite5DayAdv'
    marginalContributionToRisk = 'marginalContributionToRisk'
    closeDate = 'closeDate'
    temperatureHourForecast = 'temperatureHourForecast'
    newIdeasWtd = 'newIdeasWtd'
    assetClassSDR = 'assetClassSDR'
    yieldToWorst = 'yieldToWorst'
    assetParametersForwardRate = 'assetParametersForwardRate'
    _80 = '80'
    closingPrice = 'closingPrice'
    clientFwdPointsAsk = 'clientFwdPointsAsk'
    _81 = '81'
    turnoverCompositeAdjusted = 'turnoverCompositeAdjusted'
    comment = 'comment'
    sourceSymbol = 'sourceSymbol'
    _82 = '82'
    _83 = '83'
    _84 = '84'
    askUnadjusted = 'askUnadjusted'
    appliedSpeedBump = 'appliedSpeedBump'
    _85 = '85'
    _86 = '86'
    restrictExternalDerivedData = 'restrictExternalDerivedData'
    _87 = '87'
    _88 = '88'
    _89 = '89'
    askChange = 'askChange'
    countIdeasMtd = 'countIdeasMtd'
    endDate = 'endDate'
    sunshine = 'sunshine'
    contractType = 'contractType'
    momentumType = 'momentumType'
    specificRisk = 'specificRisk'
    chargeInQuoteConventionTwo = 'chargeInQuoteConventionTwo'
    assetParametersIndex = 'assetParametersIndex'
    freeFloatMarketCap = 'freeFloatMarketCap'
    mdapi = 'mdapi'
    payoffQtd = 'payoffQtd'
    loss = 'loss'
    midcurveVol = 'midcurveVol'
    sell6bps = 'sell6bps'
    tradingCostPnl = 'tradingCostPnl'
    priceNotationType = 'priceNotationType'
    price = 'price'
    paymentQuantity = 'paymentQuantity'
    _90 = '90'
    defensive = 'defensive'
    _91 = '91'
    _92 = '92'
    _93 = '93'
    assetParametersCallAmount = 'assetParametersCallAmount'
    _94 = '94'
    _95 = '95'
    outrightMarketAsk = 'outrightMarketAsk'
    _96 = '96'
    _97 = '97'
    _98 = '98'
    redemptionDate = 'redemptionDate'
    _99 = '99'
    leg2NotionalCurrency = 'leg2NotionalCurrency'
    subRegion = 'subRegion'
    productId = 'productId'
    benchmark = 'benchmark'
    nvtAdj = 'nvtAdj'
    tcmCostParticipationRate15Pct = 'tcmCostParticipationRate15Pct'
    fiscalYear = 'fiscalYear'
    recallDate = 'recallDate'
    internal = 'internal'
    gender = 'gender'
    assetClassificationsGicsIndustry = 'assetClassificationsGicsIndustry'
    adjustedBidPrice = 'adjustedBidPrice'
    lowUnadjusted = 'lowUnadjusted'
    MACSSecondaryAssetClass = 'MACSSecondaryAssetClass'
    confirmedPerMillion = 'confirmedPerMillion'
    aggregatedUsdSpotExposure = 'aggregatedUsdSpotExposure'
    exchangeRateBasis = 'exchangeRateBasis'
    dataSourceId = 'dataSourceId'
    integratedScore = 'integratedScore'
    buy7bps = 'buy7bps'
    arrivalMidUnrealizedCash = 'arrivalMidUnrealizedCash'
    knockInPrice = 'knockInPrice'
    event = 'event'
    isIntradayAuction = 'isIntradayAuction'
    locationName = 'locationName'
    coupon = 'coupon'
    percentageAuctionExecutedQuantity = 'percentageAuctionExecutedQuantity'
    avgYield7Day = 'avgYield7Day'
    referenceRateEur = 'referenceRateEur'
    originalDisseminationId = 'originalDisseminationId'
    totalOnVent = 'totalOnVent'
    twapUnrealizedCash = 'twapUnrealizedCash'
    stsCreditMarket = 'stsCreditMarket'
    weightOfMarketValue = 'weightOfMarketValue'
    onsCode = 'onsCode'
    passiveTouchFillsPercentage = 'passiveTouchFillsPercentage'
    seniority = 'seniority'
    inflationDelta = 'inflationDelta'
    leg1Index = 'leg1Index'
    highUnadjusted = 'highUnadjusted'
    relativeMarginalContributionToRisk = 'relativeMarginalContributionToRisk'
    submissionEvent = 'submissionEvent'
    TVProductMnemonic = 'TVProductMnemonic'
    avgTradeRateLabel = 'avgTradeRateLabel'
    lastActivityDate = 'lastActivityDate'
    disseminationTime = 'disseminationTime'
    priceToCash = 'priceToCash'
    buy10cents = 'buy10cents'
    fwdEbookPointSpreadAllInMultAsk = 'fwdEbookPointSpreadAllInMultAsk'
    realizedMarketCapRatio = 'realizedMarketCapRatio'
    failed = 'failed'
    navSpread = 'navSpread'
    venueMIC = 'venueMIC'
    dollarTotalReturn = 'dollarTotalReturn'
    blockUnit = 'blockUnit'
    midSpread = 'midSpread'
    istatProvinceCode = 'istatProvinceCode'
    totalRecoveredByState = 'totalRecoveredByState'
    displayId = 'displayId'
    repurchaseRate = 'repurchaseRate'
    dataSource = 'dataSource'
    totalBeingTested = 'totalBeingTested'
    clearedOrBilateral = 'clearedOrBilateral'
    cvaMultiplier = 'cvaMultiplier'
    metricName = 'metricName'
    askGspread = 'askGspread'
    forecastHour = 'forecastHour'
    leg2PaymentType = 'leg2PaymentType'
    calSpreadMisPricing = 'calSpreadMisPricing'
    totalTestedNegative = 'totalTestedNegative'
    impliedRetailNotional = 'impliedRetailNotional'
    rate366 = 'rate366'
    platform = 'platform'
    rate365 = 'rate365'
    fixedRateFrequency = 'fixedRateFrequency'
    rate360 = 'rate360'
    medianDailyVolume22d = 'medianDailyVolume22d'
    notionalQuantity2 = 'notionalQuantity2'
    notionalQuantity1 = 'notionalQuantity1'
    isContinuous = 'isContinuous'
    value = 'value'
    payerDesignatedMaturity = 'payerDesignatedMaturity'
    productType = 'productType'
    mdv22Day = 'mdv22Day'
    nvtAdjFf90 = 'nvtAdjFf90'
    twapRealizedBps = 'twapRealizedBps'
    testMeasureLabel = 'testMeasureLabel'
    quantity = 'quantity'
    reportId = 'reportId'
    indexWeight = 'indexWeight'
    MACSPrimaryAssetClass = 'MACSPrimaryAssetClass'
    traded = 'traded'
    trader = 'trader'
    leg2PriceType = 'leg2PriceType'
    floatingRateResetFrequencyPeriodMultiplier2 = 'floatingRateResetFrequencyPeriodMultiplier2'
    totalActive = 'totalActive'
    floatingRateResetFrequencyPeriodMultiplier1 = 'floatingRateResetFrequencyPeriodMultiplier1'
    gsid2 = 'gsid2'
    matchedMaturityOISSwapSpread = 'matchedMaturityOISSwapSpread'
    valuationDate = 'valuationDate'
    restrictGsFederation = 'restrictGsFederation'
    positionSource = 'positionSource'
    tcmCostHorizon6Hour = 'tcmCostHorizon6Hour'
    commodityReferencePrice = 'commodityReferencePrice'
    buy200cents = 'buy200cents'
    vwapUnrealizedBps = 'vwapUnrealizedBps'
    priceToBook = 'priceToBook'
    isin = 'isin'
    fwdEbookRiskSpreadMultBid = 'fwdEbookRiskSpreadMultBid'
    assetParametersStrikeType = 'assetParametersStrikeType'
    plId = 'plId'
    lastReturnsStartDate = 'lastReturnsStartDate'
    collateralValueVariance = 'collateralValueVariance'
    year = 'year'
    forecastPeriod = 'forecastPeriod'
    callFirstDate = 'callFirstDate'
    dataSetIds = 'dataSetIds'
    economicTermsHash = 'economicTermsHash'
    numBeds = 'numBeds'
    sell20bps = 'sell20bps'
    clientType = 'clientType'
    percentageCloseExecutedQuantity = 'percentageCloseExecutedQuantity'
    averageFillPriceExcludingFees = 'averageFillPriceExcludingFees'
    macaulayDuration = 'macaulayDuration'
    availableInventory = 'availableInventory'
    est1DayCompletePct = 'est1DayCompletePct'
    relativeHitRateYtd = 'relativeHitRateYtd'
    gSpread = 'gSpread'
    rai = 'rai'
    impliedRetailBuyPctNotional = 'impliedRetailBuyPctNotional'
    createdById = 'createdById'
    marketDataType = 'marketDataType'
    realShortRatesContribution = 'realShortRatesContribution'
    metricCategory = 'metricCategory'
    assetParametersCapFloor = 'assetParametersCapFloor'
    annualizedCarry = 'annualizedCarry'
    valuePrevious = 'valuePrevious'
    transmissionClassification = 'transmissionClassification'
    avgTradeRate = 'avgTradeRate'
    shortLevel = 'shortLevel'
    version = 'version'
    categoryType = 'categoryType'
    policyRateExpectation = 'policyRateExpectation'
    uploadDate = 'uploadDate'
    blockOffFacility = 'blockOffFacility'
    unrealizedVwapPerformanceUSD = 'unrealizedVwapPerformanceUSD'
    paceOfRollp75 = 'paceOfRollp75'
    earningsPerSharePositive = 'earningsPerSharePositive'
    numIcuBeds = 'numIcuBeds'
    bucketVolumeInPercentage = 'bucketVolumeInPercentage'
    estimatedTradingCost = 'estimatedTradingCost'
    eid = 'eid'
    calculationRegion = 'calculationRegion'
    relativeReturnQtd = 'relativeReturnQtd'
    assessedTestMeasure = 'assessedTestMeasure'
    mktQuotingStyle = 'mktQuotingStyle'
    expirationTenor = 'expirationTenor'
    tradedPriceNoMarkup = 'tradedPriceNoMarkup'
    priceLimit = 'priceLimit'
    marketModelId = 'marketModelId'
    receiverFrequency = 'receiverFrequency'
    realizedCorrelation = 'realizedCorrelation'
    issueStatus = 'issueStatus'
    collateralValueActual = 'collateralValueActual'
    atmFwdRate = 'atmFwdRate'
    tcmCostParticipationRate75Pct = 'tcmCostParticipationRate75Pct'
    close = 'close'
    vol30d = 'vol30d'
    esProductImpactScore = 'esProductImpactScore'
    equityVega = 'equityVega'
    executedFillQuantity = 'executedFillQuantity'
    lenderPayment = 'lenderPayment'
    fiveDayMove = 'fiveDayMove'
    realizedMarketCap = 'realizedMarketCap'
    valueFormat = 'valueFormat'
    windChillForecast = 'windChillForecast'
    assetParametersTenor = 'assetParametersTenor'
    targetNotional = 'targetNotional'
    fillLegId = 'fillLegId'
    rationale = 'rationale'
    realizedTwapPerformanceBps = 'realizedTwapPerformanceBps'
    lastUpdatedSince = 'lastUpdatedSince'
    totalTests = 'totalTests'
    equitiesContribution = 'equitiesContribution'
    fwdEbookPointSpreadMultAsk = 'fwdEbookPointSpreadMultAsk'
    simonId = 'simonId'
    congestion = 'congestion'
    leg2CommodityInstrumentId = 'leg2CommodityInstrumentId'
    notes = 'notes'
    totalProbableSeniorHome = 'totalProbableSeniorHome'
    eventCategory = 'eventCategory'
    averageFillRate = 'averageFillRate'
    cins = 'cins'
    unadjustedOpen = 'unadjustedOpen'
    criticality = 'criticality'
    bidAskSpread = 'bidAskSpread'
    arrivalMidUnrealizedBps = 'arrivalMidUnrealizedBps'
    optionType = 'optionType'
    terminationDate = 'terminationDate'
    queriesPerSecond = 'queriesPerSecond'
    liquidityType = 'liquidityType'
    creditLimit = 'creditLimit'
    rankQtd = 'rankQtd'
    combinedKey = 'combinedKey'
    girFxForecast = 'girFxForecast'
    effectiveTenor = 'effectiveTenor'
    girCommoditiesForecast = 'girCommoditiesForecast'
    relativeHumidityDailyForecast = 'relativeHumidityDailyForecast'
    std30DaysSubsidizedYield = 'std30DaysSubsidizedYield'
    annualizedTrackingError = 'annualizedTrackingError'
    futureMonthF26 = 'futureMonthF26'
    futureMonthF25 = 'futureMonthF25'
    volSwap = 'volSwap'
    futureMonthF24 = 'futureMonthF24'
    heatIndexDailyForecast = 'heatIndexDailyForecast'
    futureMonthF23 = 'futureMonthF23'
    realFCI = 'realFCI'
    blockTradesAndLargeNotionalOffFacilitySwaps = 'blockTradesAndLargeNotionalOffFacilitySwaps'
    futureMonthF22 = 'futureMonthF22'
    buy1point5bps = 'buy1point5bps'
    futureMonthF21 = 'futureMonthF21'
    expirationSettlementDate = 'expirationSettlementDate'
    absoluteReturnQtd = 'absoluteReturnQtd'
    grossExposure = 'grossExposure'
    volume = 'volume'
    adv = 'adv'
    shortConvictionMedium = 'shortConvictionMedium'
    completeTestMeasure = 'completeTestMeasure'
    percentPricesReturn = 'percentPricesReturn'
    fxQuotedVega = 'fxQuotedVega'
    exchange = 'exchange'
    esPolicyScore = 'esPolicyScore'
    rollVolumeStd = 'rollVolumeStd'
    temperatureDailyForecast = 'temperatureDailyForecast'
    relativePayoffQtd = 'relativePayoffQtd'
    onLoanPercentage = 'onLoanPercentage'
    fxCalcDeltaNoPremiumAdjustment = 'fxCalcDeltaNoPremiumAdjustment'
    twapRemainingSlices = 'twapRemainingSlices'
    fairVariance = 'fairVariance'
    hitRateWtd = 'hitRateWtd'
    previousCloseRealizedCash = 'previousCloseRealizedCash'
    realizedVolatility = 'realizedVolatility'
    unexecutedQuantity = 'unexecutedQuantity'
    clientOutrightBid = 'clientOutrightBid'
    proceedsAssetSwapSpread1m = 'proceedsAssetSwapSpread1m'
    cloneParentId = 'cloneParentId'
    windSpeedHourlyForecast = 'windSpeedHourlyForecast'
    impliedRetailSellNotional = 'impliedRetailSellNotional'
    etfFlowRatio = 'etfFlowRatio'
    assetParametersReceiverRateOption = 'assetParametersReceiverRateOption'
    buy60cents = 'buy60cents'
    securitySubTypeId = 'securitySubTypeId'
    TRSNotional = 'TRSNotional'
    denominated = 'denominated'
    message = 'message'
    stsRatesCountry = 'stsRatesCountry'
    sell65cents = 'sell65cents'
    assetParametersPremiumPaymentDate = 'assetParametersPremiumPaymentDate'
    horizon = 'horizon'
    wouldIfGoodLevel = 'wouldIfGoodLevel'
    bufferThresholdRequired = 'bufferThresholdRequired'
    faceValue = 'faceValue'
    rollVolumeHist = 'rollVolumeHist'
    counterPartyStatus = 'counterPartyStatus'
    composite22DayAdv = 'composite22DayAdv'
    percentageFarExecutedQuantity = 'percentageFarExecutedQuantity'
    tradingCentre = 'tradingCentre'
    loanSpreadRequired = 'loanSpreadRequired'
    fixingRequested = 'fixingRequested'
    assetClass = 'assetClass'
    sovereignSpreadContribution = 'sovereignSpreadContribution'
    ric = 'ric'
    bucketEndTime = 'bucketEndTime'
    rateType = 'rateType'
    totalFatalitiesSeniorHome = 'totalFatalitiesSeniorHome'
    loanStatus = 'loanStatus'
    shortWeight = 'shortWeight'
    geographyId = 'geographyId'
    sell7point5bps = 'sell7point5bps'
    nav = 'nav'
    fiscalQuarter = 'fiscalQuarter'
    versionString = 'versionString'
    payoffYtd = 'payoffYtd'
    marketImpact = 'marketImpact'
    eventType = 'eventType'
    fillPrice = 'fillPrice'
    assetCountLong = 'assetCountLong'
    sell180cents = 'sell180cents'
    expirationDateRule = 'expirationDateRule'
    spot = 'spot'
    applicationId = 'applicationId'
    indicativeClosePrice = 'indicativeClosePrice'
    swapSpread = 'swapSpread'
    tradingRestriction = 'tradingRestriction'
    assetParametersPayOrReceive = 'assetParametersPayOrReceive'
    priceSpotEntryUnit = 'priceSpotEntryUnit'
    unrealizedArrivalPerformanceBps = 'unrealizedArrivalPerformanceBps'
    city = 'city'
    assetParametersIndexSeries = 'assetParametersIndexSeries'
    pnlWtd = 'pnlWtd'
    covariance = 'covariance'
    bucketVolumeInShares = 'bucketVolumeInShares'
    commodityForecast = 'commodityForecast'
    valid = 'valid'
    stsCommodity = 'stsCommodity'
    initialPricingDate = 'initialPricingDate'
    indicationOfEndUserException = 'indicationOfEndUserException'
    windDirectionHourlyForecast = 'windDirectionHourlyForecast'
    esScore = 'esScore'
    _yield = 'yield'
    numberOfPositionsExploded = 'numberOfPositionsExploded'
    fatalitiesUnderlyingConditionsPresent = 'fatalitiesUnderlyingConditionsPresent'
    priceRangeInTicks = 'priceRangeInTicks'
    swapPointsMarketAsk = 'swapPointsMarketAsk'
    paceOfRollp25 = 'paceOfRollp25'
    dayCloseRealizedUSD = 'dayCloseRealizedUSD'
    pctChange = 'pctChange'
    brightnessType = 'brightnessType'
    futureMonth3M = 'futureMonth3M'
    fwdEbookRiskSpreadMultAsk = 'fwdEbookRiskSpreadMultAsk'
    numberOfRolls = 'numberOfRolls'
    isoCountryCodeNumeric = 'isoCountryCodeNumeric'
    priceType = 'priceType'
    realizedVwapPerformanceUSD = 'realizedVwapPerformanceUSD'
    orderSide = 'orderSide'
    tradingDesk = 'tradingDesk'
    fuelType = 'fuelType'
    bbid = 'bbid'
    vegaNotionalAmount = 'vegaNotionalAmount'
    fatalitiesUnderlyingConditionsAbsent = 'fatalitiesUnderlyingConditionsAbsent'
    effectiveDate = 'effectiveDate'
    TRSBidPrice = 'TRSBidPrice'
    capped = 'capped'
    rating = 'rating'
    optionCurrency = 'optionCurrency'
    isCloseAuction = 'isCloseAuction'
    volatility = 'volatility'
    avgVentUtil = 'avgVentUtil'
    underlyingAssetIds = 'underlyingAssetIds'
    buy6point5bps = 'buy6point5bps'
    vwapInLimitRealizedCash = 'vwapInLimitRealizedCash'
    estimatedClosingAuctionVolume = 'estimatedClosingAuctionVolume'
    sell2bps = 'sell2bps'
    annualRisk = 'annualRisk'
    eti = 'eti'
    vwapInLimitRealizedBps = 'vwapInLimitRealizedBps'
    rankMtd = 'rankMtd'
    marketBuffer = 'marketBuffer'
    futureMonthJ24 = 'futureMonthJ24'
    lastUploadedTime = 'lastUploadedTime'
    futureMonthJ23 = 'futureMonthJ23'
    oeId = 'oeId'
    futureMonthJ22 = 'futureMonthJ22'
    futureMonthJ21 = 'futureMonthJ21'
    bbidEquivalent = 'bbidEquivalent'
    initBufferThresholdRequired = 'initBufferThresholdRequired'
    leg2DesignatedMaturity = 'leg2DesignatedMaturity'
    matchedMaturityOISSwapRate = 'matchedMaturityOISSwapRate'
    fairPrice = 'fairPrice'
    participationRateInLimit = 'participationRateInLimit'
    extMktClass = 'extMktClass'
    priceCurrency = 'priceCurrency'
    failedCount = 'failedCount'
    leg1IndexLocation = 'leg1IndexLocation'
    supraStrategy = 'supraStrategy'
    dayCountConvention = 'dayCountConvention'
    roundedNotionalAmount1 = 'roundedNotionalAmount1'
    roundedNotionalAmount2 = 'roundedNotionalAmount2'
    factorSource = 'factorSource'
    futureMonthJ26 = 'futureMonthJ26'
    lendingSecType = 'lendingSecType'
    futureMonthJ25 = 'futureMonthJ25'
    leverage = 'leverage'
    factorExposure = 'factorExposure'
    forecastDay = 'forecastDay'
    optionFamily = 'optionFamily'
    generatorOutput = 'generatorOutput'
    priceSpotStopLossValue = 'priceSpotStopLossValue'
    kpiId = 'kpiId'
    windGeneration = 'windGeneration'
    percentageMidExecutedQuantity = 'percentageMidExecutedQuantity'
    staticVolumeForecast = 'staticVolumeForecast'
    borrowCost = 'borrowCost'
    knockOutDirection = 'knockOutDirection'
    screenId = 'screenId'
    riskModel = 'riskModel'
    assetParametersVendor = 'assetParametersVendor'
    assetParametersIndex1Tenor = 'assetParametersIndex1Tenor'
    isPublic = 'isPublic'
    fairValue = 'fairValue'
    openTime = 'openTime'
    pressureHourlyForecast = 'pressureHourlyForecast'
    localCcyRate = 'localCcyRate'
    endUserException = 'endUserException'
    sell90cents = 'sell90cents'
    executionVenue = 'executionVenue'
    nonStandardizedPricingIndicator = 'nonStandardizedPricingIndicator'
    primaryVwapInLimitRealizedBps = 'primaryVwapInLimitRealizedBps'
    approveRebalance = 'approveRebalance'
    adjustedClosePrice = 'adjustedClosePrice'
    lmsId = 'lmsId'
    rebateRate = 'rebateRate'
    sell130cents = 'sell130cents'
    speedBumpDelay = 'speedBumpDelay'
    priceUnitOfMeasure1 = 'priceUnitOfMeasure1'
    sell32bps = 'sell32bps'
    paceOfRollp50 = 'paceOfRollp50'
    priceMoveVsArrival = 'priceMoveVsArrival'
    strikeRelative = 'strikeRelative'
    pressureType = 'pressureType'
    buy40bps = 'buy40bps'
    priceNotation = 'priceNotation'
    strategy = 'strategy'
    priceUnitOfMeasure2 = 'priceUnitOfMeasure2'
    issueStatusDate = 'issueStatusDate'
    lenderIncome = 'lenderIncome'
    settlementCcy = 'settlementCcy'
    pbClientId = 'pbClientId'
    istatRegionCode = 'istatRegionCode'
    sell9bps = 'sell9bps'
    ownerId = 'ownerId'
    composite10DayAdv = 'composite10DayAdv'
    maxLoanBalance = 'maxLoanBalance'
    ideaActivityType = 'ideaActivityType'
    sell60cents = 'sell60cents'
    ideaSource = 'ideaSource'
    everOnVent = 'everOnVent'
    otcVolume = 'otcVolume'
    buy15cents = 'buy15cents'
    unadjustedAsk = 'unadjustedAsk'
    dynamicVolumeForecast = 'dynamicVolumeForecast'
    margin = 'margin'
    contributionName = 'contributionName'
    givenPlusPaid = 'givenPlusPaid'
    lastFillPrice = 'lastFillPrice'
    soprOut = 'soprOut'
    clientSpotAsk = 'clientSpotAsk'
    shortConvictionSmall = 'shortConvictionSmall'
    upfrontPaymentCurrency = 'upfrontPaymentCurrency'
    spotSettlementDate = 'spotSettlementDate'
    matrixOrder = 'matrixOrder'
    dayClose = 'dayClose'
    dateIndex = 'dateIndex'
    payerDayCountFraction = 'payerDayCountFraction'
    assetClassificationsIsPrimary = 'assetClassificationsIsPrimary'
    breakEvenInflationChange = 'breakEvenInflationChange'
    buy130cents = 'buy130cents'
    dwiContribution = 'dwiContribution'
    asset2Id = 'asset2Id'
    economicForecasts = 'economicForecasts'
    averageFillPrice = 'averageFillPrice'
    depthSpreadScore = 'depthSpreadScore'
    sell10cents = 'sell10cents'
    secType = 'secType'
    subAccount = 'subAccount'
    buy65cents = 'buy65cents'
    bondCdsBasis = 'bondCdsBasis'
    vendor = 'vendor'
    passMessage = 'passMessage'
    dataSet = 'dataSet'
    totalNotionalQuantity2 = 'totalNotionalQuantity2'
    totalNotionalQuantity1 = 'totalNotionalQuantity1'
    notionalAmount2 = 'notionalAmount2'
    notionalAmount1 = 'notionalAmount1'
    queueingTime = 'queueingTime'
    annReturn5Year = 'annReturn5Year'
    volumeStartOfDay = 'volumeStartOfDay'
    priceNotation3Type = 'priceNotation3Type'
    assetParametersFloatingRateDesignatedMaturity = 'assetParametersFloatingRateDesignatedMaturity'
    impliedRetailBuyPctShares = 'impliedRetailBuyPctShares'
    executedNotionalLocal = 'executedNotionalLocal'
    tsdbShortname = 'tsdbShortname'
    businessSponsor = 'businessSponsor'
    unexplained = 'unexplained'
    seasonalAdjustmentShort = 'seasonalAdjustmentShort'
    metric = 'metric'
    ask = 'ask'
    closePrice = 'closePrice'
    endTime = 'endTime'
    sell100cents = 'sell100cents'
    executionTimestamp = 'executionTimestamp'
    buy180cents = 'buy180cents'
    absoluteStrike = 'absoluteStrike'
    liquidity = 'liquidity'
    sell3point5bps = 'sell3point5bps'
    liquidityScoreBuy = 'liquidityScoreBuy'
    paymentFrequency = 'paymentFrequency'
    expenseRatioNetBps = 'expenseRatioNetBps'
    metricType = 'metricType'
    rankYtd = 'rankYtd'
    leg1Spread = 'leg1Spread'
    coverageRegion = 'coverageRegion'
    absoluteReturnYtd = 'absoluteReturnYtd'
    dayCountConvention2 = 'dayCountConvention2'
    degreeDays = 'degreeDays'
    fwdPointsAsk = 'fwdPointsAsk'
    turnoverAdjusted = 'turnoverAdjusted'
    priceSpotTargetValue = 'priceSpotTargetValue'
    marketDataPoint = 'marketDataPoint'
    numOfFunds = 'numOfFunds'
    ebcsOutrightMid = 'ebcsOutrightMid'
    tradeTime = 'tradeTime'
    executionId = 'executionId'
    turnoverUnadjusted = 'turnoverUnadjusted'
    leg1FloatingIndex = 'leg1FloatingIndex'
    hedgeAnnualizedVolatility = 'hedgeAnnualizedVolatility'
    benchmarkCurrency = 'benchmarkCurrency'
    futuresContract = 'futuresContract'
    name = 'name'
    aum = 'aum'
    leg1DayCountConvention = 'leg1DayCountConvention'
    cbsCode = 'cbsCode'
    folderName = 'folderName'
    apiUsage = 'apiUsage'
    twapInterval = 'twapInterval'
    factorPnl = 'factorPnl'
    paymentFrequencyPeriod1 = 'paymentFrequencyPeriod1'
    uniqueId = 'uniqueId'
    optionExpirationDate = 'optionExpirationDate'
    paymentFrequencyPeriod2 = 'paymentFrequencyPeriod2'
    swaptionAtmFwdRate = 'swaptionAtmFwdRate'
    liveDate = 'liveDate'
    volumeForecastAdjustment = 'volumeForecastAdjustment'
    corporateActionType = 'corporateActionType'
    primeId = 'primeId'
    description = 'description'
    assetClassificationsIsCountryPrimary = 'assetClassificationsIsCountryPrimary'
    rebateRateLimit = 'rebateRateLimit'
    spotAsk = 'spotAsk'
    swapPointsMarketBid = 'swapPointsMarketBid'
    extId = 'extId'
    factor = 'factor'
    daysOnLoan = 'daysOnLoan'
    longConvictionSmall = 'longConvictionSmall'
    sell40cents = 'sell40cents'
    relativePayoffYtd = 'relativePayoffYtd'
    gsfeer = 'gsfeer'
    relativeHitRateQtd = 'relativeHitRateQtd'
    wam = 'wam'
    wal = 'wal'
    backtestId = 'backtestId'
    dirtyPrice = 'dirtyPrice'
    darkWouldRefPrice = 'darkWouldRefPrice'
    corporateSpreadContribution = 'corporateSpreadContribution'
    relativeHumidityHourlyForecast = 'relativeHumidityHourlyForecast'
    multipleScore = 'multipleScore'
    betaAdjustedExposure = 'betaAdjustedExposure'
    momentum = 'momentum'
    isAnnualized = 'isAnnualized'
    dividendPoints = 'dividendPoints'
    brightness = 'brightness'
    assetParametersReceiverDesignatedMaturity = 'assetParametersReceiverDesignatedMaturity'
    bosInTicksDescription = 'bosInTicksDescription'
    testId = 'testId'
    risk = 'risk'
    impliedCorrelation = 'impliedCorrelation'
    normalizedPerformance = 'normalizedPerformance'
    overnightNewsEndTime = 'overnightNewsEndTime'
    bytesConsumed = 'bytesConsumed'
    swaptionVol = 'swaptionVol'
    estimatedClosingVolume = 'estimatedClosingVolume'
    issuer = 'issuer'
    dividendYield = 'dividendYield'
    marketType = 'marketType'
    numUnitsLower = 'numUnitsLower'
    sourceOrigin = 'sourceOrigin'
    proceedsAssetSwapSpread3m = 'proceedsAssetSwapSpread3m'
    totalQuantity = 'totalQuantity'
    internalUser = 'internalUser'
    sell40bps = 'sell40bps'
    redemptionOption = 'redemptionOption'
    notionalUnit2 = 'notionalUnit2'
    notionalUnit1 = 'notionalUnit1'
    sedol = 'sedol'
    roundingCostPnl = 'roundingCostPnl'
    midYield = 'midYield'
    unexecutedNotionalLocal = 'unexecutedNotionalLocal'
    sustainGlobal = 'sustainGlobal'
    endingDate = 'endingDate'
    proceedsAssetSwapSpread12m = 'proceedsAssetSwapSpread12m'
    rvtAdj90 = 'rvtAdj90'
    grossInvestmentWtd = 'grossInvestmentWtd'
    annReturn3Year = 'annReturn3Year'
    sharpeWtd = 'sharpeWtd'
    discountFactor = 'discountFactor'
    swapPointsBid = 'swapPointsBid'
    relativeReturnMtd = 'relativeReturnMtd'
    exchangeCalendar = 'exchangeCalendar'
    priceChangeOnDay = 'priceChangeOnDay'
    buy100cents = 'buy100cents'
    forwardPoint = 'forwardPoint'
    increment = 'increment'
    fci = 'fci'
    enabled = 'enabled'
    recallQuantity = 'recallQuantity'
    strikePriceCurrency = 'strikePriceCurrency'
    fxPositioning = 'fxPositioning'
    gsidEquivalent = 'gsidEquivalent'
    categories = 'categories'
    extMktAsset = 'extMktAsset'
    quotingStyle = 'quotingStyle'
    isInPosition = 'isInPosition'
    errorMessage = 'errorMessage'
    compoundedFixedRate = 'compoundedFixedRate'
    midPrice = 'midPrice'
    proceedsAssetSwapSpread6m = 'proceedsAssetSwapSpread6m'
    stsEmDm = 'stsEmDm'
    TimeinYears = 'TimeinYears'
    embeddedOption = 'embeddedOption'
    tcmCostHorizon2Day = 'tcmCostHorizon2Day'
    ageBand = 'ageBand'
    returnsEnabled = 'returnsEnabled'
    runId = 'runId'
    queueInLots = 'queueInLots'
    tenderOfferExpirationDate = 'tenderOfferExpirationDate'
    assetParametersExpirationTime = 'assetParametersExpirationTime'
    midcurveAnnuity = 'midcurveAnnuity'
    lendingFundNavTrend = 'lendingFundNavTrend'
    cloudCoverForecast = 'cloudCoverForecast'
    tcmCostParticipationRate5Pct = 'tcmCostParticipationRate5Pct'
    defaultBackcast = 'defaultBackcast'
    lockup = 'lockup'
    lockupType = 'lockupType'
    newsOnIntensity = 'newsOnIntensity'
    priceFormingContinuationData = 'priceFormingContinuationData'
    adjustedShortInterest = 'adjustedShortInterest'
    newHospitalized = 'newHospitalized'
    assetParametersStrike = 'assetParametersStrike'
    buy35cents = 'buy35cents'
    impliedRetailBuyNotional = 'impliedRetailBuyNotional'
    leg2TotalNotional = 'leg2TotalNotional'
    assetParametersEffectiveDate = 'assetParametersEffectiveDate'
    annReturn10Year = 'annReturn10Year'
    numAdultIcuBeds = 'numAdultIcuBeds'
    daysToExpiration = 'daysToExpiration'
    continuationEvent = 'continuationEvent'
    leg2CommodityUnderlyerId = 'leg2CommodityUnderlyerId'
    fillPriceExcludingFees = 'fillPriceExcludingFees'
    wiId = 'wiId'
    marketCapCategory = 'marketCapCategory'
    historicalVolume = 'historicalVolume'
    buy5cents = 'buy5cents'
    eventStartDate = 'eventStartDate'
    leg1FixedRate = 'leg1FixedRate'
    equityGamma = 'equityGamma'
    rptId = 'rptId'
    grossIncome = 'grossIncome'
    emId = 'emId'
    assetCountInModel = 'assetCountInModel'
    stsCreditRegion = 'stsCreditRegion'
    minTemperature = 'minTemperature'
    bucketStartTime = 'bucketStartTime'
    medianDailyVolume10d = 'medianDailyVolume10d'
    fillType = 'fillType'
    closeTime = 'closeTime'
    failPct = 'failPct'
    isoCountryCodeAlpha2 = 'isoCountryCodeAlpha2'
    isoCountryCodeAlpha3 = 'isoCountryCodeAlpha3'
    assetParametersOptionType = 'assetParametersOptionType'
    amount = 'amount'
    lendingFundAcct = 'lendingFundAcct'
    fwdPricingSource = 'fwdPricingSource'
    rebate = 'rebate'
    electionType = 'electionType'
    relativeHitRateMtd = 'relativeHitRateMtd'
    impliedVolatility = 'impliedVolatility'
    spread = 'spread'
    variance = 'variance'
    wtdDegreeDaysDailyForecast = 'wtdDegreeDaysDailyForecast'
    swaptionAnnuity = 'swaptionAnnuity'
    buy6bps = 'buy6bps'
    g10Currency = 'g10Currency'
    humidityForecast = 'humidityForecast'
    relativePeriod = 'relativePeriod'
    user = 'user'
    fwdEbookPointSpreadMultBid = 'fwdEbookPointSpreadMultBid'
    customer = 'customer'
    leg1ResetFrequency = 'leg1ResetFrequency'
    queueClockTimeLabel = 'queueClockTimeLabel'
    settlementResolved = 'settlementResolved'
    paceOfRollp100 = 'paceOfRollp100'
    assetClassificationsGicsSubIndustry = 'assetClassificationsGicsSubIndustry'
    dewPointHourlyForecast = 'dewPointHourlyForecast'
    locationType = 'locationType'
    facetDivisionalReportingGroupId = 'facetDivisionalReportingGroupId'
    realizedTwapPerformanceUSD = 'realizedTwapPerformanceUSD'
    swapRate = 'swapRate'
    algoExecutionStyle = 'algoExecutionStyle'
    mktFwdPointBid = 'mktFwdPointBid'
    clientContact = 'clientContact'
    minTemperatureHour = 'minTemperatureHour'
    tradingCurrency = 'tradingCurrency'
    totalByOnset = 'totalByOnset'
    agencySwapSpread = 'agencySwapSpread'
    rank = 'rank'
    mixedSwapOtherReportedSDR = 'mixedSwapOtherReportedSDR'
    humidity = 'humidity'
    dataSetCategory = 'dataSetCategory'
    vwapRealizedBps = 'vwapRealizedBps'
    buy9bps = 'buy9bps'
    totalTested = 'totalTested'
    fatalitiesConfirmed = 'fatalitiesConfirmed'
    universeId1 = 'universeId1'
    fwdPointsBid = 'fwdPointsBid'
    assetParametersPayerDayCountFraction = 'assetParametersPayerDayCountFraction'
    universeId2 = 'universeId2'
    bidLow = 'bidLow'
    bucketizePrice = 'bucketizePrice'
    fairVarianceVolatility = 'fairVarianceVolatility'
    cleanPrice = 'cleanPrice'
    covid19 = 'covid19'
    clientExposure = 'clientExposure'
    leg2TotalNotionalUnit = 'leg2TotalNotionalUnit'
    sell45cents = 'sell45cents'
    gsSustainSubSector = 'gsSustainSubSector'
    sinkable = 'sinkable'
    isReal = 'isReal'
    maxTemperatureHour = 'maxTemperatureHour'
    leg2AveragingMethod = 'leg2AveragingMethod'
    pricingDate = 'pricingDate'
    jsn = 'jsn'
    sell160cents = 'sell160cents'
    firstExerciseDate = 'firstExerciseDate'
    spotBid = 'spotBid'
    knockInDirection = 'knockInDirection'
    dayCloseUnrealizedUSD = 'dayCloseUnrealizedUSD'
    tenor = 'tenor'
    pricingConvention = 'pricingConvention'
    dealableAuto = 'dealableAuto'
    popularity = 'popularity'
    floatingRateOption = 'floatingRateOption'
    tradedNeutralSpotMid = 'tradedNeutralSpotMid'
    hedgeValueType = 'hedgeValueType'
    assetParametersClearingHouse = 'assetParametersClearingHouse'
    disclaimer = 'disclaimer'
    payerFrequency = 'payerFrequency'
    assetParametersOptionStyle = 'assetParametersOptionStyle'
    loanFee = 'loanFee'
    deploymentVersion = 'deploymentVersion'
    buy16bps = 'buy16bps'
    tradeDayCount = 'tradeDayCount'
    transactionType = 'transactionType'
    priceToSales = 'priceToSales'
    newIdeasQtd = 'newIdeasQtd'
    subdivisionName = 'subdivisionName'
    adjustedAskPrice = 'adjustedAskPrice'
    fwdPointsMarketAsk = 'fwdPointsMarketAsk'
    factorUniverse = 'factorUniverse'
    arrivalRt = 'arrivalRt'
    internalIndexCalcAgent = 'internalIndexCalcAgent'
    excessMarginValue = 'excessMarginValue'
    transactionCost = 'transactionCost'
    centralBankSwapRate = 'centralBankSwapRate'
    previousNewConfirmed = 'previousNewConfirmed'
    unrealizedVwapPerformanceBps = 'unrealizedVwapPerformanceBps'
    degreeDaysDailyForecast = 'degreeDaysDailyForecast'
    positionAmount = 'positionAmount'
    heatIndexHourlyForecast = 'heatIndexHourlyForecast'
    maRank = 'maRank'
    fxPositioningSource = 'fxPositioningSource'
    vol60d = 'vol60d'
    eventStartDateTime = 'eventStartDateTime'
    impliedVolatilityByDeltaStrike = 'impliedVolatilityByDeltaStrike'
    mqSymbol = 'mqSymbol'
    numTotalUnits = 'numTotalUnits'
    corporateAction = 'corporateAction'
    leg1PriceType = 'leg1PriceType'
    assetParametersPayerRateOption = 'assetParametersPayerRateOption'
    sell20cents = 'sell20cents'
    leg2FixedPaymentCurrency = 'leg2FixedPaymentCurrency'
    gRegionalScore = 'gRegionalScore'
    hardToBorrow = 'hardToBorrow'
    sell5bps = 'sell5bps'
    rollVwap = 'rollVwap'
    wpk = 'wpk'
    bespokeSwap = 'bespokeSwap'
    assetParametersExpirationDate = 'assetParametersExpirationDate'
    countryName = 'countryName'
    carry = 'carry'
    startingDate = 'startingDate'
    loanId = 'loanId'
    onboarded = 'onboarded'
    liquidityScore = 'liquidityScore'
    longRatesContribution = 'longRatesContribution'
    sourceDateSpan = 'sourceDateSpan'
    annYield6Month = 'annYield6Month'
    underlyingDataSetId = 'underlyingDataSetId'
    closeUnadjusted = 'closeUnadjusted'
    valueUnit = 'valueUnit'
    voiceCurveReason = 'voiceCurveReason'
    quantityUnit = 'quantityUnit'
    adjustedLowPrice = 'adjustedLowPrice'
    isMomentum = 'isMomentum'
    longConvictionLarge = 'longConvictionLarge'
    spotTier = 'spotTier'
    oad = 'oad'
    rate = 'rate'
    couponType = 'couponType'
    client = 'client'
    esgDetailedMetric = 'esgDetailedMetric'
    markToRT = 'markToRT'
    convictionList = 'convictionList'
    passiveEtfRatio = 'passiveEtfRatio'
    futureMonthG26 = 'futureMonthG26'
    futureMonthG25 = 'futureMonthG25'
    futureMonthG24 = 'futureMonthG24'
    futureMonthG23 = 'futureMonthG23'
    typeOfReturn = 'typeOfReturn'
    futureMonthG22 = 'futureMonthG22'
    servicingCostLongPnl = 'servicingCostLongPnl'
    excessMarginPercentage = 'excessMarginPercentage'
    futureMonthG21 = 'futureMonthG21'
    totalMild = 'totalMild'
    realizedArrivalPerformanceBps = 'realizedArrivalPerformanceBps'
    precipitationDailyForecastInches = 'precipitationDailyForecastInches'
    exchangeId = 'exchangeId'
    leg2FixedPayment = 'leg2FixedPayment'
    tcmCostHorizon20Day = 'tcmCostHorizon20Day'
    realm = 'realm'
    goneManual = 'goneManual'
    gate = 'gate'
    bid = 'bid'
    hedgeValue = 'hedgeValue'
    isSeasonallyAdjusted = 'isSeasonallyAdjusted'
    orderStartTime = 'orderStartTime'
    isAggressive = 'isAggressive'
    floatingRateDesignatedMaturity = 'floatingRateDesignatedMaturity'
    percentageNearExecutedQuantity = 'percentageNearExecutedQuantity'
    orderId = 'orderId'
    hospitalType = 'hospitalType'
    dayCloseRealizedBps = 'dayCloseRealizedBps'
    precipitationHourlyForecast = 'precipitationHourlyForecast'
    forwardPriceNg = 'forwardPriceNg'
    marketCapUSD = 'marketCapUSD'
    auctionFillsPercentage = 'auctionFillsPercentage'
    highPrice = 'highPrice'
    absoluteShares = 'absoluteShares'
    fixedRateDayCountFraction = 'fixedRateDayCountFraction'
    model = 'model'
    unrealizedTwapPerformanceUSD = 'unrealizedTwapPerformanceUSD'
    id = 'id'
    maturity = 'maturity'
    deltaChange = 'deltaChange'
    index = 'index'
    finalIndexLevel = 'finalIndexLevel'
    unrealizedArrivalPerformanceUSD = 'unrealizedArrivalPerformanceUSD'
    icebergSlippage = 'icebergSlippage'
    sell120cents = 'sell120cents'
    futureMonthX26 = 'futureMonthX26'
    assetTypes = 'assetTypes'
    futureMonthX25 = 'futureMonthX25'
    bcid = 'bcid'
    mktPoint = 'mktPoint'
    futureMonthX24 = 'futureMonthX24'
    restrictionStartDate = 'restrictionStartDate'
    touchLiquidityScore = 'touchLiquidityScore'
    futureMonthX23 = 'futureMonthX23'
    futureMonthX22 = 'futureMonthX22'
    factorCategoryId = 'factorCategoryId'
    securityTypeId = 'securityTypeId'
    futureMonthX21 = 'futureMonthX21'
    investmentYtd = 'investmentYtd'
    leg2Notional = 'leg2Notional'
    sell1bps = 'sell1bps'
    sell200cents = 'sell200cents'
    expectedCompletionDate = 'expectedCompletionDate'
    spreadOptionVol = 'spreadOptionVol'
    sell80cents = 'sell80cents'
    impliedRetailPctAdv = 'impliedRetailPctAdv'
    inflationSwapRate = 'inflationSwapRate'
    activeQueries = 'activeQueries'
    sell45bps = 'sell45bps'
    gsLiquidityScore = 'gsLiquidityScore'
    embededOption = 'embededOption'
    eventSource = 'eventSource'
    qisPermNo = 'qisPermNo'
    settlement = 'settlement'
    shareclassId = 'shareclassId'
    feature2 = 'feature2'
    feature3 = 'feature3'
    settlementCurrency2 = 'settlementCurrency2'
    stsCommoditySector = 'stsCommoditySector'
    exceptionStatus = 'exceptionStatus'
    overnightNewsIntensity = 'overnightNewsIntensity'
    salesCoverage = 'salesCoverage'
    feature1 = 'feature1'
    tcmCostParticipationRate10Pct = 'tcmCostParticipationRate10Pct'
    eventTime = 'eventTime'
    positionSourceName = 'positionSourceName'
    covid19Vaccine = 'covid19Vaccine'
    deliveryDate = 'deliveryDate'
    settlementCurrency1 = 'settlementCurrency1'
    cyclical = 'cyclical'
    interestRate = 'interestRate'
    side = 'side'
    dynamicHybridAggressiveStyle = 'dynamicHybridAggressiveStyle'
    complianceRestrictedStatus = 'complianceRestrictedStatus'
    borrowFee = 'borrowFee'
    everIcu = 'everIcu'
    noWorseThanLevel = 'noWorseThanLevel'
    updateTime = 'updateTime'
    loanSpread = 'loanSpread'
    tcmCostHorizon12Hour = 'tcmCostHorizon12Hour'
    dewPoint = 'dewPoint'
    researchCommission = 'researchCommission'
    buy2bps = 'buy2bps'
    assetClassificationsRiskCountryCode = 'assetClassificationsRiskCountryCode'
    newIdeasMtd = 'newIdeasMtd'
    varSwapByExpiry = 'varSwapByExpiry'
    sellDate = 'sellDate'
    aumStart = 'aumStart'
    fwdEbookRiskDirClientSellOver = 'fwdEbookRiskDirClientSellOver'
    feedbackType = 'feedbackType'
    assetParametersSettlement = 'assetParametersSettlement'
    maxTemperature = 'maxTemperature'
    acquirerShareholderMeetingDate = 'acquirerShareholderMeetingDate'
    countIdeasWtd = 'countIdeasWtd'
    arrivalRtNormalized = 'arrivalRtNormalized'
    reportType = 'reportType'
    sourceURL = 'sourceURL'
    estimatedReturn = 'estimatedReturn'
    tradedFwdPoints = 'tradedFwdPoints'
    high = 'high'
    sourceLastUpdate = 'sourceLastUpdate'
    sunshineForecast = 'sunshineForecast'
    quantityMW = 'quantityMW'
    sell70cents = 'sell70cents'
    sell110cents = 'sell110cents'
    pnodeId = 'pnodeId'
    price1 = 'price1'
    price2 = 'price2'
    referenceRate = 'referenceRate'
    humidityType = 'humidityType'
    prevCloseAsk = 'prevCloseAsk'
    level = 'level'
    impliedVolatilityByExpiration = 'impliedVolatilityByExpiration'
    hurdle = 'hurdle'
    assetParametersFixedRateDayCountFraction = 'assetParametersFixedRateDayCountFraction'
    esMomentumScore = 'esMomentumScore'
    leg1CommodityInstrumentId = 'leg1CommodityInstrumentId'
    leg2Index = 'leg2Index'
    netWeight = 'netWeight'
    portfolioManagers = 'portfolioManagers'
    bosInTicks = 'bosInTicks'
    assetParametersCouponType = 'assetParametersCouponType'
    swapPointsAsk = 'swapPointsAsk'
    expectedResidualQuantity = 'expectedResidualQuantity'
    clientSwapPointsBid = 'clientSwapPointsBid'
    rollDate = 'rollDate'
    dynamicHybridSpeed = 'dynamicHybridSpeed'
    capFloorVol = 'capFloorVol'
    targetQuantity = 'targetQuantity'
    submitter = 'submitter'
    no = 'no'
    notional = 'notional'
    esDisclosurePercentage = 'esDisclosurePercentage'
    closeExecutedQuantityPercentage = 'closeExecutedQuantityPercentage'
    twapRealizedCash = 'twapRealizedCash'
    isOpenAuction = 'isOpenAuction'
    leg1Type = 'leg1Type'
    wetBulbTempHourlyForecast = 'wetBulbTempHourlyForecast'
    cleanupPrice = 'cleanupPrice'
    externalRejectReason = 'externalRejectReason'
    total = 'total'
    filledNotionalUSD = 'filledNotionalUSD'
    assetId = 'assetId'
    blockTradeElectionIndicator = 'blockTradeElectionIndicator'
    testStatus = 'testStatus'
    mktType = 'mktType'
    covidDisrupted = 'covidDisrupted'
    lastUpdatedTime = 'lastUpdatedTime'
    yield30Day = 'yield30Day'
    optionPutPremium = 'optionPutPremium'
    buy28bps = 'buy28bps'
    proportionOfRisk = 'proportionOfRisk'
    futureMonthK23 = 'futureMonthK23'
    futureMonthK22 = 'futureMonthK22'
    futureMonthK21 = 'futureMonthK21'
    primaryEntityId = 'primaryEntityId'
    cross = 'cross'
    ideaStatus = 'ideaStatus'
    inCode = 'inCode'
    contractSubtype = 'contractSubtype'
    sri = 'sri'
    fxForecast = 'fxForecast'
    fixingTimeLabel = 'fixingTimeLabel'
    isETF = 'isETF'
    _100 = '100'
    _101 = '101'
    _102 = '102'
    _103 = '103'
    _104 = '104'
    fillId = 'fillId'
    excessReturns = 'excessReturns'
    _105 = '105'
    _106 = '106'
    dollarReturn = 'dollarReturn'
    orderInLimit = 'orderInLimit'
    expiryTime = 'expiryTime'
    _107 = '107'
    returnOnEquity = 'returnOnEquity'
    _108 = '108'
    _109 = '109'
    futureMonthK26 = 'futureMonthK26'
    futureMonthK25 = 'futureMonthK25'
    futureMonthK24 = 'futureMonthK24'
    restrictionEndDate = 'restrictionEndDate'
    queueInLotsDescription = 'queueInLotsDescription'
    volumeLimit = 'volumeLimit'
    objective = 'objective'
    navPrice = 'navPrice'
    leg1UnderlyingAsset = 'leg1UnderlyingAsset'
    _110 = '110'
    bbgid = 'bbgid'
    _111 = '111'
    _112 = '112'
    _113 = '113'
    privatePlacementType = 'privatePlacementType'
    _114 = '114'
    hedgeNotional = 'hedgeNotional'
    _115 = '115'
    _116 = '116'
    askLow = 'askLow'
    intendedPRate = 'intendedPRate'
    _117 = '117'
    _118 = '118'
    _119 = '119'
    expiry = 'expiry'
    assetParametersIndexFamily = 'assetParametersIndexFamily'
    avgMonthlyYield = 'avgMonthlyYield'
    periodDirection = 'periodDirection'
    prevRptId = 'prevRptId'
    earningsPerShare = 'earningsPerShare'
    strikePercentage = 'strikePercentage'
    esProductImpactPercentile = 'esProductImpactPercentile'
    vwapRealizedCash = 'vwapRealizedCash'
    parAssetSwapSpread1m = 'parAssetSwapSpread1m'
    prevCloseBid = 'prevCloseBid'
    minimumIncrement = 'minimumIncrement'
    tcmCostHorizon16Day = 'tcmCostHorizon16Day'
    investmentMtd = 'investmentMtd'
    settlementDate = 'settlementDate'
    weightedAverageMidNormalized = 'weightedAverageMidNormalized'
    _120 = '120'
    windowLength = 'windowLength'
    _121 = '121'
    _122 = '122'
    salesPerShare = 'salesPerShare'
    _123 = '123'
    _124 = '124'
    _125 = '125'
    unadjustedClose = 'unadjustedClose'
    _126 = '126'
    _127 = '127'
    _128 = '128'
    _129 = '129'
    loanDate = 'loanDate'
    matchedMaturitySwapSpread1m = 'matchedMaturitySwapSpread1m'
    collateralPercentageActual = 'collateralPercentageActual'
    vwapInLimitUnrealizedBps = 'vwapInLimitUnrealizedBps'
    metricValue = 'metricValue'
    autoExecState = 'autoExecState'
    totalRecovered = 'totalRecovered'
    relativeReturnYtd = 'relativeReturnYtd'
    _130 = '130'
    tickServer = 'tickServer'
    _131 = '131'
    _132 = '132'
    _133 = '133'
    clientOutrightAsk = 'clientOutrightAsk'
    _134 = '134'
    cumulativeVolumeInPercentage = 'cumulativeVolumeInPercentage'
    _135 = '135'
    underlyingRic = 'underlyingRic'
    _136 = '136'
    _137 = '137'
    _138 = '138'
    _139 = '139'
    realTimeRestrictionStatus = 'realTimeRestrictionStatus'
    tradeType = 'tradeType'
    settlementType = 'settlementType'
    netChange = 'netChange'
    percentOfIssueOutstanding = 'percentOfIssueOutstanding'
    numberOfUnderliers = 'numberOfUnderliers'
    swapType = 'swapType'
    forecastType = 'forecastType'
    leg1Notional = 'leg1Notional'
    sellSettleDate = 'sellSettleDate'
    _140 = '140'
    _141 = '141'
    _142 = '142'
    _143 = '143'
    _144 = '144'
    _145 = '145'
    _146 = '146'
    _147 = '147'
    newIdeasYtd = 'newIdeasYtd'
    managementFee = 'managementFee'
    _148 = '148'
    _149 = '149'
    parAssetSwapSpread3m = 'parAssetSwapSpread3m'
    sell36bps = 'sell36bps'
    matchedMaturitySwapSpread3m = 'matchedMaturitySwapSpread3m'
    sourceId = 'sourceId'
    country = 'country'
    optionPremiumCurrency = 'optionPremiumCurrency'
    vwap = 'vwap'
    touchSpreadScore = 'touchSpreadScore'
    ratingSecondHighest = 'ratingSecondHighest'
    sell24bps = 'sell24bps'
    _150 = '150'
    _151 = '151'
    _152 = '152'
    frequency = 'frequency'
    _153 = '153'
    _154 = '154'
    activityId = 'activityId'
    _155 = '155'
    estimatedImpact = 'estimatedImpact'
    sell35cents = 'sell35cents'
    _156 = '156'
    loanSpreadBucket = 'loanSpreadBucket'
    _157 = '157'
    _158 = '158'
    coronavirusGlobalActivityTracker = 'coronavirusGlobalActivityTracker'
    _159 = '159'
    underlyers = 'underlyers'
    assetParametersPricingLocation = 'assetParametersPricingLocation'
    eventDescription = 'eventDescription'
    icebergMaxSize = 'icebergMaxSize'
    assetParametersCoupon = 'assetParametersCoupon'
    details = 'details'
    sector = 'sector'
    mktFwdPointAsk = 'mktFwdPointAsk'
    avgBedUtilRate = 'avgBedUtilRate'
    buy20bps = 'buy20bps'
    indexLevel = 'indexLevel'
    epidemic = 'epidemic'
    mctr = 'mctr'
    exchangeTime = 'exchangeTime'
    historicalClose = 'historicalClose'
    fipsCode = 'fipsCode'
    _160 = '160'
    chargeInQuoteConvention = 'chargeInQuoteConvention'
    _161 = '161'
    buy32bps = 'buy32bps'
    _162 = '162'
    _163 = '163'
    ideaId = 'ideaId'
    commentStatus = 'commentStatus'
    marginalCost = 'marginalCost'
    _164 = '164'
    _165 = '165'
    _166 = '166'
    _167 = '167'
    _168 = '168'
    clientWeight = 'clientWeight'
    _169 = '169'
    leg1DeliveryPoint = 'leg1DeliveryPoint'
    sell5cents = 'sell5cents'
    liqWkly = 'liqWkly'
    unrealizedTwapPerformanceBps = 'unrealizedTwapPerformanceBps'
    region = 'region'
    temperatureHour = 'temperatureHour'
    upperBound = 'upperBound'
    sell55cents = 'sell55cents'
    spreadToBenchmark = 'spreadToBenchmark'
    _170 = '170'
    _171 = '171'
    numPediIcuBeds = 'numPediIcuBeds'
    _172 = '172'
    bidYield = 'bidYield'
    _173 = '173'
    assetParametersStrikePrice = 'assetParametersStrikePrice'
    _174 = '174'
    expectedResidual = 'expectedResidual'
    _175 = '175'
    _176 = '176'
    optionPremium = 'optionPremium'
    _177 = '177'
    _178 = '178'
    _179 = '179'
    ownerName = 'ownerName'
    parAssetSwapSpread6m = 'parAssetSwapSpread6m'
    zScore = 'zScore'
    sell12bps = 'sell12bps'
    eventStartTime = 'eventStartTime'
    matchedMaturitySwapSpread6m = 'matchedMaturitySwapSpread6m'
    turnover = 'turnover'
    priceSpotTargetUnit = 'priceSpotTargetUnit'
    coverage = 'coverage'
    gPercentile = 'gPercentile'
    _180 = '180'
    rvtAdj = 'rvtAdj'
    _181 = '181'
    _182 = '182'
    cloudCoverHourlyForecast = 'cloudCoverHourlyForecast'
    _183 = '183'
    assetParametersPayerSpread = 'assetParametersPayerSpread'
    _184 = '184'
    lendingFundNav = 'lendingFundNav'
    sourceOriginalCategory = 'sourceOriginalCategory'
    percentCloseExecutionQuantity = 'percentCloseExecutionQuantity'
    _185 = '185'
    latestExecutionTime = 'latestExecutionTime'
    _186 = '186'
    _187 = '187'
    arrivalMidRealizedBps = 'arrivalMidRealizedBps'
    _188 = '188'
    _189 = '189'
    location = 'location'
    scenarioId = 'scenarioId'
    terminationTenor = 'terminationTenor'
    queueClockTime = 'queueClockTime'
    discretionLowerBound = 'discretionLowerBound'
    tcmCostParticipationRate50Pct = 'tcmCostParticipationRate50Pct'
    ratingLinear = 'ratingLinear'
    previousCloseUnrealizedBps = 'previousCloseUnrealizedBps'
    _190 = '190'
    _191 = '191'
    subAssetClassForOtherCommodity = 'subAssetClassForOtherCommodity'
    _192 = '192'
    forwardPrice = 'forwardPrice'
    _193 = '193'
    type = 'type'
    fwdPointsMarketBid = 'fwdPointsMarketBid'
    _194 = '194'
    strikeRef = 'strikeRef'
    _195 = '195'
    _196 = '196'
    _197 = '197'
    cumulativePnl = 'cumulativePnl'
    _198 = '198'
    shortTenor = 'shortTenor'
    sell28bps = 'sell28bps'
    fundClass = 'fundClass'
    _199 = '199'
    unadjustedVolume = 'unadjustedVolume'
    buy36bps = 'buy36bps'
    positionIdx = 'positionIdx'
    cvaDollarChargeBid = 'cvaDollarChargeBid'
    midZSpread = 'midZSpread'
    windChillHourlyForecast = 'windChillHourlyForecast'
    secName = 'secName'
    impliedVolatilityByRelativeStrike = 'impliedVolatilityByRelativeStrike'
    assetParametersIndex2Tenor = 'assetParametersIndex2Tenor'
    percentADV = 'percentADV'
    referenceRateUSD = 'referenceRateUSD'
    leg1TotalNotional = 'leg1TotalNotional'
    contract = 'contract'
    nvtAdj90 = 'nvtAdj90'
    paymentFrequency1 = 'paymentFrequency1'
    paymentFrequency2 = 'paymentFrequency2'
    bespoke = 'bespoke'
    repoTenor = 'repoTenor'
    sell15cents = 'sell15cents'
    quoteId = 'quoteId'
    investmentQtd = 'investmentQtd'
    heatIndexForecast = 'heatIndexForecast'
    ratingStandardAndPoors = 'ratingStandardAndPoors'
    qualityStars = 'qualityStars'
    leg2FloatingIndex = 'leg2FloatingIndex'
    sourceTicker = 'sourceTicker'
    primaryVwapUnrealizedBps = 'primaryVwapUnrealizedBps'
    assetParametersCreditIndexSeries = 'assetParametersCreditIndexSeries'
    gsid = 'gsid'
    lendingFund = 'lendingFund'
    sensitivity = 'sensitivity'
    clientSwapPointsAsk = 'clientSwapPointsAsk'
    embeddedOptionType = 'embeddedOptionType'
    dayCount = 'dayCount'
    sell16bps = 'sell16bps'
    relativeBreakEvenInflationChange = 'relativeBreakEvenInflationChange'
    sell25cents = 'sell25cents'
    varSwap = 'varSwap'
    buy5point5bps = 'buy5point5bps'
    blockLargeNotional = 'blockLargeNotional'
    sell2point5bps = 'sell2point5bps'
    capacity = 'capacity'
    sectorsRaw = 'sectorsRaw'
    chargeInDollars = 'chargeInDollars'
    primaryVwapInLimit = 'primaryVwapInLimit'
    shareclassPrice = 'shareclassPrice'
    fwdEbookRiskDirClientBuyUnder = 'fwdEbookRiskDirClientBuyUnder'
    tradeSize = 'tradeSize'
    priceSpotEntryValue = 'priceSpotEntryValue'
    buy8point5bps = 'buy8point5bps'
    symbolDimensions = 'symbolDimensions'
    buy24bps = 'buy24bps'
    auctionCloseQuantity = 'auctionCloseQuantity'
    sidePocket = 'sidePocket'
    observation = 'observation'
    optionTypeSDR = 'optionTypeSDR'
    isEntity = 'isEntity'
    scenarioGroupId = 'scenarioGroupId'
    averageImpliedVariance = 'averageImpliedVariance'
    avgTradeRateDescription = 'avgTradeRateDescription'
    fraction = 'fraction'
    assetCountShort = 'assetCountShort'
    collateralPercentageRequired = 'collateralPercentageRequired'
    spotMarketAsk = 'spotMarketAsk'
    sell5point5bps = 'sell5point5bps'
    date = 'date'
    zipCode = 'zipCode'
    totalStdReturnSinceInception = 'totalStdReturnSinceInception'
    sourceCategory = 'sourceCategory'
    volumeUnadjusted = 'volumeUnadjusted'
    passiveRatio = 'passiveRatio'
    priceToEarnings = 'priceToEarnings'
    orderDepth = 'orderDepth'
    annYield3Month = 'annYield3Month'
    netFlowStd = 'netFlowStd'
    eZeroPriceWhenTraded = 'eZeroPriceWhenTraded'
    assetParametersFeeCurrency = 'assetParametersFeeCurrency'
    encodedStats = 'encodedStats'
    buy5bps = 'buy5bps'
    runTime = 'runTime'
    askSize = 'askSize'
    absoluteReturnMtd = 'absoluteReturnMtd'
    std30DaysUnsubsidizedYield = 'std30DaysUnsubsidizedYield'
    assetParametersReceiverSpread = 'assetParametersReceiverSpread'
    resource = 'resource'
    averageRealizedVolatility = 'averageRealizedVolatility'
    traceAdvBuy = 'traceAdvBuy'
    newConfirmed = 'newConfirmed'
    tax = 'tax'
    sell8bps = 'sell8bps'
    bidPrice = 'bidPrice'
    optionCallPremium = 'optionCallPremium'
    sell8point5bps = 'sell8point5bps'
    targetPriceUnrealizedBps = 'targetPriceUnrealizedBps'
    clientSpotBid = 'clientSpotBid'
    assetParametersCallCurrency = 'assetParametersCallCurrency'
    esNumericPercentile = 'esNumericPercentile'
    leg2UnderlyingAsset = 'leg2UnderlyingAsset'
    csaTerms = 'csaTerms'
    relativePayoffMtd = 'relativePayoffMtd'
    dailyNetShareholderFlows = 'dailyNetShareholderFlows'
    buy2point5bps = 'buy2point5bps'
    cai = 'cai'
    executedNotionalUSD = 'executedNotionalUSD'
    systemTime = 'systemTime'
    totalHomeIsolation = 'totalHomeIsolation'
    stationName = 'stationName'
    passPct = 'passPct'
    openingReport = 'openingReport'
    eventTimestamp = 'eventTimestamp'
    tcm = 'tcm'
    midcurveAtmFwdRate = 'midcurveAtmFwdRate'
    precipitationForecast = 'precipitationForecast'
    equityRiskPremiumIndex = 'equityRiskPremiumIndex'
    fatalitiesUnderlyingConditionsUnknown = 'fatalitiesUnderlyingConditionsUnknown'
    buy12bps = 'buy12bps'
    clearingHouse = 'clearingHouse'
    dayCloseUnrealizedBps = 'dayCloseUnrealizedBps'
    stsRatesMaturity = 'stsRatesMaturity'
    nonOwnerId = 'nonOwnerId'
    liqDly = 'liqDly'
    contributorRole = 'contributorRole'
    totalFatalities = 'totalFatalities'
    internalRejectReason = 'internalRejectReason'
    adjustedClose = 'adjustedClose'
    averageValue = 'averageValue'
    avgInterestRate = 'avgInterestRate'
    basisDuration = 'basisDuration'
    bestMonthDate = 'bestMonthDate'
    bloombergTicker = 'bloombergTicker'
    capexDepreciation = 'capexDepreciation'
    capexSales = 'capexSales'
    cashConversion = 'cashConversion'
    category = 'category'
    convexity = 'convexity'
    countryCode = 'countryCode'
    croci = 'croci'
    currentValue = 'currentValue'
    dacf = 'dacf'
    dailyVolatility = 'dailyVolatility'
    divYield = 'divYield'
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
    netDebtEbitda = 'netDebtEbitda'
    netDebtEquity = 'netDebtEquity'
    niGrowth = 'niGrowth'
    niMargin = 'niMargin'
    oisMatchedMaturitySwap = 'oisMatchedMaturitySwap'
    oisProceedsASW = 'oisProceedsASW'
    oiszSpread = 'oiszSpread'
    optionStyle = 'optionStyle'
    payup = 'payup'
    preTaxProfitGrowth = 'preTaxProfitGrowth'
    riskPremiaStyles = 'riskPremiaStyles'
    roce = 'roce'
    rolldown = 'rolldown'
    salesGrowth = 'salesGrowth'
    sharpeRatio = 'sharpeRatio'
    totalDebtCapital = 'totalDebtCapital'
    totalDebtTotalAsset = 'totalDebtTotalAsset'
    totalReturn = 'totalReturn'
    unleveredFcfYield = 'unleveredFcfYield'
    worstMonthDate = 'worstMonthDate'    


class FiniteDifferenceMethod(EnumBase, Enum):    
    
    """Direction and dimension of finite difference"""

    Up = 'Up'
    Centered = 'Centered'
    Down = 'Down'
    CenteredSecondOrder = 'CenteredSecondOrder'    


class Format(EnumBase, Enum):    
    
    """Alternative format for data to be returned in"""

    Json = 'Json'
    Excel = 'Excel'
    MessagePack = 'MessagePack'
    Pdf = 'Pdf'    


class InOut(EnumBase, Enum):    
    
    In = 'In'
    Out = 'Out'    


class IndexNotTradingReasons(EnumBase, Enum):    
    
    """Reasons the index was not traded"""

    Cost = 'Cost'
    Client_does_not_like_the_construction = 'Client does not like the construction'
    Basket_created_prematurely = 'Basket created prematurely'
    Economics_of_the_basket_changed__client_no_longer_interested_in_trading = 'Economics of the basket changed: client no longer interested in trading'
    GS_booking_OVER_operational_issues = 'GS booking/operational issues'
    _ = ''    


class KnockoutConvention(EnumBase, Enum):    
    
    """Knockout convention"""

    Continuous = 'Continuous'    


class LiquidityMeasure(EnumBase, Enum):    
    
    """A list of the different liquidity measures to choose from."""

    Summary = 'Summary'
    Constituent_Transaction_Costs = 'Constituent Transaction Costs'
    Constituents = 'Constituents'
    Largest_Holdings_By_Weight = 'Largest Holdings By Weight'
    Least_Liquid_Holdings = 'Least Liquid Holdings'
    ADV_Percent_Buckets = 'ADV Percent Buckets'
    Market_Cap_Buckets = 'Market Cap Buckets'
    Region_Buckets = 'Region Buckets'
    Country_Buckets = 'Country Buckets'
    Sector_Buckets = 'Sector Buckets'
    Industry_Buckets = 'Industry Buckets'
    Risk_Buckets = 'Risk Buckets'
    Factor_Risk_Buckets = 'Factor Risk Buckets'
    Exposure_Buckets = 'Exposure Buckets'
    Factor_Exposure_Buckets = 'Factor Exposure Buckets'
    Percent_Of_Trade_Complete_Over_Time = 'Percent Of Trade Complete Over Time'
    Execution_Cost_With_Different_Time_Horizons = 'Execution Cost With Different Time Horizons'
    Participation_Rate_With_Different_Time_Horizons = 'Participation Rate With Different Time Horizons'
    Risk_With_Different_Time_Horizons = 'Risk With Different Time Horizons'
    Historical_ADV_Percent_Curve = 'Historical ADV Percent Curve'
    Time_Series_Data = 'Time Series Data'    


class MarketDataShockType(EnumBase, Enum):    
    
    """Market data shock type"""

    Absolute = 'Absolute'
    Proportional = 'Proportional'
    Invalid = 'Invalid'
    Override = 'Override'
    StdDev = 'StdDev'
    AutoDefault = 'AutoDefault'
    CSWFFR = 'CSWFFR'
    StdVolFactor = 'StdVolFactor'
    StdVolFactorProportional = 'StdVolFactorProportional'    


class MarketDataVendor(EnumBase, Enum):    
    
    Goldman_Sachs = 'Goldman Sachs'
    Thomson_Reuters = 'Thomson Reuters'
    Solactive = 'Solactive'
    Bloomberg = 'Bloomberg'
    Axioma = 'Axioma'
    Goldman_Sachs_Prime_Services = 'Goldman Sachs Prime Services'
    Goldman_Sachs_Global_Investment_Research = 'Goldman Sachs Global Investment Research'
    National_Weather_Service = 'National Weather Service'
    WM = 'WM'
    Hedge_Fund_Research__Inc_ = 'Hedge Fund Research, Inc.'
    London_Stock_Exchange = 'London Stock Exchange'
    Goldman_Sachs_MDFarm = 'Goldman Sachs MDFarm'
    PredictIt = 'PredictIt'
    Iowa_Electronic_Markets = 'Iowa Electronic Markets'
    RealClearPolitics = 'RealClearPolitics'
    _538 = '538'
    FiveThirtyEight = 'FiveThirtyEight'
    Opinium = 'Opinium'
    YouGov = 'YouGov'
    MorningStar = 'MorningStar'
    Survation = 'Survation'
    Survation__YouGov = 'Survation, YouGov'
    European_Centre_for_Disease_Prevention_and_Control = 'European Centre for Disease Prevention and Control'
    Centers_for_Disease_Control_and_Prevention = 'Centers for Disease Control and Prevention'
    Johns_Hopkins_University = 'Johns Hopkins University'
    Google = 'Google'
    National_Health_Service = 'National Health Service'
    World_Health_Organization = 'World Health Organization'
    Wikipedia = 'Wikipedia'
    StarSchema = 'StarSchema'
    Covid_Working_Group = 'Covid Working Group'
    CovidTracking = 'CovidTracking'
    Bing = 'Bing'
    FRED = 'FRED'
    Institute_for_Health_Metrics_and_Evaluation = 'Institute for Health Metrics and Evaluation'
    Refinitiv = 'Refinitiv'
    Goldman_Sachs_Global_Investment_Research__Refinitiv = 'Goldman Sachs Global Investment Research, Refinitiv'
    EPFR = 'EPFR'
    Coin_Metrics = 'Coin Metrics'
    MSCI = 'MSCI'
    MuniNet = 'MuniNet'
    Rearc_via_AWS_Data_Exchange = 'Rearc via AWS Data Exchange'
    Bank_of_Japan = 'Bank of Japan'    


class OptionExpiryType(EnumBase, Enum):    
    
    _1m = '1m'
    _2m = '2m'
    _3m = '3m'
    _4m = '4m'
    _5m = '5m'
    _6m = '6m'    


class OptionSettlementMethod(EnumBase, Enum):    
    
    """How the option is settled (e.g. Cash, Physical)"""

    Cash = 'Cash'
    Physical = 'Physical'    


class OptionStrikeType(EnumBase, Enum):    
    
    Relative = 'Relative'
    Delta = 'Delta'    


class OptionStyle(EnumBase, Enum):    
    
    """Option Exercise Style"""

    European = 'European'
    American = 'American'
    Bermudan = 'Bermudan'    


class OptionType(EnumBase, Enum):    
    
    """Option Type"""

    Call = 'Call'
    Put = 'Put'
    Binary_Call = 'Binary Call'
    Binary_Put = 'Binary Put'    


class PCOActionType(EnumBase, Enum):    
    
    """Types of PCO Actions"""

    Generate_Orders = 'Generate Orders'
    Update_Parameters = 'Update Parameters'
    Update_Client_Data = 'Update Client Data'
    Update_Open_Hedge_Notional = 'Update Open Hedge Notional'
    Add_Order = 'Add Order'    


class PCOCurrencyType(EnumBase, Enum):    
    
    """Currency Type Options for PCO"""

    Exposure = 'Exposure'
    Base = 'Base'
    Local = 'Local'    


class PCOOrigin(EnumBase, Enum):    
    
    """Origin of PCO Report"""

    PCOGui = 'PCOGui'
    PCOBackend = 'PCOBackend'    


class PayReceive(EnumBase, Enum):    
    
    """Pay or receive fixed"""

    Pay = 'Pay'
    Payer = 'Payer'
    Receive = 'Receive'
    Receiver = 'Receiver'
    Straddle = 'Straddle'
    Rec = 'Rec'    


class PayoutType(EnumBase, Enum):    
    
    """Delayed or Immediate payout"""

    Delayed = 'Delayed'
    Immediate = 'Immediate'    


class Period(EnumBase, Enum):    
    
    """A coding scheme to define a period corresponding to a quantity amount"""

    Month = 'Month'
    Quarter = 'Quarter'
    Hour = 'Hour'
    Day = 'Day'
    BusinessDay = 'BusinessDay'    


class PricingLocation(EnumBase, Enum):    
    
    """Based on the location of the exchange. Called 'Native Region' in SecDB"""

    NYC = 'NYC'
    LDN = 'LDN'
    TKO = 'TKO'
    HKG = 'HKG'    


class PrincipalExchange(EnumBase, Enum):    
    
    """How principal is exchanged"""

    _None = 'None'
    Both = 'Both'
    First = 'First'
    Last = 'Last'    


class ProductCode(EnumBase, Enum):    
    
    """Override the clearing destination/symbol"""

    CME__BB = 'CME::BB'
    CME__BK = 'CME::BK'
    CME__BY = 'CME::BY'
    CME__BZ = 'CME::BZ'
    CME__CL = 'CME::CL'
    CME__CL_BZ = 'CME::CL-BZ'
    CME__CS = 'CME::CS'
    CME__CY = 'CME::CY'
    CME__HK = 'CME::HK'
    CME__HO = 'CME::HO'
    CME__HOB = 'CME::HOB'
    CME__HO_CL = 'CME::HO-CL'
    CME__MP = 'CME::MP'
    CME__NG = 'CME::NG'
    CME__NLS = 'CME::NLS'
    CME__RB = 'CME::RB'
    CME__RBB = 'CME::RBB'
    CME__RB_BZ = 'CME::RB-BZ'
    CME__RB_CL = 'CME::RB-CL'
    CME__RH = 'CME::RH'
    CME__RL = 'CME::RL'
    CME__RM = 'CME::RM'
    CME__WS = 'CME::WS'
    CME_ICE__RB_B = 'CME-ICE::RB-B'
    ICE__B = 'ICE::B'
    ICE__BNB = 'ICE::BNB'
    ICE__BTD = 'ICE::BTD'
    ICE__G = 'ICE::G'
    ICE__G_B = 'ICE::G-B'
    ICE__HBT = 'ICE::HBT'
    ICE__HNG = 'ICE::HNG'
    ICE__HOF = 'ICE::HOF'
    ICE__I = 'ICE::I'
    ICE__N = 'ICE::N'
    ICE__N_B = 'ICE::N-B'
    ICE__O = 'ICE::O'
    ICE__O_B = 'ICE::O-B'
    ICE__R = 'ICE::R'
    ICE__RBR = 'ICE::RBR'
    ICE__T = 'ICE::T'
    ICE__T_B = 'ICE::T-B'
    ICE__ULA = 'ICE::ULA'
    ICE__ULC = 'ICE::ULC'
    ICE__ULD = 'ICE::ULD'
    ICE__ULM = 'ICE::ULM'
    ICE__WTB = 'ICE::WTB'
    LME__MAL = 'LME::MAL'
    LME__MNI = 'LME::MNI'
    LME__MPB = 'LME::MPB'
    LME__MZN = 'LME::MZN'
    OTC__BRT = 'OTC::BRT'
    OTC__GO = 'OTC::GO'
    OTC__GO_BRT = 'OTC::GO-BRT'
    OTC__HO = 'OTC::HO'
    OTC__HO_BRT = 'OTC::HO-BRT'
    OTC__HO_GO = 'OTC::HO-GO'
    OTC__HO_WTI = 'OTC::HO-WTI'
    OTC__MAL = 'OTC::MAL'
    OTC__MNI = 'OTC::MNI'
    OTC__MPB = 'OTC::MPB'
    OTC__MZN = 'OTC::MZN'
    OTC__NG = 'OTC::NG'
    OTC__RB = 'OTC::RB'
    OTC__RB_BRT = 'OTC::RB-BRT'
    OTC__RB_HO = 'OTC::RB-HO'
    OTC__RB_WTI = 'OTC::RB-WTI'
    OTC__WTI = 'OTC::WTI'
    OTC__WTI_BRT = 'OTC::WTI-BRT'    


class ProductType(EnumBase, Enum):    
    
    """Product type of basket"""

    Flow = 'Flow'
    MPS = 'MPS'
    Volatility = 'Volatility'
    Single_Stock = 'Single Stock'    


class Region(EnumBase, Enum):    
    
    """Regional classification for the asset"""

    _ = ''
    Americas = 'Americas'
    Asia = 'Asia'
    EM = 'EM'
    Europe = 'Europe'
    Global = 'Global'    


class ReportJobPriority(EnumBase, Enum):    
    
    """Report job priority."""

    High = 'High'
    Normal = 'Normal'    


class RiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Annual_ATM_Implied_Volatility = 'Annual ATM Implied Volatility'
    Annual_ATMF_Implied_Volatility = 'Annual ATMF Implied Volatility'
    Annual_Implied_Volatility = 'Annual Implied Volatility'
    AnnuityLocalCcy = 'AnnuityLocalCcy'
    ATM_Spread = 'ATM Spread'
    BaseCPI = 'BaseCPI'
    Basis = 'Basis'
    BSPrice = 'BSPrice'
    CRIF_IRCurve = 'CRIF IRCurve'
    Cashflows = 'Cashflows'
    Compounded_Fixed_Rate = 'Compounded Fixed Rate'
    Cross_Multiplier = 'Cross Multiplier'
    Daily_Implied_Volatility = 'Daily Implied Volatility'
    Delta = 'Delta'
    DeltaLocalCcy = 'DeltaLocalCcy'
    Description = 'Description'
    Dollar_Price = 'Dollar Price'
    DV01 = 'DV01'
    Fair_Price = 'Fair Price'
    FairVarStrike = 'FairVarStrike'
    FairVolStrike = 'FairVolStrike'
    FinalCPI = 'FinalCPI'
    Forward_Price = 'Forward Price'
    Forward_Rate = 'Forward Rate'
    Forward_Spread = 'Forward Spread'
    FX_Calculated_Delta = 'FX Calculated Delta'
    FX_Calculated_Delta_No_Premium_Adjustment = 'FX Calculated Delta No Premium Adjustment'
    FX_Premium = 'FX Premium'
    FX_Quoted_Delta_No_Premium_Adjustment = 'FX Quoted Delta No Premium Adjustment'
    FX_Quoted_Vega = 'FX Quoted Vega'
    Price = 'Price'
    Gamma = 'Gamma'
    GammaLocalCcy = 'GammaLocalCcy'
    Implied_Volatility = 'Implied Volatility'
    InflationDelta = 'InflationDelta'
    Inflation_Compounding_Period = 'Inflation Compounding Period'
    Inflation_Delta_in_Bps = 'Inflation Delta in Bps'
    Local_Currency_Accrual_in_Cents = 'Local Currency Accrual in Cents'
    Local_Currency_Annuity = 'Local Currency Annuity'
    Market_Data = 'Market Data'
    Market_Data_Assets = 'Market Data Assets'
    MV = 'MV'
    NonUSDOisDomesticRate = 'NonUSDOisDomesticRate'
    OAS = 'OAS'
    OisFXSpreadRateExcludingSpikes = 'OisFXSpreadRateExcludingSpikes'
    OisFXSpreadRate = 'OisFXSpreadRate'
    ParallelBasis = 'ParallelBasis'
    ParallelDelta = 'ParallelDelta'
    ParallelDeltaLocalCcy = 'ParallelDeltaLocalCcy'
    ParallelDiscountDelta = 'ParallelDiscountDelta'
    ParallelDiscountDeltaLocalCcy = 'ParallelDiscountDeltaLocalCcy'
    ParallelInflationDelta = 'ParallelInflationDelta'
    ParallelIndexDelta = 'ParallelIndexDelta'
    ParallelIndexDeltaLocalCcy = 'ParallelIndexDeltaLocalCcy'
    ParallelInflationDeltaLocalCcy = 'ParallelInflationDeltaLocalCcy'
    ParallelXccyDelta = 'ParallelXccyDelta'
    ParallelXccyDeltaLocalCcy = 'ParallelXccyDeltaLocalCcy'
    ParallelGamma = 'ParallelGamma'
    ParallelGammaLocalCcy = 'ParallelGammaLocalCcy'
    ParallelVega = 'ParallelVega'
    ParallelVegaLocalCcy = 'ParallelVegaLocalCcy'
    Points = 'Points'
    Premium_In_Cents = 'Premium In Cents'
    Premium = 'Premium'
    Probability_Of_Exercise = 'Probability Of Exercise'
    Resolved_Instrument_Values = 'Resolved Instrument Values'
    PNL = 'PNL'
    PnlExplain = 'PnlExplain'
    PnlExplainLocalCcy = 'PnlExplainLocalCcy'
    PnlPredict = 'PnlPredict'
    PV = 'PV'
    QuotedDelta = 'QuotedDelta'
    Spot = 'Spot'
    Spot_Rate = 'Spot Rate'
    Spread = 'Spread'
    Strike = 'Strike'
    Theta = 'Theta'
    USDOisDomesticRate = 'USDOisDomesticRate'
    Vanna = 'Vanna'
    Vega = 'Vega'
    VegaLocalCcy = 'VegaLocalCcy'
    Volga = 'Volga'
    Volatility = 'Volatility'
    XccyDelta = 'XccyDelta'    


class RiskMeasureUnit(EnumBase, Enum):    
    
    """The unit of change of underlying in the risk computation."""

    Percent = 'Percent'
    Dollar = 'Dollar'
    BPS = 'BPS'
    Pips = 'Pips'    


class ScenarioType(EnumBase, Enum):    
    
    """Type of Scenario"""

    Spot_Vol = 'Spot Vol'
    Greeks = 'Greeks'    


class SettlementType(EnumBase, Enum):    
    
    """Settlement Type"""

    Cash = 'Cash'
    Physical = 'Physical'    


class Side(EnumBase, Enum):    
    
    """Official side of an index"""

    Bid = 'Bid'
    Ask = 'Ask'
    Mid = 'Mid'    


class Strategy(EnumBase, Enum):    
    
    """More specific descriptor of a fund's investment approach. Same view permissions
       as the asset"""

    Active_Extension = 'Active Extension'
    Active_Trading = 'Active Trading'
    Activist = 'Activist'
    Co_Invest__OVER__SPV = 'Co-Invest / SPV'
    Commodity = 'Commodity'
    Commodities = 'Commodities'
    Composite = 'Composite'
    Conservative = 'Conservative'
    Convert_Arb = 'Convert Arb'
    Convertible_Arbitrage = 'Convertible Arbitrage'
    Credit_Arbitrage = 'Credit Arbitrage'
    Cross_Capital_Structure = 'Cross-Capital-Structure'
    CTA__OVER__Managed_Futures = 'CTA / Managed Futures'
    Currency = 'Currency'
    Discretionary = 'Discretionary'
    Discretionary_Thematic = 'Discretionary Thematic'
    Distressed = 'Distressed'
    Distressed_Securities = 'Distressed Securities'
    Distressed_OVER_Restructuring = 'Distressed/Restructuring'
    Diversified = 'Diversified'
    Equity_Hedge = 'Equity Hedge'
    Equity_Market_Neutral = 'Equity Market Neutral'
    Equity_Only = 'Equity Only'
    Event_Driven = 'Event-Driven'
    Fixed_Income_Arb = 'Fixed Income Arb'
    Fixed_Income_Asset_Backed = 'Fixed Income-Asset Backed'
    Fixed_Income_Corporate = 'Fixed Income-Corporate'
    Fixed_Income_Sovereign = 'Fixed Income-Sovereign'
    Fundamental_Growth = 'Fundamental Growth'
    Fundamental_Value = 'Fundamental Value'
    General = 'General'
    General_Multi_Strategy = 'General Multi-Strategy'
    Generalist = 'Generalist'
    Hybrid__OVER__Illiquid = 'Hybrid / Illiquid'
    Long__OVER__Short = 'Long / Short'
    Macro = 'Macro'
    Market_Defensive = 'Market Defensive'
    Merger_Arb = 'Merger Arb'
    Merger_Arbitrage = 'Merger Arbitrage'
    Multi_Strategy = 'Multi-Strategy'
    Quantitative_Directional = 'Quantitative Directional'
    Relative_Value_Arbitrage = 'Relative Value Arbitrage'
    Risk_Premia = 'Risk Premia'
    Sector___Energy_OVER_Basic_Materials = 'Sector - Energy/Basic Materials'
    Sector___Healthcare = 'Sector - Healthcare'
    Sector___Technology = 'Sector - Technology'
    Sector___Technology_OVER_Healthcare = 'Sector - Technology/Healthcare'
    Sector_Specific = 'Sector-Specific'
    Short_Bias = 'Short Bias'
    Special_Situations = 'Special Situations'
    Stat_Arb = 'Stat Arb'
    Statistical_Arbitrage = 'Statistical Arbitrage'
    Strategic = 'Strategic'
    Structured = 'Structured'
    Systematic = 'Systematic'
    Systematic_Diversified = 'Systematic Diversified'
    Vol_Arb__OVER__Options = 'Vol Arb / Options'
    Volatility = 'Volatility'
    Volatility_Target_10 = 'Volatility Target 10'
    Volatility_Target_12 = 'Volatility Target 12'
    Volatility_Target_15 = 'Volatility Target 15'
    Yield_Alternative = 'Yield Alternative'    


class StrikeMethodType(EnumBase, Enum):    
    
    Spread = 'Spread'
    Delta = 'Delta'
    Percentage_of_Price = 'Percentage of Price'
    Fixed = 'Fixed'    


class SwapClearingHouse(EnumBase, Enum):    
    
    """Swap Clearing House"""

    LCH = 'LCH'
    EUREX = 'EUREX'
    JSCC = 'JSCC'
    CME = 'CME'
    NONE = 'NONE'    


class SwapSettlement(EnumBase, Enum):    
    
    """Swap Settlement Type"""

    Phys_CLEARED = 'Phys.CLEARED'
    Physical = 'Physical'
    Cash_CollatCash = 'Cash.CollatCash'
    Cash_PYU = 'Cash.PYU'    


class TouchNoTouch(EnumBase, Enum):    
    
    """Indicates Touch or NoTouch"""

    Touch = 'Touch'
    No_Touch = 'No Touch'    


class TradeAs(EnumBase, Enum):    
    
    """Option trade as (i.e. listed, otc, lookalike etc)"""

    Listed = 'Listed'
    Listed_Look_alike_OTC = 'Listed Look alike OTC'
    Flex = 'Flex'
    OTC = 'OTC'    


class TradeType(EnumBase, Enum):    
    
    """Direction"""

    Buy = 'Buy'
    Sell = 'Sell'    


class UnderlierType(EnumBase, Enum):    
    
    """Type of underlyer"""

    BBID = 'BBID'
    CUSIP = 'CUSIP'
    ISIN = 'ISIN'
    SEDOL = 'SEDOL'
    RIC = 'RIC'
    Ticker = 'Ticker'    


class UpDown(EnumBase, Enum):    
    
    Up = 'Up'
    Down = 'Down'    


class ValuationTime(EnumBase, Enum):    
    
    """The time of valuation, e.g. for an option"""

    MktClose = 'MktClose'
    MktOpen = 'MktOpen'
    SQ = 'SQ'
    MktPreOpen = 'MktPreOpen'
    MktPrevClose = 'MktPrevClose'
    HedgeUnwind = 'HedgeUnwind'    


class VarianceConvention(EnumBase, Enum):    
    
    """Specifies whether the variance is Annualized or Total"""

    Annualized = 'Annualized'
    Total = 'Total'    


class AssetIdPriceable(Priceable):
        
    """An object to hold assetId when it can't be passed as a string."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        


class AssetScreenerCreditStandardAndPoorsRatingOptions(Base):
        
    """Options for credit screener rating filter."""

    @camel_case_translate
    def __init__(
        self,
        min_: str = None,
        max_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__min = min_
        self.__max = max_
        self.name = name

    @property
    def min(self) -> str:
        """Minimum rating the user chooses to filter on"""
        return self.__min

    @min.setter
    def min(self, value: str):
        self._property_changed('min')
        self.__min = value        

    @property
    def max(self) -> str:
        """Maximum rating the user chooses to filter on"""
        return self.__max

    @max.setter
    def max(self, value: str):
        self._property_changed('max')
        self.__max = value        


class AssetScreenerRequestFilterDateLimits(Base):
        
    """Min and max date limits for filters on asset screener."""

    @camel_case_translate
    def __init__(
        self,
        min_: datetime.date = None,
        max_: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.__min = min_
        self.__max = max_
        self.name = name

    @property
    def min(self) -> datetime.date:
        """lower constraint value"""
        return self.__min

    @min.setter
    def min(self, value: datetime.date):
        self._property_changed('min')
        self.__min = value        

    @property
    def max(self) -> datetime.date:
        """upper constraint value"""
        return self.__max

    @max.setter
    def max(self, value: datetime.date):
        self._property_changed('max')
        self.__max = value        


class AssetScreenerRequestFilterLimits(Base):
        
    """Min and max limits for filters on asset screener."""

    @camel_case_translate
    def __init__(
        self,
        min_: float = None,
        max_: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__min = min_
        self.__max = max_
        self.name = name

    @property
    def min(self) -> float:
        """lower constraint value"""
        return self.__min

    @min.setter
    def min(self, value: float):
        self._property_changed('min')
        self.__min = value        

    @property
    def max(self) -> float:
        """upper constraint value"""
        return self.__max

    @max.setter
    def max(self, value: float):
        self._property_changed('max')
        self.__max = value        


class CSLDate(Base):
        
    """A date"""

    @camel_case_translate
    def __init__(
        self,
        date_value: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.date_value = date_value
        self.name = name

    @property
    def date_value(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date_value

    @date_value.setter
    def date_value(self, value: datetime.date):
        self._property_changed('date_value')
        self.__date_value = value        


class CSLDouble(Base):
        
    """A double"""

    @camel_case_translate
    def __init__(
        self,
        double_value: float = None,
        name: str = None
    ):        
        super().__init__()
        self.double_value = double_value
        self.name = name

    @property
    def double_value(self) -> float:
        """The value"""
        return self.__double_value

    @double_value.setter
    def double_value(self, value: float):
        self._property_changed('double_value')
        self.__double_value = value        


class CSLFXCross(Base):
        
    """An FX cross"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """Currency pair"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLIndex(Base):
        
    """An index"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """Display name of the asset"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLSimpleSchedule(Base):
        
    """A fixing date, settlement date pair"""

    @camel_case_translate
    def __init__(
        self,
        fixing_date: datetime.date = None,
        settlement_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.fixing_date = fixing_date
        self.settlement_date = settlement_date
        self.name = name

    @property
    def fixing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__fixing_date

    @fixing_date.setter
    def fixing_date(self, value: datetime.date):
        self._property_changed('fixing_date')
        self.__fixing_date = value        

    @property
    def settlement_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        


class CSLStock(Base):
        
    """A stock"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """Display name of the asset"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLString(Base):
        
    """A string"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """The value"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLSymCaseNamedParam(Base):
        
    """A named case-sensitive string."""

    @camel_case_translate
    def __init__(
        self,
        sym_case_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.sym_case_value = sym_case_value
        self.name = name

    @property
    def sym_case_value(self) -> str:
        """A case-sensitive string"""
        return self.__sym_case_value

    @sym_case_value.setter
    def sym_case_value(self, value: str):
        self._property_changed('sym_case_value')
        self.__sym_case_value = value        

    @property
    def name(self) -> str:
        """A name for the symbol"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class CurrencyParameter(Base):
        
    """Extra parameters for Currency"""

    @camel_case_translate
    def __init__(
        self,
        value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.value = value
        self.name = name

    @property
    def parameter_type(self) -> str:
        """Currency"""
        return 'Currency'        

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        


class CurveOverlay(Scenario):
        
    """A scenario to overlay existing curves"""

    @camel_case_translate
    def __init__(
        self,
        dates: Tuple[datetime.date, ...] = None,
        discount_factors: Tuple[float, ...] = None,
        denominated: str = None,
        csa_term: str = None,
        tenor: str = None,
        rate_option: str = None,
        curve_type: str = None,
        subtract_base: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.dates = dates
        self.discount_factors = discount_factors
        self.denominated = denominated
        self.csa_term = csa_term
        self.tenor = tenor
        self.rate_option = rate_option
        self.curve_type = curve_type
        self.subtract_base = subtract_base
        self.name = name

    @property
    def scenario_type(self) -> str:
        """CurveOverlay"""
        return 'CurveOverlay'        

    @property
    def dates(self) -> Tuple[datetime.date, ...]:
        """ISO 8601-formatted date"""
        return self.__dates

    @dates.setter
    def dates(self, value: Tuple[datetime.date, ...]):
        self._property_changed('dates')
        self.__dates = value        

    @property
    def discount_factors(self) -> Tuple[float, ...]:
        return self.__discount_factors

    @discount_factors.setter
    def discount_factors(self, value: Tuple[float, ...]):
        self._property_changed('discount_factors')
        self.__discount_factors = value        

    @property
    def denominated(self) -> str:
        return self.__denominated

    @denominated.setter
    def denominated(self, value: str):
        self._property_changed('denominated')
        self.__denominated = value        

    @property
    def csa_term(self) -> str:
        return self.__csa_term

    @csa_term.setter
    def csa_term(self, value: str):
        self._property_changed('csa_term')
        self.__csa_term = value        

    @property
    def tenor(self) -> str:
        return self.__tenor

    @tenor.setter
    def tenor(self, value: str):
        self._property_changed('tenor')
        self.__tenor = value        

    @property
    def rate_option(self) -> str:
        return self.__rate_option

    @rate_option.setter
    def rate_option(self, value: str):
        self._property_changed('rate_option')
        self.__rate_option = value        

    @property
    def curve_type(self) -> str:
        return self.__curve_type

    @curve_type.setter
    def curve_type(self, value: str):
        self._property_changed('curve_type')
        self.__curve_type = value        

    @property
    def subtract_base(self) -> bool:
        return self.__subtract_base

    @subtract_base.setter
    def subtract_base(self, value: bool):
        self._property_changed('subtract_base')
        self.__subtract_base = value        


class DateRange(Base):
        
    @camel_case_translate
    def __init__(
        self,
        end_date: datetime.date = None,
        start_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.end_date = end_date
        self.start_date = start_date
        self.name = name

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        


class ISelectNewUnit(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        new_units: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.new_units = new_units
        self.name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def new_units(self) -> float:
        return self.__new_units

    @new_units.setter
    def new_units(self, value: float):
        self._property_changed('new_units')
        self.__new_units = value        


class ISelectNewWeight(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        new_weight: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.new_weight = new_weight
        self.name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def new_weight(self) -> float:
        return self.__new_weight

    @new_weight.setter
    def new_weight(self, value: float):
        self._property_changed('new_weight')
        self.__new_weight = value        


class Identifier(Base):
        
    @camel_case_translate
    def __init__(
        self,
        type_: str = None,
        value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.value = value
        self.name = name

    @property
    def type(self) -> str:
        """Identifier type code"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def value(self) -> str:
        """Identifier value"""
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        


class LiborFallbackScenario(Scenario):
        
    """A scenario to change the libor rate to RFR + Spread after Dec2021 in the index
       curve"""

    @camel_case_translate
    def __init__(
        self,
        date: datetime.date = None,
        fallback_type: str = 'RFR',
        discounting: bool = False,
        cash_flows: bool = True,
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.fallback_type = fallback_type
        self.discounting = discounting
        self.cash_flows = cash_flows
        self.name = name

    @property
    def scenario_type(self) -> str:
        """LiborFallbackScenario"""
        return 'LiborFallbackScenario'        

    @property
    def date(self) -> datetime.date:
        """Announce Date For the Libor Fallback"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def fallback_type(self) -> str:
        """Different Rules for Libor Fallback"""
        return self.__fallback_type

    @fallback_type.setter
    def fallback_type(self, value: str):
        self._property_changed('fallback_type')
        self.__fallback_type = value        

    @property
    def discounting(self) -> bool:
        """If True, use RFR Discounting, otherwise continue to use libor discounting"""
        return self.__discounting

    @discounting.setter
    def discounting(self, value: bool):
        self._property_changed('discounting')
        self.__discounting = value        

    @property
    def cash_flows(self) -> bool:
        """If True, use RFR + Spread when projecting cash flows, otherwise continue to use
           libor"""
        return self.__cash_flows

    @cash_flows.setter
    def cash_flows(self, value: bool):
        self._property_changed('cash_flows')
        self.__cash_flows = value        


class LiquidityReportParameters(Base):
        
    """Parameters to be used on liquidity reports"""

    @camel_case_translate
    def __init__(
        self,
        title: str = None,
        email: str = None,
        trading_desk: str = None,
        name: str = None
    ):        
        super().__init__()
        self.title = title
        self.email = email
        self.trading_desk = trading_desk
        self.name = name

    @property
    def title(self) -> str:
        """Report title"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def trading_desk(self) -> str:
        return self.__trading_desk

    @trading_desk.setter
    def trading_desk(self, value: str):
        self._property_changed('trading_desk')
        self.__trading_desk = value        


class ListOfNumberParameter(Base):
        
    """Extra parameters for List of Number"""

    @camel_case_translate
    def __init__(
        self,
        values: Tuple[float, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.values = values
        self.name = name

    @property
    def parameter_type(self) -> str:
        """ListOfNumber"""
        return 'ListOfNumber'        

    @property
    def values(self) -> Tuple[float, ...]:
        return self.__values

    @values.setter
    def values(self, value: Tuple[float, ...]):
        self._property_changed('values')
        self.__values = value        


class ListOfStringParameter(Base):
        
    """Extra parameters for List of Strings"""

    @camel_case_translate
    def __init__(
        self,
        values: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.values = values
        self.name = name

    @property
    def parameter_type(self) -> str:
        """ListOfString"""
        return 'ListOfString'        

    @property
    def values(self) -> Tuple[str, ...]:
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        


class MapParameter(Base):
        
    """Extra parameters for Map of String type"""

    @camel_case_translate
    def __init__(
        self,
        value: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.value = value
        self.name = name

    @property
    def parameter_type(self) -> str:
        """Map"""
        return 'Map'        

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: dict):
        self._property_changed('value')
        self.__value = value        


class MarketDataCoordinate(Base):
        
    """Object representation of a market data coordinate"""

    @camel_case_translate
    def __init__(
        self,
        mkt_type: str = None,
        mkt_asset: str = None,
        mkt_class: str = None,
        mkt_point: Tuple[str, ...] = None,
        mkt_quoting_style: str = None,
        name: str = None
    ):        
        super().__init__()
        self.mkt_type = mkt_type
        self.mkt_asset = mkt_asset
        self.mkt_class = mkt_class
        self.mkt_point = mkt_point
        self.mkt_quoting_style = mkt_quoting_style
        self.name = name

    @property
    def mkt_type(self) -> str:
        """The MDAPI Type, e.g. IR, IR BASIS, FX, FX Vol"""
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: str):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def mkt_asset(self) -> str:
        """The MDAPI Asset, e.g. USD, EUR-EURIBOR-Telerate, WTI"""
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: str):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def mkt_class(self) -> str:
        """The MDAPI Class, e.g. Swap, Cash."""
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: str):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def mkt_point(self) -> Tuple[str, ...]:
        """The MDAPI Point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__mkt_point

    @mkt_point.setter
    def mkt_point(self, value: Tuple[str, ...]):
        self._property_changed('mkt_point')
        self.__mkt_point = value        

    @property
    def mkt_quoting_style(self) -> str:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: str):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        


class MarketDataVolSlice(Base):
        
    """A volatility slice"""

    @camel_case_translate
    def __init__(
        self,
        date: datetime.date,
        strikes: Tuple[float, ...],
        levels: Tuple[float, ...],
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.strikes = strikes
        self.levels = levels
        self.name = name

    @property
    def date(self) -> datetime.date:
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def strikes(self) -> Tuple[float, ...]:
        """list of vol strikes"""
        return self.__strikes

    @strikes.setter
    def strikes(self, value: Tuple[float, ...]):
        self._property_changed('strikes')
        self.__strikes = value        

    @property
    def levels(self) -> Tuple[float, ...]:
        """list of vol levels"""
        return self.__levels

    @levels.setter
    def levels(self, value: Tuple[float, ...]):
        self._property_changed('levels')
        self.__levels = value        


class Op(Base):
        
    """Operations for searches."""

    @camel_case_translate
    def __init__(
        self,
        gte: Union[datetime.date, float] = None,
        lte: Union[datetime.date, float] = None,
        lt: Union[datetime.date, float] = None,
        gt: Union[datetime.date, float] = None,
        name: str = None
    ):        
        super().__init__()
        self.gte = gte
        self.lte = lte
        self.lt = lt
        self.gt = gt
        self.name = name

    @property
    def gte(self) -> Union[datetime.date, float]:
        """search for values greater than or equal."""
        return self.__gte

    @gte.setter
    def gte(self, value: Union[datetime.date, float]):
        self._property_changed('gte')
        self.__gte = value        

    @property
    def lte(self) -> Union[datetime.date, float]:
        """search for values less than or equal to."""
        return self.__lte

    @lte.setter
    def lte(self, value: Union[datetime.date, float]):
        self._property_changed('lte')
        self.__lte = value        

    @property
    def lt(self) -> Union[datetime.date, float]:
        """search for values less than."""
        return self.__lt

    @lt.setter
    def lt(self, value: Union[datetime.date, float]):
        self._property_changed('lt')
        self.__lt = value        

    @property
    def gt(self) -> Union[datetime.date, float]:
        """search for values greater than."""
        return self.__gt

    @gt.setter
    def gt(self, value: Union[datetime.date, float]):
        self._property_changed('gt')
        self.__gt = value        


class PCOBenchmarkOptions(Base):
        
    """Parameters required for PCO Benchmark"""

    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        target_ratio: str = None
    ):        
        super().__init__()
        self.name = name
        self.target_ratio = target_ratio

    @property
    def name(self) -> str:
        """Benchmark name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def target_ratio(self) -> str:
        return self.__target_ratio

    @target_ratio.setter
    def target_ratio(self, value: str):
        self._property_changed('target_ratio')
        self.__target_ratio = value        


class PCOExposureAdjustments(Base):
        
    """Parameters required for PCO Exposure Adjustments"""

    @camel_case_translate
    def __init__(
        self,
        nav_adjustment: str = None,
        net_subscription_redemption: str = None,
        net_subscription_redemption_limits: Tuple[str, ...] = None,
        adjustment_vs_subscription_redemption: str = None,
        adjustment_vs_subscription_redemption_limits: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.nav_adjustment = nav_adjustment
        self.net_subscription_redemption = net_subscription_redemption
        self.net_subscription_redemption_limits = net_subscription_redemption_limits
        self.adjustment_vs_subscription_redemption = adjustment_vs_subscription_redemption
        self.adjustment_vs_subscription_redemption_limits = adjustment_vs_subscription_redemption_limits
        self.name = name

    @property
    def nav_adjustment(self) -> str:
        return self.__nav_adjustment

    @nav_adjustment.setter
    def nav_adjustment(self, value: str):
        self._property_changed('nav_adjustment')
        self.__nav_adjustment = value        

    @property
    def net_subscription_redemption(self) -> str:
        """net subscription and redemption"""
        return self.__net_subscription_redemption

    @net_subscription_redemption.setter
    def net_subscription_redemption(self, value: str):
        self._property_changed('net_subscription_redemption')
        self.__net_subscription_redemption = value        

    @property
    def net_subscription_redemption_limits(self) -> Tuple[str, ...]:
        """Upper and lower limit of subscription and redemption adjustment"""
        return self.__net_subscription_redemption_limits

    @net_subscription_redemption_limits.setter
    def net_subscription_redemption_limits(self, value: Tuple[str, ...]):
        self._property_changed('net_subscription_redemption_limits')
        self.__net_subscription_redemption_limits = value        

    @property
    def adjustment_vs_subscription_redemption(self) -> str:
        """subscription and redemption adjustment"""
        return self.__adjustment_vs_subscription_redemption

    @adjustment_vs_subscription_redemption.setter
    def adjustment_vs_subscription_redemption(self, value: str):
        self._property_changed('adjustment_vs_subscription_redemption')
        self.__adjustment_vs_subscription_redemption = value        

    @property
    def adjustment_vs_subscription_redemption_limits(self) -> Tuple[str, ...]:
        """Upper and lower limit of subscription and redemption adjustment"""
        return self.__adjustment_vs_subscription_redemption_limits

    @adjustment_vs_subscription_redemption_limits.setter
    def adjustment_vs_subscription_redemption_limits(self, value: Tuple[str, ...]):
        self._property_changed('adjustment_vs_subscription_redemption_limits')
        self.__adjustment_vs_subscription_redemption_limits = value        


class PCOMtMHistoricalData(Base):
        
    """Parameters required for PCO Unrealised Mark to Market Historical Data"""

    @camel_case_translate
    def __init__(
        self,
        value: str = None,
        timestamp: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.value = value
        self.timestamp = timestamp
        self.name = name

    @property
    def value(self) -> str:
        """Indicative unrealised mark to market value"""
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        

    @property
    def timestamp(self) -> datetime.datetime:
        """Timestamp of unrealised mark to market of open trade for a currency"""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        self._property_changed('timestamp')
        self.__timestamp = value        


class PCONetSubscription(Base):
        
    """Parameters required for PCO  Net Subscription Data"""

    @camel_case_translate
    def __init__(
        self,
        confirmed: str = None,
        estimated: str = None,
        id_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.confirmed = confirmed
        self.estimated = estimated
        self.__id = id_
        self.name = name

    @property
    def confirmed(self) -> str:
        """Confirmed net subscription provided by client for a share class"""
        return self.__confirmed

    @confirmed.setter
    def confirmed(self, value: str):
        self._property_changed('confirmed')
        self.__confirmed = value        

    @property
    def estimated(self) -> str:
        """Estimated net subscription provided by client for a share class"""
        return self.__estimated

    @estimated.setter
    def estimated(self, value: str):
        self._property_changed('estimated')
        self.__estimated = value        

    @property
    def id(self) -> str:
        """Id for the net subscription set"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        


class PCOSettlementsData(Base):
        
    """Parameters required for a PCO Settlement"""

    @camel_case_translate
    def __init__(
        self,
        timestamp: datetime.datetime = None,
        settlement: str = None,
        name: str = None
    ):        
        super().__init__()
        self.timestamp = timestamp
        self.settlement = settlement
        self.name = name

    @property
    def timestamp(self) -> datetime.datetime:
        """Timestamp of settlement"""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        self._property_changed('timestamp')
        self.__timestamp = value        

    @property
    def settlement(self) -> str:
        """Settlement value"""
        return self.__settlement

    @settlement.setter
    def settlement(self, value: str):
        self._property_changed('settlement')
        self.__settlement = value        


class PCOTargetDeviationData(Base):
        
    """Parameters required for a Target Deviation data"""

    @camel_case_translate
    def __init__(
        self,
        value: str = None,
        timestamp: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.value = value
        self.timestamp = timestamp
        self.name = name

    @property
    def value(self) -> str:
        """Target deviation  value"""
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        

    @property
    def timestamp(self) -> datetime.datetime:
        """Timestamp"""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        self._property_changed('timestamp')
        self.__timestamp = value        


class PerformanceStats(Base):
        
    """Performance statistics."""

    @camel_case_translate
    def __init__(
        self,
        alpha: float = None,
        annualized_return: float = None,
        annualized_volatility: float = None,
        average_return: float = None,
        average_value: float = None,
        average_volume_last_month: float = None,
        best_month: float = None,
        best_month_date: datetime.date = None,
        beta: float = None,
        close_price: float = None,
        correlation: float = None,
        cumulative_return: float = None,
        current_value: float = None,
        drawdown_over_return: float = None,
        high: float = None,
        high_eod: float = None,
        last_change: float = None,
        last_change_pct: float = None,
        last_date: datetime.date = None,
        last_value: float = None,
        low: float = None,
        low_eod: float = None,
        max_draw_down: float = None,
        max_draw_down_duration: int = None,
        open_price: float = None,
        positive_months: float = None,
        sharpe_ratio: float = None,
        sortino_ratio: float = None,
        worst_month: float = None,
        worst_month_date: datetime.date = None,
        total_return: float = None,
        volume: float = None,
        name: str = None
    ):        
        super().__init__()
        self.alpha = alpha
        self.annualized_return = annualized_return
        self.annualized_volatility = annualized_volatility
        self.average_return = average_return
        self.average_value = average_value
        self.average_volume_last_month = average_volume_last_month
        self.best_month = best_month
        self.best_month_date = best_month_date
        self.beta = beta
        self.close_price = close_price
        self.correlation = correlation
        self.cumulative_return = cumulative_return
        self.current_value = current_value
        self.drawdown_over_return = drawdown_over_return
        self.high = high
        self.high_eod = high_eod
        self.last_change = last_change
        self.last_change_pct = last_change_pct
        self.last_date = last_date
        self.last_value = last_value
        self.low = low
        self.low_eod = low_eod
        self.max_draw_down = max_draw_down
        self.max_draw_down_duration = max_draw_down_duration
        self.open_price = open_price
        self.positive_months = positive_months
        self.sharpe_ratio = sharpe_ratio
        self.sortino_ratio = sortino_ratio
        self.worst_month = worst_month
        self.worst_month_date = worst_month_date
        self.total_return = total_return
        self.volume = volume
        self.name = name

    @property
    def alpha(self) -> float:
        """Measure of performance compared to a market benchmark."""
        return self.__alpha

    @alpha.setter
    def alpha(self, value: float):
        self._property_changed('alpha')
        self.__alpha = value        

    @property
    def annualized_return(self) -> float:
        """Compounded Annual Growth Rate (CAGR)."""
        return self.__annualized_return

    @annualized_return.setter
    def annualized_return(self, value: float):
        self._property_changed('annualized_return')
        self.__annualized_return = value        

    @property
    def annualized_volatility(self) -> float:
        """Standard deviation of daily returns, annualized."""
        return self.__annualized_volatility

    @annualized_volatility.setter
    def annualized_volatility(self, value: float):
        self._property_changed('annualized_volatility')
        self.__annualized_volatility = value        

    @property
    def average_return(self) -> float:
        """Average of the performance returns."""
        return self.__average_return

    @average_return.setter
    def average_return(self, value: float):
        self._property_changed('average_return')
        self.__average_return = value        

    @property
    def average_value(self) -> float:
        """Average value."""
        return self.__average_value

    @average_value.setter
    def average_value(self, value: float):
        self._property_changed('average_value')
        self.__average_value = value        

    @property
    def average_volume_last_month(self) -> float:
        """30 day average volume."""
        return self.__average_volume_last_month

    @average_volume_last_month.setter
    def average_volume_last_month(self, value: float):
        self._property_changed('average_volume_last_month')
        self.__average_volume_last_month = value        

    @property
    def best_month(self) -> float:
        """Best monthly return (first to last day of month)."""
        return self.__best_month

    @best_month.setter
    def best_month(self, value: float):
        self._property_changed('best_month')
        self.__best_month = value        

    @property
    def best_month_date(self) -> datetime.date:
        """Best monthly return date (first to last day of month)."""
        return self.__best_month_date

    @best_month_date.setter
    def best_month_date(self, value: datetime.date):
        self._property_changed('best_month_date')
        self.__best_month_date = value        

    @property
    def beta(self) -> float:
        """Measure of volatility compared to a market benchmark."""
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self._property_changed('beta')
        self.__beta = value        

    @property
    def close_price(self) -> float:
        """previous close price."""
        return self.__close_price

    @close_price.setter
    def close_price(self, value: float):
        self._property_changed('close_price')
        self.__close_price = value        

    @property
    def correlation(self) -> float:
        """Pearson correlation."""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self._property_changed('correlation')
        self.__correlation = value        

    @property
    def cumulative_return(self) -> float:
        """Cumulative monthly returns."""
        return self.__cumulative_return

    @cumulative_return.setter
    def cumulative_return(self, value: float):
        self._property_changed('cumulative_return')
        self.__cumulative_return = value        

    @property
    def current_value(self) -> float:
        """Current value."""
        return self.__current_value

    @current_value.setter
    def current_value(self, value: float):
        self._property_changed('current_value')
        self.__current_value = value        

    @property
    def drawdown_over_return(self) -> float:
        """Maximum drawdown divided by annualized return."""
        return self.__drawdown_over_return

    @drawdown_over_return.setter
    def drawdown_over_return(self, value: float):
        self._property_changed('drawdown_over_return')
        self.__drawdown_over_return = value        

    @property
    def high(self) -> float:
        """Highest real time price for the previous 24 hours."""
        return self.__high

    @high.setter
    def high(self, value: float):
        self._property_changed('high')
        self.__high = value        

    @property
    def high_eod(self) -> float:
        """Highest end of day price."""
        return self.__high_eod

    @high_eod.setter
    def high_eod(self, value: float):
        self._property_changed('high_eod')
        self.__high_eod = value        

    @property
    def last_change(self) -> float:
        """Last published value."""
        return self.__last_change

    @last_change.setter
    def last_change(self, value: float):
        self._property_changed('last_change')
        self.__last_change = value        

    @property
    def last_change_pct(self) -> float:
        """Last change in percent."""
        return self.__last_change_pct

    @last_change_pct.setter
    def last_change_pct(self, value: float):
        self._property_changed('last_change_pct')
        self.__last_change_pct = value        

    @property
    def last_date(self) -> datetime.date:
        """Last publication date."""
        return self.__last_date

    @last_date.setter
    def last_date(self, value: datetime.date):
        self._property_changed('last_date')
        self.__last_date = value        

    @property
    def last_value(self) -> float:
        """Last published value."""
        return self.__last_value

    @last_value.setter
    def last_value(self, value: float):
        self._property_changed('last_value')
        self.__last_value = value        

    @property
    def low(self) -> float:
        """Lowest real time price for the previous 24 hours."""
        return self.__low

    @low.setter
    def low(self, value: float):
        self._property_changed('low')
        self.__low = value        

    @property
    def low_eod(self) -> float:
        """Lowest end of day price."""
        return self.__low_eod

    @low_eod.setter
    def low_eod(self, value: float):
        self._property_changed('low_eod')
        self.__low_eod = value        

    @property
    def max_draw_down(self) -> float:
        """Maximum peak to trough percentage drawdown."""
        return self.__max_draw_down

    @max_draw_down.setter
    def max_draw_down(self, value: float):
        self._property_changed('max_draw_down')
        self.__max_draw_down = value        

    @property
    def max_draw_down_duration(self) -> int:
        """Amount of time in days between beginning and end of drawdown."""
        return self.__max_draw_down_duration

    @max_draw_down_duration.setter
    def max_draw_down_duration(self, value: int):
        self._property_changed('max_draw_down_duration')
        self.__max_draw_down_duration = value        

    @property
    def open_price(self) -> float:
        """Open price."""
        return self.__open_price

    @open_price.setter
    def open_price(self, value: float):
        self._property_changed('open_price')
        self.__open_price = value        

    @property
    def positive_months(self) -> float:
        """Percentage of months that performed positively."""
        return self.__positive_months

    @positive_months.setter
    def positive_months(self, value: float):
        self._property_changed('positive_months')
        self.__positive_months = value        

    @property
    def sharpe_ratio(self) -> float:
        """Annualized return of the series minus risk free rate (accrued daily) divided by
           annual volatility."""
        return self.__sharpe_ratio

    @sharpe_ratio.setter
    def sharpe_ratio(self, value: float):
        self._property_changed('sharpe_ratio')
        self.__sharpe_ratio = value        

    @property
    def sortino_ratio(self) -> float:
        """Annualized return of the series minus risk free rate (accrued daily) divided by
           annual volatility of negative returns."""
        return self.__sortino_ratio

    @sortino_ratio.setter
    def sortino_ratio(self, value: float):
        self._property_changed('sortino_ratio')
        self.__sortino_ratio = value        

    @property
    def worst_month(self) -> float:
        """Worst monthly return (first to last day of month)."""
        return self.__worst_month

    @worst_month.setter
    def worst_month(self, value: float):
        self._property_changed('worst_month')
        self.__worst_month = value        

    @property
    def worst_month_date(self) -> datetime.date:
        """Worst monthly return date (first to last day of month)."""
        return self.__worst_month_date

    @worst_month_date.setter
    def worst_month_date(self, value: datetime.date):
        self._property_changed('worst_month_date')
        self.__worst_month_date = value        

    @property
    def total_return(self) -> float:
        """Total return."""
        return self.__total_return

    @total_return.setter
    def total_return(self, value: float):
        self._property_changed('total_return')
        self.__total_return = value        

    @property
    def volume(self) -> float:
        """volume."""
        return self.__volume

    @volume.setter
    def volume(self, value: float):
        self._property_changed('volume')
        self.__volume = value        


class PositionTag(Base):
        
    """Tag name and value associated with a portfolio position."""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        value: str
    ):        
        super().__init__()
        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        """Tag name."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def value(self) -> str:
        """Tag value."""
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        


class RefMarket(Base):
        
    """Reference to a market"""

    @camel_case_translate
    def __init__(
        self,
        market_ref: str = None,
        name: str = None
    ):        
        super().__init__()
        self.market_ref = market_ref
        self.name = name

    @property
    def market_type(self) -> str:
        """RefMarket"""
        return 'RefMarket'        

    @property
    def market_ref(self) -> str:
        """Market Reference"""
        return self.__market_ref

    @market_ref.setter
    def market_ref(self, value: str):
        self._property_changed('market_ref')
        self.__market_ref = value        


class RiskRequestParameters(Base):
        
    """Parameters for the risk request"""

    @camel_case_translate
    def __init__(
        self,
        csa_term: str = None,
        raw_results: bool = False,
        use_historical_diddles_only: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.csa_term = csa_term
        self.raw_results = raw_results
        self.use_historical_diddles_only = use_historical_diddles_only
        self.name = name

    @property
    def csa_term(self) -> str:
        """The CSA Term for CSA specific discounting, e.g. EUR-1"""
        return self.__csa_term

    @csa_term.setter
    def csa_term(self, value: str):
        self._property_changed('csa_term')
        self.__csa_term = value        

    @property
    def raw_results(self) -> bool:
        return self.__raw_results

    @raw_results.setter
    def raw_results(self, value: bool):
        self._property_changed('raw_results')
        self.__raw_results = value        

    @property
    def use_historical_diddles_only(self) -> bool:
        """Enables a backward compatible pricing mode"""
        return self.__use_historical_diddles_only

    @use_historical_diddles_only.setter
    def use_historical_diddles_only(self, value: bool):
        self._property_changed('use_historical_diddles_only')
        self.__use_historical_diddles_only = value        


class SimpleParty(Base):
        
    @camel_case_translate
    def __init__(
        self,
        party_type: str = None,
        party_name: str = None,
        party_book: str = None,
        name: str = None
    ):        
        super().__init__()
        self.party_type = party_type
        self.party_name = party_name
        self.party_book = party_book
        self.name = name

    @property
    def party_type(self) -> str:
        return self.__party_type

    @party_type.setter
    def party_type(self, value: str):
        self._property_changed('party_type')
        self.__party_type = value        

    @property
    def party_name(self) -> str:
        return self.__party_name

    @party_name.setter
    def party_name(self, value: str):
        self._property_changed('party_name')
        self.__party_name = value        

    @property
    def party_book(self) -> str:
        return self.__party_book

    @party_book.setter
    def party_book(self, value: str):
        self._property_changed('party_book')
        self.__party_book = value        


class SocialDomain(Base):
        
    @camel_case_translate
    def __init__(
        self,
        onboarded: dict,
        returns_enabled: bool = None,
        auto_approve_connections: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.onboarded = onboarded
        self.returns_enabled = returns_enabled
        self.auto_approve_connections = auto_approve_connections
        self.name = name

    @property
    def onboarded(self) -> dict:
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: dict):
        self._property_changed('onboarded')
        self.__onboarded = value        

    @property
    def returns_enabled(self) -> bool:
        """True if the fund has returns enabled"""
        return self.__returns_enabled

    @returns_enabled.setter
    def returns_enabled(self, value: bool):
        self._property_changed('returns_enabled')
        self.__returns_enabled = value        

    @property
    def auto_approve_connections(self) -> bool:
        """True if the fund auto approves connection requests"""
        return self.__auto_approve_connections

    @auto_approve_connections.setter
    def auto_approve_connections(self, value: bool):
        self._property_changed('auto_approve_connections')
        self.__auto_approve_connections = value        


class StringParameter(Base):
        
    """Extra parameters for String"""

    @camel_case_translate
    def __init__(
        self,
        value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.value = value
        self.name = name

    @property
    def parameter_type(self) -> str:
        """String"""
        return 'String'        

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        


class TimeFilter(Base):
        
    """Filter to restrict data to a range of hours per day."""

    @camel_case_translate
    def __init__(
        self,
        start_hours: str,
        end_hours: str,
        time_zone: str,
        name: str = None
    ):        
        super().__init__()
        self.start_hours = start_hours
        self.end_hours = end_hours
        self.time_zone = time_zone
        self.name = name

    @property
    def start_hours(self) -> str:
        """Start hours in the format HH::MM::SS after which the data will be shown. Data is
           inclusive of the startHours value."""
        return self.__start_hours

    @start_hours.setter
    def start_hours(self, value: str):
        self._property_changed('start_hours')
        self.__start_hours = value        

    @property
    def end_hours(self) -> str:
        """End hours in the format HH::MM::SS up to which the data will be shown. Data is
           exclusive of the endHours value with a precision of 1 second."""
        return self.__end_hours

    @end_hours.setter
    def end_hours(self, value: str):
        self._property_changed('end_hours')
        self.__end_hours = value        

    @property
    def time_zone(self) -> str:
        """The time zone with respect to which the start and end hours will be applied
           (must be a valid IANA TimeZone identifier)."""
        return self.__time_zone

    @time_zone.setter
    def time_zone(self, value: str):
        self._property_changed('time_zone')
        self.__time_zone = value        


class UserCoverage(Base):
        
    """Sales coverage for user"""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        email: str,
        app: str = None,
        phone: str = None,
        guid: str = None
    ):        
        super().__init__()
        self.app = app
        self.phone = phone
        self.name = name
        self.email = email
        self.guid = guid

    @property
    def app(self) -> str:
        """Marquee application covered by sales person"""
        return self.__app

    @app.setter
    def app(self, value: str):
        self._property_changed('app')
        self.__app = value        

    @property
    def phone(self) -> str:
        """Coverage phone number"""
        return self.__phone

    @phone.setter
    def phone(self, value: str):
        self._property_changed('phone')
        self.__phone = value        

    @property
    def name(self) -> str:
        """Coverage name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def email(self) -> str:
        """Coverage email"""
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def guid(self) -> str:
        """Coverage guid"""
        return self.__guid

    @guid.setter
    def guid(self, value: str):
        self._property_changed('guid')
        self.__guid = value        


class WeightedPosition(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        weight: float,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.weight = weight
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique identifier"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def weight(self) -> float:
        """Relative net weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        


class XRef(Priceable):
        
    @camel_case_translate
    def __init__(
        self,
        ric: str = None,
        rcic: str = None,
        eid: str = None,
        gsideid: str = None,
        gsid: str = None,
        gsid_equivalent: str = None,
        cid: str = None,
        bbid: str = None,
        bcid: str = None,
        delisted: str = None,
        bbid_equivalent: str = None,
        cusip: str = None,
        gss: str = None,
        isin: str = None,
        jsn: str = None,
        prime_id: str = None,
        sedol: str = None,
        ticker: str = None,
        valoren: str = None,
        wpk: str = None,
        gsn: str = None,
        sec_name: str = None,
        cross: str = None,
        simon_id: str = None,
        em_id: str = None,
        cm_id: str = None,
        lms_id: str = None,
        tdapi: str = None,
        mdapi: str = None,
        mdapi_class: str = None,
        mic: str = None,
        sf_id: str = None,
        dollar_cross: str = None,
        mq_symbol: str = None,
        primary_country_ric: str = None,
        pnode_id: str = None,
        wi_id: str = None,
        ps_id: str = None,
        pl_id: str = None,
        exchange_code: str = None,
        plot_id: str = None,
        cins: str = None,
        bbgid: str = None,
        display_id: str = None,
        tsdb_shortname: str = None,
        name: str = None
    ):        
        super().__init__()
        self.ric = ric
        self.rcic = rcic
        self.eid = eid
        self.gsideid = gsideid
        self.gsid = gsid
        self.gsid_equivalent = gsid_equivalent
        self.cid = cid
        self.bbid = bbid
        self.bcid = bcid
        self.delisted = delisted
        self.bbid_equivalent = bbid_equivalent
        self.cusip = cusip
        self.gss = gss
        self.isin = isin
        self.jsn = jsn
        self.prime_id = prime_id
        self.sedol = sedol
        self.ticker = ticker
        self.valoren = valoren
        self.wpk = wpk
        self.gsn = gsn
        self.sec_name = sec_name
        self.cross = cross
        self.simon_id = simon_id
        self.em_id = em_id
        self.cm_id = cm_id
        self.lms_id = lms_id
        self.tdapi = tdapi
        self.mdapi = mdapi
        self.mdapi_class = mdapi_class
        self.mic = mic
        self.sf_id = sf_id
        self.dollar_cross = dollar_cross
        self.mq_symbol = mq_symbol
        self.primary_country_ric = primary_country_ric
        self.pnode_id = pnode_id
        self.wi_id = wi_id
        self.ps_id = ps_id
        self.pl_id = pl_id
        self.exchange_code = exchange_code
        self.plot_id = plot_id
        self.cins = cins
        self.bbgid = bbgid
        self.display_id = display_id
        self.tsdb_shortname = tsdb_shortname
        self.name = name

    @property
    def ric(self) -> str:
        """Reuters Instrument Code identifier"""
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def rcic(self) -> str:
        """Reuters Composite Instrument Code Identifier"""
        return self.__rcic

    @rcic.setter
    def rcic(self, value: str):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def eid(self) -> str:
        """EID Identifier"""
        return self.__eid

    @eid.setter
    def eid(self, value: str):
        self._property_changed('eid')
        self.__eid = value        

    @property
    def gsideid(self) -> str:
        """GSID_EID Identifier"""
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: str):
        self._property_changed('gsideid')
        self.__gsideid = value        

    @property
    def gsid(self) -> str:
        """GSID Identifier"""
        return self.__gsid

    @gsid.setter
    def gsid(self, value: str):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def gsid_equivalent(self) -> str:
        """GSID Equivalent Identifier"""
        return self.__gsid_equivalent

    @gsid_equivalent.setter
    def gsid_equivalent(self, value: str):
        self._property_changed('gsid_equivalent')
        self.__gsid_equivalent = value        

    @property
    def cid(self) -> str:
        """Company Id Identifier"""
        return self.__cid

    @cid.setter
    def cid(self, value: str):
        self._property_changed('cid')
        self.__cid = value        

    @property
    def bbid(self) -> str:
        """Bloomberg Id Identifier"""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def bcid(self) -> str:
        """Bloomberg Composite Identifier"""
        return self.__bcid

    @bcid.setter
    def bcid(self, value: str):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def delisted(self) -> str:
        """Whether an asset has been delisted"""
        return self.__delisted

    @delisted.setter
    def delisted(self, value: str):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def bbid_equivalent(self) -> str:
        """Bloomberg Equivalent Identifier"""
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: str):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def cusip(self) -> str:
        """Cusip Identifier"""
        return self.__cusip

    @cusip.setter
    def cusip(self, value: str):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def gss(self) -> str:
        """GS Symbol identifier"""
        return self.__gss

    @gss.setter
    def gss(self, value: str):
        self._property_changed('gss')
        self.__gss = value        

    @property
    def isin(self) -> str:
        """International Security Number"""
        return self.__isin

    @isin.setter
    def isin(self, value: str):
        self._property_changed('isin')
        self.__isin = value        

    @property
    def jsn(self) -> str:
        """Japan Security Number"""
        return self.__jsn

    @jsn.setter
    def jsn(self, value: str):
        self._property_changed('jsn')
        self.__jsn = value        

    @property
    def prime_id(self) -> str:
        """PrimeID Identifier"""
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: str):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def sedol(self) -> str:
        """Sedol Identifier"""
        return self.__sedol

    @sedol.setter
    def sedol(self, value: str):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def ticker(self) -> str:
        """Ticker Identifier"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def valoren(self) -> str:
        """Valoren Identifier"""
        return self.__valoren

    @valoren.setter
    def valoren(self, value: str):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def wpk(self) -> str:
        """Wertpapier Kenn-Nummer"""
        return self.__wpk

    @wpk.setter
    def wpk(self, value: str):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def gsn(self) -> str:
        """Goldman Sachs internal product number"""
        return self.__gsn

    @gsn.setter
    def gsn(self, value: str):
        self._property_changed('gsn')
        self.__gsn = value        

    @property
    def sec_name(self) -> str:
        """Internal Goldman Sachs security name"""
        return self.__sec_name

    @sec_name.setter
    def sec_name(self, value: str):
        self._property_changed('sec_name')
        self.__sec_name = value        

    @property
    def cross(self) -> str:
        """Cross identifier"""
        return self.__cross

    @cross.setter
    def cross(self, value: str):
        self._property_changed('cross')
        self.__cross = value        

    @property
    def simon_id(self) -> str:
        """SIMON product identifier"""
        return self.__simon_id

    @simon_id.setter
    def simon_id(self, value: str):
        self._property_changed('simon_id')
        self.__simon_id = value        

    @property
    def em_id(self) -> str:
        """Entity Master Identifier"""
        return self.__em_id

    @em_id.setter
    def em_id(self, value: str):
        self._property_changed('em_id')
        self.__em_id = value        

    @property
    def cm_id(self) -> str:
        """Client Master Party Id"""
        return self.__cm_id

    @cm_id.setter
    def cm_id(self, value: str):
        self._property_changed('cm_id')
        self.__cm_id = value        

    @property
    def lms_id(self) -> str:
        """Listed Market Symbol"""
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: str):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def tdapi(self) -> str:
        """TDAPI Description"""
        return self.__tdapi

    @tdapi.setter
    def tdapi(self, value: str):
        self._property_changed('tdapi')
        self.__tdapi = value        

    @property
    def mdapi(self) -> str:
        """MDAPI Asset"""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: str):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def mdapi_class(self) -> str:
        """MDAPI Asset Class"""
        return self.__mdapi_class

    @mdapi_class.setter
    def mdapi_class(self, value: str):
        self._property_changed('mdapi_class')
        self.__mdapi_class = value        

    @property
    def mic(self) -> str:
        """Market Identifier Code"""
        return self.__mic

    @mic.setter
    def mic(self, value: str):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def sf_id(self) -> str:
        """SalesForce ID"""
        return self.__sf_id

    @sf_id.setter
    def sf_id(self, value: str):
        self._property_changed('sf_id')
        self.__sf_id = value        

    @property
    def dollar_cross(self) -> str:
        """USD cross identifier for a particular currency"""
        return self.__dollar_cross

    @dollar_cross.setter
    def dollar_cross(self, value: str):
        self._property_changed('dollar_cross')
        self.__dollar_cross = value        

    @property
    def mq_symbol(self) -> str:
        """Marquee Symbol for generic MQ entities"""
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: str):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def primary_country_ric(self) -> str:
        """Reuters Primary Country Instrument Code Identifier"""
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: str):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def pnode_id(self) -> str:
        """Pricing node identifier sourced from Morningstar"""
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: str):
        self._property_changed('pnode_id')
        self.__pnode_id = value        

    @property
    def wi_id(self) -> str:
        """Weather Index Identifier"""
        return self.__wi_id

    @wi_id.setter
    def wi_id(self, value: str):
        self._property_changed('wi_id')
        self.__wi_id = value        

    @property
    def ps_id(self) -> str:
        """Platts Symbol"""
        return self.__ps_id

    @ps_id.setter
    def ps_id(self, value: str):
        self._property_changed('ps_id')
        self.__ps_id = value        

    @property
    def pl_id(self) -> str:
        """Platts Symbol Name"""
        return self.__pl_id

    @pl_id.setter
    def pl_id(self, value: str):
        self._property_changed('pl_id')
        self.__pl_id = value        

    @property
    def exchange_code(self) -> str:
        """EEX Exchange Code"""
        return self.__exchange_code

    @exchange_code.setter
    def exchange_code(self, value: str):
        self._property_changed('exchange_code')
        self.__exchange_code = value        

    @property
    def plot_id(self) -> str:
        """Plot Identifier"""
        return self.__plot_id

    @plot_id.setter
    def plot_id(self, value: str):
        self._property_changed('plot_id')
        self.__plot_id = value        

    @property
    def cins(self) -> str:
        """Cins Identifier"""
        return self.__cins

    @cins.setter
    def cins(self, value: str):
        self._property_changed('cins')
        self.__cins = value        

    @property
    def bbgid(self) -> str:
        """Bloomberg Global Identifier"""
        return self.__bbgid

    @bbgid.setter
    def bbgid(self, value: str):
        self._property_changed('bbgid')
        self.__bbgid = value        

    @property
    def display_id(self) -> str:
        """Non-unique human readable identifier for assets."""
        return self.__display_id

    @display_id.setter
    def display_id(self, value: str):
        self._property_changed('display_id')
        self.__display_id = value        

    @property
    def tsdb_shortname(self) -> str:
        """Short name for symbol as used to plot data in Plottool."""
        return self.__tsdb_shortname

    @tsdb_shortname.setter
    def tsdb_shortname(self, value: str):
        self._property_changed('tsdb_shortname')
        self.__tsdb_shortname = value        


class AssetParameters(Base):
        
    """Parameters specific to the asset type"""

    @camel_case_translate
    def __init__(
        self,
        basket_type: str = None,
        style: str = None,
        index_calculation_type: str = None,
        index_return_type: str = None,
        index_divisor: float = None,
        currency: Union[Currency, str] = None,
        quote_currency: Union[Currency, str] = None,
        index_initial_price: float = None,
        initial_pricing_date: datetime.date = None,
        expiration_date: datetime.date = None,
        expiration_location: str = None,
        option_style: str = None,
        option_type: Union[OptionType, str] = None,
        settlement_date: datetime.date = None,
        settlement_type: str = None,
        strike_price: Union[float, str] = None,
        put_currency: Union[Currency, str] = None,
        put_amount: float = None,
        automatic_exercise: bool = None,
        call_amount: float = None,
        call_currency: Union[Currency, str] = None,
        exercise_time: str = None,
        multiplier: float = None,
        premium_payment_date: datetime.date = None,
        premium: float = None,
        premium_currency: Union[Currency, str] = None,
        callable_: bool = None,
        puttable: bool = None,
        perpetual: bool = None,
        seniority: str = None,
        coupon_type: str = None,
        index: str = None,
        index_term: str = None,
        index_margin: float = None,
        coupon: float = None,
        issue_date: datetime.date = None,
        issuer: str = None,
        issuer_country_code: str = None,
        issuer_type: str = None,
        issue_size: float = None,
        commodity_sector: Union[CommoditySector, str] = None,
        pricing_location: Union[PricingLocation, str] = None,
        contract_months: Tuple[str, ...] = None,
        g10_currency: bool = None,
        portfolio_id: str = None,
        hedge_id: str = None,
        ultimate_ticker: str = None,
        strategy: Union[Strategy, str] = None,
        exchange_currency: Union[Currency, str] = None,
        region: str = None,
        delivery_point: str = None,
        pricing_index: str = None,
        common_code: str = None,
        issuer_id: str = None,
        contract_month: str = None,
        bloomberg_collateral_classification: str = None,
        load_type: str = None,
        contract_unit: str = None,
        index_approval_ids: Tuple[str, ...] = None,
        is_pair_basket: bool = None,
        is_legacy_pair_basket: bool = None,
        fixed_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        floating_rate_day_count_fraction: Union[DayCountFraction, str] = None,
        pair_calculation: str = None,
        pay_day_count_fraction: Union[DayCountFraction, str] = None,
        receive_day_count_fraction: Union[DayCountFraction, str] = None,
        pay_frequency: str = None,
        receive_frequency: str = None,
        resettable_leg: Union[PayReceive, str] = None,
        inflation_lag: str = None,
        fx_index: str = None,
        index_notes: str = None,
        index_not_trading_reasons: Union[IndexNotTradingReasons, str] = None,
        trade_as: str = None,
        clone_parent_id: str = None,
        on_behalf_of: str = None,
        index_calculation_agent: str = None,
        product_type: Union[ProductType, str] = None,
        vendor: str = None,
        call_first_date: datetime.date = None,
        call_last_date: datetime.date = None,
        amount_outstanding: float = None,
        covered_bond: bool = None,
        issue_status: str = None,
        issue_status_date: datetime.date = None,
        issue_price: float = None,
        sinkable: bool = None,
        sink_factor: float = None,
        accrued_interest_standard: float = None,
        redemption_date: datetime.date = None,
        redemption_price: float = None,
        redemption_amount: float = None,
        redemption_percent: float = None,
        private_placement_type: str = None,
        minimum_piece: float = None,
        minimum_increment: float = None,
        next_coupon_payment: datetime.date = None,
        minimum_denomination: float = None,
        default_backcast: bool = None,
        index_precision: float = None,
        official_side: Union[Side, str] = None,
        credit_index_series: str = None,
        reference_entity: str = None,
        restructuring_type: str = None,
        underlying_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.basket_type = basket_type
        self.style = style
        self.index_calculation_type = index_calculation_type
        self.index_return_type = index_return_type
        self.index_divisor = index_divisor
        self.currency = currency
        self.quote_currency = quote_currency
        self.index_initial_price = index_initial_price
        self.initial_pricing_date = initial_pricing_date
        self.expiration_date = expiration_date
        self.expiration_location = expiration_location
        self.option_style = option_style
        self.option_type = option_type
        self.settlement_date = settlement_date
        self.settlement_type = settlement_type
        self.strike_price = strike_price
        self.put_currency = put_currency
        self.put_amount = put_amount
        self.automatic_exercise = automatic_exercise
        self.call_amount = call_amount
        self.call_currency = call_currency
        self.exercise_time = exercise_time
        self.multiplier = multiplier
        self.premium_payment_date = premium_payment_date
        self.premium = premium
        self.premium_currency = premium_currency
        self.__callable = callable_
        self.puttable = puttable
        self.perpetual = perpetual
        self.seniority = seniority
        self.coupon_type = coupon_type
        self.index = index
        self.index_term = index_term
        self.index_margin = index_margin
        self.coupon = coupon
        self.issue_date = issue_date
        self.issuer = issuer
        self.issuer_country_code = issuer_country_code
        self.issuer_type = issuer_type
        self.issue_size = issue_size
        self.commodity_sector = commodity_sector
        self.pricing_location = pricing_location
        self.contract_months = contract_months
        self.g10_currency = g10_currency
        self.portfolio_id = portfolio_id
        self.hedge_id = hedge_id
        self.ultimate_ticker = ultimate_ticker
        self.strategy = strategy
        self.exchange_currency = exchange_currency
        self.region = region
        self.delivery_point = delivery_point
        self.pricing_index = pricing_index
        self.common_code = common_code
        self.issuer_id = issuer_id
        self.contract_month = contract_month
        self.bloomberg_collateral_classification = bloomberg_collateral_classification
        self.load_type = load_type
        self.contract_unit = contract_unit
        self.index_approval_ids = index_approval_ids
        self.is_pair_basket = is_pair_basket
        self.is_legacy_pair_basket = is_legacy_pair_basket
        self.fixed_rate_day_count_fraction = fixed_rate_day_count_fraction
        self.floating_rate_day_count_fraction = floating_rate_day_count_fraction
        self.pair_calculation = pair_calculation
        self.pay_day_count_fraction = pay_day_count_fraction
        self.receive_day_count_fraction = receive_day_count_fraction
        self.pay_frequency = pay_frequency
        self.receive_frequency = receive_frequency
        self.resettable_leg = resettable_leg
        self.inflation_lag = inflation_lag
        self.fx_index = fx_index
        self.index_notes = index_notes
        self.index_not_trading_reasons = index_not_trading_reasons
        self.trade_as = trade_as
        self.clone_parent_id = clone_parent_id
        self.on_behalf_of = on_behalf_of
        self.index_calculation_agent = index_calculation_agent
        self.product_type = product_type
        self.vendor = vendor
        self.call_first_date = call_first_date
        self.call_last_date = call_last_date
        self.amount_outstanding = amount_outstanding
        self.covered_bond = covered_bond
        self.issue_status = issue_status
        self.issue_status_date = issue_status_date
        self.issue_price = issue_price
        self.sinkable = sinkable
        self.sink_factor = sink_factor
        self.accrued_interest_standard = accrued_interest_standard
        self.redemption_date = redemption_date
        self.redemption_price = redemption_price
        self.redemption_amount = redemption_amount
        self.redemption_percent = redemption_percent
        self.private_placement_type = private_placement_type
        self.minimum_piece = minimum_piece
        self.minimum_increment = minimum_increment
        self.next_coupon_payment = next_coupon_payment
        self.minimum_denomination = minimum_denomination
        self.default_backcast = default_backcast
        self.index_precision = index_precision
        self.official_side = official_side
        self.credit_index_series = credit_index_series
        self.reference_entity = reference_entity
        self.restructuring_type = restructuring_type
        self.underlying_type = underlying_type
        self.name = name

    @property
    def basket_type(self) -> str:
        """Type of basket / implementation"""
        return self.__basket_type

    @basket_type.setter
    def basket_type(self, value: str):
        self._property_changed('basket_type')
        self.__basket_type = value        

    @property
    def style(self) -> str:
        """Asset style"""
        return self.__style

    @style.setter
    def style(self, value: str):
        self._property_changed('style')
        self.__style = value        

    @property
    def attribution_dataset_id(self) -> str:
        """Identifier of dataset which provides performance attribution data"""
        return 'STSATTR'        

    @property
    def index_calculation_type(self) -> str:
        """Determines the index calculation methodology with respect to dividend
           reinvestment"""
        return self.__index_calculation_type

    @index_calculation_type.setter
    def index_calculation_type(self, value: str):
        self._property_changed('index_calculation_type')
        self.__index_calculation_type = value        

    @property
    def index_return_type(self) -> str:
        """Determines the return calculation type method with respect to cash accrual /
           funding"""
        return self.__index_return_type

    @index_return_type.setter
    def index_return_type(self, value: str):
        self._property_changed('index_return_type')
        self.__index_return_type = value        

    @property
    def index_divisor(self) -> float:
        """Divisor to be applied to the overall position set of the index"""
        return self.__index_divisor

    @index_divisor.setter
    def index_divisor(self, value: float):
        self._property_changed('index_divisor')
        self.__index_divisor = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def quote_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__quote_currency

    @quote_currency.setter
    def quote_currency(self, value: Union[Currency, str]):
        self._property_changed('quote_currency')
        self.__quote_currency = get_enum_value(Currency, value)        

    @property
    def index_initial_price(self) -> float:
        """Initial Price for the Index"""
        return self.__index_initial_price

    @index_initial_price.setter
    def index_initial_price(self, value: float):
        self._property_changed('index_initial_price')
        self.__index_initial_price = value        

    @property
    def initial_pricing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: datetime.date):
        self._property_changed('initial_pricing_date')
        self.__initial_pricing_date = value        

    @property
    def expiration_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: datetime.date):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def expiration_location(self) -> str:
        return self.__expiration_location

    @expiration_location.setter
    def expiration_location(self, value: str):
        self._property_changed('expiration_location')
        self.__expiration_location = value        

    @property
    def option_style(self) -> str:
        return self.__option_style

    @option_style.setter
    def option_style(self, value: str):
        self._property_changed('option_style')
        self.__option_style = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def settlement_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def settlement_type(self) -> str:
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: str):
        self._property_changed('settlement_type')
        self.__settlement_type = value        

    @property
    def strike_price(self) -> Union[float, str]:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: Union[float, str]):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def put_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__put_currency

    @put_currency.setter
    def put_currency(self, value: Union[Currency, str]):
        self._property_changed('put_currency')
        self.__put_currency = get_enum_value(Currency, value)        

    @property
    def put_amount(self) -> float:
        return self.__put_amount

    @put_amount.setter
    def put_amount(self, value: float):
        self._property_changed('put_amount')
        self.__put_amount = value        

    @property
    def automatic_exercise(self) -> bool:
        return self.__automatic_exercise

    @automatic_exercise.setter
    def automatic_exercise(self, value: bool):
        self._property_changed('automatic_exercise')
        self.__automatic_exercise = value        

    @property
    def call_amount(self) -> float:
        return self.__call_amount

    @call_amount.setter
    def call_amount(self, value: float):
        self._property_changed('call_amount')
        self.__call_amount = value        

    @property
    def call_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__call_currency

    @call_currency.setter
    def call_currency(self, value: Union[Currency, str]):
        self._property_changed('call_currency')
        self.__call_currency = get_enum_value(Currency, value)        

    @property
    def exercise_time(self) -> str:
        """Time at which the asset can be exercised"""
        return self.__exercise_time

    @exercise_time.setter
    def exercise_time(self, value: str):
        self._property_changed('exercise_time')
        self.__exercise_time = value        

    @property
    def multiplier(self) -> float:
        """Underlying unit per asset multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def premium_payment_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__premium_payment_date

    @premium_payment_date.setter
    def premium_payment_date(self, value: datetime.date):
        self._property_changed('premium_payment_date')
        self.__premium_payment_date = value        

    @property
    def premium(self) -> float:
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def premium_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__premium_currency

    @premium_currency.setter
    def premium_currency(self, value: Union[Currency, str]):
        self._property_changed('premium_currency')
        self.__premium_currency = get_enum_value(Currency, value)        

    @property
    def callable(self) -> bool:
        """Bond is callable"""
        return self.__callable

    @callable.setter
    def callable(self, value: bool):
        self._property_changed('callable')
        self.__callable = value        

    @property
    def puttable(self) -> bool:
        """Bond is puttable"""
        return self.__puttable

    @puttable.setter
    def puttable(self, value: bool):
        self._property_changed('puttable')
        self.__puttable = value        

    @property
    def perpetual(self) -> bool:
        """Bond is a perpetual"""
        return self.__perpetual

    @perpetual.setter
    def perpetual(self, value: bool):
        self._property_changed('perpetual')
        self.__perpetual = value        

    @property
    def seniority(self) -> str:
        """The seniority of the bond"""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: str):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def coupon_type(self) -> str:
        """The coupon type of the bond"""
        return self.__coupon_type

    @coupon_type.setter
    def coupon_type(self, value: str):
        self._property_changed('coupon_type')
        self.__coupon_type = value        

    @property
    def index(self) -> str:
        """The rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self._property_changed('index')
        self.__index = value        

    @property
    def index_term(self) -> str:
        """The term of rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this
           bond"""
        return self.__index_term

    @index_term.setter
    def index_term(self, value: str):
        self._property_changed('index_term')
        self.__index_term = value        

    @property
    def index_margin(self) -> float:
        """The spread over the rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon
           of this bond"""
        return self.__index_margin

    @index_margin.setter
    def index_margin(self, value: float):
        self._property_changed('index_margin')
        self.__index_margin = value        

    @property
    def coupon(self) -> float:
        """The fixed coupon for this bond"""
        return self.__coupon

    @coupon.setter
    def coupon(self, value: float):
        self._property_changed('coupon')
        self.__coupon = value        

    @property
    def issue_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: datetime.date):
        self._property_changed('issue_date')
        self.__issue_date = value        

    @property
    def issuer(self) -> str:
        """The issuer of this bond"""
        return self.__issuer

    @issuer.setter
    def issuer(self, value: str):
        self._property_changed('issuer')
        self.__issuer = value        

    @property
    def issuer_country_code(self) -> str:
        """The country code (ISO 3166) in which this bond was issued"""
        return self.__issuer_country_code

    @issuer_country_code.setter
    def issuer_country_code(self, value: str):
        self._property_changed('issuer_country_code')
        self.__issuer_country_code = value        

    @property
    def issuer_type(self) -> str:
        """The type of the bond issuer"""
        return self.__issuer_type

    @issuer_type.setter
    def issuer_type(self, value: str):
        self._property_changed('issuer_type')
        self.__issuer_type = value        

    @property
    def issue_size(self) -> float:
        """The notional issue size of the bond"""
        return self.__issue_size

    @issue_size.setter
    def issue_size(self, value: float):
        self._property_changed('issue_size')
        self.__issue_size = value        

    @property
    def commodity_sector(self) -> Union[CommoditySector, str]:
        """The sector of the commodity"""
        return self.__commodity_sector

    @commodity_sector.setter
    def commodity_sector(self, value: Union[CommoditySector, str]):
        self._property_changed('commodity_sector')
        self.__commodity_sector = get_enum_value(CommoditySector, value)        

    @property
    def pricing_location(self) -> Union[PricingLocation, str]:
        """Based on the location of the exchange. Called 'Native Region' in SecDB"""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: Union[PricingLocation, str]):
        self._property_changed('pricing_location')
        self.__pricing_location = get_enum_value(PricingLocation, value)        

    @property
    def contract_months(self) -> Tuple[str, ...]:
        """Contract months"""
        return self.__contract_months

    @contract_months.setter
    def contract_months(self, value: Tuple[str, ...]):
        self._property_changed('contract_months')
        self.__contract_months = value        

    @property
    def g10_currency(self) -> bool:
        """Is a G10 asset."""
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: bool):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def portfolio_id(self) -> str:
        """Marquee unique identifier"""
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: str):
        self._property_changed('portfolio_id')
        self.__portfolio_id = value        

    @property
    def hedge_id(self) -> str:
        """Marquee unique identifier"""
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: str):
        self._property_changed('hedge_id')
        self.__hedge_id = value        

    @property
    def ultimate_ticker(self) -> str:
        """The ultimate ticker for this security (e.g. SPXW)"""
        return self.__ultimate_ticker

    @ultimate_ticker.setter
    def ultimate_ticker(self, value: str):
        self._property_changed('ultimate_ticker')
        self.__ultimate_ticker = value        

    @property
    def strategy(self) -> Union[Strategy, str]:
        """More specific descriptor of a fund's investment approach. Same view permissions
           as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union[Strategy, str]):
        self._property_changed('strategy')
        self.__strategy = get_enum_value(Strategy, value)        

    @property
    def exchange_currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__exchange_currency

    @exchange_currency.setter
    def exchange_currency(self, value: Union[Currency, str]):
        self._property_changed('exchange_currency')
        self.__exchange_currency = get_enum_value(Currency, value)        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def delivery_point(self) -> str:
        return self.__delivery_point

    @delivery_point.setter
    def delivery_point(self, value: str):
        self._property_changed('delivery_point')
        self.__delivery_point = value        

    @property
    def pricing_index(self) -> str:
        return self.__pricing_index

    @pricing_index.setter
    def pricing_index(self, value: str):
        self._property_changed('pricing_index')
        self.__pricing_index = value        

    @property
    def common_code(self) -> str:
        return self.__common_code

    @common_code.setter
    def common_code(self, value: str):
        self._property_changed('common_code')
        self.__common_code = value        

    @property
    def issuer_id(self) -> str:
        return self.__issuer_id

    @issuer_id.setter
    def issuer_id(self, value: str):
        self._property_changed('issuer_id')
        self.__issuer_id = value        

    @property
    def contract_month(self) -> str:
        return self.__contract_month

    @contract_month.setter
    def contract_month(self, value: str):
        self._property_changed('contract_month')
        self.__contract_month = value        

    @property
    def bloomberg_collateral_classification(self) -> str:
        return self.__bloomberg_collateral_classification

    @bloomberg_collateral_classification.setter
    def bloomberg_collateral_classification(self, value: str):
        self._property_changed('bloomberg_collateral_classification')
        self.__bloomberg_collateral_classification = value        

    @property
    def load_type(self) -> str:
        return self.__load_type

    @load_type.setter
    def load_type(self, value: str):
        self._property_changed('load_type')
        self.__load_type = value        

    @property
    def contract_unit(self) -> str:
        return self.__contract_unit

    @contract_unit.setter
    def contract_unit(self, value: str):
        self._property_changed('contract_unit')
        self.__contract_unit = value        

    @property
    def index_approval_ids(self) -> Tuple[str, ...]:
        """Array of approval identifiers related to the object"""
        return self.__index_approval_ids

    @index_approval_ids.setter
    def index_approval_ids(self, value: Tuple[str, ...]):
        self._property_changed('index_approval_ids')
        self.__index_approval_ids = value        

    @property
    def is_pair_basket(self) -> bool:
        return self.__is_pair_basket

    @is_pair_basket.setter
    def is_pair_basket(self, value: bool):
        self._property_changed('is_pair_basket')
        self.__is_pair_basket = value        

    @property
    def is_legacy_pair_basket(self) -> bool:
        return self.__is_legacy_pair_basket

    @is_legacy_pair_basket.setter
    def is_legacy_pair_basket(self, value: bool):
        self._property_changed('is_legacy_pair_basket')
        self.__is_legacy_pair_basket = value        

    @property
    def fixed_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for fixed legs"""
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def floating_rate_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for floating legs"""
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def pair_calculation(self) -> str:
        """Pair basket calculation composed of long and short coefficients for each leg, as
           well as cash amount"""
        return self.__pair_calculation

    @pair_calculation.setter
    def pair_calculation(self, value: str):
        self._property_changed('pair_calculation')
        self.__pair_calculation = value        

    @property
    def pay_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for pay leg"""
        return self.__pay_day_count_fraction

    @pay_day_count_fraction.setter
    def pay_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('pay_day_count_fraction')
        self.__pay_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def receive_day_count_fraction(self) -> Union[DayCountFraction, str]:
        """Default day count fraction for the receive leg"""
        return self.__receive_day_count_fraction

    @receive_day_count_fraction.setter
    def receive_day_count_fraction(self, value: Union[DayCountFraction, str]):
        self._property_changed('receive_day_count_fraction')
        self.__receive_day_count_fraction = get_enum_value(DayCountFraction, value)        

    @property
    def pay_frequency(self) -> str:
        """Default frequency of the pay leg"""
        return self.__pay_frequency

    @pay_frequency.setter
    def pay_frequency(self, value: str):
        self._property_changed('pay_frequency')
        self.__pay_frequency = value        

    @property
    def receive_frequency(self) -> str:
        """Default frequency of the receive leg"""
        return self.__receive_frequency

    @receive_frequency.setter
    def receive_frequency(self, value: str):
        self._property_changed('receive_frequency')
        self.__receive_frequency = value        

    @property
    def resettable_leg(self) -> Union[PayReceive, str]:
        """Resettable leg"""
        return self.__resettable_leg

    @resettable_leg.setter
    def resettable_leg(self, value: Union[PayReceive, str]):
        self._property_changed('resettable_leg')
        self.__resettable_leg = get_enum_value(PayReceive, value)        

    @property
    def inflation_lag(self) -> str:
        """Inflation lag"""
        return self.__inflation_lag

    @inflation_lag.setter
    def inflation_lag(self, value: str):
        self._property_changed('inflation_lag')
        self.__inflation_lag = value        

    @property
    def fx_index(self) -> str:
        """FX index"""
        return self.__fx_index

    @fx_index.setter
    def fx_index(self, value: str):
        self._property_changed('fx_index')
        self.__fx_index = value        

    @property
    def index_notes(self) -> str:
        """Notes for the index"""
        return self.__index_notes

    @index_notes.setter
    def index_notes(self, value: str):
        self._property_changed('index_notes')
        self.__index_notes = value        

    @property
    def index_not_trading_reasons(self) -> Union[IndexNotTradingReasons, str]:
        """Reasons the index was not traded"""
        return self.__index_not_trading_reasons

    @index_not_trading_reasons.setter
    def index_not_trading_reasons(self, value: Union[IndexNotTradingReasons, str]):
        self._property_changed('index_not_trading_reasons')
        self.__index_not_trading_reasons = get_enum_value(IndexNotTradingReasons, value)        

    @property
    def trade_as(self) -> str:
        """How to trade the Option."""
        return self.__trade_as

    @trade_as.setter
    def trade_as(self, value: str):
        self._property_changed('trade_as')
        self.__trade_as = value        

    @property
    def clone_parent_id(self) -> str:
        """Marquee unique identifier"""
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: str):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def on_behalf_of(self) -> str:
        """Marquee unique identifier"""
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def index_calculation_agent(self) -> str:
        """Calculation agent of the index."""
        return self.__index_calculation_agent

    @index_calculation_agent.setter
    def index_calculation_agent(self, value: str):
        self._property_changed('index_calculation_agent')
        self.__index_calculation_agent = value        

    @property
    def product_type(self) -> Union[ProductType, str]:
        """Basket Product Type."""
        return self.__product_type

    @product_type.setter
    def product_type(self, value: Union[ProductType, str]):
        self._property_changed('product_type')
        self.__product_type = get_enum_value(ProductType, value)        

    @property
    def vendor(self) -> str:
        """Basket Vendor OEID."""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def call_first_date(self) -> datetime.date:
        """The first date which you call the bond."""
        return self.__call_first_date

    @call_first_date.setter
    def call_first_date(self, value: datetime.date):
        self._property_changed('call_first_date')
        self.__call_first_date = value        

    @property
    def call_last_date(self) -> datetime.date:
        """The first date which you call the bond."""
        return self.__call_last_date

    @call_last_date.setter
    def call_last_date(self, value: datetime.date):
        self._property_changed('call_last_date')
        self.__call_last_date = value        

    @property
    def amount_outstanding(self) -> float:
        """The aggregate principal amount of the total number of bonds not redeemed or
           otherwise discharged."""
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: float):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value        

    @property
    def covered_bond(self) -> bool:
        """Whether the debt security is collateralized against a pool of assets that, in
           case of failure of the issuer, can cover claims at any point of time."""
        return self.__covered_bond

    @covered_bond.setter
    def covered_bond(self, value: bool):
        self._property_changed('covered_bond')
        self.__covered_bond = value        

    @property
    def issue_status(self) -> str:
        """Status of the issue."""
        return self.__issue_status

    @issue_status.setter
    def issue_status(self, value: str):
        self._property_changed('issue_status')
        self.__issue_status = value        

    @property
    def issue_status_date(self) -> datetime.date:
        """Date at which the status was given to the issue."""
        return self.__issue_status_date

    @issue_status_date.setter
    def issue_status_date(self, value: datetime.date):
        self._property_changed('issue_status_date')
        self.__issue_status_date = value        

    @property
    def issue_price(self) -> float:
        """The price for which the instrument is issued"""
        return self.__issue_price

    @issue_price.setter
    def issue_price(self, value: float):
        self._property_changed('issue_price')
        self.__issue_price = value        

    @property
    def sinkable(self) -> bool:
        """A bond that is protected by a fund (called a sinking fund) that sets aside money
           to ensure principal and interest payments are made by the issuer as
           promised."""
        return self.__sinkable

    @sinkable.setter
    def sinkable(self, value: bool):
        self._property_changed('sinkable')
        self.__sinkable = value        

    @property
    def sink_factor(self) -> float:
        """The level to which a sinkable bond has currently sunk."""
        return self.__sink_factor

    @sink_factor.setter
    def sink_factor(self, value: float):
        self._property_changed('sink_factor')
        self.__sink_factor = value        

    @property
    def accrued_interest_standard(self) -> float:
        """The accrued interest paid on the bond if it is settled two business days after
           the trade date."""
        return self.__accrued_interest_standard

    @accrued_interest_standard.setter
    def accrued_interest_standard(self, value: float):
        self._property_changed('accrued_interest_standard')
        self.__accrued_interest_standard = value        

    @property
    def redemption_date(self) -> datetime.date:
        """The date on which a bond's face value is repaid to bondholders."""
        return self.__redemption_date

    @redemption_date.setter
    def redemption_date(self, value: datetime.date):
        self._property_changed('redemption_date')
        self.__redemption_date = value        

    @property
    def redemption_price(self) -> float:
        """The price for which the issuer will repurchase the security for at the
           redemption date."""
        return self.__redemption_price

    @redemption_price.setter
    def redemption_price(self, value: float):
        self._property_changed('redemption_price')
        self.__redemption_price = value        

    @property
    def redemption_amount(self) -> float:
        """The repayment of the principal amount."""
        return self.__redemption_amount

    @redemption_amount.setter
    def redemption_amount(self, value: float):
        self._property_changed('redemption_amount')
        self.__redemption_amount = value        

    @property
    def redemption_percent(self) -> float:
        """The price for which the issuer will repurchase the security for at the
           redemption date."""
        return self.__redemption_percent

    @redemption_percent.setter
    def redemption_percent(self, value: float):
        self._property_changed('redemption_percent')
        self.__redemption_percent = value        

    @property
    def private_placement_type(self) -> str:
        """Regulation that applies to a bond."""
        return self.__private_placement_type

    @private_placement_type.setter
    def private_placement_type(self, value: str):
        self._property_changed('private_placement_type')
        self.__private_placement_type = value        

    @property
    def minimum_piece(self) -> float:
        """The lowest denomination of an issue that can be purchased as authorized by the
           bond documents"""
        return self.__minimum_piece

    @minimum_piece.setter
    def minimum_piece(self, value: float):
        self._property_changed('minimum_piece')
        self.__minimum_piece = value        

    @property
    def minimum_increment(self) -> float:
        """The minimum increment size of the bond purchase allowed above the minimum
           denomination as authorized by the bond documents"""
        return self.__minimum_increment

    @minimum_increment.setter
    def minimum_increment(self, value: float):
        self._property_changed('minimum_increment')
        self.__minimum_increment = value        

    @property
    def next_coupon_payment(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__next_coupon_payment

    @next_coupon_payment.setter
    def next_coupon_payment(self, value: datetime.date):
        self._property_changed('next_coupon_payment')
        self.__next_coupon_payment = value        

    @property
    def minimum_denomination(self) -> float:
        """The lowest denomination of an issue that can be purchased as authorized by the
           bond documents"""
        return self.__minimum_denomination

    @minimum_denomination.setter
    def minimum_denomination(self, value: float):
        self._property_changed('minimum_denomination')
        self.__minimum_denomination = value        

    @property
    def default_backcast(self) -> bool:
        """Is basket backcasted using initial positions."""
        return self.__default_backcast

    @default_backcast.setter
    def default_backcast(self, value: bool):
        self._property_changed('default_backcast')
        self.__default_backcast = value        

    @property
    def index_precision(self) -> float:
        """The precision of the index levels."""
        return self.__index_precision

    @index_precision.setter
    def index_precision(self, value: float):
        self._property_changed('index_precision')
        self.__index_precision = value        

    @property
    def official_side(self) -> Union[Side, str]:
        """Official side of an index"""
        return self.__official_side

    @official_side.setter
    def official_side(self, value: Union[Side, str]):
        self._property_changed('official_side')
        self.__official_side = get_enum_value(Side, value)        

    @property
    def credit_index_series(self) -> str:
        """Series of the credit index."""
        return self.__credit_index_series

    @credit_index_series.setter
    def credit_index_series(self, value: str):
        self._property_changed('credit_index_series')
        self.__credit_index_series = value        

    @property
    def reference_entity(self) -> str:
        """Underlying reference entity."""
        return self.__reference_entity

    @reference_entity.setter
    def reference_entity(self, value: str):
        self._property_changed('reference_entity')
        self.__reference_entity = value        

    @property
    def restructuring_type(self) -> str:
        """CDS Restructuring type."""
        return self.__restructuring_type

    @restructuring_type.setter
    def restructuring_type(self, value: str):
        self._property_changed('restructuring_type')
        self.__restructuring_type = value        

    @property
    def underlying_type(self) -> str:
        """Underlying CDS credit market."""
        return self.__underlying_type

    @underlying_type.setter
    def underlying_type(self, value: str):
        self._property_changed('underlying_type')
        self.__underlying_type = value        


class CSLCurrency(Base):
        
    """A currency"""

    @camel_case_translate
    def __init__(
        self,
        string_value: Union[Currency, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: Union[Currency, str]):
        self._property_changed('string_value')
        self.__string_value = get_enum_value(Currency, value)        


class CSLDateArray(Base):
        
    """An array of dates"""

    @camel_case_translate
    def __init__(
        self,
        date_values: Tuple[CSLDate, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.date_values = date_values
        self.name = name

    @property
    def date_values(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__date_values

    @date_values.setter
    def date_values(self, value: Tuple[CSLDate, ...]):
        self._property_changed('date_values')
        self.__date_values = value        


class CSLDateArrayNamedParam(Base):
        
    """A named array of dates"""

    @camel_case_translate
    def __init__(
        self,
        date_values: Tuple[CSLDate, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.date_values = date_values
        self.name = name

    @property
    def date_values(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__date_values

    @date_values.setter
    def date_values(self, value: Tuple[CSLDate, ...]):
        self._property_changed('date_values')
        self.__date_values = value        

    @property
    def name(self) -> str:
        """A name for the array"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class CSLDoubleArray(Base):
        
    """An array of doubles"""

    @camel_case_translate
    def __init__(
        self,
        double_values: Tuple[CSLDouble, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.double_values = double_values
        self.name = name

    @property
    def double_values(self) -> Tuple[CSLDouble, ...]:
        """A double"""
        return self.__double_values

    @double_values.setter
    def double_values(self, value: Tuple[CSLDouble, ...]):
        self._property_changed('double_values')
        self.__double_values = value        


class CSLFXCrossArray(Base):
        
    """An array of FX crosses"""

    @camel_case_translate
    def __init__(
        self,
        fx_cross_values: Tuple[CSLFXCross, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.fx_cross_values = fx_cross_values
        self.name = name

    @property
    def fx_cross_values(self) -> Tuple[CSLFXCross, ...]:
        """An FX cross"""
        return self.__fx_cross_values

    @fx_cross_values.setter
    def fx_cross_values(self, value: Tuple[CSLFXCross, ...]):
        self._property_changed('fx_cross_values')
        self.__fx_cross_values = value        


class CSLIndexArray(Base):
        
    """An array of indices"""

    @camel_case_translate
    def __init__(
        self,
        index_values: Tuple[CSLIndex, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.index_values = index_values
        self.name = name

    @property
    def index_values(self) -> Tuple[CSLIndex, ...]:
        """An index"""
        return self.__index_values

    @index_values.setter
    def index_values(self, value: Tuple[CSLIndex, ...]):
        self._property_changed('index_values')
        self.__index_values = value        


class CSLSimpleScheduleArray(Base):
        
    """An array of simple schedules"""

    @camel_case_translate
    def __init__(
        self,
        simple_schedule_values: Tuple[CSLSimpleSchedule, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.simple_schedule_values = simple_schedule_values
        self.name = name

    @property
    def simple_schedule_values(self) -> Tuple[CSLSimpleSchedule, ...]:
        """A fixing date, settlement date pair"""
        return self.__simple_schedule_values

    @simple_schedule_values.setter
    def simple_schedule_values(self, value: Tuple[CSLSimpleSchedule, ...]):
        self._property_changed('simple_schedule_values')
        self.__simple_schedule_values = value        


class CSLStockArray(Base):
        
    """An array of stocks"""

    @camel_case_translate
    def __init__(
        self,
        stock_values: Tuple[CSLStock, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.stock_values = stock_values
        self.name = name

    @property
    def stock_values(self) -> Tuple[CSLStock, ...]:
        """A stock"""
        return self.__stock_values

    @stock_values.setter
    def stock_values(self, value: Tuple[CSLStock, ...]):
        self._property_changed('stock_values')
        self.__stock_values = value        


class CSLStringArray(Base):
        
    """An array of strings"""

    @camel_case_translate
    def __init__(
        self,
        string_values: Tuple[CSLString, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.string_values = string_values
        self.name = name

    @property
    def string_values(self) -> Tuple[CSLString, ...]:
        """A string"""
        return self.__string_values

    @string_values.setter
    def string_values(self, value: Tuple[CSLString, ...]):
        self._property_changed('string_values')
        self.__string_values = value        


class CarryScenario(Scenario):
        
    """A scenario to manipulate time along the forward curve"""

    @deprecation.deprecated(deprecated_in='0.8.216', removed_in='1.0.0', details='CarryScenario is now deprecated, please use RollFwd instead. CarryScenario will not be supported in all versions of gs-quant starting 2021.')
    @camel_case_translate
    def __init__(
        self,
        date: Union[datetime.date, str] = None,
        time_shift: int = None,
        roll_to_fwds: bool = True,
        holiday_calendar: Union[PricingLocation, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.time_shift = time_shift
        self.roll_to_fwds = roll_to_fwds
        self.holiday_calendar = holiday_calendar
        self.name = name

    @property
    def scenario_type(self) -> str:
        """CarryScenario"""
        return 'CarryScenario'        

    @property
    def date(self) -> Union[datetime.date, str]:
        """Date to shift markets to (absolute or relative)"""
        return self.__date

    @date.setter
    def date(self, value: Union[datetime.date, str]):
        self._property_changed('date')
        self.__date = value        

    @property
    def time_shift(self) -> int:
        """Number of days to shift market (in days)"""
        return self.__time_shift

    @time_shift.setter
    def time_shift(self, value: int):
        self._property_changed('time_shift')
        self.__time_shift = value        

    @property
    def roll_to_fwds(self) -> bool:
        """Roll along the forward curve or roll in spot space"""
        return self.__roll_to_fwds

    @roll_to_fwds.setter
    def roll_to_fwds(self, value: bool):
        self._property_changed('roll_to_fwds')
        self.__roll_to_fwds = value        

    @property
    def holiday_calendar(self) -> Union[PricingLocation, str]:
        """Calendar to use for relative dates"""
        return self.__holiday_calendar

    @holiday_calendar.setter
    def holiday_calendar(self, value: Union[PricingLocation, str]):
        self._property_changed('holiday_calendar')
        self.__holiday_calendar = get_enum_value(PricingLocation, value)        


class CloseMarket(Base):
        
    """Close market"""

    @camel_case_translate
    def __init__(
        self,
        date: datetime.date,
        location: Union[PricingLocation, str],
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.location = location
        self.name = name

    @property
    def market_type(self) -> str:
        """CloseMarket"""
        return 'CloseMarket'        

    @property
    def date(self) -> datetime.date:
        """Date for the market data"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def location(self) -> Union[PricingLocation, str]:
        """Location for the market data"""
        return self.__location

    @location.setter
    def location(self, value: Union[PricingLocation, str]):
        self._property_changed('location')
        self.__location = get_enum_value(PricingLocation, value)        


class CommodPrice(Base):
        
    """Commodity price in units and currency, used for quoting strike, premium, fixed
       price"""

    @camel_case_translate
    def __init__(
        self,
        unit: Union[CommodUnit, str] = None,
        price: Union[float, str] = None,
        currency: Union[CurrencyName, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.unit = unit
        self.price = price
        self.currency = currency
        self.name = name

    @property
    def unit(self) -> Union[CommodUnit, str]:
        """A coding scheme value to identify the unit of measure (e.g. Therms) in which the
           undelryer is denominated."""
        return self.__unit

    @unit.setter
    def unit(self, value: Union[CommodUnit, str]):
        self._property_changed('unit')
        self.__unit = get_enum_value(CommodUnit, value)        

    @property
    def price(self) -> Union[float, str]:
        """price"""
        return self.__price

    @price.setter
    def price(self, value: Union[float, str]):
        self._property_changed('price')
        self.__price = value        

    @property
    def currency(self) -> Union[CurrencyName, str]:
        """Currency Names"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[CurrencyName, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(CurrencyName, value)        


class EntitlementExclusions(Base):
        
    """Defines the exclusion entitlements of a given resource."""

    @camel_case_translate
    def __init__(
        self,
        view: Tuple[Tuple[str, ...], ...] = None,
        edit: Tuple[Tuple[str, ...], ...] = None,
        admin: Tuple[Tuple[str, ...], ...] = None,
        rebalance: Tuple[Tuple[str, ...], ...] = None,
        execute: Tuple[Tuple[str, ...], ...] = None,
        trade: Tuple[Tuple[str, ...], ...] = None,
        upload: Tuple[Tuple[str, ...], ...] = None,
        query: Tuple[Tuple[str, ...], ...] = None,
        performance_details: Tuple[Tuple[str, ...], ...] = None,
        plot: Tuple[Tuple[str, ...], ...] = None,
        delete: Tuple[Tuple[str, ...], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.view = view
        self.edit = edit
        self.admin = admin
        self.rebalance = rebalance
        self.execute = execute
        self.trade = trade
        self.upload = upload
        self.query = query
        self.performance_details = performance_details
        self.plot = plot
        self.delete = delete
        self.name = name

    @property
    def view(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__view

    @view.setter
    def view(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('view')
        self.__view = value        

    @property
    def edit(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('edit')
        self.__edit = value        

    @property
    def admin(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('admin')
        self.__admin = value        

    @property
    def rebalance(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('rebalance')
        self.__rebalance = value        

    @property
    def execute(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__execute

    @execute.setter
    def execute(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('execute')
        self.__execute = value        

    @property
    def trade(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__trade

    @trade.setter
    def trade(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('trade')
        self.__trade = value        

    @property
    def upload(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__upload

    @upload.setter
    def upload(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('upload')
        self.__upload = value        

    @property
    def query(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__query

    @query.setter
    def query(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('query')
        self.__query = value        

    @property
    def performance_details(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__performance_details

    @performance_details.setter
    def performance_details(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('performance_details')
        self.__performance_details = value        

    @property
    def plot(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__plot

    @plot.setter
    def plot(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('plot')
        self.__plot = value        

    @property
    def delete(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__delete

    @delete.setter
    def delete(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('delete')
        self.__delete = value        


class Entitlements(Base):
        
    """Defines the entitlements of a given resource."""

    @camel_case_translate
    def __init__(
        self,
        view: Tuple[str, ...] = None,
        edit: Tuple[str, ...] = None,
        admin: Tuple[str, ...] = None,
        rebalance: Tuple[str, ...] = None,
        execute: Tuple[str, ...] = None,
        trade: Tuple[str, ...] = None,
        upload: Tuple[str, ...] = None,
        query: Tuple[str, ...] = None,
        performance_details: Tuple[str, ...] = None,
        plot: Tuple[str, ...] = None,
        delete: Tuple[str, ...] = None,
        display: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.view = view
        self.edit = edit
        self.admin = admin
        self.rebalance = rebalance
        self.execute = execute
        self.trade = trade
        self.upload = upload
        self.query = query
        self.performance_details = performance_details
        self.plot = plot
        self.delete = delete
        self.display = display
        self.name = name

    @property
    def view(self) -> Tuple[str, ...]:
        """Permission to view the resource and its contents"""
        return self.__view

    @view.setter
    def view(self, value: Tuple[str, ...]):
        self._property_changed('view')
        self.__view = value        

    @property
    def edit(self) -> Tuple[str, ...]:
        """Permission to edit details about the resource content, excluding entitlements.
           Can also delete the resource"""
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[str, ...]):
        self._property_changed('edit')
        self.__edit = value        

    @property
    def admin(self) -> Tuple[str, ...]:
        """Permission to edit all details of the resource, including entitlements. Can also
           delete the resource"""
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[str, ...]):
        self._property_changed('admin')
        self.__admin = value        

    @property
    def rebalance(self) -> Tuple[str, ...]:
        """Permission to rebalance the constituent weights of the resource"""
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value: Tuple[str, ...]):
        self._property_changed('rebalance')
        self.__rebalance = value        

    @property
    def execute(self) -> Tuple[str, ...]:
        """Permission to execute functions and/or reports with the resource"""
        return self.__execute

    @execute.setter
    def execute(self, value: Tuple[str, ...]):
        self._property_changed('execute')
        self.__execute = value        

    @property
    def trade(self) -> Tuple[str, ...]:
        """Permission to trade the resource"""
        return self.__trade

    @trade.setter
    def trade(self, value: Tuple[str, ...]):
        self._property_changed('trade')
        self.__trade = value        

    @property
    def upload(self) -> Tuple[str, ...]:
        """Permission to upload data to the given resource"""
        return self.__upload

    @upload.setter
    def upload(self, value: Tuple[str, ...]):
        self._property_changed('upload')
        self.__upload = value        

    @property
    def query(self) -> Tuple[str, ...]:
        """Permission to query data from the given resource"""
        return self.__query

    @query.setter
    def query(self, value: Tuple[str, ...]):
        self._property_changed('query')
        self.__query = value        

    @property
    def performance_details(self) -> Tuple[str, ...]:
        """Permission to view the resource, it's entire contents, and related data"""
        return self.__performance_details

    @performance_details.setter
    def performance_details(self, value: Tuple[str, ...]):
        self._property_changed('performance_details')
        self.__performance_details = value        

    @property
    def plot(self) -> Tuple[str, ...]:
        """Permission to plot data from the given resource"""
        return self.__plot

    @plot.setter
    def plot(self, value: Tuple[str, ...]):
        self._property_changed('plot')
        self.__plot = value        

    @property
    def delete(self) -> Tuple[str, ...]:
        """Permission to delete the resource"""
        return self.__delete

    @delete.setter
    def delete(self, value: Tuple[str, ...]):
        self._property_changed('delete')
        self.__delete = value        

    @property
    def display(self) -> Tuple[str, ...]:
        """Permission to query data for web router request so that it can prevent
           programmatic access (api access) to the licensed data."""
        return self.__display

    @display.setter
    def display(self, value: Tuple[str, ...]):
        self._property_changed('display')
        self.__display = value        


class FieldValueMap(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class FiniteDifferenceParameter(Base):
        
    """Extra parameters for griffin reports"""

    @camel_case_translate
    def __init__(
        self,
        aggregation_level: Union[AggregationLevel, str] = None,
        currency: str = None,
        local_curve: bool = None,
        bump_size: float = None,
        finite_difference_method: Union[FiniteDifferenceMethod, str] = None,
        scale_factor: float = None,
        mkt_marking_mode: str = None,
        name: str = None
    ):        
        super().__init__()
        self.aggregation_level = aggregation_level
        self.currency = currency
        self.local_curve = local_curve
        self.bump_size = bump_size
        self.finite_difference_method = finite_difference_method
        self.scale_factor = scale_factor
        self.mkt_marking_mode = mkt_marking_mode
        self.name = name

    @property
    def parameter_type(self) -> str:
        """FiniteDifference"""
        return 'FiniteDifference'        

    @property
    def aggregation_level(self) -> Union[AggregationLevel, str]:
        """Aggregation Level"""
        return self.__aggregation_level

    @aggregation_level.setter
    def aggregation_level(self, value: Union[AggregationLevel, str]):
        self._property_changed('aggregation_level')
        self.__aggregation_level = get_enum_value(AggregationLevel, value)        

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def local_curve(self) -> bool:
        return self.__local_curve

    @local_curve.setter
    def local_curve(self, value: bool):
        self._property_changed('local_curve')
        self.__local_curve = value        

    @property
    def bump_size(self) -> float:
        return self.__bump_size

    @bump_size.setter
    def bump_size(self, value: float):
        self._property_changed('bump_size')
        self.__bump_size = value        

    @property
    def finite_difference_method(self) -> Union[FiniteDifferenceMethod, str]:
        """Direction and dimension of finite difference"""
        return self.__finite_difference_method

    @finite_difference_method.setter
    def finite_difference_method(self, value: Union[FiniteDifferenceMethod, str]):
        self._property_changed('finite_difference_method')
        self.__finite_difference_method = get_enum_value(FiniteDifferenceMethod, value)        

    @property
    def scale_factor(self) -> float:
        return self.__scale_factor

    @scale_factor.setter
    def scale_factor(self, value: float):
        self._property_changed('scale_factor')
        self.__scale_factor = value        

    @property
    def mkt_marking_mode(self) -> str:
        return self.__mkt_marking_mode

    @mkt_marking_mode.setter
    def mkt_marking_mode(self, value: str):
        self._property_changed('mkt_marking_mode')
        self.__mkt_marking_mode = value        


class ISelectNewParameter(Base):
        
    _name_mappings = {'is_fsr_target_factor': 'isFSRTargetFactor', 'trend_signal_0': 'trendSignal_0', 'trend_signal_1': 'trendSignal_1', 'trend_signal_2': 'trendSignal_2', 'trend_signal_3': 'trendSignal_3'}

    @camel_case_translate
    def __init__(
        self,
        early_unwind_after: float = None,
        early_unwind_applicable: str = None,
        expiry_date_rule: str = None,
        option_target_expiry_parameter: float = None,
        option_early_unwind_days: float = None,
        in_alpha: bool = None,
        is_fsr_target_factor: bool = None,
        fsr_max_ratio: float = None,
        fsr_min_ratio: float = None,
        module_enabled: bool = None,
        trend_signal_0: bool = None,
        trend_signal_1: bool = None,
        trend_signal_2: bool = None,
        trend_signal_3: bool = None,
        module_name: str = None,
        target_strike: float = None,
        strike_method: Union[StrikeMethodType, str] = None,
        option_expiry: Union[OptionExpiryType, str] = None,
        bloomberg_id: str = None,
        stock_id: str = None,
        future_id: str = None,
        ric: str = None,
        new_weight: float = None,
        execution_participation_rate: float = None,
        new_shares: float = None,
        new_lots: float = None,
        execution_start_time: dict = None,
        execution_end_time: dict = None,
        execution_style: str = None,
        execution_timezone: str = None,
        notional: float = None,
        leverage: float = None,
        quantity: float = None,
        hedge_ratio: float = None,
        option_type: Union[OptionType, str] = None,
        option_strike_type: Union[OptionStrikeType, str] = None,
        credit_option_type: Union[CreditOptionType, str] = None,
        credit_option_strike_type: Union[CreditOptionStrikeType, str] = None,
        strike_relative: float = None,
        trade_type: Union[TradeType, str] = None,
        signal: float = None,
        new_signal: float = None,
        new_min_weight: float = None,
        new_max_weight: float = None,
        min_weight: float = None,
        max_weight: float = None,
        weight_smoothing_window: float = None,
        election: str = None,
        base_date: str = None,
        commodity: str = None,
        component_weight: float = None,
        contract_nearby_number: float = None,
        expiration_schedule: str = None,
        fixing_type: str = None,
        last_eligible_date: float = None,
        num_roll_days: float = None,
        roll_end: float = None,
        roll_start: float = None,
        roll_type: str = None,
        valid_contract_expiry: str = None,
        name: str = None
    ):        
        super().__init__()
        self.early_unwind_after = early_unwind_after
        self.early_unwind_applicable = early_unwind_applicable
        self.expiry_date_rule = expiry_date_rule
        self.option_target_expiry_parameter = option_target_expiry_parameter
        self.option_early_unwind_days = option_early_unwind_days
        self.in_alpha = in_alpha
        self.is_fsr_target_factor = is_fsr_target_factor
        self.fsr_max_ratio = fsr_max_ratio
        self.fsr_min_ratio = fsr_min_ratio
        self.module_enabled = module_enabled
        self.trend_signal_0 = trend_signal_0
        self.trend_signal_1 = trend_signal_1
        self.trend_signal_2 = trend_signal_2
        self.trend_signal_3 = trend_signal_3
        self.module_name = module_name
        self.target_strike = target_strike
        self.strike_method = strike_method
        self.option_expiry = option_expiry
        self.bloomberg_id = bloomberg_id
        self.stock_id = stock_id
        self.future_id = future_id
        self.ric = ric
        self.new_weight = new_weight
        self.execution_participation_rate = execution_participation_rate
        self.new_shares = new_shares
        self.new_lots = new_lots
        self.execution_start_time = execution_start_time
        self.execution_end_time = execution_end_time
        self.execution_style = execution_style
        self.execution_timezone = execution_timezone
        self.notional = notional
        self.leverage = leverage
        self.quantity = quantity
        self.hedge_ratio = hedge_ratio
        self.option_type = option_type
        self.option_strike_type = option_strike_type
        self.credit_option_type = credit_option_type
        self.credit_option_strike_type = credit_option_strike_type
        self.strike_relative = strike_relative
        self.trade_type = trade_type
        self.signal = signal
        self.new_signal = new_signal
        self.new_min_weight = new_min_weight
        self.new_max_weight = new_max_weight
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.weight_smoothing_window = weight_smoothing_window
        self.election = election
        self.base_date = base_date
        self.commodity = commodity
        self.component_weight = component_weight
        self.contract_nearby_number = contract_nearby_number
        self.expiration_schedule = expiration_schedule
        self.fixing_type = fixing_type
        self.last_eligible_date = last_eligible_date
        self.num_roll_days = num_roll_days
        self.roll_end = roll_end
        self.roll_start = roll_start
        self.roll_type = roll_type
        self.valid_contract_expiry = valid_contract_expiry
        self.name = name

    @property
    def early_unwind_after(self) -> float:
        return self.__early_unwind_after

    @early_unwind_after.setter
    def early_unwind_after(self, value: float):
        self._property_changed('early_unwind_after')
        self.__early_unwind_after = value        

    @property
    def early_unwind_applicable(self) -> str:
        """Indicates whether the module can be unwinded early"""
        return self.__early_unwind_applicable

    @early_unwind_applicable.setter
    def early_unwind_applicable(self, value: str):
        self._property_changed('early_unwind_applicable')
        self.__early_unwind_applicable = value        

    @property
    def expiry_date_rule(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__expiry_date_rule

    @expiry_date_rule.setter
    def expiry_date_rule(self, value: str):
        self._property_changed('expiry_date_rule')
        self.__expiry_date_rule = value        

    @property
    def option_target_expiry_parameter(self) -> float:
        return self.__option_target_expiry_parameter

    @option_target_expiry_parameter.setter
    def option_target_expiry_parameter(self, value: float):
        self._property_changed('option_target_expiry_parameter')
        self.__option_target_expiry_parameter = value        

    @property
    def option_early_unwind_days(self) -> float:
        return self.__option_early_unwind_days

    @option_early_unwind_days.setter
    def option_early_unwind_days(self, value: float):
        self._property_changed('option_early_unwind_days')
        self.__option_early_unwind_days = value        

    @property
    def in_alpha(self) -> bool:
        return self.__in_alpha

    @in_alpha.setter
    def in_alpha(self, value: bool):
        self._property_changed('in_alpha')
        self.__in_alpha = value        

    @property
    def is_fsr_target_factor(self) -> bool:
        return self.__is_fsr_target_factor

    @is_fsr_target_factor.setter
    def is_fsr_target_factor(self, value: bool):
        self._property_changed('is_fsr_target_factor')
        self.__is_fsr_target_factor = value        

    @property
    def fsr_max_ratio(self) -> float:
        return self.__fsr_max_ratio

    @fsr_max_ratio.setter
    def fsr_max_ratio(self, value: float):
        self._property_changed('fsr_max_ratio')
        self.__fsr_max_ratio = value        

    @property
    def fsr_min_ratio(self) -> float:
        return self.__fsr_min_ratio

    @fsr_min_ratio.setter
    def fsr_min_ratio(self, value: float):
        self._property_changed('fsr_min_ratio')
        self.__fsr_min_ratio = value        

    @property
    def module_enabled(self) -> bool:
        """Enable to disable the module"""
        return self.__module_enabled

    @module_enabled.setter
    def module_enabled(self, value: bool):
        self._property_changed('module_enabled')
        self.__module_enabled = value        

    @property
    def trend_signal_0(self) -> bool:
        return self.__trend_signal_0

    @trend_signal_0.setter
    def trend_signal_0(self, value: bool):
        self._property_changed('trend_signal_0')
        self.__trend_signal_0 = value        

    @property
    def trend_signal_1(self) -> bool:
        return self.__trend_signal_1

    @trend_signal_1.setter
    def trend_signal_1(self, value: bool):
        self._property_changed('trend_signal_1')
        self.__trend_signal_1 = value        

    @property
    def trend_signal_2(self) -> bool:
        return self.__trend_signal_2

    @trend_signal_2.setter
    def trend_signal_2(self, value: bool):
        self._property_changed('trend_signal_2')
        self.__trend_signal_2 = value        

    @property
    def trend_signal_3(self) -> bool:
        return self.__trend_signal_3

    @trend_signal_3.setter
    def trend_signal_3(self, value: bool):
        self._property_changed('trend_signal_3')
        self.__trend_signal_3 = value        

    @property
    def module_name(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__module_name

    @module_name.setter
    def module_name(self, value: str):
        self._property_changed('module_name')
        self.__module_name = value        

    @property
    def target_strike(self) -> float:
        return self.__target_strike

    @target_strike.setter
    def target_strike(self, value: float):
        self._property_changed('target_strike')
        self.__target_strike = value        

    @property
    def strike_method(self) -> Union[StrikeMethodType, str]:
        return self.__strike_method

    @strike_method.setter
    def strike_method(self, value: Union[StrikeMethodType, str]):
        self._property_changed('strike_method')
        self.__strike_method = get_enum_value(StrikeMethodType, value)        

    @property
    def option_expiry(self) -> Union[OptionExpiryType, str]:
        return self.__option_expiry

    @option_expiry.setter
    def option_expiry(self, value: Union[OptionExpiryType, str]):
        self._property_changed('option_expiry')
        self.__option_expiry = get_enum_value(OptionExpiryType, value)        

    @property
    def bloomberg_id(self) -> str:
        return self.__bloomberg_id

    @bloomberg_id.setter
    def bloomberg_id(self, value: str):
        self._property_changed('bloomberg_id')
        self.__bloomberg_id = value        

    @property
    def stock_id(self) -> str:
        return self.__stock_id

    @stock_id.setter
    def stock_id(self, value: str):
        self._property_changed('stock_id')
        self.__stock_id = value        

    @property
    def future_id(self) -> str:
        return self.__future_id

    @future_id.setter
    def future_id(self, value: str):
        self._property_changed('future_id')
        self.__future_id = value        

    @property
    def ric(self) -> str:
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def new_weight(self) -> float:
        return self.__new_weight

    @new_weight.setter
    def new_weight(self, value: float):
        self._property_changed('new_weight')
        self.__new_weight = value        

    @property
    def execution_participation_rate(self) -> float:
        """Execution Participation Rate"""
        return self.__execution_participation_rate

    @execution_participation_rate.setter
    def execution_participation_rate(self, value: float):
        self._property_changed('execution_participation_rate')
        self.__execution_participation_rate = value        

    @property
    def new_shares(self) -> float:
        return self.__new_shares

    @new_shares.setter
    def new_shares(self, value: float):
        self._property_changed('new_shares')
        self.__new_shares = value        

    @property
    def new_lots(self) -> float:
        return self.__new_lots

    @new_lots.setter
    def new_lots(self, value: float):
        self._property_changed('new_lots')
        self.__new_lots = value        

    @property
    def execution_start_time(self) -> dict:
        """When to start executing"""
        return self.__execution_start_time

    @execution_start_time.setter
    def execution_start_time(self, value: dict):
        self._property_changed('execution_start_time')
        self.__execution_start_time = value        

    @property
    def execution_end_time(self) -> dict:
        """When to stop executing"""
        return self.__execution_end_time

    @execution_end_time.setter
    def execution_end_time(self, value: dict):
        self._property_changed('execution_end_time')
        self.__execution_end_time = value        

    @property
    def execution_style(self) -> str:
        """String representing the execution style"""
        return self.__execution_style

    @execution_style.setter
    def execution_style(self, value: str):
        self._property_changed('execution_style')
        self.__execution_style = value        

    @property
    def execution_timezone(self) -> str:
        """String representing the time zone"""
        return self.__execution_timezone

    @execution_timezone.setter
    def execution_timezone(self, value: str):
        self._property_changed('execution_timezone')
        self.__execution_timezone = value        

    @property
    def notional(self) -> float:
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def leverage(self) -> float:
        return self.__leverage

    @leverage.setter
    def leverage(self, value: float):
        self._property_changed('leverage')
        self.__leverage = value        

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def hedge_ratio(self) -> float:
        return self.__hedge_ratio

    @hedge_ratio.setter
    def hedge_ratio(self, value: float):
        self._property_changed('hedge_ratio')
        self.__hedge_ratio = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        """Option Type"""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def option_strike_type(self) -> Union[OptionStrikeType, str]:
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: Union[OptionStrikeType, str]):
        self._property_changed('option_strike_type')
        self.__option_strike_type = get_enum_value(OptionStrikeType, value)        

    @property
    def credit_option_type(self) -> Union[CreditOptionType, str]:
        return self.__credit_option_type

    @credit_option_type.setter
    def credit_option_type(self, value: Union[CreditOptionType, str]):
        self._property_changed('credit_option_type')
        self.__credit_option_type = get_enum_value(CreditOptionType, value)        

    @property
    def credit_option_strike_type(self) -> Union[CreditOptionStrikeType, str]:
        return self.__credit_option_strike_type

    @credit_option_strike_type.setter
    def credit_option_strike_type(self, value: Union[CreditOptionStrikeType, str]):
        self._property_changed('credit_option_strike_type')
        self.__credit_option_strike_type = get_enum_value(CreditOptionStrikeType, value)        

    @property
    def strike_relative(self) -> float:
        return self.__strike_relative

    @strike_relative.setter
    def strike_relative(self, value: float):
        self._property_changed('strike_relative')
        self.__strike_relative = value        

    @property
    def trade_type(self) -> Union[TradeType, str]:
        """Direction"""
        return self.__trade_type

    @trade_type.setter
    def trade_type(self, value: Union[TradeType, str]):
        self._property_changed('trade_type')
        self.__trade_type = get_enum_value(TradeType, value)        

    @property
    def signal(self) -> float:
        return self.__signal

    @signal.setter
    def signal(self, value: float):
        self._property_changed('signal')
        self.__signal = value        

    @property
    def new_signal(self) -> float:
        return self.__new_signal

    @new_signal.setter
    def new_signal(self, value: float):
        self._property_changed('new_signal')
        self.__new_signal = value        

    @property
    def new_min_weight(self) -> float:
        return self.__new_min_weight

    @new_min_weight.setter
    def new_min_weight(self, value: float):
        self._property_changed('new_min_weight')
        self.__new_min_weight = value        

    @property
    def new_max_weight(self) -> float:
        return self.__new_max_weight

    @new_max_weight.setter
    def new_max_weight(self, value: float):
        self._property_changed('new_max_weight')
        self.__new_max_weight = value        

    @property
    def min_weight(self) -> float:
        return self.__min_weight

    @min_weight.setter
    def min_weight(self, value: float):
        self._property_changed('min_weight')
        self.__min_weight = value        

    @property
    def max_weight(self) -> float:
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, value: float):
        self._property_changed('max_weight')
        self.__max_weight = value        

    @property
    def weight_smoothing_window(self) -> float:
        return self.__weight_smoothing_window

    @weight_smoothing_window.setter
    def weight_smoothing_window(self, value: float):
        self._property_changed('weight_smoothing_window')
        self.__weight_smoothing_window = value        

    @property
    def election(self) -> str:
        return self.__election

    @election.setter
    def election(self, value: str):
        self._property_changed('election')
        self.__election = value        

    @property
    def base_date(self) -> str:
        """The base date type to use for the nearby contract roll"""
        return self.__base_date

    @base_date.setter
    def base_date(self, value: str):
        self._property_changed('base_date')
        self.__base_date = value        

    @property
    def commodity(self) -> str:
        """The commodity symbol for the module"""
        return self.__commodity

    @commodity.setter
    def commodity(self, value: str):
        self._property_changed('commodity')
        self.__commodity = value        

    @property
    def component_weight(self) -> float:
        """The weight allocated to the specified module"""
        return self.__component_weight

    @component_weight.setter
    def component_weight(self, value: float):
        self._property_changed('component_weight')
        self.__component_weight = value        

    @property
    def contract_nearby_number(self) -> float:
        """The nearby contract to roll into"""
        return self.__contract_nearby_number

    @contract_nearby_number.setter
    def contract_nearby_number(self, value: float):
        self._property_changed('contract_nearby_number')
        self.__contract_nearby_number = value        

    @property
    def expiration_schedule(self) -> str:
        """The contract expiration schedule to be used"""
        return self.__expiration_schedule

    @expiration_schedule.setter
    def expiration_schedule(self, value: str):
        self._property_changed('expiration_schedule')
        self.__expiration_schedule = value        

    @property
    def fixing_type(self) -> str:
        """Type of fixing used to determine the price"""
        return self.__fixing_type

    @fixing_type.setter
    def fixing_type(self, value: str):
        self._property_changed('fixing_type')
        self.__fixing_type = value        

    @property
    def last_eligible_date(self) -> float:
        """The last eligible date for the roll"""
        return self.__last_eligible_date

    @last_eligible_date.setter
    def last_eligible_date(self, value: float):
        self._property_changed('last_eligible_date')
        self.__last_eligible_date = value        

    @property
    def num_roll_days(self) -> float:
        """The number of days over which the roll is spread"""
        return self.__num_roll_days

    @num_roll_days.setter
    def num_roll_days(self, value: float):
        self._property_changed('num_roll_days')
        self.__num_roll_days = value        

    @property
    def roll_end(self) -> float:
        """Day on which to end the roll"""
        return self.__roll_end

    @roll_end.setter
    def roll_end(self, value: float):
        self._property_changed('roll_end')
        self.__roll_end = value        

    @property
    def roll_start(self) -> float:
        """Day on which to start the roll"""
        return self.__roll_start

    @roll_start.setter
    def roll_start(self, value: float):
        self._property_changed('roll_start')
        self.__roll_start = value        

    @property
    def roll_type(self) -> str:
        """Type of contract roll"""
        return self.__roll_type

    @roll_type.setter
    def roll_type(self, value: str):
        self._property_changed('roll_type')
        self.__roll_type = value        

    @property
    def valid_contract_expiry(self) -> str:
        """The valid contract expiry months"""
        return self.__valid_contract_expiry

    @valid_contract_expiry.setter
    def valid_contract_expiry(self, value: str):
        self._property_changed('valid_contract_expiry')
        self.__valid_contract_expiry = value        


class LiveMarket(Base):
        
    """Live market"""

    @camel_case_translate
    def __init__(
        self,
        location: Union[PricingLocation, str],
        name: str = None
    ):        
        super().__init__()
        self.location = location
        self.name = name

    @property
    def market_type(self) -> str:
        """LiveMarket"""
        return 'LiveMarket'        

    @property
    def location(self) -> Union[PricingLocation, str]:
        """Location for the market data"""
        return self.__location

    @location.setter
    def location(self, value: Union[PricingLocation, str]):
        self._property_changed('location')
        self.__location = get_enum_value(PricingLocation, value)        


class MarketDataCoordinateValue(Base):
        
    """Market data coordinate and value"""

    @camel_case_translate
    def __init__(
        self,
        coordinate: MarketDataCoordinate,
        value: float,
        name: str = None
    ):        
        super().__init__()
        self.coordinate = coordinate
        self.value = value
        self.name = name

    @property
    def coordinate(self) -> MarketDataCoordinate:
        """Market data coordinate"""
        return self.__coordinate

    @coordinate.setter
    def coordinate(self, value: MarketDataCoordinate):
        self._property_changed('coordinate')
        self.__coordinate = value        

    @property
    def value(self) -> float:
        """Value for the coordinate"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        


class MarketDataPattern(Base):
        
    """A pattern used to match market coordinates"""

    @camel_case_translate
    def __init__(
        self,
        mkt_type: str = None,
        mkt_asset: str = None,
        mkt_class: str = None,
        mkt_point: Tuple[str, ...] = None,
        mkt_quoting_style: str = None,
        is_active: bool = None,
        is_investment_grade: bool = None,
        currency: Union[Currency, str] = None,
        country_code: Union[CountryCode, str] = None,
        gics_sector: str = None,
        gics_industry_group: str = None,
        gics_industry: str = None,
        gics_sub_industry: str = None,
        name: str = None
    ):        
        super().__init__()
        self.mkt_type = mkt_type
        self.mkt_asset = mkt_asset
        self.mkt_class = mkt_class
        self.mkt_point = mkt_point
        self.mkt_quoting_style = mkt_quoting_style
        self.is_active = is_active
        self.is_investment_grade = is_investment_grade
        self.currency = currency
        self.country_code = country_code
        self.gics_sector = gics_sector
        self.gics_industry_group = gics_industry_group
        self.gics_industry = gics_industry
        self.gics_sub_industry = gics_sub_industry
        self.name = name

    @property
    def mkt_type(self) -> str:
        """The Market Data Type, e.g. IR, IR_BASIS, FX, FX_Vol"""
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: str):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def mkt_asset(self) -> str:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: str):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def mkt_class(self) -> str:
        """The market data pointClass, e.g. Swap, Cash."""
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: str):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def mkt_point(self) -> Tuple[str, ...]:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__mkt_point

    @mkt_point.setter
    def mkt_point(self, value: Tuple[str, ...]):
        self._property_changed('mkt_point')
        self.__mkt_point = value        

    @property
    def mkt_quoting_style(self) -> str:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: str):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        

    @property
    def is_active(self) -> bool:
        """Is the asset active"""
        return self.__is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._property_changed('is_active')
        self.__is_active = value        

    @property
    def is_investment_grade(self) -> bool:
        """Is the asset investment grade"""
        return self.__is_investment_grade

    @is_investment_grade.setter
    def is_investment_grade(self, value: bool):
        self._property_changed('is_investment_grade')
        self.__is_investment_grade = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def country_code(self) -> Union[CountryCode, str]:
        """ISO Country code"""
        return self.__country_code

    @country_code.setter
    def country_code(self, value: Union[CountryCode, str]):
        self._property_changed('country_code')
        self.__country_code = get_enum_value(CountryCode, value)        

    @property
    def gics_sector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gics_sector

    @gics_sector.setter
    def gics_sector(self, value: str):
        self._property_changed('gics_sector')
        self.__gics_sector = value        

    @property
    def gics_industry_group(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gics_industry_group

    @gics_industry_group.setter
    def gics_industry_group(self, value: str):
        self._property_changed('gics_industry_group')
        self.__gics_industry_group = value        

    @property
    def gics_industry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gics_industry

    @gics_industry.setter
    def gics_industry(self, value: str):
        self._property_changed('gics_industry')
        self.__gics_industry = value        

    @property
    def gics_sub_industry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gics_sub_industry

    @gics_sub_industry.setter
    def gics_sub_industry(self, value: str):
        self._property_changed('gics_sub_industry')
        self.__gics_sub_industry = value        


class MarketDataShock(Base):
        
    """A shock to apply to market coordinate values"""

    @camel_case_translate
    def __init__(
        self,
        shock_type: Union[MarketDataShockType, str],
        value: float,
        precision: float = None,
        cap: float = None,
        floor: float = None,
        coordinate_cap: float = None,
        coordinate_floor: float = None,
        name: str = None
    ):        
        super().__init__()
        self.shock_type = shock_type
        self.value = value
        self.precision = precision
        self.cap = cap
        self.floor = floor
        self.coordinate_cap = coordinate_cap
        self.coordinate_floor = coordinate_floor
        self.name = name

    @property
    def shock_type(self) -> Union[MarketDataShockType, str]:
        """Market data shock type"""
        return self.__shock_type

    @shock_type.setter
    def shock_type(self, value: Union[MarketDataShockType, str]):
        self._property_changed('shock_type')
        self.__shock_type = get_enum_value(MarketDataShockType, value)        

    @property
    def value(self) -> float:
        """The amount by which to shock matching coordinates"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def precision(self) -> float:
        """The precision to which the shock will be rounded"""
        return self.__precision

    @precision.setter
    def precision(self, value: float):
        self._property_changed('precision')
        self.__precision = value        

    @property
    def cap(self) -> float:
        """Upper bound on the shocked value"""
        return self.__cap

    @cap.setter
    def cap(self, value: float):
        self._property_changed('cap')
        self.__cap = value        

    @property
    def floor(self) -> float:
        """Lower bound on the shocked value"""
        return self.__floor

    @floor.setter
    def floor(self, value: float):
        self._property_changed('floor')
        self.__floor = value        

    @property
    def coordinate_cap(self) -> float:
        """Upper bound on the pre-shocked value of matching coordinates"""
        return self.__coordinate_cap

    @coordinate_cap.setter
    def coordinate_cap(self, value: float):
        self._property_changed('coordinate_cap')
        self.__coordinate_cap = value        

    @property
    def coordinate_floor(self) -> float:
        """Lower bound on the pre-shocked value of matching coordinates"""
        return self.__coordinate_floor

    @coordinate_floor.setter
    def coordinate_floor(self, value: float):
        self._property_changed('coordinate_floor')
        self.__coordinate_floor = value        


class PCOBenchmark(Base):
        
    """Parameters required for PCO Benchmark"""

    @camel_case_translate
    def __init__(
        self,
        selected: str = None,
        options: Tuple[PCOBenchmarkOptions, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.selected = selected
        self.options = options
        self.name = name

    @property
    def selected(self) -> str:
        return self.__selected

    @selected.setter
    def selected(self, value: str):
        self._property_changed('selected')
        self.__selected = value        

    @property
    def options(self) -> Tuple[PCOBenchmarkOptions, ...]:
        """Parameters required for PCO Benchmark"""
        return self.__options

    @options.setter
    def options(self, value: Tuple[PCOBenchmarkOptions, ...]):
        self._property_changed('options')
        self.__options = value        


class PCOCashBalance(Base):
        
    """Parameters required for PCO Cash Balance"""

    @camel_case_translate
    def __init__(
        self,
        local_currency: Union[Currency, str] = None,
        cash_balance_limits: Tuple[str, ...] = None,
        cash_reserve: str = None,
        long_threshold: str = None,
        short_threshold: str = None,
        name: str = None
    ):        
        super().__init__()
        self.local_currency = local_currency
        self.cash_balance_limits = cash_balance_limits
        self.cash_reserve = cash_reserve
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold
        self.name = name

    @property
    def local_currency(self) -> Union[Currency, str]:
        """Local currency"""
        return self.__local_currency

    @local_currency.setter
    def local_currency(self, value: Union[Currency, str]):
        self._property_changed('local_currency')
        self.__local_currency = get_enum_value(Currency, value)        

    @property
    def cash_balance_limits(self) -> Tuple[str, ...]:
        """Upper and lower limits for cash balance"""
        return self.__cash_balance_limits

    @cash_balance_limits.setter
    def cash_balance_limits(self, value: Tuple[str, ...]):
        self._property_changed('cash_balance_limits')
        self.__cash_balance_limits = value        

    @property
    def cash_reserve(self) -> str:
        """Target cash reserve"""
        return self.__cash_reserve

    @cash_reserve.setter
    def cash_reserve(self, value: str):
        self._property_changed('cash_reserve')
        self.__cash_reserve = value        

    @property
    def long_threshold(self) -> str:
        """Long cash threshold"""
        return self.__long_threshold

    @long_threshold.setter
    def long_threshold(self, value: str):
        self._property_changed('long_threshold')
        self.__long_threshold = value        

    @property
    def short_threshold(self) -> str:
        """Short cash threshold"""
        return self.__short_threshold

    @short_threshold.setter
    def short_threshold(self, value: str):
        self._property_changed('short_threshold')
        self.__short_threshold = value        


class PCOParameterValues(Base):
        
    """Parameters required for a PCO Generic Value"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str] = None,
        value: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.value = value
        self.name = name

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def value(self) -> Union[float, str]:
        """Generic value for a PCO parameter"""
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


class PCOSettlements(Base):
        
    """Parameters required for a PCO Settlement"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str] = None,
        data: Tuple[PCOSettlementsData, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.data = data
        self.name = name

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def data(self) -> Tuple[PCOSettlementsData, ...]:
        """Parameters required for a PCO Settlement"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[PCOSettlementsData, ...]):
        self._property_changed('data')
        self.__data = value        


class PCOShareClass(Base):
        
    """Parameters required for PCO Share Class"""

    @camel_case_translate
    def __init__(
        self,
        total_net_assets: str = None,
        estimated_switch: str = None,
        estimated_net_subscription_effective_date: datetime.datetime = None,
        confirmed_net_subscription_effective_date: datetime.datetime = None,
        estimated_net_dividend: str = None,
        confirmed_net_dividend: str = None,
        net_subscriptions: Tuple[PCONetSubscription, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.total_net_assets = total_net_assets
        self.estimated_switch = estimated_switch
        self.estimated_net_subscription_effective_date = estimated_net_subscription_effective_date
        self.confirmed_net_subscription_effective_date = confirmed_net_subscription_effective_date
        self.estimated_net_dividend = estimated_net_dividend
        self.confirmed_net_dividend = confirmed_net_dividend
        self.net_subscriptions = net_subscriptions
        self.name = name

    @property
    def total_net_assets(self) -> str:
        """Total net assets of a share class"""
        return self.__total_net_assets

    @total_net_assets.setter
    def total_net_assets(self, value: str):
        self._property_changed('total_net_assets')
        self.__total_net_assets = value        

    @property
    def estimated_switch(self) -> str:
        """Estimated switch provided by client for a share class"""
        return self.__estimated_switch

    @estimated_switch.setter
    def estimated_switch(self, value: str):
        self._property_changed('estimated_switch')
        self.__estimated_switch = value        

    @property
    def estimated_net_subscription_effective_date(self) -> datetime.datetime:
        """Effective date for estimated net subscription"""
        return self.__estimated_net_subscription_effective_date

    @estimated_net_subscription_effective_date.setter
    def estimated_net_subscription_effective_date(self, value: datetime.datetime):
        self._property_changed('estimated_net_subscription_effective_date')
        self.__estimated_net_subscription_effective_date = value        

    @property
    def confirmed_net_subscription_effective_date(self) -> datetime.datetime:
        """Confirmed date for estimated net subscription"""
        return self.__confirmed_net_subscription_effective_date

    @confirmed_net_subscription_effective_date.setter
    def confirmed_net_subscription_effective_date(self, value: datetime.datetime):
        self._property_changed('confirmed_net_subscription_effective_date')
        self.__confirmed_net_subscription_effective_date = value        

    @property
    def estimated_net_dividend(self) -> str:
        """Estimated net dividend provided by client for a share class"""
        return self.__estimated_net_dividend

    @estimated_net_dividend.setter
    def estimated_net_dividend(self, value: str):
        self._property_changed('estimated_net_dividend')
        self.__estimated_net_dividend = value        

    @property
    def confirmed_net_dividend(self) -> str:
        """Confirmed net dividend provided by client for a share class"""
        return self.__confirmed_net_dividend

    @confirmed_net_dividend.setter
    def confirmed_net_dividend(self, value: str):
        self._property_changed('confirmed_net_dividend')
        self.__confirmed_net_dividend = value        

    @property
    def net_subscriptions(self) -> Tuple[PCONetSubscription, ...]:
        """Net subscriptions provided by client for a share class"""
        return self.__net_subscriptions

    @net_subscriptions.setter
    def net_subscriptions(self, value: Tuple[PCONetSubscription, ...]):
        self._property_changed('net_subscriptions')
        self.__net_subscriptions = value        


class PCOTargetDeviation(Base):
        
    """Parameters required for a Target Deviation"""

    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str] = None,
        data: Tuple[PCOTargetDeviationData, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency = currency
        self.data = data
        self.name = name

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def data(self) -> Tuple[PCOTargetDeviationData, ...]:
        """Parameters required for a Target Deviation data"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[PCOTargetDeviationData, ...]):
        self._property_changed('data')
        self.__data = value        


class PCOUnrealisedMarkToMarket(Base):
        
    """Parameters required for a Unrealised mark to market."""

    @camel_case_translate
    def __init__(
        self,
        total: str = None,
        next_settlement_date: datetime.datetime = None,
        next_settlement: str = None,
        next_roll_date: datetime.datetime = None,
        historical_data: Tuple[PCOMtMHistoricalData, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.total = total
        self.next_settlement_date = next_settlement_date
        self.next_settlement = next_settlement
        self.next_roll_date = next_roll_date
        self.historical_data = historical_data
        self.name = name

    @property
    def total(self) -> str:
        """Total indicative unrealised mark to market value"""
        return self.__total

    @total.setter
    def total(self, value: str):
        self._property_changed('total')
        self.__total = value        

    @property
    def next_settlement_date(self) -> datetime.datetime:
        """Next settlement date"""
        return self.__next_settlement_date

    @next_settlement_date.setter
    def next_settlement_date(self, value: datetime.datetime):
        self._property_changed('next_settlement_date')
        self.__next_settlement_date = value        

    @property
    def next_settlement(self) -> str:
        """Next settlement value"""
        return self.__next_settlement

    @next_settlement.setter
    def next_settlement(self, value: str):
        self._property_changed('next_settlement')
        self.__next_settlement = value        

    @property
    def next_roll_date(self) -> datetime.datetime:
        """Next roll date"""
        return self.__next_roll_date

    @next_roll_date.setter
    def next_roll_date(self, value: datetime.datetime):
        self._property_changed('next_roll_date')
        self.__next_roll_date = value        

    @property
    def historical_data(self) -> Tuple[PCOMtMHistoricalData, ...]:
        """History of unrealised mark to market of open trades"""
        return self.__historical_data

    @historical_data.setter
    def historical_data(self, value: Tuple[PCOMtMHistoricalData, ...]):
        self._property_changed('historical_data')
        self.__historical_data = value        


class PerformanceStatsRequest(Base):
        
    """Performance statistics."""

    @camel_case_translate
    def __init__(
        self,
        annualized_return: Op = None,
        annualized_volatility: Op = None,
        best_month: Op = None,
        max_draw_down: Op = None,
        max_draw_down_duration: Op = None,
        positive_months: Op = None,
        sharpe_ratio: Op = None,
        sortino_ratio: Op = None,
        worst_month: Op = None,
        average_return: Op = None,
        name: str = None
    ):        
        super().__init__()
        self.annualized_return = annualized_return
        self.annualized_volatility = annualized_volatility
        self.best_month = best_month
        self.max_draw_down = max_draw_down
        self.max_draw_down_duration = max_draw_down_duration
        self.positive_months = positive_months
        self.sharpe_ratio = sharpe_ratio
        self.sortino_ratio = sortino_ratio
        self.worst_month = worst_month
        self.average_return = average_return
        self.name = name

    @property
    def annualized_return(self) -> Op:
        """Operations for searches."""
        return self.__annualized_return

    @annualized_return.setter
    def annualized_return(self, value: Op):
        self._property_changed('annualized_return')
        self.__annualized_return = value        

    @property
    def annualized_volatility(self) -> Op:
        """Operations for searches."""
        return self.__annualized_volatility

    @annualized_volatility.setter
    def annualized_volatility(self, value: Op):
        self._property_changed('annualized_volatility')
        self.__annualized_volatility = value        

    @property
    def best_month(self) -> Op:
        """Operations for searches."""
        return self.__best_month

    @best_month.setter
    def best_month(self, value: Op):
        self._property_changed('best_month')
        self.__best_month = value        

    @property
    def max_draw_down(self) -> Op:
        """Operations for searches."""
        return self.__max_draw_down

    @max_draw_down.setter
    def max_draw_down(self, value: Op):
        self._property_changed('max_draw_down')
        self.__max_draw_down = value        

    @property
    def max_draw_down_duration(self) -> Op:
        """Operations for searches."""
        return self.__max_draw_down_duration

    @max_draw_down_duration.setter
    def max_draw_down_duration(self, value: Op):
        self._property_changed('max_draw_down_duration')
        self.__max_draw_down_duration = value        

    @property
    def positive_months(self) -> Op:
        """Operations for searches."""
        return self.__positive_months

    @positive_months.setter
    def positive_months(self, value: Op):
        self._property_changed('positive_months')
        self.__positive_months = value        

    @property
    def sharpe_ratio(self) -> Op:
        """Operations for searches."""
        return self.__sharpe_ratio

    @sharpe_ratio.setter
    def sharpe_ratio(self, value: Op):
        self._property_changed('sharpe_ratio')
        self.__sharpe_ratio = value        

    @property
    def sortino_ratio(self) -> Op:
        """Operations for searches."""
        return self.__sortino_ratio

    @sortino_ratio.setter
    def sortino_ratio(self, value: Op):
        self._property_changed('sortino_ratio')
        self.__sortino_ratio = value        

    @property
    def worst_month(self) -> Op:
        """Operations for searches."""
        return self.__worst_month

    @worst_month.setter
    def worst_month(self, value: Op):
        self._property_changed('worst_month')
        self.__worst_month = value        

    @property
    def average_return(self) -> Op:
        """Operations for searches."""
        return self.__average_return

    @average_return.setter
    def average_return(self, value: Op):
        self._property_changed('average_return')
        self.__average_return = value        


class RollFwd(Scenario):
        
    """A scenario to manipulate time along the forward curve"""

    @camel_case_translate
    def __init__(
        self,
        date: Union[datetime.date, str] = None,
        realise_fwd: bool = True,
        holiday_calendar: Union[PricingLocation, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.realise_fwd = realise_fwd
        self.holiday_calendar = holiday_calendar
        self.name = name

    @property
    def scenario_type(self) -> str:
        """RollFwd"""
        return 'RollFwd'        

    @property
    def date(self) -> Union[datetime.date, str]:
        """Absolute or Relative Date to shift markets to"""
        return self.__date

    @date.setter
    def date(self, value: Union[datetime.date, str]):
        self._property_changed('date')
        self.__date = value        

    @property
    def realise_fwd(self) -> bool:
        """Roll along the forward curve or roll in spot space"""
        return self.__realise_fwd

    @realise_fwd.setter
    def realise_fwd(self, value: bool):
        self._property_changed('realise_fwd')
        self.__realise_fwd = value        

    @property
    def holiday_calendar(self) -> Union[PricingLocation, str]:
        """Calendar to use for relative dates"""
        return self.__holiday_calendar

    @holiday_calendar.setter
    def holiday_calendar(self, value: Union[PricingLocation, str]):
        self._property_changed('holiday_calendar')
        self.__holiday_calendar = get_enum_value(PricingLocation, value)        


class TimestampedMarket(Base):
        
    """Timestamped market"""

    @camel_case_translate
    def __init__(
        self,
        timestamp: datetime.datetime,
        location: Union[PricingLocation, str],
        name: str = None
    ):        
        super().__init__()
        self.timestamp = timestamp
        self.location = location
        self.name = name

    @property
    def market_type(self) -> str:
        """TimestampedMarket"""
        return 'TimestampedMarket'        

    @property
    def timestamp(self) -> datetime.datetime:
        """Timestamp for the market data"""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        self._property_changed('timestamp')
        self.__timestamp = value        

    @property
    def location(self) -> Union[PricingLocation, str]:
        """Location for the market data"""
        return self.__location

    @location.setter
    def location(self, value: Union[PricingLocation, str]):
        self._property_changed('location')
        self.__location = get_enum_value(PricingLocation, value)        


class AssetStatsRequest(Base):
        
    """Performance statistics."""

    @camel_case_translate
    def __init__(
        self,
        last_updated_time: DateRange = None,
        period: Union[AssetStatsPeriod, str] = None,
        type_: Union[AssetStatsType, str] = None,
        stats: PerformanceStatsRequest = None,
        name: str = None
    ):        
        super().__init__()
        self.last_updated_time = last_updated_time
        self.period = period
        self.__type = get_enum_value(AssetStatsType, type_)
        self.stats = stats
        self.name = name

    @property
    def last_updated_time(self) -> DateRange:
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: DateRange):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def period(self) -> Union[AssetStatsPeriod, str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union[AssetStatsPeriod, str]):
        self._property_changed('period')
        self.__period = get_enum_value(AssetStatsPeriod, value)        

    @property
    def type(self) -> Union[AssetStatsType, str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetStatsType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(AssetStatsType, value)        

    @property
    def stats(self) -> PerformanceStatsRequest:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: PerformanceStatsRequest):
        self._property_changed('stats')
        self.__stats = value        


class CSLCurrencyArray(Base):
        
    """An array of currencies"""

    @camel_case_translate
    def __init__(
        self,
        currency_values: Tuple[CSLCurrency, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency_values = currency_values
        self.name = name

    @property
    def currency_values(self) -> Tuple[CSLCurrency, ...]:
        """A currency"""
        return self.__currency_values

    @currency_values.setter
    def currency_values(self, value: Tuple[CSLCurrency, ...]):
        self._property_changed('currency_values')
        self.__currency_values = value        


class CSLSchedule(Base):
        
    """A schedule"""

    @camel_case_translate
    def __init__(
        self,
        first_date: datetime.date = None,
        last_date: datetime.date = None,
        calendar_name: str = None,
        period: str = None,
        delay: str = None,
        business_day_convention: str = None,
        day_count_convention: str = None,
        days_per_term: str = None,
        delay_business_day_convention: str = None,
        delay_calendar_name: str = None,
        has_reset_date: bool = None,
        term_formula: str = None,
        extra_dates: Tuple[CSLDateArrayNamedParam, ...] = None,
        extra_dates_by_offset: Tuple[CSLSymCaseNamedParam, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.first_date = first_date
        self.last_date = last_date
        self.calendar_name = calendar_name
        self.period = period
        self.delay = delay
        self.business_day_convention = business_day_convention
        self.day_count_convention = day_count_convention
        self.days_per_term = days_per_term
        self.delay_business_day_convention = delay_business_day_convention
        self.delay_calendar_name = delay_calendar_name
        self.has_reset_date = has_reset_date
        self.term_formula = term_formula
        self.extra_dates = extra_dates
        self.extra_dates_by_offset = extra_dates_by_offset
        self.name = name

    @property
    def first_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__first_date

    @first_date.setter
    def first_date(self, value: datetime.date):
        self._property_changed('first_date')
        self.__first_date = value        

    @property
    def last_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__last_date

    @last_date.setter
    def last_date(self, value: datetime.date):
        self._property_changed('last_date')
        self.__last_date = value        

    @property
    def calendar_name(self) -> str:
        """The name of the holiday calendar"""
        return self.__calendar_name

    @calendar_name.setter
    def calendar_name(self, value: str):
        self._property_changed('calendar_name')
        self.__calendar_name = value        

    @property
    def period(self) -> str:
        """Tenor"""
        return self.__period

    @period.setter
    def period(self, value: str):
        self._property_changed('period')
        self.__period = value        

    @property
    def delay(self) -> str:
        """The delay"""
        return self.__delay

    @delay.setter
    def delay(self, value: str):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def business_day_convention(self) -> str:
        return self.__business_day_convention

    @business_day_convention.setter
    def business_day_convention(self, value: str):
        self._property_changed('business_day_convention')
        self.__business_day_convention = value        

    @property
    def day_count_convention(self) -> str:
        return self.__day_count_convention

    @day_count_convention.setter
    def day_count_convention(self, value: str):
        self._property_changed('day_count_convention')
        self.__day_count_convention = value        

    @property
    def days_per_term(self) -> str:
        return self.__days_per_term

    @days_per_term.setter
    def days_per_term(self, value: str):
        self._property_changed('days_per_term')
        self.__days_per_term = value        

    @property
    def delay_business_day_convention(self) -> str:
        return self.__delay_business_day_convention

    @delay_business_day_convention.setter
    def delay_business_day_convention(self, value: str):
        self._property_changed('delay_business_day_convention')
        self.__delay_business_day_convention = value        

    @property
    def delay_calendar_name(self) -> str:
        """The name of the holiday calendar"""
        return self.__delay_calendar_name

    @delay_calendar_name.setter
    def delay_calendar_name(self, value: str):
        self._property_changed('delay_calendar_name')
        self.__delay_calendar_name = value        

    @property
    def has_reset_date(self) -> bool:
        return self.__has_reset_date

    @has_reset_date.setter
    def has_reset_date(self, value: bool):
        self._property_changed('has_reset_date')
        self.__has_reset_date = value        

    @property
    def term_formula(self) -> str:
        return self.__term_formula

    @term_formula.setter
    def term_formula(self, value: str):
        self._property_changed('term_formula')
        self.__term_formula = value        

    @property
    def extra_dates(self) -> Tuple[CSLDateArrayNamedParam, ...]:
        """A named array of dates"""
        return self.__extra_dates

    @extra_dates.setter
    def extra_dates(self, value: Tuple[CSLDateArrayNamedParam, ...]):
        self._property_changed('extra_dates')
        self.__extra_dates = value        

    @property
    def extra_dates_by_offset(self) -> Tuple[CSLSymCaseNamedParam, ...]:
        """A named case-sensitive string."""
        return self.__extra_dates_by_offset

    @extra_dates_by_offset.setter
    def extra_dates_by_offset(self, value: Tuple[CSLSymCaseNamedParam, ...]):
        self._property_changed('extra_dates_by_offset')
        self.__extra_dates_by_offset = value        


class CurveScenario(Scenario):
        
    """A scenario to manipulate curve shape"""

    @camel_case_translate
    def __init__(
        self,
        market_data_pattern: MarketDataPattern = None,
        parallel_shift: float = None,
        curve_shift: float = None,
        pivot_point: float = None,
        tenor_start: float = None,
        tenor_end: float = None,
        name: str = None
    ):        
        super().__init__()
        self.market_data_pattern = market_data_pattern
        self.parallel_shift = parallel_shift
        self.curve_shift = curve_shift
        self.pivot_point = pivot_point
        self.tenor_start = tenor_start
        self.tenor_end = tenor_end
        self.name = name

    @property
    def scenario_type(self) -> str:
        """CurveScenario"""
        return 'CurveScenario'        

    @property
    def market_data_pattern(self) -> MarketDataPattern:
        """Market pattern for matching curve assets"""
        return self.__market_data_pattern

    @market_data_pattern.setter
    def market_data_pattern(self, value: MarketDataPattern):
        self._property_changed('market_data_pattern')
        self.__market_data_pattern = value        

    @property
    def parallel_shift(self) -> float:
        """A constant (X bps) which shifts all points by the same amount"""
        return self.__parallel_shift

    @parallel_shift.setter
    def parallel_shift(self, value: float):
        self._property_changed('parallel_shift')
        self.__parallel_shift = value        

    @property
    def curve_shift(self) -> float:
        """A double which represents the net rate change (X bps) between tenorStart and
           tenorEnd"""
        return self.__curve_shift

    @curve_shift.setter
    def curve_shift(self, value: float):
        self._property_changed('curve_shift')
        self.__curve_shift = value        

    @property
    def pivot_point(self) -> float:
        """The tenor at which there is zero rate change, which is between tenorStart and
           tenorEnd inclusive, informing the type of curve shift"""
        return self.__pivot_point

    @pivot_point.setter
    def pivot_point(self, value: float):
        self._property_changed('pivot_point')
        self.__pivot_point = value        

    @property
    def tenor_start(self) -> float:
        """The tenor, in years, which is the starting point of the curve shift"""
        return self.__tenor_start

    @tenor_start.setter
    def tenor_start(self, value: float):
        self._property_changed('tenor_start')
        self.__tenor_start = value        

    @property
    def tenor_end(self) -> float:
        """The tenor, in years, which is the end point of the curve shift"""
        return self.__tenor_end

    @tenor_end.setter
    def tenor_end(self, value: float):
        self._property_changed('tenor_end')
        self.__tenor_end = value        


class FieldFilterMap(Base):
        
    _name_mappings = {'sec_db': 'secDB'}

    @camel_case_translate
    def __init__(
        self,
        **kwargs
    ):        
        super().__init__()
        self.internal_index_calc_region = kwargs.get('internal_index_calc_region')
        self.issue_status_date = kwargs.get('issue_status_date')
        self.pl_id = kwargs.get('pl_id')
        self.last_returns_start_date = kwargs.get('last_returns_start_date')
        self.amount_outstanding = kwargs.get('amount_outstanding')
        self.asset_classifications_gics_sub_industry = kwargs.get('asset_classifications_gics_sub_industry')
        self.mdapi_class = kwargs.get('mdapi_class')
        self.data_set_ids = kwargs.get('data_set_ids')
        self.call_first_date = kwargs.get('call_first_date')
        self.pb_client_id = kwargs.get('pb_client_id')
        self.asset_parameters_start = kwargs.get('asset_parameters_start')
        self.owner_id = kwargs.get('owner_id')
        self.economic_terms_hash = kwargs.get('economic_terms_hash')
        self.sec_db = kwargs.get('sec_db')
        self.objective = kwargs.get('objective')
        self.simon_intl_asset_tags = kwargs.get('simon_intl_asset_tags')
        self.private_placement_type = kwargs.get('private_placement_type')
        self.hedge_notional = kwargs.get('hedge_notional')
        self.rank = kwargs.get('rank')
        self.data_set_category = kwargs.get('data_set_category')
        self.pair_calculation = kwargs.get('pair_calculation')
        self.asset_parameters_index_family = kwargs.get('asset_parameters_index_family')
        self.created_by_id = kwargs.get('created_by_id')
        self.vehicle_type = kwargs.get('vehicle_type')
        self.market_data_type = kwargs.get('market_data_type')
        self.asset_parameters_payer_day_count_fraction = kwargs.get('asset_parameters_payer_day_count_fraction')
        self.point_class = kwargs.get('point_class')
        self.asset_parameters_cap_floor = kwargs.get('asset_parameters_cap_floor')
        self.minimum_increment = kwargs.get('minimum_increment')
        self.asset_parameters_payer_currency = kwargs.get('asset_parameters_payer_currency')
        self.settlement_date = kwargs.get('settlement_date')
        self.hedge_volatility = kwargs.get('hedge_volatility')
        self.version = kwargs.get('version')
        self.tags = kwargs.get('tags')
        self.asset_classifications_gics_industry_group = kwargs.get('asset_classifications_gics_industry_group')
        self.market_data_asset = kwargs.get('market_data_asset')
        self.asset_classifications_is_primary = kwargs.get('asset_classifications_is_primary')
        self.styles = kwargs.get('styles')
        self.short_name = kwargs.get('short_name')
        self.calculation_region = kwargs.get('calculation_region')
        self.eid = kwargs.get('eid')
        self.jsn = kwargs.get('jsn')
        self.mkt_quoting_style = kwargs.get('mkt_quoting_style')
        self.hurdle_type = kwargs.get('hurdle_type')
        self.mic = kwargs.get('mic')
        self.ps_id = kwargs.get('ps_id')
        self.issue_status = kwargs.get('issue_status')
        self.region_code = kwargs.get('region_code')
        self.dollar_cross = kwargs.get('dollar_cross')
        self.portfolio_type = kwargs.get('portfolio_type')
        self.vendor = kwargs.get('vendor')
        self.popularity = kwargs.get('popularity')
        self.term = kwargs.get('term')
        self.currency = kwargs.get('currency')
        self.real_time_restriction_status = kwargs.get('real_time_restriction_status')
        self.asset_parameters_clearing_house = kwargs.get('asset_parameters_clearing_house')
        self.rating_fitch = kwargs.get('rating_fitch')
        self.non_symbol_dimensions = kwargs.get('non_symbol_dimensions')
        self.asset_parameters_option_style = kwargs.get('asset_parameters_option_style')
        self.share_class_type = kwargs.get('share_class_type')
        self.asset_parameters_put_amount = kwargs.get('asset_parameters_put_amount')
        self.asset_parameters_floating_rate_designated_maturity = kwargs.get(
            'asset_parameters_floating_rate_designated_maturity')
        self.target_notional = kwargs.get('target_notional')
        self.asset_parameters_tenor = kwargs.get('asset_parameters_tenor')
        self.mkt_class = kwargs.get('mkt_class')
        self.delisted = kwargs.get('delisted')
        self.last_updated_since = kwargs.get('last_updated_since')
        self.regional_focus = kwargs.get('regional_focus')
        self.asset_parameters_payer_designated_maturity = kwargs.get('asset_parameters_payer_designated_maturity')
        self.tsdb_shortname = kwargs.get('tsdb_shortname')
        self.seasonal_adjustment_short = kwargs.get('seasonal_adjustment_short')
        self.asset_parameters_exchange_currency = kwargs.get('asset_parameters_exchange_currency')
        self.asset_classifications_country_name = kwargs.get('asset_classifications_country_name')
        self.management_fee = kwargs.get('management_fee')
        self.asset_parameters_settlement_date = kwargs.get('asset_parameters_settlement_date')
        self.rating_moodys = kwargs.get('rating_moodys')
        self.simon_id = kwargs.get('simon_id')
        self.development_status = kwargs.get('development_status')
        self.cusip = kwargs.get('cusip')
        self.notes = kwargs.get('notes')
        self.tags_to_exclude = kwargs.get('tags_to_exclude')
        self.asset_parameters_floating_rate_option = kwargs.get('asset_parameters_floating_rate_option')
        self.internal_index_calc_agent = kwargs.get('internal_index_calc_agent')
        self.rating_second_highest = kwargs.get('rating_second_highest')
        self.asset_classifications_country_code = kwargs.get('asset_classifications_country_code')
        self.frequency = kwargs.get('frequency')
        self.option_type = kwargs.get('option_type')
        self.data_set_sub_category = kwargs.get('data_set_sub_category')
        self.is_live = kwargs.get('is_live')
        self.is_legacy_pair_basket = kwargs.get('is_legacy_pair_basket')
        self.issuer_type = kwargs.get('issuer_type')
        self.asset_parameters_pricing_location = kwargs.get('asset_parameters_pricing_location')
        self.plot_id = kwargs.get('plot_id')
        self.asset_parameters_coupon = kwargs.get('asset_parameters_coupon')
        self.data_product = kwargs.get('data_product')
        self.mq_symbol = kwargs.get('mq_symbol')
        self.sectors = kwargs.get('sectors')
        self.redemption_notice_period = kwargs.get('redemption_notice_period')
        self.multiplier = kwargs.get('multiplier')
        self.asset_parameters_payer_rate_option = kwargs.get('asset_parameters_payer_rate_option')
        self.market_data_point = kwargs.get('market_data_point')
        self.external = kwargs.get('external')
        self.wpk = kwargs.get('wpk')
        self.sts_fx_currency = kwargs.get('sts_fx_currency')
        self.hedge_annualized_volatility = kwargs.get('hedge_annualized_volatility')
        self.name = kwargs.get('name')
        self.asset_parameters_expiration_date = kwargs.get('asset_parameters_expiration_date')
        self.aum = kwargs.get('aum')
        self.exchange = kwargs.get('exchange')
        self.folder_name = kwargs.get('folder_name')
        self.region = kwargs.get('region')
        self.cid = kwargs.get('cid')
        self.onboarded = kwargs.get('onboarded')
        self.live_date = kwargs.get('live_date')
        self.issue_price = kwargs.get('issue_price')
        self.sink_factor = kwargs.get('sink_factor')
        self.underlying_data_set_id = kwargs.get('underlying_data_set_id')
        self.asset_parameters_notional_amount_in_other_currency = kwargs.get(
            'asset_parameters_notional_amount_in_other_currency')
        self.asset_parameters_payer_frequency = kwargs.get('asset_parameters_payer_frequency')
        self.prime_id = kwargs.get('prime_id')
        self.asset_classifications_gics_sector = kwargs.get('asset_classifications_gics_sector')
        self.asset_parameters_pair = kwargs.get('asset_parameters_pair')
        self.sts_asset_name = kwargs.get('sts_asset_name')
        self.description = kwargs.get('description')
        self.asset_classifications_is_country_primary = kwargs.get('asset_classifications_is_country_primary')
        self.title = kwargs.get('title')
        self.net_exposure_classification = kwargs.get('net_exposure_classification')
        self.asset_parameters_strike_price = kwargs.get('asset_parameters_strike_price')
        self.coupon_type = kwargs.get('coupon_type')
        self.last_updated_by_id = kwargs.get('last_updated_by_id')
        self.clone_parent_id = kwargs.get('clone_parent_id')
        self.company = kwargs.get('company')
        self.gate_type = kwargs.get('gate_type')
        self.issue_date = kwargs.get('issue_date')
        self.expiration_date = kwargs.get('expiration_date')
        self.coverage = kwargs.get('coverage')
        self.ticker = kwargs.get('ticker')
        self.asset_parameters_receiver_rate_option = kwargs.get('asset_parameters_receiver_rate_option')
        self.call_last_date = kwargs.get('call_last_date')
        self.asset_parameters_payer_spread = kwargs.get('asset_parameters_payer_spread')
        self.sts_rates_country = kwargs.get('sts_rates_country')
        self.asset_parameters_premium_payment_date = kwargs.get('asset_parameters_premium_payment_date')
        self.latest_execution_time = kwargs.get('latest_execution_time')
        self.asset_parameters_forward_rate = kwargs.get('asset_parameters_forward_rate')
        self.asset_parameters_receiver_designated_maturity = kwargs.get(
            'asset_parameters_receiver_designated_maturity')
        self.gate = kwargs.get('gate')
        self.multi_tags = kwargs.get('multi_tags')
        self.gsn = kwargs.get('gsn')
        self.gss = kwargs.get('gss')
        self.rating_linear = kwargs.get('rating_linear')
        self.asset_class = kwargs.get('asset_class')
        self.asset_parameters_index = kwargs.get('asset_parameters_index')
        self.cm_id = kwargs.get('cm_id')
        self.__type = kwargs.get('type_')
        self.gsideid = kwargs.get('gsideid')
        self.mdapi = kwargs.get('mdapi')
        self.ric = kwargs.get('ric')
        self.issuer = kwargs.get('issuer')
        self.position_source_id = kwargs.get('position_source_id')
        self.measures = kwargs.get('measures')
        self.asset_parameters_floating_rate_day_count_fraction = kwargs.get(
            'asset_parameters_floating_rate_day_count_fraction')
        self.asset_parameters_notional_amount = kwargs.get('asset_parameters_notional_amount')
        self.action = kwargs.get('action')
        self.__id = kwargs.get('id_')
        self.asset_parameters_call_amount = kwargs.get('asset_parameters_call_amount')
        self.asset_parameters_seniority = kwargs.get('asset_parameters_seniority')
        self.redemption_date = kwargs.get('redemption_date')
        self.identifier = kwargs.get('identifier')
        self.index_create_source = kwargs.get('index_create_source')
        self.sec_name = kwargs.get('sec_name')
        self.sub_region = kwargs.get('sub_region')
        self.asset_parameters_receiver_day_count_fraction = kwargs.get('asset_parameters_receiver_day_count_fraction')
        self.asset_parameters_index2_tenor = kwargs.get('asset_parameters_index2_tenor')
        self.asset_parameters_notional_currency = kwargs.get('asset_parameters_notional_currency')
        self.sedol = kwargs.get('sedol')
        self.mkt_asset = kwargs.get('mkt_asset')
        self.rating_standard_and_poors = kwargs.get('rating_standard_and_poors')
        self.asset_types = kwargs.get('asset_types')
        self.bcid = kwargs.get('bcid')
        self.asset_parameters_credit_index_series = kwargs.get('asset_parameters_credit_index_series')
        self.gsid = kwargs.get('gsid')
        self.tdapi = kwargs.get('tdapi')
        self.last_updated_message = kwargs.get('last_updated_message')
        self.rcic = kwargs.get('rcic')
        self.trading_restriction = kwargs.get('trading_restriction')
        self.name_raw = kwargs.get('name_raw')
        self.status = kwargs.get('status')
        self.asset_parameters_pay_or_receive = kwargs.get('asset_parameters_pay_or_receive')
        self.client_name = kwargs.get('client_name')
        self.asset_parameters_index_series = kwargs.get('asset_parameters_index_series')
        self.asset_classifications_gics_industry = kwargs.get('asset_classifications_gics_industry')
        self.on_behalf_of = kwargs.get('on_behalf_of')
        self.increment = kwargs.get('increment')
        self.accrued_interest_standard = kwargs.get('accrued_interest_standard')
        self.enabled = kwargs.get('enabled')
        self.sts_commodity = kwargs.get('sts_commodity')
        self.sectors_raw = kwargs.get('sectors_raw')
        self.sts_commodity_sector = kwargs.get('sts_commodity_sector')
        self.asset_parameters_receiver_frequency = kwargs.get('asset_parameters_receiver_frequency')
        self.position_source_name = kwargs.get('position_source_name')
        self.gsid_equivalent = kwargs.get('gsid_equivalent')
        self.categories = kwargs.get('categories')
        self.symbol_dimensions = kwargs.get('symbol_dimensions')
        self.ext_mkt_asset = kwargs.get('ext_mkt_asset')
        self.asset_parameters_fixed_rate_frequency = kwargs.get('asset_parameters_fixed_rate_frequency')
        self.coupon = kwargs.get('coupon')
        self.side_pocket = kwargs.get('side_pocket')
        self.compliance_restricted_status = kwargs.get('compliance_restricted_status')
        self.quoting_style = kwargs.get('quoting_style')
        self.is_entity = kwargs.get('is_entity')
        self.scenario_group_id = kwargs.get('scenario_group_id')
        self.redemption_period = kwargs.get('redemption_period')
        self.asset_parameters_issuer_type = kwargs.get('asset_parameters_issuer_type')
        self.sts_credit_market = kwargs.get('sts_credit_market')
        self.bbid = kwargs.get('bbid')
        self.asset_classifications_risk_country_code = kwargs.get('asset_classifications_risk_country_code')
        self.asset_parameters_receiver_currency = kwargs.get('asset_parameters_receiver_currency')
        self.sts_em_dm = kwargs.get('sts_em_dm')
        self.issue_size = kwargs.get('issue_size')
        self.returns_enabled = kwargs.get('returns_enabled')
        self.seniority = kwargs.get('seniority')
        self.asset_parameters_settlement = kwargs.get('asset_parameters_settlement')
        self.asset_parameters_expiration_time = kwargs.get('asset_parameters_expiration_time')
        self.primary_country_ric = kwargs.get('primary_country_ric')
        self.is_pair_basket = kwargs.get('is_pair_basket')
        self.asset_parameters_index_version = kwargs.get('asset_parameters_index_version')
        self.asset_parameters_commodity_reference_price = kwargs.get('asset_parameters_commodity_reference_price')
        self.default_backcast = kwargs.get('default_backcast')
        self.use_machine_learning = kwargs.get('use_machine_learning')
        self.performance_fee = kwargs.get('performance_fee')
        self.report_type = kwargs.get('report_type')
        self.lockup_type = kwargs.get('lockup_type')
        self.lockup = kwargs.get('lockup')
        self.underlying_asset_ids = kwargs.get('underlying_asset_ids')
        self.asset_parameters_fee_currency = kwargs.get('asset_parameters_fee_currency')
        self.encoded_stats = kwargs.get('encoded_stats')
        self.pnode_id = kwargs.get('pnode_id')
        self.backtest_type = kwargs.get('backtest_type')
        self.asset_parameters_issuer = kwargs.get('asset_parameters_issuer')
        self.exchange_code = kwargs.get('exchange_code')
        self.asset_parameters_strike = kwargs.get('asset_parameters_strike')
        self.oe_id = kwargs.get('oe_id')
        self.asset_parameters_termination_date = kwargs.get('asset_parameters_termination_date')
        self.resource = kwargs.get('resource')
        self.asset_parameters_receiver_spread = kwargs.get('asset_parameters_receiver_spread')
        self.bbid_equivalent = kwargs.get('bbid_equivalent')
        self.hurdle = kwargs.get('hurdle')
        self.asset_parameters_effective_date = kwargs.get('asset_parameters_effective_date')
        self.valoren = kwargs.get('valoren')
        self.asset_parameters_fixed_rate_day_count_fraction = kwargs.get(
            'asset_parameters_fixed_rate_day_count_fraction')
        self.auto_tags = kwargs.get('auto_tags')
        self.short_description = kwargs.get('short_description')
        self.ext_mkt_class = kwargs.get('ext_mkt_class')
        self.mkt_point1 = kwargs.get('mkt_point1')
        self.portfolio_managers = kwargs.get('portfolio_managers')
        self.asset_parameters_commodity_sector = kwargs.get('asset_parameters_commodity_sector')
        self.hedge_tracking_error = kwargs.get('hedge_tracking_error')
        self.asset_parameters_put_currency = kwargs.get('asset_parameters_put_currency')
        self.asset_parameters_coupon_type = kwargs.get('asset_parameters_coupon_type')
        self.supra_strategy = kwargs.get('supra_strategy')
        self.term_status = kwargs.get('term_status')
        self.wi_id = kwargs.get('wi_id')
        self.market_cap_category = kwargs.get('market_cap_category')
        self.asset_parameters_call_currency = kwargs.get('asset_parameters_call_currency')
        self.mkt_point3 = kwargs.get('mkt_point3')
        self.display_id = kwargs.get('display_id')
        self.mkt_point2 = kwargs.get('mkt_point2')
        self.strike_price = kwargs.get('strike_price')
        self.mkt_point4 = kwargs.get('mkt_point4')
        self.risk_packages = kwargs.get('risk_packages')
        self.units = kwargs.get('units')
        self.em_id = kwargs.get('em_id')
        self.sts_credit_region = kwargs.get('sts_credit_region')
        self.country_id = kwargs.get('country_id')
        self.ext_mkt_point3 = kwargs.get('ext_mkt_point3')
        self.asset_classifications_risk_country_name = kwargs.get('asset_classifications_risk_country_name')
        self.asset_parameters_vendor = kwargs.get('asset_parameters_vendor')
        self.asset_parameters_index1_tenor = kwargs.get('asset_parameters_index1_tenor')
        self.mkt_type = kwargs.get('mkt_type')
        self.is_public = kwargs.get('is_public')
        self.alias = kwargs.get('alias')
        self.ext_mkt_point1 = kwargs.get('ext_mkt_point1')
        self.product_type = kwargs.get('product_type')
        self.ext_mkt_point2 = kwargs.get('ext_mkt_point2')
        self.sub_region_code = kwargs.get('sub_region_code')
        self.asset_parameters_option_type = kwargs.get('asset_parameters_option_type')
        self.asset_parameters_fixed_rate = kwargs.get('asset_parameters_fixed_rate')
        self.last_returns_end_date = kwargs.get('last_returns_end_date')
        self.tsdb_synced_symbol = kwargs.get('tsdb_synced_symbol')
        self.position_source_type = kwargs.get('position_source_type')
        self.minimum_denomination = kwargs.get('minimum_denomination')
        self.flagship = kwargs.get('flagship')
        self.lms_id = kwargs.get('lms_id')
        self.cross = kwargs.get('cross')
        self.in_code = kwargs.get('in_code')
        self.asset_parameters_strike_price_relative = kwargs.get('asset_parameters_strike_price_relative')
        self.sts_rates_maturity = kwargs.get('sts_rates_maturity')
        self.position_source = kwargs.get('position_source')
        self.listed = kwargs.get('listed')
        self.non_owner_id = kwargs.get('non_owner_id')
        self.shock_style = kwargs.get('shock_style')
        self.g10_currency = kwargs.get('g10_currency')
        self.strategy = kwargs.get('strategy')
        self.methodology = kwargs.get('methodology')
        self.isin = kwargs.get('isin')
        self.asset_parameters_strike_type = kwargs.get('asset_parameters_strike_type')

    @property
    def internal_index_calc_region(self) -> dict:
        return self.__internal_index_calc_region

    @internal_index_calc_region.setter
    def internal_index_calc_region(self, value: dict):
        self._property_changed('internal_index_calc_region')
        self.__internal_index_calc_region = value        

    @property
    def issue_status_date(self) -> dict:
        return self.__issue_status_date

    @issue_status_date.setter
    def issue_status_date(self, value: dict):
        self._property_changed('issue_status_date')
        self.__issue_status_date = value        

    @property
    def pl_id(self) -> dict:
        return self.__pl_id

    @pl_id.setter
    def pl_id(self, value: dict):
        self._property_changed('pl_id')
        self.__pl_id = value        

    @property
    def last_returns_start_date(self) -> dict:
        return self.__last_returns_start_date

    @last_returns_start_date.setter
    def last_returns_start_date(self, value: dict):
        self._property_changed('last_returns_start_date')
        self.__last_returns_start_date = value        

    @property
    def amount_outstanding(self) -> dict:
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: dict):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value        

    @property
    def asset_classifications_gics_sub_industry(self) -> dict:
        return self.__asset_classifications_gics_sub_industry

    @asset_classifications_gics_sub_industry.setter
    def asset_classifications_gics_sub_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_sub_industry')
        self.__asset_classifications_gics_sub_industry = value        

    @property
    def mdapi_class(self) -> dict:
        return self.__mdapi_class

    @mdapi_class.setter
    def mdapi_class(self, value: dict):
        self._property_changed('mdapi_class')
        self.__mdapi_class = value        

    @property
    def data_set_ids(self) -> dict:
        return self.__data_set_ids

    @data_set_ids.setter
    def data_set_ids(self, value: dict):
        self._property_changed('data_set_ids')
        self.__data_set_ids = value        

    @property
    def call_first_date(self) -> dict:
        return self.__call_first_date

    @call_first_date.setter
    def call_first_date(self, value: dict):
        self._property_changed('call_first_date')
        self.__call_first_date = value        

    @property
    def pb_client_id(self) -> dict:
        return self.__pb_client_id

    @pb_client_id.setter
    def pb_client_id(self, value: dict):
        self._property_changed('pb_client_id')
        self.__pb_client_id = value        

    @property
    def asset_parameters_start(self) -> dict:
        return self.__asset_parameters_start

    @asset_parameters_start.setter
    def asset_parameters_start(self, value: dict):
        self._property_changed('asset_parameters_start')
        self.__asset_parameters_start = value        

    @property
    def owner_id(self) -> dict:
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: dict):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def economic_terms_hash(self) -> dict:
        return self.__economic_terms_hash

    @economic_terms_hash.setter
    def economic_terms_hash(self, value: dict):
        self._property_changed('economic_terms_hash')
        self.__economic_terms_hash = value        

    @property
    def sec_db(self) -> dict:
        return self.__sec_db

    @sec_db.setter
    def sec_db(self, value: dict):
        self._property_changed('sec_db')
        self.__sec_db = value        

    @property
    def objective(self) -> dict:
        return self.__objective

    @objective.setter
    def objective(self, value: dict):
        self._property_changed('objective')
        self.__objective = value        

    @property
    def simon_intl_asset_tags(self) -> dict:
        return self.__simon_intl_asset_tags

    @simon_intl_asset_tags.setter
    def simon_intl_asset_tags(self, value: dict):
        self._property_changed('simon_intl_asset_tags')
        self.__simon_intl_asset_tags = value        

    @property
    def private_placement_type(self) -> dict:
        return self.__private_placement_type

    @private_placement_type.setter
    def private_placement_type(self, value: dict):
        self._property_changed('private_placement_type')
        self.__private_placement_type = value        

    @property
    def hedge_notional(self) -> dict:
        return self.__hedge_notional

    @hedge_notional.setter
    def hedge_notional(self, value: dict):
        self._property_changed('hedge_notional')
        self.__hedge_notional = value        

    @property
    def rank(self) -> dict:
        return self.__rank

    @rank.setter
    def rank(self, value: dict):
        self._property_changed('rank')
        self.__rank = value        

    @property
    def data_set_category(self) -> dict:
        return self.__data_set_category

    @data_set_category.setter
    def data_set_category(self, value: dict):
        self._property_changed('data_set_category')
        self.__data_set_category = value        

    @property
    def pair_calculation(self) -> dict:
        return self.__pair_calculation

    @pair_calculation.setter
    def pair_calculation(self, value: dict):
        self._property_changed('pair_calculation')
        self.__pair_calculation = value        

    @property
    def asset_parameters_index_family(self) -> dict:
        return self.__asset_parameters_index_family

    @asset_parameters_index_family.setter
    def asset_parameters_index_family(self, value: dict):
        self._property_changed('asset_parameters_index_family')
        self.__asset_parameters_index_family = value        

    @property
    def created_by_id(self) -> dict:
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: dict):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def vehicle_type(self) -> dict:
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: dict):
        self._property_changed('vehicle_type')
        self.__vehicle_type = value        

    @property
    def market_data_type(self) -> dict:
        return self.__market_data_type

    @market_data_type.setter
    def market_data_type(self, value: dict):
        self._property_changed('market_data_type')
        self.__market_data_type = value        

    @property
    def asset_parameters_payer_day_count_fraction(self) -> dict:
        return self.__asset_parameters_payer_day_count_fraction

    @asset_parameters_payer_day_count_fraction.setter
    def asset_parameters_payer_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_payer_day_count_fraction')
        self.__asset_parameters_payer_day_count_fraction = value        

    @property
    def point_class(self) -> dict:
        return self.__point_class

    @point_class.setter
    def point_class(self, value: dict):
        self._property_changed('point_class')
        self.__point_class = value        

    @property
    def asset_parameters_cap_floor(self) -> dict:
        return self.__asset_parameters_cap_floor

    @asset_parameters_cap_floor.setter
    def asset_parameters_cap_floor(self, value: dict):
        self._property_changed('asset_parameters_cap_floor')
        self.__asset_parameters_cap_floor = value        

    @property
    def minimum_increment(self) -> dict:
        return self.__minimum_increment

    @minimum_increment.setter
    def minimum_increment(self, value: dict):
        self._property_changed('minimum_increment')
        self.__minimum_increment = value        

    @property
    def asset_parameters_payer_currency(self) -> dict:
        return self.__asset_parameters_payer_currency

    @asset_parameters_payer_currency.setter
    def asset_parameters_payer_currency(self, value: dict):
        self._property_changed('asset_parameters_payer_currency')
        self.__asset_parameters_payer_currency = value        

    @property
    def settlement_date(self) -> dict:
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: dict):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def hedge_volatility(self) -> dict:
        return self.__hedge_volatility

    @hedge_volatility.setter
    def hedge_volatility(self, value: dict):
        self._property_changed('hedge_volatility')
        self.__hedge_volatility = value        

    @property
    def version(self) -> dict:
        return self.__version

    @version.setter
    def version(self, value: dict):
        self._property_changed('version')
        self.__version = value        

    @property
    def tags(self) -> dict:
        return self.__tags

    @tags.setter
    def tags(self, value: dict):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def asset_classifications_gics_industry_group(self) -> dict:
        return self.__asset_classifications_gics_industry_group

    @asset_classifications_gics_industry_group.setter
    def asset_classifications_gics_industry_group(self, value: dict):
        self._property_changed('asset_classifications_gics_industry_group')
        self.__asset_classifications_gics_industry_group = value        

    @property
    def market_data_asset(self) -> dict:
        return self.__market_data_asset

    @market_data_asset.setter
    def market_data_asset(self, value: dict):
        self._property_changed('market_data_asset')
        self.__market_data_asset = value        

    @property
    def asset_classifications_is_primary(self) -> dict:
        return self.__asset_classifications_is_primary

    @asset_classifications_is_primary.setter
    def asset_classifications_is_primary(self, value: dict):
        self._property_changed('asset_classifications_is_primary')
        self.__asset_classifications_is_primary = value        

    @property
    def styles(self) -> dict:
        return self.__styles

    @styles.setter
    def styles(self, value: dict):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def short_name(self) -> dict:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: dict):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def calculation_region(self) -> dict:
        return self.__calculation_region

    @calculation_region.setter
    def calculation_region(self, value: dict):
        self._property_changed('calculation_region')
        self.__calculation_region = value        

    @property
    def eid(self) -> dict:
        return self.__eid

    @eid.setter
    def eid(self, value: dict):
        self._property_changed('eid')
        self.__eid = value        

    @property
    def jsn(self) -> dict:
        return self.__jsn

    @jsn.setter
    def jsn(self, value: dict):
        self._property_changed('jsn')
        self.__jsn = value        

    @property
    def mkt_quoting_style(self) -> dict:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: dict):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        

    @property
    def hurdle_type(self) -> dict:
        return self.__hurdle_type

    @hurdle_type.setter
    def hurdle_type(self, value: dict):
        self._property_changed('hurdle_type')
        self.__hurdle_type = value        

    @property
    def mic(self) -> dict:
        return self.__mic

    @mic.setter
    def mic(self, value: dict):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def ps_id(self) -> dict:
        return self.__ps_id

    @ps_id.setter
    def ps_id(self, value: dict):
        self._property_changed('ps_id')
        self.__ps_id = value        

    @property
    def issue_status(self) -> dict:
        return self.__issue_status

    @issue_status.setter
    def issue_status(self, value: dict):
        self._property_changed('issue_status')
        self.__issue_status = value        

    @property
    def region_code(self) -> dict:
        return self.__region_code

    @region_code.setter
    def region_code(self, value: dict):
        self._property_changed('region_code')
        self.__region_code = value        

    @property
    def dollar_cross(self) -> dict:
        return self.__dollar_cross

    @dollar_cross.setter
    def dollar_cross(self, value: dict):
        self._property_changed('dollar_cross')
        self.__dollar_cross = value        

    @property
    def portfolio_type(self) -> dict:
        return self.__portfolio_type

    @portfolio_type.setter
    def portfolio_type(self, value: dict):
        self._property_changed('portfolio_type')
        self.__portfolio_type = value        

    @property
    def vendor(self) -> dict:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: dict):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def popularity(self) -> dict:
        return self.__popularity

    @popularity.setter
    def popularity(self, value: dict):
        self._property_changed('popularity')
        self.__popularity = value        

    @property
    def term(self) -> dict:
        return self.__term

    @term.setter
    def term(self, value: dict):
        self._property_changed('term')
        self.__term = value        

    @property
    def currency(self) -> dict:
        return self.__currency

    @currency.setter
    def currency(self, value: dict):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def real_time_restriction_status(self) -> dict:
        return self.__real_time_restriction_status

    @real_time_restriction_status.setter
    def real_time_restriction_status(self, value: dict):
        self._property_changed('real_time_restriction_status')
        self.__real_time_restriction_status = value        

    @property
    def asset_parameters_clearing_house(self) -> dict:
        return self.__asset_parameters_clearing_house

    @asset_parameters_clearing_house.setter
    def asset_parameters_clearing_house(self, value: dict):
        self._property_changed('asset_parameters_clearing_house')
        self.__asset_parameters_clearing_house = value        

    @property
    def rating_fitch(self) -> dict:
        return self.__rating_fitch

    @rating_fitch.setter
    def rating_fitch(self, value: dict):
        self._property_changed('rating_fitch')
        self.__rating_fitch = value        

    @property
    def non_symbol_dimensions(self) -> dict:
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: dict):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def asset_parameters_option_style(self) -> dict:
        return self.__asset_parameters_option_style

    @asset_parameters_option_style.setter
    def asset_parameters_option_style(self, value: dict):
        self._property_changed('asset_parameters_option_style')
        self.__asset_parameters_option_style = value        

    @property
    def share_class_type(self) -> dict:
        return self.__share_class_type

    @share_class_type.setter
    def share_class_type(self, value: dict):
        self._property_changed('share_class_type')
        self.__share_class_type = value        

    @property
    def asset_parameters_put_amount(self) -> dict:
        return self.__asset_parameters_put_amount

    @asset_parameters_put_amount.setter
    def asset_parameters_put_amount(self, value: dict):
        self._property_changed('asset_parameters_put_amount')
        self.__asset_parameters_put_amount = value        

    @property
    def asset_parameters_floating_rate_designated_maturity(self) -> dict:
        return self.__asset_parameters_floating_rate_designated_maturity

    @asset_parameters_floating_rate_designated_maturity.setter
    def asset_parameters_floating_rate_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_designated_maturity')
        self.__asset_parameters_floating_rate_designated_maturity = value        

    @property
    def target_notional(self) -> dict:
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: dict):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def asset_parameters_tenor(self) -> dict:
        return self.__asset_parameters_tenor

    @asset_parameters_tenor.setter
    def asset_parameters_tenor(self, value: dict):
        self._property_changed('asset_parameters_tenor')
        self.__asset_parameters_tenor = value        

    @property
    def mkt_class(self) -> dict:
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: dict):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def delisted(self) -> dict:
        return self.__delisted

    @delisted.setter
    def delisted(self, value: dict):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def last_updated_since(self) -> dict:
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: dict):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def regional_focus(self) -> dict:
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: dict):
        self._property_changed('regional_focus')
        self.__regional_focus = value        

    @property
    def asset_parameters_payer_designated_maturity(self) -> dict:
        return self.__asset_parameters_payer_designated_maturity

    @asset_parameters_payer_designated_maturity.setter
    def asset_parameters_payer_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_payer_designated_maturity')
        self.__asset_parameters_payer_designated_maturity = value        

    @property
    def tsdb_shortname(self) -> dict:
        return self.__tsdb_shortname

    @tsdb_shortname.setter
    def tsdb_shortname(self, value: dict):
        self._property_changed('tsdb_shortname')
        self.__tsdb_shortname = value        

    @property
    def seasonal_adjustment_short(self) -> dict:
        return self.__seasonal_adjustment_short

    @seasonal_adjustment_short.setter
    def seasonal_adjustment_short(self, value: dict):
        self._property_changed('seasonal_adjustment_short')
        self.__seasonal_adjustment_short = value        

    @property
    def asset_parameters_exchange_currency(self) -> dict:
        return self.__asset_parameters_exchange_currency

    @asset_parameters_exchange_currency.setter
    def asset_parameters_exchange_currency(self, value: dict):
        self._property_changed('asset_parameters_exchange_currency')
        self.__asset_parameters_exchange_currency = value        

    @property
    def asset_classifications_country_name(self) -> dict:
        return self.__asset_classifications_country_name

    @asset_classifications_country_name.setter
    def asset_classifications_country_name(self, value: dict):
        self._property_changed('asset_classifications_country_name')
        self.__asset_classifications_country_name = value        

    @property
    def management_fee(self) -> dict:
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: dict):
        self._property_changed('management_fee')
        self.__management_fee = value        

    @property
    def asset_parameters_settlement_date(self) -> dict:
        return self.__asset_parameters_settlement_date

    @asset_parameters_settlement_date.setter
    def asset_parameters_settlement_date(self, value: dict):
        self._property_changed('asset_parameters_settlement_date')
        self.__asset_parameters_settlement_date = value        

    @property
    def rating_moodys(self) -> dict:
        return self.__rating_moodys

    @rating_moodys.setter
    def rating_moodys(self, value: dict):
        self._property_changed('rating_moodys')
        self.__rating_moodys = value        

    @property
    def simon_id(self) -> dict:
        return self.__simon_id

    @simon_id.setter
    def simon_id(self, value: dict):
        self._property_changed('simon_id')
        self.__simon_id = value        

    @property
    def development_status(self) -> dict:
        return self.__development_status

    @development_status.setter
    def development_status(self, value: dict):
        self._property_changed('development_status')
        self.__development_status = value        

    @property
    def cusip(self) -> dict:
        return self.__cusip

    @cusip.setter
    def cusip(self, value: dict):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def notes(self) -> dict:
        return self.__notes

    @notes.setter
    def notes(self, value: dict):
        self._property_changed('notes')
        self.__notes = value        

    @property
    def tags_to_exclude(self) -> dict:
        return self.__tags_to_exclude

    @tags_to_exclude.setter
    def tags_to_exclude(self, value: dict):
        self._property_changed('tags_to_exclude')
        self.__tags_to_exclude = value        

    @property
    def asset_parameters_floating_rate_option(self) -> dict:
        return self.__asset_parameters_floating_rate_option

    @asset_parameters_floating_rate_option.setter
    def asset_parameters_floating_rate_option(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_option')
        self.__asset_parameters_floating_rate_option = value        

    @property
    def internal_index_calc_agent(self) -> dict:
        return self.__internal_index_calc_agent

    @internal_index_calc_agent.setter
    def internal_index_calc_agent(self, value: dict):
        self._property_changed('internal_index_calc_agent')
        self.__internal_index_calc_agent = value        

    @property
    def rating_second_highest(self) -> dict:
        return self.__rating_second_highest

    @rating_second_highest.setter
    def rating_second_highest(self, value: dict):
        self._property_changed('rating_second_highest')
        self.__rating_second_highest = value        

    @property
    def asset_classifications_country_code(self) -> dict:
        return self.__asset_classifications_country_code

    @asset_classifications_country_code.setter
    def asset_classifications_country_code(self, value: dict):
        self._property_changed('asset_classifications_country_code')
        self.__asset_classifications_country_code = value        

    @property
    def frequency(self) -> dict:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: dict):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def option_type(self) -> dict:
        return self.__option_type

    @option_type.setter
    def option_type(self, value: dict):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def data_set_sub_category(self) -> dict:
        return self.__data_set_sub_category

    @data_set_sub_category.setter
    def data_set_sub_category(self, value: dict):
        self._property_changed('data_set_sub_category')
        self.__data_set_sub_category = value        

    @property
    def is_live(self) -> dict:
        return self.__is_live

    @is_live.setter
    def is_live(self, value: dict):
        self._property_changed('is_live')
        self.__is_live = value        

    @property
    def is_legacy_pair_basket(self) -> dict:
        return self.__is_legacy_pair_basket

    @is_legacy_pair_basket.setter
    def is_legacy_pair_basket(self, value: dict):
        self._property_changed('is_legacy_pair_basket')
        self.__is_legacy_pair_basket = value        

    @property
    def issuer_type(self) -> dict:
        return self.__issuer_type

    @issuer_type.setter
    def issuer_type(self, value: dict):
        self._property_changed('issuer_type')
        self.__issuer_type = value        

    @property
    def asset_parameters_pricing_location(self) -> dict:
        return self.__asset_parameters_pricing_location

    @asset_parameters_pricing_location.setter
    def asset_parameters_pricing_location(self, value: dict):
        self._property_changed('asset_parameters_pricing_location')
        self.__asset_parameters_pricing_location = value        

    @property
    def plot_id(self) -> dict:
        return self.__plot_id

    @plot_id.setter
    def plot_id(self, value: dict):
        self._property_changed('plot_id')
        self.__plot_id = value        

    @property
    def asset_parameters_coupon(self) -> dict:
        return self.__asset_parameters_coupon

    @asset_parameters_coupon.setter
    def asset_parameters_coupon(self, value: dict):
        self._property_changed('asset_parameters_coupon')
        self.__asset_parameters_coupon = value        

    @property
    def data_product(self) -> dict:
        return self.__data_product

    @data_product.setter
    def data_product(self, value: dict):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def mq_symbol(self) -> dict:
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: dict):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def sectors(self) -> dict:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: dict):
        self._property_changed('sectors')
        self.__sectors = value        

    @property
    def redemption_notice_period(self) -> dict:
        return self.__redemption_notice_period

    @redemption_notice_period.setter
    def redemption_notice_period(self, value: dict):
        self._property_changed('redemption_notice_period')
        self.__redemption_notice_period = value        

    @property
    def multiplier(self) -> dict:
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: dict):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def asset_parameters_payer_rate_option(self) -> dict:
        return self.__asset_parameters_payer_rate_option

    @asset_parameters_payer_rate_option.setter
    def asset_parameters_payer_rate_option(self, value: dict):
        self._property_changed('asset_parameters_payer_rate_option')
        self.__asset_parameters_payer_rate_option = value        

    @property
    def market_data_point(self) -> dict:
        return self.__market_data_point

    @market_data_point.setter
    def market_data_point(self, value: dict):
        self._property_changed('market_data_point')
        self.__market_data_point = value        

    @property
    def external(self) -> dict:
        return self.__external

    @external.setter
    def external(self, value: dict):
        self._property_changed('external')
        self.__external = value        

    @property
    def wpk(self) -> dict:
        return self.__wpk

    @wpk.setter
    def wpk(self, value: dict):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def sts_fx_currency(self) -> dict:
        return self.__sts_fx_currency

    @sts_fx_currency.setter
    def sts_fx_currency(self, value: dict):
        self._property_changed('sts_fx_currency')
        self.__sts_fx_currency = value        

    @property
    def hedge_annualized_volatility(self) -> dict:
        return self.__hedge_annualized_volatility

    @hedge_annualized_volatility.setter
    def hedge_annualized_volatility(self, value: dict):
        self._property_changed('hedge_annualized_volatility')
        self.__hedge_annualized_volatility = value        

    @property
    def name(self) -> dict:
        return self.__name

    @name.setter
    def name(self, value: dict):
        self._property_changed('name')
        self.__name = value        

    @property
    def asset_parameters_expiration_date(self) -> dict:
        return self.__asset_parameters_expiration_date

    @asset_parameters_expiration_date.setter
    def asset_parameters_expiration_date(self, value: dict):
        self._property_changed('asset_parameters_expiration_date')
        self.__asset_parameters_expiration_date = value        

    @property
    def aum(self) -> dict:
        return self.__aum

    @aum.setter
    def aum(self, value: dict):
        self._property_changed('aum')
        self.__aum = value        

    @property
    def exchange(self) -> dict:
        return self.__exchange

    @exchange.setter
    def exchange(self, value: dict):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def folder_name(self) -> dict:
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: dict):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def region(self) -> dict:
        return self.__region

    @region.setter
    def region(self, value: dict):
        self._property_changed('region')
        self.__region = value        

    @property
    def cid(self) -> dict:
        return self.__cid

    @cid.setter
    def cid(self, value: dict):
        self._property_changed('cid')
        self.__cid = value        

    @property
    def onboarded(self) -> dict:
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: dict):
        self._property_changed('onboarded')
        self.__onboarded = value        

    @property
    def live_date(self) -> dict:
        return self.__live_date

    @live_date.setter
    def live_date(self, value: dict):
        self._property_changed('live_date')
        self.__live_date = value        

    @property
    def issue_price(self) -> dict:
        return self.__issue_price

    @issue_price.setter
    def issue_price(self, value: dict):
        self._property_changed('issue_price')
        self.__issue_price = value        

    @property
    def sink_factor(self) -> dict:
        return self.__sink_factor

    @sink_factor.setter
    def sink_factor(self, value: dict):
        self._property_changed('sink_factor')
        self.__sink_factor = value        

    @property
    def underlying_data_set_id(self) -> dict:
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: dict):
        self._property_changed('underlying_data_set_id')
        self.__underlying_data_set_id = value        

    @property
    def asset_parameters_notional_amount_in_other_currency(self) -> dict:
        return self.__asset_parameters_notional_amount_in_other_currency

    @asset_parameters_notional_amount_in_other_currency.setter
    def asset_parameters_notional_amount_in_other_currency(self, value: dict):
        self._property_changed('asset_parameters_notional_amount_in_other_currency')
        self.__asset_parameters_notional_amount_in_other_currency = value        

    @property
    def asset_parameters_payer_frequency(self) -> dict:
        return self.__asset_parameters_payer_frequency

    @asset_parameters_payer_frequency.setter
    def asset_parameters_payer_frequency(self, value: dict):
        self._property_changed('asset_parameters_payer_frequency')
        self.__asset_parameters_payer_frequency = value        

    @property
    def prime_id(self) -> dict:
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: dict):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def asset_classifications_gics_sector(self) -> dict:
        return self.__asset_classifications_gics_sector

    @asset_classifications_gics_sector.setter
    def asset_classifications_gics_sector(self, value: dict):
        self._property_changed('asset_classifications_gics_sector')
        self.__asset_classifications_gics_sector = value        

    @property
    def asset_parameters_pair(self) -> dict:
        return self.__asset_parameters_pair

    @asset_parameters_pair.setter
    def asset_parameters_pair(self, value: dict):
        self._property_changed('asset_parameters_pair')
        self.__asset_parameters_pair = value        

    @property
    def sts_asset_name(self) -> dict:
        return self.__sts_asset_name

    @sts_asset_name.setter
    def sts_asset_name(self, value: dict):
        self._property_changed('sts_asset_name')
        self.__sts_asset_name = value        

    @property
    def description(self) -> dict:
        return self.__description

    @description.setter
    def description(self, value: dict):
        self._property_changed('description')
        self.__description = value        

    @property
    def asset_classifications_is_country_primary(self) -> dict:
        return self.__asset_classifications_is_country_primary

    @asset_classifications_is_country_primary.setter
    def asset_classifications_is_country_primary(self, value: dict):
        self._property_changed('asset_classifications_is_country_primary')
        self.__asset_classifications_is_country_primary = value        

    @property
    def title(self) -> dict:
        return self.__title

    @title.setter
    def title(self, value: dict):
        self._property_changed('title')
        self.__title = value        

    @property
    def net_exposure_classification(self) -> dict:
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: dict):
        self._property_changed('net_exposure_classification')
        self.__net_exposure_classification = value        

    @property
    def asset_parameters_strike_price(self) -> dict:
        return self.__asset_parameters_strike_price

    @asset_parameters_strike_price.setter
    def asset_parameters_strike_price(self, value: dict):
        self._property_changed('asset_parameters_strike_price')
        self.__asset_parameters_strike_price = value        

    @property
    def coupon_type(self) -> dict:
        return self.__coupon_type

    @coupon_type.setter
    def coupon_type(self, value: dict):
        self._property_changed('coupon_type')
        self.__coupon_type = value        

    @property
    def last_updated_by_id(self) -> dict:
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: dict):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def clone_parent_id(self) -> dict:
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: dict):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def company(self) -> dict:
        return self.__company

    @company.setter
    def company(self, value: dict):
        self._property_changed('company')
        self.__company = value        

    @property
    def gate_type(self) -> dict:
        return self.__gate_type

    @gate_type.setter
    def gate_type(self, value: dict):
        self._property_changed('gate_type')
        self.__gate_type = value        

    @property
    def issue_date(self) -> dict:
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: dict):
        self._property_changed('issue_date')
        self.__issue_date = value        

    @property
    def expiration_date(self) -> dict:
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: dict):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def coverage(self) -> dict:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: dict):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def ticker(self) -> dict:
        return self.__ticker

    @ticker.setter
    def ticker(self, value: dict):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def asset_parameters_receiver_rate_option(self) -> dict:
        return self.__asset_parameters_receiver_rate_option

    @asset_parameters_receiver_rate_option.setter
    def asset_parameters_receiver_rate_option(self, value: dict):
        self._property_changed('asset_parameters_receiver_rate_option')
        self.__asset_parameters_receiver_rate_option = value        

    @property
    def call_last_date(self) -> dict:
        return self.__call_last_date

    @call_last_date.setter
    def call_last_date(self, value: dict):
        self._property_changed('call_last_date')
        self.__call_last_date = value        

    @property
    def asset_parameters_payer_spread(self) -> dict:
        return self.__asset_parameters_payer_spread

    @asset_parameters_payer_spread.setter
    def asset_parameters_payer_spread(self, value: dict):
        self._property_changed('asset_parameters_payer_spread')
        self.__asset_parameters_payer_spread = value        

    @property
    def sts_rates_country(self) -> dict:
        return self.__sts_rates_country

    @sts_rates_country.setter
    def sts_rates_country(self, value: dict):
        self._property_changed('sts_rates_country')
        self.__sts_rates_country = value        

    @property
    def asset_parameters_premium_payment_date(self) -> dict:
        return self.__asset_parameters_premium_payment_date

    @asset_parameters_premium_payment_date.setter
    def asset_parameters_premium_payment_date(self, value: dict):
        self._property_changed('asset_parameters_premium_payment_date')
        self.__asset_parameters_premium_payment_date = value        

    @property
    def latest_execution_time(self) -> dict:
        return self.__latest_execution_time

    @latest_execution_time.setter
    def latest_execution_time(self, value: dict):
        self._property_changed('latest_execution_time')
        self.__latest_execution_time = value        

    @property
    def asset_parameters_forward_rate(self) -> dict:
        return self.__asset_parameters_forward_rate

    @asset_parameters_forward_rate.setter
    def asset_parameters_forward_rate(self, value: dict):
        self._property_changed('asset_parameters_forward_rate')
        self.__asset_parameters_forward_rate = value        

    @property
    def asset_parameters_receiver_designated_maturity(self) -> dict:
        return self.__asset_parameters_receiver_designated_maturity

    @asset_parameters_receiver_designated_maturity.setter
    def asset_parameters_receiver_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_receiver_designated_maturity')
        self.__asset_parameters_receiver_designated_maturity = value        

    @property
    def gate(self) -> dict:
        return self.__gate

    @gate.setter
    def gate(self, value: dict):
        self._property_changed('gate')
        self.__gate = value        

    @property
    def multi_tags(self) -> dict:
        return self.__multi_tags

    @multi_tags.setter
    def multi_tags(self, value: dict):
        self._property_changed('multi_tags')
        self.__multi_tags = value        

    @property
    def gsn(self) -> dict:
        return self.__gsn

    @gsn.setter
    def gsn(self, value: dict):
        self._property_changed('gsn')
        self.__gsn = value        

    @property
    def gss(self) -> dict:
        return self.__gss

    @gss.setter
    def gss(self, value: dict):
        self._property_changed('gss')
        self.__gss = value        

    @property
    def rating_linear(self) -> dict:
        return self.__rating_linear

    @rating_linear.setter
    def rating_linear(self, value: dict):
        self._property_changed('rating_linear')
        self.__rating_linear = value        

    @property
    def asset_class(self) -> dict:
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: dict):
        self._property_changed('asset_class')
        self.__asset_class = value        

    @property
    def asset_parameters_index(self) -> dict:
        return self.__asset_parameters_index

    @asset_parameters_index.setter
    def asset_parameters_index(self, value: dict):
        self._property_changed('asset_parameters_index')
        self.__asset_parameters_index = value        

    @property
    def cm_id(self) -> dict:
        return self.__cm_id

    @cm_id.setter
    def cm_id(self, value: dict):
        self._property_changed('cm_id')
        self.__cm_id = value        

    @property
    def type(self) -> dict:
        return self.__type

    @type.setter
    def type(self, value: dict):
        self._property_changed('type')
        self.__type = value        

    @property
    def gsideid(self) -> dict:
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: dict):
        self._property_changed('gsideid')
        self.__gsideid = value        

    @property
    def mdapi(self) -> dict:
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: dict):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def ric(self) -> dict:
        return self.__ric

    @ric.setter
    def ric(self, value: dict):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def issuer(self) -> dict:
        return self.__issuer

    @issuer.setter
    def issuer(self, value: dict):
        self._property_changed('issuer')
        self.__issuer = value        

    @property
    def position_source_id(self) -> dict:
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: dict):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def measures(self) -> dict:
        return self.__measures

    @measures.setter
    def measures(self, value: dict):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def asset_parameters_floating_rate_day_count_fraction(self) -> dict:
        return self.__asset_parameters_floating_rate_day_count_fraction

    @asset_parameters_floating_rate_day_count_fraction.setter
    def asset_parameters_floating_rate_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_day_count_fraction')
        self.__asset_parameters_floating_rate_day_count_fraction = value        

    @property
    def asset_parameters_notional_amount(self) -> dict:
        return self.__asset_parameters_notional_amount

    @asset_parameters_notional_amount.setter
    def asset_parameters_notional_amount(self, value: dict):
        self._property_changed('asset_parameters_notional_amount')
        self.__asset_parameters_notional_amount = value        

    @property
    def action(self) -> dict:
        return self.__action

    @action.setter
    def action(self, value: dict):
        self._property_changed('action')
        self.__action = value        

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self._property_changed('id')
        self.__id = value        

    @property
    def asset_parameters_call_amount(self) -> dict:
        return self.__asset_parameters_call_amount

    @asset_parameters_call_amount.setter
    def asset_parameters_call_amount(self, value: dict):
        self._property_changed('asset_parameters_call_amount')
        self.__asset_parameters_call_amount = value        

    @property
    def asset_parameters_seniority(self) -> dict:
        return self.__asset_parameters_seniority

    @asset_parameters_seniority.setter
    def asset_parameters_seniority(self, value: dict):
        self._property_changed('asset_parameters_seniority')
        self.__asset_parameters_seniority = value        

    @property
    def redemption_date(self) -> dict:
        return self.__redemption_date

    @redemption_date.setter
    def redemption_date(self, value: dict):
        self._property_changed('redemption_date')
        self.__redemption_date = value        

    @property
    def identifier(self) -> dict:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: dict):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def index_create_source(self) -> dict:
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: dict):
        self._property_changed('index_create_source')
        self.__index_create_source = value        

    @property
    def sec_name(self) -> dict:
        return self.__sec_name

    @sec_name.setter
    def sec_name(self, value: dict):
        self._property_changed('sec_name')
        self.__sec_name = value        

    @property
    def sub_region(self) -> dict:
        return self.__sub_region

    @sub_region.setter
    def sub_region(self, value: dict):
        self._property_changed('sub_region')
        self.__sub_region = value        

    @property
    def asset_parameters_receiver_day_count_fraction(self) -> dict:
        return self.__asset_parameters_receiver_day_count_fraction

    @asset_parameters_receiver_day_count_fraction.setter
    def asset_parameters_receiver_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_receiver_day_count_fraction')
        self.__asset_parameters_receiver_day_count_fraction = value        

    @property
    def asset_parameters_index2_tenor(self) -> dict:
        return self.__asset_parameters_index2_tenor

    @asset_parameters_index2_tenor.setter
    def asset_parameters_index2_tenor(self, value: dict):
        self._property_changed('asset_parameters_index2_tenor')
        self.__asset_parameters_index2_tenor = value        

    @property
    def asset_parameters_notional_currency(self) -> dict:
        return self.__asset_parameters_notional_currency

    @asset_parameters_notional_currency.setter
    def asset_parameters_notional_currency(self, value: dict):
        self._property_changed('asset_parameters_notional_currency')
        self.__asset_parameters_notional_currency = value        

    @property
    def sedol(self) -> dict:
        return self.__sedol

    @sedol.setter
    def sedol(self, value: dict):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def mkt_asset(self) -> dict:
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: dict):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def rating_standard_and_poors(self) -> dict:
        return self.__rating_standard_and_poors

    @rating_standard_and_poors.setter
    def rating_standard_and_poors(self, value: dict):
        self._property_changed('rating_standard_and_poors')
        self.__rating_standard_and_poors = value        

    @property
    def asset_types(self) -> dict:
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: dict):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def bcid(self) -> dict:
        return self.__bcid

    @bcid.setter
    def bcid(self, value: dict):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def asset_parameters_credit_index_series(self) -> dict:
        return self.__asset_parameters_credit_index_series

    @asset_parameters_credit_index_series.setter
    def asset_parameters_credit_index_series(self, value: dict):
        self._property_changed('asset_parameters_credit_index_series')
        self.__asset_parameters_credit_index_series = value        

    @property
    def gsid(self) -> dict:
        return self.__gsid

    @gsid.setter
    def gsid(self, value: dict):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def tdapi(self) -> dict:
        return self.__tdapi

    @tdapi.setter
    def tdapi(self, value: dict):
        self._property_changed('tdapi')
        self.__tdapi = value        

    @property
    def last_updated_message(self) -> dict:
        return self.__last_updated_message

    @last_updated_message.setter
    def last_updated_message(self, value: dict):
        self._property_changed('last_updated_message')
        self.__last_updated_message = value        

    @property
    def rcic(self) -> dict:
        return self.__rcic

    @rcic.setter
    def rcic(self, value: dict):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def trading_restriction(self) -> dict:
        return self.__trading_restriction

    @trading_restriction.setter
    def trading_restriction(self, value: dict):
        self._property_changed('trading_restriction')
        self.__trading_restriction = value        

    @property
    def name_raw(self) -> dict:
        return self.__name_raw

    @name_raw.setter
    def name_raw(self, value: dict):
        self._property_changed('name_raw')
        self.__name_raw = value        

    @property
    def status(self) -> dict:
        return self.__status

    @status.setter
    def status(self, value: dict):
        self._property_changed('status')
        self.__status = value        

    @property
    def asset_parameters_pay_or_receive(self) -> dict:
        return self.__asset_parameters_pay_or_receive

    @asset_parameters_pay_or_receive.setter
    def asset_parameters_pay_or_receive(self, value: dict):
        self._property_changed('asset_parameters_pay_or_receive')
        self.__asset_parameters_pay_or_receive = value        

    @property
    def client_name(self) -> dict:
        return self.__client_name

    @client_name.setter
    def client_name(self, value: dict):
        self._property_changed('client_name')
        self.__client_name = value        

    @property
    def asset_parameters_index_series(self) -> dict:
        return self.__asset_parameters_index_series

    @asset_parameters_index_series.setter
    def asset_parameters_index_series(self, value: dict):
        self._property_changed('asset_parameters_index_series')
        self.__asset_parameters_index_series = value        

    @property
    def asset_classifications_gics_industry(self) -> dict:
        return self.__asset_classifications_gics_industry

    @asset_classifications_gics_industry.setter
    def asset_classifications_gics_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_industry')
        self.__asset_classifications_gics_industry = value        

    @property
    def on_behalf_of(self) -> dict:
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: dict):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def increment(self) -> dict:
        return self.__increment

    @increment.setter
    def increment(self, value: dict):
        self._property_changed('increment')
        self.__increment = value        

    @property
    def accrued_interest_standard(self) -> dict:
        return self.__accrued_interest_standard

    @accrued_interest_standard.setter
    def accrued_interest_standard(self, value: dict):
        self._property_changed('accrued_interest_standard')
        self.__accrued_interest_standard = value        

    @property
    def enabled(self) -> dict:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: dict):
        self._property_changed('enabled')
        self.__enabled = value        

    @property
    def sts_commodity(self) -> dict:
        return self.__sts_commodity

    @sts_commodity.setter
    def sts_commodity(self, value: dict):
        self._property_changed('sts_commodity')
        self.__sts_commodity = value        

    @property
    def sectors_raw(self) -> dict:
        return self.__sectors_raw

    @sectors_raw.setter
    def sectors_raw(self, value: dict):
        self._property_changed('sectors_raw')
        self.__sectors_raw = value        

    @property
    def sts_commodity_sector(self) -> dict:
        return self.__sts_commodity_sector

    @sts_commodity_sector.setter
    def sts_commodity_sector(self, value: dict):
        self._property_changed('sts_commodity_sector')
        self.__sts_commodity_sector = value        

    @property
    def asset_parameters_receiver_frequency(self) -> dict:
        return self.__asset_parameters_receiver_frequency

    @asset_parameters_receiver_frequency.setter
    def asset_parameters_receiver_frequency(self, value: dict):
        self._property_changed('asset_parameters_receiver_frequency')
        self.__asset_parameters_receiver_frequency = value        

    @property
    def position_source_name(self) -> dict:
        return self.__position_source_name

    @position_source_name.setter
    def position_source_name(self, value: dict):
        self._property_changed('position_source_name')
        self.__position_source_name = value        

    @property
    def gsid_equivalent(self) -> dict:
        return self.__gsid_equivalent

    @gsid_equivalent.setter
    def gsid_equivalent(self, value: dict):
        self._property_changed('gsid_equivalent')
        self.__gsid_equivalent = value        

    @property
    def categories(self) -> dict:
        return self.__categories

    @categories.setter
    def categories(self, value: dict):
        self._property_changed('categories')
        self.__categories = value        

    @property
    def symbol_dimensions(self) -> dict:
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: dict):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def ext_mkt_asset(self) -> dict:
        return self.__ext_mkt_asset

    @ext_mkt_asset.setter
    def ext_mkt_asset(self, value: dict):
        self._property_changed('ext_mkt_asset')
        self.__ext_mkt_asset = value        

    @property
    def asset_parameters_fixed_rate_frequency(self) -> dict:
        return self.__asset_parameters_fixed_rate_frequency

    @asset_parameters_fixed_rate_frequency.setter
    def asset_parameters_fixed_rate_frequency(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate_frequency')
        self.__asset_parameters_fixed_rate_frequency = value        

    @property
    def coupon(self) -> dict:
        return self.__coupon

    @coupon.setter
    def coupon(self, value: dict):
        self._property_changed('coupon')
        self.__coupon = value        

    @property
    def side_pocket(self) -> dict:
        return self.__side_pocket

    @side_pocket.setter
    def side_pocket(self, value: dict):
        self._property_changed('side_pocket')
        self.__side_pocket = value        

    @property
    def compliance_restricted_status(self) -> dict:
        return self.__compliance_restricted_status

    @compliance_restricted_status.setter
    def compliance_restricted_status(self, value: dict):
        self._property_changed('compliance_restricted_status')
        self.__compliance_restricted_status = value        

    @property
    def quoting_style(self) -> dict:
        return self.__quoting_style

    @quoting_style.setter
    def quoting_style(self, value: dict):
        self._property_changed('quoting_style')
        self.__quoting_style = value        

    @property
    def is_entity(self) -> dict:
        return self.__is_entity

    @is_entity.setter
    def is_entity(self, value: dict):
        self._property_changed('is_entity')
        self.__is_entity = value        

    @property
    def scenario_group_id(self) -> dict:
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: dict):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def redemption_period(self) -> dict:
        return self.__redemption_period

    @redemption_period.setter
    def redemption_period(self, value: dict):
        self._property_changed('redemption_period')
        self.__redemption_period = value        

    @property
    def asset_parameters_issuer_type(self) -> dict:
        return self.__asset_parameters_issuer_type

    @asset_parameters_issuer_type.setter
    def asset_parameters_issuer_type(self, value: dict):
        self._property_changed('asset_parameters_issuer_type')
        self.__asset_parameters_issuer_type = value        

    @property
    def sts_credit_market(self) -> dict:
        return self.__sts_credit_market

    @sts_credit_market.setter
    def sts_credit_market(self, value: dict):
        self._property_changed('sts_credit_market')
        self.__sts_credit_market = value        

    @property
    def bbid(self) -> dict:
        return self.__bbid

    @bbid.setter
    def bbid(self, value: dict):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def asset_classifications_risk_country_code(self) -> dict:
        return self.__asset_classifications_risk_country_code

    @asset_classifications_risk_country_code.setter
    def asset_classifications_risk_country_code(self, value: dict):
        self._property_changed('asset_classifications_risk_country_code')
        self.__asset_classifications_risk_country_code = value        

    @property
    def asset_parameters_receiver_currency(self) -> dict:
        return self.__asset_parameters_receiver_currency

    @asset_parameters_receiver_currency.setter
    def asset_parameters_receiver_currency(self, value: dict):
        self._property_changed('asset_parameters_receiver_currency')
        self.__asset_parameters_receiver_currency = value        

    @property
    def sts_em_dm(self) -> dict:
        return self.__sts_em_dm

    @sts_em_dm.setter
    def sts_em_dm(self, value: dict):
        self._property_changed('sts_em_dm')
        self.__sts_em_dm = value        

    @property
    def issue_size(self) -> dict:
        return self.__issue_size

    @issue_size.setter
    def issue_size(self, value: dict):
        self._property_changed('issue_size')
        self.__issue_size = value        

    @property
    def returns_enabled(self) -> dict:
        return self.__returns_enabled

    @returns_enabled.setter
    def returns_enabled(self, value: dict):
        self._property_changed('returns_enabled')
        self.__returns_enabled = value        

    @property
    def seniority(self) -> dict:
        return self.__seniority

    @seniority.setter
    def seniority(self, value: dict):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def asset_parameters_settlement(self) -> dict:
        return self.__asset_parameters_settlement

    @asset_parameters_settlement.setter
    def asset_parameters_settlement(self, value: dict):
        self._property_changed('asset_parameters_settlement')
        self.__asset_parameters_settlement = value        

    @property
    def asset_parameters_expiration_time(self) -> dict:
        return self.__asset_parameters_expiration_time

    @asset_parameters_expiration_time.setter
    def asset_parameters_expiration_time(self, value: dict):
        self._property_changed('asset_parameters_expiration_time')
        self.__asset_parameters_expiration_time = value        

    @property
    def primary_country_ric(self) -> dict:
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: dict):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def is_pair_basket(self) -> dict:
        return self.__is_pair_basket

    @is_pair_basket.setter
    def is_pair_basket(self, value: dict):
        self._property_changed('is_pair_basket')
        self.__is_pair_basket = value        

    @property
    def asset_parameters_index_version(self) -> dict:
        return self.__asset_parameters_index_version

    @asset_parameters_index_version.setter
    def asset_parameters_index_version(self, value: dict):
        self._property_changed('asset_parameters_index_version')
        self.__asset_parameters_index_version = value        

    @property
    def asset_parameters_commodity_reference_price(self) -> dict:
        return self.__asset_parameters_commodity_reference_price

    @asset_parameters_commodity_reference_price.setter
    def asset_parameters_commodity_reference_price(self, value: dict):
        self._property_changed('asset_parameters_commodity_reference_price')
        self.__asset_parameters_commodity_reference_price = value        

    @property
    def default_backcast(self) -> dict:
        return self.__default_backcast

    @default_backcast.setter
    def default_backcast(self, value: dict):
        self._property_changed('default_backcast')
        self.__default_backcast = value        

    @property
    def use_machine_learning(self) -> dict:
        return self.__use_machine_learning

    @use_machine_learning.setter
    def use_machine_learning(self, value: dict):
        self._property_changed('use_machine_learning')
        self.__use_machine_learning = value        

    @property
    def performance_fee(self) -> dict:
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: dict):
        self._property_changed('performance_fee')
        self.__performance_fee = value        

    @property
    def report_type(self) -> dict:
        return self.__report_type

    @report_type.setter
    def report_type(self, value: dict):
        self._property_changed('report_type')
        self.__report_type = value        

    @property
    def lockup_type(self) -> dict:
        return self.__lockup_type

    @lockup_type.setter
    def lockup_type(self, value: dict):
        self._property_changed('lockup_type')
        self.__lockup_type = value        

    @property
    def lockup(self) -> dict:
        return self.__lockup

    @lockup.setter
    def lockup(self, value: dict):
        self._property_changed('lockup')
        self.__lockup = value        

    @property
    def underlying_asset_ids(self) -> dict:
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: dict):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        

    @property
    def asset_parameters_fee_currency(self) -> dict:
        return self.__asset_parameters_fee_currency

    @asset_parameters_fee_currency.setter
    def asset_parameters_fee_currency(self, value: dict):
        self._property_changed('asset_parameters_fee_currency')
        self.__asset_parameters_fee_currency = value        

    @property
    def encoded_stats(self) -> dict:
        return self.__encoded_stats

    @encoded_stats.setter
    def encoded_stats(self, value: dict):
        self._property_changed('encoded_stats')
        self.__encoded_stats = value        

    @property
    def pnode_id(self) -> dict:
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: dict):
        self._property_changed('pnode_id')
        self.__pnode_id = value        

    @property
    def backtest_type(self) -> dict:
        return self.__backtest_type

    @backtest_type.setter
    def backtest_type(self, value: dict):
        self._property_changed('backtest_type')
        self.__backtest_type = value        

    @property
    def asset_parameters_issuer(self) -> dict:
        return self.__asset_parameters_issuer

    @asset_parameters_issuer.setter
    def asset_parameters_issuer(self, value: dict):
        self._property_changed('asset_parameters_issuer')
        self.__asset_parameters_issuer = value        

    @property
    def exchange_code(self) -> dict:
        return self.__exchange_code

    @exchange_code.setter
    def exchange_code(self, value: dict):
        self._property_changed('exchange_code')
        self.__exchange_code = value        

    @property
    def asset_parameters_strike(self) -> dict:
        return self.__asset_parameters_strike

    @asset_parameters_strike.setter
    def asset_parameters_strike(self, value: dict):
        self._property_changed('asset_parameters_strike')
        self.__asset_parameters_strike = value        

    @property
    def oe_id(self) -> dict:
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: dict):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def asset_parameters_termination_date(self) -> dict:
        return self.__asset_parameters_termination_date

    @asset_parameters_termination_date.setter
    def asset_parameters_termination_date(self, value: dict):
        self._property_changed('asset_parameters_termination_date')
        self.__asset_parameters_termination_date = value        

    @property
    def resource(self) -> dict:
        return self.__resource

    @resource.setter
    def resource(self, value: dict):
        self._property_changed('resource')
        self.__resource = value        

    @property
    def asset_parameters_receiver_spread(self) -> dict:
        return self.__asset_parameters_receiver_spread

    @asset_parameters_receiver_spread.setter
    def asset_parameters_receiver_spread(self, value: dict):
        self._property_changed('asset_parameters_receiver_spread')
        self.__asset_parameters_receiver_spread = value        

    @property
    def bbid_equivalent(self) -> dict:
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: dict):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def hurdle(self) -> dict:
        return self.__hurdle

    @hurdle.setter
    def hurdle(self, value: dict):
        self._property_changed('hurdle')
        self.__hurdle = value        

    @property
    def asset_parameters_effective_date(self) -> dict:
        return self.__asset_parameters_effective_date

    @asset_parameters_effective_date.setter
    def asset_parameters_effective_date(self, value: dict):
        self._property_changed('asset_parameters_effective_date')
        self.__asset_parameters_effective_date = value        

    @property
    def valoren(self) -> dict:
        return self.__valoren

    @valoren.setter
    def valoren(self, value: dict):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def asset_parameters_fixed_rate_day_count_fraction(self) -> dict:
        return self.__asset_parameters_fixed_rate_day_count_fraction

    @asset_parameters_fixed_rate_day_count_fraction.setter
    def asset_parameters_fixed_rate_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate_day_count_fraction')
        self.__asset_parameters_fixed_rate_day_count_fraction = value        

    @property
    def auto_tags(self) -> dict:
        return self.__auto_tags

    @auto_tags.setter
    def auto_tags(self, value: dict):
        self._property_changed('auto_tags')
        self.__auto_tags = value        

    @property
    def short_description(self) -> dict:
        return self.__short_description

    @short_description.setter
    def short_description(self, value: dict):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def ext_mkt_class(self) -> dict:
        return self.__ext_mkt_class

    @ext_mkt_class.setter
    def ext_mkt_class(self, value: dict):
        self._property_changed('ext_mkt_class')
        self.__ext_mkt_class = value        

    @property
    def mkt_point1(self) -> dict:
        return self.__mkt_point1

    @mkt_point1.setter
    def mkt_point1(self, value: dict):
        self._property_changed('mkt_point1')
        self.__mkt_point1 = value        

    @property
    def portfolio_managers(self) -> dict:
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: dict):
        self._property_changed('portfolio_managers')
        self.__portfolio_managers = value        

    @property
    def asset_parameters_commodity_sector(self) -> dict:
        return self.__asset_parameters_commodity_sector

    @asset_parameters_commodity_sector.setter
    def asset_parameters_commodity_sector(self, value: dict):
        self._property_changed('asset_parameters_commodity_sector')
        self.__asset_parameters_commodity_sector = value        

    @property
    def hedge_tracking_error(self) -> dict:
        return self.__hedge_tracking_error

    @hedge_tracking_error.setter
    def hedge_tracking_error(self, value: dict):
        self._property_changed('hedge_tracking_error')
        self.__hedge_tracking_error = value        

    @property
    def asset_parameters_put_currency(self) -> dict:
        return self.__asset_parameters_put_currency

    @asset_parameters_put_currency.setter
    def asset_parameters_put_currency(self, value: dict):
        self._property_changed('asset_parameters_put_currency')
        self.__asset_parameters_put_currency = value        

    @property
    def asset_parameters_coupon_type(self) -> dict:
        return self.__asset_parameters_coupon_type

    @asset_parameters_coupon_type.setter
    def asset_parameters_coupon_type(self, value: dict):
        self._property_changed('asset_parameters_coupon_type')
        self.__asset_parameters_coupon_type = value        

    @property
    def supra_strategy(self) -> dict:
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: dict):
        self._property_changed('supra_strategy')
        self.__supra_strategy = value        

    @property
    def term_status(self) -> dict:
        return self.__term_status

    @term_status.setter
    def term_status(self, value: dict):
        self._property_changed('term_status')
        self.__term_status = value        

    @property
    def wi_id(self) -> dict:
        return self.__wi_id

    @wi_id.setter
    def wi_id(self, value: dict):
        self._property_changed('wi_id')
        self.__wi_id = value        

    @property
    def market_cap_category(self) -> dict:
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: dict):
        self._property_changed('market_cap_category')
        self.__market_cap_category = value        

    @property
    def asset_parameters_call_currency(self) -> dict:
        return self.__asset_parameters_call_currency

    @asset_parameters_call_currency.setter
    def asset_parameters_call_currency(self, value: dict):
        self._property_changed('asset_parameters_call_currency')
        self.__asset_parameters_call_currency = value        

    @property
    def mkt_point3(self) -> dict:
        return self.__mkt_point3

    @mkt_point3.setter
    def mkt_point3(self, value: dict):
        self._property_changed('mkt_point3')
        self.__mkt_point3 = value        

    @property
    def display_id(self) -> dict:
        return self.__display_id

    @display_id.setter
    def display_id(self, value: dict):
        self._property_changed('display_id')
        self.__display_id = value        

    @property
    def mkt_point2(self) -> dict:
        return self.__mkt_point2

    @mkt_point2.setter
    def mkt_point2(self, value: dict):
        self._property_changed('mkt_point2')
        self.__mkt_point2 = value        

    @property
    def strike_price(self) -> dict:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: dict):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def mkt_point4(self) -> dict:
        return self.__mkt_point4

    @mkt_point4.setter
    def mkt_point4(self, value: dict):
        self._property_changed('mkt_point4')
        self.__mkt_point4 = value        

    @property
    def risk_packages(self) -> dict:
        return self.__risk_packages

    @risk_packages.setter
    def risk_packages(self, value: dict):
        self._property_changed('risk_packages')
        self.__risk_packages = value        

    @property
    def units(self) -> dict:
        return self.__units

    @units.setter
    def units(self, value: dict):
        self._property_changed('units')
        self.__units = value        

    @property
    def em_id(self) -> dict:
        return self.__em_id

    @em_id.setter
    def em_id(self, value: dict):
        self._property_changed('em_id')
        self.__em_id = value        

    @property
    def sts_credit_region(self) -> dict:
        return self.__sts_credit_region

    @sts_credit_region.setter
    def sts_credit_region(self, value: dict):
        self._property_changed('sts_credit_region')
        self.__sts_credit_region = value        

    @property
    def country_id(self) -> dict:
        return self.__country_id

    @country_id.setter
    def country_id(self, value: dict):
        self._property_changed('country_id')
        self.__country_id = value        

    @property
    def ext_mkt_point3(self) -> dict:
        return self.__ext_mkt_point3

    @ext_mkt_point3.setter
    def ext_mkt_point3(self, value: dict):
        self._property_changed('ext_mkt_point3')
        self.__ext_mkt_point3 = value        

    @property
    def asset_classifications_risk_country_name(self) -> dict:
        return self.__asset_classifications_risk_country_name

    @asset_classifications_risk_country_name.setter
    def asset_classifications_risk_country_name(self, value: dict):
        self._property_changed('asset_classifications_risk_country_name')
        self.__asset_classifications_risk_country_name = value        

    @property
    def asset_parameters_vendor(self) -> dict:
        return self.__asset_parameters_vendor

    @asset_parameters_vendor.setter
    def asset_parameters_vendor(self, value: dict):
        self._property_changed('asset_parameters_vendor')
        self.__asset_parameters_vendor = value        

    @property
    def asset_parameters_index1_tenor(self) -> dict:
        return self.__asset_parameters_index1_tenor

    @asset_parameters_index1_tenor.setter
    def asset_parameters_index1_tenor(self, value: dict):
        self._property_changed('asset_parameters_index1_tenor')
        self.__asset_parameters_index1_tenor = value        

    @property
    def mkt_type(self) -> dict:
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: dict):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def is_public(self) -> dict:
        return self.__is_public

    @is_public.setter
    def is_public(self, value: dict):
        self._property_changed('is_public')
        self.__is_public = value        

    @property
    def alias(self) -> dict:
        return self.__alias

    @alias.setter
    def alias(self, value: dict):
        self._property_changed('alias')
        self.__alias = value        

    @property
    def ext_mkt_point1(self) -> dict:
        return self.__ext_mkt_point1

    @ext_mkt_point1.setter
    def ext_mkt_point1(self, value: dict):
        self._property_changed('ext_mkt_point1')
        self.__ext_mkt_point1 = value        

    @property
    def product_type(self) -> dict:
        return self.__product_type

    @product_type.setter
    def product_type(self, value: dict):
        self._property_changed('product_type')
        self.__product_type = value        

    @property
    def ext_mkt_point2(self) -> dict:
        return self.__ext_mkt_point2

    @ext_mkt_point2.setter
    def ext_mkt_point2(self, value: dict):
        self._property_changed('ext_mkt_point2')
        self.__ext_mkt_point2 = value        

    @property
    def sub_region_code(self) -> dict:
        return self.__sub_region_code

    @sub_region_code.setter
    def sub_region_code(self, value: dict):
        self._property_changed('sub_region_code')
        self.__sub_region_code = value        

    @property
    def asset_parameters_option_type(self) -> dict:
        return self.__asset_parameters_option_type

    @asset_parameters_option_type.setter
    def asset_parameters_option_type(self, value: dict):
        self._property_changed('asset_parameters_option_type')
        self.__asset_parameters_option_type = value        

    @property
    def asset_parameters_fixed_rate(self) -> dict:
        return self.__asset_parameters_fixed_rate

    @asset_parameters_fixed_rate.setter
    def asset_parameters_fixed_rate(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate')
        self.__asset_parameters_fixed_rate = value        

    @property
    def last_returns_end_date(self) -> dict:
        return self.__last_returns_end_date

    @last_returns_end_date.setter
    def last_returns_end_date(self, value: dict):
        self._property_changed('last_returns_end_date')
        self.__last_returns_end_date = value        

    @property
    def tsdb_synced_symbol(self) -> dict:
        return self.__tsdb_synced_symbol

    @tsdb_synced_symbol.setter
    def tsdb_synced_symbol(self, value: dict):
        self._property_changed('tsdb_synced_symbol')
        self.__tsdb_synced_symbol = value        

    @property
    def position_source_type(self) -> dict:
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: dict):
        self._property_changed('position_source_type')
        self.__position_source_type = value        

    @property
    def minimum_denomination(self) -> dict:
        return self.__minimum_denomination

    @minimum_denomination.setter
    def minimum_denomination(self, value: dict):
        self._property_changed('minimum_denomination')
        self.__minimum_denomination = value        

    @property
    def flagship(self) -> dict:
        return self.__flagship

    @flagship.setter
    def flagship(self, value: dict):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def lms_id(self) -> dict:
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: dict):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def cross(self) -> dict:
        return self.__cross

    @cross.setter
    def cross(self, value: dict):
        self._property_changed('cross')
        self.__cross = value        

    @property
    def in_code(self) -> dict:
        return self.__in_code

    @in_code.setter
    def in_code(self, value: dict):
        self._property_changed('in_code')
        self.__in_code = value        

    @property
    def asset_parameters_strike_price_relative(self) -> dict:
        return self.__asset_parameters_strike_price_relative

    @asset_parameters_strike_price_relative.setter
    def asset_parameters_strike_price_relative(self, value: dict):
        self._property_changed('asset_parameters_strike_price_relative')
        self.__asset_parameters_strike_price_relative = value        

    @property
    def sts_rates_maturity(self) -> dict:
        return self.__sts_rates_maturity

    @sts_rates_maturity.setter
    def sts_rates_maturity(self, value: dict):
        self._property_changed('sts_rates_maturity')
        self.__sts_rates_maturity = value        

    @property
    def position_source(self) -> dict:
        return self.__position_source

    @position_source.setter
    def position_source(self, value: dict):
        self._property_changed('position_source')
        self.__position_source = value        

    @property
    def listed(self) -> dict:
        return self.__listed

    @listed.setter
    def listed(self, value: dict):
        self._property_changed('listed')
        self.__listed = value        

    @property
    def non_owner_id(self) -> dict:
        return self.__non_owner_id

    @non_owner_id.setter
    def non_owner_id(self, value: dict):
        self._property_changed('non_owner_id')
        self.__non_owner_id = value        

    @property
    def shock_style(self) -> dict:
        return self.__shock_style

    @shock_style.setter
    def shock_style(self, value: dict):
        self._property_changed('shock_style')
        self.__shock_style = value        

    @property
    def g10_currency(self) -> dict:
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: dict):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def strategy(self) -> dict:
        return self.__strategy

    @strategy.setter
    def strategy(self, value: dict):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def methodology(self) -> dict:
        return self.__methodology

    @methodology.setter
    def methodology(self, value: dict):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def isin(self) -> dict:
        return self.__isin

    @isin.setter
    def isin(self, value: dict):
        self._property_changed('isin')
        self.__isin = value        

    @property
    def asset_parameters_strike_type(self) -> dict:
        return self.__asset_parameters_strike_type

    @asset_parameters_strike_type.setter
    def asset_parameters_strike_type(self, value: dict):
        self._property_changed('asset_parameters_strike_type')
        self.__asset_parameters_strike_type = value        


class IndexCurveShift(Scenario):
        
    """A scenario to manipulate index curve shape"""

    @camel_case_translate
    def __init__(
        self,
        market_data_pattern: MarketDataPattern = None,
        annualised_parallel_shift: float = None,
        annualised_slope_shift: float = None,
        cutoff: float = None,
        floor: float = None,
        tenor: str = None,
        rate_option: str = None,
        bucket_shift: float = None,
        bucket_start: datetime.date = None,
        bucket_end: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.market_data_pattern = market_data_pattern
        self.annualised_parallel_shift = annualised_parallel_shift
        self.annualised_slope_shift = annualised_slope_shift
        self.cutoff = cutoff
        self.floor = floor
        self.tenor = tenor
        self.rate_option = rate_option
        self.bucket_shift = bucket_shift
        self.bucket_start = bucket_start
        self.bucket_end = bucket_end
        self.name = name

    @property
    def scenario_type(self) -> str:
        """IndexCurveShift"""
        return 'IndexCurveShift'        

    @property
    def market_data_pattern(self) -> MarketDataPattern:
        """Market pattern for matching curve assets"""
        return self.__market_data_pattern

    @market_data_pattern.setter
    def market_data_pattern(self, value: MarketDataPattern):
        self._property_changed('market_data_pattern')
        self.__market_data_pattern = value        

    @property
    def annualised_parallel_shift(self) -> float:
        """Size of the parallel shift (in bps/year)"""
        return self.__annualised_parallel_shift

    @annualised_parallel_shift.setter
    def annualised_parallel_shift(self, value: float):
        self._property_changed('annualised_parallel_shift')
        self.__annualised_parallel_shift = value        

    @property
    def annualised_slope_shift(self) -> float:
        """Size of the slope shift (in bps/year)"""
        return self.__annualised_slope_shift

    @annualised_slope_shift.setter
    def annualised_slope_shift(self, value: float):
        self._property_changed('annualised_slope_shift')
        self.__annualised_slope_shift = value        

    @property
    def cutoff(self) -> float:
        """The cutoff point (in years)"""
        return self.__cutoff

    @cutoff.setter
    def cutoff(self, value: float):
        self._property_changed('cutoff')
        self.__cutoff = value        

    @property
    def floor(self) -> float:
        """The floor value (in bps)"""
        return self.__floor

    @floor.setter
    def floor(self, value: float):
        self._property_changed('floor')
        self.__floor = value        

    @property
    def tenor(self) -> str:
        """Tenor of rate option to which shock is applied"""
        return self.__tenor

    @tenor.setter
    def tenor(self, value: str):
        self._property_changed('tenor')
        self.__tenor = value        

    @property
    def rate_option(self) -> str:
        """Rate option to which shock is applied"""
        return self.__rate_option

    @rate_option.setter
    def rate_option(self, value: str):
        self._property_changed('rate_option')
        self.__rate_option = value        

    @property
    def bucket_shift(self) -> float:
        """Size of the bucket shift (in bps)"""
        return self.__bucket_shift

    @bucket_shift.setter
    def bucket_shift(self, value: float):
        self._property_changed('bucket_shift')
        self.__bucket_shift = value        

    @property
    def bucket_start(self) -> datetime.date:
        """The start date of the custom bucket"""
        return self.__bucket_start

    @bucket_start.setter
    def bucket_start(self, value: datetime.date):
        self._property_changed('bucket_start')
        self.__bucket_start = value        

    @property
    def bucket_end(self) -> datetime.date:
        """The end date of the custom bucket"""
        return self.__bucket_end

    @bucket_end.setter
    def bucket_end(self, value: datetime.date):
        self._property_changed('bucket_end')
        self.__bucket_end = value        


class MarketDataPatternAndShock(Base):
        
    """A shock to apply to market coordinate values matching the supplied pattern"""

    @camel_case_translate
    def __init__(
        self,
        pattern: MarketDataPattern,
        shock: MarketDataShock,
        name: str = None
    ):        
        super().__init__()
        self.pattern = pattern
        self.shock = shock
        self.name = name

    @property
    def pattern(self) -> MarketDataPattern:
        """A pattern used to match market coordinates"""
        return self.__pattern

    @pattern.setter
    def pattern(self, value: MarketDataPattern):
        self._property_changed('pattern')
        self.__pattern = value        

    @property
    def shock(self) -> MarketDataShock:
        """A shock to apply to market coordinate values"""
        return self.__shock

    @shock.setter
    def shock(self, value: MarketDataShock):
        self._property_changed('shock')
        self.__shock = value        


class MarketDataVolShockScenario(Scenario):
        
    """A scenario to shock volatility surface"""

    @camel_case_translate
    def __init__(
        self,
        pattern: MarketDataPattern,
        shock_type: Union[MarketDataShockType, str],
        vol_levels: Tuple[MarketDataVolSlice, ...],
        ref_spot: float,
        name: str = None
    ):        
        super().__init__()
        self.pattern = pattern
        self.shock_type = shock_type
        self.vol_levels = vol_levels
        self.ref_spot = ref_spot
        self.name = name

    @property
    def scenario_type(self) -> str:
        """MarketDataVolShockScenario"""
        return 'MarketDataVolShockScenario'        

    @property
    def pattern(self) -> MarketDataPattern:
        """A pattern used to match market coordinates"""
        return self.__pattern

    @pattern.setter
    def pattern(self, value: MarketDataPattern):
        self._property_changed('pattern')
        self.__pattern = value        

    @property
    def shock_type(self) -> Union[MarketDataShockType, str]:
        """Market data shock type"""
        return self.__shock_type

    @shock_type.setter
    def shock_type(self, value: Union[MarketDataShockType, str]):
        self._property_changed('shock_type')
        self.__shock_type = get_enum_value(MarketDataShockType, value)        

    @property
    def vol_levels(self) -> Tuple[MarketDataVolSlice, ...]:
        """A volatility slice"""
        return self.__vol_levels

    @vol_levels.setter
    def vol_levels(self, value: Tuple[MarketDataVolSlice, ...]):
        self._property_changed('vol_levels')
        self.__vol_levels = value        

    @property
    def ref_spot(self) -> float:
        return self.__ref_spot

    @ref_spot.setter
    def ref_spot(self, value: float):
        self._property_changed('ref_spot')
        self.__ref_spot = value        


class PCOExposureLeg(Base):
        
    """Parameters required for PCO Exposure Leg"""

    @camel_case_translate
    def __init__(
        self,
        local_to_base_rate: str = None,
        local_nav_limits: Tuple[str, ...] = None,
        base_nav_limits: Tuple[str, ...] = None,
        all_approved_hedge_ratio: str = None,
        show_all_approved_hedge_ratio: bool = None,
        hedge_ratio: str = None,
        exposure_ratio: str = None,
        local_currency: Union[Currency, str] = None,
        target_ratio: str = None,
        benchmark: PCOBenchmark = None,
        long_rebalance_threshold: str = None,
        short_rebalance_threshold: str = None,
        base_nav: str = None,
        local_nav: str = None,
        base_fx_forward: str = None,
        local_fx_forward: str = None,
        auto_roll: bool = None,
        exposure_currencies: Tuple[Union[Currency, str], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.local_to_base_rate = local_to_base_rate
        self.local_nav_limits = local_nav_limits
        self.base_nav_limits = base_nav_limits
        self.all_approved_hedge_ratio = all_approved_hedge_ratio
        self.show_all_approved_hedge_ratio = show_all_approved_hedge_ratio
        self.hedge_ratio = hedge_ratio
        self.exposure_ratio = exposure_ratio
        self.local_currency = local_currency
        self.target_ratio = target_ratio
        self.benchmark = benchmark
        self.long_rebalance_threshold = long_rebalance_threshold
        self.short_rebalance_threshold = short_rebalance_threshold
        self.base_nav = base_nav
        self.local_nav = local_nav
        self.base_fx_forward = base_fx_forward
        self.local_fx_forward = local_fx_forward
        self.auto_roll = auto_roll
        self.exposure_currencies = exposure_currencies
        self.name = name

    @property
    def local_to_base_rate(self) -> str:
        """Previously day FX spot rates for each currency pair"""
        return self.__local_to_base_rate

    @local_to_base_rate.setter
    def local_to_base_rate(self, value: str):
        self._property_changed('local_to_base_rate')
        self.__local_to_base_rate = value        

    @property
    def local_nav_limits(self) -> Tuple[str, ...]:
        """Net Asset Value limits for local currency"""
        return self.__local_nav_limits

    @local_nav_limits.setter
    def local_nav_limits(self, value: Tuple[str, ...]):
        self._property_changed('local_nav_limits')
        self.__local_nav_limits = value        

    @property
    def base_nav_limits(self) -> Tuple[str, ...]:
        """Net Asset Value limits for base currency"""
        return self.__base_nav_limits

    @base_nav_limits.setter
    def base_nav_limits(self, value: Tuple[str, ...]):
        self._property_changed('base_nav_limits')
        self.__base_nav_limits = value        

    @property
    def all_approved_hedge_ratio(self) -> str:
        """Projected hedge ratio"""
        return self.__all_approved_hedge_ratio

    @all_approved_hedge_ratio.setter
    def all_approved_hedge_ratio(self, value: str):
        self._property_changed('all_approved_hedge_ratio')
        self.__all_approved_hedge_ratio = value        

    @property
    def show_all_approved_hedge_ratio(self) -> bool:
        """If UI displays projected hedge ratio"""
        return self.__show_all_approved_hedge_ratio

    @show_all_approved_hedge_ratio.setter
    def show_all_approved_hedge_ratio(self, value: bool):
        self._property_changed('show_all_approved_hedge_ratio')
        self.__show_all_approved_hedge_ratio = value        

    @property
    def hedge_ratio(self) -> str:
        """Ratio of target exposure that is intended to be hedged"""
        return self.__hedge_ratio

    @hedge_ratio.setter
    def hedge_ratio(self, value: str):
        self._property_changed('hedge_ratio')
        self.__hedge_ratio = value        

    @property
    def exposure_ratio(self) -> str:
        """Exposure ratio"""
        return self.__exposure_ratio

    @exposure_ratio.setter
    def exposure_ratio(self, value: str):
        self._property_changed('exposure_ratio')
        self.__exposure_ratio = value        

    @property
    def local_currency(self) -> Union[Currency, str]:
        """Local currency"""
        return self.__local_currency

    @local_currency.setter
    def local_currency(self, value: Union[Currency, str]):
        self._property_changed('local_currency')
        self.__local_currency = get_enum_value(Currency, value)        

    @property
    def target_ratio(self) -> str:
        """Target hedge ratio for each currency"""
        return self.__target_ratio

    @target_ratio.setter
    def target_ratio(self, value: str):
        self._property_changed('target_ratio')
        self.__target_ratio = value        

    @property
    def benchmark(self) -> PCOBenchmark:
        """Benchmark used for each currency"""
        return self.__benchmark

    @benchmark.setter
    def benchmark(self, value: PCOBenchmark):
        self._property_changed('benchmark')
        self.__benchmark = value        

    @property
    def long_rebalance_threshold(self) -> str:
        """Long threshold for TNA adjustment for each currency"""
        return self.__long_rebalance_threshold

    @long_rebalance_threshold.setter
    def long_rebalance_threshold(self, value: str):
        self._property_changed('long_rebalance_threshold')
        self.__long_rebalance_threshold = value        

    @property
    def short_rebalance_threshold(self) -> str:
        """Short threshold for TNA adjustment for each currency"""
        return self.__short_rebalance_threshold

    @short_rebalance_threshold.setter
    def short_rebalance_threshold(self, value: str):
        self._property_changed('short_rebalance_threshold')
        self.__short_rebalance_threshold = value        

    @property
    def base_nav(self) -> str:
        """Total net assets in base currency"""
        return self.__base_nav

    @base_nav.setter
    def base_nav(self, value: str):
        self._property_changed('base_nav')
        self.__base_nav = value        

    @property
    def local_nav(self) -> str:
        """Total net assets in share class currency"""
        return self.__local_nav

    @local_nav.setter
    def local_nav(self, value: str):
        self._property_changed('local_nav')
        self.__local_nav = value        

    @property
    def base_fx_forward(self) -> str:
        """Open hedge notional in base currency"""
        return self.__base_fx_forward

    @base_fx_forward.setter
    def base_fx_forward(self, value: str):
        self._property_changed('base_fx_forward')
        self.__base_fx_forward = value        

    @property
    def local_fx_forward(self) -> str:
        """Open hedge notional in local currency"""
        return self.__local_fx_forward

    @local_fx_forward.setter
    def local_fx_forward(self, value: str):
        self._property_changed('local_fx_forward')
        self.__local_fx_forward = value        

    @property
    def auto_roll(self) -> bool:
        """Whether roll orders will be automatically generated for each currency"""
        return self.__auto_roll

    @auto_roll.setter
    def auto_roll(self, value: bool):
        self._property_changed('auto_roll')
        self.__auto_roll = value        

    @property
    def exposure_currencies(self) -> Tuple[Union[Currency, str], ...]:
        """List of exposure currencies"""
        return self.__exposure_currencies

    @exposure_currencies.setter
    def exposure_currencies(self, value: Tuple[Union[Currency, str], ...]):
        self._property_changed('exposure_currencies')
        self.__exposure_currencies = value        


class User(Base):
        
    _name_mappings = {'root_oe_id': 'rootOEId', 'root_oe_name': 'rootOEName', 'internal_id': 'internalID', 'mi_fidii_trade_idea_declined': 'miFIDIITradeIdeaDeclined'}

    @camel_case_translate
    def __init__(
        self,
        company: str,
        id_: str,
        country: str,
        city: str,
        region: str,
        email: str,
        name: str,
        internal: bool = None,
        system_user: bool = None,
        app_user: bool = None,
        analytics_id: str = None,
        eaa_company: str = None,
        root_oe_id: str = None,
        oe_id: str = None,
        root_oe_name: str = None,
        oe_name: str = None,
        oe_alias: int = None,
        coverage: Tuple[dict, ...] = None,
        internal_email: str = None,
        kerberos: str = None,
        first_name: str = None,
        last_name: str = None,
        internal_id: str = None,
        mi_fidii_trade_idea_declined: str = None,
        department_code: str = None,
        department_name: str = None,
        division_name: str = None,
        business_unit: str = None,
        title: str = None,
        pmd: bool = None,
        login: str = None,
        tokens: Tuple[str, ...] = None,
        roles: Tuple[str, ...] = None,
        groups: Tuple[str, ...] = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        entitlements: Entitlements = None,
        app_managers: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.internal = internal
        self.system_user = system_user
        self.app_user = app_user
        self.analytics_id = analytics_id
        self.city = city
        self.company = company
        self.eaa_company = eaa_company
        self.root_oe_id = root_oe_id
        self.oe_id = oe_id
        self.root_oe_name = root_oe_name
        self.oe_name = oe_name
        self.oe_alias = oe_alias
        self.country = country
        self.coverage = coverage
        self.email = email
        self.internal_email = internal_email
        self.kerberos = kerberos
        self.__id = id_
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.internal_id = internal_id
        self.region = region
        self.mi_fidii_trade_idea_declined = mi_fidii_trade_idea_declined
        self.department_code = department_code
        self.department_name = department_name
        self.division_name = division_name
        self.business_unit = business_unit
        self.title = title
        self.pmd = pmd
        self.login = login
        self.tokens = tokens
        self.roles = roles
        self.groups = groups
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.entitlements = entitlements
        self.app_managers = app_managers

    @property
    def internal(self) -> bool:
        """Is internal"""
        return self.__internal

    @internal.setter
    def internal(self, value: bool):
        self._property_changed('internal')
        self.__internal = value        

    @property
    def system_user(self) -> bool:
        """Is system user"""
        return self.__system_user

    @system_user.setter
    def system_user(self, value: bool):
        self._property_changed('system_user')
        self.__system_user = value        

    @property
    def app_user(self) -> bool:
        """Is app user"""
        return self.__app_user

    @app_user.setter
    def app_user(self, value: bool):
        self._property_changed('app_user')
        self.__app_user = value        

    @property
    def analytics_id(self) -> str:
        """Marquee unique identifier"""
        return self.__analytics_id

    @analytics_id.setter
    def analytics_id(self, value: str):
        self._property_changed('analytics_id')
        self.__analytics_id = value        

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, value: str):
        self._property_changed('city')
        self.__city = value        

    @property
    def company(self) -> str:
        return self.__company

    @company.setter
    def company(self, value: str):
        self._property_changed('company')
        self.__company = value        

    @property
    def eaa_company(self) -> str:
        return self.__eaa_company

    @eaa_company.setter
    def eaa_company(self, value: str):
        self._property_changed('eaa_company')
        self.__eaa_company = value        

    @property
    def root_oe_id(self) -> str:
        """Goldman Sachs unique identifier for user's root organization"""
        return self.__root_oe_id

    @root_oe_id.setter
    def root_oe_id(self, value: str):
        self._property_changed('root_oe_id')
        self.__root_oe_id = value        

    @property
    def oe_id(self) -> str:
        """Goldman Sachs unique identifier for user's organization"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def root_oe_name(self) -> str:
        """The name of the company."""
        return self.__root_oe_name

    @root_oe_name.setter
    def root_oe_name(self, value: str):
        self._property_changed('root_oe_name')
        self.__root_oe_name = value        

    @property
    def oe_name(self) -> str:
        """The name of the company."""
        return self.__oe_name

    @oe_name.setter
    def oe_name(self, value: str):
        self._property_changed('oe_name')
        self.__oe_name = value        

    @property
    def oe_alias(self) -> int:
        """Goldman Sachs alias for user's organization"""
        return self.__oe_alias

    @oe_alias.setter
    def oe_alias(self, value: int):
        self._property_changed('oe_alias')
        self.__oe_alias = value        

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str):
        self._property_changed('country')
        self.__country = value        

    @property
    def coverage(self) -> Tuple[dict, ...]:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: Tuple[dict, ...]):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def internal_email(self) -> str:
        return self.__internal_email

    @internal_email.setter
    def internal_email(self, value: str):
        self._property_changed('internal_email')
        self.__internal_email = value        

    @property
    def kerberos(self) -> str:
        return self.__kerberos

    @kerberos.setter
    def kerberos(self, value: str):
        self._property_changed('kerberos')
        self.__kerberos = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        self._property_changed('first_name')
        self.__first_name = value        

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        self._property_changed('last_name')
        self.__last_name = value        

    @property
    def internal_id(self) -> str:
        return self.__internal_id

    @internal_id.setter
    def internal_id(self, value: str):
        self._property_changed('internal_id')
        self.__internal_id = value        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def mi_fidii_trade_idea_declined(self) -> str:
        return self.__mi_fidii_trade_idea_declined

    @mi_fidii_trade_idea_declined.setter
    def mi_fidii_trade_idea_declined(self, value: str):
        self._property_changed('mi_fidii_trade_idea_declined')
        self.__mi_fidii_trade_idea_declined = value        

    @property
    def department_code(self) -> str:
        return self.__department_code

    @department_code.setter
    def department_code(self, value: str):
        self._property_changed('department_code')
        self.__department_code = value        

    @property
    def department_name(self) -> str:
        return self.__department_name

    @department_name.setter
    def department_name(self, value: str):
        self._property_changed('department_name')
        self.__department_name = value        

    @property
    def division_name(self) -> str:
        return self.__division_name

    @division_name.setter
    def division_name(self, value: str):
        self._property_changed('division_name')
        self.__division_name = value        

    @property
    def business_unit(self) -> str:
        return self.__business_unit

    @business_unit.setter
    def business_unit(self, value: str):
        self._property_changed('business_unit')
        self.__business_unit = value        

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def pmd(self) -> bool:
        """Is a PMD."""
        return self.__pmd

    @pmd.setter
    def pmd(self, value: bool):
        self._property_changed('pmd')
        self.__pmd = value        

    @property
    def login(self) -> str:
        return self.__login

    @login.setter
    def login(self, value: str):
        self._property_changed('login')
        self.__login = value        

    @property
    def tokens(self) -> Tuple[str, ...]:
        return self.__tokens

    @tokens.setter
    def tokens(self, value: Tuple[str, ...]):
        self._property_changed('tokens')
        self.__tokens = value        

    @property
    def roles(self) -> Tuple[str, ...]:
        """Role set used for entitlements"""
        return self.__roles

    @roles.setter
    def roles(self, value: Tuple[str, ...]):
        self._property_changed('roles')
        self.__roles = value        

    @property
    def groups(self) -> Tuple[str, ...]:
        """Group set used for data level entitlements"""
        return self.__groups

    @groups.setter
    def groups(self, value: Tuple[str, ...]):
        self._property_changed('groups')
        self.__groups = value        

    @property
    def created_by_id(self) -> str:
        """Marquee unique identifier"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Timestamp of when the user was created"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_by_id(self) -> str:
        """Marquee unique identifier"""
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
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def app_managers(self) -> Tuple[str, ...]:
        """Application managers associated with the app user"""
        return self.__app_managers

    @app_managers.setter
    def app_managers(self, value: Tuple[str, ...]):
        self._property_changed('app_managers')
        self.__app_managers = value        


class CSLScheduleArray(Base):
        
    """An array of schedules"""

    @camel_case_translate
    def __init__(
        self,
        schedule_values: Tuple[CSLSchedule, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.schedule_values = schedule_values
        self.name = name

    @property
    def schedule_values(self) -> Tuple[CSLSchedule, ...]:
        """A schedule"""
        return self.__schedule_values

    @schedule_values.setter
    def schedule_values(self, value: Tuple[CSLSchedule, ...]):
        self._property_changed('schedule_values')
        self.__schedule_values = value        


class EntityQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        format_: Union[Format, str] = None,
        where: FieldFilterMap = None,
        as_of_time: datetime.datetime = None,
        last_updated_since: datetime.datetime = None,
        date: datetime.date = None,
        time: datetime.datetime = None,
        delay: int = None,
        order_by: Tuple[Union[dict, str], ...] = None,
        scroll: str = None,
        scroll_id: str = None,
        fields: Tuple[Union[dict, str], ...] = None,
        limit: int = None,
        offset: int = None,
        vendor: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__format = get_enum_value(Format, format_)
        self.where = where
        self.as_of_time = as_of_time
        self.last_updated_since = last_updated_since
        self.date = date
        self.time = time
        self.delay = delay
        self.order_by = order_by
        self.scroll = scroll
        self.scroll_id = scroll_id
        self.fields = fields
        self.limit = limit
        self.offset = offset
        self.vendor = vendor
        self.name = name

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def where(self) -> FieldFilterMap:
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMap):
        self._property_changed('where')
        self.__where = value        

    @property
    def as_of_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__as_of_time

    @as_of_time.setter
    def as_of_time(self, value: datetime.datetime):
        self._property_changed('as_of_time')
        self.__as_of_time = value        

    @property
    def last_updated_since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: datetime.datetime):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__time

    @time.setter
    def time(self, value: datetime.datetime):
        self._property_changed('time')
        self.__time = value        

    @property
    def delay(self) -> int:
        """Number of minutes to delay returning data"""
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def order_by(self) -> Tuple[Union[dict, str], ...]:
        return self.__order_by

    @order_by.setter
    def order_by(self, value: Tuple[Union[dict, str], ...]):
        self._property_changed('order_by')
        self.__order_by = value        

    @property
    def scroll(self) -> str:
        """Time for which to keep the scroll search context alive, i.e. 1m (1 minute) or
           10s (10 seconds)"""
        return self.__scroll

    @scroll.setter
    def scroll(self, value: str):
        self._property_changed('scroll')
        self.__scroll = value        

    @property
    def scroll_id(self) -> str:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scroll_id

    @scroll_id.setter
    def scroll_id(self, value: str):
        self._property_changed('scroll_id')
        self.__scroll_id = value        

    @property
    def fields(self) -> Tuple[Union[dict, str], ...]:
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[dict, str], ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def limit(self) -> int:
        """Limit on the number of objects to be returned in the response. Can range between
           1 and 10000"""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self._property_changed('limit')
        self.__limit = value        

    @property
    def offset(self) -> int:
        """The offset of the first result returned (default 0). Can be used in pagination
           to defined the first item in the list to be returned, for example if
           you request 100 objects, to query the next page you would specify
           offset = 100."""
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self._property_changed('offset')
        self.__offset = value        

    @property
    def vendor(self) -> str:
        """Risk model vendor name"""
        return self.__vendor

    @vendor.setter
    def vendor(self, value: str):
        self._property_changed('vendor')
        self.__vendor = value        


class MarketDataShockBasedScenario(Scenario):
        
    """A scenario comprised of user-defined market data shocks"""

    @camel_case_translate
    def __init__(
        self,
        shocks: Tuple[MarketDataPatternAndShock, ...],
        name: str = None
    ):        
        super().__init__()
        self.shocks = shocks
        self.name = name

    @property
    def scenario_type(self) -> str:
        """MarketDataShockBasedScenario"""
        return 'MarketDataShockBasedScenario'        

    @property
    def shocks(self) -> Tuple[MarketDataPatternAndShock, ...]:
        """A shock to apply to market coordinate values matching the supplied pattern"""
        return self.__shocks

    @shocks.setter
    def shocks(self, value: Tuple[MarketDataPatternAndShock, ...]):
        self._property_changed('shocks')
        self.__shocks = value        


class OverlayMarket(Base):
        
    """A market with explicit coordinate values overlayed over a base market"""

    @camel_case_translate
    def __init__(
        self,
        base_market: Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket],
        market_data: Tuple[MarketDataCoordinateValue, ...],
        name: str = None
    ):        
        super().__init__()
        self.base_market = base_market
        self.market_data = market_data
        self.name = name

    @property
    def market_type(self) -> str:
        """OverlayMarket"""
        return 'OverlayMarket'        

    @property
    def base_market(self) -> Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket]:
        """The base market"""
        return self.__base_market

    @base_market.setter
    def base_market(self, value: Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket]):
        self._property_changed('base_market')
        self.__base_market = value        

    @property
    def market_data(self) -> Tuple[MarketDataCoordinateValue, ...]:
        """Market data to overlay over the base market"""
        return self.__market_data

    @market_data.setter
    def market_data(self, value: Tuple[MarketDataCoordinateValue, ...]):
        self._property_changed('market_data')
        self.__market_data = value        


class PCOExposure(Base):
        
    """Parameters required for PCO Exposure"""

    @camel_case_translate
    def __init__(
        self,
        last_data_updated_date_time: datetime.datetime = None,
        nav_includes_fx_hedges: bool = None,
        use_fx_rate_on_base_fx_forward: bool = None,
        last_generate_orders_date_time: datetime.datetime = None,
        legs: Tuple[PCOExposureLeg, ...] = None,
        adjustments: PCOExposureAdjustments = None,
        ratio_mode: str = None,
        hedge_calc_currency: Union[PCOCurrencyType, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.last_data_updated_date_time = last_data_updated_date_time
        self.nav_includes_fx_hedges = nav_includes_fx_hedges
        self.use_fx_rate_on_base_fx_forward = use_fx_rate_on_base_fx_forward
        self.last_generate_orders_date_time = last_generate_orders_date_time
        self.legs = legs
        self.adjustments = adjustments
        self.ratio_mode = ratio_mode
        self.hedge_calc_currency = hedge_calc_currency
        self.name = name

    @property
    def last_data_updated_date_time(self) -> datetime.datetime:
        """Last time when data was updated"""
        return self.__last_data_updated_date_time

    @last_data_updated_date_time.setter
    def last_data_updated_date_time(self, value: datetime.datetime):
        self._property_changed('last_data_updated_date_time')
        self.__last_data_updated_date_time = value        

    @property
    def nav_includes_fx_hedges(self) -> bool:
        """Whether Net Asset Value includes FX hedges"""
        return self.__nav_includes_fx_hedges

    @nav_includes_fx_hedges.setter
    def nav_includes_fx_hedges(self, value: bool):
        self._property_changed('nav_includes_fx_hedges')
        self.__nav_includes_fx_hedges = value        

    @property
    def use_fx_rate_on_base_fx_forward(self) -> bool:
        """Use open hedge in notional of base currency or local currency"""
        return self.__use_fx_rate_on_base_fx_forward

    @use_fx_rate_on_base_fx_forward.setter
    def use_fx_rate_on_base_fx_forward(self, value: bool):
        self._property_changed('use_fx_rate_on_base_fx_forward')
        self.__use_fx_rate_on_base_fx_forward = value        

    @property
    def last_generate_orders_date_time(self) -> datetime.datetime:
        """Last time when orders are generated"""
        return self.__last_generate_orders_date_time

    @last_generate_orders_date_time.setter
    def last_generate_orders_date_time(self, value: datetime.datetime):
        self._property_changed('last_generate_orders_date_time')
        self.__last_generate_orders_date_time = value        

    @property
    def legs(self) -> Tuple[PCOExposureLeg, ...]:
        """Exposure details for each leg"""
        return self.__legs

    @legs.setter
    def legs(self, value: Tuple[PCOExposureLeg, ...]):
        self._property_changed('legs')
        self.__legs = value        

    @property
    def adjustments(self) -> PCOExposureAdjustments:
        """Exposure adjustments"""
        return self.__adjustments

    @adjustments.setter
    def adjustments(self, value: PCOExposureAdjustments):
        self._property_changed('adjustments')
        self.__adjustments = value        

    @property
    def ratio_mode(self) -> str:
        """One of hedge ratio or exposure ratio"""
        return self.__ratio_mode

    @ratio_mode.setter
    def ratio_mode(self, value: str):
        self._property_changed('ratio_mode')
        self.__ratio_mode = value        

    @property
    def hedge_calc_currency(self) -> Union[PCOCurrencyType, str]:
        """One of Local and Base"""
        return self.__hedge_calc_currency

    @hedge_calc_currency.setter
    def hedge_calc_currency(self, value: Union[PCOCurrencyType, str]):
        self._property_changed('hedge_calc_currency')
        self.__hedge_calc_currency = get_enum_value(PCOCurrencyType, value)        


class RiskMeasure(Base):
        
    """The measure to perform risk on. Each risk measure consists of an asset class, a
       measure type, and a unit."""

    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        measure_type: Union[RiskMeasureType, str] = None,
        unit: Union[RiskMeasureUnit, str] = None,
        parameters: Union[CurrencyParameter, FiniteDifferenceParameter, ListOfNumberParameter, ListOfStringParameter, MapParameter, StringParameter] = None,
        value: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.measure_type = measure_type
        self.unit = unit
        self.parameters = parameters
        self.value = value
        self.name = name

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def measure_type(self) -> Union[RiskMeasureType, str]:
        """The type of measure to perform risk on. e.g. Greeks"""
        return self.__measure_type

    @measure_type.setter
    def measure_type(self, value: Union[RiskMeasureType, str]):
        self._property_changed('measure_type')
        self.__measure_type = get_enum_value(RiskMeasureType, value)        

    @property
    def unit(self) -> Union[RiskMeasureUnit, str]:
        """The unit of change of underlying in the risk computation."""
        return self.__unit

    @unit.setter
    def unit(self, value: Union[RiskMeasureUnit, str]):
        self._property_changed('unit')
        self.__unit = get_enum_value(RiskMeasureUnit, value)        

    @property
    def parameters(self) -> Union[CurrencyParameter, FiniteDifferenceParameter, ListOfNumberParameter, ListOfStringParameter, MapParameter, StringParameter]:
        """Extra Params for Parameterised Risk Measures"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: Union[CurrencyParameter, FiniteDifferenceParameter, ListOfNumberParameter, ListOfStringParameter, MapParameter, StringParameter]):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def value(self) -> Union[float, str]:
        """Value of this measure"""
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


class DataSetFieldMap(Base):
        
    """The mapping between data set field and risk measure type"""

    @camel_case_translate
    def __init__(
        self,
        data_set_id: str,
        field: str,
        results_field: str,
        risk_measure: RiskMeasure,
        name: str = None
    ):        
        super().__init__()
        self.data_set_id = data_set_id
        self.field = field
        self.results_field = results_field
        self.risk_measure = risk_measure
        self.name = name

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def field(self) -> str:
        """The field for data set, e.g. rate"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def results_field(self) -> str:
        """The source field in the results, e.g. value or fixedRate"""
        return self.__results_field

    @results_field.setter
    def results_field(self, value: str):
        self._property_changed('results_field')
        self.__results_field = value        

    @property
    def risk_measure(self) -> RiskMeasure:
        """The measure to perform risk on. Each risk measure consists of an asset class, a
           measure type, and a unit."""
        return self.__risk_measure

    @risk_measure.setter
    def risk_measure(self, value: RiskMeasure):
        self._property_changed('risk_measure')
        self.__risk_measure = value        


class CompositeScenario(Base):
        
    """A scenario for composing scenarios"""

    @camel_case_translate
    def __init__(
        self,
        scenarios: Tuple[Scenario, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.scenarios = scenarios
        self.name = name

    @property
    def scenario_type(self) -> str:
        """CompositeScenario"""
        return 'CompositeScenario'        

    @property
    def scenarios(self) -> Tuple[Scenario, ...]:
        """The scenarios, in order"""
        return self.__scenarios

    @scenarios.setter
    def scenarios(self, value: Tuple[Scenario, ...]):
        self._property_changed('scenarios')
        self.__scenarios = value        


class Position(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        quantity: float = None,
        notional: float = None,
        party_to: SimpleParty = None,
        party_from: SimpleParty = None,
        external_ids: Tuple[dict, ...] = None,
        margin_ids: Tuple[dict, ...] = None,
        tags: Tuple[PositionTag, ...] = None,
        instrument: InstrumentBase = None,
        description: str = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.quantity = quantity
        self.notional = notional
        self.party_to = party_to
        self.party_from = party_from
        self.external_ids = external_ids
        self.margin_ids = margin_ids
        self.tags = tags
        self.instrument = instrument
        self.description = description
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def quantity(self) -> float:
        """Quantity of position"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def notional(self) -> float:
        """Notional of position"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def party_to(self) -> SimpleParty:
        return self.__party_to

    @party_to.setter
    def party_to(self, value: SimpleParty):
        self._property_changed('party_to')
        self.__party_to = value        

    @property
    def party_from(self) -> SimpleParty:
        return self.__party_from

    @party_from.setter
    def party_from(self, value: SimpleParty):
        self._property_changed('party_from')
        self.__party_from = value        

    @property
    def external_ids(self) -> Tuple[dict, ...]:
        """A list of identifiers (external to Marquee) for this position"""
        return self.__external_ids

    @external_ids.setter
    def external_ids(self, value: Tuple[dict, ...]):
        self._property_changed('external_ids')
        self.__external_ids = value        

    @property
    def margin_ids(self) -> Tuple[dict, ...]:
        """A list of margin identifiers (e.g. CSA) for this position"""
        return self.__margin_ids

    @margin_ids.setter
    def margin_ids(self, value: Tuple[dict, ...]):
        self._property_changed('margin_ids')
        self.__margin_ids = value        

    @property
    def tags(self) -> Tuple[PositionTag, ...]:
        """Array of tag name and values associated with the position."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[PositionTag, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def instrument(self) -> InstrumentBase:
        """Valid Instruments"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: InstrumentBase):
        self._property_changed('instrument')
        self.__instrument = value        

    @property
    def description(self) -> str:
        """Description of a particular trade or position."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        


class RelativeMarket(Base):
        
    """Market for pricing between two states (e.g. for PnlExplain)"""

    @camel_case_translate
    def __init__(
        self,
        from_market: Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket, OverlayMarket],
        to_market: Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket, OverlayMarket],
        name: str = None
    ):        
        super().__init__()
        self.from_market = from_market
        self.to_market = to_market
        self.name = name

    @property
    def market_type(self) -> str:
        """RelativeMarket"""
        return 'RelativeMarket'        

    @property
    def from_market(self) -> Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket, OverlayMarket]:
        """The base market"""
        return self.__from_market

    @from_market.setter
    def from_market(self, value: Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket, OverlayMarket]):
        self._property_changed('from_market')
        self.__from_market = value        

    @property
    def to_market(self) -> Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket, OverlayMarket]:
        """The target market"""
        return self.__to_market

    @to_market.setter
    def to_market(self, value: Union[CloseMarket, LiveMarket, RefMarket, TimestampedMarket, OverlayMarket]):
        self._property_changed('to_market')
        self.__to_market = value        


class MarketDataScenario(Base):
        
    """A market data scenario to apply to the calculation"""

    @camel_case_translate
    def __init__(
        self,
        scenario: dict,
        subtract_base: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.scenario = scenario
        self.subtract_base = subtract_base
        self.name = name

    @property
    def scenario(self) -> dict:
        """The scenario"""
        return self.__scenario

    @scenario.setter
    def scenario(self, value: dict):
        self._property_changed('scenario')
        self.__scenario = value        

    @property
    def subtract_base(self) -> bool:
        """Subtract values computed under the base market data state, to return a diff, if
           true"""
        return self.__subtract_base

    @subtract_base.setter
    def subtract_base(self, value: bool):
        self._property_changed('subtract_base')
        self.__subtract_base = value        


class PricingDateAndMarketDataAsOf(Base):
        
    """Pricing date and market data as of (date or time)"""

    @camel_case_translate
    def __init__(
        self,
        pricing_date: datetime.date,
        market_data_as_of: Union[datetime.date, datetime.datetime] = None,
        market: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.pricing_date = pricing_date
        self.market_data_as_of = market_data_as_of
        self.market = market
        self.name = name

    @property
    def pricing_date(self) -> datetime.date:
        """The date for which to perform the calculation"""
        return self.__pricing_date

    @pricing_date.setter
    def pricing_date(self, value: datetime.date):
        self._property_changed('pricing_date')
        self.__pricing_date = value        

    @property
    def market_data_as_of(self) -> Union[datetime.date, datetime.datetime]:
        """The date or time to source market data"""
        return self.__market_data_as_of

    @market_data_as_of.setter
    def market_data_as_of(self, value: Union[datetime.date, datetime.datetime]):
        self._property_changed('market_data_as_of')
        self.__market_data_as_of = value        

    @property
    def market(self) -> dict:
        """The market used for pricing"""
        return self.__market

    @market.setter
    def market(self, value: dict):
        self._property_changed('market')
        self.__market = value        


class LiquidityRequest(Base):
        
    """Required parameters in order to get liquidity information on a set of positions"""

    @camel_case_translate
    def __init__(
        self,
        notional: float = None,
        positions: dict = None,
        risk_model: str = None,
        date: datetime.date = None,
        currency: Union[Currency, str] = None,
        participation_rate: float = None,
        execution_horizon: float = None,
        execution_start_time: datetime.datetime = None,
        execution_end_time: datetime.datetime = None,
        benchmark_id: str = None,
        measures: Tuple[Union[LiquidityMeasure, str], ...] = None,
        time_series_benchmark_ids: Tuple[str, ...] = None,
        time_series_start_date: datetime.date = None,
        time_series_end_date: datetime.date = None,
        format_: Union[Format, str] = None,
        report_parameters: LiquidityReportParameters = None,
        explode_positions: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.notional = notional
        self.positions = positions
        self.risk_model = risk_model
        self.date = date
        self.currency = currency
        self.participation_rate = participation_rate
        self.execution_horizon = execution_horizon
        self.execution_start_time = execution_start_time
        self.execution_end_time = execution_end_time
        self.benchmark_id = benchmark_id
        self.measures = measures
        self.time_series_benchmark_ids = time_series_benchmark_ids
        self.time_series_start_date = time_series_start_date
        self.time_series_end_date = time_series_end_date
        self.__format = get_enum_value(Format, format_)
        self.report_parameters = report_parameters
        self.explode_positions = explode_positions
        self.name = name

    @property
    def notional(self) -> float:
        """Notional value of the positions."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def positions(self) -> dict:
        """A set of quantity or weighted positions."""
        return self.__positions

    @positions.setter
    def positions(self, value: dict):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def participation_rate(self) -> float:
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def execution_horizon(self) -> float:
        return self.__execution_horizon

    @execution_horizon.setter
    def execution_horizon(self, value: float):
        self._property_changed('execution_horizon')
        self.__execution_horizon = value        

    @property
    def execution_start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_start_time

    @execution_start_time.setter
    def execution_start_time(self, value: datetime.datetime):
        self._property_changed('execution_start_time')
        self.__execution_start_time = value        

    @property
    def execution_end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_end_time

    @execution_end_time.setter
    def execution_end_time(self, value: datetime.datetime):
        self._property_changed('execution_end_time')
        self.__execution_end_time = value        

    @property
    def benchmark_id(self) -> str:
        """Marquee unique asset identifier of the benchmark."""
        return self.__benchmark_id

    @benchmark_id.setter
    def benchmark_id(self, value: str):
        self._property_changed('benchmark_id')
        self.__benchmark_id = value        

    @property
    def measures(self) -> Tuple[Union[LiquidityMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[LiquidityMeasure, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def time_series_benchmark_ids(self) -> Tuple[str, ...]:
        """Marquee unique identifiers of assets to be used as benchmarks."""
        return self.__time_series_benchmark_ids

    @time_series_benchmark_ids.setter
    def time_series_benchmark_ids(self, value: Tuple[str, ...]):
        self._property_changed('time_series_benchmark_ids')
        self.__time_series_benchmark_ids = value        

    @property
    def time_series_start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__time_series_start_date

    @time_series_start_date.setter
    def time_series_start_date(self, value: datetime.date):
        self._property_changed('time_series_start_date')
        self.__time_series_start_date = value        

    @property
    def time_series_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__time_series_end_date

    @time_series_end_date.setter
    def time_series_end_date(self, value: datetime.date):
        self._property_changed('time_series_end_date')
        self.__time_series_end_date = value        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def report_parameters(self) -> LiquidityReportParameters:
        """Parameters to be used on liquidity reports"""
        return self.__report_parameters

    @report_parameters.setter
    def report_parameters(self, value: LiquidityReportParameters):
        self._property_changed('report_parameters')
        self.__report_parameters = value        

    @property
    def explode_positions(self) -> bool:
        """Flag determining whether the positions should be exploded before doing
           calculations."""
        return self.__explode_positions

    @explode_positions.setter
    def explode_positions(self, value: bool):
        self._property_changed('explode_positions')
        self.__explode_positions = value        


class PositionSet(Base):
        
    @camel_case_translate
    def __init__(
        self,
        positions: Tuple[Position, ...],
        position_date: datetime.date,
        id_: str = None,
        last_update_time: datetime.datetime = None,
        type_: str = None,
        divisor: float = None,
        last_updated_time: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.position_date = position_date
        self.last_update_time = last_update_time
        self.positions = positions
        self.__type = type_
        self.divisor = divisor
        self.last_updated_time = last_updated_time
        self.name = name

    @property
    def id(self) -> str:
        """Unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def position_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__position_date

    @position_date.setter
    def position_date(self, value: datetime.date):
        self._property_changed('position_date')
        self.__position_date = value        

    @property
    def last_update_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_update_time

    @last_update_time.setter
    def last_update_time(self, value: datetime.datetime):
        self._property_changed('last_update_time')
        self.__last_update_time = value        

    @property
    def positions(self) -> Tuple[Position, ...]:
        """Array of quantity position objects."""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[Position, ...]):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def type(self) -> str:
        """The composition type of a Portfolio"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def divisor(self) -> float:
        """optional index divisor for a position set"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: float):
        self._property_changed('divisor')
        self.__divisor = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        


class RiskPosition(Base):
        
    @camel_case_translate
    def __init__(
        self,
        instrument: Priceable,
        quantity: float = None,
        name: str = None
    ):        
        super().__init__()
        self.instrument = instrument
        self.quantity = quantity
        self.name = name

    @property
    def instrument(self) -> Priceable:
        """Instrument or Id   To specify a Marquee asset use the asset Id. For listed
           products use an XRef, e.g. { 'bid': 'NGZ19 Comdty' }, { 'isin':
           'US912810SD19' }. To specify an instrument use one of the listed
           types"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: Priceable):
        self._property_changed('instrument')
        self.__instrument = value        

    @property
    def quantity(self) -> float:
        """Quantity of instrument"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        


class RiskRequest(Base):
        
    """Object representation of a risk calculation request"""

    @camel_case_translate
    def __init__(
        self,
        positions: Tuple[RiskPosition, ...],
        measures: Tuple[RiskMeasure, ...],
        pricing_and_market_data_as_of: Tuple[PricingDateAndMarketDataAsOf, ...] = None,
        pricing_location: Union[PricingLocation, str] = None,
        wait_for_results: bool = False,
        scenario: MarketDataScenario = None,
        parameters: RiskRequestParameters = None,
        request_visible_to_gs: bool = False,
        use_cache: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.positions = positions
        self.measures = measures
        self.pricing_and_market_data_as_of = pricing_and_market_data_as_of
        self.pricing_location = pricing_location
        self.wait_for_results = wait_for_results
        self.scenario = scenario
        self.parameters = parameters
        self.request_visible_to_gs = request_visible_to_gs
        self.use_cache = use_cache
        self.name = name

    @property
    def positions(self) -> Tuple[RiskPosition, ...]:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[RiskPosition, ...]):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def measures(self) -> Tuple[RiskMeasure, ...]:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta',
           'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[RiskMeasure, ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def pricing_and_market_data_as_of(self) -> Tuple[PricingDateAndMarketDataAsOf, ...]:
        """Pricing date and market data as of (date or time)"""
        return self.__pricing_and_market_data_as_of

    @pricing_and_market_data_as_of.setter
    def pricing_and_market_data_as_of(self, value: Tuple[PricingDateAndMarketDataAsOf, ...]):
        self._property_changed('pricing_and_market_data_as_of')
        self.__pricing_and_market_data_as_of = value        

    @property
    def pricing_location(self) -> Union[PricingLocation, str]:
        """The location for pricing and market data"""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: Union[PricingLocation, str]):
        self._property_changed('pricing_location')
        self.__pricing_location = get_enum_value(PricingLocation, value)        

    @property
    def wait_for_results(self) -> bool:
        """For short-running requests this may be set to true and the results will be
           returned directly. If false, the response will contain the Id to
           retrieve the results"""
        return self.__wait_for_results

    @wait_for_results.setter
    def wait_for_results(self, value: bool):
        self._property_changed('wait_for_results')
        self.__wait_for_results = value        

    @property
    def scenario(self) -> MarketDataScenario:
        """A market data scenario to apply to the calculation"""
        return self.__scenario

    @scenario.setter
    def scenario(self, value: MarketDataScenario):
        self._property_changed('scenario')
        self.__scenario = value        

    @property
    def parameters(self) -> RiskRequestParameters:
        """Parameters for the risk request"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: RiskRequestParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def request_visible_to_gs(self) -> bool:
        """Is the request visible to GS logging?"""
        return self.__request_visible_to_gs

    @request_visible_to_gs.setter
    def request_visible_to_gs(self, value: bool):
        self._property_changed('request_visible_to_gs')
        self.__request_visible_to_gs = value        

    @property
    def use_cache(self) -> bool:
        """Should results be cached in the risk service?"""
        return self.__use_cache

    @use_cache.setter
    def use_cache(self, value: bool):
        self._property_changed('use_cache')
        self.__use_cache = value        


class ReportParameters(Base):
        
    """Parameters specific to the report type"""

    _name_mappings = {'enable_rfq': 'enableRFQ'}

    @camel_case_translate
    def __init__(
        self,
        approval_id: str = None,
        asset_class: Union[AssetClass, str] = None,
        transaction_cost_model: str = None,
        trading_cost: float = None,
        servicing_cost_long: float = None,
        servicing_cost_short: float = None,
        region: str = None,
        risk_model: str = None,
        fx_hedged: bool = None,
        publish_to_bloomberg: bool = None,
        publish_to_reuters: bool = None,
        publish_to_factset: bool = None,
        include_price_history: bool = None,
        index_update: bool = None,
        index_rebalance: bool = None,
        index_source_id: str = None,
        basket_action: Union[BasketAction, str] = None,
        api_domain: bool = None,
        initial_price: float = None,
        stock_level_exposures: bool = None,
        explode_positions: bool = None,
        scenario_id: str = None,
        scenario_ids: Tuple[str, ...] = None,
        scenario_group_id: str = None,
        scenario_type: Union[ScenarioType, str] = None,
        market_model_id: str = None,
        risk_measures: Tuple[RiskMeasure, ...] = None,
        initial_pricing_date: datetime.date = None,
        backcast: bool = None,
        risk_request: RiskRequest = None,
        participation_rate: float = None,
        approve_rebalance: bool = None,
        auto_approved_rebalance: bool = None,
        use_risk_request_batch_mode: bool = False,
        limited_access_assets: Tuple[str, ...] = None,
        corporate_action_restricted_assets: Tuple[str, ...] = None,
        backcast_dates: Tuple[datetime.date, ...] = None,
        base_currency: Union[Currency, str] = None,
        local_currency: Union[Currency, str] = None,
        fund_calendar: str = None,
        calculation_currency: Union[PCOCurrencyType, str] = None,
        hedge_settlement_interval: Tuple[PCOParameterValues, ...] = None,
        hedge_settlement_day: Tuple[PCOParameterValues, ...] = None,
        roll_horizon: Tuple[PCOParameterValues, ...] = None,
        pnl_currency: Tuple[PCOParameterValues, ...] = None,
        nav_publication_period: Tuple[PCOParameterValues, ...] = None,
        roll_date_zero_threshold: bool = None,
        unrealised_mark_to_market: PCOUnrealisedMarkToMarket = None,
        target_deviation: Tuple[PCOTargetDeviation, ...] = None,
        cash_balances: Tuple[PCOCashBalance, ...] = None,
        exposure: PCOExposure = None,
        pco_share_class: PCOShareClass = None,
        settlements: Tuple[PCOSettlements, ...] = None,
        show_cash: bool = None,
        show_exposure: bool = None,
        enable_rfq: bool = None,
        fixing_descriptions: Tuple[str, ...] = None,
        pco_origin: Union[PCOOrigin, str] = None,
        pco_action_type: Union[PCOActionType, str] = None,
        version: str = None,
        roll_currency: Tuple[PCOParameterValues, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.approval_id = approval_id
        self.asset_class = asset_class
        self.transaction_cost_model = transaction_cost_model
        self.trading_cost = trading_cost
        self.servicing_cost_long = servicing_cost_long
        self.servicing_cost_short = servicing_cost_short
        self.region = region
        self.risk_model = risk_model
        self.fx_hedged = fx_hedged
        self.publish_to_bloomberg = publish_to_bloomberg
        self.publish_to_reuters = publish_to_reuters
        self.publish_to_factset = publish_to_factset
        self.include_price_history = include_price_history
        self.index_update = index_update
        self.index_rebalance = index_rebalance
        self.index_source_id = index_source_id
        self.basket_action = basket_action
        self.api_domain = api_domain
        self.initial_price = initial_price
        self.stock_level_exposures = stock_level_exposures
        self.explode_positions = explode_positions
        self.scenario_id = scenario_id
        self.scenario_ids = scenario_ids
        self.scenario_group_id = scenario_group_id
        self.scenario_type = scenario_type
        self.market_model_id = market_model_id
        self.risk_measures = risk_measures
        self.initial_pricing_date = initial_pricing_date
        self.backcast = backcast
        self.risk_request = risk_request
        self.participation_rate = participation_rate
        self.approve_rebalance = approve_rebalance
        self.auto_approved_rebalance = auto_approved_rebalance
        self.use_risk_request_batch_mode = use_risk_request_batch_mode
        self.limited_access_assets = limited_access_assets
        self.corporate_action_restricted_assets = corporate_action_restricted_assets
        self.backcast_dates = backcast_dates
        self.base_currency = base_currency
        self.local_currency = local_currency
        self.fund_calendar = fund_calendar
        self.calculation_currency = calculation_currency
        self.hedge_settlement_interval = hedge_settlement_interval
        self.hedge_settlement_day = hedge_settlement_day
        self.roll_horizon = roll_horizon
        self.pnl_currency = pnl_currency
        self.nav_publication_period = nav_publication_period
        self.roll_date_zero_threshold = roll_date_zero_threshold
        self.unrealised_mark_to_market = unrealised_mark_to_market
        self.target_deviation = target_deviation
        self.cash_balances = cash_balances
        self.exposure = exposure
        self.pco_share_class = pco_share_class
        self.settlements = settlements
        self.show_cash = show_cash
        self.show_exposure = show_exposure
        self.enable_rfq = enable_rfq
        self.fixing_descriptions = fixing_descriptions
        self.pco_origin = pco_origin
        self.pco_action_type = pco_action_type
        self.version = version
        self.roll_currency = roll_currency
        self.name = name

    @property
    def approval_id(self) -> str:
        """Marquee unique identifier of approval created, only present in case of basket
           rebalance"""
        return self.__approval_id

    @approval_id.setter
    def approval_id(self, value: str):
        self._property_changed('approval_id')
        self.__approval_id = value        

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def transaction_cost_model(self) -> str:
        """Determines which model to use"""
        return self.__transaction_cost_model

    @transaction_cost_model.setter
    def transaction_cost_model(self, value: str):
        self._property_changed('transaction_cost_model')
        self.__transaction_cost_model = value        

    @property
    def trading_cost(self) -> float:
        """bps cost to execute delta"""
        return self.__trading_cost

    @trading_cost.setter
    def trading_cost(self, value: float):
        self._property_changed('trading_cost')
        self.__trading_cost = value        

    @property
    def servicing_cost_long(self) -> float:
        """bps cost to fund long positions"""
        return self.__servicing_cost_long

    @servicing_cost_long.setter
    def servicing_cost_long(self, value: float):
        self._property_changed('servicing_cost_long')
        self.__servicing_cost_long = value        

    @property
    def servicing_cost_short(self) -> float:
        """bps cost to fund short positions"""
        return self.__servicing_cost_short

    @servicing_cost_short.setter
    def servicing_cost_short(self, value: float):
        self._property_changed('servicing_cost_short')
        self.__servicing_cost_short = value        

    @property
    def region(self) -> str:
        """The region of the report"""
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def fx_hedged(self) -> bool:
        """Assume portfolio is FX Hedged"""
        return self.__fx_hedged

    @fx_hedged.setter
    def fx_hedged(self, value: bool):
        self._property_changed('fx_hedged')
        self.__fx_hedged = value        

    @property
    def publish_to_bloomberg(self) -> bool:
        """Publish Basket to Bloomberg"""
        return self.__publish_to_bloomberg

    @publish_to_bloomberg.setter
    def publish_to_bloomberg(self, value: bool):
        self._property_changed('publish_to_bloomberg')
        self.__publish_to_bloomberg = value        

    @property
    def publish_to_reuters(self) -> bool:
        """Publish Basket to Reuters"""
        return self.__publish_to_reuters

    @publish_to_reuters.setter
    def publish_to_reuters(self, value: bool):
        self._property_changed('publish_to_reuters')
        self.__publish_to_reuters = value        

    @property
    def publish_to_factset(self) -> bool:
        """Publish Basket to Factset"""
        return self.__publish_to_factset

    @publish_to_factset.setter
    def publish_to_factset(self, value: bool):
        self._property_changed('publish_to_factset')
        self.__publish_to_factset = value        

    @property
    def include_price_history(self) -> bool:
        """Include full price history"""
        return self.__include_price_history

    @include_price_history.setter
    def include_price_history(self, value: bool):
        self._property_changed('include_price_history')
        self.__include_price_history = value        

    @property
    def index_update(self) -> bool:
        """Update the basket"""
        return self.__index_update

    @index_update.setter
    def index_update(self, value: bool):
        self._property_changed('index_update')
        self.__index_update = value        

    @property
    def index_rebalance(self) -> bool:
        """Rebalance the basket"""
        return self.__index_rebalance

    @index_rebalance.setter
    def index_rebalance(self, value: bool):
        self._property_changed('index_rebalance')
        self.__index_rebalance = value        

    @property
    def index_source_id(self) -> str:
        """Marquee Id of the source portfolio, hedge, or parent basket, in case current
           basket composition is sourced from marquee entity"""
        return self.__index_source_id

    @index_source_id.setter
    def index_source_id(self, value: str):
        self._property_changed('index_source_id')
        self.__index_source_id = value        

    @property
    def basket_action(self) -> Union[BasketAction, str]:
        """Indicates which basket action triggered the report"""
        return self.__basket_action

    @basket_action.setter
    def basket_action(self, value: Union[BasketAction, str]):
        self._property_changed('basket_action')
        self.__basket_action = get_enum_value(BasketAction, value)        

    @property
    def api_domain(self) -> bool:
        """Indicates if report is triggered from ui/api call"""
        return self.__api_domain

    @api_domain.setter
    def api_domain(self, value: bool):
        self._property_changed('api_domain')
        self.__api_domain = value        

    @property
    def initial_price(self) -> float:
        """Initial price for the position set"""
        return self.__initial_price

    @initial_price.setter
    def initial_price(self, value: float):
        self._property_changed('initial_price')
        self.__initial_price = value        

    @property
    def stock_level_exposures(self) -> bool:
        """Publish stock level exposures"""
        return self.__stock_level_exposures

    @stock_level_exposures.setter
    def stock_level_exposures(self, value: bool):
        self._property_changed('stock_level_exposures')
        self.__stock_level_exposures = value        

    @property
    def explode_positions(self) -> bool:
        """Whether to explode positions during risk run"""
        return self.__explode_positions

    @explode_positions.setter
    def explode_positions(self, value: bool):
        self._property_changed('explode_positions')
        self.__explode_positions = value        

    @property
    def scenario_id(self) -> str:
        """Marquee unique scenario identifier"""
        return self.__scenario_id

    @scenario_id.setter
    def scenario_id(self, value: str):
        self._property_changed('scenario_id')
        self.__scenario_id = value        

    @property
    def scenario_ids(self) -> Tuple[str, ...]:
        """Array of scenario identifiers related to the object"""
        return self.__scenario_ids

    @scenario_ids.setter
    def scenario_ids(self, value: Tuple[str, ...]):
        self._property_changed('scenario_ids')
        self.__scenario_ids = value        

    @property
    def scenario_group_id(self) -> str:
        """Marquee unique scenario group identifier"""
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: str):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def scenario_type(self) -> Union[ScenarioType, str]:
        """Type of Scenario"""
        return self.__scenario_type

    @scenario_type.setter
    def scenario_type(self, value: Union[ScenarioType, str]):
        self._property_changed('scenario_type')
        self.__scenario_type = get_enum_value(ScenarioType, value)        

    @property
    def market_model_id(self) -> str:
        """Marquee unique market model identifier"""
        return self.__market_model_id

    @market_model_id.setter
    def market_model_id(self, value: str):
        self._property_changed('market_model_id')
        self.__market_model_id = value        

    @property
    def risk_measures(self) -> Tuple[RiskMeasure, ...]:
        """An array of risk measures to get from the risk calculation."""
        return self.__risk_measures

    @risk_measures.setter
    def risk_measures(self, value: Tuple[RiskMeasure, ...]):
        self._property_changed('risk_measures')
        self.__risk_measures = value        

    @property
    def initial_pricing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: datetime.date):
        self._property_changed('initial_pricing_date')
        self.__initial_pricing_date = value        

    @property
    def backcast(self) -> bool:
        """Use backcasted portfolio derived from positions on the end date."""
        return self.__backcast

    @backcast.setter
    def backcast(self, value: bool):
        self._property_changed('backcast')
        self.__backcast = value        

    @property
    def risk_request(self) -> RiskRequest:
        """A request for a risk calculation"""
        return self.__risk_request

    @risk_request.setter
    def risk_request(self, value: RiskRequest):
        self._property_changed('risk_request')
        self.__risk_request = value        

    @property
    def participation_rate(self) -> float:
        """Liquidity analytics participation rate."""
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def approve_rebalance(self) -> bool:
        """An approved basket"""
        return self.__approve_rebalance

    @approve_rebalance.setter
    def approve_rebalance(self, value: bool):
        self._property_changed('approve_rebalance')
        self.__approve_rebalance = value        

    @property
    def auto_approved_rebalance(self) -> bool:
        """Indicates whether the rebalance was auto approved by the system"""
        return self.__auto_approved_rebalance

    @auto_approved_rebalance.setter
    def auto_approved_rebalance(self, value: bool):
        self._property_changed('auto_approved_rebalance')
        self.__auto_approved_rebalance = value        

    @property
    def use_risk_request_batch_mode(self) -> bool:
        """Switch to enable RiskRequest batching"""
        return self.__use_risk_request_batch_mode

    @use_risk_request_batch_mode.setter
    def use_risk_request_batch_mode(self, value: bool):
        self._property_changed('use_risk_request_batch_mode')
        self.__use_risk_request_batch_mode = value        

    @property
    def limited_access_assets(self) -> Tuple[str, ...]:
        """List of constituents in the basket that GS has limited access to"""
        return self.__limited_access_assets

    @limited_access_assets.setter
    def limited_access_assets(self, value: Tuple[str, ...]):
        self._property_changed('limited_access_assets')
        self.__limited_access_assets = value        

    @property
    def corporate_action_restricted_assets(self) -> Tuple[str, ...]:
        """List of constituents in the basket that will not be adjusted for corporate
           actions in the future"""
        return self.__corporate_action_restricted_assets

    @corporate_action_restricted_assets.setter
    def corporate_action_restricted_assets(self, value: Tuple[str, ...]):
        self._property_changed('corporate_action_restricted_assets')
        self.__corporate_action_restricted_assets = value        

    @property
    def backcast_dates(self) -> Tuple[datetime.date, ...]:
        """List of dates user upload to backcast basket"""
        return self.__backcast_dates

    @backcast_dates.setter
    def backcast_dates(self, value: Tuple[datetime.date, ...]):
        self._property_changed('backcast_dates')
        self.__backcast_dates = value        

    @property
    def base_currency(self) -> Union[Currency, str]:
        """Base currency"""
        return self.__base_currency

    @base_currency.setter
    def base_currency(self, value: Union[Currency, str]):
        self._property_changed('base_currency')
        self.__base_currency = get_enum_value(Currency, value)        

    @property
    def local_currency(self) -> Union[Currency, str]:
        """Local currency"""
        return self.__local_currency

    @local_currency.setter
    def local_currency(self, value: Union[Currency, str]):
        self._property_changed('local_currency')
        self.__local_currency = get_enum_value(Currency, value)        

    @property
    def fund_calendar(self) -> str:
        """Holiday Calendar of Fund"""
        return self.__fund_calendar

    @fund_calendar.setter
    def fund_calendar(self, value: str):
        self._property_changed('fund_calendar')
        self.__fund_calendar = value        

    @property
    def calculation_currency(self) -> Union[PCOCurrencyType, str]:
        """Calculation currency type"""
        return self.__calculation_currency

    @calculation_currency.setter
    def calculation_currency(self, value: Union[PCOCurrencyType, str]):
        self._property_changed('calculation_currency')
        self.__calculation_currency = get_enum_value(PCOCurrencyType, value)        

    @property
    def hedge_settlement_interval(self) -> Tuple[PCOParameterValues, ...]:
        """Default tenor of hedging for each currency"""
        return self.__hedge_settlement_interval

    @hedge_settlement_interval.setter
    def hedge_settlement_interval(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('hedge_settlement_interval')
        self.__hedge_settlement_interval = value        

    @property
    def hedge_settlement_day(self) -> Tuple[PCOParameterValues, ...]:
        """Settlement date of each currency"""
        return self.__hedge_settlement_day

    @hedge_settlement_day.setter
    def hedge_settlement_day(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('hedge_settlement_day')
        self.__hedge_settlement_day = value        

    @property
    def roll_horizon(self) -> Tuple[PCOParameterValues, ...]:
        """Number of days to roll before settlement for each currency"""
        return self.__roll_horizon

    @roll_horizon.setter
    def roll_horizon(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('roll_horizon')
        self.__roll_horizon = value        

    @property
    def pnl_currency(self) -> Tuple[PCOParameterValues, ...]:
        """One of Local and Base"""
        return self.__pnl_currency

    @pnl_currency.setter
    def pnl_currency(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('pnl_currency')
        self.__pnl_currency = value        

    @property
    def nav_publication_period(self) -> Tuple[PCOParameterValues, ...]:
        """Days it takes for a subscription or redemption show up in NAV after it happens"""
        return self.__nav_publication_period

    @nav_publication_period.setter
    def nav_publication_period(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('nav_publication_period')
        self.__nav_publication_period = value        

    @property
    def roll_date_zero_threshold(self) -> bool:
        """If true, rebalance this program when rolling"""
        return self.__roll_date_zero_threshold

    @roll_date_zero_threshold.setter
    def roll_date_zero_threshold(self, value: bool):
        self._property_changed('roll_date_zero_threshold')
        self.__roll_date_zero_threshold = value        

    @property
    def unrealised_mark_to_market(self) -> PCOUnrealisedMarkToMarket:
        """History of unrealised mark to market of open trades for each currency"""
        return self.__unrealised_mark_to_market

    @unrealised_mark_to_market.setter
    def unrealised_mark_to_market(self, value: PCOUnrealisedMarkToMarket):
        self._property_changed('unrealised_mark_to_market')
        self.__unrealised_mark_to_market = value        

    @property
    def target_deviation(self) -> Tuple[PCOTargetDeviation, ...]:
        """History of target deviation for each currency"""
        return self.__target_deviation

    @target_deviation.setter
    def target_deviation(self, value: Tuple[PCOTargetDeviation, ...]):
        self._property_changed('target_deviation')
        self.__target_deviation = value        

    @property
    def cash_balances(self) -> Tuple[PCOCashBalance, ...]:
        """Cash flows for each currency"""
        return self.__cash_balances

    @cash_balances.setter
    def cash_balances(self, value: Tuple[PCOCashBalance, ...]):
        self._property_changed('cash_balances')
        self.__cash_balances = value        

    @property
    def exposure(self) -> PCOExposure:
        """Total exposure for portfolio"""
        return self.__exposure

    @exposure.setter
    def exposure(self, value: PCOExposure):
        self._property_changed('exposure')
        self.__exposure = value        

    @property
    def pco_share_class(self) -> PCOShareClass:
        """Data for a PCO share class"""
        return self.__pco_share_class

    @pco_share_class.setter
    def pco_share_class(self, value: PCOShareClass):
        self._property_changed('pco_share_class')
        self.__pco_share_class = value        

    @property
    def settlements(self) -> Tuple[PCOSettlements, ...]:
        """History of settlements for each currency"""
        return self.__settlements

    @settlements.setter
    def settlements(self, value: Tuple[PCOSettlements, ...]):
        self._property_changed('settlements')
        self.__settlements = value        

    @property
    def show_cash(self) -> bool:
        """If cash table is shown in UI"""
        return self.__show_cash

    @show_cash.setter
    def show_cash(self, value: bool):
        self._property_changed('show_cash')
        self.__show_cash = value        

    @property
    def show_exposure(self) -> bool:
        """If exposure table is shown in UI"""
        return self.__show_exposure

    @show_exposure.setter
    def show_exposure(self, value: bool):
        self._property_changed('show_exposure')
        self.__show_exposure = value        

    @property
    def enable_rfq(self) -> bool:
        """If RFQ is enabled for the program"""
        return self.__enable_rfq

    @enable_rfq.setter
    def enable_rfq(self, value: bool):
        self._property_changed('enable_rfq')
        self.__enable_rfq = value        

    @property
    def fixing_descriptions(self) -> Tuple[str, ...]:
        """List of available fixing for this program"""
        return self.__fixing_descriptions

    @fixing_descriptions.setter
    def fixing_descriptions(self, value: Tuple[str, ...]):
        self._property_changed('fixing_descriptions')
        self.__fixing_descriptions = value        

    @property
    def pco_origin(self) -> Union[PCOOrigin, str]:
        """Origin of PCO Report"""
        return self.__pco_origin

    @pco_origin.setter
    def pco_origin(self, value: Union[PCOOrigin, str]):
        self._property_changed('pco_origin')
        self.__pco_origin = get_enum_value(PCOOrigin, value)        

    @property
    def pco_action_type(self) -> Union[PCOActionType, str]:
        """Type of PCO Action"""
        return self.__pco_action_type

    @pco_action_type.setter
    def pco_action_type(self, value: Union[PCOActionType, str]):
        self._property_changed('pco_action_type')
        self.__pco_action_type = get_enum_value(PCOActionType, value)        

    @property
    def version(self) -> str:
        """Version"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self._property_changed('version')
        self.__version = value        

    @property
    def roll_currency(self) -> Tuple[PCOParameterValues, ...]:
        """One of Local and Base"""
        return self.__roll_currency

    @roll_currency.setter
    def roll_currency(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('roll_currency')
        self.__roll_currency = value        


class ReportScheduleRequest(Base):
        
    """Parameters in order to schedule a report"""

    @camel_case_translate
    def __init__(
        self,
        parameters: ReportParameters = None,
        end_date: datetime.date = None,
        start_date: datetime.date = None,
        priority: Union[ReportJobPriority, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.parameters = parameters
        self.end_date = end_date
        self.start_date = start_date
        self.priority = priority
        self.name = name

    @property
    def parameters(self) -> ReportParameters:
        """Parameters specific to the report type"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ReportParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def priority(self) -> Union[ReportJobPriority, str]:
        """Report job priority."""
        return self.__priority

    @priority.setter
    def priority(self, value: Union[ReportJobPriority, str]):
        self._property_changed('priority')
        self.__priority = get_enum_value(ReportJobPriority, value)        
