"""ValueObject classes related to temperatures

Classes:
    TempScale : Enum class for Farenheit or Celsius
    Temperature : Value object representing a temperature
    TempRange : Value object representing a temperature range
"""
from dataclasses import dataclass
from enum import Enum, auto

from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import TemperatureError


class TempScale(Enum):
    """Enum class for Farenheit or Celsius scales

    Used in the Temperature value object to represent which temperature
    scale the value is using.

    Attributes:
        F: Value representing Farenheit
        C: Value representing Celsius
    """

    F = auto()
    C = auto()

    def __str__(self):
        """__str__ method for TempScale object

        Returns:
            string: degree symbol and F or C
        """
        return f"\u00B0{self.name}"

    def __repr__(self):
        """__repr__ method for TempScale object

        Returns:
            string: degree symbol and F or C
        """
        return self.__str__()


@dataclass(eq=True, order=True, frozen=True)
class Temperature(ValueObject):
    """Value object representing a temperature value

    Uses an int to represent the degrees, and a TempScale object to
    represent the scale (Farenheit or Celsius)

    Attributes:
        temp: an int
        scale: a TempScale
    """

    temp: int
    scale: TempScale

    @classmethod
    def new(cls, temp: int | float, scale: TempScale = TempScale.F):
        """Create a new Temperature value object

        Takes an int or float, and a TempScale, validates and cleans,
        then returns a Temperature value object.

        Arguments:
            temp: an int or float
            scale: a TempScale

        Returns:
            Temperature value object
        """
        cls._validate(temp, scale)
        temp = cls._clean(temp)
        return cls(temp, scale)

    @classmethod
    def _validate(cls, temp: int | float, scale: TempScale):
        """Validate arguments for a new Temperature object

        Checks if the temp is an int or float, and checks if the scale
        is a TempScale object.

        Arguments:
            temp: submitted temperature value
            scale: submitted temperature scale

        Returns:
            None

        Raises:
            TemperatureError: if temp is not an int or float, or if
                scale is not a TempScale object
        """
        if not isinstance(temp, int | float):
            raise TemperatureError()
        if not isinstance(scale, TempScale):
            raise TemperatureError()

    @classmethod
    def _clean(cls, temp):
        """Cleans number argument for a new Temperature object

        Value is rounded to a whole number and cast as an integer.

        Arguments:
            temp: submitted temperature value

        Returns:
           An integer
        """
        return int(round(temp))

    def __str__(self) -> str:
        return f"{self.temp} {self.scale}"

    def __repr__(self) -> str:
        return self.__str__()

    def __sub__(self, other):
        return Temperature.new(self.temp - other.temp)

    def __add__(self, other):
        return Temperature.new(self.temp + other.temp)


@dataclass(frozen=True, eq=True)
class TempRange(ValueObject):
    """Value object representing a temperature range

    Two Temperature objects, 'min' and 'max' and the TempScale value
    of the two temperatures.

    Attributes:
        min: a Temperature
        max: a Temperature
        scale: the TempScale value of min and max
    """

    min: Temperature
    max: Temperature
    scale: TempScale

    @classmethod
    def new(
        cls,
        min: int | float,
        max: int | float,
        scale: TempScale = TempScale.F,
    ):
        """Create a new TempRange object

        Accepts two numbers and a scale (defaults to F) and returns a
        TempRange object.

        Arguments:
            min: int or float
            max: int or float
            scale: a TempScale, default to F

        Returns:
            a TempRange object
        """
        cls._validate(min, max, scale)
        min, max = cls._clean(min, max, scale)
        return cls(min, max, scale)

    @classmethod
    def _validate(cls, min: int | float, max: int | float, scale: TempScale):
        """Validate arguments for a new TempRange object

        Checks if min and max are numbers, and checks if scale is a
        TempScale object.

        Arguments:
            min: int or float
            max: int or float
            scale: a TempScale

        Returns:
            a TempRange object

        Raises:
            TemperatureError if min or max are not int or float, or if
            scale is not a TempScale object
        """
        if not isinstance(min, int | float):
            raise TemperatureError()
        if not isinstance(max, int | float):
            raise TemperatureError()
        if not isinstance(scale, TempScale):
            raise TemperatureError()

    @classmethod
    def _clean(cls, min, max, scale):
        """Cleans arguments for a new TempRange object

        Creates two Temperature objects for the min and max of the
        TempRange object.

        Arguments:
            min: int or float
            max: int or float
            scale: a TempScale object

        Returns:
            two Temperature objects, min and max
        """
        min = Temperature.new(min, scale)
        max = Temperature.new(max, scale)
        return min, max

    def __str__(self) -> str:
        return f"{self.min.temp} \u2013 {self.max.temp} {self.scale}"

    def __repr__(self) -> str:
        return self.__str__()

    def includes_temp(self, t: Temperature):
        """Checks if a temperature is within the range

        First checks if 't' is a Temperature object, then returns a
        bool, False if the Temp is outside the TempRange, True otherwise.

        Arguments:
            t: Temperature object

        Returns:
            a boolean value

        Raise:
            TemperatureError if t is not a Temperature object

        """
        if not isinstance(t, Temperature):
            raise TemperatureError()
        return self.min < t and t < self.max

    def includes_range(self, r):
        """Checks if a TemperatureRange object is within the range

        First checks if 'r' is a TempRange object, then returns a
        bool, False if the TempRange is outside the range, True
        otherwise.

        Arguments:
            r: TempRange object

        Returns:
            a boolean value

        Raises:
            TemperatureError if t is not a TempRange object
        """
        if not isinstance(r, TempRange):
            raise TemperatureError()
        return not (r.max > self.max or self.min > r.min)
