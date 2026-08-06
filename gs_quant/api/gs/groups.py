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

from gs_quant.session import GsSession
from gs_quant.target.groups import Group


class GsGroupsApi:
    @classmethod
    def get_groups(
        cls,
        ids: list[str] = None,
        names: list[str] = None,
        oe_ids: list[str] = None,
        owner_ids: list[str] = None,
        tags: list[str] = None,
        user_ids: list[str] = None,
        scroll_id: str = None,
        scroll_time: str = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = None,
    ) -> list:
        url = f'/groups?limit={limit}&offset={offset}'
        if ids:
            url += f'&id={"&id=".join(ids)}'
        if names:
            url += f'&name={"&name=".join(names)}'
        if oe_ids:
            url += f'&oeId={"&oeId=".join(oe_ids)}'
        if owner_ids:
            url += f'&ownerId={"&ownerId=".join(owner_ids)}'
        if tags:
            url += f'&tags={"&tags=".join(tags)}'
        if user_ids:
            url += f'&userIds={"&userIds=".join(user_ids)}'
        if scroll_id:
            url += f'&scrollId={scroll_id}'
        if scroll_time:
            url += f'&scrollTime={scroll_time}'
        if order_by:
            url += f'&orderBy={order_by}'
        return GsSession.current.sync.get(url, cls=Group)['results']

    @classmethod
    def create_group(cls, group: Group) -> dict:
        return GsSession.current.sync.post('/groups', group, cls=Group)

    @classmethod
    def get_group(cls, group_id: str) -> Group:
        return GsSession.current.sync.get(f'/groups/{group_id}', cls=Group)

    @classmethod
    def update_group(cls, group_id: str, group: Group) -> Group:
        # PUT request for updating a group can't have the group ID in it
        group_dict = group.to_json()
        if group_dict.get('entitlements'):
            group_dict['entitlements'] = group_dict['entitlements'].to_json()
        group_dict.pop('id')
        return GsSession.current.sync.put(f'/groups/{group_id}', group_dict, cls=Group)

    @classmethod
    def delete_group(cls, group_id: str):
        GsSession.current.sync.delete(f'/groups/{group_id}')

    @classmethod
    def get_users_in_group(
        cls,
        group_id: str,
        fields: list[str] = None,
        limit: int = None,
        offset: int = None,
        order_by: list[str] = None,
        show_members_count: bool = None,
        scroll_id: str = None,
        scroll_time: str = None,
    ) -> list:
        url = f'/groups/{group_id}/users?'
        if fields:
            url += f'&fields={"&fields=".join(fields)}'
        if limit is not None:
            url += f'&limit={limit}'
        if offset is not None:
            url += f'&offset={offset}'
        if order_by:
            url += f'&orderBy={"&orderBy=".join(order_by)}'
        if show_members_count is not None:
            url += f'&showMembersCount={str(show_members_count).lower()}'
        if scroll_id:
            url += f'&scrollId={scroll_id}'
        if scroll_time:
            url += f'&scrollTime={scroll_time}'
        return GsSession.current.sync.get(url).get('users', [])

    @classmethod
    def add_users_to_group(cls, group_id: str, user_ids: list[str]):
        GsSession.current.sync.post(f'/groups/{group_id}/users', {'userIds': user_ids})

    @classmethod
    def delete_users_from_group(cls, group_id: str, user_ids: list[str]):
        GsSession.current.sync.delete(f'/groups/{group_id}/users', {'userIds': user_ids}, use_body=True)
