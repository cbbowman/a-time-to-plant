from django.test import TestCase
from datetime import datetime
from at2p_app.domain.value_objects.recommendation import Recommendation
from at2p_app.domain.value_objects.temperature import TempRange, Temperature
from at2p_app.domain.value_objects.location import ZipCode
from at2p_app.domain.entities.place import Place

from at2p_app.domain.entities.crop import Crop


class RecommendationTests(TestCase):
    def setUp(self) -> None:
        self.zip = ZipCode.new("22407")
        self.place = Place.new(zip_code=self.zip)

        self.crop = Crop(
            id=73,
            name="Boberries",
            abs_range=TempRange.new(40, 80),
            opt_range=TempRange.new(65, 75),
        )

        self.r = Recommendation.new(self.place, self.crop, True, Temperature.new(40))
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.r, Recommendation)
        self.assertTrue(self.r.recommended)
        self.assertEqual(self.r.margin, Temperature.new(40))
        self.assertIsInstance(self.r.time_stamp, datetime)
