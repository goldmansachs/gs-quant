---
title: GS API
excerpt: Understanding the Goldman Sachs APIs
datePublished: 2019/06/19
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - API
  - Marquee
  - Developer
  - GS API
  - Marquee API
  - developer.gs.com
  - api.gs.com
  - api.marquee.gom
authors:
  - name: Roberto Ronderos
    github: robertoronderosjr
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Goldman Sachs Developer
    url: https://developer.gs.com
  - title: Marquee Developer
    url: https://marquee.gs.com/s/developer/home
---

In order to access the full range of data, analytics, and other content offered by Goldman Sachs, gs-quant uses the
[Marquee APIs](https://marquee.gs.com/s/developer/docs/getting-started) as an interface to the underlying
services, including the SecDb risk platform. Clients of Goldman Sachs can request access to these APIs through their
sales representative or through [developer@gs.com](mailto:developer@gs.com). These services can then be accessed through gs-quant for native
integration into the python environment.

We have provided direct interfaces between gs-quant and the following APIs:

| API                                                                                        | Description                                         |
| ------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| [Assets](https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service)         | Definition of securities and observable instruments |
| [Content](https://marquee.gs.com/s/developer/docs/endpoint-reference/content-service)      | Access to GS insights and ideas                     |
| [Data](https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service)            | Proprietary end-of-day and intraday data            |
| [Indices](https://marquee.gs.com/s/developer/docs/endpoint-reference/indices-service)      | Create and rebalance index products                 |
| [Portfolios](https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service) | Upload and interact with portfolio data             |
| [Risk](https://marquee.gs.com/s/developer/docs/endpoint-reference/risk-service)            | Access SecDb pricing models and risk engines        |

By connecting gs-quant to these APIs, users will be able to perform most of the operations available through
the API itself (e.g. create, update, get or delete resources) via friendly python methods. This allows straightforward
interaction with GS data, pricing engines and the rest of the Marquee platform programmatically.
