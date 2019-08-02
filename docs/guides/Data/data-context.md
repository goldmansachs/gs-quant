---
title: Data Contexts
excerpt: Understanding data contexts
datePublished: 2019/06/22
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Timeseries
  - Data
  - Data Context
  - Context
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Datasets
    url: /gsquant/guides/Data/datasets/
  - title: Timeseries
    url: /gsquant/guides/Data/timeseries/
  - title: Sessions
    url: /gsquant/guides/Authentication/1-sessions/
  - title: Security Master
    url: /gsquant/guides/Markets/security-master/
---

`DataContext`s are objects which provide a set of parameters which describe how to query data. These can be used to
provide a common context which can be reused for a number of different data access or manipulation functions. The
gs-quant market data apis use `DataContext` to determine how to query data (e.g. what date range to use) if no specific
parameters are provided.

## Creating a DataContext

Creating a `DataContext` is straightforward given a start and end date:

```python
from gs_quant.data import DataContext
from datetime import date

data_ctx = DataContext(start=date(2018, 1, 1), end=date(2018, 12, 31))       # Create data context
```

This example creates a context covering 2018.

## Usage

`DataContext`s can be used within a scoped block to provide a common reference for subsequent operations. Similar to
[Sessions](/gsquant/guides/Authentication/1-sessions/), there are two ways to use a DataContext:

- Set as global
- Use within a block

## Global Context

Any request which is not scoped will use the global data context automatically. The global context can be accessed through
`current`:

```python
current = DataContext.current     # Get current data context
DataContext.current = data_ctx    # Set current data context
```

## Scoped Context

`DataContext` objects can be used within blocks. This allows the same data query parameters shared by multiple requests
within a defined scope.

```python
data_ctx_2017 = DataContext(start=date(2017, 1, 1), end=date(2017, 12, 31))       # Create 2017 data context
data_ctx_2018 = DataContext(start=date(2018, 1, 1), end=date(2018, 12, 31))       # Create 2018 data context

with data_ctx_2017:

    # query data for 2017

with data_ctx_2018:

    # query data for 2018
```

## Example

The following example shows how to access historical implied volatility level for SPX using a `DataContext`:

<note>Requires an initialized GsSession and data subscription, please refer to <a href="/docs/gsquant/guides/Authentication/2-gs-session">
Sessions</a> for details</note>

```python
from datetime import date
from gs_quant.data import DataContext
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier, ExchangeCode
import gs_quant.timeseries as ts

data_ctx = DataContext(start=date(2018, 1, 1), end=date(2018, 12, 31))      # Create a data context covering 2018
spx = SecurityMaster.get_asset('SPX', AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE)               # Lookup S&P 500 Index via Security Master

with data_ctx:                                                              # Use the data context we setup
    vol = ts.implied_volatility(spx, '1m', ts.VolReference.DELTA_CALL, 25)  # Get 25 delta call implied volatility

vol.tail()
```

Output:

```
Out[1]:
2021-12-20 26.108257
2021-12-21 21.794968
2021-12-22 22.398788
2021-12-23 20.985507
2021-12-24 19.574263
dtype: float64
```
