---
title: 01 - Querying Datasets
excerpt: How to query and access data using pandas dataframes
datePublished: 2019/06/17
dateModified: 2019/06/23
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Querying Data
  - Retrieving Data
  - Datasets
  - Dataframes
  - Dataseries
  - Series
  - Pandas
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
  - name: Roberto Ronderos
    github: robertoronderosjr
links:
  - title: Next - Financial Series
    url: /docs/gsquant/tutorials/Data-Analytics/2-financial-series/
---


Welcome! This tutorial demonstrates how to use gs-quant to access Datasets available through the Goldman Sachs Developer 
platform. This provides an overview of how to interact with dataset objects in order to query multi-dimensional data
and interact with the results via [pandas dataframes](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html).
These are two-dimensional, size-mutable, tabular data structures with labeled axes (rows and columns). Here we cover the 
basics of the data apis and dataset objects.

## Accessing a dataset

To start with, we'll use the the [WEATHER](https://marquee.gs.com/s/developer/datasets/WEATHER) dataset. This is a public
dataset which provides historical information on the weather across various cities in the US.   

<note>Examples require an initialized GsSession and data subcription, please refer to 
<a href="/docs/gsquant/guides/Authentication/2-gs-session">Sessions</a> for details</note>

Let's start by getting the dataset, and looking at the coverage:

```
from gs_quant.data import Dataset

weather_ds = Dataset(Dataset.GS.WEATHER)
weather_ds.get_coverage()
```
Output:
```
Out[1]: 
           city
0    LosAngeles
1        Boston
2  SanFrancisco
3        Austin
4   NewYorkCity
5       Chicago
```

The [get_coverage](/docs/gsquant/api/classes/gs_quant.data.Dataset.html#gs_quant.data.Dataset.get_coverage) method on a 
dataset will tell you the asset coverage. For financial datasets, the assets will generally be securities or other 
financial observables, as described in the [Assets Guide](/docs/gsquant/guides/Markets/assets/). In this case, the 
dataset coverage is a set of US cities. 

## Querying Data

Now that we know the coverage of the dataset, we can go ahead and query for the underlying data at a given location. 
We'll use the [datetime](https://docs.python.org/2/library/datetime.html) class to query the weather in Boston from 
through January 2016, and use the `tail` function to show the last 5 rows:

```
from datetime import date

data_frame = weather_ds.get_data(date(2016, 1, 1), date(2016, 1, 31), city=["Boston"])
data_frame.tail()
```
Output:
```
Out[2]: 
      city        date    ...                    updateTime  windSpeed
26  Boston  2016-01-27    ...      2017-03-06T16:49:36.475Z       11.7
27  Boston  2016-01-28    ...      2017-03-06T16:49:36.475Z        7.1
28  Boston  2016-01-29    ...      2017-03-06T16:49:36.475Z        6.3
29  Boston  2016-01-30    ...      2017-03-06T16:49:36.476Z       11.3
30  Boston  2016-01-31    ...      2017-03-06T16:49:36.476Z       11.6
[5 rows x 10 columns]
```

## Basic analytics

Let's say we want to find out which of the days in January 2016 it snowed in Boston. We can now use the regular 
pandas API functions to query the dataframe. We are going to create a pandas 
[Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html) object from the snowfall 
column. Dataframes are aligned in a tabular fashion using rows and columns, and accessing data works similar to the way 
you would select data with python dictionaries. To access columns simply reference them by their name. Likewise, use 
multiple column names in case you want to select more than one column. 

Then we can filter for days with values greater than 0:

```python
snowfall = data_frame.snowfall
snowfall.where(lambda x: x > 0).dropna()
```
Output:
```
Out[3]: 
11    0.3
16    1.3
17    1.8
22    6.1
Name: snowfall, dtype: float64
```

So there were 4 days with snow in January 2016. Let's look at the statistical properties of the series:

```python
snowfall.describe()
```
Output:
```
Out[4]: 
count    31.000000
mean      0.306452
std       1.144825
min       0.000000
25%       0.000000
50%       0.000000
75%       0.000000
max       6.100000
Name: snowfall, dtype: float64
```

The average (mean) snowfall in January 2016 was 0.3 inches per day, with the most (6 inches) on the 22nd. Next up we'll 
look at functions we can use to work with larger datasets. 

## Selecting Columns

As described above, we can use the pandas apis to select different rows and columns in our local python process. 
However, when dealing with large series, we may want to filter rows or columns on the server to avoid having to retrieve 
large amounts of data. Let's just grab the snowfall data as a Series from the server and show the last few values: 

```python
snow_srv = weather_ds.get_data_series('snowfall', date(2016, 1, 1), date(2016, 1, 31), city=["Boston"])
snow_srv.tail()
```
Output: 
```
Out[5]: 
2016-01-27    0.0
2016-01-28    0.0
2016-01-29    0.0
2016-01-30    0.0
2016-01-31    0.0
dtype: float64
```

This query only retrieved the snowfall column from the server, directly into a Series, so we cut out a few steps above 
and made this more efficient if we only need these values. 

## Downsampling Data

Whilst the 31 days snowfall data in January doesn't represent a huge amount of data (only 496 bytes!), let's imagine 
this dataset had a large amount of intraday trading data, which could mean many thousands of updates per second. We can 
use the GS data platform to automatically downsample data on the server. In this example, we'll sample the wind speed
in Chicago at 4 equally-spaced times over the month of January:

```python
wind_speed = weather_ds.get_data_series('windSpeed', date(2016, 1, 1), date(2016, 1, 31), city=["Chicago"], intervals=4)
print(wind_speed)
```
Output: 
```
2016-01-08     5.1
2016-01-16    12.3
2016-01-23     2.6
2016-01-31     5.5
dtype: float64
```

This allows us to interact with very large datasets in an efficient way. For more information on datasets, refer to the 
[Datasets](/docs/gsquant/guides/Data/datasets/) guide. Next, we'll explore how to interact with asset price data.