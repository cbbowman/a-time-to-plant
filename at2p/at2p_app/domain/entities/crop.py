from dataclasses import dataclass
from uuid import uuid4, UUID
from at2p_app.domain.value_objects.temperature import TempRange
from at2p_app.domain.common.error import CropError


@dataclass(eq=True)
class CropName:

    name: str

    @classmethod
    def new(cls, name: str):
        cls._validate(name)
        name = cls._clean(name)
        return cls(name)

    @classmethod
    def _validate(cls, name):
        if not isinstance(name, str):
            raise ValueError("name must be a string")

        if not len(name.strip()) > 0:
            error_msg = "Name may not be an empty string"
            raise ValueError(error_msg)
        return name

    @classmethod
    def _clean(cls, name: str):
        name = name.strip()
        name = name.title()
        return name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(eq=True)
class Crop:
    id: UUID
    name: CropName
    abs_range: TempRange
    opt_range: TempRange

    @classmethod
    def new(cls, name: str, abs_range: TempRange, opt_range: TempRange):

        name, abs_range, opt_range = cls._validate(name, abs_range, opt_range)
        id = uuid4()
        name = cls._clean(name)
        return cls(id, name, abs_range, opt_range)

    @classmethod
    def get(
        cls,
        id: UUID,
        name: CropName,
        abs_range: TempRange,
        opt_range: TempRange,
    ):

        name, abs_range, opt_range = cls._validate(name, abs_range, opt_range)
        name = cls._clean(name)
        return cls(id, name, abs_range, opt_range)

    @classmethod
    def _validate(cls, name: str, abs_range: TempRange, opt_range: TempRange):

        cls._check_ranges(abs_range, opt_range)
        return name, abs_range, opt_range

    @classmethod
    def _clean(cls, name: CropName):
        if not isinstance(name, CropName):
            return CropName.new(name)
        return name

    @classmethod
    def _check_ranges(cls, abs_range, opt_range):

        if not isinstance(abs_range, TempRange):
            error_msg = "Absolute Range must be an instance of 'TempRange'."
            raise CropError(error_msg)

        if not isinstance(opt_range, TempRange):
            error_msg = "Optimal Range must be an instance of 'TempRange'."
            raise CropError(error_msg)

    @classmethod
    def new_from_dict(cls, d):
        return cls.new(**d)

    @classmethod
    def get_from_dict(cls, d):
        return cls.get(**d)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()
