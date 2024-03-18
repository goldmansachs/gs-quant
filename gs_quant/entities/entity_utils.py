"""
Copyright 2024 Goldman Sachs.
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

from typing import Union

import pandas as pd


def _explode_data(data: pd.Series,
                  parent_label: str) -> Union[pd.DataFrame, pd.Series]:
    parent_to_child_map = {
        "factorCategories": "factors",
        "factors": "byAsset",
        "sectors": "industries",
        "industries": None,
        "countries": None,
        "direction": None
    }

    labels_to_ignore_map = {
        "factorCategories": ["factorExposure", "estimatedPnl", "factors"],
        "factors": ["factorExposure", "estimatedPnl", "byAsset"],
        "sectors": ["exposure", "estimatedPnl", "industries"],
        "industries": [],
        "countries": [],
        "direction": [],
        "byAsset": []
    }

    data = data.rename({'name': parent_label}) if parent_label in parent_to_child_map.keys() else data
    child_label = parent_to_child_map.get(parent_label)

    if child_label and child_label in data.index.values:
        child_df = pd.DataFrame(data[child_label])
        child_df = child_df.apply(_explode_data, axis=1, parent_label=child_label)

        data = data.drop(labels=labels_to_ignore_map.get(parent_label))
        if isinstance(child_df, pd.Series):
            child_df = pd.concat(child_df.values, ignore_index=True)
        child_df = child_df.assign(**data.to_dict())

        return child_df

    return data
