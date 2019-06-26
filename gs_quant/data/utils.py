import datetime
import logging
from typing import Union

import numpy
import pandas as pd

from gs_quant.base import Base

_logger = logging.getLogger(__name__)


def _get_dict(obj):
    dict_func = getattr(obj, 'as_dict', None)
    if callable(dict_func):
        return obj.as_dict()
    else:
        return obj


def construct_dataframe_with_types(data: Union[Base, list, tuple]) -> pd.DataFrame:
    """
    Constructs a dataframe with correct date types.
    Note: datetime.datetime will be converted to a datetime64 automatically. Only datetime.date needs to be converted.
    :param data: data to convert with correct types
    :return: dataframe with correct types
    """
    if len(data) > 0:

        dl = [r if isinstance(r, dict) else _get_dict(r) for r in data]
        df = pd.DataFrame(dl)

        if isinstance(data, (list, tuple)) and isinstance(data[0], Base):
            types = [(k, data[0].prop_type(k)) for k in _get_dict(data[0]).keys()]
            for type_tuple in types:
                col_name, col_type = type_tuple
                if col_type == datetime.date:
                    df = df.astype({col_name: numpy.datetime64})
                if col_name in ['time', 'date']:
                    df = df.set_index(col_name)
        else:
            _logger.warning('Could not change types on given data.')
        return df
    else:
        return pd.DataFrame({})
