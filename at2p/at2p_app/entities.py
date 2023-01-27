from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict
from enum import Enum, auto


@dataclass
class TempScale(Enum):
    F = auto()
    C = auto()


@dataclass(slots=True, order=True, eq=True)
class Temp:
    """Class for temperate value"""

    temp: float
    scale: TempScale = "F"

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return f"{self.temp:.0F} \u00B0{self.scale}"

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> bool:
        if not isinstance(self.temp, (int, float)):
            raise ValueError("Temp must be a number!")

    def is_in_range(self, min: int, max: int, scale: TempScale) -> bool:
        
        return min < self.temp and self.temp < max


@dataclass(slots=True, kw_only=True)
class TempRange:
    """Class for a range of temperatures"""

    min: Temp
    max: Temp

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __init__(self, min, max) -> None:
        self.min = Temp(min)
        self.max = Temp(max)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.min.temp > self.max.temp:
            raise ValueError("Temp range incorrect")

    def __str__(self) -> str:
        return f"{self.min} \u2013 {self.max}"


@dataclass
class AbstractRequirementList(ABC):
    requirements: Dict

    @abstractmethod
    def _validate(self) -> None:
        pass


@dataclass
class TempReqList(AbstractRequirementList):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        mins_wrong = (
            not self.requirements["abs"].min < self.requirements["opt"].min
        )
        maxs_wrong = (
            not self.requirements["abs"].max > self.requirements["opt"].max
        )
        if mins_wrong or maxs_wrong:
            raise ValueError("Temp ranges are incorrrect")
        return


@dataclass
class Crop:
    name: str
    reqs: AbstractRequirementList

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
            raise ValueError(error_msg)

        error_msg = "Crop name may not be blank"
        if not len(self.name) > 0:
            raise ValueError(error_msg)


@dataclass(slots=True, kw_only=True)
class Country:
    name: str
    code: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return self.name

    def __post_init__(self) -> None:
        self._validate()
        # self._clean()

    def _validate(self) -> None:
        error_msg = "Name and code must be strings!"
        name_not_str = not isinstance(self.name, str)
        code_not_str = not isinstance(self.code, str)
        if name_not_str or code_not_str:
            raise ValueError(error_msg)

        error_msg = "Name may not be blank!"
        name_is_blank = not len(self.name) > 0
        if name_is_blank:
            raise ValueError(error_msg)

        error_msg = "Code must be exactly two characters!"
        code_is_2_chars = len(self.code) == 2
        if not code_is_2_chars:
            raise ValueError(error_msg)

    def _clean(self):
        self.name = self.name.title()
        self.code = self.code.upper()


@dataclass
class LatLong:
    lat: float
    long: float

    def __post_init__(self):
        self._check_values()
        return

    def __str__(self):
        ns = "S" if self.lat < 0 else "N"
        ew = "W" if self.long < 0 else "E"
        lat_str = f"{self.lat:.2f{ns}}\u00b0"
        long_str = f"{self.long:.2f{ew}}\u00b0"
        return f"{lat_str} {long_str}"

    def _check_values(self) -> None:
        self._check_lat()
        self._check_long()

    def _check_lat(self) -> None:
        error_msg = "Latitude must be a number between -90 and 90"
        if not self._is_a_number(self.lat):
            raise ValueError(error_msg)
        lat_ok = self.lat < 90 and self.lat > -90
        if not lat_ok:
            raise ValueError(error_msg)
        return

    def _check_long(self) -> None:
        error_msg = "Longitude must be a number between -180 and 180"
        if not self._is_a_number(self.long):
            raise ValueError(error_msg)
        long_ok = self.long < 180 and self.long > -180
        if not long_ok:
            raise ValueError(error_msg)

    def _is_a_number(self, value) -> bool:
        return isinstance(value, int) or isinstance(value, float)


# class Place:
#     def __init__(
#         self,
#         country: Country,
#         state: str,
#         city: str,
#         zip: str,
#         coord: LatLong,
#         elev: int,
#     ) -> None:

#         self.check_values(country, state, city, zip, coord, elev)

#         self.country = country
#         self.state = state
#         self.city = city
#         self.zip = zip
#         self.coord = coord
#         self.elev = elev

#     def __str__(self) -> str:
#         return f"{self.city}, {self.state}, {self.country.code}"

#     def __repr__(self) -> str:
#         return (self.country.code, self.zip)

#     def check_values(
#         self,
#         country: Country,
#         state: str,
#         city: str,
#         zip: str,
#         coord: LatLong,
#         elev: int,
#     ) -> None:
#         if not isinstance(country, Country):
#             raise ValueError()
#         if not self.is_nonempty_string(state):
#             raise ValueError()
#         if not self.is_nonempty_string(city):
#             raise ValueError()
#         if not self.is_nonempty_string(zip):
#             raise ValueError()
#         if not isinstance(coord, LatLong):
#             raise ValueError()
#         if not isinstance(elev, int):
#             raise ValueError()

#     def is_nonempty_string(self, value) -> bool:
#         if not isinstance(value, str):
#             raise ValueError("Value must be a string!")
#         return len(value) > 0


# class Planter:
#     username: str
#     location: Place

#     pass


# class Weather:
#     pass


# class Weather:
#     pass
