from django.test import TestCase
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.use_cases.recommending import CropRecommender
from at2p_app.domain.value_objects.temperature import TempRange, Temperature
from at2p_app.domain.value_objects.weather import Weather
from at2p_app.domain.value_objects.recommendation import Recommendation


class CropRecommenderTests(TestCase):
    def setUp(self) -> None:
        self.crop = Crop(
            id=73,
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )
        self.weather = Weather(
            high=Temperature.new(79), low=Temperature.new(41), avg=Temperature.new(70)
        )
        self.recommender = CropRecommender(weather=self.weather)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.recommender, CropRecommender)

    def test_recommendation(self):
        r = self.recommender.crop(self.crop)
        self.assertIsInstance(r, Recommendation)
        self.assertTrue(r.recommended)
        self.assertTrue(r.margin.temp > 0)

        crop = Crop(
            id=73,
            name="Boberries",
            abs_range=TempRange.new(45, 80),
            opt_range=TempRange.new(65, 75),
        )
        r = self.recommender.crop(crop)
        self.assertFalse(r.recommended)
        self.assertTrue(r.margin.temp < 0)