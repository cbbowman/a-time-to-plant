from unittest import TestCase
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.recommendation import Recommendation
from at2p_app.domain.value_objects.temperature import TempRange, Temperature
from at2p_app.domain.common.error import RecommendationError


class RecommendationTests(TestCase):
    def setUp(self) -> None:
        self.place = Place.new("22407")

        self.crop = Crop.new(
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )

        self.r = Recommendation.new(
            self.place.id, self.crop, True, Temperature.new(40)
        )
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.r, Recommendation)
        r_str = f"{self.place.id.int}; {self.crop}; {self.r.time_stamp}"
        self.assertEqual(self.r.__str__(), r_str)
        self.assertEqual(self.r.__repr__(), r_str)

    def test_validation(self):
        bad_value = "Bad Value"
        self.assertRaises(
            RecommendationError,
            Recommendation.new,
            bad_value,
            self.crop,
            True,
            Temperature.new(40),
        )

        self.assertRaises(
            RecommendationError,
            Recommendation.new,
            self.place.id,
            bad_value,
            True,
            Temperature.new(40),
        )

        self.assertRaises(
            RecommendationError,
            Recommendation.new,
            self.place.id,
            self.crop,
            bad_value,
            Temperature.new(40),
        )

        self.assertRaises(
            RecommendationError,
            Recommendation.new,
            self.place.id,
            self.crop,
            True,
            bad_value,
        )
