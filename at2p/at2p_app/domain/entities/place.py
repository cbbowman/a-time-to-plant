from dataclasses import dataclass
# from dataclasses import dataclass, field
# from at2p_app.domain.entities.crop import Crop
# from at2p_app.domain.value_objects.weather import Weather
from at2p_app.domain.value_objects.location import ZipCode, Country
from uuid import uuid4


class PlaceError(Exception):
    generic_msg = "Generic Place Error"

    def __init__(self, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\n"
        super().__init__(message)


@dataclass(eq=True)
class Place:
    id: int
    zip_code: ZipCode
    country: Country = Country.new("US")
    # crops: list = field(default_factory=list)
    # weather: Weather = None

    @classmethod
    def new(cls, zip_code: ZipCode, country: Country = Country.new("US")):
        zip_code, country = cls._validate(zip_code, country)
        return cls(uuid4().int, zip_code, country)

    @classmethod
    def _validate(cls, zip_code: ZipCode, country: Country):
        zip_code = cls._check_zip(zip_code)
        country = cls._check_country(country)
        return zip_code, country

    @classmethod
    def _clean(cls):
        pass

    @classmethod
    def _check_zip(cls, zip_code):
        if not isinstance(zip_code, ZipCode):
            error_msg = "Zip code must be an instance of ZipCode"
            raise PlaceError(error_msg)
        return zip_code

    @classmethod
    def _check_country(cls, country):
        if not isinstance(country, Country):
            error_msg = "Country argument must be an instance of 'Country'."
            raise PlaceError(error_msg)
        return country

    def __str__(self) -> str:
        return f"{self.zip_code}, {self.country.code}"

    def __repr__(self) -> str:
        return self.__str__()
