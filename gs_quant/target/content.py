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

from gs_quant.base import Base, get_enum_value
from gs_quant.target.common import *
from typing import Tuple, Union
import datetime


class Author(Base):
        
    """Object containing author data"""
       
    def __init__(
        self,
        id: str = None,
        name: str = None,
        division=None        
    ):
        super().__init__()
        self.__id = id
        self.__name = name
        self.__division = division

    @property
    def id(self) -> str:
        """Author GUID"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def name(self) -> str:
        """Author name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def division(self):
        return self.__division

    @division.setter
    def division(self, value):
        self.__division = value
        self._property_changed('division')        


class BulkDeleteContentResponse(Base):
               
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: Tuple[str, ...] = None        
    ):
        super().__init__()
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self.__status = value
        self._property_changed('status')        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
        self._property_changed('message')        

    @property
    def data(self) -> Tuple[str, ...]:
        """Array of content IDs which were successfully deleted"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[str, ...]):
        self.__data = value
        self._property_changed('data')        


class Content(Base):
        
    """Body of the content piece"""
       
    def __init__(
        self,
        body: str,
        mime_type,
        encoding        
    ):
        super().__init__()
        self.__body = body
        self.__mime_type = mime_type
        self.__encoding = encoding

    @property
    def body(self) -> str:
        """Content body - text/* or base64-encoded binary"""
        return self.__body

    @body.setter
    def body(self, value: str):
        self.__body = value
        self._property_changed('body')        

    @property
    def mime_type(self):
        """Allowed mime-types"""
        return self.__mime_type

    @mime_type.setter
    def mime_type(self, value):
        self.__mime_type = value
        self._property_changed('mime_type')        

    @property
    def encoding(self):
        """Encoding for content piece body"""
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        self.__encoding = value
        self._property_changed('encoding')        


class DeleteContentResponse(Base):
               
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: str = None        
    ):
        super().__init__()
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self.__status = value
        self._property_changed('status')        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
        self._property_changed('message')        

    @property
    def data(self) -> str:
        """Content ID which was successfully deleted"""
        return self.__data

    @data.setter
    def data(self, value: str):
        self.__data = value
        self._property_changed('data')        


class Disclaimer(Base):
        
    """Disclaimer associated with a content piece"""
       
    def __init__(
        self,
        text: str = None,
        type=None        
    ):
        super().__init__()
        self.__text = text
        self.__type = type

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str):
        self.__text = value
        self._property_changed('text')        

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
        self._property_changed('type')        


class Object(Base):
               
    def __init__(
        self,
                
    ):
        super().__init__()
        


class Certification(Base):
        
    """Field to store SEAL certification object"""
       
    def __init__(
        self,
        submission_id: str,
        version: str,
        submission_state,
        allowed_distribution: Tuple[Object, ...],
        etask_process_instance_id: str = None,
        tags: Tuple[None, ...] = None        
    ):
        super().__init__()
        self.__submission_id = submission_id
        self.__version = version
        self.__submission_state = submission_state
        self.__etask_process_instance_id = etask_process_instance_id
        self.__allowed_distribution = allowed_distribution
        self.__tags = tags

    @property
    def submission_id(self) -> str:
        """Submission ID assigned by SEAL"""
        return self.__submission_id

    @submission_id.setter
    def submission_id(self, value: str):
        self.__submission_id = value
        self._property_changed('submission_id')        

    @property
    def version(self) -> str:
        """Submission version assigned by SEAL"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self.__version = value
        self._property_changed('version')        

    @property
    def submission_state(self):
        """Current state of a submission as reported by SEAL"""
        return self.__submission_state

    @submission_state.setter
    def submission_state(self, value):
        self.__submission_state = value
        self._property_changed('submission_state')        

    @property
    def etask_process_instance_id(self) -> str:
        """Field to store eTask ID associated with SEAL certification of content piece"""
        return self.__etask_process_instance_id

    @etask_process_instance_id.setter
    def etask_process_instance_id(self, value: str):
        self.__etask_process_instance_id = value
        self._property_changed('etask_process_instance_id')        

    @property
    def allowed_distribution(self) -> Tuple[Object, ...]:
        """A list of allowed distributions"""
        return self.__allowed_distribution

    @allowed_distribution.setter
    def allowed_distribution(self, value: Tuple[Object, ...]):
        self.__allowed_distribution = value
        self._property_changed('allowed_distribution')        

    @property
    def tags(self) -> Tuple[None, ...]:
        """SEAL generated, enumerated tags"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[None, ...]):
        self.__tags = value
        self._property_changed('tags')        


class ContentResponse(Base):
               
    def __init__(
        self,
        id: str = None,
        version: str = None,
        name: str = None,
        entitlements: Entitlements = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        channels: Tuple[str, ...] = None,
        content: Content = None        
    ):
        super().__init__()
        self.__id = id
        self.__version = version
        self.__name = name
        self.__entitlements = entitlements
        self.__created_by_id = created_by_id
        self.__created_time = created_time
        self.__last_updated_time = last_updated_time
        self.__channels = channels
        self.__content = content

    @property
    def id(self) -> str:
        """UUID for the content piece"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def version(self) -> str:
        """Version UUID for the content piece"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self.__version = value
        self._property_changed('version')        

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def created_by_id(self) -> str:
        """Original user GUID who created the content piece"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self.__created_by_id = value
        self._property_changed('created_by_id')        

    @property
    def created_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self.__created_time = value
        self._property_changed('created_time')        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        

    @property
    def channels(self) -> Tuple[str, ...]:
        """List of channels on the content piece"""
        return self.__channels

    @channels.setter
    def channels(self, value: Tuple[str, ...]):
        self.__channels = value
        self._property_changed('channels')        

    @property
    def content(self) -> Content:
        """Body of the content piece"""
        return self.__content

    @content.setter
    def content(self, value: Content):
        self.__content = value
        self._property_changed('content')        


class ContentUpdateRequest(Base):
               
    def __init__(
        self,
        name: str = None,
        entitlements: Entitlements = None,
        content: Content = None        
    ):
        super().__init__()
        self.__name = name
        self.__entitlements = entitlements
        self.__content = content

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def content(self) -> Content:
        """Body of the content piece"""
        return self.__content

    @content.setter
    def content(self, value: Content):
        self.__content = value
        self._property_changed('content')        


class BulkContentUpdateRequestItem(Base):
               
    def __init__(
        self,
        id: str = None,
        update: ContentUpdateRequest = None        
    ):
        super().__init__()
        self.__id = id
        self.__update = update

    @property
    def id(self) -> str:
        """UUID for the content piece"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def update(self) -> ContentUpdateRequest:
        return self.__update

    @update.setter
    def update(self, value: ContentUpdateRequest):
        self.__update = value
        self._property_changed('update')        


class ContentAuditFields(Base):
               
    def __init__(
        self,
        id: str = None,
        version: str = None,
        name: str = None,
        entitlements: Entitlements = None,
        created_by_id: str = None,
        authors: Tuple[Author, ...] = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None        
    ):
        super().__init__()
        self.__id = id
        self.__version = version
        self.__name = name
        self.__entitlements = entitlements
        self.__created_by_id = created_by_id
        self.__authors = authors
        self.__created_time = created_time
        self.__last_updated_time = last_updated_time

    @property
    def id(self) -> str:
        """UUID for the content piece"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        self._property_changed('id')        

    @property
    def version(self) -> str:
        """Version UUID for the content piece"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self.__version = value
        self._property_changed('version')        

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def created_by_id(self) -> str:
        """Original user GUID who created the content piece"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self.__created_by_id = value
        self._property_changed('created_by_id')        

    @property
    def authors(self) -> Tuple[Author, ...]:
        """List of author objects"""
        return self.__authors

    @authors.setter
    def authors(self, value: Tuple[Author, ...]):
        self.__authors = value
        self._property_changed('authors')        

    @property
    def created_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self.__created_time = value
        self._property_changed('created_time')        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self.__last_updated_time = value
        self._property_changed('last_updated_time')        


class ContentParameters(Base):
        
    """Parameters of the content piece"""
       
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
        asset_ids: Tuple[str, ...] = None,
        origin=None,
        disclaimers: Tuple[Disclaimer, ...] = None        
    ):
        super().__init__()
        self.__status = status
        self.__namespace = namespace
        self.__tags = tags
        self.__slug = slug
        self.__author_ids = author_ids
        self.__attachments = attachments
        self.__certification = certification
        self.__asset_ids = asset_ids
        self.__origin = origin
        self.__disclaimers = disclaimers
        self.__language = language

    @property
    def status(self):
        """Status/state of the content piece"""
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        self._property_changed('status')        

    @property
    def namespace(self) -> str:
        """Namespace for which the content piece is associated"""
        return self.__namespace

    @namespace.setter
    def namespace(self, value: str):
        self.__namespace = value
        self._property_changed('namespace')        

    @property
    def tags(self) -> Tuple[str, ...]:
        """List of tags (hashtags or raw string tags) on the content piece"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self.__tags = value
        self._property_changed('tags')        

    @property
    def slug(self) -> str:
        """Optional slug that could be used to refer to this document"""
        return self.__slug

    @slug.setter
    def slug(self, value: str):
        self.__slug = value
        self._property_changed('slug')        

    @property
    def author_ids(self) -> Tuple[str, ...]:
        """List of author GUIDs for the content piece"""
        return self.__author_ids

    @author_ids.setter
    def author_ids(self, value: Tuple[str, ...]):
        self.__author_ids = value
        self._property_changed('author_ids')        

    @property
    def attachments(self) -> Tuple[Content, ...]:
        """List of attachments on the parent content piece """
        return self.__attachments

    @attachments.setter
    def attachments(self, value: Tuple[Content, ...]):
        self.__attachments = value
        self._property_changed('attachments')        

    @property
    def certification(self) -> Certification:
        """Field to store SEAL certification object"""
        return self.__certification

    @certification.setter
    def certification(self, value: Certification):
        self.__certification = value
        self._property_changed('certification')        

    @property
    def asset_ids(self) -> Tuple[str, ...]:
        """Array of Marquee Asset Ids associated with the content piece"""
        return self.__asset_ids

    @asset_ids.setter
    def asset_ids(self, value: Tuple[str, ...]):
        self.__asset_ids = value
        self._property_changed('asset_ids')        

    @property
    def origin(self):
        """Where the content originated from"""
        return self.__origin

    @origin.setter
    def origin(self, value):
        self.__origin = value
        self._property_changed('origin')        

    @property
    def disclaimers(self) -> Tuple[Disclaimer, ...]:
        """List of disclaimers associated with a content piece"""
        return self.__disclaimers

    @disclaimers.setter
    def disclaimers(self, value: Tuple[Disclaimer, ...]):
        self.__disclaimers = value
        self._property_changed('disclaimers')        

    @property
    def language(self):
        """ISO 639-1 language code for the content piece"""
        return self.__language

    @language.setter
    def language(self, value):
        self.__language = value
        self._property_changed('language')        


class GetManyContentsResponse(Base):
               
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: Tuple[ContentResponse, ...] = None        
    ):
        super().__init__()
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self.__status = value
        self._property_changed('status')        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
        self._property_changed('message')        

    @property
    def data(self) -> Tuple[ContentResponse, ...]:
        """Array of content pieces"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[ContentResponse, ...]):
        self.__data = value
        self._property_changed('data')        


class BulkContentUpdateResponse(Base):
               
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: Tuple[ContentAuditFields, ...] = None        
    ):
        super().__init__()
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self.__status = value
        self._property_changed('status')        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
        self._property_changed('message')        

    @property
    def data(self) -> Tuple[ContentAuditFields, ...]:
        """Array of updated content data"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[ContentAuditFields, ...]):
        self.__data = value
        self._property_changed('data')        


class ContentCreateRequest(Base):
               
    def __init__(
        self,
        name: str,
        entitlements: Entitlements,
        content: Content,
        parameters: ContentParameters        
    ):
        super().__init__()
        self.__name = name
        self.__entitlements = entitlements
        self.__content = content
        self.__parameters = parameters

    @property
    def name(self) -> str:
        """Name of the content piece"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self._property_changed('name')        

    @property
    def entitlements(self) -> Entitlements:
        """Entitlements for a content piece"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self.__entitlements = value
        self._property_changed('entitlements')        

    @property
    def content(self) -> Content:
        """Body of the content piece"""
        return self.__content

    @content.setter
    def content(self, value: Content):
        self.__content = value
        self._property_changed('content')        

    @property
    def parameters(self) -> ContentParameters:
        """Parameters of the content piece"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: ContentParameters):
        self.__parameters = value
        self._property_changed('parameters')        


class ContentCreateResponse(Base):
               
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: ContentAuditFields = None        
    ):
        super().__init__()
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self.__status = value
        self._property_changed('status')        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
        self._property_changed('message')        

    @property
    def data(self) -> ContentAuditFields:
        return self.__data

    @data.setter
    def data(self, value: ContentAuditFields):
        self.__data = value
        self._property_changed('data')        


class ContentUpdateResponse(Base):
               
    def __init__(
        self,
        status: int = None,
        message: str = None,
        data: ContentAuditFields = None        
    ):
        super().__init__()
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> int:
        """HTTP Status Code"""
        return self.__status

    @status.setter
    def status(self, value: int):
        self.__status = value
        self._property_changed('status')        

    @property
    def message(self) -> str:
        """Field to store any informational message / error returned by the server"""
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
        self._property_changed('message')        

    @property
    def data(self) -> ContentAuditFields:
        return self.__data

    @data.setter
    def data(self, value: ContentAuditFields):
        self.__data = value
        self._property_changed('data')        
