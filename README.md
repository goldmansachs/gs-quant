# GS Quant

GS Quant is a python toolkit for quantitative finance, which provides access to an extensive set of derivatives pricing data through the Goldman Sachs Marquee developer APIs. Libraries are provided for timeseries analytics, portfolio manipulation, risk and scenario analytics and backtesting. Can be used to interact with the Marquee platform programmatically, or as a standalone software package for quantitiative analytics.
Created and maintained by quantitative developers (quants) at Goldman Sachs to enable development of trading strategies and analysis of derivative products. Can be used to facilitate derivative structuring and trading, or as statistical packages for a variety of timeseries analytics applications.
See also Getting Started notebook in the gs_quant folder or package.

## Installation
pip install gs_quant

## Dependencies
Python 3.6 or 3.7  
Package dependencies can be installed by pip.

## Example
```python
import datetime
import numpy as np
import pandas as pd
from gs_quant.api.gs.data import GsDataApi
from gs_quant.data import DataSet
from gs_quant.instrument import IRSwap
from gs_quant.common import Currency, PayReceive
import gs_quant.risk as risk
from gs_quant.session import Environment, GsSession
from gs_quant.timeseries import volatility

# N.b., GsSession.use(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')) will set the default session
 
with GsSession.get(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')):
    # get coverage for a dataset; run a query
    weather = DataSet('WEATHER')
    coverage = GsDataApi.get_coverage(weather) # GS-specific functionality
    df = weather.get_data(datetime.date(2016, 1, 15), datetime.date(2016, 1, 16), city=['Boston', 'Austin'])

    # calculate vol for a time series
    range = pd.date_range('1/1/2005', periods=3650, freq='D')
    series = pd.Series(np.random.rand(len(range)), index=range)  # randomly generated
    vol = volatility(series, 252)
    vol.plot()  # requires matplotlib
    
    # price an interest rates swap and compute its bucketed delta
    irs = IRSwap(PayReceive.Pay, "5y", Currency.USD, fixedRate=0.0275)
    pv = irs.price()
    ir_delta = irs.calc(risk.IRDelta)
```

## Help
Questions? Comments? Write to data-services@gs.com
