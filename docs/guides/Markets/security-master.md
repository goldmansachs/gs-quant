---
title: Security Master
excerpt: Understanding the Security Master
datePublished: 2019/06/22
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Securities Master
  - Security Master
  - Securities
  - Security
  - Asset
  - SecMaster
  - SMF
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Assets
    url: /gsquant/guides/Markets/assets/
  - title: OpenFIGI
    url: https://www.openfigi.com/
---

The `SecurityMaster` class in gs-quant provides access to security lookups and symbology functions to resolve assets
across different asset classes. This allows security lookup through time using a range of different identifiers, subject
to the licensing considerations of the various providers.

## Identifiers

Below is an overview of some of the various identifiers used to reference securities in financial markets. These
identifiers can be proprietary to individual vendors or in the public domain.

| Identifier             | Description                                                  | Example             |
| ---------------------- | ------------------------------------------------------------ | ------------------- |
| MARQUEE_ID             | Goldman Sachs Marquee identifier code                        | MA4B66MW5E27UAHKG34 |
| REUTERS_ID             | Thompson Reuters / Refinitiv Instrument Code (RIC)           | GS.N                |
| BLOOMBERG_ID           | Bloomberg identifier and exchange code                       | GS UN               |
| BLOOMBERG_COMPOSITE_ID | Bloomberg composite identifier and exchange code             | GS US               |
| CUSIP                  | Committee on Uniform Security Identification Procedures code | 38141G104           |
| ISIN                   | International Securities Identification Number               | US38141G1040        |
| SEDOL                  | LSE Stock Exchange Daily Official List code                  | 2407966             |
| TICKER                 | Exchange ticker                                              | GS                  |

## Security Lookups

The `SecurityMaster` class can be used to perform lookups against different identifiers. For example, to look up an
asset based on a SEDOL:

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

Get the asset name:

```python
asset.name
```

Output:

```
Out[2]:
'The Goldman Sachs Group, Inc.'
```

## Exchange Codes

Securities can also be identified by exchange codes. Goldman Sachs' names for the various securities exchanges are
enumerated in the `ExchangeCode` class. These can be used in security lookups:

```python
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier, ExchangeCode

asset = SecurityMaster.get_asset('GS', AssetIdentifier.TICKER, exchange_code=ExchangeCode.NYSE)
```

Output:

```
Out[3]:
<gs_quant.markets.securities.Stock at 0x2df00a956a0>
```

## As-of Lookups

The `SecurityMaster` class supports historical symbology resolution against a variety of identifiers for equities,
dating back to 2002. To perform a historical lookup, use the `asof` parameter:

```python
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier
from datetime import date

asset = SecurityMaster.get_asset('2407966', AssetIdentifier.SEDOL, as_of=date(2017,1,1))
```

Output:

```
Out[4]:
<gs_quant.markets.securities.Stock at 0x2df7fb95748>
```

## Identifier Maps

Given an asset, the SecurityMaster in gs-quant can retrieve the other identifiers for a given date as a Python `dict`:

```python
from gs_quant.markets.securities import SecurityMaster, AssetIdentifier
from datetime import date

asset = SecurityMaster.get_asset('2407966', AssetIdentifier.SEDOL)
asset.get_identifiers()
```

Output:

```
Out[5]:
{'BBID': 'GS UN',
 'BCID': 'GS US',
 'CUSIP': '38141G104',
 'ISIN': 'US38141G1040',
 'RIC': 'GS.N',
 'SEDOL': '2407966',
 'TICKER': 'GS'}
```
