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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from enum import Enum


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
    empty = 'empty'
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


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ComponentSelection(Base):
    selector_id: str = None
    tag: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContainerComponentParameters(Base):
    component_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LegendItem(Base):
    color: str = None
    icon: str = None
    name: str = None
    tooltip: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketComponentParameters(Base):
    height: float = None


class NotificationTokenBody(DictBase):
    pass


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PromoComponentParameters(Base):
    height: float = None
    transparent: Optional[bool] = None
    body: Optional[str] = None
    size: Optional[str] = None
    hide_border: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SeparatorComponentParameters(Base):
    height: float = None
    name: Optional[str] = None
    size: Optional[str] = None
    show_more_url: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VideoComponentParameters(Base):
    replay_url: str = None
    date: Optional[str] = None
    description: Optional[str] = None
    height: Optional[float] = None
    title: Optional[str] = None
    transparent: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WebinarProvider(Base):
    url: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WebinarSpeaker(Base):
    name: str = None
    title: str = None
    author_url: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceDate(Base):
    days: float = None
    text: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceTab(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ArticleComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None
    commentary_channels: Optional[Tuple[str, ...]] = None
    commentary_to_desktop_link: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetPlotComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BarChartComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None
    hide_legend: Optional[bool] = None
    chart_name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartComponentParameters(Base):
    height: float = None
    ids: Tuple[str, ...] = None
    tooltip: Optional[str] = None
    hide_legend: Optional[bool] = None
    chart_name: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommentaryComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None
    commentary_channels: Optional[Tuple[str, ...]] = None
    commentary_to_desktop_link: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommentaryPromoComponentParameters(Base):
    height: Optional[float] = None
    tooltip: Optional[str] = None
    commentary_channels: Optional[Tuple[str, ...]] = None
    transparent: Optional[bool] = None
    body: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataGridComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LegendComponentParameters(Base):
    height: float = None
    items: Tuple[LegendItem, ...] = None
    position: Optional[str] = None
    transparent: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class NotificationTokens(Base):
    tokens: NotificationTokenBody = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PlotComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None
    hide_legend: Optional[bool] = None
    plot_frequency_mode: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ResearchComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None
    commentary_channels: Optional[Tuple[str, ...]] = None
    commentary_to_desktop_link: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SelectorComponentOption(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    name: str = None
    tags: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TreemapComponentParameters(Base):
    height: float = None
    tooltip: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WebinarComponentParameters(Base):
    date: str = None
    date_text: str = None
    description: str = None
    provider: WebinarProvider = None
    replay_url: str = None
    title: str = None
    height: Optional[float] = None
    hosts: Optional[Tuple[WebinarSpeaker, ...]] = None
    password: Optional[str] = None
    series: Optional[str] = None
    speakers: Optional[Tuple[WebinarSpeaker, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RelatedLink(Base):
    type_: str = field(default=None, metadata=config(field_name='type'))
    name: str = None
    link: str = None
    description: Optional[str] = None
    notification_properties: Optional[NotificationTokens] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SelectorComponentParameters(Base):
    height: float = None
    container_ids: Optional[Tuple[str, ...]] = None
    default_option_index: Optional[float] = None
    options: Optional[Tuple[SelectorComponentOption, ...]] = None
    title: Optional[str] = None
    tooltip: Optional[str] = None
    width: Optional[float] = None
    parent_selector_id: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RelatedLinksComponentParameters(Base):
    height: float = None
    links: Tuple[RelatedLink, ...] = None
    title: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceCallToAction(Base):
    actions: Tuple[RelatedLink, ...] = None
    text: str = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceComponent(Base):
    id_: str = field(default=None, metadata=config(field_name='id'))
    type_: ComponentType = field(default=None, metadata=config(field_name='type'))
    hide: Optional[bool] = None
    tags: Optional[Tuple[str, ...]] = None
    selections: Optional[Tuple[ComponentSelection, ...]] = None
    container_ids: Optional[Tuple[str, ...]] = None
    parameters: Optional[DictBase] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceParameters(Base):
    layout: str = None
    components: Tuple[WorkspaceComponent, ...] = None
    call_to_action: Optional[WorkspaceCallToAction] = None
    can_share: Optional[bool] = None
    date: Optional[WorkspaceDate] = None
    disclaimer: Optional[str] = None
    maintainers: Optional[Tuple[str, ...]] = None
    tabs: Optional[Tuple[WorkspaceTab, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Workspace(Base):
    parameters: WorkspaceParameters = None
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    alias: Optional[str] = None
    name: Optional[str] = None
    type_: Optional[WorkspaceType] = field(default=None, metadata=config(field_name='type'))
    tags: Optional[Tuple[str, ...]] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    created_by_id: Optional[str] = None
    last_updated_by_id: Optional[str] = None
    owner_id: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    folder_name: Optional[str] = None
    description: Optional[str] = None
    children_aliases: Optional[Tuple[str, ...]] = None
