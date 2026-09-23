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
from importlib.metadata import PackageNotFoundError, version as get_lib_version

from ._version import get_versions

name = "gs_quant"
__version__ = get_versions()['version']


def get_environment_summary():
    """
    Returns a summary of the Python version and the versions of specific libraries.
    """
    libraries = ['gs_quant', 'gs_quant_internal', 'numpy', 'pandas']
    summary = {
        'Python Version': sys.version,
    }
    for lib in libraries:
        try:
            lib_version = get_lib_version(lib)
        except PackageNotFoundError:
            lib_version = 'Not Installed'
        summary[lib] = lib_version
    return summary


__summary__ = get_environment_summary()
del get_versions

version = __version__
summary = __summary__

# Set up PyXll, if available
try:
    from .xl_interface.instrument_generation import install_hook

    install_hook()
except ModuleNotFoundError:
    pass

# Jupyter-specific setup (nest_asyncio + tracing). Both are only needed inside
# a running kernel; guard them behind an active-kernel check so plain Python
# scripts don't pay the heavy IPython / OpenTelemetry import costs.
ipython = None
try:
    if 'IPython' in sys.modules or 'ipykernel' in sys.modules:
        from IPython import get_ipython

        ipython = get_ipython()
except ImportError:
    pass

if ipython and 'IPKernelApp' in ipython.config:
    try:
        # Jupyter needs nest_asyncio to avoid event loop issues
        import nest_asyncio

        nest_asyncio.apply()
    except ImportError:
        pass
    try:
        # Setup tracing for Jupyter
        from gs_quant.tracing import tracing  # noqa: F401  pylint: disable=unused-import
    except ImportError:
        pass
