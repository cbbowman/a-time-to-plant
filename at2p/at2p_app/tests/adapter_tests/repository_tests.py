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

    def test_save_crop(self):
        self.assertIsNone(self.repo.save(self.crop))
        self.assertIsNone(self.repo.save(self.crop))

    def test_get_crop(self):
        self.repo.save(self.crop)
        retrieved_crop = self.repo.get(id=self.crop_id)
        self.assertEqual(retrieved_crop, self.crop)

    def test_delete_crop(self):
        self.repo.save(self.crop)
        self.repo.delete(id=self.crop_id)
        self.assertRaises(CropRepoError, self.repo.get, self.crop_id)
        self.assertRaises(CropRepoError, self.repo.delete, self.crop_id)
