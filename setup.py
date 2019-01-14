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

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gs_quant",
    version="0.5.2",
    author="Goldman Sachs",
    author_email="developer@gs.com",
    description="Goldman Sachs Quant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://marquee.gs.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "backoff",
        "cachetools",
        "configparser",
        "enum34",
        "funcsigs",
        "future",
        "inflection",
        "pandas",
        "requests",
        "scipy",
        "six",
        "typing",
        "scipy",
    ],
    extras_require={
        "kerb": ["requests-kerberos"],
        "notebook": ["jupyter", "matplotlib~=2.1.0", "pprint"],
        "test": ["pytest", "pytest-cov", "pytest-mock"],
        "develop": ["sphinx", "sphinx_rtd_theme"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
