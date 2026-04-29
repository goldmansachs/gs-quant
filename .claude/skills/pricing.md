---
name: gs-quant-pricing
description: "Pricing instruments and portfolios in gs_quant: PricingContext, HistoricalPricingContext for historical pricing over date ranges, and LiveMarket for real-time FX pricing. Covers pricing dates, market data location, batch mode, and async patterns."
---

# Pricing in gs_quant

## PricingContext Basics

All pricing in gs_quant happens within a `PricingContext`. The default context uses today's close-of-business market data.

```python
from gs_quant.markets import PricingContext
from gs_quant.risk import DollarPrice, IRDelta

# Implicit default context — uses today's close
price = swap.dollar_price()

# Explicit context with parameters
with PricingContext(pricing_date=dt.date(2025, 1, 15), market_data_location='LDN'):
    price_f = swap.dollar_price()
    delta_f = swap.calc(IRDelta)

price = price_f.result()
delta = delta_f.result()
```

**Key parameters:**

| Parameter | Description |
|---|---|
| `pricing_date` | Date for pricing (default: today) |
| `market_data_location` | `'NYC'`, `'LDN'`, or `'HKG'` (default: `'LDN'`) |
| `market` | Market object (e.g. `CloseMarket()`, `LiveMarket()`) |
| `csa_term` | CSA term for discounting |
| `is_batch` | Use batch mode for long-running calculations |
| `is_async` | Return immediately without blocking |
| `show_progress` | Display a tqdm progress bar |

Inside an entered `PricingContext`, calculations return `PricingFuture` objects. Call `.result()` after exiting the context.

---

## Resolving Under a Pricing Context

Resolution can be targeted to a specific date or market:

```python
from gs_quant.markets import PricingContext
import datetime as dt

with PricingContext(pricing_date=dt.date(2025, 1, 15)):
    resolved = swap.resolve(in_place=False)
    resolved_swap = resolved.result()
```

Historical resolution across multiple dates (must use `in_place=False`):

```python
from gs_quant.markets import HistoricalPricingContext

with HistoricalPricingContext(dt.date(2025, 1, 1), dt.date(2025, 1, 31)):
    resolved_by_date = swap.resolve(in_place=False)

# resolved_by_date is a dict of {date: resolved_instrument}
```

---

## Historical Pricing with `HistoricalPricingContext`

Compute risk measures across a range of dates using the close-of-business market for each date.

### Basic Usage

```python
import datetime as dt
from gs_quant.instrument import IRSwap
from gs_quant.markets import HistoricalPricingContext
from gs_quant.risk import DollarPrice

swap = IRSwap('Pay', '10y', 'USD')

with HistoricalPricingContext(dt.date(2025, 1, 2), dt.date(2025, 1, 31)):
    price_f = swap.price()

price_series = price_f.result()  # a pandas Series indexed by date
```

### By Number of Business Days

```python
with HistoricalPricingContext(10):
    price_f = swap.price()

price_series = price_f.result()
```

### With Custom Date List

```python
dates = [dt.date(2025, 1, 2), dt.date(2025, 3, 15), dt.date(2025, 6, 30)]

with HistoricalPricingContext(dates=dates):
    price_f = swap.price()
```

### Key Parameters

| Parameter | Description |
|---|---|
| `start` | Start date (or number of business days back from today) |
| `end` | End date (defaults to today) |
| `calendars` | Holiday calendar(s) for date generation |
| `dates` | Explicit iterable of dates (mutually exclusive with `start`) |
| `is_batch` | Use batch mode for long-running calculations (avoids timeouts) |
| `is_async` | Return immediately without blocking |
| `show_progress` | Display a tqdm progress bar |
| `market_data_location` | `'NYC'`, `'LDN'`, or `'HKG'` (defaults to `'LDN'`) |
| `csa_term` | CSA term for discounting |

### Historical Pricing with Portfolios

```python
with HistoricalPricingContext(dt.date(2025, 1, 2), dt.date(2025, 1, 31)):
    result = portfolio.calc(DollarPrice)

# result is a PortfolioRiskResult with a date dimension
```

---

## Live Market Pricing with `LiveMarket`

By default, `PricingContext` uses close-of-business market data. To price against **real-time, live market data**, set `market=LiveMarket()`. This uses a market snapshot captured at the moment the calculation runs.

> **Note:** Live market pricing is currently only available for **FX instruments** (e.g. `FXOption`, `FXForward`, `FXBinary`, `FXMultiCrossBinary`).

### Basic Usage

```python
from gs_quant.instrument import FXOption
from gs_quant.markets import PricingContext, LiveMarket
from gs_quant.risk import DollarPrice

option = FXOption(
    pair='EURUSD',
    expiration_date='3m',
    option_type='Call',
    strike_price='ATMF',
    notional_amount=10e6,
    premium=0,
)

with PricingContext(market=LiveMarket()):
    price_f = option.dollar_price()

price = price_f.result()  # priced against the live market
```

### Live Market with Portfolios

```python
from gs_quant.instrument import FXOption, FXForward
from gs_quant.markets import PricingContext, LiveMarket
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import DollarPrice

portfolio = Portfolio([
    FXOption(pair='EURUSD', expiration_date='3m', option_type='Call',
             strike_price='ATMF', notional_amount=10e6, premium=0, name='EUR Call'),
    FXForward(pair='USDJPY', settlement_date='6m', notional_amount=10e6, name='JPY Fwd'),
])

with PricingContext(market=LiveMarket()):
    result = portfolio.calc(DollarPrice)

prices = result[DollarPrice]
```

### Key Points

- **FX only** — `LiveMarket` is currently supported for FX instruments only.
- **No caching** — results are not cached since the market state changes continuously.
- **Combines with other parameters** — you can still set `csa_term`, `is_async`, `is_batch`, etc. alongside `market=LiveMarket()`.

See `gs-quant-results` for how to extract and work with calculation results.
