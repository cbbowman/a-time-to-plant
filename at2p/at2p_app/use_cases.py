from dataclasses import dataclass
from abc import ABC, abstractmethod
from .entities import TempRange
from typing import Optional, Dict, TypedDict


class ReqList(TypedDict):
    type: str
    req: object


@dataclass
class CropRequirement(ABC):
    def __post_init__(self) -> None:
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        pass


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


class CropError(Exception):
    generic_msg = "Generic Crop Error"

    def __init__(
        self, name: str, reqs: ReqList, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nName: {name}\nRequirements: {reqs}"
        super().__init__(message)


@dataclass
class TempRequirement(CropRequirement):

    absolute: TempRange = None
    optimal: TempRange = None

    def _is_fully_defined(self):
        if self.absolute is None or self.optimal is None:
            return False
        else:
            return True

    def _scales_are_correct(self):
        if self.absolute.min.scale != self.optimal.min.scale:
            error_msg = "Absolute and optimal temp scales must be equal."
            raise (TempRequirementError(self, error_msg))
        return

    def _validate(self) -> None:
        if not self._is_fully_defined():
            return
        self._scales_are_correct()
        self._check_ranges()
        return

    def _check_ranges(self):
        mins_wrong = self.absolute.min.value > self.optimal.min.value
        maxs_wrong = self.absolute.max.value < self.optimal.max.value
        ranges_intersect = mins_wrong or maxs_wrong
        if ranges_intersect:
            error_msg = "Absolute and optimal ranges are incorrect"
            raise TempRequirementError(self, error_msg)
        return


@dataclass
class Crop:
    name: str
    reqs: ReqList

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return self.name

    def __post_init__(self):
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


# class Planter:
#     username: str
#     location: Place

#     pass


# class Weather:
#     pass


# class Weather:
#     pass
