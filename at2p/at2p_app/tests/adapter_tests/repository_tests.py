from at2p_app.adapters.repositories import (
    DjangoCropRepo,
    CropRepo,
    CropRepoError,
)
from django.test import TestCase
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.temperature import TempRange


class TestDjangoRepo(TestCase):
    def setUp(self) -> None:
        self.opt_range = TempRange.new(30, 50)
        self.abs_range = TempRange.new(10, 100)
        self.crop_name = "Boberries"
        self.crop_id = 73
        self.crop_initdict = {
            "id": self.crop_id,
            "name": self.crop_name,
            "opt_range": self.opt_range,
            "abs_range": self.abs_range,
        }
        self.repo = DjangoCropRepo()
        self.crop = Crop.from_dict(self.crop_initdict)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.repo, CropRepo)

    def test_create_crop(self):
        crop_id = self.repo.create(self.crop_initdict)
        self.assertEqual(crop_id, self.crop_id)

    def test_get_crop(self):
        crop_id = self.repo.create(self.crop_initdict)
        retrieved_crop = self.repo.get(crop_id=crop_id)
        self.assertEqual(crop_id, retrieved_crop.id)
        self.assertRaises(CropRepoError, self.repo.get, crop_id + 1)

    def test_save_crop(self):
        crop_id = self.repo.create(self.crop_initdict)
        crop = self.repo.get(crop_id=crop_id)
        new_name = "Huckleberries"
        crop.name = new_name
        self.repo.save(crop)
        crop = self.repo.get(crop_id=crop_id)
        self.assertEqual(crop.name, new_name)

        crop.id = crop.id + 1
        self.assertRaises(CropRepoError, self.repo.save, crop)

    def test_delete_crop(self):
        crop_id = self.repo.create(self.crop_initdict)
        self.repo.delete(crop_id=crop_id)
        self.assertRaises(CropRepoError, self.repo.delete, crop_id)
