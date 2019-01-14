from abc import ABCMeta


class ContextMeta(type, metaclass=ABCMeta):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.__current = None
        cls.__default = None

    @classmethod
    def has_default(mcs) -> bool:
        return False

    @property
    def current(cls) -> 'ContextBase':
        return cls.__current or cls.default

    @current.setter
    def current(cls, current: 'ContextBase'):
        cls.__current = current

    @property
    def default(cls) -> 'ContextBase':
        if cls.__default is None and cls.has_default():
            cls.__default = cls()

        return cls.__default


class ContextBase(metaclass=ContextMeta):

    def __init__(self):
        self.__previous = None

    def __enter__(self):
        cls = next(b for b in self.__class__.__bases__ if issubclass(b, ContextBase))
        self.__previous = cls.current
        cls.current = self
        self._on_enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._on_exit(exc_type, exc_val, exc_tb)
        finally:
            cls = next(b for b in self.__class__.__bases__ if issubclass(b, ContextBase))
            cls.current = self.__previous
            self.__previous = None

    @property
    def _is_entered(self) -> bool:
        return self.__previous is not None

    def _on_enter(self):
        pass

    def _on_exit(self, exc_type, exc_val, exc_tb):
        pass


class ContextBaseWithDefault(ContextBase):

    @classmethod
    def has_default(cls) -> bool:
        return True

