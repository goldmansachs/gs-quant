"""
Copyright 2023 Goldman Sachs.
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
from typing import Callable, Optional

from gs_quant.session import GsSession


class ApiWithCustomSession:
    __SESSION_SUPPLIER: Optional[Callable[[], GsSession]] = None

    @classmethod
    def set_session_provider(cls, session_supplier: Callable[[], GsSession]):
        """
        To allow session context override specific to this API, set a factory/supplier.
        Default is GsSession.current.
        :param session_supplier: callable which returns a GsSession
        """
        cls.__SESSION_SUPPLIER = session_supplier

    @classmethod
    def set_session(cls, session: GsSession):
        """
        To allow session context override specific to this API, set a session directly.
        Default is GsSession.current.
        :param session: a GsSession
        """
        cls.__SESSION_SUPPLIER = None if session is None else lambda: session

    @classmethod
    def get_session(cls) -> GsSession:
        if cls.__SESSION_SUPPLIER:
            return cls.__SESSION_SUPPLIER()
        else:
            return GsSession.current
