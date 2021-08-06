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
import re

from gs_quant.errors import MqError

registry = {}


class MultiMeasure:
    def __init__(self, display_name):
        self.display_name = display_name
        self.measure_map = {}

    def get_fn(self, asset):
        asset_class = asset.asset_class
        asset_type = asset.get_type()
        fns = self.measure_map.get(asset_class, ())

        def canonicalize(word):
            pruned = re.sub(r"[^\w]", "", word)
            return pruned.casefold()

        canonicalized = canonicalize(asset_type.value)

        for fn in fns:
            if (fn.asset_type is None or canonicalized in map(lambda x: canonicalize(x.value), fn.asset_type)) \
                    and (fn.asset_type_excluded is None or canonicalized not in
                         map(lambda x: canonicalize(x.value), fn.asset_type_excluded)):
                return fn

        raise MqError("No measure {} defined for asset class {} and type {}".format(self.display_name, asset_class,
                                                                                    asset_type))

    def __call__(self, asset, *args, **kwargs):
        fn = self.get_fn(asset)
        return fn(asset, *args, **kwargs)

    def register(self, function):
        for asset_class in function.asset_class:
            self.measure_map[asset_class] = self.measure_map.get(asset_class, ()) + (function, )


def register_measure(fn):
    display_name = fn.display_name if fn.display_name else fn.__name__
    multi_measure = registry.get(display_name)
    if multi_measure is None:
        multi_measure = registry[display_name] = MultiMeasure(display_name)
    multi_measure.register(fn)
    return multi_measure
