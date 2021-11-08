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

import numpy as np
import pytest

from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.analytics.datagrid import DataGrid, DataColumn
from gs_quant.analytics.datagrid.data_cell import DataCell
from gs_quant.analytics.datagrid.utils import SortOrder, DataGridSort, DataGridFilter, FilterOperation, FilterCondition
from gs_quant.test.utils.datagrid_test_utils import get_test_entity


class TestSortingAndFiltering:
    def get_test_entities(self):
        spx = get_test_entity('MA4B66MW5E27U8P32SB')
        aapl = get_test_entity('MARCRZHY163GQ4H3')
        amzn = get_test_entity('MASGTFZYNA7PMQ3H')
        return spx, aapl, amzn

    def get_test_datagrid(self):
        spx, aapl, amzn = self.get_test_entities()
        datagrid = DataGrid('Test DataGrid', rows=[], columns=[DataColumn('Name', None), DataColumn('Value', None)])

        results = [
            [DataCell('Name', None, None, None, 0, 0), DataCell('Value', None, None, None, 1, 0)],
            [DataCell('Name', None, None, None, 0, 1), DataCell('Value', None, None, None, 1, 1)],
            [DataCell('Name', None, None, None, 0, 2), DataCell('Value', None, None, None, 1, 2)],
        ]

        results[0][0].value = ProcessorResult(True, spx.name)
        results[0][1].value = ProcessorResult(True, np.float64(10))
        results[1][0].value = ProcessorResult(True, aapl.name)
        results[1][1].value = ProcessorResult(True, np.float64(0))
        results[2][0].value = ProcessorResult(True, amzn.name)
        results[2][1].value = ProcessorResult(True, np.float64(-10))

        datagrid.results = results
        return datagrid

    def test_post_processing_base_case(self):
        spx, aapl, amzn = self.get_test_entities()
        datagrid = self.get_test_datagrid()
        df = datagrid._post_process()

        # Check no filters/sorts
        assert df['Name'].iloc[0] == spx.name
        assert df['Name'].iloc[1] == aapl.name
        assert df['Name'].iloc[2] == amzn.name
        assert df['Value'].iloc[0] == 10
        assert df['Value'].iloc[1] == 0
        assert df['Value'].iloc[2] == -10

    def test_sorting(self):
        # Test 1: simple name in ascending order
        spx, aapl, amzn = self.get_test_entities()
        datagrid = self.get_test_datagrid()
        datagrid.add_sort(DataGridSort('Name'))
        df = datagrid._post_process()
        assert df['Name'].iloc[0] == amzn.name
        assert df['Name'].iloc[1] == aapl.name
        assert df['Name'].iloc[2] == spx.name
        assert df['Value'].iloc[0] == -10
        assert df['Value'].iloc[1] == 0
        assert df['Value'].iloc[2] == 10

        # Test 2: simple name in descending order
        spx, aapl, amzn = self.get_test_entities()
        datagrid = self.get_test_datagrid()
        datagrid.sorts = [DataGridSort('Name', order=SortOrder.DESCENDING)]
        df = datagrid._post_process()
        assert df['Name'].iloc[0] == spx.name
        assert df['Name'].iloc[1] == aapl.name
        assert df['Name'].iloc[2] == amzn.name
        assert df['Value'].iloc[0] == 10
        assert df['Value'].iloc[1] == 0
        assert df['Value'].iloc[2] == -10

        # Test 3: Sort values in ascending order
        spx, aapl, amzn = self.get_test_entities()
        datagrid = self.get_test_datagrid()
        datagrid.sorts = [DataGridSort('Value')]
        df = datagrid._post_process()
        assert df['Name'].iloc[0] == amzn.name
        assert df['Name'].iloc[1] == aapl.name
        assert df['Name'].iloc[2] == spx.name
        assert df['Value'].iloc[0] == -10
        assert df['Value'].iloc[1] == 0
        assert df['Value'].iloc[2] == 10

    def test_filtering(self):
        spx, aapl, amzn = self.get_test_entities()

        # Test 1: Test equals number
        datagrid = self.get_test_datagrid()
        datagrid.add_filter(DataGridFilter('Value', FilterOperation.EQUALS, 0))
        df = datagrid._post_process()
        assert df['Name'].iloc[0] == aapl.name
        assert df['Value'].iloc[0] == 0
        assert len(df) == 1

        # Test 2: Test equals numbers
        datagrid = self.get_test_datagrid()
        datagrid.add_filter(DataGridFilter('Value', FilterOperation.EQUALS, [0, 10]))
        df = datagrid._post_process()
        assert df['Name'].iloc[0] == spx.name
        assert df['Value'].iloc[0] == 10
        assert df['Name'].iloc[1] == aapl.name
        assert df['Value'].iloc[1] == 0
        assert len(df) == 2

        # Test 3: Test greater than 0 and less than 0
        datagrid = self.get_test_datagrid()
        datagrid.add_filter(DataGridFilter('Value', FilterOperation.GREATER_THAN, 0))
        datagrid.add_filter(DataGridFilter('Value', FilterOperation.LESS_THAN, 0))
        df = datagrid._post_process()
        assert len(df) == 0

        # Test 3: Test greater than 0 or less than 0
        datagrid = self.get_test_datagrid()
        datagrid.add_filter(DataGridFilter('Value', FilterOperation.GREATER_THAN, 0))
        datagrid.add_filter(DataGridFilter('Value', FilterOperation.LESS_THAN, 0, FilterCondition.OR))
        df = datagrid._post_process()
        assert df['Name'].iloc[0] == spx.name
        assert df['Value'].iloc[0] == 10
        assert df['Name'].iloc[1] == amzn.name
        assert df['Value'].iloc[1] == -10
        assert len(df) == 2


if __name__ == '__main__':
    pytest.main(args=["test_sorting_and_filtering.py"])
