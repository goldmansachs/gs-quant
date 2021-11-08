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
from testfixtures import Replacer
from testfixtures.mock import Mock

from gs_quant.entities.entitlements import Group
from gs_quant.target.groups import Group as TargetGroup


def test_get():
    group = TargetGroup.from_dict({
        'name': 'fakeGroup',
        'id': 'groupId',
        'tags': []
    })
    replace = Replacer()
    mock = replace('gs_quant.api.gs.groups.GsGroupsApi.get_group', Mock())
    mock.return_value = group
    assert Group.get('groupId').name == 'fakeGroup'
    replace.restore()


def test_get_many():
    groups = [
        TargetGroup.from_dict({
            'name': 'fakeGroup',
            'id': 'groupId',
            'tags': []
        }),
        TargetGroup.from_dict({
            'name': 'fakeGroup2',
            'id': 'groupId2',
            'tags': []
        })
    ]
    replace = Replacer()
    mock = replace('gs_quant.api.gs.groups.GsGroupsApi.get_groups', Mock())
    mock.return_value = groups
    assert len(Group.get_many(group_ids=['groupId', 'groupId2'])) == 2
    replace.restore()


def test_save_update():
    group = TargetGroup.from_dict({
        'name': 'fakeGroup',
        'id': 'groupId',
        'tags': []
    })
    replace = Replacer()
    mock = replace('gs_quant.api.gs.groups.GsGroupsApi.update_group', Mock())
    mock.return_value = group
    mock = replace('gs_quant.entities.entitlements.Group._group_exists', Mock())
    mock.return_value = True
    g = Group(group_id='groupId', name='fakeGroup', tags=[])
    assert g.save().name == 'fakeGroup'
    replace.restore()


def test_save_create():
    group = TargetGroup.from_dict({
        'name': 'fakeGroup',
        'id': 'groupId',
        'tags': []
    })
    replace = Replacer()
    mock = replace('gs_quant.api.gs.groups.GsGroupsApi.create_group', Mock())
    mock.return_value = group
    mock = replace('gs_quant.entities.entitlements.Group._group_exists', Mock())
    mock.return_value = False
    g = Group(group_id='groupId', name='fakeGroup', tags=[])
    assert g.save().name == 'fakeGroup'
    replace.restore()
