# GS Quant

**GS Quant** is a Python toolkit for quantitative finance, which provides access to derivatives pricing and risk capabilities through the Goldman Sachs developer APIs, as well as standalone packages for financial analytics.

It is created and maintained by quantitative developers (quants) at Goldman Sachs to enable the development of trading strategies and analysis of derivative products. GS Quant can be used to facilitate derivative structuring, trading, and risk management, or as a set of statistical packages for data analytics applications.

See also Getting Started notebook in the gs_quant folder or package.

## Requirements

* Python 3.6 or greater
* Access to PIP package manager

You can verity your Python version with the command python --version.

Any Python-ready IDE will work. However, most of our team uses PyCharm.

## Installation
```
pip install gs-quant
```
GS users: 
```
pip install gs-quant[internal] --user
```

## Examples

The following example generates a random timeseries and computes 1-month (22 day) rolling realized volatility:

```python
import gs_quant.timeseries as ts

x = ts.generate_series(1000)           # Generate random timeseries with 1000 observations
vol = ts.volatility(x, Window(22, 0))  # Compute realized volatility using a window of 22 and a ramp up value of 0
vol.tail()                             # Show last few values
```

Out:
```
Out[1]:
2021-12-20 12.898025
2021-12-21 12.927230
2021-12-22 12.929520
2021-12-23 13.987033
2021-12-24 14.048165
dtype: float64
```

Clients of Goldman Sachs have access to a wide array of data through our developer APIs (please contact your sales coverage for details):

```python
from gs_quant.session import Environment, GsSession
from gs_quant.data import Dataset, Fields
from datetime import date

with GsSession.get(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data')):

    basket_ds = Dataset(Dataset.GS.CB)
    start_date = date(2007,1,1)

    vip_px = basket_ds.get_data_series(Fields.CLOSE_PRICE, start=start_date, ticker='GSTHHVIP')
    vip_px.tail()
```

Entitled users can also access pricing and risk engines programmatically:

```python
from gs_quant.instrument import IRSwap
from gs_quant.common import Currency, PayReceive
import gs_quant.risk as risk
 
with GsSession.get(Environment.PROD, <client_id>, <client_secret>, scopes=('read_product_data','run_analytics')):
     
    # price an interest rate swap and compute its bucketed delta
    irs = IRSwap(PayReceive.Pay, "5y", Currency.USD, fixed_rate=0.0275)
    pv = irs.price()
    ir_delta = irs.calc(risk.IRDelta)
```

## Contributions

Contributions are encouraged! Please see CONTRIBUTING.MD for more details

## Help
If you need any help or have feedback, please email us at: gs-quant@gs.com
