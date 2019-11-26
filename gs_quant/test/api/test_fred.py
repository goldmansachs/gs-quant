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

This product uses the FRED® API but is not endorsed or certified
by the Federal Reserve Bank of St. Louis. FRED terms of use
available at https://research.stlouisfed.org/docs/api/terms_of_use.html
"""

import pandas as pd
import pytest
from pandas.util.testing import assert_frame_equal, assert_series_equal

from gs_quant.data import Dataset
from gs_quant.api.fred.data import FredDataApi

from unittest.mock import Mock

fredAPI = FredDataApi(api_key='')
fred_data = Dataset('GDP', fredAPI)

GDP_data = {
    'realtime_start': '2019-10-25',
    'realtime_end': '2019-10-25',
    'observation_start': '1600-01-01',
    'observation_end': '9999-12-31',
    'units': 'lin', 'output_type': 1,
    'file_type': 'json',
    'order_by': 'observation_date',
    'sort_order': 'asc',
    'count': 294,
    'offset': 0,
    'limit': 20,
    'observations': [
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1946-01-01', 'value': '.'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1946-04-01', 'value': '.'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1946-07-01', 'value': '.'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1946-10-01', 'value': '.'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1947-01-01', 'value': '243.164'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1947-04-01', 'value': '245.968'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1947-07-01', 'value': '249.585'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1947-10-01', 'value': '259.745'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1948-01-01', 'value': '265.742'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1948-04-01', 'value': '272.567'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1948-07-01', 'value': '279.196'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1948-10-01', 'value': '280.366'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1949-01-01', 'value': '275.034'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1949-04-01', 'value': '271.351'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1949-07-01', 'value': '272.889'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1949-10-01', 'value': '270.627'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1950-01-01', 'value': '280.828'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1950-04-01', 'value': '290.383'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1950-07-01', 'value': '308.153'},
        {'realtime_start': '2019-10-25', 'realtime_end': '2019-10-25', 'date': '1950-10-01', 'value': '319.945'}
    ]
}


def _mock_requests_response(status=200, content='', json_data=None, raise_for_status=None):
    """ Helper function to build mock requests responses."""
    mock_resp = Mock()
    mock_resp.status_code = status
    mock_resp.content = content
    mock_resp.raise_for_status = Mock()

    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status

    if json_data:
        mock_resp.json = Mock(return_value=json_data)

    return mock_resp


def test_get_data(mocker):
    mocker.patch('requests.get', return_value=_mock_requests_response(json_data=GDP_data))
    result = fred_data.get_data()

    expected_result = pd.DataFrame(GDP_data['observations'])[['date', 'value']]
    expected_result = expected_result[expected_result.value != '.']
    expected_result['date'] = pd.to_datetime(expected_result['date'])
    expected_result['value'] = expected_result['value'].astype(float)
    expected_result = expected_result.set_index('date')['value']
    expected_result = expected_result.sort_index()
    expected_result.name = 'GDP'
    assert_frame_equal(result, expected_result.to_frame())


def test_failed_get_data(mocker):
    """test case where FRED API is down"""
    mocker.patch('requests.get', side_effect=ValueError(_mock_requests_response(status=404)))
    with pytest.raises(ValueError):
        fred_data.get_data()


def test_get_data_series(mocker):
    mocker.patch('requests.get', return_value=_mock_requests_response(json_data=GDP_data))
    result = fred_data.get_data_series(field='GDP')

    expected_result = pd.DataFrame(GDP_data['observations'])[['date', 'value']]
    expected_result = expected_result[expected_result.value != '.']
    expected_result['date'] = pd.to_datetime(expected_result['date'])
    expected_result['value'] = expected_result['value'].astype(float)
    expected_result = expected_result.set_index('date')['value']
    expected_result = expected_result.sort_index()
    expected_result.name = None

    assert_series_equal(result, expected_result)


def test_failed_get_data_series(mocker):
    """test case where FRED API is down"""
    mocker.patch('requests.get', side_effect=ValueError(_mock_requests_response(status=404)))
    with pytest.raises(ValueError):
        fred_data.get_data_series(field='GDP')
