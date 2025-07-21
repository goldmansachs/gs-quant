"""
Copyright 2023 Goldman Sachs.
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

import unittest
import datetime as dt
from gs_quant.data.utilities import SecmasterXrefFormatter


class TestSecmasterXrefFormatter(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.formatter = SecmasterXrefFormatter()

    def test_event_creation_and_priority(self):
        """Test Event dataclass creation and priority assignment."""
        start_event = SecmasterXrefFormatter.Event(
            date="2023-01-01",
            event_type=SecmasterXrefFormatter.EventType.START,
            record={"type": "CUSIP", "value": "12345", "startDate": "2023-01-01", "endDate": "2023-12-31"}
        )

        end_event = SecmasterXrefFormatter.Event(
            date="2023-01-01",
            event_type=SecmasterXrefFormatter.EventType.END,
            record={"type": "ISIN", "value": "US12345", "startDate": "2023-01-01", "endDate": "2023-12-31"}
        )

        self.assertEqual(start_event.priority, 0)
        self.assertEqual(end_event.priority, 1)

    def test_date_sort_key(self):
        """Test date sorting functionality."""
        normal_date = "2023-01-01"
        infinity_date = SecmasterXrefFormatter.INFINITY_DATE

        normal_key = SecmasterXrefFormatter._date_sort_key(normal_date)
        infinity_key = SecmasterXrefFormatter._date_sort_key(infinity_date)

        self.assertEqual(normal_key, dt.datetime(2023, 1, 1))
        self.assertEqual(infinity_key, dt.datetime(9999, 12, 31))
        self.assertTrue(infinity_key > normal_key)

    def test_add_one_day(self):
        """Test adding one day to various date scenarios."""
        # Normal date
        result = SecmasterXrefFormatter._add_one_day("2023-01-01")
        self.assertEqual(result, "2023-01-02")

        # End of month
        result = SecmasterXrefFormatter._add_one_day("2023-01-31")
        self.assertEqual(result, "2023-02-01")

        # End of year
        result = SecmasterXrefFormatter._add_one_day("2023-12-31")
        self.assertEqual(result, "2024-01-01")

        # Leap year
        result = SecmasterXrefFormatter._add_one_day("2024-02-28")
        self.assertEqual(result, "2024-02-29")

        # Infinity date
        result = SecmasterXrefFormatter._add_one_day(SecmasterXrefFormatter.INFINITY_DATE)
        self.assertIsNone(result)

        # Invalid date
        result = SecmasterXrefFormatter._add_one_day("invalid-date")
        self.assertIsNone(result)

    def test_subtract_one_day(self):
        """Test subtracting one day from various date scenarios."""
        # Normal date
        result = SecmasterXrefFormatter._subtract_one_day("2023-01-02")
        self.assertEqual(result, "2023-01-01")

        # Beginning of month
        result = SecmasterXrefFormatter._subtract_one_day("2023-02-01")
        self.assertEqual(result, "2023-01-31")

        # Beginning of year
        result = SecmasterXrefFormatter._subtract_one_day("2024-01-01")
        self.assertEqual(result, "2023-12-31")

        # Invalid date (should return original)
        result = SecmasterXrefFormatter._subtract_one_day("invalid-date")
        self.assertEqual(result, "invalid-date")

    def test_create_events(self):
        """Test event creation from records."""
        records = [
            {
                "type": "CUSIP",
                "value": "12345",
                "startDate": "2023-01-01",
                "endDate": "2023-06-30"
            },
            {
                "type": "ISIN",
                "value": "US12345",
                "startDate": "2023-07-01",
                "endDate": SecmasterXrefFormatter.INFINITY_DATE
            }
        ]

        events = SecmasterXrefFormatter._create_events(records)

        # Should have 3 events: 2 start events + 1 end event (no end event for infinity)
        self.assertEqual(len(events), 3)

        # Check start events
        start_events = [e for e in events if e.event_type == SecmasterXrefFormatter.EventType.START]
        self.assertEqual(len(start_events), 2)

        # Check end events
        end_events = [e for e in events if e.event_type == SecmasterXrefFormatter.EventType.END]
        self.assertEqual(len(end_events), 1)
        self.assertEqual(end_events[0].date, "2023-07-01")  # Day after end date

    def test_convert_empty_data(self):
        """Test conversion with empty data."""
        result = SecmasterXrefFormatter.convert({})
        self.assertEqual(result, {})

        result = SecmasterXrefFormatter.convert({"entity1": []})
        self.assertEqual(result, {"entity1": {"xrefs": []}})

    def test_convert_simple_case(self):
        """Test conversion with a simple single identifier case."""
        data = {
            "entity1": [
                {
                    "type": "CUSIP",
                    "value": "12345",
                    "startDate": "2023-01-01",
                    "endDate": "2023-12-31"
                }
            ]
        }

        result = SecmasterXrefFormatter.convert(data)
        expected = {
            "entity1": {
                "xrefs": [
                    {
                        "startDate": "2023-01-01",
                        "endDate": "2023-12-31",
                        "identifiers": {"CUSIP": "12345"}
                    }
                ]
            }
        }

        self.assertEqual(result, expected)

    def test_convert_infinity_marker_normalization(self):
        """Test that infinity markers are converted to infinity dates."""
        data = {
            "entity1": [
                {
                    "type": "CUSIP",
                    "value": "12345",
                    "startDate": "2023-01-01",
                    "endDate": SecmasterXrefFormatter.INFINITY_MARKER
                }
            ]
        }

        result = SecmasterXrefFormatter.convert(data)
        expected = {
            "entity1": {
                "xrefs": [
                    {
                        "startDate": "2023-01-01",
                        "endDate": SecmasterXrefFormatter.INFINITY_DATE,
                        "identifiers": {"CUSIP": "12345"}
                    }
                ]
            }
        }

        self.assertEqual(result, expected)

    def test_convert_overlapping_periods(self):
        """Test conversion with overlapping identifier periods."""
        data = {
            "entity1": [
                {
                    "type": "CUSIP",
                    "value": "12345",
                    "startDate": "2023-01-01",
                    "endDate": "2023-06-30"
                },
                {
                    "type": "ISIN",
                    "value": "US12345",
                    "startDate": "2023-03-01",
                    "endDate": "2023-09-30"
                }
            ]
        }

        result = SecmasterXrefFormatter.convert(data)
        xrefs = result["entity1"]["xrefs"]

        # Should have 3 periods
        self.assertEqual(len(xrefs), 3)

        # Period 1: Only CUSIP (Jan 1 - Feb 28)
        self.assertEqual(xrefs[0]["startDate"], "2023-01-01")
        self.assertEqual(xrefs[0]["endDate"], "2023-02-28")
        self.assertEqual(xrefs[0]["identifiers"], {"CUSIP": "12345"})

        # Period 2: Both CUSIP and ISIN (Mar 1 - Jun 30)
        self.assertEqual(xrefs[1]["startDate"], "2023-03-01")
        self.assertEqual(xrefs[1]["endDate"], "2023-06-30")
        self.assertEqual(xrefs[1]["identifiers"], {"CUSIP": "12345", "ISIN": "US12345"})

        # Period 3: Only ISIN (Jul 1 - Sep 30)
        self.assertEqual(xrefs[2]["startDate"], "2023-07-01")
        self.assertEqual(xrefs[2]["endDate"], "2023-09-30")
        self.assertEqual(xrefs[2]["identifiers"], {"ISIN": "US12345"})

    def test_convert_adjacent_periods(self):
        """Test conversion with adjacent periods (no gaps)."""
        data = {
            "entity1": [
                {
                    "type": "CUSIP",
                    "value": "12345",
                    "startDate": "2023-01-01",
                    "endDate": "2023-06-30"
                },
                {
                    "type": "CUSIP",
                    "value": "67890",
                    "startDate": "2023-07-01",
                    "endDate": "2023-12-31"
                }
            ]
        }

        result = SecmasterXrefFormatter.convert(data)
        xrefs = result["entity1"]["xrefs"]

        # Should have 2 periods with no gaps
        self.assertEqual(len(xrefs), 2)

        self.assertEqual(xrefs[0]["startDate"], "2023-01-01")
        self.assertEqual(xrefs[0]["endDate"], "2023-06-30")
        self.assertEqual(xrefs[0]["identifiers"], {"CUSIP": "12345"})

        self.assertEqual(xrefs[1]["startDate"], "2023-07-01")
        self.assertEqual(xrefs[1]["endDate"], "2023-12-31")
        self.assertEqual(xrefs[1]["identifiers"], {"CUSIP": "67890"})

    def test_convert_same_date_start_end(self):
        """Test conversion when identifiers start and end on the same date."""
        data = {
            "entity1": [
                {
                    "type": "CUSIP",
                    "value": "12345",
                    "startDate": "2023-01-01",
                    "endDate": "2023-06-30"
                },
                {
                    "type": "ISIN",
                    "value": "US12345",
                    "startDate": "2023-06-30",
                    "endDate": "2023-12-31"
                }
            ]
        }

        result = SecmasterXrefFormatter.convert(data)
        xrefs = result["entity1"]["xrefs"]

        # Should handle the overlap correctly
        self.assertTrue(len(xrefs) >= 1)

    def test_convert_multiple_entities(self):
        """Test conversion with multiple entities."""
        data = {
            "entity1": [
                {
                    "type": "CUSIP",
                    "value": "12345",
                    "startDate": "2023-01-01",
                    "endDate": "2023-12-31"
                }
            ],
            "entity2": [
                {
                    "type": "ISIN",
                    "value": "US67890",
                    "startDate": "2023-01-01",
                    "endDate": "2023-12-31"
                }
            ]
        }

        result = SecmasterXrefFormatter.convert(data)

        self.assertIn("entity1", result)
        self.assertIn("entity2", result)
        self.assertEqual(len(result["entity1"]["xrefs"]), 1)
        self.assertEqual(len(result["entity2"]["xrefs"]), 1)
        self.assertEqual(result["entity1"]["xrefs"][0]["identifiers"], {"CUSIP": "12345"})
        self.assertEqual(result["entity2"]["xrefs"][0]["identifiers"], {"ISIN": "US67890"})

    def test_event_sorting(self):
        """Test that events are sorted correctly by date and priority."""
        events = [
            SecmasterXrefFormatter.Event("2023-01-02", SecmasterXrefFormatter.EventType.START, {}),
            SecmasterXrefFormatter.Event("2023-01-01", SecmasterXrefFormatter.EventType.END, {}),
            SecmasterXrefFormatter.Event("2023-01-01", SecmasterXrefFormatter.EventType.START, {}),
            SecmasterXrefFormatter.Event("2023-01-02", SecmasterXrefFormatter.EventType.END, {}),
        ]

        events.sort(key=lambda e: (SecmasterXrefFormatter._date_sort_key(e.date), e.priority))

        # Should be ordered: 2023-01-01 START, 2023-01-01 END, 2023-01-02 START, 2023-01-02 END
        self.assertEqual(events[0].date, "2023-01-01")
        self.assertEqual(events[0].event_type, SecmasterXrefFormatter.EventType.START)
        self.assertEqual(events[1].date, "2023-01-01")
        self.assertEqual(events[1].event_type, SecmasterXrefFormatter.EventType.END)
        self.assertEqual(events[2].date, "2023-01-02")
        self.assertEqual(events[2].event_type, SecmasterXrefFormatter.EventType.START)
        self.assertEqual(events[3].date, "2023-01-02")
        self.assertEqual(events[3].event_type, SecmasterXrefFormatter.EventType.END)


if __name__ == '__main__':
    # Run the tests
    unittest.main()
