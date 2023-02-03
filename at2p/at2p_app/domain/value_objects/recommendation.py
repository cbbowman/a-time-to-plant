from dataclasses import dataclass
from datetime import datetime
from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import RecommendationError
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.entities.place import Place
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Recommendation(ValueObject):
    place: Place
    crop: Crop
    recommended: bool
    margin: Temperature
    time_stamp: datetime

    @classmethod
    def new(
        cls, place: Place, crop: Crop, recommended: bool, margin: Temperature
    ):
        place, crop, recommended, margin = cls._validate(
            place, crop, recommended, margin
        )
        cls._clean()
        return cls(place, crop, recommended, margin, datetime.now())

    @classmethod
    def _validate(cls, place: Place, crop: Crop, recommended: bool, margin: Temperature):
        if not isinstance(place, Place):
            error_msg = "Place must be a Place!"
            raise RecommendationError(error_msg=error_msg)
        if not isinstance(crop, Crop):
            error_msg = "Crop must be a Crop!"
            raise RecommendationError(error_msg=error_msg)
        if not isinstance(recommended, bool):
            error_msg = "Recommended must be a bool!"
            raise RecommendationError(error_msg=error_msg)
        if not isinstance(margin, Temperature):
            error_msg = "Margin must be a temperature!"
            raise RecommendationError(error_msg=error_msg)
        return place, crop, recommended, margin

    @classmethod
    def _clean(cls):
        return

    def __str__(self) -> str:
        rec_str = (
            f"{self.crop}; {self.recommended}; "
            f"{self.margin}; {self.time_stamp}"
        )
        return rec_str

    def __repr__(self) -> str:
        return self.__str__()
