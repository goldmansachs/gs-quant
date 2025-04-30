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
import datetime
from unittest.mock import Mock

import pandas as pd
import pytest
from pandas import DatetimeIndex, Timestamp
from pandas.testing import assert_series_equal
from testfixtures import Replacer

import gs_quant.timeseries.measures_factset as tm
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.index import Index
from gs_quant.timeseries.measures_factset import (EstimateItem, EstimateStatistic, EstimateBasis, FiscalPeriod,
                                                  FundamentalMetric, FundamentalFormat, FundamentalBasis, RatingType)

_index = [pd.Timestamp('2021-03-30')]
_test_datasets = ('TEST_DATASET',)


def mock_fe_estimate_af(_cls, bbid, start, end, feItem):
    d = {
        'date': [
            datetime.date(2022, 1, 8),
            datetime.date(2022, 1, 12),
            datetime.date(2022, 1, 13)
        ],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'fePerRel': [1.0] * 3,
        'adjDate': [datetime.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'consEndDate': [datetime.date(2022, 1, 11)] * 3,
        'feItemDesc': ['Earnings Per Share'] * 3,
        'feFpEnd': [datetime.date(2022, 9, 30)] * 3,
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
        'date': [
            datetime.date(2022, 1, 8),
            datetime.date(2022, 1, 12),
            datetime.date(2022, 1, 13)
        ],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'fePerRel': [1.0] * 3,
        'adjDate': [datetime.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'consEndDate': [datetime.date(2022, 1, 11)] * 3,
        'feItemDesc': ['Earnings Per Share'] * 3,
        'feFpEnd': [datetime.date(2022, 9, 30)] * 3,
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
        'date': [
            datetime.date(2022, 1, 8),
            datetime.date(2022, 1, 12),
            datetime.date(2022, 1, 13)
        ],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'fePerRel': [1.0] * 3,
        'adjDate': [datetime.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'consEndDate': [datetime.date(2022, 1, 11)] * 3,
        'feItemDesc': ['Earnings Per Share'] * 3,
        'feFpEnd': [datetime.date(2022, 9, 30)] * 3,
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
        'date': [
            datetime.date(2022, 1, 8),
            datetime.date(2022, 1, 9),
            datetime.date(2022, 1, 10)
        ],
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
        'date': [
            datetime.date(2022, 1, 8),
            datetime.date(2022, 1, 12),
            datetime.date(2022, 1, 13)
        ],
        'isin': ['US0378331005'] * 3,
        'feItem': ['PRICE_TGT'] * 3,
        'adjDate': [datetime.date(2020, 8, 31)] * 3,
        'consEndDate': [datetime.date(2022, 1, 11)] * 3,
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
        'date': [
            datetime.date(2020, 1, 8),
            datetime.date(2021, 1, 12),
            datetime.date(2022, 1, 13)
        ],
        'isin': ['US0378331005'] * 3,
        'feItem': ['EPS'] * 3,
        'adjDate': [datetime.date(2020, 8, 31)] * 3,
        'currency': ['USD'] * 3,
        'feFpEnd': [datetime.date(2022, 9, 30),
                    datetime.date(2021, 9, 30),
                    datetime.date(2020, 9, 30)
                    ],
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
        'date': [Timestamp('2024-09-30 00:00:00')],
        'isin': ['US0378331005'],
        'adjDate': [Timestamp('2020-08-31 00:00:00')],
        'currency': ['USD'],
        'ffEpsBasic': [6.109],
        'fsymId': ['MH33D6-R'],
        'bbid': ['AAPL UW']
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FF_BASIC_AF_GLOBAL'
    return df


def mock_factset_fundamentals_basic_derived(_cls, bbid, start, end):
    d = {
        'date': [Timestamp('2024-09-30 00:00:00')],
        'isin': ['US0378331005'],
        'adjDate': [Timestamp('2020-08-31 00:00:00')],
        'currency': ['USD'],
        'ffEbitdaOper': [6.109],
        'fsymId': ['MH33D6-R'],
        'bbid': ['AAPL UW']
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FF_BASIC_DER_AF_GLOBAL'
    return df


def mock_factset_fundamentals_basic_restated(_cls, bbid, start, end):
    d = {
        'date': [Timestamp('2024-09-30 00:00:00')],
        'isin': ['US0378331005'],
        'adjDate': [Timestamp('2020-08-31 00:00:00')],
        'currency': ['USD'],
        'ffEpsBasic': [6.109],
        'fsymId': ['MH33D6-R'],
        'bbid': ['AAPL UW']
    }
    df = MarketDataResponseFrame(data=d)
    df.dataset_id = 'FF_BASIC_R_AF_GLOBAL'
    return df


def mock_factset_ratings(_cls, bbid, start, end):
    d = {
        'date': [Timestamp('2024-12-31 00:00:00')] * 3,
        'isin': ['US0378331005'] * 3,
        'feItem': ['REC'] * 3,
        'adjDate': [datetime.date(2024, 12, 31)] * 3,
        'consEndDate': [datetime.date(2024, 12, 31)] * 3,
        'feItemDesc': ['Recommendation'] * 3,
        'feFpEnd': [datetime.date(2024, 12, 31)] * 3,
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
    with DataContext(start=datetime.date(2022, 1, 1),
                     end=datetime.date(2025, 1, 31)):
        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_af)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.MEDIAN,
                                      report_basis=EstimateBasis.ANN,
                                      period=FiscalPeriod(2022),
                                      )
        assert_series_equal(pd.Series([5.745] * 4,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_CONH_AF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_qf)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.MEDIAN,
                                      report_basis=EstimateBasis.QTR,
                                      period=FiscalPeriod(2022, 3),
                                      )
        assert_series_equal(pd.Series([5.745] * 4,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_CONH_QF_GLOBAL'

        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.QTR,
                                 period=FiscalPeriod(2022, 1)
                                 )

        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.QTR,
                                 period=FiscalPeriod(2022, -1)
                                 )

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_saf)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.MEDIAN,
                                      report_basis=EstimateBasis.SEMI,
                                      period=FiscalPeriod(2022, 2),
                                      )
        assert_series_equal(pd.Series([5.745] * 4,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_CONH_SAF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_ntm)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.MEDIAN,
                                      report_basis=EstimateBasis.NTM
                                      )
        assert_series_equal(pd.Series([5.745] * 3,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_NTM'

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.MEDIAN,
                                      report_basis=EstimateBasis.STM
                                      )
        assert_series_equal(pd.Series([5.745] * 3,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_NTM'

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_lt)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.PRICE_TGT,
                                      statistic=EstimateStatistic.MEDIAN
                                      )
        assert_series_equal(pd.Series([5.745] * 4,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_CONH_LT_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_fe_actual)

        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.ACTUAL,
                                      report_basis=EstimateBasis.ANN
                                      )
        assert_series_equal(pd.Series([15.0],
                                      index=DatetimeIndex(['2022-09-30'], dtype='datetime64[ns]', name='date',
                                                          freq=None),
                                      name=EstimateStatistic.ACTUAL.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_ACT_AF_GLOBAL'

        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.SEMI,
                                 period=FiscalPeriod(2022)
                                 )
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.SEMI,
                                 period=FiscalPeriod(2022, -1)
                                 )

        replace('gs_quant.data.Dataset.get_data', None)
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.SEMI,
                                 period=FiscalPeriod(2022, 1)
                                 )

        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_af)
        actual = tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                      statistic=EstimateStatistic.MEDIAN,
                                      report_basis=EstimateBasis.ANN,
                                      period=1,
                                      )
        assert_series_equal(pd.Series([5.745] * 4,
                                      index=DatetimeIndex(['2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=EstimateStatistic.MEDIAN.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_CONH_AF_GLOBAL'

        # Get quarterly data without specifying period
        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_qf)
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.QTR,
                                 period=FiscalPeriod(2022),
                                 )

        # Invalid estimate basis
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis='INV',
                                 period=FiscalPeriod(2022, 1),
                                 )
        # Invalid report basis for actuals
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.ACTUAL,
                                 report_basis=EstimateBasis.NTM,
                                 )
        # Invalid metric for actuals
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.PRICE_TGT,
                                 statistic=EstimateStatistic.ACTUAL,
                                 report_basis=EstimateBasis.ANN,
                                 )

        # Get empty data response
        replace('gs_quant.data.Dataset.get_data', mock_fe_estimate_empty)
        with pytest.raises(MqValueError):
            tm.factset_estimates(mock_asset, metric=EstimateItem.EPS,
                                 statistic=EstimateStatistic.MEDIAN,
                                 report_basis=EstimateBasis.SEMI,
                                 period=FiscalPeriod(2022, 1),
                                 )

    replace.restore()


def test_factset_fundamentals():
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=datetime.date(2024, 9, 30),
                     end=datetime.date(2024, 9, 30)):
        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_basic)

        actual = tm.factset_fundamentals(mock_asset, metric=FundamentalMetric.EPS_BASIC,
                                         report_basis=FundamentalBasis.ANN,
                                         report_format=FundamentalFormat.NON_RESTATED
                                         )
        assert_series_equal(pd.Series([6.109],
                                      index=DatetimeIndex(['2024-09-30'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=FundamentalMetric.EPS_BASIC.value), pd.Series(actual))
        assert actual.dataset_ids == 'FF_BASIC_AF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_basic_derived)

        actual = tm.factset_fundamentals(mock_asset, metric=FundamentalMetric.EBITDA_OPER,
                                         report_basis=FundamentalBasis.ANN,
                                         report_format=FundamentalFormat.NON_RESTATED
                                         )
        assert_series_equal(pd.Series([6.109],
                                      index=DatetimeIndex(['2024-09-30'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=FundamentalMetric.EBITDA_OPER.value), pd.Series(actual))
        assert actual.dataset_ids == 'FF_BASIC_DER_AF_GLOBAL'

        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_basic_restated)

        actual = tm.factset_fundamentals(mock_asset, metric=FundamentalMetric.EPS_BASIC,
                                         report_basis=FundamentalBasis.ANN,
                                         report_format=FundamentalFormat.RESTATED
                                         )
        assert_series_equal(pd.Series([6.109],
                                      index=DatetimeIndex(['2024-09-30'],
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=FundamentalMetric.EPS_BASIC.value), pd.Series(actual))
        assert actual.dataset_ids == 'FF_BASIC_R_AF_GLOBAL'

        # Get empty data response
        replace('gs_quant.data.Dataset.get_data', mock_factset_fundamentals_empty)
        with pytest.raises(MqValueError):
            tm.factset_fundamentals(mock_asset, metric=FundamentalMetric.EPS_BASIC,
                                    report_basis=FundamentalBasis.ANN,
                                    report_format=FundamentalFormat.RESTATED
                                    )

    replace.restore()


def test_factset_ratings():
    replace = Replacer()
    bbid_mock = replace('gs_quant.markets.securities.Asset.get_identifier', Mock())
    bbid_mock.return_value = 'AAPL UW'
    with DataContext(start=datetime.date(2024, 9, 30),
                     end=datetime.date(2024, 9, 30)):
        replace('gs_quant.data.Dataset.get_data', mock_factset_ratings)

        actual = tm.factset_ratings(mock_asset, rating_type=RatingType.BUY)
        assert_series_equal(pd.Series([21.0, 3.0, 3.0],
                                      index=DatetimeIndex([datetime.date(2024, 12, 31)] * 3,
                                                          dtype='datetime64[ns]', name='date', freq=None),
                                      name=RatingType.BUY.value), pd.Series(actual))
        assert actual.dataset_ids == 'FE_BASIC_CONH_REC_GLOBAL'

    replace.restore()


def test_fiscal_period():
    fp = FiscalPeriod.from_dict({'y': 2022, 'p': 1})
    assert fp.y == 2022
    assert fp.p == 1

    assert fp.as_dict() == {'y': 2022, 'p': 1}


if __name__ == '__main__':
    pytest.main(args=["test_measures_factset.py"])
