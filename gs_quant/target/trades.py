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
from gs_quant.base import Base, EnumBase, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class MqexsAssetClass(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""

    Commod = 'Commod'
    FX = 'FX'
    Equity = 'Equity'
    Earon = 'Earon'
    FICC = 'FICC'
    
    def __repr__(self):
        return self.value


class MqexsAssetClassExt(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""

    Commod = 'Commod'
    FX = 'FX'
    Equity = 'Equity'
    
    def __repr__(self):
        return self.value


class MqexsClearer(EnumBase, Enum):    
    
    """The clearer code"""

    CME = 'CME'
    ICE = 'ICE'
    NFX = 'NFX'
    OTC = 'OTC'
    LME = 'LME'
    CME_ICE = 'CME-ICE'
    
    def __repr__(self):
        return self.value


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
    
    def __repr__(self):
        return self.value


class MqexsOtcSettlementType(EnumBase, Enum):    
    
    """OTC settlement type"""

    Bullet = 'Bullet'
    Calendar_Month_Average = 'Calendar Month Average'
    Trade_Month_Average = 'Trade Month Average'
    
    def __repr__(self):
        return self.value


class MqexsSide(EnumBase, Enum):    
    
    """Field represents the order or trade action."""

    Buy = 'Buy'
    Sell = 'Sell'
    _ = ''
    
    def __repr__(self):
        return self.value


class MqexsErrorInfo(Base):
        
    """Service specific error code and message returned as a server response"""
       
    def __init__(self, errorCode: str, errorMsg: str, assetClass: Union[MqexsAssetClass, str] = None):
        super().__init__()
        self.__errorCode = errorCode
        self.__errorMsg = errorMsg
        self.__assetClass = assetClass if isinstance(assetClass, MqexsAssetClass) else get_enum_value(MqexsAssetClass, assetClass)

    @property
    def errorCode(self) -> str:
        """specific error code in the server response indicating an order processing error."""
        return self.__errorCode

    @errorCode.setter
    def errorCode(self, value: str):
        self.__errorCode = value
        self._property_changed('errorCode')        

    @property
    def errorMsg(self) -> str:
        """specific error message in the server response indicating an order processing error."""
        return self.__errorMsg

    @errorMsg.setter
    def errorMsg(self, value: str):
        self.__errorMsg = value
        self._property_changed('errorMsg')        

    @property
    def assetClass(self) -> Union[MqexsAssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[MqexsAssetClass, str]):
        self.__assetClass = value if isinstance(value, MqexsAssetClass) else get_enum_value(MqexsAssetClass, value)
        self._property_changed('assetClass')        


class MqexsProductDetails(Base):
        
    """Details specific to the product type."""
       
    def __init__(self, name: str, contractCode: str = None, clearer: Union[MqexsClearer, str] = None, settlementType: Union[MqexsOtcSettlementType, str] = None):
        super().__init__()
        self.__contractCode = contractCode
        self.__name = name
        self.__clearer = clearer if isinstance(clearer, MqexsClearer) else get_enum_value(MqexsClearer, clearer)
        self.__settlementType = settlementType if isinstance(settlementType, MqexsOtcSettlementType) else get_enum_value(MqexsOtcSettlementType, settlementType)

    @property
    def contractCode(self) -> str:
        """Contract month"""
        return self.__contractCode

    @contractCode.setter
    def contractCode(self, value: str):
        self.__contractCode = value
        self._property_changed('contractCode')        

    @property
    def name(self) -> str:
        """The financial product symbol"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def clearer(self) -> Union[MqexsClearer, str]:
        """The clearer code"""
        return self.__clearer

    @clearer.setter
    def clearer(self, value: Union[MqexsClearer, str]):
        self.__clearer = value if isinstance(value, MqexsClearer) else get_enum_value(MqexsClearer, value)
        self._property_changed('clearer')        

    @property
    def settlementType(self) -> Union[MqexsOtcSettlementType, str]:
        """OTC settlement type"""
        return self.__settlementType

    @settlementType.setter
    def settlementType(self, value: Union[MqexsOtcSettlementType, str]):
        self.__settlementType = value if isinstance(value, MqexsOtcSettlementType) else get_enum_value(MqexsOtcSettlementType, value)
        self._property_changed('settlementType')        


class MqexsTradeDetails(Base):
        
    """Details specific to the trade type."""
       
    def __init__(self, side: Union[MqexsSide, str], quantity: str, unitPrice: str, currency: Union[MqexsCurrencyExt, str], settlementDate: datetime.date = None, quantityUnit: str = None):
        super().__init__()
        self.__settlementDate = settlementDate
        self.__side = side if isinstance(side, MqexsSide) else get_enum_value(MqexsSide, side)
        self.__quantity = quantity
        self.__unitPrice = unitPrice
        self.__quantityUnit = quantityUnit
        self.__currency = currency if isinstance(currency, MqexsCurrencyExt) else get_enum_value(MqexsCurrencyExt, currency)

    @property
    def settlementDate(self) -> datetime.date:
        """Settlement date, formatted as yyyy-MM or yyyy-MM-dd (ISO-8601)"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: datetime.date):
        self.__settlementDate = value
        self._property_changed('settlementDate')        

    @property
    def side(self) -> Union[MqexsSide, str]:
        """Field represents the order or trade action."""
        return self.__side

    @side.setter
    def side(self, value: Union[MqexsSide, str]):
        self.__side = value if isinstance(value, MqexsSide) else get_enum_value(MqexsSide, value)
        self._property_changed('side')        

    @property
    def quantity(self) -> str:
        """Quantity of product being requested, as a string representation of the double value"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: str):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def unitPrice(self) -> str:
        """trade unit price."""
        return self.__unitPrice

    @unitPrice.setter
    def unitPrice(self, value: str):
        self.__unitPrice = value
        self._property_changed('unitPrice')        

    @property
    def quantityUnit(self) -> str:
        """unit and frequency of the quantity of a product in a quote"""
        return self.__quantityUnit

    @quantityUnit.setter
    def quantityUnit(self, value: str):
        self.__quantityUnit = value
        self._property_changed('quantityUnit')        

    @property
    def currency(self) -> Union[MqexsCurrencyExt, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[MqexsCurrencyExt, str]):
        self.__currency = value if isinstance(value, MqexsCurrencyExt) else get_enum_value(MqexsCurrencyExt, value)
        self._property_changed('currency')        


class MqexsTradeExt(Base):
        
    """Trade Object Model"""
       
    def __init__(self, id: str, tradeDetails: MqexsTradeDetails, productDetails: MqexsProductDetails, quoteId: str, assetClass: Union[MqexsAssetClassExt, str], createdById: str, createdTime: datetime.datetime, lastUpdatedTime: datetime.datetime, lastUpdatedById: str):
        super().__init__()
        self.__id = id
        self.__tradeDetails = tradeDetails
        self.__productDetails = productDetails
        self.__quoteId = quoteId
        self.__assetClass = assetClass if isinstance(assetClass, MqexsAssetClassExt) else get_enum_value(MqexsAssetClassExt, assetClass)
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__lastUpdatedTime = lastUpdatedTime
        self.__lastUpdatedById = lastUpdatedById

    @property
    def id(self) -> str:
        """trade unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def tradeDetails(self) -> MqexsTradeDetails:
        """Details specific to the trade type."""
        return self.__tradeDetails

    @tradeDetails.setter
    def tradeDetails(self, value: MqexsTradeDetails):
        self.__tradeDetails = value
        self._property_changed('tradeDetails')        

    @property
    def productDetails(self) -> MqexsProductDetails:
        """Details specific to the product type."""
        return self.__productDetails

    @productDetails.setter
    def productDetails(self, value: MqexsProductDetails):
        self.__productDetails = value
        self._property_changed('productDetails')        

    @property
    def quoteId(self) -> str:
        """trade unique identifier"""
        return self.__quoteId

    @quoteId.setter
    def quoteId(self, value: str):
        self.__quoteId = value
        self._property_changed('quoteId')        

    @property
    def assetClass(self) -> Union[MqexsAssetClassExt, str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union[MqexsAssetClassExt, str]):
        self.__assetClass = value if isinstance(value, MqexsAssetClassExt) else get_enum_value(MqexsAssetClassExt, value)
        self._property_changed('assetClass')        

    @property
    def createdById(self) -> str:
        """Creation user's unique identifier"""
        return self.__createdById

    @createdById.setter
    def createdById(self, value: str):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def createdTime(self) -> datetime.datetime:
        """Creation time as ISO-8601 UTC instant"""
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: datetime.datetime):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        """Last update time as ISO-8601 UTC instant"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def lastUpdatedById(self) -> str:
        """Last update user's unique identifier"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: str):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        
