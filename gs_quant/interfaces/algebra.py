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

import abc


class AlgebraicType(abc.ABC):
    @abc.abstractmethod
    def __add__(self, other):
        ...

    def __radd__(self, other):
        return self.__add__(other)

    @abc.abstractmethod
    def __sub__(self, other):
        ...

    @abc.abstractmethod
    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        return self.__mul__(other)

    @abc.abstractmethod
    def __div__(self, other):
        ...
