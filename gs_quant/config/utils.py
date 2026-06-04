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
import re
import socket
from typing import Any

import yaml


def _env_var_or_cwd(var_name):
    if var_name == "CWD":
        return os.getcwd()
    elif var_name == "HOSTNAME":
        return socket.gethostname()
    else:
        return os.environ.get(var_name, 'UNKNOWN')


def expand_string_with_variables(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    env_regex = r"\$([A-Za-z_]+)"
    env_regex_with_squiggles = r"\$\{([A-Za-z_]+)\}"
    for reg in (env_regex_with_squiggles, env_regex):
        value = re.sub(reg, lambda m: _env_var_or_cwd(m.group(1)), value)
    return value


def load_model_from_yaml(config_path: str, model_class):
    with open(config_path, 'r') as f:
        yaml_config = yaml.safe_load(f)
    return model_class.model_validate(yaml_config)
