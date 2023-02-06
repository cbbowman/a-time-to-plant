from django.test import TestCase
from at2p_app.data_source.weather_source import WeatherScraper
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.weather import Weather


class WeatherScraperTests(TestCase):
    def setUp(self) -> None:
        place = Place.new("22405")
        self.scraper = WeatherScraper.new(place)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.scraper, WeatherScraper)

    def test_get_weather(self):
        weather = self.scraper.get()
        self.assertIsInstance(weather, Weather)
