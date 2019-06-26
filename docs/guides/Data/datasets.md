---
title: Datasets
excerpt: Understanding how datasets work
datePublished: 2019/06/17
dateModified: 2019/06/17
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Data
  - Datasets
  - Timeseries
authors:
  - name: Roberto Ronderos
    github: robertoronderosjr
  - name: Andy Phillips
    github: andyphillipsgs
links:
  - title: Weather Dataset
    url: https://marquee.gs.com/s/developer/datasets/WEATHER
  - title: Dataset Catalog
    url: https://marquee.gs.com/s/developer/datasets
  - title: Pandas
    url: https://pandas.pydata.org/
---

Datasets represent a collection of timeseries which share a common schema, owner, and are generally subject to consistent
entitlements. The easiest way to learn how to interact with datasets is to use the
[WEATHER](https://marquee.gs.com/s/developer/datasets/WEATHER) example, which contains weather information for
several major US cities from the National Weather Service. This dataset is available to all applications and does not
need to be requested explicitly.

You can view and request available datasets from the [Marquee Data Catalog](https://marquee.gs.com/s/developer/datasets).

## Dataset Objects

All our datasets are either time-based (intraday) or date-based (daily). Datasets return fields that are categorized as
either measures or dimensions:

- Measures are facts that are usually quantities and that can be aggregated, such as tickers and exchanges
- Dimensions describe or provide context to measures, like closing prices and volumes

If the data is a curve or surface, then the axes will usually be dimensions.

## Date-based Datasets

Date-based datasets have `date` listed as a field in their data
description. The following parameters are valid for queries to date-based datasets:

- `startDate` (optional) - defaults to the end date minus a dataset-specific interval, which is currently 30 days
- `endDate` (optional) - defaults to the current date
- `dates` (optional) - used to return data from a specific set of dates

## Time-based Datasets

Time-based datasets have time and updateTime listed as a field in their data description page. The following parameters
are valid for queries to time-based datasets:

- `startTime` (optional) - defaults to the end time minus a dataset-specific
- `interval` - currently 24 hours for all real-time datasets
- `endTime` (optional) - defaults to the current datetime
- `times` (optional) - used to return data from a specific set of date times

### Using Intervals

Time-based datasets can have very large number of observations over a given window (thousands per second). In order to
interact with this data, our APIs provide the ability to down-sample data on our servers over given intervals. The
`intervals` parameter allow you to get data which is evenly distributed in the specified number
of intervals between the time or date range specified. Example:

```
from gs_quant.data import Dataset
from datetime import date

weather_ds = Dataset('WEATHER')
data_frame = weather_ds.get_data(date(2016, 1, 1),  date(2016, 1, 31), city=["Boston"], intervals=3)

print(data_frame)
```

Output:

```
     city        date  dewPoint  ...  snowfall                updateTime  windSpeed
0  Boston  2016-01-11      12.0  ...       0.0  2017-03-06T16:49:36.472Z       19.0
1  Boston  2016-01-21       7.0  ...       0.0  2017-03-06T16:49:36.473Z       13.6
2  Boston  2016-01-31      29.0  ...       0.0  2017-03-06T16:49:36.476Z       11.6

[3 rows x 10 columns]
```

<note>API responses are limited to approximately 100MB. If you receive a 400 Bad Request exception with the message
"Number of rows returned... are more than maximum allowed", batch your query down into multiple, smaller queries.
Consider using smaller date / time ranges (adjust startTime and endTime or startDate and endDate as needed) or
querying for fewer entities (e.g. asset ids, reports) each time.</note>

### Field Selection

If you want to ensure the response only contains the fields that you are interested in, you can use the `fields`
parameters. In the weather dataset, say that you are only interested in `maxTemperature` and `minTemperature`. To only
return these two fields, pass in the desired fields as arguments. Example:

```
from gs_quant.data import Dataset
from datetime import date

weather_ds = Dataset('WEATHER')
data_frame = weather_ds.get_data(date(2016, 1, 1), date(2016, 1, 2), city=["Boston"], fields=['maxTemperature', 'minTemperature'])

print(data_frame)
```

Output:

```
     city        date  maxTemperature  minTemperature
0  Boston  2016-01-01            41.0            33.0
1  Boston  2016-01-02            40.0            31.0
```
