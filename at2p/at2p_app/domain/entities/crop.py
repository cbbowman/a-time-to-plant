from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import TypedDict
from at2p_app.domain.entities.temperature import TempRange


class ReqList(TypedDict):
    type: str
    req: object


@dataclass
class CropRequirement(ABC):
    @abstractmethod
    def __post_init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _validate(self) -> None:
        raise NotImplementedError

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


class CropError(Exception):
    generic_msg = "Generic Crop Error"

    def __init__(
        self, name: str, reqs: ReqList, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nName: {name}\nRequirements: {reqs}"
        super().__init__(message)


@dataclass
class CropRequirementError(Exception):
    error_msg = "Generic Crop Requirements Error"

    def __init__(self, r: CropRequirement, message: str = error_msg) -> None:
        self.req = r
        self.message = message
        super().__init__(self.message)


class TempRequirementError(CropRequirementError):
    generic_msg = "Generic Temperature Requirement Error"

    def __init__(
        self, opt: TempRange, abs: TempRange, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nOpt: {opt}\nAbs: {abs}"
        super().__init__(message)


@dataclass
class TempRequirement(CropRequirement):

    absolute: TempRange = TempRange(10, 90)
    optimal: TempRange = TempRange(30, 50)

    def __post_init__(self) -> None:
        self._validate()
        return

    def _validate(self) -> None:
        self._scales_are_correct()
        self._check_ranges()
        return

    def _scales_are_correct(self):
        if self.absolute.scale.value != self.optimal.scale.value:
            error_msg = "Absolute and optimal temp scales must be equal."
            raise TempRequirementError(self, error_msg)
        return

    def _check_ranges(self):
        ranges_ok = self.absolute.includes(self.optimal)
        if not ranges_ok:
            error_msg = "Absolute and optimal ranges are incorrect"
            raise TempRequirementError(self.optimal, self.absolute, error_msg)
        return


@dataclass
class Crop:
    name: str
    reqs: ReqList
    id: int = None

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return f"{self.name}[{self.id}]"

    def __post_init__(self):
        if self.id is None:
            self.id = hash(self.name)
        self._validate()

    def _validate(self):
        error_msg = "Crop name must be a string!"
        if not isinstance(self.name, str):
            raise CropError(self.name, self.reqs, error_msg)

        error_msg = "Crop name may not be blank"
        if not len(self.name) > 0:
            raise CropError(self.name, self.reqs, error_msg)

        error_msg = "Crop requirements must be a dictionary!"
        if not isinstance(self.reqs, dict):
            raise CropError(self.name, self.reqs, error_msg)

        error_msg = "Crop reqs must be a CropRequirement"
        for key in self.reqs:
            if not isinstance(self.reqs[key], CropRequirement):
                raise CropError(self.name, self.reqs, error_msg)
