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
import os
import shutil
import subprocess
import sys
from pathlib import Path

import setuptools
import versioneer

if "sdist" in sys.argv:
    reference = os.path.dirname(__file__)
    doc_dir = os.path.join(reference, "docs")
    p = subprocess.Popen("sphinx-build -M help . _build", cwd=doc_dir, shell=True)
    p.wait(30)
    if p.returncode != 0:
        raise RuntimeError("unable to make docs")

    generated_dir = Path(os.path.join(doc_dir, "_build", "html", "functions"))
    generated_dir.mkdir(parents=True, exist_ok=True)
    target_dir = os.path.join(reference, "gs_quant", "docs")
    shutil.rmtree(target_dir, ignore_errors=True)
    shutil.copytree(generated_dir, target_dir)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gs_quant",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Goldman Sachs",
    author_email="developer@gs.com",
    description="Goldman Sachs Quant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://marquee.gs.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "aenum",
        "backoff",
        "cachetools",
        "certifi",
        "dataclasses_json",
        "deprecation",
        "freezegun",
        "funcsigs",
        "inflection",
        "lmfit",
        "more_itertools",
        "msgpack",
        "nest-asyncio",
        "opentracing",
        "numpy<2.0.0",
        "pandas>=1.4",
        "pydash<7.0.0",
        "python-dateutil>=2.7.0",
        "pytz==2024.1",
        "requests",
        "httpx>=0.23.3",
        "scipy>=1.2.0",
        "statsmodels>=0.13.0",
        "tqdm",
        "websockets"
    ],
    extras_require={
        "internal": ["gs_quant_internal>=1.5.416"],
        "turbo": ["quant-extensions"],
        "notebook": ["jupyter", "matplotlib", "seaborn", "treelib"],
        "test": ["pytest", "pytest-cov", "pytest-mock", "pytest-order", "testfixtures", "nbconvert", "nbformat",
                 "jupyter_client"],
        "develop": ["wheel", "sphinx", "sphinx_rtd_theme", "sphinx_autodoc_typehints", "pytest", "pytest-cov",
                    "pytest-mock", "pytest-order", "testfixtures"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
)
