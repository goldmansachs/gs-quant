# GS Quant

**GS Quant** is a python toolkit for quantitative finance, which provides access to an extensive set of derivatives pricing data through the Goldman Sachs Marquee developer APIs. Libraries are provided for timeseries analytics, portfolio manipulation, risk and scenario analytics and backtesting. Can be used to interact with the Marquee platform programmatically, or as a standalone software package for quantitiative analytics.

Created and maintained by quantitative developers (quants) at Goldman Sachs to enable development of trading strategies and analysis of derivative products. Can be used to facilitate derivative structuring and trading, or as statistical packages for a variety of timeseries analytics applications. 

See also Getting Started notebook in the gs_quant folder or package.

## Installation
```pip install gs_quant```

## Dependencies
Python 3.6 or 3.7  
Package dependencies can be installed by pip.

## Example
```python
from gs_quant import *

with AppSession('CLIENT_ID', 'CLIENT_SECRET', Environment.PROD) as session:
    # get coverage for a dataset and run a query
    coverage = session.get_coverage('WEATHER')
    df = session.get_data('WEATHER', {'city': ['Boston', 'Austin']}, '2016-02-01', '2016-02-14')
```

## Help
Questions? Comments? Write to data-services@gs.com
