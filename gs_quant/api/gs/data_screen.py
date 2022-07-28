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
from typing import Tuple, Dict
from gs_quant.session import GsSession
from gs_quant.target.data_screen import AnalyticsScreen, FilterRequest, DataRow

_logger = logging.getLogger(__name__)


class GsDataScreenApi:

    @classmethod
    def get_screens(cls) -> Tuple[AnalyticsScreen, ...]:
        """
        Retrieves screen information about all screens accessible to the current user.

        :return: AnalyticsScreen tuple, a tuple containing each screen available to the user.
        """
        return GsSession.current._get('/data/screens', cls=AnalyticsScreen)['results']

    @classmethod
    def get_screen(cls, screen_id: str) -> AnalyticsScreen:
        """
        Retrieves information about the screen specified in parameter screen_id.

        :param screen_id: str, the id of the screen whose information is being retrieved.

        :return: AnalyticsScreen, an object containing information about the screen associated with screen_id.
        """
        return GsSession.current._get('/data/screens/{id}'.format(id=screen_id), cls=AnalyticsScreen)

    @classmethod
    def get_column_info(cls, screen_id: str) -> Dict[str, Dict]:
        """
        Retrieves information about each column in the screen with id corresponding to screen_id. This column
        information can be used to create filters on the screen.

        :param screen_id: str, the id of the screen whose column information is being retrieved.

        :return: dict, a dictionary where each key identifies a column and each value identifies properties of that
        column.
        """
        return GsSession.current._get(
            '/data/screens/{id}/filters'.format(id=screen_id))['aggregations']

    @classmethod
    def delete_screen(cls, screen_id: str) -> None:
        """
        Deletes the screen identified by screen_id. A deleted screen's data and information cannot be retrieved again.

        :param screen_id: str, the id of the screen that is being deleted

        :return: None
        """
        return GsSession.current._delete('/data/screens/{id}'.format(id=screen_id))

    @classmethod
    def create_screen(cls, screen: AnalyticsScreen) -> AnalyticsScreen:
        """
        Creates a new screen with a new id from an existing screen object. The new screen is a copy of the screen
        object passed into this function. To make changes to the new screen upon creation, change the attributes of
        the AnalyticsScreen object before passing it into this function.

        :param screen: AnalyticsScreen, the screen object that is copied to make the new screen.

        :return: AnalyticsScreen, the new screen object containing a new id
        """
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/data/screens', screen, request_headers=request_headers, cls=AnalyticsScreen)

    @classmethod
    def filter_screen(cls, screen_id: str, filter_request: FilterRequest) -> Tuple[DataRow, ...]:
        """
        Returns filtered data from the screen associated with this screen_id. The filters applied to the data are
        contained in the filters parameter. Any filters previously applied to the relevant screen will be temporarily
        ignored in favor of the filters passed into this function. To see the data from this screen with the
        screen's current filters, simply pass in the screen's id and filter_parameters from the screen's
        AnalyticsScreen object.

        :param screen_id: str, the id of the screen whose data is being retrieved.
        :param filter_request: FilterRequest, an object populated with information about how the retrieved data should
        be filtered.

        :return: Tuple of DataRow objects, each DataRow in the tuple is a row of filtered data from this screen.
        """
        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._post('/data/screens/{id}/filter'.format(id=screen_id), filter_request,
                                       request_headers=request_headers, cls=DataRow)['results']

    @classmethod
    def update_screen(cls, screen_id: str, screen: AnalyticsScreen) -> AnalyticsScreen:
        """
        Permanently overwrites the screen at screen_id with the screen object provided in the screen parameter.
        This includes overwriting any filters applied to the screen at screen_id.

        Throws an error if the screen_id provided does not match the ID of the screen object provided.

        :param screen_id: str, the id of the screen being updated. Must be the same id as is contained in the screen
        parameter.
        :param screen: AnalyticsScreen, the object representing the screen to be updated. This object should contain
        any desired changes to the screen

        :return: AnalyticsScreen, an object containing information about the updated screen.

        """
        assert screen_id == screen.id_

        request_headers = {'Content-Type': 'application/json;charset=utf-8'}
        return GsSession.current._put('/data/screens/{id}'.format(id=screen_id), screen,
                                      request_headers=request_headers, cls=AnalyticsScreen)
