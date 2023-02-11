"""Value object classes related to weather

Classes:
    Weather: Value object representing a weather report
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Weather(ValueObject):
    """Value object representing a weather report

    Includes a reference to the place of interest, the high, low,
    and average temperatures, and a time-stamp.

    Attributes:
        place_id: the UUID of the relevant Place object
        high: a Temperature object
        low: a Temperature object
        avg: a Temperature object
        time_stamp: a datetime object
    """
    place_id: UUID
    high: Temperature
    low: Temperature
    avg: Temperature
    time_stamp: datetime

    @classmethod
    def new(cls, place_id, high, low, avg):
        """Create a new Weather value object

        Takes a Place UUID, and three Temperature objects, validates and
        cleans, then returns a Weather value object.

        Arguments:
            place_id: a UUID
            high: a Temperature object
            low: Temperature object
            avg: Temperature object

        Returns:
            a Weather object
        """
        place_id, high, low, avg = cls._validate(place_id, high, low, avg)
        cls._clean()
        return cls(place_id, high, low, avg, datetime.now())

    @classmethod
    def _validate(cls, place_id, high, low, avg):
        """Create a new Weather value object

        Takes a Place UUID, and three Temperature objects, validates
        them, then returns them.

        Arguments:
            place_id: a UUID
            high: a Temperature object
            low: Temperature object
            avg: Temperature object

        Returns:
            a Weather object

        Raises:
            a TemperatureError if the argument types are incorrect
        """
        if not isinstance(place_id, UUID):
            error_msg = "place_id must be a UUID"
            raise WeatherError(error_msg)

        if not isinstance(high, Temperature):
            error_msg = "High must be an instance of Temperature"
            raise WeatherError(error_msg)

        if not isinstance(low, Temperature):
            error_msg = "High must be an instance of Temperature"
            raise WeatherError(error_msg)

        if not isinstance(avg, Temperature):
            error_msg = "High must be an instance of Temperature"
            raise WeatherError(error_msg)

        return place_id, high, low, avg

    @classmethod
    def _clean(cls):
        return

    def __str__(self) -> str:
        id = f"ID: {self.place_id.__str__()}"
        high = f"High: {self.high.__str__()}"
        low = f"Low: {self.low.__str__()}"
        avg = f"Average: {self.avg.__str__()}"
        time_stamp = f"Time-stamp: {self.time_stamp.isoformat()}"
        return f"\n{id}\n{high}\n{low}\n{avg}\n{time_stamp}\n"
