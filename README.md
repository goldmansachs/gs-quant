# GS Quant

## Installation
pip install gs_quant

## Dependencies
Python 3.6 or 3.7  
Package dependencies can be installed by pip.

## Example
```python
from gs_quant.api.dataset import Dataset
from gs_quant.api.instrument import IRSwap
from gs_quant.api.common import Currency, PayReceive
import gs_quant.api.risk as risk
from gs_quant.session import Environment, GsSession
from gs_quant.timeseries import realized_volatility

# N.b., GsSession.use(Environment.PROD, <client_id>, <client_secret>) will set the default session
 
with GsSession.get(Environment.PROD, <client_id>, <client_secret>):
    # get coverage for a dataset; run a query
    wmFxSpot = Dataset('WMFXSPOT')
    coverage = wmFxSpot.get_coverage()
    df = wmFxSpot.get_data('2018-01-03', '2018-01-04', bbid=['USDEUR', 'USDGBP'])

    # get prices as a time series, then calculate vol
    treod = Dataset('TREOD')
    curve = treod.get_data_series('tradePrice', ric='.SPX', start='2003-01-01', end='2018-08-31')
    vol = realized_volatility(curve, 252)
    vol.plot()  # requires matplotlib
    
    # price an interest rates swap and compute its bucketed delta
    irs = IRSwap(PayReceive.Pay, "5y", Currency.USD, fixedRate=0.035)
    pv = irs.price()
    irDelta = irs.calc(risk.IRDelta)
```

## Help
## Help
Questions? Comments? Write to data-services@gs.com
