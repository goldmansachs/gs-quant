# Risk measures

This page says what each risk measure's number means.

## Parameters

**`currency=`** converts the result into that currency, e.g. `EqDelta(currency='EUR')`;
`currency='local'` gives the instrument's own currency. Without it, some measures report USD rather
than the instrument's currency, e.g. `IRVegaParallel`.

**`aggregation_level=`** sets how finely a bucketed measure is broken down:

| Level | Result |
|---|---|
| `'Point'` (default) | a table with one row per market data point, e.g. each curve tenor |
| `'Class'` | a table with one row per instrument class, e.g. the cash, FRA and swap points of a rate curve |
| `'Asset'` | a table with one row per asset, e.g. per currency |
| `'Type'` | one number |

**`.unit`** on a result names its unit when it is set, e.g. the currency of a price. Many results
have no unit set; that does not mean they are unitless.

## Scales

**Rates, vols and fractions come back as decimals**: `IRFwdRate`, `IRSpotRate`,
`IRAnnualImpliedVol`, `FXAnnualImpliedVol`, `EqAnnualImpliedVol`, `FXQuotedDelta`, `FXCalcDelta`
and `FairPremiumInPercent`. For example, `0.0466` is 4.66%.

**Prices, premiums and sensitivities scale with the trade's size** (notional, or number of
options); fractions, rates, vols and spot levels don't.

## Equities

**`EqDelta` is the USD present value change for a 100% move in spot**: divide by 100 for a 1% move.
It is a bump-and-reprice of spot by ±1% in which vols move with spot under GS's market model, so it
can differ from a Black-Scholes delta. It is in USD even for a non-USD underlying, whose `.price()`
is in its own currency, so convert one of the two before comparing them.

With **`EqGamma`**, a spot move of `x` (a fraction, so `0.01` is 1%) changes the present value by
about `EqDelta * x + 50 * EqGamma * x**2`.

**`EqVega` is the USD present value change for a 1 vol point rise** in implied vol (`0.01`).

## FX

**`FXDelta` is the USD present value change for a move of 1 in spot**, one row per USD cross:
`PnL = dSpot * FXDelta`. **`FXCalcDelta`** is the delta as a fraction of notional, and
**`FXQuotedDelta`** the Black-Scholes delta as a fraction (the delta a strike such as `'25d'` is
solved against). **`FXDeltaHedge`** gives the notionals of USD-cross forwards that hedge the delta.

**`FXGamma` is the change in wing delta, in the underlying currency and scaled by notional, for a
100% move in spot.** A pair's rate is the number of units of the overlying currency per unit of the
underlying currency, so in USDJPY the underlying is USD and the overlying is JPY. A spot move of X%
changes the delta by about `FXGamma * X / 100`, and a move of 1 in spot by about `FXGamma / FXSpot`.

**`FXVega` is the USD present value change for a 1 vol point rise** in ATM vols (`0.01`).

**`FairPremium`** is the premium that makes the present value zero, paid on the premium payment
date, so it differs from the discounted price. **`FairPremiumInPercent`** is `FairPremium` divided
by notional times the forward (`FXFwd`).

**`FXSpot` reflects a spot shock only if the shock's pattern leaves `mkt_class` unset**; the price
moves either way.

**There is no Volga or Vanna measure**: calculate `FXVega` and `FXDelta` under a vol scenario and
take the difference from the unshocked values.

## Rates

**`IRDelta` is the present value change for a 1bp move in the instruments the curve is built
from**. **`IRGammaParallelLocalCcy`** is the change in that delta, in local currency, for a 1bp
move, so its unit is local currency per bp².

**`IRVega` is the present value change for a 1bp rise in normal vol**; **`IRVegaParallel`** is the
same in USD unless `currency=` is set, so on a non-USD trade it differs from
`IRVega(currency='local')` by the exchange rate.

**`IRAnnualImpliedVol` is a normal vol** as a decimal (`0.0087` is 87bp). **`IRFwdRate`** is the
forward par rate and **`IRSpotRate`** the spot par rate, both decimals.
