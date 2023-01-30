from django.test import TestCase
from at2p_app.domain.entities.crop import (
    Crop,
    TempRequirement,
    ReqList,
)
from at2p_app.domain.entities.temperature import TempRange
from at2p_app.adapters.repositories import TestingCropRepo
from at2p_app.domain.use_cases.crop_use_cases import CropInterface


class TestCropInterface(TestCase):
    def setUp(self) -> None:
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp=req)
        self.crop_name = "Boberries"
        self.crop_initdict = {"name": self.crop_name, "reqs": self.reqs}
        self.crop = Crop.from_dict(self.crop_initdict)
        self.crop_id = self.crop.id

        self.repo = TestingCropRepo()
        self.interface = CropInterface(self.repo)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.interface, CropInterface)

    def test_create_a_crop(self):
        crop = self.interface.create_crop(self.crop_initdict)
        self.assertIsInstance(crop, Crop)
        self.assertEqual(crop.name, self.crop_name)

    def test_get_a_crop(self):
        crop = self.interface.get_crop(self.crop_id)
        self.assertIsInstance(crop, Crop)
        self.assertEqual(crop.id, self.crop_id)

    def test_update_a_crop(self):
        self.assertIsNone(self.interface.update_crop(self.crop))

    def test_delete_a_crop(self):
        self.assertIsNone(self.interface.delete_crop(self.crop))
