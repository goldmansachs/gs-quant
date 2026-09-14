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


class MqError(Exception):
    """Base class for errors in this module"""

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'


class MqValueError(MqError, ValueError):
    pass


class MqTypeError(MqError):
    pass


class MqWrappedError(MqError):
    pass


class MqRequestError(MqError):
    def __init__(self, status, message, context=None):
        self.status = status
        self.message = message
        self.context = context

    def __str__(self):
        prepend = f'context: {self.context}\n' if self.context else ''
        return f'{prepend}status: {self.status}, message: {self.message}'


class MqAuthenticationError(MqRequestError):
    pass


class MqAuthorizationError(MqRequestError):
    pass


class MqUninitialisedError(MqError):
    pass


# Creating errors based on status code to be able to effectively use backoff decorator
class MqRateLimitedError(MqRequestError):
    pass


class MqTimeoutError(MqRequestError):
    pass


class MqInternalServerError(MqRequestError):
    pass


# Maps HTTP status codes to their corresponding exception classes
_ERROR_STATUS_MAP = {
    401: MqAuthenticationError,
    403: MqAuthorizationError,
    429: MqRateLimitedError,
    500: MqInternalServerError,
    504: MqTimeoutError,
}


def error_builder(status, message, context=None):
    error_class = _ERROR_STATUS_MAP.get(status, MqRequestError)
    return error_class(status, message, context)
