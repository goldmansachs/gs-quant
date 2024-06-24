"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import builtins
import copy
import datetime as dt
import logging
import sys
import typing
from abc import ABC, ABCMeta, abstractmethod
from collections import namedtuple
from dataclasses import Field, InitVar, MISSING, dataclass, field, fields, replace
from enum import EnumMeta, Enum
from functools import update_wrapper
from typing import Iterable, Mapping, Optional, Union, Tuple

import numpy as np
from dataclasses_json import config, global_config, LetterCase, dataclass_json
from dataclasses_json.core import _decode_generic, _is_supported_generic
from inflection import camelize, underscore

from gs_quant.context_base import ContextBase, ContextMeta
from gs_quant.json_convertors import encode_date_or_str, decode_date_or_str, decode_optional_date, encode_datetime, \
    decode_datetime, decode_float_or_str, decode_instrument, encode_dictable, decode_quote_report, decode_quote_reports, \
    decode_custom_comment, decode_custom_comments, decode_optional_time, encode_optional_time

_logger = logging.getLogger(__name__)

__builtins = set(dir(builtins))
__getattribute__ = object.__getattribute__
__setattr__ = object.__setattr__

_rename_cache = {}
_is_supported_generic_cache = {}


def exclude_none(o):
    return o is None


def exclude_always(_o):
    return True


def is_iterable(o, t):
    return isinstance(o, Iterable) and all(isinstance(it, t) for it in o)


def is_instance_or_iterable(o, t):
    return isinstance(o, t) or is_iterable(o, t)


def _get_underscore(arg):
    if arg not in _rename_cache:
        _rename_cache[arg] = underscore(arg)

    return _rename_cache[arg]


def _get_is_supported_generic(arg):
    if arg in _is_supported_generic_cache:
        is_supported_generic = _is_supported_generic_cache[arg]
    else:
        is_supported_generic = _is_supported_generic(arg)
        _is_supported_generic_cache[arg] = is_supported_generic
    return is_supported_generic


def handle_camel_case_args(cls):
    init = cls.__init__

    def wrapper(self, *args, **kwargs):
        normalised_kwargs = {}

        for arg, value in kwargs.items():
            if not arg.isupper():
                snake_case_arg = _get_underscore(arg)
                if snake_case_arg != arg and snake_case_arg in kwargs:
                    raise ValueError('{} and {} both specified'.format(arg, snake_case_arg))

                arg = snake_case_arg

            arg = cls._field_mappings().get(arg, arg)
            normalised_kwargs[arg] = value

        return init(self, *args, **normalised_kwargs)

    cls.__init__ = update_wrapper(wrapper=wrapper, wrapped=init)

    return cls


def static_field(val):
    return field(init=False, default=val)


field_metadata = config(exclude=exclude_none)
name_metadata = config(exclude=exclude_always)


class RiskKey(namedtuple('RiskKey', ('provider', 'date', 'market', 'params', 'scenario', 'risk_measure'))):

    @property
    def ex_measure(self):
        from gs_quant.target.common import RiskRequestParameters
        return RiskKey(self.provider, self.date, self.market,
                       RiskRequestParameters(self.params.csa_term, self.params.raw_results, False,
                                             self.params.market_behaviour),
                       self.scenario, None)

    @property
    def ex_historical_diddle(self):
        from gs_quant.target.common import RiskRequestParameters
        return RiskKey(self.provider, self.date, self.market,
                       RiskRequestParameters(self.params.csa_term, self.params.raw_results, False,
                                             self.params.market_behaviour),
                       self.scenario, self.risk_measure)

    @property
    def fields(self):
        return self._fields


class EnumBase:

    @classmethod
    def _missing_(cls: EnumMeta, key):
        if not isinstance(key, str):
            key = str(key)
        return next((m for m in cls.__members__.values() if m.value.lower() == key.lower()), None)

    def __reduce_ex__(self, protocol):
        return self.__class__, (self.value,)

    def __lt__(self: EnumMeta, other):
        return self.value < other.value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class HashableDict(dict):

    @staticmethod
    def hashables(in_dict) -> Tuple:
        hashables = []
        for it in in_dict.items():
            if isinstance(it[1], dict):
                hashables.append((it[0], HashableDict.hashables(it[1])))
            else:
                hashables.append(it)
        return tuple(hashables)

    def __hash__(self):
        return hash(HashableDict.hashables(self))


class DictBase(HashableDict):
    _PROPERTIES = set()

    def __init__(self, *args, **kwargs):
        if self._PROPERTIES:
            invalid_arg = next((k for k in kwargs.keys() if k not in self._PROPERTIES), None)
            if invalid_arg is not None:
                raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{invalid_arg}'")

        super().__init__(*args, **{camelize(k, uppercase_first_letter=False): v for k, v in kwargs.items()
                                   if v is not None})

    def __getitem__(self, item):
        return super().__getitem__(camelize(item, uppercase_first_letter=False))

    def __setitem__(self, key, value):
        if value is not None:
            return super().__setitem__(camelize(key, uppercase_first_letter=False), value)

    def __getattr__(self, item):
        if self._PROPERTIES:
            if _get_underscore(item) in self._PROPERTIES:
                return self.get(item)
        elif item in self:
            return self[item]

        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in dir(self):
            return super().__setattr__(key, value)
        elif self._PROPERTIES and _get_underscore(key) not in self._PROPERTIES:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")

        self[key] = value

    @classmethod
    def properties(cls) -> set:
        return cls._PROPERTIES


class Base(ABC):
    """The base class for all generated classes"""

    __fields_by_name = None
    __field_mappings = None

    def __getattr__(self, item):
        fields_by_name = __getattribute__(self, '_fields_by_name')()

        if item.startswith('_') or item in fields_by_name:
            return __getattribute__(self, item)

        # Handle setting via camelCase names (legacy behaviour) and field mappings from disallowed names
        snake_case_item = _get_underscore(item)
        field_mappings = __getattribute__(self, '_field_mappings')()
        snake_case_item = field_mappings.get(snake_case_item, snake_case_item)

        try:
            return __getattribute__(self, snake_case_item)
        except AttributeError:
            return __getattribute__(self, item)

    def __setattr__(self, key, value):
        # Handle setting via camelCase names (legacy behaviour)
        snake_case_key = _get_underscore(key)
        snake_case_key = self._field_mappings().get(snake_case_key, snake_case_key)
        fld = self._fields_by_name().get(snake_case_key)

        if fld:
            if not fld.init:
                raise ValueError(f'{key} cannot be set')

            key = snake_case_key
            value = self.__coerce_value(fld.type, value)

        __setattr__(self, key, value)

    def __repr__(self):
        if self.name is not None:
            return f'{self.name} ({self.__class__.__name__})'

        return super().__repr__()

    @classmethod
    def __is_type_match(cls, tp, val):
        if sys.version_info >= (3, 9):
            from types import GenericAlias
            is_generic_alias = isinstance(tp, (typing._GenericAlias, GenericAlias))
        else:
            is_generic_alias = isinstance(tp, typing._GenericAlias)
        if not is_generic_alias:
            # Do not convert Enums to strings
            is_enum_to_str = isinstance(val, Enum) and tp == str
            return isinstance(tp, type) and (isinstance(val, tp) or is_enum_to_str)
        if getattr(tp, '_special', False):
            return False
        origin = tp.__origin__
        args = tp.__args__
        if float in args:
            args += (int,)
        if origin == Union:
            return any(cls.__is_type_match(arg, val) for arg in args)
        if origin == tuple:
            if not isinstance(val, tuple) or not args:
                return False
            if len(args) == 1 or args[1] == Ellipsis:
                return all(cls.__is_type_match(args[0], x) for x in val)
            else:
                return len(args) == len(val) and all(cls.__is_type_match(arg, x) for arg, x in zip(args, val))
        return False

    @classmethod
    def __coerce_value(cls, typ: type, value):
        if cls.__is_type_match(typ, value):
            return value
        if isinstance(value, np.generic):
            # Handle numpy types
            return value.item()
        elif hasattr(value, 'tolist'):
            # tolist converts scalar or array to native python type if not already native.
            return value.tolist()
        elif typ in (DictBase, Optional[DictBase]) and isinstance(value, Base):
            return value.to_dict()
        is_supported_generic = _get_is_supported_generic(typ)
        if is_supported_generic:
            return _decode_generic(typ, value, False)
        else:
            return value

    @classmethod
    def _fields_by_name(cls) -> Mapping[str, Field]:
        if cls is Base:
            return {}

        if cls.__fields_by_name is None:
            cls.__fields_by_name = {f.name: f for f in fields(cls)}

        return cls.__fields_by_name

    @classmethod
    def _field_mappings(cls) -> Mapping[str, str]:
        if cls is Base:
            return {}

        if cls.__field_mappings is None:
            field_mappings = {}
            for fld in fields(cls):
                config_fn = fld.metadata.get('dataclasses_json', {}).get('letter_case')
                if config_fn:
                    mapped_name = config_fn('field_name')
                    if mapped_name:
                        field_mappings[mapped_name] = fld.name

            cls.__field_mappings = field_mappings
        return cls.__field_mappings

    def clone(self, **kwargs):
        """
            Clone this object, overriding specified values

            :param kwargs: property names and values, e.g. swap.clone(fixed_rate=0.01)

            **Examples**

            To change the market data location of the default context:

            >>> from gs_quant.instrument import IRCap
            >>> cap = IRCap('5y', 'GBP')
            >>>
            >>> new_cap = cap.clone(cap_rate=0.01)
        """
        return replace(self, **kwargs)

    @classmethod
    def properties(cls) -> set:
        """The public property names of this class"""
        return set(f[:-1] if f[-1] == '_' else f for f in cls._fields_by_name().keys())

    @classmethod
    def properties_init(cls) -> set:
        """The public property names of this class"""
        return set(f[:-1] if f[-1] == '_' else f for f, v in cls._fields_by_name().items() if v.init)

    def as_dict(self, as_camel_case: bool = False) -> dict:
        """Dictionary of the public, non-null properties and values"""

        # to_dict() converts all the values to JSON type, does camel case and name mappings
        # asdict() does not convert values or case of the keys or do name mappings

        ret = {}
        field_mappings = {v: k for k, v in self._field_mappings().items()}

        for key in self.__fields_by_name.keys():
            value = __getattribute__(self, key)
            key = field_mappings.get(key, key)

            if value is not None:
                if as_camel_case:
                    key = camelize(key, uppercase_first_letter=False)

                ret[key] = value

        return ret

    @classmethod
    def default_instance(cls):
        """
        Construct a default instance of this type
        """
        required = {f.name: None if f.default == MISSING else f.default for f in fields(cls) if f.init}
        return cls(**required)

    def from_instance(self, instance):
        """
        Copy the values from an existing instance of the same type to our self
        :param instance: from which to copy:
        :return:
        """
        if not isinstance(instance, type(self)):
            raise ValueError('Can only use from_instance with an object of the same type')

        for fld in fields(self.__class__):
            if fld.init:
                __setattr__(self, fld.name, __getattribute__(instance, fld.name))


@dataclass_json
@dataclass
class Priceable(Base):

    def resolve(self, in_place: bool = True):
        """
        Resolve non-supplied properties of an instrument

        **Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'USD')
        >>> rate = swap.fixedRate

        rate is None

        >>> swap.resolve()
        >>> rate = swap.fixedRate

        rates is now the solved fixed rate
        """
        raise NotImplementedError

    def dollar_price(self):
        """
        Present value in USD

        :return:  a float or a future, depending on whether the current PricingContext is async, or has been entered

        **Examples**

        >>> from gs_quant.instrument import IRCap
        >>>
        >>> cap = IRCap('1y', 'EUR')
        >>> price = cap.dollar_price()

        price is the present value in USD (a float)

        >>> cap_usd = IRCap('1y', 'USD')
        >>> cap_eur = IRCap('1y', 'EUR')
        >>>
        >>> from gs_quant.markets import PricingContext
        >>>
        >>> with PricingContext():
        >>>     price_usd_f = cap_usd.dollar_price()
        >>>     price_eur_f = cap_eur.dollar_price()
        >>>
        >>> price_usd = price_usd_f.result()
        >>> price_eur = price_eur_f.result()

        price_usd_f and price_eur_f are futures, price_usd and price_eur are floats
        """
        raise NotImplementedError

    def price(self):
        """
        Present value in local currency. Note that this is not yet supported on all instruments

        ***Examples**

        >>> from gs_quant.instrument import IRSwap
        >>>
        >>> swap = IRSwap('Pay', '10y', 'EUR')
        >>> price = swap.price()

        price is the present value in EUR (a float)
        """
        raise NotImplementedError

    def calc(self, risk_measure, fn=None):
        """
        Calculate the value of the risk_measure

        :param risk_measure: the risk measure to compute, e.g. IRDelta (from gs_quant.risk)
        :param fn: a function for post-processing results
        :return: a float or dataframe, depending on whether the value is scalar or structured, or a future thereof
        (depending on how PricingContext is being used)

        **Examples**

        >>> from gs_quant.instrument import IRCap
        >>> from gs_quant.risk import IRDelta
        >>>
        >>> cap = IRCap('1y', 'USD')
        >>> delta = cap.calc(IRDelta)

        delta is a dataframe

        >>> from gs_quant.instrument import EqOption
        >>> from gs_quant.risk import EqDelta
        >>>
        >>> option = EqOption('.SPX', '3m', 'ATMF', 'Call', 'European')
        >>> delta = option.calc(EqDelta)

        delta is a float

        >>> from gs_quant.markets import PricingContext
        >>>
        >>> cap_usd = IRCap('1y', 'USD')
        >>> cap_eur = IRCap('1y', 'EUR')

        >>> with PricingContext():
        >>>     usd_delta_f = cap_usd.calc(IRDelta)
        >>>     eur_delta_f = cap_eur.calc(IRDelta)
        >>>
        >>> usd_delta = usd_delta_f.result()
        >>> eur_delta = eur_delta_f.result()

        usd_delta_f and eur_delta_f are futures, usd_delta and eur_delta are dataframes
        """
        raise NotImplementedError


class __ScenarioMeta(ABCMeta, ContextMeta):
    pass


@dataclass
class Scenario(Base, ContextBase, ABC, metaclass=__ScenarioMeta):
    def __lt__(self, other):
        if self.__repr__ != other.__repr__:
            return self.name < other.name
        return False

    def __repr__(self):
        if self.name:
            return self.name
        else:
            params = self.as_dict()
            sorted_keys = sorted(params.keys(), key=lambda x: x.lower())
            params = ', '.join(
                [f'{k}:{params[k].__repr__ if isinstance(params[k], Base) else params[k]}' for k in sorted_keys])
            return self.scenario_type + '(' + params + ')'


@dataclass
class RiskMeasureParameter(Base, ABC):
    pass


@dataclass
class InstrumentBase(Base, ABC):
    quantity_: InitVar[float] = field(default=1, init=False)

    @property
    @abstractmethod
    def provider(self):
        ...

    @property
    def instrument_quantity(self) -> float:
        return self.quantity_

    @property
    def resolution_key(self) -> Optional[RiskKey]:
        try:
            return self.__resolution_key
        except AttributeError:
            return None

    @property
    def unresolved(self):
        try:
            return self.__unresolved
        except AttributeError:
            return None

    @property
    def metadata(self):
        try:
            return self.__metadata
        except AttributeError:
            return None

    @metadata.setter
    def metadata(self, value):
        self.__metadata = value

    def from_instance(self, instance):
        self.__resolution_key = None
        super().from_instance(instance)
        self.__unresolved = instance.__unresolved
        self.__resolution_key = instance.__resolution_key

    def resolved(self, values: dict, resolution_key: RiskKey):
        all_values = self.as_dict(True)
        all_values.update(values)
        new_instrument = self.from_dict(all_values)
        new_instrument.name = self.name
        new_instrument.__unresolved = copy.copy(self)
        new_instrument.__resolution_key = resolution_key
        return new_instrument

    def clone(self, **kwargs):
        new_instrument = super().clone(**kwargs)
        new_instrument.__unresolved = self.unresolved
        new_instrument.metadata = self.metadata
        new_instrument.__resolution_key = self.resolution_key
        return new_instrument


@dataclass
class Market(ABC):

    def __hash__(self):
        return hash(self.market or self.location)

    def __eq__(self, other):
        return (self.market or self.location) == (other.market or other.location)

    def __lt__(self, other):
        return repr(self) < repr(other)

    @property
    @abstractmethod
    def market(self):
        ...

    @property
    @abstractmethod
    def location(self):
        ...

    def to_dict(self):
        return self.market.to_dict()


class Sentinel:

    def __init__(self, name: str):
        self.__name = name

    def __eq__(self, other):
        return self.__name == other.__name


@dataclass
class QuoteReport(Base, ABC):
    pass


@dataclass
class CustomComments(Base, ABC):
    pass


def get_enum_value(enum_type: EnumMeta, value: Union[EnumBase, str]):
    if value in (None,):
        return None

    if isinstance(value, enum_type):
        return value

    try:
        enum_value = enum_type(value)
    except ValueError:
        _logger.warning('Setting value to {}, which is not a valid entry in {}'.format(value, enum_type))
        enum_value = value

    return enum_value


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class MarketDataScenario(Base):
    scenario: Scenario = field(default=None, metadata=field_metadata)
    subtract_base: Optional[bool] = field(default=False, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


# Yes, I know this is a little evil ...
global_config.encoders[dt.date] = dt.date.isoformat
global_config.encoders[Optional[dt.date]] = encode_date_or_str
global_config.decoders[dt.date] = decode_optional_date
global_config.decoders[Optional[dt.date]] = decode_optional_date
global_config.encoders[Union[dt.date, str]] = encode_date_or_str
global_config.encoders[Optional[Union[dt.date, str]]] = encode_date_or_str
global_config.decoders[Union[dt.date, str]] = decode_date_or_str
global_config.decoders[Optional[Union[dt.date, str]]] = decode_date_or_str
global_config.encoders[dt.time] = dt.time.isoformat
global_config.decoders[dt.time] = dt.time.fromisoformat
global_config.encoders[Optional[dt.time]] = encode_optional_time
global_config.decoders[Optional[dt.time]] = decode_optional_time
global_config.encoders[dt.datetime] = encode_datetime
global_config.encoders[Optional[dt.datetime]] = encode_datetime
global_config.decoders[dt.datetime] = decode_datetime
global_config.decoders[Optional[dt.datetime]] = decode_datetime
global_config.decoders[Union[float, str]] = decode_float_or_str
global_config.decoders[Optional[Union[float, str]]] = decode_float_or_str

global_config.decoders[InstrumentBase] = decode_instrument
global_config.decoders[Optional[InstrumentBase]] = decode_instrument
global_config.decoders[QuoteReport] = decode_quote_report
global_config.decoders[Optional[Tuple[QuoteReport, ...]]] = decode_quote_reports
global_config.decoders[CustomComments] = decode_custom_comment
global_config.decoders[Optional[Tuple[CustomComments, ...]]] = decode_custom_comments
global_config.encoders[Market] = encode_dictable
global_config.encoders[Optional[Market]] = encode_dictable
