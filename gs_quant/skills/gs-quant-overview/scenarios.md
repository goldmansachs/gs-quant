# Scenarios

A scenario changes market data for the calculations run inside it. It maps patterns, which select
market data points, to shocks, which move them:

```python
from gs_quant.risk import MarketDataPattern, MarketDataShock, MarketDataShockType, MarketDataShockBasedScenario

scenario = MarketDataShockBasedScenario(
    shocks={
        MarketDataPattern(mkt_type, mkt_asset, mkt_class, mkt_point, mkt_quoting_style): MarketDataShock(
            MarketDataShockType.Absolute,  # or Proportional, Override
            value,
        ),
    }
)
with PricingContext(pricing_date=d, market_data_location=loc):  # the context you already price in
    base_f = inst.price()
    with scenario:
        shocked_f = inst.price()
```

Outside any pricing context, each calculation under the scenario is sent on its own.

**Choosing the pattern fields.** Set only the fields you need; unset fields match everything. To
get the values, call `inst.market()`: it lists the market data points the instrument uses, each
named `<mkt_type>_<mkt_asset>_<mkt_class>_<mkt_point>.<mkt_quoting_style>`. Copy the field values
from those names rather than guessing, because they can differ from market convention. For
example, EURUSD's points are under `USD/EUR`, and the spot point there holds the EURUSD rate, so a
shock to it moves EURUSD; `'EUR/USD'` matches nothing. Pass `mkt_point` as a tuple, such as
`('10Y',)`: a plain string like `'10Y'` is split into characters and does not select the 10Y point.

**A pattern that selects nothing changes nothing, without an error**: a misspelt field, a pair
written the other way round from its market data name, or several assets in one string. Use one
pattern per asset, and check that the shocked price moved.

**Absolute shocks and overrides are decimals in the point's own units**: for example, `0.0001` is
1bp on a rate and `0.01` is 1 vol point on an FX vol. **A proportional shock is a fraction of the
current level**: `0.06` raises it by 6%.

**If overriding a single point makes the model fail to calibrate**, override the whole curve
instead by leaving `mkt_point` unset. For example, single-tenor overrides of an FX vol can fail with
`Wing vols are substantially different to ATM vol`.

**FX options on several pairs take the correlation between two pairs from the vol of their cross**
(for example, the cross of EUR/SEK and EUR/MXN is MXN/SEK); their market data has no correlation
points. To test a different correlation, override the cross's ATM vol curve.

**Equities: vols are a scale (1.0) plus spreads (0.0).** An absolute shock on `mkt_class='Scale'`,
`mkt_quoting_style='Value'` scales the vols: `0.1` raises them by 10%. A proportional shock on
`ATM VOL` multiplies a spread of 0 and changes nothing.

**For shocked P&L over time**, use a `HistoricalPricingContext` in place of the `PricingContext`
above and subtract the two series.

## Examples

```python
# +1bp on the EUR 10y swap rate only
eur_10y = {
    MarketDataPattern('IR', 'EUR', mkt_class='SWAP', mkt_point=('10Y',)): MarketDataShock(
        MarketDataShockType.Absolute, 0.0001
    )
}
# SPX vols up 10%
spx_vols = {
    MarketDataPattern('EQ VOL', '.SPX', 'Scale', mkt_quoting_style='Value'): MarketDataShock(
        MarketDataShockType.Absolute, 0.1
    )
}
# MXN/SEK ATM vol curve set to 10.4%, which changes the EUR/SEK–EUR/MXN correlation
mxnsek_vol = {MarketDataPattern('FX VOL', 'MXN/SEK', 'ATM VOL'): MarketDataShock(MarketDataShockType.Override, 0.104)}
```
