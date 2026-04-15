"""
Copyright 2021 Goldman Sachs.
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
from unittest.mock import ANY

import pytest
from unittest import mock

from gs_quant.session import GsSession, Environment

from gs_quant.models.risk_model_utils import _upload_factor_data_if_present, get_closest_date_index


@pytest.mark.parametrize('total_factors', [100])
def test__upload_factor_data_if_present(mocker, total_factors: int):
    from gs_quant.session import OAuth2Session

    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')

    date = "2024-03-28"
    factor_data = [
        {
            'factorCategory': '1',
            'factorName': f'Factor {i + 1}',
            'factorCategoryId': 'z',
            'factorReturn': 0.001 * (i + 1),
        }
        for i in range(total_factors)
    ]

    covariance_matrix = [[0 for i in range(total_factors)] for j in range(total_factors)]
    pre_vra_covariance_matrix = [[0 for i in range(total_factors)] for j in range(total_factors)]
    unadjusted_covariance_matrix = [[0 for i in range(total_factors)] for j in range(total_factors)]

    risk_model_data = {
        "factorData": factor_data,
        "covarianceMatrix": covariance_matrix,
        "preVRACovarianceMatrix": pre_vra_covariance_matrix,
        "unadjustedCovarianceMatrix": unadjusted_covariance_matrix,
    }

    # Ensuring GsSession._post receives the values that we pass to _upload_factor_data_if_present method
    def match_dictionaries(*args, **kwargs):
        url = args[0]
        actual_data = args[1]

        for key in risk_model_data:
            if key in ['preVRACovarianceMatrix', 'unadjustedCovarianceMatrix'] and 'awsUpload' not in url:
                # making sure new covariance matrices are only uploaded to AWS
                assert key not in actual_data
                continue
            assert key in actual_data
            assert risk_model_data[key] == actual_data[key]

    mocker.patch.object(GsSession.current.sync, 'post', return_value='success', side_effect=match_dictionaries)

    _upload_factor_data_if_present('TEST_RISK_MODEL', risk_model_data, date)
    GsSession.current.sync.post.assert_called_with(
        '/risk/models/data/TEST_RISK_MODEL?partialUpload=true', ANY, timeout=200
    )

    _upload_factor_data_if_present('TEST_RISK_MODEL', risk_model_data, date, aws_upload=True)
    GsSession.current.sync.post.assert_called_with(
        '/risk/models/data/TEST_RISK_MODEL?partialUpload=true&awsUpload=true', ANY, timeout=200
    )


class TestGetClosestDateIndex:
    """Tests for get_closest_date_index covering both str and dt.date date lists."""

    # Helper to build date lists in both formats
    STR_DATES = ['2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-08']
    DATE_DATES = [
        dt.date(2024, 1, 2),
        dt.date(2024, 1, 3),
        dt.date(2024, 1, 4),
        dt.date(2024, 1, 5),
        dt.date(2024, 1, 8),
    ]

    # --- Exact match (parametrized over both list types) ---

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    @pytest.mark.parametrize('direction', ['after', 'before'])
    def test_exact_match(self, dates, direction):
        assert get_closest_date_index(dt.date(2024, 1, 3), dates, direction) == 1

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    def test_exact_match_first_element(self, dates):
        assert get_closest_date_index(dt.date(2024, 1, 2), dates, 'after') == 0

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    def test_exact_match_last_element(self, dates):
        assert get_closest_date_index(dt.date(2024, 1, 8), dates, 'before') == 4

    # --- Direction: 'after' scans forward to find the nearest date ---

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    def test_after_skips_weekend(self, dates):
        # Saturday Jan 6 should find Monday Jan 8 (index 4)
        assert get_closest_date_index(dt.date(2024, 1, 6), dates, 'after') == 4

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    def test_after_skips_one_day(self, dates):
        # Jan 1 (not in list) should find Jan 2 (index 0)
        assert get_closest_date_index(dt.date(2024, 1, 1), dates, 'after') == 0

    # --- Direction: 'before' scans backward to find the nearest date ---

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    def test_before_skips_weekend(self, dates):
        # Sunday Jan 7 should find Friday Jan 5 (index 3)
        assert get_closest_date_index(dt.date(2024, 1, 7), dates, 'before') == 3

    @pytest.mark.parametrize('dates', [STR_DATES, DATE_DATES], ids=['str_dates', 'date_dates'])
    def test_before_skips_one_day(self, dates):
        # Jan 9 (not in list) should find Jan 8 (index 4)
        assert get_closest_date_index(dt.date(2024, 1, 9), dates, 'before') == 4

    # --- No match within 50-day scan window ---

    @pytest.mark.parametrize('dates', [['2024-06-01'], [dt.date(2024, 6, 1)]], ids=['str_dates', 'date_dates'])
    def test_no_match_after_returns_negative_one(self, dates):
        assert get_closest_date_index(dt.date(2024, 1, 1), dates, 'after') == -1

    @pytest.mark.parametrize('dates', [['2024-06-01'], [dt.date(2024, 6, 1)]], ids=['str_dates', 'date_dates'])
    def test_no_match_before_returns_negative_one(self, dates):
        assert get_closest_date_index(dt.date(2024, 1, 1), dates, 'before') == -1

    # --- Single element list ---

    @pytest.mark.parametrize('dates', [['2024-03-15'], [dt.date(2024, 3, 15)]], ids=['str_dates', 'date_dates'])
    def test_single_element_exact_match(self, dates):
        assert get_closest_date_index(dt.date(2024, 3, 15), dates, 'after') == 0
        assert get_closest_date_index(dt.date(2024, 3, 15), dates, 'before') == 0

    # --- Regression: the original reported bug ---

    def test_regression_date_objects_not_empty(self):
        """The original bug: calendar.business_dates contained dt.date objects,
        but the old code converted the search date to a string via strftime and
        compared str == dt.date, which is always False — returning -1 and
        producing an empty calendar slice."""
        calendar_dates = [dt.date(2024, 1, 1), dt.date(2024, 1, 2), dt.date(2024, 1, 3)]
        start_idx = get_closest_date_index(dt.date(2024, 1, 1), calendar_dates, 'after')
        end_idx = get_closest_date_index(dt.date(2024, 1, 3), calendar_dates, 'before')
        assert start_idx == 0
        assert end_idx == 2
        assert calendar_dates[start_idx : end_idx + 1] == calendar_dates

    def test_regression_string_dates_still_work(self):
        """Ensure the legacy path (str dates) continues to work after the fix."""
        calendar_dates = ['2024-01-01', '2024-01-02', '2024-01-03']
        start_idx = get_closest_date_index(dt.date(2024, 1, 1), calendar_dates, 'after')
        end_idx = get_closest_date_index(dt.date(2024, 1, 3), calendar_dates, 'before')
        assert start_idx == 0
        assert end_idx == 2
        assert calendar_dates[start_idx : end_idx + 1] == calendar_dates

    def test_regression_tuple_dates_work(self):
        calendar_dates = tuple([dt.date(2024, 1, 1), dt.date(2024, 1, 2), dt.date(2024, 1, 3)])
        start_idx = get_closest_date_index(dt.date(2024, 1, 1), calendar_dates, 'after')
        end_idx = get_closest_date_index(dt.date(2024, 1, 3), calendar_dates, 'before')
        assert start_idx == 0
        assert end_idx == 2
        assert calendar_dates[start_idx : end_idx + 1] == calendar_dates
