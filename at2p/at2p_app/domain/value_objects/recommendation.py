"""ValueObject classes related to recommendations

Classes:
    Recommendation: Value object representing a crop recommendation
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from at2p_app.domain.common.base import ValueObject
from at2p_app.domain.common.error import RecommendationError
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.temperature import Temperature


@dataclass(frozen=True)
class Recommendation(ValueObject):
    """A timestamped recommendation to plant a crop

    Uses current weather info to provide a boolean recommendation to
    plant a particular crop at a place. The recommendation includes
    a timestamp of when it was generated.

    Attributes:
        place_id: the UUID for the relevant place
        crop: the type of crop being evaluated
        recommended: a boolean value
        margin: a Temperature value; positive if weather is within
            the crops required temperature range; negative otherwise
    """

    place_id: UUID
    crop: Crop
    recommended: bool
    margin: Temperature
    time_stamp: datetime

    @classmethod
    def new(
        """Create a new Recommendation object

        Accepts all the attributes except for the timestamp. All
        attributes are validated and cleaned. A timestamp is
        generated the class __init__ method is called.

        Args:
            place_id: a UUID for a Place entity
            crop: a Crop entity 
            recommended:
            margin:
        """
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
