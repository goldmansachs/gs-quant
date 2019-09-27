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

from base64 import b64decode
from unittest import mock

import pytest

from gs_quant.api.gs.content import GsContentApi, OrderBy
from gs_quant.session import GsSession, Environment
from gs_quant.target.content import GetManyContentsResponse
from gs_quant.test.fixtures.content import ContentFixtures


def set_session():
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')


@pytest.mark.parametrize(
    'description, channels, asset_ids, author_ids, tags, offset, limit, order_by, expected_uri, expected_exception',
    [('Limit is too large, expect exception', set(),
      set(),
      set(),
      set(),
      0, 1001, None, None, ValueError),
     ("Offset is too small, expect exception", set(),
      set(),
      set(),
      set(),
      -1, None, None, None, ValueError),
     ('Default params (none specified)', None, None, None, None, None, None, None, '/content', None),
     ('Normal case, multiple parameters', ('channel-1', 'channel-2'),
      {'asset-id-1'},
      {'author-id-1'},
      {'tag-1'},
      None, None, None,
      '/content?channel=channel-1&channel=channel-2&asset_id=asset-id-1&author_id=author-id-1&tag=tag-1', None),
     ("With offset, limit, and orderBy", set(),
      set(),
      set(),
      set(),
      2, 12, {'direction': OrderBy.ASC, 'field': 'some-field'},
      '/content?offset=2&limit=12&order_by=<some-field', None)])
def test_get_contents(
        description,
        channels,
        asset_ids,
        author_ids,
        tags,
        offset,
        limit,
        order_by,
        expected_uri,
        expected_exception):

    # Arrange
    set_session()

    contents = ContentFixtures.get_many_contents_response()
    with mock.patch.object(GsSession, '_get', return_value=contents) as mock_method:
        # Act
        if expected_exception is not None:
            with pytest.raises(expected_exception):
                actual = GsContentApi.get_contents(
                    channels=channels,
                    asset_ids=asset_ids,
                    author_ids=author_ids,
                    tags=tags,
                    offset=offset,
                    limit=limit,
                    order_by=order_by)
                print(actual)
        else:
            actual = GsContentApi.get_contents(
                channels=channels,
                asset_ids=asset_ids,
                author_ids=author_ids,
                tags=tags,
                offset=offset,
                limit=limit,
                order_by=order_by)
            print(actual)

            # Assert
            mock_method.assert_called_with(expected_uri, cls=GetManyContentsResponse)


def test_get_text():
    # Arrange
    target = GsContentApi()
    contents = ContentFixtures.get_many_contents_response().data

    # Act
    actual = target.get_text(contents)

    # Assert
    assert actual == [(content.id, b64decode(content.content.body)) for content in contents]
