"""
Copyright 2025 Goldman Sachs.
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

from unittest.mock import patch, MagicMock

from gs_quant.api.gs.data import GsDataApi
from gs_quant.tracing import Tracer


def test_execute_query_creates_span():
    Tracer.reset()
    mock_query = MagicMock()
    mock_query.format = None

    with patch.object(GsDataApi, "_check_data_on_cloud", return_value=None):
        with patch.object(GsDataApi, "_post_with_cache_check", return_value={"data": []}):
            GsDataApi.execute_query("MY_DATASET", mock_query)

    spans = Tracer.get_spans()
    matching = [s for s in spans if "GsDataApi.execute_query/MY_DATASET" == s.operation_name]
    assert len(matching) == 1
    assert matching[0].tags.get("dataset_id") == "MY_DATASET"
    Tracer.reset()


def test_get_market_data_creates_span():
    Tracer.reset()
    mock_body = {
        "requestId": "req-456",
        "responses": [
            {
                "queryResponse": [
                    {
                        "dataSetIds": ["DS1"],
                        "response": {"data": [{"date": "2021-01-01", "value": 1.0}]},
                    }
                ]
            }
        ],
    }

    with patch.object(GsDataApi, "_post_with_cache_check", return_value=mock_body):
        GsDataApi.get_market_data(query={"q": "test"})

    spans = Tracer.get_spans()
    matching = [s for s in spans if "GsDataApi.get_market_data" == s.operation_name]
    assert len(matching) == 1
    assert matching[0].tags.get("request_id") == "req-456"
    assert matching[0].tags.get("dataset_ids") == "['DS1']"
    Tracer.reset()
