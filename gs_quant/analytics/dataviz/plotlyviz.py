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

This product uses the FRED® API but is not endorsed or certified
by the Federal Reserve Bank of St. Louis. FRED terms of use
available at https://research.stlouisfed.org/docs/api/terms_of_use.html
"""

from typing import Union, Dict

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure

from gs_quant.analytics.datagrid import DataGrid
from gs_quant.analytics.dataviz.dataviz_base import __DataVizBase, SupportedFigure, DataVizSource, DataVizSourceType
from gs_quant.api.gs.datagrid import GsDataGridApi
from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqValueError
from gs_quant.target.common import Entitlements as Entitlements_

AURORA_DATAVIZ_COLOR_SEQUENCE = [
    "#186ade",
    "#fa5343",
    "#16a163",
    "#0073ba",
    "#3a45b0",
    "#8f49de",
    "#fc9162",
    "#0073ba",
    "#fc9162",
    "#d32d47",
    "#75b1ff"
]


class PlotlyViz(__DataVizBase):
    def __init__(self,
                 id_: str = None,
                 datagrid_id: str = None,
                 datagrid: DataGrid = None,
                 *,
                 entitlements: Union[Entitlements, Entitlements_] = None,
                 dataviz_dict: dict = None):
        super().__init__(self.__class__.__name__, id_, entitlements=entitlements, dataviz_dict=dataviz_dict)
        if id_:
            if not self._viz_response:
                raise MqValueError('Unable to instantiate DataViz. Unable to fetch visualization entity.')
            if len(self._sources) == 1 and self._sources[0].type == DataVizSourceType.DATAGRID.value:
                self.__datagrid = GsDataGridApi.get_datagrid(self._sources[0].id)
            else:
                raise MqValueError('Unable to instantiate DataViz. Invalid datagrid source or multiple set.')
        elif dataviz_dict:
            if datagrid:
                self.__datagrid = datagrid
            else:
                raise MqValueError('A valid Datagrid is required to initialize DataViz.')
        else:
            if datagrid:
                self.__datagrid = datagrid
            elif datagrid_id:
                self.__datagrid = GsDataGridApi.get_datagrid(datagrid_id)
            else:
                raise MqValueError('There must be a valid Datagrid or DataGrid Id to create a visualization.')

    @property
    def datagrid(self) -> DataGrid:
        return self.__datagrid

    def create_payload(self, attributes: Dict) -> None:
        cds = 'color_discrete_sequence'
        if cds in attributes and attributes[cds] is None:
            attributes[cds] = AURORA_DATAVIZ_COLOR_SEQUENCE
        super()._create_payload(attributes)

    def save(self) -> str:
        if self._type:
            datagrid_id = self.__datagrid.save()
            dataviz_id = super()._save(sources=[DataVizSource(type=DataVizSourceType.DATAGRID, id=datagrid_id)])
            return dataviz_id
        else:
            raise MqValueError('Figure not yet initialized/created. Please create a figure before saving it.')

    def get_dataframe(self) -> pd.DataFrame:
        if not self.__datagrid.is_initialized:
            self.__datagrid.initialize()
            self.__datagrid.poll()
        return self.__datagrid.to_frame()

    def get_figure(self) -> Figure:
        try:
            df = self.get_dataframe()
            figure_initializer = getattr(px, self._type.value)
            figure: Figure = figure_initializer(data_frame=df, **self._parameters)
            figure.update_layout(
                template=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Goldman-Sans-Regular, sans-serif'),
                hoverlabel=dict(
                    font_size=12,
                    font_family='Goldman-Sans-Regular, sans-serif',
                )
            )
            figure.update_xaxes(
                tickfont=dict(family='Roboto-Mono, monospace', size=9),
                showline=True, linewidth=1, linecolor='#9fb1bd', gridcolor='rgba(42, 63, 77, 0.2)')
            figure.update_yaxes(
                tickfont=dict(family='Roboto-Mono, monospace', size=9),
                showline=True, linewidth=1, linecolor='#9fb1bd', gridcolor='rgba(42, 63, 77, 0.2)')
            return figure
        except Exception as e:
            raise RuntimeError(f'Unable to get Figure. {e}')

    def bar(self,
            x=None,
            y=None,
            color=None,
            facet_row=None,
            facet_col=None,
            facet_col_wrap=0,
            facet_row_spacing=None,
            facet_col_spacing=None,
            hover_name=None,
            hover_data=None,
            custom_data=None,
            text=None,
            base=None,
            error_x=None,
            error_x_minus=None,
            error_y=None,
            error_y_minus=None,
            animation_frame=None,
            animation_group=None,
            category_orders=None,
            labels=None,
            color_discrete_sequence=None,
            color_discrete_map=None,
            color_continuous_scale=None,
            range_color=None,
            color_continuous_midpoint=None,
            opacity=None,
            orientation=None,
            barmode="relative",
            log_x=False,
            log_y=False,
            range_x=None,
            range_y=None,
            title=None,
            template=None,
            width=None,
            height=None) -> None:
        """
        In a bar plot, each row of `data_frame` is represented as a rectangular
        mark.
        https://plotly.com/python-api-reference/generated/plotly.express.bar.html#plotly.express.bar
        """
        self.type = SupportedFigure.BAR
        self.create_payload(locals())

    def line(
            self,
            x=None,
            y=None,
            line_group=None,
            color=None,
            line_dash=None,
            hover_name=None,
            hover_data=None,
            custom_data=None,
            text=None,
            facet_row=None,
            facet_col=None,
            facet_col_wrap=0,
            facet_row_spacing=None,
            facet_col_spacing=None,
            error_x=None,
            error_x_minus=None,
            error_y=None,
            error_y_minus=None,
            animation_frame=None,
            animation_group=None,
            category_orders=None,
            labels=None,
            orientation=None,
            color_discrete_sequence=None,
            color_discrete_map=None,
            line_dash_sequence=None,
            line_dash_map=None,
            log_x=False,
            log_y=False,
            range_x=None,
            range_y=None,
            line_shape=None,
            render_mode="auto",
            title=None,
            template=None,
            width=None,
            height=None,
    ) -> None:
        """
        In a 2D line plot, each row of `data_frame` is represented as vertex of
        a polyline mark in 2D space.
        https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
        """
        self.type = SupportedFigure.LINE
        self.create_payload(locals())

    def pie(
            self,
            names=None,
            values=None,
            color=None,
            color_discrete_sequence=None,
            color_discrete_map=None,
            hover_name=None,
            hover_data=None,
            custom_data=None,
            labels=None,
            title=None,
            template=None,
            width=None,
            height=None,
            opacity=None,
            hole=None,
    ) -> None:
        """
        In a pie plot, each row of `data_frame` is represented as a sector of a
        pie.
        https://plotly.com/python-api-reference/generated/plotly.express.pie.html#plotly.express.pie
        """
        self.type = SupportedFigure.PIE
        self.create_payload(locals())

    def scatter(
            self,
            x=None,
            y=None,
            color=None,
            symbol=None,
            size=None,
            hover_name=None,
            hover_data=None,
            custom_data=None,
            text=None,
            facet_row=None,
            facet_col=None,
            facet_col_wrap=0,
            facet_row_spacing=None,
            facet_col_spacing=None,
            error_x=None,
            error_x_minus=None,
            error_y=None,
            error_y_minus=None,
            animation_frame=None,
            animation_group=None,
            category_orders=None,
            labels=None,
            orientation=None,
            color_discrete_sequence=None,
            color_discrete_map=None,
            color_continuous_scale=None,
            range_color=None,
            color_continuous_midpoint=None,
            symbol_sequence=None,
            symbol_map=None,
            opacity=None,
            size_max=None,
            marginal_x=None,
            marginal_y=None,
            trendline=None,
            trendline_color_override=None,
            log_x=False,
            log_y=False,
            range_x=None,
            range_y=None,
            render_mode="auto",
            title=None,
            template=None,
            width=None,
            height=None,
    ) -> None:
        """
        In a scatter plot, each row of `data_frame` is represented by a symbol
        mark in 2D space.
        https://plotly.com/python-api-reference/generated/plotly.express.scatter.html
        """
        self.type = SupportedFigure.SCATTER
        self.create_payload(locals())

    def line_polar(self,
                   r=None,
                   theta=None,
                   color=None,
                   line_dash=None,
                   hover_name=None,
                   hover_data=None,
                   custom_data=None,
                   line_group=None,
                   text=None,
                   animation_frame=None,
                   animation_group=None,
                   category_orders=None,
                   labels=None,
                   color_discrete_sequence=None,
                   color_discrete_map=None,
                   line_dash_sequence=None,
                   line_dash_map=None,
                   direction="clockwise",
                   start_angle=90,
                   line_close=False,
                   line_shape=None,
                   render_mode="auto",
                   range_r=None,
                   range_theta=None,
                   log_r=False,
                   title=None,
                   template=None,
                   width=None,
                   height=None,
                   ) -> None:
        """
        In a polar line plot, each row of `data_frame` is represented as vertex
        of a polyline mark in polar coordinates.
        https://plotly.com/python-api-reference/generated/plotly.express.line_polar
        """
        self.type = SupportedFigure.LINE_POLAR
        self.create_payload(locals())
