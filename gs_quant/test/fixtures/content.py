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

import datetime as dt
from base64 import b64encode

from gs_quant.target.common import Entitlements
from gs_quant.target.content import GetManyContentsResponse, ContentResponse, Content


class ContentFixtures:
    _data = {
        'id': 'some-id',
        'version': 'some-version',
        'name': 'some-name',
        'entitlements': {
            'view': [
                'some-view-entitlement'
            ],
            'edit': [
                'some-edit-entitlement'
            ],
            'delete': [
                'some-delete-token'
            ],
            'admin': [
                'some-admin-token'
            ]
        },
        'createdById': 'some-created-by-id',
        'createdTime': dt.date(2019, 5, 13),
        'authors': [
            {
                'name': 'some-author-name',
                'firstName': 'some-author-first-name',
                'lastName': 'some-author-last-name',
                'id': 'some-author-id',
                'division': 'some-author-division'
            }
        ],
        'lastUpdatedTime': dt.date(2019, 5, 14),
        'content': {
            'body': b64encode(b'Hello world!'),
            'mimeType': 'text/plain',
            'encoding': 'UTF-8'
        },
        'channels': [
            'some-channel'
        ]
    }

    @classmethod
    def _get_content_response(cls):
        return ContentResponse(
            id=cls._data['id'],
            version=cls._data['version'],
            name=cls._data['name'],
            entitlements=Entitlements(
                cls._data['entitlements']['view'],
                cls._data['entitlements']['edit'],
                cls._data['entitlements']['admin'],
                cls._data['entitlements']['delete']
            ),
            created_by_id=cls._data['createdById'],
            created_time=cls._data['createdTime'],
            last_updated_time=cls._data['lastUpdatedTime'],
            channels=cls._data['channels'],
            content=Content(
                cls._data['content']['body'],
                cls._data['content']['mimeType'],
                cls._data['content']['encoding']
            )
        )

    @classmethod
    def get_many_contents_response(cls, status: int = 200, message: str = "Ok"):
        content = cls._get_content_response()
        return GetManyContentsResponse(status, message, (content,))
