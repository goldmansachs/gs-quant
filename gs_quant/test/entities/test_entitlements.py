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

from gs_quant.common import Entitlements as TargetEntitlements
from gs_quant.entities.entitlements import Group, Entitlements, User, EntitlementBlock
from gs_quant.target.groups import Group as TargetGroup
from gs_quant.target.reports import User as TargetUser


def get_fake_user():
    user = TargetUser.from_dict({
        'id': 'userId',
        'email': 'jane.doe@gs.com',
        'name': 'Jane Doe',
        'company': 'Goldman Sachs Group'
    })

    replace = Replacer()
    mock = replace('gs_quant.api.gs.users.GsUsersApi.get_users', Mock())
    mock.return_value = [user]
    user = User.get(email='jane.doe@gs.com')
    replace.restore()

    return user


def get_fake_group():
    group = TargetGroup.from_dict({
        'name': 'fakeGroup',
        'id': 'groupId',
        'tags': []
    })

    replace = Replacer()
    mock = replace('gs_quant.api.gs.groups.GsGroupsApi.get_group', Mock())
    mock.return_value = group
    group = Group.get(group_id='groupId')
    replace.restore()

    return group


def test_to_target():
    ent = Entitlements(edit=EntitlementBlock(users=[get_fake_user()], groups=[get_fake_group()]))
    as_target = ent.to_target()
    assert as_target.edit == ('guid:userId', 'group:groupId')


def test_to_dict():
    ent = Entitlements(edit=EntitlementBlock(users=[get_fake_user()], groups=[get_fake_group()]))
    as_dict = ent.to_dict()
    assert as_dict == {'edit': ('guid:userId', 'group:groupId')}


def test_from_target():
    replace = Replacer()
    mock = replace('gs_quant.api.gs.users.GsUsersApi.get_users', Mock())
    mock.return_value = [TargetUser.from_dict({
        'id': 'userId',
        'email': 'jane.doe@gs.com',
        'name': 'Jane Doe',
        'company': 'Goldman Sachs Group'
    })]
    ent = Entitlements.from_target(TargetEntitlements(edit=('guid:userId', 'role:roleId')))
    replace.restore()
    assert ent.edit.users == [get_fake_user()]
    assert ent.edit.roles == ['roleId']


def test_from_dict():
    replace = Replacer()
    mock = replace('gs_quant.api.gs.users.GsUsersApi.get_users', Mock())
    mock.return_value = [TargetUser.from_dict({
        'id': 'userId',
        'email': 'jane.doe@gs.com',
        'name': 'Jane Doe',
        'company': 'Goldman Sachs Group'
    })]
    ent = Entitlements.from_dict({'edit': ['guid:userId', 'role:roleId']})
    replace.restore()
    assert ent.edit.users == [get_fake_user()]
    assert ent.edit.roles == ['roleId']
