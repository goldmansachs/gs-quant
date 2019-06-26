---
title: Timeseries
excerpt: Understanding timeseries functions
datePublished: 2019/06/20
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Timeseries
  - pandas
  - Technical analysis
  - Timeseries algebra
  - Timeseries models
authors:
  - name: Roberto Ronderos
    github: robertoronderosjr
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: pandas
    url: https://pandas.pydata.org/
  - title: NumPy
    url: https://www.numpy.org/
  - title: LaTeX
    url: https://www.latex-project.org/
---

gs-quant comes with a `timeseries` package which provides a number of functions for dealing with analytics of financial
timeseries. This is based on the [pandas](https://pandas.pydata.org/) series object to provide extensions which are
specific to analyzing asset prices or other observable market data. These functions are used by our strategists to
analyze and backtest trading strategies.

## Timeseries Modules

Below is an overview of the various timeseries modules within gs-quant. Some are simple wrappers around the equivalent
pandas or NumPy function to provide consistent interface and documentation. Many are Goldman Sachs' implementations of
useful financial analysis functions which we use to quantify the performance of different strategies.

| Module       | Description                                                                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Algebra      | Basic numerical and algebraic operations, including addition, division, multiplication and other functions on timeseries                                                   |
| Analysis     | Functions used to analyze properties of timeseries, including lagging, differencing, autocorrelation, co-integration and other related operations                          |
| Datetime     | Date and time manipulation for timeseries, including date or time shifting, calendar operations, curve alignment and interpolation operations                              |
| Econometrics | Standard economic and time series analytics operations, including returns, drawdowns, volatility and other numerical operations which are generally finance-oriented       |
| Statistics   | Basic statistical operations, including probability and distribution analysis (generally not finance-specific routines)                                                    |
| Technicals   | Technical analysis functions including moving averages, volatility indicators, and and other numerical operations for analyzing statistical properties of trading activity |

## Usage

Import timeseries package or individual modules to access functionality:

```python
import gs_quant.timeseries as ts

x = ts.generate_series(1000)           # Generate random timeseries with 1000 observations
vol = ts.volatility(x, 22)             # Compute realized volatility
vol.tail()                             # Show last few values
```

Output:

```
2021-12-20 12.898025
2021-12-21 12.927230
2021-12-22 12.929520
2021-12-23 13.987033
2021-12-24 14.048165
dtype: float64
```

## Contributions

In addition to the standard [contribution guidelines](/gsquant/contribute/) for
gs-quant, we request that all timeseries function have 100% test coverage and full mathematical documentation using
[Latex](https://www.latex-project.org/). This helps ensure consumers of these functions can understand the exact
mathematical definition and usage semantics.
