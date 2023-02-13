from dataclasses import dataclass
from uuid import UUID

from at2p_app.adapters.repositories.place_repo import Place, PlaceRepo
from at2p_app.domain.common.error import InterfaceError


@dataclass
class PlaceInterface:
    _place_repo: PlaceRepo

    @classmethod
    def new(cls, place_repo: PlaceRepo):
        cls._validate(place_repo)
        return cls(place_repo)

    @classmethod
    def _validate(cls, place_repo: PlaceRepo):
        if not isinstance(place_repo, PlaceRepo):
            error_msg = "Interface must be given a valid PlaceRepo object"
            raise InterfaceError(error_msg)

    def create_place(self, zip_code, country="US") -> Place:
        place = self._place_repo.create(zip_code, country)
        return place

    def get_place(self, place_id: UUID) -> Place:
        place = self._place_repo.get(place_id)
        return place

    def save_place(self, place: Place):
        self._place_repo.save(place)
        return

    def delete_place(self, place):
        self._place_repo.delete(place)
        return
