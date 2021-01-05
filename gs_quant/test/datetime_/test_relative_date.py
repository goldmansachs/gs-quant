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

import pytest

from gs_quant.datetime.relative_date import RelativeDate


def test_rule_parsing():
    assert RelativeDate('A')._get_rules() == ['A']
    assert RelativeDate('1d')._get_rules() == ['1d']
    assert RelativeDate('-1d')._get_rules() == ['-1d']
    assert RelativeDate('1y-1d')._get_rules() == ['1y', '-1d']
    assert RelativeDate('-1y-1d')._get_rules() == ['-1y', '-1d']
    assert RelativeDate('-1y+1d')._get_rules() == ['-1y', '1d']


if __name__ == "__main__":
    pytest.main(args=["test_relative_date.py"])
