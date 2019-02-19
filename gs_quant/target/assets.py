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

import datetime
from typing import Any, Iterable, Union
from enum import Enum
from gs_quant.base import EnumBase, Base


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
    Systematic_Hedging = 'Systematic Hedging'
    
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


class AssetStatsType(EnumBase, Enum):    
    
    """Is it rolling, none etc."""

    Rolling = 'Rolling'
    Calendar = 'Calendar'
    
    def __repr__(self):
        return self.value


class AssetStatsPeriod(EnumBase, Enum):    
    
    """The period used to produce date range."""

    _1y = '1y'
    _3y = '3y'
    _5y = '5y'
    _10y = '10y'
    
    def __repr__(self):
        return self.value


class NetExposureClassification(EnumBase, Enum):    
    
    """Classification for net exposure of fund."""

    Short_Only__OVER__Short_Bias = 'Short Only / Short Bias'
    Market_Neutral = 'Market Neutral'
    Low_Net = 'Low Net'
    Variable_Net = 'Variable Net'
    Long_Biased = 'Long Biased'
    Long_Only = 'Long Only'
    
    def __repr__(self):
        return self.value


class SupraStrategy(EnumBase, Enum):    
    
    """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""

    Composite = 'Composite'
    Credit = 'Credit'
    Equity = 'Equity'
    Equity_Hedge = 'Equity Hedge'
    Event_Driven = 'Event Driven'
    Fund_of_Funds = 'Fund of Funds'
    Macro = 'Macro'
    Multi_Strategy = 'Multi-Strategy'
    Other = 'Other'
    Quant = 'Quant'
    Relative_Value = 'Relative Value'
    Risk_Parity = 'Risk Parity'
    
    def __repr__(self):
        return self.value


class Strategy(EnumBase, Enum):    
    
    """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""

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
    
    def __repr__(self):
        return self.value


class AllocatorType(EnumBase, Enum):    
    
    """Allocator type defines the type of investor company managing an asset"""

    Advisor = 'Advisor'
    Consultant_Institutional = 'Consultant Institutional'
    Endowment = 'Endowment'
    Family_Office_Multi = 'Family Office Multi'
    Family_Office_Single = 'Family Office Single'
    Foundation = 'Foundation'
    Fund_of_Funds = 'Fund of Funds'
    Insurance_Company = 'Insurance Company'
    Outsourced_CIO = 'Outsourced CIO'
    Pension_Private = 'Pension Private'
    Pension_Public = 'Pension Public'
    Private_Bank = 'Private Bank'
    Prop_Capital_OVER_Commercial_Bank = 'Prop Capital/Commercial Bank'
    Sovereign_Wealth_Fund = 'Sovereign Wealth Fund'
    
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


class CommoditySubFamily(EnumBase, Enum):    
    
    """Commodity SubFamily"""

    Crude = 'Crude'
    Fuel = 'Fuel'
    Heat = 'Heat'
    NG = 'NG'
    
    def __repr__(self):
        return self.value


class CommodityFamily(EnumBase, Enum):    
    
    """Commodity Family"""

    Base_Metal = 'Base Metal'
    Gas = 'Gas'
    Oil = 'Oil'
    Oil_Products = 'Oil Products'
    
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


class Asset(Base):
        
    """A security or instrument which can be held in a trading book (for example a stock or a bond) or a publically identifiable object with observable market data fixings which can be referenced in derivative transations (for example the SPX Index)"""
       
    def __init__(self, assetClass: Union['AssetClass', str], type: Union['AssetType', str], name: Union[str, str], createdById: Union[str, str] = None, createdTime: Union[datetime.datetime, str] = None, currency: Union['Currency', str] = None, description: Union[str, str] = None, domains: Union['Domains', str] = None, entitlements: Union['Entitlements', str] = None, exchange: Union[str, str] = None, id: Union[str, str] = None, identifiers: Iterable['Identifier'] = None, lastUpdatedById: Union[str, str] = None, lastUpdatedTime: Union[datetime.datetime, str] = None, listed: bool = None, liveDate: Union[datetime.date, str] = None, ownerId: Union[str, str] = None, parameters=None, assetStats: Iterable['AssetStats'] = None, people: Union['People', str] = None, region: Union['Region', str] = None, reportIds=None, shortName: Union[str, str] = None, styles=None, tags=None, underlyingAssetIds: Iterable[str] = None):
        super().__init__()
        self.__assetClass = assetClass
        self.__createdById = createdById
        self.__createdTime = createdTime
        self.__currency = currency
        self.__description = description
        self.__domains = domains
        self.__entitlements = entitlements
        self.__exchange = exchange
        self.__id = id
        self.__identifiers = identifiers
        self.__lastUpdatedById = lastUpdatedById
        self.__lastUpdatedTime = lastUpdatedTime
        self.__listed = listed
        self.__liveDate = liveDate
        self.__name = name
        self.__ownerId = ownerId
        self.__parameters = parameters
        self.__assetStats = assetStats
        self.__people = people
        self.__region = region
        self.__reportIds = reportIds
        self.__shortName = shortName
        self.__styles = styles
        self.__tags = tags
        self.__type = type
        self.__underlyingAssetIds = underlyingAssetIds

    @property
    def assetClass(self) -> Union['AssetClass', str]:
        """Asset classification of security. Assets are classified into broad groups which exhibit similar characteristics and behave in a consistent way under different market conditions"""
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value: Union['AssetClass', str]):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def createdById(self) -> Union[str, str]:
        """Unique identifier of user who created the object"""
        return self.__createdById

    @createdById.setter
    def createdById(self, value: Union[str, str]):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def createdTime(self) -> Union[datetime.datetime, str]:
        """Time created. ISO 8601 formatted string"""
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value: Union[datetime.datetime, str]):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def currency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union['Currency', str]):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def description(self) -> Union[str, str]:
        """Free text description of asset. Description provided will be indexed in the search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: Union[str, str]):
        self.__description = value
        self._property_changed('description')        

    @property
    def domains(self) -> Union['Domains', str]:
        """Application specific domain information"""
        return self.__domains

    @domains.setter
    def domains(self, value: Union['Domains', str]):
        self.__domains = value
        self._property_changed('domains')        

    @property
    def entitlements(self) -> Union['Entitlements', str]:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Union['Entitlements', str]):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def exchange(self) -> Union[str, str]:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: Union[str, str]):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def id(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: Union[str, str]):
        self.__id = value
        self._property_changed('id')        

    @property
    def identifiers(self) -> Iterable['Identifier']:
        """Array of identifier objects which can be used to locate this item in searches and other services"""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Iterable['Identifier']):
        self.__identifiers = value
        self._property_changed('identifiers')        

    @property
    def lastUpdatedById(self) -> Union[str, str]:
        """Unique identifier of user who last updated the object"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: Union[str, str]):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def lastUpdatedTime(self) -> Union[datetime.datetime, str]:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: Union[datetime.datetime, str]):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def listed(self) -> bool:
        """Whether the asset is currently listed or not"""
        return self.__listed

    @listed.setter
    def listed(self, value: bool):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def liveDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__liveDate

    @liveDate.setter
    def liveDate(self, value: Union[datetime.date, str]):
        self.__liveDate = value
        self._property_changed('liveDate')        

    @property
    def name(self) -> Union[str, str]:
        """Display name of the asset"""
        return self.__name

    @name.setter
    def name(self, value: Union[str, str]):
        self.__name = value
        self._property_changed('name')        

    @property
    def ownerId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value: Union[str, str]):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value
        self._property_changed('parameters')        

    @property
    def assetStats(self) -> Iterable['AssetStats']:
        return self.__assetStats

    @assetStats.setter
    def assetStats(self, value: Iterable['AssetStats']):
        self.__assetStats = value
        self._property_changed('assetStats')        

    @property
    def people(self) -> Union['People', str]:
        """Key people associated with asset"""
        return self.__people

    @people.setter
    def people(self, value: Union['People', str]):
        self.__people = value
        self._property_changed('people')        

    @property
    def region(self) -> Union['Region', str]:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: Union['Region', str]):
        self.__region = value
        self._property_changed('region')        

    @property
    def reportIds(self):
        """Array of report identifiers related to the object"""
        return self.__reportIds

    @reportIds.setter
    def reportIds(self, value):
        self.__reportIds = value
        self._property_changed('reportIds')        

    @property
    def shortName(self) -> Union[str, str]:
        """Short name or alias for the asset"""
        return self.__shortName

    @shortName.setter
    def shortName(self, value: Union[str, str]):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def styles(self):
        """Styles or themes associated with the asset (max 50)"""
        return self.__styles

    @styles.setter
    def styles(self, value):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def tags(self):
        """Metadata associated with the object. Provide an array of strings which will be indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def type(self) -> Union['AssetType', str]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: Union['AssetType', str]):
        self.__type = value
        self._property_changed('type')        

    @property
    def underlyingAssetIds(self) -> Iterable[str]:
        """Underlying asset ids"""
        return self.__underlyingAssetIds

    @underlyingAssetIds.setter
    def underlyingAssetIds(self, value: Iterable[str]):
        self.__underlyingAssetIds = value
        self._property_changed('underlyingAssetIds')        


class TemporalXRef(Base):
               
    def __init__(self, startDate: Union[datetime.date, str] = None, endDate: Union[datetime.date, str] = None, identifiers: Union['XRef', str] = None):
        super().__init__()
        self.__startDate = startDate
        self.__endDate = endDate
        self.__identifiers = identifiers

    @property
    def startDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: Union[datetime.date, str]):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def endDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: Union[datetime.date, str]):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def identifiers(self) -> Union['XRef', str]:
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Union['XRef', str]):
        self.__identifiers = value
        self._property_changed('identifiers')        


class TemporalPeople(Base):
        
    """People associated with an asset during a certain date range"""
       
    def __init__(self, startDate: Union[datetime.date, str] = None, endDate: Union[datetime.date, str] = None, people: Union['People', str] = None):
        super().__init__()
        self.__startDate = startDate
        self.__endDate = endDate
        self.__people = people

    @property
    def startDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: Union[datetime.date, str]):
        self.__startDate = value
        self._property_changed('startDate')        

    @property
    def endDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: Union[datetime.date, str]):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def people(self) -> Union['People', str]:
        """People associated with an asset"""
        return self.__people

    @people.setter
    def people(self, value: Union['People', str]):
        self.__people = value
        self._property_changed('people')        


class People(Base):
        
    """People associated with an asset"""
       
    def __init__(self, portfolioManagers: Iterable[str] = None):
        super().__init__()
        self.__portfolioManagers = portfolioManagers

    @property
    def portfolioManagers(self) -> Iterable[str]:
        """Portfolio managers of asset"""
        return self.__portfolioManagers

    @portfolioManagers.setter
    def portfolioManagers(self, value: Iterable[str]):
        self.__portfolioManagers = value
        self._property_changed('portfolioManagers')        


class AssetStats(Base):
        
    """Performance statistics."""
       
    def __init__(self, lastUpdatedTime: datetime.datetime = None, period: Union['AssetStatsPeriod', str] = None, type: Union['AssetStatsType', str] = None, stats: Union['PerformanceStats', str] = None):
        super().__init__()
        self.__lastUpdatedTime = lastUpdatedTime
        self.__period = period
        self.__type = type
        self.__stats = stats

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def period(self) -> Union['AssetStatsPeriod', str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union['AssetStatsPeriod', str]):
        self.__period = value
        self._property_changed('period')        

    @property
    def type(self) -> Union['AssetStatsType', str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union['AssetStatsType', str]):
        self.__type = value
        self._property_changed('type')        

    @property
    def stats(self) -> Union['PerformanceStats', str]:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: Union['PerformanceStats', str]):
        self.__stats = value
        self._property_changed('stats')        


class PerformanceStats(Base):
        
    """Performance statistics."""
       
    def __init__(self, alpha: float = None, annualizedReturn: float = None, annualizedVolatility: float = None, averageReturn: float = None, averageValue: float = None, averageVolumeLastMonth: float = None, bestMonth: float = None, bestMonthDate: datetime.date = None, beta: float = None, closePrice: float = None, correlation: float = None, currentValue: float = None, drawdownOverReturn: float = None, high: float = None, highEod: float = None, lastChange: float = None, lastChangePct: float = None, lastDate: datetime.date = None, lastValue: float = None, low: float = None, lowEod: float = None, maxDrawDown: float = None, maxDrawDownDuration: int = None, openPrice: float = None, positiveMonths: float = None, sharpeRatio: float = None, sortinoRatio: float = None, worstMonth: float = None, worstMonthDate: datetime.date = None, totalReturn: float = None, volume: float = None):
        super().__init__()
        self.__alpha = alpha
        self.__annualizedReturn = annualizedReturn
        self.__annualizedVolatility = annualizedVolatility
        self.__averageReturn = averageReturn
        self.__averageValue = averageValue
        self.__averageVolumeLastMonth = averageVolumeLastMonth
        self.__bestMonth = bestMonth
        self.__bestMonthDate = bestMonthDate
        self.__beta = beta
        self.__closePrice = closePrice
        self.__correlation = correlation
        self.__currentValue = currentValue
        self.__drawdownOverReturn = drawdownOverReturn
        self.__high = high
        self.__highEod = highEod
        self.__lastChange = lastChange
        self.__lastChangePct = lastChangePct
        self.__lastDate = lastDate
        self.__lastValue = lastValue
        self.__low = low
        self.__lowEod = lowEod
        self.__maxDrawDown = maxDrawDown
        self.__maxDrawDownDuration = maxDrawDownDuration
        self.__openPrice = openPrice
        self.__positiveMonths = positiveMonths
        self.__sharpeRatio = sharpeRatio
        self.__sortinoRatio = sortinoRatio
        self.__worstMonth = worstMonth
        self.__worstMonthDate = worstMonthDate
        self.__totalReturn = totalReturn
        self.__volume = volume

    @property
    def alpha(self) -> float:
        """Measure of performance compared to a market benchmark."""
        return self.__alpha

    @alpha.setter
    def alpha(self, value: float):
        self.__alpha = value
        self._property_changed('alpha')        

    @property
    def annualizedReturn(self) -> float:
        """Compounded Annual Growth Rate (CAGR)."""
        return self.__annualizedReturn

    @annualizedReturn.setter
    def annualizedReturn(self, value: float):
        self.__annualizedReturn = value
        self._property_changed('annualizedReturn')        

    @property
    def annualizedVolatility(self) -> float:
        """Standard deviation of daily returns, annualized."""
        return self.__annualizedVolatility

    @annualizedVolatility.setter
    def annualizedVolatility(self, value: float):
        self.__annualizedVolatility = value
        self._property_changed('annualizedVolatility')        

    @property
    def averageReturn(self) -> float:
        """Average of the performance returns."""
        return self.__averageReturn

    @averageReturn.setter
    def averageReturn(self, value: float):
        self.__averageReturn = value
        self._property_changed('averageReturn')        

    @property
    def averageValue(self) -> float:
        """Average value."""
        return self.__averageValue

    @averageValue.setter
    def averageValue(self, value: float):
        self.__averageValue = value
        self._property_changed('averageValue')        

    @property
    def averageVolumeLastMonth(self) -> float:
        """30 day average volume."""
        return self.__averageVolumeLastMonth

    @averageVolumeLastMonth.setter
    def averageVolumeLastMonth(self, value: float):
        self.__averageVolumeLastMonth = value
        self._property_changed('averageVolumeLastMonth')        

    @property
    def bestMonth(self) -> float:
        """Best monthly return (first to last day of month)."""
        return self.__bestMonth

    @bestMonth.setter
    def bestMonth(self, value: float):
        self.__bestMonth = value
        self._property_changed('bestMonth')        

    @property
    def bestMonthDate(self) -> datetime.date:
        """Best monthly return date (first to last day of month)."""
        return self.__bestMonthDate

    @bestMonthDate.setter
    def bestMonthDate(self, value: datetime.date):
        self.__bestMonthDate = value
        self._property_changed('bestMonthDate')        

    @property
    def beta(self) -> float:
        """Measure of volatility compared to a market benchmark."""
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def closePrice(self) -> float:
        """previous close price."""
        return self.__closePrice

    @closePrice.setter
    def closePrice(self, value: float):
        self.__closePrice = value
        self._property_changed('closePrice')        

    @property
    def correlation(self) -> float:
        """Pearson correlation."""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def currentValue(self) -> float:
        """Current value."""
        return self.__currentValue

    @currentValue.setter
    def currentValue(self, value: float):
        self.__currentValue = value
        self._property_changed('currentValue')        

    @property
    def drawdownOverReturn(self) -> float:
        """Maximum drawdown divided by annualized return."""
        return self.__drawdownOverReturn

    @drawdownOverReturn.setter
    def drawdownOverReturn(self, value: float):
        self.__drawdownOverReturn = value
        self._property_changed('drawdownOverReturn')        

    @property
    def high(self) -> float:
        """Highest real time price for the previous 24 hours."""
        return self.__high

    @high.setter
    def high(self, value: float):
        self.__high = value
        self._property_changed('high')        

    @property
    def highEod(self) -> float:
        """Highest end of day price."""
        return self.__highEod

    @highEod.setter
    def highEod(self, value: float):
        self.__highEod = value
        self._property_changed('highEod')        

    @property
    def lastChange(self) -> float:
        """Last published value."""
        return self.__lastChange

    @lastChange.setter
    def lastChange(self, value: float):
        self.__lastChange = value
        self._property_changed('lastChange')        

    @property
    def lastChangePct(self) -> float:
        """Last change in percent."""
        return self.__lastChangePct

    @lastChangePct.setter
    def lastChangePct(self, value: float):
        self.__lastChangePct = value
        self._property_changed('lastChangePct')        

    @property
    def lastDate(self) -> datetime.date:
        """Last publication date."""
        return self.__lastDate

    @lastDate.setter
    def lastDate(self, value: datetime.date):
        self.__lastDate = value
        self._property_changed('lastDate')        

    @property
    def lastValue(self) -> float:
        """Last published value."""
        return self.__lastValue

    @lastValue.setter
    def lastValue(self, value: float):
        self.__lastValue = value
        self._property_changed('lastValue')        

    @property
    def low(self) -> float:
        """Lowest real time price for the previous 24 hours."""
        return self.__low

    @low.setter
    def low(self, value: float):
        self.__low = value
        self._property_changed('low')        

    @property
    def lowEod(self) -> float:
        """Lowest end of day price."""
        return self.__lowEod

    @lowEod.setter
    def lowEod(self, value: float):
        self.__lowEod = value
        self._property_changed('lowEod')        

    @property
    def maxDrawDown(self) -> float:
        """Maximum peak to trough percentage drawdown."""
        return self.__maxDrawDown

    @maxDrawDown.setter
    def maxDrawDown(self, value: float):
        self.__maxDrawDown = value
        self._property_changed('maxDrawDown')        

    @property
    def maxDrawDownDuration(self) -> int:
        """Amount of time in days between beginning and end of drawdown."""
        return self.__maxDrawDownDuration

    @maxDrawDownDuration.setter
    def maxDrawDownDuration(self, value: int):
        self.__maxDrawDownDuration = value
        self._property_changed('maxDrawDownDuration')        

    @property
    def openPrice(self) -> float:
        """Open price."""
        return self.__openPrice

    @openPrice.setter
    def openPrice(self, value: float):
        self.__openPrice = value
        self._property_changed('openPrice')        

    @property
    def positiveMonths(self) -> float:
        """Percentage of months that performed positively."""
        return self.__positiveMonths

    @positiveMonths.setter
    def positiveMonths(self, value: float):
        self.__positiveMonths = value
        self._property_changed('positiveMonths')        

    @property
    def sharpeRatio(self) -> float:
        """Annualized return of the series minus risk free rate (accrued daily) divided by annual volatility."""
        return self.__sharpeRatio

    @sharpeRatio.setter
    def sharpeRatio(self, value: float):
        self.__sharpeRatio = value
        self._property_changed('sharpeRatio')        

    @property
    def sortinoRatio(self) -> float:
        """Annualized return of the series minus risk free rate (accrued daily) divided by annual volatility of negative returns."""
        return self.__sortinoRatio

    @sortinoRatio.setter
    def sortinoRatio(self, value: float):
        self.__sortinoRatio = value
        self._property_changed('sortinoRatio')        

    @property
    def worstMonth(self) -> float:
        """Worst monthly return (first to last day of month)."""
        return self.__worstMonth

    @worstMonth.setter
    def worstMonth(self, value: float):
        self.__worstMonth = value
        self._property_changed('worstMonth')        

    @property
    def worstMonthDate(self) -> datetime.date:
        """Worst monthly return date (first to last day of month)."""
        return self.__worstMonthDate

    @worstMonthDate.setter
    def worstMonthDate(self, value: datetime.date):
        self.__worstMonthDate = value
        self._property_changed('worstMonthDate')        

    @property
    def totalReturn(self) -> float:
        """Total return."""
        return self.__totalReturn

    @totalReturn.setter
    def totalReturn(self, value: float):
        self.__totalReturn = value
        self._property_changed('totalReturn')        

    @property
    def volume(self) -> float:
        """volume."""
        return self.__volume

    @volume.setter
    def volume(self, value: float):
        self.__volume = value
        self._property_changed('volume')        


class ShareClassParameters(Base):
        
    """Attributes specific to share class assets"""
       
    def __init__(self, additionalProvisions: str = None, benchmark: Union['Benchmark', str] = None, earlyRedemptionFee: float = None, gate: float = None, gateType: str = None, hurdle: float = None, hurdleType: str = None, lockup: float = None, lockupType: str = None, managementFee: float = None, minimumSubscription: float = None, name: str = None, performanceFee: float = None, redemptionNoticePeriod: float = None, redemptionPeriod: str = None, sidePocket: str = None, status: str = None, termType: str = None):
        super().__init__()
        self.__additionalProvisions = additionalProvisions
        self.__benchmark = benchmark
        self.__earlyRedemptionFee = earlyRedemptionFee
        self.__gate = gate
        self.__gateType = gateType
        self.__hurdle = hurdle
        self.__hurdleType = hurdleType
        self.__lockup = lockup
        self.__lockupType = lockupType
        self.__managementFee = managementFee
        self.__minimumSubscription = minimumSubscription
        self.__name = name
        self.__performanceFee = performanceFee
        self.__redemptionNoticePeriod = redemptionNoticePeriod
        self.__redemptionPeriod = redemptionPeriod
        self.__sidePocket = sidePocket
        self.__status = status
        self.__termType = termType

    @property
    def additionalProvisions(self) -> str:
        """Additional details that are relevant to the share class that not captured by the other fields"""
        return self.__additionalProvisions

    @additionalProvisions.setter
    def additionalProvisions(self, value: str):
        self.__additionalProvisions = value
        self._property_changed('additionalProvisions')        

    @property
    def benchmark(self) -> Union['Benchmark', str]:
        """Reference rate that can based on an absolute value or absolute value + index"""
        return self.__benchmark

    @benchmark.setter
    def benchmark(self, value: Union['Benchmark', str]):
        self.__benchmark = value
        self._property_changed('benchmark')        

    @property
    def earlyRedemptionFee(self) -> float:
        """Fee an investor pays to redeem before the expiry of a soft lock-up"""
        return self.__earlyRedemptionFee

    @earlyRedemptionFee.setter
    def earlyRedemptionFee(self, value: float):
        self.__earlyRedemptionFee = value
        self._property_changed('earlyRedemptionFee')        

    @property
    def gate(self) -> float:
        """Limit to the amount of capital that can be redeemed from a fund"""
        return self.__gate

    @gate.setter
    def gate(self, value: float):
        self.__gate = value
        self._property_changed('gate')        

    @property
    def gateType(self) -> str:
        """Category that gate relates to"""
        return self.__gateType

    @gateType.setter
    def gateType(self, value: str):
        self.__gateType = value
        self._property_changed('gateType')        

    @property
    def hurdle(self) -> float:
        """Minimum rate of return a fund must generate before it collects a performance fee"""
        return self.__hurdle

    @hurdle.setter
    def hurdle(self, value: float):
        self.__hurdle = value
        self._property_changed('hurdle')        

    @property
    def hurdleType(self) -> str:
        """Determines if the hurdle is calculated on all profits above hurdle rate"""
        return self.__hurdleType

    @hurdleType.setter
    def hurdleType(self, value: str):
        self.__hurdleType = value
        self._property_changed('hurdleType')        

    @property
    def lockup(self) -> float:
        """Number of months an investor is not allowed to redeem investment"""
        return self.__lockup

    @lockup.setter
    def lockup(self, value: float):
        self.__lockup = value
        self._property_changed('lockup')        

    @property
    def lockupType(self) -> str:
        """Classification of lockup"""
        return self.__lockupType

    @lockupType.setter
    def lockupType(self, value: str):
        self.__lockupType = value
        self._property_changed('lockupType')        

    @property
    def managementFee(self) -> float:
        """Percent fee paid by investor to compensate manager for the cost of managing their assets"""
        return self.__managementFee

    @managementFee.setter
    def managementFee(self, value: float):
        self.__managementFee = value
        self._property_changed('managementFee')        

    @property
    def minimumSubscription(self) -> float:
        """Lowest level of investment a fund will accept"""
        return self.__minimumSubscription

    @minimumSubscription.setter
    def minimumSubscription(self, value: float):
        self.__minimumSubscription = value
        self._property_changed('minimumSubscription')        

    @property
    def name(self) -> str:
        """Identifier for particular share class"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def performanceFee(self) -> float:
        """Fee paid by investor to compensate manager for generating positive returns or alpha"""
        return self.__performanceFee

    @performanceFee.setter
    def performanceFee(self, value: float):
        self.__performanceFee = value
        self._property_changed('performanceFee')        

    @property
    def redemptionNoticePeriod(self) -> float:
        """Number of days prior to a redemption that an investor must notify a manager of their intent"""
        return self.__redemptionNoticePeriod

    @redemptionNoticePeriod.setter
    def redemptionNoticePeriod(self, value: float):
        self.__redemptionNoticePeriod = value
        self._property_changed('redemptionNoticePeriod')        

    @property
    def redemptionPeriod(self) -> str:
        """Frequency on which an investor can redeem from a fund"""
        return self.__redemptionPeriod

    @redemptionPeriod.setter
    def redemptionPeriod(self, value: str):
        self.__redemptionPeriod = value
        self._property_changed('redemptionPeriod')        

    @property
    def sidePocket(self) -> str:
        """Account utilized to separate illiquid assets from more liquid investments"""
        return self.__sidePocket

    @sidePocket.setter
    def sidePocket(self, value: str):
        self.__sidePocket = value
        self._property_changed('sidePocket')        

    @property
    def status(self) -> str:
        """Denotes whether the share class is currently accepting new subscriptions"""
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value
        self._property_changed('status')        

    @property
    def termType(self) -> str:
        """category that describes share class offering"""
        return self.__termType

    @termType.setter
    def termType(self, value: str):
        self.__termType = value
        self._property_changed('termType')        


class Benchmark(Base):
        
    """Reference rate that can based on an absolute value or absolute value + index"""
       
    def __init__(self, assetId: Union[str, str] = None, value: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__value = value

    @property
    def assetId(self) -> Union[str, str]:
        """Asset for rate index"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def value(self) -> float:
        """Absolute value for reference rate"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class SecuritiesLendingLoan(Base):
        
    """Parameters specific to a securities lending loan"""
       
    def __init__(self, assetId: Union[str, str], fundId: Union[str, str], lenderId: Union[str, str], borrowerId: Union[str, str], loanStatus: str = None, settlementStatus: str = None, collateralType: str = None, loanCurrency: Union['Currency', str] = None, adjustmentInd: bool = None, countryOfIssue: str = None, inputDate: Union[datetime.date, str] = None, effectiveDate: Union[datetime.date, str] = None, securitySettleDate: Union[datetime.date, str] = None, cashSettleDate: Union[datetime.date, str] = None, termDate: Union[datetime.date, str] = None, returnDate: Union[datetime.date, str] = None):
        super().__init__()
        self.__assetId = assetId
        self.__fundId = fundId
        self.__lenderId = lenderId
        self.__borrowerId = borrowerId
        self.__loanStatus = loanStatus
        self.__settlementStatus = settlementStatus
        self.__collateralType = collateralType
        self.__loanCurrency = loanCurrency
        self.__adjustmentInd = adjustmentInd
        self.__countryOfIssue = countryOfIssue
        self.__inputDate = inputDate
        self.__effectiveDate = effectiveDate
        self.__securitySettleDate = securitySettleDate
        self.__cashSettleDate = cashSettleDate
        self.__termDate = termDate
        self.__returnDate = returnDate

    @property
    def assetId(self) -> Union[str, str]:
        """Id of the security being lent as part of this loan.  This Id should tie to an Asset"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def fundId(self) -> Union[str, str]:
        """Id of the fund from which the loan is booked.  This Id should tie to an Asset"""
        return self.__fundId

    @fundId.setter
    def fundId(self, value: Union[str, str]):
        self.__fundId = value
        self._property_changed('fundId')        

    @property
    def lenderId(self) -> Union[str, str]:
        """Id of the counterpart lending the security.  This Id should tie to a Company"""
        return self.__lenderId

    @lenderId.setter
    def lenderId(self, value: Union[str, str]):
        self.__lenderId = value
        self._property_changed('lenderId')        

    @property
    def borrowerId(self) -> Union[str, str]:
        """Id of the counterpart borrowing the security.  This Id should tie to a Company"""
        return self.__borrowerId

    @borrowerId.setter
    def borrowerId(self, value: Union[str, str]):
        self.__borrowerId = value
        self._property_changed('borrowerId')        

    @property
    def loanStatus(self) -> str:
        """The current state of the loan"""
        return self.__loanStatus

    @loanStatus.setter
    def loanStatus(self, value: str):
        self.__loanStatus = value
        self._property_changed('loanStatus')        

    @property
    def settlementStatus(self) -> str:
        """State of the underlying components of the loan."""
        return self.__settlementStatus

    @settlementStatus.setter
    def settlementStatus(self, value: str):
        self.__settlementStatus = value
        self._property_changed('settlementStatus')        

    @property
    def collateralType(self) -> str:
        """Type of collateral used to collateralize the loan"""
        return self.__collateralType

    @collateralType.setter
    def collateralType(self, value: str):
        self.__collateralType = value
        self._property_changed('collateralType')        

    @property
    def loanCurrency(self) -> Union['Currency', str]:
        """Currency in which the loan value is represented"""
        return self.__loanCurrency

    @loanCurrency.setter
    def loanCurrency(self, value: Union['Currency', str]):
        self.__loanCurrency = value
        self._property_changed('loanCurrency')        

    @property
    def adjustmentInd(self) -> bool:
        """Defines whether or not this contract is for the purpose of a month end loan adjustment."""
        return self.__adjustmentInd

    @adjustmentInd.setter
    def adjustmentInd(self, value: bool):
        self.__adjustmentInd = value
        self._property_changed('adjustmentInd')        

    @property
    def countryOfIssue(self) -> str:
        """The country code (ISO 3166) of the underlying security"""
        return self.__countryOfIssue

    @countryOfIssue.setter
    def countryOfIssue(self, value: str):
        self.__countryOfIssue = value
        self._property_changed('countryOfIssue')        

    @property
    def inputDate(self) -> Union[datetime.date, str]:
        """Date that the loan is booked"""
        return self.__inputDate

    @inputDate.setter
    def inputDate(self, value: Union[datetime.date, str]):
        self.__inputDate = value
        self._property_changed('inputDate')        

    @property
    def effectiveDate(self) -> Union[datetime.date, str]:
        """Date of the trade"""
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value: Union[datetime.date, str]):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def securitySettleDate(self) -> Union[datetime.date, str]:
        """Date that the loaned securities settled"""
        return self.__securitySettleDate

    @securitySettleDate.setter
    def securitySettleDate(self, value: Union[datetime.date, str]):
        self.__securitySettleDate = value
        self._property_changed('securitySettleDate')        

    @property
    def cashSettleDate(self) -> Union[datetime.date, str]:
        """Date of the cash collateral settled"""
        return self.__cashSettleDate

    @cashSettleDate.setter
    def cashSettleDate(self, value: Union[datetime.date, str]):
        self.__cashSettleDate = value
        self._property_changed('cashSettleDate')        

    @property
    def termDate(self) -> Union[datetime.date, str]:
        """Date the dividend is paid for dividend based loans"""
        return self.__termDate

    @termDate.setter
    def termDate(self, value: Union[datetime.date, str]):
        self.__termDate = value
        self._property_changed('termDate')        

    @property
    def returnDate(self) -> Union[datetime.date, str]:
        """Date the loan is returned"""
        return self.__returnDate

    @returnDate.setter
    def returnDate(self, value: Union[datetime.date, str]):
        self.__returnDate = value
        self._property_changed('returnDate')        


class HedgeFundParameters(Base):
        
    """Asset parameters specific to hedge funds"""
       
    def __init__(self, aum: float = None, strategyAum: float = None, aumRange: Union['NumberRange', str] = None, disclaimers: str = None, marketCapCategory: Iterable[str] = None, marketingStatus: str = None, preferences=None, regionalFocus: Iterable[str] = None, riskTakingModel: str = None, strategy: Union['Strategy', str] = None, supraStrategy: Union['SupraStrategy', str] = None, strategyDescription: str = None, targetedGrossExposure: Union['NumberRange', str] = None, targetedNetExposure: Union['NumberRange', str] = None, targetedNumOfPositionsShort: Union['NumberRange', str] = None, targetedNumOfPositionsLong: Union['NumberRange', str] = None, turnover: str = None, vehicleType: str = None, netExposureClassification: Union['NetExposureClassification', str] = None):
        super().__init__()
        self.__aum = aum
        self.__strategyAum = strategyAum
        self.__aumRange = aumRange
        self.__disclaimers = disclaimers
        self.__marketCapCategory = marketCapCategory
        self.__marketingStatus = marketingStatus
        self.__preferences = preferences
        self.__regionalFocus = regionalFocus
        self.__riskTakingModel = riskTakingModel
        self.__strategy = strategy
        self.__supraStrategy = supraStrategy
        self.__strategyDescription = strategyDescription
        self.__targetedGrossExposure = targetedGrossExposure
        self.__targetedNetExposure = targetedNetExposure
        self.__targetedNumOfPositionsShort = targetedNumOfPositionsShort
        self.__targetedNumOfPositionsLong = targetedNumOfPositionsLong
        self.__turnover = turnover
        self.__vehicleType = vehicleType
        self.__netExposureClassification = netExposureClassification

    @property
    def aum(self) -> float:
        """Current assets under management. Only viewable after having been granted additional access to asset information."""
        return self.__aum

    @aum.setter
    def aum(self, value: float):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def strategyAum(self) -> float:
        """Total assets under management for this strategy (including comingled fund, managed accounts, and funds of one). Only viewable after having been granted additional access to asset information."""
        return self.__strategyAum

    @strategyAum.setter
    def strategyAum(self, value: float):
        self.__strategyAum = value
        self._property_changed('strategyAum')        

    @property
    def aumRange(self) -> Union['NumberRange', str]:
        """Range in which assets under management fall. Same view permissions as the asset."""
        return self.__aumRange

    @aumRange.setter
    def aumRange(self, value: Union['NumberRange', str]):
        self.__aumRange = value
        self._property_changed('aumRange')        

    @property
    def disclaimers(self) -> str:
        """Legal disclaimers for performance data. Same view permissions as the asset."""
        return self.__disclaimers

    @disclaimers.setter
    def disclaimers(self, value: str):
        self.__disclaimers = value
        self._property_changed('disclaimers')        

    @property
    def marketCapCategory(self) -> Iterable[str]:
        """Category of market capitalizations a fund is focused on from an investment perspective. Same view permissions as the asset."""
        return self.__marketCapCategory

    @marketCapCategory.setter
    def marketCapCategory(self, value: Iterable[str]):
        self.__marketCapCategory = value
        self._property_changed('marketCapCategory')        

    @property
    def marketingStatus(self) -> str:
        """A fund's posture as to whether it is currently accepting new subscriptions. Same view permissions as the asset."""
        return self.__marketingStatus

    @marketingStatus.setter
    def marketingStatus(self, value: str):
        self.__marketingStatus = value
        self._property_changed('marketingStatus')        

    @property
    def preferences(self):
        """Lists of blacklisted company attributes."""
        return self.__preferences

    @preferences.setter
    def preferences(self, value):
        self.__preferences = value
        self._property_changed('preferences')        

    @property
    def regionalFocus(self) -> Iterable[str]:
        """Section of the world a fund is focused on from an investment perspective. Same view permissions as the asset"""
        return self.__regionalFocus

    @regionalFocus.setter
    def regionalFocus(self, value: Iterable[str]):
        self.__regionalFocus = value
        self._property_changed('regionalFocus')        

    @property
    def riskTakingModel(self) -> str:
        """Number of risk takers a fund has. Same view permissions as the asset"""
        return self.__riskTakingModel

    @riskTakingModel.setter
    def riskTakingModel(self, value: str):
        self.__riskTakingModel = value
        self._property_changed('riskTakingModel')        

    @property
    def strategy(self) -> Union['Strategy', str]:
        """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union['Strategy', str]):
        self.__strategy = value
        self._property_changed('strategy')        

    @property
    def supraStrategy(self) -> Union['SupraStrategy', str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value: Union['SupraStrategy', str]):
        self.__supraStrategy = value
        self._property_changed('supraStrategy')        

    @property
    def strategyDescription(self) -> str:
        """Statement explaining a fund's investment approach. Only viewable after having been granted additional access to asset information."""
        return self.__strategyDescription

    @strategyDescription.setter
    def strategyDescription(self, value: str):
        self.__strategyDescription = value
        self._property_changed('strategyDescription')        

    @property
    def targetedGrossExposure(self) -> Union['NumberRange', str]:
        """Value of a fund's long positions plus short positions, expressed in percentage terms. Only viewable after having been granted additional access to asset information."""
        return self.__targetedGrossExposure

    @targetedGrossExposure.setter
    def targetedGrossExposure(self, value: Union['NumberRange', str]):
        self.__targetedGrossExposure = value
        self._property_changed('targetedGrossExposure')        

    @property
    def targetedNetExposure(self) -> Union['NumberRange', str]:
        """Value of a fund's long positions minus short positions, expressed in percentage terms. Only viewable after having been granted additional access to asset information."""
        return self.__targetedNetExposure

    @targetedNetExposure.setter
    def targetedNetExposure(self, value: Union['NumberRange', str]):
        self.__targetedNetExposure = value
        self._property_changed('targetedNetExposure')        

    @property
    def targetedNumOfPositionsShort(self) -> Union['NumberRange', str]:
        """Range of positions the fund typically holds on the short side of its portfolio. Only viewable after having been granted additional access to asset information."""
        return self.__targetedNumOfPositionsShort

    @targetedNumOfPositionsShort.setter
    def targetedNumOfPositionsShort(self, value: Union['NumberRange', str]):
        self.__targetedNumOfPositionsShort = value
        self._property_changed('targetedNumOfPositionsShort')        

    @property
    def targetedNumOfPositionsLong(self) -> Union['NumberRange', str]:
        """Range of positions the fund typically holds on the long side of its portfolio. Only viewable after having been granted additional access to asset information."""
        return self.__targetedNumOfPositionsLong

    @targetedNumOfPositionsLong.setter
    def targetedNumOfPositionsLong(self, value: Union['NumberRange', str]):
        self.__targetedNumOfPositionsLong = value
        self._property_changed('targetedNumOfPositionsLong')        

    @property
    def turnover(self) -> str:
        """Rate at which a fund replaces its investment holdings. Only viewable after having been granted additional access to asset information."""
        return self.__turnover

    @turnover.setter
    def turnover(self, value: str):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def vehicleType(self) -> str:
        """Type of investment vehicle. Only viewable after having been granted additional access to asset information."""
        return self.__vehicleType

    @vehicleType.setter
    def vehicleType(self, value: str):
        self.__vehicleType = value
        self._property_changed('vehicleType')        

    @property
    def netExposureClassification(self) -> Union['NetExposureClassification', str]:
        """Classification for net exposure of fund."""
        return self.__netExposureClassification

    @netExposureClassification.setter
    def netExposureClassification(self, value: Union['NetExposureClassification', str]):
        self.__netExposureClassification = value
        self._property_changed('netExposureClassification')        


class NumberRange(Base):
        
    """lower and upper bound to define a number range"""
       
    def __init__(self, lowerBound: float = None, upperBound: float = None):
        super().__init__()
        self.__lowerBound = lowerBound
        self.__upperBound = upperBound

    @property
    def lowerBound(self) -> float:
        """value that defines the lower boundary of the range"""
        return self.__lowerBound

    @lowerBound.setter
    def lowerBound(self, value: float):
        self.__lowerBound = value
        self._property_changed('lowerBound')        

    @property
    def upperBound(self) -> float:
        """value that defines the upper boundary of the range"""
        return self.__upperBound

    @upperBound.setter
    def upperBound(self, value: float):
        self.__upperBound = value
        self._property_changed('upperBound')        


class CommodConfigParameters(Base):
        
    """Commodity configuration parameters"""
       
    def __init__(self, infra: str, fieldHistory: Iterable[Any]):
        super().__init__()
        self.__infra = infra
        self.__fieldHistory = fieldHistory

    @property
    def infra(self) -> str:
        return self.__infra

    @infra.setter
    def infra(self, value: str):
        self.__infra = value
        self._property_changed('infra')        

    @property
    def fieldHistory(self) -> Iterable[Any]:
        return self.__fieldHistory

    @fieldHistory.setter
    def fieldHistory(self, value: Iterable[Any]):
        self.__fieldHistory = value
        self._property_changed('fieldHistory')        


class AssetParameters(Base):
        
    """Parameters specific to the asset type"""
       
    def __init__(self, basketType: str = None, constituents: Iterable['IndexConstituent'] = None, style: str = None, indexCalculationType: str = None, indexReturnType: str = None, indexDivisor: float = None, currency: Union['Currency', str] = None, quoteCurrency: Union['Currency', str] = None, indexInitialPrice: float = None, initialPricingDate: Union[datetime.date, str] = None, expirationDate: Union[datetime.date, str] = None, expirationLocation: str = None, optionStyle: str = None, optionType: Union['OptionType', str] = None, settlementDate: Union[datetime.date, str] = None, settlementType: str = None, strikePrice: float = None, putCurrency: Union['Currency', str] = None, putAmount: float = None, automaticExercise: bool = None, callAmount: float = None, callCurrency: Union['Currency', str] = None, exerciseTime: str = None, multiplier: float = None, premiumPaymentDate: Union[datetime.date, str] = None, premium: float = None, premiumCurrency: Union['Currency', str] = None, callable: bool = None, puttable: bool = None, perpetual: bool = None, seniority: str = None, couponType: str = None, index: str = None, indexTerm: str = None, indexMargin: float = None, coupon: float = None, issueDate: Union[datetime.date, str] = None, issuer: str = None, issuerCountryCode: str = None, issuerType: str = None, issueSize: float = None, commoditySector: str = None, pricingLocation: Union['PricingLocation', str] = None, contractMonths: Iterable[str] = None, g10Currency: bool = None, hedgeId: Union[str, str] = None, ultimateTicker: str = None, strategy: Union['Strategy', str] = None, supraStrategy: Union['SupraStrategy', str] = None, exchangeCurrency: Union['Currency', str] = None, region: str = None, deliveryPoint: str = None, pricingIndex: str = None, contractMonth: str = None, loadType: str = None, contractUnit: str = None, indexCreateSource: str = None, indexApprovalIds=None, isPairBasket: bool = None, fixedRateDayCountFraction: Union['DayCountFraction', str] = None, floatingRateDayCountFraction: Union['DayCountFraction', str] = None, payDayCountFraction: Union['DayCountFraction', str] = None, receiveDayCountFraction: Union['DayCountFraction', str] = None, payFrequency: Union[str, str] = None, receiveFrequency: Union[str, str] = None, resettableLeg: Union['PayReceive', str] = None, fxIndex: str = None):
        super().__init__()
        self.__basketType = basketType
        self.__constituents = constituents
        self.__style = style
        self.__indexCalculationType = indexCalculationType
        self.__indexReturnType = indexReturnType
        self.__indexDivisor = indexDivisor
        self.__currency = currency
        self.__quoteCurrency = quoteCurrency
        self.__indexInitialPrice = indexInitialPrice
        self.__initialPricingDate = initialPricingDate
        self.__expirationDate = expirationDate
        self.__expirationLocation = expirationLocation
        self.__optionStyle = optionStyle
        self.__optionType = optionType
        self.__settlementDate = settlementDate
        self.__settlementType = settlementType
        self.__strikePrice = strikePrice
        self.__putCurrency = putCurrency
        self.__putAmount = putAmount
        self.__automaticExercise = automaticExercise
        self.__callAmount = callAmount
        self.__callCurrency = callCurrency
        self.__exerciseTime = exerciseTime
        self.__multiplier = multiplier
        self.__premiumPaymentDate = premiumPaymentDate
        self.__premium = premium
        self.__premiumCurrency = premiumCurrency
        self.__callable = callable
        self.__puttable = puttable
        self.__perpetual = perpetual
        self.__seniority = seniority
        self.__couponType = couponType
        self.__index = index
        self.__indexTerm = indexTerm
        self.__indexMargin = indexMargin
        self.__coupon = coupon
        self.__issueDate = issueDate
        self.__issuer = issuer
        self.__issuerCountryCode = issuerCountryCode
        self.__issuerType = issuerType
        self.__issueSize = issueSize
        self.__commoditySector = commoditySector
        self.__pricingLocation = pricingLocation
        self.__contractMonths = contractMonths
        self.__g10Currency = g10Currency
        self.__hedgeId = hedgeId
        self.__ultimateTicker = ultimateTicker
        self.__strategy = strategy
        self.__supraStrategy = supraStrategy
        self.__exchangeCurrency = exchangeCurrency
        self.__region = region
        self.__deliveryPoint = deliveryPoint
        self.__pricingIndex = pricingIndex
        self.__contractMonth = contractMonth
        self.__loadType = loadType
        self.__contractUnit = contractUnit
        self.__indexCreateSource = indexCreateSource
        self.__indexApprovalIds = indexApprovalIds
        self.__isPairBasket = isPairBasket
        self.__fixedRateDayCountFraction = fixedRateDayCountFraction
        self.__floatingRateDayCountFraction = floatingRateDayCountFraction
        self.__payDayCountFraction = payDayCountFraction
        self.__receiveDayCountFraction = receiveDayCountFraction
        self.__payFrequency = payFrequency
        self.__receiveFrequency = receiveFrequency
        self.__resettableLeg = resettableLeg
        self.__fxIndex = fxIndex

    @property
    def basketType(self) -> str:
        """Type of basket / implementation"""
        return self.__basketType

    @basketType.setter
    def basketType(self, value: str):
        self.__basketType = value
        self._property_changed('basketType')        

    @property
    def constituents(self) -> Iterable['IndexConstituent']:
        """Target basket constituents, e.g. ids, weights"""
        return self.__constituents

    @constituents.setter
    def constituents(self, value: Iterable['IndexConstituent']):
        self.__constituents = value
        self._property_changed('constituents')        

    @property
    def style(self) -> str:
        """Asset style"""
        return self.__style

    @style.setter
    def style(self, value: str):
        self.__style = value
        self._property_changed('style')        

    @property
    def attributionDatasetId(self) -> str:
        """Identifier of dataset which provides performance attribution data"""
        return 'STSATTR'        

    @property
    def indexCalculationType(self) -> str:
        """Determines the index calculation methodology with respect to dividend reinvestment"""
        return self.__indexCalculationType

    @indexCalculationType.setter
    def indexCalculationType(self, value: str):
        self.__indexCalculationType = value
        self._property_changed('indexCalculationType')        

    @property
    def indexReturnType(self) -> str:
        """Determines the return calculation type method with respect to cash accrual / funding"""
        return self.__indexReturnType

    @indexReturnType.setter
    def indexReturnType(self, value: str):
        self.__indexReturnType = value
        self._property_changed('indexReturnType')        

    @property
    def indexDivisor(self) -> float:
        """Divisor to be applied to the overall position set of the index"""
        return self.__indexDivisor

    @indexDivisor.setter
    def indexDivisor(self, value: float):
        self.__indexDivisor = value
        self._property_changed('indexDivisor')        

    @property
    def currency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union['Currency', str]):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def quoteCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__quoteCurrency

    @quoteCurrency.setter
    def quoteCurrency(self, value: Union['Currency', str]):
        self.__quoteCurrency = value
        self._property_changed('quoteCurrency')        

    @property
    def indexInitialPrice(self) -> float:
        """Initial Price for the Index"""
        return self.__indexInitialPrice

    @indexInitialPrice.setter
    def indexInitialPrice(self, value: float):
        self.__indexInitialPrice = value
        self._property_changed('indexInitialPrice')        

    @property
    def initialPricingDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__initialPricingDate

    @initialPricingDate.setter
    def initialPricingDate(self, value: Union[datetime.date, str]):
        self.__initialPricingDate = value
        self._property_changed('initialPricingDate')        

    @property
    def expirationDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value: Union[datetime.date, str]):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def expirationLocation(self) -> str:
        return self.__expirationLocation

    @expirationLocation.setter
    def expirationLocation(self, value: str):
        self.__expirationLocation = value
        self._property_changed('expirationLocation')        

    @property
    def optionStyle(self) -> str:
        return self.__optionStyle

    @optionStyle.setter
    def optionStyle(self, value: str):
        self.__optionStyle = value
        self._property_changed('optionStyle')        

    @property
    def optionType(self) -> Union['OptionType', str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union['OptionType', str]):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def settlementDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__settlementDate

    @settlementDate.setter
    def settlementDate(self, value: Union[datetime.date, str]):
        self.__settlementDate = value
        self._property_changed('settlementDate')        

    @property
    def settlementType(self) -> str:
        return self.__settlementType

    @settlementType.setter
    def settlementType(self, value: str):
        self.__settlementType = value
        self._property_changed('settlementType')        

    @property
    def strikePrice(self) -> float:
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value: float):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def putCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__putCurrency

    @putCurrency.setter
    def putCurrency(self, value: Union['Currency', str]):
        self.__putCurrency = value
        self._property_changed('putCurrency')        

    @property
    def putAmount(self) -> float:
        return self.__putAmount

    @putAmount.setter
    def putAmount(self, value: float):
        self.__putAmount = value
        self._property_changed('putAmount')        

    @property
    def automaticExercise(self) -> bool:
        return self.__automaticExercise

    @automaticExercise.setter
    def automaticExercise(self, value: bool):
        self.__automaticExercise = value
        self._property_changed('automaticExercise')        

    @property
    def callAmount(self) -> float:
        return self.__callAmount

    @callAmount.setter
    def callAmount(self, value: float):
        self.__callAmount = value
        self._property_changed('callAmount')        

    @property
    def callCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__callCurrency

    @callCurrency.setter
    def callCurrency(self, value: Union['Currency', str]):
        self.__callCurrency = value
        self._property_changed('callCurrency')        

    @property
    def exerciseTime(self) -> str:
        """Time at which the asset can be exercised"""
        return self.__exerciseTime

    @exerciseTime.setter
    def exerciseTime(self, value: str):
        self.__exerciseTime = value
        self._property_changed('exerciseTime')        

    @property
    def multiplier(self) -> float:
        """Underlying unit per asset multiplier"""
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: float):
        self.__multiplier = value
        self._property_changed('multiplier')        

    @property
    def premiumPaymentDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__premiumPaymentDate

    @premiumPaymentDate.setter
    def premiumPaymentDate(self, value: Union[datetime.date, str]):
        self.__premiumPaymentDate = value
        self._property_changed('premiumPaymentDate')        

    @property
    def premium(self) -> float:
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self.__premium = value
        self._property_changed('premium')        

    @property
    def premiumCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__premiumCurrency

    @premiumCurrency.setter
    def premiumCurrency(self, value: Union['Currency', str]):
        self.__premiumCurrency = value
        self._property_changed('premiumCurrency')        

    @property
    def callable(self) -> bool:
        """Bond is callable"""
        return self.__callable

    @callable.setter
    def callable(self, value: bool):
        self.__callable = value
        self._property_changed('callable')        

    @property
    def puttable(self) -> bool:
        """Bond is puttable"""
        return self.__puttable

    @puttable.setter
    def puttable(self, value: bool):
        self.__puttable = value
        self._property_changed('puttable')        

    @property
    def perpetual(self) -> bool:
        """Bond is a perpetual"""
        return self.__perpetual

    @perpetual.setter
    def perpetual(self, value: bool):
        self.__perpetual = value
        self._property_changed('perpetual')        

    @property
    def seniority(self) -> str:
        """The seniority of the bond"""
        return self.__seniority

    @seniority.setter
    def seniority(self, value: str):
        self.__seniority = value
        self._property_changed('seniority')        

    @property
    def couponType(self) -> str:
        """The coupon type of the bond"""
        return self.__couponType

    @couponType.setter
    def couponType(self, value: str):
        self.__couponType = value
        self._property_changed('couponType')        

    @property
    def index(self) -> str:
        """The rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__index

    @index.setter
    def index(self, value: str):
        self.__index = value
        self._property_changed('index')        

    @property
    def indexTerm(self) -> str:
        """The term of rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__indexTerm

    @indexTerm.setter
    def indexTerm(self, value: str):
        self.__indexTerm = value
        self._property_changed('indexTerm')        

    @property
    def indexMargin(self) -> float:
        """The spread over the rate index (e.g. USD-LIBOR-BBA) for the floating rate coupon of this bond"""
        return self.__indexMargin

    @indexMargin.setter
    def indexMargin(self, value: float):
        self.__indexMargin = value
        self._property_changed('indexMargin')        

    @property
    def coupon(self) -> float:
        """The fixed coupon for this bond"""
        return self.__coupon

    @coupon.setter
    def coupon(self, value: float):
        self.__coupon = value
        self._property_changed('coupon')        

    @property
    def issueDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__issueDate

    @issueDate.setter
    def issueDate(self, value: Union[datetime.date, str]):
        self.__issueDate = value
        self._property_changed('issueDate')        

    @property
    def issuer(self) -> str:
        """The issuer of this bond"""
        return self.__issuer

    @issuer.setter
    def issuer(self, value: str):
        self.__issuer = value
        self._property_changed('issuer')        

    @property
    def issuerCountryCode(self) -> str:
        """The country code (ISO 3166) in which this bond was issued"""
        return self.__issuerCountryCode

    @issuerCountryCode.setter
    def issuerCountryCode(self, value: str):
        self.__issuerCountryCode = value
        self._property_changed('issuerCountryCode')        

    @property
    def issuerType(self) -> str:
        """The type of the bond issuer"""
        return self.__issuerType

    @issuerType.setter
    def issuerType(self, value: str):
        self.__issuerType = value
        self._property_changed('issuerType')        

    @property
    def issueSize(self) -> float:
        """The notional issue size of the bond"""
        return self.__issueSize

    @issueSize.setter
    def issueSize(self, value: float):
        self.__issueSize = value
        self._property_changed('issueSize')        

    @property
    def commoditySector(self) -> str:
        """The sector of the commodity"""
        return self.__commoditySector

    @commoditySector.setter
    def commoditySector(self, value: str):
        self.__commoditySector = value
        self._property_changed('commoditySector')        

    @property
    def pricingLocation(self) -> Union['PricingLocation', str]:
        """Based on the location of the exchange. Called 'Native Region' in SecDB"""
        return self.__pricingLocation

    @pricingLocation.setter
    def pricingLocation(self, value: Union['PricingLocation', str]):
        self.__pricingLocation = value
        self._property_changed('pricingLocation')        

    @property
    def contractMonths(self) -> Iterable[str]:
        """Contract months"""
        return self.__contractMonths

    @contractMonths.setter
    def contractMonths(self, value: Iterable[str]):
        self.__contractMonths = value
        self._property_changed('contractMonths')        

    @property
    def g10Currency(self) -> bool:
        """Is a G10 asset."""
        return self.__g10Currency

    @g10Currency.setter
    def g10Currency(self, value: bool):
        self.__g10Currency = value
        self._property_changed('g10Currency')        

    @property
    def hedgeId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__hedgeId

    @hedgeId.setter
    def hedgeId(self, value: Union[str, str]):
        self.__hedgeId = value
        self._property_changed('hedgeId')        

    @property
    def ultimateTicker(self) -> str:
        """The ultimate ticker for this security (e.g. SPXW)"""
        return self.__ultimateTicker

    @ultimateTicker.setter
    def ultimateTicker(self, value: str):
        self.__ultimateTicker = value
        self._property_changed('ultimateTicker')        

    @property
    def strategy(self) -> Union['Strategy', str]:
        """More specific descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: Union['Strategy', str]):
        self.__strategy = value
        self._property_changed('strategy')        

    @property
    def supraStrategy(self) -> Union['SupraStrategy', str]:
        """Broad descriptor of a fund's investment approach. Same view permissions as the asset"""
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value: Union['SupraStrategy', str]):
        self.__supraStrategy = value
        self._property_changed('supraStrategy')        

    @property
    def exchangeCurrency(self) -> Union['Currency', str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__exchangeCurrency

    @exchangeCurrency.setter
    def exchangeCurrency(self, value: Union['Currency', str]):
        self.__exchangeCurrency = value
        self._property_changed('exchangeCurrency')        

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str):
        self.__region = value
        self._property_changed('region')        

    @property
    def deliveryPoint(self) -> str:
        return self.__deliveryPoint

    @deliveryPoint.setter
    def deliveryPoint(self, value: str):
        self.__deliveryPoint = value
        self._property_changed('deliveryPoint')        

    @property
    def pricingIndex(self) -> str:
        return self.__pricingIndex

    @pricingIndex.setter
    def pricingIndex(self, value: str):
        self.__pricingIndex = value
        self._property_changed('pricingIndex')        

    @property
    def contractMonth(self) -> str:
        return self.__contractMonth

    @contractMonth.setter
    def contractMonth(self, value: str):
        self.__contractMonth = value
        self._property_changed('contractMonth')        

    @property
    def loadType(self) -> str:
        return self.__loadType

    @loadType.setter
    def loadType(self, value: str):
        self.__loadType = value
        self._property_changed('loadType')        

    @property
    def contractUnit(self) -> str:
        return self.__contractUnit

    @contractUnit.setter
    def contractUnit(self, value: str):
        self.__contractUnit = value
        self._property_changed('contractUnit')        

    @property
    def indexCreateSource(self) -> str:
        """Source of basket create"""
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value: str):
        self.__indexCreateSource = value
        self._property_changed('indexCreateSource')        

    @property
    def indexApprovalIds(self):
        return self.__indexApprovalIds

    @indexApprovalIds.setter
    def indexApprovalIds(self, value):
        self.__indexApprovalIds = value
        self._property_changed('indexApprovalIds')        

    @property
    def isPairBasket(self) -> bool:
        return self.__isPairBasket

    @isPairBasket.setter
    def isPairBasket(self, value: bool):
        self.__isPairBasket = value
        self._property_changed('isPairBasket')        

    @property
    def fixedRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Default day count fraction for fixed legs"""
        return self.__fixedRateDayCountFraction

    @fixedRateDayCountFraction.setter
    def fixedRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__fixedRateDayCountFraction = value
        self._property_changed('fixedRateDayCountFraction')        

    @property
    def floatingRateDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Default day count fraction for floating legs"""
        return self.__floatingRateDayCountFraction

    @floatingRateDayCountFraction.setter
    def floatingRateDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__floatingRateDayCountFraction = value
        self._property_changed('floatingRateDayCountFraction')        

    @property
    def payDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Default day count fraction for pay leg"""
        return self.__payDayCountFraction

    @payDayCountFraction.setter
    def payDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__payDayCountFraction = value
        self._property_changed('payDayCountFraction')        

    @property
    def receiveDayCountFraction(self) -> Union['DayCountFraction', str]:
        """Default day count fraction for the receive leg"""
        return self.__receiveDayCountFraction

    @receiveDayCountFraction.setter
    def receiveDayCountFraction(self, value: Union['DayCountFraction', str]):
        self.__receiveDayCountFraction = value
        self._property_changed('receiveDayCountFraction')        

    @property
    def payFrequency(self) -> Union[str, str]:
        """Default frequency of the pay leg"""
        return self.__payFrequency

    @payFrequency.setter
    def payFrequency(self, value: Union[str, str]):
        self.__payFrequency = value
        self._property_changed('payFrequency')        

    @property
    def receiveFrequency(self) -> Union[str, str]:
        """Default frequency of the receive leg"""
        return self.__receiveFrequency

    @receiveFrequency.setter
    def receiveFrequency(self, value: Union[str, str]):
        self.__receiveFrequency = value
        self._property_changed('receiveFrequency')        

    @property
    def resettableLeg(self) -> Union['PayReceive', str]:
        """Resettable leg"""
        return self.__resettableLeg

    @resettableLeg.setter
    def resettableLeg(self, value: Union['PayReceive', str]):
        self.__resettableLeg = value
        self._property_changed('resettableLeg')        

    @property
    def fxIndex(self) -> str:
        """FX index"""
        return self.__fxIndex

    @fxIndex.setter
    def fxIndex(self, value: str):
        self.__fxIndex = value
        self._property_changed('fxIndex')        


class IndexConstituent(Base):
               
    def __init__(self, assetId: Union[str, str] = None, weight: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__weight = weight

    @property
    def assetId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def weight(self) -> float:
        """Target asset weight"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value
        self._property_changed('weight')        


class Identifier(Base):
               
    def __init__(self, type: str = None, value: str = None):
        super().__init__()
        self.__type = type
        self.__value = value

    @property
    def type(self) -> str:
        """Identifier type code"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def value(self) -> str:
        """Identifier value"""
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value
        self._property_changed('value')        


class Domains(Base):
        
    """Application specific domain information"""
       
    def __init__(self, simon: Union['SimonDomain', str] = None, simonIntl: Union['SimonDomain', str] = None, sts: Union['StsDomain', str] = None, data: Union['DataDomain', str] = None, compliance: Union['ComplianceDomain', str] = None, compl: Union['ComplDomain', str] = None, gir: Union['GIRDomain', str] = None, social: Union['SocialDomain', str] = None):
        super().__init__()
        self.__simon = simon
        self.__simonIntl = simonIntl
        self.__sts = sts
        self.__data = data
        self.__compliance = compliance
        self.__compl = compl
        self.__gir = gir
        self.__social = social

    @property
    def simon(self) -> Union['SimonDomain', str]:
        return self.__simon

    @simon.setter
    def simon(self, value: Union['SimonDomain', str]):
        self.__simon = value
        self._property_changed('simon')        

    @property
    def simonIntl(self) -> Union['SimonDomain', str]:
        return self.__simonIntl

    @simonIntl.setter
    def simonIntl(self, value: Union['SimonDomain', str]):
        self.__simonIntl = value
        self._property_changed('simonIntl')        

    @property
    def sts(self) -> Union['StsDomain', str]:
        return self.__sts

    @sts.setter
    def sts(self, value: Union['StsDomain', str]):
        self.__sts = value
        self._property_changed('sts')        

    @property
    def data(self) -> Union['DataDomain', str]:
        return self.__data

    @data.setter
    def data(self, value: Union['DataDomain', str]):
        self.__data = value
        self._property_changed('data')        

    @property
    def compliance(self) -> Union['ComplianceDomain', str]:
        return self.__compliance

    @compliance.setter
    def compliance(self, value: Union['ComplianceDomain', str]):
        self.__compliance = value
        self._property_changed('compliance')        

    @property
    def compl(self) -> Union['ComplDomain', str]:
        return self.__compl

    @compl.setter
    def compl(self, value: Union['ComplDomain', str]):
        self.__compl = value
        self._property_changed('compl')        

    @property
    def gir(self) -> Union['GIRDomain', str]:
        return self.__gir

    @gir.setter
    def gir(self, value: Union['GIRDomain', str]):
        self.__gir = value
        self._property_changed('gir')        

    @property
    def social(self) -> Union['SocialDomain', str]:
        return self.__social

    @social.setter
    def social(self, value: Union['SocialDomain', str]):
        self.__social = value
        self._property_changed('social')        


class SocialDomain(Base):
               
    def __init__(self, onboarded):
        super().__init__()
        self.__onboarded = onboarded

    @property
    def onboarded(self):
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value):
        self.__onboarded = value
        self._property_changed('onboarded')        


class ComplDomain(Base):
               
    def __init__(self, rtlRestrictions: Iterable['RTL'] = None, lastUpdatedTime: datetime.datetime = None, lastUpdatedById: Union[str, str] = None):
        super().__init__()
        self.__rtlRestrictions = rtlRestrictions
        self.__lastUpdatedTime = lastUpdatedTime
        self.__lastUpdatedById = lastUpdatedById

    @property
    def rtlRestrictions(self) -> Iterable['RTL']:
        """List of RTL restrictions for the asset"""
        return self.__rtlRestrictions

    @rtlRestrictions.setter
    def rtlRestrictions(self, value: Iterable['RTL']):
        self.__rtlRestrictions = value
        self._property_changed('rtlRestrictions')        

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def lastUpdatedById(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value: Union[str, str]):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        


class RTL(Base):
               
    def __init__(self, restrictionType: str = None, effectiveTime: datetime.datetime = None, deactivationTime: datetime.datetime = None, updateTime: datetime.datetime = None, restrictionId: float = None, restrictionCode: str = None):
        super().__init__()
        self.__restrictionType = restrictionType
        self.__effectiveTime = effectiveTime
        self.__deactivationTime = deactivationTime
        self.__updateTime = updateTime
        self.__restrictionId = restrictionId
        self.__restrictionCode = restrictionCode

    @property
    def restrictionType(self) -> str:
        """Internal compliance restriction type"""
        return self.__restrictionType

    @restrictionType.setter
    def restrictionType(self, value: str):
        self.__restrictionType = value
        self._property_changed('restrictionType')        

    @property
    def effectiveTime(self) -> datetime.datetime:
        """Time the RTL became effective"""
        return self.__effectiveTime

    @effectiveTime.setter
    def effectiveTime(self, value: datetime.datetime):
        self.__effectiveTime = value
        self._property_changed('effectiveTime')        

    @property
    def deactivationTime(self) -> datetime.datetime:
        return self.__deactivationTime

    @deactivationTime.setter
    def deactivationTime(self, value: datetime.datetime):
        self.__deactivationTime = value
        self._property_changed('deactivationTime')        

    @property
    def updateTime(self) -> datetime.datetime:
        """Time the RTL was updated"""
        return self.__updateTime

    @updateTime.setter
    def updateTime(self, value: datetime.datetime):
        self.__updateTime = value
        self._property_changed('updateTime')        

    @property
    def restrictionId(self) -> float:
        """Internal compliance ID"""
        return self.__restrictionId

    @restrictionId.setter
    def restrictionId(self, value: float):
        self.__restrictionId = value
        self._property_changed('restrictionId')        

    @property
    def restrictionCode(self) -> str:
        """Internal compliance restriction code"""
        return self.__restrictionCode

    @restrictionCode.setter
    def restrictionCode(self, value: str):
        self.__restrictionCode = value
        self._property_changed('restrictionCode')        


class ComplianceDomain(Base):
               
    def __init__(self, restrictedStatus: str = None, effectiveTime: datetime.datetime = None):
        super().__init__()
        self.__restrictedStatus = restrictedStatus
        self.__effectiveTime = effectiveTime

    @property
    def restrictedStatus(self) -> str:
        return self.__restrictedStatus

    @restrictedStatus.setter
    def restrictedStatus(self, value: str):
        self.__restrictedStatus = value
        self._property_changed('restrictedStatus')        

    @property
    def effectiveTime(self) -> datetime.datetime:
        """Time that the compliance status became effective"""
        return self.__effectiveTime

    @effectiveTime.setter
    def effectiveTime(self, value: datetime.datetime):
        self.__effectiveTime = value
        self._property_changed('effectiveTime')        


class DataDomain(Base):
               
    def __init__(self, arcticSymbols=None):
        super().__init__()
        self.__arcticSymbols = arcticSymbols

    @property
    def arcticSymbols(self):
        """Mapping of data set IDs to the symbol of this asset's data in that data set"""
        return self.__arcticSymbols

    @arcticSymbols.setter
    def arcticSymbols(self, value):
        self.__arcticSymbols = value
        self._property_changed('arcticSymbols')        


class StsDomain(Base):
               
    def __init__(self, documentIds: Iterable[str] = None, aggregations=None, defaultAggregator: str = None):
        super().__init__()
        self.__documentIds = documentIds
        self.__aggregations = aggregations
        self.__defaultAggregator = defaultAggregator

    @property
    def documentIds(self) -> Iterable[str]:
        """Documents related to this asset"""
        return self.__documentIds

    @documentIds.setter
    def documentIds(self, value: Iterable[str]):
        self.__documentIds = value
        self._property_changed('documentIds')        

    @property
    def aggregations(self):
        return self.__aggregations

    @aggregations.setter
    def aggregations(self, value):
        self.__aggregations = value
        self._property_changed('aggregations')        

    @property
    def defaultAggregator(self) -> str:
        return self.__defaultAggregator

    @defaultAggregator.setter
    def defaultAggregator(self, value: str):
        self.__defaultAggregator = value
        self._property_changed('defaultAggregator')        


class SimonDomain(Base):
               
    def __init__(self, assetTags: Iterable[str] = None, pricingParamEnabled: float = None):
        super().__init__()
        self.__assetTags = assetTags
        self.__pricingParamEnabled = pricingParamEnabled

    @property
    def assetTags(self) -> Iterable[str]:
        """Tags to determine how the asset can be traded"""
        return self.__assetTags

    @assetTags.setter
    def assetTags(self, value: Iterable[str]):
        self.__assetTags = value
        self._property_changed('assetTags')        

    @property
    def pricingParamEnabled(self) -> float:
        """Is parameterized pricing enabled for this asset"""
        return self.__pricingParamEnabled

    @pricingParamEnabled.setter
    def pricingParamEnabled(self, value: float):
        self.__pricingParamEnabled = value
        self._property_changed('pricingParamEnabled')        


class AssetClassifications(Base):
               
    def __init__(self, countryName: str = None, countryCode: str = None, isPrimary: bool = None, gicsSector: str = None, gicsIndustryGroup: str = None, gicsIndustry: str = None, gicsSubIndustry: str = None, commodTemplate: str = None):
        super().__init__()
        self.__countryName = countryName
        self.__countryCode = countryCode
        self.__isPrimary = isPrimary
        self.__gicsSector = gicsSector
        self.__gicsIndustryGroup = gicsIndustryGroup
        self.__gicsIndustry = gicsIndustry
        self.__gicsSubIndustry = gicsSubIndustry
        self.__commodTemplate = commodTemplate

    @property
    def countryName(self) -> str:
        """Country name of asset"""
        return self.__countryName

    @countryName.setter
    def countryName(self, value: str):
        self.__countryName = value
        self._property_changed('countryName')        

    @property
    def countryCode(self) -> str:
        """Country code (ISO 3166)"""
        return self.__countryCode

    @countryCode.setter
    def countryCode(self, value: str):
        self.__countryCode = value
        self._property_changed('countryCode')        

    @property
    def isPrimary(self) -> bool:
        """Is this the primary exchange listing for the asset"""
        return self.__isPrimary

    @isPrimary.setter
    def isPrimary(self, value: bool):
        self.__isPrimary = value
        self._property_changed('isPrimary')        

    @property
    def gicsSector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gicsSector

    @gicsSector.setter
    def gicsSector(self, value: str):
        self.__gicsSector = value
        self._property_changed('gicsSector')        

    @property
    def gicsIndustryGroup(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gicsIndustryGroup

    @gicsIndustryGroup.setter
    def gicsIndustryGroup(self, value: str):
        self.__gicsIndustryGroup = value
        self._property_changed('gicsIndustryGroup')        

    @property
    def gicsIndustry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gicsIndustry

    @gicsIndustry.setter
    def gicsIndustry(self, value: str):
        self.__gicsIndustry = value
        self._property_changed('gicsIndustry')        

    @property
    def gicsSubIndustry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gicsSubIndustry

    @gicsSubIndustry.setter
    def gicsSubIndustry(self, value: str):
        self.__gicsSubIndustry = value
        self._property_changed('gicsSubIndustry')        

    @property
    def commodTemplate(self) -> str:
        """Commodities generic template, i.e. Heating Oil"""
        return self.__commodTemplate

    @commodTemplate.setter
    def commodTemplate(self, value: str):
        self.__commodTemplate = value
        self._property_changed('commodTemplate')        


class EntityQuery(Base):
               
    def __init__(self, format: Union['Format', str] = None, where: Union['FieldFilterMap', str] = None, asOfTime: Union[datetime.datetime, str] = None, date: Union[datetime.date, str] = None, time: Union[datetime.datetime, str] = None, delay: int = None, orderBy: Iterable['OrderBy'] = None, scroll: str = None, scrollId: str = None, fields: Iterable['Selector'] = None, limit: int = None, offset: int = None):
        super().__init__()
        self.__format = format
        self.__where = where
        self.__asOfTime = asOfTime
        self.__date = date
        self.__time = time
        self.__delay = delay
        self.__orderBy = orderBy
        self.__scroll = scroll
        self.__scrollId = scrollId
        self.__fields = fields
        self.__limit = limit
        self.__offset = offset

    @property
    def format(self) -> Union['Format', str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union['Format', str]):
        self.__format = value
        self._property_changed('format')        

    @property
    def where(self) -> Union['FieldFilterMap', str]:
        return self.__where

    @where.setter
    def where(self, value: Union['FieldFilterMap', str]):
        self.__where = value
        self._property_changed('where')        

    @property
    def asOfTime(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__asOfTime

    @asOfTime.setter
    def asOfTime(self, value: Union[datetime.datetime, str]):
        self.__asOfTime = value
        self._property_changed('asOfTime')        

    @property
    def date(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: Union[datetime.date, str]):
        self.__date = value
        self._property_changed('date')        

    @property
    def time(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__time

    @time.setter
    def time(self, value: Union[datetime.datetime, str]):
        self.__time = value
        self._property_changed('time')        

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self.__delay = value
        self._property_changed('delay')        

    @property
    def orderBy(self) -> Iterable['OrderBy']:
        return self.__orderBy

    @orderBy.setter
    def orderBy(self, value: Iterable['OrderBy']):
        self.__orderBy = value
        self._property_changed('orderBy')        

    @property
    def scroll(self) -> str:
        """Time for which to keep the scroll search context alive, i.e. 1m (1 minute) or 10s (10 seconds)"""
        return self.__scroll

    @scroll.setter
    def scroll(self, value: str):
        self.__scroll = value
        self._property_changed('scroll')        

    @property
    def scrollId(self) -> str:
        """Scroll identifier to be used to retrieve the next batch of results"""
        return self.__scrollId

    @scrollId.setter
    def scrollId(self, value: str):
        self.__scrollId = value
        self._property_changed('scrollId')        

    @property
    def fields(self) -> Iterable['Selector']:
        return self.__fields

    @fields.setter
    def fields(self, value: Iterable['Selector']):
        self.__fields = value
        self._property_changed('fields')        

    @property
    def limit(self) -> int:
        """Limit on the number of objects to be returned in the response. Can range between 1 and 10000"""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self.__limit = value
        self._property_changed('limit')        

    @property
    def offset(self) -> int:
        """The offset of the first result returned (default 0). Can be used in pagination to defined the first item in the list to be returned, for example if you request 100 objects, to query the next page you would specify offset = 100."""
        return self.__offset

    @offset.setter
    def offset(self, value: int):
        self.__offset = value
        self._property_changed('offset')        


class AssetStatsRequest(Base):
        
    """Performance statistics."""
       
    def __init__(self, lastUpdatedTime: datetime.datetime = None, period: Union['AssetStatsPeriod', str] = None, type: Union['AssetStatsType', str] = None, stats: Union['PerformanceStatsRequest', str] = None):
        super().__init__()
        self.__lastUpdatedTime = lastUpdatedTime
        self.__period = period
        self.__type = type
        self.__stats = stats

    @property
    def lastUpdatedTime(self) -> datetime.datetime:
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value: datetime.datetime):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def period(self) -> Union['AssetStatsPeriod', str]:
        """The period used to produce date range."""
        return self.__period

    @period.setter
    def period(self, value: Union['AssetStatsPeriod', str]):
        self.__period = value
        self._property_changed('period')        

    @property
    def type(self) -> Union['AssetStatsType', str]:
        """Is it rolling, none etc."""
        return self.__type

    @type.setter
    def type(self, value: Union['AssetStatsType', str]):
        self.__type = value
        self._property_changed('type')        

    @property
    def stats(self) -> Union['PerformanceStatsRequest', str]:
        """Performance statistics."""
        return self.__stats

    @stats.setter
    def stats(self, value: Union['PerformanceStatsRequest', str]):
        self.__stats = value
        self._property_changed('stats')        


class PerformanceStatsRequest(Base):
        
    """Performance statistics."""
       
    def __init__(self, annualizedReturn: Union['Op', str] = None, annualizedVolatility: Union['Op', str] = None, bestMonth: Union['Op', str] = None, maxDrawDown: Union['Op', str] = None, maxDrawDownDuration: Union['Op', str] = None, positiveMonths: Union['Op', str] = None, sharpeRatio: Union['Op', str] = None, sortinoRatio: Union['Op', str] = None, worstMonth: Union['Op', str] = None, averageReturn: Union['Op', str] = None):
        super().__init__()
        self.__annualizedReturn = annualizedReturn
        self.__annualizedVolatility = annualizedVolatility
        self.__bestMonth = bestMonth
        self.__maxDrawDown = maxDrawDown
        self.__maxDrawDownDuration = maxDrawDownDuration
        self.__positiveMonths = positiveMonths
        self.__sharpeRatio = sharpeRatio
        self.__sortinoRatio = sortinoRatio
        self.__worstMonth = worstMonth
        self.__averageReturn = averageReturn

    @property
    def annualizedReturn(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__annualizedReturn

    @annualizedReturn.setter
    def annualizedReturn(self, value: Union['Op', str]):
        self.__annualizedReturn = value
        self._property_changed('annualizedReturn')        

    @property
    def annualizedVolatility(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__annualizedVolatility

    @annualizedVolatility.setter
    def annualizedVolatility(self, value: Union['Op', str]):
        self.__annualizedVolatility = value
        self._property_changed('annualizedVolatility')        

    @property
    def bestMonth(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__bestMonth

    @bestMonth.setter
    def bestMonth(self, value: Union['Op', str]):
        self.__bestMonth = value
        self._property_changed('bestMonth')        

    @property
    def maxDrawDown(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__maxDrawDown

    @maxDrawDown.setter
    def maxDrawDown(self, value: Union['Op', str]):
        self.__maxDrawDown = value
        self._property_changed('maxDrawDown')        

    @property
    def maxDrawDownDuration(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__maxDrawDownDuration

    @maxDrawDownDuration.setter
    def maxDrawDownDuration(self, value: Union['Op', str]):
        self.__maxDrawDownDuration = value
        self._property_changed('maxDrawDownDuration')        

    @property
    def positiveMonths(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__positiveMonths

    @positiveMonths.setter
    def positiveMonths(self, value: Union['Op', str]):
        self.__positiveMonths = value
        self._property_changed('positiveMonths')        

    @property
    def sharpeRatio(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__sharpeRatio

    @sharpeRatio.setter
    def sharpeRatio(self, value: Union['Op', str]):
        self.__sharpeRatio = value
        self._property_changed('sharpeRatio')        

    @property
    def sortinoRatio(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__sortinoRatio

    @sortinoRatio.setter
    def sortinoRatio(self, value: Union['Op', str]):
        self.__sortinoRatio = value
        self._property_changed('sortinoRatio')        

    @property
    def worstMonth(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__worstMonth

    @worstMonth.setter
    def worstMonth(self, value: Union['Op', str]):
        self.__worstMonth = value
        self._property_changed('worstMonth')        

    @property
    def averageReturn(self) -> Union['Op', str]:
        """Operations for searches."""
        return self.__averageReturn

    @averageReturn.setter
    def averageReturn(self, value: Union['Op', str]):
        self.__averageReturn = value
        self._property_changed('averageReturn')        


class Op(Base):
        
    """Operations for searches."""
       
    def __init__(self, gte=None, lte=None, lt=None, gt=None):
        super().__init__()
        self.__gte = gte
        self.__lte = lte
        self.__lt = lt
        self.__gt = gt

    @property
    def gte(self):
        """search for values greater than or equal."""
        return self.__gte

    @gte.setter
    def gte(self, value):
        self.__gte = value
        self._property_changed('gte')        

    @property
    def lte(self):
        """search for values less than or equal to."""
        return self.__lte

    @lte.setter
    def lte(self, value):
        self.__lte = value
        self._property_changed('lte')        

    @property
    def lt(self):
        """search for values less than."""
        return self.__lt

    @lt.setter
    def lt(self, value):
        self.__lt = value
        self._property_changed('lt')        

    @property
    def gt(self):
        """search for values greater than."""
        return self.__gt

    @gt.setter
    def gt(self, value):
        self.__gt = value
        self._property_changed('gt')        


class PositionSet(Base):
               
    def __init__(self, positionDate: Union[datetime.date, str] = None, lastUpdateTime: Union[datetime.datetime, str] = None, positions=None, type: str = None, divisor: float = None):
        super().__init__()
        self.__positionDate = positionDate
        self.__lastUpdateTime = lastUpdateTime
        self.__positions = positions
        self.__type = type
        self.__divisor = divisor

    @property
    def positionDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__positionDate

    @positionDate.setter
    def positionDate(self, value: Union[datetime.date, str]):
        self.__positionDate = value
        self._property_changed('positionDate')        

    @property
    def lastUpdateTime(self) -> Union[datetime.datetime, str]:
        """ISO 8601-formatted timestamp"""
        return self.__lastUpdateTime

    @lastUpdateTime.setter
    def lastUpdateTime(self, value: Union[datetime.datetime, str]):
        self.__lastUpdateTime = value
        self._property_changed('lastUpdateTime')        

    @property
    def positions(self):
        """Array of quantity position objects."""
        return self.__positions

    @positions.setter
    def positions(self, value):
        self.__positions = value
        self._property_changed('positions')        

    @property
    def type(self) -> str:
        """The composition type of a Portfolio"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
        self._property_changed('type')        

    @property
    def divisor(self) -> float:
        """optional index divisor for a position set"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: float):
        self.__divisor = value
        self._property_changed('divisor')        


class DateRange(Base):
               
    def __init__(self, endDate: Union[datetime.date, str] = None, startDate: Union[datetime.date, str] = None):
        super().__init__()
        self.__endDate = endDate
        self.__startDate = startDate

    @property
    def endDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__endDate

    @endDate.setter
    def endDate(self, value: Union[datetime.date, str]):
        self.__endDate = value
        self._property_changed('endDate')        

    @property
    def startDate(self) -> Union[datetime.date, str]:
        """ISO 8601-formatted date"""
        return self.__startDate

    @startDate.setter
    def startDate(self, value: Union[datetime.date, str]):
        self.__startDate = value
        self._property_changed('startDate')        


class AssetComplDomainMap(Base):
               
    def __init__(self, assetId: Union[str, str] = None, complDomain: Union['ComplDomain', str] = None):
        super().__init__()
        self.__assetId = assetId
        self.__complDomain = complDomain

    @property
    def assetId(self) -> Union[str, str]:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def complDomain(self) -> Union['ComplDomain', str]:
        return self.__complDomain

    @complDomain.setter
    def complDomain(self, value: Union['ComplDomain', str]):
        self.__complDomain = value
        self._property_changed('complDomain')        
