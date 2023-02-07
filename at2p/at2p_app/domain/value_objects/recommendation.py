from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import RecommendationError
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Recommendation(ValueObject):
    place_id: UUID
    crop: Crop
    recommended: bool
    margin: Temperature
    time_stamp: datetime

    @classmethod
    def new(
        cls,
        place_id: UUID,
        crop: Crop,
        recommended: bool,
        margin: Temperature,
    ):
        place_id, crop, recommended, margin = cls._validate(
            place_id, crop, recommended, margin
        )
        cls._clean()
        return cls(place_id, crop, recommended, margin, datetime.now())

    @classmethod
    def _validate(
        cls,
        place_id: UUID,
        crop: Crop,
        recommended: bool,
        margin: Temperature,
    ):
        if not isinstance(place_id, UUID):
            error_msg = "Place_id must be a UUID!"
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
        return place_id, crop, recommended, margin

    @classmethod
    def _clean(cls):
        return

    def __str__(self) -> str:
        rec_str = f"{self.place_id.int}; {self.crop}; {self.time_stamp}"
        return rec_str

    def __repr__(self) -> str:
        return self.__str__()
