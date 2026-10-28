# gs_quant Backtesting Guide

## Do you need a backtest engine?

**If the strategy is one instrument or a fixed portfolio held over a date range, with no triggers,
rebalancing or hedging, don't use an engine: price it with a `HistoricalPricingContext`.** The
engines add trade management (triggers, actions, hedges) on top of pricing on each date; with
nothing to manage, price directly. For example, to track a trade entered on a given date, resolve
it on that date, then price it over the range in one `HistoricalPricingContext` (see "Relative
terms and resolve()" in `pricing.md`).

---

## 1. Architecture Overview

| Concept | Description |
|---|---|
| **Strategy** | Combines an optional initial portfolio with one or more `Trigger` objects. |
| **Trigger** | Defines *when* to act — on a schedule, risk threshold, market data level, etc. Each trigger holds one or more `Action` objects. |
| **Action** | Defines *what* to do when the trigger fires — add a trade, hedge, exit, rebalance. |

A backtest **Engine** runs the strategy over a date range, resolving instruments, computing risks, and building the P&L time series.

### Import Map

```python
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import (
    PeriodicTrigger,
    PeriodicTriggerRequirements,
    StrategyRiskTrigger,
    RiskTriggerRequirements,
    MktTrigger,
    MktTriggerRequirements,
    AggregateTrigger,
    AggregateTriggerRequirements,
    DateTrigger,
    DateTriggerRequirements,
    MeanReversionTrigger,
    MeanReversionTriggerRequirements,
    PortfolioTrigger,
    PortfolioTriggerRequirements,
    NotTrigger,
    NotTriggerRequirements,
    TriggerDirection,
    AggType,
)
from gs_quant.backtests.actions import (
    AddTradeAction,
    AddScaledTradeAction,
    HedgeAction,
    ExitTradeAction,
    ExitAllPositionsAction,
    EnterPositionQuantityScaledAction,
    RebalanceAction,
)
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.equity_vol_engine import EquityVolEngine
from gs_quant.backtests.data_sources import GenericDataSource, GsDataSource, MissingDataStrategy
```

---

## 2. Engines

| Engine | Best For | Instruments |
|---|---|---|
| **GenericEngine** | Multi-asset OTC strategies | IRSwap, IRSwaption, FXOption, FXForward, FXBinary, EqOption, etc. |
| **EquityVolEngine** | Equity vol strategies (server-side) | EqOption, EqVarianceSwap |
| **PredefinedAssetEngine** | Custom order-based backtests | Predefined assets |

**`EquityVolEngine` is faster, but runs only on the equity underliers and dates for which the
service holds market data, and accepts only a restricted strategy shape. `GenericEngine` prices
anything gs_quant can price.** Use `GenericEngine` unless you need `EquityVolEngine`'s speed for
equity options or variance swaps.

---

## 3. Strategy Construction

```python
strategy = Strategy(None, trigger)  # empty starting portfolio
strategy = Strategy(initial_instrument, trigger)  # start with an instrument
strategy = Strategy(None, [trigger_add, trigger_hedge])  # multiple triggers
```

---

## 4. Triggers

### 4.1 PeriodicTrigger — Trade on a Schedule

```python
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements

trig_req = PeriodicTriggerRequirements(
    start_date=start_date,
    end_date=end_date,
    frequency='1m',  # '1b' (daily), '1w', '1m', '3m', '1y'
)
trigger = PeriodicTrigger(trig_req, action)
```

### 4.2 StrategyRiskTrigger — Trigger on Risk Breach

```python
from gs_quant.backtests.triggers import StrategyRiskTrigger, RiskTriggerRequirements, TriggerDirection
from gs_quant.risk import FXDelta
from gs_quant.common import AggregationLevel

hedge_risk = FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')
trig_req = RiskTriggerRequirements(
    risk=hedge_risk,
    trigger_level=50_000,
    direction=TriggerDirection.ABOVE,
)
trigger = StrategyRiskTrigger(trig_req, hedge_action)
```

### 4.3 MktTrigger — Trigger on Market Data

```python
from gs_quant.backtests.triggers import MktTrigger, MktTriggerRequirements
from gs_quant.backtests.data_sources import GenericDataSource, MissingDataStrategy

data_source = GenericDataSource(pandas_series, MissingDataStrategy.fill_forward)
trig_req = MktTriggerRequirements(
    data_source=data_source,
    trigger_level=100.0,
    direction=TriggerDirection.BELOW,
)
trigger = MktTrigger(trig_req, action)
```

### 4.4 DateTrigger — Trigger on Specific Dates

```python
from gs_quant.backtests.triggers import DateTrigger, DateTriggerRequirements

trig_req = DateTriggerRequirements(
    dates=[date(2024, 3, 15), date(2024, 6, 15), date(2024, 9, 15)],
)
trigger = DateTrigger(trig_req, action)
```

### 4.5 AggregateTrigger — Combine with AND/OR

```python
from gs_quant.backtests.triggers import AggregateTrigger, AggregateTriggerRequirements, AggType

agg_req = AggregateTriggerRequirements(
    triggers=[periodic_trigger, risk_trigger],
    aggregate_type=AggType.ALL_OF,  # ALL_OF (AND) or ANY_OF (OR)
)
trigger = AggregateTrigger(agg_req, action)
```

**To trigger when a risk is outside ±X**, put a requirement for each side in an `AggregateTrigger`
with `ANY_OF`, and pass the measure in `run_backtest(risks=[...])`:

```python
from gs_quant.backtests.triggers import RiskTriggerRequirements, TriggerDirection

delta = FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')
agg_req = AggregateTriggerRequirements(
    triggers=[
        RiskTriggerRequirements(risk=delta, trigger_level=50_000, direction=TriggerDirection.ABOVE),
        RiskTriggerRequirements(risk=delta, trigger_level=-50_000, direction=TriggerDirection.BELOW),
    ],
    aggregate_type=AggType.ANY_OF,
)
trigger = AggregateTrigger(agg_req, action)
backtest = GE.run_backtest(Strategy(None, trigger), start=start_date, end=end_date, risks=[delta])
```

**On each date `GenericEngine` calculates only the price, the measures in `risks=` and
`pnl_explain`, and the measures of top-level `StrategyRiskTrigger`s and of `HedgeAction`s.** A risk
condition inside an `AggregateTrigger` or `NotTrigger` isn't among them: without `risks=[delta]`,
the run raises `ValueError: <measure> not computed`.

### 4.6 NotTrigger — Invert a Trigger

```python
from gs_quant.backtests.triggers import NotTrigger, NotTriggerRequirements

not_req = NotTriggerRequirements(trigger=some_trigger_requirements)
trigger = NotTrigger(not_req, action)
```

---

## 5. Actions

### 5.1 AddTradeAction — Add a Trade

```python
action = AddTradeAction(
    priceables=instrument,
    trade_duration='1m',
    name='my_trade',
)
```

**In `GenericEngine`, `trade_duration` sets when each added trade is closed:**

- `None`: no closing date; the trade stays in the portfolio until the backtest ends or an exit
  action removes it, even after it expires
- a tenor such as `'1m'`: that long after the trade date
- a `datetime.date`: on that date
- the name of a date field on the instrument: on that field's date as resolved on the trade date,
  for example `'expiration_date'` on an `FXOption`, `EqOption` or `IRSwaption`, or
  `'termination_date'` on an `IRSwap`
- `'next schedule'`: on the trigger's next date, for a trigger that has one, as a `PeriodicTrigger`
  or `DateTrigger` does

**In `GenericEngine`, each added trade is resolved on the date it is added, and the resolved trade
is then held unchanged for its whole life**, so a field that resolution fills in keeps the value it
had on that date. To keep a field unresolved, or to change how trades are built, subclass the
action's handler and map the action to it when you create the engine. For example, to leave an
inflation swap's `base_cpi` unset after the trade is added:

```python
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.generic_engine_action_impls import AddTradeActionImpl
from gs_quant.markets.portfolio import Portfolio


class FloatingBaseCpiAddTrade(AddTradeActionImpl):
    def _raise_order(self, state, trigger_info=None):
        orders = super()._raise_order(state, trigger_info)
        return {
            d: (Portfolio([i.clone(base_cpi=None) for i in p.all_instruments]), ti) for d, (p, ti) in orders.items()
        }


engine = GenericEngine(action_impl_map={AddTradeAction: FloatingBaseCpiAddTrade})
```

### 5.2 HedgeAction — Delta Hedge

```python
from gs_quant.backtests.actions import HedgeAction
from gs_quant.risk import FXDelta

hedge_risk = FXDelta(aggregation_level='Type', currency='USD')
action = HedgeAction(
    risk=hedge_risk,
    priceables=FXForward(pair='EURUSD', settlement_date='1y', name='hedge_fwd'),
    trade_duration='1m',
)
```

### 5.3 AddScaledTradeAction — Scale a Trade

```python
from gs_quant.backtests.actions import AddScaledTradeAction, ScalingActionType

action = AddScaledTradeAction(
    priceables=instrument,
    trade_duration='1m',
    scaling_type=ScalingActionType.size,
    scaling_level=1_000_000,
)
```

**In `GenericEngine`, `scaling_type` sets the size of each added trade:**

| `scaling_type` | Each trade is multiplied by |
|---|---|
| `ScalingActionType.size` | `scaling_level` |
| `ScalingActionType.risk_measure` | `scaling_level` divided by `scaling_risk` of the action's priceables (summed) on the trade date, so the trade starts with that risk equal to `scaling_level` |
| `ScalingActionType.NAV` | whatever makes the trade cost the cash available, net of transaction costs: `scaling_level` for the action's first trade, then the proceeds of the trades it closed since its previous one |

For example, to spend a fixed premium on each trade, use `risk_measure` with `scaling_risk=Price`.
On FX options this needs `premium=0`, or the premium is solved so that `Price` is zero (see "Always
Set `premium=0` on FX Options" in `instruments.md`).

### 5.4 EnterPositionQuantityScaledAction — Quantity-Based Entry

```python
from gs_quant.backtests.actions import EnterPositionQuantityScaledAction
from gs_quant.target.backtests import BacktestTradingQuantityType

action = EnterPositionQuantityScaledAction(
    priceables=eq_option,
    trade_duration='1m',
    trade_quantity=1000,
    trade_quantity_type=BacktestTradingQuantityType.quantity,
)
```

### 5.5 ExitTradeAction / ExitAllPositionsAction

```python
exit_named = ExitTradeAction(priceable_names='my_trade')
exit_all = ExitAllPositionsAction()
```

### 5.6 Multiple Actions on a Single Trigger

Order matters — they execute in sequence:

```python
trigger = StrategyRiskTrigger(trig_req, [exit_action, add_action])
```

---

## 6. GenericEngine Parameters

| Parameter | Description | Default |
|---|---|---|
| `strategy` | The Strategy object | *required* |
| `start` / `end` | Backtest date range | None |
| `frequency` | Evaluation frequency: `'1b'`, `'1w'`, `'1m'` | `'1m'` |
| `states` | Explicit date list (overrides start/end/frequency) | None |
| `risks` | Additional risk measures to compute | None |
| `show_progress` | Show progress bar | True |
| `initial_value` | Starting cash value | 0 |
| `result_ccy` | Currency to report every risk, price and cash amount in; see below | None |
| `holiday_calendar` | Dates left out of the schedule built from `start`, `end` and `frequency` | None |
| `market_data_location` | `'LDN'`, `'NYC'`, `'HKG'`, `'TKO'` | None |
| `is_batch` | Use websocket batching | True |

**`result_ccy` adds `currency=` to every measure in the run**: the price, those in `risks`, those
of triggers and actions, and those in `pnl_explain`. A measure that has no currency, for example
`FXSpot`, `FXAnnualImpliedVol` or `IRFwdRate`, makes the run raise `Unparameterised risk`, so
`result_ccy` can't be used with `fx_pnl_definition()`. In that case leave `result_ccy` unset and
pass the currency only to the measures that take one: `GenericEngine(price_measure=Price(currency='EUR'))`
for the price and cash, and for example `FXDelta(aggregation_level='Type', currency='EUR')` in `risks`.

**To skip dates, for example ones whose market data fails, give the list of dates in three
places**: `GenericEngine.run_backtest(holiday_calendar=...)` leaves them out of the schedule built
from `start`, `end` and `frequency`, `PeriodicTriggerRequirements(calendar=...)` stops trades
opening on them, and `holiday_calendar=` on each action stops a `trade_duration` given as a tenor
from ending on them.

---

## 7. Extracting Results

### result_summary — Main P&L DataFrame

```python
summary = backtest.result_summary
```

Columns: `Price` (MTM of live instruments), `Cumulative Cash` (from unwound trades), `Transaction Costs`, `Total` (Price + Cash + Costs), plus any additional risk columns.

```python
backtest.result_summary['Total'].plot(title='Strategy Performance')
```

### trade_ledger — Trade History

```python
ledger = backtest.trade_ledger()
```

### summary_stats — Performance Statistics

```python
stats = backtest.summary_stats()
```

Returns: Start/End Date, Duration, Total PnL, Total Transaction Costs, Total Trades, Peak PnL, Annualised Return/Volatility, Sharpe Ratio, Sortino Ratio, Max Drawdown, Max Drawdown Duration, Calmar Ratio, Current Drawdown, Average/Std Daily PnL, Best/Worst Day, % Positive Days, Skewness, Kurtosis.

```python
# Compare two backtests
import pandas as pd

pd.DataFrame({'A': backtest_a.summary_stats(), 'B': backtest_b.summary_stats()})
```

### Additional Risks

```python
from gs_quant.risk import Price, FXDelta
from gs_quant.common import AggregationLevel

backtest = GE.run_backtest(
    strategy,
    start=start_date,
    end=end_date,
    frequency='1b',
    risks=[Price, FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')],
)
delta_series = backtest.result_summary[FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')]
```

### P&L Explain

**`GenericEngine.run_backtest(pnl_explain=...)` splits the P&L into named parts, each a
sensitivity times the daily move in a market quantity.** A `PnlDefinition` is a list of parts, each
`PnlAttribute(attribute_name, attribute_metric, market_data_metric, scaling_factor)`, with
`second_order=True` added for a second-order part. Each day, for every instrument held the day before, a part adds
`scaling_factor * sensitivity * move`, or `0.5 * scaling_factor * sensitivity * move**2` when
`second_order=True`, where `sensitivity` is `attribute_metric` on the day before and `move` is the
change in `market_data_metric` since then. For FX options, `fx_pnl_definition()` gives delta, gamma
and vega parts:

```python
from gs_quant.backtests.backtest_objects import fx_pnl_definition

backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', pnl_explain=fx_pnl_definition())
explain = backtest.pnl_explain()  # {'PNL_delta': {date: cumulative P&L}, 'PNL_gamma': ..., 'VegaPnL': ...}
```

`fx_pnl_definition()`'s parts don't add up to the change in `Total`: they leave out, for example,
time decay.

---

## 8. Transaction Costs

Actions accept `transaction_cost` and `transaction_cost_exit` parameters.

### ConstantTransactionModel — Fixed Cost

```python
from gs_quant.backtests.backtest_objects import ConstantTransactionModel

action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ConstantTransactionModel(500),
    transaction_cost_exit=ConstantTransactionModel(250),
)
```

### ScaledTransactionModel — Proportional Cost

Scale by instrument attribute or risk measure:

```python
from gs_quant.backtests.backtest_objects import ScaledTransactionModel
from gs_quant.risk import Price

# By notional: cost = notional_amount x 0.0001 (1bp)
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ScaledTransactionModel(scaling_type='notional_amount', scaling_level=0.0001),
)

# By risk measure: cost = |Price| x 0.01 (1% of premium)
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ScaledTransactionModel(scaling_type=Price, scaling_level=0.01),
)
```

### AggregateTransactionModel — Combine Models

```python
from gs_quant.backtests.backtest_objects import (
    AggregateTransactionModel,
    ConstantTransactionModel,
    ScaledTransactionModel,
)

# Total cost = fixed $100 + 0.5bp of notional
combined = AggregateTransactionModel(
    transaction_models=(
        ConstantTransactionModel(100),
        ScaledTransactionModel('notional_amount', 0.00005),
    ),
    # aggregate_type defaults to TransactionAggType.SUM; also supports MAX, MIN
)
action = AddTradeAction(instrument, trade_duration='1m', transaction_cost=combined)
```

Transaction costs appear in `backtest.result_summary` as the `'Transaction Costs'` column (cumulative) and are included in `'Total'`.

---

## 9. Best Practices

- **Always set `premium=0` on FX options** — see `instruments.md` for details
- **Match trade_duration to trigger frequency** for roll strategies (e.g. `'1m'` + `'1m'`)
- **Use `'expiration_date'`** to hold options until expiry
- **Order triggers correctly** — entry before hedge: `Strategy(None, [entry_trigger, hedge_trigger])`
- **Order actions within a trigger** — exit before add: `PeriodicTrigger(trig_req, [exit_action, add_action])`
- **Name your instruments** — names appear in trade_ledger and aid debugging
- **`frequency='1b'`** for daily P&L; trigger frequency and evaluation frequency are independent
- **Before a long run, time a short one when a trigger depends on the strategy's own risk**, for example a `StrategyRiskTrigger`: the engine then has to price each date before it can decide what to do on the next, so it sends requests one date at a time and a run over several years can take hours

---

## 10. EquityVolEngine

Server-side execution for equity option and variance swap backtests:

```python
from gs_quant.instrument import EqOption, OptionType, OptionStyle
from gs_quant.backtests.equity_vol_engine import EquityVolEngine

option = EqOption(
    '.STOXX50E',
    expiration_date='3m',
    strike_price='ATM',
    option_type=OptionType.Call,
    option_style=OptionStyle.European,
)

action = EnterPositionQuantityScaledAction(
    priceables=option,
    trade_duration='1m',
    trade_quantity=1000,
    trade_quantity_type=BacktestTradingQuantityType.quantity,
)
trig_req = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m')
trigger = PeriodicTrigger(trig_req, action)

engine = EquityVolEngine()
backtest = engine.run_backtest(Strategy(None, trigger), start=start_date, end=end_date)
```

**`EquityVolEngine` accepts only one shape of strategy**; `run_backtest` raises `RuntimeError`
listing every rule the strategy breaks, and `EquityVolEngine.check_strategy(strategy)` returns that
list without running. The main rules:

- one underlier: every trade on the same asset
- no initial portfolio, at most 3 triggers, each a `PeriodicTrigger` or an `AggregateTrigger` of one
  `DateTrigger` and one `PortfolioTrigger` (`data_source='len'`, `trigger_level=0`)
- one action per trigger, no two actions of the same type, each one of `AddTradeAction`,
  `AddScaledTradeAction`, `EnterPositionQuantityScaledAction`, `HedgeAction` or `ExitTradeAction`
- trades are `EqOption` or `EqVarianceSwap` whose `quantity`, `number_of_options` and `multiplier`
  multiply to 1 (unset counts as 1); set the size on the action instead
- a `PeriodicTrigger`'s `frequency` equals its action's `trade_duration`, so trades roll at a fixed
  interval
- the only hedge is a delta hedge (`risk=EqDelta`) with a synthetic forward: a long call and a short
  put with the same underlier, strike and expiry

The service applies further checks, for example a maximum expiry. For anything else, use
`GenericEngine`.

**`EquityVolEngine` returns a P&L breakdown by date, each part cumulative from the start**:
`backtest.get_measure_series(FlowVolBacktestMeasure.PNL_delta)` (import `FlowVolBacktestMeasure`
from `gs_quant.target.backtests`), and likewise `PNL_gamma`, `PNL_vega`, `PNL_theta`,
`PNL_transactions` and the total `PNL`. `PNL_spot` is delta plus gamma plus the higher-order spot
part, `PNL_vol` is vega plus the higher-order vol part, and `PNL_carry` is `PNL_spot` plus
`PNL_theta`. `PNL` minus `PNL_spot`, `PNL_vol` and `PNL_theta` is the unexplained part.

**To see the strike that a relative strike such as `'ATM'` gives on each date of a range**, request
`Strike_Level` from the backtest API. The strike is set again on each date, and the result is
`{'Strike Level': [['YYYY-MM-DD', strike], ...]}`:

```python
from gs_quant.api.gs.backtests import GsBacktestApi
from gs_quant.target.backtests import BacktestRiskMeasureType, BacktestRiskPosition, BacktestRiskRequest

request = BacktestRiskRequest(
    positions=(BacktestRiskPosition(instrument=option, quantity=1),),
    measures=(BacktestRiskMeasureType.Strike_Level,),
    start_date=start_date,
    end_date=end_date,
)
strikes = GsBacktestApi.calculate_position_risk(request)['Strike Level']
```

---

## 11. Quick Reference Template

```python
from datetime import date
from gs_quant.session import GsSession
from gs_quant.instrument import IRSwaption
from gs_quant.common import Currency
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.strategy import Strategy
from gs_quant.risk import Price

GsSession.use()

start_date = date(2023, 1, 3)
end_date = date(2024, 12, 31)

# 1. Define the instrument
instrument = IRSwaption('Pay', '10y', Currency.USD, expiration_date='6m', name='6m10y')

# 2. Define trigger + action
trig_req = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='6m')
action = AddTradeAction(instrument, trade_duration='6m')
trigger = PeriodicTrigger(trig_req, action)

# 3. Build strategy
strategy = Strategy(None, trigger)

# 4. Run
GE = GenericEngine()
backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)

# 5. View results
backtest.result_summary['Total'].plot(title='Performance')
backtest.trade_ledger()
backtest.summary_stats()
```
