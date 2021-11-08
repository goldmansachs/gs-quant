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

from gs_quant.entities.entitlements import User
from gs_quant.target.reports import User as TargetUser


def test_get():
    user = TargetUser.from_dict({
        'id': 'userId',
        'email': 'jane.doe@gs.com',
        'name': 'Doe, Jane',
        'company': 'Goldman Sachs Group'
    })
    replace = Replacer()
    mock = replace('gs_quant.api.gs.users.GsUsersApi.get_users', Mock())
    mock.return_value = [user]
    assert User.get(name='Doe, Jane').id == 'userId'
    replace.restore()


def test_get_many():
    users = [TargetUser.from_dict({
        'id': 'userId',
        'email': 'jane.doe@gs.com',
        'name': 'Doe, Jane',
        'company': 'Goldman Sachs Group'
    }),
        TargetUser.from_dict({
            'id': 'userId2',
            'email': 'john.doe@gs.com',
            'name': 'Doe, John',
            'company': 'Goldman Sachs Group'
        })
    ]
    replace = Replacer()
    mock = replace('gs_quant.api.gs.users.GsUsersApi.get_users', Mock())
    mock.return_value = users
    assert len(User.get_many(user_ids=['userId', 'userId2'])) == 2
    replace.restore()
