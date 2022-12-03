# noinspection PyUnresolvedReferences,PyProtectedMember
from typing import Dict, Generic, Optional, Tuple, Type, _GenericAlias

from registry.types import MT, T


class SubclassRegistry(Generic[MT]):
    """
    A base class for these classes which want to be used as a registry for their
    subclasses.

    Similar with `Registry`, `SubclassRegistry` manage registered classes. But,
    the difference is, `SubclassRegistry` is designed to manage only registry
    class's subclasses, while `Registry` collects arbitrary classes/methods.
    Another difference is, `SubclassRegistry` registers by inheritance, while
    `Registry` registers by annotator returned by `Registry.register`.
    """

    _center: Optional[Dict[Type[T], MT]] = None

    def __init_subclass__(cls, **meta):
        base_cls = cls._base_that_directly_derive_registry()
        if base_cls:
            meta_cls = base_cls._meta_cls()
            base_cls.center()[cls] = meta_cls(**meta)

    @classmethod
    def query(cls: Type[T], *, fn=None, **query) -> Optional[Type[T]]:
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
        fn = fn or (lambda meta: query.items() <= (
            (meta if isinstance(meta, dict) else meta.__dict__)).items())

        for registered_cls, registered_meta in cls.center().items():
            if fn(registered_meta):
                return registered_cls
        else:
            return None

    @classmethod
    def meta_of(cls, subclass) -> MT:
        """Return the registered meta information by `subclass`."""
        return cls.center()[subclass]

    @classmethod
    def center(cls) -> Dict[Type[T], MT]:
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

    @classmethod
    def _meta_cls(cls) -> type:
        args = cls._generic_args()
        return args[0] if args else dict

    @classmethod
    def _generic_args(cls) -> Tuple[type] or None:
        orig_base = cls._orig_base_that_derive_register()
        return orig_base.__args__ if orig_base else None

    @classmethod
    def _orig_base_that_derive_register(cls) -> _GenericAlias or None:
        orig_bases = getattr(cls, '__orig_bases__', None)
        if not orig_bases:
            return

        for base, orig_base in zip(cls.__bases__, orig_bases):
            if issubclass(base, SubclassRegistry):
                if isinstance(orig_base, _GenericAlias):
                    if getattr(orig_base, '__origin__', None) == base:
                        return orig_base
