---
title: GsSession
excerpt: Understanding GS authentication sessions
datePublished: 2019/06/16
dateModified: 2019/06/16
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Authentication
  - Session
  - GsSession
  - Marquee API
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
  - name: Nick Young
    github: nick-young-gs
links:
  - title: Sessions
    url: /gsquant/guides/Authentication/1-sessions/
  - title: Marquee Developer
    url: https://marquee.gs.com/s/developer
---

## GsSession

GsSession manages authentication for the GS Developer APIs. This class allows you to hold an authentication context to
the developer APIs within a given process. You can hold a reference to multiple sessions within the same process.

## OAuth

Authenticating with OAuth application credentials.

<note>Application credentials can be created through the <a href='https://marquee.gs.com/s/developer/home'>Marquee Developer Site</a>. OAuth is the recommended approach for
GS Clients.</note>

Create and use a GsSession with OAuth application credentials:

```python
from gs_quant.session import GsSession

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

GsSession.use(client_id=client_id, client_secret=client_secret)
```

Replace the above `clientid` and `client_secret` with your own credentials.

## Single-Sign-On

Where SSO is available, users can authenticate as follows:

```python
from gs_quant.session import GsSession

GsSession.use()
```

## Scopes

GS Developer scopes provide access to different capabilities within gs-quant. These scopes can be requested through the
[Marquee Developer Site](https://marquee.gs.com/developer). Scopes are linked to your registered application. You can
create multiple applications with different scopes in order to protect your processes. For example, your trading
application may require the `execute_trades` scope, but you wouldn't need other applications which only read data to
have these elevated permissions. More information on the different scopes is available
[here](https://marquee.gs.com/s/developer/docs/guides/scopes).

To initialize a session with the default set of scopes:

```python
from gs_quant.session import GsSession

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

scopes = GsSession.Scopes.get_default()

GsSession.use(client_id=client_id, client_secret=client_secret, scopes=scopes)
```

To initialize a session with the a specific set of scopes:

```python
from gs_quant.session import GsSession

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

scopes = [
    GsSession.Scopes.MODIFY_FINANCIAL_DATA,
    GsSession.Scopes.READ_FINANCIAL_DATA
]

GsSession.use(client_id=client_id, client_secret=client_secret, scopes=scopes)
```

## Environments

Developers can access different environments using the provided constants. Production environments should be used for
all GS-Quant access except where testing workflows prior to deployment (e.g. testing trading integration).

```python
from gs_quant.session import Environment

GsSession.use(environment_or_domain=Environment.QA, client_id=client_id, client_secret=client_secret, scopes=scopes)
```
