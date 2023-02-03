from dataclasses import dataclass
from at2p_app.domain.value_objects.location import ZipCode, Country
from at2p_app.domain.common.error import PlaceError
from uuid import uuid4


@dataclass(eq=True)
class Place:
    id: int
    zip_code: ZipCode
    country: Country = Country.new("US")

    @classmethod
    def new(cls, zip_code: ZipCode, country: Country = Country.new("US")):
        zip_code, country = cls._validate(zip_code, country)
        id = uuid4().int % 10**9
        cls._clean()
        return cls(id, zip_code, country)

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
