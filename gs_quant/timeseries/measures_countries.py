"""
Copyright 2020 Goldman Sachs.
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
from enum import Enum
from typing import Optional

import pandas as pd
import inflection

from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.data import Dataset
from gs_quant.entities.entity import EntityType
from gs_quant.timeseries import plot_measure_entity
from gs_quant.timeseries.measures import _market_data_timed, _extract_series_from_df, \
    ExtendedSeries

LOGGER = logging.getLogger(__name__)


class _FCI_MEASURE(Enum):
    FCI = "fci"
    LONG_RATES_CONTRIBUTION = "long_rates_contribution"
    SHORT_RATES_CONTRIBUTION = "short_rates_contribution"
    CORPORATE_SPREAD_CONTRIBUTION = "corporate_spread_contribution"
    SOVEREIGN_SPREAD_CONTRIBUTION = "sovereign_spread_contribution"
    EQUITIES_CONTRIBUTION = "equities_contribution"
    REAL_LONG_RATES_CONTRIBUTION = "real_long_rates_contribution"
    REAL_SHORT_RATES_CONTRIBUTION = "real_short_rates_contribution"
    DWI_CONTRIBUTION = "dwi_contribution"
    REAL_FCI = "real_fci"
    REAL_TWI_CONTRIBUTION = "real_twi_contribution"
    TWI_CONTRIBUTION = "twi_contribution"


@plot_measure_entity(EntityType.COUNTRY, [QueryType.FCI])
def fci(country_id: str, measure: _FCI_MEASURE = _FCI_MEASURE.FCI, *, source: str = None,
        real_time: bool = False, request_id: Optional[str] = None) -> pd.Series:
    """
    Daily Financial Conditions Index (FCI) for each of the world's large economies and many smaller ones,
    as well as aggregate FCIs for regions.

    :param country_id: id of country/region
    :param measure: FCI metric to retrieve
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :param request_id: server request id
    :return: FCI metric value
    """
    if real_time:
        raise NotImplementedError('real-time FCI data is not available')

    type_ = QueryType(inflection.titleize(measure.value))
    if measure == _FCI_MEASURE.REAL_FCI or measure == _FCI_MEASURE.REAL_TWI_CONTRIBUTION:
        ds = Dataset('FCI')
        df = ds.get_data(geographyId=country_id)
        if measure == _FCI_MEASURE.REAL_FCI:
            measure = 'realFCI'
        else:
            measure = 'realTWIContribution'
        series = ExtendedSeries(dtype=float) if (measure not in df.columns) else ExtendedSeries(df[measure])
        series.dataset_ids = ('FCI',)
        return series

    q = GsDataApi.build_market_data_query([country_id], query_type=type_, source=source,
                                          real_time=real_time)
    df = _market_data_timed(q, request_id)
    return _extract_series_from_df(df, type_, True)
