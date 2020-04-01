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
from abc import ABCMeta
import builtins
from collections import namedtuple
import copy
import datetime as dt
import dateutil
from enum import EnumMeta
from functools import wraps
import inflection
from inspect import signature, Parameter
import keyword
import logging
from typing import Union, get_type_hints

from gs_quant.context_base import ContextBase, ContextMeta

_logger = logging.getLogger(__name__)


def _normalise_arg(arg: str) -> str:
    if keyword.iskeyword(arg) or arg in dir(builtins):
        return arg + '_'
    else:
        return arg


def camel_case_translate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        normalised_kwargs = {}
        for arg, value in kwargs.items():
            arg = _normalise_arg(arg)

            if not arg.isupper():
                snake_case_arg = inflection.underscore(arg)
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


class PricingKey(
    namedtuple('_PricingKey', ('pricing_market_data_as_of', 'market_data_location', 'parameters', 'scenario'))
):

    def __iter__(self):
        if len(self.pricing_market_data_as_of) > 1:
            return iter(self.clone(pricing_market_data_as_of=(as_of,)) for as_of in self.pricing_market_data_as_of)
        else:
            return iter([self])

    def clone(self, **kwargs):
        dict = {f: getattr(self, f, None) for f in super()._fields}
        dict.update(kwargs)
        return PricingKey(**dict)

    def for_pricing_date(self, pricing_date: dt.date):
        as_of = next((a for a in self.pricing_market_data_as_of if a.pricing_date == pricing_date), None)
        if as_of is None:
            raise ValueError('{} not found'.format(pricing_date))

        return self.clone(pricing_market_data_as_of=(as_of,))



class EnumBase:

    @classmethod
    def _missing_(cls: EnumMeta, key):
        return next((m for m in cls.__members__.values() if m.value.lower() == key.lower()), None)


class Base(metaclass=ABCMeta):

    """The base class for all generated classes"""

    __properties = set()

    def __init__(self, **_kwargs):
        self.__calced_hash: int = None

        try:
            self.name: str = None
        except AttributeError:
            # Regrettably, read-only properties called name exist
            pass

    def __getattr__(self, item):
        snake_case_item = inflection.underscore(item)
        if snake_case_item in super().__getattribute__('properties')():
            return super().__getattribute__(snake_case_item)
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        properties = super().__getattribute__('properties')()
        snake_case_key = inflection.underscore(key)
        key_is_property = key in properties
        snake_case_key_is_property = snake_case_key in properties

        if snake_case_key_is_property and not key_is_property:
            return super().__setattr__(snake_case_key, value)
        else:
            return super().__setattr__(key, value)

    def __repr__(self):
        if self.name is not None:
            return self.name

        return super().__repr__()

    def _property_changed(self, prop: str):
        self.__calced_hash = None

    @property
    def _hash_is_calced(self) -> bool:
        return self.__calced_hash is not None

    def __hash__(self) -> int:
        if not self._hash_is_calced:
            calced_hash = hash(self.name)
            for prop in self.properties():
                calced_hash ^= hash(super().__getattribute__(prop))

            self.__calced_hash = calced_hash

        return self.__calced_hash

    def __eq__(self, other) -> bool:
        return\
            type(self) == type(other) and self.name == other.name and\
            (self.__calced_hash is None or other.__calced_hash is None or self.__calced_hash == other.__calced_hash) \
            and all(super(Base, self).__getattribute__(p) == super(Base, other).__getattribute__(p)
                    for p in self.properties())

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

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

    def as_dict(self, as_camel_case: bool=False) -> dict:
        """Dictionary of the public, non-null properties and values"""
        raw_properties = self.properties()
        properties = (inflection.camelize(p, uppercase_first_letter=False) for p in raw_properties) \
            if as_camel_case else raw_properties
        values = (super(Base, self).__getattribute__(p) for p in raw_properties)
        return dict((p, v) for p, v in zip(properties, values) if v is not None)

    @classmethod
    def prop_type(cls, prop: str) -> type:
        return_hints = get_type_hints(getattr(cls, prop).fget).get('return')
        if hasattr(return_hints, '__origin__'):
            prop_type = return_hints.__origin__
        else:
            prop_type = return_hints

        if prop_type == Union:
            prop_type = next((a for a in return_hints.__args__ if issubclass(a, (Base, EnumBase))), None)

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
        for prop in self.properties():
            if getattr(type(self), prop).fset is None:
                continue

            prop_value = values.get(prop, values.get(inflection.camelize(prop, uppercase_first_letter=False)))

            if prop_value is not None:
                prop_type = self.prop_type(prop)

                if prop_type is None:
                    # This shouldn't happen
                    setattr(self, prop, prop_value)
                elif issubclass(prop_type, dt.datetime):
                    if isinstance(prop_value, int):
                        setattr(self, prop, dt.datetime.fromtimestamp(prop_value / 1000).isoformat())
                    else:
                        import re
                        matcher = re.search('\.([0-9]*)Z$', prop_value)
                        if matcher:
                            sub_seconds = matcher.group(1)
                            if len(sub_seconds) > 6:
                                prop_value = re.sub(matcher.re, '.{}Z'.format(sub_seconds[:6]), prop_value)
                        setattr(self, prop, dateutil.parser.isoparse(prop_value))
                elif issubclass(prop_type, dt.date):
                    setattr(self, prop, dateutil.parser.isoparse(prop_value).date())
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
    def _from_dict(cls, values: dict) -> 'Base':
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
    def from_dict(cls, values: dict) -> 'Base':
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
            attr = getattr(super().__getattribute__('__class__'), prop)
            if attr.fset:
                super(Base, self).__setattr__(prop, super(Base, instance).__getattribute__(prop))


class Priceable(Base, metaclass=ABCMeta):

    PROVIDER = None

    def provider(self):
        """
        The risk provider - defaults to GsRiskApi
        """
        if self.PROVIDER is None:
            from gs_quant.api.gs.risk import GsRiskApi
            type(self).PROVIDER = GsRiskApi

        return self.PROVIDER

    def get_quantity(self) -> float:
        """
        Quantity of the instrument
        """
        raise NotImplementedError

    def resolve(self, in_place: bool=True):
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

    def calc(self, risk_measure):
        """
        Calculate the value of the risk_measure

        :param risk_measure: the risk measure to compute, e.g. IRDelta (from gs_quant.risk)
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
    pass


def get_enum_value(enum_type: EnumMeta, value: Union[EnumBase, str]):
    if value in (None, 'None'):
        return None

    if isinstance(value, enum_type):
        return value

    try:
        enum_value = enum_type(value)
    except ValueError:
        _logger.warning('Setting value to {}, which is not a valid entry in {}'.format(value, enum_type))
        enum_value = value

    return enum_value
