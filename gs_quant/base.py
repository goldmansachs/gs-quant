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
import itertools
import keyword
import logging
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from enum import EnumMeta
from functools import wraps
from inspect import signature, Parameter
import re
from typing import Iterable, Optional, Union, get_type_hints

import inflection
from dateutil.parser import isoparse
import numpy as np

from gs_quant.context_base import ContextBase, ContextMeta, do_not_serialise

_logger = logging.getLogger(__name__)

_valid_date_formats = ('%Y-%m-%d',  # '2020-07-28'
                       '%d%b%y',    # '28Jul20'
                       '%d-%b-%y',  # '28-Jul-20'
                       '%d/%m/%Y')  # '28/07/2020

__builtins = set(dir(builtins))
__iskeyword = keyword.iskeyword
__getattribute__ = object.__getattribute__
__setattr__ = object.__setattr__
_underscore = inflection.underscore


def is_iterable(o, t):
    return isinstance(o, Iterable) and all(isinstance(it, t) for it in o)


def is_instance_or_iterable(o, t):
    return isinstance(o, t) or is_iterable(o, t)


def camel_case_translate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        normalised_kwargs = {}
        for arg, value in kwargs.items():
            if arg in __builtins or __iskeyword(arg):
                arg += '_'

            if not arg.isupper():
                snake_case_arg = _underscore(arg)
                if snake_case_arg != arg:
                    if snake_case_arg in kwargs:
                        raise ValueError('{} and {} both specified'.format(arg, snake_case_arg))

                    normalised_kwargs[snake_case_arg] = value
                else:
                    normalised_kwargs[arg] = value
            else:
                normalised_kwargs[arg] = value

        return f(*args, **normalised_kwargs)

    return wrapper


def do_not_resolve(func):
    func.do_not_resolve = True
    return func


class RiskKey(namedtuple('RiskKey', ('provider', 'date', 'market', 'params', 'scenario', 'risk_measure'))):

    @property
    def ex_measure(self):
        return RiskKey(self.provider, self.date, self.market, self.params, self.scenario, None)

    @property
    def fields(self):
        return self._fields


class EnumBase:

    @classmethod
    def _missing_(cls: EnumMeta, key):
        return next((m for m in cls.__members__.values() if m.value.lower() == key.lower()), None)

    def __reduce_ex__(self, protocol):
        return self.__class__, (self.value,)

    def __lt__(self: EnumMeta, other):
        return self.value < other.value

    def __repr__(self):
        return self.value


class Base(metaclass=ABCMeta):
    """The base class for all generated classes"""

    __properties = set()

    def __init__(self, **kwargs):
        self.__calced_hash: Optional[int] = None
        self.__as_dict = {False: {}, True: {}}

        try:
            self.name: Optional[str] = None
        except AttributeError:
            # Regrettably, read-only properties called name exist
            pass

    def __getattr__(self, item):
        properties = __getattribute__(self, 'properties')()

        if item.startswith('_') or item == 'name' or item in properties:
            return __getattribute__(self, item)

        snake_case_item = _underscore(item)
        if snake_case_item in properties:
            return __getattribute__(self, snake_case_item)
        else:
            return __getattribute__(self, item)

    def __setattr__(self, key, value):
        properties = __getattribute__(self, 'properties')()

        # tolist converts scalar or array to native python type if not already native.
        value = getattr(value, "tolist", lambda: value)()

        if key.startswith('_') or key == 'name' or key in properties:
            return __setattr__(self, key, value)

        snake_case_key = inflection.underscore(key)

        if snake_case_key in properties:
            return __setattr__(self, snake_case_key, value)
        else:
            return __setattr__(self, key, value)

    def __repr__(self):
        if self.name is not None:
            return '{} ({})'.format(self.name, self.__class__.__name__)

        return super().__repr__()

    def _property_changed(self, prop: str):
        self.__calced_hash = None
        self.__as_dict = {False: {}, True: {}}

    @property
    def _hash_is_calced(self) -> bool:
        return self.__calced_hash is not None

    def __hash__(self) -> int:
        if not self._hash_is_calced:
            calced_hash = hash(self.name)
            for prop in self.properties():
                value = __getattribute__(self, prop)
                if isinstance(value, dict):
                    value = tuple(value.items())
                elif isinstance(value, list):
                    value = tuple(value)
                calced_hash ^= hash(value)

            self.__calced_hash = calced_hash

        return self.__calced_hash

    def __eq__(self, other) -> bool:
        return \
            type(self) == type(other) and (self.name is None or other.name is None or self.name == other.name) and \
            (self.__calced_hash is None or other.__calced_hash is None or self.__calced_hash == other.__calced_hash) \
            and all(__getattribute__(self, p) == __getattribute__(other, p) for p in self.properties())

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return type(self).__name__ < type(other).__name__

        for prop in itertools.chain(('name',), sorted(self.properties())):
            val = __getattribute__(self, prop)
            other_val = __getattribute__(other, prop)

            if val != other_val:
                if val is None:
                    return False
                return val < other_val

        return False

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
        clone = copy.copy(self)
        properties = self.properties()
        for key, value in kwargs.items():
            if key in properties:
                setattr(clone, key, value)
            else:
                raise ValueError('Only properties may be passed as kwargs')

        return clone

    @classmethod
    def properties(cls) -> set:
        """The public property names of this class"""
        if not cls.__properties:
            cls.__properties = set(i for i in dir(cls) if isinstance(getattr(cls, i), property)
                                   and not i.startswith('_') and not
                                   getattr(getattr(cls, i).fget, 'do_not_serialise', False))
        return cls.__properties

    def as_dict(self, as_camel_case: bool = False) -> dict:
        """Dictionary of the public, non-null properties and values"""
        name_mappings = getattr(self, '_name_mappings', {})

        if not self.__as_dict[as_camel_case]:
            raw_properties = self.properties()
            properties = (name_mappings[p] if p in name_mappings else
                          inflection.camelize(p, uppercase_first_letter=False) for p in raw_properties) \
                if as_camel_case else raw_properties
            values = (__getattribute__(self, p) for p in raw_properties)
            self.__as_dict[as_camel_case] = dict((p, v) for p, v in zip(properties, values) if v is not None)

        return copy.copy(self.__as_dict[as_camel_case])

    @classmethod
    def prop_type(cls, prop: str, additional: Optional[list] = None) -> type:
        return_hints = get_type_hints(getattr(cls, prop).fget).get('return')
        if hasattr(return_hints, '__origin__'):
            prop_type = return_hints.__origin__
        else:
            prop_type = return_hints

        if prop_type == Union:
            prop_type = next((a for a in return_hints.__args__ if issubclass(a, (Base, EnumBase))), None)
            if prop_type is None:
                for typ in (dt.datetime, dt.date):
                    if typ in return_hints.__args__:
                        prop_type = typ

                        if additional is not None:
                            additional.extend([a for a in return_hints.__args__ if a != prop_type])
                        break

            if prop_type is None and additional is not None:
                prop_type = return_hints.__args__[-1]
                additional.extend(return_hints.__args__[:-1])

        if prop_type is InstrumentBase:
            # TODO Fix this
            from .instrument import Instrument
            prop_type = Instrument

        return prop_type

    @classmethod
    def prop_item_type(cls, prop: str) -> type:
        return_hints = get_type_hints(getattr(cls, prop).fget).get('return')
        item_type = return_hints.__args__[0]

        item_args = [i for i in getattr(item_type, '__args__', ()) if isinstance(i, type)]
        if item_args:
            item_type = next((a for a in item_args if issubclass(a, (Base, EnumBase))), item_args[-1])

        return item_type

    def __from_dict(self, values: dict):
        name_mappings = getattr(self, '_name_mappings', {})

        for prop in self.properties():
            if getattr(type(self), prop).fset is None:
                continue

            prop_value = values.get(name_mappings.get(prop, prop),
                                    values.get(inflection.camelize(prop, uppercase_first_letter=False)))

            if prop_value is not None:
                if isinstance(prop_value, np.generic):
                    prop_value = prop_value.item()

                additional_types = []
                prop_type = self.prop_type(prop, additional=additional_types)

                if prop_type is None:
                    # This shouldn't happen
                    setattr(self, prop, prop_value)
                elif issubclass(prop_type, dt.datetime):
                    if isinstance(prop_value, int):
                        setattr(self, prop, dt.datetime.fromtimestamp(prop_value / 1000).isoformat())
                    else:
                        import re
                        matcher = re.search('\\.([0-9]*)Z$', prop_value)
                        if matcher:
                            sub_seconds = matcher.group(1)
                            if len(sub_seconds) > 6:
                                prop_value = re.sub(matcher.re, '.{}Z'.format(sub_seconds[:6]), prop_value)

                        try:
                            setattr(self, prop, isoparse(prop_value))
                        except ValueError:
                            if str in additional_types:
                                setattr(self, prop, prop_value)
                elif issubclass(prop_type, dt.date) and type(prop_value) is not dt.date:
                    date_value = None

                    if isinstance(prop_value, float):
                        # Assume it's an Excel date
                        if prop_value > 59:
                            prop_value -= 1  # Excel leap year bug, 1900 is not a leap year!
                        date_value = dt.datetime(1899, 12, 31) + dt.timedelta(days=prop_value).date()
                    elif isinstance(prop_value, str):
                        for format in _valid_date_formats:
                            try:
                                date_value = dt.datetime.strptime(prop_value, format).date()
                                break
                            except ValueError:
                                pass

                    setattr(self, prop, date_value or prop_value)
                elif issubclass(prop_type, float) and isinstance(prop_value, str):
                    if prop_value.endswith('%'):
                        setattr(self, prop, float(prop_value[:-1]) / 100)
                    else:
                        setattr(self, prop, float(prop_value))
                elif issubclass(prop_type, EnumBase):
                    setattr(self, prop, get_enum_value(prop_type, prop_value))
                elif issubclass(prop_type, Base):
                    if isinstance(prop_value, Base):
                        setattr(self, prop, prop_value)
                    else:
                        setattr(self, prop, prop_type.from_dict(prop_value))
                elif issubclass(prop_type, (list, tuple)):
                    item_type = self.prop_item_type(prop)
                    if issubclass(item_type, Base):
                        item_values = tuple(v if isinstance(v, (Base, EnumBase)) else item_type.from_dict(v)
                                            for v in prop_value)
                    elif issubclass(item_type, EnumBase):
                        item_values = tuple(get_enum_value(item_type, v) for v in prop_value)
                    else:
                        item_values = tuple(prop_value)
                    setattr(self, prop, item_values)
                else:
                    setattr(self, prop, prop_value)

    @classmethod
    def _from_dict(cls, values: dict):
        args = [k for k, v in signature(cls.__init__).parameters.items() if k not in ('kwargs', '_kwargs')
                and v.default == Parameter.empty][1:]
        required = {}

        for arg in args:
            prop_name = arg[:-1] if arg.endswith('_') and not keyword.iskeyword(arg) else arg
            prop_type = cls.prop_type(prop_name)
            value = values.pop(arg, None)

            if prop_type:
                if issubclass(prop_type, Base) and isinstance(value, dict):
                    value = prop_type.from_dict(value)
                elif issubclass(prop_type, (list, tuple)) and isinstance(value, (list, tuple)):
                    item_type = cls.prop_item_type(prop_name)
                    if issubclass(item_type, Base):
                        value = tuple(v if isinstance(v, (Base, EnumBase)) else item_type.from_dict(v) for v in value)
                elif issubclass(prop_type, EnumBase):
                    value = get_enum_value(prop_type, value)

            required[arg] = value

        instance = cls(**required)
        instance.__from_dict(values)
        return instance

    @classmethod
    def from_dict(cls, values: dict):
        """
        Construct an instance of this type from a dictionary

        :param values: a dictionary (potentially nested)
        :return: an instance of this type, populated with values
        """
        return cls._from_dict(values)

    @classmethod
    def default_instance(cls):
        """
        Construct a default instance of this type
        """
        args = [k for k, v in signature(cls.__init__).parameters.items() if v.default == Parameter.empty][1:]
        required = {a: None for a in args}
        return cls(**required)

    def from_instance(self, instance):
        """
        Copy the values from an existing instance of the same type to our self
        :param instance: from which to copy:
        :return:
        """
        if not isinstance(instance, type(self)):
            raise ValueError('Can only use from_instance with an object of the same type')

        for prop in self.properties():
            attr = getattr(__getattribute__(self, '__class__'), prop)
            if attr.fset:
                __setattr__(self, prop, __getattribute__(instance, prop))

    def to_json(self) -> dict:
        return {re.sub('_$', '', k): v for k, v in self.as_dict(as_camel_case=True).items()}


class TypeMixin(metaclass=ABCMeta):

    @property
    @abstractmethod
    def _type(self) -> str:
        ...

    def to_json(self) -> dict:
        ret = super().to_json()
        ret['$type'] = self._type
        return ret


class TypedBase(TypeMixin, Base):
    pass


class Priceable(Base, metaclass=ABCMeta):

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


class Scenario(Base, ContextBase, metaclass=__ScenarioMeta):
    pass


class InstrumentBase(Base):

    def __init__(self, quantity: Optional[float] = 1):
        super().__init__()
        self.__instrument_quantity = quantity
        self.__resolution_key: Optional[RiskKey] = None
        self.__unresolved: Optional[InstrumentBase] = None

    @property
    @abstractmethod
    @do_not_serialise
    def provider(self):
        ...

    @property
    @do_not_serialise
    def instrument_quantity(self) -> float:
        return self.__instrument_quantity

    @property
    @do_not_serialise
    def resolution_key(self) -> RiskKey:
        return self.__resolution_key

    @property
    @do_not_serialise
    def unresolved(self):
        return self.__unresolved

    def _property_changed(self, prop: str):
        if self.__resolution_key:
            self.__resolution_key = None
            self.unresolve()

        super()._property_changed(prop)

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

    def unresolve(self):
        if self.__resolution_key and self.__unresolved:
            self.from_instance(self.__unresolved)
            self.__resolution_key = None
            self.__unresolved = None


class QuotableBuilder(TypeMixin):

    def __init__(self, valuation_overrides: Optional[dict] = None):
        super().__init__()
        self.valuation_overrides = valuation_overrides

    @property
    @do_not_resolve
    @do_not_serialise
    def valuation_overrides(self) -> Optional[dict]:
        return self.__valuation_overrides

    @valuation_overrides.setter
    def valuation_overrides(self, value: dict):
        self.__valuation_overrides = value

    def to_json(self):
        ret = {'properties': TypeMixin.to_json(self)}
        ret['$type'] = ret['properties'].pop('$type')

        if self.__valuation_overrides:
            ret['valuationOverrides'] = self.__valuation_overrides

        return ret


class Market(Base):

    @property
    @abstractmethod
    def location(self):
        ...


class Sentinel:

    def __init__(self, name: str):
        self.__name = name

    def __eq__(self, other):
        return self.__name == other.__name


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


def as_tuple(f):
    def wrap(*args):
        value = args[1]
        if value is not None and not isinstance(value, str):
            try:
                iter(value)
            except TypeError:
                value = (value,)

        return f(args[0], value)

    return wrap
