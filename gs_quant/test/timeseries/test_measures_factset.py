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

import datetime as dt
from unittest.mock import Mock

import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from testfixtures import Replacer

import gs_quant.timeseries.measures_factset as tm
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.index import Index
from gs_quant.timeseries.measures_factset import (
    EstimateItem,
    EstimateStatistic,
    EstimateBasis,
    FiscalPeriod,
    FundamentalMetric,
    FundamentalFormat,
    FundamentalBasis,
    RatingType,
    GIREstimateItem,
    GIREstimateBasis,
    EVItem,
)

_index = [pd.Timestamp('2021-03-30')]
_test_datasets = ('TEST_DATASET',)


def mock_fe_estimate_af(_cls, bbid, start, end, feItem):
    d = {
        'date': [dt.date(2022, 1, 8), dt.date(2022, 1, 12), dt.date(2022, 1, 13)],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'fePerRel': [1.0] * 3,
        'adjDate': [dt.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'consEndDate': [dt.date(2022, 1, 11)] * 3,
        'feItemDesc': ['Earnings Per Share'] * 3,
        'feFpEnd': [dt.date(2022, 9, 30)] * 3,
        'feDownAf': [10.0, 3.0, 3.0],
        'feHighAf': [6.353628] * 3,
        'feLowAf': [5.2] * 3,
        'feMeanAf': [5.749689, 5.748439, 5.756439],
        'feMedianAf': [5.745] * 3,
        'feNumEstAf': [40] * 3,
        'feStdDevAf': [0.259250, 0.258130, 0.258687],
        'feUpAf': [15.0, 5.0, 6.0],
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_BASIC_CONH_AF_GLOBAL'

    return df


def mock_fe_estimate_qf(_cls, bbid, start, end, feItem):
    d = {
        'date': [dt.date(2022, 1, 8), dt.date(2022, 1, 12), dt.date(2022, 1, 13)],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'fePerRel': [1.0] * 3,
        'adjDate': [dt.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'consEndDate': [dt.date(2022, 1, 11)] * 3,
        'feItemDesc': ['Earnings Per Share'] * 3,
        'feFpEnd': [dt.date(2022, 9, 30)] * 3,
        'feDownQf': [10.0, 3.0, 3.0],
        'feHighQf': [6.353628] * 3,
        'feLowQf': [5.2] * 3,
        'feMeanQf': [5.749689, 5.748439, 5.756439],
        'feMedianQf': [5.745] * 3,
        'feNumEstQf': [40] * 3,
        'feStdDevQf': [0.259250, 0.258130, 0.258687],
        'feUpQf': [15.0, 5.0, 6.0],
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_BASIC_CONH_QF_GLOBAL'
    return df


def mock_fe_estimate_saf(_cls, bbid, start, end, feItem):
    d = {
        'date': [dt.date(2022, 1, 8), dt.date(2022, 1, 12), dt.date(2022, 1, 13)],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'fePerRel': [1.0] * 3,
        'adjDate': [dt.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'consEndDate': [dt.date(2022, 1, 11)] * 3,
        'feItemDesc': ['Earnings Per Share'] * 3,
        'feFpEnd': [dt.date(2022, 9, 30)] * 3,
        'feDownSaf': [10.0, 3.0, 3.0],
        'feHighSaf': [6.353628] * 3,
        'feLowSaf': [5.2] * 3,
        'feMeanSaf': [5.749689, 5.748439, 5.756439],
        'feMedianSaf': [5.745] * 3,
        'feNumEstSaf': [40] * 3,
        'feStdDevSaf': [0.259250, 0.258130, 0.258687],
        'feUpSaf': [15.0, 5.0, 6.0],
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_BASIC_CONH_SAF_GLOBAL'
    return df


def mock_fe_estimate_ntm(_cls, bbid, start, end, feItem):
    d = {
        'date': [dt.date(2022, 1, 8), dt.date(2022, 1, 9), dt.date(2022, 1, 10)],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'feHighNtm': [6.353628] * 3,
        'feLowNtm': [5.2] * 3,
        'feMeanNtm': [5.749689, 5.748439, 5.756439],
        'feMedianNtm': [5.745] * 3,
        'feHighStm': [6.353628] * 3,
        'feLowStm': [5.2] * 3,
        'feMeanStm': [5.749689, 5.748439, 5.756439],
        'feMedianStm': [5.745] * 3,
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_NTM'
    return df


def mock_fe_estimate_lt(_cls, bbid, start, end, feItem):
    d = {
        'date': [dt.date(2022, 1, 8), dt.date(2022, 1, 12), dt.date(2022, 1, 13)],
        'isin': ['US0378331005'] * 3,
        'feItem': ['PRICE_TGT'] * 3,
        'adjDate': [dt.date(2020, 8, 31)] * 3,
        'consEndDate': [dt.date(2022, 1, 11)] * 3,
        'feDownLt': [10.0, 3.0, 3.0],
        'feHighLt': [6.353628] * 3,
        'feLowLt': [5.2] * 3,
        'feMeanLt': [5.749689, 5.748439, 5.756439],
        'feMedianLt': [5.745] * 3,
        'feNumEstLt': [40] * 3,
        'feStdDevLt': [0.259250, 0.258130, 0.258687],
        'feUpLt': [15.0, 5.0, 6.0],
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_BASIC_CONH_LT_GLOBAL'
    return df


def mock_fe_actual(_cls, bbid, start, end, feItem):
    d = {
        'date': [dt.date(2020, 1, 8), dt.date(2021, 1, 12), dt.date(2022, 1, 13)],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'adjDate': [dt.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'feFpEnd': [dt.date(2022, 9, 30), dt.date(2021, 9, 30), dt.date(2020, 9, 30)],
        'feValue': [15.0, 5.0, 6.0],
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_BASIC_ACT_AF_GLOBAL'

    return df


def mock_fe_estimate_empty(_cls, bbid, start, end, feItem):
    df = MarketDataResponseFrame()
    df.dataset_id = 'FE_BASIC_CONH_SAF_GLOBAL'
    return df


def mock_factset_fundamentals_empty(_cls, bbid, start, end):
    df = MarketDataResponseFrame()
    df.dataset_id = 'FF_BASIC_R_AF_GLOBAL'
    return df


def mock_factset_fundamentals_basic(_cls, bbid, start, end):
    d = {
        'date': [pd.Timestamp('2024-09-30 00:00:00')],
        'isin': ['US0378331005'],
        'adjDate': [pd.Timestamp('2020-08-31 00:00:00')],
        'currency': ['USD'],
        'ffEpsBasic': [6.109],
        'fsymId': ['MH33D6-R'],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FF_BASIC_AF_GLOBAL'
    return df


def mock_factset_fundamentals_basic_derived(_cls, bbid, start, end):
    d = {
        'date': [pd.Timestamp('2024-09-30 00:00:00')],
        'isin': ['US0378331005'],
        'adjDate': [pd.Timestamp('2020-08-31 00:00:00')],
        'currency': ['USD'],
        'ffEbitdaOper': [6.109],
        'fsymId': ['MH33D6-R'],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FF_BASIC_DER_AF_GLOBAL'
    return df


def mock_factset_fundamentals_basic_restated(_cls, bbid, start, end):
    d = {
        'date': [pd.Timestamp('2024-09-30 00:00:00')],
        'isin': ['US0378331005'],
        'adjDate': [pd.Timestamp('2020-08-31 00:00:00')],
        'currency': ['USD'],
        'ffEpsBasic': [6.109],
        'fsymId': ['MH33D6-R'],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FF_BASIC_R_AF_GLOBAL'
    return df


def mock_factset_ratings(_cls, bbid, start, end):
    d = {
        'date': [pd.Timestamp('2024-12-31 00:00:00')] * 3,
        'isin': ['US0378331005'] * 3,
        'feItem': ['REC'] * 3,
        'adjDate': [dt.date(2024, 12, 31)] * 3,
        'consEndDate': [dt.date(2024, 12, 31)] * 3,
        'feItemDesc': ['Recommendation'] * 3,
        'feFpEnd': [dt.date(2024, 12, 31)] * 3,
        'feBuy': [21.0, 3.0, 3.0],
        'feHold': [14.0, 3.0, 3.0],
        'feNoRec': [1.0, 3.0, 3.0],
        'feOver': [10.0, 3.0, 3.0],
        'feSell': [4.0, 3.0, 3.0],
        'feUnder': [1.0, 3.0, 3.0],
        'feTotal': [10.0, 3.0, 3.0],
        'feMark': [1.57] * 3,
        'fsymId': ['MH33D6-R'] * 3,
        'bbid': ['AAPL UW'] * 3,
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FE_BASIC_CONH_REC_GLOBAL'
    return df


mock_asset = Index(
    id_='MA000',
    asset_class='Equity',
    name='test',
    currency='USD',
    exchange='NASD',
)


def test_factset_estimates():
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2022, 1, 1), end=dt.date(2025, 1, 31)):
        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_af)

        actual = tm.factset_estimates(
            mock_asset,
            metric=EstimateItem.EPS,
            statistic=EstimateStatistic.MEDIAN,
            report_basis=EstimateBasis.ANN,
            period=FiscalPeriod(2022),
        )
        assert_series_equal(
            pd.Series(
                [5.745] * 4,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                    dtype='datetime64[ns]',
                    name='date',
                    freq=None,
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_CONH_AF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_qf)

        actual = tm.factset_estimates(
            mock_asset,
            metric=EstimateItem.EPS,
            statistic=EstimateStatistic.MEDIAN,
            report_basis=EstimateBasis.QTR,
            period=FiscalPeriod(2022, 3),
        )
        assert_series_equal(
            pd.Series(
                [5.745] * 4,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                    dtype='datetime64[ns]',
                    name='date',
                    freq=None,
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_CONH_QF_GLOBAL'

        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.QTR,
                period=FiscalPeriod(2022, 1),
            )

        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.QTR,
                period=FiscalPeriod(2022, -1),
            )

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_saf)

        actual = tm.factset_estimates(
            mock_asset,
            metric=EstimateItem.EPS,
            statistic=EstimateStatistic.MEDIAN,
            report_basis=EstimateBasis.SEMI,
            period=FiscalPeriod(2022, 2),
        )
        assert_series_equal(
            pd.Series(
                [5.745] * 4,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                    dtype='datetime64[ns]',
                    name='date',
                    freq=None,
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_CONH_SAF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_ntm)

        actual = tm.factset_estimates(
            mock_asset, metric=EstimateItem.EPS, statistic=EstimateStatistic.MEDIAN, report_basis=EstimateBasis.NTM
        )
        assert_series_equal(
            pd.Series(
                [5.745] * 3,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10'], dtype='datetime64[ns]', name='date', freq=None
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_NTM'

        actual = tm.factset_estimates(
            mock_asset, metric=EstimateItem.EPS, statistic=EstimateStatistic.MEDIAN, report_basis=EstimateBasis.STM
        )
        assert_series_equal(
            pd.Series(
                [5.745] * 3,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10'], dtype='datetime64[ns]', name='date', freq=None
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_NTM'

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_lt)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.PRICE_TGT, statistic=EstimateStatistic.MEDIAN)
        assert_series_equal(
            pd.Series(
                [5.745] * 4,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                    dtype='datetime64[ns]',
                    name='date',
                    freq=None,
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_CONH_LT_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_fe_actual)

        actual = tm.factset_estimates(
            mock_asset, metric=EstimateItem.EPS, statistic=EstimateStatistic.ACTUAL, report_basis=EstimateBasis.ANN
        )
        assert_series_equal(
            pd.Series(
                [15.0],
                index=pd.DatetimeIndex(['2022-09-30'], dtype='datetime64[ns]', name='date', freq=None),
                name=EstimateStatistic.ACTUAL.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_ACT_AF_GLOBAL'

        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.SEMI,
                period=FiscalPeriod(2022),
            )
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.SEMI,
                period=FiscalPeriod(2022, -1),
            )

        replace('gs_quant.data.Dataset.get_data', None)
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.SEMI,
                period=FiscalPeriod(2022, 1),
            )

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_af)
        actual = tm.factset_estimates(
            mock_asset,
            metric=EstimateItem.EPS,
            statistic=EstimateStatistic.MEDIAN,
            report_basis=EstimateBasis.ANN,
            period=1,
        )
        assert_series_equal(
            pd.Series(
                [5.745] * 4,
                index=pd.DatetimeIndex(
                    ['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                    dtype='datetime64[ns]',
                    name='date',
                    freq=None,
                ),
                name=EstimateStatistic.MEDIAN.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_CONH_AF_GLOBAL'

        # Get quarterly data without specifying period
        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_qf)
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.QTR,
                period=FiscalPeriod(2022),
            )

        # Invalid estimate basis
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis='INV',
                period=FiscalPeriod(2022, 1),
            )
        # Invalid report basis for actuals
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.ACTUAL,
                report_basis=EstimateBasis.NTM,
            )
        # Invalid metric for actuals
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.PRICE_TGT,
                statistic=EstimateStatistic.ACTUAL,
                report_basis=EstimateBasis.ANN,
            )

        # Get empty data response
        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_empty)
        with pytest.raises(MqValueError):
            tm.factset_estimates(
                mock_asset,
                metric=EstimateItem.EPS,
                statistic=EstimateStatistic.MEDIAN,
                report_basis=EstimateBasis.SEMI,
                period=FiscalPeriod(2022, 1),
            )

    replace.restore()


def test_factset_fundamentals():
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2024, 9, 30), end=dt.date(2024, 9, 30)):
        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_basic)

        actual = tm.factset_fundamentals(
            mock_asset,
            metric=FundamentalMetric.EPS_BASIC,
            report_basis=FundamentalBasis.ANN,
            report_format=FundamentalFormat.NON_RESTATED,
        )
        assert_series_equal(
            pd.Series(
                [6.109],
                index=pd.DatetimeIndex(['2024-09-30'], dtype='datetime64[ns]', name='date', freq=None),
                name=FundamentalMetric.EPS_BASIC.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FF_BASIC_AF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_basic_derived)

        actual = tm.factset_fundamentals(
            mock_asset,
            metric=FundamentalMetric.EBITDA_OPER,
            report_basis=FundamentalBasis.ANN,
            report_format=FundamentalFormat.NON_RESTATED,
        )
        assert_series_equal(
            pd.Series(
                [6.109],
                index=pd.DatetimeIndex(['2024-09-30'], dtype='datetime64[ns]', name='date', freq=None),
                name=FundamentalMetric.EBITDA_OPER.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FF_BASIC_DER_AF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_basic_restated)

        actual = tm.factset_fundamentals(
            mock_asset,
            metric=FundamentalMetric.EPS_BASIC,
            report_basis=FundamentalBasis.ANN,
            report_format=FundamentalFormat.RESTATED,
        )
        assert_series_equal(
            pd.Series(
                [6.109],
                index=pd.DatetimeIndex(['2024-09-30'], dtype='datetime64[ns]', name='date', freq=None),
                name=FundamentalMetric.EPS_BASIC.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FF_BASIC_R_AF_GLOBAL'

        # Get empty data response
        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_empty)
        with pytest.raises(MqValueError):
            tm.factset_fundamentals(
                mock_asset,
                metric=FundamentalMetric.EPS_BASIC,
                report_basis=FundamentalBasis.ANN,
                report_format=FundamentalFormat.RESTATED,
            )

    replace.restore()


def test_factset_ratings():
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2024, 9, 30), end=dt.date(2024, 9, 30)):
        replace('gs_quant.data.Dataset.get_data', mock_factset_ratings)

        actual = tm.factset_ratings(mock_asset, rating_type=RatingType.BUY)
        assert_series_equal(
            pd.Series(
                [21.0, 3.0, 3.0],
                index=pd.DatetimeIndex([dt.date(2024, 12, 31)] * 3, dtype='datetime64[ns]', name='date', freq=None),
                name=RatingType.BUY.value,
            ),
            pd.Series(actual),
        )
        assert actual.dataset_ids == 'FE_BASIC_CONH_REC_GLOBAL'

    replace.restore()


def test_fiscal_period():
    fp = FiscalPeriod.from_dict({'y': 2022, 'p': 1})
    assert fp.y == 2022
    assert fp.p == 1

    assert fp.as_dict() == {'y': 2022, 'p': 1}


# ---------- GIR Estimates helpers ----------


def _mock_gir_dataset_get_data(**kwargs):
    """Return a small DataFrame that looks like GIR_EQUITY_ANALYST_FORECASTS_V1 rows."""
    d = {
        'date': [kwargs.get('end', dt.date(2027, 1, 1))],
        'metricName': [kwargs.get('metricName', 'EPS')],
        'metricValueNumeric': [3.14],
        'periodType': [kwargs.get('periodType', 'A')],
        'bbid': [kwargs.get('bbid', 'AAPL UW')],
    }
    return MarketDataResponseFrame(data=d)


def _mock_gir_dataset_get_data_empty(**kwargs):
    return MarketDataResponseFrame()


def _mock_gir_dataset_get_data_null_numeric(**kwargs):
    d = {
        'date': [kwargs.get('end', dt.date(2027, 1, 1))],
        'metricName': [kwargs.get('metricName', 'EPS')],
        'metricValueNumeric': [None],
        'periodType': [kwargs.get('periodType', 'A')],
        'bbid': [kwargs.get('bbid', 'AAPL UW')],
    }
    return MarketDataResponseFrame(data=d)


def _mock_gir_dataset_get_data_old_date(**kwargs):
    """Return data whose date is BEFORE the relative_date so the filter removes it."""
    d = {
        'date': [dt.date(2020, 1, 1)],
        'metricName': [kwargs.get('metricName', 'EPS')],
        'metricValueNumeric': [3.14],
        'periodType': [kwargs.get('periodType', 'A')],
        'bbid': [kwargs.get('bbid', 'AAPL UW')],
    }
    return MarketDataResponseFrame(data=d)


def test_gir_estimates_invalid_basis():
    """Invalid report_basis raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2025, 3, 20), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Invalid Estimate Basis argument'):
            tm.gir_estimates(mock_asset, report_basis='INVALID')
    replace.restore()


def test_gir_estimates_invalid_period_type():
    """period must be int or FiscalPeriod."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2025, 3, 20), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Period must be an integer'):
            tm.gir_estimates(mock_asset, period='bad')
    replace.restore()


def test_gir_estimates_fiscal_period_no_year():
    """FiscalPeriod without year raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2025, 3, 20), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='year'):
            tm.gir_estimates(mock_asset, period=FiscalPeriod(None))
    replace.restore()


def test_gir_estimates_qtr_fiscal_period_no_quarter():
    """Quarterly basis with FiscalPeriod but no period number raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2025, 3, 20), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Please specify the period'):
            tm.gir_estimates(
                mock_asset,
                report_basis=GIREstimateBasis.QTR,
                period=FiscalPeriod(2025),
            )
    replace.restore()


def test_gir_estimates_qtr_fiscal_period_invalid_quarter():
    """Quarterly basis with period number outside 1-4 raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2025, 3, 20), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Period number has to be one of'):
            tm.gir_estimates(
                mock_asset,
                report_basis=GIREstimateBasis.QTR,
                period=FiscalPeriod(2025, 5),
            )
    replace.restore()


def test_gir_estimates_no_bbid():
    """Asset without Bloomberg ID raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = None
    with DataContext(start=dt.date(2025, 3, 20), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Could not resolve Bloomberg ID'):
            tm.gir_estimates(mock_asset)
    replace.restore()


def test_gir_estimates_rolling_annual():
    """Rolling (int) period with annual basis returns expected series."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    # Use a single-day range so only one task is created
    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [
                _mock_gir_dataset_get_data(
                    start=dt.date(2025, 3, 25),
                    metricName='EPS',
                    periodType='A',
                    bbid='AAPL UW',
                )
            ],
        )

        actual = tm.gir_estimates(
            mock_asset,
            metric=GIREstimateItem.EPS,
            report_basis=GIREstimateBasis.ANN,
            period=1,
        )
        assert actual.dataset_ids == 'GIR_EQUITY_ANALYST_FORECASTS_V1'
        assert len(actual) == 1
        assert actual.iloc[0] == 3.14

    replace.restore()


def test_gir_estimates_rolling_quarterly():
    """Rolling (int) period with quarterly basis returns expected series."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [
                _mock_gir_dataset_get_data(
                    start=dt.date(2025, 3, 25),
                    metricName='EPS',
                    periodType='Q',
                    bbid='AAPL UW',
                )
            ],
        )

        actual = tm.gir_estimates(
            mock_asset,
            metric=GIREstimateItem.EPS,
            report_basis=GIREstimateBasis.QTR,
            period=1,
        )
        assert actual.dataset_ids == 'GIR_EQUITY_ANALYST_FORECASTS_V1'
        assert len(actual) == 1

    replace.restore()


def test_gir_estimates_fixed_annual():
    """FiscalPeriod annual basis."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [
                _mock_gir_dataset_get_data(
                    start=dt.date(2025, 1, 1),
                    metricName='EPS',
                    periodType='A',
                    bbid='AAPL UW',
                )
            ],
        )

        actual = tm.gir_estimates(
            mock_asset,
            metric=GIREstimateItem.EPS,
            report_basis=GIREstimateBasis.ANN,
            period=FiscalPeriod(2025),
        )
        assert actual.dataset_ids == 'GIR_EQUITY_ANALYST_FORECASTS_V1'
        assert actual.name == GIREstimateItem.EPS.value

    replace.restore()


def test_gir_estimates_fixed_quarterly():
    """FiscalPeriod quarterly basis with valid quarter."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [
                _mock_gir_dataset_get_data(
                    start=dt.date(2025, 4, 1),
                    metricName='EPS',
                    periodType='Q',
                    bbid='AAPL UW',
                )
            ],
        )

        actual = tm.gir_estimates(
            mock_asset,
            metric=GIREstimateItem.EPS,
            report_basis=GIREstimateBasis.QTR,
            period=FiscalPeriod(2025, 2),
        )
        assert len(actual) == 1
        assert actual.iloc[0] == 3.14

    replace.restore()


def test_gir_estimates_empty_response():
    """Empty concatenated response raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [_mock_gir_dataset_get_data_empty()],
        )

        with pytest.raises(MqValueError, match='No data found'):
            tm.gir_estimates(mock_asset, period=1)

    replace.restore()


def test_gir_estimates_null_numeric():
    """All-null metricValueNumeric raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [_mock_gir_dataset_get_data_null_numeric()],
        )

        with pytest.raises(MqValueError, match='No numeric data found'):
            tm.gir_estimates(mock_asset, period=1)

    replace.restore()


def test_gir_estimates_null_numeric_fixed_period():
    """All-null metricValueNumeric in fixed period branch raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [_mock_gir_dataset_get_data_null_numeric()],
        )

        with pytest.raises(MqValueError, match='No numeric data found'):
            tm.gir_estimates(mock_asset, period=FiscalPeriod(2025))

    replace.restore()


def test_gir_estimates_empty_response_fixed_period():
    """Empty response in fixed FiscalPeriod branch raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [_mock_gir_dataset_get_data_empty()],
        )

        with pytest.raises(MqValueError, match='No data found'):
            tm.gir_estimates(mock_asset, period=FiscalPeriod(2025))

    replace.restore()


def test_gir_estimates_threadpool_exception():
    """ThreadPoolManager exception is wrapped in MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    def _raise(_cls, _tasks):
        raise RuntimeError('network error')

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace('gs_quant.api.utils.ThreadPoolManager.run_async', _raise)

        with pytest.raises(MqValueError, match='Could not query dataset'):
            tm.gir_estimates(mock_asset, period=1)

    replace.restore()


def test_gir_estimates_threadpool_exception_fixed():
    """ThreadPoolManager exception in fixed-period branch."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    def _raise(_cls, _tasks):
        raise RuntimeError('network error')

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace('gs_quant.api.utils.ThreadPoolManager.run_async', _raise)

        with pytest.raises(MqValueError, match='Could not query dataset'):
            tm.gir_estimates(mock_asset, period=FiscalPeriod(2025))

    replace.restore()


def test_gir_estimates_no_data_within_period():
    """Rolling period where data dates are before relative_date filter raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'

    with DataContext(start=dt.date(2025, 3, 25), end=dt.date(2025, 3, 25)):
        replace(
            'gs_quant.api.utils.ThreadPoolManager.run_async',
            lambda cls, tasks: [_mock_gir_dataset_get_data_old_date()],
        )

        with pytest.raises(MqValueError, match='No data found .* within the requested period'):
            tm.gir_estimates(mock_asset, period=1)

    replace.restore()


# ---------- factset_enterprise_value helpers ----------


def _mock_ev_capital_structure(_cls=None, **kwargs):
    d = {
        'mvPricingDate': [dt.date(2025, 3, 20)],
        'sharesOutstanding': [15_000_000_000.0],
        'marketCap': [3_500_000_000_000.0],
        'fullyDilutedSharesOutstanding': [15_500_000_000.0],
        'fullyDilutedMarketCap': [3_600_000_000_000.0],
        'consolidatedDebt': [100_000_000_000.0],
        'convertibleDebt': [5_000_000_000.0],
        'capLease': [10_000_000_000.0],
        'cashAndEquivalents': [60_000_000_000.0],
        'longTermMarketableSecurity': [20_000_000_000.0],
        'totalPreferred': [1_000_000_000.0],
        'convertiblePreferred': [500_000_000.0],
        'investmentInUnconsolidatedSubs': [2_000_000_000.0],
        'nonControllingInterest': [3_000_000_000.0],
        'pensionLiabilities': [4_000_000_000.0],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d, index=pd.DatetimeIndex([dt.date(2025, 3, 20)], name='date'))
    df.dataset_id = 'FACTSET_EQ_CAPITAL_STRUCTURE'
    return df


def _mock_ev_capital_structure_neg_pension(_cls=None, **kwargs):
    d = {
        'mvPricingDate': [dt.date(2025, 3, 20)],
        'sharesOutstanding': [15_000_000_000.0],
        'marketCap': [3_500_000_000_000.0],
        'fullyDilutedSharesOutstanding': [15_500_000_000.0],
        'fullyDilutedMarketCap': [3_600_000_000_000.0],
        'consolidatedDebt': [100_000_000_000.0],
        'convertibleDebt': [5_000_000_000.0],
        'capLease': [10_000_000_000.0],
        'cashAndEquivalents': [60_000_000_000.0],
        'longTermMarketableSecurity': [20_000_000_000.0],
        'totalPreferred': [1_000_000_000.0],
        'convertiblePreferred': [500_000_000.0],
        'investmentInUnconsolidatedSubs': [2_000_000_000.0],
        'nonControllingInterest': [3_000_000_000.0],
        'pensionLiabilities': [-5_000_000_000.0],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d, index=pd.DatetimeIndex([dt.date(2025, 3, 20)], name='date'))
    df.dataset_id = 'FACTSET_EQ_CAPITAL_STRUCTURE'
    return df


def _mock_ev_capital_structure_empty(_cls=None, **kwargs):
    df = MarketDataResponseFrame()
    df.dataset_id = 'FACTSET_EQ_CAPITAL_STRUCTURE'
    return df


def _mock_ev_fundamentals_with_lease(_cls=None, **kwargs):
    d = {
        'ffDebtOthCapl': [50_000_000.0],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d, index=pd.DatetimeIndex([dt.date(2025, 1, 1)], name='date'))
    df.dataset_id = 'FF_ADVANCED_AF_GLOBAL'
    return df


def _mock_ev_fundamentals_no_lease(_cls=None, **kwargs):
    d = {
        'ffDebtOthCapl': [0.0],
        'bbid': ['AAPL UW'],
    }
    df = MarketDataResponseFrame(data=d, index=pd.DatetimeIndex([dt.date(2025, 1, 1)], name='date'))
    df.dataset_id = 'FF_ADVANCED_AF_GLOBAL'
    return df


def _mock_ev_fundamentals_empty(_cls=None, **kwargs):
    df = MarketDataResponseFrame()
    df.dataset_id = 'FF_ADVANCED_AF_GLOBAL'
    return df


class _DatasetDispatcher:
    """Routes Dataset.get_data calls to different mocks based on the bbid kwarg."""

    def __init__(self, capital_mock, fund_mock):
        self._capital_mock = capital_mock
        self._fund_mock = fund_mock

    def __call__(self, *args, **kwargs):
        bbid = kwargs.get('bbid', '')
        # args[0] is the Dataset instance (self) when Replacer passes it
        _cls = args[0] if args else None
        if bbid == 'AAPL US':  # bcid for capital structure
            return self._capital_mock(_cls, **kwargs)
        else:
            return self._fund_mock(_cls, **kwargs)


def test_factset_ev_invalid_metric():
    """Non-EVItem metric raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Invalid EV metric'):
            tm.factset_enterprise_value(mock_asset, metric='bad')
    replace.restore()


def test_factset_ev_no_bbid():
    """Missing Bloomberg ID raises MqValueError."""
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = None
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Could not resolve Bloomberg ID'):
            tm.factset_enterprise_value(mock_asset)
    replace.restore()


def test_factset_ev_no_bcid():
    """Missing Bloomberg Composite ID raises MqValueError."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return None

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Could not resolve Bloomberg Composite ID'):
            tm.factset_enterprise_value(mock_asset)
    replace.restore()


def test_factset_ev_empty_capital_structure():
    """Empty capital structure dataset raises MqValueError."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    replace('gs_quant.data.Dataset.get_data', _mock_ev_capital_structure_empty)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='No data found'):
            tm.factset_enterprise_value(mock_asset)
    replace.restore()


def test_factset_ev_success_with_lease():
    """Full EV calculation with operating leases included."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    dispatcher = _DatasetDispatcher(_mock_ev_capital_structure, _mock_ev_fundamentals_with_lease)
    replace('gs_quant.data.Dataset.get_data', dispatcher)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        actual = tm.factset_enterprise_value(mock_asset, metric=EVItem.ENTERPRISE_VALUE)
        assert len(actual) == 1
        assert actual.name == EVItem.ENTERPRISE_VALUE.value
        # EV = fullyDilutedMarketCap + consolidatedDebt - convertibleDebt + capLease
        #      - cashAndEquivalents - longTermMarketableSecurity + totalPreferred
        #      - convertiblePreferred - investmentInUnconsolidatedSubs + nonControllingInterest
        #      + pensionLiabilities
        expected_ev = (
            3_600_000_000_000.0
            + 100_000_000_000.0
            - 5_000_000_000.0
            + 10_000_000_000.0
            - 60_000_000_000.0
            - 20_000_000_000.0
            + 1_000_000_000.0
            - 500_000_000.0
            - 2_000_000_000.0
            + 3_000_000_000.0
            + 4_000_000_000.0
        )
        assert actual.iloc[0] == expected_ev

    replace.restore()


def test_factset_ev_success_no_lease():
    """EV calculation with op_lease = False (capLease set to 0)."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    dispatcher = _DatasetDispatcher(_mock_ev_capital_structure, _mock_ev_fundamentals_empty)
    replace('gs_quant.data.Dataset.get_data', dispatcher)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        actual = tm.factset_enterprise_value(mock_asset, metric=EVItem.ENTERPRISE_VALUE)
        # capLease should be 0 now
        expected_ev = (
            3_600_000_000_000.0
            + 100_000_000_000.0
            - 5_000_000_000.0
            + 0
            - 60_000_000_000.0
            - 20_000_000_000.0
            + 1_000_000_000.0
            - 500_000_000.0
            - 2_000_000_000.0
            + 3_000_000_000.0
            + 4_000_000_000.0
        )
        assert actual.iloc[0] == expected_ev

    replace.restore()


def test_factset_ev_negative_pension():
    """Negative pension liabilities are clipped to 0."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    dispatcher = _DatasetDispatcher(_mock_ev_capital_structure_neg_pension, _mock_ev_fundamentals_with_lease)
    replace('gs_quant.data.Dataset.get_data', dispatcher)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        actual = tm.factset_enterprise_value(mock_asset, metric=EVItem.ENTERPRISE_VALUE)
        # pension clipped to 0 because original value is -5B
        expected_ev = (
            3_600_000_000_000.0
            + 100_000_000_000.0
            - 5_000_000_000.0
            + 10_000_000_000.0
            - 60_000_000_000.0
            - 20_000_000_000.0
            + 1_000_000_000.0
            - 500_000_000.0
            - 2_000_000_000.0
            + 3_000_000_000.0
            + 0
        )
        assert actual.iloc[0] == expected_ev

    replace.restore()


def test_factset_ev_market_cap_metric():
    """Request a non-EV metric (MARKET_CAP)."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    dispatcher = _DatasetDispatcher(_mock_ev_capital_structure, _mock_ev_fundamentals_empty)
    replace('gs_quant.data.Dataset.get_data', dispatcher)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        actual = tm.factset_enterprise_value(mock_asset, metric=EVItem.MARKET_CAP)
        assert actual.iloc[0] == 3_500_000_000_000.0
        assert actual.name == EVItem.MARKET_CAP.value

    replace.restore()


def test_factset_ev_capital_structure_exception():
    """Exception querying capital structure dataset raises MqValueError."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))

    def _raise(*args, **kwargs):
        raise RuntimeError('connection error')

    replace('gs_quant.data.Dataset.get_data', _raise)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Could not query dataset'):
            tm.factset_enterprise_value(mock_asset)
    replace.restore()


def test_factset_ev_fundamentals_exception():
    """Exception querying fundamentals dataset raises MqValueError."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))

    call_count = [0]

    def _dispatch(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return _mock_ev_capital_structure(None, **kwargs)
        raise RuntimeError('fund error')

    replace('gs_quant.data.Dataset.get_data', _dispatch)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        with pytest.raises(MqValueError, match='Could not query dataset'):
            tm.factset_enterprise_value(mock_asset)
    replace.restore()


def test_factset_ev_no_lease_column():
    """Fundamentals data with ffDebtOthCapl = 0 means no lease."""
    replace = Replacer()

    def _side_effect(identifier):
        from gs_quant.markets.securities import AssetIdentifier

        if identifier == AssetIdentifier.BLOOMBERG_ID:
            return 'AAPL UW'
        return 'AAPL US'

    replace('gs_quant.markets.securities.Asset.get_identifier', Mock(side_effect=_side_effect))
    dispatcher = _DatasetDispatcher(_mock_ev_capital_structure, _mock_ev_fundamentals_no_lease)
    replace('gs_quant.data.Dataset.get_data', dispatcher)
    with DataContext(start=dt.date(2025, 3, 1), end=dt.date(2025, 3, 25)):
        actual = tm.factset_enterprise_value(mock_asset, metric=EVItem.ENTERPRISE_VALUE)
        # capLease should be 0 when ffDebtOthCapl <= 0
        expected_ev = (
            3_600_000_000_000.0
            + 100_000_000_000.0
            - 5_000_000_000.0
            + 0
            - 60_000_000_000.0
            - 20_000_000_000.0
            + 1_000_000_000.0
            - 500_000_000.0
            - 2_000_000_000.0
            + 3_000_000_000.0
            + 4_000_000_000.0
        )
        assert actual.iloc[0] == expected_ev

    replace.restore()


if __name__ == '__main__':
    pytest.main(args=["test_measures_factset.py"])
