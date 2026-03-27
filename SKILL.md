---
name: gs-quant
description: "This document covers the core workflows for using the `gs_quant` library: establishing a session, constructing and resolving instruments, building portfolios, pricing historically, and extracting results."
---

## 1. Creating a Session with `GsSession.use`

All API communication in `gs_quant` flows through an authenticated `GsSession`. Before making any pricing or data calls you must initialise a session with `GsSession.use()`.

### OAuth2 (Application Credentials)

```python
from gs_quant.session import GsSession, Environment

GsSession.use(
    environment_or_domain=Environment.PROD,
    client_id='my_client_id',
    client_secret='my_client_secret',
    scopes=('run_analytics',)
)
```

- **`environment_or_domain`** — `Environment.PROD` (default), `Environment.QA`, or `Environment.DEV`. You can also pass a raw URL string.
- **`client_id` / `client_secret`** — OAuth2 application credentials. When both are provided the library creates an `OAuth2Session`.
- **`scopes`** — Optional iterable of `GsSession.Scopes` values. Usually when pricing trade you will need `RUN_ANALYTICS`.

### Kerberos / SSO (Internal GS)

If no `client_id` is supplied, the library will attempt Kerberos or pass-through authentication automatically:
This is for internal GS users only and requires appropriate network access and installation of gs_quant_internal.

```python
GsSession.use(Environment.PROD)
```

### Using as a Context Manager

`GsSession` can also be used as a context manager so the session is cleaned up on exit:

```python
with GsSession.get(Environment.PROD, client_id='...', client_secret='...') as session:
    # session is active inside this block
    ...
```

### Verifying the Session

After calling `GsSession.use(...)`, the active session is accessible as:

```python
GsSession.current  # the currently active GsSession instance
```

All subsequent API calls (instrument resolution, pricing, data queries) will use this session automatically.

---

## 2. Constructing Trades with `gs_quant.instrument`

Instruments are the building blocks of gs_quant. Every tradeable product is represented as a dataclass in `gs_quant.instrument`. Construct an instrument by importing its class and supplying the key economic parameters — any parameter you omit will be resolved by the server later.
### Common Instrument Examples

#### Interest Rate Swap

```python
from gs_quant.instrument import IRSwap

swap = IRSwap(
    pay_or_receive='Pay',       # 'Pay' or 'Receive' the fixed leg
    termination_date='10y',     # tenor or explicit date
    notional_currency='USD',    # currency
    fixed_rate=0.03,            # optional — leave None to resolve at market
)
```

#### Cross-Currency Swap — Fix / Fix (`IRXccySwapFixFix`)

Both legs pay a fixed coupon. Each leg has its own notional, set independently to encode
the agreed FX rate at inception.

```python
from gs_quant.instrument import IRXccySwapFixFix
from gs_quant.common import Currency, PrincipalExchange

swap = IRXccySwapFixFix(
    termination_date='5y',
    effective_date='0b',                # spot start
    payer_currency=Currency.USD,
    payer_rate=0.04,                    # 4.00% fixed USD coupon
    receiver_currency=Currency.EUR,
    receiver_rate=0.025,                # 2.50% fixed EUR coupon
    notional_amount=10e6,
    principal_exchange=PrincipalExchange.Both,
)
swap.resolve()
```

Key parameters: `payer_rate`, `receiver_rate`, `notional_amount` (payer leg),
`receiver_notional_amount` (receiver leg — set explicitly to encode the agreed FX rate),
`payer_frequency`, `receiver_frequency`, `payer_day_count_fraction`,
`receiver_day_count_fraction`, `payer_business_day_convention`,
`receiver_business_day_convention`.

#### Cross-Currency Swap — Fix / Float (`IRXccySwapFixFlt`)

One leg pays a fixed rate; the other pays a floating rate (LIBOR/RFR + spread).
`pay_or_receive` controls which side you pay. Currencies are specified via
`fixed_rate_currency` and `floating_rate_currency` (not payer/receiver).

```python
from gs_quant.instrument import IRXccySwapFixFlt
from gs_quant.common import Currency, PrincipalExchange, PayReceive

swap = IRXccySwapFixFlt(
    pay_or_receive=PayReceive.Pay,      # pay fixed USD, receive floating EUR
    termination_date='5y',
    effective_date='0b',
    fixed_rate_currency=Currency.USD,
    fixed_rate=0.04,                    # 4.00% fixed USD rate
    floating_rate_currency=Currency.EUR,
    floating_rate_spread=0.0,
    notional_amount=10000,
    principal_exchange=PrincipalExchange.Both,
)
swap.resolve()
```

Key parameters: `pay_or_receive`, `fixed_rate_currency`, `fixed_rate`,
`fixed_rate_frequency`, `fixed_rate_day_count_fraction`,
`fixed_rate_business_day_convention`, `fixed_first_stub`, `fixed_last_stub`,
`fixed_holidays`, `floating_rate_currency`, `floating_rate_option`,
`floating_rate_designated_maturity`, `floating_rate_spread`, `floating_rate_frequency`,
`floating_rate_day_count_fraction`, `floating_rate_business_day_convention`,
`floating_first_stub`, `floating_last_stub`, `floating_holidays`,
`floating_rate_for_the_initial_calculation_period`.

#### Cross-Currency Swap — Float / Float non-MTM (`IRXccySwapFltFlt`)

Both legs pay a floating rate in different currencies. The notional is **fixed for the
life of the trade** — the FX rate does not reset. Set `receiver_amount` to encode the
agreed FX rate. The XCcy basis spread is typically applied as `receiver_spread`.

```python
from gs_quant.instrument import IRXccySwapFltFlt
from gs_quant.common import Currency, PrincipalExchange

swap = IRXccySwapFltFlt(
    termination_date='5y',
    effective_date='0b',
    payer_currency=Currency.USD,
    payer_spread=0.0,
    receiver_currency=Currency.EUR,
    receiver_spread=0.0,                # XCcy basis spread — resolve at par if omitted
    notional_amount=10000,
    principal_exchange=PrincipalExchange.Both,
)
swap.resolve()
```

Key parameters: `payer_rate_option`, `payer_designated_maturity`, `payer_spread`,
`payer_frequency`, `payer_day_count_fraction`, `payer_business_day_convention`,
`payer_first_stub`, `payer_last_stub`, `payer_holidays`, and the equivalent `receiver_*`
fields. `receiver_amount` encodes the agreed FX rate and is fixed at inception.

#### Cross-Currency Swap — Float / Float MTM (`IRXccySwap`)

Same structure as `IRXccySwapFltFlt` but the receiver notional **resets to FX spot at
each period start**, eliminating FX credit exposure. This is the standard interbank
product. Note: `receiver_amount` is **not** a field — the receiver notional is computed
automatically each period.

```python
from gs_quant.instrument import IRXccySwap
from gs_quant.common import Currency, PrincipalExchange, PayReceive

swap = IRXccySwap(
    termination_date='5y',
    effective_date='0b',
    payer_currency=Currency.USD,
    payer_spread=0.0,
    receiver_currency=Currency.EUR,
    receiver_spread=0.0,                # XCcy basis — resolve at par if omitted
    notional_amount=10000,         # payer notional only; receiver resets to FX spot
    principal_exchange=PrincipalExchange.Both,
    # initial_fx_rate=1.10,             # optional: pin the opening FX rate
    # notional_reset_side=PayReceive.Receive,  # default — receiver resets (standard MTM)
)
swap.resolve()
```

Key additional parameters vs `IRXccySwapFltFlt`: `initial_fx_rate` (optional, pins the
opening FX rate), `notional_reset_side` (`PayReceive.Receive` by default — the standard
convention). `receiver_amount` is absent; do not set it.

**MTM vs non-MTM at a glance:**

| | `IRXccySwap` (MTM) | `IRXccySwapFltFlt` (non-MTM) |
|---|---|---|
| Receiver notional | Resets to FX spot each period | Fixed at inception |
| FX credit exposure | Eliminated | Builds up over trade life |
| `receiver_amount` field | Not present | Required — encodes the agreed FX rate |
| `initial_fx_rate` field | Available | Not available |
| `notional_reset_side` field | Available | Not available |

All four XCcy swap types accept `principal_exchange` (`PrincipalExchange.Both` is
standard — notionals exchanged at start and maturity) and an optional `fee` /
`fee_currency` / `fee_payment_date`. Note if you have a principal exchange which is
in the past this cash flow will not be ignored by the Price measure.  So in general
only have exchanges which are in the past relative to the PricingContext.
Relevant risk measures:

```python
from gs_quant.risk import IRDeltaParallel, IRXccyDeltaParallel, IRDelta, IRXccyDelta
# IRDeltaParallel      — total rate DV01 (1bp parallel shift in discount/fwd curve, USD)
# IRXccyDeltaParallel  — total XCcy basis DV01 (1bp shift in cross-ccy basis, USD)
# IRDelta              — bucketed rate delta ladder (per tenor)
# IRXccyDelta          — bucketed XCcy basis delta ladder (per tenor)
```

---

#### Interest Rate Swaption

```python
from gs_quant.instrument import IRSwaption

swaption = IRSwaption(
    pay_or_receive='Receive',
    termination_date='10y',
    notional_currency='EUR',
    expiration_date='1y',
    strike='ATM',
)
```

#### Interest Rate Cap

```python
from gs_quant.instrument import IRCap

cap = IRCap(
    termination_date='1y',
    notional_currency='USD',
)
```

#### FX Option

```python
from gs_quant.instrument import FXOption

option = FXOption(
    pair='EURUSD',
    expiration_date='3m',
    option_type='Call',
    strike_price='ATMF',
    notional_amount=10e6,
)
```

#### FX Forward

```python
from gs_quant.instrument import FXForward

fwd = FXForward(
    pair='USDJPY',
    settlement_date='6m',
    notional_amount=10e6,
)
```

### Important: FX Instrument Pitfalls

There are two common mistakes when working with FX options that can lead to confusing results:

#### 1. Always Set `premium=0` on FX Options

When constructing FX options (FXOption, FXBinary, FXMultiCrossBinary, etc.), if you don't specify a `premium`, the instrument resolution will automatically set a premium such that the `DollarPrice` becomes zero. This is by design — it represents a "fair value" trade where the premium exactly offsets the option value.

**Problem:** If you want to know the cost/value of the option, you'll always get 0.

**Solution:** Always set `premium=0` explicitly when you want `DollarPrice` to return the actual option value:

```python
from gs_quant.instrument import FXOption, FXBinary

# WRONG - DollarPrice will be ~0 after resolution
option_wrong = FXOption(
    pair='EURUSD',
    expiration_date='3m',
    option_type='Call',
    strike_price='ATMF',
    notional_amount=10e6,
)

# CORRECT - DollarPrice will be the option value
option_correct = FXOption(
    pair='EURUSD',
    expiration_date='3m',
    option_type='Call',
    strike_price='ATMF',
    notional_amount=10e6,
    premium=0,  # <-- Important!
)

# Same applies to FXBinary
binary = FXBinary(
    pair='EURUSD',
    buy_sell=BuySell.Buy,
    option_type=OptionType.Call,
    strike_price='s',
    notional_amount=1e6,
    notional_currency=Currency.USD,
    expiration_date='3m',
    premium=0,  # <-- Important!
)
```

#### 2. FXMultiCrossBinaryLeg Uses Different OptionType Values

When constructing `FXMultiCrossBinaryLeg` objects (used within `FXMultiCrossBinary` for dual digital options), you must use `OptionType.Binary_Call` or `OptionType.Binary_Put` — **not** `OptionType.Call` or `OptionType.Put`.

This is different from `FXBinary` which uses `OptionType.Call` / `OptionType.Put`.

```python
from gs_quant.instrument import FXBinary, FXMultiCrossBinary, FXMultiCrossBinaryLeg
from gs_quant.common import BuySell, OptionType, Currency

# FXBinary uses OptionType.Call / OptionType.Put
single_digital = FXBinary(
    pair='EURUSD',
    buy_sell=BuySell.Buy,
    option_type=OptionType.Call,  # <-- Call or Put
    strike_price='s',
    notional_amount=1e6,
    notional_currency=Currency.USD,
    expiration_date='3m',
    premium=0,
)

# FXMultiCrossBinaryLeg uses OptionType.Binary_Call / OptionType.Binary_Put
dual_digital = FXMultiCrossBinary(
    legs=(
        FXMultiCrossBinaryLeg(
            pair='EURUSD',
            option_type=OptionType.Binary_Call,  # <-- Binary_Call or Binary_Put
            strike_price='s',
        ),
        FXMultiCrossBinaryLeg(
            pair='USDJPY',
            option_type=OptionType.Binary_Call,  # <-- Binary_Call or Binary_Put
            strike_price='s',
        ),
    ),
    buy_sell=BuySell.Buy,
    notional_amount=1e6,
    notional_currency=Currency.USD,
    expiration_date='3m',
    premium=0,  # <-- Don't forget this too!
)
```

#### Equity Option

```python
from gs_quant.instrument import EqOption

eq_opt = EqOption(
    underlier='.SPX',
    expiration_date='3m',
    strike_price='ATMF',
    option_type='Call',
    option_style='European',
)
```

You can set the instrument `name` property for easy identification later:

```python
swap.name = 'USD 10y Payer'
```

---

## 3. Resolving an Instrument

When you construct an instrument you typically only specify a subset of its parameters. **Resolving** fills in all remaining fields by sending the instrument to the GS pricing service, which returns a fully specified version based on current market data.

```python
from gs_quant.instrument import IRSwap

swap = IRSwap('Pay', '10y', 'USD')

# Before resolve: swap.fixed_rate is None
swap.resolve()
# After resolve: swap.fixed_rate is now populated with the current par rate

print(swap.fixed_rate)  # e.g. 0.0345
```

### What `resolve()` Does

1. Sends the instrument to the GS analytics service along with the current `PricingContext` (pricing date and market).
2. The service computes any missing parameters — for example the fixed rate of a par swap, the premium of an option, or the forward points of an FX forward.
3. By default (`in_place=True`), the instrument is updated in place. Pass `in_place=False` to receive a new resolved copy instead.

### Resolve Under a Specific Pricing Date

```python
from gs_quant.markets import PricingContext
import datetime as dt

with PricingContext(pricing_date=dt.date(2025, 1, 15)):
    resolved = swap.resolve(in_place=False)
    resolved_swap = resolved.result()
```

### Historical Resolution

Resolution can be done across multiple dates via `HistoricalPricingContext`, but `in_place` must be `False`:

```python
from gs_quant.markets import HistoricalPricingContext
import datetime as dt

with HistoricalPricingContext(dt.date(2025, 1, 1), dt.date(2025, 1, 31)):
    resolved_by_date = swap.resolve(in_place=False)

# resolved_by_date is a dict of {date: resolved_instrument}
```

---

## 4. Combining Instruments in Portfolios

The `Portfolio` class groups instruments together so you can price, resolve, and analyse them as a single unit.

### Creating a Portfolio

```python
from gs_quant.instrument import IRSwap, IRSwaption
from gs_quant.markets.portfolio import Portfolio

swap = IRSwap('Pay', '10y', 'USD', name='USD 10y Payer')
swaption = IRSwaption('Receive', '10y', 'EUR', expiration_date='1y', name='EUR 1y10y Receiver')

portfolio = Portfolio([swap, swaption], name='My Portfolio')
```

You can also construct a portfolio from a dictionary (keys become instrument names):

```python
portfolio = Portfolio({
    'USD 10y Payer': IRSwap('Pay', '10y', 'USD'),
    'EUR 5y Receiver': IRSwap('Receive', '5y', 'EUR'),
})
```

### Nesting Portfolios

Portfolios can contain other portfolios, creating a hierarchy:

```python
usd_book = Portfolio([IRSwap('Pay', '5y', 'USD'), IRSwap('Receive', '10y', 'USD')], name='USD Book')
eur_book = Portfolio([IRSwap('Pay', '5y', 'EUR')], name='EUR Book')

master = Portfolio([usd_book, eur_book], name='Master Book')
```

### Portfolio Operations

```python
# Add instruments
portfolio.append(IRSwap('Pay', '2y', 'GBP'))

# Iterate
for instrument in portfolio:
    print(instrument)

# Access by index
first = portfolio[0]

# Access by name
usd_swap = portfolio['USD 10y Payer']

# Number of top-level priceables
len(portfolio)

# All instruments across nested portfolios
portfolio.all_instruments
```

### Resolving a Portfolio

```python
portfolio.resolve()  # resolves all instruments in place
```

### Pricing a Portfolio

```python
from gs_quant.risk import DollarPrice, IRDelta

# Single risk measure
prices = portfolio.calc(DollarPrice)

# Multiple risk measures at once
results = portfolio.calc([DollarPrice, IRDelta])
```

The result is a `PortfolioRiskResult` which can be sliced by instrument, risk measure, or date (see section 6).

---

## 5. Historical Pricing with `HistoricalPricingContext`

`HistoricalPricingContext` lets you compute risk measures across a range of dates using the close-of-business market for each date.

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

Pass an integer to price over the last N business days:

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

## 6. Result Extraction

Calculation results in gs_quant are rich typed objects that carry metadata (risk key, unit, error info) alongside the actual values. Understanding the result types and how to extract data from them is essential.

### Result Types

| Type | Description |
|---|---|
| `FloatWithInfo` | Scalar result (e.g. present value). Behaves like a `float` but carries a `risk_key` and `unit`. |
| `SeriesWithInfo` | Time series result (historical pricing). A `pandas.Series` with metadata. |
| `DataFrameWithInfo` | Structured/bucketed result (e.g. delta ladder). A `pandas.DataFrame` with metadata. |
| `ErrorValue` | Indicates a calculation error. Check `.error` for the message. |
| `MultipleRiskMeasureResult` | Dict-like mapping of `RiskMeasure → result` when multiple measures are requested on a single instrument. |
| `PortfolioRiskResult` | Result for a portfolio — can be sliced by instrument, risk measure, or date. |

### Single Instrument Results

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

### Using Futures (Async / Batched)

Inside an entered `PricingContext`, calculations return `PricingFuture` objects. Call `.result()` after exiting the context:

```python
from gs_quant.markets import PricingContext

with PricingContext():
    price_f = swap.dollar_price()
    delta_f = swap.calc(IRDelta)

price = price_f.result()   # FloatWithInfo
delta = delta_f.result()   # DataFrameWithInfo
```

### Multiple Risk Measures on a Single Instrument

```python
from gs_quant.risk import DollarPrice, IRDelta, IRVega

result = swap.calc([DollarPrice, IRDelta, IRVega])  # MultipleRiskMeasureResult

price = result[DollarPrice]    # FloatWithInfo
delta = result[IRDelta]        # DataFrameWithInfo
vega = result[IRVega]          # DataFrameWithInfo
```

### Portfolio Results

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

### Historical Results

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

### Converting to DataFrames

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

### Checking for Errors

```python
from gs_quant.risk import ErrorValue

price = swap.dollar_price()
if isinstance(price, ErrorValue):
    print(f'Calculation failed: {price.error}')
else:
    print(f'Price: {float(price)}')
```

### Arithmetic on Results

Results support arithmetic operations, which is useful for computing P&L or scaling:

```python
# Multiply portfolio result by a scalar
scaled = result * 1000

# Add results from different portfolios
combined = result_a + result_b
```

---

## 7. Backtesting

gs_quant includes a full backtesting framework under `gs_quant.backtests`. It lets you define trading strategies as combinations of **triggers** (when to act) and **actions** (what to do), then simulate them historically using one of several engines.

For the complete backtesting guide — including all trigger types, action types, engine selection, and result extraction — see:

📄 **[`gs_quant/backtests/SKILL.md`](gs_quant/backtests/SKILL.md)**

### Quick Example — Monthly FX Option Roll

```python
from datetime import date
from gs_quant.instrument import FXOption
from gs_quant.common import BuySell, OptionType
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.strategy import Strategy
from gs_quant.risk import Price

start_date = date(2023, 1, 3)
end_date = date(2024, 12, 31)

call = FXOption(
    buy_sell=BuySell.Buy, option_type=OptionType.Call,
    pair='USDJPY', strike_price='ATMF', expiration_date='2y',
    name='2y_call', premium=0,
)

trig_req = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m')
action = AddTradeAction(call, '1m')
trigger = PeriodicTrigger(trig_req, action)

strategy = Strategy(None, trigger)
GE = GenericEngine()
backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

# View results
backtest.result_summary['Total'].plot(title='Performance')
```

---

## 8. Accessing Data with `Dataset`

The `Dataset` class in `gs_quant.data` provides access to Marquee datasets — structured,
time-series collections of market and reference data. Each dataset has a fixed schema, a
set of symbol dimensions (e.g. `bbid`, `assetId`, `ticker`), and entitlements that control
access.

```python
from gs_quant.data import Dataset
import datetime as dt
```

### Constructing a Dataset

Pass the dataset ID string (visible in the Marquee catalog URL):

```python
ds = Dataset('FXIVOL_STANDARD')
```

You can also use the built-in vendor enums to avoid hardcoding strings:

```python
ds = Dataset(Dataset.GS.HOLIDAY)
ds = Dataset(Dataset.TR.TREOD)
```

> **Equities and listed instruments:** For equities and most other listed instruments
> (equity indices, ETFs, futures, etc.) the correct dataset is almost always `TREOD`
> (Thomson Reuters End-of-Day). This is a broad coverage, daily EOD dataset sourced from
> Refinitiv. Use `bbid` as the symbol dimension.
>
> ```python
> ds = Dataset('TREOD')                          # or Dataset(Dataset.TR.TREOD)
> df = ds.get_data(dt.date(2025, 1, 2), dt.date(2026, 3, 19), bbid=['GS UN', 'AAPL UW'])
> ```

### `get_data` — Fetch a DataFrame

The primary method. Returns a `pandas.DataFrame` with one row per data point.

```python
df = ds.get_data(
    start=dt.date(2025, 1, 2),
    end=dt.date(2025, 3, 19),
    bbid=['EURUSD', 'USDJPY'],      # filter by symbol dimension — passed as kwargs
)
```

**Key parameters:**

| Parameter | Description |
|---|---|
| `start` | Start date or datetime of the query |
| `end` | End date or datetime (inclusive) |
| `as_of` | Return data as it existed at this point in time |
| `since` | Return data updated since this datetime |
| `fields` | List of field names to return; omit for all fields |
| `**kwargs` | Symbol dimension filters, e.g. `bbid=['EURUSD']`, `ticker='SPX'`, `assetId='...'` |

Filter kwargs match the dataset's symbol dimensions exactly — check the Marquee catalog
page for the correct dimension name. Multiple values are passed as a list.

```python
# Filter by a single value
df = ds.get_data(dt.date(2025, 1, 2), dt.date(2025, 3, 19), bbid='EURUSD')

# Filter by multiple values
df = ds.get_data(dt.date(2025, 1, 2), dt.date(2025, 3, 19), bbid=['EURUSD', 'GBPUSD'])

# Restrict to specific fields
df = ds.get_data(dt.date(2025, 1, 2), dt.date(2025, 3, 19),
                 bbid=['EURUSD'],
                 fields=['impliedVolatility', 'tenor'])

# Query specific dates rather than a range
df = ds.get_data(dates=[dt.date(2025, 1, 15), dt.date(2025, 3, 19)], bbid=['EURUSD'])
```

### `get_data_series` — Fetch a Single-Field Time Series

Returns a `pandas.Series` indexed by date/time when the dataset has exactly one symbol
dimension and you want a single field:

```python
series = ds.get_data_series(
    field='impliedVolatility',
    start=dt.date(2025, 1, 2),
    end=dt.date(2025, 3, 19),
    bbid='EURUSD',
)
# series is a pd.Series indexed by date
```

### `get_data_last` — Most Recent Data Point

Returns the latest available row at or before `as_of`:

```python
latest = ds.get_data_last(
    as_of=dt.datetime.now(),
    bbid=['EURUSD', 'USDJPY'],
)
```

### `get_coverage` — What Assets Are Available

Returns a DataFrame listing every symbol covered by the dataset:

```python
coverage = ds.get_coverage()
print(coverage.head())

# Include the history start date for each asset
coverage = ds.get_coverage(include_history=True)
coverage = coverage.sort_values('historyStartDate')
```

### Iterating Over Large Queries

For datasets with many assets or long date ranges, break the query into smaller chunks
to avoid API limits:

```python
import datetime as dt

def query_in_batches(dataset, ids, start, end, id_field='bbid', time_delta=dt.timedelta(days=30)):
    """Fetch data in time batches for a list of symbol IDs."""
    frames = []
    batch_start = start
    while batch_start < end:
        batch_end = min(batch_start + time_delta, end)
        df = dataset.get_data(batch_start, batch_end, **{id_field: ids})
        frames.append(df)
        batch_start = batch_end
    return pd.concat(frames) if frames else pd.DataFrame()

import pandas as pd
ds = Dataset('EDRVOL_PERCENT_V1_STANDARD')
coverage = ds.get_coverage()
ids = coverage['assetId'].tolist()[:10]   # first 10 assets

df = query_in_batches(ds, ids, dt.date(2024, 1, 1), dt.date(2025, 3, 19), id_field='assetId')
```

### Uploading Data

You can write data back to a dataset you own:

```python
import pandas as pd

data = [
    {'date': '2025-03-19', 'city': 'London', 'maxTemperature': 14.0, 'minTemperature': 7.0},
    {'date': '2025-03-19', 'city': 'New York', 'maxTemperature': 18.0, 'minTemperature': 9.0},
]
ds = Dataset('MY_CUSTOM_DATASET')
ds.upload_data(data)                     # accepts list of dicts or a DataFrame
```

### Common Pitfalls

- **Wrong dimension name** — each dataset has its own symbol dimension (`bbid`, `assetId`,
  `ticker`, `ric`, etc.). Check the Marquee catalog page. Passing the wrong kwarg silently
  returns an empty DataFrame.
- **Query size limits** — very wide queries (many assets × long date range) will time out
  or be rejected. Iterate in batches as shown above.
- **Entitlements** — if `get_data` returns an empty DataFrame unexpectedly, your session
  may not have the required entitlement scope (e.g. `read_product_data`). Ensure your
  `GsSession` was initialised with the appropriate scopes.
- **Intraday vs daily** — some datasets are indexed by `datetime` (intraday); others by
  `date` (EOD). Pass `dt.datetime` objects for intraday datasets and `dt.date` for EOD.
