from abc import ABC, abstractmethod

from at2p_app.data_source.weather_source import Place, Weather, WeatherSource
from at2p_app.domain.common.error import WeatherError


class WeatherRetriever(ABC):

    _weather_source: WeatherSource

    @classmethod
    def new(cls, weather_source: WeatherSource):
        cls._validate(weather_source)
        return cls(weather_source)

    @classmethod
    def _validate(cls, weather_source: WeatherSource):
        if not isinstance(weather_source, WeatherSource):
            error_msg = "weather_source must be an instance of WeatherSource"
            raise WeatherError(error_msg)

    @abstractmethod
    def get_weather(self, place: Place) -> Weather:
        return self._weather_source.get(place)
