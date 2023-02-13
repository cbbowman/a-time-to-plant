"""ValueObject classes related to recommendations

Classes:
    CropName: an object for a the names of Crop objects
    Crop: an entity object representing a type of crop
"""
from dataclasses import dataclass
from uuid import UUID, uuid4

from at2p_app.domain.common.error import CropError
from at2p_app.domain.value_objects.temperature import TempRange


@dataclass(eq=True)
class CropName:
    """Class for storing the name of a Crop object

    Used for validation that the name of a Crop object is a non-empty
    string.

    Attributes:
        name: string
    """

    name: str

    @classmethod
    def new(cls, name: str):
        """Create a new CropName object

        Takes one string argument, validates it, cleans it, then return
        it.

        Arguments:
            name: str

        Returns:
           a CropName object
        """
        cls._validate(name)
        name = cls._clean(name)
        return cls(name)

    @classmethod
    def _validate(cls, name):
        """Validate a CropName

        Checks if the name is string, and not empty.

        Arguments:
            name: a string

        Return:
            a string 'name'

        Raises:
            ValueError if 'name' is not a non-empty string
        """
        if not isinstance(name, str):
            raise ValueError("name must be a string")

        if not len(name.strip()) > 0:
            error_msg = "Name may not be an empty string"
            raise ValueError(error_msg)
        return name

    @classmethod
    def _clean(cls, name: str):
        """Clean a crop name

        Strips the white space off the name, then makes it TitleCase.

        Arguments:
            name: a string

        Return:
            a string 'name'
        """
        name = name.strip()
        name = name.title()
        return name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(eq=True)
class Crop:
    """Class to represent a type of crop

    Includes a name, a UUID, and the germination temperature
    requirements.

    Attributes:
        name: a CropName object
        abs_range: a TempRange object
        opt_range: a TempRange object
    """
    name: CropName
    abs_range: TempRange
    opt_range: TempRange
    id: UUID

    @classmethod
    def new(
        cls,
        name: str,
        abs_range: TempRange,
        opt_range: TempRange,
        id: UUID = None,
    ):
        """Create a new Crop object

        Takes one string, two TempRange's, and an optional UUID,
        validates and cleans the arguments, then returns a new Crop
        object.

        Arguments:
            name: str
            abs_range:
            opt_range:
            id: an optional UUID

        Returns:
           a Crop object
        """
        cls._validate(abs_range, opt_range)
        name, id = cls._clean(name, id)
        return cls(name, abs_range, opt_range, id)

    @classmethod
    def _validate(cls, abs_range: TempRange, opt_range: TempRange):
        """Validate inputs for a new Crop

        Calls the _check_ranges method on abs_range and opt_range.

        Arguments:
            abs_range: a TempRange
            opt_range: a TempRange

        Return:
            None
        """
        cls._check_ranges(abs_range, opt_range)
        return

    @classmethod
    def _clean(cls, name: CropName, id: UUID):
        """Clean the inputs for a new Crop

        If name is not a CropName, creates one from it. If id is not a
        UUID, creates a new UUID. Then returns a CropName and a UUID.

        Arguments:
            name: a CropName object
            id: a UUID

        Return:
            a CropName object, and a UUID
        """
        if not isinstance(name, CropName):
            name = CropName.new(name)

        if not isinstance(id, UUID):
            id = uuid4()

        return name, id

    @classmethod
    def _check_ranges(cls, abs_range, opt_range):
        """Checks the TempRange objects for a new Crop

        Checks if abs_range and opt_range are instances of TempRange.

        Arguments:
            abs_range: a TempRange
            opt_range: a TempRange

        Return:
            None

        Raises:
            CropError if either argument is not a TempRange
        """
        if not isinstance(abs_range, TempRange):
            error_msg = "Absolute Range must be an instance of 'TempRange'."
            raise CropError(error_msg)

        if not isinstance(opt_range, TempRange):
            error_msg = "Optimal Range must be an instance of 'TempRange'."
            raise CropError(error_msg)

    @classmethod
    def new_from_dict(cls, d):
        return cls.new(**d)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return self.__str__()
