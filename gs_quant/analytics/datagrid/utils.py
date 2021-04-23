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

from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum
from typing import Union, List


def get_utc_now() -> str:
    return f'{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'


class SortType(str, Enum):
    VALUE = 'value'  # Sort the column based off the value
    ABSOLUTE_VALUE = 'absoluteValue'  # Sort the column based off the absolute value


class SortOrder(str, Enum):
    ASCENDING = 'ascending'  # Sort the column in ascending order
    DESCENDING = 'descending'  # Sort the column in descending order


class FilterOperation(str, Enum):
    TOP = 'top'  # Top n rows by value
    BOTTOM = 'bottom'  # Bottom n rows by value
    ABSOLUTE_TOP = 'absoluteTop'  # Top n rows by absolute value
    ABSOLUTE_BOTTOM = 'absoluteBottom'  # Bottom n rows by absolute value
    EQUALS = 'equals'  # Rows with column value equal to a value or list of values
    NOT_EQUALS = 'notEquals'  # Rows with column value not equal to a value or list of values
    GREATER_THAN = 'greaterThan'  # Rows with column value greater than a value
    LESS_THAN = 'lessThan'  # Rows with column value less than a value
    LESS_THAN_EQUALS = 'lessThanEquals'  # Rows with column value greater than or equal to a value
    GREATER_THAN_EQUALS = 'greaterThanEquals'  # Rows with column value less than or equal to a value


class FilterCondition(str, Enum):
    AND = 'and'  # Intersect the rows that match the filter
    OR = 'or'  # Union the rows that match the filter


@dataclass
class DataGridSort:
    columnName: str
    sortType: SortType = SortType.VALUE
    order: SortOrder = SortOrder.ASCENDING

    def __post_init__(self):
        self.sortType = SortType(self.sortType)
        self.order = SortOrder(self.order)

    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return DataGridSort(**{k: v for k, v in dict_.items() if k in class_fields})


@dataclass
class DataGridFilter:
    columnName: str
    operation: FilterOperation
    value: Union[float, str, List[float], List[str]]
    condition: FilterCondition = FilterCondition.AND

    def __post_init__(self):
        self.operation = FilterOperation(self.operation)
        self.condition = FilterCondition(self.condition)

    @classmethod
    def from_dict(cls, dict_):
        class_fields = {f.name for f in fields(cls)}
        return DataGridFilter(**{k: v for k, v in dict_.items() if k in class_fields})
