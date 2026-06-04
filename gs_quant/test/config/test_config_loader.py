"""
Copyright 2026 Goldman Sachs.
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

import os
import socket

from gs_quant.config.utils import expand_string_with_variables


def test_expand_string_with_env_var():
    os.environ['TEST_VAR'] = 'test_value'
    result = expand_string_with_variables("Value is $TEST_VAR")
    assert result == "Value is test_value"


def test_expand_string_with_env_var_in_squiggles():
    os.environ['TEST_VAR'] = 'test_value'
    result = expand_string_with_variables("Value is ${TEST_VAR}")
    assert result == "Value is test_value"


def test_expand_string_with_cwd():
    cwd = os.getcwd()
    result = expand_string_with_variables("Current directory: $CWD")
    assert result == f"Current directory: {cwd}"


def test_expand_string_with_hostname():
    hostname = socket.gethostname()
    result = expand_string_with_variables("Hostname: $HOSTNAME")
    assert result == f"Hostname: {hostname}"


def test_expand_string_with_unknown_var():
    result = expand_string_with_variables("Unknown variable: $UNKNOWN_VAR")
    assert result == "Unknown variable: UNKNOWN"


def test_expand_string_with_bad_syntax():
    result = expand_string_with_variables("Unknown variable: ${UNKNOWN_VAR NO ENDING")
    assert result == "Unknown variable: ${UNKNOWN_VAR NO ENDING"


def test_expand_string_no_variables():
    result = expand_string_with_variables("No variables here")
    assert result == "No variables here"
