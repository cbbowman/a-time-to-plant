from abc import ABC, abstractmethod
from at2p_app.domain.entities.location import Place


class PlaceAdapter(ABC):
    @abstractmethod
    def get(self, place_id):
        pass

    @abstractmethod
    def delete(self, place_id):
        pass

    @abstractmethod
    def save(self, place: Place):
        pass
