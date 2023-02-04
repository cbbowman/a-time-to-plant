from django.test import TestCase
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.location import ZipCode
from at2p_app.domain.value_objects.temperature import Temperature
from at2p_app.domain.value_objects.weather import Weather


class WeatherReportTest(TestCase):
    def setUp(self) -> None:
        place = Place.new(ZipCode.new("22405"))
        self.place_id = place.id
        self.high = Temperature.new(90)
        self.low = Temperature.new(50)
        self.avg = Temperature.new(65)
        self.weather = Weather.new(
            self.place_id, self.high, self.low, self.avg
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
            self.place_id,
            bad_value,
            self.low,
            self.avg,
        )
        self.assertRaises(
            WeatherError,
            Weather.new,
            self.place_id,
            self.high,
            bad_value,
            self.avg,
        )
        self.assertRaises(
            WeatherError,
            Weather.new,
            self.place_id,
            self.high,
            self.low,
            bad_value,
        )
