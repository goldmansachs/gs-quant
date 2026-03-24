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

import pytest
from freezegun import freeze_time

from gs_quant.markets import RealtimePricingContext
from gs_quant.markets.markets import LiveMarket, TimestampedMarket


class TestRealtimePricingContextValidation:
    def test_start_end_must_be_datetime(self):
        with pytest.raises(ValueError, match='start and end must be datetime instances'):
            RealtimePricingContext(
                start=dt.date(2025, 3, 18),
                end=dt.date(2025, 3, 18),
                interval=dt.timedelta(minutes=30),
            )

    def test_start_must_be_before_end(self):
        with pytest.raises(ValueError, match='start must be before end'):
            RealtimePricingContext(
                start=dt.datetime(2025, 3, 18, 16, 0),
                end=dt.datetime(2025, 3, 18, 9, 0),
                interval=dt.timedelta(minutes=30),
            )

    def test_start_equal_to_end_raises(self):
        with pytest.raises(ValueError, match='start must be before end'):
            RealtimePricingContext(
                start=dt.datetime(2025, 3, 18, 9, 0),
                end=dt.datetime(2025, 3, 18, 9, 0),
                interval=dt.timedelta(minutes=30),
            )

    def test_interval_too_small(self):
        with pytest.raises(ValueError, match='interval must be at least'):
            RealtimePricingContext(
                start=dt.datetime(2025, 3, 18, 9, 0),
                end=dt.datetime(2025, 3, 18, 16, 0),
                interval=dt.timedelta(seconds=30),
            )

    def test_interval_too_large(self):
        with pytest.raises(ValueError, match='interval must be less than 1 day'):
            RealtimePricingContext(
                start=dt.datetime(2025, 3, 18, 9, 0),
                end=dt.datetime(2025, 3, 19, 9, 0),
                interval=dt.timedelta(days=1),
            )

    def test_interval_at_minimum(self):
        ctx = RealtimePricingContext(
            start=dt.datetime(2025, 3, 18, 9, 0),
            end=dt.datetime(2025, 3, 18, 9, 30),
            interval=dt.timedelta(minutes=10),
        )
        assert len(ctx.timestamps) == 4  # 9:00, 9:10, 9:20, 9:30


class TestBuildTimestamps:
    def test_basic_timestamps(self):
        ctx = RealtimePricingContext(
            start=dt.datetime(2025, 3, 18, 9, 0),
            end=dt.datetime(2025, 3, 18, 11, 0),
            interval=dt.timedelta(minutes=30),
        )
        expected = (
            dt.datetime(2025, 3, 18, 9, 0),
            dt.datetime(2025, 3, 18, 9, 30),
            dt.datetime(2025, 3, 18, 10, 0),
            dt.datetime(2025, 3, 18, 10, 30),
            dt.datetime(2025, 3, 18, 11, 0),
        )
        assert ctx.timestamps == expected

    def test_end_not_on_interval_boundary(self):
        ctx = RealtimePricingContext(
            start=dt.datetime(2025, 3, 18, 9, 0),
            end=dt.datetime(2025, 3, 18, 10, 15),
            interval=dt.timedelta(minutes=30),
        )
        expected = (
            dt.datetime(2025, 3, 18, 9, 0),
            dt.datetime(2025, 3, 18, 9, 30),
            dt.datetime(2025, 3, 18, 10, 0),
        )
        assert ctx.timestamps == expected

    def test_properties(self):
        start = dt.datetime(2025, 3, 18, 9, 0)
        end = dt.datetime(2025, 3, 18, 16, 0)
        interval = dt.timedelta(minutes=30)
        ctx = RealtimePricingContext(start=start, end=end, interval=interval)
        assert ctx.start == start
        assert ctx.end == end
        assert ctx.interval == interval


class TestMarketForTimestamp:
    @freeze_time('2025-03-18 12:00:00')
    @pytest.mark.parametrize(
        'timestamp, is_last, expected_type',
        [
            # Past timestamp today, not last → TimestampedMarket
            (dt.datetime(2025, 3, 18, 9, 0), False, TimestampedMarket),
            # Historical date → TimestampedMarket
            (dt.datetime(2025, 3, 17, 9, 0), False, TimestampedMarket),
            # Close to now but not last → TimestampedMarket
            (dt.datetime(2025, 3, 18, 12, 0), False, TimestampedMarket),
            # Close to now and last → LiveMarket
            (dt.datetime(2025, 3, 18, 12, 0), True, LiveMarket),
            # Far from now even if last → TimestampedMarket
            (dt.datetime(2025, 3, 18, 10, 0), True, TimestampedMarket),
        ],
    )
    def test_market_for_timestamp(self, timestamp, is_last, expected_type):
        ctx = RealtimePricingContext(
            start=dt.datetime(2025, 3, 17, 9, 0),
            end=dt.datetime(2025, 3, 18, 12, 10),
            interval=dt.timedelta(minutes=10),
        )
        market = ctx._market_for_timestamp(timestamp, 'LDN', is_last=is_last)
        assert isinstance(market, expected_type)
