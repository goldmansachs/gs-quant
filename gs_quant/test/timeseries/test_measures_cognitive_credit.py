"""
Copyright 2024 Goldman Sachs.
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
from unittest.mock import Mock

import pandas as pd
import pytest

import gs_quant.timeseries.measures_cognitive_credit as tm_cc
from gs_quant.api.gs.data import MarketDataResponseFrame
from gs_quant.data import DataContext
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.timeseries.measures_cognitive_credit import (
    CognitiveCreditKPI,
    CognitiveCreditReportType,
    REPORT_TYPE_TO_DATASET,
)


def _mock_asset(ticker="Carnival"):
    """Create a mock Asset with a ticker identifier."""
    asset = Mock(spec=Asset)
    asset.name = "Carnival Corp"
    asset.get_identifier = Mock(side_effect=lambda id_type: ticker if id_type == AssetIdentifier.TICKER else None)
    return asset


def _mock_asset_bbid(bbid="CCL US"):
    """Create a mock Asset with only a Bloomberg ID."""
    asset = Mock(spec=Asset)
    asset.name = "Carnival Corp"

    def _get_id(id_type):
        if id_type == AssetIdentifier.TICKER:
            return None
        if id_type == AssetIdentifier.BLOOMBERG_ID:
            return bbid
        return None

    asset.get_identifier = Mock(side_effect=_get_id)
    return asset


def _mock_dataset_response(value_col="cognitiveCreditLtmKpi"):
    """Build a mock DataFrame mimicking Cognitive Credit dataset output."""
    data = {
        "date": [dt.date(2023, 6, 30), dt.date(2023, 9, 30), dt.date(2023, 12, 31)],
        "ticker": ["Carnival"] * 3,
        value_col: [3500.0, 3800.0, 4100.0],
    }
    df = MarketDataResponseFrame(data=data)
    df.index = pd.DatetimeIndex(data["date"])
    return df


class TestCognitiveCreditFundamentals:
    """Tests for the cognitive_credit_fundamentals measure."""

    def test_basic_ebitda_query(self, mocker):
        """Test successful retrieval of EBITDA KPI."""
        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=_mock_dataset_response())
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            result = tm_cc.cognitive_credit_fundamentals(
                _mock_asset(),
                kpi=CognitiveCreditKPI.EBITDA,
                report_type=CognitiveCreditReportType.LTM,
            )

        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert result.iloc[0] == 3500.0
        assert result.name == "EBITDA"

    def test_annual_report_type(self, mocker):
        """Test that annual report type queries the correct dataset."""
        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=_mock_dataset_response("cognitiveCreditAnnualKpi"))
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_ANNUAL_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            result = tm_cc.cognitive_credit_fundamentals(
                _mock_asset(),
                kpi=CognitiveCreditKPI.REVENUE,
                report_type=CognitiveCreditReportType.ANNUAL,
            )

        assert result.iloc[0] == 3500.0

    def test_interim_report_type(self, mocker):
        """Test that interim report type queries the correct dataset."""
        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=_mock_dataset_response("cognitiveCreditInterimKpi"))
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_INTERIM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            result = tm_cc.cognitive_credit_fundamentals(
                _mock_asset(),
                kpi=CognitiveCreditKPI.TOTAL_NET_LEVERAGE,
                report_type=CognitiveCreditReportType.INTERIM,
            )

        assert isinstance(result, pd.Series)
        assert len(result) == 3

    def test_real_time_raises(self):
        """Test that real_time=True raises MqValueError."""
        with pytest.raises(MqValueError, match="not supported"):
            tm_cc.cognitive_credit_fundamentals(
                _mock_asset(),
                kpi=CognitiveCreditKPI.EBITDA,
                report_type=CognitiveCreditReportType.LTM,
                real_time=True,
            )

    def test_invalid_kpi_raises(self):
        """Test that an invalid kpi type raises MqValueError."""
        with pytest.raises(MqValueError, match="Invalid kpi"):
            tm_cc.cognitive_credit_fundamentals(
                _mock_asset(),
                kpi="NOT_A_KPI",
                report_type=CognitiveCreditReportType.LTM,
            )

    def test_invalid_report_type_raises(self):
        """Test that an invalid report_type raises MqValueError."""
        with pytest.raises(MqValueError, match="Invalid report_type"):
            tm_cc.cognitive_credit_fundamentals(
                _mock_asset(),
                kpi=CognitiveCreditKPI.EBITDA,
                report_type="BAD",
            )

    def test_no_ticker_no_bbid_raises(self):
        """Test that an asset without ticker or BBID raises MqValueError."""
        asset = Mock(spec=Asset)
        asset.name = "Unknown"
        asset.get_identifier = Mock(return_value=None)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            with pytest.raises(MqValueError, match="Could not resolve ticker"):
                tm_cc.cognitive_credit_fundamentals(
                    asset,
                    kpi=CognitiveCreditKPI.EBITDA,
                    report_type=CognitiveCreditReportType.LTM,
                )

    def test_empty_data_raises(self, mocker):
        """Test that empty dataset response raises MqValueError."""
        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=pd.DataFrame())
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            with pytest.raises(MqValueError, match="No data found"):
                tm_cc.cognitive_credit_fundamentals(
                    _mock_asset(),
                    kpi=CognitiveCreditKPI.EBITDA,
                    report_type=CognitiveCreditReportType.LTM,
                )

    def test_fallback_to_bbid(self, mocker):
        """Test ticker resolution falls back to Bloomberg ID."""
        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=_mock_dataset_response())
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            result = tm_cc.cognitive_credit_fundamentals(
                _mock_asset_bbid("CCL US"),
                kpi=CognitiveCreditKPI.EBITDA,
                report_type=CognitiveCreditReportType.LTM,
            )

        assert isinstance(result, pd.Series)
        # Ticker resolved from "CCL US" -> "CCL"
        call_kwargs = mock_ds.get_data.call_args[1]
        assert call_kwargs["ticker"] == "CCL"

    def test_dataset_query_exception(self, mocker):
        """Test that dataset query exceptions are wrapped in MqValueError."""
        mock_ds = Mock()
        mock_ds.get_data = Mock(side_effect=RuntimeError("Connection failed"))
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            with pytest.raises(MqValueError, match="Could not query dataset"):
                tm_cc.cognitive_credit_fundamentals(
                    _mock_asset(),
                    kpi=CognitiveCreditKPI.EBITDA,
                    report_type=CognitiveCreditReportType.LTM,
                )

    def test_wittur_total_assets_ltm(self, mocker):
        """Test WITTUR ticker with TOTAL_ASSETS KPI and LTM report type."""
        data = {
            "date": [
                dt.date(2025, 6, 30),
                dt.date(2025, 9, 30),
                dt.date(2025, 12, 31),
                dt.date(2026, 3, 31),
            ],
            "ticker": ["Wittur"] * 4,
            "cognitiveCreditLtmKpi": [1200.0, 1250.0, 1300.0, 1350.0],
        }
        mock_df = MarketDataResponseFrame(data=data)
        mock_df.index = pd.DatetimeIndex(data["date"])

        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=mock_df)
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2025, 4, 29), dt.date(2026, 4, 29)):
            result = tm_cc.cognitive_credit_fundamentals(
                _mock_asset(ticker="Wittur"),
                kpi=CognitiveCreditKPI.ASSETS,
                report_type=CognitiveCreditReportType.LTM,
            )

        assert isinstance(result, pd.Series)
        assert len(result) == 4
        assert result.name == "ASSETS"
        assert result.iloc[-1] == 1350.0

    def test_missing_value_column_raises(self, mocker):
        """Test that missing value column raises MqValueError."""
        data = {
            "date": [dt.date(2023, 6, 30)],
            "ticker": ["Carnival"],
            "someOtherColumn": [100.0],
        }
        mock_df = MarketDataResponseFrame(data=data)
        mock_df.index = pd.DatetimeIndex(data["date"])

        mock_ds = Mock()
        mock_ds.get_data = Mock(return_value=mock_df)
        mock_ds.id = "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER"
        mocker.patch("gs_quant.timeseries.measures_cognitive_credit.Dataset", return_value=mock_ds)

        with DataContext(dt.date(2023, 1, 1), dt.date(2023, 12, 31)):
            with pytest.raises(MqValueError, match="column not found in response"):
                tm_cc.cognitive_credit_fundamentals(
                    _mock_asset(),
                    kpi=CognitiveCreditKPI.EBITDA,
                    report_type=CognitiveCreditReportType.LTM,
                )


class TestEnums:
    """Tests to verify enum definitions are correct."""

    def test_report_type_dataset_mapping(self):
        """Test all report types map to valid dataset IDs."""
        assert REPORT_TYPE_TO_DATASET[CognitiveCreditReportType.LTM] == ("COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER")
        assert REPORT_TYPE_TO_DATASET[CognitiveCreditReportType.INTERIM] == (
            "COGNITIVE_CREDIT_COMPARABLES_INTERIM_BY_TICKER"
        )
        assert REPORT_TYPE_TO_DATASET[CognitiveCreditReportType.ANNUAL] == (
            "COGNITIVE_CREDIT_COMPARABLES_ANNUAL_BY_TICKER"
        )

    def test_kpi_enum_has_values(self):
        """Test that the KPI enum contains expected entries."""
        assert CognitiveCreditKPI.EBITDA.value == "EBITDA"
        assert CognitiveCreditKPI.TOTAL_NET_LEVERAGE.value == "TOTAL_NET_LEVERAGE"
        assert CognitiveCreditKPI.ASSETS.value == "ASSETS"
        assert CognitiveCreditKPI.REVENUE.value == "REVENUE"
