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
from typing import Mapping, Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, Priceable, Scenario, camel_case_translate, get_enum_value


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
    
    def __repr__(self):
        return self.value


class AssetType(EnumBase, Enum):    
    
    """Asset type differentiates the product categorization or contract type"""

    Access = 'Access'
    AssetSwapFxdFlt = 'AssetSwapFxdFlt'
    AssetSwapFxdFxd = 'AssetSwapFxdFxd'
    Any = 'Any'
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
    Convertible_Bond = 'Convertible Bond'
    Credit_Basket = 'Credit Basket'
    Cross = 'Cross'
    CSL = 'CSL'
    Currency = 'Currency'
    Custom_Basket = 'Custom Basket'
    Cryptocurrency = 'Cryptocurrency'
    Default_Swap = 'Default Swap'
    Economic = 'Economic'
    Endowment = 'Endowment'
    Equity_Basket = 'Equity Basket'
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
    InflationSwap = 'InflationSwap'
    Inter_Commodity_Spread = 'Inter-Commodity Spread'
    InvoiceSpread = 'InvoiceSpread'
    Market_Location = 'Market Location'
    MLF = 'MLF'
    Multi_Asset_Allocation = 'Multi-Asset Allocation'
    MultiCrossBinary = 'MultiCrossBinary'
    MultiCrossBinaryLeg = 'MultiCrossBinaryLeg'
    Mutual_Fund = 'Mutual Fund'
    Note = 'Note'
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
    Swap = 'Swap'
    SwapLeg = 'SwapLeg'
    SwapStrategy = 'SwapStrategy'
    Swaption = 'Swaption'
    Synthetic = 'Synthetic'
    Systematic_Hedging = 'Systematic Hedging'
    VarianceSwap = 'VarianceSwap'
    VolatilitySwap = 'VolatilitySwap'
    WeatherIndex = 'WeatherIndex'
    XccySwap = 'XccySwap'
    XccySwapFixFix = 'XccySwapFixFix'
    XccySwapFixFlt = 'XccySwapFixFlt'
    XccySwapMTM = 'XccySwapMTM'
    
    def __repr__(self):
        return self.value


class AswType(EnumBase, Enum):    
    
    """Asset Swap Type"""

    Par = 'Par'
    Proceeds = 'Proceeds'
    
    def __repr__(self):
        return self.value


class BasketAction(EnumBase, Enum):    
    
    """Indicates what was the action taken on basket - create/edit/rebalance"""

    Create = 'Create'
    Edit = 'Edit'
    Rebalance = 'Rebalance'
    
    def __repr__(self):
        return self.value


class BondStrikeType(EnumBase, Enum):    
    
    """The type of the bond strike - price, yield etc"""

    Price = 'Price'
    Yield = 'Yield'
    
    def __repr__(self):
        return self.value


class BusinessDayConvention(EnumBase, Enum):    
    
    """Business Day Convention"""

    Following = 'Following'
    Modified_Following = 'Modified Following'
    Previous = 'Previous'
    Unadjusted = 'Unadjusted'
    
    def __repr__(self):
        return self.value


class BuySell(EnumBase, Enum):    
    
    """Buy or Sell side of contract"""

    Buy = 'Buy'
    Sell = 'Sell'
    
    def __repr__(self):
        return self.value


class CommodMeanRule(EnumBase, Enum):    
    
    """Commodity mean rule"""

    Do_Not_Remove = 'Do Not Remove'
    Remove_Calculated = 'Remove Calculated'
    Remove_Fixed = 'Remove Fixed'
    
    def __repr__(self):
        return self.value


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


class CreditOptionStrikeType(EnumBase, Enum):    
    
    Spread_Adj = 'Spread Adj'
    Delta = 'Delta'
    
    def __repr__(self):
        return self.value


class CreditOptionType(EnumBase, Enum):    
    
    Payer = 'Payer'
    Receiver = 'Receiver'
    
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


class CurrencyName(EnumBase, Enum):    
    
    """Currency Names"""

    _ = ''
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
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


class Field(EnumBase, Enum):    
    
    """Field to be returned"""

    investmentRate = 'investmentRate'
    startingEmmaLegalEntityId = 'startingEmmaLegalEntityId'
    mdapiClass = 'mdapiClass'
    totalNotionalUSD = 'totalNotionalUSD'
    bidUnadjusted = 'bidUnadjusted'
    navTargetQuantity = 'navTargetQuantity'
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
    arrivalMidRealizedCash = 'arrivalMidRealizedCash'
    sc10 = 'sc10'
    sc05 = 'sc05'
    lastTradingDateRule = 'lastTradingDateRule'
    a = 'a'
    sc04 = 'sc04'
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
    performanceContribution = 'performanceContribution'
    sc09 = 'sc09'
    mktClass = 'mktClass'
    sc08 = 'sc08'
    collateralization = 'collateralization'
    futureMonthU26 = 'futureMonthU26'
    futureMonthU25 = 'futureMonthU25'
    futureMonthU24 = 'futureMonthU24'
    futureMonthU23 = 'futureMonthU23'
    futureMonthU22 = 'futureMonthU22'
    statementId = 'statementId'
    futureMonthU21 = 'futureMonthU21'
    assetParametersSettlementDate = 'assetParametersSettlementDate'
    modifiedDuration = 'modifiedDuration'
    vol180d = 'vol180d'
    shortRatesContribution = 'shortRatesContribution'
    impliedNormalVolatility = 'impliedNormalVolatility'
    solarGeneration = 'solarGeneration'
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
    assetParametersPair = 'assetParametersPair'
    temperatureForecast = 'temperatureForecast'
    primaryAssetClass = 'primaryAssetClass'
    bidHigh = 'bidHigh'
    pnlQtd = 'pnlQtd'
    buy50cents = 'buy50cents'
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
    sourceValueForecast = 'sourceValueForecast'
    leg2Spread = 'leg2Spread'
    shortConvictionLarge = 'shortConvictionLarge'
    leg1FloatingRateIndex = 'leg1FloatingRateIndex'
    ccgName = 'ccgName'
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
    buy3point5bps = 'buy3point5bps'
    gsSustainRegion = 'gsSustainRegion'
    absoluteReturnWtd = 'absoluteReturnWtd'
    deploymentId = 'deploymentId'
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
    javaType = 'javaType'
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
    weightedAverageMid = 'weightedAverageMid'
    clusterRegion = 'clusterRegion'
    valoren = 'valoren'
    indexName = 'indexName'
    averageExecutionPrice = 'averageExecutionPrice'
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
    extMktPoint1 = 'extMktPoint1'
    direction = 'direction'
    extMktPoint2 = 'extMktPoint2'
    subRegionCode = 'subRegionCode'
    assetParametersFixedRate = 'assetParametersFixedRate'
    factorProportionOfRisk = 'factorProportionOfRisk'
    isEstimatedReturn = 'isEstimatedReturn'
    valueForecast = 'valueForecast'
    totalIcu = 'totalIcu'
    positionSourceType = 'positionSourceType'
    previousCloseUnrealizedCash = 'previousCloseUnrealizedCash'
    minimumDenomination = 'minimumDenomination'
    futureValueNotional = 'futureValueNotional'
    participationRate = 'participationRate'
    obfr = 'obfr'
    _220 = '220'
    _221 = '221'
    _222 = '222'
    buy9point5bps = 'buy9point5bps'
    _223 = '223'
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
    arrivalMid = 'arrivalMid'
    assetParametersExchangeCurrency = 'assetParametersExchangeCurrency'
    candidateName = 'candidateName'
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
    proceedsAssetSwapSpread = 'proceedsAssetSwapSpread'
    isADR = 'isADR'
    issueDate = 'issueDate'
    serviceId = 'serviceId'
    yes = 'yes'
    gScore = 'gScore'
    marketValue = 'marketValue'
    entityId = 'entityId'
    notionalCurrency1 = 'notionalCurrency1'
    netDebtToEbitda = 'netDebtToEbitda'
    numUnitsUpper = 'numUnitsUpper'
    notionalCurrency2 = 'notionalCurrency2'
    inLimitParticipationRate = 'inLimitParticipationRate'
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
    daysOpen = 'daysOpen'
    buy110cents = 'buy110cents'
    averageSpreadBps = 'averageSpreadBps'
    buy55cents = 'buy55cents'
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
    optionExpirationFrequency = 'optionExpirationFrequency'
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
    termStatus = 'termStatus'
    windSpeedType = 'windSpeedType'
    strikePrice = 'strikePrice'
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
    fredId = 'fredId'
    twiContribution = 'twiContribution'
    cloudCoverType = 'cloudCoverType'
    delisted = 'delisted'
    regionalFocus = 'regionalFocus'
    volumePrimary = 'volumePrimary'
    assetParametersPayerDesignatedMaturity = 'assetParametersPayerDesignatedMaturity'
    buy30cents = 'buy30cents'
    fundingBidPrice = 'fundingBidPrice'
    series = 'series'
    sell3bps = 'sell3bps'
    settlementPrice = 'settlementPrice'
    quarter = 'quarter'
    sell18bps = 'sell18bps'
    assetParametersFloatingRateOption = 'assetParametersFloatingRateOption'
    TRSAskPrice = 'TRSAskPrice'
    realizedVwapPerformanceBps = 'realizedVwapPerformanceBps'
    voteShare = 'voteShare'
    servicingCostShortPnl = 'servicingCostShortPnl'
    totalConfirmed = 'totalConfirmed'
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
    alpha = 'alpha'
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
    _81 = '81'
    turnoverCompositeAdjusted = 'turnoverCompositeAdjusted'
    comment = 'comment'
    sourceSymbol = 'sourceSymbol'
    _82 = '82'
    _83 = '83'
    _84 = '84'
    askUnadjusted = 'askUnadjusted'
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
    _91 = '91'
    _92 = '92'
    _93 = '93'
    _94 = '94'
    _95 = '95'
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
    onsCode = 'onsCode'
    passiveTouchFillsPercentage = 'passiveTouchFillsPercentage'
    seniority = 'seniority'
    inflationDelta = 'inflationDelta'
    leg1Index = 'leg1Index'
    highUnadjusted = 'highUnadjusted'
    submissionEvent = 'submissionEvent'
    TVProductMnemonic = 'TVProductMnemonic'
    avgTradeRateLabel = 'avgTradeRateLabel'
    lastActivityDate = 'lastActivityDate'
    disseminationTime = 'disseminationTime'
    priceToCash = 'priceToCash'
    buy10cents = 'buy10cents'
    fwdEbookPointSpreadAllInMultAsk = 'fwdEbookPointSpreadAllInMultAsk'
    realizedMarketCapRatio = 'realizedMarketCapRatio'
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
    metricName = 'metricName'
    askGspread = 'askGspread'
    forecastHour = 'forecastHour'
    leg2PaymentType = 'leg2PaymentType'
    calSpreadMisPricing = 'calSpreadMisPricing'
    totalTestedNegative = 'totalTestedNegative'
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
    buy200cents = 'buy200cents'
    vwapUnrealizedBps = 'vwapUnrealizedBps'
    priceToBook = 'priceToBook'
    isin = 'isin'
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
    macaulayDuration = 'macaulayDuration'
    availableInventory = 'availableInventory'
    est1DayCompletePct = 'est1DayCompletePct'
    relativeHitRateYtd = 'relativeHitRateYtd'
    rai = 'rai'
    createdById = 'createdById'
    marketDataType = 'marketDataType'
    realShortRatesContribution = 'realShortRatesContribution'
    metricCategory = 'metricCategory'
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
    targetNotional = 'targetNotional'
    fillLegId = 'fillLegId'
    rationale = 'rationale'
    realizedTwapPerformanceBps = 'realizedTwapPerformanceBps'
    lastUpdatedSince = 'lastUpdatedSince'
    totalTests = 'totalTests'
    equitiesContribution = 'equitiesContribution'
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
    exchange = 'exchange'
    esPolicyScore = 'esPolicyScore'
    rollVolumeStd = 'rollVolumeStd'
    temperatureDailyForecast = 'temperatureDailyForecast'
    relativePayoffQtd = 'relativePayoffQtd'
    onLoanPercentage = 'onLoanPercentage'
    twapRemainingSlices = 'twapRemainingSlices'
    fairVariance = 'fairVariance'
    hitRateWtd = 'hitRateWtd'
    previousCloseRealizedCash = 'previousCloseRealizedCash'
    realizedVolatility = 'realizedVolatility'
    unexecutedQuantity = 'unexecutedQuantity'
    proceedsAssetSwapSpread1m = 'proceedsAssetSwapSpread1m'
    cloneParentId = 'cloneParentId'
    windSpeedHourlyForecast = 'windSpeedHourlyForecast'
    etfFlowRatio = 'etfFlowRatio'
    assetParametersReceiverRateOption = 'assetParametersReceiverRateOption'
    buy60cents = 'buy60cents'
    securitySubTypeId = 'securitySubTypeId'
    TRSNotional = 'TRSNotional'
    denominated = 'denominated'
    message = 'message'
    stsRatesCountry = 'stsRatesCountry'
    sell65cents = 'sell65cents'
    horizon = 'horizon'
    wouldIfGoodLevel = 'wouldIfGoodLevel'
    bufferThresholdRequired = 'bufferThresholdRequired'
    faceValue = 'faceValue'
    rollVolumeHist = 'rollVolumeHist'
    counterPartyStatus = 'counterPartyStatus'
    composite22DayAdv = 'composite22DayAdv'
    percentageFarExecutedQuantity = 'percentageFarExecutedQuantity'
    loanSpreadRequired = 'loanSpreadRequired'
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
    paceOfRollp25 = 'paceOfRollp25'
    dayCloseRealizedUSD = 'dayCloseRealizedUSD'
    pctChange = 'pctChange'
    brightnessType = 'brightnessType'
    futureMonth3M = 'futureMonth3M'
    numberOfRolls = 'numberOfRolls'
    isoCountryCodeNumeric = 'isoCountryCodeNumeric'
    priceType = 'priceType'
    realizedVwapPerformanceUSD = 'realizedVwapPerformanceUSD'
    orderSide = 'orderSide'
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
    riskModel = 'riskModel'
    assetParametersVendor = 'assetParametersVendor'
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
    buy15cents = 'buy15cents'
    unadjustedAsk = 'unadjustedAsk'
    dynamicVolumeForecast = 'dynamicVolumeForecast'
    contributionName = 'contributionName'
    givenPlusPaid = 'givenPlusPaid'
    lastFillPrice = 'lastFillPrice'
    soprOut = 'soprOut'
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
    executedNotionalLocal = 'executedNotionalLocal'
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
    turnoverAdjusted = 'turnoverAdjusted'
    priceSpotTargetValue = 'priceSpotTargetValue'
    marketDataPoint = 'marketDataPoint'
    numOfFunds = 'numOfFunds'
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
    corporateSpreadContribution = 'corporateSpreadContribution'
    relativeHumidityHourlyForecast = 'relativeHumidityHourlyForecast'
    multipleScore = 'multipleScore'
    betaAdjustedExposure = 'betaAdjustedExposure'
    isAnnualized = 'isAnnualized'
    dividendPoints = 'dividendPoints'
    brightness = 'brightness'
    assetParametersReceiverDesignatedMaturity = 'assetParametersReceiverDesignatedMaturity'
    bosInTicksDescription = 'bosInTicksDescription'
    testId = 'testId'
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
    relativeReturnMtd = 'relativeReturnMtd'
    exchangeCalendar = 'exchangeCalendar'
    priceChangeOnDay = 'priceChangeOnDay'
    buy100cents = 'buy100cents'
    forwardPoint = 'forwardPoint'
    fci = 'fci'
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
    leg2TotalNotional = 'leg2TotalNotional'
    assetParametersEffectiveDate = 'assetParametersEffectiveDate'
    annReturn10Year = 'annReturn10Year'
    numAdultIcuBeds = 'numAdultIcuBeds'
    daysToExpiration = 'daysToExpiration'
    continuationEvent = 'continuationEvent'
    leg2CommodityUnderlyerId = 'leg2CommodityUnderlyerId'
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
    amount = 'amount'
    lendingFundAcct = 'lendingFundAcct'
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
    customer = 'customer'
    leg1ResetFrequency = 'leg1ResetFrequency'
    queueClockTimeLabel = 'queueClockTimeLabel'
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
    assetParametersPayerDayCountFraction = 'assetParametersPayerDayCountFraction'
    universeId2 = 'universeId2'
    bidLow = 'bidLow'
    bucketizePrice = 'bucketizePrice'
    fairVarianceVolatility = 'fairVarianceVolatility'
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
    popularity = 'popularity'
    floatingRateOption = 'floatingRateOption'
    hedgeValueType = 'hedgeValueType'
    assetParametersClearingHouse = 'assetParametersClearingHouse'
    disclaimer = 'disclaimer'
    payerFrequency = 'payerFrequency'
    loanFee = 'loanFee'
    deploymentVersion = 'deploymentVersion'
    buy16bps = 'buy16bps'
    tradeDayCount = 'tradeDayCount'
    transactionType = 'transactionType'
    priceToSales = 'priceToSales'
    newIdeasQtd = 'newIdeasQtd'
    subdivisionName = 'subdivisionName'
    adjustedAskPrice = 'adjustedAskPrice'
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
    inflationSwapRate = 'inflationSwapRate'
    activeQueries = 'activeQueries'
    sell45bps = 'sell45bps'
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
    assetParametersSettlement = 'assetParametersSettlement'
    maxTemperature = 'maxTemperature'
    acquirerShareholderMeetingDate = 'acquirerShareholderMeetingDate'
    countIdeasWtd = 'countIdeasWtd'
    arrivalRtNormalized = 'arrivalRtNormalized'
    reportType = 'reportType'
    sourceURL = 'sourceURL'
    estimatedReturn = 'estimatedReturn'
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
    expectedResidualQuantity = 'expectedResidualQuantity'
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
    total = 'total'
    filledNotionalUSD = 'filledNotionalUSD'
    assetId = 'assetId'
    blockTradeElectionIndicator = 'blockTradeElectionIndicator'
    testStatus = 'testStatus'
    mktType = 'mktType'
    lastUpdatedTime = 'lastUpdatedTime'
    yield30Day = 'yield30Day'
    buy28bps = 'buy28bps'
    proportionOfRisk = 'proportionOfRisk'
    futureMonthK23 = 'futureMonthK23'
    futureMonthK22 = 'futureMonthK22'
    futureMonthK21 = 'futureMonthK21'
    primaryEntityId = 'primaryEntityId'
    cross = 'cross'
    ideaStatus = 'ideaStatus'
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
    _170 = '170'
    _171 = '171'
    numPediIcuBeds = 'numPediIcuBeds'
    _172 = '172'
    bidYield = 'bidYield'
    _173 = '173'
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
    windChillHourlyForecast = 'windChillHourlyForecast'
    secName = 'secName'
    impliedVolatilityByRelativeStrike = 'impliedVolatilityByRelativeStrike'
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
    gsid = 'gsid'
    lendingFund = 'lendingFund'
    sensitivity = 'sensitivity'
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
    scenarioGroupId = 'scenarioGroupId'
    averageImpliedVariance = 'averageImpliedVariance'
    avgTradeRateDescription = 'avgTradeRateDescription'
    fraction = 'fraction'
    assetCountShort = 'assetCountShort'
    collateralPercentageRequired = 'collateralPercentageRequired'
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
    encodedStats = 'encodedStats'
    buy5bps = 'buy5bps'
    runTime = 'runTime'
    askSize = 'askSize'
    absoluteReturnMtd = 'absoluteReturnMtd'
    std30DaysUnsubsidizedYield = 'std30DaysUnsubsidizedYield'
    resource = 'resource'
    averageRealizedVolatility = 'averageRealizedVolatility'
    traceAdvBuy = 'traceAdvBuy'
    newConfirmed = 'newConfirmed'
    sell8bps = 'sell8bps'
    bidPrice = 'bidPrice'
    sell8point5bps = 'sell8point5bps'
    targetPriceUnrealizedBps = 'targetPriceUnrealizedBps'
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
    liqDly = 'liqDly'
    contributorRole = 'contributorRole'
    totalFatalities = 'totalFatalities'
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
    positionDate = 'positionDate'
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


class IndexNotTradingReasons(EnumBase, Enum):    
    
    """Reasons the index was not traded"""

    Cost = 'Cost'
    Client_does_not_like_the_construction = 'Client does not like the construction'
    Basket_created_prematurely = 'Basket created prematurely'
    Economics_of_the_basket_changed__client_no_longer_interested_in_trading = 'Economics of the basket changed: client no longer interested in trading'
    GS_booking_OVER_operational_issues = 'GS booking/operational issues'
    _ = ''
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


class MarketDataFrequency(EnumBase, Enum):    
    
    Real_Time = 'Real Time'
    End_Of_Day = 'End Of Day'
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


class OptionExpiryType(EnumBase, Enum):    
    
    _1m = '1m'
    _2m = '2m'
    _3m = '3m'
    _4m = '4m'
    _5m = '5m'
    _6m = '6m'
    
    def __repr__(self):
        return self.value


class OptionSettlementMethod(EnumBase, Enum):    
    
    """How the option is settled (e.g. Cash, Physical)"""

    Cash = 'Cash'
    Physical = 'Physical'
    
    def __repr__(self):
        return self.value


class OptionStrikeType(EnumBase, Enum):    
    
    Relative = 'Relative'
    Delta = 'Delta'
    
    def __repr__(self):
        return self.value


class OptionStyle(EnumBase, Enum):    
    
    """Option Exercise Style"""

    European = 'European'
    American = 'American'
    Bermudan = 'Bermudan'
    
    def __repr__(self):
        return self.value


class OptionType(EnumBase, Enum):    
    
    """Option Type"""

    Call = 'Call'
    Put = 'Put'
    Binary_Call = 'Binary Call'
    Binary_Put = 'Binary Put'
    
    def __repr__(self):
        return self.value


class PCOCurrencyType(EnumBase, Enum):    
    
    """Currency Type Options for PCO"""

    Exposure = 'Exposure'
    Base = 'Base'
    Local = 'Local'
    
    def __repr__(self):
        return self.value


class PayReceive(EnumBase, Enum):    
    
    """Pay or receive fixed"""

    Pay = 'Pay'
    Receive = 'Receive'
    Straddle = 'Straddle'
    
    def __repr__(self):
        return self.value


class Period(EnumBase, Enum):    
    
    """A coding scheme to define a period corresponding to a quantity amount"""

    Month = 'Month'
    Quarter = 'Quarter'
    Hour = 'Hour'
    Day = 'Day'
    BusinessDay = 'BusinessDay'
    
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


class PrincipalExchange(EnumBase, Enum):    
    
    """How principal is exchanged"""

    _None = 'None'
    Both = 'Both'
    First = 'First'
    Last = 'Last'
    
    def __repr__(self):
        return self.value


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


class ReportJobPriority(EnumBase, Enum):    
    
    """Report job priority."""

    High = 'High'
    Normal = 'Normal'
    
    def __repr__(self):
        return self.value


class RiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Annual_ATM_Implied_Volatility = 'Annual ATM Implied Volatility'
    Annual_ATMF_Implied_Volatility = 'Annual ATMF Implied Volatility'
    Annual_Implied_Volatility = 'Annual Implied Volatility'
    AnnuityLocalCcy = 'AnnuityLocalCcy'
    BaseCPI = 'BaseCPI'
    Basis = 'Basis'
    BSPrice = 'BSPrice'
    CRIF_IRCurve = 'CRIF IRCurve'
    Cashflows = 'Cashflows'
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
    Price = 'Price'
    Gamma = 'Gamma'
    GammaLocalCcy = 'GammaLocalCcy'
    InflationDelta = 'InflationDelta'
    Inflation_Compounding_Period = 'Inflation Compounding Period'
    Local_Currency_Accrual_in_Cents = 'Local Currency Accrual in Cents'
    Local_Currency_Annuity = 'Local Currency Annuity'
    Market_Data = 'Market Data'
    Market_Data_Assets = 'Market Data Assets'
    MV = 'MV'
    NonUSDOisDomesticRate = 'NonUSDOisDomesticRate'
    OAS = 'OAS'
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
    
    def __repr__(self):
        return self.value


class RiskMeasureUnit(EnumBase, Enum):    
    
    """The unit of change of underlying in the risk computation."""

    Percent = 'Percent'
    Dollar = 'Dollar'
    BPS = 'BPS'
    
    def __repr__(self):
        return self.value


class ScenarioType(EnumBase, Enum):    
    
    """Type of Scenario"""

    Spot_Vol = 'Spot Vol'
    Greeks = 'Greeks'
    
    def __repr__(self):
        return self.value


class SettlementType(EnumBase, Enum):    
    
    """Settlement Type"""

    Cash = 'Cash'
    Physical = 'Physical'
    
    def __repr__(self):
        return self.value


class StrikeMethodType(EnumBase, Enum):    
    
    Spread = 'Spread'
    Delta = 'Delta'
    Percentage_of_Price = 'Percentage of Price'
    Fixed = 'Fixed'
    
    def __repr__(self):
        return self.value


class SwapClearingHouse(EnumBase, Enum):    
    
    """Swap Clearing House"""

    LCH = 'LCH'
    EUREX = 'EUREX'
    JSCC = 'JSCC'
    CME = 'CME'
    NONE = 'NONE'
    
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


class TradeAs(EnumBase, Enum):    
    
    """Option trade as (i.e. listed, otc, lookalike etc)"""

    Listed = 'Listed'
    Listed_Look_alike_OTC = 'Listed Look alike OTC'
    Flex = 'Flex'
    OTC = 'OTC'
    
    def __repr__(self):
        return self.value


class TradeType(EnumBase, Enum):    
    
    """Direction"""

    Buy = 'Buy'
    Sell = 'Sell'
    
    def __repr__(self):
        return self.value


class UnderlierType(EnumBase, Enum):    
    
    """Type of underlyer"""

    BBID = 'BBID'
    CUSIP = 'CUSIP'
    ISIN = 'ISIN'
    SEDOL = 'SEDOL'
    RIC = 'RIC'
    Ticker = 'Ticker'
    
    def __repr__(self):
        return self.value


class ValuationTime(EnumBase, Enum):    
    
    """The time of valuation, e.g. for an option"""

    MktClose = 'MktClose'
    MktOpen = 'MktOpen'
    SQ = 'SQ'
    
    def __repr__(self):
        return self.value


class VarianceConvention(EnumBase, Enum):    
    
    """Specifies whether the variance is Annualized or Total"""

    Annualized = 'Annualized'
    Total = 'Total'
    
    def __repr__(self):
        return self.value


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


class CompositeScenario(Base):
        
    """A scenario for composing scenarios"""

    @camel_case_translate
    def __init__(
        self,
        scenarios: tuple = None,
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
    def scenarios(self) -> tuple:
        """The scenarios, in order"""
        return self.__scenarios

    @scenarios.setter
    def scenarios(self, value: tuple):
        self._property_changed('scenarios')
        self.__scenarios = value        


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


class Link(Base):
        
    """Hyperlink"""

    @camel_case_translate
    def __init__(
        self,
        title: str = None,
        source: str = None,
        name: str = None
    ):        
        super().__init__()
        self.title = title
        self.source = source
        self.name = name

    @property
    def title(self) -> str:
        """display text"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def source(self) -> str:
        """link"""
        return self.__source

    @source.setter
    def source(self, value: str):
        self._property_changed('source')
        self.__source = value        


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
        pco_number_as_string: str = None,
        net_subscription_redemption: str = None,
        net_subscription_redemption_limits: Tuple[str, ...] = None,
        adjustment_vs_subscription_redemption: str = None,
        adjustment_vs_subscription_redemption_limits: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.pco_number_as_string = pco_number_as_string
        self.net_subscription_redemption = net_subscription_redemption
        self.net_subscription_redemption_limits = net_subscription_redemption_limits
        self.adjustment_vs_subscription_redemption = adjustment_vs_subscription_redemption
        self.adjustment_vs_subscription_redemption_limits = adjustment_vs_subscription_redemption_limits
        self.name = name

    @property
    def pco_number_as_string(self) -> str:
        return self.__pco_number_as_string

    @pco_number_as_string.setter
    def pco_number_as_string(self, value: str):
        self._property_changed('pco_number_as_string')
        self.__pco_number_as_string = value        

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
        price: Union[float, str] = None,
        unit: Union[CommodUnit, str] = None,
        currency: Union[CurrencyName, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.price = price
        self.unit = unit
        self.currency = currency
        self.name = name

    @property
    def price(self) -> Union[float, str]:
        """price"""
        return self.__price

    @price.setter
    def price(self, value: Union[float, str]):
        self._property_changed('price')
        self.__price = value        

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


class GIRDomain(Base):
        
    @camel_case_translate
    def __init__(
        self,
        document_links: Tuple[Link, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.document_links = document_links
        self.name = name

    @property
    def document_links(self) -> Tuple[Link, ...]:
        """Documents related to this asset"""
        return self.__document_links

    @document_links.setter
    def document_links(self, value: Tuple[Link, ...]):
        self._property_changed('document_links')
        self.__document_links = value        


class ISelectNewParameter(Base):
        
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
        module_name: str = None,
        target_strike: float = None,
        strike_method: Union[StrikeMethodType, str] = None,
        option_expiry: Union[OptionExpiryType, str] = None,
        bloomberg_id: str = None,
        stock_id: str = None,
        ric: str = None,
        new_weight: float = None,
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
        self.module_name = module_name
        self.target_strike = target_strike
        self.strike_method = strike_method
        self.option_expiry = option_expiry
        self.bloomberg_id = bloomberg_id
        self.stock_id = stock_id
        self.ric = ric
        self.new_weight = new_weight
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


class RiskMeasure(Base):
        
    """The measure to perform risk on. Each risk measure consists of an asset class, a
       measure type, and a unit."""

    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        measure_type: Union[RiskMeasureType, str] = None,
        unit: Union[RiskMeasureUnit, str] = None,
        value: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.measure_type = measure_type
        self.unit = unit
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
    def value(self) -> Union[float, str]:
        """Value of this measure"""
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


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
        location: Union[PricingLocation, str],
        timestamp: datetime.datetime = None,
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
        auto_roll: bool = None,
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
        self.auto_roll = auto_roll
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
    def auto_roll(self) -> bool:
        """Whether roll orders will be automatically generated for each currency"""
        return self.__auto_roll

    @auto_roll.setter
    def auto_roll(self, value: bool):
        self._property_changed('auto_roll')
        self.__auto_roll = value        


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
        base_market: Union[CloseMarket, LiveMarket, TimestampedMarket],
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
    def base_market(self) -> Union[CloseMarket, LiveMarket, TimestampedMarket]:
        """The base market"""
        return self.__base_market

    @base_market.setter
    def base_market(self, value: Union[CloseMarket, LiveMarket, TimestampedMarket]):
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
        from_market: Union[CloseMarket, LiveMarket, TimestampedMarket, OverlayMarket],
        to_market: Union[CloseMarket, LiveMarket, TimestampedMarket, OverlayMarket],
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
    def from_market(self) -> Union[CloseMarket, LiveMarket, TimestampedMarket, OverlayMarket]:
        """The base market"""
        return self.__from_market

    @from_market.setter
    def from_market(self, value: Union[CloseMarket, LiveMarket, TimestampedMarket, OverlayMarket]):
        self._property_changed('from_market')
        self.__from_market = value        

    @property
    def to_market(self) -> Union[CloseMarket, LiveMarket, TimestampedMarket, OverlayMarket]:
        """The target market"""
        return self.__to_market

    @to_market.setter
    def to_market(self, value: Union[CloseMarket, LiveMarket, TimestampedMarket, OverlayMarket]):
        self._property_changed('to_market')
        self.__to_market = value        


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
        return self.__request_visible_to_gs

    @request_visible_to_gs.setter
    def request_visible_to_gs(self, value: bool):
        self._property_changed('request_visible_to_gs')
        self.__request_visible_to_gs = value        


class ReportParameters(Base):
        
    """Parameters specific to the report type"""

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
        settlements: Tuple[PCOSettlements, ...] = None,
        show_cash: bool = None,
        show_exposure: bool = None,
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
        self.settlements = settlements
        self.show_cash = show_cash
        self.show_exposure = show_exposure
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
