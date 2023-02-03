from django.test import TestCase
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.value_objects.temperature import Temperature
from at2p_app.domain.value_objects.location import ZipCode
from at2p_app.domain.entities.weather import Weather
from at2p_app.domain.entities.place import Place


class WeatherReportTest(TestCase):
    def setUp(self) -> None:
        self.location = Place.new(ZipCode.new("22405"))
        self.high = Temperature.new(90)
        self.low = Temperature.new(50)
        self.avg = Temperature.new(65)
        self.weather = Weather.new(
            self.location, self.high, self.low, self.avg
        )
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.weather, Weather)

    def test_validation(self):
        bad_value = "bad value"
        self.assertRaises(
            WeatherError,
            Weather.new,
            bad_value,
            self.high,
            self.low,
            self.avg,
        )
        self.assertRaises(
            WeatherError,
            Weather.new,
            self.location,
            bad_value,
            self.low,
            self.avg,
        )
        self.assertRaises(
            WeatherError,
            Weather.new,
            self.location,
            self.high,
            bad_value,
            self.avg,
        )
        self.assertRaises(
            WeatherError,
            Weather.new,
            self.location,
            self.high,
            self.low,
            bad_value,
        )
