from typing import Dict, TypeVar

try:
    from typing import Protocol

except ImportError:
    Protocol = object


class DataclassProtocol(Protocol):
    __dataclass_fields__: Dict


T = TypeVar('T')
MT = TypeVar('MT', bound=DataclassProtocol)
