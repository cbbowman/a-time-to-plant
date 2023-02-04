from abc import ABC, abstractmethod
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.weather import Weather


class WeatherGenerator(ABC):
    @abstractmethod
    def get_weather(self, place: Place) -> Weather:
        pass
