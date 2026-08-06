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

import logging

from gs_quant.session import GsSession

_logger = logging.getLogger(__name__)

API = '/marketview/widgets'


class GsMarketviewWidgetsApi:
    """
    Client library for the Goldman Sachs Marketview Widgets API.

    Provides read-only methods for searching, retrieving, and discovering
    Marketview widgets.
    """

    # ------------------------------------------------------------------
    # Widget search / retrieval
    # ------------------------------------------------------------------

    @classmethod
    def get_widgets(
        cls,
        ids: list[str] = None,
        query: str = None,
        limit: int = 100,
        offset: int = 0,
        author: list[str] = None,
        tags: list[str] = None,
        order_by: str = None,
        status: list[str] = None,
        state: str = None,
        metadata: bool = False,
    ) -> dict:
        """
        Search / list widgets with optional filters.

        :param ids: Filter by a list of widget IDs. Cannot be combined with ``query``.
        :param query: Full-text search string. Cannot be combined with ``ids``.
        :param limit: Maximum number of results to return per page (default 100).
        :param offset: Number of results to skip (default 0).
        :param author: Filter by author GUID(s).
        :param tags: Filter by widget tag(s).
        :param order_by: Sort expression, e.g. ``'>lastUpdatedTime'``.
        :param status: Filter by widget status(es), e.g. ``['PUBLISHED']``.
        :param state: Optional widget state to query. See the Marketview API reference for supported values.
        :param metadata: If ``True``, include full widget metadata in each result (default ``False``).
        :return: dict containing ``results`` and ``total_results``.
        """
        url = f'{API}?limit={limit}&offset={offset}&metadata={str(metadata).lower()}'
        if ids:
            url += ''.join(f'&ids={i}' for i in ids)
        if query:
            url += f'&query={query}'
        if author:
            url += ''.join(f'&author={a}' for a in author)
        if tags:
            url += ''.join(f'&tags={t}' for t in tags)
        if order_by:
            url += f'&orderBy={order_by}'
        if status:
            url += ''.join(f'&status={s}' for s in status)
        if state:
            url += f'&state={state}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_widget(
        cls,
        widget_id: str,
        merge_params: bool = False,
        state: str = None,
    ) -> dict:
        """
        Retrieve a single widget by its ID.

        :param widget_id: Widget ID.
        :param merge_params: If ``True``, merge user-modified parameters into the widget (default ``False``).
        :param state: Optional widget state to retrieve. See the Marketview API reference for supported values.
        :return: Widget document as a dict.
        """
        url = f'{API}/{widget_id}?mergeParams={str(merge_params).lower()}'
        if state:
            url += f'&state={state}'
        return GsSession.current.sync.get(url)

    @classmethod
    def get_trending_widgets(cls, limit: int = 10) -> dict:
        """
        Retrieve trending widgets based on platform-wide engagement signals.

        :param limit: Maximum number of widgets to return (default 10).
        :return: dict containing ``results`` and ``total_results``.
        """
        return GsSession.current.sync.get(f'{API}/trending?limit={limit}')

    @classmethod
    def get_personalized_widgets(cls, limit: int = 10, metadata: bool = False) -> dict:
        """
        Retrieve widgets personalised for the current user.

        :param limit: Maximum number of widgets to return (default 10).
        :param metadata: If ``True``, include full widget metadata in each result (default ``False``).
        :return: dict containing ``results`` and ``total_results``.
        """
        return GsSession.current.sync.get(f'{API}/personalized?limit={limit}&metadata={str(metadata).lower()}')
