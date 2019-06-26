---
title: Assets
excerpt: Understanding assets
datePublished: 2019/06/22
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Assets
  - Stock
  - Future
  - Bond
  - Basket
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: SecurityMaster
    url: /gsquant/guides/Markets/security-master/
---

The `Asset` class in gs-quant provides a base for any security or observable instrument. In the gs-quant environment,
assets are used to describe any security with public identifiers (for example, a stock or bond), as well as any custom
product (e.g. bespoke index or basket). Assets are also used to describe observable fixings which are used in derivative
contracts (e.g. USD 3m Libor Rate).

## Asset Types

Below is an overview of a few of the various asset types used in gs-quant to cover the various securities used across
financial markets.

| Asset Type | Description                                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| INDEX      | Index which tracks an evolving portfolio of securities, and can be traded through cash or derivatives markets             |
| ETF        | Exchange traded fund which tracks an evolving portfolio of securities and is listed on an exchange                        |
| BASKET     | Bespoke basket which provides exposure to a customized collection of assets with levels published daily                   |
| STOCK      | Listed equities which provide access to equity holding in a company and participation in dividends or other distributions |
| FUTURE     | Standardized listed contract which provides delivery of an asset at a pre-defined forward date                            |
| CROSS      | FX cross or currency pair which provides expoure to foreign exchange markets                                              |

## Asset Lookups

Asset lookups can be performed through the `SecurityMaster` class.

<note>Examples require an initialized GsSession and relevant identifier licenses, please refer to <a href="/gsquant/guides/authentication/2-gs-session">
Sessions</a> for details</note>

```python
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier

asset = SecurityMaster.get_asset('2407966', AssetIdentifier.SEDOL)
```

Output:

```
Out[1]:
<gs_quant.markets.securities.Stock at 0x2df00a956a0>
```

See the [SecurityMaster](/gsquant/guides/Markets/security-master/) guide for more details.
