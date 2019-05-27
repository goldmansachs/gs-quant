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

import pytest
from unittest import mock
from base64 import b64decode

from gs_quant.session import GsSession, Environment
from gs_quant.api.gs.content import GsContentApi, OrderBy
from gs_quant.test.fixtures.content import ContentFixtures
from gs_quant.target.content import GetManyContentsResponse

def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')

@pytest.mark.parametrize("description, channels, assetIds, authorIds, tags, offset, limit, orderBy, expected_uri, expected_exception", [
	(
		"Limit is too large, expect exception",
		set(),
		set(),
		set(),
		set(),
		0, 
		1001,
		None,
		None,
		ValueError
	),
	(
		"Offset is too small, expect exception",
		set(),
		set(),
		set(),
		set(),
		-1, 
		None,
		None,
		None,
		ValueError
	),
	(
		"Default params (none specified)", 
		None,
		None,
		None,
		None,
		None, 
		None,
		None,
		'/content',
		None
	),
	(
		"Normal case, multiple parameters", 
		set(['channel-1', 'channel-2']),
		set(['asset-id-1']),
		set(['author-id-1']),
		set(['tag-1']),
		None, 
		None,
		None,
		'/content?channel=channel-1&channel=channel-2&assetId=asset-id-1&authorId=author-id-1&tag=tag-1',
		None
	),
	(
		"With offset, limit, and orderBy", 
		set(),
		set(),
		set(),
		set(),
		2, 
		12,
		{ 'direction': OrderBy.ASC, 'field': 'some-field' },
		'/content?offset=2&limit=12&orderBy=<some-field',
		None
	)
])
def test_get_contents(
	description, 
	channels,
	assetIds,
	authorIds,
	tags,
	offset, 
	limit, 
	orderBy,
	expected_uri,
	expected_exception):
	
	# Arrange
	set_session()

	contents = ContentFixtures.get_many_contents_response()
	with mock.patch.object(GsSession, '_get', return_value=contents) as mock_method:
		
		target = GsContentApi()

		# Act
		if expected_exception != None:
			with pytest.raises(expected_exception):
				actual = target.get_contents(
					channels=channels,
					assetIds=assetIds,
					authorIds=authorIds,
					tags=tags,
					offset=offset,
					limit=limit, 
					orderBy=orderBy)
		else:
			actual = target.get_contents(
				channels=channels,
				assetIds=assetIds,
				authorIds=authorIds,
				tags=tags,
				offset=offset, 
				limit=limit, 
				orderBy=orderBy)
	
			# Assert
			mock_method.assert_called_with(expected_uri, cls=mock.ANY)


def test_get_text():
	# Arrange
	target = GsContentApi()
	contents = ContentFixtures.get_many_contents_response().data

	# Act
	actual = target.get_text(contents)

	# Assert
	assert actual == [(content.id, b64decode(content.content.body)) for content in contents]
