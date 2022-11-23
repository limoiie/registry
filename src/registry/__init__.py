__all__ = ['__version__', 'Registry', 'SubclassRegistry']

try:
    from importlib.metadata import version, PackageNotFoundError
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("registry")
except PackageNotFoundError:
    __version__ = "unknown version"

from .registry import Registry
from .subclass_registry import SubclassRegistry
