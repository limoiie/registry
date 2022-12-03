from typing import Dict, Protocol, TypeVar


class DataclassProtocol(Protocol):
    __dataclass_fields__: Dict


T = TypeVar('T')
MT = TypeVar('MT', bound=DataclassProtocol)
