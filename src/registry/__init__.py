__all__ = ['__version__', 'Registry', 'SubclassRegistry']

try:
    import importlib.metadata as _importlib_metadata
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences
    import importlib_metadata as _importlib_metadata

try:
    __version__ = _importlib_metadata.version("registry")
except _importlib_metadata.PackageNotFoundError:
    __version__ = "unknown version"

from .registry import Registry
from .subclass_registry import SubclassRegistry
