from datetime import datetime
from django.test import TestCase
from at2p_app.domain.entities.crop import Crop, TempRequirement, ReqList
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.recommendation import Recommendation, Confidence


class TestRecommendation(TestCase):
    def setUp(self) -> None:
        self.place = Place(zip="22407")
        req = TempRequirement()
        self.reqs = ReqList(temp=req)
        self.crop_name_1 = "Boberries"
        self.crop_name_2 = "Carrots"
        self.crop_name_3 = "Peppers"
        self.crop_1 = Crop(name=self.crop_name_1, reqs=self.reqs)
        self.crop_2 = Crop(name=self.crop_name_2, reqs=self.reqs)
        self.crop_3 = Crop(name=self.crop_name_3, reqs=self.reqs)
        self.crops = [self.crop_1, self.crop_2, self.crop_3]

        self.recommendation = Recommendation(
            location=self.place,
            crops=self.crops,
            confidence=Confidence.MODERATE,
            time_stamp=datetime.now(),
        )
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.recommendation, Recommendation)
        self.assertEqual(self.recommendation.confidence.__str__(), "Moderate")
