from dataclasses import dataclass
from uuid import uuid4, UUID
from at2p_app.domain.value_objects.location import ZipCode, Country
from at2p_app.domain.value_objects.weather import Weather


@dataclass(eq=True)
class Place:
    id: UUID
    zip_code: ZipCode
    country: Country
    weather_id: int

    @classmethod
    def new(
        cls,
        zip_code: ZipCode,
        country: Country = Country.new("US"),
        weather_id: Weather = None,
        id: UUID = None,
    ):
        cls._validate()
        if id is None:
            id = uuid4()
        zip_code, country = cls._clean(zip_code, country)
        return cls(id, zip_code, country, weather_id)

    @classmethod
    def _validate(cls):
        pass

    @classmethod
    def _clean(cls, zip_code: ZipCode, country: Country):
        zip_code = cls._check_zip(zip_code)
        country = cls._check_country(country)
        return zip_code, country

    @classmethod
    def _check_zip(cls, zip_code):
        if not isinstance(zip_code, ZipCode):
            return ZipCode.new(zip_code)
        return zip_code

    @classmethod
    def _check_country(cls, country):
        if not isinstance(country, Country):
            return Country.new(country)
        return country

    def __str__(self) -> str:
        return f"{self.zip_code}, {self.country.code}"

    def __repr__(self) -> str:
        return self.__str__()
