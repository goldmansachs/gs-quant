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

import pandas as pd
import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

from gs_quant.markets.report import PerformanceReport
from gs_quant.target.reports import Report, ReportParameters
import gs_quant.timeseries.measures_portfolios as mp
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data.core import DataContext


def test_financial_conditions_index():
    data = {
        'pnl': [
            101,
            102,
            103
        ],
        'date': [
            '2020-01-01',
            '2020-01-02',
            '2020-01-03'
        ]
    }
    idx = pd.date_range('2020-01-01', freq='D', periods=3)
    df = MarketDataResponseFrame(data=data, index=idx)
    df.dataset_ids = ('PNL',)
    replace = Replacer()

    # mock PerformanceReport.get_pnl()
    mock = replace('gs_quant.markets.report.PerformanceReport.get_pnl', Mock())
    mock.return_value = df

    # mock GsPortfolioApi.get_reports()
    mock = replace('gs_quant.api.gs.portfolios.GsPortfolioApi.get_reports', Mock())
    mock.return_value = [Report.from_dict({'id': 'RP1', 'positionSourceType': 'Portfolio', 'positionSourceId': 'MP1',
                                           'type': 'Portfolio Performance Analytics',
                                           'parameters': {'transactionCostModel': 'FIXED'}})]

    # mock PerformanceReport.get()
    mock = replace('gs_quant.markets.report.PerformanceReport.get', Mock())
    mock.return_value = PerformanceReport(report_id='RP1',
                                          position_source_type='Portfolio',
                                          position_source_id='MP1',
                                          report_type='Portfolio Performance Analytics',
                                          parameters=ReportParameters(transaction_cost_model='FIXED'))

    with DataContext(datetime.date(2020, 1, 1), datetime.date(2019, 1, 3)):
        actual = mp.portfolio_pnl('MP1')
        assert actual.index.equals(idx)
        assert all(actual.values == data['pnl'])
    replace.restore()


if __name__ == '__main__':
    pytest.main(args=[__file__])
