# GS Quant

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

from gs_quant.session import Environment, GsSession

# N.b., GsSession.use(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')) will set the default session
 
with GsSession.get(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')):
    # get coverage for a dataset; run a query
	from gs_quant.api.dataset import Dataset
    weather = Dataset('WEATHER')
    coverage = weather.get_coverage()
    df = weather.get_data(datetime.date(2016, 1, 15), datetime.date(2016, 1, 16), city=['Boston', 'Austin'])

    # calculate vol for a time series
	from gs_quant.timeseries import realized_volatility
    range = pd.date_range('1/1/2005', periods=3650, freq='D')
    curve = pd.Series(np.random.rand(len(range)), index=range)  # randomly generated
    vol = realized_volatility(curve, 252)
    vol.plot()  # requires matplotlib
    
    # price an interest rates swap and compute its bucketed delta
	from gs_quant.api.instrument import IRSwap
	from gs_quant.api.common import Currency, PayReceive
	import gs_quant.api.risk as risk
    irs = IRSwap(PayReceive.Pay, "5y", Currency.USD, fixedRate=0.035)
    pv = irs.price()
    irDelta = irs.calc(risk.IRDelta)
```

## Help
Questions? Comments? Write to data-services@gs.com
