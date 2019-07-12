---
title: 02 - Financial Series
excerpt: How to access financial data series
datePublished: 2019/06/23
dateModified: 2019/06/23
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Financial Series
  - Asset Prices
  - Datasets
  - Dataframes
  - Dataseries
  - Series
  - Pandas
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Previous - Querying Data
    url: /gsquant/tutorials/Data-Analytics/1-querying-data/
  - title: Next - Financial Measures
    url: /gsquant/tutorials/Data-Analytics/3-financial-measures/
---

This tutorial provides an overview of how to interact with financial data series. We'll walk through some examples of
how to retrieve and visualize market data in order to analyze the performance of different assets. In this tutorial we
will examine the prices of equity baskets, which provide investors with exposure to different market themes through
custom baskets of stocks.

## Retrieving Prices

First, let's get the prices of the Goldman Sachs Hedge Fund VIP Basket (Ticker: [GSTHHVIP](https://marquee.gs.com/s/products/MAMGDVSWVXWHEHFQ/summary)).
This is a custom basket created by the Goldman Sachs Investment Research (GIR) group to track stocks which are widely
held by the hedge fund community in the US, based on [13-F](https://en.wikipedia.org/wiki/Form_13F) filings.

<note>Examples require an initialized GsSession and data subscription, please refer to
<a href="/docs/gsquant/guides/Authentication/2-gs-session">Sessions</a> for details</note>

We'll use the [GS Custom Basket Prices](https://marquee.gs.com/s/developer/datasets/CB) dataset, which contains prices
for a selection of GS thematic equity baskets. This dataset contains the `closePrice` field, which tracks the official
closing price for each asset on a daily basis, and is exposed in gs-quant as `Fields.CLOSE_PRICE`:

```python
from gs_quant.data import Dataset, Fields
from datetime import date

basket_ds = Dataset(Dataset.GS.CB)
start_date = date(2007,1,1)

vip_px = basket_ds.get_data_series(Fields.CLOSE_PRICE, start=start_date, ticker='GSTHHVIP')
vip_px.tail()
```

Output:

```python
Out[1]:
2019-06-14    269.314751
2019-06-17    271.106028
2019-06-18    274.046304
2019-06-19    276.174911
2019-06-20    279.399869
dtype: float64
```

The first observation in the series is on 28th November 2007, and prices are available up to the most recent US market
close. Let's plot the series to see how the basket has performed over the last 10+ years:

```python
vip_px.plot()
```

Output:

![VIP Price](/docs/gsquant/tutorials/images/vip_px.png)

## Comparing Performance

In addition to the Hedge Fund VIP Basket, the Portfolio Strategies Group within Goldman Sachs Investment Research also
computes a basket of stocks which are most widely shorted across the hedge fund community. This basket is called the
HF Important Shorts Basket (ticker: [GSTHVISP](https://marquee.gs.com/s/products/MAAB9K3SPS202CRS/summary)). We'll
retrieve the price history for this basket:

```python
visp_px = basket_ds.get_data_series(Fields.CLOSE_PRICE, start=start_date, ticker='GSTHVISP')
visp_px.tail()
```

Output:

```python
Out[3]:
2019-06-14    231.022088
2019-06-17    230.661374
2019-06-18    232.949564
2019-06-19    233.424179
2019-06-20    235.450614
dtype: float64
```

Now let's compare the prices of the two assets. First, we'll align the two series so that they cover the same date range,
then index both series to 100 on the initial date and plot:

```python
import gs_quant.timeseries as ts
import pandas as pd

[vip, visp] = ts.align(vip_px, visp_px, ts.Interpolate.INTERSECT)
vip = ts.index( vip, 100 )
visp = ts.index( visp, 100 )
compare = pd.DataFrame({'vip': vip, 'visp': visp})
compare.plot()
```

Output:

![VIP vs VISP](/docs/gsquant/tutorials/images/vip_visp.png)

Looks like the VIP basket has outperformed, the VISP basket over the last 5 or so years. Next we'll analyze performance
over a few key statistical dimensions.

## Analyzing Series

There are a few basic properties of a financial series we would look at in order to evaluate how it would fit into a
portfolio. We'll run a quick analysis of our two series to evaluate them against these dimensions. Here's a quick
summary of what we are going to compute:

| Measure           | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| Annual Volatility | Historical annualized realized volatility                      |
| Max Drawdown      | Maximum peak-to-trough percentage drawdown over a given period |
| Correlation       | Degree of linear relationship between the two assets           |

Use the gs-quant timeseries functions to calculate, and then plot results:

```python
import matplotlib.pyplot as plt

window = 22     # 1 month (22 business day) lookback

vols = pd.DataFrame({'vip': ts.volatility(vip, window), 'visp': ts.volatility(visp, window)})
draws = pd.DataFrame({'vip': ts.max_drawdown(vip, window), 'visp': ts.max_drawdown(visp, window)})
corr = ts.correlation(vip, visp, window )

plot, axs = plt.subplots(3, sharex=True)
plot.suptitle('Hedge Fund VIP vs Hedge Fund VIP Short')

axs[0].title.set_text('Volaility')
axs[1].title.set_text('Max Drawdown')
axs[2].title.set_text('Correlation')

axs[0].plot(vols)
axs[1].plot(draws)
axs[2].plot(corr)
```

Output:

![VIP vs VISP Analytics](/docs/gsquant/tutorials/images/vip_visp_analytics.png)

A few quick takeaways, which were probably intuitive from the original price curves:

- The hedge fund short basket generally has lower volatility than the long basket
- The long basket has larger maximum drawdown than the short basket
- The correlation between the products is generally close to 1
