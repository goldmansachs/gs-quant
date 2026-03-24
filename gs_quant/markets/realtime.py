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

import datetime as dt
from typing import Optional, Tuple, Type

from gs_quant.base import InstrumentBase, RiskKey
from gs_quant.common import RiskMeasure
from gs_quant.datetime.date import prev_business_date
from gs_quant.risk.results import PricingFuture, HistoricalPricingFuture
from .historical import HistoricalPricingContext
from .markets import LiveMarket, TimestampedMarket
from ..api.risk import GenericRiskApi


class RealtimePricingContext(HistoricalPricingContext):
    """
    A context for producing valuations at multiple intraday timestamps with a given interval.

    Uses RefMarket for each timestamp derived from start/end with the specified interval.
    If the timestamp's date is today, the base_date is set to the previous business date.
    If the last timestamp is close to the current time, a LiveMarket is used instead.
    """

    _MIN_INTERVAL = dt.timedelta(minutes=1)
    _MAX_INTERVAL = dt.timedelta(days=1)
    _LIVE_THRESHOLD = dt.timedelta(minutes=15)

    def __init__(
        self,
        start: dt.datetime,
        end: dt.datetime,
        interval: dt.timedelta,
        is_async: bool = None,
        is_batch: bool = None,
        use_cache: bool = None,
        visible_to_gs: bool = None,
        request_priority: Optional[int] = None,
        csa_term: str = None,
        market_data_location: Optional[str] = None,
        timeout: Optional[int] = None,
        show_progress: Optional[bool] = None,
        use_server_cache: Optional[bool] = None,
        provider: Optional[Type[GenericRiskApi]] = None,
    ):
        """
        A context for producing valuations at multiple intraday timestamps

        :param start: start datetime
        :param end: end datetime
        :param interval: time interval between pricing timestamps (minimum 10 minutes, must be less than 1 day)
        :param is_async: return immediately (True) or wait for results (False) (defaults to False)
        :param is_batch: use for calculations expected to run longer than 3 mins, to avoid timeouts.
            It can be used with is_async=True|False (defaults to False)
        :param use_cache: store results in the pricing cache (defaults to False)
        :param visible_to_gs: are the contents of risk requests visible to GS (defaults to False)
        :param csa_term: the csa under which the calculations are made. Default is local ccy ois index
        :param market_data_location: the location for sourcing market data ('NYC', 'LDN' or 'HKG' (defaults to LDN)
        :param timeout: the timeout for batch operations
        :param show_progress: add a progress bar (tqdm)
        :param use_server_cache: cache query results on the GS servers

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> ir_swap = IRSwap('Pay', '10y', 'DKK')
        >>> with RealtimePricingContext(
        ...     start=dt.datetime(2025, 3, 18, 9, 0),
        ...     end=dt.datetime(2025, 3, 18, 16, 0),
        ...     interval=dt.timedelta(minutes=30),
        ... ):
        ...     price_f = ir_swap.price()
        >>>
        >>> price_series = price_f.result()
        """
        if not isinstance(start, dt.datetime) or not isinstance(end, dt.datetime):
            raise ValueError('start and end must be datetime instances')

        if start >= end:
            raise ValueError('start must be before end')

        if interval < self._MIN_INTERVAL:
            raise ValueError(f'interval must be at least {self._MIN_INTERVAL}')

        if interval >= self._MAX_INTERVAL:
            raise ValueError('interval must be less than 1 day; use HistoricalPricingContext for daily intervals')

        self.__start = start
        self.__end = end
        self.__interval = interval
        self.__timestamps = self._build_timestamps(start, end, interval)

        # Use the start date as pricing_date for the parent context
        dates = [ts.date() for ts in self.__timestamps]

        super().__init__(
            dates=dates,
            is_async=is_async,
            is_batch=is_batch,
            use_cache=use_cache,
            visible_to_gs=visible_to_gs,
            request_priority=request_priority,
            csa_term=csa_term,
            market_data_location=market_data_location,
            timeout=timeout,
            show_progress=show_progress,
            use_server_cache=use_server_cache,
            provider=provider,
        )

    @staticmethod
    def _build_timestamps(start: dt.datetime, end: dt.datetime, interval: dt.timedelta) -> Tuple[dt.datetime, ...]:
        timestamps = []
        current = start
        while current <= end:
            timestamps.append(current)
            current += interval
        return tuple(timestamps)

    def _market_for_timestamp(self, timestamp: dt.datetime, location, *, is_last: bool = False):
        if is_last:
            now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
            if abs(timestamp - now) < self._LIVE_THRESHOLD:
                return LiveMarket(location=location)

        base_date = timestamp.date()
        if base_date == dt.date.today():
            base_date = prev_business_date(base_date)

        return TimestampedMarket(timestamp=timestamp, location=location, base_date=base_date)

    def calc(self, instrument: InstrumentBase, risk_measure: RiskMeasure) -> PricingFuture:
        futures = []

        provider = instrument.provider if self.provider is None else self.provider
        scenario = self._scenario
        parameters = self._parameters
        location = self.market.location
        last_ts = self.__timestamps[-1]

        for timestamp in self.__timestamps:
            market = self._market_for_timestamp(timestamp, location, is_last=(timestamp == last_ts))
            risk_key = RiskKey(provider, timestamp, market, parameters, scenario, risk_measure)
            futures.append(self._calc(instrument, risk_key))

        return HistoricalPricingFuture(futures)

    @property
    def timestamps(self) -> Tuple[dt.datetime, ...]:
        return self.__timestamps

    @property
    def start(self) -> dt.datetime:
        return self.__start

    @property
    def end(self) -> dt.datetime:
        return self.__end

    @property
    def interval(self) -> dt.timedelta:
        return self.__interval
