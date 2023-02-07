from unittest import TestCase
from at2p_app.domain.common.error import RecommenderError
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.entities.place import Place
from at2p_app.domain.use_cases.recommender import (
    SimpleRecommender,
    CropRecommender,
)
from at2p_app.domain.value_objects.location import ZipCode
from at2p_app.domain.value_objects.recommendation import Recommendation
from at2p_app.domain.value_objects.temperature import TempRange, Temperature
from at2p_app.domain.value_objects.weather import Weather


class CropRecommenderTests(TestCase):
    def setUp(self) -> None:
        self.zip = ZipCode.new("22407")
        self.place = Place.new(self.zip)

        self.crop = Crop.new(
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )
        self.weather = Weather.new(
            place_id=self.place.id,
            high=Temperature.new(79),
            low=Temperature.new(41),
            avg=Temperature.new(70),
        )
        self.recommender = SimpleRecommender.new(self.weather)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.recommender, CropRecommender)

    def test_validation(self):
        self.assertRaises(RecommenderError, SimpleRecommender.new, "weather")

    def test_recommendation(self):
        r = self.recommender.crop(self.crop)
        self.assertIsInstance(r, Recommendation)
        self.assertTrue(r.recommended)
        self.assertTrue(r.margin.temp > 0)

        crop = Crop.new(
            name="Boberries",
            abs_range=TempRange.new(45, 80),
            opt_range=TempRange.new(65, 75),
        )
        r = self.recommender.crop(crop)
        self.assertFalse(r.recommended)
        self.assertTrue(r.margin.temp < 0)
