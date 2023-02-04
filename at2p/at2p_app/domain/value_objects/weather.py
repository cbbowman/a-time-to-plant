from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Weather(ValueObject):
    place_id: UUID
    high: Temperature
    low: Temperature
    avg: Temperature
    time_stamp: datetime

    @classmethod
    def new(cls, place_id, high, low, avg):

        place_id, high, low, avg = cls._validate(place_id, high, low, avg)
        cls._clean()
        return cls(place_id, high, low, avg, datetime.now())

    @classmethod
    def _validate(cls, place_id, high, low, avg):

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
