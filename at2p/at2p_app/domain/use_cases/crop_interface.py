import csv
from at2p_app.domain.value_objects.temperature import TempRange
from at2p_app.adapters.repositories import CropRepo

CROP_LIST_CSV = "at2p/at2p_app/static/crops_and_temps.csv"


class CropInterface:
    def __init__(self, crop_repo: CropRepo) -> None:
        self._crop_repo = crop_repo

    def create_crop(self, init_dict):
        crop_id = self._crop_repo.create(init_dict)
        return crop_id

    def get_crop(self, crop_id):
        crop = self._crop_repo.get(crop_id)
        return crop

    def save_crop(self, crop):
        self._crop_repo.save(crop)
        return

    def delete_crop(self, crop):
        self._crop_repo.delete(crop)
        return

    def import_crops(self, source: str = CROP_LIST_CSV):
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
                    "id": i,
                    "name": row[0],
                    "abs_range": abs_range,
                    "opt_range": opt_range
                }
                new_crop = self._crop_repo.create(init_dict)
                imported_crops.append(new_crop)
                i += 1
        return imported_crops
