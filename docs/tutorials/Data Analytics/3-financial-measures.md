---
title: 03 - Financial Measures
excerpt: How to use market-model based measures
datePublished: 2019/06/23
dateModified: 2019/06/23
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Financial Measures
  - Market Models
  - Datasets
  - Dataframes
  - Dataseries
  - Series
  - Pandas
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
  - name: Francis Giannaros
    github: francisg77
links:
  - title: Previous - Financial Series
    url: /gsquant/tutorials/Data-Analytics/2-financial-series/
  - title: Next - Charting Data
    url: /gsquant/tutorials/Data-Analytics/4-charting-data/
---

GS Quant allows for access to more complex market models and associated measures. These are functions which allow more
intuitive slicing of various market-model based datasets. Examples of this would include:

| Measure            | Description                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------- |
| Implied Volatility | Historical implied volatility curve for different strikes and tenors                          |
| Normalized Skew    | Difference in volatility between out-of-the-money and in-the-money option (Put - call ) / ATM |
| Term Structure     | Forward looking term structures of volatility or forward levels at a given point in time      |

## Skew

<note>Examples require an initialized GsSession and data subscription, please refer to 
<a href="/docs/gsquant/guides/Authentication/2-gs-session">Sessions</a> for details</note>

The following example shows how to chart historical skew level for SPX:

```python
from datetime import date
from gs_quant.data import DataContext
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier, ExchangeCode
import matplotlib.pyplot as plt
import gs_quant.timeseries as ts

data_ctx = DataContext(start=date(2018, 1, 1), end=date(2018, 12, 31))  # Create a data context covering 2018
spx = SecurityMaster.get_asset('SPX', AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE) # Lookup S&P 500 Index via the Security Master

with data_ctx:                                                          # Use the data context we setup
    skew = ts.skew(spx, '1m', ts.SkewReference.DELTA, 25)               # Get 25 delta skew
    skew.plot(title='SPX 25 Delta Skew')

plt.show()                                                              # Plot output
```

Should produce something like this:

![SPX 25 Delta Skew](/docs/gsquant/tutorials/images/spx_skew.png)
