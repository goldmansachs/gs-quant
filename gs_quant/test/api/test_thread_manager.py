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

from functools import partial

import pytest

from gs_quant.api.utils import ThreadPoolManager
from gs_quant.session import GsSession


class NullContextManager(object):
    def __init__(self, dummy_resource=None):
        self.dummy_resource = dummy_resource

    def __enter__(self):
        return self.dummy_resource

    def __exit__(self, *args):
        pass


def dummy_function(number: int):
    return number


def test_thread_manager():
    func_0 = partial(dummy_function, 5)
    func_1 = partial(dummy_function, 0)
    func_2 = partial(dummy_function, 10)
    GsSession.current = NullContextManager()
    results = ThreadPoolManager.run_async([func_0, func_1, func_2])
    assert results[0] == 5
    assert results[1] == 0
    assert results[2] == 10


if __name__ == '__main__':
    pytest.main(args=[__file__])
