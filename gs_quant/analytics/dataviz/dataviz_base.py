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

import json
import webbrowser
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Union, Dict, List, Optional

from gs_quant.entities.entitlements import Entitlements
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.session import GsSession
from gs_quant.target.common import Entitlements as Entitlements_

API = '/data/visualizations'
HEADERS: Dict[str, str] = {'Content-Type': 'application/json;charset=utf-8'}
DATAVIZ_ENTITY_PROPS = ["id", "name", "type", "classname", "sources", "parameters"]


class DataVizSourceType(Enum):
    DATAGRID = 'datagrid'
    HEADER = 'header'
    TEMPLATE = 'template'


@dataclass
class DataVizSource:
    """
    Dataclass to specify the Visualization source used in the Entity.
    """
    type: DataVizSourceType
    id: str = None
    alias: str = None

    def as_dict(self):
        obj = {
            'type': self.type.value
        }
        if self.id:
            obj['id'] = self.id
        if self.alias:
            obj['alias'] = self.alias
        return obj


class SupportedFigure(Enum):
    BAR = 'bar'
    LINE = 'line'
    LINE_POLAR = 'line_polar'
    SCATTER = 'scatter'
    PIE = 'pie'
    PLOT = 'plot'


class SupportedClass(Enum):
    PlotlyViz = 'plotlyviz'
    PlotToolViz = 'plottoolviz'


class __DataVizBase(ABC):
    def __init__(self,
                 class_name: str,
                 id_: str = None,
                 *,
                 entitlements: Union[Entitlements, Entitlements_] = None,
                 dataviz_dict: dict = None):
        try:
            self._class_name = SupportedClass(class_name.lower())
            if id_:
                self._viz_response = GsSession.current._get(f'{API}/{id_}')
                self._id = self._viz_response['id']
                self._name = self._viz_response.get('title', '')
                self._type = SupportedFigure(self._viz_response['type'])
                self._sources = [DataVizSource(type=source.get('type'), id=source.get('id'), alias=source.get('alias'))
                                 for source in self._viz_response['sources']]
                self._parameters = self._viz_response['parameters']
            elif dataviz_dict:
                if all(key in dataviz_dict.keys() for key in DATAVIZ_ENTITY_PROPS):
                    self._id = dataviz_dict['id']
                    self._name = dataviz_dict["name"]
                    self._type = SupportedFigure(dataviz_dict['type'])
                    self._class = SupportedClass(dataviz_dict["classname"])
                    self._sources = [DataVizSource(type=source.get('type'),
                                                   id=source.get('id'),
                                                   alias=source.get('alias'))
                                     for source in dataviz_dict['sources']]
                    self._parameters = dataviz_dict['parameters']
                else:
                    raise MqValueError('A valid Dataviz dict including '
                                       '(id, name, classname, type, sources and parameters) is '
                                       'required to initialize DataViz.')
            else:
                self._id = id_
                self._type: Optional[SupportedFigure] = None
                self._sources = []
                self._parameters = {}
            self.__entitlements = entitlements
        except Exception as e:
            raise MqValueError(f'Unable to instantiate DataViz. {e}')

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, figure_type: SupportedFigure):
        self._type = figure_type

    def create(self):
        if self._type:
            response = GsSession.current._post(f'{API}', self._parameters, request_headers=HEADERS)
            self._id = response['id']
            return response['id']
        else:
            raise MqValueError('Figure not yet initialized or created. Please create a figure before saving it.')

    @abstractmethod
    def save(self):
        pass

    def _save(self, sources: List[DataVizSource] = None) -> str:
        if self._type:
            try:
                if sources:
                    self._sources = sources
                figure_json = self.__as_json()
                if self._id:  # update
                    GsSession.current._put(f'{API}/{self._id}', figure_json, request_headers=HEADERS)
                else:  # create
                    response = GsSession.current._post(f'{API}', figure_json, request_headers=HEADERS)
                    self._id = response['id']
                return self._id
            except Exception as e:
                raise MqValueError(f'Unable to save DataViz. {e}')
        else:
            raise MqValueError('Figure not yet initialized or created. Please create a figure before saving it.')

    def delete(self) -> None:
        """
        Deletes the DataViz if it has been persisted.
        :return: None
        """
        if self._id:
            GsSession.current._delete(f'{API}/{self._id}', request_headers=HEADERS)
        else:
            raise MqValueError('DataViz has not been persisted.')

    def open(self) -> None:
        """
        Opens the DataViz in the default browser.
        :return: None
        """
        if self._id is None:
            raise MqValueError('DataViz must be created or saved before opening.')
        webbrowser.open(f'{GsSession.current.domain.replace(".web", "")}/s/markets/visualizations/{self._id}')

    def _create_payload(self, attributes: Dict) -> None:
        for name, val in attributes.items():
            if name not in ['self', '__class__']:
                self._parameters[name] = val

    def as_dict(self) -> Dict:
        dataviz_dict = {
            'name': self._parameters.get('title', ''),
            'type': self._type.value,
            'classname': self._class_name.value.lower(),
            'sources': [source.as_dict() for source in self._sources],
            'parameters': self.__parameters_to_dict(self._parameters)
        }
        if self.__entitlements:
            if isinstance(self.__entitlements, Entitlements_):
                dataviz_dict['entitlements'] = self.__entitlements.as_dict()
            elif isinstance(self.__entitlements, Entitlements):
                dataviz_dict['entitlements'] = self.__entitlements.to_dict()
            else:
                dataviz_dict['entitlements'] = self.__entitlements
        return dataviz_dict

    def __as_json(self) -> str:
        return json.dumps(self.as_dict())

    def __parameters_to_dict(self, parameters: Dict) -> Dict:
        obj = {}
        for prop_key, prop_val in parameters.items():
            if self.type == SupportedFigure.PLOT:
                if isinstance(prop_val, List):
                    obj[prop_key] = []
                    for v in prop_val:
                        if isinstance(v, Asset):
                            asset: Asset = v
                            obj[prop_key].append(asset.get_identifier(AssetIdentifier.BLOOMBERG_ID))
                        else:
                            obj[prop_key].append(prop_val)
                elif isinstance(prop_val, date):
                    obj[prop_key] = prop_val.strftime('%Y-%m-%d')
                elif not prop_val or (prop_val and len(prop_val) == 0):
                    # if no value set, will use header file for defaults for Plots
                    obj[prop_key] = ''
                else:
                    obj[prop_key] = prop_val
            else:
                if prop_val:
                    obj[prop_key] = prop_val
        return obj
