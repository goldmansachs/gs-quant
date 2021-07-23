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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class ComponentType(EnumBase, Enum):    
    
    """Enum listing supported component types."""

    article = 'article'
    assetPlot = 'assetPlot'
    chart = 'chart'
    barChart = 'barChart'
    commentary = 'commentary'
    commentaryPromo = 'commentaryPromo'
    container = 'container'
    datagrid = 'datagrid'
    dataviz = 'dataviz'
    legend = 'legend'
    market = 'market'
    monitor = 'monitor'
    plot = 'plot'
    promo = 'promo'
    rates = 'rates'
    relatedLinks = 'relatedLinks'
    research = 'research'
    selector = 'selector'
    separator = 'separator'
    stackedBarChart = 'stackedBarChart'
    treemap = 'treemap'
    video = 'video'
    webinar = 'webinar'    


class WorkspaceType(EnumBase, Enum):    
    
    """Enum listing support workspace types."""

    cashboard = 'cashboard'
    multiplot = 'multiplot'
    study = 'study'    


class ComponentSelection(Base):
        
    """Available selections for a particular component."""

    @camel_case_translate
    def __init__(
        self,
        selector_id: str,
        tag: str,
        name: str = None
    ):        
        super().__init__()
        self.selector_id = selector_id
        self.tag = tag
        self.name = name

    @property
    def selector_id(self) -> str:
        """Selector ID to use."""
        return self.__selector_id

    @selector_id.setter
    def selector_id(self, value: str):
        self._property_changed('selector_id')
        self.__selector_id = value        

    @property
    def tag(self) -> str:
        """Tag id to match in selector."""
        return self.__tag

    @tag.setter
    def tag(self, value: str):
        self._property_changed('tag')
        self.__tag = value        


class ContainerComponentParameters(Base):
        
    """Parameters provided for a container component."""

    @camel_case_translate
    def __init__(
        self,
        component_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.component_id = component_id
        self.name = name

    @property
    def component_id(self) -> str:
        """The identifier of the component that the container will initially render."""
        return self.__component_id

    @component_id.setter
    def component_id(self, value: str):
        self._property_changed('component_id')
        self.__component_id = value        


class LegendItem(Base):
        
    """Parameters provided for a legend item."""

    @camel_case_translate
    def __init__(
        self,
        color: str,
        icon: str,
        name: str,
        tooltip: str = None
    ):        
        super().__init__()
        self.color = color
        self.icon = icon
        self.name = name
        self.tooltip = tooltip

    @property
    def color(self) -> str:
        """Hex color of the legend item. i.e. #FF0000"""
        return self.__color

    @color.setter
    def color(self, value: str):
        self._property_changed('color')
        self.__color = value        

    @property
    def icon(self) -> str:
        """Icon of the legend. i.e. Circle or Square."""
        return self.__icon

    @icon.setter
    def icon(self, value: str):
        self._property_changed('icon')
        self.__icon = value        

    @property
    def name(self) -> str:
        """Name of the legend item."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def tooltip(self) -> str:
        """Tooltip for the legend item."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class MarketComponentParameters(Base):
        
    """Parameters provided for a market component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        


class NotificationTokenBody(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class PromoComponentParameters(Base):
        
    """Parameters provided for a promo component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        transparent: bool = None,
        body: str = None,
        size: str = None,
        hide_border: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.transparent = transparent
        self.body = body
        self.size = size
        self.hide_border = hide_border
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background."""
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

    @property
    def size(self) -> str:
        """Represents the size of the text for the promo component."""
        return self.__size

    @size.setter
    def size(self, value: str):
        self._property_changed('size')
        self.__size = value        

    @property
    def hide_border(self) -> bool:
        """Whether or not to hide the border of the card."""
        return self.__hide_border

    @hide_border.setter
    def hide_border(self, value: bool):
        self._property_changed('hide_border')
        self.__hide_border = value        


class SeparatorComponentParameters(Base):
        
    """Parameters provided for a separator component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        name: str = None,
        size: str = None,
        show_more_url: str = None
    ):        
        super().__init__()
        self.height = height
        self.name = name
        self.size = size
        self.show_more_url = show_more_url

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def name(self) -> str:
        """Name of the component. For example a separator name."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def size(self) -> str:
        """Represents the size of the text for the separator component."""
        return self.__size

    @size.setter
    def size(self, value: str):
        self._property_changed('size')
        self.__size = value        

    @property
    def show_more_url(self) -> str:
        """Show more link on the component header. Provide absolute or relative url."""
        return self.__show_more_url

    @show_more_url.setter
    def show_more_url(self, value: str):
        self._property_changed('show_more_url')
        self.__show_more_url = value        


class VideoComponentParameters(Base):
        
    """Parameters provided for a video component."""

    @camel_case_translate
    def __init__(
        self,
        replay_url: str,
        date: str = None,
        description: str = None,
        height: float = None,
        title: str = None,
        transparent: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.description = description
        self.height = height
        self.replay_url = replay_url
        self.title = title
        self.transparent = transparent
        self.name = name

    @property
    def date(self) -> str:
        """ISO 8601 Formatted datetime string for when the video will be hosted."""
        return self.__date

    @date.setter
    def date(self, value: str):
        self._property_changed('date')
        self.__date = value        

    @property
    def description(self) -> str:
        """Description of video."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def replay_url(self) -> str:
        """URL for the replay of the video."""
        return self.__replay_url

    @replay_url.setter
    def replay_url(self, value: str):
        self._property_changed('replay_url')
        self.__replay_url = value        

    @property
    def title(self) -> str:
        """Title of the video."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background."""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        


class WebinarProvider(Base):
        
    """The provider of the webinar."""

    @camel_case_translate
    def __init__(
        self,
        url: str,
        name: str = None
    ):        
        super().__init__()
        self.url = url
        self.name = name

    @property
    def url(self) -> str:
        """Url for the the webinar."""
        return self.__url

    @url.setter
    def url(self, value: str):
        self._property_changed('url')
        self.__url = value        


class WebinarSpeaker(Base):
        
    """A speaker or host of a webinar."""

    @camel_case_translate
    def __init__(
        self,
        name: str,
        title: str,
        author_url: str = None
    ):        
        super().__init__()
        self.author_url = author_url
        self.name = name
        self.title = title

    @property
    def author_url(self) -> str:
        """A url to the speaker or hosts webpage."""
        return self.__author_url

    @author_url.setter
    def author_url(self, value: str):
        self._property_changed('author_url')
        self.__author_url = value        

    @property
    def name(self) -> str:
        """Name of the speaker or host."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def title(self) -> str:
        """Title of the speaker or host."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        


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
        """Workspace unique identifier that starts with CB followed by 16 alphanumeric
           characters."""
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


class ArticleComponentParameters(Base):
        
    """Parameters provided for a article component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Channels to subscribe for articles."""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header."""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class AssetPlotComponentParameters(Base):
        
    """Parameters provided for a asset plot component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class BarChartComponentParameters(Base):
        
    """Parameters provided for a bar chart component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend."""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        

    @property
    def chart_name(self) -> str:
        """Name of the chart."""
        return self.__chart_name

    @chart_name.setter
    def chart_name(self, value: str):
        self._property_changed('chart_name')
        self.__chart_name = value        


class ChartComponentParameters(Base):
        
    """Parameters provided for a chart component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        ids: Tuple[str, ...],
        tooltip: str = None,
        hide_legend: bool = None,
        chart_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.ids = ids
        self.tooltip = tooltip
        self.hide_legend = hide_legend
        self.chart_name = chart_name
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def ids(self) -> Tuple[str, ...]:
        """List of monitor ids. One for each series."""
        return self.__ids

    @ids.setter
    def ids(self, value: Tuple[str, ...]):
        self._property_changed('ids')
        self.__ids = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend."""
        return self.__hide_legend

    @hide_legend.setter
    def hide_legend(self, value: bool):
        self._property_changed('hide_legend')
        self.__hide_legend = value        

    @property
    def chart_name(self) -> str:
        """Name of the chart, only if component type is chart."""
        return self.__chart_name

    @chart_name.setter
    def chart_name(self, value: str):
        self._property_changed('chart_name')
        self.__chart_name = value        


class CommentaryComponentParameters(Base):
        
    """Parameters provided for a commentary component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component."""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header."""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class CommentaryPromoComponentParameters(Base):
        
    """Parameters provided for a commentary promo component."""

    @camel_case_translate
    def __init__(
        self,
        height: float = None,
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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component."""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background."""
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


class DataGridComponentParameters(Base):
        
    """Parameters provided for a datagrid component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class LegendComponentParameters(Base):
        
    """Parameters provided for the legend component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        items: Tuple[LegendItem, ...],
        position: str = None,
        transparent: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.items = items
        self.position = position
        self.transparent = transparent
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def items(self) -> Tuple[LegendItem, ...]:
        """The legend items displayed in the component."""
        return self.__items

    @items.setter
    def items(self, value: Tuple[LegendItem, ...]):
        self._property_changed('items')
        self.__items = value        

    @property
    def position(self) -> str:
        """Whether or not to position the legend items on the left or right."""
        return self.__position

    @position.setter
    def position(self, value: str):
        self._property_changed('position')
        self.__position = value        

    @property
    def transparent(self) -> bool:
        """Sets the component card to have a transparent background."""
        return self.__transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._property_changed('transparent')
        self.__transparent = value        


class MonitorComponentParameters(Base):
        
    """Parameters provided for a monitor component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class NotificationTokens(Base):
        
    """The required tokens to render the template to be sent."""

    @camel_case_translate
    def __init__(
        self,
        tokens: NotificationTokenBody,
        name: str = None
    ):        
        super().__init__()
        self.tokens = tokens
        self.name = name

    @property
    def tokens(self) -> NotificationTokenBody:
        return self.__tokens

    @tokens.setter
    def tokens(self, value: NotificationTokenBody):
        self._property_changed('tokens')
        self.__tokens = value        


class PlotComponentParameters(Base):
        
    """Parameters provided for a plot component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def hide_legend(self) -> bool:
        """Whether to hide a chart or plot component legend."""
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


class ResearchComponentParameters(Base):
        
    """Parameters provided for a research component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def commentary_channels(self) -> Tuple[str, ...]:
        """Optional channels associated with a commentary component."""
        return self.__commentary_channels

    @commentary_channels.setter
    def commentary_channels(self, value: Tuple[str, ...]):
        self._property_changed('commentary_channels')
        self.__commentary_channels = value        

    @property
    def commentary_to_desktop_link(self) -> bool:
        """Whether or not to display a link from commentary to desktop in the header."""
        return self.__commentary_to_desktop_link

    @commentary_to_desktop_link.setter
    def commentary_to_desktop_link(self, value: bool):
        self._property_changed('commentary_to_desktop_link')
        self.__commentary_to_desktop_link = value        


class SelectorComponentOption(Base):
        
    """A selector component option."""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.__id = id_
        self.name = name
        self.tags = tags

    @property
    def id(self) -> str:
        """A unique id of the selector option."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name of the option in the dropdown. This will be the text displayed in the
           dropdown."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """An array of component tags for this selector option. This should match in length
           the selector component containerIds length."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        


class TreemapComponentParameters(Base):
        
    """Parameters provided for a treemap component."""

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
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        


class WebinarComponentParameters(Base):
        
    """Parameters provided for a webinar component."""

    @camel_case_translate
    def __init__(
        self,
        date: str,
        date_text: str,
        description: str,
        provider: WebinarProvider,
        replay_url: str,
        title: str,
        height: float = None,
        hosts: Tuple[WebinarSpeaker, ...] = None,
        password: str = None,
        series: str = None,
        speakers: Tuple[WebinarSpeaker, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.date = date
        self.date_text = date_text
        self.description = description
        self.height = height
        self.hosts = hosts
        self.password = password
        self.provider = provider
        self.replay_url = replay_url
        self.series = series
        self.speakers = speakers
        self.title = title
        self.name = name

    @property
    def date(self) -> str:
        """ISO 8601 Formatted datetime string for when the webinar will be hosted."""
        return self.__date

    @date.setter
    def date(self, value: str):
        self._property_changed('date')
        self.__date = value        

    @property
    def date_text(self) -> str:
        """A custom date string to display on the webinar card, for example 01 Oct 2020
           6:00PM (ET)."""
        return self.__date_text

    @date_text.setter
    def date_text(self, value: str):
        self._property_changed('date_text')
        self.__date_text = value        

    @property
    def description(self) -> str:
        """Description of webinar."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def hosts(self) -> Tuple[WebinarSpeaker, ...]:
        """List of hosts for the webinar."""
        return self.__hosts

    @hosts.setter
    def hosts(self, value: Tuple[WebinarSpeaker, ...]):
        self._property_changed('hosts')
        self.__hosts = value        

    @property
    def password(self) -> str:
        """Password for the webinar."""
        return self.__password

    @password.setter
    def password(self, value: str):
        self._property_changed('password')
        self.__password = value        

    @property
    def provider(self) -> WebinarProvider:
        """The provider of the webinar."""
        return self.__provider

    @provider.setter
    def provider(self, value: WebinarProvider):
        self._property_changed('provider')
        self.__provider = value        

    @property
    def replay_url(self) -> str:
        """URL for the replay of the webinar."""
        return self.__replay_url

    @replay_url.setter
    def replay_url(self, value: str):
        self._property_changed('replay_url')
        self.__replay_url = value        

    @property
    def series(self) -> str:
        """Name of the series of the webinar."""
        return self.__series

    @series.setter
    def series(self, value: str):
        self._property_changed('series')
        self.__series = value        

    @property
    def speakers(self) -> Tuple[WebinarSpeaker, ...]:
        """List of speakers for the webinar."""
        return self.__speakers

    @speakers.setter
    def speakers(self, value: Tuple[WebinarSpeaker, ...]):
        self._property_changed('speakers')
        self.__speakers = value        

    @property
    def title(self) -> str:
        """Title of the webinar."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        


class RelatedLink(Base):
        
    """Parameters provided for a related link."""

    @camel_case_translate
    def __init__(
        self,
        type_: str,
        name: str,
        link: str,
        description: str = None,
        notification_properties: NotificationTokens = None
    ):        
        super().__init__()
        self.__type = type_
        self.description = description
        self.link = link
        self.name = name
        self.notification_properties = notification_properties

    @property
    def type(self) -> str:
        """Type of related link."""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def description(self) -> str:
        """Description of related link."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def link(self) -> str:
        """URL of related link, notification ID or component ID to scroll to."""
        return self.__link

    @link.setter
    def link(self, value: str):
        self._property_changed('link')
        self.__link = value        

    @property
    def name(self) -> str:
        """Name to be displayed."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def notification_properties(self) -> NotificationTokens:
        """The required tokens to render the template to be sent."""
        return self.__notification_properties

    @notification_properties.setter
    def notification_properties(self, value: NotificationTokens):
        self._property_changed('notification_properties')
        self.__notification_properties = value        


class SelectorComponentParameters(Base):
        
    """Parameters provided for a selector component."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        container_ids: Tuple[str, ...] = None,
        default_option_index: float = None,
        options: Tuple[SelectorComponentOption, ...] = None,
        title: str = None,
        tooltip: str = None,
        width: float = None,
        parent_selector_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.container_ids = container_ids
        self.default_option_index = default_option_index
        self.height = height
        self.options = options
        self.title = title
        self.tooltip = tooltip
        self.width = width
        self.parent_selector_id = parent_selector_id
        self.name = name

    @property
    def container_ids(self) -> Tuple[str, ...]:
        """The component ids of the containers the selector will fill using it's options."""
        return self.__container_ids

    @container_ids.setter
    def container_ids(self, value: Tuple[str, ...]):
        self._property_changed('container_ids')
        self.__container_ids = value        

    @property
    def default_option_index(self) -> float:
        """The default option for the selector. This references the index in the options
           array. Defaults to 0."""
        return self.__default_option_index

    @default_option_index.setter
    def default_option_index(self, value: float):
        self._property_changed('default_option_index')
        self.__default_option_index = value        

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def options(self) -> Tuple[SelectorComponentOption, ...]:
        """A list of options for the selector dropdown. Options references other components
           in the workspace."""
        return self.__options

    @options.setter
    def options(self, value: Tuple[SelectorComponentOption, ...]):
        self._property_changed('options')
        self.__options = value        

    @property
    def title(self) -> str:
        """Title of the text to the left of the selector component."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def tooltip(self) -> str:
        """Tooltip that is displayed when hovering mouse on the component title."""
        return self.__tooltip

    @tooltip.setter
    def tooltip(self, value: str):
        self._property_changed('tooltip')
        self.__tooltip = value        

    @property
    def width(self) -> float:
        """Used for restricting the width in pixels of the component on a workspace.
           Defaults to 280px."""
        return self.__width

    @width.setter
    def width(self, value: float):
        self._property_changed('width')
        self.__width = value        

    @property
    def parent_selector_id(self) -> str:
        """Id of the parent selector. Used for multi-selectors ony."""
        return self.__parent_selector_id

    @parent_selector_id.setter
    def parent_selector_id(self, value: str):
        self._property_changed('parent_selector_id')
        self.__parent_selector_id = value        


class RelatedLinksComponentParameters(Base):
        
    """Parameters provided for a related link components."""

    @camel_case_translate
    def __init__(
        self,
        height: float,
        links: Tuple[RelatedLink, ...],
        title: str,
        name: str = None
    ):        
        super().__init__()
        self.height = height
        self.links = links
        self.title = title
        self.name = name

    @property
    def height(self) -> float:
        """Used for restricting the height in pixels of the component."""
        return self.__height

    @height.setter
    def height(self, value: float):
        self._property_changed('height')
        self.__height = value        

    @property
    def links(self) -> Tuple[RelatedLink, ...]:
        """Description associated with link."""
        return self.__links

    @links.setter
    def links(self, value: Tuple[RelatedLink, ...]):
        self._property_changed('links')
        self.__links = value        

    @property
    def title(self) -> str:
        """Title of the related link component."""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        


class WorkspaceCallToAction(Base):
        
    """Call to action displayed on the top right of the page."""

    @camel_case_translate
    def __init__(
        self,
        actions: Tuple[RelatedLink, ...],
        text: str,
        name: str = None
    ):        
        super().__init__()
        self.actions = actions
        self.text = text
        self.name = name

    @property
    def actions(self) -> Tuple[RelatedLink, ...]:
        """Call to action in the call to actions list."""
        return self.__actions

    @actions.setter
    def actions(self, value: Tuple[RelatedLink, ...]):
        self._property_changed('actions')
        self.__actions = value        

    @property
    def text(self) -> str:
        """Text to go on the call to action button."""
        return self.__text

    @text.setter
    def text(self, value: str):
        self._property_changed('text')
        self.__text = value        


class WorkspaceComponent(Base):
        
    """Parameters provided for a market workspace."""

    @camel_case_translate
    def __init__(
        self,
        id_: str,
        type_: Union[ComponentType, str],
        hide: bool = None,
        tags: Tuple[str, ...] = None,
        selections: Tuple[ComponentSelection, ...] = None,
        container_ids: Tuple[str, ...] = None,
        parameters: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.hide = hide
        self.tags = tags
        self.__type = get_enum_value(ComponentType, type_)
        self.selections = selections
        self.container_ids = container_ids
        self.parameters = parameters
        self.name = name

    @property
    def id(self) -> str:
        """Workspace unique identifier that starts with CB followed by 16 alphanumeric
           characters."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def hide(self) -> bool:
        """Whether to hide the component."""
        return self.__hide

    @hide.setter
    def hide(self, value: bool):
        self._property_changed('hide')
        self.__hide = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """An array of component tags for this component. Tags are referenced by other
           components within the workspace."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def type(self) -> Union[ComponentType, str]:
        """Enum listing supported component types."""
        return self.__type

    @type.setter
    def type(self, value: Union[ComponentType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(ComponentType, value)        

    @property
    def selections(self) -> Tuple[ComponentSelection, ...]:
        """List of available selections for a particular component."""
        return self.__selections

    @selections.setter
    def selections(self, value: Tuple[ComponentSelection, ...]):
        self._property_changed('selections')
        self.__selections = value        

    @property
    def container_ids(self) -> Tuple[str, ...]:
        """The component ids of the containers the selector will fill using it's options."""
        return self.__container_ids

    @container_ids.setter
    def container_ids(self, value: Tuple[str, ...]):
        self._property_changed('container_ids')
        self.__container_ids = value        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        


class WorkspaceParameters(Base):
        
    """Parameters provided for a market workspace."""

    @camel_case_translate
    def __init__(
        self,
        layout: str,
        components: Tuple[WorkspaceComponent, ...],
        call_to_action: WorkspaceCallToAction = None,
        can_share: bool = None,
        date: WorkspaceDate = None,
        disclaimer: str = None,
        maintainers: Tuple[str, ...] = None,
        tabs: Tuple[WorkspaceTab, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.call_to_action = call_to_action
        self.can_share = can_share
        self.components = components
        self.date = date
        self.disclaimer = disclaimer
        self.layout = layout
        self.maintainers = maintainers
        self.tabs = tabs
        self.name = name

    @property
    def call_to_action(self) -> WorkspaceCallToAction:
        """Call to action displayed on the top right of the page."""
        return self.__call_to_action

    @call_to_action.setter
    def call_to_action(self, value: WorkspaceCallToAction):
        self._property_changed('call_to_action')
        self.__call_to_action = value        

    @property
    def can_share(self) -> bool:
        """ whether the user has the ability to share a cashboard."""
        return self.__can_share

    @can_share.setter
    def can_share(self, value: bool):
        self._property_changed('can_share')
        self.__can_share = value        

    @property
    def components(self) -> Tuple[WorkspaceComponent, ...]:
        """Array of workspace components."""
        return self.__components

    @components.setter
    def components(self, value: Tuple[WorkspaceComponent, ...]):
        self._property_changed('components')
        self.__components = value        

    @property
    def date(self) -> WorkspaceDate:
        """Relative date to display at the bottom of the page."""
        return self.__date

    @date.setter
    def date(self, value: WorkspaceDate):
        self._property_changed('date')
        self.__date = value        

    @property
    def disclaimer(self) -> str:
        """Disclaimer that applies directly to the whole workspace displayed at the bottom."""
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: str):
        self._property_changed('disclaimer')
        self.__disclaimer = value        

    @property
    def layout(self) -> str:
        """A workspace layout expression. For example: r(c12($0))"""
        return self.__layout

    @layout.setter
    def layout(self, value: str):
        self._property_changed('layout')
        self.__layout = value        

    @property
    def maintainers(self) -> Tuple[str, ...]:
        """User Ids of the markets workspace maintainers."""
        return self.__maintainers

    @maintainers.setter
    def maintainers(self, value: Tuple[str, ...]):
        self._property_changed('maintainers')
        self.__maintainers = value        

    @property
    def tabs(self) -> Tuple[WorkspaceTab, ...]:
        """Tabs of additional market workspaces that can be linked to."""
        return self.__tabs

    @tabs.setter
    def tabs(self, value: Tuple[WorkspaceTab, ...]):
        self._property_changed('tabs')
        self.__tabs = value        


class Workspace(Base):
        
    """A market workspace object."""

    @camel_case_translate
    def __init__(
        self,
        parameters: WorkspaceParameters,
        id_: str = None,
        alias: str = None,
        name: str = None,
        type_: Union[WorkspaceType, str] = None,
        tags: Tuple[str, ...] = None,
        created_time: datetime.datetime = None,
        last_updated_time: datetime.datetime = None,
        created_by_id: str = None,
        last_updated_by_id: str = None,
        owner_id: str = None,
        entitlements: Entitlements = None,
        folder_name: str = None,
        description: str = None,
        children_aliases: Tuple[str, ...] = None
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
        self.children_aliases = children_aliases

    @property
    def id(self) -> str:
        """Workspace unique identifier that starts with CB followed by 16 alphanumeric
           characters."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def alias(self) -> str:
        """Configurable unique identifier for a Workspace. Allows user to choose the URL
           for the Workspace, i.e. https://marquee.gs.com/s/markets/{alias}."""
        return self.__alias

    @alias.setter
    def alias(self, value: str):
        self._property_changed('alias')
        self.__alias = value        

    @property
    def name(self) -> str:
        """Workspace name that is shown as the title on the UI."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def type(self) -> Union[WorkspaceType, str]:
        """Enum listing support workspace types."""
        return self.__type

    @type.setter
    def type(self, value: Union[WorkspaceType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(WorkspaceType, value)        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Array of strings that can be queried."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def parameters(self) -> WorkspaceParameters:
        """Parameters provided for a market workspace."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: WorkspaceParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
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
        """Marquee unique identifier of a user."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def folder_name(self) -> str:
        """Folder name of the workspace."""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def description(self) -> str:
        """Workspace description that is displayed under the workspace title on the UI."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def children_aliases(self) -> Tuple[str, ...]:
        """Child workspaces for navigation."""
        return self.__children_aliases

    @children_aliases.setter
    def children_aliases(self, value: Tuple[str, ...]):
        self._property_changed('children_aliases')
        self.__children_aliases = value        
