from abc import ABC, abstractmethod
from at2p_app.domain.entities.temperature import TempRange
from at2p_app.domain.entities.crop import (
    Crop,
    TempRequirement,
    ReqList,
)
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
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp=req)
        self.crop_name = "Boberries"
        self.crop_initdict = {"name": self.crop_name, "reqs": self.reqs}
        self.crop = Crop.from_dict(self.crop_initdict)
        super().__init__()

    def create(self, crop_initdict):
        return Crop.from_dict(crop_initdict)

    def get(self, crop_id):
        self.crop.id = crop_id
        return self.crop

    def save(self, crop: Crop):
        return

    def delete(self, crop_id):
        return


class DjangoCropRepo(CropRepo):
    def create(self, initdict) -> int:
        crop = Crop.from_dict(initdict)
        reqs = crop.reqs.get("temp")
        absolute = reqs.absolute
        optimal = reqs.optimal
        crop_model = CropModel(
            id=crop.id,
            name=crop.name,
            abs_low=absolute.low,
            abs_high=absolute.high,
            opt_low=optimal.low,
            opt_high=optimal.high,
            scale=absolute.scale,
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
        opt = TempRange(crop_model.opt_low, crop_model.opt_high)
        abs = TempRange(crop_model.abs_low, crop_model.abs_high)
        req = TempRequirement(absolute=abs, optimal=opt)
        reqs = ReqList(temp=req)
        crop_initdict = {"id": crop_id, "name": crop_name, "reqs": reqs}
        return Crop.from_dict(crop_initdict)

    def save(self, crop: Crop) -> None:
        temp_req = crop.reqs["temp"]
        crop_query = CropModel.objects.filter(id=crop.id)
        if not len(crop_query) > 0:
            raise CropRepoError()
        model_crop = crop_query[0]
        model_crop.name = crop.name
        model_crop.abs_low = temp_req.absolute.low
        model_crop.abs_high = temp_req.absolute.high
        model_crop.opt_low = temp_req.optimal.low
        model_crop.opt_high = temp_req.optimal.high
        model_crop.scale = temp_req.absolute.scale
        model_crop.save()
        return

    def delete(self, crop_id) -> None:
        crop_query = CropModel.objects.filter(id=crop_id)
        if not len(crop_query) > 0:
            raise CropRepoError()
        crop_query[0].delete()
        return
