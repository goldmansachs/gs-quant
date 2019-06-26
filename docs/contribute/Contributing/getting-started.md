---
title: Getting Started
excerpt: How to contribute to GS Quant
datePublished: 2019/06/19
keywords:
  - Contribute
  - Getting Started
---

<note>GS employees should follow <a href='http://go.gs.com/3ca779b8'>this</a> guide instead</note>

## Prerequisites

- [GitHub account](https://guides.github.com/activities/hello-world/)
- Python 3.6 or higher installed
- Any Python IDE. We use [PyCharm](https://www.jetbrains.com/pycharm/)
- Marquee API Credentials by [registering an app](https://marquee.gs.com/s/developer/myapps) (optional)
- [GitHub SSH configured for your account](https://help.github.com/en/articles/connecting-to-github-with-ssh)

## Configuring a Working Copy of GS Quant

You will need to have the project running locally:

1. Visit our [GitHub Repo](https://github.com/goldmansachs/gs-quant) and press the "fork" button. By doing so, a copy of the project will be created in your own GitHub repository.

2. Clone the repository. Find the "Clone or Download" button and copy the SSH URL to clone the repository locally. e.g.:

   ```bash
   git clone git@github.com:YOUR_GITHUB_USERNAME/gs-quant.git
   ```

3. Change into the project directory

   ```bash
   cd gs-quant
   ```

4. Setup a new remote that points to the original project so you can receive any new changes and merge them to your local project. First, go to the [GS Quant GitHub Repo](https://github.com/goldmansachs/gs-quant) and copy the SSH URL. Then add the remote upstream:

   ```bash
   git remote add upstream
   ```

   By now you will have two remotes for GS Quant.

   - `origin` which points to the forked project in your GitHub account, you have read and write access to this project.
   - `upstream` which points to the main GS Quant project. You only have read access to the main project.

## Running the Project

Now that you have a local version of the project, you can open it in your preferred Python IDE. Then, you should:

1. [Create a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
2. [Activate your environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
3. Install the project in develop mode. Make sure you are at the root of the project and then:
   ```bash
   pip install -e .[develop]
   ```
4. Run some code:

```python
import datetime
import numpy as np
import pandas as pd

from gs_quant.timeseries import volatility, generate_series

# calculate vol for a time series
series = generate_series(100)
vol = volatility(series, 252)
```

5. (optional) Test API access by replacing `CLIENT_ID` and `CLIENT_SECRET` with your own Marquee app ID and secret:

```python
import datetime
from gs_quant.data import Dataset
from gs_quant.session import Environment, GsSession


with GsSession.get(Environment.PROD, < client_id >, < client_secret >, scopes=('read_product_data', 'run_analytics')):
    weather = Dataset('WEATHER')
    df = weather.get_data(datetime.date(2016, 1, 15), datetime.date(2016, 1, 16), city=['Boston', 'Austin'])
```

## Contribute

Please follow the guidelines on how to contribute found at the root of the project in the
[CONTRIBUTING.MD](https://github.com/goldmansachs/gs-quant/blob/master/CONTRIBUTING.md) file.
