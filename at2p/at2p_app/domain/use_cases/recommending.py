from at2p_app.domain.value_objects.recommendation import Recommendation
from at2p_app.domain.value_objects.temperature import Temperature
from at2p_app.domain.value_objects.weather import Weather
from at2p_app.domain.entities.crop import Crop


class CropRecommender:
    def __init__(self, weather: Weather) -> None:
        self._weather = weather

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
            self._weather.location, crop, recommended, margin
        )
