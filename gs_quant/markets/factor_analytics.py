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

import logging
from typing import Dict, List
import pandas as pd
import plotly.graph_objects as go

from gs_quant.api.gs.risk import GsRiskApi
from gs_quant.markets.position_set import PositionSet
from gs_quant.errors import MqValueError

_logger = logging.getLogger(__name__)


class FactorAnalytics:
    """
    Helper class for performing style factor analysis and visualizations.
    Provides methods to analyze style factor exposures, performance metrics, and create visualizations.
    """

    def __init__(self, risk_model_id: str, currency: str = 'USD', participation_rate: float = 0.1):
        """
        Initialize FactorAnalytics helper.

        :param risk_model_id: Risk model identifier (e.g., 'AXIOMA_AXUS4S', 'BARRA_EFM_USALTL')
        :param currency: Currency for analysis (default: USD)
        :param participation_rate: Market participation rate (default: 0.1 = 10%)
        """
        self.risk_model_id = risk_model_id
        self.currency = currency
        self.participation_rate = participation_rate

    def get_factor_analysis(self, position_set: PositionSet) -> Dict:
        """
        Get style factor analysis for a position set using the liquidity endpoint.
        Returns risk metrics and style factor exposures.

        :param position_set: Portfolio positions to analyze
        :return: Factor analysis results dictionary with style factors
        """
        if not position_set or not position_set.positions:
            raise MqValueError("Position set is empty")

        if not position_set.date:
            raise MqValueError("Position set must have a date")

        unresolved = [p for p in position_set.positions if not p.asset_id]
        if unresolved:
            _logger.info(f"Resolving {len(unresolved)} unresolved positions...")
            position_set.resolve()

        api_positions = []
        position_mapping = {}

        for position in position_set.positions:
            if not position.asset_id:
                _logger.warning(f"Skipping unresolved position: {position.identifier}")
                continue

            position_mapping[position.asset_id] = position.identifier

            if position.quantity is not None:
                api_positions.append({
                    "assetId": position.asset_id,
                    "quantity": position.quantity
                })
            elif position.weight is not None:
                api_positions.append({
                    "assetId": position.asset_id,
                    "weight": position.weight * 100
                })
            else:
                _logger.warning(f"Position {position.identifier} has no quantity or weight")

        if not api_positions:
            raise MqValueError("No valid positions to analyze")

        notional = position_set.reference_notional if position_set.reference_notional else None

        try:
            results = GsRiskApi.get_liquidity_and_factor_analysis(
                positions=api_positions,
                risk_model=self.risk_model_id,
                date=position_set.date,
                currency=self.currency,
                participation_rate=self.participation_rate,
                notional=notional,
                measures=[
                    "Time Series Data",
                    "Risk Buckets",
                    "Factor Risk Buckets",
                    "Factor Exposure Buckets",
                    "Exposure Buckets"
                ]
            )
            return results
        except MqValueError as e:
            error_msg = str(e)
            if 'missing in marquee' in error_msg.lower():
                import re
                asset_ids_match = re.findall(r'MA[A-Z0-9]+', error_msg)
                if asset_ids_match:
                    problematic_positions = []
                    for asset_id in asset_ids_match:
                        identifier = position_mapping.get(asset_id, f"Unknown (Asset ID: {asset_id})")
                        problematic_positions.append(f"{identifier} ({asset_id})")

                    raise MqValueError(
                        f"Factor analysis failed due to asset resolution issues.\n\n"
                        f"The following positions could not be found in Marquee:\n"
                        f"{chr(10).join(['  - ' + pos for pos in problematic_positions])}\n\n"
                        f"Please verify:\n"
                        f"1. Asset identifiers are correct (e.g., 'AAPL UW' for Bloomberg tickers)\n"
                        f"2. Positions are available in the Marquee system\n"
                        f"3. Asset IDs were resolved correctly\n\n"
                        f"Original error: {error_msg}"
                    )
            raise
        except Exception as e:
            _logger.error(f"Factor analysis failed: {str(e)}")
            raise

    def convert_hedge_factor_exposures(self, style_factors: List) -> Dict:
        """
        Convert hedge result style factor exposures to factor analysis format.
        This allows reusing visualization methods with data from the hedge API.

        :param style_factors: Style factor exposures from hedge result (style, sector, country)
        :return: Dictionary in the same format as get_factor_analysis() for visualization
        """
        if not style_factors:
            raise MqValueError("Style factor exposures data is empty")

        if not style_factors:
            _logger.warning("No style factor data in hedge result")

        sub_factors = [
            {'name': item['factor'], 'value': item['exposure']}
            for item in style_factors
        ]

        return {
            'factorExposureBuckets': [
                {
                    'name': 'Style',
                    'subFactors': sub_factors
                }
            ],
            'notional': 0,
            'currency': 'USD',
            'riskBuckets': []
        }

    def create_exposure_bar_chart(self,
                                  exposures: Dict[str, float],
                                  title: str,
                                  horizontal: bool = True) -> go.Figure:
        """
        Create a bar chart for style factor exposures with color coding.
        Note: This method is intended for style factors only.

        :param exposures: Dictionary of factor names to exposure values
        :param title: Chart title
        :param horizontal: If True, creates horizontal bars; otherwise vertical
        :return: Plotly figure
        """
        if not exposures:
            return go.Figure().add_annotation(text="No data available", showarrow=False)

        names = list(exposures.keys())
        values = list(exposures.values())

        colors = ['green' if v >= 0 else 'red' for v in values]

        fig = go.Figure()

        if horizontal:
            fig.add_trace(go.Bar(
                y=names,
                x=values,
                orientation='h',
                marker_color=colors,
                text=[f'{v:,.0f}' for v in values],
                textposition='outside',
                showlegend=False
            ))
            fig.update_xaxes(title="Exposure")
            fig.update_yaxes(title="")
        else:
            fig.add_trace(go.Bar(
                x=names,
                y=values,
                marker_color=colors,
                text=[f'{v:,.0f}' for v in values],
                textposition='outside',
                showlegend=False
            ))
            fig.update_xaxes(title="")
            fig.update_yaxes(title="Exposure")

        if horizontal:
            chart_height = max(300, len(names) * 40 + 150)
        else:
            chart_height = 500

        fig.update_layout(
            title=title,
            height=chart_height,
            margin=dict(l=200 if horizontal else 50, r=50, t=80, b=50)
        )

        return fig

    def create_style_factor_chart(self, factor_analysis: Dict, rows: int = None,
                                  title: str = "Style Factor Exposures") -> go.Figure:
        """
        Create a bar chart showing positive and negative style factor exposures.

        :param factor_analysis: Factor analysis results from liquidity endpoint
        :param title: Chart title
        :return: Plotly figure showing top positive and negative style factors
        """
        if 'factorExposureBuckets' not in factor_analysis:
            return go.Figure().add_annotation(text="No style factor data available", showarrow=False)

        style_factors = {}
        for bucket in factor_analysis['factorExposureBuckets']:
            if bucket.get('name') == 'Style':
                for sub_factor in bucket.get('subFactors', []):
                    factor_name = sub_factor.get('name')
                    factor_value = sub_factor.get('value', 0)
                    if factor_name:
                        style_factors[factor_name] = factor_value
                break

        if not style_factors:
            return go.Figure().add_annotation(text="No style factor data available", showarrow=False)

        positive_factors = {k: v for k, v in style_factors.items() if v > 0}
        negative_factors = {k: v for k, v in style_factors.items() if v < 0}

        # most negative first - ascending order by value)
        top_negative_limit = rows if rows is not None else None
        top_negative = dict(sorted(negative_factors.items(), key=lambda x: x[1])[:top_negative_limit])

        # descending order - highest first)
        top_positive_limit = rows if rows is not None else None
        top_positive_items = sorted(positive_factors.items(), key=lambda x: x[1],
                                    reverse=True)[:top_positive_limit]
        # Reverse to get ascending order for display (lowest to highest)
        top_positive = dict(reversed(top_positive_items))

        selected_factors = {**top_negative, **top_positive}

        if not selected_factors:
            return go.Figure().add_annotation(text="No style factor data available", showarrow=False)

        total_factors = len(style_factors)

        subset_title = title
        if rows is not None:
            subset_title = f"{title} (Top {rows} Positive & Top {rows} Negative, {total_factors} Total)"

        return self.create_exposure_bar_chart(
            selected_factors,
            subset_title,
            horizontal=True
        )

    def create_exposure_summary_table(self, factor_analysis: Dict) -> pd.DataFrame:
        """
        Create a summary table of key portfolio metrics.

        :param factor_analysis: Factor analysis results from liquidity endpoint
        :return: Pandas DataFrame with summary metrics
        """
        notional = factor_analysis.get('notional', 0)
        currency = factor_analysis.get('currency', 'USD')

        risk_buckets = {bucket['name']: bucket['value']
                        for bucket in factor_analysis.get('riskBuckets', [])}

        data = {
            'Metric': [
                'Notional',
                'Currency',
                'Market Risk',
                'Specific Risk',
                'Sector Risk',
                'Style Risk'
            ],
            'Value': [
                f"${notional:,.0f}",
                currency,
                f"{risk_buckets.get('Market', 0):.4f}",
                f"{risk_buckets.get('Specific', 0):.4f}",
                f"{risk_buckets.get('Sector', 0):.4f}",
                f"{risk_buckets.get('Style', 0):.4f}"
            ]
        }

        return pd.DataFrame(data, index=None)

    def create_performance_chart(self,
                                 performance_data: pd.DataFrame,
                                 metric: str = 'cumulativePnl',
                                 title: str = "Performance") -> go.Figure:
        """
        Create a time series performance chart.

        :param performance_data: DataFrame with date and performance columns
        :param metric: Column name to plot
        :param title: Chart title
        :return: Plotly figure
        """
        if performance_data.empty:
            return go.Figure().add_annotation(text="No performance data available", showarrow=False)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=performance_data['date'] if 'date' in performance_data.columns else performance_data.index,
            y=performance_data[metric] if metric in performance_data.columns else performance_data.iloc[:, 0],
            mode='lines',
            name=metric,
            line=dict(width=2)
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title=metric.replace('_', ' ').title(),
            height=500,
            hovermode='x unified'
        )

        return fig

    def create_dynamic_performance_chart(self,
                                         factor_analysis: Dict,
                                         title: str = "Portfolio Performance Metrics") -> go.Figure:
        """
        Create a dynamic chart with toggleable performance metrics from timeseriesData.
        Shows cumulative PnL and normalized performance.

        :param factor_analysis: Factor analysis results from liquidity endpoint
        :param title: Chart title
        :return: Plotly figure with dropdown menu for cumulative PnL and normalized performance
        """
        timeseries_data = factor_analysis.get('timeseriesData', [])

        if not timeseries_data:
            return go.Figure().add_annotation(
                text="No time series data available. Ensure 'Time Series Data' measure is included.",
                showarrow=False,
                font=dict(size=14)
            )

        total_data = None
        for item in timeseries_data:
            if item.get('name') == 'total':
                total_data = item
                break

        cumulative_pnl_raw = total_data.get('cumulativePnl', [])
        normalized_performance_raw = total_data.get('normalizedPerformance', [])

        if not cumulative_pnl_raw and not normalized_performance_raw:
            return go.Figure().add_annotation(
                text="No cumulative PnL or normalized performance data available.",
                showarrow=False,
                font=dict(size=14)
            )

        cumulative_dates = []
        cumulative_values = []
        for item in cumulative_pnl_raw:
            if len(item) == 2 and isinstance(item[0], str):
                cumulative_dates.append(item[0])
                cumulative_values.append(item[1])

        normalized_dates = []
        normalized_values = []
        for item in normalized_performance_raw:
            if len(item) == 2 and isinstance(item[0], str):
                normalized_dates.append(item[0])
                normalized_values.append(item[1])

        if not cumulative_dates and cumulative_values:
            cumulative_dates = list(range(len(cumulative_values)))
        if not normalized_dates and normalized_values:
            normalized_dates = list(range(len(normalized_values)))

        fig = go.Figure()

        if cumulative_values:
            fig.add_trace(go.Scatter(
                x=cumulative_dates,
                y=cumulative_values,
                mode='lines',
                name='Cumulative PnL',
                visible=True,
                line=dict(width=2, color='blue')
            ))

        if normalized_values:
            fig.add_trace(go.Scatter(
                x=normalized_dates,
                y=normalized_values,
                mode='lines',
                name='Normalized Performance',
                visible=False,
                line=dict(width=2, color='green')
            ))

        buttons = [
            dict(
                label="Cumulative PnL",
                method="update",
                args=[
                    {"visible": [True, False]},
                    {"yaxis.title.text": "Cumulative PnL ($)"}
                ]
            ),
            dict(
                label="Normalized Performance",
                method="update",
                args=[
                    {"visible": [False, True]},
                    {"yaxis.title.text": "Normalized Performance"}
                ]
            )
        ]

        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Cumulative PnL ($)",
            height=500,
            hovermode='x unified',
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                )
            ],
            annotations=[
                dict(
                    text="Select Metric:",
                    showarrow=False,
                    x=0.01,
                    xref="paper",
                    y=1.13,
                    yref="paper",
                    align="left"
                )
            ]
        )

        return fig

    def create_factor_heatmap_comparison(self,
                                         initial_analysis: Dict,
                                         hedged_analysis: Dict,
                                         title: str = "Style Factor Comparison: Initial vs Hedged") -> go.Figure:
        """
        Create a grouped bar chart comparing style factor exposures.
        Shows side-by-side bars for easy comparison.

        :param initial_analysis: Factor analysis for initial portfolio
        :param hedged_analysis: Factor analysis for hedged portfolio
        :param title: Chart title
        :return: Plotly figure with grouped bar chart
        """
        def extract_style_factors(analysis):
            for bucket in analysis.get('factorExposureBuckets', []):
                if bucket.get('name') == 'Style':
                    return {sf['name']: sf['value'] for sf in bucket.get('subFactors', [])}
            return {}

        initial_factors = extract_style_factors(initial_analysis)
        hedged_factors = extract_style_factors(hedged_analysis)

        all_factors = set(initial_factors.keys()) | set(hedged_factors.keys())

        if not all_factors:
            return go.Figure().add_annotation(text="No factor data available", showarrow=False)

        sorted_factors = sorted(all_factors, key=lambda f: abs(initial_factors.get(f, 0)), reverse=True)

        initial_values = [initial_factors.get(f, 0) for f in sorted_factors]
        hedged_values = [hedged_factors.get(f, 0) for f in sorted_factors]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Initial Portfolio',
            y=sorted_factors,
            x=initial_values,
            orientation='h',
            marker_color='#4472C4',
            text=[f'{v:,.0f}' for v in initial_values],
            textposition='outside',
            textfont=dict(size=10)
        ))

        # Hedged portfolio bars
        fig.add_trace(go.Bar(
            name='Hedged Portfolio',
            y=sorted_factors,
            x=hedged_values,
            orientation='h',
            marker_color='#70AD47',
            text=[f'{v:,.0f}' for v in hedged_values],
            textposition='outside',
            textfont=dict(size=10)
        ))

        # Calculate dynamic height based on number of factors
        chart_height = max(500, len(sorted_factors) * 35 + 150)

        fig.update_layout(
            title=title,
            xaxis_title="Exposure Value",
            yaxis_title="",
            height=chart_height,
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=200, r=100, t=100, b=50)
        )

        # Add vertical line at x=0 for reference
        fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray")

        return fig
