from dataclasses import dataclass

COUNTRIES = {"US": "United States"}
COUNTRY_CODE_LENGTH = 2


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


class PlaceError(Exception):
    generic_msg = "Generic Place Error"

    def __init__(self, zip, country, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nZip: {zip}\nCountry: {country}"
        super().__init__(message)


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


@dataclass
class Place:
    zip: str
    country: Country = Country("US")
    state: str = None
    city: str = None
    coord: LatLong = None

    def __str__(self) -> str:
        return f"{self.zip}, {self.country}"

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._check_zip()
        self._check_country()

    def _check_zip(self):
        if not self._is_nonempty_string(self.zip):
            error_msg = "Zip code must be a non-empty string."
            raise PlaceError(self.zip, self.country, error_msg)

    def _check_country(self):
        if not isinstance(self.country, Country):
            error_msg = "Country argument must be an instance of 'Country'."
            raise PlaceError(self.zip, self.country, error_msg)

    def _is_nonempty_string(self, value) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) > 0
