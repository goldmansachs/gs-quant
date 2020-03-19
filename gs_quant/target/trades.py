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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


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
    
    def __repr__(self):
        return self.value


class MqexsAssetClassExt(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which
       exhibit similar characteristics and behave in a consistent way under
       different market conditions"""

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


class MqexsErrorSeverity(EnumBase, Enum):    
    
    """The severity of the error, which can be a warning or a fatal error"""

    Pass = 'Pass'
    Warning = 'Warning'
    Fatal = 'Fatal'
    FatalException = 'FatalException'
    
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
    BuySell = 'BuySell'
    SellBuy = 'SellBuy'
    Above = 'Above'
    Below = 'Below'
    _ = ''
    
    def __repr__(self):
        return self.value


class MqexsErrorInfo(Base):
        
    """Service specific error code and message returned as a server response"""

    @camel_case_translate
    def __init__(
        self,
        error_code: str,
        error_msg: str,
        error_severity: Union[MqexsErrorSeverity, str] = None,
        asset_class: Union[MqexsAssetClass, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_severity = error_severity
        self.asset_class = asset_class
        self.name = name

    @property
    def error_code(self) -> str:
        """specific error code in the server response indicating an order processing error."""
        return self.__error_code

    @error_code.setter
    def error_code(self, value: str):
        self._property_changed('error_code')
        self.__error_code = value        

    @property
    def error_msg(self) -> str:
        """specific error message in the server response indicating an order processing
           error."""
        return self.__error_msg

    @error_msg.setter
    def error_msg(self, value: str):
        self._property_changed('error_msg')
        self.__error_msg = value        

    @property
    def error_severity(self) -> Union[MqexsErrorSeverity, str]:
        """The severity of the error, which can be a warning or a fatal error"""
        return self.__error_severity

    @error_severity.setter
    def error_severity(self, value: Union[MqexsErrorSeverity, str]):
        self._property_changed('error_severity')
        self.__error_severity = get_enum_value(MqexsErrorSeverity, value)        

    @property
    def asset_class(self) -> Union[MqexsAssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[MqexsAssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(MqexsAssetClass, value)        


class MqexsProductDetails(Base):
        
    """Details specific to the product type."""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        contract_code: str = None,
        clearer: Union[MqexsClearer, str] = None,
        settlement_type: Union[MqexsOtcSettlementType, str] = None
    ):        
        super().__init__()
        self.contract_code = contract_code
        self.name = name
        self.clearer = clearer
        self.settlement_type = settlement_type

    @property
    def contract_code(self) -> str:
        """Contract month"""
        return self.__contract_code

    @contract_code.setter
    def contract_code(self, value: str):
        self._property_changed('contract_code')
        self.__contract_code = value        

    @property
    def name(self) -> str:
        """The financial product symbol"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def clearer(self) -> Union[MqexsClearer, str]:
        """The clearer code"""
        return self.__clearer

    @clearer.setter
    def clearer(self, value: Union[MqexsClearer, str]):
        self._property_changed('clearer')
        self.__clearer = get_enum_value(MqexsClearer, value)        

    @property
    def settlement_type(self) -> Union[MqexsOtcSettlementType, str]:
        """OTC settlement type"""
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: Union[MqexsOtcSettlementType, str]):
        self._property_changed('settlement_type')
        self.__settlement_type = get_enum_value(MqexsOtcSettlementType, value)        


class MqexsTradeDetails(Base):
        
    """Details specific to the trade type."""

    @camel_case_translate
    def __init__(
        self,
        side: Union[MqexsSide, str],
        quantity: str,
        unit_price: str,
        currency: Union[MqexsCurrencyExt, str],
        settlement_date: datetime.date = None,
        quantity_lots: str = None,
        quantity_unit: str = None,
        name: str = None
    ):        
        super().__init__()
        self.settlement_date = settlement_date
        self.side = side
        self.quantity = quantity
        self.quantity_lots = quantity_lots
        self.unit_price = unit_price
        self.quantity_unit = quantity_unit
        self.currency = currency
        self.name = name

    @property
    def settlement_date(self) -> datetime.date:
        """Settlement date, formatted as yyyy-MM or yyyy-MM-dd (ISO-8601)"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def side(self) -> Union[MqexsSide, str]:
        """Field represents the order or trade action."""
        return self.__side

    @side.setter
    def side(self, value: Union[MqexsSide, str]):
        self._property_changed('side')
        self.__side = get_enum_value(MqexsSide, value)        

    @property
    def quantity(self) -> str:
        """Quantity of product being requested, as a string representation of the double
           value"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: str):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def quantity_lots(self) -> str:
        """Quantity in lots of product being requested, as a string representation of the
           double value"""
        return self.__quantity_lots

    @quantity_lots.setter
    def quantity_lots(self, value: str):
        self._property_changed('quantity_lots')
        self.__quantity_lots = value        

    @property
    def unit_price(self) -> str:
        """trade unit price."""
        return self.__unit_price

    @unit_price.setter
    def unit_price(self, value: str):
        self._property_changed('unit_price')
        self.__unit_price = value        

    @property
    def quantity_unit(self) -> str:
        """unit and frequency of the quantity of a product in a quote"""
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: str):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def currency(self) -> Union[MqexsCurrencyExt, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[MqexsCurrencyExt, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(MqexsCurrencyExt, value)        


class MqexsTradeExt(Base):
        
    """Trade Object Model"""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        trade_details: MqexsTradeDetails,
        product_details: MqexsProductDetails,
        quote_id: str,
        asset_class: Union[MqexsAssetClassExt, str],
        created_by_id: str,
        created_time: datetime.datetime,
        last_updated_time: datetime.datetime,
        last_updated_by_id: str,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.trade_details = trade_details
        self.product_details = product_details
        self.quote_id = quote_id
        self.asset_class = asset_class
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.last_updated_by_id = last_updated_by_id
        self.name = name

    @property
    def id(self) -> str:
        """trade unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def trade_details(self) -> MqexsTradeDetails:
        """Details specific to the trade type."""
        return self.__trade_details

    @trade_details.setter
    def trade_details(self, value: MqexsTradeDetails):
        self._property_changed('trade_details')
        self.__trade_details = value        

    @property
    def product_details(self) -> MqexsProductDetails:
        """Details specific to the product type."""
        return self.__product_details

    @product_details.setter
    def product_details(self, value: MqexsProductDetails):
        self._property_changed('product_details')
        self.__product_details = value        

    @property
    def quote_id(self) -> str:
        """trade unique identifier"""
        return self.__quote_id

    @quote_id.setter
    def quote_id(self, value: str):
        self._property_changed('quote_id')
        self.__quote_id = value        

    @property
    def asset_class(self) -> Union[MqexsAssetClassExt, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[MqexsAssetClassExt, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(MqexsAssetClassExt, value)        

    @property
    def created_by_id(self) -> str:
        """Creation user's unique identifier"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Creation time as ISO-8601 UTC instant"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Last update time as ISO-8601 UTC instant"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def last_updated_by_id(self) -> str:
        """Last update user's unique identifier"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        


class MqexsTradesWErrorExt(Base):
        
    """List of trade objects returned as a server response with specific error code and
       message in case of a server error."""

    @camel_case_translate
    def __init__(
        self,
        trades: Tuple[MqexsTradeExt, ...] = None,
        errors: Tuple[MqexsErrorInfo, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.trades = trades
        self.errors = errors
        self.name = name

    @property
    def trades(self) -> Tuple[MqexsTradeExt, ...]:
        """The requested trades"""
        return self.__trades

    @trades.setter
    def trades(self, value: Tuple[MqexsTradeExt, ...]):
        self._property_changed('trades')
        self.__trades = value        

    @property
    def errors(self) -> Tuple[MqexsErrorInfo, ...]:
        """Errors encountered during request"""
        return self.__errors

    @errors.setter
    def errors(self, value: Tuple[MqexsErrorInfo, ...]):
        self._property_changed('errors')
        self.__errors = value        
