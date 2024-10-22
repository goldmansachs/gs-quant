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

import sys


class MqError(Exception):
    """Base class for errors in this module"""
    pass


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
        prepend = 'context: {}\n'.format(self.context) if self.context else ''
        result = '{}status: {}, message: {}'.format(prepend, self.status, self.message)
        if sys.version_info.major < 3:
            result = result.encode('ascii', 'ignore')
        return result


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


def error_builder(status, message, context=None):
    if status == 401:
        return MqAuthenticationError(status, message, context)
    elif status == 403:
        return MqAuthorizationError(status, message, context)
    elif status == 429:
        return MqRateLimitedError(status, message, context)
    elif status == 500:
        return MqInternalServerError(status, message, context)
    elif status == 504:
        return MqTimeoutError(status, message, context)
    else:
        return MqRequestError(status, message, context)
