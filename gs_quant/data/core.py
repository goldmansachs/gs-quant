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
import datetime
from gs_quant.context_base import ContextBaseWithDefault


class DataContext(ContextBaseWithDefault):
    def __init__(self, start=None, end=None):
        super().__init__()
        self.__start = start
        self.__end = end

    @property
    def start_date(self):
        return self.__start or (datetime.date.today() - datetime.timedelta(days=30))

    @property
    def end_date(self):
        return self.__end or datetime.date.today()
