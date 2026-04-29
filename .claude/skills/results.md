---
name: gs-quant-results
description: "Extracting and working with gs_quant calculation results: FloatWithInfo, SeriesWithInfo, DataFrameWithInfo, ErrorValue, MultipleRiskMeasureResult, PortfolioRiskResult. Covers futures, slicing portfolio results by instrument/measure/date, historical results, to_frame(), error handling, and arithmetic."
---

# Result Extraction

Calculation results in gs_quant are rich typed objects that carry metadata (risk key, unit, error info) alongside the actual values.

## Result Types

| Type | Description |
|---|---|
| `FloatWithInfo` | Scalar result (e.g. present value). Behaves like a `float` but carries a `risk_key` and `unit`. |
| `SeriesWithInfo` | Time series result (historical pricing). A `pandas.Series` with metadata. |
| `DataFrameWithInfo` | Structured/bucketed result (e.g. delta ladder). A `pandas.DataFrame` with metadata. |
| `ErrorValue` | Indicates a calculation error. Check `.error` for the message. |
| `MultipleRiskMeasureResult` | Dict-like mapping of `RiskMeasure -> result` when multiple measures are requested on a single instrument. |
| `PortfolioRiskResult` | Result for a portfolio — can be sliced by instrument, risk measure, or date. |

## Single Instrument Results

```python
from gs_quant.instrument import IRSwap
from gs_quant.risk import DollarPrice, IRDelta

swap = IRSwap('Pay', '10y', 'USD')

# Scalar result
price = swap.dollar_price()       # FloatWithInfo
print(float(price))               # the numeric value

# Local currency price
local_price = swap.price()        # FloatWithInfo

# Structured result
delta = swap.calc(IRDelta)        # DataFrameWithInfo — a bucketed delta ladder
print(delta)                      # displays as a DataFrame with columns like mkt_type, mkt_asset, etc.
```

## Using Futures (Async / Batched)

Inside an entered `PricingContext`, calculations return `PricingFuture` objects. Call `.result()` after exiting the context:

```python
from gs_quant.markets import PricingContext

with PricingContext():
    price_f = swap.dollar_price()
    delta_f = swap.calc(IRDelta)

price = price_f.result()   # FloatWithInfo
delta = delta_f.result()   # DataFrameWithInfo
```

## Multiple Risk Measures on a Single Instrument

```python
from gs_quant.risk import DollarPrice, IRDelta, IRVega

result = swap.calc([DollarPrice, IRDelta, IRVega])  # MultipleRiskMeasureResult

price = result[DollarPrice]    # FloatWithInfo
delta = result[IRDelta]        # DataFrameWithInfo
vega = result[IRVega]          # DataFrameWithInfo
```

## Portfolio Results

`portfolio.calc()` returns a `PortfolioRiskResult` which supports flexible slicing:

```python
from gs_quant.risk import DollarPrice, IRDelta

result = portfolio.calc([DollarPrice, IRDelta])

# Slice by risk measure
prices = result[DollarPrice]          # PortfolioRiskResult for DollarPrice only

# Slice by instrument (name or object)
swap_result = result['USD 10y Payer']  # MultipleRiskMeasureResult for that instrument
swap_price = swap_result[DollarPrice]  # FloatWithInfo

# Slice by index
first_result = result[0]

# Iterate over instruments
for instrument_result in result:
    print(instrument_result)

# Aggregate across all instruments
total_price = result[DollarPrice].aggregate()  # sums all instrument prices
```

## Historical Results

When using `HistoricalPricingContext`, scalar results become time series:

```python
import datetime as dt
from gs_quant.markets import HistoricalPricingContext

with HistoricalPricingContext(dt.date(2025, 1, 2), dt.date(2025, 1, 31)):
    price_f = swap.price()

price_series = price_f.result()  # SeriesWithInfo indexed by date
print(price_series)

# Access value for a specific date
jan_15_price = price_series[dt.date(2025, 1, 15)]
```

Historical portfolio results can also be sliced by date:

```python
with HistoricalPricingContext(dt.date(2025, 1, 2), dt.date(2025, 1, 31)):
    result = portfolio.calc(DollarPrice)

# Slice by date
jan_15 = result[dt.date(2025, 1, 15)]  # PortfolioRiskResult for that single date

# Available dates
result.dates  # tuple of dt.date
```

## Converting to DataFrames

All result types support conversion to pandas DataFrames:

```python
# Portfolio result to DataFrame (pivoted)
df = result.to_frame()

# Unpivoted (raw records)
df_raw = result.to_frame(values=None, index=None, columns=None)

# Custom pivoting
df_custom = result.to_frame(values='value', index='dates', columns='instrument_name')
```

`MultipleRiskMeasureResult` also supports `.to_frame()`:

```python
multi_result = swap.calc([DollarPrice, IRDelta])
df = multi_result.to_frame()
```

## Checking for Errors

```python
from gs_quant.risk import ErrorValue

price = swap.dollar_price()
if isinstance(price, ErrorValue):
    print(f'Calculation failed: {price.error}')
else:
    print(f'Price: {float(price)}')
```

## Arithmetic on Results

Results support arithmetic operations, useful for computing P&L or scaling:

```python
# Multiply portfolio result by a scalar
scaled = result * 1000

# Add results from different portfolios
combined = result_a + result_b
```

## Common Risk Measures

```python
from gs_quant.risk import (
    DollarPrice,       # USD present value
    Price,             # local currency present value
    IRDelta,           # bucketed rate delta ladder
    IRDeltaParallel,   # total rate DV01 (1bp parallel shift)
    IRVega,            # bucketed IR vol sensitivity
    FXDelta,           # FX delta
    IRXccyDelta,       # bucketed cross-currency basis delta
    IRXccyDeltaParallel,  # total cross-currency basis DV01
)
```
