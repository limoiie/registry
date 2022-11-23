from typing import Optional, Dict, Type, Any


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
