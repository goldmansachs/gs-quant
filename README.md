# GS Quant

**GS Quant** is a python toolkit for quantitative finance, which provides access to an extensive set of derivatives pricing data through the Goldman Sachs Marquee developer APIs. Libraries are provided for timeseries analytics, portfolio manipulation, risk and scenario analytics and backtesting. Can be used to interact with the Marquee platform programmatically, or as a standalone software package for quantitiative analytics.

Created and maintained by quantitative developers (quants) at Goldman Sachs to enable development of trading strategies and analysis of derivative products. Can be used to facilitate derivative structuring and trading, or as statistical packages for a variety of timeseries analytics applications.

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

## Help
Write to our distribution list: developer@gs.com
