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
    screener = 'screener'
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


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ComponentSelection(Base):
    selector_id: str = field(default=None, metadata=field_metadata)
    tag: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContainerComponentParameters(Base):
    component_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LegendItem(Base):
    color: str = field(default=None, metadata=field_metadata)
    icon: str = field(default=None, metadata=field_metadata)
    name: str = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class NotificationTokenBody(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PromoComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    transparent: Optional[bool] = field(default=None, metadata=field_metadata)
    body: Optional[str] = field(default=None, metadata=field_metadata)
    size: Optional[str] = field(default=None, metadata=field_metadata)
    hide_border: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SeparatorComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    size: Optional[str] = field(default=None, metadata=field_metadata)
    show_more_url: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class VideoComponentParameters(Base):
    replay_url: str = field(default=None, metadata=field_metadata)
    date: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    height: Optional[float] = field(default=None, metadata=field_metadata)
    title: Optional[str] = field(default=None, metadata=field_metadata)
    transparent: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WebinarProvider(Base):
    url: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WebinarSpeaker(Base):
    name: str = field(default=None, metadata=field_metadata)
    title: str = field(default=None, metadata=field_metadata)
    author_url: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceDate(Base):
    days: float = field(default=None, metadata=field_metadata)
    text: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceTab(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ArticleComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    commentary_channels: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    commentary_to_desktop_link: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetPlotComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BarChartComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    hide_legend: Optional[bool] = field(default=None, metadata=field_metadata)
    chart_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChartComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    ids: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    hide_legend: Optional[bool] = field(default=None, metadata=field_metadata)
    chart_name: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommentaryComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    commentary_channels: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    commentary_to_desktop_link: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommentaryPromoComponentParameters(Base):
    height: Optional[float] = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    commentary_channels: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    transparent: Optional[bool] = field(default=None, metadata=field_metadata)
    body: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DataGridComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class LegendComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    items: Tuple[LegendItem, ...] = field(default=None, metadata=field_metadata)
    position: Optional[str] = field(default=None, metadata=field_metadata)
    transparent: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MonitorComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class NotificationTokens(Base):
    tokens: NotificationTokenBody = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class PlotComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    hide_legend: Optional[bool] = field(default=None, metadata=field_metadata)
    plot_frequency_mode: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ResearchComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    commentary_channels: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    commentary_to_desktop_link: Optional[bool] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ScreenerComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SelectorComponentOption(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class TreemapComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WebinarComponentParameters(Base):
    date: str = field(default=None, metadata=field_metadata)
    date_text: str = field(default=None, metadata=field_metadata)
    description: str = field(default=None, metadata=field_metadata)
    provider: WebinarProvider = field(default=None, metadata=field_metadata)
    replay_url: str = field(default=None, metadata=field_metadata)
    title: str = field(default=None, metadata=field_metadata)
    height: Optional[float] = field(default=None, metadata=field_metadata)
    hosts: Optional[Tuple[WebinarSpeaker, ...]] = field(default=None, metadata=field_metadata)
    password: Optional[str] = field(default=None, metadata=field_metadata)
    series: Optional[str] = field(default=None, metadata=field_metadata)
    speakers: Optional[Tuple[WebinarSpeaker, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RelatedLink(Base):
    type_: str = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    name: str = field(default=None, metadata=field_metadata)
    link: str = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    notification_properties: Optional[NotificationTokens] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class SelectorComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    container_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    default_option_index: Optional[float] = field(default=None, metadata=field_metadata)
    options: Optional[Tuple[SelectorComponentOption, ...]] = field(default=None, metadata=field_metadata)
    title: Optional[str] = field(default=None, metadata=field_metadata)
    tooltip: Optional[str] = field(default=None, metadata=field_metadata)
    width: Optional[float] = field(default=None, metadata=field_metadata)
    parent_selector_id: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class RelatedLinksComponentParameters(Base):
    height: float = field(default=None, metadata=field_metadata)
    links: Tuple[RelatedLink, ...] = field(default=None, metadata=field_metadata)
    title: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceCallToAction(Base):
    actions: Tuple[RelatedLink, ...] = field(default=None, metadata=field_metadata)
    text: str = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceComponent(Base):
    id_: str = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    type_: ComponentType = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    hide: Optional[bool] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    selections: Optional[Tuple[ComponentSelection, ...]] = field(default=None, metadata=field_metadata)
    container_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    parameters: Optional[DictBase] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class WorkspaceParameters(Base):
    layout: str = field(default=None, metadata=field_metadata)
    components: Tuple[WorkspaceComponent, ...] = field(default=None, metadata=field_metadata)
    call_to_action: Optional[WorkspaceCallToAction] = field(default=None, metadata=field_metadata)
    can_share: Optional[bool] = field(default=None, metadata=field_metadata)
    date: Optional[WorkspaceDate] = field(default=None, metadata=field_metadata)
    disclaimer: Optional[str] = field(default=None, metadata=field_metadata)
    maintainers: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    tabs: Optional[Tuple[WorkspaceTab, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Workspace(Base):
    parameters: WorkspaceParameters = field(default=None, metadata=field_metadata)
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    alias: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    type_: Optional[WorkspaceType] = field(default=None, metadata=config(field_name='type', exclude=exclude_none))
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    last_updated_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    owner_id: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    folder_name: Optional[str] = field(default=None, metadata=field_metadata)
    description: Optional[str] = field(default=None, metadata=field_metadata)
    children_aliases: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
