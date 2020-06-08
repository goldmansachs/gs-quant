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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class ComponentType(EnumBase, Enum):    
    
    """Enum listing supported component types"""

    article = 'article'
    assetPlot = 'assetPlot'
    chart = 'chart'
    barChart = 'barChart'
    commentary = 'commentary'
    commentaryPromo = 'commentaryPromo'
    monitor = 'monitor'
    plot = 'plot'
    promo = 'promo'
    rates = 'rates'
    research = 'research'
    separator = 'separator'
    
    def __repr__(self):
        return self.value


class WorkspaceType(EnumBase, Enum):    
    
    """Enum listing support workspace types"""

    cashboard = 'cashboard'
    multiplot = 'multiplot'
    
    def __repr__(self):
        return self.value


class ArticleComponentParameters(Base):
        
    """Parameters provided for a article component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        commentary_to_desktop_link: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header"""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class AssetPlotComponentParameters(Base):
        
    """Parameters provided for a asset plot component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class BarChartComponentParameters(Base):
        
    """Parameters provided for a bar chart component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        hide_legend: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend"""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        


class ChartComponentParameters(Base):
        
    """Parameters provided for a chart component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        hide_legend: bool = None,
        chart_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.chart_name = chart_name
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend"""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        

    @property
    def chart_name(self) -> str:
        """Name of the chart, only if component type is chart"""
        return self.__chart_name

    @chart_name.setter
    def chart_name(self, value: str):
        self._property_changed('chart_name')
        self.__chart_name = value        


class CommentaryComponentParameters(Base):
        
    """Parameters provided for a commentary component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        commentary_to_desktop_link: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header"""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class CommentaryPromoComponentParameters(Base):
        
    """Parameters provided for a commentary promo component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        transparent: bool = None,
        body: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.transparent = transparent
        self.body = body
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background"""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        

    @property
    def body(self) -> str:
        """The body of content to be injected into the promo component type."""
        return self.__body

    @body.setter
    def body(self, value: str):
        self._property_changed('body')
        self.__body = value        


class Entitlements(Base):
        
    """Defines the entitlements of a given resource"""

    @camel_case_translate
    def __init__(
        self,
        view: Tuple[str, ...],
        edit: Tuple[str, ...],
        admin: Tuple[str, ...],
        name: str = None
    ):        
        super().__init__()
        self.view = view
        self.edit = edit
        self.admin = admin
        self.name = name

    @property
    def view(self) -> Tuple[str, ...]:
        """Permission to view the resource and its contents"""
        return self.__view

    @view.setter
    def view(self, value: Tuple[str, ...]):
        self._property_changed('view')
        self.__view = value        

    @property
    def edit(self) -> Tuple[str, ...]:
        """Permission to edit details about the resource content, excluding entitlements.
           Can also delete the resource"""
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[str, ...]):
        self._property_changed('edit')
        self.__edit = value        

    @property
    def admin(self) -> Tuple[str, ...]:
        """Permission to edit all details of the resource, including entitlements. Can also
           delete the resource"""
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[str, ...]):
        self._property_changed('admin')
        self.__admin = value        


class MonitorComponentParameters(Base):
        
    """Parameters provided for a monitor component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class PlotComponentParameters(Base):
        
    """Parameters provided for a plot component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        hide_legend: bool = None,
        plot_frequency_mode: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.plot_frequency_mode = plot_frequency_mode
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend"""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        

    @property
    def plot_frequency_mode(self) -> str:
        """For plot component types, set the plot frequency mode."""
        return self.__plot_frequency_mode

    @plot_frequency_mode.setter
    def plot_frequency_mode(self, value: str):
        self._property_changed('plot_frequency_mode')
        self.__plot_frequency_mode = value        


class PromoComponentParameters(Base):
        
    """Parameters provided for a promo component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        transparent: bool = None,
        body: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.transparent = transparent
        self.body = body
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background"""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        

    @property
    def body(self) -> str:
        """The body of content to be injected into the promo component type."""
        return self.__body

    @body.setter
    def body(self, value: str):
        self._property_changed('body')
        self.__body = value        


class RatesComponentParameters(Base):
        
    """Parameters provided for a rates component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class ResearchComponentParameters(Base):
        
    """Parameters provided for a research component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        tooltip: str = None,
        commentary_channels: Tuple[str, ...] = None,
        commentary_to_desktop_link: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.tooltip = tooltip
        self.commentary_channels = commentary_channels
        self.commentary_to_desktop_link = commentary_to_desktop_link
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed in an info icon next to the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component"""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header"""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class SeparatorComponentParameters(Base):
        
    """Parameters provided for a separator component"""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component on a workspace"""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def name(self) -> str:
        """Name of the component. For example a separator name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class WorkspaceDate(Base):
        
    """Relative date to display at the bottom of the page."""

    @camel_case_translate
    def __init__(
        self,
        days: float,
        text: str,
        name: str = None
    ):        
        super().__init__()
        self.days = days
        self.text = text
        self.name = name

    @property
    def days(self) -> float:
        """Number of days to deduct relative to the current date. For example: 0 days
           represents today."""
        return self.__days

    @days.setter
    def days(self, value: float):
        self._property_changed('days')
        self.__days = value        

    @property
    def text(self) -> str:
        """Text to go next to the date. For example: Data as of."""
        return self.__text

    @text.setter
    def text(self, value: str):
        self._property_changed('text')
        self.__text = value        


class WorkspaceTab(Base):
        
    """Tab represents another workspace that can be linked to."""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str
    ):        
        super().__init__()
        self.__id = id_
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name that appears on the tab."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class WorkspaceComponent(Base):
        
    """Parameters provided for a market workspace"""

    @camel_case_translate
    def __init__(
        self,
        id_: dict,
        type_: Union[ComponentType, str],
        parameters: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.__type = get_enum_value(ComponentType, type_)
        self.parameters = parameters
        self.name = name

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self._property_changed('id')
        self.__id = value        

    @property
    def type(self) -> Union[ComponentType, str]:
        """Enum listing supported component types"""
        return self.__type

    @type.setter
    def type(self, value: Union[ComponentType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ComponentType, value)        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        


class WorkspaceParameters(Base):
        
    """Parameters provided for a market workspace"""

    @camel_case_translate
    def __init__(
        self,
        layout: str,
        components: Tuple[WorkspaceComponent, ...],
        tabs: Tuple[WorkspaceTab, ...] = None,
        disclaimer: str = None,
        date: WorkspaceDate = None,
        name: str = None
    ):        
        super().__init__()
        self.layout = layout
        self.components = components
        self.tabs = tabs
        self.disclaimer = disclaimer
        self.date = date
        self.name = name

    @property
    def layout(self) -> str:
        """A workspace layout expression. For example: r(c12($0))"""
        return self.__layout

    @layout.setter
    def layout(self, value: str):
        self._property_changed('layout')
        self.__layout = value        

    @property
    def components(self) -> Tuple[WorkspaceComponent, ...]:
        """Array of workspace components"""
        return self.__components

    @components.setter
    def components(self, value: Tuple[WorkspaceComponent, ...]):
        self._property_changed('components')
        self.__components = value        

    @property
    def tabs(self) -> Tuple[WorkspaceTab, ...]:
        """Tabs of additional market workspaces that can be linked to."""
        return self.__tabs

    @tabs.setter
    def tabs(self, value: Tuple[WorkspaceTab, ...]):
        self._property_changed('tabs')
        self.__tabs = value        

    @property
    def disclaimer(self) -> str:
        """Disclaimer that applies directly to the whole workspace displayed at the bottom."""
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: str):
        self._property_changed('disclaimer')
        self.__disclaimer = value        

    @property
    def date(self) -> WorkspaceDate:
        """Relative date to display at the bottom of the page."""
        return self.__date

    @date.setter
    def date(self, value: WorkspaceDate):
        self._property_changed('date')
        self.__date = value        


class Workspace(Base):
        
    """A market workspace object"""

    @camel_case_translate
    def __init__(
        self,
        parameters: WorkspaceParameters,
        type_: Union[WorkspaceType, str],
        id_: str = None,
        alias: str = None,
        name: str = None,
        tags: Tuple[str, ...] = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        owner_id: str = None,
        entitlements: Entitlements = None,
        folder_name: str = None,
        description: str = None,
        children_ids: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.alias = alias
        self.name = name
        self.__type = get_enum_value(WorkspaceType, type_)
        self.tags = tags
        self.parameters = parameters
        self.created_time = created_time
        self.last_updated_time = last_updated_time
        self.created_by_id = created_by_id
        self.last_updated_by_id = last_updated_by_id
        self.owner_id = owner_id
        self.entitlements = entitlements
        self.folder_name = folder_name
        self.description = description
        self.children_ids = children_ids

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def alias(self) -> str:
        """Market workspace alias"""
        return self.__alias

    @alias.setter
    def alias(self, value: str):
        self._property_changed('alias')
        self.__alias = value        

    @property
    def name(self) -> str:
        """Market workspace name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def type(self) -> Union[WorkspaceType, str]:
        """Enum listing support workspace types"""
        return self.__type

    @type.setter
    def type(self, value: Union[WorkspaceType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(WorkspaceType, value)        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Array of tags"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def parameters(self) -> WorkspaceParameters:
        """Parameters provided for a market workspace"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: WorkspaceParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier"""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource"""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def folder_name(self) -> str:
        """Folder name of the monitor"""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def description(self) -> str:
        """Market workspace description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def children_ids(self) -> Tuple[str, ...]:
        """Child workspaces for navigation"""
        return self.__children_ids

    @children_ids.setter
    def children_ids(self, value: Tuple[str, ...]):
        self._property_changed('children_ids')
        self.__children_ids = value        
