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
"""

# Macro-event source adapter.
#
# Purpose
#
#     Own dataset access for country-scoped macro events so source-specific
#     query details do not live inside the generic processing helpers.

import pandas as pd

from gs_quant.data import Dataset

from .event_study_definitions import MACRO_EVENT_SOURCE, ResolvedEventDefinition
from .event_study_processing import extract_event_payload


def query_event_payload(
    definition: ResolvedEventDefinition,
    start_time: pd.Timestamp,
    end_time: pd.Timestamp,
) -> pd.DataFrame:
    """Query the macro-events dataset for one resolved event definition.

    :param definition: Resolved event metadata.
    :param start_time: Query start.
    :param end_time: Query end.
    :return: Normalized payload DataFrame.
    :raises Exception: Propagates Dataset.get_data and payload-normalization errors.
    """
    dataset = Dataset('MACRO_EVENTS_CALENDAR')
    raw_events = dataset.get_data(
        startTime=start_time.to_pydatetime(),
        endTime=end_time.to_pydatetime(),
        source=[MACRO_EVENT_SOURCE],
        country=definition.country,
        eventName=definition.event_name,
        limit=1000,
    )
    return extract_event_payload(raw_events)
