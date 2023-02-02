from abc import ABC, abstractmethod
from at2p_app.domain.value_objects.temperature import TempRange
from at2p_app.domain.entities.crop import Crop
from at2p_app.models import CropModel


class CropRepo(ABC):
    @abstractmethod
    def create(self, crop_id):
        pass

    @abstractmethod
    def get(self, crop_id):
        pass

    @abstractmethod
    def save(self, crop: Crop):
        pass

    @abstractmethod
    def delete(self, crop_id):
        pass


class CropRepoError(Exception):
    generic_msg = "Generic Repository Error"

    def __init__(self, error_msg: str = generic_msg) -> None:
        message = f"\n{error_msg}\n"
        super().__init__(message)


class TestingCropRepo(CropRepo):
    def __init__(
        self,
    ) -> None:
        self.opt_range = TempRange.new(30, 50)
        self.abs_range = TempRange.new(10, 100)
        self.crop_name = "Boberries"
        self.crop_initdict = {
            "id": 73,
            "name": self.crop_name,
            "opt_range": self.opt_range,
            "abs_range": self.abs_range,
        }
        self.crop = Crop.from_dict(self.crop_initdict)
        super().__init__()

    def create(self, crop_initdict):
        return Crop.from_dict(crop_initdict)

    def get(self, crop_id):
        self.crop_initdict["id"] = crop_id
        return Crop.from_dict(self.crop_initdict)

    def save(self, crop: Crop):
        return

    def delete(self, crop_id):
        return


class DjangoCropRepo(CropRepo):
    def create(self, initdict) -> int:
        crop = Crop.from_dict(initdict)
        absolute = crop.abs_range
        optimal = crop.opt_range
        crop_model = CropModel(
            id=crop.id,
            name=crop.name,
            abs_low=absolute.min.temp,
            abs_high=absolute.max.temp,
            opt_low=optimal.min.temp,
            opt_high=optimal.max.temp,
        )
        crop_model.save()
        return crop_model.id

    def get(self, crop_id) -> Crop:
        crop_query = CropModel.objects.filter(id=crop_id)
        if not (len(crop_query) > 0):
            raise CropRepoError()
        crop_model = crop_query[0]
        crop_id = crop_model.id
        crop_name = crop_model.name
        opt_range = TempRange.new(crop_model.opt_low, crop_model.opt_high)
        abs_range = TempRange.new(crop_model.abs_low, crop_model.abs_high)
        crop_initdict = {
            "id": crop_id,
            "name": crop_name,
            "opt_range": opt_range,
            "abs_range": abs_range,
        }
        return Crop.from_dict(crop_initdict)

    def save(self, crop: Crop) -> None:
        crop_query = CropModel.objects.filter(id=crop.id)
        if not len(crop_query) > 0:
            raise CropRepoError()
        model_crop = crop_query[0]
        model_crop.name = crop.name
        model_crop.abs_low = crop.abs_range.min.temp
        model_crop.abs_high = crop.abs_range.max.temp
        model_crop.opt_low = crop.opt_range.min.temp
        model_crop.opt_high = crop.opt_range.max.temp
        model_crop.save()
        return

    def delete(self, crop_id) -> None:
        crop_query = CropModel.objects.filter(id=crop_id)
        if not len(crop_query) > 0:
            raise CropRepoError()
        crop_query[0].delete()
        return
