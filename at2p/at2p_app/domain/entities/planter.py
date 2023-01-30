from dataclasses import dataclass
from itertools import count
from typing import List
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.crop import Crop


@dataclass
class PlanterError(Exception):
    error_msg = "Generic Person Requirements Error"

    def __init__(self, message: str = error_msg) -> None:
        self.message = message
        super().__init__(self.message)


class Planter:
    username: str
    location: Place
    crops: List[Crop] = []
    _id_iter: int = count()

    def __init__(self, username: str, location: Place) -> None:
        self.username = username
        self.location = location
        self.id = next(self._id_iter)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        self._check_username()
        self._check_location()
        self._check_crops()
        self._check_id()

    def _check_username(self):
        if isinstance(self.username, str):
            error_msg = "ARGUMENT must be of type 'TYPE'"
            raise PlanterError(error_msg)

    def _check_location(self):
        if isinstance(self.location, Place):
            error_msg = "ARGUMENT must be of type 'TYPE'"
            raise PlanterError(error_msg)

    def _check_crops(self):
        if isinstance(self.crops, List):
            error_msg = "ARGUMENT must be of type 'TYPE'"
            raise PlanterError(error_msg)

    def _check_id(self):
        if isinstance(self.id, int):
            error_msg = "ARGUMENT must be of type 'TYPE'"
            return PlanterError(error_msg)
