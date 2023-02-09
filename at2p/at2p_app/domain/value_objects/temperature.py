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
        cls._validate(temp, scale)
        temp = cls._clean(temp)
        return cls(temp, scale)

    @classmethod
    def _validate(cls, temp: int | float, scale: TempScale):
        if not isinstance(temp, int | float):
            raise TemperatureError()
        if not isinstance(scale, TempScale):
            raise TemperatureError()

    @classmethod
    def _clean(cls, temp):
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
        cls._validate(min, max, scale)
        min, max = cls._clean(min, max, scale)
        return cls(min, max, scale)

    @classmethod
    def _validate(cls, min: int | float, max: int | float, scale: TempScale):
        if not isinstance(min, int | float):
            raise TemperatureError()
        if not isinstance(max, int | float):
            raise TemperatureError()
        if not isinstance(scale, TempScale):
            raise TemperatureError()

    @classmethod
    def _clean(cls, min, max, scale):
        min = Temperature.new(min, scale)
        max = Temperature.new(max, scale)
        return min, max

    def __str__(self) -> str:
        return f"{self.min.temp} \u2013 {self.max.temp} {self.scale}"

    def __repr__(self) -> str:
        return self.__str__()

    def includes_temp(self, t: Temperature):
        if not isinstance(t, Temperature):
            raise TemperatureError()
        return self.min < t and t < self.max

    def includes_range(self, r):
        if not isinstance(r, TempRange):
            raise TemperatureError()
        return not (r.max > self.max or self.min > r.min)
