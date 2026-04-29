---
name: gs-quant-instruments
description: "How to construct financial instruments in gs_quant: IRSwap, cross-currency swaps (IRXccySwap, IRXccySwapFltFlt, IRXccySwapFixFlt, IRXccySwapFixFix), IRSwaption, IRCap, FXOption, FXForward, FXBinary, FXMultiCrossBinary, EqOption. Includes FX pitfalls (premium=0, FXMultiCrossBinaryLeg OptionType)."
---

# Constructing Trades with `gs_quant.instrument`

Instruments are the building blocks of gs_quant. Every tradeable product is represented as a dataclass in `gs_quant.instrument`. Construct an instrument by importing its class and supplying the key economic parameters — any parameter you omit will be resolved by the server later.

## Interest Rate Swap

```python
from gs_quant.instrument import IRSwap

swap = IRSwap(
    pay_or_receive='Pay',       # 'Pay' or 'Receive' the fixed leg
    termination_date='10y',     # tenor or explicit date
    notional_currency='USD',    # currency
    fixed_rate=0.03,            # optional — leave None to resolve at market
)
```

## Cross-Currency Swap — Fix / Fix (`IRXccySwapFixFix`)

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

## Cross-Currency Swap — Fix / Float (`IRXccySwapFixFlt`)

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

## Cross-Currency Swap — Float / Float non-MTM (`IRXccySwapFltFlt`)

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

## Cross-Currency Swap — Float / Float MTM (`IRXccySwap`)

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
in the past this cash flow will not be ignored by the Price measure. So in general
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

## Interest Rate Swaption

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

## Interest Rate Cap

```python
from gs_quant.instrument import IRCap

cap = IRCap(
    termination_date='1y',
    notional_currency='USD',
)
```

## FX Option

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

## FX Forward

```python
from gs_quant.instrument import FXForward

fwd = FXForward(
    pair='USDJPY',
    settlement_date='6m',
    notional_amount=10e6,
)
```

## Important: FX Instrument Pitfalls

### 1. Always Set `premium=0` on FX Options

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

### 2. FXMultiCrossBinaryLeg Uses Different OptionType Values

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

## Equity Option

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

## Naming Instruments

Set the instrument `name` property for easy identification in portfolios and results:

```python
swap.name = 'USD 10y Payer'
```

See `gs-quant-overview` for resolving instruments and building portfolios. See `gs-quant-pricing` for pricing.
