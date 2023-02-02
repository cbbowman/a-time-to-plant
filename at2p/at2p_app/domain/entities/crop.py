from dataclasses import dataclass
from at2p_app.domain.value_objects.temperature import TempRange


class CropError(Exception):
    generic_msg = "Generic Crop Error"

    def __init__(
        self, name: str, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nName: {name}\n"
        super().__init__(message)


@dataclass
class Crop:
    id: int
    name: str
    abs_range: TempRange
    opt_range: TempRange

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return f"{self.name}"

    def __post_init__(self):
        self._validate()

    def _validate(self):
        error_msg = "Crop name must be a string!"
        if not isinstance(self.name, str):
            raise CropError(self.name, error_msg)

        if not len(self.name) > 0:
            error_msg = "Crop name may not be blank"
            raise CropError(self.name, error_msg)
