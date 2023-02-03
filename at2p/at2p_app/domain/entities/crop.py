from dataclasses import dataclass
from uuid import uuid4
from at2p_app.domain.value_objects.temperature import TempRange
from at2p_app.domain.common.error import CropError


@dataclass(eq=True)
class Crop:
    id: int
    name: str
    abs_range: TempRange
    opt_range: TempRange

    @classmethod
    def new(cls, name: str, abs_range: TempRange, opt_range: TempRange):

        name, abs_range, opt_range = cls._validate(name, abs_range, opt_range)
        id = uuid4().int % 10**9
        name = cls._clean(name)
        return cls(id, name, abs_range, opt_range)

    @classmethod
    def get(
        cls, id: int, name: str, abs_range: TempRange, opt_range: TempRange
    ):

        return cls(id, name, abs_range, opt_range)

    @classmethod
    def _validate(cls, name: str, abs_range: TempRange, opt_range: TempRange):

        cls._check_name(name)
        cls._check_ranges(abs_range, opt_range)
        return name, abs_range, opt_range

    @classmethod
    def _clean(cls, name: str):
        name = name.strip()
        name = name.title()
        return name

    @classmethod
    def _check_name(cls, name):
        if not isinstance(name, str):
            error_msg = "Crop name must be a string"
            raise CropError(error_msg)
        if not len(name) > 0:
            error_msg = "Crop may not be an empty string"
            raise CropError(error_msg)

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
