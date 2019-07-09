# GS Quant

**GS Quant** is a python toolkit for quantitative finance, which provides access to an extensive set
of derivatives pricing data through the Goldman Sachs Marquee developer APIs. Libraries are provided
for timeseries analytics, portfolio manipulation, risk and scenario analytics and backtesting. Can
be used to interact with the Marquee platform programmatically, or as a standalone software package
for quantitiative analytics.

Created and maintained by quantitative developers (quants) at Goldman Sachs to enable development of
trading strategies and analysis of derivative products. Can be used to facilitate derivative
structuring and trading, or as statistical packages for a variety of timeseries analytics
applications.

See also Getting Started notebook in the gs_quant folder or package.

## Installation

pip install gs-quant

GS users: pip install gs-quant[internal] --user

## Dependencies

Python 3.6 or 3.7 \
Package dependencies can be installed by pip.

## Example

```python
import datetime
import numpy as np
import pandas as pd
from gs_quant.data import Dataset
from gs_quant.instrument import IRSwap
from gs_quant.common import Currency, PayReceive
import gs_quant.risk as risk
from gs_quant.session import Environment, GsSession
from gs_quant.timeseries import volatility

# N.b., GsSession.use(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')) will set the default session

with GsSession.get(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')):
    # get coverage for a dataset; run a query
    weather = Dataset('WEATHER')
    coverage = weather.get_coverage() # GS-specific functionality
    df = weather.get_data(datetime.date(2016, 1, 15), datetime.date(2016, 1, 16), city=['Boston', 'Austin'])

    # calculate vol for a time series
    range = pd.date_range('1/1/2005', periods=3650, freq='D')
    series = pd.Series(np.random.rand(len(range)), index=range)  # randomly generated
    vol = volatility(series, 252)
    vol.plot()  # requires matplotlib

    # Non-GS users: the below functionality requires extra permissions
    # Please contact your sales coverage to request access

    # price an interest rates swap and compute its bucketed delta
    irs = IRSwap(PayReceive.Pay, "5y", Currency.USD, fixedRate=0.0275)
    pv = irs.price()
    ir_delta = irs.calc(risk.IRDelta)
```

## 3rd Party Packages and Licenses

| package                  | license                                  | url                                                | usage                       |
| ------------------------ | ---------------------------------------- | -------------------------------------------------- | --------------------------- |
| backoff                  | MIT                                      | https://pypi.org/project/backoff/                  | install_require             |
| cachetools               | MIT                                      | https://pypi.org/project/cachetools/               | install_require             |
| configparser             | MIT                                      | https://pypi.org/project/configparser/             | install_require             |
| funcsigs                 | Apache Software License (ASL)            | https://pypi.org/project/funcsigs/                 | install_require             |
| future                   | OSI Approved, MIT License (MIT)          | https://pypi.org/project/future/                   | install_require             |
| inflection               | MIT                                      | https://pypi.org/project/inflection/               | install_require             |
| msgpack                  | Apache Software License (Apache 2.0)     | https://pypi.org/project/msgpack/                  | install_require             |
| pandas                   | BSD                                      | https://pypi.org/project/pandas/                   | install_require             |
| python-dateutil          | Apache Software License, BSD License     | https://pypi.org/project/python-dateutil/          | install_require             |
| requests                 | Apache Software License (Apache 2.0)     | https://pypi.org/project/requests/                 | install_require             |
| scipy                    | BSD License (BSD)                        | https://pypi.org/project/scipy/                    | install_require             |
| six                      | MIT License (MIT)                        | https://pypi.org/project/six/                      | install_require             |
| requests_kerberos        | ISC License                              | https://pypi.org/project/requests-kerberos/        | extras_require internal     |
| jupyter                  | BSD License (BSD)                        | https://pypi.org/project/jupyter/                  | extras_require notebook     |
| matplotlib               | Python Software Foundation License (PSF) | https://pypi.org/project/matplotlib/               | extras_require notebook     |
| pprint                   | MIT                                      | https://pypi.org/project/pprint/                   | extras_require notebook     |
| pytest                   | MIT                                      | https://pypi.org/project/pytest/                   | extras_require test,develop |
| pytest-cov               | BSD License (MIT)                        | https://pypi.org/project/pytest-cov/               | extras_require test,develop |
| pytest-mock              | MIT License (MIT)                        | https://pypi.org/project/pytest-mock/              | extras_require test,develop |
| testfixtures             | MIT License (MIT)                        | https://pypi.org/project/testfixtures/             | extras_require test,develop |
| sphinx                   | BSD License (BSD)                        | https://pypi.org/project/Sphinx/                   | extras_require develop      |
| sphinx_rtd_theme         | MIT License (MIT)                        | https://pypi.org/project/sphinx_rtd_theme/         | extras_require develop      |
| sphinx_autodoc_typehints | MIT License (MIT)                        | https://pypi.org/project/sphinx_autodoc_typehints/ | extras_require develop      |

## Adding a new package

We advise checking with gs-quant maintainers before adding any additional vendor packages that are
not covered under one of the above licenses to determine whether it would be acceptable Generally
speaking, copyleft licenses such as GNU AGPLv3, GNS GPLv3, GNU LGPLv3, Mozilla Public License 2.0
are not acceptable. Information on various licenses can be found on
[choosealicense.com](https://choosealicense.com/appendix/). See [contributing.md](./CONTRIBUTING.md)
for help on how to contribute.

## Help

Write to our distribution list: developer@gs.com
