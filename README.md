# GS Quant
Test Change
## Installation
pip install gs-quant

GS users: pip install gs-quant[internal] --user

## Dependencies
Python 3.6 or 3.7  

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
    coverage = weather.get_coverage(weather) # GS-specific functionality
    df = weather.get_data(datetime.date(2016, 1, 15), datetime.date(2016, 1, 16), city=['Boston', 'Austin'])

    # calculate vol for a time series
    range = pd.date_range('1/1/2005', periods=3650, freq='D')
    series = pd.Series(np.random.rand(len(range)), index=range)  # randomly generated
    vol = volatility(series, 63)
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
