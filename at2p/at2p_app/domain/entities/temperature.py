from dataclasses import dataclass
from enum import Enum, auto


@dataclass(eq=True)
class TempScale(Enum):
    F = auto()
    C = auto()

    def __str__(self):
        return f"\u00b0{self.name}"


class TemperatureError(Exception):
    error_msg = "Generic Temperature Error"

    def __init__(
        self, temp: int, scale: TempScale, error_msg: str = error_msg
    ) -> None:
        message = f"\n{error_msg}\nTemp: {temp} {scale}\n"
        super().__init__(message)


class TempRangeError(Exception):
    generic_msg = "Generic Temperature Range Error"

    def __init__(
        self,
        low: int,
        high: int,
        scale: TempScale,
        error_msg: str = generic_msg,
    ) -> None:
        message = f"\n{error_msg} {low} \u2013 {high} {scale}"
        super().__init__(message)


@dataclass(eq=True, order=True, slots=True)
class Temp:
    """Class for temperate value"""

    value: int
    scale: TempScale = TempScale.F

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __str__(self) -> str:
        return f"{self.value} {self.scale}"

    def __post_init__(self) -> None:
        self._validate()
        self._clean()

    def _validate(self) -> None:
        if not isinstance(self.value, (int, float)):
            raise TemperatureError(self.value, self.scale)

    def _clean(self) -> None:
        self.value = int(round(self.value))

    def is_in_range(
        self, low: int, high: int, scale: TempScale = TempScale.F
    ) -> bool:
        if self.scale.value == scale.value:
            return (low < self.value) and (self.value < high)
        else:
            error_msg = f"Temperature range must be of scale {self.scale}"
            raise TemperatureError(self, error_msg)


@dataclass(eq=True, order=True, kw_only=True, slots=True)
class TempRange:
    """Class for a range of temperatures"""

    low: int
    high: int
    scale: TempScale

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __init__(self, low, high, scale=TempScale.F) -> None:
        self.low = low
        self.high = high
        self.scale = scale
        self.__post_init__()

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.low > self.high:
            error_msg = "'Low' may not be greater than 'high'"
            raise TempRangeError(self.low, self.high, self.scale, error_msg)

    def __str__(self) -> str:
        return f"{self.low} \u2013 {self.high} {self.scale}"

    def includes(self, t: any) -> bool:
        type_supported = isinstance(t, Temp) or isinstance(t, TempRange)
        if not type_supported:
            error_msg = "Argument must be of type Temp or TempScale"
            raise TempRangeError(self.low, self.high, self.scale, error_msg)

        if self.scale.value != t.scale.value:
            msg = "Comparison of \u00b0F to \u00b0C is unsupported"
            raise TempRangeError(self.low, self.high, self.scale, msg)

        if isinstance(t, Temp):
            return (self.low < t.value) and (self.high > t.value)
        else:
            return (self.low < t.low) and (self.high > t.high)
