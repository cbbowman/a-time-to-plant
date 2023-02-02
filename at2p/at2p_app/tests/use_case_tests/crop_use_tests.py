from django.test import TestCase
from at2p_app.domain.entities.crop import Crop
from at2p_app.domain.value_objects.temperature import TempRange
from at2p_app.adapters.repositories import TestingCropRepo
from at2p_app.domain.use_cases.crop_interface import CropInterface


class TestCropInterface(TestCase):
    def setUp(self) -> None:
        self.initdict = {
            "name": "Boberries",
            "abs_range": TempRange.new(40, 80),
            "opt_range": TempRange.new(65, 75),
        }
        self.crop = Crop.from_dict(self.initdict)
        self.crop_id = self.crop.id

        self.repo = TestingCropRepo()
        self.interface = CropInterface(self.repo)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.interface, CropInterface)

    def test_create_a_crop(self):
        crop = self.interface.create_crop(self.initdict)
        self.assertIsInstance(crop, Crop)

    def test_get_a_crop(self):
        crop = self.interface.get_crop(self.crop_id)
        self.assertIsInstance(crop, Crop)

    def test_save_a_crop(self):
        self.assertIsNone(self.interface.save_crop(self.crop))

    def test_delete_a_crop(self):
        self.assertIsNone(self.interface.delete_crop(self.crop))

    def test_import_crops(self):
        crops = self.interface.import_crops()
        for c in crops:
            self.assertIsInstance(c, Crop)
