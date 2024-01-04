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

from ._version import get_versions

name = "gs_quant"
__version__ = get_versions()['version']
del get_versions

version = __version__

# Set up PyXll, if available
try:
    from .xl_interface.instrument_generation import install_hook
    install_hook()
except ModuleNotFoundError:
    pass

# Jupyter needs nest_asyncio to avoid event loop issues
try:
    from IPython import get_ipython
    ipython = get_ipython()
    if ipython and 'IPKernelApp' in get_ipython().config:
        import nest_asyncio
        nest_asyncio.apply()
except ImportError:
    pass

# Setup tracing for Jupyter
try:
    from gs_quant.tracing import tracing  # pylint: disable=unused-import
except ImportError:
    pass
