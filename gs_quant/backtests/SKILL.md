---
name: gs-quant-backtesting
description: Guide to the gs_quant backtesting framework — engines, triggers, actions, strategies, and result extraction. Covers GenericEngine (multi-asset OTC), EquityVolEngine, and PredefinedAssetEngine.
---

# SKILL.md — gs_quant Backtesting Guide

This document covers the backtesting framework in `gs_quant.backtests`. It explains how to construct strategies from triggers and actions, choose the right engine, run backtests, and extract results.

---

## 1. Architecture Overview

A backtest in gs_quant is built from three core concepts:

| Concept | Description |
|---|---|
| **Strategy** | Combines an optional initial portfolio with one or more `Trigger` objects. |
| **Trigger** | Defines *when* to act — on a schedule, when a risk threshold is breached, when market data crosses a level, etc. Each trigger holds one or more `Action` objects. |
| **Action** | Defines *what* to do when the trigger fires — add a trade, hedge a risk, exit a position, rebalance, etc. |

A backtest **Engine** runs the strategy over a date range, resolving instruments, computing risks, and building the P&L time series.

### Import Map

```python
# Strategy
from gs_quant.backtests.strategy import Strategy

# Triggers
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

# Actions
from gs_quant.backtests.actions import (
    AddTradeAction,
    AddScaledTradeAction,
    HedgeAction,
    ExitTradeAction,
    ExitAllPositionsAction,
    EnterPositionQuantityScaledAction,
    RebalanceAction,
)

# Engines
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.equity_vol_engine import EquityVolEngine

# Data sources (for market triggers)
from gs_quant.backtests.data_sources import GenericDataSource, GsDataSource, MissingDataStrategy
```

---

## 2. Engines

gs_quant ships three backtest engines. Choose the one that matches your instrument type and use case:

| Engine | Best For | Instruments | Notes |
|---|---|---|---|
| **GenericEngine** | Multi-asset OTC strategies | IRSwap, IRSwaption, FXOption, FXForward, FXBinary, EqOption, etc. | Most flexible. Prices via the GS analytics API. Supports all trigger and action types. |
| **EquityVolEngine** | Equity vol strategies | EqOption, EqVarianceSwap | Server-side execution — faster for simple equity vol roll strategies. Supports delta hedging and signals. |
| **PredefinedAssetEngine** | Strategies on predefined assets with intraday logic | Custom order-based | For advanced users building execution-style backtests. |

**Best practice:** Use `GenericEngine` unless you specifically need `EquityVolEngine` performance for equity options.

---

## 3. Strategy Construction

A `Strategy` takes an optional initial portfolio and one or more triggers:

```python
from gs_quant.backtests.strategy import Strategy

# Empty starting portfolio, one trigger
strategy = Strategy(None, trigger)

# Start with an instrument already in the portfolio
strategy = Strategy(initial_instrument, trigger)

# Multiple triggers
strategy = Strategy(None, [trigger_add_trade, trigger_hedge])
```

---

## 4. Triggers

Triggers define *when* actions fire. Each trigger pairs a `TriggerRequirements` (the condition) with one or more `Action` objects (what to do).

### 4.1 PeriodicTrigger — Trade on a Schedule

The most common trigger. Fires on a regular frequency (e.g. monthly, weekly).

```python
from datetime import date
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.backtests.actions import AddTradeAction

start_date = date(2023, 1, 3)
end_date = date(2024, 12, 31)

trig_req = PeriodicTriggerRequirements(
    start_date=start_date,
    end_date=end_date,
    frequency='1m',         # '1b' (daily), '1w', '1m', '3m', '1y', etc.
)

action = AddTradeAction(instrument, trade_duration='1m')
trigger = PeriodicTrigger(trig_req, action)
```

**Key parameters for `PeriodicTriggerRequirements`:**
- `start_date` / `end_date` — date range for the schedule
- `frequency` — tenor string: `'1b'` (daily), `'1w'`, `'1m'`, `'3m'`, `'6m'`, `'1y'`
- `calendar` — optional holiday calendar (iterable of dates)

### 4.2 StrategyRiskTrigger — Trigger on Risk Breach

Fires when a portfolio risk measure breaches a threshold.

```python
from gs_quant.backtests.triggers import StrategyRiskTrigger, RiskTriggerRequirements, TriggerDirection
from gs_quant.backtests.actions import HedgeAction
from gs_quant.risk import FXDelta
from gs_quant.common import AggregationLevel

hedge_risk = FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')

trig_req = RiskTriggerRequirements(
    risk=hedge_risk,
    trigger_level=50_000,
    direction=TriggerDirection.ABOVE,  # ABOVE, BELOW, or EQUAL
)

trigger = StrategyRiskTrigger(trig_req, hedge_action)
```

### 4.3 MktTrigger — Trigger on Market Data

Fires when an external data series crosses a level.

```python
from gs_quant.backtests.triggers import MktTrigger, MktTriggerRequirements, TriggerDirection
from gs_quant.backtests.data_sources import GenericDataSource, MissingDataStrategy

# Build a data source from a pandas Series
data_source = GenericDataSource(pandas_series, MissingDataStrategy.fill_forward)

trig_req = MktTriggerRequirements(
    data_source=data_source,
    trigger_level=100.0,
    direction=TriggerDirection.BELOW,
)

trigger = MktTrigger(trig_req, action)
```

You can also use `GsDataSource` to pull data directly from the GS Marquee Data Catalog.

### 4.4 DateTrigger — Trigger on Specific Dates

```python
from gs_quant.backtests.triggers import DateTrigger, DateTriggerRequirements

trig_req = DateTriggerRequirements(
    dates=[date(2024, 3, 15), date(2024, 6, 15), date(2024, 9, 15)],
)

trigger = DateTrigger(trig_req, action)
```

### 4.5 AggregateTrigger — Combine Triggers with AND/OR Logic

```python
from gs_quant.backtests.triggers import AggregateTrigger, AggregateTriggerRequirements, AggType

agg_req = AggregateTriggerRequirements(
    triggers=[periodic_trigger, risk_trigger],  # can be Trigger or TriggerRequirements
    aggregate_type=AggType.ALL_OF,              # ALL_OF (AND) or ANY_OF (OR)
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

Actions define *what* happens when a trigger fires.

### 5.1 AddTradeAction — Add a Trade

The most common action. Resolves an instrument on the trigger date and adds it to the portfolio.

```python
from gs_quant.backtests.actions import AddTradeAction

action = AddTradeAction(
    priceables=instrument,          # single instrument or list of instruments
    trade_duration='1m',            # how long to hold: tenor, date, 'expiration_date', or None (forever)
    name='my_trade',                # optional name prefix
)
```

**`trade_duration` options:**
- `None` — hold forever (trade stays in portfolio until backtest ends)
- Tenor string (`'1m'`, `'3m'`, `'1y'`) — hold for that period then unwind
- `'expiration_date'` — hold until the instrument's expiration date (useful for options)
- `'next schedule'` — hold until the next periodic trigger date (auto-rolling)
- Explicit `datetime.date` — hold until that date
- `datetime.timedelta` — hold for that time delta

### 5.2 HedgeAction — Delta Hedge

Computes a risk measure on the portfolio and scales a hedge instrument to offset it.

```python
from gs_quant.backtests.actions import HedgeAction
from gs_quant.risk import FXDelta, IRDelta
from gs_quant.instrument import FXForward, IRSwap

# FX Delta hedge
hedge_risk = FXDelta(aggregation_level='Type', currency='USD')
hedge_instrument = FXForward(pair='EURUSD', settlement_date='1y', name='hedge_fwd')

action = HedgeAction(
    risk=hedge_risk,
    priceables=hedge_instrument,
    trade_duration='1m',             # optional — how long to hold the hedge
)
```

### 5.3 AddScaledTradeAction — Scale a Trade

Adds a trade scaled by a risk measure, size, or NAV.

```python
from gs_quant.backtests.actions import AddScaledTradeAction, ScalingActionType

action = AddScaledTradeAction(
    priceables=instrument,
    trade_duration='1m',
    scaling_type=ScalingActionType.size,
    scaling_level=1_000_000,         # target notional
)
```

### 5.4 EnterPositionQuantityScaledAction — Enter with Specific Quantity

Used primarily with the EquityVolEngine for quantity-based trading.

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

### 5.5 ExitTradeAction / ExitAllPositionsAction — Close Positions

```python
from gs_quant.backtests.actions import ExitTradeAction, ExitAllPositionsAction

# Exit a specific named trade
exit_named = ExitTradeAction(priceable_names='my_trade')

# Exit everything
exit_all = ExitAllPositionsAction()
```

### 5.6 Combining Actions on a Single Trigger

A trigger can have multiple actions. **Order matters** — they execute in sequence:

```python
# First exit old position, then add new one
trigger = StrategyRiskTrigger(trig_req, [exit_action, add_action])
```

---

## 6. Running a Backtest with GenericEngine

### Basic Example — Monthly FX Option Roll

```python
from datetime import date, datetime
from gs_quant.session import GsSession
from gs_quant.instrument import FXOption
from gs_quant.common import BuySell, OptionType
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.backtests.actions import AddTradeAction
from gs_quant.backtests.generic_engine import GenericEngine
from gs_quant.backtests.strategy import Strategy
from gs_quant.risk import Price

GsSession.use()

start_date = date(2023, 1, 3)
end_date = date(2024, 12, 31)

# Define instrument — remember premium=0 for FX options!
call = FXOption(
    buy_sell=BuySell.Buy,
    option_type=OptionType.Call,
    pair='USDJPY',
    strike_price='ATMF',
    expiration_date='2y',
    name='2y_call',
    premium=0,
)

# Periodic trigger: roll monthly, hold for 1 month
trig_req = PeriodicTriggerRequirements(start_date=start_date, end_date=end_date, frequency='1m')
action = AddTradeAction(call, '1m')
trigger = PeriodicTrigger(trig_req, action)

strategy = Strategy(None, trigger)

# Run
GE = GenericEngine()
backtest = GE.run_backtest(strategy, start=start_date, end=end_date, frequency='1b', show_progress=True)
```

### GenericEngine.run_backtest Parameters

| Parameter | Description | Default |
|---|---|---|
| `strategy` | The Strategy object | *required* |
| `start` | Backtest start date | None |
| `end` | Backtest end date | None |
| `frequency` | How often to evaluate: `'1b'` (daily), `'1w'`, `'1m'` | `'1m'` |
| `states` | Explicit list of dates (overrides start/end/frequency) | None |
| `risks` | Additional risk measures to compute | None |
| `show_progress` | Show progress bar | True |
| `csa_term` | CSA term for discounting | None |
| `initial_value` | Starting cash value | 0 |
| `result_ccy` | Currency for results | None |
| `market_data_location` | `'LDN'`, `'NYC'`, `'HKG'` | None |
| `is_batch` | Use websocket batching | True |

---

## 7. Extracting Backtest Results

The `run_backtest` call returns a `BackTest` object with several useful views.

### 7.1 result_summary — Main P&L DataFrame

```python
summary = backtest.result_summary
```

This is a `pandas.DataFrame` indexed by date with columns:
- `Price` — mark-to-market of live instruments
- `Cumulative Cash` — cumulative cash from unwound trades
- `Transaction Costs` — cumulative transaction costs
- `Total` — `Price + Cumulative Cash + Transaction Costs` (the total strategy P&L)
- Additional risk columns if requested

### 7.2 Plotting Performance

```python
import pandas as pd

# Total performance (MTM + Cash)
backtest.result_summary['Total'].plot(figsize=(10, 6), title='Strategy Performance')

# Or build manually
perf = backtest.result_summary[Price] + backtest.result_summary['Cumulative Cash']
perf.plot(figsize=(10, 6), title='Performance')
```

### 7.3 trade_ledger — Trade History

```python
ledger = backtest.trade_ledger()
```

Returns a DataFrame showing each trade: when it was entered, when it was closed, entry/exit values, and P&L.

### 7.4 risk_summary — Risk Time Series

```python
risk_df = backtest.risk_summary
```

Like `result_summary` but fills zero for dates with no instruments held (useful for risk plots).

### 7.5 Accessing Additional Risks

Pass extra risk measures via the `risks` parameter:

```python
from gs_quant.risk import Price, FXDelta
from gs_quant.common import AggregationLevel

backtest = GE.run_backtest(
    strategy, start=start_date, end=end_date, frequency='1b',
    risks=[Price, FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')],
)

# Access the risk time series
delta_series = backtest.result_summary[FXDelta(aggregation_level=AggregationLevel.Type, currency='USD')]
```

### 7.6 summary_stats — Strategy Performance Statistics

Call `summary_stats()` to get a pandas Series of key metrics for evaluating and comparing backtests:

```python
stats = backtest.summary_stats()
print(stats)
```

Output includes:

| Metric | Description |
|---|---|
| Start Date / End Date | Backtest date range |
| Duration (days) | Calendar days in backtest |
| Total PnL | Final cumulative P&L |
| Total Transaction Costs | Cumulative transaction costs |
| Total Trades | Number of trades entered |
| Peak PnL | Highest P&L reached |
| Annualised Return | Average daily P&L × 252 |
| Annualised Volatility | Std dev of daily P&L × √252 |
| Sharpe Ratio | Annualised return / annualised volatility |
| Sortino Ratio | Annualised return / annualised downside deviation |
| Max Drawdown | Largest peak-to-trough decline |
| Max Drawdown Duration (days) | Longest period spent in drawdown |
| Calmar Ratio | Annualised return / |max drawdown| |
| Current Drawdown | Drawdown at end of backtest |
| Average Daily PnL | Mean of daily P&L changes |
| Daily PnL Std Dev | Std dev of daily P&L changes |
| Best Day / Worst Day | Largest gain and loss in a single day |
| % Positive Days | Proportion of days with positive P&L |
| Skewness | Skewness of daily P&L distribution |
| Kurtosis | Excess kurtosis of daily P&L distribution |

You can customise the annualisation factor (default 252 business days):

```python
# Use 260 for a different convention
stats = backtest.summary_stats(annualisation_factor=260)
```

To compare two backtests side by side:

```python
comparison = pd.DataFrame({
    'Strategy A': backtest_a.summary_stats(),
    'Strategy B': backtest_b.summary_stats(),
})
comparison
```

---

## 8. Common Patterns and Best Practices

### 8.1 FX Options — Always Set premium=0

When backtesting FX options, always set `premium=0`. Otherwise resolution sets a premium that makes `DollarPrice` zero, and your backtest P&L will be meaningless.

```python
call = FXOption(
    buy_sell=BuySell.Buy,
    option_type=OptionType.Call,
    pair='EURUSD',
    strike_price='ATMF',
    expiration_date='1y',
    name='1y_call',
    premium=0,  # <-- Essential for backtests!
)
```

### 8.2 trade_duration — Controlling Position Lifetime

The `trade_duration` on `AddTradeAction` is critical:

- Use a **tenor matching the trigger frequency** for roll strategies (e.g. `'1m'` trade_duration with `'1m'` trigger frequency)
- Use **`'expiration_date'`** to hold options until expiry
- Use **`None`** if you want the trade to stay in the portfolio indefinitely
- Use **`'next schedule'`** to auto-exit when the next periodic trigger fires

### 8.3 Multiple Triggers — Order Matters

When passing multiple triggers to a Strategy, they are evaluated in order on each date. Put entry triggers before hedge triggers:

```python
strategy = Strategy(None, [entry_trigger, hedge_trigger])
```

When a single trigger has multiple actions, they execute in sequence:

```python
# Exit old positions first, then add new ones
trigger = PeriodicTrigger(trig_req, [exit_action, add_action])
```

### 8.4 Running Daily vs Monthly

- `frequency='1b'` — evaluate every business day (most common for accurate P&L)
- `frequency='1m'` — evaluate monthly (faster but misses intra-month dynamics)
- The trigger frequency and the backtest evaluation frequency are independent — e.g. you can run daily (`'1b'`) evaluation with monthly (`'1m'`) trigger to see daily P&L of a monthly roll strategy.

### 8.5 Naming Instruments

Always name your instruments. Names appear in the trade ledger and make debugging much easier:

```python
call = FXOption(..., name='1y_call')
hedge = FXForward(..., name='hedge_fwd')
```

### 8.6 Starting with a Pre-Existing Portfolio

Pass an instrument or list of instruments as the first argument to Strategy:

```python
# Start with a swaption already in the portfolio
strategy = Strategy(swaption, trigger)

# Start with multiple instruments
strategy = Strategy([swaption, swap], trigger)
```

### 8.7 Transaction Costs

Actions accept `transaction_cost` and `transaction_cost_exit` parameters. There are three transaction cost models, which can be used individually or combined.

#### ConstantTransactionModel — Fixed Cost per Transaction

A flat cash amount charged every time a trade is entered (or exited).

```python
from gs_quant.backtests.backtest_objects import ConstantTransactionModel
from gs_quant.backtests.actions import AddTradeAction

# $500 flat cost on entry; same cost on exit (default)
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ConstantTransactionModel(500),
)

# Different cost for entry vs exit
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ConstantTransactionModel(500),       # entry cost
    transaction_cost_exit=ConstantTransactionModel(250),   # exit cost
)
```

#### ScaledTransactionModel — Cost Proportional to an Instrument Attribute or Risk

The cost is computed by reading an instrument attribute (e.g. `notional_amount`) or calculating a risk measure, then multiplying by a `scaling_level`.

**Scaling by instrument attribute** (e.g. notional):

```python
from gs_quant.backtests.backtest_objects import ScaledTransactionModel

# Cost = notional_amount × 0.0001 (i.e. 1bp of notional)
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ScaledTransactionModel(
        scaling_type='notional_amount',  # any instrument property name
        scaling_level=0.0001,            # multiplier applied to the attribute value
    ),
)
```

**Scaling by a risk measure** (e.g. dollar price, vega):

```python
from gs_quant.backtests.backtest_objects import ScaledTransactionModel
from gs_quant.risk import Price, IRVega

# Cost = |Price| × 0.01 (i.e. 1% of premium)
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ScaledTransactionModel(
        scaling_type=Price,      # a RiskMeasure — will be calculated on the instrument
        scaling_level=0.01,
    ),
)

# Cost = |IRVega| × 0.05
action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=ScaledTransactionModel(
        scaling_type=IRVega,
        scaling_level=0.05,
    ),
)
```

The formula is: **cost = |scaling_type value| × scaling_level**. The absolute value is always taken for risk-based costs.

#### AggregateTransactionModel — Combine Multiple Models

Combines multiple transaction models using SUM, MAX, or MIN aggregation.

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
    # aggregate_type defaults to TransactionAggType.SUM
)

action = AddTradeAction(
    instrument,
    trade_duration='1m',
    transaction_cost=combined,
)
```

```python
from gs_quant.backtests.backtest_objects import AggregateTransactionModel, TransactionAggType

# Pay the MAX of a fixed cost or a scaled cost (e.g. minimum fee with proportional cost)
floor_model = AggregateTransactionModel(
    transaction_models=(
        ConstantTransactionModel(1000),                       # minimum $1000
        ScaledTransactionModel('notional_amount', 0.0001),    # or 1bp of notional
    ),
    aggregate_type=TransactionAggType.MAX,
)
```

#### Transaction Costs on HedgeAction

Transaction costs work the same way on `HedgeAction`:

```python
action = HedgeAction(
    risk=hedge_risk,
    priceables=hedge_instrument,
    trade_duration='1m',
    transaction_cost=ScaledTransactionModel('notional_amount', 0.00005),
    transaction_cost_exit=ConstantTransactionModel(0),  # no cost on hedge unwind
)
```

#### Viewing Transaction Costs in Results

Transaction costs appear in `backtest.result_summary` as the `'Transaction Costs'` column (cumulative). They are also included in the `'Total'` column:

```python
# Total = Price + Cumulative Cash + Transaction Costs
backtest.result_summary[['Total', 'Transaction Costs']].plot(title='Performance & Transaction Costs')
```

---

## 9. EquityVolEngine — Equity Vol Strategies

The `EquityVolEngine` runs equity option and variance swap backtests server-side for better performance.

```python
from gs_quant.instrument import EqOption, OptionType, OptionStyle
from gs_quant.backtests.strategy import Strategy
from gs_quant.backtests.triggers import PeriodicTrigger, PeriodicTriggerRequirements
from gs_quant.backtests.actions import EnterPositionQuantityScaledAction
from gs_quant.backtests.equity_vol_engine import EquityVolEngine
from gs_quant.target.backtests import BacktestTradingQuantityType

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

strategy = Strategy(None, trigger)

engine = EquityVolEngine()
backtest = engine.run_backtest(strategy, start=start_date, end=end_date)
```

---

## 10. Quick Reference — Minimal Backtest Template

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
```


