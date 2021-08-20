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
from typing import Mapping, Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


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


class AssetScreenerRequestStringOptions(Base):
        
    """Options for string filters on asset screener."""

    @camel_case_translate
    def __init__(
        self,
        options: tuple,
        type_: str,
        name: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.options = options
        self.name = name

    @property
    def type(self) -> str:
        """whether to include or exclude the provided options"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def options(self) -> tuple:
        """the values to either include or exclude"""
        return self.__options

    @options.setter
    def options(self, value: tuple):
        self._property_changed('options')
        self.__options = value        


class AssetScreenerCreditRequestFilters(Base):
        
    """Filters for credit asset screener request object."""

    @camel_case_translate
    def __init__(
        self,
        face_value: float = None,
        direction: str = None,
        liquidity_score: AssetScreenerRequestFilterLimits = None,
        gs_charge_bps: AssetScreenerRequestFilterLimits = None,
        gs_charge_dollars: AssetScreenerRequestFilterLimits = None,
        duration: AssetScreenerRequestFilterLimits = None,
        issue_date: AssetScreenerRequestFilterDateLimits = None,
        yield_: AssetScreenerRequestFilterLimits = None,
        spread: AssetScreenerRequestFilterLimits = None,
        z_spread: AssetScreenerRequestFilterLimits = None,
        g_spread: AssetScreenerRequestFilterLimits = None,
        mid_price: AssetScreenerRequestFilterLimits = None,
        maturity: AssetScreenerRequestFilterLimits = None,
        amount_outstanding: AssetScreenerRequestFilterLimits = None,
        rating: AssetScreenerCreditStandardAndPoorsRatingOptions = None,
        seniority: AssetScreenerRequestStringOptions = None,
        currency: AssetScreenerRequestStringOptions = None,
        region: AssetScreenerRequestStringOptions = None,
        sector: AssetScreenerRequestStringOptions = None,
        name: str = None
    ):        
        super().__init__()
        self.face_value = face_value
        self.direction = direction
        self.liquidity_score = liquidity_score
        self.gs_charge_bps = gs_charge_bps
        self.gs_charge_dollars = gs_charge_dollars
        self.duration = duration
        self.issue_date = issue_date
        self.__yield = yield_
        self.spread = spread
        self.z_spread = z_spread
        self.g_spread = g_spread
        self.mid_price = mid_price
        self.maturity = maturity
        self.amount_outstanding = amount_outstanding
        self.rating = rating
        self.seniority = seniority
        self.currency = currency
        self.region = region
        self.sector = sector
        self.name = name

    @property
    def face_value(self) -> float:
        """Face value of the bond."""
        return self.__face_value

    @face_value.setter
    def face_value(self, value: float):
        self._property_changed('face_value')
        self.__face_value = value        

    @property
    def direction(self) -> str:
        """Whether the position is a buy or sell."""
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self._property_changed('direction')
        self.__direction = value        

    @property
    def liquidity_score(self) -> AssetScreenerRequestFilterLimits:
        """Liquidity score assigned to buying/selling the bond."""
        return self.__liquidity_score

    @liquidity_score.setter
    def liquidity_score(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('liquidity_score')
        self.__liquidity_score = value        

    @property
    def gs_charge_bps(self) -> AssetScreenerRequestFilterLimits:
        """Goldman Sachs' indicative charge of the bond (bps)."""
        return self.__gs_charge_bps

    @gs_charge_bps.setter
    def gs_charge_bps(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('gs_charge_bps')
        self.__gs_charge_bps = value        

    @property
    def gs_charge_dollars(self) -> AssetScreenerRequestFilterLimits:
        """Goldman Sachs' indicative charge of the bond (dollars)."""
        return self.__gs_charge_dollars

    @gs_charge_dollars.setter
    def gs_charge_dollars(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('gs_charge_dollars')
        self.__gs_charge_dollars = value        

    @property
    def duration(self) -> AssetScreenerRequestFilterLimits:
        """Measure of a bond's price sensitivity to changes in interest rates."""
        return self.__duration

    @duration.setter
    def duration(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('duration')
        self.__duration = value        

    @property
    def issue_date(self) -> AssetScreenerRequestFilterDateLimits:
        """Issue date of the instrument."""
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: AssetScreenerRequestFilterDateLimits):
        self._property_changed('issue_date')
        self.__issue_date = value        

    @property
    def yield_(self) -> AssetScreenerRequestFilterLimits:
        """Return an investor realizes on a bond sold at the mid price."""
        return self.__yield

    @yield_.setter
    def yield_(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('yield_')
        self.__yield = value        

    @property
    def spread(self) -> AssetScreenerRequestFilterLimits:
        """Spread between the yields of a debt security and its benchmark when both are
           purchased at bid price."""
        return self.__spread

    @spread.setter
    def spread(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('spread')
        self.__spread = value        

    @property
    def z_spread(self) -> AssetScreenerRequestFilterLimits:
        """Zero volatility spread of a bond."""
        return self.__z_spread

    @z_spread.setter
    def z_spread(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('z_spread')
        self.__z_spread = value        

    @property
    def g_spread(self) -> AssetScreenerRequestFilterLimits:
        """Difference between yield on treasury bonds and yield on corporate bonds of same
           maturity."""
        return self.__g_spread

    @g_spread.setter
    def g_spread(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('g_spread')
        self.__g_spread = value        

    @property
    def mid_price(self) -> AssetScreenerRequestFilterLimits:
        """Mid price."""
        return self.__mid_price

    @mid_price.setter
    def mid_price(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('mid_price')
        self.__mid_price = value        

    @property
    def maturity(self) -> AssetScreenerRequestFilterLimits:
        """Length of time bond owner will receive interest payments on the investment."""
        return self.__maturity

    @maturity.setter
    def maturity(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('maturity')
        self.__maturity = value        

    @property
    def amount_outstanding(self) -> AssetScreenerRequestFilterLimits:
        """Aggregate principal amount of the total number of bonds not redeemed or
           otherwise discharged."""
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: AssetScreenerRequestFilterLimits):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value        

    @property
    def rating(self) -> AssetScreenerCreditStandardAndPoorsRatingOptions:
        """S&P rating given to a bond."""
        return self.__rating

    @rating.setter
    def rating(self, value: AssetScreenerCreditStandardAndPoorsRatingOptions):
        self._property_changed('rating')
        self.__rating = value        

    @property
    def seniority(self) -> AssetScreenerRequestStringOptions:
        """Seniority of the bond."""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: AssetScreenerRequestStringOptions):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def currency(self) -> AssetScreenerRequestStringOptions:
        """Currency of the bond."""
        return self.__currency

    @currency.setter
    def currency(self, value: AssetScreenerRequestStringOptions):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def region(self) -> AssetScreenerRequestStringOptions:
        """Options for string filters on asset screener."""
        return self.__region

    @region.setter
    def region(self, value: AssetScreenerRequestStringOptions):
        self._property_changed('region')
        self.__region = value        

    @property
    def sector(self) -> AssetScreenerRequestStringOptions:
        """Sector / industry of the bond."""
        return self.__sector

    @sector.setter
    def sector(self, value: AssetScreenerRequestStringOptions):
        self._property_changed('sector')
        self.__sector = value        


class AssetScreenerCreditResponseItem(Base):
        
    """Response object for credit asset screener."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        name: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        cusip: str = None,
        isin: str = None,
        bbid: str = None,
        currency: Union[Currency, str] = None,
        region: Union[Region, str] = None,
        seniority: str = None,
        rating_standard_and_poors: str = None,
        gs_liquidity_score: float = None,
        amount_outstanding: float = None,
        maturity: float = None,
        bval_mid_price: float = None,
        yield_to_convention: float = None,
        modified_duration: float = None,
        spread_to_benchmark: float = None,
        g_spread: float = None,
        z_spread: float = None,
        charge_in_dollars: str = None,
        charge_in_bps: str = None,
        direction: str = None,
        face_value: float = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.name = name
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.cusip = cusip
        self.isin = isin
        self.bbid = bbid
        self.currency = currency
        self.region = region
        self.seniority = seniority
        self.rating_standard_and_poors = rating_standard_and_poors
        self.gs_liquidity_score = gs_liquidity_score
        self.amount_outstanding = amount_outstanding
        self.maturity = maturity
        self.bval_mid_price = bval_mid_price
        self.yield_to_convention = yield_to_convention
        self.modified_duration = modified_duration
        self.spread_to_benchmark = spread_to_benchmark
        self.g_spread = g_spread
        self.z_spread = z_spread
        self.charge_in_dollars = charge_in_dollars
        self.charge_in_bps = charge_in_bps
        self.direction = direction
        self.face_value = face_value

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def name(self) -> str:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def cusip(self) -> str:
        """Cusip Identifier"""
        return self.__cusip

    @cusip.setter
    def cusip(self, value: str):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def isin(self) -> str:
        """International Security Number"""
        return self.__isin

    @isin.setter
    def isin(self, value: str):
        self._property_changed('isin')
        self.__isin = value        

    @property
    def bbid(self) -> str:
        """Bloomberg Identifier"""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def region(self) -> Union[Region, str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union[Region, str]):
        self._property_changed('region')
        self.__region = get_enum_value(Region, value)        

    @property
    def seniority(self) -> str:
        """The seniority of the bond"""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: str):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def rating_standard_and_poors(self) -> str:
        """Bond rating from Standard And Poor's."""
        return self.__rating_standard_and_poors

    @rating_standard_and_poors.setter
    def rating_standard_and_poors(self, value: str):
        self._property_changed('rating_standard_and_poors')
        self.__rating_standard_and_poors = value        

    @property
    def gs_liquidity_score(self) -> float:
        """Goldman Sachs' liquidity score for the bond (1-5.99)."""
        return self.__gs_liquidity_score

    @gs_liquidity_score.setter
    def gs_liquidity_score(self, value: float):
        self._property_changed('gs_liquidity_score')
        self.__gs_liquidity_score = value        

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
    def maturity(self) -> float:
        """Time to the bond's maturity."""
        return self.__maturity

    @maturity.setter
    def maturity(self, value: float):
        self._property_changed('maturity')
        self.__maturity = value        

    @property
    def bval_mid_price(self) -> float:
        """BVAL mid price."""
        return self.__bval_mid_price

    @bval_mid_price.setter
    def bval_mid_price(self, value: float):
        self._property_changed('bval_mid_price')
        self.__bval_mid_price = value        

    @property
    def yield_to_convention(self) -> float:
        """The bond's yield to convention."""
        return self.__yield_to_convention

    @yield_to_convention.setter
    def yield_to_convention(self, value: float):
        self._property_changed('yield_to_convention')
        self.__yield_to_convention = value        

    @property
    def modified_duration(self) -> float:
        """Price sensitivity of a bond when there is a change in the yield to maturity."""
        return self.__modified_duration

    @modified_duration.setter
    def modified_duration(self, value: float):
        self._property_changed('modified_duration')
        self.__modified_duration = value        

    @property
    def spread_to_benchmark(self) -> float:
        """Spread to benchmark."""
        return self.__spread_to_benchmark

    @spread_to_benchmark.setter
    def spread_to_benchmark(self, value: float):
        self._property_changed('spread_to_benchmark')
        self.__spread_to_benchmark = value        

    @property
    def g_spread(self) -> float:
        """Bid G Spread."""
        return self.__g_spread

    @g_spread.setter
    def g_spread(self, value: float):
        self._property_changed('g_spread')
        self.__g_spread = value        

    @property
    def z_spread(self) -> float:
        """Mid Z Spread."""
        return self.__z_spread

    @z_spread.setter
    def z_spread(self, value: float):
        self._property_changed('z_spread')
        self.__z_spread = value        

    @property
    def charge_in_dollars(self) -> str:
        """Goldman's charge to buy or sell the bond from you in $."""
        return self.__charge_in_dollars

    @charge_in_dollars.setter
    def charge_in_dollars(self, value: str):
        self._property_changed('charge_in_dollars')
        self.__charge_in_dollars = value        

    @property
    def charge_in_bps(self) -> str:
        """Goldman's charge to buy or sell the bond from you in bps."""
        return self.__charge_in_bps

    @charge_in_bps.setter
    def charge_in_bps(self, value: str):
        self._property_changed('charge_in_bps')
        self.__charge_in_bps = value        

    @property
    def direction(self) -> str:
        """Whether the position is a buy or sell."""
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self._property_changed('direction')
        self.__direction = value        

    @property
    def face_value(self) -> float:
        """The face value of the bond."""
        return self.__face_value

    @face_value.setter
    def face_value(self, value: float):
        self._property_changed('face_value')
        self.__face_value = value        


class AssetScreenerRequest(Base):
        
    """Request object for asset screener."""

    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        type_: Union[AssetType, str] = None,
        scroll: str = None,
        scroll_id: str = None,
        limit: int = None,
        offset: int = None,
        filters: AssetScreenerCreditRequestFilters = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.__type = get_enum_value(AssetType, type_)
        self.scroll = scroll
        self.scroll_id = scroll_id
        self.limit = limit
        self.offset = offset
        self.filters = filters
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
    def type(self) -> Union[AssetType, str]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: Union[AssetType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(AssetType, value)        

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
    def filters(self) -> AssetScreenerCreditRequestFilters:
        """constraints a user can filter on for asset screener"""
        return self.__filters

    @filters.setter
    def filters(self, value: AssetScreenerCreditRequestFilters):
        self._property_changed('filters')
        self.__filters = value        


class AssetScreenerCreditResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        total_results: int,
        results: Tuple[AssetScreenerCreditResponseItem, ...] = None,
        scroll_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.total_results = total_results
        self.results = results
        self.scroll_id = scroll_id
        self.name = name

    @property
    def total_results(self) -> int:
        """Total number of results that match the query."""
        return self.__total_results

    @total_results.setter
    def total_results(self, value: int):
        self._property_changed('total_results')
        self.__total_results = value        

    @property
    def results(self) -> Tuple[AssetScreenerCreditResponseItem, ...]:
        """Array of Asset Screener Credit Response Item objects"""
        return self.__results

    @results.setter
    def results(self, value: Tuple[AssetScreenerCreditResponseItem, ...]):
        self._property_changed('results')
        self.__results = value        

    @property
    def scroll_id(self) -> str:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scroll_id

    @scroll_id.setter
    def scroll_id(self, value: str):
        self._property_changed('scroll_id')
        self.__scroll_id = value        
