from dataclasses import dataclass
from typing import List
from at2p_app.domain.entities.place import Place
from at2p_app.domain.entities.crop import Crop


@dataclass
class PlanterError(Exception):
    error_msg = "Generic Person Requirements Error"

    def __init__(self, message: str = error_msg) -> None:
        self.message = message
        super().__init__(self.message)


class Planter:
    id: int = None
    username: str
    location: Place
    crops: List[Crop] = []

    def __init__(self, username: str, location: Place) -> None:
        self.username = username
        self.location = location
        if self.id is None:
            self.id = hash(username)
        self.__post_init__()

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._check_username()
        self._check_location()
        self._check_crops()
        self._check_id()

    def _check_username(self):
        if not isinstance(self.username, str):
            error_msg = "username must be of type 'string'"
            raise PlanterError(error_msg)

    def _check_location(self):
        if not isinstance(self.location, Place):
            error_msg = "location must be of type 'Place'"
            raise PlanterError(error_msg)

    def _check_crops(self):
        if not isinstance(self.crops, List):
            error_msg = "crops must be of type 'List'"
            raise PlanterError(error_msg)

    def _check_id(self):
        if not isinstance(self.id, int):
            error_msg = "id must be of type 'int'"
            raise PlanterError(error_msg)
