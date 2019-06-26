---
title: Functions
excerpt: Writing python function documentation
datePublished: 2019/06/22
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Python
  - LaTeX
  - Sphinx
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Sphinx
    url: http://www.sphinx-doc.org/en/master/
  - title: LaTeX
    url: https://www.latex-project.org/
  - title: reStructuredText
    url: http://docutils.sourceforge.net/rst.html
---

gs-quant uses [Sphinx](http://www.sphinx-doc.org/en/master/) to generate python
[API documentation](/gsquant/api/) automatically from the source code.

## Type Hinting

Since Python 3.5, functions can use type hinting to document both parameter and return types:

```python
import pandas as pd

def abs(x: pd.Series) -> pd.Series:
    """Docstring"""

    # function code
```

Each variable can be typed through the syntax `param: type`. The `abs` function above has a parameter `x` which is
documented as type `pd.Series`, which is a pandas Series object. The `->` syntax is used to declare the return type of
the function. The `abs` function above also returns a pandas Series object.

## Docstring

Functions should use Docstrings per [PEP 257](https://www.python.org/dev/peps/pep-0257/) standard to document usage. Python
function documentation should have the following components:

- Function title
- Parameters and return type
- Usage info
- Examples
- See also

Here's an example of a doc string:

```python
def my_func(x: int) -> str:
    """
    Title / one line description

    :param x: description of parameter x
    :return: description of return value

    **Usage**

    Describe how to use the function should be used

    **Examples**

    Provide one or more examples:

    result = my_func(1)

    **See also**

    :func:`his_func` :func:`her_func`
    """
    # function code
```

## Mathematical Formulas

The gs-quant documentation supports inline LaTex within python docstrings in order to render mathematical formulae. This
can be declared using the `:math:` declaration. For example:

```python
import pandas as pd

def abs(x: pd.Series) -> pd.Series:
    """Absolute value

    :math:`R_t = |X_t|`
    """
    # function code
```

Everything inside the math block quote marks will be rendered as LaTeX-formatted math.

## Full Example

See below for an example of a fully documented function:

```python
def abs(x: pd.Series) -> pd.Series:
    """
    Absolute value of each element in series

    :param x: date-based time series of prices
    :return: date-based time series of absolute value

    **Usage**

    Return the absolute value of :math:`X`. For each value in time series :math:`X_t`, return :math:`X_t` if :math:`X_t`
    is greater than or equal to 0; otherwise return :math:`-X_t`:

    :math:`R_t = |X_t|`

    Equivalent to :math:`R_t = \sqrt{X_t^2}`

    **Examples**

    Generate price series and take absolute value of :math:`X_t-100`

    >>> prices = generate_series(100) - 100
    >>> abs_(prices)

    **See also**

    :func:`exp` :func:`sqrt`

    """
    return abs(x)
```
