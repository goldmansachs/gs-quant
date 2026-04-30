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

from enum import Enum
from typing import Optional

import pandas as pd

from gs_quant.common import AssetClass, AssetType
from gs_quant.data import DataContext, Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.timeseries.helper import plot_measure
from gs_quant.timeseries.measures import ExtendedSeries


class CognitiveCreditReportType(Enum):
    """Report type determining which Cognitive Credit dataset to query."""

    LTM = "Last Twelve Months"
    INTERIM = "Interim"
    ANNUAL = "Annual"


class CognitiveCreditKPI(Enum):
    """KPI items available for Cognitive Credit fundamental queries.
    Source: https://marquee.gs.com/v1/marketview/groups/CGXBXSXTUF94ESA71X
    """

    YOY_ADJUSTED_EBITDA_MARGIN_CHANGE = "YOY_ADJUSTED_EBITDA_MARGIN_CHANGE"
    PROFIT_LOSS = "PROFIT_LOSS"
    FFO_VS_TOTAL_DEBT = "FFO_VS_TOTAL_DEBT"
    DEPRECIATION_RATE = "DEPRECIATION_RATE"
    GROSS_PROFIT = "GROSS_PROFIT"
    CAPEX_VS_DEPRECIATION_AND_AMORTISATION = "CAPEX_VS_DEPRECIATION_AND_AMORTISATION"
    COMPANY_REPORTED_ADJUSTED_EBITDA = "COMPANY_REPORTED_ADJUSTED_EBITDA"
    GROSS_MARGIN = "GROSS_MARGIN"
    NONCURRENT_LIABILITIES = "NONCURRENT_LIABILITIES"
    PROFIT_LOSS_FROM_OPERATING_ACTIVITIES = "PROFIT_LOSS_FROM_OPERATING_ACTIVITIES"
    PROFIT_LOSS_BEFORE_TAX = "PROFIT_LOSS_BEFORE_TAX"
    ASSETS = "ASSETS"
    EBITDA = "EBITDA"
    FIXED_CHARGES = "FIXED_CHARGES"
    YOY_GROSS_DEBT_CHANGE = "YOY_GROSS_DEBT_CHANGE"
    NET_INTEREST = "NET_INTEREST"
    YOY_EBIT_MARGIN_CHANGE = "YOY_EBIT_MARGIN_CHANGE"
    CASH_FLOWS_FROM_USED_IN_OPERATING_ACTIVITIES = "CASH_FLOWS_FROM_USED_IN_OPERATING_ACTIVITIES"
    GROSS_CAPEX = "GROSS_CAPEX"
    YOY_REVENUE_CHANGE = "YOY_REVENUE_CHANGE"
    INVENTORY_DAYS = "INVENTORY_DAYS"
    DEPRECIATION_AND_AMORTISATION_RATE = "DEPRECIATION_AND_AMORTISATION_RATE"
    CASH_FLOWS_FROM_USED_IN_INVESTING_ACTIVITIES = "CASH_FLOWS_FROM_USED_IN_INVESTING_ACTIVITIES"
    LIABILITIES = "LIABILITIES"
    FREE_CASH_FLOW = "FREE_CASH_FLOW"
    NET_WORKING_CAPITAL = "NET_WORKING_CAPITAL"
    CHANGE_IN_NET_WORKING_CAPITAL = "CHANGE_IN_NET_WORKING_CAPITAL"
    EBIT_MARGIN = "EBIT_MARGIN"
    INTEREST_COVERAGE_RATIO = "INTEREST_COVERAGE_RATIO"
    EBT_MARGIN = "EBT_MARGIN"
    TOTAL_NET_LEVERAGE = "TOTAL_NET_LEVERAGE"
    FREE_CASH_FLOW_TO_THE_FIRM = "FREE_CASH_FLOW_TO_THE_FIRM"
    FCF_VS_TOTAL_DEBT = "FCF_VS_TOTAL_DEBT"
    EFFECTIVE_INTEREST_RATE = "EFFECTIVE_INTEREST_RATE"
    YOY_TOTAL_NET_CASH_FLOW_CHANGE = "YOY_TOTAL_NET_CASH_FLOW_CHANGE"
    REVENUE = "REVENUE"
    CURRENT_ASSETS = "CURRENT_ASSETS"
    ACCOUNTS_RECEIVABLE_DAYS = "ACCOUNTS_RECEIVABLE_DAYS"
    YOY_FCF_CHANGE = "YOY_FCF_CHANGE"
    NONCURRENT_ASSETS = "NONCURRENT_ASSETS"
    ADJUSTMENTS_VS_EBITDA = "ADJUSTMENTS_VS_EBITDA"
    DERIVED_EBITDA_VS_COMPANY_REPORTED_EBITDA = "DERIVED_EBITDA_VS_COMPANY_REPORTED_EBITDA"
    PPE_GROWTH_RATE = "PPE_GROWTH_RATE"
    YOY_FCFF_CHANGE = "YOY_FCFF_CHANGE"
    CURRENT_LIABILITIES = "CURRENT_LIABILITIES"
    EQUITY = "EQUITY"
    ACCOUNTS_PAYABLE_DAYS = "ACCOUNTS_PAYABLE_DAYS"
    ADJUSTED_EBITDA_MARGIN = "ADJUSTED_EBITDA_MARGIN"
    YOY_NET_INCOME_CHANGE = "YOY_NET_INCOME_CHANGE"
    YOY_GROSS_CAPEX_CHANGE = "YOY_GROSS_CAPEX_CHANGE"
    CASH_DIVIDENDS_PAID = "CASH_DIVIDENDS_PAID"
    EBITDA_MARGIN = "EBITDA_MARGIN"
    NET_TAX = "NET_TAX"
    CASH_FLOWS_FROM_USED_IN_FINANCING_ACTIVITIES = "CASH_FLOWS_FROM_USED_IN_FINANCING_ACTIVITIES"
    INCREASE_DECREASE_IN_CASH_AND_CASH_EQUIVALENTS = "INCREASE_DECREASE_IN_CASH_AND_CASH_EQUIVALENTS"
    NET_CAPEX = "NET_CAPEX"
    TOTAL_CASH = "TOTAL_CASH"
    YOY_EBT_CHANGE = "YOY_EBT_CHANGE"
    TOTAL_NET_DEBT = "TOTAL_NET_DEBT"
    TOTAL_LEASE_PAYMENTS = "TOTAL_LEASE_PAYMENTS"
    TOTAL_GROSS_LEVERAGE = "TOTAL_GROSS_LEVERAGE"
    YOY_GROSS_PROFIT_CHANGE = "YOY_GROSS_PROFIT_CHANGE"
    FCFF_VS_TOTAL_DEBT = "FCFF_VS_TOTAL_DEBT"
    YOY_ADJUSTED_EBITDA_CHANGE = "YOY_ADJUSTED_EBITDA_CHANGE"
    YOY_EBIT_CHANGE = "YOY_EBIT_CHANGE"
    YOY_GROSS_MARGIN_CHANGE = "YOY_GROSS_MARGIN_CHANGE"
    TOTAL_ADJUSTMENTS_TO_COMPANY_EBITDA = "TOTAL_ADJUSTMENTS_TO_COMPANY_EBITDA"
    DEPRECIATION_AND_AMORTISATION = "DEPRECIATION_AND_AMORTISATION"
    INTANGIBLES_GROWTH_RATE = "INTANGIBLES_GROWTH_RATE"
    NET_PROFIT_MARGIN = "NET_PROFIT_MARGIN"
    FUNDS_FROM_OPERATIONS = "FUNDS_FROM_OPERATIONS"
    YOY_CFO_CHANGE = "YOY_CFO_CHANGE"
    TOTAL_GROSS_DEBT = "TOTAL_GROSS_DEBT"
    ADJUSTED_NET_LEVERAGE = "ADJUSTED_NET_LEVERAGE"
    CAPEX_VS_SALES = "CAPEX_VS_SALES"
    YOY_EBITDA_CHANGE = "YOY_EBITDA_CHANGE"
    AMORTISATION_RATE = "AMORTISATION_RATE"
    ADJUSTED_GROSS_LEVERAGE = "ADJUSTED_GROSS_LEVERAGE"
    YOY_FFO_CHANGE = "YOY_FFO_CHANGE"
    YOY_EBITDA_MARGIN_CHANGE = "YOY_EBITDA_MARGIN_CHANGE"
    FIXED_CHARGE_COVERAGE_RATIO = "FIXED_CHARGE_COVERAGE_RATIO"
    YOY_NET_DEBT_CHANGE = "YOY_NET_DEBT_CHANGE"


REPORT_TYPE_TO_DATASET = {
    CognitiveCreditReportType.LTM: "COGNITIVE_CREDIT_COMPARABLES_LTM_BY_TICKER",
    CognitiveCreditReportType.INTERIM: "COGNITIVE_CREDIT_COMPARABLES_INTERIM_BY_TICKER",
    CognitiveCreditReportType.ANNUAL: "COGNITIVE_CREDIT_COMPARABLES_ANNUAL_BY_TICKER",
}

REPORT_TYPE_TO_VALUE_COLUMN = {
    CognitiveCreditReportType.LTM: "cognitiveCreditLtmKpi",
    CognitiveCreditReportType.INTERIM: "cognitiveCreditInterimKpi",
    CognitiveCreditReportType.ANNUAL: "cognitiveCreditAnnualKpi",
}


@plot_measure((AssetClass.Equity, AssetClass.Credit), (AssetType.Company,))
def cognitive_credit_fundamentals(
    asset: Asset,
    kpi: CognitiveCreditKPI = CognitiveCreditKPI.EBITDA,
    report_type: CognitiveCreditReportType = CognitiveCreditReportType.LTM,
    *,
    source: str = None,
    real_time: bool = False,
    request_id: Optional[str] = None,
) -> pd.Series:
    """Cognitive Credit fundamental data for credit comparables.

    :param asset: asset object loaded from security master
    :param kpi: KPI metric to retrieve, e.g. EBITDA, Revenue, Net Leverage
    :param report_type: reporting period — Last Twelve Months, Interim, or Annual
    :param source: name of function caller; default source = None
    :param real_time: whether to retrieve intraday data (not supported)
    :param request_id: service request id, if any
    :return: time series of the selected KPI values

    **Usage**

    Retrieves fundamental KPI data from Cognitive Credit comparables datasets.
    The asset is mapped to a ticker, and data is fetched from the appropriate
    dataset based on the report_type (LTM, Interim, or Annual).

    **Examples**

    # >>> from gs_quant.timeseries.measures_cognitive_credit import cognitive_credit_fundamentals
    # >>> cognitive_credit_fundamentals(asset, CognitiveCreditKPI.EBITDA, CognitiveCreditReportType.ANNUAL)
    """
    if real_time:
        raise MqValueError("Real-time pricing is not supported for Cognitive Credit fundamentals.")

    if not isinstance(kpi, CognitiveCreditKPI):
        raise MqValueError("Invalid kpi argument. Must be a CognitiveCreditKPI enum value.")

    if not isinstance(report_type, CognitiveCreditReportType):
        raise MqValueError("Invalid report_type argument. Must be a CognitiveCreditReportType enum value.")

    # Resolve the ticker from the asset
    ticker = asset.get_identifier(AssetIdentifier.TICKER)
    if ticker is None:
        bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
        if bbid is not None:
            ticker = bbid.split(" ")[0] if " " in bbid else bbid
        else:
            raise MqValueError(
                f"Could not resolve ticker for asset {asset.name}. "
                "Please ensure the asset has a valid ticker identifier."
            )

    start, end = DataContext.current.start_date, DataContext.current.end_date
    ds_id = REPORT_TYPE_TO_DATASET[report_type]
    ds = Dataset(ds_id)

    try:
        # Pass the KPI name (e.g., "TOTAL_ASSETS") directly to the query
        df = ds.get_data(ticker=ticker, kpi=kpi.name, start=start, end=end)
    except Exception as e:
        raise MqValueError(f"Could not query dataset {ds_id}: {e}")

    if df.empty:
        raise MqValueError(f"No data found for ticker '{ticker}' and KPI '{kpi.value}' in dataset {ds_id}.")

    df = df.reset_index()

    # The value column name depends on the report type
    value_col = REPORT_TYPE_TO_VALUE_COLUMN[report_type]
    if value_col not in df.columns:
        raise MqValueError(
            f"'{value_col}' column not found in response for KPI '{kpi.value}'. Available columns: {list(df.columns)}"
        )

    df = df[["date", value_col]].dropna(subset=[value_col])
    df = df.sort_values(by="date", ascending=True).set_index("date")

    series = ExtendedSeries(df[value_col], name=kpi.value)
    _idx = pd.DatetimeIndex(series.index)
    series.index = _idx.as_unit("ns") if hasattr(_idx, "as_unit") else _idx
    series.dataset_ids = ds.id

    return series
