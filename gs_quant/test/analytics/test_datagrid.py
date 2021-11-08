"""
Copyright 2018 Goldman Sachs.
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
from datetime import date

import pytest
from gs_quant.session import GsSession, Environment

from gs_quant.analytics.datagrid import DataGrid, DataColumn, DataRow
from gs_quant.analytics.processors import EntityProcessor, ChangeProcessor, AppendProcessor
from gs_quant.data import DataCoordinate, DataMeasure, DataFrequency
from gs_quant.datetime.relative_date import RelativeDate
from gs_quant.test.utils.datagrid_test_utils import get_test_entity


def test_simple_datagrid():
    name = 'Testing'
    SPX = get_test_entity('MA4B66MW5E27U8P32SB')
    rows = [
        DataRow(SPX),
    ]
    columns = [
        DataColumn(name="Name", processor=EntityProcessor(field="short_name"))
    ]

    datagrid = DataGrid(name=name, rows=rows, columns=columns)

    assert datagrid.name == name
    assert datagrid.rows == rows
    assert datagrid.columns == columns

    assert datagrid.is_initialized is False
    assert len(datagrid.results) == 0
    datagrid.initialize()
    assert datagrid.is_initialized is True
    assert len(datagrid.results) > 0


def test_rdate_datagrid(mocker):
    mocker.patch.object(GsSession.__class__, 'default_value',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    name = 'Testing'
    SPX = get_test_entity('MA4B66MW5E27U8P32SB')
    close = DataCoordinate(
        measure=DataMeasure.CLOSE_PRICE,
        frequency=DataFrequency.DAILY,
    )

    last_trade_price = DataCoordinate(
        measure=DataMeasure.TRADE_PRICE,
        frequency=DataFrequency.REAL_TIME,
    )
    rows = [
        DataRow(SPX),
    ]
    columns = [
        DataColumn(name="1d Chg (RT)",
                   processor=ChangeProcessor(AppendProcessor(close, last_trade_price,
                                                             start=RelativeDate("-1d",
                                                                                base_date=date(2021, 1, 22)))))
    ]

    datagrid = DataGrid(name=name, rows=rows, columns=columns)
    start_date = datagrid.columns[0].processor.children['a'].start
    assert start_date.base_date == RelativeDate('-1d', base_date=date(2021, 1, 22)).base_date
    assert start_date.rule == RelativeDate('-1d').rule

    datagrid.initialize()
    datagrid.poll()
    assert str(datagrid._data_queries[0].query.start) == '2021-01-21'

    as_dict = datagrid.as_dict()
    start = as_dict['parameters']['columns'][0]['parameters']['a']['parameters']['start']
    assert start['type'] == 'relativeDate'
    assert start['value'] == {'rule': '-1d', 'baseDate': '2021-01-22'}

    # Check that base_date is not persisted when not passed in.
    columns = [
        DataColumn(name="1d Chg (RT)",
                   processor=ChangeProcessor(AppendProcessor(close, last_trade_price,
                                                             start=RelativeDate("-1d"))))
    ]
    datagrid = DataGrid(name=name, rows=rows, columns=columns)
    as_dict = datagrid.as_dict()
    start = as_dict['parameters']['columns'][0]['parameters']['a']['parameters']['start']
    assert start['type'] == 'relativeDate'
    assert start['type'] == 'relativeDate'
    assert start['value'] == {'rule': '-1d'}


if __name__ == '__main__':
    pytest.main(args=["test_datagrid.py"])
