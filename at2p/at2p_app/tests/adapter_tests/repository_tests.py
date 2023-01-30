from at2p_app.adapters.repositories import DjangoCropRepo, CropRepo
from django.test import TestCase
from at2p_app.domain.entities.crop import Crop, ReqList, TempRequirement
from at2p_app.domain.entities.temperature import TempRange


class TestDjangoRepo(TestCase):
    def setUp(self) -> None:
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp=req)
        self.crop_name = "Boberries"
        self.crop_initdict = {"name": self.crop_name, "reqs": self.reqs}
        self.repo = DjangoCropRepo()
        self.crop = Crop.from_dict(self.crop_initdict)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.repo, CropRepo)

    def test_create_crop(self):
        self.crop = self.repo.create(self.crop_initdict)
        self.assertIsInstance(self.crop, Crop)

    def test_get_crop(self):
        crop_id = self.repo.create(self.crop_initdict)
        retrieved_crop = self.repo.get(crop_id=crop_id)
        self.assertEqual(crop_id, retrieved_crop.id)

    def test_update_crop(self):
        crop_id = self.repo.create(self.crop_initdict)
        crop = self.repo.get(crop_id=crop_id)
        new_name = "Huckleberries"
        crop.name = new_name
        self.repo.update(crop)
        crop = self.repo.get(crop_id=crop_id)
        self.assertEqual(crop.name, new_name)
