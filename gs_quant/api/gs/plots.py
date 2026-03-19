"""
Copyright 2020 Goldman Sachs.
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

from collections.abc import Iterable
from typing import Tuple, Union, Sequence

from gs_quant.datetime.relative_date import RelativeDate
from gs_quant.session import GsSession
from gs_quant.target.charts import Chart, ChartShare
import datetime as dt

from gs_quant.common import TimeFilter


class GsPlotApi:
    """GS Chart API client implementation"""

    # CRUD

    @classmethod
    def get_many_charts(cls, limit: int = 100) -> Tuple[Chart, ...]:
        return GsSession.current.sync.get(f'/charts?limit={limit}', cls=Chart)['results']

    @classmethod
    async def get_many_charts_async(cls, limit: int = 100) -> Tuple[Chart, ...]:
        return (await GsSession.current.async_.get(f'/charts?limit={limit}', cls=Chart))['results']

    @classmethod
    def get_chart(cls, chart_id: str) -> Chart:
        return GsSession.current.sync.get(f'/charts/{chart_id}', cls=Chart)

    @classmethod
    async def get_chart_async(cls, chart_id: str) -> Chart:
        return await GsSession.current.async_.get(f'/charts/{chart_id}', cls=Chart)

    @classmethod
    def create_chart(cls, chart: Chart) -> Chart:
        return GsSession.current.sync.post('/charts', chart, cls=Chart)

    @classmethod
    async def create_chart_async(cls, chart: Chart) -> Chart:
        return await GsSession.current.async_.post('/charts', chart, cls=Chart)

    @classmethod
    def update_chart(cls, chart: Chart):
        return GsSession.current.sync.put(f'/charts/{chart.id}', chart, cls=Chart)

    @classmethod
    async def update_chart_async(cls, chart: Chart):
        return await GsSession.current.async_.put(f'/charts/{chart.id}', chart, cls=Chart)

    @classmethod
    def delete_chart(cls, chart_id: str) -> dict:
        return GsSession.current.sync.delete(f'/charts/{chart_id}')

    @classmethod
    async def delete_chart_async(cls, chart_id: str) -> dict:
        return await GsSession.current.async_.delete(f'/charts/{chart_id}')

    # Additional methods

    @staticmethod
    def _build_plot_payload(
        expressions: Sequence[str],
        start: Union[dt.date, dt.datetime, RelativeDate, str] = RelativeDate("-1y"),
        end: Union[dt.date, dt.datetime, RelativeDate, str] = RelativeDate("-1b"),
        real_time: bool = False,
        *,
        statistics: bool = False,
        interval: str = None,
        time_filter: TimeFilter = None,
    ) -> dict:
        start = start.apply_rule() if isinstance(start, RelativeDate) else start
        end = end.apply_rule() if isinstance(end, RelativeDate) else end
        expressions = [expressions] if isinstance(expressions, str) else expressions
        if real_time and (
            (isinstance(start, dt.date) and not isinstance(start, dt.datetime))
            or (isinstance(end, dt.date) and not isinstance(end, dt.datetime))
        ):
            raise ValueError("Real-time plots require start and end to be datetimes, not dates.")
        return {
            "expressions": expressions,
            "statistics": statistics,
            "realTime": real_time,
            "interval": interval or ("1m" if real_time else "1D"),
            **({"startTime": start, "endTime": end} if real_time else {"startDate": start, "endDate": end}),
            **({"timeFilter": time_filter} if time_filter else {}),
        }

    @classmethod
    async def plot_runner_async(
        cls,
        expressions: Sequence[str],
        start: Union[dt.date, dt.datetime, RelativeDate, str] = RelativeDate("-1y"),
        end: Union[dt.date, dt.datetime, RelativeDate, str] = RelativeDate("-1b"),
        real_time: bool = False,
        *,
        statistics: bool = False,
        interval: str = None,
        time_filter: TimeFilter = None,
    ) -> dict:
        payload = cls._build_plot_payload(
            expressions, start, end, real_time, statistics=statistics, interval=interval, time_filter=time_filter
        )
        return await GsSession.current.async_.post('/plots/runner', payload)

    @classmethod
    def plot_runner(
        cls,
        expressions: Sequence[str],
        start: Union[dt.date, dt.datetime, RelativeDate, str] = RelativeDate("-1y"),
        end: Union[dt.date, dt.datetime, RelativeDate, str] = RelativeDate("-1b"),
        real_time: bool = False,
        *,
        statistics: bool = False,
        interval: str = None,
        time_filter: TimeFilter = None,
    ) -> dict:
        payload = cls._build_plot_payload(
            expressions, start, end, real_time, statistics=statistics, interval=interval, time_filter=time_filter
        )
        return GsSession.current.sync.post('/plots/runner', payload)

    @classmethod
    def share_chart(cls, chart_id: str, users: Iterable):
        # endpoint silently discards tokens not prefixed with 'guid:' => can't be used for roles, groups, etc.
        if any(map(lambda x: not x.startswith('guid:'), users)):
            raise ValueError('Chart can only be shared with individual users via this method.')
        chart = cls.get_chart(chart_id)
        share = ChartShare(tuple(users), chart.version)
        return GsSession.current.sync.post(f'/charts/{chart_id}/share', share, cls=Chart)

    @classmethod
    async def share_chart_async(cls, chart_id: str, users: Iterable):
        # endpoint silently discards tokens not prefixed with 'guid:' => can't be used for roles, groups, etc.
        if any(map(lambda x: not x.startswith('guid:'), users)):
            raise ValueError('Chart can only be shared with individual users via this method.')
        chart = await cls.get_chart_async(chart_id)
        share = ChartShare(tuple(users), chart.version)
        return await GsSession.current.async_.post(f'/charts/{chart_id}/share', share, cls=Chart)
