from typing import Optional, Dict, Hashable


class Registry:
    """
    A base class for these classes which want to be used as a registry.

    Any class inherited `Registry` will become a registry class. A registry
    class can register classes or methods of interest with corresponding meta
    info. If you want to manage a set of classes or methods, and usually need to
    fetch them by their meta info, then derive `Registry`.
    """

    _center: Optional[Dict[Hashable, Dict]] = None

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

        >>> class Tool(Registry): ...
        >>> @Tool.register(return_annotated=False)
        ... class SubTool: ...
        """

        def do_register(subclass: Hashable):
            cls.center()[subclass] = meta
            return subclass if return_annotated else default_return

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
    def query(cls, **query):
        """
        Find the registered class/method by partial meta info `query`.

        :param query: The partial meta info.
        :return: the matched registered class/method, or `None` if no such one.

        Examples
        --------

        >>> class Tool(Registry): ...
        >>> @Tool.register(name='Hammer', place='toolbox', year=2002)
        ... class HammerTool: ...
        >>> assert Tool.query(name='Hammer', place='toolbox') is HammerTool
        """
        center = cls.center()
        for registered, registered_meta in center.items():
            if registered_meta.items() >= query.items():
                return registered

        return None

    @classmethod
    def meta_of(cls, annotated) -> Dict:
        """Return the registered meta information by `subclass`."""
        return cls.center()[annotated]

    @classmethod
    def center(cls) -> Dict[Hashable, Dict]:
        """Return all the registered subclasses with bound meta info."""
        if not cls._center:
            cls._center = dict()
        return cls._center
