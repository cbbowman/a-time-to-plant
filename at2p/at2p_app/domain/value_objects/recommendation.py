from dataclasses import dataclass
from datetime import datetime
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.value_objects.temperature import Temperature


class RecommendationError(Exception):
    error_msg = "Generic Recommendation Error"

    def __init__(self, error_msg: str = error_msg) -> None:
        super().__init__(error_msg)


@dataclass(frozen=True)
class Recommendation(ValueObject):
    crop: Crop
    recommended: bool
    margin: Temperature
    time_stamp: datetime

    @classmethod
    def new(cls, crop: Crop, recommended: bool, margin: Temperature):
        crop, recommended, margin = cls._validate(crop, recommended, margin)
        return cls(crop, recommended, margin, datetime.now())

    @classmethod
    def _validate(cls, crop: Crop, recommended: bool, margin: Temperature):
        if not isinstance(crop, Crop):
            error_msg = "Crop must be a Crop!"
            raise RecommendationError(error_msg=error_msg)
        if not isinstance(recommended, bool):
            error_msg = "Recommended must be a bool!"
            raise RecommendationError(error_msg=error_msg)
        if not isinstance(margin, Temperature):
            error_msg = "Margin must be a temperature!"
            raise RecommendationError(error_msg=error_msg)
        return crop, recommended, margin

    @classmethod
    def _clean(cls, code: str):
        return

    def __str__(self) -> str:
        return f"{self.crop}; {self.recommended}; {self.margin}; {self.time_stamp}"

    def __repr__(self) -> str:
        return self.__str__()
