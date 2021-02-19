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
from typing import Mapping
from pandas import DataFrame

from gs_quant.target.risk import MarketDataPattern, MarketDataShock,\
    MarketDataPatternAndShock, MarketDataShockBasedScenario as __MarketDataShockBasedScenario,\
    MarketDataVolShockScenario as __MarketDataVolShockScenario, MarketDataVolSlice, MarketDataShockType


class MarketDataShockBasedScenario(__MarketDataShockBasedScenario):

    def __init__(self, shocks: Mapping[MarketDataPattern, MarketDataShock]):
        super().__init__(tuple(MarketDataPatternAndShock(p, s) for p, s in shocks.items()))


class MarketDataVolShockScenario(__MarketDataVolShockScenario):

    @classmethod
    def from_dataframe(cls, asset_ric: str, df: DataFrame, ref_spot: float = None):
        """
        Create a MarketDataVolShockScenario using an input DataFrame containing expiry dates, strikes and vol levels
        :param df: input data frame.  Expects a DataFrame indexed by date/time and containing columns expirationDate,
        absoluteStrike and impliedVolatility.
        :param ref_spot: the current reference spot level
        :return: MarketDataVolShockScenario
        """
        last_datetime = max(list(df.index))
        df_filtered = df.loc[df.index == last_datetime]
        df_grouped = df_filtered.groupby(['expirationDate'])

        vol_slices = []
        for key in df_grouped.groups:
            value = df_grouped.get_group(key)
            df_sorted = value.sort_values(['absoluteStrike'])
            strikes = list(df_sorted.absoluteStrike)
            levels = list(df_sorted.impliedVolatility)
            vol_slice = MarketDataVolSlice(key.date(), strikes, levels)
            vol_slices.append(vol_slice)

        scenario = MarketDataVolShockScenario(MarketDataPattern('Eq Vol', asset_ric),
                                              MarketDataShockType.Override, vol_slices, ref_spot)
        return scenario
