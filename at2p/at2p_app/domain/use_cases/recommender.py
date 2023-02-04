from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass
from at2p_app.domain.common.error import RecommenderError
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.recommendation import Recommendation
from at2p_app.domain.value_objects.weather import Weather


class CropRecommender(ABC):
    @abstractclassmethod
    def new(cls):
        pass

    @abstractclassmethod
    def _validate(cls):
        pass

    @abstractmethod
    def crop(self):
        pass


@dataclass
class SimpleRecommender(CropRecommender):

    _weather: Weather

    @classmethod
    def new(cls, weather):
        cls._validate(weather)
        return cls(weather)

    @classmethod
    def _validate(cls, weather):
        if not isinstance(weather, Weather):
            raise RecommenderError
        return

    def crop(self, crop: Crop) -> Recommendation:

        low = self._weather.low
        high = self._weather.high
        avg = self._weather.avg

        abs_max = crop.abs_range.max
        abs_min = crop.abs_range.min
        opt_min = crop.opt_range.min
        opt_max = crop.opt_range.max

        absolute_margin = min(abs_max - high, low - abs_min)
        optimal_margin = min(opt_max - avg, avg - opt_min)
        margin = min(absolute_margin, optimal_margin)
        recommended = margin.temp > 0
        return Recommendation.new(
            self._weather.place_id, crop, recommended, margin
        )
