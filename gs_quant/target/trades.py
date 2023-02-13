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


class MqexsAssetClass(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which
       exhibit similar characteristics and behave in a consistent way under
       different market conditions"""

    Commod = 'Commod'
    FX = 'FX'
    Equity = 'Equity'
    Earon = 'Earon'
    FICC = 'FICC'
    Prime = 'Prime'
    IOI = 'IOI'
    Rates = 'Rates'
    PCO = 'PCO'    


class MqexsAssetClassExt(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which
       exhibit similar characteristics and behave in a consistent way under
       different market conditions"""

    Commod = 'Commod'
    FX = 'FX'
    Equity = 'Equity'    


class MqexsClearer(EnumBase, Enum):    
    
    """The clearer code"""

    CME = 'CME'
    ICE = 'ICE'
    NFX = 'NFX'
    OTC = 'OTC'
    LME = 'LME'
    CME_ICE = 'CME-ICE'    


class MqexsCurrencyExt(EnumBase, Enum):    
    
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


class MqexsErrorSeverity(EnumBase, Enum):    
    
    """The severity of the error, which can be a warning or a fatal error"""

    Pass = 'Pass'
    Warning = 'Warning'
    Fatal = 'Fatal'
    FatalException = 'FatalException'    


class MqexsOtcSettlementType(EnumBase, Enum):    
    
    """OTC settlement type"""

    Bullet = 'Bullet'
    Calendar_Month_Average = 'Calendar Month Average'
    Trade_Month_Average = 'Trade Month Average'
    Physical = 'Physical'
    CalMonth_Avg_No_Roll_Adjust = 'CalMonth Avg No Roll Adjust'
    Heren_Month_Ahead = 'Heren Month Ahead'
    Heren_Day_Ahead = 'Heren Day Ahead'    


class MqexsPricingType(EnumBase, Enum):    
    
    """The source to be used to get a quote"""

    CommodStream = 'CommodStream'
    eAronStream = 'eAronStream'
    FXStreaming = 'FXStreaming'
    Heat = 'Heat'
    Indicative = 'Indicative'
    LiquidityStream = 'LiquidityStream'
    OneDeltaStream = 'OneDeltaStream'
    OptionChain = 'OptionChain'
    RFQ = 'RFQ'
    RFQSales = 'RFQSales'
    Roll = 'Roll'
    RFQRollSales = 'RFQRollSales'
    Swap = 'Swap'
    RFQSwapSales = 'RFQSwapSales'
    TradableStream = 'TradableStream'
    UnifiedRFQ = 'UnifiedRFQ'
    PCORFQ = 'PCORFQ'    


class MqexsSide(EnumBase, Enum):    
    
    """Field represents the order or trade action."""

    Buy = 'Buy'
    Sell = 'Sell'
    BuySell = 'BuySell'
    SellBuy = 'SellBuy'
    Above = 'Above'
    Below = 'Below'
    _ = ''    


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MqexsErrorInfo(Base):
    error_code: str = field(default=None, metadata=field_metadata)
    error_msg: str = field(default=None, metadata=field_metadata)
    error_severity: Optional[MqexsErrorSeverity] = field(default=None, metadata=field_metadata)
    asset_class: Optional[MqexsAssetClass] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MqexsProductDetails(Base):
    name: str = field(default=None, metadata=field_metadata)
    contract_code: Optional[str] = field(default=None, metadata=field_metadata)
    clearer: Optional[MqexsClearer] = field(default=None, metadata=field_metadata)
    settlement_type: Optional[MqexsOtcSettlementType] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MqexsTradeDetails(Base):
    side: MqexsSide = field(default=None, metadata=field_metadata)
    quantity: str = field(default=None, metadata=field_metadata)
    unit_price: str = field(default=None, metadata=field_metadata)
    currency: MqexsCurrencyExt = field(default=None, metadata=field_metadata)
    settlement_date: Optional[datetime.date] = field(default=None, metadata=field_metadata)
    quantity_lots: Optional[str] = field(default=None, metadata=field_metadata)
    quantity_unit: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MqexsTradeExt(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    trade_details: MqexsTradeDetails = field(default=None, metadata=field_metadata)
    product_details: MqexsProductDetails = field(default=None, metadata=field_metadata)
    quote_id: str = field(default=None, metadata=field_metadata)
    asset_class: MqexsAssetClassExt = field(default=None, metadata=field_metadata)
    created_by_id: str = field(default=None, metadata=field_metadata)
    created_time: datetime.datetime = field(default=None, metadata=field_metadata)
    last_updated_time: datetime.datetime = field(default=None, metadata=field_metadata)
    last_updated_by_id: str = field(default=None, metadata=field_metadata)
    inquiry_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MqexsTradesWErrorExt(Base):
    trades: Optional[Tuple[MqexsTradeExt, ...]] = field(default=None, metadata=field_metadata)
    errors: Optional[Tuple[MqexsErrorInfo, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
