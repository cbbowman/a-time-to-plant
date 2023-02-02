from dataclasses import dataclass
from abc import abstractclassmethod
from abc import ABC


@dataclass(frozen=True, eq=True)
class ValueObject(ABC):
    @abstractclassmethod
    def new(cls, *args, **kwargs):
        pass

    @abstractclassmethod
    def _validate(cls, *args, **kwargs):
        pass
