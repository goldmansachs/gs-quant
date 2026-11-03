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

**Look up a dataset's fields with `GsDataApi.get_types('<ID>')` (`from gs_quant.api.gs.data import GsDataApi`)
before guessing a field name**: it returns every field and its type. For what the fields mean, coverage, history and
who supports the dataset, point the user to its page, `https://marquee.gs.com/s/developer/datasets/<ID>`.

You can also use the built-in vendor enums:

```python
ds = Dataset(Dataset.GS.HOLIDAY)
ds = Dataset(Dataset.TR.TREOD)
```

> **Equities and listed instruments:** For equities and most listed instruments
> (equity indices, ETFs, futures, etc.) the correct dataset is almost always `TREOD`
> (Thomson Reuters End-of-Day). Filter it by `bbid`.
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
    bbid=['EURUSD', 'USDJPY'],  # filters are passed as kwargs
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
| `**kwargs` | Filters, e.g. `bbid=['EURUSD']`, `ric='.SPX'`, `assetId='...'` |

Filter by the dataset's symbol dimension, which `GsDataApi.get_definition('<ID>').dimensions.symbol_dimensions`
returns. When it is `assetId`, you can filter by `bbid` or `ric` instead. Multiple values are passed as a list.

```python
# Filter by a single value
df = ds.get_data(dt.date(2025, 1, 2), dt.date(2025, 3, 19), bbid='EURUSD')

# Filter by multiple values
df = ds.get_data(dt.date(2025, 1, 2), dt.date(2025, 3, 19), bbid=['EURUSD', 'GBPUSD'])

# Restrict to specific fields
df = ds.get_data(dt.date(2025, 1, 2), dt.date(2025, 3, 19), bbid=['EURUSD'], fields=['impliedVolatility', 'tenor'])

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

## Index Constituents

**`Index.get(identifier).get_constituents_for_date(date)` returns the constituents Marquee holds for
an index on a date**: one row each, with columns `identifier`, `name`, `asset_id` and `quantity`.
For SPX the identifiers are Bloomberg tickers such as `OKE UN`. If Marquee holds none for that
date, the table is empty. `get_latest_constituents()` returns the latest.

```python
from gs_quant.markets.index import Index

constituents = Index.get('SPX').get_constituents_for_date(dt.date(2020, 1, 2))
```

`SecurityMaster.get_asset(...).entity['underliers']` lists the current constituents as Marquee IDs
only; for a past date use `Index`.

## Realised Volatility

**`gs_quant.timeseries.volatility(series, w)` turns a price series into rolling realised
volatility**, annualised and in percent (20% comes back as `20.0`), unlike risk measures, which
return vols as decimals. `w` is the window: a number of observations such as `22`, or a tenor such
as `'1m'`.

```python
from gs_quant.timeseries import volatility

close = Dataset('TREOD').get_data_series('closePrice', dt.date(2026, 6, 1), dt.date(2026, 9, 30), bbid='SPX')
vol = volatility(close, 22)
```

## Intraday Data

**Intraday data comes from datasets indexed by time, queried with `dt.datetime` bounds.** For
example, for SPX, `TR` has bid, ask and trade prices, and `EDRVOL_PERCENT_INTRADAY` has implied vols
by tenor and strike. Both take `bbid`; times without a time zone are read as UTC.

```python
ticks = Dataset('TR').get_data(dt.datetime(2026, 10, 26, 14, 0), dt.datetime(2026, 10, 26, 15, 0), bbid=['SPX'])
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
ds.upload_data(data)  # accepts list of dicts or a DataFrame
```

## Common Pitfalls

- **Unknown filter name** — raises `MqRequestError` with status 400. A value that matches nothing
  usually returns an empty DataFrame, but some datasets raise the same 400 for it, so check both the
  filter name and the value.
- **`ticker` can match several assets** — `ticker='SPX'` does. Filter by `bbid`, `ric` or `assetId`.
- **Query size limits** — very wide queries (many assets x long date range) will time out
  or be rejected. Iterate in batches as shown above.
- **Entitlements** — if `get_data` returns an empty DataFrame unexpectedly, your session
  may not have the required entitlement scope (e.g. `read_product_data`).
- **Intraday vs daily** — some datasets are indexed by `datetime` (intraday); others by
  `date` (EOD). Pass `dt.datetime` objects for intraday datasets and `dt.date` for EOD.
