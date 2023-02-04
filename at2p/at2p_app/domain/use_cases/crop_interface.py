import csv
from uuid import UUID
from dataclasses import dataclass
from at2p_app.adapters.repositories.crop_repo import CropRepo, Crop, TempRange
from at2p_app.domain.common.error import InterfaceError

CROP_LIST_CSV = "at2p/at2p_app/static/crops_and_temps.csv"


@dataclass
class CropInterface:
    _crop_repo: CropRepo

    @classmethod
    def new(cls, crop_repo: CropRepo):
        cls._validate(crop_repo)
        return cls(crop_repo)

    @classmethod
    def _validate(cls, crop_repo: CropRepo):
        if not isinstance(crop_repo, CropRepo):
            error_msg = "Interface must be given a valid CropRepo object"
            raise InterfaceError(error_msg)

    def create_crop(self, crop_dict) -> Crop:
        crop = self._crop_repo.create(crop_dict)
        return crop

    def get_crop(self, crop_id: UUID) -> Crop:
        crop = self._crop_repo.get(crop_id)
        return crop

    def save_crop(self, crop: Crop):
        self._crop_repo.save(crop)
        return

    def delete_crop(self, crop):
        self._crop_repo.delete(crop)
        return

    def import_crops(self, source: str = CROP_LIST_CSV) -> list:
        imported_crops = []
        with open(source, encoding="UTF-8") as f:
            reader = csv.reader(f)
            i = 1
            for row in reader:
                abs_min = int(row[1])
                opt_min = int(row[2])
                opt_max = int(row[3])
                abs_max = int(row[4])
                abs_range = TempRange.new(abs_min, abs_max)
                opt_range = TempRange.new(opt_min, opt_max)
                init_dict = {
                    "name": row[0],
                    "abs_range": abs_range,
                    "opt_range": opt_range,
                }
                new_crop = self._crop_repo.create(init_dict)
                imported_crops.append(new_crop)
                i += 1
        return imported_crops
