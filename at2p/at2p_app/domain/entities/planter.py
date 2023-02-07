from dataclasses import dataclass
from uuid import uuid4

from at2p_app.domain.common.error import PlanterError
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.entities.place import Place


@dataclass
class Planter:
    id: int
    username: str
    location: Place
    crops: list

    @classmethod
    def new(cls, username: str, location: Place):
        username, location = cls._validate(username, location)
        return cls(uuid4().int, username, location, [])

    @classmethod
    def _validate(cls, username, location):
        cls._check_username(username)
        cls._check_location(location)
        return username, location

    @classmethod
    def _check_username(cls, username):
        if not isinstance(username, str):
            error_msg = "username must be of type 'string'"
            raise PlanterError(error_msg)

    @classmethod
    def _check_location(cls, location):
        if not isinstance(location, Place):
            error_msg = "location must be of type 'Place'"
            raise PlanterError(error_msg)

    def __str__(self) -> str:
        return f"{self.username} ({self.id})"

    def __repr__(self) -> str:
        return self.__str__()

    def change_username(self, username):
        self.__class__._check_username(username)
        self.username = username
        return

    def change_location(self, location):
        self.__class__._check_location(location)
        self.location = location
        return

    def add_crop(self, crop: Crop):
        if not self._crop_in_list(crop):
            self.crops.append(crop)
        else:
            error_msg = "Crop ({crop}) already in list"
            raise PlanterError(error_msg)

    def remove_crop(self, crop: Crop):
        if self._crop_in_list(crop):
            self.crops.remove(crop)
        else:
            error_msg = "Crop ({crop}) not in list"
            raise PlanterError(error_msg)

    def _crop_in_list(self, crop) -> bool:
        for c in self.crops:
            if c == crop:
                return True
        return False
