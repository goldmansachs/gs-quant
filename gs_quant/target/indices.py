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


class MarketDataVendor(EnumBase, Enum):    
    
    Goldman_Sachs = 'Goldman Sachs'
    Thomson_Reuters = 'Thomson Reuters'
    Solactive = 'Solactive'
    WM = 'WM'
    
    def __repr__(self):
        return self.value


class IndicesCurrency(EnumBase, Enum):    
    
    """Currencies supported for Indices"""

    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    CAD = 'CAD'
    AUD = 'AUD'
    CHF = 'CHF'
    CNY = 'CNY'
    DKK = 'DKK'
    HKD = 'HKD'
    IDR = 'IDR'
    INR = 'INR'
    JPY = 'JPY'
    KRW = 'KRW'
    MXN = 'MXN'
    MYR = 'MYR'
    NOK = 'NOK'
    NZD = 'NZD'
    RUB = 'RUB'
    SEK = 'SEK'
    SGD = 'SGD'
    THB = 'THB'
    TRY = 'TRY'
    TWD = 'TWD'
    ZAR = 'ZAR'
    
    def __repr__(self):
        return self.value


class TradeType(EnumBase, Enum):    
    
    """Direction"""

    Buy = 'Buy'
    Sell = 'Sell'
    
    def __repr__(self):
        return self.value


class OptionStrikeType(EnumBase, Enum):    
    
    Relative = 'Relative'
    Delta = 'Delta'
    
    def __repr__(self):
        return self.value


class IndicesCreateInputs(Base):
        
    """Inputs used to create an index"""
       
    def __init__(self, ticker: str, name: str, pricingParameters: Union['IndicesPriceParameters', str], positionSet: Iterable['PositionPriceInput'], description: Union[str, str] = None, styles=None, relatedContent: Union['GIRDomain', str] = None, returnType: str = 'Price Return', publishParameters: Union['PublishParameters', str] = None):
        super().__init__()
        self.__ticker = ticker
        self.__name = name
        self.__description = description
        self.__styles = styles
        self.__relatedContent = relatedContent
        self.__returnType = returnType
        self.__positionSet = positionSet
        self.__publishParameters = publishParameters
        self.__pricingParameters = pricingParameters

    @property
    def ticker(self) -> str:
        """Ticker Identifier of the new asset (Prefix with 'GS' to publish to Bloomberg)"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self.__ticker = value
        self._property_changed('ticker')        

    @property
    def name(self) -> str:
        """Display name of the index"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def description(self) -> Union[str, str]:
        """Free text description of asset, default to empty. Description provided will be indexed in the search service for free text relevance match."""
        return self.__description

    @description.setter
    def description(self, value: Union[str, str]):
        self.__description = value
        self._property_changed('description')        

    @property
    def styles(self):
        """Styles or themes associated with the asset (max 50), default to Bespoke"""
        return self.__styles

    @styles.setter
    def styles(self, value):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def relatedContent(self) -> Union['GIRDomain', str]:
        """Links to content related to this index or any of its constituents (optional)"""
        return self.__relatedContent

    @relatedContent.setter
    def relatedContent(self, value: Union['GIRDomain', str]):
        self.__relatedContent = value
        self._property_changed('relatedContent')        

    @property
    def returnType(self) -> str:
        """Determines the index calculation methodology with respect to dividend reinvestment, default to Price Return"""
        return self.__returnType

    @returnType.setter
    def returnType(self, value: str):
        self.__returnType = value
        self._property_changed('returnType')        

    @property
    def positionSet(self) -> Iterable['PositionPriceInput']:
        """Information of constituents associated with the index. Need to supply one of weight, quantity."""
        return self.__positionSet

    @positionSet.setter
    def positionSet(self, value: Iterable['PositionPriceInput']):
        self.__positionSet = value
        self._property_changed('positionSet')        

    @property
    def publishParameters(self) -> Union['PublishParameters', str]:
        """Publishing parameters to determine where and how to publish indices, default all to false"""
        return self.__publishParameters

    @publishParameters.setter
    def publishParameters(self, value: Union['PublishParameters', str]):
        self.__publishParameters = value
        self._property_changed('publishParameters')        

    @property
    def pricingParameters(self) -> Union['IndicesPriceParameters', str]:
        """Parameters for pricing indices"""
        return self.__pricingParameters

    @pricingParameters.setter
    def pricingParameters(self, value: Union['IndicesPriceParameters', str]):
        self.__pricingParameters = value
        self._property_changed('pricingParameters')        


class IndicesPriceParameters(Base):
        
    """Parameters for pricing indices"""
       
    def __init__(self, currency: Union['IndicesCurrency', str] = 'USD', divisor: float = None, initialPrice: float = None, targetNotional: float = None, weightingStrategy: str = None):
        super().__init__()
        self.__currency = currency
        self.__divisor = divisor
        self.__initialPrice = initialPrice
        self.__targetNotional = targetNotional
        self.__weightingStrategy = weightingStrategy

    @property
    def currency(self) -> Union['IndicesCurrency', str]:
        """Currencies supported for Indices, default to USD"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union['IndicesCurrency', str]):
        self.__currency = value
        self._property_changed('currency')        

    @property
    def divisor(self) -> float:
        """Divisor to be applied to the overall position set"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: float):
        self.__divisor = value
        self._property_changed('divisor')        

    @property
    def initialPrice(self) -> float:
        """Initial overall price for the position set"""
        return self.__initialPrice

    @initialPrice.setter
    def initialPrice(self, value: float):
        self.__initialPrice = value
        self._property_changed('initialPrice')        

    @property
    def targetNotional(self) -> float:
        """Target notional for the position set"""
        return self.__targetNotional

    @targetNotional.setter
    def targetNotional(self, value: float):
        self.__targetNotional = value
        self._property_changed('targetNotional')        

    @property
    def weightingStrategy(self) -> str:
        """Strategy used to price the position set. If not supplied, it is inferred from the quantities or weights in the positions."""
        return self.__weightingStrategy

    @weightingStrategy.setter
    def weightingStrategy(self, value: str):
        self.__weightingStrategy = value
        self._property_changed('weightingStrategy')        


class PublishParameters(Base):
        
    """Publishing parameters to determine where and how to publish indices, default all to false"""
       
    def __init__(self, publishToReuters: bool, publishToBloomberg: bool, includePriceHistory: bool):
        super().__init__()
        self.__includePriceHistory = includePriceHistory
        self.__publishToBloomberg = publishToBloomberg
        self.__publishToReuters = publishToReuters

    @property
    def includePriceHistory(self) -> bool:
        """Include full price history, default to false"""
        return self.__includePriceHistory

    @includePriceHistory.setter
    def includePriceHistory(self, value: bool):
        self.__includePriceHistory = value
        self._property_changed('includePriceHistory')        

    @property
    def publishToBloomberg(self) -> bool:
        """Publish Basket to Bloomberg, default to false"""
        return self.__publishToBloomberg

    @publishToBloomberg.setter
    def publishToBloomberg(self, value: bool):
        self.__publishToBloomberg = value
        self._property_changed('publishToBloomberg')        

    @property
    def publishToReuters(self) -> bool:
        """Publish Basket to Reuters, default to false"""
        return self.__publishToReuters

    @publishToReuters.setter
    def publishToReuters(self, value: bool):
        self.__publishToReuters = value
        self._property_changed('publishToReuters')        


class PositionPriceInput(Base):
               
    def __init__(self, assetId: Union[str, str], quantity: float = None, weight: float = None, notional: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__quantity = quantity
        self.__weight = weight
        self.__notional = notional

    @property
    def assetId(self) -> Union[str, str]:
        """Marquee unique identifier"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        

    @property
    def quantity(self) -> float:
        """Quantity of the given position"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value
        self._property_changed('quantity')        

    @property
    def weight(self) -> float:
        """Relative weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value
        self._property_changed('weight')        

    @property
    def notional(self) -> float:
        """Notional of the given position"""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value
        self._property_changed('notional')        


class CustomBasketsResponse(Base):
        
    """Rebalance custom basket response"""
       
    def __init__(self, status: str = None, approvalId: Union[str, str] = None, reportId: Union[str, str] = None, assetId: Union[str, str] = None):
        super().__init__()
        self.__status = status
        self.__approvalId = approvalId
        self.__reportId = reportId
        self.__assetId = assetId

    @property
    def status(self) -> str:
        """Indices rebalance process status. Status is done if basket assets rebalance, report creation and scheduling are all successfully executed."""
        return self.__status

    @status.setter
    def status(self, value: str):
        self.__status = value
        self._property_changed('status')        

    @property
    def approvalId(self) -> Union[str, str]:
        """Marquee unique identifier of approval created"""
        return self.__approvalId

    @approvalId.setter
    def approvalId(self, value: Union[str, str]):
        self.__approvalId = value
        self._property_changed('approvalId')        

    @property
    def reportId(self) -> Union[str, str]:
        """Marquee unique identifier of report created"""
        return self.__reportId

    @reportId.setter
    def reportId(self, value: Union[str, str]):
        self.__reportId = value
        self._property_changed('reportId')        

    @property
    def assetId(self) -> Union[str, str]:
        """Marquee unique identifier of asset created"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: Union[str, str]):
        self.__assetId = value
        self._property_changed('assetId')        


class ApprovalAction(Base):
        
    """Comments for the approval action"""
       
    def __init__(self, comment: str = None):
        super().__init__()
        self.__comment = comment

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self.__comment = value
        self._property_changed('comment')        


class ISelectResponse(Base):
               
    def __init__(self, __TYPE: str = None, Action=None, ActionComment: str = None, assetName: str = None, assetShortName: str = None, availableActionConfirms: Iterable[Any] = None, availableActions: Iterable[Any] = None, availableRebalanceDates: Iterable[str] = None, constituentValidations: Iterable[Any] = None, dateValidationStatus: str = None, dateValidations: Iterable[Any] = None, entryMode: str = None, entryType: str = None, internalRebalance: int = None, indexParameterDefinitions: Iterable[Any] = None, indexParameters: Iterable[Any] = None, indexParameterValidation: Iterable[Any] = None, newUnits: Iterable['ISelectNewUnit'] = None, newWeights: Iterable['ISelectNewWeight'] = None, notificationDate: str = None, rebalanceDate=None, rebalanceDeterminationDate: str = None, rebDeterminationIndexLevel: Union[float, str] = None, requestCounter: int = None, series: Union['ISelectSeries', str] = None, status=None, submissionData: Iterable[Any] = None, submissionDataColumns: Iterable['ISelectConstituentColumn'] = None, submissionText: str = None, valid: int = None, validationMessages: Iterable[str] = None):
        super().__init__()
        self.____TYPE = __TYPE
        self.__Action = Action
        self.__ActionComment = ActionComment
        self.__assetName = assetName
        self.__assetShortName = assetShortName
        self.__availableActionConfirms = availableActionConfirms
        self.__availableActions = availableActions
        self.__availableRebalanceDates = availableRebalanceDates
        self.__constituentValidations = constituentValidations
        self.__dateValidationStatus = dateValidationStatus
        self.__dateValidations = dateValidations
        self.__entryMode = entryMode
        self.__entryType = entryType
        self.__internalRebalance = internalRebalance
        self.__indexParameterDefinitions = indexParameterDefinitions
        self.__indexParameters = indexParameters
        self.__indexParameterValidation = indexParameterValidation
        self.__newUnits = newUnits
        self.__newWeights = newWeights
        self.__notificationDate = notificationDate
        self.__rebalanceDate = rebalanceDate
        self.__rebalanceDeterminationDate = rebalanceDeterminationDate
        self.__rebDeterminationIndexLevel = rebDeterminationIndexLevel
        self.__requestCounter = requestCounter
        self.__series = series
        self.__status = status
        self.__submissionData = submissionData
        self.__submissionDataColumns = submissionDataColumns
        self.__submissionText = submissionText
        self.__valid = valid
        self.__validationMessages = validationMessages

    @property
    def __TYPE(self) -> str:
        return self.____TYPE

    @__TYPE.setter
    def __TYPE(self, value: str):
        self.____TYPE = value
        self._property_changed('__TYPE')        

    @property
    def Action(self):
        """Rebalance type"""
        return self.__Action

    @Action.setter
    def Action(self, value):
        self.__Action = value
        self._property_changed('Action')        

    @property
    def ActionComment(self) -> str:
        """Comment for request the action"""
        return self.__ActionComment

    @ActionComment.setter
    def ActionComment(self, value: str):
        self.__ActionComment = value
        self._property_changed('ActionComment')        

    @property
    def assetName(self) -> str:
        """Asset name"""
        return self.__assetName

    @assetName.setter
    def assetName(self, value: str):
        self.__assetName = value
        self._property_changed('assetName')        

    @property
    def assetShortName(self) -> str:
        """Short name of asset which can be displayed where there are constraints on space."""
        return self.__assetShortName

    @assetShortName.setter
    def assetShortName(self, value: str):
        self.__assetShortName = value
        self._property_changed('assetShortName')        

    @property
    def availableActionConfirms(self) -> Iterable[Any]:
        return self.__availableActionConfirms

    @availableActionConfirms.setter
    def availableActionConfirms(self, value: Iterable[Any]):
        self.__availableActionConfirms = value
        self._property_changed('availableActionConfirms')        

    @property
    def availableActions(self) -> Iterable[Any]:
        return self.__availableActions

    @availableActions.setter
    def availableActions(self, value: Iterable[Any]):
        self.__availableActions = value
        self._property_changed('availableActions')        

    @property
    def availableRebalanceDates(self) -> Iterable[str]:
        return self.__availableRebalanceDates

    @availableRebalanceDates.setter
    def availableRebalanceDates(self, value: Iterable[str]):
        self.__availableRebalanceDates = value
        self._property_changed('availableRebalanceDates')        

    @property
    def constituentValidations(self) -> Iterable[Any]:
        return self.__constituentValidations

    @constituentValidations.setter
    def constituentValidations(self, value: Iterable[Any]):
        self.__constituentValidations = value
        self._property_changed('constituentValidations')        

    @property
    def dateValidationStatus(self) -> str:
        return self.__dateValidationStatus

    @dateValidationStatus.setter
    def dateValidationStatus(self, value: str):
        self.__dateValidationStatus = value
        self._property_changed('dateValidationStatus')        

    @property
    def dateValidations(self) -> Iterable[Any]:
        return self.__dateValidations

    @dateValidations.setter
    def dateValidations(self, value: Iterable[Any]):
        self.__dateValidations = value
        self._property_changed('dateValidations')        

    @property
    def entryMode(self) -> str:
        return self.__entryMode

    @entryMode.setter
    def entryMode(self, value: str):
        self.__entryMode = value
        self._property_changed('entryMode')        

    @property
    def entryType(self) -> str:
        return self.__entryType

    @entryType.setter
    def entryType(self, value: str):
        self.__entryType = value
        self._property_changed('entryType')        

    @property
    def internalRebalance(self) -> int:
        """Indicate if Workflow Sender User is internal user"""
        return self.__internalRebalance

    @internalRebalance.setter
    def internalRebalance(self, value: int):
        self.__internalRebalance = value
        self._property_changed('internalRebalance')        

    @property
    def indexParameterDefinitions(self) -> Iterable[Any]:
        return self.__indexParameterDefinitions

    @indexParameterDefinitions.setter
    def indexParameterDefinitions(self, value: Iterable[Any]):
        self.__indexParameterDefinitions = value
        self._property_changed('indexParameterDefinitions')        

    @property
    def indexParameters(self) -> Iterable[Any]:
        return self.__indexParameters

    @indexParameters.setter
    def indexParameters(self, value: Iterable[Any]):
        self.__indexParameters = value
        self._property_changed('indexParameters')        

    @property
    def indexParameterValidation(self) -> Iterable[Any]:
        return self.__indexParameterValidation

    @indexParameterValidation.setter
    def indexParameterValidation(self, value: Iterable[Any]):
        self.__indexParameterValidation = value
        self._property_changed('indexParameterValidation')        

    @property
    def newUnits(self) -> Iterable['ISelectNewUnit']:
        return self.__newUnits

    @newUnits.setter
    def newUnits(self, value: Iterable['ISelectNewUnit']):
        self.__newUnits = value
        self._property_changed('newUnits')        

    @property
    def newWeights(self) -> Iterable['ISelectNewWeight']:
        return self.__newWeights

    @newWeights.setter
    def newWeights(self, value: Iterable['ISelectNewWeight']):
        self.__newWeights = value
        self._property_changed('newWeights')        

    @property
    def notificationDate(self) -> str:
        return self.__notificationDate

    @notificationDate.setter
    def notificationDate(self, value: str):
        self.__notificationDate = value
        self._property_changed('notificationDate')        

    @property
    def rebalanceDate(self):
        return self.__rebalanceDate

    @rebalanceDate.setter
    def rebalanceDate(self, value):
        self.__rebalanceDate = value
        self._property_changed('rebalanceDate')        

    @property
    def rebalanceDeterminationDate(self) -> str:
        return self.__rebalanceDeterminationDate

    @rebalanceDeterminationDate.setter
    def rebalanceDeterminationDate(self, value: str):
        self.__rebalanceDeterminationDate = value
        self._property_changed('rebalanceDeterminationDate')        

    @property
    def rebDeterminationIndexLevel(self) -> Union[float, str]:
        return self.__rebDeterminationIndexLevel

    @rebDeterminationIndexLevel.setter
    def rebDeterminationIndexLevel(self, value: Union[float, str]):
        self.__rebDeterminationIndexLevel = value
        self._property_changed('rebDeterminationIndexLevel')        

    @property
    def requestCounter(self) -> int:
        return self.__requestCounter

    @requestCounter.setter
    def requestCounter(self, value: int):
        self.__requestCounter = value
        self._property_changed('requestCounter')        

    @property
    def series(self) -> Union['ISelectSeries', str]:
        return self.__series

    @series.setter
    def series(self, value: Union['ISelectSeries', str]):
        self.__series = value
        self._property_changed('series')        

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        self._property_changed('status')        

    @property
    def submissionData(self) -> Iterable[Any]:
        return self.__submissionData

    @submissionData.setter
    def submissionData(self, value: Iterable[Any]):
        self.__submissionData = value
        self._property_changed('submissionData')        

    @property
    def submissionDataColumns(self) -> Iterable['ISelectConstituentColumn']:
        return self.__submissionDataColumns

    @submissionDataColumns.setter
    def submissionDataColumns(self, value: Iterable['ISelectConstituentColumn']):
        self.__submissionDataColumns = value
        self._property_changed('submissionDataColumns')        

    @property
    def submissionText(self) -> str:
        return self.__submissionText

    @submissionText.setter
    def submissionText(self, value: str):
        self.__submissionText = value
        self._property_changed('submissionText')        

    @property
    def valid(self) -> int:
        return self.__valid

    @valid.setter
    def valid(self, value: int):
        self.__valid = value
        self._property_changed('valid')        

    @property
    def validationMessages(self) -> Iterable[str]:
        return self.__validationMessages

    @validationMessages.setter
    def validationMessages(self, value: Iterable[str]):
        self.__validationMessages = value
        self._property_changed('validationMessages')        


class ISelectConstituentColumn(Base):
               
    def __init__(self, id: str, field: Union['ISelectNullableString', str], name: str, __TYPE: str = None, aggregatorString: Union['ISelectNullableString', str] = None, class_: Union['ISelectNullableString', str] = None, filter: Union['ISelectNullableString', str] = None, formatterString: Union['ISelectNullableString', str] = None, ID: int = None, maxWidth: int = None, minWidth: int = None, precision: int = None, sortable: int = None, tooltip: Union['ISelectNullableString', str] = None):
        super().__init__()
        self.____TYPE = __TYPE
        self.__aggregatorString = aggregatorString
        self.__class = class_
        self.__field = field
        self.__filter = filter
        self.__formatterString = formatterString
        self.__id = id
        self.__ID = ID
        self.__maxWidth = maxWidth
        self.__minWidth = minWidth
        self.__name = name
        self.__precision = precision
        self.__sortable = sortable
        self.__tooltip = tooltip

    @property
    def __TYPE(self) -> str:
        return self.____TYPE

    @__TYPE.setter
    def __TYPE(self, value: str):
        self.____TYPE = value
        self._property_changed('__TYPE')        

    @property
    def aggregatorString(self) -> Union['ISelectNullableString', str]:
        return self.__aggregatorString

    @aggregatorString.setter
    def aggregatorString(self, value: Union['ISelectNullableString', str]):
        self.__aggregatorString = value
        self._property_changed('aggregatorString')        

    @property
    def class_(self) -> Union['ISelectNullableString', str]:
        return self.__class

    @class_.setter
    def class_(self, value: Union['ISelectNullableString', str]):
        self.__class = value
        self._property_changed('class')        

    @property
    def field(self) -> Union['ISelectNullableString', str]:
        return self.__field

    @field.setter
    def field(self, value: Union['ISelectNullableString', str]):
        self.__field = value
        self._property_changed('field')        

    @property
    def filter(self) -> Union['ISelectNullableString', str]:
        return self.__filter

    @filter.setter
    def filter(self, value: Union['ISelectNullableString', str]):
        self.__filter = value
        self._property_changed('filter')        

    @property
    def formatterString(self) -> Union['ISelectNullableString', str]:
        return self.__formatterString

    @formatterString.setter
    def formatterString(self, value: Union['ISelectNullableString', str]):
        self.__formatterString = value
        self._property_changed('formatterString')        

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def ID(self) -> int:
        return self.__ID

    @ID.setter
    def ID(self, value: int):
        self.__ID = value
        self._property_changed('ID')        

    @property
    def maxWidth(self) -> int:
        return self.__maxWidth

    @maxWidth.setter
    def maxWidth(self, value: int):
        self.__maxWidth = value
        self._property_changed('maxWidth')        

    @property
    def minWidth(self) -> int:
        return self.__minWidth

    @minWidth.setter
    def minWidth(self, value: int):
        self.__minWidth = value
        self._property_changed('minWidth')        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def precision(self) -> int:
        return self.__precision

    @precision.setter
    def precision(self, value: int):
        self.__precision = value
        self._property_changed('precision')        

    @property
    def sortable(self) -> int:
        return self.__sortable

    @sortable.setter
    def sortable(self, value: int):
        self.__sortable = value
        self._property_changed('sortable')        

    @property
    def tooltip(self) -> Union['ISelectNullableString', str]:
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: Union['ISelectNullableString', str]):
        self.__tooltip = value
        self._property_changed('tooltip')        


class ISelectSeries(Base):
               
    def __init__(self, __TYPE: str = None, data: Iterable[Any] = None, identifier: str = None, identifierType: str = None, name: str = None):
        super().__init__()
        self.____TYPE = __TYPE
        self.__data = data
        self.__identifier = identifier
        self.__identifierType = identifierType
        self.__name = name

    @property
    def __TYPE(self) -> str:
        return self.____TYPE

    @__TYPE.setter
    def __TYPE(self, value: str):
        self.____TYPE = value
        self._property_changed('__TYPE')        

    @property
    def data(self) -> Iterable[Any]:
        return self.__data

    @data.setter
    def data(self, value: Iterable[Any]):
        self.__data = value
        self._property_changed('data')        

    @property
    def identifier(self) -> str:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str):
        self.__identifier = value
        self._property_changed('identifier')        

    @property
    def identifierType(self) -> str:
        return self.__identifierType

    @identifierType.setter
    def identifierType(self, value: str):
        self.__identifierType = value
        self._property_changed('identifierType')        

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        


class ISelectNewWeight(Base):
               
    def __init__(self, id: str, newWeight: Union[float, str] = None):
        super().__init__()
        self.__id = id
        self.__newWeight = newWeight

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def newWeight(self) -> Union[float, str]:
        return self.__newWeight

    @newWeight.setter
    def newWeight(self, value: Union[float, str]):
        self.__newWeight = value
        self._property_changed('newWeight')        


class ISelectNewUnit(Base):
               
    def __init__(self, id: str, newUnits: Union[float, str] = None):
        super().__init__()
        self.__id = id
        self.__newUnits = newUnits

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def newUnits(self) -> Union[float, str]:
        return self.__newUnits

    @newUnits.setter
    def newUnits(self, value: Union[float, str]):
        self.__newUnits = value
        self._property_changed('newUnits')        


class IndicesRebalanceInputs(Base):
               
    def __init__(self, parameters):
        super().__init__()
        self.__parameters = parameters

    @property
    def parameters(self):
        """The inputs used to rebalance an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value
        self._property_changed('parameters')        


class CustomBasketsRebalanceInputs(Base):
        
    """Inputs used to rebalance a custom basket"""
       
    def __init__(self, positionSet: Iterable['PositionPriceInput'] = None, publishParameters: Union['PublishParameters', str] = None, pricingParameters: Union['IndicesPriceParameters', str] = None):
        super().__init__()
        self.__positionSet = positionSet
        self.__publishParameters = publishParameters
        self.__pricingParameters = pricingParameters

    @property
    def positionSet(self) -> Iterable['PositionPriceInput']:
        """Information of constituents associated with the rebalance."""
        return self.__positionSet

    @positionSet.setter
    def positionSet(self, value: Iterable['PositionPriceInput']):
        self.__positionSet = value
        self._property_changed('positionSet')        

    @property
    def publishParameters(self) -> Union['PublishParameters', str]:
        """Publishing parameters to determine where and how to publish indices, default all to false"""
        return self.__publishParameters

    @publishParameters.setter
    def publishParameters(self, value: Union['PublishParameters', str]):
        self.__publishParameters = value
        self._property_changed('publishParameters')        

    @property
    def pricingParameters(self) -> Union['IndicesPriceParameters', str]:
        """Parameters for pricing indices"""
        return self.__pricingParameters

    @pricingParameters.setter
    def pricingParameters(self, value: Union['IndicesPriceParameters', str]):
        self.__pricingParameters = value
        self._property_changed('pricingParameters')        


class ISelectRebalance(Base):
               
    def __init__(self, newWeights: Iterable['ISelectNewWeight'] = None, rebalanceDate: str = None, newParameters: Iterable['ISelectNewParameter'] = None, indexParameters: Iterable['ISelectIndexParameters'] = None):
        super().__init__()
        self.__newWeights = newWeights
        self.__rebalanceDate = rebalanceDate
        self.__newParameters = newParameters
        self.__indexParameters = indexParameters

    @property
    def newWeights(self) -> Iterable['ISelectNewWeight']:
        """New Weight array to be updated"""
        return self.__newWeights

    @newWeights.setter
    def newWeights(self, value: Iterable['ISelectNewWeight']):
        self.__newWeights = value
        self._property_changed('newWeights')        

    @property
    def rebalanceDate(self) -> str:
        """Date the rebalance will occur"""
        return self.__rebalanceDate

    @rebalanceDate.setter
    def rebalanceDate(self, value: str):
        self.__rebalanceDate = value
        self._property_changed('rebalanceDate')        

    @property
    def newParameters(self) -> Iterable['ISelectNewParameter']:
        """New parameters to be updated"""
        return self.__newParameters

    @newParameters.setter
    def newParameters(self, value: Iterable['ISelectNewParameter']):
        self.__newParameters = value
        self._property_changed('newParameters')        

    @property
    def indexParameters(self) -> Iterable['ISelectIndexParameters']:
        """Index parameters to be updated"""
        return self.__indexParameters

    @indexParameters.setter
    def indexParameters(self, value: Iterable['ISelectIndexParameters']):
        self.__indexParameters = value
        self._property_changed('indexParameters')        


class ISelectIndexParameters(Base):
               
    def __init__(self, name: str = None, value: Union[float, str] = None):
        super().__init__()
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def value(self) -> Union[float, str]:
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self.__value = value
        self._property_changed('value')        


class ISelectNewParameter(Base):
               
    def __init__(self, earlyUnwindAfter: Union[float, str] = None, earlyUnwindApplicable: Union[str, str] = None, expiryDateRule: Union[str, str] = None, optionTargetExpiryParameter: Union[float, str] = None, optionEarlyUnwindDays: Union[float, str] = None, inAlpha: bool = None, isFSRTargetFactor: bool = None, fsrMaxRatio: Union[float, str] = None, fsrMinRatio: Union[float, str] = None, moduleEnabled: bool = None, moduleName: Union[str, str] = None, bloombergId: Union['ISelectNullableString', str] = None, stockId: Union['ISelectNullableString', str] = None, newWeight: Union[float, str] = None, notional: Union[float, str] = None, optionType: Union['OptionType', str] = None, optionStrikeType: Union['OptionStrikeType', str] = None, strikeRelative: Union[float, str] = None, tradeType: Union['TradeType', str] = None, signal: Union[float, str] = None, newSignal: Union[float, str] = None, newMinWeight: Union[float, str] = None, newMaxWeight: Union[float, str] = None, minWeight: Union[float, str] = None, maxWeight: Union[float, str] = None):
        super().__init__()
        self.__earlyUnwindAfter = earlyUnwindAfter
        self.__earlyUnwindApplicable = earlyUnwindApplicable
        self.__expiryDateRule = expiryDateRule
        self.__optionTargetExpiryParameter = optionTargetExpiryParameter
        self.__optionEarlyUnwindDays = optionEarlyUnwindDays
        self.__inAlpha = inAlpha
        self.__isFSRTargetFactor = isFSRTargetFactor
        self.__fsrMaxRatio = fsrMaxRatio
        self.__fsrMinRatio = fsrMinRatio
        self.__moduleEnabled = moduleEnabled
        self.__moduleName = moduleName
        self.__bloombergId = bloombergId
        self.__stockId = stockId
        self.__newWeight = newWeight
        self.__notional = notional
        self.__optionType = optionType
        self.__optionStrikeType = optionStrikeType
        self.__strikeRelative = strikeRelative
        self.__tradeType = tradeType
        self.__signal = signal
        self.__newSignal = newSignal
        self.__newMinWeight = newMinWeight
        self.__newMaxWeight = newMaxWeight
        self.__minWeight = minWeight
        self.__maxWeight = maxWeight

    @property
    def earlyUnwindAfter(self) -> Union[float, str]:
        return self.__earlyUnwindAfter

    @earlyUnwindAfter.setter
    def earlyUnwindAfter(self, value: Union[float, str]):
        self.__earlyUnwindAfter = value
        self._property_changed('earlyUnwindAfter')        

    @property
    def earlyUnwindApplicable(self) -> Union[str, str]:
        """Indicates whether the module can be unwinded early"""
        return self.__earlyUnwindApplicable

    @earlyUnwindApplicable.setter
    def earlyUnwindApplicable(self, value: Union[str, str]):
        self.__earlyUnwindApplicable = value
        self._property_changed('earlyUnwindApplicable')        

    @property
    def expiryDateRule(self) -> Union[str, str]:
        """Free text description of asset. Description provided will be indexed in the search service for free text relevance match"""
        return self.__expiryDateRule

    @expiryDateRule.setter
    def expiryDateRule(self, value: Union[str, str]):
        self.__expiryDateRule = value
        self._property_changed('expiryDateRule')        

    @property
    def optionTargetExpiryParameter(self) -> Union[float, str]:
        return self.__optionTargetExpiryParameter

    @optionTargetExpiryParameter.setter
    def optionTargetExpiryParameter(self, value: Union[float, str]):
        self.__optionTargetExpiryParameter = value
        self._property_changed('optionTargetExpiryParameter')        

    @property
    def optionEarlyUnwindDays(self) -> Union[float, str]:
        return self.__optionEarlyUnwindDays

    @optionEarlyUnwindDays.setter
    def optionEarlyUnwindDays(self, value: Union[float, str]):
        self.__optionEarlyUnwindDays = value
        self._property_changed('optionEarlyUnwindDays')        

    @property
    def inAlpha(self) -> bool:
        return self.__inAlpha

    @inAlpha.setter
    def inAlpha(self, value: bool):
        self.__inAlpha = value
        self._property_changed('inAlpha')        

    @property
    def isFSRTargetFactor(self) -> bool:
        return self.__isFSRTargetFactor

    @isFSRTargetFactor.setter
    def isFSRTargetFactor(self, value: bool):
        self.__isFSRTargetFactor = value
        self._property_changed('isFSRTargetFactor')        

    @property
    def fsrMaxRatio(self) -> Union[float, str]:
        return self.__fsrMaxRatio

    @fsrMaxRatio.setter
    def fsrMaxRatio(self, value: Union[float, str]):
        self.__fsrMaxRatio = value
        self._property_changed('fsrMaxRatio')        

    @property
    def fsrMinRatio(self) -> Union[float, str]:
        return self.__fsrMinRatio

    @fsrMinRatio.setter
    def fsrMinRatio(self, value: Union[float, str]):
        self.__fsrMinRatio = value
        self._property_changed('fsrMinRatio')        

    @property
    def moduleEnabled(self) -> bool:
        """Enable to disable the module"""
        return self.__moduleEnabled

    @moduleEnabled.setter
    def moduleEnabled(self, value: bool):
        self.__moduleEnabled = value
        self._property_changed('moduleEnabled')        

    @property
    def moduleName(self) -> Union[str, str]:
        """Free text description of asset. Description provided will be indexed in the search service for free text relevance match"""
        return self.__moduleName

    @moduleName.setter
    def moduleName(self, value: Union[str, str]):
        self.__moduleName = value
        self._property_changed('moduleName')        

    @property
    def bloombergId(self) -> Union['ISelectNullableString', str]:
        return self.__bloombergId

    @bloombergId.setter
    def bloombergId(self, value: Union['ISelectNullableString', str]):
        self.__bloombergId = value
        self._property_changed('bloombergId')        

    @property
    def stockId(self) -> Union['ISelectNullableString', str]:
        return self.__stockId

    @stockId.setter
    def stockId(self, value: Union['ISelectNullableString', str]):
        self.__stockId = value
        self._property_changed('stockId')        

    @property
    def newWeight(self) -> Union[float, str]:
        return self.__newWeight

    @newWeight.setter
    def newWeight(self, value: Union[float, str]):
        self.__newWeight = value
        self._property_changed('newWeight')        

    @property
    def notional(self) -> Union[float, str]:
        return self.__notional

    @notional.setter
    def notional(self, value: Union[float, str]):
        self.__notional = value
        self._property_changed('notional')        

    @property
    def optionType(self) -> Union['OptionType', str]:
        return self.__optionType

    @optionType.setter
    def optionType(self, value: Union['OptionType', str]):
        self.__optionType = value
        self._property_changed('optionType')        

    @property
    def optionStrikeType(self) -> Union['OptionStrikeType', str]:
        return self.__optionStrikeType

    @optionStrikeType.setter
    def optionStrikeType(self, value: Union['OptionStrikeType', str]):
        self.__optionStrikeType = value
        self._property_changed('optionStrikeType')        

    @property
    def strikeRelative(self) -> Union[float, str]:
        return self.__strikeRelative

    @strikeRelative.setter
    def strikeRelative(self, value: Union[float, str]):
        self.__strikeRelative = value
        self._property_changed('strikeRelative')        

    @property
    def tradeType(self) -> Union['TradeType', str]:
        """Direction"""
        return self.__tradeType

    @tradeType.setter
    def tradeType(self, value: Union['TradeType', str]):
        self.__tradeType = value
        self._property_changed('tradeType')        

    @property
    def signal(self) -> Union[float, str]:
        return self.__signal

    @signal.setter
    def signal(self, value: Union[float, str]):
        self.__signal = value
        self._property_changed('signal')        

    @property
    def newSignal(self) -> Union[float, str]:
        return self.__newSignal

    @newSignal.setter
    def newSignal(self, value: Union[float, str]):
        self.__newSignal = value
        self._property_changed('newSignal')        

    @property
    def newMinWeight(self) -> Union[float, str]:
        return self.__newMinWeight

    @newMinWeight.setter
    def newMinWeight(self, value: Union[float, str]):
        self.__newMinWeight = value
        self._property_changed('newMinWeight')        

    @property
    def newMaxWeight(self) -> Union[float, str]:
        return self.__newMaxWeight

    @newMaxWeight.setter
    def newMaxWeight(self, value: Union[float, str]):
        self.__newMaxWeight = value
        self._property_changed('newMaxWeight')        

    @property
    def minWeight(self) -> Union[float, str]:
        return self.__minWeight

    @minWeight.setter
    def minWeight(self, value: Union[float, str]):
        self.__minWeight = value
        self._property_changed('minWeight')        

    @property
    def maxWeight(self) -> Union[float, str]:
        return self.__maxWeight

    @maxWeight.setter
    def maxWeight(self, value: Union[float, str]):
        self.__maxWeight = value
        self._property_changed('maxWeight')        
