from dataclasses import dataclass
from enum import Enum, auto
from at2p_app.domain.entities.temperature import (
    Temp,
    TempRange,
)
from at2p_app.domain.entities.location import Place
from datetime import datetime


@dataclass
class WeatherReportType(Enum):
    FORECAST = auto()
    HISTORIC = auto()

    def __str__(self) -> str:
        return f"{self.name.capitalize()}"


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
    highs: TempRange = None
    lows: TempRange = None
    average: Temp = None
    report_type: WeatherReportType = WeatherReportType.FORECAST
    time_reported: datetime = datetime.now()

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._check_location()
        self._check_type()
        self._check_time()
        if self.highs is not None:
            self._check_highs()
        if self.lows is not None:
            self._check_lows()
        if self.average is not None:
            self._check_average()

    def _check_location(self):
        if not isinstance(self.location, Place):
            msg = "Location is not an instance of class 'Place'"
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

    def _check_highs(self):
        if not isinstance(self.highs, TempRange):
            msg = "Highs are not an instance of class 'TempRange'"
            raise WeatherReportError(self.location, self.time_reported, msg)

    def _check_lows(self):
        if not isinstance(self.lows, TempRange):
            msg = "Lows are not an instance of class 'TempRange'"
            raise WeatherReportError(self.location, self.time_reported, msg)

    def _check_average(self):
        if not isinstance(self.average, Temp):
            msg = "Average is not an instance of class 'Temp'"
            raise WeatherReportError(self.location, self.time_reported, msg)
