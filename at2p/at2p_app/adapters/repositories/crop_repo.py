from abc import ABC, abstractmethod

from at2p_app.domain.common.error import CropRepoError
from at2p_app.domain.entities.crop import Crop, CropName, TempRange
from at2p_app.models import CropModel


class CropRepo(ABC):
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


class TestingCropRepo(CropRepo):
    def __init__(
        self,
    ) -> None:
        self.opt_range = TempRange.new(30, 50)
        self.abs_range = TempRange.new(10, 100)
        self.crop_name = "Boberries"
        self.crop_initdict = {
            "name": self.crop_name,
            "opt_range": self.opt_range,
            "abs_range": self.abs_range,
        }
        self.crop = Crop.new_from_dict(self.crop_initdict)
        super().__init__()

    def create(self, crop_dict):
        return Crop.new_from_dict(crop_dict)

    def get(self, crop_id) -> Crop:
        self.crop_initdict["id"] = crop_id
        return Crop.new_from_dict(self.crop_initdict)

    def save(self, crop: Crop):
        return

    def delete(self, crop: Crop):
        return


class DjangoCropRepo(CropRepo):
    def create(self, crop_dict: dict) -> Crop:
        crop = Crop.new_from_dict(crop_dict)
        crop_query = CropModel.objects.filter(id=crop.id)
        while len(crop_query) > 0:
            crop = Crop.new_from_dict(crop_dict)
            crop_query = CropModel.objects.filter(id=id)
        crop_model = self._model_from_crop(crop)
        crop_model.save()
        return crop

    def get(self, crop_id) -> Crop:
        crop_query = CropModel.objects.filter(id=crop_id)
        if not (len(crop_query) > 0):
            error_msg = "Crop not found"
            raise CropRepoError(error_msg)
        model_crop = crop_query[0]
        return self._crop_from_model(model_crop)

    def save(self, crop: Crop) -> None:
        crop_query = CropModel.objects.filter(id=crop.id)
        if not len(crop_query) > 0:
            error_msg = "Crop not found"
            raise CropRepoError(error_msg)
        model_crop = self._model_from_crop(crop)
        model_crop.save()
        return

    def delete(self, crop: Crop) -> None:
        crop_query = CropModel.objects.filter(id=crop.id)
        if not len(crop_query) > 0:
            error_msg = "Crop not found"
            raise CropRepoError(error_msg)
        model_crop = crop_query[0]
        model_crop.delete()
        return

    def _crop_from_model(self, model: CropModel) -> Crop:
        id = model.id
        name = CropName.new(model.name)
        opt_range = TempRange.new(model.opt_low, model.opt_high)
        abs_range = TempRange.new(model.abs_low, model.abs_high)
        crop_initdict = {
            "id": id,
            "name": name,
            "opt_range": opt_range,
            "abs_range": abs_range,
        }
        return Crop.new_from_dict(crop_initdict)

    def _model_from_crop(self, crop: Crop) -> CropModel:
        model_crop = CropModel()
        model_crop.id = crop.id
        model_crop.name = crop.name.name
        model_crop.abs_low = crop.abs_range.min.temp
        model_crop.abs_high = crop.abs_range.max.temp
        model_crop.opt_low = crop.opt_range.min.temp
        model_crop.opt_high = crop.opt_range.max.temp
        return model_crop
