from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from at2p_app.domain.entities.temperature import Temp, TempRange
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.crop import (
    Crop,
    TempRequirement,
)
from at2p_app.domain.entities.weather import WeatherReport
from at2p_app.domain.entities.recommendation import Recommendation, Confidence


class RequirementChecker(ABC):
    @abstractmethod
    def check_requirements(self):
        pass


class TempReqChecker(RequirementChecker):
    def __init__(
        self,
        reqs: TempRequirement,
        conf: Confidence = Confidence.HIGH,
    ) -> None:
        self.reqs = reqs
        self.conf = (100 - conf.value) / 100

    def check_requirements(
        self, forecast: WeatherReport, historic: WeatherReport
    ):
        forecast_ok = self.check_forecast(forecast)
        historic_ok = self.check_historic(historic)
        return forecast_ok and historic_ok

    def check_forecast(self, forecast: WeatherReport):
        adjusted_range = TempRange(
            self.reqs.optimal.low * (1 - self.conf),
            self.reqs.optimal.high * (1 + self.conf),
        )
        high_ok = self.reqs.absolute.high > forecast.highs.high
        low_ok = self.reqs.absolute.low < forecast.lows.low
        forecast_avg = Temp((forecast.highs.low + forecast.lows.high) / 2)
        optimal_ok = adjusted_range.includes(forecast_avg)
        crop_ok_to_plant = high_ok and low_ok and optimal_ok
        return crop_ok_to_plant

    def check_historic(
        self,
        historic: WeatherReport,
    ):
        adjusted_range = TempRange(
            self.reqs.optimal.low * (1 - self.conf),
            self.reqs.optimal.high * (1 + self.conf),
        )
        optimal_ok = adjusted_range.includes(historic.average)
        return optimal_ok


class CropRecommender(ABC):
    @abstractmethod
    def recommend_crops(self):
        raise NotImplementedError


class TempBasedRecommender(CropRecommender):
    def check_crop(
        self,
        crop: Crop,
        here: Place,
        confidence: Confidence = Confidence.HIGH,
    ) -> bool:
        checker = TempReqChecker(crop.reqs.get("temp"), confidence)
        crop_ok_to_plant = checker.check_requirements(
            here.forecast, here.historic
        )
        return crop_ok_to_plant

    def recommend_crops(
        self,
        crop_list: List[Crop],
        here: Place,
        confidence: Confidence = Confidence.HIGH,
    ) -> list:
        recommended_crops = []
        for c in crop_list:
            ok_to_plant = self.check_crop(
                c,
                here,
                confidence,
            )
            if ok_to_plant:
                print(c)
                print(here.forecast)
                print(here.historic)
                recommended_crops.append(c)
        return Recommendation(
            location=here,
            crops=tuple(crop_list),
            confidence=confidence,
            time_stamp=datetime.now(),
        )
