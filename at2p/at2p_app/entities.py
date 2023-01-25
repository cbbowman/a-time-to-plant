from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict


@dataclass(slots=True, order=True, eq=True)
class Temp:
    """Class for temperate value"""

    temp: float
    scale: str = "F"

    def __str__(self) -> str:
        return f"{self.temp:.0F} \u00B0{self.scale}"

    def __post_init__(self) -> None:
        if not isinstance(self.temp, (int, float)):
            raise ValueError("Temp must be a number!")


@dataclass(slots=True, kw_only=True)
class TempRange:
    """Class for a range of temperatures"""

    min: Temp
    max: Temp

    def __init__(self, min, max) -> None:
        self.min = Temp(min)
        self.max = Temp(max)

    def __post_init__(self) -> None:
        if not self.validate():
            raise ValueError("Temp range incorrect")
        return

    def validate(self) -> bool:
        if not isinstance(self.min, Temp):
            return False
        if not isinstance(self.max, Temp):
            return False
        if self.min > self.max:
            return False
        return True

    def __str__(self) -> str:
        return f"{self.min} \u2013 {self.max}"


@dataclass
class AbstractRequirementList(ABC):
    requirements: dict

    @abstractmethod
    def _validate_requirements(self) -> None:
        pass

    def __init__(self) -> None:
        self._validate_requirements()
        super().__init__()


@dataclass(slots=True)
class TempReqList(AbstractRequirementList):
    requirements: Dict[str, TempRange]

    def __post_init__(self) -> None:
        self._validate_requirements()

    def _validate_requirements(self) -> None:
        mins_wrong = (
            not self.requirements["absolute"].min
            < self.requirements["optimal"].min
        )
        maxs_wrong = (
            not self.requirements["absolute"].max
            > self.requirements["optimal"].max
        )
        if mins_wrong or maxs_wrong:
            raise ValueError("Temp ranges are incorrrect")
        return


@dataclass
class Crop:
    name: str
    reqs: AbstractRequirementList

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


@dataclass
class LatLong:
    lat: float
    long: float

    def __str__(self) -> str:
        lat = self._deg_min_sec(self.lat)
        if self.lat < 0:
            vert = 'S'
        else:
            vert = 'N'
        long = self._deg_min_sec(self.long)
        if self.long < 0:
            hor = 'W'
        else:
            hor = 'E'
        return f"{lat}{vert} {long}{hor}"

    def _deg_min_sec(self, coord) -> str:
        if coord < 0:
            coord = -1 * coord
        deg = coord // 1
        min_dec = (self.lat % 1) * 60
        min = min_dec // 1
        sec = round((min_dec % 1) * 60)
        return f"{deg:.0F}\u00B0{min:.0F}\u2032{sec:.0F}\u2033"

#     def __str__(self):
#         str_lat = f"Latitude: {self.lat:.4f}"
#         str_long = f"Longitude: {self.long:.4f}"
#         return str_lat + "\n" + str_long

#     def __repr__(self):
#         return (self.lat, self.long)

#     def check_values(self, lat: float, long: float) -> None:
#         self.check_lat(lat)
#         self.check_long(long)

#     def check_lat(self, lat: float) -> None:
#         error_msg = "Latitude must be a number between -90 and 90"
#         if not self.is_a_number(lat):
#             raise ValueError(error_msg)
#         lat_ok = lat < 90 and lat > -90
#         if not lat_ok:
#             raise ValueError(error_msg)
#         return

#     def check_long(self, long: float) -> None:
#         error_msg = "Longitude must be a number between -180 and 180"
#         if not self.is_a_number(long):
#             raise ValueError(error_msg)
#         long_ok = long < 180 and long > -180
#         if not long_ok:
#             raise ValueError(error_msg)

#     def is_a_number(self, value) -> bool:
#         return isinstance(value, int) or isinstance(value, float)


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
