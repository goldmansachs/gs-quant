from abc import ABCMeta
import threading

from gs_quant.errors import MqUninitialisedError


thread_local = threading.local()


class ContextMeta(type, metaclass=ABCMeta):

    @classmethod
    def has_default(mcs) -> bool:
        return False

    @property
    def current(cls) -> 'ContextBase':
        """
        The current instance of this context
        """
        current = getattr(thread_local, '{}_current'.format(cls.__name__), None) or cls.default
        if current is None:
            raise MqUninitialisedError('{} is not initialised'.format(cls.__name__))

        return current

    @current.setter
    def current(cls, current: 'ContextBase'):
        setattr(thread_local, '{}_current'.format(cls.__name__), current)

    @property
    def current_is_set(cls) -> bool:
        return getattr(thread_local, '{}_current'.format(cls.__name__), None) is not None

    @property
    def default(cls) -> 'ContextBase':
        attr_name = '{}_default'.format(cls.__name__)
        default = getattr(thread_local, attr_name, None)
        if (not cls.default_is_set) and cls.has_default():
            default = cls()
            setattr(thread_local, attr_name, default)

        return default

    @property
    def default_is_set(cls) -> bool:
        return getattr(thread_local, '{}_default'.format(cls.__name__), None) is not None

    @default.setter
    def default(cls, default: 'ContextBase'):
        setattr(thread_local, '{}_default'.format(cls.__name__), default)


class ContextBase(metaclass=ContextMeta):
    
    def __enter__(self):
        clz = self._cls

        try:
            current = clz.current
            setattr(thread_local, '{}_previous'.format(clz.__name__), current)
        except MqUninitialisedError:
            pass

        setattr(thread_local, '{}_entered'.format(clz.__name__), True)
        clz.current = self
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._on_exit(exc_type, exc_val, exc_tb)
        finally:
            clz = self._cls
            clz.current = getattr(thread_local, '{}_previous'.format(clz.__name__), None)
            setattr(thread_local, '{}_previous'.format(clz.__name__), None)
            setattr(thread_local, '{}_entered'.format(clz.__name__), False)

    @property
    def _cls(self) -> ContextMeta:
        cls = next(b for b in self.__class__.__bases__ if issubclass(b, ContextBase))
        return self.__class__ if cls.__name__ in ('ContextBase', 'ContextBaseWithDefault') else cls

    @property
    def _is_entered(self) -> bool:
        return getattr(thread_local, '{}_entered'.format(self._cls.__name__), False)

    def _on_enter(self):
        pass

    def _on_exit(self, exc_type, exc_val, exc_tb):
        pass


class ContextBaseWithDefault(ContextBase):

    @classmethod
    def has_default(cls) -> bool:
        return True
