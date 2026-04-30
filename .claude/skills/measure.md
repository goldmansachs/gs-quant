# Writing a Measure and Its Test

Guide for adding a new measure function in `gs_quant/timeseries/` and its corresponding test in `gs_quant/test/timeseries/`.

---

## 1. Create or Add to a Measure File

Place your measure in an existing `measures_*.py` file or create a new one (e.g., `measures_custom.py`).

### File Structure

```python
"""
Copyright 2020 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
...
"""

import datetime as dt
import logging
from typing import Optional, Union

import pandas as pd

from gs_quant.api.gs.data import QueryType, GsDataApi
from gs_quant.common import AssetClass, AssetType, PricingLocation
from gs_quant.data import DataContext, Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.timeseries.helper import plot_measure, check_forward_looking, _to_offset
from gs_quant.timeseries.measures import (
    _market_data_timed,
    _range_from_pricing_date,
    ExtendedSeries,
    GENERIC_DATE,
    ASSET_SPEC,
    _asset_from_spec,
)

_logger = logging.getLogger(__name__)
```

### Import Conventions (enforced by ruff)

- `import pandas as pd` — never `from pandas import ...`
- `import numpy as np`
- `import datetime as dt`
- Do NOT import from `gs_quant.target.common` — use `gs_quant.common`
- Do NOT use `pytz` — use `zoneinfo` or `datetime.timezone`
- Max line length: 120 characters

### PEP 8 Standards (mandatory)

All new measure code **must** comply with PEP 8. Key requirements:

#### Naming

- **Functions and variables:** `snake_case` (e.g., `swap_rate`, `implied_volatility_fwd`)
- **Classes and Enums:** `CamelCase` (e.g., `EventType`, `RateType`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `CENTRAL_BANK_WATCH_START_DATE`)
- **Private/internal helpers:** prefix with underscore (e.g., `_extract_series_from_df`)

#### Formatting

- **Indentation:** 4 spaces, never tabs.
- **Blank lines:** 2 blank lines before and after top-level function/class definitions; 1 blank line between methods inside a class.
- **Trailing whitespace:** none.
- **Imports:** grouped in order — stdlib → third-party → local — each group separated by a blank line. Alphabetize within each group.

#### Docstrings

- Use triple double-quotes (`"""`).
- First line is a concise summary ending with a period.
- Include `:param`, `:return:`, `**Usage**`, and `**Examples**` sections.

#### Type Annotations

- All public function parameters and return types must be annotated.
- Use `Optional[X]` for parameters that can be `None`.
- Use `Union[X, Y]` when multiple types are accepted.

#### Expressions and Statements

- Surround top-level operators with spaces: `x = 1`, `a + b`.
- No spaces inside brackets: `func(arg)`, `list[0]`.
- Use `is` / `is not` for `None` comparisons: `if x is None:`.
- Avoid bare `except:`; always catch a specific exception.
- Keep functions focused — if a function exceeds ~50 lines, consider extracting helpers.

#### Test Naming

- Test functions: `test_<function_name>` or `test_<function_name>_<scenario>`.
- Test classes (if used): `TestMyMeasure`.
- Each test should have a descriptive docstring explaining what is verified.

#### Enforcement

Run before every commit:

```bash
ruff check --fix
ruff format
```

---

### Writing the Measure Function

```python
@plot_measure((AssetClass.Rates,), (AssetType.Swap,), [QueryType.SWAP_RATE])
def my_measure(
    asset: Asset,
    tenor: str,
    pricing_date: Optional[GENERIC_DATE] = None,
    *,
    real_time: bool = False,
) -> pd.Series:
    """Short description of what this measure returns.

    :param asset: asset object loaded from security master
    :param tenor: e.g. '10y'
    :param pricing_date: specific date or relative date string
    :param real_time: whether to retrieve intraday data (default: False)
    :return: time series of the measure values

    **Usage**

    Explain what the measure does and when to use it.

    **Examples**

    >>> from gs_quant.timeseries.measures_custom import my_measure
    >>> my_measure(Asset('MA...', AssetClass.Rates, 'USD'), '10y')
    """
    # 1. Validate inputs
    if real_time:
        raise MqValueError('real-time not supported for this measure')

    # 2. Resolve the asset (if using ASSET_SPEC)
    asset = _asset_from_spec(asset)

    # 3. Build query parameters
    query_params = dict(tenor=tenor)

    # 4. Fetch data via _market_data_timed or Dataset
    q = GsDataApi.build_market_data_query([asset.get_marquee_id()], QueryType.SWAP_RATE, where=query_params)
    df = _market_data_timed(q)

    # 5. Extract and return a pd.Series
    return _extract_series_from_df(df, QueryType.SWAP_RATE, True)
```

### Key Patterns

| Pattern | Description |
|---------|-------------|
| `@plot_measure(asset_classes, asset_types, query_types)` | Decorator that registers the function in the Plot Service and handles entitlement/logging |
| `_market_data_timed(query)` | Fetches market data with timing/logging |
| `_range_from_pricing_date(exchange, pricing_date)` | Returns (start, end) date range from a pricing date |
| `check_forward_looking(...)` | Validates forward-looking date inputs |
| `ExtendedSeries` | A `pd.Series` subclass used for returning results with metadata |
| `MqValueError` | Raise for invalid user inputs |

### Registering Your Module

If you create a new file, make sure it is imported in `gs_quant/timeseries/__init__.py` so the measures are discoverable.

---

## 2. Write the Corresponding Test

Place your test in `gs_quant/test/timeseries/test_measures_custom.py` (matching the source file name).

### Test File Structure

```python
"""
Copyright 2020 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
...
"""

import datetime as dt

import pandas as pd
import pytest
from testfixtures import Replacer
from testfixtures.mock import Mock

import gs_quant.timeseries.measures_custom as tm_custom
from gs_quant.api.gs.data import MarketDataResponseFrame, QueryType
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Currency
from gs_quant.session import GsSession, Environment
from gs_quant.test.timeseries.utils import mock_request

_index = [pd.Timestamp('2021-01-04')]


def test_my_measure(mocker):
    # 1. Mock the GsSession
    replace = Replacer()
    mock_session = Mock(spec=GsSession)
    mock_session.current = mock_session
    mock_session._get = Mock()
    mock_session.domain = 'https://marquee.gs.com'
    replace('gs_quant.timeseries.measures.GsSession', mock_session)

    # 2. Build mock response data
    mock_df = MarketDataResponseFrame(
        data={'swapRate': [0.025]},
        index=_index,
    )

    # 3. Patch the data-fetching function
    mocker.patch.object(
        tm_custom,
        '_market_data_timed',
        return_value=mock_df,
    )

    # 4. Create a mock asset
    mock_asset = Currency('MA_TEST', 'USD')

    # 5. Call the measure and assert
    result = tm_custom.my_measure(mock_asset, '10y')
    assert isinstance(result, pd.Series)
    assert len(result) == 1
    assert result.iloc[0] == 0.025

    # 6. Cleanup
    replace.restore()


def test_my_measure_invalid_input():
    mock_asset = Currency('MA_TEST', 'USD')
    with pytest.raises(MqValueError):
        tm_custom.my_measure(mock_asset, '10y', real_time=True)
```

### Testing Patterns

| Pattern | When to Use |
|---------|-------------|
| `Replacer` + `Mock(spec=GsSession)` | Mock the HTTP session to avoid real API calls |
| `mocker.patch.object(module, 'func', return_value=...)` | Replace data-fetching internals |
| `MarketDataResponseFrame` | Construct fake API response DataFrames |
| `pytest.raises(MqValueError)` | Assert that invalid inputs raise proper errors |
| `mock_request` (from `utils.py`) | Helper to mock `GsSession._get` with canned JSON |

### Running Tests

```bash
# Single test file
uv run pytest gs_quant/test/timeseries/test_measures_custom.py

# Single test function
uv run pytest gs_quant/test/timeseries/test_measures_custom.py::test_my_measure

# All timeseries tests
uv run pytest gs_quant/test/timeseries/
```

---

## 3. Checklist Before Committing

- [ ] Function has `@plot_measure` decorator with correct asset classes/types
- [ ] Docstring with `:param`, `:return:`, `**Usage**`, and `**Examples**` sections
- [ ] All public parameters and return types have type annotations
- [ ] Input validation raises `MqValueError` with a clear message
- [ ] `real_time` parameter handled (raise if unsupported)
- [ ] PEP 8 naming: `snake_case` functions/variables, `CamelCase` classes, `UPPER_SNAKE_CASE` constants
- [ ] Imports ordered: stdlib → third-party → local, alphabetized within groups
- [ ] No unused imports or variables
- [ ] New module imported in `__init__.py` (if new file)
- [ ] Test covers happy path and error cases; test names are descriptive
- [ ] Run `ruff format` and `ruff check --fix` — zero warnings
- [ ] All tests pass: `uv run pytest gs_quant/test/timeseries/`
