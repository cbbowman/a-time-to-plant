from dataclasses import dataclass, field
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.weather import Weather
from at2p_app.domain.value_objects.location import ZipCode, Country


class PlaceError(Exception):
    generic_msg = "Generic Place Error"

    def __init__(self, zip, country, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\nZip: {zip}\nCountry: {country}"
        super().__init__(message)


@dataclass(eq=True)
class Place:
    zip: ZipCode
    country: Country = Country.new("US")
    crops: list = field(default_factory=list)
    weather: Weather = None

    def __str__(self) -> str:
        return f"{self.zip}, {self.country}"

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._check_zip()
        self._check_country()
        self._check_crops()
        self._check_weather()

    def _check_zip(self):
        if not isinstance(self.zip, ZipCode):
            error_msg = "Zip code must be an instance of ZipCode"
            raise PlaceError(self.zip, self.country, error_msg)

    def _check_country(self):
        if not isinstance(self.country, Country):
            error_msg = "Country argument must be an instance of 'Country'."
            raise PlaceError(self.zip, self.country, error_msg)

    def _check_crops(self):
        if not isinstance(self.crops, list):
            error_msg = "Crops argument must be an instance of list"
            raise PlaceError(self.zip, self.country, error_msg)
        for c in self.crops:
            if not isinstance(c, Crop):
                error_msg = "Crops argument must be a list of Crops"
                raise PlaceError(self.zip, self.country, error_msg)

    def _check_weather(self):
        if not isinstance(self.weather, Weather | None):
            error_msg = "Weather argument must be an instance of 'Weather'."
            raise PlaceError(self.zip, self.country, error_msg)

    def _is_nonempty_string(self, value) -> bool:
        if not isinstance(value, str):
            return False
        return len(value) > 0
