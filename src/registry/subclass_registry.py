from typing import Optional, Dict, Type, TypeVar

T = TypeVar('T')


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
