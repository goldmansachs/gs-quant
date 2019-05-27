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

import operator
from enum import Enum
from base64 import b64decode
from urllib.parse import quote
from typing import List, Tuple
from collections import OrderedDict

from gs_quant.session import GsSession
from gs_quant.target.content import ContentResponse, GetManyContentsResponse

class OrderBy(Enum):
	"""
	Content ordering
	"""
	ASC = 'asc'
	DESC = 'desc'

	def __str__(self):
		return str(self.value)

class GsContentApi:
	"""GS Content API client implementation"""

	@classmethod
	def get_contents(
		cls,
		channels: set = None,
		assetIds: set = None,
		authorIds: set = None,
		tags: set = None,
		offset: int = 0,
		limit: int = 10,
		orderBy: dict = { 'direction': OrderBy.DESC, 'field': 'createdTime'}
	) -> List[ContentResponse]:
		"""
		Get contents for given parameters

		:param channels: Channels
		:param assetIds: Marquee Asset Ids
		:param authorIds: Marquee Author Guids
		:param tags: Tags
		:param limit: Limit (number of contents to return)
		:param limit: Offset (offset of contents)
		:param limit: OrderBy (dict for specifying how to sort contents)
		:return: A list of ContentResponse objects

		**Examples**

		>>> from gs_quant.api.gs.content import GsContentApi
		>>>
		>>> gs_content_api = GsContentApi()
		>>> contents = gs_content_api.get_contents(channels=['G10'])
		"""

		if limit and limit > 1000:
			raise ValueError('Limit is too large. Limit must be <= 1000.')

		if offset and (offset < 0 or offset >= limit):
			raise ValueError('Invalid offset. Offset must be >= 0 and < limit')

		parameters_dict = cls._build_parameters_dict(
			channel=channels,
			assetId=assetIds,
			authorId=authorIds,
			tag=tags,
			offset=[offset] if offset else None,
			limit=[limit] if limit else None,
			orderBy=[orderBy] if orderBy else None)

		query_string = '' if not parameters_dict else cls._build_query_string(parameters_dict)
		contents = GsSession.current._get(f'/content{query_string}', cls=GetManyContentsResponse)
		return contents.data

	@staticmethod
	def get_text(contents: List[ContentResponse]) -> List[Tuple[str, str]]:
		"""
		Get text for contents

		:param contents: List of ContentResponse objects
		:return: A list of tuples representing (<content_id>, <content_text>)

		**Examples**

		>>> from gs_quant.api.gs.content import GsContentApi
		>>>
		>>> gs_content_api = GsContentApi()
		>>> contents = gs_content_api.get_contents(channels=['G10'])
		>>> text = gs_content_api.get_text(contents)
		"""
		return [(content.id, b64decode(content.content.body)) for content in contents]

	@classmethod
	def _build_parameters_dict(cls, **kwargs) -> dict:
		"""
		Builds dict of valid parameters to their value,
		filtering out any parameters for which "None" is
		the value.
		"""
		parameters = {}
		for key, value in kwargs.items():
			if value:
				parameters.setdefault(key, []).extend(sorted(value))
		return OrderedDict(parameters)

	@classmethod
	def _build_query_string(cls, parameters: dict) -> str:
		"""
		Builds a query string accepted by the Content API

		Example:

		In: { 'channel': ['G10', 'EM'], 'limit': 10 }
		Out: ?channel=G10&channel=EM&limit=10
		"""
		query_string = '?'

		# Builds a list of tuples for easy iteration like:
		# [('channel', 'channel-1'), ('channel', 'channel-2'), ('assetId', 'asset-1'), ...]
		parameter_tuples =  [(parameter_name, parameter_value) 
			for parameter_name, parameter_values in parameters.items()
				for parameter_value in parameter_values]

		for index, parameter_tuple in enumerate(parameter_tuples):
			name, value = parameter_tuple
			value = quote(value.encode()) if type(value) == str else value

			if name == 'orderBy':
				value = cls._convert_order_by(value)

			query_string += f'{name}={value}' if index == 0 else f'&{name}={value}'

		return query_string


	@classmethod
	def _convert_order_by(cls, orderBy: dict) -> str:
		"""
		Converts an orderByDirection and orderByField to an acceptable query parameter format
		expected by the Content API
		"""
		orderByParameter = ''

		direction = orderBy['direction']
		field = orderBy['field']

		if direction == OrderBy.DESC:
			orderByParameter = '>'
		else:
			orderByParameter = '<'

		orderByParameter += field
		return orderByParameter
