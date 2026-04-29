---
name: gs-quant-backtesting
description: "Guide to the gs_quant backtesting framework: Strategy, triggers (PeriodicTrigger, StrategyRiskTrigger, MktTrigger, DateTrigger, AggregateTrigger, NotTrigger), actions (AddTradeAction, HedgeAction, AddScaledTradeAction, ExitTradeAction), GenericEngine, EquityVolEngine, transaction costs, and result extraction (result_summary, trade_ledger, summary_stats)."
---

# gs_quant Backtesting Guide

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
    PeriodicTrigger, PeriodicTriggerRequirements,
    StrategyRiskTrigger, RiskTriggerRequirements,
    MktTrigger, MktTriggerRequirements,
    AggregateTrigger, AggregateTriggerRequirements,
    DateTrigger, DateTriggerRequirements,
    MeanReversionTrigger, MeanReversionTriggerRequirements,
    PortfolioTrigger, PortfolioTriggerRequirements,
    NotTrigger, NotTriggerRequirements,
    TriggerDirection, AggType,
)
from gs_quant.backtests.actions import (
    AddTradeAction, AddScaledTradeAction, HedgeAction,
    ExitTradeAction, ExitAllPositionsAction,
    EnterPositionQuantityScaledAction, RebalanceAction,
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

Use `GenericEngine` unless you specifically need `EquityVolEngine` performance for equity options.

---

## 3. Strategy Construction

```python
strategy = Strategy(None, trigger)                    # empty starting portfolio
strategy = Strategy(initial_instrument, trigger)      # start with an instrument
strategy = Strategy(None, [trigger_add, trigger_hedge])  # multiple triggers
```

---

## 4. Triggers

### 4.1 PeriodicTrigger — Trade on a Schedule

```python
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements

trig_req = PeriodicTriggerRequirements(
    start_date=start_date, end_date=end_date,
    frequency='1m',         # '1b' (daily), '1w', '1m', '3m', '1y'
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
    risk=hedge_risk, trigger_level=50_000, direction=TriggerDirection.ABOVE,
)
trigger = StrategyRiskTrigger(trig_req, hedge_action)
```

### 4.3 MktTrigger — Trigger on Market Data

```python
from gs_quant.backtests.triggers import MktTrigger, MktTriggerRequirements
from gs_quant.backtests.data_sources import GenericDataSource, MissingDataStrategy

data_source = GenericDataSource(pandas_series, MissingDataStrategy.fill_forward)
trig_req = MktTriggerRequirements(
    data_source=data_source, trigger_level=100.0, direction=TriggerDirection.BELOW,
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
    aggregate_type=AggType.ALL_OF,   # ALL_OF (AND) or ANY_OF (OR)
)
trigger = AggregateTrigger(agg_req, action)
```

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
    trade_duration='1m',    # tenor, date, 'expiration_date', 'next schedule', or None (forever)
    name='my_trade',
)
```

**`trade_duration` options:** `None` (hold forever), tenor string (`'1m'`, `'3m'`), `'expiration_date'` (hold until expiry), `'next schedule'` (auto-rolling), explicit `datetime.date`, or `datetime.timedelta`.

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
    priceables=instrument, trade_duration='1m',
    scaling_type=ScalingActionType.size, scaling_level=1_000_000,
)
```

### 5.4 EnterPositionQuantityScaledAction — Quantity-Based Entry

```python
from gs_quant.backtests.actions import EnterPositionQuantityScaledAction
from gs_quant.target.backtests import BacktestTradingQuantityType

action = EnterPositionQuantityScaledAction(
    priceables=eq_option, trade_duration='1m',
    trade_quantity=1000, trade_quantity_type=BacktestTradingQuantityType.quantity,
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
| `result_ccy` | Currency for results | None |
| `market_data_location` | `'LDN'`, `'NYC'`, `'HKG'` | None |
| `is_batch` | Use websocket batching | True |

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
    strategy, start=start_date, end=end_date, frequency='1b',
    risks=[Price, FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')],
)
delta_series = backtest.result_summary[FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')]
```

---

## 8. Transaction Costs

Actions accept `transaction_cost` and `transaction_cost_exit` parameters.

### ConstantTransactionModel — Fixed Cost

```python
from gs_quant.backtests.backtest_objects import ConstantTransactionModel

action = AddTradeAction(instrument, trade_duration='1m',
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
action = AddTradeAction(instrument, trade_duration='1m',
    transaction_cost=ScaledTransactionModel(scaling_type='notional_amount', scaling_level=0.0001),
)

# By risk measure: cost = |Price| x 0.01 (1% of premium)
action = AddTradeAction(instrument, trade_duration='1m',
    transaction_cost=ScaledTransactionModel(scaling_type=Price, scaling_level=0.01),
)
```

### AggregateTransactionModel — Combine Models

```python
from gs_quant.backtests.backtest_objects import AggregateTransactionModel, ConstantTransactionModel, ScaledTransactionModel

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

- **Always set `premium=0` on FX options** — see `gs-quant-instruments` for details
- **Match trade_duration to trigger frequency** for roll strategies (e.g. `'1m'` + `'1m'`)
- **Use `'expiration_date'`** to hold options until expiry
- **Order triggers correctly** — entry before hedge: `Strategy(None, [entry_trigger, hedge_trigger])`
- **Order actions within a trigger** — exit before add: `PeriodicTrigger(trig_req, [exit_action, add_action])`
- **Name your instruments** — names appear in trade_ledger and aid debugging
- **`frequency='1b'`** for daily P&L; trigger frequency and evaluation frequency are independent

---

## 10. EquityVolEngine

Server-side execution for equity option and variance swap backtests:

```python
from gs_quant.instrument import EqOption, OptionType, OptionStyle
from gs_quant.backtests.equity_vol_engine import EquityVolEngine

option = EqOption('.STOXX50E', expiration_date='3m', strike_price='ATM',
    option_type=OptionType.Call, option_style=OptionStyle.European)

action = EnterPositionQuantityScaledAction(
    priceables=option, trade_duration='1m',
    trade_quantity=1000, trade_quantity_type=BacktestTradingQuantityType.quantity,
)
trig_req = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m')
trigger = PeriodicTrigger(trig_req, action)

engine = EquityVolEngine()
backtest = engine.run_backtest(Strategy(None, trigger), start=start_date, end=end_date)
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
