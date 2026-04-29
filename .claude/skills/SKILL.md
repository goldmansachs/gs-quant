---
name: gs-quant-overview
description: "Quick-start guide for gs_quant: session setup with GsSession, constructing portfolios, resolving instruments. Start here for any gs_quant task."
---

# gs_quant Quick Start

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

```python
with GsSession.get(Environment.PROD, client_id='...', client_secret='...') as session:
    # session is active inside this block
    ...
```

### Verifying the Session

```python
GsSession.current  # the currently active GsSession instance
```

---

## 2. Resolving an Instrument

When you construct an instrument you typically only specify a subset of its parameters. **Resolving** fills in all remaining fields by sending the instrument to the GS pricing service.

```python
from gs_quant.instrument import IRSwap

swap = IRSwap('Pay', '10y', 'USD')

# Before resolve: swap.fixed_rate is None
swap.resolve()
# After resolve: swap.fixed_rate is now populated with the current par rate

print(swap.fixed_rate)  # e.g. 0.0345
```

### What `resolve()` Does

1. Sends the instrument to the GS analytics service along with the current `PricingContext`.
2. The service computes any missing parameters — par rate, premium, forward points, etc.
3. By default (`in_place=True`), the instrument is updated in place. Pass `in_place=False` to receive a new resolved copy.

---

## 3. Combining Instruments in Portfolios

The `Portfolio` class groups instruments for pricing, resolution, and analysis as a single unit.

### Creating a Portfolio

```python
from gs_quant.instrument import IRSwap, IRSwaption
from gs_quant.markets.portfolio import Portfolio

swap = IRSwap('Pay', '10y', 'USD', name='USD 10y Payer')
swaption = IRSwaption('Receive', '10y', 'EUR', expiration_date='1y', name='EUR 1y10y Receiver')

portfolio = Portfolio([swap, swaption], name='My Portfolio')
```

From a dictionary (keys become instrument names):

```python
portfolio = Portfolio({
    'USD 10y Payer': IRSwap('Pay', '10y', 'USD'),
    'EUR 5y Receiver': IRSwap('Receive', '5y', 'EUR'),
})
```

### Nesting Portfolios

```python
usd_book = Portfolio([IRSwap('Pay', '5y', 'USD'), IRSwap('Receive', '10y', 'USD')], name='USD Book')
eur_book = Portfolio([IRSwap('Pay', '5y', 'EUR')], name='EUR Book')
master = Portfolio([usd_book, eur_book], name='Master Book')
```

### Portfolio Operations

```python
portfolio.append(IRSwap('Pay', '2y', 'GBP'))  # add instruments
first = portfolio[0]                            # access by index
usd_swap = portfolio['USD 10y Payer']           # access by name
len(portfolio)                                  # top-level count
portfolio.all_instruments                       # all instruments across nested portfolios
```

### Resolving and Pricing

```python
from gs_quant.risk import DollarPrice, IRDelta

portfolio.resolve()                              # resolves all instruments in place
prices = portfolio.calc(DollarPrice)             # single risk measure
results = portfolio.calc([DollarPrice, IRDelta]) # multiple risk measures
```

---

## See Also

For detailed guidance on specific topics, see these focused skills:

- **`gs-quant-instruments`** (`.claude/skills/instruments.md`) — constructing all instrument types (IRSwap, XCcy swaps, FXOption, EqOption, etc.) and FX pitfalls
- **`gs-quant-pricing`** (`.claude/skills/pricing.md`) — PricingContext, HistoricalPricingContext, LiveMarket
- **`gs-quant-results`** (`.claude/skills/results.md`) — extracting results (FloatWithInfo, DataFrameWithInfo, PortfolioRiskResult, etc.)
- **`gs-quant-datasets`** (`.claude/skills/datasets.md`) — accessing market data with the Dataset class
- **`gs-quant-backtesting`** (`.claude/skills/backtesting.md`) — backtesting framework (triggers, actions, engines, results)
