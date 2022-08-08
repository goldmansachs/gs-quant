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
from typing import Tuple, Dict, Any, List
from gs_quant.session import GsSession
from gs_quant.target.base_screener import Screener

_logger = logging.getLogger(__name__)


class GsBaseScreenerApi:

    @classmethod
    def get_screeners(cls) -> Tuple[Screener, ...]:
        """
        Retrieves screener information about all screeners accessible to the current user.

        :return: Screener tuple, a tuple containing each screener available to the user.
        """
        return GsSession.current._get('/data/screeners', cls=Screener)['results']

    @classmethod
    def get_screener(cls, screener_id: str) -> Screener:
        """
        Retrieves information about the screener specified in parameter screener_id.

        :param screener_id: str, the id of the screener whose information is being retrieved.

        :return: Screener, an object containing information about the screener associated
        with screener_id.
        """
        return GsSession.current._get('/data/screeners/{id}'.format(id=screener_id), cls=Screener)

    @classmethod
    def create_screener(cls, screener: Screener) -> Screener:
        """
        Creates a new screener with a new id from a Screener object. The new screener copies
        the specifications of the Screener object passed into this function. To make changes to
        the new screener's schema upon creation, change the attributes of the Screener object
        before passing it into this function.

        User must be a part of the PlotScreenerAdmins group to perform this action.

        :param screener: Screener, the screener object that is copied to make the new screener.

        :return: Screener, the new screener object containing a new id
        """
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/data/screeners', screener, request_headers=request_headers, cls=Screener)

    @classmethod
    def edit_screener(cls, screener_id: str, screener: Screener) -> Screener:
        """
        Edits the existing screener with ID screener_id to follow the schema specified in
        the passed in Screener object. The existing screener's original schema will be
        entirely overwritten by this object's schema. The edited screener will retain its
        screener ID after being altered by this function.

        User must be a part of the PlotScreenerAdmins group to perform this action.

        Throws an error if the screener_id provided does not match the ID of the
        screener object provided.

        :param screener_id: str, the ID of the screener being edited. Must be the same
        ID as contained in the
         screener parameter.
        :param screener: Screener, the object representing the screener to be edited.
        This object should contain any desired changes to the screener.

        :return: Screener, an object containing information about the updated screener.
        """
        assert screener_id == screener.id

        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._put('/data/screeners/{id}'.format(id=screener_id), screener,
                                      request_headers=request_headers, cls=Screener)

    @classmethod
    def publish_to_screener(cls, screener_id: str, data: Dict[str, List[Dict[str, Any]]]) \
            -> List[Dict[str, Any]]:
        """
        Permanently publishes additional data specified in screener_rows to the existing screener
        with ID screener_id. Although this function returns a dictionary of all published data,
        only data formats consistent with the screener schema will be persisted.

        User must be a part of the PlotScreenerAdmins group to perform this action.

        :param screener_id: str, the ID of the screener to which data will be published.
        :param data:, dict list, a list of dictionaries where each dictionary
        represents a row of data to publish to the screener.

        :return: dict list, a list of dictionaries, where each dictionary represents a row
        of data to be published to the screener.
        """
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/data/screeners/{id}/publish'.format(id=screener_id), data,
                                       request_headers=request_headers)['data']

    @classmethod
    def clear_screener(cls, screener_id: str) -> Dict[str, Any]:
        """
        Permanently clears all data from a screener with the corresponding screener_id,
        but does not delete the screener. This function leaves the schema of the screener
        unchanged.

        User must be a part of the PlotScreenerAdmins group to perform this action.

        :param screener_id: str, the ID of the screener whose data is being cleared.

        :return: dict, a dictionary with information about if the screener was successfully cleared.
        """
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/data/screeners/{id}/clear'.format(id=screener_id), {},
                                       request_headers=request_headers)

    @classmethod
    def delete_screener(cls, screener_id: str) -> None:
        """
        Permanently deletes the screener associated with ID screener_id, as well as all of its data.

        User must be a part of the PlotScreenerAdmins group to perform this action.

        :param screener_id: str, the ID of the screener being deleted.

        :return: None
        """
        return GsSession.current._delete('/data/screeners/{id}'.format(id=screener_id))
