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
from unittest.mock import ANY

import pytest
from unittest import mock

from gs_quant.session import GsSession, Environment

from gs_quant.models.risk_model_utils import _upload_factor_data_if_present


@pytest.mark.parametrize('total_factors', [100])
def test__upload_factor_data_if_present(mocker, total_factors: int):

    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')

    date = "2024-03-28"
    factor_data = [{'factorCategory': '1', 'factorName': f'Factor {i + 1}', 'factorCategoryId': 'z',
                    'factorReturn': 0.001 * (i + 1)} for i in range(total_factors)]

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

    mocker.patch.object(GsSession.current, '_post', return_value='success', side_effect=match_dictionaries)

    _upload_factor_data_if_present('TEST_RISK_MODEL', risk_model_data, date)
    GsSession.current._post.assert_called_with('/risk/models/data/TEST_RISK_MODEL?partialUpload=true', ANY, timeout=200)

    _upload_factor_data_if_present('TEST_RISK_MODEL', risk_model_data, date, aws_upload=True)
    GsSession.current._post.assert_called_with('/risk/models/data/TEST_RISK_MODEL?partialUpload=true&awsUpload=true',
                                               ANY, timeout=200)
