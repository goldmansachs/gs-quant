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
        self.__entered = False

    def __enter__(self):
        clz = self._cls
        self.__previous = clz.current
        self.__entered = True
        clz.current = self
        self._on_enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._on_exit(exc_type, exc_val, exc_tb)
        finally:
            self._cls.current = self.__previous
            self.__previous = None
            self.__entered = False

    @property
    def _cls(self) -> ContextMeta:
        return next(b for b in self.__class__.__bases__ if issubclass(b, ContextBase))

    @property
    def _is_entered(self) -> bool:
        return self.__entered

    def _on_enter(self):
        pass

    def _on_exit(self, exc_type, exc_val, exc_tb):
        pass


class ContextBaseWithDefault(ContextBase):

    @property
    def _cls(self) -> ContextMeta:
        return self.__class__

    @classmethod
    def has_default(cls) -> bool:
        return True

