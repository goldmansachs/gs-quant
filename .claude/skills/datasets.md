---
name: gs-quant-datasets
description: "Accessing market and reference data via the gs_quant Dataset class: get_data, get_data_series, get_data_last, get_coverage, uploading data, batching large queries. Covers TREOD for equities, FXIVOL_STANDARD, symbol dimensions, and common pitfalls."
---

# Accessing Data with `Dataset`

The `Dataset` class in `gs_quant.data` provides access to Marquee datasets — structured,
time-series collections of market and reference data.

```python
from gs_quant.data import Dataset
import datetime as dt
```

## Constructing a Dataset

Pass the dataset ID string (visible in the Marquee catalog URL):

```python
ds = Dataset('FXIVOL_STANDARD')
```

You can also use the built-in vendor enums:

```python
ds = Dataset(Dataset.GS.HOLIDAY)
ds = Dataset(Dataset.TR.TREOD)
```

> **Equities and listed instruments:** For equities and most listed instruments
> (equity indices, ETFs, futures, etc.) the correct dataset is almost always `TREOD`
> (Thomson Reuters End-of-Day). Use `bbid` as the symbol dimension.
>
> ```python
> ds = Dataset('TREOD')
> df = ds.get_data(dt.date(2025, 1, 2), dt.date(2026, 3, 19), bbid=['GS UN', 'AAPL UW'])
> ```

## `get_data` — Fetch a DataFrame

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

## `get_data_series` — Fetch a Single-Field Time Series

Returns a `pandas.Series` indexed by date/time:

```python
series = ds.get_data_series(
    field='impliedVolatility',
    start=dt.date(2025, 1, 2),
    end=dt.date(2025, 3, 19),
    bbid='EURUSD',
)
```

## `get_data_last` — Most Recent Data Point

Returns the latest available row at or before `as_of`:

```python
latest = ds.get_data_last(
    as_of=dt.datetime.now(),
    bbid=['EURUSD', 'USDJPY'],
)
```

## `get_coverage` — What Assets Are Available

```python
coverage = ds.get_coverage()
print(coverage.head())

# Include the history start date for each asset
coverage = ds.get_coverage(include_history=True)
coverage = coverage.sort_values('historyStartDate')
```

## Iterating Over Large Queries

For datasets with many assets or long date ranges, break queries into smaller chunks:

```python
import pandas as pd

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

ds = Dataset('EDRVOL_PERCENT_V1_STANDARD')
coverage = ds.get_coverage()
ids = coverage['assetId'].tolist()[:10]

df = query_in_batches(ds, ids, dt.date(2024, 1, 1), dt.date(2025, 3, 19), id_field='assetId')
```

## Uploading Data

```python
import pandas as pd

data = [
    {'date': '2025-03-19', 'city': 'London', 'maxTemperature': 14.0, 'minTemperature': 7.0},
    {'date': '2025-03-19', 'city': 'New York', 'maxTemperature': 18.0, 'minTemperature': 9.0},
]
ds = Dataset('MY_CUSTOM_DATASET')
ds.upload_data(data)                     # accepts list of dicts or a DataFrame
```

## Common Pitfalls

- **Wrong dimension name** — each dataset has its own symbol dimension (`bbid`, `assetId`,
  `ticker`, `ric`, etc.). Check the Marquee catalog page. Passing the wrong kwarg silently
  returns an empty DataFrame.
- **Query size limits** — very wide queries (many assets x long date range) will time out
  or be rejected. Iterate in batches as shown above.
- **Entitlements** — if `get_data` returns an empty DataFrame unexpectedly, your session
  may not have the required entitlement scope (e.g. `read_product_data`).
- **Intraday vs daily** — some datasets are indexed by `datetime` (intraday); others by
  `date` (EOD). Pass `dt.datetime` objects for intraday datasets and `dt.date` for EOD.
