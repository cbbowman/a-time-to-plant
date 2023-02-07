from dataclasses import dataclass
from uuid import UUID, uuid4

from at2p_app.domain.common.error import CropError
from at2p_app.domain.value_objects.temperature import TempRange


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
    name: CropName
    abs_range: TempRange
    opt_range: TempRange
    id: UUID

    @classmethod
    def new(
        cls,
        name: str,
        abs_range: TempRange,
        opt_range: TempRange,
        id: UUID = None,
    ):

        cls._validate(abs_range, opt_range)
        name, id = cls._clean(name, id)
        return cls(name, abs_range, opt_range, id)

    @classmethod
    def _validate(cls, abs_range: TempRange, opt_range: TempRange):

        cls._check_ranges(abs_range, opt_range)
        return

    @classmethod
    def _clean(cls, name: CropName, id: UUID):

        if not isinstance(name, CropName):
            name = CropName.new(name)

        if not isinstance(id, UUID):
            id = uuid4()

        return name, id

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

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()
