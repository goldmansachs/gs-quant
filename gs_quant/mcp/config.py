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

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from gs_quant.session import Environment

# Configuration to handle aliases and field names
camel_model_config = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True,
)


class SSLConfig(BaseModel):
    model_config = camel_model_config

    cert_path: str
    key_path: str


class McpServiceConfig(BaseModel):
    model_config = camel_model_config

    base_path: str = "/mcp"
    port: int | None = None
    host: str = "0.0.0.0"
    env: Environment = Environment.PROD
    ssl_config: SSLConfig | None = None
