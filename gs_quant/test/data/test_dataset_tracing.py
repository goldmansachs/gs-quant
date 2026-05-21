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

from unittest.mock import MagicMock

import pandas as pd

from gs_quant.data.dataset import Dataset
from gs_quant.tracing import Tracer


def test_dataset_get_data_creates_span():
    Tracer.reset()
    mock_provider = MagicMock()
    mock_provider.query_data.return_value = [{"date": "2021-01-01", "value": 1.0}]
    mock_provider.construct_dataframe_with_types.return_value = pd.DataFrame({"value": [1.0]})
    mock_provider.build_query.return_value = (MagicMock(), False)

    ds = Dataset("TEST_DATASET", provider=mock_provider)
    ds.get_data()

    spans = Tracer.get_spans()
    matching = [s for s in spans if "Dataset.get_data/TEST_DATASET" == s.operation_name]
    assert len(matching) == 1
    assert matching[0].tags.get("dataset_id") == "TEST_DATASET"
    assert matching[0].tags.get("row_count") == 1
    Tracer.reset()
