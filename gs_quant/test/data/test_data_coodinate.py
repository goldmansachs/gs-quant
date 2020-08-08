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

from gs_quant.data import Dataset, DataCoordinate, DataMeasure, DataDimension
import pytest


def test_immutability():

    dimensions = {
        DataDimension.TENOR: '1m',
        DataDimension.STRIKE_REFERENCE: 'Delta',
        DataDimension.RELATIVE_STRIKE: 50
    }

    coord1 = DataCoordinate(Dataset.GS.EDRVOL_PERCENT_STANDARD, DataMeasure.IMPLIED_VOLATILITY, dimensions)
    coord2 = DataCoordinate(Dataset.GS.EDRVOL_PERCENT_STANDARD, DataMeasure.IMPLIED_VOLATILITY, dimensions)

    assert id(coord1) != id(coord2)
    assert coord1 == coord2

    with pytest.raises(AttributeError):
        coord1.dataset_id = 'test'

    with pytest.raises(AttributeError):
        coord1.dimensions = {}

    with pytest.raises(AttributeError):
        coord1.measure = 'test'

    dimensions[DataDimension.TENOR] = '2m'

    coord3 = DataCoordinate(Dataset.GS.EDRVOL_PERCENT_STANDARD, DataMeasure.IMPLIED_VOLATILITY, dimensions)

    assert id(coord1) != id(coord2)
    assert coord1 != coord3


if __name__ == "__main__":
    pytest.main(args=["test_data_coordinate.py"])
