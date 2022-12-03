# noinspection PyUnresolvedReferences,PyProtectedMember
from typing import Callable, Dict, Generic, Hashable, Optional, Tuple, \
    _GenericAlias

from registry.types import MT


class Registry(Generic[MT]):
    """
    A base class for these classes which want to be used as a registry.

    Any class inherited `Registry` will become a registry class. A registry
    class can register classes or methods of interest with corresponding meta
    info. If you want to manage a set of classes or methods, and usually need to
    fetch them by their meta info, then derive `Registry`.
    """

    _center: Optional[Dict[Hashable, MT]] = None

    @classmethod
    def register(cls, return_annotated=True, default_return=None, **meta):
        """
        Register the annotated class/method with meta information.

        :param return_annotated: If false, hidden the annotated class/method.
        :param default_return: The replacement when `return_annotated` is false.
        :return: the annotated class if `return_annotated` is true; otherwise,
          return `default_return` instead.

        Examples:
        --------

        >>> class Toolbox(Registry): ...
        >>> @Toolbox.register(return_annotated=False)
        ... class Hammer: ...
        """
        meta_cls = cls._meta_cls()

        def do_register(annotated: Hashable):
            cls.center()[annotated] = meta_cls(**meta)
            return annotated if return_annotated else default_return

        return do_register

    @classmethod
    def unregister(cls, annotated):
        """Unregister `annotated`."""
        del cls.center()[annotated]

    @classmethod
    def registered(cls, annotated):
        """Return true if `subclass` is registered."""
        return annotated in cls.center()

    @classmethod
    def query(cls, *, fn: Callable[[MT], bool] = None, **query):
        """
        Find the registered class/method by partial meta info `query`.

        :param fn: Match function that accepts meta, return if matched or not.
        :param query: The partial meta info.
        :return: the matched registered class/method, or `None` if no such one.

        Examples
        --------

        >>> class Toolbox(Registry): ...
        >>> @Toolbox.register(name='Hammer', place='toolbox', year=2002)
        ... class Hammer: ...
        >>> assert Toolbox.query(name='Hammer', place='toolbox') is Hammer

        Or, find by callback function:

        >>> assert Toolbox.query(fn=lambda m: m['name'] == 'Hammer') is Hammer
        """
        fn = fn or (lambda meta: query.items() <= (
            (meta if isinstance(meta, dict) else meta.__dict__)).items())

        for registered, registered_meta in cls.center().items():
            if fn(registered_meta):
                return registered

        return None

    @classmethod
    def meta_of(cls, annotated) -> MT:
        """Return the registered meta information by `subclass`."""
        return cls.center()[annotated]

    @classmethod
    def center(cls) -> Dict[Hashable, MT]:
        """Return all the registered subclasses with bound meta info."""
        if not cls._center:
            cls._center = dict()
        return cls._center

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
            if issubclass(base, Registry):
                if isinstance(orig_base, _GenericAlias):
                    if getattr(orig_base, '__origin__', None) == base:
                        return orig_base
