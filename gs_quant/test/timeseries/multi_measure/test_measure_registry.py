"""
Copyright 2021 Goldman Sachs.
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
from gs_quant.timeseries.helper import USE_DISPLAY_NAME


@pytest.mark.skipif(not USE_DISPLAY_NAME, reason="requires certain evnvar to run")
def test_registry():
    from gs_quant.timeseries.measure_registry import registry
    assert len(registry) > 0
    for name, mm in registry.items():
        assert name == mm.display_name, \
            'registry key {} does not match with MultiMeasure display_name {}'.format(name, mm.display_name)
        for cls, fns in mm.measure_map.items():
            types = [t for fn in fns if fn.asset_type is not None for t in fn.asset_type]
            assert len(set(types)) == len(types), \
                'duplicate measures are defined for the same asset type in class ' + cls.value

            fn_types_excluded = [fn.asset_type_excluded for fn in fns if fn.asset_type_excluded is not None]
            assert len(fn_types_excluded) <= 1, \
                'more than one measure with asset_type_excluded is defined for asset class ' + cls.value
            types_excluded = [t for types_excluded in fn_types_excluded for t in types_excluded]
            assert len(types_excluded) == 0 or set(types).issubset(set(types_excluded)), \
                'the asset type scope overlaps in class ' + cls.value


if __name__ == "__main__":
    pytest.main(args=["test_measure_registry.py"])
