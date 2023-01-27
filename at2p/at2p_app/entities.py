from dataclasses import dataclass
from enum import Enum, auto

COUNTRIES = {"US": "United States"}
COUNTRY_CODE_LENGTH = 2


@dataclass
class TempScale(Enum):
    F = auto()
    C = auto()


class TemperatureError(Exception):
    error_msg = "Generic Temperature Error"

    def __init__(
        self, temp: int, scale: TempScale, error_msg: str = error_msg
    ) -> None:
        message = f"\n{error_msg}\nTemp: {temp}\nScale: {scale}"
        super().__init__(message)


class TempRangeError(Exception):
    generic_msg = "Generic Temperature Range Error"

    def __init__(
        self, min: int, max: int, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nMin: {min}\nMax: {max}"
        super().__init__(message)


class CountryError(Exception):
    generic_msg = "Generic Country Error"

    def __init__(self, code: str, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nCode: {code}"
        super().__init__(message)


class LatLongError(Exception):
    generic_msg = "Generic Coordinates Error"

    def __init__(
        self, lat: float, long: float, error_msg: str = generic_msg
    ) -> None:
        message = f"\n{error_msg}\nLat: {lat}\nLong: {long}"
        super().__init__(message)


@dataclass(slots=True, order=True, eq=True)
class Temp:
    """Class for temperate value"""

    value: float
    scale: TempScale = "F"

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return f"{self.value} \u00B0{self.scale}"

    def __post_init__(self) -> None:
        self._validate()
        self._clean()

    def _validate(self) -> None:
        if not isinstance(self.value, (int, float)):
            raise TemperatureError(self.value, self.scale)

    def _clean(self) -> None:
        self.value = int(round(self.value))

    def is_in_range(self, min: int, max: int, scale: TempScale = "F") -> bool:
        if self.scale == scale:
            return (min < self.value) and (self.value < max)
        else:
            error_msg = f"Temperature range must be of scale {self.scale}"
            raise TemperatureError(self.value, self.scale, error_msg)


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
        self.__post_init__()

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        error_msg = "Min may not be greater than max"
        if self.min.value > self.max.value:
            raise TempRangeError(self.min.value, self.max.value, error_msg)

    def __str__(self) -> str:
        return f"{self.min} \u2013 {self.max}"


@dataclass(slots=True, kw_only=True)
class Country:
    code: str
    name: str

    def __init__(self, code) -> None:
        self.code = code
        self.__post_init__()
        return

    def __str__(self) -> str:
        return self.name

    def __post_init__(self) -> None:
        self._validate()
        self.name = COUNTRIES[self.code]
        return

    def _clean(self):
        self.code = self.code.upper()
        self.code = self.code.strip()
        self.code = self.code.replace(" ", "")
        return

    def _validate(self) -> None:
        if not isinstance(self.code, str):
            error_msg = "Code must be a string!"
            raise CountryError(self.code, error_msg)

        self._clean()
        length_incorrect = len(self.code) != COUNTRY_CODE_LENGTH
        if length_incorrect:
            error_msg = "Code length is incorrect!"
            raise CountryError(self.code, error_msg)

        if self.code not in COUNTRIES.keys():
            error_msg = "Country code {self.code} is currently unsupported."
            raise CountryError(self.code, error_msg)


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
        lat_str = f"{abs(self.lat):.2f}\u00b0{ns}"
        long_str = f"{abs(self.long):.2f}\u00b0{ew}"
        return f"{lat_str} {long_str}"

    def _check_values(self) -> None:
        self._check_lat()
        self._check_long()

    def _check_lat(self) -> None:
        error_msg = "Latitude must be a number between -90 and 90"
        if not self._is_a_number(self.lat):
            raise LatLongError(self.lat, self.long, error_msg)
        lat_ok = self.lat < 90 and self.lat > -90
        if not lat_ok:
            raise LatLongError(self.lat, self.long, error_msg)
        return

    def _check_long(self) -> None:
        error_msg = "Longitude must be a number between -180 and 180"
        if not self._is_a_number(self.long):
            raise LatLongError(self.lat, self.long, error_msg)
        long_ok = self.long < 180 and self.long > -180
        if not long_ok:
            raise LatLongError(self.lat, self.long, error_msg)

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
