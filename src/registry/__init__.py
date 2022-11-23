__all__ = ['__version__', 'Registry', 'SubclassRegistry']

from typing import Dict, Type, Optional, Any, TypeVar

try:
    from importlib.metadata import version, PackageNotFoundError
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("registry")
except PackageNotFoundError:
    __version__ = "unknown version"

T = TypeVar('T')


class Registry:
    _center: Optional[Dict[Type, Any]] = None

    @classmethod
    def register(cls, return_class=True, default_return=None, **meta):
        def do_register(subclass: Type):
            cls.center()[subclass] = meta
            return subclass if return_class else default_return

        return do_register

    @classmethod
    def unregister(cls, subclass):
        del cls.center()[subclass]

    @classmethod
    def registered(cls, subclass: type):
        return subclass in cls.center()

    @classmethod
    def query(cls, **query):
        center = cls.center()
        for registered_cls, registered_meta in center.items():
            if registered_meta.items() >= query.items():
                return registered_cls

        return None

    @classmethod
    def meta_of(cls, subclass):
        return cls.center()[subclass]

    @classmethod
    def center(cls) -> Dict[Type, Any]:
        if not cls._center:
            cls._center = dict()
        return cls._center


class SubclassRegistry:
    _center: Optional[Dict[Type[T], Dict]] = None

    def __init_subclass__(cls, **meta):
        base_cls = SubclassRegistry._base_of(cls)
        if base_cls is not SubclassRegistry:
            base_cls.center()[cls] = meta

    @classmethod
    def query(cls: Type[T], *, fn=None, **query) -> Type[T]:
        fn = fn or (lambda meta: query.items() <= meta.items())

        for registered_cls, registered_meta in cls.center().items():
            if fn(registered_meta):
                return registered_cls
        else:
            return None

    @classmethod
    def meta_of(cls, subclass):
        return cls.center()[subclass]

    @classmethod
    def center(cls) -> Dict[Type[T], Dict]:
        if cls._center is None:
            cls._center = dict()

        return cls._center

    @staticmethod
    def _base_of(cls):
        for parent in cls.__bases__:
            if issubclass(parent, SubclassRegistry):
                return parent

        return None
