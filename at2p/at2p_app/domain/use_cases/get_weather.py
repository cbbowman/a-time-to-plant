from abc import ABC, abstractmethod
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.weather import Weather
from at2p_app.scrape import get_soup


class WeatherRetriever(ABC):
    @abstractmethod
    def get_weather(self) -> Weather:
        pass

class WeatherScraper(Weather):

    def get_weather(self, place: Place) -> Weather:

