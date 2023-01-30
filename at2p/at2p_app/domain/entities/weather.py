from dataclasses import dataclass
from enum import Enum, auto
from at2p_app.domain.entities.location import Place
from datetime import datetime


@dataclass
class TempScale(Enum):
    F = auto()
    C = auto()

    def __str__(self):
        return f"\u00b0{self.name}"


@dataclass
class WeatherReportType(Enum):
    FORECAST = auto()
    HISTORIC = auto()

    def __str__(self) -> str:
        return f"{self.name.title()}"


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


@dataclass(slots=True, order=True, eq=True)
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


@dataclass(slots=True, kw_only=True)
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
        if self.scale.value == t.scale.value:
            if isinstance(t, Temp):
                return (self.low < t.value) and (self.high > t.value)
            elif isinstance(t, TempRange):
                return (self.low < t.low) and (self.high > t.high)
            else:
                error_msg = "Argument must be of type Temp or TempScale"
                raise TempRangeError(
                    self.low, self.high, self.scale, error_msg
                )
        else:
            msg = "Comparison of \u00b0F to \u00b0C is unsupported"
            raise TempRangeError(self.low, self.high, self.scale, msg)


class WeatherReportError(Exception):
    generic_msg = "Generic Weather Report Error"

    def __init__(
        self, location: Place, time_reported: datetime, error_msg: str
    ) -> None:
        message = f"\n{error_msg}\nWeather Report for {location} created at {time_reported}"
        super().__init__(message)


@dataclass
class WeatherReport:
    location: Place
    highs: TempRange
    lows: TempRange
    report_type: WeatherReportType = WeatherReportType.FORECAST
    time_reported: datetime = datetime.now()

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._check_location()
        self._check_temps()
        self._check_type()
        self._check_time()

    def _check_location(self):
        if not isinstance(self.location, Place):
            msg = "Location is not an instance of class 'Place'"
            raise WeatherReportError(self.location, self.time_reported, msg)

    def _check_temps(self):
        lows_wrong = not isinstance(self.lows, TempRange)
        highs_wrong = not isinstance(self.highs, TempRange)
        if lows_wrong or highs_wrong:
            msg = "Highs or lows are not an instance of class 'TempRange'"
            raise WeatherReportError(self.location, self.time_reported, msg)

    def _check_type(self):
        if not isinstance(self.report_type, WeatherReportType):
            msg = (
                "Report type is not an instance of class 'WeatherReportType'"
            )
            raise WeatherReportError(self.location, self.time_reported, msg)

    def _check_time(self):
        if not isinstance(self.time_reported, datetime):
            msg = "Report time is not an instance of class 'datetime'"
            raise WeatherReportError(self.location, self.time_reported, msg)
