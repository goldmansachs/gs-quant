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
import deprecation
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from enum import Enum


class AccrualConvention(EnumBase, Enum):    
    
    Adjusted = 'Adjusted'
    Unadjusted = 'Unadjusted'    


class AccumOrDecum(EnumBase, Enum):    
    
    Accum = 'Accum'
    Decum = 'Decum'
    Non_Standard = 'Non-Standard'    


class AccumulatorType(EnumBase, Enum):    
    
    Terminating = 'Terminating'
    Non_Terminating = 'Non-Terminating'    


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
    Digital_Asset = 'Digital Asset'
    Econ = 'Econ'
    Equity = 'Equity'
    Fund = 'Fund'
    FX = 'FX'
    Mortgage = 'Mortgage'
    Rates = 'Rates'
    Repo = 'Repo'
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
    Accumulator = 'Accumulator'
    AccumulatorScheduleLeg = 'AccumulatorScheduleLeg'
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
    Bond_Forward = 'Bond Forward'
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
    Coin = 'Coin'
    Commodity = 'Commodity'
    CommodityReferencePrice = 'CommodityReferencePrice'
    CommodVarianceSwap = 'CommodVarianceSwap'
    CommodityPowerNode = 'CommodityPowerNode'
    CommodityPowerAggregatedNodes = 'CommodityPowerAggregatedNodes'
    CommodityEUNaturalGasHub = 'CommodityEUNaturalGasHub'
    CommodityNaturalGasHub = 'CommodityNaturalGasHub'
    Company = 'Company'
    Convertible = 'Convertible'
    CorrelationSwap = 'CorrelationSwap'
    CorrelationSwapLeg = 'CorrelationSwapLeg'
    Credit_Basket = 'Credit Basket'
    Cross = 'Cross'
    CSL = 'CSL'
    Currency = 'Currency'
    Custom_Basket = 'Custom Basket'
    Cryptocurrency = 'Cryptocurrency'
    Default_Swap = 'Default Swap'
    DiscreteLock = 'DiscreteLock'
    DoubleKnockout = 'DoubleKnockout'
    DoubleTouch = 'DoubleTouch'
    DualDoubleKnockout = 'DualDoubleKnockout'
    DualDoubleKnockoutLeg = 'DualDoubleKnockoutLeg'
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
    MacroBasket = 'MacroBasket'
    Market_Location = 'Market Location'
    MLF = 'MLF'
    Multi_Asset_Allocation = 'Multi-Asset Allocation'
    MultiCrossBinary = 'MultiCrossBinary'
    MultiCrossBinaryLeg = 'MultiCrossBinaryLeg'
    MultiCrossDoubleBinary = 'MultiCrossDoubleBinary'
    MultiCrossDoubleBinaryLeg = 'MultiCrossDoubleBinaryLeg'
    MultiCrossDoubleTouch = 'MultiCrossDoubleTouch'
    MultiCrossDoubleTouchLeg = 'MultiCrossDoubleTouchLeg'
    Mutual_Fund = 'Mutual Fund'
    Native_Asset = 'Native Asset'
    Note = 'Note'
    OneTouch = 'OneTouch'
    Option = 'Option'
    OptionLeg = 'OptionLeg'
    OptionPeriod = 'OptionPeriod'
    OptionStrategy = 'OptionStrategy'
    Peer_Group = 'Peer Group'
    Pension_Fund = 'Pension Fund'
    Pivot = 'Pivot'
    PivotScheduleLeg = 'PivotScheduleLeg'
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
    Tarf = 'Tarf'
    TarfScheduleLeg = 'TarfScheduleLeg'
    Token = 'Token'
    VarianceSwap = 'VarianceSwap'
    VolatilitySwap = 'VolatilitySwap'
    VolVarSwap = 'VolVarSwap'
    WeatherIndex = 'WeatherIndex'
    WorstOf = 'WorstOf'
    WorstOfLeg = 'WorstOfLeg'
    WorstOfKO = 'WorstOfKO'
    WorstOfKOLeg = 'WorstOfKOLeg'
    XccySwap = 'XccySwap'
    XccySwapFixFix = 'XccySwapFixFix'
    XccySwapFixFlt = 'XccySwapFixFlt'
    XccySwapMTM = 'XccySwapMTM'
    SyntheticOETTerms = 'SyntheticOETTerms'
    SyntheticSchedule = 'SyntheticSchedule'
    SyntheticLeg = 'SyntheticLeg'    


class AswType(EnumBase, Enum):    
    
    """Asset Swap Type"""

    Par = 'Par'
    Proceeds = 'Proceeds'    


class BasketAction(EnumBase, Enum):    
    
    """Indicates what was the action taken on basket - create/edit/rebalance"""

    Create = 'Create'
    Edit = 'Edit'
    Rebalance = 'Rebalance'    


class BasketValuationSource(EnumBase, Enum):    
    
    """The source of basket pricing"""

    GS = 'GS'
    BVAL = 'BVAL'
    CBBT = 'CBBT'    


class BestWorst(EnumBase, Enum):    
    
    Best = 'Best'
    Worst = 'Worst'    


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


class CDOptionType(EnumBase, Enum):    
    
    """Credit Option Type"""

    Call = 'Call'
    Put = 'Put'
    Straddle = 'Straddle'
    Payer = 'Payer'
    Receiver = 'Receiver'
    Digital_Call = 'Digital Call'
    Digital_Put = 'Digital Put'    


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
    SIL = 'SIL'
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
    currentConstituentsNetDebtToEbitda = 'currentConstituentsNetDebtToEbitda'
    sunshineDailyForecast = 'sunshineDailyForecast'
    sentimentScore = 'sentimentScore'
    customerBuySell = 'customerBuySell'
    assetParametersUnderlierType = 'assetParametersUnderlierType'
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
    currentConstituentsDividendYield = 'currentConstituentsDividendYield'
    assetParametersPutAmount = 'assetParametersPutAmount'
    assetParametersUnderlier = 'assetParametersUnderlier'
    performanceContribution = 'performanceContribution'
    nextRebalanceDate = 'nextRebalanceDate'
    sc09 = 'sc09'
    assetClassificationsDigitalAssetClass = 'assetClassificationsDigitalAssetClass'
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
    averageExposure = 'averageExposure'
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
    assetParametersTradeAs = 'assetParametersTradeAs'
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
    assetParametersNumberOfOptions = 'assetParametersNumberOfOptions'
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
    exchangeCurrency = 'exchangeCurrency'
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
    factorZScore = 'factorZScore'
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
    currentConstituentsPriceToSales = 'currentConstituentsPriceToSales'
    otherPriceTerm = 'otherPriceTerm'
    bidGspread = 'bidGspread'
    tradedMktFwdPointsMid = 'tradedMktFwdPointsMid'
    openPrice = 'openPrice'
    rfqState = 'rfqState'
    psId = 'psId'
    hitRateMtd = 'hitRateMtd'
    _250 = '250'
    _251 = '251'
    _252 = '252'
    _253 = '253'
    fairVolatility = 'fairVolatility'
    _254 = '254'
    dollarCross = 'dollarCross'
    _255 = '255'
    portfolioType = 'portfolioType'
    _256 = '256'
    optionExpirationRule = 'optionExpirationRule'
    _257 = '257'
    _258 = '258'
    _259 = '259'
    currency = 'currency'
    clusterClass = 'clusterClass'
    sell50bps = 'sell50bps'
    futureMonthM21 = 'futureMonthM21'
    bidSize = 'bidSize'
    coordinateId = 'coordinateId'
    arrivalMid = 'arrivalMid'
    _260 = '260'
    _261 = '261'
    _262 = '262'
    marginalContributionToRiskPercent = 'marginalContributionToRiskPercent'
    _263 = '263'
    _264 = '264'
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
    assetParametersIdentifier = 'assetParametersIdentifier'
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
    currentConstituentsEarningsPerShare = 'currentConstituentsEarningsPerShare'
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
    currentConstituentsPriceToEarningsPositive = 'currentConstituentsPriceToEarningsPositive'
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
    currentConstituentsPriceToBook = 'currentConstituentsPriceToBook'
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
    assetParametersTotalQuantity = 'assetParametersTotalQuantity'
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
    fairValueGapStandardDeviation = 'fairValueGapStandardDeviation'
    tcmCostParticipationRate100Pct = 'tcmCostParticipationRate100Pct'
    relativeUniverse = 'relativeUniverse'
    measureIdx = 'measureIdx'
    executedQuantity = 'executedQuantity'
    fredId = 'fredId'
    twiContribution = 'twiContribution'
    cloudCoverType = 'cloudCoverType'
    delisted = 'delisted'
    currentConstituentsPriceToCash = 'currentConstituentsPriceToCash'
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
    currentConstituentsEarningsPerSharePositive = 'currentConstituentsEarningsPerSharePositive'
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
    fixOrderRoutingRegion = 'fixOrderRoutingRegion'
    futureMonthV22 = 'futureMonthV22'
    futureMonthV21 = 'futureMonthV21'
    expiration = 'expiration'
    leg2ResetFrequency = 'leg2ResetFrequency'
    controversyScore = 'controversyScore'
    proceedAssetSwapSpread = 'proceedAssetSwapSpread'
    concentrationLevel = 'concentrationLevel'
    weightOfFaceValue = 'weightOfFaceValue'
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
    lastRebalanceApprovalId = 'lastRebalanceApprovalId'
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
    chargeInEntityCurrency = 'chargeInEntityCurrency'
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
    assetParametersMultiplier = 'assetParametersMultiplier'
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
    transitionPlanTransparencyPercentage = 'transitionPlanTransparencyPercentage'
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
    assetParametersLastFixingDate = 'assetParametersLastFixingDate'
    _54 = '54'
    fundamentalMetric = 'fundamentalMetric'
    _55 = '55'
    _56 = '56'
    quoteStatusId = 'quoteStatusId'
    assetParametersMethodOfSettlement = 'assetParametersMethodOfSettlement'
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
    assetParametersForwardPrice = 'assetParametersForwardPrice'
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
    strategyAum = 'strategyAum'
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
    currentConstituentsSalesPerShare = 'currentConstituentsSalesPerShare'
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
    assetClassificationsDigitalAssetSector = 'assetClassificationsDigitalAssetSector'
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
    emissionsIntensityEnterpriseValue = 'emissionsIntensityEnterpriseValue'
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
    emissionsIntensityRevenue = 'emissionsIntensityRevenue'
    askGspread = 'askGspread'
    forecastHour = 'forecastHour'
    leg2PaymentType = 'leg2PaymentType'
    calSpreadMisPricing = 'calSpreadMisPricing'
    totalTestedNegative = 'totalTestedNegative'
    impliedRetailNotional = 'impliedRetailNotional'
    rate366 = 'rate366'
    currentConstituentsReturnOnEquity = 'currentConstituentsReturnOnEquity'
    platform = 'platform'
    rate365 = 'rate365'
    fixedRateFrequency = 'fixedRateFrequency'
    rate360 = 'rate360'
    medianDailyVolume22d = 'medianDailyVolume22d'
    globalPredictedBeta = 'globalPredictedBeta'
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
    currentConstituentsPriceToEarnings = 'currentConstituentsPriceToEarnings'
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
    assetClassificationsUnderliersAssetClass = 'assetClassificationsUnderliersAssetClass'
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
    estimationUniverseWeight = 'estimationUniverseWeight'
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
    coinMetricsId = 'coinMetricsId'
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
    assetClassificationsVendor = 'assetClassificationsVendor'
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
    updateSeconds = 'updateSeconds'
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
    assetClassificationsDigitalAssetMarket = 'assetClassificationsDigitalAssetMarket'
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
    predictedBeta = 'predictedBeta'
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
    factorStandardDeviation = 'factorStandardDeviation'
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
    assetParametersNumberOfShares = 'assetParametersNumberOfShares'
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
    transitionPerformancePercentage = 'transitionPerformancePercentage'
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
    latestEndDate = 'latestEndDate'
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
    assetClassificationsDigitalAssetIndustry = 'assetClassificationsDigitalAssetIndustry'
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
    aggregatePnl = 'aggregatePnl'
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
    chargeInLocalCurrency = 'chargeInLocalCurrency'
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
    dailyReturn = 'dailyReturn'
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
    rSquared = 'rSquared'
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
    lastRebalanceDate = 'lastRebalanceDate'
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
    fairValueGapPercent = 'fairValueGapPercent'
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
    assetClassificationsDigitalAssetSubsector = 'assetClassificationsDigitalAssetSubsector'
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
    tradeDate = 'tradeDate'
    buy12bps = 'buy12bps'
    clearingHouse = 'clearingHouse'
    dayCloseUnrealizedBps = 'dayCloseUnrealizedBps'
    stsRatesMaturity = 'stsRatesMaturity'
    stsIncludeSstkAnalytics = 'stsIncludeSstkAnalytics'
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


class IndexCalculationType(EnumBase, Enum):    
    
    """Quote type that is used for the bond price"""

    Price_Return = 'Price Return'    


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
    Brazil = 'Brazil'
    INR = 'INR'
    Korea = 'Korea'
    Malaysia = 'Malaysia'
    Philippines = 'Philippines'
    Taipei = 'Taipei'    


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
    Currency_Buckets = 'Currency Buckets'
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


class LongShort(EnumBase, Enum):    
    
    """Client long or short on tarf"""

    Long = 'Long'
    Short = 'Short'    


class MarketDataFrequency(EnumBase, Enum):    
    
    Real_Time = 'Real Time'
    End_Of_Day = 'End Of Day'    


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
    Wolfe_Research = 'Wolfe Research'
    Qontigo = 'Qontigo'
    Quant_Insight = 'Quant Insight'
    FactSet_via_AWS_Data_Exchange = 'FactSet via AWS Data Exchange'
    Rearc = 'Rearc'
    FactSet = 'FactSet'
    WorldScope = 'WorldScope'
    GS_Muni = 'GS Muni'
    BlackRock = 'BlackRock'    


class NewOrUnwind(EnumBase, Enum):    
    
    """New or unwnd of product"""

    New = 'New'
    Unwind = 'Unwind'
    Non_Standard = 'Non-Standard'    


class NotionalOrStrike(EnumBase, Enum):    
    
    """Notional or Strke on target adjustment"""

    Notional = 'Notional'
    Strike = 'Strike'    


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
    ElectDfltCash = 'ElectDfltCash'
    ElectDfltPhys = 'ElectDfltPhys'
    NetShares = 'NetShares'    


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
    Digital_Call = 'Digital Call'
    Digital_Put = 'Digital Put'    


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


class PositionSetWeightingStrategy(EnumBase, Enum):    
    
    """Strategy used to price the position set."""

    Equal = 'Equal'
    Market_Capitalization = 'Market Capitalization'
    Quantity = 'Quantity'
    Weight = 'Weight'
    Notional = 'Notional'    


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


class QuoteType(EnumBase, Enum):    
    
    """Quote type that is used for the bond price"""

    Dirty_Price = 'Dirty Price'
    Clean_Price = 'Clean Price'
    BM_Spread = 'BM Spread'
    Yield = 'Yield'
    Z_Spread = 'Z-Spread'
    G_Spread = 'G-Spread'    


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
    BSPricePct = 'BSPricePct'
    CRIF_IRCurve = 'CRIF IRCurve'
    Cashflows = 'Cashflows'
    Compounded_Fixed_Rate = 'Compounded Fixed Rate'
    Correlation = 'Correlation'
    Cross_Multiplier = 'Cross Multiplier'
    Cross = 'Cross'
    Daily_Implied_Volatility = 'Daily Implied Volatility'
    Delta = 'Delta'
    DeltaLocalCcy = 'DeltaLocalCcy'
    Description = 'Description'
    Dollar_Price = 'Dollar Price'
    DV01 = 'DV01'
    FairPremium = 'FairPremium'
    FairPremiumPct = 'FairPremiumPct'
    Fair_Price = 'Fair Price'
    FairVarStrike = 'FairVarStrike'
    FairVolStrike = 'FairVolStrike'
    FinalCPI = 'FinalCPI'
    Forward_Price = 'Forward Price'
    Forward_Rate = 'Forward Rate'
    Forward_Spread = 'Forward Spread'
    FX_Calculated_Delta = 'FX Calculated Delta'
    FX_Calculated_Delta_No_Premium_Adjustment = 'FX Calculated Delta No Premium Adjustment'
    FX_Discount_Factor_Over = 'FX Discount Factor Over'
    FX_Discount_Factor_Under = 'FX Discount Factor Under'
    FX_Hedge_Delta = 'FX Hedge Delta'
    FX_Premium = 'FX Premium'
    FX_Premium_Pct = 'FX Premium Pct'
    FX_Premium_Pct_Flat_Fwd = 'FX Premium Pct Flat Fwd'
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
    Market = 'Market'
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
    RFRFXRate = 'RFRFXRate'
    RFRFXSpreadRate = 'RFRFXSpreadRate'
    RFRFXSpreadRateExcludingSpikes = 'RFRFXSpreadRateExcludingSpikes'
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


class RiskModelType(EnumBase, Enum):    
    
    """Marquee risk model type"""

    Factor = 'Factor'
    Macro = 'Macro'
    Thematic = 'Thematic'    


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


class TargetPaymentType(EnumBase, Enum):    
    
    Capped = 'Capped'
    Full = 'Full'
    _None = 'None'    


class TargetType(EnumBase, Enum):    
    
    """Target type for accural redemption forward"""

    Big_Figures = 'Big Figures'
    Amount = 'Amount'
    Num_Of_ITM_Fixes = 'Num Of ITM Fixes'    


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


class WeightingType(EnumBase, Enum):    
    
    """Weighting type that is used for the bond price"""

    Notional = 'Notional'
    Market_Value = 'Market Value'
    Dollar_Duration = 'Dollar Duration'    


@dataclass
class BaseMarket(Base):
    pass


@dataclass
class SingleMarket(Base):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetIdPriceable(Priceable):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerCreditStandardAndPoorsRatingOptions(Base):
    min_: Optional[str] = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    max_: Optional[str] = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerRequestFilterDateLimits(Base):
    min_: Optional[datetime.date] = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    max_: Optional[datetime.date] = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetScreenerRequestFilterLimits(Base):
    min_: Optional[float] = field(default=None, metadata=config(field_name='min', exclude=exclude_none))
    max_: Optional[float] = field(default=None, metadata=config(field_name='max', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLDate(Base):
    date_value: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLDouble(Base):
    double_value: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLFXCross(Base):
    string_value: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLIndex(Base):
    string_value: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLSimpleSchedule(Base):
    fixing_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    settlement_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLStock(Base):
    string_value: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLString(Base):
    string_value: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLSymCaseNamedParam(Base):
    sym_case_value: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False, order=True)
class CurrencyParameter(RiskMeasureParameter):
    value: Optional[str] = field(default=None, metadata=field_metadata)
    parameter_type: Optional[str] = field(init=False, default='Currency', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CurveOverlay(Scenario):
    dates: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    discount_factors: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    denominated: Optional[str] = field(default=None, metadata=field_metadata)
    csa_term: Optional[str] = field(default=None, metadata=field_metadata)
    tenor: Optional[str] = field(default=None, metadata=field_metadata)
    rate_option: Optional[str] = field(default=None, metadata=field_metadata)
    curve_type: Optional[str] = field(default=None, metadata=field_metadata)
    subtract_base: Optional[bool] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='CurveOverlay', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class DataRow(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DateRange(Base):
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectNewUnit(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    new_units: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectNewWeight(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    new_weight: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Identifier(Base):
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    value: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiborFallbackScenario(Scenario):
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    fallback_type: Optional[str] = field(default='RFR', metadata=field_metadata)
    discounting: Optional[bool] = field(default=False, metadata=field_metadata)
    cash_flows: Optional[bool] = field(default=True, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='LiborFallbackScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityReportParameters(Base):
    title: Optional[str] = field(default=None, metadata=field_metadata)
    email: Optional[str] = field(default=None, metadata=field_metadata)
    trading_desk: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False, order=True)
class ListOfNumberParameter(RiskMeasureParameter):
    values: Optional[Tuple[float, ...]] = field(default=None, metadata=field_metadata)
    parameter_type: Optional[str] = field(init=False, default='ListOfNumber', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False, order=True)
class ListOfStringParameter(RiskMeasureParameter):
    values: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    parameter_type: Optional[str] = field(init=False, default='ListOfString', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False, order=True)
class MapParameter(RiskMeasureParameter):
    value: Optional[DictBase] = field(default=None, metadata=field_metadata)
    parameter_type: Optional[str] = field(init=False, default='Map', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataCoordinate(Base):
    mkt_type: Optional[str] = field(default=None, metadata=field_metadata)
    mkt_asset: Optional[str] = field(default=None, metadata=field_metadata)
    mkt_class: Optional[str] = field(default=None, metadata=field_metadata)
    mkt_point: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    mkt_quoting_style: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataVolSlice(Base):
    date: datetime.date = field(default=None, metadata=field_metadata)
    strikes: Tuple[float, ...] = field(default=None, metadata=field_metadata)
    levels: Tuple[float, ...] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MktMarkingOptions(Base):
    mode: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Op(Base):
    gte: Optional[Union[datetime.date, float]] = field(default=None, metadata=field_metadata)
    lte: Optional[Union[datetime.date, float]] = field(default=None, metadata=field_metadata)
    lt: Optional[Union[datetime.date, float]] = field(default=None, metadata=field_metadata)
    gt: Optional[Union[datetime.date, float]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OrderByBody(Base):
    column_name: str = field(default=None, metadata=field_metadata)
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOBenchmarkOptions(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    target_ratio: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOExposureAdjustments(Base):
    nav_adjustment: Optional[str] = field(default=None, metadata=field_metadata)
    net_subscription_redemption: Optional[str] = field(default=None, metadata=field_metadata)
    net_subscription_redemption_limits: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    adjustment_vs_subscription_redemption: Optional[str] = field(default=None, metadata=field_metadata)
    adjustment_vs_subscription_redemption_limits: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOMtMHistoricalData(Base):
    value: Optional[str] = field(default=None, metadata=field_metadata)
    timestamp: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCONetSubscription(Base):
    confirmed: Optional[str] = field(default=None, metadata=field_metadata)
    estimated: Optional[str] = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOSettlementsData(Base):
    timestamp: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    settlement: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOTargetDeviationData(Base):
    value: Optional[str] = field(default=None, metadata=field_metadata)
    timestamp: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PatternPropertiesDateTime(Base):
    start: Optional[str] = field(default=None, metadata=field_metadata)
    end: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceStats(Base):
    alpha: Optional[float] = field(default=None, metadata=field_metadata)
    annualized_return: Optional[float] = field(default=None, metadata=field_metadata)
    annualized_volatility: Optional[float] = field(default=None, metadata=field_metadata)
    average_return: Optional[float] = field(default=None, metadata=field_metadata)
    average_value: Optional[float] = field(default=None, metadata=field_metadata)
    average_volume_last_month: Optional[float] = field(default=None, metadata=field_metadata)
    best_month: Optional[float] = field(default=None, metadata=field_metadata)
    best_month_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    beta: Optional[float] = field(default=None, metadata=field_metadata)
    close_price: Optional[float] = field(default=None, metadata=field_metadata)
    correlation: Optional[float] = field(default=None, metadata=field_metadata)
    cumulative_return: Optional[float] = field(default=None, metadata=field_metadata)
    current_value: Optional[float] = field(default=None, metadata=field_metadata)
    drawdown_over_return: Optional[float] = field(default=None, metadata=field_metadata)
    high: Optional[float] = field(default=None, metadata=field_metadata)
    high_eod: Optional[float] = field(default=None, metadata=field_metadata)
    last_change: Optional[float] = field(default=None, metadata=field_metadata)
    last_change_pct: Optional[float] = field(default=None, metadata=field_metadata)
    last_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    last_value: Optional[float] = field(default=None, metadata=field_metadata)
    low: Optional[float] = field(default=None, metadata=field_metadata)
    low_eod: Optional[float] = field(default=None, metadata=field_metadata)
    max_draw_down: Optional[float] = field(default=None, metadata=field_metadata)
    max_draw_down_duration: Optional[int] = field(default=None, metadata=field_metadata)
    open_price: Optional[float] = field(default=None, metadata=field_metadata)
    positive_months: Optional[float] = field(default=None, metadata=field_metadata)
    sharpe_ratio: Optional[float] = field(default=None, metadata=field_metadata)
    sortino_ratio: Optional[float] = field(default=None, metadata=field_metadata)
    worst_month: Optional[float] = field(default=None, metadata=field_metadata)
    worst_month_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    total_return: Optional[float] = field(default=None, metadata=field_metadata)
    volume: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionPriceInput(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    weight: Optional[float] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionTag(Base):
    name: str = field(default=None, metadata=field_metadata)
    value: str = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RefMarket(BaseMarket):
    market_ref: Optional[str] = field(default=None, metadata=field_metadata)
    market_type: Optional[str] = field(init=False, default='RefMarket', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportSubscriptionParameters(Base):
    frequency: object = field(default=None, metadata=field_metadata)
    recipients: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    pfr_report_id: str = field(default=None, metadata=field_metadata)
    day_of_week: Optional[float] = field(default=None, metadata=field_metadata)
    day_of_month: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskRequestParameters(Base):
    csa_term: Optional[str] = field(default=None, metadata=field_metadata)
    raw_results: Optional[bool] = field(default=False, metadata=field_metadata)
    use_historical_diddles_only: Optional[bool] = field(default=False, metadata=field_metadata)
    market_behaviour: Optional[str] = field(default='ContraintsBased', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SimpleParty(Base):
    party_type: Optional[str] = field(default=None, metadata=field_metadata)
    party_name: Optional[str] = field(default=None, metadata=field_metadata)
    party_book: Optional[str] = field(default=None, metadata=field_metadata)
    party_oe_id: Optional[str] = field(default=None, metadata=config(field_name='partyOEId', exclude=exclude_none))
    party_oe_name: Optional[str] = field(default=None, metadata=config(field_name='partyOEName', exclude=exclude_none))
    party_root_oe_id: Optional[str] = field(default=None, metadata=config(field_name='partyRootOEId', exclude=exclude_none))
    party_root_oe_name: Optional[str] = field(default=None, metadata=config(field_name='partyRootOEName', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False, order=True)
class StringParameter(RiskMeasureParameter):
    value: Optional[str] = field(default=None, metadata=field_metadata)
    parameter_type: Optional[str] = field(init=False, default='String', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TimeFilter(Base):
    start_hours: str = field(default=None, metadata=field_metadata)
    end_hours: str = field(default=None, metadata=field_metadata)
    time_zone: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UserCoverage(Base):
    name: str = field(default=None, metadata=field_metadata)
    email: str = field(default=None, metadata=field_metadata)
    app: Optional[str] = field(default=None, metadata=field_metadata)
    phone: Optional[str] = field(default=None, metadata=field_metadata)
    guid: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class UserTag(Base):
    name: str = field(default=None, metadata=field_metadata)
    added_on: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    added_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    removed: Optional[bool] = field(default=None, metadata=field_metadata)
    removed_on: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    removed_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    removal_reason: Optional[str] = field(default=None, metadata=field_metadata)
    category: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WeightedPosition(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    weight: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class XRef(Base):
    ric: Optional[str] = field(default=None, metadata=field_metadata)
    rcic: Optional[str] = field(default=None, metadata=field_metadata)
    eid: Optional[str] = field(default=None, metadata=field_metadata)
    gsideid: Optional[str] = field(default=None, metadata=field_metadata)
    gsid: Optional[str] = field(default=None, metadata=field_metadata)
    gsid_equivalent: Optional[str] = field(default=None, metadata=field_metadata)
    cid: Optional[str] = field(default=None, metadata=field_metadata)
    bbid: Optional[str] = field(default=None, metadata=field_metadata)
    bcid: Optional[str] = field(default=None, metadata=field_metadata)
    delisted: Optional[str] = field(default=None, metadata=field_metadata)
    bbid_equivalent: Optional[str] = field(default=None, metadata=field_metadata)
    cusip: Optional[str] = field(default=None, metadata=field_metadata)
    gss: Optional[str] = field(default=None, metadata=field_metadata)
    isin: Optional[str] = field(default=None, metadata=field_metadata)
    jsn: Optional[str] = field(default=None, metadata=field_metadata)
    prime_id: Optional[str] = field(default=None, metadata=field_metadata)
    sedol: Optional[str] = field(default=None, metadata=field_metadata)
    ticker: Optional[str] = field(default=None, metadata=field_metadata)
    valoren: Optional[str] = field(default=None, metadata=field_metadata)
    wpk: Optional[str] = field(default=None, metadata=field_metadata)
    gsn: Optional[str] = field(default=None, metadata=field_metadata)
    sec_name: Optional[str] = field(default=None, metadata=field_metadata)
    cross: Optional[str] = field(default=None, metadata=field_metadata)
    simon_id: Optional[str] = field(default=None, metadata=field_metadata)
    em_id: Optional[str] = field(default=None, metadata=field_metadata)
    cm_id: Optional[str] = field(default=None, metadata=field_metadata)
    lms_id: Optional[str] = field(default=None, metadata=field_metadata)
    tdapi: Optional[str] = field(default=None, metadata=field_metadata)
    mdapi: Optional[str] = field(default=None, metadata=field_metadata)
    mdapi_class: Optional[str] = field(default=None, metadata=field_metadata)
    mic: Optional[str] = field(default=None, metadata=field_metadata)
    sf_id: Optional[str] = field(default=None, metadata=field_metadata)
    dollar_cross: Optional[str] = field(default=None, metadata=field_metadata)
    mq_symbol: Optional[str] = field(default=None, metadata=field_metadata)
    primary_country_ric: Optional[str] = field(default=None, metadata=field_metadata)
    pnode_id: Optional[str] = field(default=None, metadata=field_metadata)
    wi_id: Optional[str] = field(default=None, metadata=field_metadata)
    ps_id: Optional[str] = field(default=None, metadata=field_metadata)
    pl_id: Optional[str] = field(default=None, metadata=field_metadata)
    exchange_code: Optional[str] = field(default=None, metadata=field_metadata)
    plot_id: Optional[str] = field(default=None, metadata=field_metadata)
    cins: Optional[str] = field(default=None, metadata=field_metadata)
    bbgid: Optional[str] = field(default=None, metadata=field_metadata)
    display_id: Optional[str] = field(default=None, metadata=field_metadata)
    tsdb_shortname: Optional[str] = field(default=None, metadata=field_metadata)
    coin_metrics_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetClassifications(Base):
    risk_country_name: Optional[str] = field(default=None, metadata=field_metadata)
    risk_country_code: Optional[str] = field(default=None, metadata=field_metadata)
    country_name: Optional[str] = field(default=None, metadata=field_metadata)
    country_code: Optional[str] = field(default=None, metadata=field_metadata)
    listing_country_name: Optional[str] = field(default=None, metadata=field_metadata)
    is_primary: Optional[bool] = field(default=None, metadata=field_metadata)
    is_country_primary: Optional[bool] = field(default=None, metadata=field_metadata)
    gics_sector: Optional[str] = field(default=None, metadata=field_metadata)
    gics_industry_group: Optional[str] = field(default=None, metadata=field_metadata)
    gics_industry: Optional[str] = field(default=None, metadata=field_metadata)
    gics_sub_industry: Optional[str] = field(default=None, metadata=field_metadata)
    naics_classification_code: Optional[str] = field(default=None, metadata=field_metadata)
    naics_industry_description: Optional[str] = field(default=None, metadata=field_metadata)
    bbg_industry_sector: Optional[str] = field(default=None, metadata=field_metadata)
    bbg_industry_group: Optional[str] = field(default=None, metadata=field_metadata)
    bbg_industry_sub_group: Optional[str] = field(default=None, metadata=field_metadata)
    rating_moodys: Optional[str] = field(default=None, metadata=field_metadata)
    rating_fitch: Optional[str] = field(default=None, metadata=field_metadata)
    rating_standard_and_poors: Optional[str] = field(default=None, metadata=field_metadata)
    rating_second_highest: Optional[str] = field(default=None, metadata=field_metadata)
    rating_linear: Optional[float] = field(default=None, metadata=field_metadata)
    commod_template: Optional[str] = field(default=None, metadata=field_metadata)
    security_subtype: Optional[str] = field(default=None, metadata=field_metadata)
    region: Optional[Region] = field(default=None, metadata=field_metadata)
    vendor: Optional[str] = field(default=None, metadata=field_metadata)
    underliers_asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    digital_asset_market: Optional[str] = field(default=None, metadata=field_metadata)
    digital_asset_sector: Optional[str] = field(default=None, metadata=field_metadata)
    digital_asset_industry: Optional[str] = field(default=None, metadata=field_metadata)
    digital_asset_class: Optional[str] = field(default=None, metadata=field_metadata)
    digital_asset_subsector: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetParameters(Base):
    basket_type: Optional[str] = field(default=None, metadata=field_metadata)
    style: Optional[str] = field(default=None, metadata=field_metadata)
    index_calculation_type: Optional[str] = field(default=None, metadata=field_metadata)
    index_return_type: Optional[str] = field(default=None, metadata=field_metadata)
    index_divisor: Optional[float] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    quote_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    index_initial_price: Optional[float] = field(default=None, metadata=field_metadata)
    initial_pricing_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    expiration_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    expiration_location: Optional[str] = field(default=None, metadata=field_metadata)
    number_of_shares: Optional[float] = field(default=None, metadata=field_metadata)
    option_style: Optional[str] = field(default=None, metadata=field_metadata)
    option_type: Optional[OptionType] = field(default=None, metadata=field_metadata)
    settlement_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    settlement_type: Optional[str] = field(default=None, metadata=field_metadata)
    strike_price: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    put_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    put_amount: Optional[float] = field(default=None, metadata=field_metadata)
    automatic_exercise: Optional[bool] = field(default=None, metadata=field_metadata)
    call_amount: Optional[float] = field(default=None, metadata=field_metadata)
    call_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    exercise_time: Optional[str] = field(default=None, metadata=field_metadata)
    multiplier: Optional[float] = field(default=None, metadata=field_metadata)
    premium_payment_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    premium: Optional[float] = field(default=None, metadata=field_metadata)
    premium_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    callable_: Optional[bool] = field(default=None, metadata=config(field_name='callable', exclude=exclude_none))
    puttable: Optional[bool] = field(default=None, metadata=field_metadata)
    perpetual: Optional[bool] = field(default=None, metadata=field_metadata)
    seniority: Optional[str] = field(default=None, metadata=field_metadata)
    coupon_type: Optional[str] = field(default=None, metadata=field_metadata)
    index: Optional[str] = field(default=None, metadata=field_metadata)
    index_term: Optional[str] = field(default=None, metadata=field_metadata)
    index_margin: Optional[float] = field(default=None, metadata=field_metadata)
    coupon: Optional[float] = field(default=None, metadata=field_metadata)
    issue_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    issuer: Optional[str] = field(default=None, metadata=field_metadata)
    issuer_country_code: Optional[str] = field(default=None, metadata=field_metadata)
    issuer_type: Optional[str] = field(default=None, metadata=field_metadata)
    issue_size: Optional[float] = field(default=None, metadata=field_metadata)
    commodity_sector: Optional[CommoditySector] = field(default=None, metadata=field_metadata)
    pricing_location: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    contract_months: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    g10_currency: Optional[bool] = field(default=None, metadata=field_metadata)
    portfolio_id: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_id: Optional[str] = field(default=None, metadata=field_metadata)
    ultimate_ticker: Optional[str] = field(default=None, metadata=field_metadata)
    strategy: Optional[Strategy] = field(default=None, metadata=field_metadata)
    exchange_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    region: Optional[str] = field(default=None, metadata=field_metadata)
    delivery_point: Optional[str] = field(default=None, metadata=field_metadata)
    pricing_index: Optional[str] = field(default=None, metadata=field_metadata)
    common_code: Optional[str] = field(default=None, metadata=field_metadata)
    issuer_id: Optional[str] = field(default=None, metadata=field_metadata)
    contract_month: Optional[str] = field(default=None, metadata=field_metadata)
    bloomberg_collateral_classification: Optional[str] = field(default=None, metadata=field_metadata)
    load_type: Optional[str] = field(default=None, metadata=field_metadata)
    contract_unit: Optional[str] = field(default=None, metadata=field_metadata)
    index_approval_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    is_pair_basket: Optional[bool] = field(default=None, metadata=field_metadata)
    is_legacy_pair_basket: Optional[bool] = field(default=None, metadata=field_metadata)
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = field(default=None, metadata=field_metadata)
    floating_rate_day_count_fraction: Optional[DayCountFraction] = field(default=None, metadata=field_metadata)
    forward_price: Optional[float] = field(default=None, metadata=field_metadata)
    pair_calculation: Optional[str] = field(default=None, metadata=field_metadata)
    pay_day_count_fraction: Optional[DayCountFraction] = field(default=None, metadata=field_metadata)
    receive_day_count_fraction: Optional[DayCountFraction] = field(default=None, metadata=field_metadata)
    pay_frequency: Optional[str] = field(default=None, metadata=field_metadata)
    receive_frequency: Optional[str] = field(default=None, metadata=field_metadata)
    resettable_leg: Optional[PayReceive] = field(default=None, metadata=field_metadata)
    inflation_lag: Optional[str] = field(default=None, metadata=field_metadata)
    fx_index: Optional[str] = field(default=None, metadata=field_metadata)
    index_notes: Optional[str] = field(default=None, metadata=field_metadata)
    index_not_trading_reasons: Optional[IndexNotTradingReasons] = field(default=None, metadata=field_metadata)
    trade_as: Optional[str] = field(default=None, metadata=field_metadata)
    clone_parent_id: Optional[str] = field(default=None, metadata=field_metadata)
    on_behalf_of: Optional[str] = field(default=None, metadata=field_metadata)
    index_calculation_agent: Optional[str] = field(default=None, metadata=field_metadata)
    product_type: Optional[ProductType] = field(default=None, metadata=field_metadata)
    vendor: Optional[str] = field(default=None, metadata=field_metadata)
    call_first_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    call_last_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    amount_outstanding: Optional[float] = field(default=None, metadata=field_metadata)
    covered_bond: Optional[bool] = field(default=None, metadata=field_metadata)
    issue_status: Optional[str] = field(default=None, metadata=field_metadata)
    issue_status_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    issue_price: Optional[float] = field(default=None, metadata=field_metadata)
    sinkable: Optional[bool] = field(default=None, metadata=field_metadata)
    sink_factor: Optional[float] = field(default=None, metadata=field_metadata)
    accrued_interest_standard: Optional[float] = field(default=None, metadata=field_metadata)
    redemption_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    redemption_price: Optional[float] = field(default=None, metadata=field_metadata)
    redemption_amount: Optional[float] = field(default=None, metadata=field_metadata)
    redemption_percent: Optional[float] = field(default=None, metadata=field_metadata)
    private_placement_type: Optional[str] = field(default=None, metadata=field_metadata)
    minimum_piece: Optional[float] = field(default=None, metadata=field_metadata)
    minimum_increment: Optional[float] = field(default=None, metadata=field_metadata)
    next_coupon_payment: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    minimum_denomination: Optional[float] = field(default=None, metadata=field_metadata)
    default_backcast: Optional[bool] = field(default=None, metadata=field_metadata)
    index_precision: Optional[float] = field(default=None, metadata=field_metadata)
    official_side: Optional[Side] = field(default=None, metadata=field_metadata)
    valuation_source: Optional[BasketValuationSource] = field(default=None, metadata=field_metadata)
    close_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    credit_index_series: Optional[str] = field(default=None, metadata=field_metadata)
    reference_entity: Optional[str] = field(default=None, metadata=field_metadata)
    restructuring_type: Optional[str] = field(default=None, metadata=field_metadata)
    underlying_type: Optional[str] = field(default=None, metadata=field_metadata)
    underlier: Optional[str] = field(default=None, metadata=field_metadata)
    next_rebalance_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    last_rebalance_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    last_rebalance_approval_id: Optional[str] = field(default=None, metadata=field_metadata)
    target_notional: Optional[float] = field(default=None, metadata=field_metadata)
    attribution_dataset_id: Optional[str] = field(init=False, default='STSATTR', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLCurrency(Base):
    string_value: Optional[Currency] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLDateArray(Base):
    date_values: Optional[Tuple[CSLDate, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLDateArrayNamedParam(Base):
    date_values: Optional[Tuple[CSLDate, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLDoubleArray(Base):
    double_values: Optional[Tuple[CSLDouble, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLFXCrossArray(Base):
    fx_cross_values: Optional[Tuple[CSLFXCross, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLIndexArray(Base):
    index_values: Optional[Tuple[CSLIndex, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLSimpleScheduleArray(Base):
    simple_schedule_values: Optional[Tuple[CSLSimpleSchedule, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLStockArray(Base):
    stock_values: Optional[Tuple[CSLStock, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLStringArray(Base):
    string_values: Optional[Tuple[CSLString, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CarryScenario(Scenario):
    date: Optional[Union[datetime.date, str]] = field(default=None, metadata=field_metadata)
    time_shift: Optional[int] = field(default=None, metadata=field_metadata)
    roll_to_fwds: Optional[bool] = field(default=True, metadata=field_metadata)
    holiday_calendar: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='CarryScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CloseMarket(BaseMarket):
    date: datetime.date = field(default=None, metadata=field_metadata)
    location: PricingLocation = field(default=None, metadata=field_metadata)
    market_type: Optional[str] = field(init=False, default='CloseMarket', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodPrice(Base):
    unit: Optional[CommodUnit] = field(default=None, metadata=field_metadata)
    price: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    currency: Optional[CurrencyName] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntitlementExclusions(Base):
    view: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    edit: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    admin: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    rebalance: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    execute: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    trade: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    upload: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    query: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    performance_details: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    plot: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
    delete: Optional[Tuple[Tuple[str, ...], ...]] = field(default=None, metadata=field_metadata)
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


class FieldValueMap(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FilterRequest(Base):
    scroll: Optional[str] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    include_columns: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    filters: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    order_by: Optional[OrderByBody] = field(default=None, metadata=field_metadata)
    limit: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FilteredData(Base):
    total_results: Optional[float] = field(default=None, metadata=field_metadata)
    results: Optional[Tuple[DataRow, ...]] = field(default=None, metadata=field_metadata)
    scroll: Optional[str] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False, order=True)
class FiniteDifferenceParameter(RiskMeasureParameter):
    aggregation_level: Optional[AggregationLevel] = field(default=None, metadata=field_metadata)
    currency: Optional[str] = field(default=None, metadata=field_metadata)
    local_curve: Optional[bool] = field(default=None, metadata=field_metadata)
    bump_size: Optional[float] = field(default=None, metadata=field_metadata)
    finite_difference_method: Optional[FiniteDifferenceMethod] = field(default=None, metadata=field_metadata)
    scale_factor: Optional[float] = field(default=None, metadata=field_metadata)
    mkt_marking_options: Optional[MktMarkingOptions] = field(default=None, metadata=field_metadata)
    parameter_type: Optional[str] = field(init=False, default='FiniteDifference', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ISelectNewParameter(Base):
    early_unwind_after: Optional[float] = field(default=None, metadata=field_metadata)
    early_unwind_applicable: Optional[str] = field(default=None, metadata=field_metadata)
    expiry_date_rule: Optional[str] = field(default=None, metadata=field_metadata)
    option_target_expiry_parameter: Optional[float] = field(default=None, metadata=field_metadata)
    option_early_unwind_days: Optional[float] = field(default=None, metadata=field_metadata)
    in_alpha: Optional[bool] = field(default=None, metadata=field_metadata)
    is_fsr_target_factor: Optional[bool] = field(default=None, metadata=config(field_name='isFSRTargetFactor', exclude=exclude_none))
    fsr_max_ratio: Optional[float] = field(default=None, metadata=field_metadata)
    fsr_min_ratio: Optional[float] = field(default=None, metadata=field_metadata)
    module_enabled: Optional[bool] = field(default=None, metadata=field_metadata)
    trend_signal_0: Optional[bool] = field(default=None, metadata=config(field_name='trendSignal_0', exclude=exclude_none))
    trend_signal_1: Optional[bool] = field(default=None, metadata=config(field_name='trendSignal_1', exclude=exclude_none))
    trend_signal_2: Optional[bool] = field(default=None, metadata=config(field_name='trendSignal_2', exclude=exclude_none))
    trend_signal_3: Optional[bool] = field(default=None, metadata=config(field_name='trendSignal_3', exclude=exclude_none))
    module_name: Optional[str] = field(default=None, metadata=field_metadata)
    target_strike: Optional[float] = field(default=None, metadata=field_metadata)
    strike_method: Optional[StrikeMethodType] = field(default=None, metadata=field_metadata)
    option_expiry: Optional[OptionExpiryType] = field(default=None, metadata=field_metadata)
    bloomberg_id: Optional[str] = field(default=None, metadata=field_metadata)
    stock_id: Optional[str] = field(default=None, metadata=field_metadata)
    asset_class: Optional[str] = field(default=None, metadata=field_metadata)
    future_id: Optional[str] = field(default=None, metadata=field_metadata)
    ric: Optional[str] = field(default=None, metadata=field_metadata)
    new_weight: Optional[float] = field(default=None, metadata=field_metadata)
    execution_participation_rate: Optional[float] = field(default=None, metadata=field_metadata)
    new_shares: Optional[float] = field(default=None, metadata=field_metadata)
    new_lots: Optional[float] = field(default=None, metadata=field_metadata)
    execution_start_time: Optional[DictBase] = field(default=None, metadata=field_metadata)
    execution_end_time: Optional[DictBase] = field(default=None, metadata=field_metadata)
    execution_style: Optional[str] = field(default=None, metadata=field_metadata)
    execution_timezone: Optional[str] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    leverage: Optional[float] = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    hedge_ratio: Optional[float] = field(default=None, metadata=field_metadata)
    option_type: Optional[OptionType] = field(default=None, metadata=field_metadata)
    option_strike_type: Optional[OptionStrikeType] = field(default=None, metadata=field_metadata)
    credit_option_type: Optional[CreditOptionType] = field(default=None, metadata=field_metadata)
    credit_option_strike_type: Optional[CreditOptionStrikeType] = field(default=None, metadata=field_metadata)
    strike_relative: Optional[float] = field(default=None, metadata=field_metadata)
    trade_type: Optional[TradeType] = field(default=None, metadata=field_metadata)
    signal: Optional[float] = field(default=None, metadata=field_metadata)
    new_signal: Optional[float] = field(default=None, metadata=field_metadata)
    new_min_weight: Optional[float] = field(default=None, metadata=field_metadata)
    new_max_weight: Optional[float] = field(default=None, metadata=field_metadata)
    min_weight: Optional[float] = field(default=None, metadata=field_metadata)
    max_weight: Optional[float] = field(default=None, metadata=field_metadata)
    weight_smoothing_window: Optional[float] = field(default=None, metadata=field_metadata)
    election: Optional[str] = field(default=None, metadata=field_metadata)
    base_date: Optional[str] = field(default=None, metadata=field_metadata)
    commodity: Optional[str] = field(default=None, metadata=field_metadata)
    component_weight: Optional[float] = field(default=None, metadata=field_metadata)
    contract_nearby_number: Optional[float] = field(default=None, metadata=field_metadata)
    expiration_schedule: Optional[str] = field(default=None, metadata=field_metadata)
    fixing_type: Optional[str] = field(default=None, metadata=field_metadata)
    last_eligible_date: Optional[float] = field(default=None, metadata=field_metadata)
    num_roll_days: Optional[float] = field(default=None, metadata=field_metadata)
    roll_end: Optional[float] = field(default=None, metadata=field_metadata)
    roll_start: Optional[float] = field(default=None, metadata=field_metadata)
    roll_type: Optional[str] = field(default=None, metadata=field_metadata)
    valid_contract_expiry: Optional[str] = field(default=None, metadata=field_metadata)
    rtl: Optional[float] = field(default=None, metadata=field_metadata)
    current_weight: Optional[float] = field(default=None, metadata=field_metadata)
    country: Optional[str] = field(default=None, metadata=field_metadata)
    region: Optional[str] = field(default=None, metadata=field_metadata)
    adv: Optional[float] = field(default=None, metadata=field_metadata)
    tadv: Optional[float] = field(default=None, metadata=field_metadata)
    hadv: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiveMarket(BaseMarket):
    location: PricingLocation = field(default=None, metadata=field_metadata)
    market_type: Optional[str] = field(init=False, default='LiveMarket', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataCoordinateValue(Base):
    coordinate: MarketDataCoordinate = field(default=None, metadata=field_metadata)
    value: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataPattern(Base):
    mkt_type: Optional[str] = field(default=None, metadata=field_metadata)
    mkt_asset: Optional[str] = field(default=None, metadata=field_metadata)
    mkt_class: Optional[str] = field(default=None, metadata=field_metadata)
    mkt_point: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    mkt_quoting_style: Optional[str] = field(default=None, metadata=field_metadata)
    is_active: Optional[bool] = field(default=None, metadata=field_metadata)
    is_investment_grade: Optional[bool] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    country_code: Optional[CountryCode] = field(default=None, metadata=field_metadata)
    gics_sector: Optional[str] = field(default=None, metadata=field_metadata)
    gics_industry_group: Optional[str] = field(default=None, metadata=field_metadata)
    gics_industry: Optional[str] = field(default=None, metadata=field_metadata)
    gics_sub_industry: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataShock(Base):
    shock_type: MarketDataShockType = field(default=None, metadata=field_metadata)
    value: float = field(default=None, metadata=field_metadata)
    precision: Optional[float] = field(default=None, metadata=field_metadata)
    cap: Optional[float] = field(default=None, metadata=field_metadata)
    floor: Optional[float] = field(default=None, metadata=field_metadata)
    coordinate_cap: Optional[float] = field(default=None, metadata=field_metadata)
    coordinate_floor: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOBenchmark(Base):
    selected: Optional[str] = field(default=None, metadata=field_metadata)
    options: Optional[Tuple[PCOBenchmarkOptions, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOCashBalance(Base):
    local_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    cash_balance_limits: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    cash_reserve: Optional[str] = field(default=None, metadata=field_metadata)
    long_threshold: Optional[str] = field(default=None, metadata=field_metadata)
    short_threshold: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOParameterValues(Base):
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOSettlements(Base):
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[PCOSettlementsData, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOShareClass(Base):
    total_net_assets: Optional[str] = field(default=None, metadata=field_metadata)
    estimated_switch: Optional[str] = field(default=None, metadata=field_metadata)
    estimated_net_subscription_effective_date: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    confirmed_net_subscription_effective_date: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    estimated_net_dividend: Optional[str] = field(default=None, metadata=field_metadata)
    confirmed_net_dividend: Optional[str] = field(default=None, metadata=field_metadata)
    net_subscriptions: Optional[Tuple[PCONetSubscription, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOTargetDeviation(Base):
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[PCOTargetDeviationData, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOUnrealisedMarkToMarket(Base):
    total: Optional[str] = field(default=None, metadata=field_metadata)
    next_settlement_date: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    next_settlement: Optional[str] = field(default=None, metadata=field_metadata)
    next_roll_date: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    historical_data: Optional[Tuple[PCOMtMHistoricalData, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PerformanceStatsRequest(Base):
    annualized_return: Optional[Op] = field(default=None, metadata=field_metadata)
    annualized_volatility: Optional[Op] = field(default=None, metadata=field_metadata)
    best_month: Optional[Op] = field(default=None, metadata=field_metadata)
    max_draw_down: Optional[Op] = field(default=None, metadata=field_metadata)
    max_draw_down_duration: Optional[Op] = field(default=None, metadata=field_metadata)
    positive_months: Optional[Op] = field(default=None, metadata=field_metadata)
    sharpe_ratio: Optional[Op] = field(default=None, metadata=field_metadata)
    sortino_ratio: Optional[Op] = field(default=None, metadata=field_metadata)
    worst_month: Optional[Op] = field(default=None, metadata=field_metadata)
    average_return: Optional[Op] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RollFwd(Scenario):
    date: Optional[Union[datetime.date, str]] = field(default=None, metadata=field_metadata)
    realise_fwd: Optional[bool] = field(default=True, metadata=field_metadata)
    holiday_calendar: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='RollFwd', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TimestampedMarket(BaseMarket):
    timestamp: datetime.datetime = field(default=None, metadata=field_metadata)
    location: PricingLocation = field(default=None, metadata=field_metadata)
    base_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    market_type: Optional[str] = field(init=False, default='TimestampedMarket', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetStatsRequest(Base):
    last_updated_time: Optional[DateRange] = field(default=None, metadata=field_metadata)
    period: Optional[AssetStatsPeriod] = field(default=None, metadata=field_metadata)
    type_: Optional[AssetStatsType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    stats: Optional[PerformanceStatsRequest] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLCurrencyArray(Base):
    currency_values: Optional[Tuple[CSLCurrency, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLSchedule(Base):
    first_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    last_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    calendar_name: Optional[str] = field(default=None, metadata=field_metadata)
    period: Optional[str] = field(default=None, metadata=field_metadata)
    delay: Optional[str] = field(default=None, metadata=field_metadata)
    business_day_convention: Optional[str] = field(default=None, metadata=field_metadata)
    day_count_convention: Optional[str] = field(default=None, metadata=field_metadata)
    days_per_term: Optional[str] = field(default=None, metadata=field_metadata)
    delay_business_day_convention: Optional[str] = field(default=None, metadata=field_metadata)
    delay_calendar_name: Optional[str] = field(default=None, metadata=field_metadata)
    has_reset_date: Optional[bool] = field(default=None, metadata=field_metadata)
    term_formula: Optional[str] = field(default=None, metadata=field_metadata)
    extra_dates: Optional[Tuple[CSLDateArrayNamedParam, ...]] = field(default=None, metadata=field_metadata)
    extra_dates_by_offset: Optional[Tuple[CSLSymCaseNamedParam, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CurveScenario(Scenario):
    market_data_pattern: Optional[MarketDataPattern] = field(default=None, metadata=field_metadata)
    parallel_shift: Optional[float] = field(default=None, metadata=field_metadata)
    curve_shift: Optional[float] = field(default=None, metadata=field_metadata)
    pivot_point: Optional[float] = field(default=None, metadata=field_metadata)
    tenor_start: Optional[float] = field(default=None, metadata=field_metadata)
    tenor_end: Optional[float] = field(default=None, metadata=field_metadata)
    shock_type: Optional[MarketDataShockType] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='CurveScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class FieldFilterMap(DictBase):
    _PROPERTIES = {'internal_index_calc_region', 'issue_status_date', 'pl_id', 'last_returns_start_date', 'amount_outstanding', 'asset_classifications_gics_sub_industry', 'mdapi_class', 'data_set_ids', 'call_first_date', 'pb_client_id', 'asset_parameters_start', 'owner_id', 'economic_terms_hash', 'sec_db', 'objective', 'simon_intl_asset_tags', 'private_placement_type', 'hedge_notional', 'rank', 'data_set_category', 'pair_calculation', 'asset_parameters_index_family', 'created_by_id', 'vehicle_type', 'market_data_type', 'asset_parameters_payer_day_count_fraction', 'point_class', 'asset_parameters_underlier_type', 'asset_parameters_cap_floor', 'minimum_increment', 'asset_parameters_payer_currency', 'settlement_date', 'hedge_volatility', 'version', 'tags', 'asset_classifications_gics_industry_group', 'market_data_asset', 'asset_classifications_is_primary', 'styles', 'asset_parameters_total_quantity', 'short_name', 'asset_classifications_underliers_asset_class', 'calculation_region', 'eid', 'jsn', 'mkt_quoting_style', 'hurdle_type', 'mic', 'ps_id', 'issue_status', 'region_code', 'dollar_cross', 'portfolio_type', 'vendor', 'popularity', 'currency', 'term', 'real_time_restriction_status', 'asset_parameters_clearing_house', 'rating_fitch', 'non_symbol_dimensions', 'asset_parameters_option_style', 'share_class_type', 'asset_parameters_put_amount', 'asset_parameters_underlier', 'next_rebalance_date', 'asset_parameters_floating_rate_designated_maturity', 'target_notional', 'asset_parameters_tenor', 'mkt_class', 'delisted', 'asset_classifications_digital_asset_class', 'last_updated_since', 'regional_focus', 'asset_parameters_payer_designated_maturity', 'tsdb_shortname', 'seasonal_adjustment_short', 'asset_parameters_exchange_currency', 'asset_classifications_country_name', 'management_fee', 'asset_parameters_settlement_date', 'rating_moodys', 'simon_id', 'development_status', 'cusip', 'notes', 'tags_to_exclude', 'asset_parameters_floating_rate_option', 'internal_index_calc_agent', 'last_rebalance_date', 'rating_second_highest', 'asset_classifications_country_code', 'frequency', 'option_type', 'data_set_sub_category', 'is_live', 'is_legacy_pair_basket', 'issuer_type', 'asset_parameters_pricing_location', 'plot_id', 'asset_parameters_coupon', 'asset_parameters_identifier', 'asset_parameters_last_fixing_date', 'data_product', 'mq_symbol', 'asset_parameters_method_of_settlement', 'sectors', 'redemption_notice_period', 'multiplier', 'asset_parameters_payer_rate_option', 'market_data_point', 'external', 'wpk', 'sts_fx_currency', 'hedge_annualized_volatility', 'fix_order_routing_region', 'name', 'asset_parameters_expiration_date', 'aum', 'exchange', 'folder_name', 'region', 'cid', 'onboarded', 'live_date', 'issue_price', 'sink_factor', 'underlying_data_set_id', 'asset_parameters_notional_amount_in_other_currency', 'asset_parameters_payer_frequency', 'prime_id', 'asset_classifications_gics_sector', 'asset_parameters_pair', 'sts_asset_name', 'description', 'asset_classifications_is_country_primary', 'title', 'net_exposure_classification', 'asset_parameters_strike_price', 'coupon_type', 'last_updated_by_id', 'asset_parameters_forward_price', 'clone_parent_id', 'company', 'gate_type', 'issue_date', 'expiration_date', 'coverage', 'ticker', 'asset_parameters_receiver_rate_option', 'coin_metrics_id', 'call_last_date', 'asset_parameters_payer_spread', 'sts_rates_country', 'asset_parameters_premium_payment_date', 'latest_execution_time', 'asset_parameters_forward_rate', 'asset_parameters_receiver_designated_maturity', 'asset_classifications_digital_asset_industry', 'gate', 'multi_tags', 'gsn', 'gss', 'rating_linear', 'asset_class', 'asset_parameters_index', 'cm_id', 'asset_classifications_vendor', 'type', 'gsideid', 'mdapi', 'ric', 'issuer', 'position_source_id', 'measures', 'asset_parameters_floating_rate_day_count_fraction', 'asset_parameters_notional_amount', 'strategy_aum', 'action', 'id', 'asset_parameters_call_amount', 'asset_parameters_seniority', 'redemption_date', 'identifier', 'index_create_source', 'sec_name', 'sub_region', 'asset_parameters_receiver_day_count_fraction', 'asset_parameters_index2_tenor', 'asset_parameters_notional_currency', 'sedol', 'mkt_asset', 'rating_standard_and_poors', 'asset_types', 'bcid', 'asset_parameters_credit_index_series', 'gsid', 'tdapi', 'asset_classifications_digital_asset_subsector', 'last_updated_message', 'rcic', 'trading_restriction', 'name_raw', 'status', 'asset_parameters_pay_or_receive', 'client_name', 'asset_parameters_index_series', 'asset_classifications_gics_industry', 'on_behalf_of', 'increment', 'accrued_interest_standard', 'enabled', 'sts_commodity', 'sectors_raw', 'sts_commodity_sector', 'asset_parameters_receiver_frequency', 'position_source_name', 'gsid_equivalent', 'categories', 'symbol_dimensions', 'ext_mkt_asset', 'asset_parameters_fixed_rate_frequency', 'coupon', 'side_pocket', 'compliance_restricted_status', 'quoting_style', 'is_entity', 'scenario_group_id', 'asset_parameters_trade_as', 'redemption_period', 'asset_parameters_issuer_type', 'sts_credit_market', 'bbid', 'asset_classifications_risk_country_code', 'asset_parameters_receiver_currency', 'sts_em_dm', 'asset_classifications_digital_asset_sector', 'issue_size', 'returns_enabled', 'seniority', 'asset_parameters_settlement', 'asset_parameters_expiration_time', 'primary_country_ric', 'is_pair_basket', 'asset_parameters_index_version', 'asset_parameters_commodity_reference_price', 'asset_classifications_digital_asset_market', 'default_backcast', 'asset_parameters_number_of_shares', 'use_machine_learning', 'performance_fee', 'report_type', 'lockup_type', 'lockup', 'underlying_asset_ids', 'asset_parameters_fee_currency', 'encoded_stats', 'pnode_id', 'backtest_type', 'asset_parameters_issuer', 'exchange_code', 'asset_parameters_strike', 'oe_id', 'asset_parameters_termination_date', 'resource', 'asset_parameters_receiver_spread', 'bbid_equivalent', 'hurdle', 'asset_parameters_effective_date', 'valoren', 'asset_parameters_number_of_options', 'asset_parameters_fixed_rate_day_count_fraction', 'auto_tags', 'short_description', 'ext_mkt_class', 'mkt_point1', 'portfolio_managers', 'asset_parameters_commodity_sector', 'hedge_tracking_error', 'asset_parameters_put_currency', 'asset_parameters_coupon_type', 'supra_strategy', 'term_status', 'wi_id', 'market_cap_category', 'asset_parameters_call_currency', 'mkt_point3', 'display_id', 'mkt_point2', 'strike_price', 'mkt_point4', 'risk_packages', 'units', 'em_id', 'sts_credit_region', 'country_id', 'ext_mkt_point3', 'asset_classifications_risk_country_name', 'asset_parameters_vendor', 'asset_parameters_index1_tenor', 'mkt_type', 'is_public', 'alias', 'ext_mkt_point1', 'product_type', 'ext_mkt_point2', 'sub_region_code', 'asset_parameters_option_type', 'asset_parameters_fixed_rate', 'last_returns_end_date', 'tsdb_synced_symbol', 'position_source_type', 'asset_parameters_multiplier', 'minimum_denomination', 'flagship', 'lms_id', 'cross', 'in_code', 'asset_parameters_strike_price_relative', 'sts_rates_maturity', 'sts_include_sstk_analytics', 'position_source', 'listed', 'non_owner_id', 'latest_end_date', 'shock_style', 'g10_currency', 'strategy', 'methodology', 'isin', 'asset_parameters_strike_type'}


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IndexCurveShift(Scenario):
    market_data_pattern: Optional[MarketDataPattern] = field(default=None, metadata=field_metadata)
    freeze_pattern: Optional[MarketDataPattern] = field(default=None, metadata=field_metadata)
    annualised_parallel_shift: Optional[float] = field(default=None, metadata=field_metadata)
    annualised_slope_shift: Optional[float] = field(default=None, metadata=field_metadata)
    cutoff: Optional[float] = field(default=None, metadata=field_metadata)
    floor: Optional[float] = field(default=None, metadata=field_metadata)
    tenor: Optional[str] = field(default=None, metadata=field_metadata)
    rate_option: Optional[str] = field(default=None, metadata=field_metadata)
    bucket_shift: Optional[float] = field(default=None, metadata=field_metadata)
    bucket_start: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    bucket_end: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='IndexCurveShift', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataPatternAndShock(Base):
    pattern: MarketDataPattern = field(default=None, metadata=field_metadata)
    shock: MarketDataShock = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataVolShockScenario(Scenario):
    pattern: MarketDataPattern = field(default=None, metadata=field_metadata)
    shock_type: MarketDataShockType = field(default=None, metadata=field_metadata)
    vol_levels: Tuple[MarketDataVolSlice, ...] = field(default=None, metadata=field_metadata)
    ref_spot: float = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='MarketDataVolShockScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOExposureLeg(Base):
    local_to_base_rate: Optional[str] = field(default=None, metadata=field_metadata)
    local_nav_limits: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    base_nav_limits: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    all_approved_hedge_ratio: Optional[str] = field(default=None, metadata=field_metadata)
    show_all_approved_hedge_ratio: Optional[bool] = field(default=None, metadata=field_metadata)
    hedge_ratio: Optional[str] = field(default=None, metadata=field_metadata)
    exposure_ratio: Optional[str] = field(default=None, metadata=field_metadata)
    local_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    target_ratio: Optional[str] = field(default=None, metadata=field_metadata)
    benchmark: Optional[PCOBenchmark] = field(default=None, metadata=field_metadata)
    long_rebalance_threshold: Optional[str] = field(default=None, metadata=field_metadata)
    short_rebalance_threshold: Optional[str] = field(default=None, metadata=field_metadata)
    base_nav: Optional[str] = field(default=None, metadata=field_metadata)
    local_nav: Optional[str] = field(default=None, metadata=field_metadata)
    base_fx_forward: Optional[str] = field(default=None, metadata=field_metadata)
    local_fx_forward: Optional[str] = field(default=None, metadata=field_metadata)
    auto_roll: Optional[bool] = field(default=None, metadata=field_metadata)
    exposure_currencies: Optional[Tuple[Currency, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class User(Base):
    company: str = field(default=None, metadata=field_metadata)
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    country: str = field(default=None, metadata=field_metadata)
    city: str = field(default=None, metadata=field_metadata)
    region: str = field(default=None, metadata=field_metadata)
    email: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    internal: Optional[bool] = field(default=None, metadata=field_metadata)
    system_user: Optional[bool] = field(default=None, metadata=field_metadata)
    app_user: Optional[bool] = field(default=None, metadata=field_metadata)
    analytics_id: Optional[str] = field(default=None, metadata=field_metadata)
    eaa_company: Optional[str] = field(default=None, metadata=field_metadata)
    root_oe_id: Optional[str] = field(default=None, metadata=config(field_name='rootOEId', exclude=exclude_none))
    oe_id: Optional[str] = field(default=None, metadata=field_metadata)
    root_oe_name: Optional[str] = field(default=None, metadata=config(field_name='rootOEName', exclude=exclude_none))
    oe_name: Optional[str] = field(default=None, metadata=field_metadata)
    oe_alias: Optional[int] = field(default=None, metadata=field_metadata)
    coverage: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    internal_email: Optional[str] = field(default=None, metadata=field_metadata)
    kerberos: Optional[str] = field(default=None, metadata=field_metadata)
    first_name: Optional[str] = field(default=None, metadata=field_metadata)
    last_name: Optional[str] = field(default=None, metadata=field_metadata)
    internal_id: Optional[str] = field(default=None, metadata=config(field_name='internalID', exclude=exclude_none))
    mi_fidii_trade_idea_declined: Optional[str] = field(default=None, metadata=config(field_name='miFIDIITradeIdeaDeclined', exclude=exclude_none))
    department_code: Optional[str] = field(default=None, metadata=field_metadata)
    department_name: Optional[str] = field(default=None, metadata=field_metadata)
    division_name: Optional[str] = field(default=None, metadata=field_metadata)
    business_unit: Optional[str] = field(default=None, metadata=field_metadata)
    title: Optional[str] = field(default=None, metadata=field_metadata)
    pmd: Optional[bool] = field(default=None, metadata=field_metadata)
    login: Optional[str] = field(default=None, metadata=field_metadata)
    tokens: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    roles: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    groups: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    app_managers: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLScheduleArray(Base):
    schedule_values: Optional[Tuple[CSLSchedule, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EntityQuery(Base):
    format_: Optional[Format] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    where: Optional[FieldFilterMap] = field(default=None, metadata=field_metadata)
    as_of_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_since: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    delay: Optional[int] = field(default=None, metadata=field_metadata)
    order_by: Optional[Tuple[Union[DictBase, str], ...]] = field(default=None, metadata=field_metadata)
    scroll: Optional[str] = field(default=None, metadata=field_metadata)
    scroll_id: Optional[str] = field(default=None, metadata=field_metadata)
    fields: Optional[Tuple[Union[DictBase, str], ...]] = field(default=None, metadata=field_metadata)
    limit: Optional[int] = field(default=None, metadata=field_metadata)
    offset: Optional[int] = field(default=None, metadata=field_metadata)
    vendor: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataShockBasedScenario(Scenario):
    shocks: Tuple[MarketDataPatternAndShock, ...] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='MarketDataShockBasedScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class OverlayMarket(SingleMarket):
    base_market: BaseMarket = field(default=None, metadata=field_metadata)
    market_data: Tuple[MarketDataCoordinateValue, ...] = field(default=None, metadata=field_metadata)
    market_model_data: Optional[str] = field(default=None, metadata=field_metadata)
    market_type: Optional[str] = field(init=False, default='OverlayMarket', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PCOExposure(Base):
    last_data_updated_date_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    nav_includes_fx_hedges: Optional[bool] = field(default=None, metadata=field_metadata)
    use_fx_rate_on_base_fx_forward: Optional[bool] = field(default=None, metadata=field_metadata)
    last_generate_orders_date_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    legs: Optional[Tuple[PCOExposureLeg, ...]] = field(default=None, metadata=field_metadata)
    adjustments: Optional[PCOExposureAdjustments] = field(default=None, metadata=field_metadata)
    ratio_mode: Optional[str] = field(default=None, metadata=field_metadata)
    hedge_calc_currency: Optional[PCOCurrencyType] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskMeasure(Base):
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    measure_type: Optional[RiskMeasureType] = field(default=None, metadata=field_metadata)
    unit: Optional[RiskMeasureUnit] = field(default=None, metadata=field_metadata)
    parameters: Optional[RiskMeasureParameter] = field(default=None, metadata=field_metadata)
    value: Optional[Union[float, str]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataSetFieldMap(Base):
    data_set_id: str = field(default=None, metadata=field_metadata)
    field_: str = field(default=None, metadata=config(field_name='field', exclude=exclude_none))
    results_field: str = field(default=None, metadata=field_metadata)
    risk_measure: RiskMeasure = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CompositeScenario(Base):
    scenarios: Optional[Tuple[Scenario, ...]] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='CompositeScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MultiScenario(Scenario):
    scenarios: Optional[Tuple[Scenario, ...]] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[str] = field(init=False, default='MultiScenario', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Position(Base):
    asset_id: Optional[str] = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    weight: Optional[float] = field(default=None, metadata=field_metadata)
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    party_to: Optional[SimpleParty] = field(default=None, metadata=field_metadata)
    party_from: Optional[SimpleParty] = field(default=None, metadata=field_metadata)
    external_ids: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    margin_ids: Optional[Tuple[DictBase, ...]] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[PositionTag, ...]] = field(default=None, metadata=field_metadata)
    instrument: Optional[InstrumentBase] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    error: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RelativeMarket(Base):
    from_market: SingleMarket = field(default=None, metadata=field_metadata)
    to_market: SingleMarket = field(default=None, metadata=field_metadata)
    market_type: Optional[str] = field(init=False, default='RelativeMarket', metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataScenario(Base):
    scenario: Scenario = field(default=None, metadata=field_metadata)
    subtract_base: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PricingDateAndMarketDataAsOf(Base):
    pricing_date: datetime.date = field(default=None, metadata=field_metadata)
    market_data_as_of: Optional[Union[datetime.date, datetime.datetime]] = field(default=None, metadata=field_metadata)
    market: Optional[Market] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LiquidityRequest(Base):
    notional: Optional[float] = field(default=None, metadata=field_metadata)
    positions: Optional[DictBase] = field(default=None, metadata=field_metadata)
    risk_model: Optional[str] = field(default=None, metadata=field_metadata)
    date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    participation_rate: Optional[float] = field(default=None, metadata=field_metadata)
    execution_horizon: Optional[float] = field(default=None, metadata=field_metadata)
    execution_start_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    execution_end_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    benchmark_id: Optional[str] = field(default=None, metadata=field_metadata)
    measures: Optional[Tuple[LiquidityMeasure, ...]] = field(default=None, metadata=field_metadata)
    time_series_benchmark_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    time_series_start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    time_series_end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    format_: Optional[Format] = field(default=None, metadata=config(field_name='format', exclude=exclude_none))
    report_parameters: Optional[LiquidityReportParameters] = field(default=None, metadata=field_metadata)
    explode_positions: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PositionSet(Base):
    positions: Tuple[Position, ...] = field(default=None, metadata=field_metadata)
    position_date: datetime.date = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    last_update_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    type_: Optional[str] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    divisor: Optional[float] = field(default=None, metadata=field_metadata)
    weighting_strategy: Optional[PositionSetWeightingStrategy] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskPosition(Base):
    instrument: Priceable = field(default=None, metadata=field_metadata)
    instrument_name: Optional[str] = field(default=None, metadata=field_metadata)
    quantity: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RiskRequest(Base):
    positions: Tuple[RiskPosition, ...] = field(default=None, metadata=field_metadata)
    measures: Tuple[RiskMeasure, ...] = field(default=None, metadata=field_metadata)
    pricing_and_market_data_as_of: Optional[Tuple[PricingDateAndMarketDataAsOf, ...]] = field(default=None, metadata=field_metadata)
    pricing_location: Optional[PricingLocation] = field(default=None, metadata=field_metadata)
    wait_for_results: Optional[bool] = field(default=False, metadata=field_metadata)
    scenario: Optional[MarketDataScenario] = field(default=None, metadata=field_metadata)
    parameters: Optional[RiskRequestParameters] = field(default=None, metadata=field_metadata)
    request_visible_to_gs: Optional[bool] = field(default=False, metadata=field_metadata)
    use_cache: Optional[bool] = field(default=False, metadata=field_metadata)
    priority: Optional[int] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportParameters(Base):
    approval_id: Optional[str] = field(default=None, metadata=field_metadata)
    asset_class: Optional[AssetClass] = field(default=None, metadata=field_metadata)
    transaction_cost_model: Optional[str] = field(default=None, metadata=field_metadata)
    trading_cost: Optional[float] = field(default=None, metadata=field_metadata)
    servicing_cost_long: Optional[float] = field(default=None, metadata=field_metadata)
    servicing_cost_short: Optional[float] = field(default=None, metadata=field_metadata)
    region: Optional[str] = field(default=None, metadata=field_metadata)
    risk_model: Optional[str] = field(default=None, metadata=field_metadata)
    benchmark: Optional[str] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[PositionTag, ...]] = field(default=None, metadata=field_metadata)
    aggregate_by_tag_name: Optional[str] = field(default=None, metadata=field_metadata)
    fx_hedged: Optional[bool] = field(default=None, metadata=field_metadata)
    publish_to_bloomberg: Optional[bool] = field(default=None, metadata=field_metadata)
    publish_to_reuters: Optional[bool] = field(default=None, metadata=field_metadata)
    publish_to_factset: Optional[bool] = field(default=None, metadata=field_metadata)
    include_price_history: Optional[bool] = field(default=None, metadata=field_metadata)
    index_update: Optional[bool] = field(default=None, metadata=field_metadata)
    index_rebalance: Optional[bool] = field(default=None, metadata=field_metadata)
    index_source_id: Optional[str] = field(default=None, metadata=field_metadata)
    basket_action: Optional[BasketAction] = field(default=None, metadata=field_metadata)
    api_domain: Optional[bool] = field(default=None, metadata=field_metadata)
    initial_price: Optional[float] = field(default=None, metadata=field_metadata)
    stock_level_exposures: Optional[bool] = field(default=None, metadata=field_metadata)
    explode_positions: Optional[bool] = field(default=None, metadata=field_metadata)
    scenario_id: Optional[str] = field(default=None, metadata=field_metadata)
    scenario_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    scenario_group_id: Optional[str] = field(default=None, metadata=field_metadata)
    scenario_type: Optional[ScenarioType] = field(default=None, metadata=field_metadata)
    market_model_id: Optional[str] = field(default=None, metadata=field_metadata)
    risk_measures: Optional[Tuple[RiskMeasure, ...]] = field(default=None, metadata=field_metadata)
    initial_pricing_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    backcast: Optional[bool] = field(default=None, metadata=field_metadata)
    risk_request: Optional[RiskRequest] = field(default=None, metadata=field_metadata)
    subscription_parameters: Optional[ReportSubscriptionParameters] = field(default=None, metadata=field_metadata)
    participation_rate: Optional[float] = field(default=None, metadata=field_metadata)
    approve_rebalance: Optional[bool] = field(default=None, metadata=field_metadata)
    auto_approved_rebalance: Optional[bool] = field(default=None, metadata=field_metadata)
    use_risk_request_batch_mode: Optional[bool] = field(default=None, metadata=field_metadata)
    limited_access_assets: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    corporate_action_restricted_assets: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    backcast_dates: Optional[Tuple[datetime.date, ...]] = field(default=None, metadata=field_metadata)
    base_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    local_currency: Optional[Currency] = field(default=None, metadata=field_metadata)
    fund_calendar: Optional[str] = field(default=None, metadata=field_metadata)
    calculation_currency: Optional[PCOCurrencyType] = field(default=None, metadata=field_metadata)
    hedge_settlement_interval: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    hedge_settlement_day: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    roll_horizon: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    pnl_currency: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    nav_publication_period: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    roll_date_zero_threshold: Optional[bool] = field(default=None, metadata=field_metadata)
    unrealised_mark_to_market: Optional[PCOUnrealisedMarkToMarket] = field(default=None, metadata=field_metadata)
    target_deviation: Optional[Tuple[PCOTargetDeviation, ...]] = field(default=None, metadata=field_metadata)
    cash_balances: Optional[Tuple[PCOCashBalance, ...]] = field(default=None, metadata=field_metadata)
    exposure: Optional[PCOExposure] = field(default=None, metadata=field_metadata)
    pco_share_class: Optional[PCOShareClass] = field(default=None, metadata=field_metadata)
    settlements: Optional[Tuple[PCOSettlements, ...]] = field(default=None, metadata=field_metadata)
    show_cash: Optional[bool] = field(default=None, metadata=field_metadata)
    show_exposure: Optional[bool] = field(default=None, metadata=field_metadata)
    enable_rfq: Optional[bool] = field(default=None, metadata=config(field_name='enableRFQ', exclude=exclude_none))
    fixing_descriptions: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    pco_origin: Optional[PCOOrigin] = field(default=None, metadata=field_metadata)
    pco_action_type: Optional[PCOActionType] = field(default=None, metadata=field_metadata)
    version: Optional[str] = field(default=None, metadata=field_metadata)
    roll_currency: Optional[Tuple[PCOParameterValues, ...]] = field(default=None, metadata=field_metadata)
    use_live_market: Optional[bool] = field(default=None, metadata=field_metadata)
    basket_ready_for_trade: Optional[bool] = field(default=None, metadata=field_metadata)
    allow_in_position_rebalance: Optional[bool] = field(default=None, metadata=field_metadata)
    weighting_strategy: Optional[PositionSetWeightingStrategy] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ReportScheduleRequest(Base):
    parameters: Optional[ReportParameters] = field(default=None, metadata=field_metadata)
    end_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    start_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    use_close_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    priority: Optional[ReportJobPriority] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
