from abc import ABC, abstractmethod

from at2p_app.domain.common.error import PlaceRepoError
from at2p_app.domain.entities.place import Country, Place, ZipCode
from at2p_app.models import PlaceModel


class PlaceRepo(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class DjangoPlaceRepo(PlaceRepo):
    def create(self, zip_code, country="US") -> Place:
        place = Place.new(zip_code, country)
        place_query = PlaceModel.objects.filter(id=place.id)
        while len(place_query) > 0:
            place = Place.new(zip_code, country)
            place_query = PlaceModel.objects.filter(id=id)
        model_place = self._model_from_place(place)
        model_place.save()
        return place

    def get(self, place_id) -> Place:
        place_query = PlaceModel.objects.filter(id=place_id)
        if not (len(place_query) > 0):
            error_msg = "Place not found"
            raise PlaceRepoError(error_msg)
        model_place = place_query[0]
        return self._place_from_model(model_place)

    def save(self, place: Place) -> None:
        place_query = PlaceModel.objects.filter(id=place.id)
        if not len(place_query) > 0:
            error_msg = "Place not found"
            raise PlaceRepoError(error_msg)
        model_place = self._model_from_place(place)
        model_place.save()
        return

    def delete(self, place: Place) -> None:
        place_query = PlaceModel.objects.filter(id=place.id)
        if not len(place_query) > 0:
            error_msg = "Place not found"
            raise PlaceRepoError(error_msg)
        model_place = place_query[0]
        model_place.delete()
        return

    def _place_from_model(self, model_place: PlaceModel) -> Place:
        id = model_place.id
        zip_code = ZipCode.new(model_place.zip_code)
        country = Country.new(model_place.country)
        return Place.new(zip_code, country, id=id)

    def _model_from_place(self, place: Place) -> PlaceModel:
        model_place = PlaceModel()
        model_place.id = place.id
        model_place.zip_code = place.zip_code.zip
        model_place.country = place.country.code
        return model_place
