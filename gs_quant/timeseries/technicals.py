""""""
"""
Copyright 2018 Goldman Sachs.
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

Chart Service will attempt to make public functions (not prefixed with _) from this module available. Such functions
should be fully documented: docstrings should describe parameters and the return value, and provide a 1-line
description. Type annotations should be provided for parameters.

The technical analysis timeseries library contains functions which compute technical indicators. These include basic
timeseries operations (moving average), and finance-specific technical indicators (e.g. bollinger bands)
"""

from .statistics import *


def moving_average(series, window=22):
    """
    Compute moving average of a timeseries over specified window

:param series: time series of prices
    :param window: number of observations in window
    :return: date-based time series of return
    """

    return mean(series, window)


moving_average.__annotations__ = {'series': pd.Series, 'window': int, 'return': pd.Series}
