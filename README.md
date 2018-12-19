# GS Quant
See also Getting Started notebook in the gs_quant folder or package.

## Installation
```pip install gs_quant```

## Dependencies
Python 3.6 or 3.7  
Package dependencies can be installed by pip.

## Example
```python
from gs_quant import *

with AppSession('CLIENT_ID', 'CLIENT_SECRET', Environment.PROD) as session:
    # get coverage for a dataset and run a query
    coverage = session.get_coverage('WEATHER')
    df = session.get_data('WEATHER', {'city': ['Boston', 'Austin']}, '2016-02-01', '2016-02-14')
```

## Help
Questions? Comments? Write to data-services@gs.com