GS Quant is a Python toolkit for quantitative finance, which provides access to an extensive set of derivatives pricing data through the Goldman Sachs Marquee developer APIs. Libraries are provided for timeseries analytics, portfolio manipulation, risk and scenario analytics and backtesting. Can be used to interact with the Marquee platform programmatically, or as a standalone software package for quantitiative analytics.

Created and maintained by quantitative developers (quants) at Goldman Sachs to enable development of trading strategies and analysis of derivative products. Can be used to facilitate derivative structuring and trading, or as statistical packages for a variety of timeseries analytics applications.

# Overview
GS Quant is a Python toolkit for quantitative finance, which provides access to an extensive set of derivatives pricing data through the Goldman Sachs Marquee developer APIs.

# Important Links
- [GS Developer](https://developer.gs.com/docs/gsquant/)
- [PyPI](https://pypi.org/project/gs-quant/)
- [gs_quant_internal](https://gitlab.gs.com/marquee/analytics/gs_quant_internal)

## Set up
- [Getting Started](https://confluence.apg.services.gs.com/display/TECHPY/Getting+started+with+Python+in+GS)
- [Git Setup](./docs/developer-setup.md)
- [Marquee Gitflow](https://gitlab.gs.com/marquee/ui-platform/sdlc/blob/develop/docs/developer-setup.md#marquee-gitflow)

### Code formatting

We are now using [ruff](https://github.com/astral-sh/ruff) for very fast code formatting. The easiest thing to do it to use the pre-commit hooks.
That way when you commit it will automatically format and fix your code.  

```bash
# If you DIDN't use uv to setup your env you might need to install ruff and pre-commit manually.
pip install ruff pre-commit
```
Installs the pre-commit hooks, this will make ruff run on every commit.
```bash
pre-commit install
```
Alternatively you can run the ruff commands locally, `check` runs lint style check for code issues and `--fix` will fix them. `format` is about the code style, whitespace etc.
```bash
ruff check --fix
ruff format
```


## Build / Test / Develop
- Install development dependencies (see extras_require in setup.py).
- Check out the project.
- Navigate to project root.
- Consider installing it in [development mode](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode).

To build distribution package:
- `python setup.py sdist`
- Package will be created in the dist/ folder.

To run tests:
- `pytest gs_quant/test`

# Contacts
- Symphony room: gs_quant
- Distribution list: gs-quant@gs.com
