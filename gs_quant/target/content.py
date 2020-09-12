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


class InvestmentRecommendationDirection(EnumBase, Enum):    
    
    Buy = 'Buy'
    Hold = 'Hold'
    Sell = 'Sell'
    Strategy = 'Strategy'
    
    def __repr__(self):
        return self.value


class Author(Base):
        
    """Object containing author data"""

    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        name: str = None,
        division=None,
        email: str = None,
        title: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.division = division
        self.email = email
        self.title = title

    @property
    def id(self) -> str:
        """Author GUID"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Author name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def division(self):
        return self.__division

    @division.setter
    def division(self, value):
        self._property_changed('division')
        self.__division = value        

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        


class BulkDeleteContentResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.message = message
        self.data = data
        self.name = name

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self._property_changed('status')
        self.__status = value        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        

    @property
    def data(self) -> Tuple[str, ...]:
        """Array of content IDs which were successfully deleted"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[str, ...]):
        self._property_changed('data')
        self.__data = value        


class Content(Base):
        
    """Body of the content piece"""

    @camel_case_translate
    def __init__(
        self,
        body: str,
        mime_type,
        encoding,
        name: str = None
    ):        
        super().__init__()
        self.body = body
        self.mime_type = mime_type
        self.encoding = encoding
        self.name = name

    @property
    def body(self) -> str:
        """Content body - text/* or base64-encoded binary"""
        return self.__body

    @body.setter
    def body(self, value: str):
        self._property_changed('body')
        self.__body = value        

    @property
    def mime_type(self):
        """Allowed mime-types"""
        return self.__mime_type

    @mime_type.setter
    def mime_type(self, value):
        self._property_changed('mime_type')
        self.__mime_type = value        

    @property
    def encoding(self):
        """Encoding for content piece body"""
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        self._property_changed('encoding')
        self.__encoding = value        


class DeleteContentResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: str = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.message = message
        self.data = data
        self.name = name

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self._property_changed('status')
        self.__status = value        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        

    @property
    def data(self) -> str:
        """Content ID which was successfully deleted"""
        return self.__data

    @data.setter
    def data(self, value: str):
        self._property_changed('data')
        self.__data = value        


class Object(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class Certification(Base):
        
    """Field to store SEAL certification object"""

    @camel_case_translate
    def __init__(
        self,
        submission_id: str,
        version: str,
        submission_state,
        allowed_distribution: Tuple[Object, ...],
        etask_process_instance_id: str = None,
        tags: Tuple[None, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.submission_id = submission_id
        self.version = version
        self.submission_state = submission_state
        self.etask_process_instance_id = etask_process_instance_id
        self.allowed_distribution = allowed_distribution
        self.tags = tags
        self.name = name

    @property
    def submission_id(self) -> str:
        """Submission ID assigned by SEAL"""
        return self.__submission_id

    @submission_id.setter
    def submission_id(self, value: str):
        self._property_changed('submission_id')
        self.__submission_id = value        

    @property
    def version(self) -> str:
        """Submission version assigned by SEAL"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self._property_changed('version')
        self.__version = value        

    @property
    def submission_state(self):
        """Current state of a submission as reported by SEAL"""
        return self.__submission_state

    @submission_state.setter
    def submission_state(self, value):
        self._property_changed('submission_state')
        self.__submission_state = value        

    @property
    def etask_process_instance_id(self) -> str:
        """Field to store eTask ID associated with SEAL certification of content piece"""
        return self.__etask_process_instance_id

    @etask_process_instance_id.setter
    def etask_process_instance_id(self, value: str):
        self._property_changed('etask_process_instance_id')
        self.__etask_process_instance_id = value        

    @property
    def allowed_distribution(self) -> Tuple[Object, ...]:
        """A list of allowed distributions"""
        return self.__allowed_distribution

    @allowed_distribution.setter
    def allowed_distribution(self, value: Tuple[Object, ...]):
        self._property_changed('allowed_distribution')
        self.__allowed_distribution = value        

    @property
    def tags(self) -> Tuple[None, ...]:
        """SEAL generated, enumerated tags"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[None, ...]):
        self._property_changed('tags')
        self.__tags = value        


class ContentResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        version: str = None,
        name: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        channels: Tuple[str, ...] = None,
        content: Content = None
    ):        
        super().__init__()
        self.__id = id_
        self.version = version
        self.name = name
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.channels = channels
        self.content = content

    @property
    def id(self) -> str:
        """UUID for the content piece"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def version(self) -> str:
        """Version UUID for the content piece"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self._property_changed('version')
        self.__version = value        

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Entitlement exclusions for a content piece"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def created_by_id(self) -> str:
        """Original user GUID who created the content piece"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def channels(self) -> Tuple[str, ...]:
        """List of channels on the content piece"""
        return self.__channels

    @channels.setter
    def channels(self, value: Tuple[str, ...]):
        self._property_changed('channels')
        self.__channels = value        

    @property
    def content(self) -> Content:
        """Body of the content piece"""
        return self.__content

    @content.setter
    def content(self, value: Content):
        self._property_changed('content')
        self.__content = value        


class ContentUpdateRequest(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        content: Content = None
    ):        
        super().__init__()
        self.name = name
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.content = content

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Entitlement exclusions for a content piece"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def content(self) -> Content:
        """Body of the content piece"""
        return self.__content

    @content.setter
    def content(self, value: Content):
        self._property_changed('content')
        self.__content = value        


class InvestmentRecommendationAsset(Base):
        
    """An asset that exists in the system."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        direction: Union[InvestmentRecommendationDirection, str] = None,
        currency: str = None,
        price: float = None,
        price_target: float = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.direction = direction
        self.currency = currency
        self.price = price
        self.price_target = price_target
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee Asset identifier"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def direction(self) -> Union[InvestmentRecommendationDirection, str]:
        return self.__direction

    @direction.setter
    def direction(self, value: Union[InvestmentRecommendationDirection, str]):
        self._property_changed('direction')
        self.__direction = get_enum_value(InvestmentRecommendationDirection, value)        

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        self._property_changed('price')
        self.__price = value        

    @property
    def price_target(self) -> float:
        return self.__price_target

    @price_target.setter
    def price_target(self, value: float):
        self._property_changed('price_target')
        self.__price_target = value        


class InvestmentRecommendationCustomAsset(Base):
        
    """An asset that does not exist in the system."""

    @camel_case_translate
    def __init__(
        self,
        asset_name: str,
        direction: Union[InvestmentRecommendationDirection, str] = None,
        currency: str = None,
        price: float = None,
        price_target: float = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_name = asset_name
        self.direction = direction
        self.currency = currency
        self.price = price
        self.price_target = price_target
        self.name = name

    @property
    def asset_name(self) -> str:
        return self.__asset_name

    @asset_name.setter
    def asset_name(self, value: str):
        self._property_changed('asset_name')
        self.__asset_name = value        

    @property
    def direction(self) -> Union[InvestmentRecommendationDirection, str]:
        return self.__direction

    @direction.setter
    def direction(self, value: Union[InvestmentRecommendationDirection, str]):
        self._property_changed('direction')
        self.__direction = get_enum_value(InvestmentRecommendationDirection, value)        

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        self._property_changed('price')
        self.__price = value        

    @property
    def price_target(self) -> float:
        return self.__price_target

    @price_target.setter
    def price_target(self, value: float):
        self._property_changed('price_target')
        self.__price_target = value        


class BulkContentUpdateRequestItem(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        update: ContentUpdateRequest = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.update = update
        self.name = name

    @property
    def id(self) -> str:
        """UUID for the content piece"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def update(self) -> ContentUpdateRequest:
        return self.__update

    @update.setter
    def update(self, value: ContentUpdateRequest):
        self._property_changed('update')
        self.__update = value        


class ContentAuditFields(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        version: str = None,
        name: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        created_by_id: str = None,
        authors: Tuple[Author, ...] = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None
    ):        
        super().__init__()
        self.__id = id_
        self.version = version
        self.name = name
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.created_by_id = created_by_id
        self.authors = authors
        self.created_time = created_time
        self.last_updated_time = last_updated_time

    @property
    def id(self) -> str:
        """UUID for the content piece"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def version(self) -> str:
        """Version UUID for the content piece"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self._property_changed('version')
        self.__version = value        

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Entitlement exclusions for a content piece"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def created_by_id(self) -> str:
        """Original user GUID who created the content piece"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def authors(self) -> Tuple[Author, ...]:
        """List of author objects"""
        return self.__authors

    @authors.setter
    def authors(self, value: Tuple[Author, ...]):
        self._property_changed('authors')
        self.__authors = value        

    @property
    def created_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        


class GetManyContentsResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: Tuple[ContentResponse, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.message = message
        self.data = data
        self.name = name

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self._property_changed('status')
        self.__status = value        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        

    @property
    def data(self) -> Tuple[ContentResponse, ...]:
        """Array of content pieces"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[ContentResponse, ...]):
        self._property_changed('data')
        self.__data = value        


class InvestmentRecommendations(Base):
        
    """Investment recommendations for an article."""

    @camel_case_translate
    def __init__(
        self,
        assets: Tuple[InvestmentRecommendationAsset, ...],
        custom_assets: Tuple[InvestmentRecommendationCustomAsset, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.assets = assets
        self.custom_assets = custom_assets
        self.name = name

    @property
    def assets(self) -> Tuple[InvestmentRecommendationAsset, ...]:
        """A list of assets."""
        return self.__assets

    @assets.setter
    def assets(self, value: Tuple[InvestmentRecommendationAsset, ...]):
        self._property_changed('assets')
        self.__assets = value        

    @property
    def custom_assets(self) -> Tuple[InvestmentRecommendationCustomAsset, ...]:
        """A list of assets that do not exist in the system."""
        return self.__custom_assets

    @custom_assets.setter
    def custom_assets(self, value: Tuple[InvestmentRecommendationCustomAsset, ...]):
        self._property_changed('custom_assets')
        self.__custom_assets = value        


class BulkContentUpdateResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: Tuple[ContentAuditFields, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.message = message
        self.data = data
        self.name = name

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self._property_changed('status')
        self.__status = value        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        

    @property
    def data(self) -> Tuple[ContentAuditFields, ...]:
        """Array of updated content data"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[ContentAuditFields, ...]):
        self._property_changed('data')
        self.__data = value        


class ContentCreateResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: ContentAuditFields = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.message = message
        self.data = data
        self.name = name

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self._property_changed('status')
        self.__status = value        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        

    @property
    def data(self) -> ContentAuditFields:
        return self.__data

    @data.setter
    def data(self, value: ContentAuditFields):
        self._property_changed('data')
        self.__data = value        


class ContentParameters(Base):
        
    """Parameters of the content piece"""

    @camel_case_translate
    def __init__(
        self,
        namespace: str,
        author_ids: Tuple[str, ...],
        language,
        status=None,
        tags: Tuple[str, ...] = None,
        slug: str = None,
        attachments: Tuple[Content, ...] = None,
        certification: Certification = None,
        certification_type=None,
        asset_ids: Tuple[str, ...] = None,
        origin=None,
        investment_recommendations: InvestmentRecommendations = None,
        is_flow: bool = None,
        is_research_summary: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.namespace = namespace
        self.tags = tags
        self.slug = slug
        self.author_ids = author_ids
        self.attachments = attachments
        self.certification = certification
        self.certification_type = certification_type
        self.asset_ids = asset_ids
        self.origin = origin
        self.language = language
        self.investment_recommendations = investment_recommendations
        self.is_flow = is_flow
        self.is_research_summary = is_research_summary
        self.name = name

    @property
    def status(self):
        """Status/state of the content piece"""
        return self.__status

    @status.setter
    def status(self, value):
        self._property_changed('status')
        self.__status = value        

    @property
    def namespace(self) -> str:
        """Namespace for which the content piece is associated"""
        return self.__namespace

    @namespace.setter
    def namespace(self, value: str):
        self._property_changed('namespace')
        self.__namespace = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """List of tags on the content piece"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def slug(self) -> str:
        """Optional slug that could be used to refer to this document"""
        return self.__slug

    @slug.setter
    def slug(self, value: str):
        self._property_changed('slug')
        self.__slug = value        

    @property
    def author_ids(self) -> Tuple[str, ...]:
        """List of author GUIDs for the content piece"""
        return self.__author_ids

    @author_ids.setter
    def author_ids(self, value: Tuple[str, ...]):
        self._property_changed('author_ids')
        self.__author_ids = value        

    @property
    def attachments(self) -> Tuple[Content, ...]:
        """List of attachments on the parent content piece"""
        return self.__attachments

    @attachments.setter
    def attachments(self, value: Tuple[Content, ...]):
        self._property_changed('attachments')
        self.__attachments = value        

    @property
    def certification(self) -> Certification:
        """Field to store SEAL certification object"""
        return self.__certification

    @certification.setter
    def certification(self, value: Certification):
        self._property_changed('certification')
        self.__certification = value        

    @property
    def certification_type(self):
        """Field to store certification type enum"""
        return self.__certification_type

    @certification_type.setter
    def certification_type(self, value):
        self._property_changed('certification_type')
        self.__certification_type = value        

    @property
    def asset_ids(self) -> Tuple[str, ...]:
        """Array of Marquee Asset Ids associated with the content piece"""
        return self.__asset_ids

    @asset_ids.setter
    def asset_ids(self, value: Tuple[str, ...]):
        self._property_changed('asset_ids')
        self.__asset_ids = value        

    @property
    def origin(self):
        """Where the content originated from"""
        return self.__origin

    @origin.setter
    def origin(self, value):
        self._property_changed('origin')
        self.__origin = value        

    @property
    def language(self):
        """ISO 639-1 language code for the content piece"""
        return self.__language

    @language.setter
    def language(self, value):
        self._property_changed('language')
        self.__language = value        

    @property
    def investment_recommendations(self) -> InvestmentRecommendations:
        """Investment recommendations for an article."""
        return self.__investment_recommendations

    @investment_recommendations.setter
    def investment_recommendations(self, value: InvestmentRecommendations):
        self._property_changed('investment_recommendations')
        self.__investment_recommendations = value        

    @property
    def is_flow(self) -> bool:
        return self.__is_flow

    @is_flow.setter
    def is_flow(self, value: bool):
        self._property_changed('is_flow')
        self.__is_flow = value        

    @property
    def is_research_summary(self) -> bool:
        return self.__is_research_summary

    @is_research_summary.setter
    def is_research_summary(self, value: bool):
        self._property_changed('is_research_summary')
        self.__is_research_summary = value        


class ContentUpdateResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: ContentAuditFields = None,
        name: str = None
    ):        
        super().__init__()
        self.status = status
        self.message = message
        self.data = data
        self.name = name

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self._property_changed('status')
        self.__status = value        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self._property_changed('message')
        self.__message = value        

    @property
    def data(self) -> ContentAuditFields:
        return self.__data

    @data.setter
    def data(self, value: ContentAuditFields):
        self._property_changed('data')
        self.__data = value        


class ContentCreateRequest(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str,
        entitlements: Entitlements,
        entitlement_exclusions: EntitlementExclusions,
        content: Content,
        parameters: ContentParameters
    ):        
        super().__init__()
        self.name = name
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.content = content
        self.parameters = parameters

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Entitlement exclusions for a content piece"""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def content(self) -> Content:
        """Body of the content piece"""
        return self.__content

    @content.setter
    def content(self, value: Content):
        self._property_changed('content')
        self.__content = value        

    @property
    def parameters(self) -> ContentParameters:
        """Parameters of the content piece"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ContentParameters):
        self._property_changed('parameters')
        self.__parameters = value        
