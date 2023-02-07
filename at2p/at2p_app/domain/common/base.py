from abc import ABC, abstractclassmethod
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ValueObject(ABC):
    @abstractclassmethod
    def new(cls, *args, **kwargs):
        pass

    @abstractclassmethod
    def _validate(cls, *args, **kwargs):
        pass
