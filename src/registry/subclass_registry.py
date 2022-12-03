from typing import Optional, Dict, Type, TypeVar

T = TypeVar('T')


class SubclassRegistry:
    """
    A base class for these classes which want to be used as a registry for their
    subclasses.

    Similar with `Registry`, `SubclassRegistry` manage registered classes. But,
    the difference is, `SubclassRegistry` is designed to manage only registry
    class's subclasses, while `Registry` collects arbitrary classes/methods.
    Another difference is, `SubclassRegistry` registers by inheritance, while
    `Registry` registers by annotator returned by `Registry.register`.
    """

    _center: Optional[Dict[Type[T], Dict]] = None

    def __init_subclass__(cls, **meta):
        base_cls = cls._base_that_directly_derive_registry()
        if base_cls:
            base_cls.center()[cls] = meta

    @classmethod
    def query(cls: Type[T], *, fn=None, **query) -> Type[T]:
        """
        Find the subclass with a match `fn` or by partial meta info `query`.

        :param fn: Match function that accepts meta, return if matched or not.
        :param query: The partial meta info.
        :return: the matched registered subclass, or `None` if no such one.

        Examples
        --------

        Find by partial meta info:

        >>> class Tool(SubclassRegistry): ...
        >>> class HammerTool(Tool, name='Hammer', place='toolbox'): ...
        >>> assert Tool.query(name='Hammer') is HammerTool

        Or, find by callback function:

        >>> assert Tool.query(fn=lambda m: m['name'] == 'Hammer') is HammerTool
        """
        fn = fn or (lambda meta: query.items() <= meta.items())

        for registered_cls, registered_meta in cls.center().items():
            if fn(registered_meta):
                return registered_cls
        else:
            return None

    @classmethod
    def meta_of(cls, subclass):
        """Return the registered meta information by `subclass`."""
        return cls.center()[subclass]

    @classmethod
    def center(cls) -> Dict[Type[T], Dict]:
        """Return all the subclasses with bound meta info."""
        if cls._center is None:
            cls._center = dict()

        return cls._center

    @classmethod
    def _base_that_directly_derive_registry(cls):
        for parent in cls.__bases__:
            if parent == SubclassRegistry:
                return None

            if issubclass(parent, SubclassRegistry):
                return parent._base_that_directly_derive_registry() or parent

        return None
