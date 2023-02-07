from dataclasses import dataclass

from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import CountryError, ZipCodeError

COUNTRIES = {"US": "United States"}
COUNTRY_CODE_LENGTH = 2


@dataclass(eq=True, slots=True, kw_only=True, frozen=True)
class Country(ValueObject):
    code: str
    name: str

    @classmethod
    def new(cls, code):
        code, name = cls._validate(code)
        return cls(code=code, name=name)

    @classmethod
    def _validate(cls, code):
        if not isinstance(code, str):
            error_msg = "Code must be a string!"
            raise CountryError(code=code, error_msg=error_msg)

        code = cls._clean(code=code)
        if not (code in COUNTRIES.keys()):
            error_msg = "Country code {code} is currently unsupported."
            raise CountryError(code=code, error_msg=error_msg)

        name = COUNTRIES[code]
        return code, name

    @classmethod
    def _clean(cls, code: str):
        code = code.strip()
        code = code.replace(" ", "")
        code = code.upper()
        return code

    def __str__(self) -> str:
        return self.name


@dataclass(eq=True, frozen=True)
class ZipCode(ValueObject):
    zip: str

    @classmethod
    def new(cls, zip):
        cls._validate(zip)
        cls._clean()
        return cls(zip)

    @classmethod
    def _validate(cls, code):
        if not isinstance(code, str):
            error_msg = "Code must be a string!"
            raise ZipCodeError(code=code, error_msg=error_msg)

    @classmethod
    def _clean(cls):
        pass

    def __str__(self) -> str:
        return self.zip

    def __repr__(self) -> str:
        return self.__str__()
