from django.test import TestCase
from at2p_app.domain.entities.temperature import Temp, TempRange
from at2p_app.domain.entities.weather import WeatherReport, WeatherReportType
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.recommendation import Recommendation, Confidence
from at2p_app.domain.use_cases.crop_interface import CropInterface
from at2p_app.adapters.repositories import TestingCropRepo
from at2p_app.domain.use_cases.recommending import (
    CropRecommender,
    TempBasedRecommender,
)


class TestCropRecommender(TestCase):
    def setUp(self) -> None:
        self.repo = TestingCropRepo()
        self.interface = CropInterface(self.repo)
        self.available_crops = self.interface.import_crops()

        init_dict = {
            "report_type": WeatherReportType.FORECAST,
            "highs": TempRange(74, 77),
            "lows": TempRange(70, 74),
        }
        self.forecast = WeatherReport.from_dict(init_dict)

        init_dict = {
            "report_type": WeatherReportType.HISTORIC,
            "average": Temp(74),
        }
        self.historic = WeatherReport.from_dict(init_dict)
        self.location = Place(
            "22407", forecast=self.forecast, historic=self.historic
        )

        self.recommender = TempBasedRecommender()
        self.confidence = Confidence.HIGH
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.recommender, CropRecommender)

    def test_recommender(self):
        recomended_crops = self.recommender.recommend_crops(
            self.available_crops,
            self.location,
            confidence=self.confidence,
        )
        self.assertIsInstance(recomended_crops, Recommendation)
        print(len(recomended_crops.crops))

        for c in recomended_crops.crops:
            crop_ok = self.recommender.check_crop(
                c, here=self.location, confidence=self.confidence
            )
            print(c)
            self.assertTrue(crop_ok)
