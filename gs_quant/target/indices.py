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
    BRL = 'BRL'
    
    def __repr__(self):
        return self.value


class ApprovalAction(Base):
        
    """Comments for the approval action"""
       
    def __init__(self, comment: str = None, actionType: str = None):
        super().__init__()
        self.__comment = comment
        self.__actionType = actionType

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self.__comment = value
        self._property_changed('comment')        

    @property
    def actionType(self) -> str:
        return self.__actionType

    @actionType.setter
    def actionType(self, value: str):
        self.__actionType = value
        self._property_changed('actionType')        


class CustomBasketsResponse(Base):
        
    """Rebalance custom basket response"""
       
    def __init__(self, status: str = None, approvalId: str = None, reportId: str = None, assetId: str = None):
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
    def approvalId(self) -> str:
        """Marquee unique identifier of approval created"""
        return self.__approvalId

    @approvalId.setter
    def approvalId(self, value: str):
        self.__approvalId = value
        self._property_changed('approvalId')        

    @property
    def reportId(self) -> str:
        """Marquee unique identifier of report created"""
        return self.__reportId

    @reportId.setter
    def reportId(self, value: str):
        self.__reportId = value
        self._property_changed('reportId')        

    @property
    def assetId(self) -> str:
        """Marquee unique identifier of asset created"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
        self.__assetId = value
        self._property_changed('assetId')        


class ISelectConstituentColumn(Base):
               
    def __init__(self, id: str, field: str, name: str, __TYPE: str = None, aggregatorString: str = None, class_: str = None, filter: str = None, formatterString: str = None, ID: int = None, maxWidth: int = None, minWidth: int = None, precision: int = None, sortable: int = None, tooltip: str = None):
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
    def aggregatorString(self) -> str:
        return self.__aggregatorString

    @aggregatorString.setter
    def aggregatorString(self, value: str):
        self.__aggregatorString = value
        self._property_changed('aggregatorString')        

    @property
    def class_(self) -> str:
        return self.__class

    @class_.setter
    def class_(self, value: str):
        self.__class = value
        self._property_changed('class')        

    @property
    def field(self) -> str:
        return self.__field

    @field.setter
    def field(self, value: str):
        self.__field = value
        self._property_changed('field')        

    @property
    def filter(self) -> str:
        return self.__filter

    @filter.setter
    def filter(self, value: str):
        self.__filter = value
        self._property_changed('filter')        

    @property
    def formatterString(self) -> str:
        return self.__formatterString

    @formatterString.setter
    def formatterString(self, value: str):
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
    def tooltip(self) -> str:
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self.__tooltip = value
        self._property_changed('tooltip')        


class ISelectIndexParameters(Base):
               
    def __init__(self, name: str = None, value: float = None):
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
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        self.__value = value
        self._property_changed('value')        


class ISelectSeries(Base):
               
    def __init__(self, __TYPE: str = None, data: tuple = None, identifier: str = None, identifierType: str = None, name: str = None):
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
    def data(self) -> tuple:
        return self.__data

    @data.setter
    def data(self, value: tuple):
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


class PositionPriceInput(Base):
               
    def __init__(self, assetId: str, quantity: float = None, weight: float = None, notional: float = None):
        super().__init__()
        self.__assetId = assetId
        self.__quantity = quantity
        self.__weight = weight
        self.__notional = notional

    @property
    def assetId(self) -> str:
        """Marquee unique identifier"""
        return self.__assetId

    @assetId.setter
    def assetId(self, value: str):
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


class CustomBasketsEditInputs(Base):
        
    """parameters used to edit a basket"""
       
    def __init__(self, name: str = None, description: str = None, styles: Tuple[str, ...] = None, relatedContent: GIRDomain = None, publishParameters: PublishParameters = None):
        super().__init__()
        self.__name = name
        self.__description = description
        self.__styles = styles
        self.__relatedContent = relatedContent
        self.__publishParameters = publishParameters

    @property
    def name(self) -> str:
        """Display name of the basket"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def description(self) -> str:
        """Free text description of asset. Description provided will be indexed in the search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the asset (max 50)"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def relatedContent(self) -> GIRDomain:
        return self.__relatedContent

    @relatedContent.setter
    def relatedContent(self, value: GIRDomain):
        self.__relatedContent = value
        self._property_changed('relatedContent')        

    @property
    def publishParameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish indices, default all to false"""
        return self.__publishParameters

    @publishParameters.setter
    def publishParameters(self, value: PublishParameters):
        self.__publishParameters = value
        self._property_changed('publishParameters')        


class ISelectRebalance(Base):
               
    def __init__(self, newWeights: Tuple[ISelectNewWeight, ...] = None, rebalanceDate: str = None, newParameters: Tuple[ISelectNewParameter, ...] = None, indexParameters: Tuple[ISelectIndexParameters, ...] = None):
        super().__init__()
        self.__newWeights = newWeights
        self.__rebalanceDate = rebalanceDate
        self.__newParameters = newParameters
        self.__indexParameters = indexParameters

    @property
    def newWeights(self) -> Tuple[ISelectNewWeight, ...]:
        """New Weight array to be updated"""
        return self.__newWeights

    @newWeights.setter
    def newWeights(self, value: Tuple[ISelectNewWeight, ...]):
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
    def newParameters(self) -> Tuple[ISelectNewParameter, ...]:
        """New parameters to be updated"""
        return self.__newParameters

    @newParameters.setter
    def newParameters(self, value: Tuple[ISelectNewParameter, ...]):
        self.__newParameters = value
        self._property_changed('newParameters')        

    @property
    def indexParameters(self) -> Tuple[ISelectIndexParameters, ...]:
        """Index parameters to be updated"""
        return self.__indexParameters

    @indexParameters.setter
    def indexParameters(self, value: Tuple[ISelectIndexParameters, ...]):
        self.__indexParameters = value
        self._property_changed('indexParameters')        


class ISelectResponse(Base):
               
    def __init__(self, __TYPE: str = None, Action=None, ActionComment: str = None, assetName: str = None, assetShortName: str = None, availableActionConfirms: Tuple[Tuple[str, ...], ...] = None, availableActions: tuple = None, availableRebalanceDates: Tuple[str, ...] = None, constituentValidations: tuple = None, dateValidationStatus: str = None, dateValidations: tuple = None, entryMode: str = None, entryType: str = None, internalRebalance: int = None, indexParameterDefinitions: tuple = None, indexParameters: tuple = None, indexParameterValidation: tuple = None, newUnits: Tuple[ISelectNewUnit, ...] = None, newWeights: Tuple[ISelectNewWeight, ...] = None, notificationDate: str = None, rebalanceDate: str = None, rebalanceDeterminationDate: str = None, rebDeterminationIndexLevel: float = None, requestCounter: int = None, series: ISelectSeries = None, status=None, submissionData: tuple = None, submissionDataColumns: Tuple[ISelectConstituentColumn, ...] = None, submissionText: str = None, valid: int = None, validationMessages: Tuple[str, ...] = None):
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
    def availableActionConfirms(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__availableActionConfirms

    @availableActionConfirms.setter
    def availableActionConfirms(self, value: Tuple[Tuple[str, ...], ...]):
        self.__availableActionConfirms = value
        self._property_changed('availableActionConfirms')        

    @property
    def availableActions(self) -> tuple:
        return self.__availableActions

    @availableActions.setter
    def availableActions(self, value: tuple):
        self.__availableActions = value
        self._property_changed('availableActions')        

    @property
    def availableRebalanceDates(self) -> Tuple[str, ...]:
        return self.__availableRebalanceDates

    @availableRebalanceDates.setter
    def availableRebalanceDates(self, value: Tuple[str, ...]):
        self.__availableRebalanceDates = value
        self._property_changed('availableRebalanceDates')        

    @property
    def constituentValidations(self) -> tuple:
        return self.__constituentValidations

    @constituentValidations.setter
    def constituentValidations(self, value: tuple):
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
    def dateValidations(self) -> tuple:
        return self.__dateValidations

    @dateValidations.setter
    def dateValidations(self, value: tuple):
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
    def indexParameterDefinitions(self) -> tuple:
        return self.__indexParameterDefinitions

    @indexParameterDefinitions.setter
    def indexParameterDefinitions(self, value: tuple):
        self.__indexParameterDefinitions = value
        self._property_changed('indexParameterDefinitions')        

    @property
    def indexParameters(self) -> tuple:
        return self.__indexParameters

    @indexParameters.setter
    def indexParameters(self, value: tuple):
        self.__indexParameters = value
        self._property_changed('indexParameters')        

    @property
    def indexParameterValidation(self) -> tuple:
        return self.__indexParameterValidation

    @indexParameterValidation.setter
    def indexParameterValidation(self, value: tuple):
        self.__indexParameterValidation = value
        self._property_changed('indexParameterValidation')        

    @property
    def newUnits(self) -> Tuple[ISelectNewUnit, ...]:
        return self.__newUnits

    @newUnits.setter
    def newUnits(self, value: Tuple[ISelectNewUnit, ...]):
        self.__newUnits = value
        self._property_changed('newUnits')        

    @property
    def newWeights(self) -> Tuple[ISelectNewWeight, ...]:
        return self.__newWeights

    @newWeights.setter
    def newWeights(self, value: Tuple[ISelectNewWeight, ...]):
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
    def rebalanceDate(self) -> str:
        return self.__rebalanceDate

    @rebalanceDate.setter
    def rebalanceDate(self, value: str):
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
    def rebDeterminationIndexLevel(self) -> float:
        return self.__rebDeterminationIndexLevel

    @rebDeterminationIndexLevel.setter
    def rebDeterminationIndexLevel(self, value: float):
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
    def series(self) -> ISelectSeries:
        return self.__series

    @series.setter
    def series(self, value: ISelectSeries):
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
    def submissionData(self) -> tuple:
        return self.__submissionData

    @submissionData.setter
    def submissionData(self, value: tuple):
        self.__submissionData = value
        self._property_changed('submissionData')        

    @property
    def submissionDataColumns(self) -> Tuple[ISelectConstituentColumn, ...]:
        return self.__submissionDataColumns

    @submissionDataColumns.setter
    def submissionDataColumns(self, value: Tuple[ISelectConstituentColumn, ...]):
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
    def validationMessages(self) -> Tuple[str, ...]:
        return self.__validationMessages

    @validationMessages.setter
    def validationMessages(self, value: Tuple[str, ...]):
        self.__validationMessages = value
        self._property_changed('validationMessages')        


class IndicesPriceParameters(Base):
        
    """Parameters for pricing indices"""
       
    def __init__(self, currency: Union[IndicesCurrency, str] = None, divisor: float = None, initialPrice: float = None, targetNotional: float = None, weightingStrategy: str = None, reweight: bool = False):
        super().__init__()
        self.__currency = currency if isinstance(currency, IndicesCurrency) else get_enum_value(IndicesCurrency, currency)
        self.__divisor = divisor
        self.__initialPrice = initialPrice
        self.__targetNotional = targetNotional
        self.__weightingStrategy = weightingStrategy
        self.__reweight = reweight

    @property
    def currency(self) -> Union[IndicesCurrency, str]:
        """Currencies supported for Indices Create, default to USD during create. During rebalance, cannot change basket currency hence the input value will be discarded."""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[IndicesCurrency, str]):
        self.__currency = value if isinstance(value, IndicesCurrency) else get_enum_value(IndicesCurrency, value)
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

    @property
    def reweight(self) -> bool:
        """To reweight positions if input weights don't add up to 1, default to false"""
        return self.__reweight

    @reweight.setter
    def reweight(self, value: bool):
        self.__reweight = value
        self._property_changed('reweight')        


class CustomBasketsRebalanceInputs(Base):
        
    """Inputs used to rebalance a custom basket"""
       
    def __init__(self, positionSet: Tuple[PositionPriceInput, ...] = None, publishParameters: PublishParameters = None, pricingParameters: IndicesPriceParameters = None):
        super().__init__()
        self.__positionSet = positionSet
        self.__publishParameters = publishParameters
        self.__pricingParameters = pricingParameters

    @property
    def positionSet(self) -> Tuple[PositionPriceInput, ...]:
        """Information of constituents associated with the rebalance."""
        return self.__positionSet

    @positionSet.setter
    def positionSet(self, value: Tuple[PositionPriceInput, ...]):
        self.__positionSet = value
        self._property_changed('positionSet')        

    @property
    def publishParameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish indices, default all to false"""
        return self.__publishParameters

    @publishParameters.setter
    def publishParameters(self, value: PublishParameters):
        self.__publishParameters = value
        self._property_changed('publishParameters')        

    @property
    def pricingParameters(self) -> IndicesPriceParameters:
        """Parameters for pricing indices"""
        return self.__pricingParameters

    @pricingParameters.setter
    def pricingParameters(self, value: IndicesPriceParameters):
        self.__pricingParameters = value
        self._property_changed('pricingParameters')        


class IndicesCreateInputs(Base):
        
    """Inputs used to create an index"""
       
    def __init__(self, ticker: str, name: str, pricingParameters: IndicesPriceParameters, positionSet: Tuple[PositionPriceInput, ...], description: str = None, styles: Tuple[str, ...] = None, relatedContent: GIRDomain = None, indexCreateSource: Union[IndexCreateSource, str] = None, returnType: str = 'Price Return', publishParameters: PublishParameters = None, onBehalfOf: str = None):
        super().__init__()
        self.__ticker = ticker
        self.__name = name
        self.__description = description
        self.__styles = styles
        self.__relatedContent = relatedContent
        self.__indexCreateSource = indexCreateSource if isinstance(indexCreateSource, IndexCreateSource) else get_enum_value(IndexCreateSource, indexCreateSource)
        self.__returnType = returnType
        self.__positionSet = positionSet
        self.__publishParameters = publishParameters
        self.__pricingParameters = pricingParameters
        self.__onBehalfOf = onBehalfOf

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
    def description(self) -> str:
        """Free text description of asset, default to empty. Description provided will be indexed in the search service for free text relevance match."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        self._property_changed('description')        

    @property
    def styles(self) -> Tuple[str, ...]:
        """Styles or themes associated with the asset (max 50), default to Bespoke"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[str, ...]):
        self.__styles = value
        self._property_changed('styles')        

    @property
    def relatedContent(self) -> GIRDomain:
        """Links to content related to this index or any of its constituents (optional)"""
        return self.__relatedContent

    @relatedContent.setter
    def relatedContent(self, value: GIRDomain):
        self.__relatedContent = value
        self._property_changed('relatedContent')        

    @property
    def indexCreateSource(self) -> Union[IndexCreateSource, str]:
        """Source of basket create"""
        return self.__indexCreateSource

    @indexCreateSource.setter
    def indexCreateSource(self, value: Union[IndexCreateSource, str]):
        self.__indexCreateSource = value if isinstance(value, IndexCreateSource) else get_enum_value(IndexCreateSource, value)
        self._property_changed('indexCreateSource')        

    @property
    def returnType(self) -> str:
        """Determines the index calculation methodology with respect to dividend reinvestment, default to Price Return"""
        return self.__returnType

    @returnType.setter
    def returnType(self, value: str):
        self.__returnType = value
        self._property_changed('returnType')        

    @property
    def positionSet(self) -> Tuple[PositionPriceInput, ...]:
        """Information of constituents associated with the index. Need to supply one of weight, quantity."""
        return self.__positionSet

    @positionSet.setter
    def positionSet(self, value: Tuple[PositionPriceInput, ...]):
        self.__positionSet = value
        self._property_changed('positionSet')        

    @property
    def publishParameters(self) -> PublishParameters:
        """Publishing parameters to determine where and how to publish indices, default all to false"""
        return self.__publishParameters

    @publishParameters.setter
    def publishParameters(self, value: PublishParameters):
        self.__publishParameters = value
        self._property_changed('publishParameters')        

    @property
    def pricingParameters(self) -> IndicesPriceParameters:
        """Parameters for pricing indices"""
        return self.__pricingParameters

    @pricingParameters.setter
    def pricingParameters(self, value: IndicesPriceParameters):
        self.__pricingParameters = value
        self._property_changed('pricingParameters')        

    @property
    def onBehalfOf(self) -> str:
        """Marquee unique identifier"""
        return self.__onBehalfOf

    @onBehalfOf.setter
    def onBehalfOf(self, value: str):
        self.__onBehalfOf = value
        self._property_changed('onBehalfOf')        


class IndicesEditInputs(Base):
               
    def __init__(self, parameters: CustomBasketsEditInputs):
        super().__init__()
        self.__parameters = parameters

    @property
    def parameters(self) -> CustomBasketsEditInputs:
        """The inputs used to edit an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: CustomBasketsEditInputs):
        self.__parameters = value
        self._property_changed('parameters')        


class IndicesRebalanceInputs(Base):
               
    def __init__(self, parameters: dict):
        super().__init__()
        self.__parameters = parameters

    @property
    def parameters(self) -> dict:
        """The inputs used to rebalance an index."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self.__parameters = value
        self._property_changed('parameters')        
