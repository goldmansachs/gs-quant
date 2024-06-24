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
import json

import pytz

from gs_quant.json_convertors import decode_iso_date_or_datetime
from gs_quant.json_encoder import JSONEncoder
from gs_quant.workflow import BinaryImageComments, ImgType, Encoding, HyperLinkImageComments, \
    VisualStructuringReport, ChartingParameters, OverlayType


def test_datetime_serialisation():
    dates = [
        dt.datetime(2021, 8, 10, 10, 39, 19),
        dt.datetime(2021, 8, 10, 10, 39, 19, 59876),
        dt.datetime(2021, 8, 10, 10, 39, 19, tzinfo=pytz.timezone('EST')),
        dt.datetime(2021, 8, 10, 10, 39, 19, tzinfo=pytz.timezone('UTC')),
    ]
    expected = [
        '"2021-08-10T10:39:19.000Z"',
        '"2021-08-10T10:39:19.059Z"',
        '"2021-08-10T10:39:19.000-05:00"',
        '"2021-08-10T10:39:19.000+00:00"',
    ]
    for d, e in zip(dates, expected):
        encoded = json.dumps(d, cls=JSONEncoder)
        assert encoded == e


def test_date_or_datetime():
    d1 = dt.date(2023, 4, 11)
    d2 = dt.date(2024, 12, 25)
    dt1 = dt.datetime(2023, 4, 11, 6, 19, 18, 59876)
    dt2 = dt.datetime(2024, 12, 25, 10, 39, 19, 59876)
    # Single date
    assert d1 == decode_iso_date_or_datetime(d1.isoformat())
    # list of dates
    assert (d1, d2) == decode_iso_date_or_datetime([d1.isoformat(), d2.isoformat()])
    # Single datetime
    assert dt1 == decode_iso_date_or_datetime(dt1.isoformat())
    # list of datetimes
    assert (dt1, dt2) == decode_iso_date_or_datetime([dt1.isoformat(), dt2.isoformat()])
    # Mixed
    assert (dt1, d2) == decode_iso_date_or_datetime([dt1.isoformat(), d2.isoformat()])


def test_time():
    t = dt.time(10, 14, 59, 59876)
    json_time = json.dumps(t, cls=JSONEncoder)
    assert json_time == '"10:14:59.059"'


def test_custom_comments():
    bc = BinaryImageComments(data='blah', img_type=ImgType.JPEG, encoding=Encoding.Base64)
    hc = HyperLinkImageComments(url='blah')
    report = VisualStructuringReport(comments=(bc, hc),
                                     charting_parameters=ChartingParameters(overlay=OverlayType.Vega,
                                                                            underlay=OverlayType.ProbabilityDistribution
                                                                            ))
    json_str = report.to_json()
    round_trip = VisualStructuringReport.from_json(json_str)
    assert round_trip == report
