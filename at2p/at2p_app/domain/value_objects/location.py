"""ValueObject classes related to location

Classes:
    Country: Value object representing a country
    ZipCode: Value object representing a ZIP code
"""
from dataclasses import dataclass

from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import CountryError, ZipCodeError

COUNTRIES = {"US": "United States"}
COUNTRY_CODE_LENGTH = 2


@dataclass(eq=True, slots=True, kw_only=True, frozen=True)
class Country(ValueObject):
    """Value object with a country name and short code

    The name can be a long string. The code must be an upper case,
    two-character string

    Attributes:
        code: string
        name: string
    """
    code: str
    name: str

    @classmethod
    def new(cls, code):
        """Create a new Country object

        Takes a two character country code, validates the values, and
        returns a Country object with the properly formatted name and code.

        Arguments:
            code: str

        Returns:
            Country object
        """
        code, name = cls._validate(code)
        return cls(code=code, name=name)

    @classmethod
    def _validate(cls, code):
        """Validate a country code

        Checks if the code is a string, cleans the code, checks if the code
        is supported, then returns the corresponding country name and
        formatted code.

        Arguments:
            code: str

        Returns:
            two strings, 'code' and 'name'

        Raises:
            CountryError: if code is not a string or an unsupported country
        """
        if not isinstance(code, str):
            error_msg = "Code must be a string!"
            raise CountryError(code=code, error_msg=error_msg)

        code = cls._clean(code=code)
        if code not in COUNTRIES:
            error_msg = "Country code {code} is currently unsupported."
            raise CountryError(code=code, error_msg=error_msg)

        name = COUNTRIES[code]
        return code, name

    @classmethod
    def _clean(cls, code: str):
        """Clean a country code

        Strips off white space, and converts the code to uppercase.

        Arguments:
            code: string

        Returns:
            string 'code'
        """
        code = code.strip()
        code = code.replace(" ", "")
        code = code.upper()
        return code

    def __str__(self) -> str:
        return self.name


@dataclass(eq=True, frozen=True)
class ZipCode(ValueObject):
    """Value object with a ZIP code string attribute

    Attributes:
        zip: string
    """
    zip: str

    @classmethod
    def new(cls, zip):
        """Create a new ZipCode object

        Takes a zip code string, validates the value, and
        returns a ZipCode object.

        Arguments:
            zip: string

        Returns:
            ZipCode object
        """
        cls._validate(zip)
        cls._clean()
        return cls(zip)

    @classmethod
    def _validate(cls, code):
        """Validate a ZIP code

        Checks if the code is a string.

        Arguments:
            code: str

        Returns:
        string 'code'

        Raises:
            ZipCodeError: if code is not a string
        """
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
