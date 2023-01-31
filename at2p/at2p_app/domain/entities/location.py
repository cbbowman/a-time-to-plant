from dataclasses import dataclass
from at2p_app.domain.entities.lat_long import LatLong
from at2p_app.domain.entities.weather import WeatherReport

COUNTRIES = {"US": "United States"}
COUNTRY_CODE_LENGTH = 2


class CountryError(Exception):
    generic_msg = "Generic Country Error"

    def __init__(self, code: str, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nCode: {code}"
        super().__init__(message)


class PlaceError(Exception):
    generic_msg = "Generic Place Error"

    def __init__(self, zip, country, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nZip: {zip}\nCountry: {country}"
        super().__init__(message)


@dataclass(eq=True, slots=True, kw_only=True)
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

        if not (self.code in COUNTRIES.keys()):
            error_msg = "Country code {self.code} is currently unsupported."
            raise CountryError(self.code, error_msg)


@dataclass(eq=True)
class Place:
    zip: str
    country: Country = Country("US")
    state: str = None
    city: str = None
    coord: LatLong = None
    forecast: WeatherReport = None
    historic: WeatherReport = None

    def __str__(self) -> str:
        return f"{self.zip}, {self.country}"

    def __post_init__(self):
        self.id = hash(f"{self.zip}{self.country}")
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
