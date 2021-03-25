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


class DisplayOptions:
    """
    config options
    """

    def __init__(self, show_na: bool = False):
        self.__show_na = show_na

    @property
    def show_na(self):
        return self.__show_na

    @show_na.setter
    def show_na(self, show_na):
        self.__show_na = show_na


display_options = DisplayOptions()
