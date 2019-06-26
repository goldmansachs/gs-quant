---
title: Sessions
excerpt: Understanding authentication sessions
datePublished: 2019/06/16
dateModified: 2019/06/16
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Authentication
  - Sessions
  - GsSession
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
  - name: Nick Young
    github: nick-young-gs
links:
  - title: GsSession
    url: /gsquant/guides/Authentication/2-gs-session/
---

## Understanding Sessions

Sessions can be used to manage an authentication token to external APIs. They can be used globally to set credentials
for the entire process, or as variables, to allow multiple sessions to be used within a single process.

<note>The following examples use GsSession, but the same methods apply to all Session objects.</note>

## Creating a Session

A new session can be created and initialized by running:

```python
from gs_quant.session import GsSession

session = GsSession.get()       # Get a new session
session.init()                  # Authenticate
```

The parameters required will depend on the authentication requirements of the external API. A session can be held prior
to initialization to control when the authentication request is made.
There are two ways to use a session:

- Set as global
- Use within a block

Initializing a session will authenticate against the API and hold a token which is reused automatically across
subsequent requests. This is done via the `init()` function.

## Global Sessions

Any request which is not scoped will use the global session automatically. The global session can be accessed through
`current`:

```python
session = GsSession.current     # Get current session
GsSession.current = session     # Set current session
```

The `use()` method creates, initializes and sets the session in one command:

```python
GsSession.use()      # Create and set session
```

## Scoped Sessions

Session objects can be used within blocks. This allows the same token to be shared by multiple requests within a defined
scope. It also allows multiple environments or credentials to be used within the same process:

```python
from gs_quant.session import Environment

prod_session = GsSession.get(Environment.PROD)      # Get PROD session
qa_session = GsSession.get(Environment.QA)          # Get QA session

with prod_session:

    # perform production requests

with qa_session:

    # perform non-production requests
```

## Closing Sessions

A session can be closed using the following command:

```python
session.close()
```

Behavior of the `close()` method will depend on the underlying implementation, but will generally close any open
HTTP or socket connections, as well as require re-authentication for further requests.
