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


class BusinessDayConvention(EnumBase, Enum):    
    
    """Business Day Convention."""

    Following = 'Following'
    Modified_Following = 'Modified Following'
    Previous = 'Previous'
    Unadjusted = 'Unadjusted'
    
    def __repr__(self):
        return self.value


class DayCountFraction(EnumBase, Enum):    
    
    """Day Count Fraction."""

    ACT_OVER_360 = 'ACT/360'
    ACT_OVER_365_Fixed = 'ACT/365 Fixed'
    ACT_OVER_365_ISDA = 'ACT/365 ISDA'
    ACT_OVER_ACT_ISDA = 'ACT/ACT ISDA'
    _30_OVER_360 = '30/360'
    _30E_OVER_360 = '30E/360'
    
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


class PayReceive(EnumBase, Enum):    
    
    """Pay or receive fixed"""

    Pay = 'Pay'
    Receive = 'Receive'
    
    def __repr__(self):
        return self.value


class OptionType(EnumBase, Enum):    
    
    Call = 'Call'
    Put = 'Put'
    
    def __repr__(self):
        return self.value


class OptionStyle(EnumBase, Enum):    
    
    """Option Style"""

    European = 'European'
    American = 'American'
    Bermudan = 'Bermudan'
    
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
    cid = 'cid'
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
    gsn = 'gsn'
    isAggressive = 'isAggressive'
    orderId = 'orderId'
    gss = 'gss'
    percentOfMediandv1m = 'percentOfMediandv1m'
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
    objective = 'objective'
    navPrice = 'navPrice'
    ideaActivityType = 'ideaActivityType'
    precipitation = 'precipitation'
    ideaSource = 'ideaSource'
    hedgeNotional = 'hedgeNotional'
    askLow = 'askLow'
    unadjustedAsk = 'unadjustedAsk'
    expiry = 'expiry'
    tradingPnl = 'tradingPnl'
    strikePercentage = 'strikePercentage'
    excessReturnPrice = 'excessReturnPrice'
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
    sourceOriginalCategory = 'sourceOriginalCategory'
    betaAdjustedExposure = 'betaAdjustedExposure'
    latestExecutionTime = 'latestExecutionTime'
    dividendPoints = 'dividendPoints'
    newIdeasWtd = 'newIdeasWtd'
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
    tradeSize = 'tradeSize'
    symbolDimensions = 'symbolDimensions'
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


class XRef(Base):
               
    def __init__(self, ric: str = None, rcic: str = None, eid: str = None, gsideid: str = None, gsid: str = None, cid: str = None, bbid: str = None, bcid: str = None, bbidEquivalent: str = None, cusip: str = None, gss: str = None, isin: str = None, jsn: str = None, primeId: str = None, sedol: str = None, ticker: str = None, valoren: str = None, wpk: str = None, gsn: str = None, secName: str = None, cross: str = None, simonId: str = None, emId: str = None, cmId: str = None, lmsId: str = None, mdapi: str = None, mic: str = None, sfId: str = None):
        super().__init__()
        self.__ric = ric
        self.__rcic = rcic
        self.__eid = eid
        self.__gsideid = gsideid
        self.__gsid = gsid
        self.__cid = cid
        self.__bbid = bbid
        self.__bcid = bcid
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
        self.__cid = kwargs.get('cid')
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
        self.__gsn = kwargs.get('gsn')
        self.__isAggressive = kwargs.get('isAggressive')
        self.__orderId = kwargs.get('orderId')
        self.__gss = kwargs.get('gss')
        self.__percentOfMediandv1m = kwargs.get('percentOfMediandv1m')
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
        self.__objective = kwargs.get('objective')
        self.__navPrice = kwargs.get('navPrice')
        self.__ideaActivityType = kwargs.get('ideaActivityType')
        self.__precipitation = kwargs.get('precipitation')
        self.__ideaSource = kwargs.get('ideaSource')
        self.__hedgeNotional = kwargs.get('hedgeNotional')
        self.__askLow = kwargs.get('askLow')
        self.__unadjustedAsk = kwargs.get('unadjustedAsk')
        self.__expiry = kwargs.get('expiry')
        self.__tradingPnl = kwargs.get('tradingPnl')
        self.__strikePercentage = kwargs.get('strikePercentage')
        self.__excessReturnPrice = kwargs.get('excessReturnPrice')
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
        self.__sourceOriginalCategory = kwargs.get('sourceOriginalCategory')
        self.__betaAdjustedExposure = kwargs.get('betaAdjustedExposure')
        self.__latestExecutionTime = kwargs.get('latestExecutionTime')
        self.__dividendPoints = kwargs.get('dividendPoints')
        self.__newIdeasWtd = kwargs.get('newIdeasWtd')
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
        self.__tradeSize = kwargs.get('tradeSize')
        self.__symbolDimensions = kwargs.get('symbolDimensions')
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
    def marketPnl(self):
        return self.__marketPnl

    @marketPnl.setter
    def marketPnl(self, value):
        self.__marketPnl = value
        self._property_changed('marketPnl')        

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value
        self._property_changed('year')        

    @property
    def sustainAsiaExJapan(self):
        return self.__sustainAsiaExJapan

    @sustainAsiaExJapan.setter
    def sustainAsiaExJapan(self, value):
        self.__sustainAsiaExJapan = value
        self._property_changed('sustainAsiaExJapan')        

    @property
    def investmentRate(self):
        return self.__investmentRate

    @investmentRate.setter
    def investmentRate(self, value):
        self.__investmentRate = value
        self._property_changed('investmentRate')        

    @property
    def assetClassificationsGicsSubIndustry(self):
        return self.__assetClassificationsGicsSubIndustry

    @assetClassificationsGicsSubIndustry.setter
    def assetClassificationsGicsSubIndustry(self, value):
        self.__assetClassificationsGicsSubIndustry = value
        self._property_changed('assetClassificationsGicsSubIndustry')        

    @property
    def bidUnadjusted(self):
        return self.__bidUnadjusted

    @bidUnadjusted.setter
    def bidUnadjusted(self, value):
        self.__bidUnadjusted = value
        self._property_changed('bidUnadjusted')        

    @property
    def economicTermsHash(self):
        return self.__economicTermsHash

    @economicTermsHash.setter
    def economicTermsHash(self, value):
        self.__economicTermsHash = value
        self._property_changed('economicTermsHash')        

    @property
    def neighbourAssetId(self):
        return self.__neighbourAssetId

    @neighbourAssetId.setter
    def neighbourAssetId(self, value):
        self.__neighbourAssetId = value
        self._property_changed('neighbourAssetId')        

    @property
    def simonIntlAssetTags(self) -> Iterable[Any]:
        return self.__simonIntlAssetTags

    @simonIntlAssetTags.setter
    def simonIntlAssetTags(self, value: Iterable[Any]):
        self.__simonIntlAssetTags = value
        self._property_changed('simonIntlAssetTags')        

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value
        self._property_changed('path')        

    @property
    def availableInventory(self):
        return self.__availableInventory

    @availableInventory.setter
    def availableInventory(self, value):
        self.__availableInventory = value
        self._property_changed('availableInventory')        

    @property
    def clientContact(self):
        return self.__clientContact

    @clientContact.setter
    def clientContact(self, value):
        self.__clientContact = value
        self._property_changed('clientContact')        

    @property
    def est1DayCompletePct(self):
        return self.__est1DayCompletePct

    @est1DayCompletePct.setter
    def est1DayCompletePct(self, value):
        self.__est1DayCompletePct = value
        self._property_changed('est1DayCompletePct')        

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        self.__rank = value
        self._property_changed('rank')        

    @property
    def dataSetCategory(self):
        return self.__dataSetCategory

    @dataSetCategory.setter
    def dataSetCategory(self, value):
        self.__dataSetCategory = value
        self._property_changed('dataSetCategory')        

    @property
    def createdById(self):
        return self.__createdById

    @createdById.setter
    def createdById(self, value):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def vehicleType(self):
        return self.__vehicleType

    @vehicleType.setter
    def vehicleType(self, value):
        self.__vehicleType = value
        self._property_changed('vehicleType')        

    @property
    def dailyRisk(self):
        return self.__dailyRisk

    @dailyRisk.setter
    def dailyRisk(self, value):
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
    def marketDataType(self):
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def sentimentScore(self):
        return self.__sentimentScore

    @sentimentScore.setter
    def sentimentScore(self, value):
        self.__sentimentScore = value
        self._property_changed('sentimentScore')        

    @property
    def bosInBps(self):
        return self.__bosInBps

    @bosInBps.setter
    def bosInBps(self, value):
        self.__bosInBps = value
        self._property_changed('bosInBps')        

    @property
    def pointClass(self):
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def fxSpot(self):
        return self.__fxSpot

    @fxSpot.setter
    def fxSpot(self, value):
        self.__fxSpot = value
        self._property_changed('fxSpot')        

    @property
    def bidLow(self):
        return self.__bidLow

    @bidLow.setter
    def bidLow(self, value):
        self.__bidLow = value
        self._property_changed('bidLow')        

    @property
    def valuePrevious(self):
        return self.__valuePrevious

    @valuePrevious.setter
    def valuePrevious(self, value):
        self.__valuePrevious = value
        self._property_changed('valuePrevious')        

    @property
    def fairVarianceVolatility(self):
        return self.__fairVarianceVolatility

    @fairVarianceVolatility.setter
    def fairVarianceVolatility(self, value):
        self.__fairVarianceVolatility = value
        self._property_changed('fairVarianceVolatility')        

    @property
    def avgTradeRate(self):
        return self.__avgTradeRate

    @avgTradeRate.setter
    def avgTradeRate(self, value):
        self.__avgTradeRate = value
        self._property_changed('avgTradeRate')        

    @property
    def shortLevel(self):
        return self.__shortLevel

    @shortLevel.setter
    def shortLevel(self, value):
        self.__shortLevel = value
        self._property_changed('shortLevel')        

    @property
    def hedgeVolatility(self):
        return self.__hedgeVolatility

    @hedgeVolatility.setter
    def hedgeVolatility(self, value):
        self.__hedgeVolatility = value
        self._property_changed('hedgeVolatility')        

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value
        self._property_changed('version')        

    @property
    def tags(self) -> Iterable[Any]:
        return self.__tags

    @tags.setter
    def tags(self, value: Iterable[Any]):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def underlyingAssetId(self):
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        

    @property
    def clientExposure(self):
        return self.__clientExposure

    @clientExposure.setter
    def clientExposure(self, value):
        self.__clientExposure = value
        self._property_changed('clientExposure')        

    @property
    def correlation(self):
        return self.__correlation

    @correlation.setter
    def correlation(self, value):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def exposure(self):
        return self.__exposure

    @exposure.setter
    def exposure(self, value):
        self.__exposure = value
        self._property_changed('exposure')        

    @property
    def gsSustainSubSector(self):
        return self.__gsSustainSubSector

    @gsSustainSubSector.setter
    def gsSustainSubSector(self, value):
        self.__gsSustainSubSector = value
        self._property_changed('gsSustainSubSector')        

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, value):
        self.__domain = value
        self._property_changed('domain')        

    @property
    def marketDataAsset(self):
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def forwardTenor(self):
        return self.__forwardTenor

    @forwardTenor.setter
    def forwardTenor(self, value):
        self.__forwardTenor = value
        self._property_changed('forwardTenor')        

    @property
    def unadjustedHigh(self):
        return self.__unadjustedHigh

    @unadjustedHigh.setter
    def unadjustedHigh(self, value):
        self.__unadjustedHigh = value
        self._property_changed('unadjustedHigh')        

    @property
    def sourceImportance(self):
        return self.__sourceImportance

    @sourceImportance.setter
    def sourceImportance(self, value):
        self.__sourceImportance = value
        self._property_changed('sourceImportance')        

    @property
    def eid(self):
        return self.__eid

    @eid.setter
    def eid(self, value):
        self.__eid = value
        self._property_changed('eid')        

    @property
    def jsn(self):
        return self.__jsn

    @jsn.setter
    def jsn(self, value):
        self.__jsn = value
        self._property_changed('jsn')        

    @property
    def relativeReturnQtd(self):
        return self.__relativeReturnQtd

    @relativeReturnQtd.setter
    def relativeReturnQtd(self, value):
        self.__relativeReturnQtd = value
        self._property_changed('relativeReturnQtd')        

    @property
    def displayName(self):
        return self.__displayName

    @displayName.setter
    def displayName(self, value):
        self.__displayName = value
        self._property_changed('displayName')        

    @property
    def minutesToTrade100Pct(self):
        return self.__minutesToTrade100Pct

    @minutesToTrade100Pct.setter
    def minutesToTrade100Pct(self, value):
        self.__minutesToTrade100Pct = value
        self._property_changed('minutesToTrade100Pct')        

    @property
    def marketModelId(self):
        return self.__marketModelId

    @marketModelId.setter
    def marketModelId(self, value):
        self.__marketModelId = value
        self._property_changed('marketModelId')        

    @property
    def quoteType(self):
        return self.__quoteType

    @quoteType.setter
    def quoteType(self, value):
        self.__quoteType = value
        self._property_changed('quoteType')        

    @property
    def tenor(self):
        return self.__tenor

    @tenor.setter
    def tenor(self, value):
        self.__tenor = value
        self._property_changed('tenor')        

    @property
    def esPolicyPercentile(self):
        return self.__esPolicyPercentile

    @esPolicyPercentile.setter
    def esPolicyPercentile(self, value):
        self.__esPolicyPercentile = value
        self._property_changed('esPolicyPercentile')        

    @property
    def tcmCostParticipationRate75Pct(self):
        return self.__tcmCostParticipationRate75Pct

    @tcmCostParticipationRate75Pct.setter
    def tcmCostParticipationRate75Pct(self, value):
        self.__tcmCostParticipationRate75Pct = value
        self._property_changed('tcmCostParticipationRate75Pct')        

    @property
    def close(self):
        return self.__close

    @close.setter
    def close(self, value):
        self.__close = value
        self._property_changed('close')        

    @property
    def tcmCostParticipationRate100Pct(self):
        return self.__tcmCostParticipationRate100Pct

    @tcmCostParticipationRate100Pct.setter
    def tcmCostParticipationRate100Pct(self, value):
        self.__tcmCostParticipationRate100Pct = value
        self._property_changed('tcmCostParticipationRate100Pct')        

    @property
    def disclaimer(self):
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value):
        self.__disclaimer = value
        self._property_changed('disclaimer')        

    @property
    def measureIdx(self):
        return self.__measureIdx

    @measureIdx.setter
    def measureIdx(self, value):
        self.__measureIdx = value
        self._property_changed('measureIdx')        

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value
        self._property_changed('a')        

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = value
        self._property_changed('b')        

    @property
    def loanFee(self):
        return self.__loanFee

    @loanFee.setter
    def loanFee(self, value):
        self.__loanFee = value
        self._property_changed('loanFee')        

    @property
    def c(self):
        return self.__c

    @c.setter
    def c(self, value):
        self.__c = value
        self._property_changed('c')        

    @property
    def equityVega(self):
        return self.__equityVega

    @equityVega.setter
    def equityVega(self, value):
        self.__equityVega = value
        self._property_changed('equityVega')        

    @property
    def deploymentVersion(self):
        return self.__deploymentVersion

    @deploymentVersion.setter
    def deploymentVersion(self, value):
        self.__deploymentVersion = value
        self._property_changed('deploymentVersion')        

    @property
    def fiveDayMove(self):
        return self.__fiveDayMove

    @fiveDayMove.setter
    def fiveDayMove(self, value):
        self.__fiveDayMove = value
        self._property_changed('fiveDayMove')        

    @property
    def borrower(self):
        return self.__borrower

    @borrower.setter
    def borrower(self, value):
        self.__borrower = value
        self._property_changed('borrower')        

    @property
    def performanceContribution(self):
        return self.__performanceContribution

    @performanceContribution.setter
    def performanceContribution(self, value):
        self.__performanceContribution = value
        self._property_changed('performanceContribution')        

    @property
    def targetNotional(self):
        return self.__targetNotional

    @targetNotional.setter
    def targetNotional(self, value):
        self.__targetNotional = value
        self._property_changed('targetNotional')        

    @property
    def fillLegId(self):
        return self.__fillLegId

    @fillLegId.setter
    def fillLegId(self, value):
        self.__fillLegId = value
        self._property_changed('fillLegId')        

    @property
    def rationale(self):
        return self.__rationale

    @rationale.setter
    def rationale(self, value):
        self.__rationale = value
        self._property_changed('rationale')        

    @property
    def regionalFocus(self):
        return self.__regionalFocus

    @regionalFocus.setter
    def regionalFocus(self, value):
        self.__regionalFocus = value
        self._property_changed('regionalFocus')        

    @property
    def volumePrimary(self):
        return self.__volumePrimary

    @volumePrimary.setter
    def volumePrimary(self, value):
        self.__volumePrimary = value
        self._property_changed('volumePrimary')        

    @property
    def series(self):
        return self.__series

    @series.setter
    def series(self, value):
        self.__series = value
        self._property_changed('series')        

    @property
    def simonId(self):
        return self.__simonId

    @simonId.setter
    def simonId(self, value):
        self.__simonId = value
        self._property_changed('simonId')        

    @property
    def newIdeasQtd(self):
        return self.__newIdeasQtd

    @newIdeasQtd.setter
    def newIdeasQtd(self, value):
        self.__newIdeasQtd = value
        self._property_changed('newIdeasQtd')        

    @property
    def adjustedAskPrice(self):
        return self.__adjustedAskPrice

    @adjustedAskPrice.setter
    def adjustedAskPrice(self, value):
        self.__adjustedAskPrice = value
        self._property_changed('adjustedAskPrice')        

    @property
    def quarter(self):
        return self.__quarter

    @quarter.setter
    def quarter(self, value):
        self.__quarter = value
        self._property_changed('quarter')        

    @property
    def factorUniverse(self):
        return self.__factorUniverse

    @factorUniverse.setter
    def factorUniverse(self, value):
        self.__factorUniverse = value
        self._property_changed('factorUniverse')        

    @property
    def eventCategory(self):
        return self.__eventCategory

    @eventCategory.setter
    def eventCategory(self, value):
        self.__eventCategory = value
        self._property_changed('eventCategory')        

    @property
    def impliedNormalVolatility(self):
        return self.__impliedNormalVolatility

    @impliedNormalVolatility.setter
    def impliedNormalVolatility(self, value):
        self.__impliedNormalVolatility = value
        self._property_changed('impliedNormalVolatility')        

    @property
    def unadjustedOpen(self):
        return self.__unadjustedOpen

    @unadjustedOpen.setter
    def unadjustedOpen(self, value):
        self.__unadjustedOpen = value
        self._property_changed('unadjustedOpen')        

    @property
    def arrivalRt(self):
        return self.__arrivalRt

    @arrivalRt.setter
    def arrivalRt(self, value):
        self.__arrivalRt = value
        self._property_changed('arrivalRt')        

    @property
    def transactionCost(self):
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def servicingCostShortPnl(self):
        return self.__servicingCostShortPnl

    @servicingCostShortPnl.setter
    def servicingCostShortPnl(self, value):
        self.__servicingCostShortPnl = value
        self._property_changed('servicingCostShortPnl')        

    @property
    def bidAskSpread(self):
        return self.__bidAskSpread

    @bidAskSpread.setter
    def bidAskSpread(self, value):
        self.__bidAskSpread = value
        self._property_changed('bidAskSpread')        

    @property
    def optionType(self):
        return self.__optionType

    @optionType.setter
    def optionType(self, value):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def tcmCostHorizon3Hour(self):
        return self.__tcmCostHorizon3Hour

    @tcmCostHorizon3Hour.setter
    def tcmCostHorizon3Hour(self, value):
        self.__tcmCostHorizon3Hour = value
        self._property_changed('tcmCostHorizon3Hour')        

    @property
    def clusterDescription(self):
        return self.__clusterDescription

    @clusterDescription.setter
    def clusterDescription(self, value):
        self.__clusterDescription = value
        self._property_changed('clusterDescription')        

    @property
    def positionAmount(self):
        return self.__positionAmount

    @positionAmount.setter
    def positionAmount(self, value):
        self.__positionAmount = value
        self._property_changed('positionAmount')        

    @property
    def numberOfPositions(self):
        return self.__numberOfPositions

    @numberOfPositions.setter
    def numberOfPositions(self, value):
        self.__numberOfPositions = value
        self._property_changed('numberOfPositions')        

    @property
    def windSpeed(self):
        return self.__windSpeed

    @windSpeed.setter
    def windSpeed(self, value):
        self.__windSpeed = value
        self._property_changed('windSpeed')        

    @property
    def openUnadjusted(self):
        return self.__openUnadjusted

    @openUnadjusted.setter
    def openUnadjusted(self, value):
        self.__openUnadjusted = value
        self._property_changed('openUnadjusted')        

    @property
    def maRank(self):
        return self.__maRank

    @maRank.setter
    def maRank(self, value):
        self.__maRank = value
        self._property_changed('maRank')        

    @property
    def eventStartDateTime(self):
        return self.__eventStartDateTime

    @eventStartDateTime.setter
    def eventStartDateTime(self, value):
        self.__eventStartDateTime = value
        self._property_changed('eventStartDateTime')        

    @property
    def askPrice(self):
        return self.__askPrice

    @askPrice.setter
    def askPrice(self, value):
        self.__askPrice = value
        self._property_changed('askPrice')        

    @property
    def eventId(self):
        return self.__eventId

    @eventId.setter
    def eventId(self, value):
        self.__eventId = value
        self._property_changed('eventId')        

    @property
    def dataProduct(self):
        return self.__dataProduct

    @dataProduct.setter
    def dataProduct(self, value):
        self.__dataProduct = value
        self._property_changed('dataProduct')        

    @property
    def sectors(self) -> Iterable[Any]:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: Iterable[Any]):
        self.__sectors = value
        self._property_changed('sectors')        

    @property
    def annualizedTrackingError(self):
        return self.__annualizedTrackingError

    @annualizedTrackingError.setter
    def annualizedTrackingError(self, value):
        self.__annualizedTrackingError = value
        self._property_changed('annualizedTrackingError')        

    @property
    def volSwap(self):
        return self.__volSwap

    @volSwap.setter
    def volSwap(self, value):
        self.__volSwap = value
        self._property_changed('volSwap')        

    @property
    def annualizedRisk(self):
        return self.__annualizedRisk

    @annualizedRisk.setter
    def annualizedRisk(self, value):
        self.__annualizedRisk = value
        self._property_changed('annualizedRisk')        

    @property
    def corporateAction(self):
        return self.__corporateAction

    @corporateAction.setter
    def corporateAction(self, value):
        self.__corporateAction = value
        self._property_changed('corporateAction')        

    @property
    def conviction(self):
        return self.__conviction

    @conviction.setter
    def conviction(self, value):
        self.__conviction = value
        self._property_changed('conviction')        

    @property
    def grossExposure(self):
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def benchmarkMaturity(self):
        return self.__benchmarkMaturity

    @benchmarkMaturity.setter
    def benchmarkMaturity(self, value):
        self.__benchmarkMaturity = value
        self._property_changed('benchmarkMaturity')        

    @property
    def volumeComposite(self):
        return self.__volumeComposite

    @volumeComposite.setter
    def volumeComposite(self, value):
        self.__volumeComposite = value
        self._property_changed('volumeComposite')        

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = value
        self._property_changed('volume')        

    @property
    def adv(self):
        return self.__adv

    @adv.setter
    def adv(self, value):
        self.__adv = value
        self._property_changed('adv')        

    @property
    def stsFxCurrency(self):
        return self.__stsFxCurrency

    @stsFxCurrency.setter
    def stsFxCurrency(self, value):
        self.__stsFxCurrency = value
        self._property_changed('stsFxCurrency')        

    @property
    def wpk(self):
        return self.__wpk

    @wpk.setter
    def wpk(self, value):
        self.__wpk = value
        self._property_changed('wpk')        

    @property
    def shortConvictionMedium(self):
        return self.__shortConvictionMedium

    @shortConvictionMedium.setter
    def shortConvictionMedium(self, value):
        self.__shortConvictionMedium = value
        self._property_changed('shortConvictionMedium')        

    @property
    def bidChange(self):
        return self.__bidChange

    @bidChange.setter
    def bidChange(self, value):
        self.__bidChange = value
        self._property_changed('bidChange')        

    @property
    def exchange(self):
        return self.__exchange

    @exchange.setter
    def exchange(self, value):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expiration(self):
        return self.__expiration

    @expiration.setter
    def expiration(self, value):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def tradePrice(self):
        return self.__tradePrice

    @tradePrice.setter
    def tradePrice(self, value):
        self.__tradePrice = value
        self._property_changed('tradePrice')        

    @property
    def esPolicyScore(self):
        return self.__esPolicyScore

    @esPolicyScore.setter
    def esPolicyScore(self, value):
        self.__esPolicyScore = value
        self._property_changed('esPolicyScore')        

    @property
    def cid(self):
        return self.__cid

    @cid.setter
    def cid(self, value):
        self.__cid = value
        self._property_changed('cid')        

    @property
    def importance(self):
        return self.__importance

    @importance.setter
    def importance(self, value):
        self.__importance = value
        self._property_changed('importance')        

    @property
    def sourceDateSpan(self):
        return self.__sourceDateSpan

    @sourceDateSpan.setter
    def sourceDateSpan(self, value):
        self.__sourceDateSpan = value
        self._property_changed('sourceDateSpan')        

    @property
    def assetClassificationsGicsSector(self):
        return self.__assetClassificationsGicsSector

    @assetClassificationsGicsSector.setter
    def assetClassificationsGicsSector(self, value):
        self.__assetClassificationsGicsSector = value
        self._property_changed('assetClassificationsGicsSector')        

    @property
    def underlyingDataSetId(self):
        return self.__underlyingDataSetId

    @underlyingDataSetId.setter
    def underlyingDataSetId(self, value):
        self.__underlyingDataSetId = value
        self._property_changed('underlyingDataSetId')        

    @property
    def stsAssetName(self):
        return self.__stsAssetName

    @stsAssetName.setter
    def stsAssetName(self, value):
        self.__stsAssetName = value
        self._property_changed('stsAssetName')        

    @property
    def closeUnadjusted(self):
        return self.__closeUnadjusted

    @closeUnadjusted.setter
    def closeUnadjusted(self, value):
        self.__closeUnadjusted = value
        self._property_changed('closeUnadjusted')        

    @property
    def valueUnit(self):
        return self.__valueUnit

    @valueUnit.setter
    def valueUnit(self, value):
        self.__valueUnit = value
        self._property_changed('valueUnit')        

    @property
    def bidHigh(self):
        return self.__bidHigh

    @bidHigh.setter
    def bidHigh(self, value):
        self.__bidHigh = value
        self._property_changed('bidHigh')        

    @property
    def adjustedLowPrice(self):
        return self.__adjustedLowPrice

    @adjustedLowPrice.setter
    def adjustedLowPrice(self, value):
        self.__adjustedLowPrice = value
        self._property_changed('adjustedLowPrice')        

    @property
    def netExposureClassification(self):
        return self.__netExposureClassification

    @netExposureClassification.setter
    def netExposureClassification(self, value):
        self.__netExposureClassification = value
        self._property_changed('netExposureClassification')        

    @property
    def longConvictionLarge(self):
        return self.__longConvictionLarge

    @longConvictionLarge.setter
    def longConvictionLarge(self, value):
        self.__longConvictionLarge = value
        self._property_changed('longConvictionLarge')        

    @property
    def fairVariance(self):
        return self.__fairVariance

    @fairVariance.setter
    def fairVariance(self, value):
        self.__fairVariance = value
        self._property_changed('fairVariance')        

    @property
    def hitRateWtd(self):
        return self.__hitRateWtd

    @hitRateWtd.setter
    def hitRateWtd(self, value):
        self.__hitRateWtd = value
        self._property_changed('hitRateWtd')        

    @property
    def oad(self):
        return self.__oad

    @oad.setter
    def oad(self, value):
        self.__oad = value
        self._property_changed('oad')        

    @property
    def bosInBpsDescription(self):
        return self.__bosInBpsDescription

    @bosInBpsDescription.setter
    def bosInBpsDescription(self, value):
        self.__bosInBpsDescription = value
        self._property_changed('bosInBpsDescription')        

    @property
    def lowPrice(self):
        return self.__lowPrice

    @lowPrice.setter
    def lowPrice(self, value):
        self.__lowPrice = value
        self._property_changed('lowPrice')        

    @property
    def realizedVolatility(self):
        return self.__realizedVolatility

    @realizedVolatility.setter
    def realizedVolatility(self, value):
        self.__realizedVolatility = value
        self._property_changed('realizedVolatility')        

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, value):
        self.__rate = value
        self._property_changed('rate')        

    @property
    def adv22DayPct(self):
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        self.__alpha = value
        self._property_changed('alpha')        

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, value):
        self.__client = value
        self._property_changed('client')        

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, value):
        self.__company = value
        self._property_changed('company')        

    @property
    def convictionList(self):
        return self.__convictionList

    @convictionList.setter
    def convictionList(self, value):
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
    def ticker(self):
        return self.__ticker

    @ticker.setter
    def ticker(self, value):
        self.__ticker = value
        self._property_changed('ticker')        

    @property
    def inRiskModel(self):
        return self.__inRiskModel

    @inRiskModel.setter
    def inRiskModel(self, value):
        self.__inRiskModel = value
        self._property_changed('inRiskModel')        

    @property
    def tcmCostHorizon1Day(self):
        return self.__tcmCostHorizon1Day

    @tcmCostHorizon1Day.setter
    def tcmCostHorizon1Day(self, value):
        self.__tcmCostHorizon1Day = value
        self._property_changed('tcmCostHorizon1Day')        

    @property
    def servicingCostLongPnl(self):
        return self.__servicingCostLongPnl

    @servicingCostLongPnl.setter
    def servicingCostLongPnl(self, value):
        self.__servicingCostLongPnl = value
        self._property_changed('servicingCostLongPnl')        

    @property
    def stsRatesCountry(self):
        return self.__stsRatesCountry

    @stsRatesCountry.setter
    def stsRatesCountry(self, value):
        self.__stsRatesCountry = value
        self._property_changed('stsRatesCountry')        

    @property
    def meetingNumber(self):
        return self.__meetingNumber

    @meetingNumber.setter
    def meetingNumber(self, value):
        self.__meetingNumber = value
        self._property_changed('meetingNumber')        

    @property
    def exchangeId(self):
        return self.__exchangeId

    @exchangeId.setter
    def exchangeId(self, value):
        self.__exchangeId = value
        self._property_changed('exchangeId')        

    @property
    def horizon(self):
        return self.__horizon

    @horizon.setter
    def horizon(self, value):
        self.__horizon = value
        self._property_changed('horizon')        

    @property
    def tcmCostHorizon20Day(self):
        return self.__tcmCostHorizon20Day

    @tcmCostHorizon20Day.setter
    def tcmCostHorizon20Day(self, value):
        self.__tcmCostHorizon20Day = value
        self._property_changed('tcmCostHorizon20Day')        

    @property
    def longLevel(self):
        return self.__longLevel

    @longLevel.setter
    def longLevel(self, value):
        self.__longLevel = value
        self._property_changed('longLevel')        

    @property
    def sourceValueForecast(self):
        return self.__sourceValueForecast

    @sourceValueForecast.setter
    def sourceValueForecast(self, value):
        self.__sourceValueForecast = value
        self._property_changed('sourceValueForecast')        

    @property
    def shortConvictionLarge(self):
        return self.__shortConvictionLarge

    @shortConvictionLarge.setter
    def shortConvictionLarge(self, value):
        self.__shortConvictionLarge = value
        self._property_changed('shortConvictionLarge')        

    @property
    def realm(self):
        return self.__realm

    @realm.setter
    def realm(self, value):
        self.__realm = value
        self._property_changed('realm')        

    @property
    def bid(self):
        return self.__bid

    @bid.setter
    def bid(self, value):
        self.__bid = value
        self._property_changed('bid')        

    @property
    def dataDescription(self):
        return self.__dataDescription

    @dataDescription.setter
    def dataDescription(self, value):
        self.__dataDescription = value
        self._property_changed('dataDescription')        

    @property
    def gsn(self):
        return self.__gsn

    @gsn.setter
    def gsn(self, value):
        self.__gsn = value
        self._property_changed('gsn')        

    @property
    def isAggressive(self):
        return self.__isAggressive

    @isAggressive.setter
    def isAggressive(self, value):
        self.__isAggressive = value
        self._property_changed('isAggressive')        

    @property
    def orderId(self):
        return self.__orderId

    @orderId.setter
    def orderId(self, value):
        self.__orderId = value
        self._property_changed('orderId')        

    @property
    def gss(self):
        return self.__gss

    @gss.setter
    def gss(self, value):
        self.__gss = value
        self._property_changed('gss')        

    @property
    def percentOfMediandv1m(self):
        return self.__percentOfMediandv1m

    @percentOfMediandv1m.setter
    def percentOfMediandv1m(self, value):
        self.__percentOfMediandv1m = value
        self._property_changed('percentOfMediandv1m')        

    @property
    def assetClass(self):
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def gsideid(self):
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value):
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
    def ric(self):
        return self.__ric

    @ric.setter
    def ric(self, value):
        self.__ric = value
        self._property_changed('ric')        

    @property
    def positionSourceId(self):
        return self.__positionSourceId

    @positionSourceId.setter
    def positionSourceId(self, value):
        self.__positionSourceId = value
        self._property_changed('positionSourceId')        

    @property
    def division(self):
        return self.__division

    @division.setter
    def division(self, value):
        self.__division = value
        self._property_changed('division')        

    @property
    def marketCapUSD(self):
        return self.__marketCapUSD

    @marketCapUSD.setter
    def marketCapUSD(self, value):
        self.__marketCapUSD = value
        self._property_changed('marketCapUSD')        

    @property
    def deploymentId(self):
        return self.__deploymentId

    @deploymentId.setter
    def deploymentId(self, value):
        self.__deploymentId = value
        self._property_changed('deploymentId')        

    @property
    def highPrice(self):
        return self.__highPrice

    @highPrice.setter
    def highPrice(self, value):
        self.__highPrice = value
        self._property_changed('highPrice')        

    @property
    def shortWeight(self):
        return self.__shortWeight

    @shortWeight.setter
    def shortWeight(self, value):
        self.__shortWeight = value
        self._property_changed('shortWeight')        

    @property
    def absoluteShares(self):
        return self.__absoluteShares

    @absoluteShares.setter
    def absoluteShares(self, value):
        self.__absoluteShares = value
        self._property_changed('absoluteShares')        

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value
        self._property_changed('action')        

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value
        self._property_changed('model')        

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value
        self._property_changed('id')        

    @property
    def arrivalHaircutVwapNormalized(self):
        return self.__arrivalHaircutVwapNormalized

    @arrivalHaircutVwapNormalized.setter
    def arrivalHaircutVwapNormalized(self, value):
        self.__arrivalHaircutVwapNormalized = value
        self._property_changed('arrivalHaircutVwapNormalized')        

    @property
    def queueClockTimeDescription(self):
        return self.__queueClockTimeDescription

    @queueClockTimeDescription.setter
    def queueClockTimeDescription(self, value):
        self.__queueClockTimeDescription = value
        self._property_changed('queueClockTimeDescription')        

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, value):
        self.__period = value
        self._property_changed('period')        

    @property
    def indexCreateSource(self):
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value):
        self.__indexCreateSource = value
        self._property_changed('indexCreateSource')        

    @property
    def fiscalQuarter(self):
        return self.__fiscalQuarter

    @fiscalQuarter.setter
    def fiscalQuarter(self, value):
        self.__fiscalQuarter = value
        self._property_changed('fiscalQuarter')        

    @property
    def deltaStrike(self):
        return self.__deltaStrike

    @deltaStrike.setter
    def deltaStrike(self, value):
        self.__deltaStrike = value
        self._property_changed('deltaStrike')        

    @property
    def marketImpact(self):
        return self.__marketImpact

    @marketImpact.setter
    def marketImpact(self, value):
        self.__marketImpact = value
        self._property_changed('marketImpact')        

    @property
    def eventType(self):
        return self.__eventType

    @eventType.setter
    def eventType(self, value):
        self.__eventType = value
        self._property_changed('eventType')        

    @property
    def assetCountLong(self):
        return self.__assetCountLong

    @assetCountLong.setter
    def assetCountLong(self, value):
        self.__assetCountLong = value
        self._property_changed('assetCountLong')        

    @property
    def valueActual(self):
        return self.__valueActual

    @valueActual.setter
    def valueActual(self, value):
        self.__valueActual = value
        self._property_changed('valueActual')        

    @property
    def bcid(self):
        return self.__bcid

    @bcid.setter
    def bcid(self, value):
        self.__bcid = value
        self._property_changed('bcid')        

    @property
    def originalCountry(self):
        return self.__originalCountry

    @originalCountry.setter
    def originalCountry(self, value):
        self.__originalCountry = value
        self._property_changed('originalCountry')        

    @property
    def touchLiquidityScore(self):
        return self.__touchLiquidityScore

    @touchLiquidityScore.setter
    def touchLiquidityScore(self, value):
        self.__touchLiquidityScore = value
        self._property_changed('touchLiquidityScore')        

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, value):
        self.__field = value
        self._property_changed('field')        

    @property
    def spot(self):
        return self.__spot

    @spot.setter
    def spot(self, value):
        self.__spot = value
        self._property_changed('spot')        

    @property
    def expectedCompletionDate(self):
        return self.__expectedCompletionDate

    @expectedCompletionDate.setter
    def expectedCompletionDate(self, value):
        self.__expectedCompletionDate = value
        self._property_changed('expectedCompletionDate')        

    @property
    def loanValue(self):
        return self.__loanValue

    @loanValue.setter
    def loanValue(self, value):
        self.__loanValue = value
        self._property_changed('loanValue')        

    @property
    def skew(self):
        return self.__skew

    @skew.setter
    def skew(self, value):
        self.__skew = value
        self._property_changed('skew')        

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        self._property_changed('status')        

    @property
    def sustainEmergingMarkets(self):
        return self.__sustainEmergingMarkets

    @sustainEmergingMarkets.setter
    def sustainEmergingMarkets(self, value):
        self.__sustainEmergingMarkets = value
        self._property_changed('sustainEmergingMarkets')        

    @property
    def eventDateTime(self):
        return self.__eventDateTime

    @eventDateTime.setter
    def eventDateTime(self, value):
        self.__eventDateTime = value
        self._property_changed('eventDateTime')        

    @property
    def totalReturnPrice(self):
        return self.__totalReturnPrice

    @totalReturnPrice.setter
    def totalReturnPrice(self, value):
        self.__totalReturnPrice = value
        self._property_changed('totalReturnPrice')        

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value
        self._property_changed('city')        

    @property
    def eventSource(self):
        return self.__eventSource

    @eventSource.setter
    def eventSource(self, value):
        self.__eventSource = value
        self._property_changed('eventSource')        

    @property
    def qisPermNo(self):
        return self.__qisPermNo

    @qisPermNo.setter
    def qisPermNo(self, value):
        self.__qisPermNo = value
        self._property_changed('qisPermNo')        

    @property
    def hitRateYtd(self):
        return self.__hitRateYtd

    @hitRateYtd.setter
    def hitRateYtd(self, value):
        self.__hitRateYtd = value
        self._property_changed('hitRateYtd')        

    @property
    def stsCommodity(self):
        return self.__stsCommodity

    @stsCommodity.setter
    def stsCommodity(self, value):
        self.__stsCommodity = value
        self._property_changed('stsCommodity')        

    @property
    def stsCommoditySector(self):
        return self.__stsCommoditySector

    @stsCommoditySector.setter
    def stsCommoditySector(self, value):
        self.__stsCommoditySector = value
        self._property_changed('stsCommoditySector')        

    @property
    def salesCoverage(self):
        return self.__salesCoverage

    @salesCoverage.setter
    def salesCoverage(self, value):
        self.__salesCoverage = value
        self._property_changed('salesCoverage')        

    @property
    def shortExposure(self):
        return self.__shortExposure

    @shortExposure.setter
    def shortExposure(self, value):
        self.__shortExposure = value
        self._property_changed('shortExposure')        

    @property
    def esScore(self):
        return self.__esScore

    @esScore.setter
    def esScore(self, value):
        self.__esScore = value
        self._property_changed('esScore')        

    @property
    def tcmCostParticipationRate10Pct(self):
        return self.__tcmCostParticipationRate10Pct

    @tcmCostParticipationRate10Pct.setter
    def tcmCostParticipationRate10Pct(self, value):
        self.__tcmCostParticipationRate10Pct = value
        self._property_changed('tcmCostParticipationRate10Pct')        

    @property
    def eventTime(self):
        return self.__eventTime

    @eventTime.setter
    def eventTime(self, value):
        self.__eventTime = value
        self._property_changed('eventTime')        

    @property
    def positionSourceName(self):
        return self.__positionSourceName

    @positionSourceName.setter
    def positionSourceName(self, value):
        self.__positionSourceName = value
        self._property_changed('positionSourceName')        

    @property
    def priceRangeInTicks(self):
        return self.__priceRangeInTicks

    @priceRangeInTicks.setter
    def priceRangeInTicks(self, value):
        self.__priceRangeInTicks = value
        self._property_changed('priceRangeInTicks')        

    @property
    def deliveryDate(self):
        return self.__deliveryDate

    @deliveryDate.setter
    def deliveryDate(self, value):
        self.__deliveryDate = value
        self._property_changed('deliveryDate')        

    @property
    def arrivalHaircutVwap(self):
        return self.__arrivalHaircutVwap

    @arrivalHaircutVwap.setter
    def arrivalHaircutVwap(self, value):
        self.__arrivalHaircutVwap = value
        self._property_changed('arrivalHaircutVwap')        

    @property
    def interestRate(self):
        return self.__interestRate

    @interestRate.setter
    def interestRate(self, value):
        self.__interestRate = value
        self._property_changed('interestRate')        

    @property
    def executionDays(self):
        return self.__executionDays

    @executionDays.setter
    def executionDays(self, value):
        self.__executionDays = value
        self._property_changed('executionDays')        

    @property
    def pctChange(self):
        return self.__pctChange

    @pctChange.setter
    def pctChange(self, value):
        self.__pctChange = value
        self._property_changed('pctChange')        

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        self.__side = value
        self._property_changed('side')        

    @property
    def numberOfRolls(self):
        return self.__numberOfRolls

    @numberOfRolls.setter
    def numberOfRolls(self, value):
        self.__numberOfRolls = value
        self._property_changed('numberOfRolls')        

    @property
    def agentLenderFee(self):
        return self.__agentLenderFee

    @agentLenderFee.setter
    def agentLenderFee(self, value):
        self.__agentLenderFee = value
        self._property_changed('agentLenderFee')        

    @property
    def complianceRestrictedStatus(self):
        return self.__complianceRestrictedStatus

    @complianceRestrictedStatus.setter
    def complianceRestrictedStatus(self, value):
        self.__complianceRestrictedStatus = value
        self._property_changed('complianceRestrictedStatus')        

    @property
    def forward(self):
        return self.__forward

    @forward.setter
    def forward(self, value):
        self.__forward = value
        self._property_changed('forward')        

    @property
    def borrowFee(self):
        return self.__borrowFee

    @borrowFee.setter
    def borrowFee(self, value):
        self.__borrowFee = value
        self._property_changed('borrowFee')        

    @property
    def strike(self):
        return self.__strike

    @strike.setter
    def strike(self, value):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def updateTime(self):
        return self.__updateTime

    @updateTime.setter
    def updateTime(self, value):
        self.__updateTime = value
        self._property_changed('updateTime')        

    @property
    def loanSpread(self):
        return self.__loanSpread

    @loanSpread.setter
    def loanSpread(self, value):
        self.__loanSpread = value
        self._property_changed('loanSpread')        

    @property
    def tcmCostHorizon12Hour(self):
        return self.__tcmCostHorizon12Hour

    @tcmCostHorizon12Hour.setter
    def tcmCostHorizon12Hour(self, value):
        self.__tcmCostHorizon12Hour = value
        self._property_changed('tcmCostHorizon12Hour')        

    @property
    def dewPoint(self):
        return self.__dewPoint

    @dewPoint.setter
    def dewPoint(self, value):
        self.__dewPoint = value
        self._property_changed('dewPoint')        

    @property
    def researchCommission(self):
        return self.__researchCommission

    @researchCommission.setter
    def researchCommission(self, value):
        self.__researchCommission = value
        self._property_changed('researchCommission')        

    @property
    def bbid(self):
        return self.__bbid

    @bbid.setter
    def bbid(self, value):
        self.__bbid = value
        self._property_changed('bbid')        

    @property
    def eventStatus(self):
        return self.__eventStatus

    @eventStatus.setter
    def eventStatus(self, value):
        self.__eventStatus = value
        self._property_changed('eventStatus')        

    @property
    def effectiveDate(self):
        return self.__effectiveDate

    @effectiveDate.setter
    def effectiveDate(self, value):
        self.__effectiveDate = value
        self._property_changed('effectiveDate')        

    @property
    def return_(self):
        return self.__return

    @return_.setter
    def return_(self, value):
        self.__return = value
        self._property_changed('return')        

    @property
    def maxTemperature(self):
        return self.__maxTemperature

    @maxTemperature.setter
    def maxTemperature(self, value):
        self.__maxTemperature = value
        self._property_changed('maxTemperature')        

    @property
    def acquirerShareholderMeetingDate(self):
        return self.__acquirerShareholderMeetingDate

    @acquirerShareholderMeetingDate.setter
    def acquirerShareholderMeetingDate(self, value):
        self.__acquirerShareholderMeetingDate = value
        self._property_changed('acquirerShareholderMeetingDate')        

    @property
    def arrivalMidNormalized(self):
        return self.__arrivalMidNormalized

    @arrivalMidNormalized.setter
    def arrivalMidNormalized(self, value):
        self.__arrivalMidNormalized = value
        self._property_changed('arrivalMidNormalized')        

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        self.__rating = value
        self._property_changed('rating')        

    @property
    def arrivalRtNormalized(self):
        return self.__arrivalRtNormalized

    @arrivalRtNormalized.setter
    def arrivalRtNormalized(self, value):
        self.__arrivalRtNormalized = value
        self._property_changed('arrivalRtNormalized')        

    @property
    def performanceFee(self):
        return self.__performanceFee

    @performanceFee.setter
    def performanceFee(self, value):
        self.__performanceFee = value
        self._property_changed('performanceFee')        

    @property
    def reportType(self):
        return self.__reportType

    @reportType.setter
    def reportType(self, value):
        self.__reportType = value
        self._property_changed('reportType')        

    @property
    def sourceURL(self):
        return self.__sourceURL

    @sourceURL.setter
    def sourceURL(self, value):
        self.__sourceURL = value
        self._property_changed('sourceURL')        

    @property
    def estimatedReturn(self):
        return self.__estimatedReturn

    @estimatedReturn.setter
    def estimatedReturn(self, value):
        self.__estimatedReturn = value
        self._property_changed('estimatedReturn')        

    @property
    def underlyingAssetIds(self) -> Iterable[Any]:
        return self.__underlyingAssetIds

    @underlyingAssetIds.setter
    def underlyingAssetIds(self, value: Iterable[Any]):
        self.__underlyingAssetIds = value
        self._property_changed('underlyingAssetIds')        

    @property
    def high(self):
        return self.__high

    @high.setter
    def high(self, value):
        self.__high = value
        self._property_changed('high')        

    @property
    def sourceLastUpdate(self):
        return self.__sourceLastUpdate

    @sourceLastUpdate.setter
    def sourceLastUpdate(self, value):
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
    def adv10DayPct(self):
        return self.__adv10DayPct

    @adv10DayPct.setter
    def adv10DayPct(self, value):
        self.__adv10DayPct = value
        self._property_changed('adv10DayPct')        

    @property
    def longConvictionMedium(self):
        return self.__longConvictionMedium

    @longConvictionMedium.setter
    def longConvictionMedium(self, value):
        self.__longConvictionMedium = value
        self._property_changed('longConvictionMedium')        

    @property
    def eventName(self):
        return self.__eventName

    @eventName.setter
    def eventName(self, value):
        self.__eventName = value
        self._property_changed('eventName')        

    @property
    def annualRisk(self):
        return self.__annualRisk

    @annualRisk.setter
    def annualRisk(self, value):
        self.__annualRisk = value
        self._property_changed('annualRisk')        

    @property
    def dailyTrackingError(self):
        return self.__dailyTrackingError

    @dailyTrackingError.setter
    def dailyTrackingError(self, value):
        self.__dailyTrackingError = value
        self._property_changed('dailyTrackingError')        

    @property
    def unadjustedBid(self):
        return self.__unadjustedBid

    @unadjustedBid.setter
    def unadjustedBid(self, value):
        self.__unadjustedBid = value
        self._property_changed('unadjustedBid')        

    @property
    def gsdeer(self):
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value):
        self.__gsdeer = value
        self._property_changed('gsdeer')        

    @property
    def marketCap(self):
        return self.__marketCap

    @marketCap.setter
    def marketCap(self, value):
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
    def bbidEquivalent(self):
        return self.__bbidEquivalent

    @bbidEquivalent.setter
    def bbidEquivalent(self, value):
        self.__bbidEquivalent = value
        self._property_changed('bbidEquivalent')        

    @property
    def prevCloseAsk(self):
        return self.__prevCloseAsk

    @prevCloseAsk.setter
    def prevCloseAsk(self, value):
        self.__prevCloseAsk = value
        self._property_changed('prevCloseAsk')        

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value
        self._property_changed('level')        

    @property
    def valoren(self):
        return self.__valoren

    @valoren.setter
    def valoren(self, value):
        self.__valoren = value
        self._property_changed('valoren')        

    @property
    def pressure(self):
        return self.__pressure

    @pressure.setter
    def pressure(self, value):
        self.__pressure = value
        self._property_changed('pressure')        

    @property
    def shortDescription(self):
        return self.__shortDescription

    @shortDescription.setter
    def shortDescription(self, value):
        self.__shortDescription = value
        self._property_changed('shortDescription')        

    @property
    def basis(self):
        return self.__basis

    @basis.setter
    def basis(self, value):
        self.__basis = value
        self._property_changed('basis')        

    @property
    def netWeight(self):
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def hedgeId(self):
        return self.__hedgeId

    @hedgeId.setter
    def hedgeId(self, value):
        self.__hedgeId = value
        self._property_changed('hedgeId')        

    @property
    def portfolioManagers(self) -> Iterable[Any]:
        return self.__portfolioManagers

    @portfolioManagers.setter
    def portfolioManagers(self, value: Iterable[Any]):
        self.__portfolioManagers = value
        self._property_changed('portfolioManagers')        

    @property
    def bosInTicks(self):
        return self.__bosInTicks

    @bosInTicks.setter
    def bosInTicks(self, value):
        self.__bosInTicks = value
        self._property_changed('bosInTicks')        

    @property
    def tcmCostHorizon8Day(self):
        return self.__tcmCostHorizon8Day

    @tcmCostHorizon8Day.setter
    def tcmCostHorizon8Day(self, value):
        self.__tcmCostHorizon8Day = value
        self._property_changed('tcmCostHorizon8Day')        

    @property
    def supraStrategy(self):
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value):
        self.__supraStrategy = value
        self._property_changed('supraStrategy')        

    @property
    def adv5DayPct(self):
        return self.__adv5DayPct

    @adv5DayPct.setter
    def adv5DayPct(self, value):
        self.__adv5DayPct = value
        self._property_changed('adv5DayPct')        

    @property
    def factorSource(self):
        return self.__factorSource

    @factorSource.setter
    def factorSource(self, value):
        self.__factorSource = value
        self._property_changed('factorSource')        

    @property
    def leverage(self):
        return self.__leverage

    @leverage.setter
    def leverage(self, value):
        self.__leverage = value
        self._property_changed('leverage')        

    @property
    def submitter(self):
        return self.__submitter

    @submitter.setter
    def submitter(self, value):
        self.__submitter = value
        self._property_changed('submitter')        

    @property
    def notional(self):
        return self.__notional

    @notional.setter
    def notional(self, value):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def esDisclosurePercentage(self):
        return self.__esDisclosurePercentage

    @esDisclosurePercentage.setter
    def esDisclosurePercentage(self, value):
        self.__esDisclosurePercentage = value
        self._property_changed('esDisclosurePercentage')        

    @property
    def clientShortName(self):
        return self.__clientShortName

    @clientShortName.setter
    def clientShortName(self, value):
        self.__clientShortName = value
        self._property_changed('clientShortName')        

    @property
    def fwdPoints(self):
        return self.__fwdPoints

    @fwdPoints.setter
    def fwdPoints(self, value):
        self.__fwdPoints = value
        self._property_changed('fwdPoints')        

    @property
    def groupCategory(self):
        return self.__groupCategory

    @groupCategory.setter
    def groupCategory(self, value):
        self.__groupCategory = value
        self._property_changed('groupCategory')        

    @property
    def kpiId(self):
        return self.__kpiId

    @kpiId.setter
    def kpiId(self, value):
        self.__kpiId = value
        self._property_changed('kpiId')        

    @property
    def relativeReturnWtd(self):
        return self.__relativeReturnWtd

    @relativeReturnWtd.setter
    def relativeReturnWtd(self, value):
        self.__relativeReturnWtd = value
        self._property_changed('relativeReturnWtd')        

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value
        self._property_changed('total')        

    @property
    def riskModel(self):
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value):
        self.__riskModel = value
        self._property_changed('riskModel')        

    @property
    def assetId(self):
        return self.__assetId

    @assetId.setter
    def assetId(self, value):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def lastUpdatedTime(self):
        return self.__lastUpdatedTime

    @lastUpdatedTime.setter
    def lastUpdatedTime(self, value):
        self.__lastUpdatedTime = value
        self._property_changed('lastUpdatedTime')        

    @property
    def fairValue(self):
        return self.__fairValue

    @fairValue.setter
    def fairValue(self, value):
        self.__fairValue = value
        self._property_changed('fairValue')        

    @property
    def adjustedHighPrice(self):
        return self.__adjustedHighPrice

    @adjustedHighPrice.setter
    def adjustedHighPrice(self, value):
        self.__adjustedHighPrice = value
        self._property_changed('adjustedHighPrice')        

    @property
    def openTime(self):
        return self.__openTime

    @openTime.setter
    def openTime(self, value):
        self.__openTime = value
        self._property_changed('openTime')        

    @property
    def beta(self):
        return self.__beta

    @beta.setter
    def beta(self, value):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        self._property_changed('direction')        

    @property
    def valueForecast(self):
        return self.__valueForecast

    @valueForecast.setter
    def valueForecast(self, value):
        self.__valueForecast = value
        self._property_changed('valueForecast')        

    @property
    def longExposure(self):
        return self.__longExposure

    @longExposure.setter
    def longExposure(self, value):
        self.__longExposure = value
        self._property_changed('longExposure')        

    @property
    def positionSourceType(self):
        return self.__positionSourceType

    @positionSourceType.setter
    def positionSourceType(self, value):
        self.__positionSourceType = value
        self._property_changed('positionSourceType')        

    @property
    def tcmCostParticipationRate20Pct(self):
        return self.__tcmCostParticipationRate20Pct

    @tcmCostParticipationRate20Pct.setter
    def tcmCostParticipationRate20Pct(self, value):
        self.__tcmCostParticipationRate20Pct = value
        self._property_changed('tcmCostParticipationRate20Pct')        

    @property
    def adjustedClosePrice(self):
        return self.__adjustedClosePrice

    @adjustedClosePrice.setter
    def adjustedClosePrice(self, value):
        self.__adjustedClosePrice = value
        self._property_changed('adjustedClosePrice')        

    @property
    def cross(self):
        return self.__cross

    @cross.setter
    def cross(self, value):
        self.__cross = value
        self._property_changed('cross')        

    @property
    def lmsId(self):
        return self.__lmsId

    @lmsId.setter
    def lmsId(self, value):
        self.__lmsId = value
        self._property_changed('lmsId')        

    @property
    def rebateRate(self):
        return self.__rebateRate

    @rebateRate.setter
    def rebateRate(self, value):
        self.__rebateRate = value
        self._property_changed('rebateRate')        

    @property
    def ideaStatus(self):
        return self.__ideaStatus

    @ideaStatus.setter
    def ideaStatus(self, value):
        self.__ideaStatus = value
        self._property_changed('ideaStatus')        

    @property
    def participationRate(self):
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def fxForecast(self):
        return self.__fxForecast

    @fxForecast.setter
    def fxForecast(self, value):
        self.__fxForecast = value
        self._property_changed('fxForecast')        

    @property
    def fixingTimeLabel(self):
        return self.__fixingTimeLabel

    @fixingTimeLabel.setter
    def fixingTimeLabel(self, value):
        self.__fixingTimeLabel = value
        self._property_changed('fixingTimeLabel')        

    @property
    def fillId(self):
        return self.__fillId

    @fillId.setter
    def fillId(self, value):
        self.__fillId = value
        self._property_changed('fillId')        

    @property
    def esNumericScore(self):
        return self.__esNumericScore

    @esNumericScore.setter
    def esNumericScore(self, value):
        self.__esNumericScore = value
        self._property_changed('esNumericScore')        

    @property
    def inBenchmark(self):
        return self.__inBenchmark

    @inBenchmark.setter
    def inBenchmark(self, value):
        self.__inBenchmark = value
        self._property_changed('inBenchmark')        

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, value):
        self.__strategy = value
        self._property_changed('strategy')        

    @property
    def shortInterest(self):
        return self.__shortInterest

    @shortInterest.setter
    def shortInterest(self, value):
        self.__shortInterest = value
        self._property_changed('shortInterest')        

    @property
    def referencePeriod(self):
        return self.__referencePeriod

    @referencePeriod.setter
    def referencePeriod(self, value):
        self.__referencePeriod = value
        self._property_changed('referencePeriod')        

    @property
    def adjustedVolume(self):
        return self.__adjustedVolume

    @adjustedVolume.setter
    def adjustedVolume(self, value):
        self.__adjustedVolume = value
        self._property_changed('adjustedVolume')        

    @property
    def queueInLotsDescription(self):
        return self.__queueInLotsDescription

    @queueInLotsDescription.setter
    def queueInLotsDescription(self, value):
        self.__queueInLotsDescription = value
        self._property_changed('queueInLotsDescription')        

    @property
    def pbClientId(self):
        return self.__pbClientId

    @pbClientId.setter
    def pbClientId(self, value):
        self.__pbClientId = value
        self._property_changed('pbClientId')        

    @property
    def ownerId(self):
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def secDB(self):
        return self.__secDB

    @secDB.setter
    def secDB(self, value):
        self.__secDB = value
        self._property_changed('secDB')        

    @property
    def objective(self):
        return self.__objective

    @objective.setter
    def objective(self, value):
        self.__objective = value
        self._property_changed('objective')        

    @property
    def navPrice(self):
        return self.__navPrice

    @navPrice.setter
    def navPrice(self, value):
        self.__navPrice = value
        self._property_changed('navPrice')        

    @property
    def ideaActivityType(self):
        return self.__ideaActivityType

    @ideaActivityType.setter
    def ideaActivityType(self, value):
        self.__ideaActivityType = value
        self._property_changed('ideaActivityType')        

    @property
    def precipitation(self):
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value):
        self.__precipitation = value
        self._property_changed('precipitation')        

    @property
    def ideaSource(self):
        return self.__ideaSource

    @ideaSource.setter
    def ideaSource(self, value):
        self.__ideaSource = value
        self._property_changed('ideaSource')        

    @property
    def hedgeNotional(self):
        return self.__hedgeNotional

    @hedgeNotional.setter
    def hedgeNotional(self, value):
        self.__hedgeNotional = value
        self._property_changed('hedgeNotional')        

    @property
    def askLow(self):
        return self.__askLow

    @askLow.setter
    def askLow(self, value):
        self.__askLow = value
        self._property_changed('askLow')        

    @property
    def unadjustedAsk(self):
        return self.__unadjustedAsk

    @unadjustedAsk.setter
    def unadjustedAsk(self, value):
        self.__unadjustedAsk = value
        self._property_changed('unadjustedAsk')        

    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, value):
        self.__expiry = value
        self._property_changed('expiry')        

    @property
    def tradingPnl(self):
        return self.__tradingPnl

    @tradingPnl.setter
    def tradingPnl(self, value):
        self.__tradingPnl = value
        self._property_changed('tradingPnl')        

    @property
    def strikePercentage(self):
        return self.__strikePercentage

    @strikePercentage.setter
    def strikePercentage(self, value):
        self.__strikePercentage = value
        self._property_changed('strikePercentage')        

    @property
    def excessReturnPrice(self):
        return self.__excessReturnPrice

    @excessReturnPrice.setter
    def excessReturnPrice(self, value):
        self.__excessReturnPrice = value
        self._property_changed('excessReturnPrice')        

    @property
    def shortConvictionSmall(self):
        return self.__shortConvictionSmall

    @shortConvictionSmall.setter
    def shortConvictionSmall(self, value):
        self.__shortConvictionSmall = value
        self._property_changed('shortConvictionSmall')        

    @property
    def prevCloseBid(self):
        return self.__prevCloseBid

    @prevCloseBid.setter
    def prevCloseBid(self, value):
        self.__prevCloseBid = value
        self._property_changed('prevCloseBid')        

    @property
    def fxPnl(self):
        return self.__fxPnl

    @fxPnl.setter
    def fxPnl(self, value):
        self.__fxPnl = value
        self._property_changed('fxPnl')        

    @property
    def forecast(self):
        return self.__forecast

    @forecast.setter
    def forecast(self, value):
        self.__forecast = value
        self._property_changed('forecast')        

    @property
    def tcmCostHorizon16Day(self):
        return self.__tcmCostHorizon16Day

    @tcmCostHorizon16Day.setter
    def tcmCostHorizon16Day(self, value):
        self.__tcmCostHorizon16Day = value
        self._property_changed('tcmCostHorizon16Day')        

    @property
    def pnl(self):
        return self.__pnl

    @pnl.setter
    def pnl(self, value):
        self.__pnl = value
        self._property_changed('pnl')        

    @property
    def assetClassificationsGicsIndustryGroup(self):
        return self.__assetClassificationsGicsIndustryGroup

    @assetClassificationsGicsIndustryGroup.setter
    def assetClassificationsGicsIndustryGroup(self, value):
        self.__assetClassificationsGicsIndustryGroup = value
        self._property_changed('assetClassificationsGicsIndustryGroup')        

    @property
    def unadjustedClose(self):
        return self.__unadjustedClose

    @unadjustedClose.setter
    def unadjustedClose(self, value):
        self.__unadjustedClose = value
        self._property_changed('unadjustedClose')        

    @property
    def tcmCostHorizon4Day(self):
        return self.__tcmCostHorizon4Day

    @tcmCostHorizon4Day.setter
    def tcmCostHorizon4Day(self, value):
        self.__tcmCostHorizon4Day = value
        self._property_changed('tcmCostHorizon4Day')        

    @property
    def assetClassificationsIsPrimary(self):
        return self.__assetClassificationsIsPrimary

    @assetClassificationsIsPrimary.setter
    def assetClassificationsIsPrimary(self, value):
        self.__assetClassificationsIsPrimary = value
        self._property_changed('assetClassificationsIsPrimary')        

    @property
    def styles(self) -> Iterable[Any]:
        return self.__styles

    @styles.setter
    def styles(self, value: Iterable[Any]):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def shortName(self):
        return self.__shortName

    @shortName.setter
    def shortName(self, value):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def equityTheta(self):
        return self.__equityTheta

    @equityTheta.setter
    def equityTheta(self, value):
        self.__equityTheta = value
        self._property_changed('equityTheta')        

    @property
    def averageFillPrice(self):
        return self.__averageFillPrice

    @averageFillPrice.setter
    def averageFillPrice(self, value):
        self.__averageFillPrice = value
        self._property_changed('averageFillPrice')        

    @property
    def snowfall(self):
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value):
        self.__snowfall = value
        self._property_changed('snowfall')        

    @property
    def mic(self):
        return self.__mic

    @mic.setter
    def mic(self, value):
        self.__mic = value
        self._property_changed('mic')        

    @property
    def openPrice(self):
        return self.__openPrice

    @openPrice.setter
    def openPrice(self, value):
        self.__openPrice = value
        self._property_changed('openPrice')        

    @property
    def autoExecState(self):
        return self.__autoExecState

    @autoExecState.setter
    def autoExecState(self, value):
        self.__autoExecState = value
        self._property_changed('autoExecState')        

    @property
    def depthSpreadScore(self):
        return self.__depthSpreadScore

    @depthSpreadScore.setter
    def depthSpreadScore(self, value):
        self.__depthSpreadScore = value
        self._property_changed('depthSpreadScore')        

    @property
    def relativeReturnYtd(self):
        return self.__relativeReturnYtd

    @relativeReturnYtd.setter
    def relativeReturnYtd(self, value):
        self.__relativeReturnYtd = value
        self._property_changed('relativeReturnYtd')        

    @property
    def long(self):
        return self.__long

    @long.setter
    def long(self, value):
        self.__long = value
        self._property_changed('long')        

    @property
    def fairVolatility(self):
        return self.__fairVolatility

    @fairVolatility.setter
    def fairVolatility(self, value):
        self.__fairVolatility = value
        self._property_changed('fairVolatility')        

    @property
    def longWeight(self):
        return self.__longWeight

    @longWeight.setter
    def longWeight(self, value):
        self.__longWeight = value
        self._property_changed('longWeight')        

    @property
    def vendor(self):
        return self.__vendor

    @vendor.setter
    def vendor(self, value):
        self.__vendor = value
        self._property_changed('vendor')        

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def clusterClass(self):
        return self.__clusterClass

    @clusterClass.setter
    def clusterClass(self, value):
        self.__clusterClass = value
        self._property_changed('clusterClass')        

    @property
    def financialReturnsScore(self):
        return self.__financialReturnsScore

    @financialReturnsScore.setter
    def financialReturnsScore(self, value):
        self.__financialReturnsScore = value
        self._property_changed('financialReturnsScore')        

    @property
    def netChange(self):
        return self.__netChange

    @netChange.setter
    def netChange(self, value):
        self.__netChange = value
        self._property_changed('netChange')        

    @property
    def nonSymbolDimensions(self) -> Iterable[Any]:
        return self.__nonSymbolDimensions

    @nonSymbolDimensions.setter
    def nonSymbolDimensions(self, value: Iterable[Any]):
        self.__nonSymbolDimensions = value
        self._property_changed('nonSymbolDimensions')        

    @property
    def bidSize(self):
        return self.__bidSize

    @bidSize.setter
    def bidSize(self, value):
        self.__bidSize = value
        self._property_changed('bidSize')        

    @property
    def arrivalMid(self):
        return self.__arrivalMid

    @arrivalMid.setter
    def arrivalMid(self, value):
        self.__arrivalMid = value
        self._property_changed('arrivalMid')        

    @property
    def assetParametersExchangeCurrency(self):
        return self.__assetParametersExchangeCurrency

    @assetParametersExchangeCurrency.setter
    def assetParametersExchangeCurrency(self, value):
        self.__assetParametersExchangeCurrency = value
        self._property_changed('assetParametersExchangeCurrency')        

    @property
    def unexplained(self):
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value):
        self.__unexplained = value
        self._property_changed('unexplained')        

    @property
    def assetClassificationsCountryName(self):
        return self.__assetClassificationsCountryName

    @assetClassificationsCountryName.setter
    def assetClassificationsCountryName(self, value):
        self.__assetClassificationsCountryName = value
        self._property_changed('assetClassificationsCountryName')        

    @property
    def metric(self):
        return self.__metric

    @metric.setter
    def metric(self, value):
        self.__metric = value
        self._property_changed('metric')        

    @property
    def newIdeasYtd(self):
        return self.__newIdeasYtd

    @newIdeasYtd.setter
    def newIdeasYtd(self, value):
        self.__newIdeasYtd = value
        self._property_changed('newIdeasYtd')        

    @property
    def managementFee(self):
        return self.__managementFee

    @managementFee.setter
    def managementFee(self, value):
        self.__managementFee = value
        self._property_changed('managementFee')        

    @property
    def ask(self):
        return self.__ask

    @ask.setter
    def ask(self, value):
        self.__ask = value
        self._property_changed('ask')        

    @property
    def impliedLognormalVolatility(self):
        return self.__impliedLognormalVolatility

    @impliedLognormalVolatility.setter
    def impliedLognormalVolatility(self, value):
        self.__impliedLognormalVolatility = value
        self._property_changed('impliedLognormalVolatility')        

    @property
    def closePrice(self):
        return self.__closePrice

    @closePrice.setter
    def closePrice(self, value):
        self.__closePrice = value
        self._property_changed('closePrice')        

    @property
    def endTime(self):
        return self.__endTime

    @endTime.setter
    def endTime(self, value):
        self.__endTime = value
        self._property_changed('endTime')        

    @property
    def open(self):
        return self.__open

    @open.setter
    def open(self, value):
        self.__open = value
        self._property_changed('open')        

    @property
    def sourceId(self):
        return self.__sourceId

    @sourceId.setter
    def sourceId(self, value):
        self.__sourceId = value
        self._property_changed('sourceId')        

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        self.__country = value
        self._property_changed('country')        

    @property
    def cusip(self):
        return self.__cusip

    @cusip.setter
    def cusip(self, value):
        self.__cusip = value
        self._property_changed('cusip')        

    @property
    def ideaActivityTime(self):
        return self.__ideaActivityTime

    @ideaActivityTime.setter
    def ideaActivityTime(self, value):
        self.__ideaActivityTime = value
        self._property_changed('ideaActivityTime')        

    @property
    def touchSpreadScore(self):
        return self.__touchSpreadScore

    @touchSpreadScore.setter
    def touchSpreadScore(self, value):
        self.__touchSpreadScore = value
        self._property_changed('touchSpreadScore')        

    @property
    def absoluteStrike(self):
        return self.__absoluteStrike

    @absoluteStrike.setter
    def absoluteStrike(self, value):
        self.__absoluteStrike = value
        self._property_changed('absoluteStrike')        

    @property
    def netExposure(self):
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value
        self._property_changed('source')        

    @property
    def assetClassificationsCountryCode(self):
        return self.__assetClassificationsCountryCode

    @assetClassificationsCountryCode.setter
    def assetClassificationsCountryCode(self, value):
        self.__assetClassificationsCountryCode = value
        self._property_changed('assetClassificationsCountryCode')        

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def activityId(self):
        return self.__activityId

    @activityId.setter
    def activityId(self, value):
        self.__activityId = value
        self._property_changed('activityId')        

    @property
    def estimatedImpact(self):
        return self.__estimatedImpact

    @estimatedImpact.setter
    def estimatedImpact(self, value):
        self.__estimatedImpact = value
        self._property_changed('estimatedImpact')        

    @property
    def dataSetSubCategory(self):
        return self.__dataSetSubCategory

    @dataSetSubCategory.setter
    def dataSetSubCategory(self, value):
        self.__dataSetSubCategory = value
        self._property_changed('dataSetSubCategory')        

    @property
    def assetParametersPricingLocation(self):
        return self.__assetParametersPricingLocation

    @assetParametersPricingLocation.setter
    def assetParametersPricingLocation(self, value):
        self.__assetParametersPricingLocation = value
        self._property_changed('assetParametersPricingLocation')        

    @property
    def eventDescription(self):
        return self.__eventDescription

    @eventDescription.setter
    def eventDescription(self, value):
        self.__eventDescription = value
        self._property_changed('eventDescription')        

    @property
    def strikeReference(self):
        return self.__strikeReference

    @strikeReference.setter
    def strikeReference(self, value):
        self.__strikeReference = value
        self._property_changed('strikeReference')        

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, value):
        self.__details = value
        self._property_changed('details')        

    @property
    def assetCount(self):
        return self.__assetCount

    @assetCount.setter
    def assetCount(self, value):
        self.__assetCount = value
        self._property_changed('assetCount')        

    @property
    def absoluteValue(self):
        return self.__absoluteValue

    @absoluteValue.setter
    def absoluteValue(self, value):
        self.__absoluteValue = value
        self._property_changed('absoluteValue')        

    @property
    def delistingDate(self):
        return self.__delistingDate

    @delistingDate.setter
    def delistingDate(self, value):
        self.__delistingDate = value
        self._property_changed('delistingDate')        

    @property
    def longTenor(self):
        return self.__longTenor

    @longTenor.setter
    def longTenor(self, value):
        self.__longTenor = value
        self._property_changed('longTenor')        

    @property
    def mctr(self):
        return self.__mctr

    @mctr.setter
    def mctr(self, value):
        self.__mctr = value
        self._property_changed('mctr')        

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value
        self._property_changed('weight')        

    @property
    def historicalClose(self):
        return self.__historicalClose

    @historicalClose.setter
    def historicalClose(self, value):
        self.__historicalClose = value
        self._property_changed('historicalClose')        

    @property
    def assetCountPriced(self):
        return self.__assetCountPriced

    @assetCountPriced.setter
    def assetCountPriced(self, value):
        self.__assetCountPriced = value
        self._property_changed('assetCountPriced')        

    @property
    def marketDataPoint(self) -> Iterable[Any]:
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value: Iterable[Any]):
        self.__marketDataPoint = value
        self._property_changed('marketDataPoint')        

    @property
    def ideaId(self):
        return self.__ideaId

    @ideaId.setter
    def ideaId(self, value):
        self.__ideaId = value
        self._property_changed('ideaId')        

    @property
    def commentStatus(self):
        return self.__commentStatus

    @commentStatus.setter
    def commentStatus(self, value):
        self.__commentStatus = value
        self._property_changed('commentStatus')        

    @property
    def marginalCost(self):
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def absoluteWeight(self):
        return self.__absoluteWeight

    @absoluteWeight.setter
    def absoluteWeight(self, value):
        self.__absoluteWeight = value
        self._property_changed('absoluteWeight')        

    @property
    def tradeTime(self):
        return self.__tradeTime

    @tradeTime.setter
    def tradeTime(self, value):
        self.__tradeTime = value
        self._property_changed('tradeTime')        

    @property
    def measure(self):
        return self.__measure

    @measure.setter
    def measure(self, value):
        self.__measure = value
        self._property_changed('measure')        

    @property
    def clientWeight(self):
        return self.__clientWeight

    @clientWeight.setter
    def clientWeight(self, value):
        self.__clientWeight = value
        self._property_changed('clientWeight')        

    @property
    def hedgeAnnualizedVolatility(self):
        return self.__hedgeAnnualizedVolatility

    @hedgeAnnualizedVolatility.setter
    def hedgeAnnualizedVolatility(self, value):
        self.__hedgeAnnualizedVolatility = value
        self._property_changed('hedgeAnnualizedVolatility')        

    @property
    def benchmarkCurrency(self):
        return self.__benchmarkCurrency

    @benchmarkCurrency.setter
    def benchmarkCurrency(self, value):
        self.__benchmarkCurrency = value
        self._property_changed('benchmarkCurrency')        

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self._property_changed('name')        

    @property
    def aum(self):
        return self.__aum

    @aum.setter
    def aum(self, value):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def folderName(self):
        return self.__folderName

    @folderName.setter
    def folderName(self, value):
        self.__folderName = value
        self._property_changed('folderName')        

    @property
    def lendingPartnerFee(self):
        return self.__lendingPartnerFee

    @lendingPartnerFee.setter
    def lendingPartnerFee(self, value):
        self.__lendingPartnerFee = value
        self._property_changed('lendingPartnerFee')        

    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, value):
        self.__region = value
        self._property_changed('region')        

    @property
    def liveDate(self):
        return self.__liveDate

    @liveDate.setter
    def liveDate(self, value):
        self.__liveDate = value
        self._property_changed('liveDate')        

    @property
    def askHigh(self):
        return self.__askHigh

    @askHigh.setter
    def askHigh(self, value):
        self.__askHigh = value
        self._property_changed('askHigh')        

    @property
    def corporateActionType(self):
        return self.__corporateActionType

    @corporateActionType.setter
    def corporateActionType(self, value):
        self.__corporateActionType = value
        self._property_changed('corporateActionType')        

    @property
    def primeId(self):
        return self.__primeId

    @primeId.setter
    def primeId(self, value):
        self.__primeId = value
        self._property_changed('primeId')        

    @property
    def tenor2(self):
        return self.__tenor2

    @tenor2.setter
    def tenor2(self, value):
        self.__tenor2 = value
        self._property_changed('tenor2')        

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value
        self._property_changed('description')        

    @property
    def valueRevised(self):
        return self.__valueRevised

    @valueRevised.setter
    def valueRevised(self, value):
        self.__valueRevised = value
        self._property_changed('valueRevised')        

    @property
    def ownerName(self):
        return self.__ownerName

    @ownerName.setter
    def ownerName(self, value):
        self.__ownerName = value
        self._property_changed('ownerName')        

    @property
    def adjustedTradePrice(self):
        return self.__adjustedTradePrice

    @adjustedTradePrice.setter
    def adjustedTradePrice(self, value):
        self.__adjustedTradePrice = value
        self._property_changed('adjustedTradePrice')        

    @property
    def lastUpdatedById(self):
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def zScore(self):
        return self.__zScore

    @zScore.setter
    def zScore(self, value):
        self.__zScore = value
        self._property_changed('zScore')        

    @property
    def targetShareholderMeetingDate(self):
        return self.__targetShareholderMeetingDate

    @targetShareholderMeetingDate.setter
    def targetShareholderMeetingDate(self, value):
        self.__targetShareholderMeetingDate = value
        self._property_changed('targetShareholderMeetingDate')        

    @property
    def isADR(self):
        return self.__isADR

    @isADR.setter
    def isADR(self, value):
        self.__isADR = value
        self._property_changed('isADR')        

    @property
    def eventStartTime(self):
        return self.__eventStartTime

    @eventStartTime.setter
    def eventStartTime(self, value):
        self.__eventStartTime = value
        self._property_changed('eventStartTime')        

    @property
    def factor(self):
        return self.__factor

    @factor.setter
    def factor(self, value):
        self.__factor = value
        self._property_changed('factor')        

    @property
    def longConvictionSmall(self):
        return self.__longConvictionSmall

    @longConvictionSmall.setter
    def longConvictionSmall(self, value):
        self.__longConvictionSmall = value
        self._property_changed('longConvictionSmall')        

    @property
    def serviceId(self):
        return self.__serviceId

    @serviceId.setter
    def serviceId(self, value):
        self.__serviceId = value
        self._property_changed('serviceId')        

    @property
    def turnover(self):
        return self.__turnover

    @turnover.setter
    def turnover(self, value):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def complianceEffectiveTime(self):
        return self.__complianceEffectiveTime

    @complianceEffectiveTime.setter
    def complianceEffectiveTime(self, value):
        self.__complianceEffectiveTime = value
        self._property_changed('complianceEffectiveTime')        

    @property
    def expirationDate(self):
        return self.__expirationDate

    @expirationDate.setter
    def expirationDate(self, value):
        self.__expirationDate = value
        self._property_changed('expirationDate')        

    @property
    def gsfeer(self):
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value):
        self.__gsfeer = value
        self._property_changed('gsfeer')        

    @property
    def coverage(self):
        return self.__coverage

    @coverage.setter
    def coverage(self, value):
        self.__coverage = value
        self._property_changed('coverage')        

    @property
    def backtestId(self):
        return self.__backtestId

    @backtestId.setter
    def backtestId(self, value):
        self.__backtestId = value
        self._property_changed('backtestId')        

    @property
    def gPercentile(self):
        return self.__gPercentile

    @gPercentile.setter
    def gPercentile(self, value):
        self.__gPercentile = value
        self._property_changed('gPercentile')        

    @property
    def gScore(self):
        return self.__gScore

    @gScore.setter
    def gScore(self, value):
        self.__gScore = value
        self._property_changed('gScore')        

    @property
    def marketValue(self):
        return self.__marketValue

    @marketValue.setter
    def marketValue(self, value):
        self.__marketValue = value
        self._property_changed('marketValue')        

    @property
    def multipleScore(self):
        return self.__multipleScore

    @multipleScore.setter
    def multipleScore(self, value):
        self.__multipleScore = value
        self._property_changed('multipleScore')        

    @property
    def sourceOriginalCategory(self):
        return self.__sourceOriginalCategory

    @sourceOriginalCategory.setter
    def sourceOriginalCategory(self, value):
        self.__sourceOriginalCategory = value
        self._property_changed('sourceOriginalCategory')        

    @property
    def betaAdjustedExposure(self):
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def latestExecutionTime(self):
        return self.__latestExecutionTime

    @latestExecutionTime.setter
    def latestExecutionTime(self, value):
        self.__latestExecutionTime = value
        self._property_changed('latestExecutionTime')        

    @property
    def dividendPoints(self):
        return self.__dividendPoints

    @dividendPoints.setter
    def dividendPoints(self, value):
        self.__dividendPoints = value
        self._property_changed('dividendPoints')        

    @property
    def newIdeasWtd(self):
        return self.__newIdeasWtd

    @newIdeasWtd.setter
    def newIdeasWtd(self, value):
        self.__newIdeasWtd = value
        self._property_changed('newIdeasWtd')        

    @property
    def short(self):
        return self.__short

    @short.setter
    def short(self, value):
        self.__short = value
        self._property_changed('short')        

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value
        self._property_changed('location')        

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        self.__comment = value
        self._property_changed('comment')        

    @property
    def bosInTicksDescription(self):
        return self.__bosInTicksDescription

    @bosInTicksDescription.setter
    def bosInTicksDescription(self, value):
        self.__bosInTicksDescription = value
        self._property_changed('bosInTicksDescription')        

    @property
    def sourceSymbol(self):
        return self.__sourceSymbol

    @sourceSymbol.setter
    def sourceSymbol(self, value):
        self.__sourceSymbol = value
        self._property_changed('sourceSymbol')        

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value
        self._property_changed('time')        

    @property
    def scenarioId(self):
        return self.__scenarioId

    @scenarioId.setter
    def scenarioId(self, value):
        self.__scenarioId = value
        self._property_changed('scenarioId')        

    @property
    def askUnadjusted(self):
        return self.__askUnadjusted

    @askUnadjusted.setter
    def askUnadjusted(self, value):
        self.__askUnadjusted = value
        self._property_changed('askUnadjusted')        

    @property
    def queueClockTime(self):
        return self.__queueClockTime

    @queueClockTime.setter
    def queueClockTime(self, value):
        self.__queueClockTime = value
        self._property_changed('queueClockTime')        

    @property
    def askChange(self):
        return self.__askChange

    @askChange.setter
    def askChange(self, value):
        self.__askChange = value
        self._property_changed('askChange')        

    @property
    def tcmCostParticipationRate50Pct(self):
        return self.__tcmCostParticipationRate50Pct

    @tcmCostParticipationRate50Pct.setter
    def tcmCostParticipationRate50Pct(self, value):
        self.__tcmCostParticipationRate50Pct = value
        self._property_changed('tcmCostParticipationRate50Pct')        

    @property
    def normalizedPerformance(self):
        return self.__normalizedPerformance

    @normalizedPerformance.setter
    def normalizedPerformance(self, value):
        self.__normalizedPerformance = value
        self._property_changed('normalizedPerformance')        

    @property
    def cmId(self):
        return self.__cmId

    @cmId.setter
    def cmId(self, value):
        self.__cmId = value
        self._property_changed('cmId')        

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        

    @property
    def mdapi(self):
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def dividendYield(self):
        return self.__dividendYield

    @dividendYield.setter
    def dividendYield(self, value):
        self.__dividendYield = value
        self._property_changed('dividendYield')        

    @property
    def cumulativePnl(self):
        return self.__cumulativePnl

    @cumulativePnl.setter
    def cumulativePnl(self, value):
        self.__cumulativePnl = value
        self._property_changed('cumulativePnl')        

    @property
    def sourceOrigin(self):
        return self.__sourceOrigin

    @sourceOrigin.setter
    def sourceOrigin(self, value):
        self.__sourceOrigin = value
        self._property_changed('sourceOrigin')        

    @property
    def shortTenor(self):
        return self.__shortTenor

    @shortTenor.setter
    def shortTenor(self, value):
        self.__shortTenor = value
        self._property_changed('shortTenor')        

    @property
    def unadjustedVolume(self):
        return self.__unadjustedVolume

    @unadjustedVolume.setter
    def unadjustedVolume(self, value):
        self.__unadjustedVolume = value
        self._property_changed('unadjustedVolume')        

    @property
    def measures(self) -> Iterable[Any]:
        return self.__measures

    @measures.setter
    def measures(self, value: Iterable[Any]):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def tradingCostPnl(self):
        return self.__tradingCostPnl

    @tradingCostPnl.setter
    def tradingCostPnl(self, value):
        self.__tradingCostPnl = value
        self._property_changed('tradingCostPnl')        

    @property
    def internalUser(self):
        return self.__internalUser

    @internalUser.setter
    def internalUser(self, value):
        self.__internalUser = value
        self._property_changed('internalUser')        

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value
        self._property_changed('price')        

    @property
    def paymentQuantity(self):
        return self.__paymentQuantity

    @paymentQuantity.setter
    def paymentQuantity(self, value):
        self.__paymentQuantity = value
        self._property_changed('paymentQuantity')        

    @property
    def underlyer(self):
        return self.__underlyer

    @underlyer.setter
    def underlyer(self, value):
        self.__underlyer = value
        self._property_changed('underlyer')        

    @property
    def createdTime(self):
        return self.__createdTime

    @createdTime.setter
    def createdTime(self, value):
        self.__createdTime = value
        self._property_changed('createdTime')        

    @property
    def positionIdx(self):
        return self.__positionIdx

    @positionIdx.setter
    def positionIdx(self, value):
        self.__positionIdx = value
        self._property_changed('positionIdx')        

    @property
    def secName(self):
        return self.__secName

    @secName.setter
    def secName(self, value):
        self.__secName = value
        self._property_changed('secName')        

    @property
    def percentADV(self):
        return self.__percentADV

    @percentADV.setter
    def percentADV(self, value):
        self.__percentADV = value
        self._property_changed('percentADV')        

    @property
    def unadjustedLow(self):
        return self.__unadjustedLow

    @unadjustedLow.setter
    def unadjustedLow(self, value):
        self.__unadjustedLow = value
        self._property_changed('unadjustedLow')        

    @property
    def contract(self):
        return self.__contract

    @contract.setter
    def contract(self, value):
        self.__contract = value
        self._property_changed('contract')        

    @property
    def sedol(self):
        return self.__sedol

    @sedol.setter
    def sedol(self, value):
        self.__sedol = value
        self._property_changed('sedol')        

    @property
    def roundingCostPnl(self):
        return self.__roundingCostPnl

    @roundingCostPnl.setter
    def roundingCostPnl(self, value):
        self.__roundingCostPnl = value
        self._property_changed('roundingCostPnl')        

    @property
    def sustainGlobal(self):
        return self.__sustainGlobal

    @sustainGlobal.setter
    def sustainGlobal(self, value):
        self.__sustainGlobal = value
        self._property_changed('sustainGlobal')        

    @property
    def sourceTicker(self):
        return self.__sourceTicker

    @sourceTicker.setter
    def sourceTicker(self, value):
        self.__sourceTicker = value
        self._property_changed('sourceTicker')        

    @property
    def portfolioId(self):
        return self.__portfolioId

    @portfolioId.setter
    def portfolioId(self, value):
        self.__portfolioId = value
        self._property_changed('portfolioId')        

    @property
    def gsid(self):
        return self.__gsid

    @gsid.setter
    def gsid(self, value):
        self.__gsid = value
        self._property_changed('gsid')        

    @property
    def esPercentile(self):
        return self.__esPercentile

    @esPercentile.setter
    def esPercentile(self, value):
        self.__esPercentile = value
        self._property_changed('esPercentile')        

    @property
    def tcmCostParticipationRate15Pct(self):
        return self.__tcmCostParticipationRate15Pct

    @tcmCostParticipationRate15Pct.setter
    def tcmCostParticipationRate15Pct(self, value):
        self.__tcmCostParticipationRate15Pct = value
        self._property_changed('tcmCostParticipationRate15Pct')        

    @property
    def sensitivity(self):
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        self.__sensitivity = value
        self._property_changed('sensitivity')        

    @property
    def fiscalYear(self):
        return self.__fiscalYear

    @fiscalYear.setter
    def fiscalYear(self, value):
        self.__fiscalYear = value
        self._property_changed('fiscalYear')        

    @property
    def rcic(self):
        return self.__rcic

    @rcic.setter
    def rcic(self, value):
        self.__rcic = value
        self._property_changed('rcic')        

    @property
    def simonAssetTags(self) -> Iterable[Any]:
        return self.__simonAssetTags

    @simonAssetTags.setter
    def simonAssetTags(self, value: Iterable[Any]):
        self.__simonAssetTags = value
        self._property_changed('simonAssetTags')        

    @property
    def internal(self):
        return self.__internal

    @internal.setter
    def internal(self, value):
        self.__internal = value
        self._property_changed('internal')        

    @property
    def forwardPoint(self):
        return self.__forwardPoint

    @forwardPoint.setter
    def forwardPoint(self, value):
        self.__forwardPoint = value
        self._property_changed('forwardPoint')        

    @property
    def assetClassificationsGicsIndustry(self):
        return self.__assetClassificationsGicsIndustry

    @assetClassificationsGicsIndustry.setter
    def assetClassificationsGicsIndustry(self, value):
        self.__assetClassificationsGicsIndustry = value
        self._property_changed('assetClassificationsGicsIndustry')        

    @property
    def adjustedBidPrice(self):
        return self.__adjustedBidPrice

    @adjustedBidPrice.setter
    def adjustedBidPrice(self, value):
        self.__adjustedBidPrice = value
        self._property_changed('adjustedBidPrice')        

    @property
    def hitRateQtd(self):
        return self.__hitRateQtd

    @hitRateQtd.setter
    def hitRateQtd(self, value):
        self.__hitRateQtd = value
        self._property_changed('hitRateQtd')        

    @property
    def varSwap(self):
        return self.__varSwap

    @varSwap.setter
    def varSwap(self, value):
        self.__varSwap = value
        self._property_changed('varSwap')        

    @property
    def lowUnadjusted(self):
        return self.__lowUnadjusted

    @lowUnadjusted.setter
    def lowUnadjusted(self, value):
        self.__lowUnadjusted = value
        self._property_changed('lowUnadjusted')        

    @property
    def sectorsRaw(self) -> Iterable[Any]:
        return self.__sectorsRaw

    @sectorsRaw.setter
    def sectorsRaw(self, value: Iterable[Any]):
        self.__sectorsRaw = value
        self._property_changed('sectorsRaw')        

    @property
    def low(self):
        return self.__low

    @low.setter
    def low(self, value):
        self.__low = value
        self._property_changed('low')        

    @property
    def crossGroup(self):
        return self.__crossGroup

    @crossGroup.setter
    def crossGroup(self, value):
        self.__crossGroup = value
        self._property_changed('crossGroup')        

    @property
    def integratedScore(self):
        return self.__integratedScore

    @integratedScore.setter
    def integratedScore(self, value):
        self.__integratedScore = value
        self._property_changed('integratedScore')        

    @property
    def reportRunTime(self):
        return self.__reportRunTime

    @reportRunTime.setter
    def reportRunTime(self, value):
        self.__reportRunTime = value
        self._property_changed('reportRunTime')        

    @property
    def tradeSize(self):
        return self.__tradeSize

    @tradeSize.setter
    def tradeSize(self, value):
        self.__tradeSize = value
        self._property_changed('tradeSize')        

    @property
    def symbolDimensions(self) -> Iterable[Any]:
        return self.__symbolDimensions

    @symbolDimensions.setter
    def symbolDimensions(self, value: Iterable[Any]):
        self.__symbolDimensions = value
        self._property_changed('symbolDimensions')        

    @property
    def scenarioGroupId(self):
        return self.__scenarioGroupId

    @scenarioGroupId.setter
    def scenarioGroupId(self, value):
        self.__scenarioGroupId = value
        self._property_changed('scenarioGroupId')        

    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, value):
        self.__errorMessage = value
        self._property_changed('errorMessage')        

    @property
    def avgTradeRateDescription(self):
        return self.__avgTradeRateDescription

    @avgTradeRateDescription.setter
    def avgTradeRateDescription(self, value):
        self.__avgTradeRateDescription = value
        self._property_changed('avgTradeRateDescription')        

    @property
    def midPrice(self):
        return self.__midPrice

    @midPrice.setter
    def midPrice(self, value):
        self.__midPrice = value
        self._property_changed('midPrice')        

    @property
    def fraction(self):
        return self.__fraction

    @fraction.setter
    def fraction(self, value):
        self.__fraction = value
        self._property_changed('fraction')        

    @property
    def stsCreditMarket(self):
        return self.__stsCreditMarket

    @stsCreditMarket.setter
    def stsCreditMarket(self, value):
        self.__stsCreditMarket = value
        self._property_changed('stsCreditMarket')        

    @property
    def assetCountShort(self):
        return self.__assetCountShort

    @assetCountShort.setter
    def assetCountShort(self, value):
        self.__assetCountShort = value
        self._property_changed('assetCountShort')        

    @property
    def stsEmDm(self):
        return self.__stsEmDm

    @stsEmDm.setter
    def stsEmDm(self, value):
        self.__stsEmDm = value
        self._property_changed('stsEmDm')        

    @property
    def tcmCostHorizon2Day(self):
        return self.__tcmCostHorizon2Day

    @tcmCostHorizon2Day.setter
    def tcmCostHorizon2Day(self, value):
        self.__tcmCostHorizon2Day = value
        self._property_changed('tcmCostHorizon2Day')        

    @property
    def queueInLots(self):
        return self.__queueInLots

    @queueInLots.setter
    def queueInLots(self, value):
        self.__queueInLots = value
        self._property_changed('queueInLots')        

    @property
    def priceRangeInTicksDescription(self):
        return self.__priceRangeInTicksDescription

    @priceRangeInTicksDescription.setter
    def priceRangeInTicksDescription(self, value):
        self.__priceRangeInTicksDescription = value
        self._property_changed('priceRangeInTicksDescription')        

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value
        self._property_changed('date')        

    @property
    def tenderOfferExpirationDate(self):
        return self.__tenderOfferExpirationDate

    @tenderOfferExpirationDate.setter
    def tenderOfferExpirationDate(self, value):
        self.__tenderOfferExpirationDate = value
        self._property_changed('tenderOfferExpirationDate')        

    @property
    def highUnadjusted(self):
        return self.__highUnadjusted

    @highUnadjusted.setter
    def highUnadjusted(self, value):
        self.__highUnadjusted = value
        self._property_changed('highUnadjusted')        

    @property
    def sourceCategory(self):
        return self.__sourceCategory

    @sourceCategory.setter
    def sourceCategory(self, value):
        self.__sourceCategory = value
        self._property_changed('sourceCategory')        

    @property
    def volumeUnadjusted(self):
        return self.__volumeUnadjusted

    @volumeUnadjusted.setter
    def volumeUnadjusted(self, value):
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
    def tcmCostParticipationRate5Pct(self):
        return self.__tcmCostParticipationRate5Pct

    @tcmCostParticipationRate5Pct.setter
    def tcmCostParticipationRate5Pct(self, value):
        self.__tcmCostParticipationRate5Pct = value
        self._property_changed('tcmCostParticipationRate5Pct')        

    @property
    def isActive(self):
        return self.__isActive

    @isActive.setter
    def isActive(self, value):
        self.__isActive = value
        self._property_changed('isActive')        

    @property
    def growthScore(self):
        return self.__growthScore

    @growthScore.setter
    def growthScore(self, value):
        self.__growthScore = value
        self._property_changed('growthScore')        

    @property
    def encodedStats(self):
        return self.__encodedStats

    @encodedStats.setter
    def encodedStats(self, value):
        self.__encodedStats = value
        self._property_changed('encodedStats')        

    @property
    def adjustedShortInterest(self):
        return self.__adjustedShortInterest

    @adjustedShortInterest.setter
    def adjustedShortInterest(self, value):
        self.__adjustedShortInterest = value
        self._property_changed('adjustedShortInterest')        

    @property
    def askSize(self):
        return self.__askSize

    @askSize.setter
    def askSize(self, value):
        self.__askSize = value
        self._property_changed('askSize')        

    @property
    def mdapiType(self):
        return self.__mdapiType

    @mdapiType.setter
    def mdapiType(self, value):
        self.__mdapiType = value
        self._property_changed('mdapiType')        

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value
        self._property_changed('group')        

    @property
    def estimatedSpread(self):
        return self.__estimatedSpread

    @estimatedSpread.setter
    def estimatedSpread(self, value):
        self.__estimatedSpread = value
        self._property_changed('estimatedSpread')        

    @property
    def resource(self):
        return self.__resource

    @resource.setter
    def resource(self, value):
        self.__resource = value
        self._property_changed('resource')        

    @property
    def created(self):
        return self.__created

    @created.setter
    def created(self, value):
        self.__created = value
        self._property_changed('created')        

    @property
    def tcmCost(self):
        return self.__tcmCost

    @tcmCost.setter
    def tcmCost(self, value):
        self.__tcmCost = value
        self._property_changed('tcmCost')        

    @property
    def sustainJapan(self):
        return self.__sustainJapan

    @sustainJapan.setter
    def sustainJapan(self, value):
        self.__sustainJapan = value
        self._property_changed('sustainJapan')        

    @property
    def navSpread(self):
        return self.__navSpread

    @navSpread.setter
    def navSpread(self, value):
        self.__navSpread = value
        self._property_changed('navSpread')        

    @property
    def bidPrice(self):
        return self.__bidPrice

    @bidPrice.setter
    def bidPrice(self, value):
        self.__bidPrice = value
        self._property_changed('bidPrice')        

    @property
    def hedgeTrackingError(self):
        return self.__hedgeTrackingError

    @hedgeTrackingError.setter
    def hedgeTrackingError(self, value):
        self.__hedgeTrackingError = value
        self._property_changed('hedgeTrackingError')        

    @property
    def marketCapCategory(self):
        return self.__marketCapCategory

    @marketCapCategory.setter
    def marketCapCategory(self, value):
        self.__marketCapCategory = value
        self._property_changed('marketCapCategory')        

    @property
    def historicalVolume(self):
        return self.__historicalVolume

    @historicalVolume.setter
    def historicalVolume(self, value):
        self.__historicalVolume = value
        self._property_changed('historicalVolume')        

    @property
    def esNumericPercentile(self):
        return self.__esNumericPercentile

    @esNumericPercentile.setter
    def esNumericPercentile(self, value):
        self.__esNumericPercentile = value
        self._property_changed('esNumericPercentile')        

    @property
    def strikePrice(self):
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def eventStartDate(self):
        return self.__eventStartDate

    @eventStartDate.setter
    def eventStartDate(self, value):
        self.__eventStartDate = value
        self._property_changed('eventStartDate')        

    @property
    def calSpreadMisPricing(self):
        return self.__calSpreadMisPricing

    @calSpreadMisPricing.setter
    def calSpreadMisPricing(self, value):
        self.__calSpreadMisPricing = value
        self._property_changed('calSpreadMisPricing')        

    @property
    def equityGamma(self):
        return self.__equityGamma

    @equityGamma.setter
    def equityGamma(self, value):
        self.__equityGamma = value
        self._property_changed('equityGamma')        

    @property
    def grossIncome(self):
        return self.__grossIncome

    @grossIncome.setter
    def grossIncome(self, value):
        self.__grossIncome = value
        self._property_changed('grossIncome')        

    @property
    def emId(self):
        return self.__emId

    @emId.setter
    def emId(self, value):
        self.__emId = value
        self._property_changed('emId')        

    @property
    def adjustedOpenPrice(self):
        return self.__adjustedOpenPrice

    @adjustedOpenPrice.setter
    def adjustedOpenPrice(self, value):
        self.__adjustedOpenPrice = value
        self._property_changed('adjustedOpenPrice')        

    @property
    def assetCountInModel(self):
        return self.__assetCountInModel

    @assetCountInModel.setter
    def assetCountInModel(self, value):
        self.__assetCountInModel = value
        self._property_changed('assetCountInModel')        

    @property
    def stsCreditRegion(self):
        return self.__stsCreditRegion

    @stsCreditRegion.setter
    def stsCreditRegion(self, value):
        self.__stsCreditRegion = value
        self._property_changed('stsCreditRegion')        

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        self.__point = value
        self._property_changed('point')        

    @property
    def lender(self):
        return self.__lender

    @lender.setter
    def lender(self, value):
        self.__lender = value
        self._property_changed('lender')        

    @property
    def minTemperature(self):
        return self.__minTemperature

    @minTemperature.setter
    def minTemperature(self, value):
        self.__minTemperature = value
        self._property_changed('minTemperature')        

    @property
    def closeTime(self):
        return self.__closeTime

    @closeTime.setter
    def closeTime(self, value):
        self.__closeTime = value
        self._property_changed('closeTime')        

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self._property_changed('value')        

    @property
    def relativeStrike(self):
        return self.__relativeStrike

    @relativeStrike.setter
    def relativeStrike(self, value):
        self.__relativeStrike = value
        self._property_changed('relativeStrike')        

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = value
        self._property_changed('amount')        

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def reportId(self):
        return self.__reportId

    @reportId.setter
    def reportId(self, value):
        self.__reportId = value
        self._property_changed('reportId')        

    @property
    def indexWeight(self):
        return self.__indexWeight

    @indexWeight.setter
    def indexWeight(self, value):
        self.__indexWeight = value
        self._property_changed('indexWeight')        

    @property
    def rebate(self):
        return self.__rebate

    @rebate.setter
    def rebate(self, value):
        self.__rebate = value
        self._property_changed('rebate')        

    @property
    def trader(self):
        return self.__trader

    @trader.setter
    def trader(self, value):
        self.__trader = value
        self._property_changed('trader')        

    @property
    def factorCategory(self):
        return self.__factorCategory

    @factorCategory.setter
    def factorCategory(self, value):
        self.__factorCategory = value
        self._property_changed('factorCategory')        

    @property
    def impliedVolatility(self):
        return self.__impliedVolatility

    @impliedVolatility.setter
    def impliedVolatility(self, value):
        self.__impliedVolatility = value
        self._property_changed('impliedVolatility')        

    @property
    def spread(self):
        return self.__spread

    @spread.setter
    def spread(self, value):
        self.__spread = value
        self._property_changed('spread')        

    @property
    def stsRatesMaturity(self):
        return self.__stsRatesMaturity

    @stsRatesMaturity.setter
    def stsRatesMaturity(self, value):
        self.__stsRatesMaturity = value
        self._property_changed('stsRatesMaturity')        

    @property
    def equityDelta(self):
        return self.__equityDelta

    @equityDelta.setter
    def equityDelta(self, value):
        self.__equityDelta = value
        self._property_changed('equityDelta')        

    @property
    def grossWeight(self):
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def listed(self):
        return self.__listed

    @listed.setter
    def listed(self, value):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def tcmCostHorizon6Hour(self):
        return self.__tcmCostHorizon6Hour

    @tcmCostHorizon6Hour.setter
    def tcmCostHorizon6Hour(self, value):
        self.__tcmCostHorizon6Hour = value
        self._property_changed('tcmCostHorizon6Hour')        

    @property
    def g10Currency(self):
        return self.__g10Currency

    @g10Currency.setter
    def g10Currency(self, value):
        self.__g10Currency = value
        self._property_changed('g10Currency')        

    @property
    def shockStyle(self):
        return self.__shockStyle

    @shockStyle.setter
    def shockStyle(self, value):
        self.__shockStyle = value
        self._property_changed('shockStyle')        

    @property
    def relativePeriod(self):
        return self.__relativePeriod

    @relativePeriod.setter
    def relativePeriod(self, value):
        self.__relativePeriod = value
        self._property_changed('relativePeriod')        

    @property
    def isin(self):
        return self.__isin

    @isin.setter
    def isin(self, value):
        self.__isin = value
        self._property_changed('isin')        

    @property
    def methodology(self):
        return self.__methodology

    @methodology.setter
    def methodology(self, value):
        self.__methodology = value
        self._property_changed('methodology')        


class MarketDataCoordinate(Base):
        
    """Object representation of a market data coordinate"""
       
    def __init__(self, marketDataType: str, field: str, assetId: Union[str, str] = None, marketDataAsset: str = None, pointClass: str = None, marketDataPoint: Iterable[str] = None):
        super().__init__()
        self.__marketDataType = marketDataType
        self.__assetId = assetId
        self.__marketDataAsset = marketDataAsset
        self.__pointClass = pointClass
        self.__marketDataPoint = marketDataPoint
        self.__field = field

    @property
    def marketDataType(self) -> str:
        """The Market Data Type, e.g. IR, IR_BASIS, FX, FX_Vol"""
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value: str):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def assetId(self) -> Union[str, str]:
        """Marquee unique asset identifier."""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def marketDataAsset(self) -> str:
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value: str):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def pointClass(self) -> str:
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value: str):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def marketDataPoint(self) -> Iterable[str]:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value: Iterable[str]):
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


class Entitlements(Base):
        
    """Defines the entitlements of a given resource"""
       
    def __init__(self, view=None, edit=None, admin=None, rebalance=None, trade=None, upload=None, query=None, performanceDetails=None):
        super().__init__()
        self.__view = view
        self.__edit = edit
        self.__admin = admin
        self.__rebalance = rebalance
        self.__trade = trade
        self.__upload = upload
        self.__query = query
        self.__performanceDetails = performanceDetails

    @property
    def view(self):
        """Permission to view the resource and its contents"""
        return self.__view

    @view.setter
    def view(self, value):
        self.__view = value
        self._property_changed('view')        

    @property
    def edit(self):
        """Permission to edit details about the resource content, excluding entitlements. Can also delete the resource"""
        return self.__edit

    @edit.setter
    def edit(self, value):
        self.__edit = value
        self._property_changed('edit')        

    @property
    def admin(self):
        """Permission to edit all details of the resource, including entitlements. Can also delete the resource"""
        return self.__admin

    @admin.setter
    def admin(self, value):
        self.__admin = value
        self._property_changed('admin')        

    @property
    def rebalance(self):
        """Permission to rebalance the constituent weights of the resource"""
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value):
        self.__rebalance = value
        self._property_changed('rebalance')        

    @property
    def trade(self):
        """Permission to trade the resource"""
        return self.__trade

    @trade.setter
    def trade(self, value):
        self.__trade = value
        self._property_changed('trade')        

    @property
    def upload(self):
        """Permission to upload data to the given resource"""
        return self.__upload

    @upload.setter
    def upload(self, value):
        self.__upload = value
        self._property_changed('upload')        

    @property
    def query(self):
        """Permission to query data from the give resource"""
        return self.__query

    @query.setter
    def query(self, value):
        self.__query = value
        self._property_changed('query')        

    @property
    def performanceDetails(self):
        """Permission to view the resource, it's entire contents, and related data"""
        return self.__performanceDetails

    @performanceDetails.setter
    def performanceDetails(self, value):
        self.__performanceDetails = value
        self._property_changed('performanceDetails')        


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
        self.__cid = kwargs.get('cid')
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
        self.__gsn = kwargs.get('gsn')
        self.__isAggressive = kwargs.get('isAggressive')
        self.__orderId = kwargs.get('orderId')
        self.__gss = kwargs.get('gss')
        self.__percentOfMediandv1m = kwargs.get('percentOfMediandv1m')
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
        self.__objective = kwargs.get('objective')
        self.__navPrice = kwargs.get('navPrice')
        self.__ideaActivityType = kwargs.get('ideaActivityType')
        self.__precipitation = kwargs.get('precipitation')
        self.__ideaSource = kwargs.get('ideaSource')
        self.__hedgeNotional = kwargs.get('hedgeNotional')
        self.__askLow = kwargs.get('askLow')
        self.__unadjustedAsk = kwargs.get('unadjustedAsk')
        self.__expiry = kwargs.get('expiry')
        self.__tradingPnl = kwargs.get('tradingPnl')
        self.__strikePercentage = kwargs.get('strikePercentage')
        self.__excessReturnPrice = kwargs.get('excessReturnPrice')
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
        self.__sourceOriginalCategory = kwargs.get('sourceOriginalCategory')
        self.__betaAdjustedExposure = kwargs.get('betaAdjustedExposure')
        self.__dividendPoints = kwargs.get('dividendPoints')
        self.__newIdeasWtd = kwargs.get('newIdeasWtd')
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
        self.__tradeSize = kwargs.get('tradeSize')
        self.__symbolDimensions = kwargs.get('symbolDimensions')
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
    def marketPnl(self):
        return self.__marketPnl

    @marketPnl.setter
    def marketPnl(self, value):
        self.__marketPnl = value
        self._property_changed('marketPnl')        

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value
        self._property_changed('year')        

    @property
    def sustainAsiaExJapan(self):
        return self.__sustainAsiaExJapan

    @sustainAsiaExJapan.setter
    def sustainAsiaExJapan(self, value):
        self.__sustainAsiaExJapan = value
        self._property_changed('sustainAsiaExJapan')        

    @property
    def investmentRate(self):
        return self.__investmentRate

    @investmentRate.setter
    def investmentRate(self, value):
        self.__investmentRate = value
        self._property_changed('investmentRate')        

    @property
    def assetClassificationsGicsSubIndustry(self):
        return self.__assetClassificationsGicsSubIndustry

    @assetClassificationsGicsSubIndustry.setter
    def assetClassificationsGicsSubIndustry(self, value):
        self.__assetClassificationsGicsSubIndustry = value
        self._property_changed('assetClassificationsGicsSubIndustry')        

    @property
    def bidUnadjusted(self):
        return self.__bidUnadjusted

    @bidUnadjusted.setter
    def bidUnadjusted(self, value):
        self.__bidUnadjusted = value
        self._property_changed('bidUnadjusted')        

    @property
    def economicTermsHash(self):
        return self.__economicTermsHash

    @economicTermsHash.setter
    def economicTermsHash(self, value):
        self.__economicTermsHash = value
        self._property_changed('economicTermsHash')        

    @property
    def neighbourAssetId(self):
        return self.__neighbourAssetId

    @neighbourAssetId.setter
    def neighbourAssetId(self, value):
        self.__neighbourAssetId = value
        self._property_changed('neighbourAssetId')        

    @property
    def simonIntlAssetTags(self):
        return self.__simonIntlAssetTags

    @simonIntlAssetTags.setter
    def simonIntlAssetTags(self, value):
        self.__simonIntlAssetTags = value
        self._property_changed('simonIntlAssetTags')        

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value
        self._property_changed('path')        

    @property
    def availableInventory(self):
        return self.__availableInventory

    @availableInventory.setter
    def availableInventory(self, value):
        self.__availableInventory = value
        self._property_changed('availableInventory')        

    @property
    def clientContact(self):
        return self.__clientContact

    @clientContact.setter
    def clientContact(self, value):
        self.__clientContact = value
        self._property_changed('clientContact')        

    @property
    def est1DayCompletePct(self):
        return self.__est1DayCompletePct

    @est1DayCompletePct.setter
    def est1DayCompletePct(self, value):
        self.__est1DayCompletePct = value
        self._property_changed('est1DayCompletePct')        

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, value):
        self.__rank = value
        self._property_changed('rank')        

    @property
    def dataSetCategory(self):
        return self.__dataSetCategory

    @dataSetCategory.setter
    def dataSetCategory(self, value):
        self.__dataSetCategory = value
        self._property_changed('dataSetCategory')        

    @property
    def createdById(self):
        return self.__createdById

    @createdById.setter
    def createdById(self, value):
        self.__createdById = value
        self._property_changed('createdById')        

    @property
    def vehicleType(self):
        return self.__vehicleType

    @vehicleType.setter
    def vehicleType(self, value):
        self.__vehicleType = value
        self._property_changed('vehicleType')        

    @property
    def dailyRisk(self):
        return self.__dailyRisk

    @dailyRisk.setter
    def dailyRisk(self, value):
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
    def marketDataType(self):
        return self.__marketDataType

    @marketDataType.setter
    def marketDataType(self, value):
        self.__marketDataType = value
        self._property_changed('marketDataType')        

    @property
    def sentimentScore(self):
        return self.__sentimentScore

    @sentimentScore.setter
    def sentimentScore(self, value):
        self.__sentimentScore = value
        self._property_changed('sentimentScore')        

    @property
    def bosInBps(self):
        return self.__bosInBps

    @bosInBps.setter
    def bosInBps(self, value):
        self.__bosInBps = value
        self._property_changed('bosInBps')        

    @property
    def pointClass(self):
        return self.__pointClass

    @pointClass.setter
    def pointClass(self, value):
        self.__pointClass = value
        self._property_changed('pointClass')        

    @property
    def fxSpot(self):
        return self.__fxSpot

    @fxSpot.setter
    def fxSpot(self, value):
        self.__fxSpot = value
        self._property_changed('fxSpot')        

    @property
    def bidLow(self):
        return self.__bidLow

    @bidLow.setter
    def bidLow(self, value):
        self.__bidLow = value
        self._property_changed('bidLow')        

    @property
    def valuePrevious(self):
        return self.__valuePrevious

    @valuePrevious.setter
    def valuePrevious(self, value):
        self.__valuePrevious = value
        self._property_changed('valuePrevious')        

    @property
    def fairVarianceVolatility(self):
        return self.__fairVarianceVolatility

    @fairVarianceVolatility.setter
    def fairVarianceVolatility(self, value):
        self.__fairVarianceVolatility = value
        self._property_changed('fairVarianceVolatility')        

    @property
    def avgTradeRate(self):
        return self.__avgTradeRate

    @avgTradeRate.setter
    def avgTradeRate(self, value):
        self.__avgTradeRate = value
        self._property_changed('avgTradeRate')        

    @property
    def shortLevel(self):
        return self.__shortLevel

    @shortLevel.setter
    def shortLevel(self, value):
        self.__shortLevel = value
        self._property_changed('shortLevel')        

    @property
    def hedgeVolatility(self):
        return self.__hedgeVolatility

    @hedgeVolatility.setter
    def hedgeVolatility(self, value):
        self.__hedgeVolatility = value
        self._property_changed('hedgeVolatility')        

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value
        self._property_changed('version')        

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, value):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def underlyingAssetId(self):
        return self.__underlyingAssetId

    @underlyingAssetId.setter
    def underlyingAssetId(self, value):
        self.__underlyingAssetId = value
        self._property_changed('underlyingAssetId')        

    @property
    def clientExposure(self):
        return self.__clientExposure

    @clientExposure.setter
    def clientExposure(self, value):
        self.__clientExposure = value
        self._property_changed('clientExposure')        

    @property
    def correlation(self):
        return self.__correlation

    @correlation.setter
    def correlation(self, value):
        self.__correlation = value
        self._property_changed('correlation')        

    @property
    def exposure(self):
        return self.__exposure

    @exposure.setter
    def exposure(self, value):
        self.__exposure = value
        self._property_changed('exposure')        

    @property
    def gsSustainSubSector(self):
        return self.__gsSustainSubSector

    @gsSustainSubSector.setter
    def gsSustainSubSector(self, value):
        self.__gsSustainSubSector = value
        self._property_changed('gsSustainSubSector')        

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, value):
        self.__domain = value
        self._property_changed('domain')        

    @property
    def marketDataAsset(self):
        return self.__marketDataAsset

    @marketDataAsset.setter
    def marketDataAsset(self, value):
        self.__marketDataAsset = value
        self._property_changed('marketDataAsset')        

    @property
    def forwardTenor(self):
        return self.__forwardTenor

    @forwardTenor.setter
    def forwardTenor(self, value):
        self.__forwardTenor = value
        self._property_changed('forwardTenor')        

    @property
    def unadjustedHigh(self):
        return self.__unadjustedHigh

    @unadjustedHigh.setter
    def unadjustedHigh(self, value):
        self.__unadjustedHigh = value
        self._property_changed('unadjustedHigh')        

    @property
    def sourceImportance(self):
        return self.__sourceImportance

    @sourceImportance.setter
    def sourceImportance(self, value):
        self.__sourceImportance = value
        self._property_changed('sourceImportance')        

    @property
    def eid(self):
        return self.__eid

    @eid.setter
    def eid(self, value):
        self.__eid = value
        self._property_changed('eid')        

    @property
    def jsn(self):
        return self.__jsn

    @jsn.setter
    def jsn(self, value):
        self.__jsn = value
        self._property_changed('jsn')        

    @property
    def relativeReturnQtd(self):
        return self.__relativeReturnQtd

    @relativeReturnQtd.setter
    def relativeReturnQtd(self, value):
        self.__relativeReturnQtd = value
        self._property_changed('relativeReturnQtd')        

    @property
    def displayName(self):
        return self.__displayName

    @displayName.setter
    def displayName(self, value):
        self.__displayName = value
        self._property_changed('displayName')        

    @property
    def minutesToTrade100Pct(self):
        return self.__minutesToTrade100Pct

    @minutesToTrade100Pct.setter
    def minutesToTrade100Pct(self, value):
        self.__minutesToTrade100Pct = value
        self._property_changed('minutesToTrade100Pct')        

    @property
    def marketModelId(self):
        return self.__marketModelId

    @marketModelId.setter
    def marketModelId(self, value):
        self.__marketModelId = value
        self._property_changed('marketModelId')        

    @property
    def quoteType(self):
        return self.__quoteType

    @quoteType.setter
    def quoteType(self, value):
        self.__quoteType = value
        self._property_changed('quoteType')        

    @property
    def tenor(self):
        return self.__tenor

    @tenor.setter
    def tenor(self, value):
        self.__tenor = value
        self._property_changed('tenor')        

    @property
    def esPolicyPercentile(self):
        return self.__esPolicyPercentile

    @esPolicyPercentile.setter
    def esPolicyPercentile(self, value):
        self.__esPolicyPercentile = value
        self._property_changed('esPolicyPercentile')        

    @property
    def tcmCostParticipationRate75Pct(self):
        return self.__tcmCostParticipationRate75Pct

    @tcmCostParticipationRate75Pct.setter
    def tcmCostParticipationRate75Pct(self, value):
        self.__tcmCostParticipationRate75Pct = value
        self._property_changed('tcmCostParticipationRate75Pct')        

    @property
    def close(self):
        return self.__close

    @close.setter
    def close(self, value):
        self.__close = value
        self._property_changed('close')        

    @property
    def tcmCostParticipationRate100Pct(self):
        return self.__tcmCostParticipationRate100Pct

    @tcmCostParticipationRate100Pct.setter
    def tcmCostParticipationRate100Pct(self, value):
        self.__tcmCostParticipationRate100Pct = value
        self._property_changed('tcmCostParticipationRate100Pct')        

    @property
    def disclaimer(self):
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value):
        self.__disclaimer = value
        self._property_changed('disclaimer')        

    @property
    def measureIdx(self):
        return self.__measureIdx

    @measureIdx.setter
    def measureIdx(self, value):
        self.__measureIdx = value
        self._property_changed('measureIdx')        

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value
        self._property_changed('a')        

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = value
        self._property_changed('b')        

    @property
    def loanFee(self):
        return self.__loanFee

    @loanFee.setter
    def loanFee(self, value):
        self.__loanFee = value
        self._property_changed('loanFee')        

    @property
    def c(self):
        return self.__c

    @c.setter
    def c(self, value):
        self.__c = value
        self._property_changed('c')        

    @property
    def equityVega(self):
        return self.__equityVega

    @equityVega.setter
    def equityVega(self, value):
        self.__equityVega = value
        self._property_changed('equityVega')        

    @property
    def deploymentVersion(self):
        return self.__deploymentVersion

    @deploymentVersion.setter
    def deploymentVersion(self, value):
        self.__deploymentVersion = value
        self._property_changed('deploymentVersion')        

    @property
    def fiveDayMove(self):
        return self.__fiveDayMove

    @fiveDayMove.setter
    def fiveDayMove(self, value):
        self.__fiveDayMove = value
        self._property_changed('fiveDayMove')        

    @property
    def borrower(self):
        return self.__borrower

    @borrower.setter
    def borrower(self, value):
        self.__borrower = value
        self._property_changed('borrower')        

    @property
    def performanceContribution(self):
        return self.__performanceContribution

    @performanceContribution.setter
    def performanceContribution(self, value):
        self.__performanceContribution = value
        self._property_changed('performanceContribution')        

    @property
    def targetNotional(self):
        return self.__targetNotional

    @targetNotional.setter
    def targetNotional(self, value):
        self.__targetNotional = value
        self._property_changed('targetNotional')        

    @property
    def fillLegId(self):
        return self.__fillLegId

    @fillLegId.setter
    def fillLegId(self, value):
        self.__fillLegId = value
        self._property_changed('fillLegId')        

    @property
    def rationale(self):
        return self.__rationale

    @rationale.setter
    def rationale(self, value):
        self.__rationale = value
        self._property_changed('rationale')        

    @property
    def regionalFocus(self):
        return self.__regionalFocus

    @regionalFocus.setter
    def regionalFocus(self, value):
        self.__regionalFocus = value
        self._property_changed('regionalFocus')        

    @property
    def volumePrimary(self):
        return self.__volumePrimary

    @volumePrimary.setter
    def volumePrimary(self, value):
        self.__volumePrimary = value
        self._property_changed('volumePrimary')        

    @property
    def series(self):
        return self.__series

    @series.setter
    def series(self, value):
        self.__series = value
        self._property_changed('series')        

    @property
    def simonId(self):
        return self.__simonId

    @simonId.setter
    def simonId(self, value):
        self.__simonId = value
        self._property_changed('simonId')        

    @property
    def newIdeasQtd(self):
        return self.__newIdeasQtd

    @newIdeasQtd.setter
    def newIdeasQtd(self, value):
        self.__newIdeasQtd = value
        self._property_changed('newIdeasQtd')        

    @property
    def adjustedAskPrice(self):
        return self.__adjustedAskPrice

    @adjustedAskPrice.setter
    def adjustedAskPrice(self, value):
        self.__adjustedAskPrice = value
        self._property_changed('adjustedAskPrice')        

    @property
    def quarter(self):
        return self.__quarter

    @quarter.setter
    def quarter(self, value):
        self.__quarter = value
        self._property_changed('quarter')        

    @property
    def factorUniverse(self):
        return self.__factorUniverse

    @factorUniverse.setter
    def factorUniverse(self, value):
        self.__factorUniverse = value
        self._property_changed('factorUniverse')        

    @property
    def eventCategory(self):
        return self.__eventCategory

    @eventCategory.setter
    def eventCategory(self, value):
        self.__eventCategory = value
        self._property_changed('eventCategory')        

    @property
    def impliedNormalVolatility(self):
        return self.__impliedNormalVolatility

    @impliedNormalVolatility.setter
    def impliedNormalVolatility(self, value):
        self.__impliedNormalVolatility = value
        self._property_changed('impliedNormalVolatility')        

    @property
    def unadjustedOpen(self):
        return self.__unadjustedOpen

    @unadjustedOpen.setter
    def unadjustedOpen(self, value):
        self.__unadjustedOpen = value
        self._property_changed('unadjustedOpen')        

    @property
    def arrivalRt(self):
        return self.__arrivalRt

    @arrivalRt.setter
    def arrivalRt(self, value):
        self.__arrivalRt = value
        self._property_changed('arrivalRt')        

    @property
    def transactionCost(self):
        return self.__transactionCost

    @transactionCost.setter
    def transactionCost(self, value):
        self.__transactionCost = value
        self._property_changed('transactionCost')        

    @property
    def servicingCostShortPnl(self):
        return self.__servicingCostShortPnl

    @servicingCostShortPnl.setter
    def servicingCostShortPnl(self, value):
        self.__servicingCostShortPnl = value
        self._property_changed('servicingCostShortPnl')        

    @property
    def bidAskSpread(self):
        return self.__bidAskSpread

    @bidAskSpread.setter
    def bidAskSpread(self, value):
        self.__bidAskSpread = value
        self._property_changed('bidAskSpread')        

    @property
    def optionType(self):
        return self.__optionType

    @optionType.setter
    def optionType(self, value):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def tcmCostHorizon3Hour(self):
        return self.__tcmCostHorizon3Hour

    @tcmCostHorizon3Hour.setter
    def tcmCostHorizon3Hour(self, value):
        self.__tcmCostHorizon3Hour = value
        self._property_changed('tcmCostHorizon3Hour')        

    @property
    def clusterDescription(self):
        return self.__clusterDescription

    @clusterDescription.setter
    def clusterDescription(self, value):
        self.__clusterDescription = value
        self._property_changed('clusterDescription')        

    @property
    def positionAmount(self):
        return self.__positionAmount

    @positionAmount.setter
    def positionAmount(self, value):
        self.__positionAmount = value
        self._property_changed('positionAmount')        

    @property
    def numberOfPositions(self):
        return self.__numberOfPositions

    @numberOfPositions.setter
    def numberOfPositions(self, value):
        self.__numberOfPositions = value
        self._property_changed('numberOfPositions')        

    @property
    def windSpeed(self):
        return self.__windSpeed

    @windSpeed.setter
    def windSpeed(self, value):
        self.__windSpeed = value
        self._property_changed('windSpeed')        

    @property
    def openUnadjusted(self):
        return self.__openUnadjusted

    @openUnadjusted.setter
    def openUnadjusted(self, value):
        self.__openUnadjusted = value
        self._property_changed('openUnadjusted')        

    @property
    def maRank(self):
        return self.__maRank

    @maRank.setter
    def maRank(self, value):
        self.__maRank = value
        self._property_changed('maRank')        

    @property
    def askPrice(self):
        return self.__askPrice

    @askPrice.setter
    def askPrice(self, value):
        self.__askPrice = value
        self._property_changed('askPrice')        

    @property
    def eventId(self):
        return self.__eventId

    @eventId.setter
    def eventId(self, value):
        self.__eventId = value
        self._property_changed('eventId')        

    @property
    def dataProduct(self):
        return self.__dataProduct

    @dataProduct.setter
    def dataProduct(self, value):
        self.__dataProduct = value
        self._property_changed('dataProduct')        

    @property
    def sectors(self):
        return self.__sectors

    @sectors.setter
    def sectors(self, value):
        self.__sectors = value
        self._property_changed('sectors')        

    @property
    def annualizedTrackingError(self):
        return self.__annualizedTrackingError

    @annualizedTrackingError.setter
    def annualizedTrackingError(self, value):
        self.__annualizedTrackingError = value
        self._property_changed('annualizedTrackingError')        

    @property
    def volSwap(self):
        return self.__volSwap

    @volSwap.setter
    def volSwap(self, value):
        self.__volSwap = value
        self._property_changed('volSwap')        

    @property
    def annualizedRisk(self):
        return self.__annualizedRisk

    @annualizedRisk.setter
    def annualizedRisk(self, value):
        self.__annualizedRisk = value
        self._property_changed('annualizedRisk')        

    @property
    def corporateAction(self):
        return self.__corporateAction

    @corporateAction.setter
    def corporateAction(self, value):
        self.__corporateAction = value
        self._property_changed('corporateAction')        

    @property
    def conviction(self):
        return self.__conviction

    @conviction.setter
    def conviction(self, value):
        self.__conviction = value
        self._property_changed('conviction')        

    @property
    def grossExposure(self):
        return self.__grossExposure

    @grossExposure.setter
    def grossExposure(self, value):
        self.__grossExposure = value
        self._property_changed('grossExposure')        

    @property
    def benchmarkMaturity(self):
        return self.__benchmarkMaturity

    @benchmarkMaturity.setter
    def benchmarkMaturity(self, value):
        self.__benchmarkMaturity = value
        self._property_changed('benchmarkMaturity')        

    @property
    def volumeComposite(self):
        return self.__volumeComposite

    @volumeComposite.setter
    def volumeComposite(self, value):
        self.__volumeComposite = value
        self._property_changed('volumeComposite')        

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        self.__volume = value
        self._property_changed('volume')        

    @property
    def adv(self):
        return self.__adv

    @adv.setter
    def adv(self, value):
        self.__adv = value
        self._property_changed('adv')        

    @property
    def stsFxCurrency(self):
        return self.__stsFxCurrency

    @stsFxCurrency.setter
    def stsFxCurrency(self, value):
        self.__stsFxCurrency = value
        self._property_changed('stsFxCurrency')        

    @property
    def wpk(self):
        return self.__wpk

    @wpk.setter
    def wpk(self, value):
        self.__wpk = value
        self._property_changed('wpk')        

    @property
    def shortConvictionMedium(self):
        return self.__shortConvictionMedium

    @shortConvictionMedium.setter
    def shortConvictionMedium(self, value):
        self.__shortConvictionMedium = value
        self._property_changed('shortConvictionMedium')        

    @property
    def bidChange(self):
        return self.__bidChange

    @bidChange.setter
    def bidChange(self, value):
        self.__bidChange = value
        self._property_changed('bidChange')        

    @property
    def exchange(self):
        return self.__exchange

    @exchange.setter
    def exchange(self, value):
        self.__exchange = value
        self._property_changed('exchange')        

    @property
    def expiration(self):
        return self.__expiration

    @expiration.setter
    def expiration(self, value):
        self.__expiration = value
        self._property_changed('expiration')        

    @property
    def tradePrice(self):
        return self.__tradePrice

    @tradePrice.setter
    def tradePrice(self, value):
        self.__tradePrice = value
        self._property_changed('tradePrice')        

    @property
    def esPolicyScore(self):
        return self.__esPolicyScore

    @esPolicyScore.setter
    def esPolicyScore(self, value):
        self.__esPolicyScore = value
        self._property_changed('esPolicyScore')        

    @property
    def cid(self):
        return self.__cid

    @cid.setter
    def cid(self, value):
        self.__cid = value
        self._property_changed('cid')        

    @property
    def importance(self):
        return self.__importance

    @importance.setter
    def importance(self, value):
        self.__importance = value
        self._property_changed('importance')        

    @property
    def sourceDateSpan(self):
        return self.__sourceDateSpan

    @sourceDateSpan.setter
    def sourceDateSpan(self, value):
        self.__sourceDateSpan = value
        self._property_changed('sourceDateSpan')        

    @property
    def assetClassificationsGicsSector(self):
        return self.__assetClassificationsGicsSector

    @assetClassificationsGicsSector.setter
    def assetClassificationsGicsSector(self, value):
        self.__assetClassificationsGicsSector = value
        self._property_changed('assetClassificationsGicsSector')        

    @property
    def underlyingDataSetId(self):
        return self.__underlyingDataSetId

    @underlyingDataSetId.setter
    def underlyingDataSetId(self, value):
        self.__underlyingDataSetId = value
        self._property_changed('underlyingDataSetId')        

    @property
    def stsAssetName(self):
        return self.__stsAssetName

    @stsAssetName.setter
    def stsAssetName(self, value):
        self.__stsAssetName = value
        self._property_changed('stsAssetName')        

    @property
    def closeUnadjusted(self):
        return self.__closeUnadjusted

    @closeUnadjusted.setter
    def closeUnadjusted(self, value):
        self.__closeUnadjusted = value
        self._property_changed('closeUnadjusted')        

    @property
    def valueUnit(self):
        return self.__valueUnit

    @valueUnit.setter
    def valueUnit(self, value):
        self.__valueUnit = value
        self._property_changed('valueUnit')        

    @property
    def bidHigh(self):
        return self.__bidHigh

    @bidHigh.setter
    def bidHigh(self, value):
        self.__bidHigh = value
        self._property_changed('bidHigh')        

    @property
    def adjustedLowPrice(self):
        return self.__adjustedLowPrice

    @adjustedLowPrice.setter
    def adjustedLowPrice(self, value):
        self.__adjustedLowPrice = value
        self._property_changed('adjustedLowPrice')        

    @property
    def netExposureClassification(self):
        return self.__netExposureClassification

    @netExposureClassification.setter
    def netExposureClassification(self, value):
        self.__netExposureClassification = value
        self._property_changed('netExposureClassification')        

    @property
    def longConvictionLarge(self):
        return self.__longConvictionLarge

    @longConvictionLarge.setter
    def longConvictionLarge(self, value):
        self.__longConvictionLarge = value
        self._property_changed('longConvictionLarge')        

    @property
    def fairVariance(self):
        return self.__fairVariance

    @fairVariance.setter
    def fairVariance(self, value):
        self.__fairVariance = value
        self._property_changed('fairVariance')        

    @property
    def hitRateWtd(self):
        return self.__hitRateWtd

    @hitRateWtd.setter
    def hitRateWtd(self, value):
        self.__hitRateWtd = value
        self._property_changed('hitRateWtd')        

    @property
    def oad(self):
        return self.__oad

    @oad.setter
    def oad(self, value):
        self.__oad = value
        self._property_changed('oad')        

    @property
    def bosInBpsDescription(self):
        return self.__bosInBpsDescription

    @bosInBpsDescription.setter
    def bosInBpsDescription(self, value):
        self.__bosInBpsDescription = value
        self._property_changed('bosInBpsDescription')        

    @property
    def lowPrice(self):
        return self.__lowPrice

    @lowPrice.setter
    def lowPrice(self, value):
        self.__lowPrice = value
        self._property_changed('lowPrice')        

    @property
    def realizedVolatility(self):
        return self.__realizedVolatility

    @realizedVolatility.setter
    def realizedVolatility(self, value):
        self.__realizedVolatility = value
        self._property_changed('realizedVolatility')        

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, value):
        self.__rate = value
        self._property_changed('rate')        

    @property
    def adv22DayPct(self):
        return self.__adv22DayPct

    @adv22DayPct.setter
    def adv22DayPct(self, value):
        self.__adv22DayPct = value
        self._property_changed('adv22DayPct')        

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        self.__alpha = value
        self._property_changed('alpha')        

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, value):
        self.__client = value
        self._property_changed('client')        

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, value):
        self.__company = value
        self._property_changed('company')        

    @property
    def convictionList(self):
        return self.__convictionList

    @convictionList.setter
    def convictionList(self, value):
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
    def ticker(self):
        return self.__ticker

    @ticker.setter
    def ticker(self, value):
        self.__ticker = value
        self._property_changed('ticker')        

    @property
    def inRiskModel(self):
        return self.__inRiskModel

    @inRiskModel.setter
    def inRiskModel(self, value):
        self.__inRiskModel = value
        self._property_changed('inRiskModel')        

    @property
    def tcmCostHorizon1Day(self):
        return self.__tcmCostHorizon1Day

    @tcmCostHorizon1Day.setter
    def tcmCostHorizon1Day(self, value):
        self.__tcmCostHorizon1Day = value
        self._property_changed('tcmCostHorizon1Day')        

    @property
    def servicingCostLongPnl(self):
        return self.__servicingCostLongPnl

    @servicingCostLongPnl.setter
    def servicingCostLongPnl(self, value):
        self.__servicingCostLongPnl = value
        self._property_changed('servicingCostLongPnl')        

    @property
    def stsRatesCountry(self):
        return self.__stsRatesCountry

    @stsRatesCountry.setter
    def stsRatesCountry(self, value):
        self.__stsRatesCountry = value
        self._property_changed('stsRatesCountry')        

    @property
    def meetingNumber(self):
        return self.__meetingNumber

    @meetingNumber.setter
    def meetingNumber(self, value):
        self.__meetingNumber = value
        self._property_changed('meetingNumber')        

    @property
    def exchangeId(self):
        return self.__exchangeId

    @exchangeId.setter
    def exchangeId(self, value):
        self.__exchangeId = value
        self._property_changed('exchangeId')        

    @property
    def horizon(self):
        return self.__horizon

    @horizon.setter
    def horizon(self, value):
        self.__horizon = value
        self._property_changed('horizon')        

    @property
    def tcmCostHorizon20Day(self):
        return self.__tcmCostHorizon20Day

    @tcmCostHorizon20Day.setter
    def tcmCostHorizon20Day(self, value):
        self.__tcmCostHorizon20Day = value
        self._property_changed('tcmCostHorizon20Day')        

    @property
    def longLevel(self):
        return self.__longLevel

    @longLevel.setter
    def longLevel(self, value):
        self.__longLevel = value
        self._property_changed('longLevel')        

    @property
    def sourceValueForecast(self):
        return self.__sourceValueForecast

    @sourceValueForecast.setter
    def sourceValueForecast(self, value):
        self.__sourceValueForecast = value
        self._property_changed('sourceValueForecast')        

    @property
    def shortConvictionLarge(self):
        return self.__shortConvictionLarge

    @shortConvictionLarge.setter
    def shortConvictionLarge(self, value):
        self.__shortConvictionLarge = value
        self._property_changed('shortConvictionLarge')        

    @property
    def realm(self):
        return self.__realm

    @realm.setter
    def realm(self, value):
        self.__realm = value
        self._property_changed('realm')        

    @property
    def bid(self):
        return self.__bid

    @bid.setter
    def bid(self, value):
        self.__bid = value
        self._property_changed('bid')        

    @property
    def dataDescription(self):
        return self.__dataDescription

    @dataDescription.setter
    def dataDescription(self, value):
        self.__dataDescription = value
        self._property_changed('dataDescription')        

    @property
    def gsn(self):
        return self.__gsn

    @gsn.setter
    def gsn(self, value):
        self.__gsn = value
        self._property_changed('gsn')        

    @property
    def isAggressive(self):
        return self.__isAggressive

    @isAggressive.setter
    def isAggressive(self, value):
        self.__isAggressive = value
        self._property_changed('isAggressive')        

    @property
    def orderId(self):
        return self.__orderId

    @orderId.setter
    def orderId(self, value):
        self.__orderId = value
        self._property_changed('orderId')        

    @property
    def gss(self):
        return self.__gss

    @gss.setter
    def gss(self, value):
        self.__gss = value
        self._property_changed('gss')        

    @property
    def percentOfMediandv1m(self):
        return self.__percentOfMediandv1m

    @percentOfMediandv1m.setter
    def percentOfMediandv1m(self, value):
        self.__percentOfMediandv1m = value
        self._property_changed('percentOfMediandv1m')        

    @property
    def assetClass(self):
        return self.__assetClass

    @assetClass.setter
    def assetClass(self, value):
        self.__assetClass = value
        self._property_changed('assetClass')        

    @property
    def gsideid(self):
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value):
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
    def ric(self):
        return self.__ric

    @ric.setter
    def ric(self, value):
        self.__ric = value
        self._property_changed('ric')        

    @property
    def positionSourceId(self):
        return self.__positionSourceId

    @positionSourceId.setter
    def positionSourceId(self, value):
        self.__positionSourceId = value
        self._property_changed('positionSourceId')        

    @property
    def division(self):
        return self.__division

    @division.setter
    def division(self, value):
        self.__division = value
        self._property_changed('division')        

    @property
    def marketCapUSD(self):
        return self.__marketCapUSD

    @marketCapUSD.setter
    def marketCapUSD(self, value):
        self.__marketCapUSD = value
        self._property_changed('marketCapUSD')        

    @property
    def deploymentId(self):
        return self.__deploymentId

    @deploymentId.setter
    def deploymentId(self, value):
        self.__deploymentId = value
        self._property_changed('deploymentId')        

    @property
    def highPrice(self):
        return self.__highPrice

    @highPrice.setter
    def highPrice(self, value):
        self.__highPrice = value
        self._property_changed('highPrice')        

    @property
    def shortWeight(self):
        return self.__shortWeight

    @shortWeight.setter
    def shortWeight(self, value):
        self.__shortWeight = value
        self._property_changed('shortWeight')        

    @property
    def absoluteShares(self):
        return self.__absoluteShares

    @absoluteShares.setter
    def absoluteShares(self, value):
        self.__absoluteShares = value
        self._property_changed('absoluteShares')        

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value
        self._property_changed('action')        

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value
        self._property_changed('model')        

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value
        self._property_changed('id')        

    @property
    def arrivalHaircutVwapNormalized(self):
        return self.__arrivalHaircutVwapNormalized

    @arrivalHaircutVwapNormalized.setter
    def arrivalHaircutVwapNormalized(self, value):
        self.__arrivalHaircutVwapNormalized = value
        self._property_changed('arrivalHaircutVwapNormalized')        

    @property
    def queueClockTimeDescription(self):
        return self.__queueClockTimeDescription

    @queueClockTimeDescription.setter
    def queueClockTimeDescription(self, value):
        self.__queueClockTimeDescription = value
        self._property_changed('queueClockTimeDescription')        

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, value):
        self.__period = value
        self._property_changed('period')        

    @property
    def indexCreateSource(self):
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value):
        self.__indexCreateSource = value
        self._property_changed('indexCreateSource')        

    @property
    def fiscalQuarter(self):
        return self.__fiscalQuarter

    @fiscalQuarter.setter
    def fiscalQuarter(self, value):
        self.__fiscalQuarter = value
        self._property_changed('fiscalQuarter')        

    @property
    def deltaStrike(self):
        return self.__deltaStrike

    @deltaStrike.setter
    def deltaStrike(self, value):
        self.__deltaStrike = value
        self._property_changed('deltaStrike')        

    @property
    def marketImpact(self):
        return self.__marketImpact

    @marketImpact.setter
    def marketImpact(self, value):
        self.__marketImpact = value
        self._property_changed('marketImpact')        

    @property
    def eventType(self):
        return self.__eventType

    @eventType.setter
    def eventType(self, value):
        self.__eventType = value
        self._property_changed('eventType')        

    @property
    def assetCountLong(self):
        return self.__assetCountLong

    @assetCountLong.setter
    def assetCountLong(self, value):
        self.__assetCountLong = value
        self._property_changed('assetCountLong')        

    @property
    def valueActual(self):
        return self.__valueActual

    @valueActual.setter
    def valueActual(self, value):
        self.__valueActual = value
        self._property_changed('valueActual')        

    @property
    def bcid(self):
        return self.__bcid

    @bcid.setter
    def bcid(self, value):
        self.__bcid = value
        self._property_changed('bcid')        

    @property
    def originalCountry(self):
        return self.__originalCountry

    @originalCountry.setter
    def originalCountry(self, value):
        self.__originalCountry = value
        self._property_changed('originalCountry')        

    @property
    def touchLiquidityScore(self):
        return self.__touchLiquidityScore

    @touchLiquidityScore.setter
    def touchLiquidityScore(self, value):
        self.__touchLiquidityScore = value
        self._property_changed('touchLiquidityScore')        

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, value):
        self.__field = value
        self._property_changed('field')        

    @property
    def spot(self):
        return self.__spot

    @spot.setter
    def spot(self, value):
        self.__spot = value
        self._property_changed('spot')        

    @property
    def expectedCompletionDate(self):
        return self.__expectedCompletionDate

    @expectedCompletionDate.setter
    def expectedCompletionDate(self, value):
        self.__expectedCompletionDate = value
        self._property_changed('expectedCompletionDate')        

    @property
    def loanValue(self):
        return self.__loanValue

    @loanValue.setter
    def loanValue(self, value):
        self.__loanValue = value
        self._property_changed('loanValue')        

    @property
    def skew(self):
        return self.__skew

    @skew.setter
    def skew(self, value):
        self.__skew = value
        self._property_changed('skew')        

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        self._property_changed('status')        

    @property
    def sustainEmergingMarkets(self):
        return self.__sustainEmergingMarkets

    @sustainEmergingMarkets.setter
    def sustainEmergingMarkets(self, value):
        self.__sustainEmergingMarkets = value
        self._property_changed('sustainEmergingMarkets')        

    @property
    def totalReturnPrice(self):
        return self.__totalReturnPrice

    @totalReturnPrice.setter
    def totalReturnPrice(self, value):
        self.__totalReturnPrice = value
        self._property_changed('totalReturnPrice')        

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value
        self._property_changed('city')        

    @property
    def eventSource(self):
        return self.__eventSource

    @eventSource.setter
    def eventSource(self, value):
        self.__eventSource = value
        self._property_changed('eventSource')        

    @property
    def qisPermNo(self):
        return self.__qisPermNo

    @qisPermNo.setter
    def qisPermNo(self, value):
        self.__qisPermNo = value
        self._property_changed('qisPermNo')        

    @property
    def hitRateYtd(self):
        return self.__hitRateYtd

    @hitRateYtd.setter
    def hitRateYtd(self, value):
        self.__hitRateYtd = value
        self._property_changed('hitRateYtd')        

    @property
    def stsCommodity(self):
        return self.__stsCommodity

    @stsCommodity.setter
    def stsCommodity(self, value):
        self.__stsCommodity = value
        self._property_changed('stsCommodity')        

    @property
    def stsCommoditySector(self):
        return self.__stsCommoditySector

    @stsCommoditySector.setter
    def stsCommoditySector(self, value):
        self.__stsCommoditySector = value
        self._property_changed('stsCommoditySector')        

    @property
    def salesCoverage(self):
        return self.__salesCoverage

    @salesCoverage.setter
    def salesCoverage(self, value):
        self.__salesCoverage = value
        self._property_changed('salesCoverage')        

    @property
    def shortExposure(self):
        return self.__shortExposure

    @shortExposure.setter
    def shortExposure(self, value):
        self.__shortExposure = value
        self._property_changed('shortExposure')        

    @property
    def esScore(self):
        return self.__esScore

    @esScore.setter
    def esScore(self, value):
        self.__esScore = value
        self._property_changed('esScore')        

    @property
    def tcmCostParticipationRate10Pct(self):
        return self.__tcmCostParticipationRate10Pct

    @tcmCostParticipationRate10Pct.setter
    def tcmCostParticipationRate10Pct(self, value):
        self.__tcmCostParticipationRate10Pct = value
        self._property_changed('tcmCostParticipationRate10Pct')        

    @property
    def eventTime(self):
        return self.__eventTime

    @eventTime.setter
    def eventTime(self, value):
        self.__eventTime = value
        self._property_changed('eventTime')        

    @property
    def positionSourceName(self):
        return self.__positionSourceName

    @positionSourceName.setter
    def positionSourceName(self, value):
        self.__positionSourceName = value
        self._property_changed('positionSourceName')        

    @property
    def priceRangeInTicks(self):
        return self.__priceRangeInTicks

    @priceRangeInTicks.setter
    def priceRangeInTicks(self, value):
        self.__priceRangeInTicks = value
        self._property_changed('priceRangeInTicks')        

    @property
    def arrivalHaircutVwap(self):
        return self.__arrivalHaircutVwap

    @arrivalHaircutVwap.setter
    def arrivalHaircutVwap(self, value):
        self.__arrivalHaircutVwap = value
        self._property_changed('arrivalHaircutVwap')        

    @property
    def interestRate(self):
        return self.__interestRate

    @interestRate.setter
    def interestRate(self, value):
        self.__interestRate = value
        self._property_changed('interestRate')        

    @property
    def executionDays(self):
        return self.__executionDays

    @executionDays.setter
    def executionDays(self, value):
        self.__executionDays = value
        self._property_changed('executionDays')        

    @property
    def pctChange(self):
        return self.__pctChange

    @pctChange.setter
    def pctChange(self, value):
        self.__pctChange = value
        self._property_changed('pctChange')        

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        self.__side = value
        self._property_changed('side')        

    @property
    def numberOfRolls(self):
        return self.__numberOfRolls

    @numberOfRolls.setter
    def numberOfRolls(self, value):
        self.__numberOfRolls = value
        self._property_changed('numberOfRolls')        

    @property
    def agentLenderFee(self):
        return self.__agentLenderFee

    @agentLenderFee.setter
    def agentLenderFee(self, value):
        self.__agentLenderFee = value
        self._property_changed('agentLenderFee')        

    @property
    def complianceRestrictedStatus(self):
        return self.__complianceRestrictedStatus

    @complianceRestrictedStatus.setter
    def complianceRestrictedStatus(self, value):
        self.__complianceRestrictedStatus = value
        self._property_changed('complianceRestrictedStatus')        

    @property
    def forward(self):
        return self.__forward

    @forward.setter
    def forward(self, value):
        self.__forward = value
        self._property_changed('forward')        

    @property
    def borrowFee(self):
        return self.__borrowFee

    @borrowFee.setter
    def borrowFee(self, value):
        self.__borrowFee = value
        self._property_changed('borrowFee')        

    @property
    def strike(self):
        return self.__strike

    @strike.setter
    def strike(self, value):
        self.__strike = value
        self._property_changed('strike')        

    @property
    def loanSpread(self):
        return self.__loanSpread

    @loanSpread.setter
    def loanSpread(self, value):
        self.__loanSpread = value
        self._property_changed('loanSpread')        

    @property
    def tcmCostHorizon12Hour(self):
        return self.__tcmCostHorizon12Hour

    @tcmCostHorizon12Hour.setter
    def tcmCostHorizon12Hour(self, value):
        self.__tcmCostHorizon12Hour = value
        self._property_changed('tcmCostHorizon12Hour')        

    @property
    def dewPoint(self):
        return self.__dewPoint

    @dewPoint.setter
    def dewPoint(self, value):
        self.__dewPoint = value
        self._property_changed('dewPoint')        

    @property
    def researchCommission(self):
        return self.__researchCommission

    @researchCommission.setter
    def researchCommission(self, value):
        self.__researchCommission = value
        self._property_changed('researchCommission')        

    @property
    def bbid(self):
        return self.__bbid

    @bbid.setter
    def bbid(self, value):
        self.__bbid = value
        self._property_changed('bbid')        

    @property
    def eventStatus(self):
        return self.__eventStatus

    @eventStatus.setter
    def eventStatus(self, value):
        self.__eventStatus = value
        self._property_changed('eventStatus')        

    @property
    def return_(self):
        return self.__return

    @return_.setter
    def return_(self, value):
        self.__return = value
        self._property_changed('return')        

    @property
    def maxTemperature(self):
        return self.__maxTemperature

    @maxTemperature.setter
    def maxTemperature(self, value):
        self.__maxTemperature = value
        self._property_changed('maxTemperature')        

    @property
    def acquirerShareholderMeetingDate(self):
        return self.__acquirerShareholderMeetingDate

    @acquirerShareholderMeetingDate.setter
    def acquirerShareholderMeetingDate(self, value):
        self.__acquirerShareholderMeetingDate = value
        self._property_changed('acquirerShareholderMeetingDate')        

    @property
    def arrivalMidNormalized(self):
        return self.__arrivalMidNormalized

    @arrivalMidNormalized.setter
    def arrivalMidNormalized(self, value):
        self.__arrivalMidNormalized = value
        self._property_changed('arrivalMidNormalized')        

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        self.__rating = value
        self._property_changed('rating')        

    @property
    def arrivalRtNormalized(self):
        return self.__arrivalRtNormalized

    @arrivalRtNormalized.setter
    def arrivalRtNormalized(self, value):
        self.__arrivalRtNormalized = value
        self._property_changed('arrivalRtNormalized')        

    @property
    def performanceFee(self):
        return self.__performanceFee

    @performanceFee.setter
    def performanceFee(self, value):
        self.__performanceFee = value
        self._property_changed('performanceFee')        

    @property
    def reportType(self):
        return self.__reportType

    @reportType.setter
    def reportType(self, value):
        self.__reportType = value
        self._property_changed('reportType')        

    @property
    def sourceURL(self):
        return self.__sourceURL

    @sourceURL.setter
    def sourceURL(self, value):
        self.__sourceURL = value
        self._property_changed('sourceURL')        

    @property
    def estimatedReturn(self):
        return self.__estimatedReturn

    @estimatedReturn.setter
    def estimatedReturn(self, value):
        self.__estimatedReturn = value
        self._property_changed('estimatedReturn')        

    @property
    def underlyingAssetIds(self):
        return self.__underlyingAssetIds

    @underlyingAssetIds.setter
    def underlyingAssetIds(self, value):
        self.__underlyingAssetIds = value
        self._property_changed('underlyingAssetIds')        

    @property
    def high(self):
        return self.__high

    @high.setter
    def high(self, value):
        self.__high = value
        self._property_changed('high')        

    @property
    def sourceLastUpdate(self):
        return self.__sourceLastUpdate

    @sourceLastUpdate.setter
    def sourceLastUpdate(self, value):
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
    def adv10DayPct(self):
        return self.__adv10DayPct

    @adv10DayPct.setter
    def adv10DayPct(self, value):
        self.__adv10DayPct = value
        self._property_changed('adv10DayPct')        

    @property
    def longConvictionMedium(self):
        return self.__longConvictionMedium

    @longConvictionMedium.setter
    def longConvictionMedium(self, value):
        self.__longConvictionMedium = value
        self._property_changed('longConvictionMedium')        

    @property
    def eventName(self):
        return self.__eventName

    @eventName.setter
    def eventName(self, value):
        self.__eventName = value
        self._property_changed('eventName')        

    @property
    def annualRisk(self):
        return self.__annualRisk

    @annualRisk.setter
    def annualRisk(self, value):
        self.__annualRisk = value
        self._property_changed('annualRisk')        

    @property
    def dailyTrackingError(self):
        return self.__dailyTrackingError

    @dailyTrackingError.setter
    def dailyTrackingError(self, value):
        self.__dailyTrackingError = value
        self._property_changed('dailyTrackingError')        

    @property
    def unadjustedBid(self):
        return self.__unadjustedBid

    @unadjustedBid.setter
    def unadjustedBid(self, value):
        self.__unadjustedBid = value
        self._property_changed('unadjustedBid')        

    @property
    def gsdeer(self):
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value):
        self.__gsdeer = value
        self._property_changed('gsdeer')        

    @property
    def marketCap(self):
        return self.__marketCap

    @marketCap.setter
    def marketCap(self, value):
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
    def bbidEquivalent(self):
        return self.__bbidEquivalent

    @bbidEquivalent.setter
    def bbidEquivalent(self, value):
        self.__bbidEquivalent = value
        self._property_changed('bbidEquivalent')        

    @property
    def prevCloseAsk(self):
        return self.__prevCloseAsk

    @prevCloseAsk.setter
    def prevCloseAsk(self, value):
        self.__prevCloseAsk = value
        self._property_changed('prevCloseAsk')        

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value
        self._property_changed('level')        

    @property
    def valoren(self):
        return self.__valoren

    @valoren.setter
    def valoren(self, value):
        self.__valoren = value
        self._property_changed('valoren')        

    @property
    def pressure(self):
        return self.__pressure

    @pressure.setter
    def pressure(self, value):
        self.__pressure = value
        self._property_changed('pressure')        

    @property
    def shortDescription(self):
        return self.__shortDescription

    @shortDescription.setter
    def shortDescription(self, value):
        self.__shortDescription = value
        self._property_changed('shortDescription')        

    @property
    def basis(self):
        return self.__basis

    @basis.setter
    def basis(self, value):
        self.__basis = value
        self._property_changed('basis')        

    @property
    def netWeight(self):
        return self.__netWeight

    @netWeight.setter
    def netWeight(self, value):
        self.__netWeight = value
        self._property_changed('netWeight')        

    @property
    def hedgeId(self):
        return self.__hedgeId

    @hedgeId.setter
    def hedgeId(self, value):
        self.__hedgeId = value
        self._property_changed('hedgeId')        

    @property
    def portfolioManagers(self):
        return self.__portfolioManagers

    @portfolioManagers.setter
    def portfolioManagers(self, value):
        self.__portfolioManagers = value
        self._property_changed('portfolioManagers')        

    @property
    def bosInTicks(self):
        return self.__bosInTicks

    @bosInTicks.setter
    def bosInTicks(self, value):
        self.__bosInTicks = value
        self._property_changed('bosInTicks')        

    @property
    def tcmCostHorizon8Day(self):
        return self.__tcmCostHorizon8Day

    @tcmCostHorizon8Day.setter
    def tcmCostHorizon8Day(self, value):
        self.__tcmCostHorizon8Day = value
        self._property_changed('tcmCostHorizon8Day')        

    @property
    def supraStrategy(self):
        return self.__supraStrategy

    @supraStrategy.setter
    def supraStrategy(self, value):
        self.__supraStrategy = value
        self._property_changed('supraStrategy')        

    @property
    def adv5DayPct(self):
        return self.__adv5DayPct

    @adv5DayPct.setter
    def adv5DayPct(self, value):
        self.__adv5DayPct = value
        self._property_changed('adv5DayPct')        

    @property
    def factorSource(self):
        return self.__factorSource

    @factorSource.setter
    def factorSource(self, value):
        self.__factorSource = value
        self._property_changed('factorSource')        

    @property
    def leverage(self):
        return self.__leverage

    @leverage.setter
    def leverage(self, value):
        self.__leverage = value
        self._property_changed('leverage')        

    @property
    def submitter(self):
        return self.__submitter

    @submitter.setter
    def submitter(self, value):
        self.__submitter = value
        self._property_changed('submitter')        

    @property
    def notional(self):
        return self.__notional

    @notional.setter
    def notional(self, value):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def esDisclosurePercentage(self):
        return self.__esDisclosurePercentage

    @esDisclosurePercentage.setter
    def esDisclosurePercentage(self, value):
        self.__esDisclosurePercentage = value
        self._property_changed('esDisclosurePercentage')        

    @property
    def clientShortName(self):
        return self.__clientShortName

    @clientShortName.setter
    def clientShortName(self, value):
        self.__clientShortName = value
        self._property_changed('clientShortName')        

    @property
    def fwdPoints(self):
        return self.__fwdPoints

    @fwdPoints.setter
    def fwdPoints(self, value):
        self.__fwdPoints = value
        self._property_changed('fwdPoints')        

    @property
    def groupCategory(self):
        return self.__groupCategory

    @groupCategory.setter
    def groupCategory(self, value):
        self.__groupCategory = value
        self._property_changed('groupCategory')        

    @property
    def kpiId(self):
        return self.__kpiId

    @kpiId.setter
    def kpiId(self, value):
        self.__kpiId = value
        self._property_changed('kpiId')        

    @property
    def relativeReturnWtd(self):
        return self.__relativeReturnWtd

    @relativeReturnWtd.setter
    def relativeReturnWtd(self, value):
        self.__relativeReturnWtd = value
        self._property_changed('relativeReturnWtd')        

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value
        self._property_changed('total')        

    @property
    def riskModel(self):
        return self.__riskModel

    @riskModel.setter
    def riskModel(self, value):
        self.__riskModel = value
        self._property_changed('riskModel')        

    @property
    def assetId(self):
        return self.__assetId

    @assetId.setter
    def assetId(self, value):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def fairValue(self):
        return self.__fairValue

    @fairValue.setter
    def fairValue(self, value):
        self.__fairValue = value
        self._property_changed('fairValue')        

    @property
    def adjustedHighPrice(self):
        return self.__adjustedHighPrice

    @adjustedHighPrice.setter
    def adjustedHighPrice(self, value):
        self.__adjustedHighPrice = value
        self._property_changed('adjustedHighPrice')        

    @property
    def beta(self):
        return self.__beta

    @beta.setter
    def beta(self, value):
        self.__beta = value
        self._property_changed('beta')        

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        self._property_changed('direction')        

    @property
    def valueForecast(self):
        return self.__valueForecast

    @valueForecast.setter
    def valueForecast(self, value):
        self.__valueForecast = value
        self._property_changed('valueForecast')        

    @property
    def longExposure(self):
        return self.__longExposure

    @longExposure.setter
    def longExposure(self, value):
        self.__longExposure = value
        self._property_changed('longExposure')        

    @property
    def positionSourceType(self):
        return self.__positionSourceType

    @positionSourceType.setter
    def positionSourceType(self, value):
        self.__positionSourceType = value
        self._property_changed('positionSourceType')        

    @property
    def tcmCostParticipationRate20Pct(self):
        return self.__tcmCostParticipationRate20Pct

    @tcmCostParticipationRate20Pct.setter
    def tcmCostParticipationRate20Pct(self, value):
        self.__tcmCostParticipationRate20Pct = value
        self._property_changed('tcmCostParticipationRate20Pct')        

    @property
    def adjustedClosePrice(self):
        return self.__adjustedClosePrice

    @adjustedClosePrice.setter
    def adjustedClosePrice(self, value):
        self.__adjustedClosePrice = value
        self._property_changed('adjustedClosePrice')        

    @property
    def cross(self):
        return self.__cross

    @cross.setter
    def cross(self, value):
        self.__cross = value
        self._property_changed('cross')        

    @property
    def lmsId(self):
        return self.__lmsId

    @lmsId.setter
    def lmsId(self, value):
        self.__lmsId = value
        self._property_changed('lmsId')        

    @property
    def rebateRate(self):
        return self.__rebateRate

    @rebateRate.setter
    def rebateRate(self, value):
        self.__rebateRate = value
        self._property_changed('rebateRate')        

    @property
    def ideaStatus(self):
        return self.__ideaStatus

    @ideaStatus.setter
    def ideaStatus(self, value):
        self.__ideaStatus = value
        self._property_changed('ideaStatus')        

    @property
    def participationRate(self):
        return self.__participationRate

    @participationRate.setter
    def participationRate(self, value):
        self.__participationRate = value
        self._property_changed('participationRate')        

    @property
    def fxForecast(self):
        return self.__fxForecast

    @fxForecast.setter
    def fxForecast(self, value):
        self.__fxForecast = value
        self._property_changed('fxForecast')        

    @property
    def fixingTimeLabel(self):
        return self.__fixingTimeLabel

    @fixingTimeLabel.setter
    def fixingTimeLabel(self, value):
        self.__fixingTimeLabel = value
        self._property_changed('fixingTimeLabel')        

    @property
    def fillId(self):
        return self.__fillId

    @fillId.setter
    def fillId(self, value):
        self.__fillId = value
        self._property_changed('fillId')        

    @property
    def esNumericScore(self):
        return self.__esNumericScore

    @esNumericScore.setter
    def esNumericScore(self, value):
        self.__esNumericScore = value
        self._property_changed('esNumericScore')        

    @property
    def inBenchmark(self):
        return self.__inBenchmark

    @inBenchmark.setter
    def inBenchmark(self, value):
        self.__inBenchmark = value
        self._property_changed('inBenchmark')        

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, value):
        self.__strategy = value
        self._property_changed('strategy')        

    @property
    def shortInterest(self):
        return self.__shortInterest

    @shortInterest.setter
    def shortInterest(self, value):
        self.__shortInterest = value
        self._property_changed('shortInterest')        

    @property
    def referencePeriod(self):
        return self.__referencePeriod

    @referencePeriod.setter
    def referencePeriod(self, value):
        self.__referencePeriod = value
        self._property_changed('referencePeriod')        

    @property
    def adjustedVolume(self):
        return self.__adjustedVolume

    @adjustedVolume.setter
    def adjustedVolume(self, value):
        self.__adjustedVolume = value
        self._property_changed('adjustedVolume')        

    @property
    def queueInLotsDescription(self):
        return self.__queueInLotsDescription

    @queueInLotsDescription.setter
    def queueInLotsDescription(self, value):
        self.__queueInLotsDescription = value
        self._property_changed('queueInLotsDescription')        

    @property
    def pbClientId(self):
        return self.__pbClientId

    @pbClientId.setter
    def pbClientId(self, value):
        self.__pbClientId = value
        self._property_changed('pbClientId')        

    @property
    def ownerId(self):
        return self.__ownerId

    @ownerId.setter
    def ownerId(self, value):
        self.__ownerId = value
        self._property_changed('ownerId')        

    @property
    def secDB(self):
        return self.__secDB

    @secDB.setter
    def secDB(self, value):
        self.__secDB = value
        self._property_changed('secDB')        

    @property
    def objective(self):
        return self.__objective

    @objective.setter
    def objective(self, value):
        self.__objective = value
        self._property_changed('objective')        

    @property
    def navPrice(self):
        return self.__navPrice

    @navPrice.setter
    def navPrice(self, value):
        self.__navPrice = value
        self._property_changed('navPrice')        

    @property
    def ideaActivityType(self):
        return self.__ideaActivityType

    @ideaActivityType.setter
    def ideaActivityType(self, value):
        self.__ideaActivityType = value
        self._property_changed('ideaActivityType')        

    @property
    def precipitation(self):
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value):
        self.__precipitation = value
        self._property_changed('precipitation')        

    @property
    def ideaSource(self):
        return self.__ideaSource

    @ideaSource.setter
    def ideaSource(self, value):
        self.__ideaSource = value
        self._property_changed('ideaSource')        

    @property
    def hedgeNotional(self):
        return self.__hedgeNotional

    @hedgeNotional.setter
    def hedgeNotional(self, value):
        self.__hedgeNotional = value
        self._property_changed('hedgeNotional')        

    @property
    def askLow(self):
        return self.__askLow

    @askLow.setter
    def askLow(self, value):
        self.__askLow = value
        self._property_changed('askLow')        

    @property
    def unadjustedAsk(self):
        return self.__unadjustedAsk

    @unadjustedAsk.setter
    def unadjustedAsk(self, value):
        self.__unadjustedAsk = value
        self._property_changed('unadjustedAsk')        

    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, value):
        self.__expiry = value
        self._property_changed('expiry')        

    @property
    def tradingPnl(self):
        return self.__tradingPnl

    @tradingPnl.setter
    def tradingPnl(self, value):
        self.__tradingPnl = value
        self._property_changed('tradingPnl')        

    @property
    def strikePercentage(self):
        return self.__strikePercentage

    @strikePercentage.setter
    def strikePercentage(self, value):
        self.__strikePercentage = value
        self._property_changed('strikePercentage')        

    @property
    def excessReturnPrice(self):
        return self.__excessReturnPrice

    @excessReturnPrice.setter
    def excessReturnPrice(self, value):
        self.__excessReturnPrice = value
        self._property_changed('excessReturnPrice')        

    @property
    def shortConvictionSmall(self):
        return self.__shortConvictionSmall

    @shortConvictionSmall.setter
    def shortConvictionSmall(self, value):
        self.__shortConvictionSmall = value
        self._property_changed('shortConvictionSmall')        

    @property
    def prevCloseBid(self):
        return self.__prevCloseBid

    @prevCloseBid.setter
    def prevCloseBid(self, value):
        self.__prevCloseBid = value
        self._property_changed('prevCloseBid')        

    @property
    def fxPnl(self):
        return self.__fxPnl

    @fxPnl.setter
    def fxPnl(self, value):
        self.__fxPnl = value
        self._property_changed('fxPnl')        

    @property
    def forecast(self):
        return self.__forecast

    @forecast.setter
    def forecast(self, value):
        self.__forecast = value
        self._property_changed('forecast')        

    @property
    def tcmCostHorizon16Day(self):
        return self.__tcmCostHorizon16Day

    @tcmCostHorizon16Day.setter
    def tcmCostHorizon16Day(self, value):
        self.__tcmCostHorizon16Day = value
        self._property_changed('tcmCostHorizon16Day')        

    @property
    def pnl(self):
        return self.__pnl

    @pnl.setter
    def pnl(self, value):
        self.__pnl = value
        self._property_changed('pnl')        

    @property
    def assetClassificationsGicsIndustryGroup(self):
        return self.__assetClassificationsGicsIndustryGroup

    @assetClassificationsGicsIndustryGroup.setter
    def assetClassificationsGicsIndustryGroup(self, value):
        self.__assetClassificationsGicsIndustryGroup = value
        self._property_changed('assetClassificationsGicsIndustryGroup')        

    @property
    def unadjustedClose(self):
        return self.__unadjustedClose

    @unadjustedClose.setter
    def unadjustedClose(self, value):
        self.__unadjustedClose = value
        self._property_changed('unadjustedClose')        

    @property
    def tcmCostHorizon4Day(self):
        return self.__tcmCostHorizon4Day

    @tcmCostHorizon4Day.setter
    def tcmCostHorizon4Day(self, value):
        self.__tcmCostHorizon4Day = value
        self._property_changed('tcmCostHorizon4Day')        

    @property
    def assetClassificationsIsPrimary(self):
        return self.__assetClassificationsIsPrimary

    @assetClassificationsIsPrimary.setter
    def assetClassificationsIsPrimary(self, value):
        self.__assetClassificationsIsPrimary = value
        self._property_changed('assetClassificationsIsPrimary')        

    @property
    def styles(self):
        return self.__styles

    @styles.setter
    def styles(self, value):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def shortName(self):
        return self.__shortName

    @shortName.setter
    def shortName(self, value):
        self.__shortName = value
        self._property_changed('shortName')        

    @property
    def equityTheta(self):
        return self.__equityTheta

    @equityTheta.setter
    def equityTheta(self, value):
        self.__equityTheta = value
        self._property_changed('equityTheta')        

    @property
    def averageFillPrice(self):
        return self.__averageFillPrice

    @averageFillPrice.setter
    def averageFillPrice(self, value):
        self.__averageFillPrice = value
        self._property_changed('averageFillPrice')        

    @property
    def snowfall(self):
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value):
        self.__snowfall = value
        self._property_changed('snowfall')        

    @property
    def mic(self):
        return self.__mic

    @mic.setter
    def mic(self, value):
        self.__mic = value
        self._property_changed('mic')        

    @property
    def openPrice(self):
        return self.__openPrice

    @openPrice.setter
    def openPrice(self, value):
        self.__openPrice = value
        self._property_changed('openPrice')        

    @property
    def autoExecState(self):
        return self.__autoExecState

    @autoExecState.setter
    def autoExecState(self, value):
        self.__autoExecState = value
        self._property_changed('autoExecState')        

    @property
    def depthSpreadScore(self):
        return self.__depthSpreadScore

    @depthSpreadScore.setter
    def depthSpreadScore(self, value):
        self.__depthSpreadScore = value
        self._property_changed('depthSpreadScore')        

    @property
    def relativeReturnYtd(self):
        return self.__relativeReturnYtd

    @relativeReturnYtd.setter
    def relativeReturnYtd(self, value):
        self.__relativeReturnYtd = value
        self._property_changed('relativeReturnYtd')        

    @property
    def long(self):
        return self.__long

    @long.setter
    def long(self, value):
        self.__long = value
        self._property_changed('long')        

    @property
    def fairVolatility(self):
        return self.__fairVolatility

    @fairVolatility.setter
    def fairVolatility(self, value):
        self.__fairVolatility = value
        self._property_changed('fairVolatility')        

    @property
    def longWeight(self):
        return self.__longWeight

    @longWeight.setter
    def longWeight(self, value):
        self.__longWeight = value
        self._property_changed('longWeight')        

    @property
    def vendor(self):
        return self.__vendor

    @vendor.setter
    def vendor(self, value):
        self.__vendor = value
        self._property_changed('vendor')        

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def clusterClass(self):
        return self.__clusterClass

    @clusterClass.setter
    def clusterClass(self, value):
        self.__clusterClass = value
        self._property_changed('clusterClass')        

    @property
    def financialReturnsScore(self):
        return self.__financialReturnsScore

    @financialReturnsScore.setter
    def financialReturnsScore(self, value):
        self.__financialReturnsScore = value
        self._property_changed('financialReturnsScore')        

    @property
    def netChange(self):
        return self.__netChange

    @netChange.setter
    def netChange(self, value):
        self.__netChange = value
        self._property_changed('netChange')        

    @property
    def nonSymbolDimensions(self):
        return self.__nonSymbolDimensions

    @nonSymbolDimensions.setter
    def nonSymbolDimensions(self, value):
        self.__nonSymbolDimensions = value
        self._property_changed('nonSymbolDimensions')        

    @property
    def bidSize(self):
        return self.__bidSize

    @bidSize.setter
    def bidSize(self, value):
        self.__bidSize = value
        self._property_changed('bidSize')        

    @property
    def arrivalMid(self):
        return self.__arrivalMid

    @arrivalMid.setter
    def arrivalMid(self, value):
        self.__arrivalMid = value
        self._property_changed('arrivalMid')        

    @property
    def assetParametersExchangeCurrency(self):
        return self.__assetParametersExchangeCurrency

    @assetParametersExchangeCurrency.setter
    def assetParametersExchangeCurrency(self, value):
        self.__assetParametersExchangeCurrency = value
        self._property_changed('assetParametersExchangeCurrency')        

    @property
    def unexplained(self):
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value):
        self.__unexplained = value
        self._property_changed('unexplained')        

    @property
    def assetClassificationsCountryName(self):
        return self.__assetClassificationsCountryName

    @assetClassificationsCountryName.setter
    def assetClassificationsCountryName(self, value):
        self.__assetClassificationsCountryName = value
        self._property_changed('assetClassificationsCountryName')        

    @property
    def metric(self):
        return self.__metric

    @metric.setter
    def metric(self, value):
        self.__metric = value
        self._property_changed('metric')        

    @property
    def newIdeasYtd(self):
        return self.__newIdeasYtd

    @newIdeasYtd.setter
    def newIdeasYtd(self, value):
        self.__newIdeasYtd = value
        self._property_changed('newIdeasYtd')        

    @property
    def managementFee(self):
        return self.__managementFee

    @managementFee.setter
    def managementFee(self, value):
        self.__managementFee = value
        self._property_changed('managementFee')        

    @property
    def ask(self):
        return self.__ask

    @ask.setter
    def ask(self, value):
        self.__ask = value
        self._property_changed('ask')        

    @property
    def impliedLognormalVolatility(self):
        return self.__impliedLognormalVolatility

    @impliedLognormalVolatility.setter
    def impliedLognormalVolatility(self, value):
        self.__impliedLognormalVolatility = value
        self._property_changed('impliedLognormalVolatility')        

    @property
    def closePrice(self):
        return self.__closePrice

    @closePrice.setter
    def closePrice(self, value):
        self.__closePrice = value
        self._property_changed('closePrice')        

    @property
    def open(self):
        return self.__open

    @open.setter
    def open(self, value):
        self.__open = value
        self._property_changed('open')        

    @property
    def sourceId(self):
        return self.__sourceId

    @sourceId.setter
    def sourceId(self, value):
        self.__sourceId = value
        self._property_changed('sourceId')        

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        self.__country = value
        self._property_changed('country')        

    @property
    def cusip(self):
        return self.__cusip

    @cusip.setter
    def cusip(self, value):
        self.__cusip = value
        self._property_changed('cusip')        

    @property
    def touchSpreadScore(self):
        return self.__touchSpreadScore

    @touchSpreadScore.setter
    def touchSpreadScore(self, value):
        self.__touchSpreadScore = value
        self._property_changed('touchSpreadScore')        

    @property
    def absoluteStrike(self):
        return self.__absoluteStrike

    @absoluteStrike.setter
    def absoluteStrike(self, value):
        self.__absoluteStrike = value
        self._property_changed('absoluteStrike')        

    @property
    def netExposure(self):
        return self.__netExposure

    @netExposure.setter
    def netExposure(self, value):
        self.__netExposure = value
        self._property_changed('netExposure')        

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value
        self._property_changed('source')        

    @property
    def assetClassificationsCountryCode(self):
        return self.__assetClassificationsCountryCode

    @assetClassificationsCountryCode.setter
    def assetClassificationsCountryCode(self, value):
        self.__assetClassificationsCountryCode = value
        self._property_changed('assetClassificationsCountryCode')        

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        self._property_changed('frequency')        

    @property
    def activityId(self):
        return self.__activityId

    @activityId.setter
    def activityId(self, value):
        self.__activityId = value
        self._property_changed('activityId')        

    @property
    def estimatedImpact(self):
        return self.__estimatedImpact

    @estimatedImpact.setter
    def estimatedImpact(self, value):
        self.__estimatedImpact = value
        self._property_changed('estimatedImpact')        

    @property
    def dataSetSubCategory(self):
        return self.__dataSetSubCategory

    @dataSetSubCategory.setter
    def dataSetSubCategory(self, value):
        self.__dataSetSubCategory = value
        self._property_changed('dataSetSubCategory')        

    @property
    def assetParametersPricingLocation(self):
        return self.__assetParametersPricingLocation

    @assetParametersPricingLocation.setter
    def assetParametersPricingLocation(self, value):
        self.__assetParametersPricingLocation = value
        self._property_changed('assetParametersPricingLocation')        

    @property
    def eventDescription(self):
        return self.__eventDescription

    @eventDescription.setter
    def eventDescription(self, value):
        self.__eventDescription = value
        self._property_changed('eventDescription')        

    @property
    def strikeReference(self):
        return self.__strikeReference

    @strikeReference.setter
    def strikeReference(self, value):
        self.__strikeReference = value
        self._property_changed('strikeReference')        

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, value):
        self.__details = value
        self._property_changed('details')        

    @property
    def assetCount(self):
        return self.__assetCount

    @assetCount.setter
    def assetCount(self, value):
        self.__assetCount = value
        self._property_changed('assetCount')        

    @property
    def absoluteValue(self):
        return self.__absoluteValue

    @absoluteValue.setter
    def absoluteValue(self, value):
        self.__absoluteValue = value
        self._property_changed('absoluteValue')        

    @property
    def delistingDate(self):
        return self.__delistingDate

    @delistingDate.setter
    def delistingDate(self, value):
        self.__delistingDate = value
        self._property_changed('delistingDate')        

    @property
    def longTenor(self):
        return self.__longTenor

    @longTenor.setter
    def longTenor(self, value):
        self.__longTenor = value
        self._property_changed('longTenor')        

    @property
    def mctr(self):
        return self.__mctr

    @mctr.setter
    def mctr(self, value):
        self.__mctr = value
        self._property_changed('mctr')        

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value
        self._property_changed('weight')        

    @property
    def historicalClose(self):
        return self.__historicalClose

    @historicalClose.setter
    def historicalClose(self, value):
        self.__historicalClose = value
        self._property_changed('historicalClose')        

    @property
    def assetCountPriced(self):
        return self.__assetCountPriced

    @assetCountPriced.setter
    def assetCountPriced(self, value):
        self.__assetCountPriced = value
        self._property_changed('assetCountPriced')        

    @property
    def marketDataPoint(self):
        return self.__marketDataPoint

    @marketDataPoint.setter
    def marketDataPoint(self, value):
        self.__marketDataPoint = value
        self._property_changed('marketDataPoint')        

    @property
    def ideaId(self):
        return self.__ideaId

    @ideaId.setter
    def ideaId(self, value):
        self.__ideaId = value
        self._property_changed('ideaId')        

    @property
    def commentStatus(self):
        return self.__commentStatus

    @commentStatus.setter
    def commentStatus(self, value):
        self.__commentStatus = value
        self._property_changed('commentStatus')        

    @property
    def marginalCost(self):
        return self.__marginalCost

    @marginalCost.setter
    def marginalCost(self, value):
        self.__marginalCost = value
        self._property_changed('marginalCost')        

    @property
    def absoluteWeight(self):
        return self.__absoluteWeight

    @absoluteWeight.setter
    def absoluteWeight(self, value):
        self.__absoluteWeight = value
        self._property_changed('absoluteWeight')        

    @property
    def measure(self):
        return self.__measure

    @measure.setter
    def measure(self, value):
        self.__measure = value
        self._property_changed('measure')        

    @property
    def clientWeight(self):
        return self.__clientWeight

    @clientWeight.setter
    def clientWeight(self, value):
        self.__clientWeight = value
        self._property_changed('clientWeight')        

    @property
    def hedgeAnnualizedVolatility(self):
        return self.__hedgeAnnualizedVolatility

    @hedgeAnnualizedVolatility.setter
    def hedgeAnnualizedVolatility(self, value):
        self.__hedgeAnnualizedVolatility = value
        self._property_changed('hedgeAnnualizedVolatility')        

    @property
    def benchmarkCurrency(self):
        return self.__benchmarkCurrency

    @benchmarkCurrency.setter
    def benchmarkCurrency(self, value):
        self.__benchmarkCurrency = value
        self._property_changed('benchmarkCurrency')        

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self._property_changed('name')        

    @property
    def aum(self):
        return self.__aum

    @aum.setter
    def aum(self, value):
        self.__aum = value
        self._property_changed('aum')        

    @property
    def folderName(self):
        return self.__folderName

    @folderName.setter
    def folderName(self, value):
        self.__folderName = value
        self._property_changed('folderName')        

    @property
    def lendingPartnerFee(self):
        return self.__lendingPartnerFee

    @lendingPartnerFee.setter
    def lendingPartnerFee(self, value):
        self.__lendingPartnerFee = value
        self._property_changed('lendingPartnerFee')        

    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, value):
        self.__region = value
        self._property_changed('region')        

    @property
    def liveDate(self):
        return self.__liveDate

    @liveDate.setter
    def liveDate(self, value):
        self.__liveDate = value
        self._property_changed('liveDate')        

    @property
    def askHigh(self):
        return self.__askHigh

    @askHigh.setter
    def askHigh(self, value):
        self.__askHigh = value
        self._property_changed('askHigh')        

    @property
    def corporateActionType(self):
        return self.__corporateActionType

    @corporateActionType.setter
    def corporateActionType(self, value):
        self.__corporateActionType = value
        self._property_changed('corporateActionType')        

    @property
    def primeId(self):
        return self.__primeId

    @primeId.setter
    def primeId(self, value):
        self.__primeId = value
        self._property_changed('primeId')        

    @property
    def tenor2(self):
        return self.__tenor2

    @tenor2.setter
    def tenor2(self, value):
        self.__tenor2 = value
        self._property_changed('tenor2')        

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value
        self._property_changed('description')        

    @property
    def valueRevised(self):
        return self.__valueRevised

    @valueRevised.setter
    def valueRevised(self, value):
        self.__valueRevised = value
        self._property_changed('valueRevised')        

    @property
    def ownerName(self):
        return self.__ownerName

    @ownerName.setter
    def ownerName(self, value):
        self.__ownerName = value
        self._property_changed('ownerName')        

    @property
    def adjustedTradePrice(self):
        return self.__adjustedTradePrice

    @adjustedTradePrice.setter
    def adjustedTradePrice(self, value):
        self.__adjustedTradePrice = value
        self._property_changed('adjustedTradePrice')        

    @property
    def lastUpdatedById(self):
        return self.__lastUpdatedById

    @lastUpdatedById.setter
    def lastUpdatedById(self, value):
        self.__lastUpdatedById = value
        self._property_changed('lastUpdatedById')        

    @property
    def zScore(self):
        return self.__zScore

    @zScore.setter
    def zScore(self, value):
        self.__zScore = value
        self._property_changed('zScore')        

    @property
    def targetShareholderMeetingDate(self):
        return self.__targetShareholderMeetingDate

    @targetShareholderMeetingDate.setter
    def targetShareholderMeetingDate(self, value):
        self.__targetShareholderMeetingDate = value
        self._property_changed('targetShareholderMeetingDate')        

    @property
    def isADR(self):
        return self.__isADR

    @isADR.setter
    def isADR(self, value):
        self.__isADR = value
        self._property_changed('isADR')        

    @property
    def eventStartTime(self):
        return self.__eventStartTime

    @eventStartTime.setter
    def eventStartTime(self, value):
        self.__eventStartTime = value
        self._property_changed('eventStartTime')        

    @property
    def factor(self):
        return self.__factor

    @factor.setter
    def factor(self, value):
        self.__factor = value
        self._property_changed('factor')        

    @property
    def longConvictionSmall(self):
        return self.__longConvictionSmall

    @longConvictionSmall.setter
    def longConvictionSmall(self, value):
        self.__longConvictionSmall = value
        self._property_changed('longConvictionSmall')        

    @property
    def serviceId(self):
        return self.__serviceId

    @serviceId.setter
    def serviceId(self, value):
        self.__serviceId = value
        self._property_changed('serviceId')        

    @property
    def turnover(self):
        return self.__turnover

    @turnover.setter
    def turnover(self, value):
        self.__turnover = value
        self._property_changed('turnover')        

    @property
    def gsfeer(self):
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value):
        self.__gsfeer = value
        self._property_changed('gsfeer')        

    @property
    def coverage(self):
        return self.__coverage

    @coverage.setter
    def coverage(self, value):
        self.__coverage = value
        self._property_changed('coverage')        

    @property
    def backtestId(self):
        return self.__backtestId

    @backtestId.setter
    def backtestId(self, value):
        self.__backtestId = value
        self._property_changed('backtestId')        

    @property
    def gPercentile(self):
        return self.__gPercentile

    @gPercentile.setter
    def gPercentile(self, value):
        self.__gPercentile = value
        self._property_changed('gPercentile')        

    @property
    def gScore(self):
        return self.__gScore

    @gScore.setter
    def gScore(self, value):
        self.__gScore = value
        self._property_changed('gScore')        

    @property
    def marketValue(self):
        return self.__marketValue

    @marketValue.setter
    def marketValue(self, value):
        self.__marketValue = value
        self._property_changed('marketValue')        

    @property
    def multipleScore(self):
        return self.__multipleScore

    @multipleScore.setter
    def multipleScore(self, value):
        self.__multipleScore = value
        self._property_changed('multipleScore')        

    @property
    def sourceOriginalCategory(self):
        return self.__sourceOriginalCategory

    @sourceOriginalCategory.setter
    def sourceOriginalCategory(self, value):
        self.__sourceOriginalCategory = value
        self._property_changed('sourceOriginalCategory')        

    @property
    def betaAdjustedExposure(self):
        return self.__betaAdjustedExposure

    @betaAdjustedExposure.setter
    def betaAdjustedExposure(self, value):
        self.__betaAdjustedExposure = value
        self._property_changed('betaAdjustedExposure')        

    @property
    def dividendPoints(self):
        return self.__dividendPoints

    @dividendPoints.setter
    def dividendPoints(self, value):
        self.__dividendPoints = value
        self._property_changed('dividendPoints')        

    @property
    def newIdeasWtd(self):
        return self.__newIdeasWtd

    @newIdeasWtd.setter
    def newIdeasWtd(self, value):
        self.__newIdeasWtd = value
        self._property_changed('newIdeasWtd')        

    @property
    def short(self):
        return self.__short

    @short.setter
    def short(self, value):
        self.__short = value
        self._property_changed('short')        

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value
        self._property_changed('location')        

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        self.__comment = value
        self._property_changed('comment')        

    @property
    def bosInTicksDescription(self):
        return self.__bosInTicksDescription

    @bosInTicksDescription.setter
    def bosInTicksDescription(self, value):
        self.__bosInTicksDescription = value
        self._property_changed('bosInTicksDescription')        

    @property
    def sourceSymbol(self):
        return self.__sourceSymbol

    @sourceSymbol.setter
    def sourceSymbol(self, value):
        self.__sourceSymbol = value
        self._property_changed('sourceSymbol')        

    @property
    def scenarioId(self):
        return self.__scenarioId

    @scenarioId.setter
    def scenarioId(self, value):
        self.__scenarioId = value
        self._property_changed('scenarioId')        

    @property
    def askUnadjusted(self):
        return self.__askUnadjusted

    @askUnadjusted.setter
    def askUnadjusted(self, value):
        self.__askUnadjusted = value
        self._property_changed('askUnadjusted')        

    @property
    def queueClockTime(self):
        return self.__queueClockTime

    @queueClockTime.setter
    def queueClockTime(self, value):
        self.__queueClockTime = value
        self._property_changed('queueClockTime')        

    @property
    def askChange(self):
        return self.__askChange

    @askChange.setter
    def askChange(self, value):
        self.__askChange = value
        self._property_changed('askChange')        

    @property
    def tcmCostParticipationRate50Pct(self):
        return self.__tcmCostParticipationRate50Pct

    @tcmCostParticipationRate50Pct.setter
    def tcmCostParticipationRate50Pct(self, value):
        self.__tcmCostParticipationRate50Pct = value
        self._property_changed('tcmCostParticipationRate50Pct')        

    @property
    def normalizedPerformance(self):
        return self.__normalizedPerformance

    @normalizedPerformance.setter
    def normalizedPerformance(self, value):
        self.__normalizedPerformance = value
        self._property_changed('normalizedPerformance')        

    @property
    def cmId(self):
        return self.__cmId

    @cmId.setter
    def cmId(self, value):
        self.__cmId = value
        self._property_changed('cmId')        

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        

    @property
    def mdapi(self):
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value):
        self.__mdapi = value
        self._property_changed('mdapi')        

    @property
    def dividendYield(self):
        return self.__dividendYield

    @dividendYield.setter
    def dividendYield(self, value):
        self.__dividendYield = value
        self._property_changed('dividendYield')        

    @property
    def cumulativePnl(self):
        return self.__cumulativePnl

    @cumulativePnl.setter
    def cumulativePnl(self, value):
        self.__cumulativePnl = value
        self._property_changed('cumulativePnl')        

    @property
    def sourceOrigin(self):
        return self.__sourceOrigin

    @sourceOrigin.setter
    def sourceOrigin(self, value):
        self.__sourceOrigin = value
        self._property_changed('sourceOrigin')        

    @property
    def shortTenor(self):
        return self.__shortTenor

    @shortTenor.setter
    def shortTenor(self, value):
        self.__shortTenor = value
        self._property_changed('shortTenor')        

    @property
    def unadjustedVolume(self):
        return self.__unadjustedVolume

    @unadjustedVolume.setter
    def unadjustedVolume(self, value):
        self.__unadjustedVolume = value
        self._property_changed('unadjustedVolume')        

    @property
    def measures(self):
        return self.__measures

    @measures.setter
    def measures(self, value):
        self.__measures = value
        self._property_changed('measures')        

    @property
    def tradingCostPnl(self):
        return self.__tradingCostPnl

    @tradingCostPnl.setter
    def tradingCostPnl(self, value):
        self.__tradingCostPnl = value
        self._property_changed('tradingCostPnl')        

    @property
    def internalUser(self):
        return self.__internalUser

    @internalUser.setter
    def internalUser(self, value):
        self.__internalUser = value
        self._property_changed('internalUser')        

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value
        self._property_changed('price')        

    @property
    def paymentQuantity(self):
        return self.__paymentQuantity

    @paymentQuantity.setter
    def paymentQuantity(self, value):
        self.__paymentQuantity = value
        self._property_changed('paymentQuantity')        

    @property
    def underlyer(self):
        return self.__underlyer

    @underlyer.setter
    def underlyer(self, value):
        self.__underlyer = value
        self._property_changed('underlyer')        

    @property
    def positionIdx(self):
        return self.__positionIdx

    @positionIdx.setter
    def positionIdx(self, value):
        self.__positionIdx = value
        self._property_changed('positionIdx')        

    @property
    def secName(self):
        return self.__secName

    @secName.setter
    def secName(self, value):
        self.__secName = value
        self._property_changed('secName')        

    @property
    def percentADV(self):
        return self.__percentADV

    @percentADV.setter
    def percentADV(self, value):
        self.__percentADV = value
        self._property_changed('percentADV')        

    @property
    def unadjustedLow(self):
        return self.__unadjustedLow

    @unadjustedLow.setter
    def unadjustedLow(self, value):
        self.__unadjustedLow = value
        self._property_changed('unadjustedLow')        

    @property
    def contract(self):
        return self.__contract

    @contract.setter
    def contract(self, value):
        self.__contract = value
        self._property_changed('contract')        

    @property
    def sedol(self):
        return self.__sedol

    @sedol.setter
    def sedol(self, value):
        self.__sedol = value
        self._property_changed('sedol')        

    @property
    def roundingCostPnl(self):
        return self.__roundingCostPnl

    @roundingCostPnl.setter
    def roundingCostPnl(self, value):
        self.__roundingCostPnl = value
        self._property_changed('roundingCostPnl')        

    @property
    def sustainGlobal(self):
        return self.__sustainGlobal

    @sustainGlobal.setter
    def sustainGlobal(self, value):
        self.__sustainGlobal = value
        self._property_changed('sustainGlobal')        

    @property
    def sourceTicker(self):
        return self.__sourceTicker

    @sourceTicker.setter
    def sourceTicker(self, value):
        self.__sourceTicker = value
        self._property_changed('sourceTicker')        

    @property
    def portfolioId(self):
        return self.__portfolioId

    @portfolioId.setter
    def portfolioId(self, value):
        self.__portfolioId = value
        self._property_changed('portfolioId')        

    @property
    def gsid(self):
        return self.__gsid

    @gsid.setter
    def gsid(self, value):
        self.__gsid = value
        self._property_changed('gsid')        

    @property
    def esPercentile(self):
        return self.__esPercentile

    @esPercentile.setter
    def esPercentile(self, value):
        self.__esPercentile = value
        self._property_changed('esPercentile')        

    @property
    def tcmCostParticipationRate15Pct(self):
        return self.__tcmCostParticipationRate15Pct

    @tcmCostParticipationRate15Pct.setter
    def tcmCostParticipationRate15Pct(self, value):
        self.__tcmCostParticipationRate15Pct = value
        self._property_changed('tcmCostParticipationRate15Pct')        

    @property
    def sensitivity(self):
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        self.__sensitivity = value
        self._property_changed('sensitivity')        

    @property
    def fiscalYear(self):
        return self.__fiscalYear

    @fiscalYear.setter
    def fiscalYear(self, value):
        self.__fiscalYear = value
        self._property_changed('fiscalYear')        

    @property
    def rcic(self):
        return self.__rcic

    @rcic.setter
    def rcic(self, value):
        self.__rcic = value
        self._property_changed('rcic')        

    @property
    def simonAssetTags(self):
        return self.__simonAssetTags

    @simonAssetTags.setter
    def simonAssetTags(self, value):
        self.__simonAssetTags = value
        self._property_changed('simonAssetTags')        

    @property
    def internal(self):
        return self.__internal

    @internal.setter
    def internal(self, value):
        self.__internal = value
        self._property_changed('internal')        

    @property
    def forwardPoint(self):
        return self.__forwardPoint

    @forwardPoint.setter
    def forwardPoint(self, value):
        self.__forwardPoint = value
        self._property_changed('forwardPoint')        

    @property
    def assetClassificationsGicsIndustry(self):
        return self.__assetClassificationsGicsIndustry

    @assetClassificationsGicsIndustry.setter
    def assetClassificationsGicsIndustry(self, value):
        self.__assetClassificationsGicsIndustry = value
        self._property_changed('assetClassificationsGicsIndustry')        

    @property
    def adjustedBidPrice(self):
        return self.__adjustedBidPrice

    @adjustedBidPrice.setter
    def adjustedBidPrice(self, value):
        self.__adjustedBidPrice = value
        self._property_changed('adjustedBidPrice')        

    @property
    def hitRateQtd(self):
        return self.__hitRateQtd

    @hitRateQtd.setter
    def hitRateQtd(self, value):
        self.__hitRateQtd = value
        self._property_changed('hitRateQtd')        

    @property
    def varSwap(self):
        return self.__varSwap

    @varSwap.setter
    def varSwap(self, value):
        self.__varSwap = value
        self._property_changed('varSwap')        

    @property
    def lowUnadjusted(self):
        return self.__lowUnadjusted

    @lowUnadjusted.setter
    def lowUnadjusted(self, value):
        self.__lowUnadjusted = value
        self._property_changed('lowUnadjusted')        

    @property
    def sectorsRaw(self):
        return self.__sectorsRaw

    @sectorsRaw.setter
    def sectorsRaw(self, value):
        self.__sectorsRaw = value
        self._property_changed('sectorsRaw')        

    @property
    def low(self):
        return self.__low

    @low.setter
    def low(self, value):
        self.__low = value
        self._property_changed('low')        

    @property
    def crossGroup(self):
        return self.__crossGroup

    @crossGroup.setter
    def crossGroup(self, value):
        self.__crossGroup = value
        self._property_changed('crossGroup')        

    @property
    def integratedScore(self):
        return self.__integratedScore

    @integratedScore.setter
    def integratedScore(self, value):
        self.__integratedScore = value
        self._property_changed('integratedScore')        

    @property
    def tradeSize(self):
        return self.__tradeSize

    @tradeSize.setter
    def tradeSize(self, value):
        self.__tradeSize = value
        self._property_changed('tradeSize')        

    @property
    def symbolDimensions(self):
        return self.__symbolDimensions

    @symbolDimensions.setter
    def symbolDimensions(self, value):
        self.__symbolDimensions = value
        self._property_changed('symbolDimensions')        

    @property
    def scenarioGroupId(self):
        return self.__scenarioGroupId

    @scenarioGroupId.setter
    def scenarioGroupId(self, value):
        self.__scenarioGroupId = value
        self._property_changed('scenarioGroupId')        

    @property
    def errorMessage(self):
        return self.__errorMessage

    @errorMessage.setter
    def errorMessage(self, value):
        self.__errorMessage = value
        self._property_changed('errorMessage')        

    @property
    def avgTradeRateDescription(self):
        return self.__avgTradeRateDescription

    @avgTradeRateDescription.setter
    def avgTradeRateDescription(self, value):
        self.__avgTradeRateDescription = value
        self._property_changed('avgTradeRateDescription')        

    @property
    def midPrice(self):
        return self.__midPrice

    @midPrice.setter
    def midPrice(self, value):
        self.__midPrice = value
        self._property_changed('midPrice')        

    @property
    def fraction(self):
        return self.__fraction

    @fraction.setter
    def fraction(self, value):
        self.__fraction = value
        self._property_changed('fraction')        

    @property
    def stsCreditMarket(self):
        return self.__stsCreditMarket

    @stsCreditMarket.setter
    def stsCreditMarket(self, value):
        self.__stsCreditMarket = value
        self._property_changed('stsCreditMarket')        

    @property
    def assetCountShort(self):
        return self.__assetCountShort

    @assetCountShort.setter
    def assetCountShort(self, value):
        self.__assetCountShort = value
        self._property_changed('assetCountShort')        

    @property
    def stsEmDm(self):
        return self.__stsEmDm

    @stsEmDm.setter
    def stsEmDm(self, value):
        self.__stsEmDm = value
        self._property_changed('stsEmDm')        

    @property
    def tcmCostHorizon2Day(self):
        return self.__tcmCostHorizon2Day

    @tcmCostHorizon2Day.setter
    def tcmCostHorizon2Day(self, value):
        self.__tcmCostHorizon2Day = value
        self._property_changed('tcmCostHorizon2Day')        

    @property
    def queueInLots(self):
        return self.__queueInLots

    @queueInLots.setter
    def queueInLots(self, value):
        self.__queueInLots = value
        self._property_changed('queueInLots')        

    @property
    def priceRangeInTicksDescription(self):
        return self.__priceRangeInTicksDescription

    @priceRangeInTicksDescription.setter
    def priceRangeInTicksDescription(self, value):
        self.__priceRangeInTicksDescription = value
        self._property_changed('priceRangeInTicksDescription')        

    @property
    def tenderOfferExpirationDate(self):
        return self.__tenderOfferExpirationDate

    @tenderOfferExpirationDate.setter
    def tenderOfferExpirationDate(self, value):
        self.__tenderOfferExpirationDate = value
        self._property_changed('tenderOfferExpirationDate')        

    @property
    def highUnadjusted(self):
        return self.__highUnadjusted

    @highUnadjusted.setter
    def highUnadjusted(self, value):
        self.__highUnadjusted = value
        self._property_changed('highUnadjusted')        

    @property
    def sourceCategory(self):
        return self.__sourceCategory

    @sourceCategory.setter
    def sourceCategory(self, value):
        self.__sourceCategory = value
        self._property_changed('sourceCategory')        

    @property
    def volumeUnadjusted(self):
        return self.__volumeUnadjusted

    @volumeUnadjusted.setter
    def volumeUnadjusted(self, value):
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
    def tcmCostParticipationRate5Pct(self):
        return self.__tcmCostParticipationRate5Pct

    @tcmCostParticipationRate5Pct.setter
    def tcmCostParticipationRate5Pct(self, value):
        self.__tcmCostParticipationRate5Pct = value
        self._property_changed('tcmCostParticipationRate5Pct')        

    @property
    def isActive(self):
        return self.__isActive

    @isActive.setter
    def isActive(self, value):
        self.__isActive = value
        self._property_changed('isActive')        

    @property
    def growthScore(self):
        return self.__growthScore

    @growthScore.setter
    def growthScore(self, value):
        self.__growthScore = value
        self._property_changed('growthScore')        

    @property
    def encodedStats(self):
        return self.__encodedStats

    @encodedStats.setter
    def encodedStats(self, value):
        self.__encodedStats = value
        self._property_changed('encodedStats')        

    @property
    def adjustedShortInterest(self):
        return self.__adjustedShortInterest

    @adjustedShortInterest.setter
    def adjustedShortInterest(self, value):
        self.__adjustedShortInterest = value
        self._property_changed('adjustedShortInterest')        

    @property
    def askSize(self):
        return self.__askSize

    @askSize.setter
    def askSize(self, value):
        self.__askSize = value
        self._property_changed('askSize')        

    @property
    def mdapiType(self):
        return self.__mdapiType

    @mdapiType.setter
    def mdapiType(self, value):
        self.__mdapiType = value
        self._property_changed('mdapiType')        

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        self.__group = value
        self._property_changed('group')        

    @property
    def estimatedSpread(self):
        return self.__estimatedSpread

    @estimatedSpread.setter
    def estimatedSpread(self, value):
        self.__estimatedSpread = value
        self._property_changed('estimatedSpread')        

    @property
    def resource(self):
        return self.__resource

    @resource.setter
    def resource(self, value):
        self.__resource = value
        self._property_changed('resource')        

    @property
    def tcmCost(self):
        return self.__tcmCost

    @tcmCost.setter
    def tcmCost(self, value):
        self.__tcmCost = value
        self._property_changed('tcmCost')        

    @property
    def sustainJapan(self):
        return self.__sustainJapan

    @sustainJapan.setter
    def sustainJapan(self, value):
        self.__sustainJapan = value
        self._property_changed('sustainJapan')        

    @property
    def navSpread(self):
        return self.__navSpread

    @navSpread.setter
    def navSpread(self, value):
        self.__navSpread = value
        self._property_changed('navSpread')        

    @property
    def bidPrice(self):
        return self.__bidPrice

    @bidPrice.setter
    def bidPrice(self, value):
        self.__bidPrice = value
        self._property_changed('bidPrice')        

    @property
    def hedgeTrackingError(self):
        return self.__hedgeTrackingError

    @hedgeTrackingError.setter
    def hedgeTrackingError(self, value):
        self.__hedgeTrackingError = value
        self._property_changed('hedgeTrackingError')        

    @property
    def marketCapCategory(self):
        return self.__marketCapCategory

    @marketCapCategory.setter
    def marketCapCategory(self, value):
        self.__marketCapCategory = value
        self._property_changed('marketCapCategory')        

    @property
    def historicalVolume(self):
        return self.__historicalVolume

    @historicalVolume.setter
    def historicalVolume(self, value):
        self.__historicalVolume = value
        self._property_changed('historicalVolume')        

    @property
    def esNumericPercentile(self):
        return self.__esNumericPercentile

    @esNumericPercentile.setter
    def esNumericPercentile(self, value):
        self.__esNumericPercentile = value
        self._property_changed('esNumericPercentile')        

    @property
    def strikePrice(self):
        return self.__strikePrice

    @strikePrice.setter
    def strikePrice(self, value):
        self.__strikePrice = value
        self._property_changed('strikePrice')        

    @property
    def calSpreadMisPricing(self):
        return self.__calSpreadMisPricing

    @calSpreadMisPricing.setter
    def calSpreadMisPricing(self, value):
        self.__calSpreadMisPricing = value
        self._property_changed('calSpreadMisPricing')        

    @property
    def equityGamma(self):
        return self.__equityGamma

    @equityGamma.setter
    def equityGamma(self, value):
        self.__equityGamma = value
        self._property_changed('equityGamma')        

    @property
    def grossIncome(self):
        return self.__grossIncome

    @grossIncome.setter
    def grossIncome(self, value):
        self.__grossIncome = value
        self._property_changed('grossIncome')        

    @property
    def emId(self):
        return self.__emId

    @emId.setter
    def emId(self, value):
        self.__emId = value
        self._property_changed('emId')        

    @property
    def adjustedOpenPrice(self):
        return self.__adjustedOpenPrice

    @adjustedOpenPrice.setter
    def adjustedOpenPrice(self, value):
        self.__adjustedOpenPrice = value
        self._property_changed('adjustedOpenPrice')        

    @property
    def assetCountInModel(self):
        return self.__assetCountInModel

    @assetCountInModel.setter
    def assetCountInModel(self, value):
        self.__assetCountInModel = value
        self._property_changed('assetCountInModel')        

    @property
    def stsCreditRegion(self):
        return self.__stsCreditRegion

    @stsCreditRegion.setter
    def stsCreditRegion(self, value):
        self.__stsCreditRegion = value
        self._property_changed('stsCreditRegion')        

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        self.__point = value
        self._property_changed('point')        

    @property
    def lender(self):
        return self.__lender

    @lender.setter
    def lender(self, value):
        self.__lender = value
        self._property_changed('lender')        

    @property
    def minTemperature(self):
        return self.__minTemperature

    @minTemperature.setter
    def minTemperature(self, value):
        self.__minTemperature = value
        self._property_changed('minTemperature')        

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self._property_changed('value')        

    @property
    def relativeStrike(self):
        return self.__relativeStrike

    @relativeStrike.setter
    def relativeStrike(self, value):
        self.__relativeStrike = value
        self._property_changed('relativeStrike')        

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = value
        self._property_changed('amount')        

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def reportId(self):
        return self.__reportId

    @reportId.setter
    def reportId(self, value):
        self.__reportId = value
        self._property_changed('reportId')        

    @property
    def indexWeight(self):
        return self.__indexWeight

    @indexWeight.setter
    def indexWeight(self, value):
        self.__indexWeight = value
        self._property_changed('indexWeight')        

    @property
    def rebate(self):
        return self.__rebate

    @rebate.setter
    def rebate(self, value):
        self.__rebate = value
        self._property_changed('rebate')        

    @property
    def trader(self):
        return self.__trader

    @trader.setter
    def trader(self, value):
        self.__trader = value
        self._property_changed('trader')        

    @property
    def factorCategory(self):
        return self.__factorCategory

    @factorCategory.setter
    def factorCategory(self, value):
        self.__factorCategory = value
        self._property_changed('factorCategory')        

    @property
    def impliedVolatility(self):
        return self.__impliedVolatility

    @impliedVolatility.setter
    def impliedVolatility(self, value):
        self.__impliedVolatility = value
        self._property_changed('impliedVolatility')        

    @property
    def spread(self):
        return self.__spread

    @spread.setter
    def spread(self, value):
        self.__spread = value
        self._property_changed('spread')        

    @property
    def stsRatesMaturity(self):
        return self.__stsRatesMaturity

    @stsRatesMaturity.setter
    def stsRatesMaturity(self, value):
        self.__stsRatesMaturity = value
        self._property_changed('stsRatesMaturity')        

    @property
    def equityDelta(self):
        return self.__equityDelta

    @equityDelta.setter
    def equityDelta(self, value):
        self.__equityDelta = value
        self._property_changed('equityDelta')        

    @property
    def grossWeight(self):
        return self.__grossWeight

    @grossWeight.setter
    def grossWeight(self, value):
        self.__grossWeight = value
        self._property_changed('grossWeight')        

    @property
    def listed(self):
        return self.__listed

    @listed.setter
    def listed(self, value):
        self.__listed = value
        self._property_changed('listed')        

    @property
    def tcmCostHorizon6Hour(self):
        return self.__tcmCostHorizon6Hour

    @tcmCostHorizon6Hour.setter
    def tcmCostHorizon6Hour(self, value):
        self.__tcmCostHorizon6Hour = value
        self._property_changed('tcmCostHorizon6Hour')        

    @property
    def g10Currency(self):
        return self.__g10Currency

    @g10Currency.setter
    def g10Currency(self, value):
        self.__g10Currency = value
        self._property_changed('g10Currency')        

    @property
    def shockStyle(self):
        return self.__shockStyle

    @shockStyle.setter
    def shockStyle(self, value):
        self.__shockStyle = value
        self._property_changed('shockStyle')        

    @property
    def relativePeriod(self):
        return self.__relativePeriod

    @relativePeriod.setter
    def relativePeriod(self, value):
        self.__relativePeriod = value
        self._property_changed('relativePeriod')        

    @property
    def isin(self):
        return self.__isin

    @isin.setter
    def isin(self, value):
        self.__isin = value
        self._property_changed('isin')        

    @property
    def methodology(self):
        return self.__methodology

    @methodology.setter
    def methodology(self, value):
        self.__methodology = value
        self._property_changed('methodology')        


class GIRDomain(Base):
               
    def __init__(self, documentLinks: Iterable['Link'] = None):
        super().__init__()
        self.__documentLinks = documentLinks

    @property
    def documentLinks(self) -> Iterable['Link']:
        """Documents related to this asset"""
        return self.__documentLinks

    @documentLinks.setter
    def documentLinks(self, value: Iterable['Link']):
        self.__documentLinks = value
        self._property_changed('documentLinks')        


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
