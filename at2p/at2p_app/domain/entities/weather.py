from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4, UUID
from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Weather(ValueObject):
    id: UUID
    location: Place
    high: Temperature
    low: Temperature
    avg: Temperature
    time_stamp: datetime

    @classmethod
    def new(cls, location, high, low, avg):
        location, high, low, avg = cls._validate(location, high, low, avg)
        id = uuid4()
        cls._clean()
        return cls(id, location, high, low, avg, datetime.now())

    @classmethod
    def _validate(cls, location, high, low, avg):

        if not isinstance(location, Place):
            error_msg = "Location must be an instance of Place"
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

        return location, high, low, avg

    @classmethod
    def _clean(cls):
        return
