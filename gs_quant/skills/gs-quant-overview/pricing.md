# Pricing in gs_quant

Pricing instruments and portfolios in gs_quant: PricingContext, HistoricalPricingContext for historical pricing over date ranges, and LiveMarket for real-time FX pricing. Covers which close market is used, market data location, choosing contexts for speed, long calculations and batch mode, relative terms and `resolve()`, and async patterns.

## PricingContext Basics

All pricing in gs_quant happens within a `PricingContext`. Without `market=`, it prices on a close market; see "Close market and location" below for which close.

```python
from gs_quant.markets import PricingContext
from gs_quant.risk import DollarPrice, IRDelta

# Implicit default context
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
| `market_data_location` | `'NYC'`, `'LDN'`, `'HKG'` or `'TKO'` (default: `'LDN'`) |
| `market` | Market object (e.g. `CloseMarket()`, `LiveMarket()`) |
| `csa_term` | CSA term for discounting |
| `is_batch` | Use batch mode for long-running calculations |
| `is_async` | Return immediately without blocking |
| `show_progress` | Display a tqdm progress bar |

Inside an entered `PricingContext`, calculations return `PricingFuture` objects. Call `.result()` after exiting the context.

---

## Close market and location: prices differ from other tools, or look a day old

**Without `market=`, gs_quant prices on the close of the pricing date at `market_data_location`
(default LDN)**, in both `PricingContext` and `HistoricalPricingContext`. Today is the exception:
by default gs_quant assumes today's close isn't marketized until midnight in that location, so
today (the default pricing date) is priced on the previous weekday's close, and so is the last date
of a `HistoricalPricingContext` ending today. A weekend or holiday you pass as the pricing date is
not moved to a business day.

**Set `market_data_location` to the close you compare against.** NYC and LDN closes are different
snapshots, so location is a common reason gs_quant disagrees with other tools. Set it on the
outermost context (inner contexts inherit it), or once for the session, outside any context:

```python
PricingContext.current = PricingContext(market_data_location='NYC')
```

**For live prices, pass a live market:** `PricingContext(market=LiveMarket('NYC'))`.

**To use today's close once it is in**, set the time when you expect the close data to have been
marketized, in the pricing context's location:

```python
CloseMarket.roll_hr_and_min = (17, 30)
```

After that time, if today's close isn't in yet, pricing fails.
`CloseMarket(date=..., location=..., check=False)` always uses exactly the date you give.

---

## Choosing contexts: slow code, many requests, 504s

**Pick the context by the shape of the job.**

| Job | Use |
|---|---|
| Same instrument(s), many dates | one `HistoricalPricingContext` |
| Many instruments, one date | one `PricingContext` around a `Portfolio` |
| Instrument terms change per date (strike from that day's spot, expiry from a row, a field that must equal the pricing date) | an outer `PricingContext` with an inner dated one per date |
| A step needs an earlier result (resolve, then price later; hedge on the previous delta) | separate contexts in sequence, `.result()` in between |

```python
prices = {}
with PricingContext(market_data_location='NYC'):  # outer: sends everything on exit
    for d, inst in instrument_by_date.items():
        with PricingContext(pricing_date=d):  # inner: sets only the date
            prices[d] = inst.price()
prices = {d: f.result() for d, f in prices.items()}
```

**Don't open and exit a `PricingContext` on every pass of a loop:** each exit sends and waits, so
requests go one at a time. If you must, set `is_async=True` and call `.result()` only after the loop.

**If you must use a scenario, wrap it in a pricing context.** A scenario is not a pricing context:
outside a `PricingContext`, each `.calc()` is sent and awaited on its own, even inside
`with MarketDataShockBasedScenario(...)`. Write `with scenario, PricingContext():`.

**There should be no need to add your own threads.** `PricingContext` already sends requests in
parallel.

---

## Long calculations: timeouts, `is_batch`

**Set `is_batch=True` on the context for calculations that take more than about 3 minutes.**
Without it, each request must finish within about 3 minutes or fail; with it, results come back
over a websocket and each request gets up to 10 minutes. If the websocket drops, see `errors.md`.

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
| `market_data_location` | `'NYC'`, `'LDN'`, `'HKG'` or `'TKO'` (defaults to `'LDN'`) |
| `csa_term` | CSA term for discounting |

### Historical Pricing with Portfolios

```python
with HistoricalPricingContext(dt.date(2025, 1, 2), dt.date(2025, 1, 31)):
    result = portfolio.calc(DollarPrice)

# result is a PortfolioRiskResult with a date dimension
```

---

## Relative terms and resolve(): marking an entered trade to market

**Relative terms are re-resolved on every pricing date, so they describe a new trade on each
date** (e.g. `expiry='6m'` means a new 6-month option each day, not one option ageing). To mark an
entered trade to market, fix its terms on the entry date: resolve it on that date (or give absolute
dates and levels), then price it on later dates.

```python
with PricingContext(pricing_date=entry_date, market_data_location='NYC'):
    trade.resolve()  # fields are filled in when the context exits
with HistoricalPricingContext(entry_date, end, market_data_location='NYC'):
    mtm = trade.price()
mtm = mtm.result()
```

**If you resolve to read the terms, resolve in the same context you price in.** `resolve()` fixes
the terms on the market it runs under (the default close if there is no context), so pricing it on
another market prices a trade struck on the first one, e.g. yesterday's ATM strike under today's
live market.

**`resolve()` does not raise when it fails.** It logs the error and leaves the field as you wrote
it (e.g. still the string `'ATM'`); check the resolved fields before using them.

**`resolve(in_place=False)` returns the resolved copy instead of changing the instrument**, like any
other calculation: a future inside a context, so call `.result()`. Under `HistoricalPricingContext`
it is the only option, and the result is a dict of resolved copies by date (useful to see, say, the
strike each date picks). `in_place=True` raises there, because one object can't hold a different set
of terms for each date.

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

portfolio = Portfolio(
    [
        FXOption(
            pair='EURUSD',
            expiration_date='3m',
            option_type='Call',
            strike_price='ATMF',
            notional_amount=10e6,
            premium=0,
            name='EUR Call',
        ),
        FXForward(pair='USDJPY', settlement_date='6m', notional_amount=10e6, name='JPY Fwd'),
    ]
)

with PricingContext(market=LiveMarket()):
    result = portfolio.calc(DollarPrice)

prices = result[DollarPrice]
```

### Key Points

- **No caching** — results are not cached since the market state changes continuously.
- **Combines with other parameters** — you can still set `csa_term`, `is_async`, `is_batch`, etc. alongside `market=LiveMarket()`.

See `results.md` for more information on extracting results from pricing calculation (FloatWithInfo, DataFrameWithInfo, PortfolioRiskResult, etc.)
