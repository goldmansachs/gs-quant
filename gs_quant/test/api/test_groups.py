"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from gs_quant.api.gs.groups import GsGroupsApi
from gs_quant.session import *
from gs_quant.target.groups import Group as TargetGroup


def test_get_groups(mocker):
    mock_response = {
        "totalResults": 1,
        "results": [
            {
                "name": "GSOE Real Time Sync - gsoe.c3e2418dcfd0c6590134deb4caa9b7d65a92a4a761cf20436298560a9ed410a0",
                "id": "gsoe.c3e2418dcfd0c6590134deb4caa9b7d65a92a4a761cf20436298560a9ed410a0",
                "createdById": "3563ed98a93f44c0a016fed2e5c8ce9d",
                "lastUpdatedById": "3563ed98a93f44c0a016fed2e5c8ce9d",
                "ownerId": "3563ed98a93f44c0a016fed2e5c8ce9d",
                "createdTime": "2020-05-22T10:57:40.449-04:00",
                "lastUpdatedTime": "2020-05-22T10:57:40.449-04:00"
            }
        ]
    }

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsGroupsApi.get_groups(ids=['id1', 'id2'],
                                      names=['name1'],
                                      tags=['tag1'],
                                      limit=1)
    GsSession.current._get.assert_called_with('/groups?limit=1&offset=0&id=id1&id=id2&name=name1&tags=tag1',
                                              cls=TargetGroup)
    assert len(response) == 1


def test_get_group(mocker):
    mock_response = TargetGroup.from_dict({
        "name": "Fake Group",
        "id": "id123",
        "createdById": "3563ed98a93f44c0a016fed2e5c8ce9d",
        "lastUpdatedById": "3563ed98a93f44c0a016fed2e5c8ce9d",
        "ownerId": "3563ed98a93f44c0a016fed2e5c8ce9d",
        "createdTime": "2020-05-22T10:57:40.449-04:00",
        "lastUpdatedTime": "2020-05-22T10:57:40.449-04:00"
    })

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsGroupsApi.get_group(group_id='id123')
    GsSession.current._get.assert_called_with('/groups/id123', cls=TargetGroup)
    assert response.name == 'Fake Group'


def test_create_group(mocker):
    target_group = TargetGroup.from_dict({
        "name": "Fake Group",
        "id": "id123",
        "createdById": "3563ed98a93f44c0a016fed2e5c8ce9d",
        "lastUpdatedById": "3563ed98a93f44c0a016fed2e5c8ce9d",
        "ownerId": "3563ed98a93f44c0a016fed2e5c8ce9d",
        "createdTime": "2020-05-22T10:57:40.449-04:00",
        "lastUpdatedTime": "2020-05-22T10:57:40.449-04:00"
    })

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=target_group)

    # run test
    response = GsGroupsApi.create_group(target_group)
    GsSession.current._post.assert_called_with('/groups', target_group, cls=TargetGroup)
    assert response.name == 'Fake Group'
