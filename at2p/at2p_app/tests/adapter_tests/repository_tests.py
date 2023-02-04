from at2p_app.adapters.repositories.crop_repo import (
    DjangoCropRepo,
    CropRepo,
    CropRepoError,
)
from django.test import TestCase
from at2p_app.domain.entities.crop import Crop, CropName
from at2p_app.domain.value_objects.temperature import TempRange


class TestDjangoRepo(TestCase):
    def setUp(self) -> None:
        self.opt_range = TempRange.new(30, 50)
        self.abs_range = TempRange.new(10, 100)
        self.crop_name = "Boberries"
        self.crop_initdict = {
            "name": self.crop_name,
            "opt_range": self.opt_range,
            "abs_range": self.abs_range,
        }
        self.repo = DjangoCropRepo()
        self.crop = Crop.new_from_dict(self.crop_initdict)
        self.crop_id = self.crop.id
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.repo, CropRepo)

    def test_create_crop(self):
        # created_crop = self.repo.create(self.crop_initdict)
        self.assertIsInstance(self.repo.create(self.crop_initdict), Crop)
        # self.assertRaises(CropRepoError, self.repo.create, self.crop_initdict)

    def test_get_crop(self):
        created_crop = self.repo.create(self.crop_initdict)
        retrieved_crop = self.repo.get(created_crop.id)
        self.assertIsInstance(created_crop.name, CropName)
        self.assertEqual(retrieved_crop.name, created_crop.name)

    def test_save_crop(self):
        created_crop = self.repo.create(self.crop_initdict)
        new_name = CropName.new("Huckleberries")
        created_crop.name = new_name
        self.repo.save(created_crop)
        retrieved_crop = self.repo.get(created_crop.id)
        self.assertEqual(retrieved_crop.name, new_name)

    def test_delete_crop(self):
        created_crop = self.repo.create(self.crop_initdict)
        self.repo.delete(created_crop)
        self.assertRaises(CropRepoError, self.repo.get, created_crop.id)
        self.assertRaises(CropRepoError, self.repo.save, created_crop)
        self.assertRaises(CropRepoError, self.repo.delete, created_crop)
