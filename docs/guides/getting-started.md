---
title: Getting Started
excerpt: How to install gs-quant.
datePublished: 2019/06/14
dateModified: 2019/06/16
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Getting Started
  - Installation
  - Usage instructions
  - Quick start
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
  - name: Nick Young
    github: nick-young-gs
---

![GS Quant Cube](/docs/gsquant/guides/images/gs-quant-cube.svg)

# Welcome to gs-quant!

gs-quant is a Python toolkit for quantitative finance, which provides access to derivatives pricing and risk capabilities
through the Goldman Sachs developer APIs, as well as standalone packages for financial analytics.

It is created and maintained by quantitative developers (quants) at [Goldman Sachs](https://www.goldmansachs.com/) to
enable the development of trading strategies and analysis of derivative products. GS Quant can be used to facilitate derivative
structuring, trading, and risk management, or as a set of statistical packages for data analytics applications.

## Requirements

- Python 3.6 or greater
- Access to [PIP](https://pypi.org/project/pip/) package manager

You can verity your Python version with the command `python --version.`

Any Python-ready IDE will work. However, most of our team uses [PyCharm](https://www.jetbrains.com/pycharm/).

## Installation

```python
pip install gs-quant
```

Run this from a terminal (mac), command prompt (windows), or shell (linux)

<tip>GS users can use the following to enable SSO</tip>

```python
pip install gs-quant[internal]         # If using Anaconda or a virtual environment
pip install gs-quant[internal] --user  # Otherwise
```

## Use gs-quant

The following is a simple example which generates a random timeseries and computes 1-month (22 day) rolling realized
volatility:

```python
import gs_quant.timeseries as ts

x = ts.generate_series(1000)           # Generate random timeseries with 1000 observations
vol = ts.volatility(x, 22)             # Compute realized volatility
vol.tail()                             # Show last few values
```

```
Out[1]:
2021-12-20 12.898025
2021-12-21 12.927230
2021-12-22 12.929520
2021-12-23 13.987033
2021-12-24 14.048165
dtype: float64
```

Congratulations! You are up and running with gs-quant.

## Learn More

Please refer to our [Guides](/gsquant/guides/) and
[Tutorials](/gsquant/tutorials/) to learn about how gs-quant works and what you can do
with it.

## Contributions

Development of gs-quant is on [GitHub](https://github.com/goldmansachs/gs-quant). Contributions are encouraged! Please
see the [Contribution](/gsquant/contribute/Contributing/getting-started/) section for more details.

## Help

If you need any help or have feedback, please email us at [gs-quant@gs.com](mailto:gs-quant@gs.com?subject=GS%20Quant%20Docs).
