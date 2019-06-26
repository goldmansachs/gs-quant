---
title: 04 - Charting Data
excerpt: Learn to chart your data through GS Quant.
datePublished: 2019/06/18
keywords:
  - Data Analytics
  - Charting Data
  - Querying Data
authors:
  - name: Roberto Ronderos
    github: robertoronderosjr
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Previous - Financial Measures
    url: /docs/gsquant/tutorials/Data-Analytics/3-financial-measures/
  - title: Next - Exporting Data
    url: /docs/gsquant/tutorials/Data-Analytics/5-exporting-data/
---

A simple way to chart data in GS Quant is by installing `matplotlib`. This plotting library can be used to easily
generate plots, histograms, power spectra, bar charts, error charts, scatter plots, etc.

Let's use this library to chart calculated implied volatility from GS Quant.

<note>Examples require an initialized GsSession and data subscription, please refer to
<a href="/docs/gsquant/guides/Authentication/2-gs-session">Sessions</a> for details</note>

## Querying Data

First, let's retrieve S&P 500 end of day implied volatility for 1 month tenor with forward strike:

```python
from gs_quant.data import Dataset
from gs_quant.markets import PricingContext

market_date = PricingContext.current.market_data_as_of  # Determine current market date

vol_dataset = Dataset(Dataset.GS.EDRVOL_PERCENT_LONG)  # Initialize the equity implied volatility dataset
vol_data = vol_dataset.get_data(market_date, market_date, ticker='SPX', tenor='1m', strikeReference='forward')

print(vol_data.tail())
```

Output:

```python
    absoluteStrike              assetId  ... ticker            updateTime
21     4049.365704  MA4B66MW5E27U8P32SB  ...    SPX  2019-06-17T22:18:01Z
22     4193.985908  MA4B66MW5E27U8P32SB  ...    SPX  2019-06-17T22:18:01Z
23     4338.606111  MA4B66MW5E27U8P32SB  ...    SPX  2019-06-17T22:18:01Z
24     5061.707130  MA4B66MW5E27U8P32SB  ...    SPX  2019-06-17T22:18:01Z
25     5784.808149  MA4B66MW5E27U8P32SB  ...    SPX  2019-06-17T22:18:01Z

[5 rows x 9 columns]
```

## Charting Data

### Implied Volatility By Strike

Now, let's use `vol_data` to chart the implied volatility by relative strike:

<note>Remember to install <a href="https://matplotlib.org/3.1.0/users/installing.html">matplotlib</a>.</note>

add the following import statement to have matplot available:

```python
import matplotlib.pyplot as plt
```

then plot your data like so:

```python
strikes = vol_data['relativeStrike']
vols = vol_data['impliedVolatility'] * 100

plt.plot(strikes, vols, label='Implied Volatility by Strike')
plt.xlabel('Relative Strike')
plt.ylabel('Implied Volatility')
plt.title('Implied Volatility by Strike')

plt.show()
```

Which will create a plot like this:

![SPX 25 Delta Skew](/gsquant/tutorials/images/spx_implied_by_strike.JPG)

### Implied Volatility By Tenor

Likewise we can use the same technique to chart the implied volatility by tenor:

```python
vol_data = vol_dataset.get_data(market_date, market_date, ticker='SPX', relativeStrike=1.0, strikeReference='forward')
tenors = vol_data['tenor']
vols = vol_data['impliedVolatility'] * 100
plt.plot(tenors, vols, label='Implied Volatility by Tenor')
plt.xlabel('Tenor')
plt.ylabel('Implied Volatility')
plt.title('Implied Volatility by Tenor')
plt.show()
```

Producing:

![SPX 25 Delta Skew](/gsquant/tutorials/images/spx_implied_by_tenor2.JPG)

### Implied Volatility Area By Tenor And Strike

Now, let's combine the two and plot a vol surface to chart the implied volatility by tenor and strike:

```python
from gs_quant.data import Dataset
from gs_quant.datetime import point_sort_order
from gs_quant.markets import PricingContext
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


vol_dataset = Dataset(Dataset.GS.EDRVOL_PERCENT_LONG)  # Create dataset for equity implied volatility

market_date = PricingContext.current.market_data_as_of
tenors_to_plot = ["2w", "1m", "2m", "3m", "4m", "5m", "6m", "9m", "1y"]
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection='3d')

# Implied vol data for the current market data date
vol_data = vol_dataset.get_data(market_date, market_date, ticker='SPX', strikeReference='forward')
vol_data = vol_data[vol_data.tenor.isin(tenors_to_plot)]
vol_data['tenorDays'] = vol_data.tenor.map(lambda t: point_sort_order(t))

# Reformat the data
X = vol_data.relativeStrike.unique()
Y = vol_data.tenorDays.unique()
Z = np.array([vol_data[vol_data.tenorDays == y].impliedVolatility.values.tolist() for y in Y]) * 100
X, Y = np.meshgrid(X, Y)

# Plot the surface
ax.xaxis.set_label_text("Strike")
ax.yaxis.set_label_text("Tenor")
ax.zaxis.set_label_text("Implied Vol")
ax.set_zlim(0, 75)
ax.set_yticks(vol_data.tenorDays.unique())
ax.set_yticklabels(vol_data.tenor.unique())
surface = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

plt.show()
```

The previous example should produce a 3D graphs similar to this:

![SPX 25 Delta Skew](/gsquant/tutorials/images/spx_area.JPG)
