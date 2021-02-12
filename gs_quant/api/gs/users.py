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

from typing import List

from pydash import get

from gs_quant.session import GsSession


class GsUsersApi:
    @classmethod
    def get_my_user_id(cls) -> str:
        return GsSession.current._get('/users/self')['id']

    @classmethod
    def get_my_guid(cls) -> str:
        return f"guid:{GsSession.current._get('/users/self')['id']}"

    @classmethod
    def get_user_ids_by_email(cls, emails: List[str]) -> List[str]:
        """
        Gets the user ids for users with the provided emails.
        :param emails: list of emails
        :return: list of user ids
        """
        if not len(emails):
            return []
        email_query = '&email='.join(emails)
        raw_users = GsSession.current._get(f'/users?limit=100&email={email_query}')

        return [user['id'] for user in get(raw_users, 'results', [])]

    @classmethod
    def get_guids_from_ids(cls, user_ids: List[str]) -> List[str]:
        """
        Creates a list of guid strings used throughout Marquee APIs.
        :param user_ids: list of user ids
        :return: list of guids (user ids appended with "guid:")
        """
        return [f'guid:{user_id}' for user_id in user_ids]
