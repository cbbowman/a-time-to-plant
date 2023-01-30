from at2p_app.domain.entities.weather import Temp, TempRange
from at2p_app.domain.use_cases.recommend import (
    Crop,
    CropRequirement,
    TempRequirement,
    ReqList,
    CropError,
    CropRequirementError,
    TempRequirementError,
)

from django.test import TestCase


class TestTempReq(TestCase):
    def setUp(self) -> None:
        self.abs_temp_range = TempRange(10, 100)
        self.opt_temp_range = TempRange(50, 60)
        self.temp_req = TempRequirement(
            absolute=self.abs_temp_range, optimal=self.opt_temp_range
        )
        return super().setUp()

    def test_create_temp_req_list(self):
        self.assertIsInstance(self.temp_req, TempRequirement)


class TestTempReqList(TestCase):
    def setUp(self) -> None:
        self.abs_range = TempRange(10, 100)
        self.opt_range = TempRange(40, 60)
        self.temp_reqs = TempRequirement(
            absolute=self.abs_range, optimal=self.opt_range
        )
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.temp_reqs, TempRequirement)

    def test_validation(self):
        bad_range = TempRange(50, 200)
        self.assertRaises(
            TempRequirementError,
            TempRequirement,
            absolute=self.abs_range,
            optimal=bad_range,
        )


class TestReqList(TestCase):
    def setUp(self) -> None:
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        self.temp_req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp_req=self.temp_req)
        return super().setUp()

    def test_creation(self):
        self.assertTrue(type(self.reqs) == dict)


class TestCrop(TestCase):
    def setUp(self) -> None:
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp=req)
        self.crop_name = "Boberries"
        self.crop = Crop(name=self.crop_name, reqs=self.reqs)
        return super().setUp()

    def test_create_from_dict(self):
        initdict = {"name": self.crop_name, "reqs": self.reqs}
        c = Crop.from_dict(initdict)
        self.assertTrue(isinstance(c, Crop))

    def test_crop_creation(self):
        self.assertTrue(isinstance(self.crop, Crop))

    def test_replace_reqs(self):
        opt = TempRange(40, 45)
        abs = TempRange(20, 90)
        reqs = TempRequirement(absolute=abs, optimal=opt)
        self.new_reqs = reqs
        self.crop.reqs = self.new_reqs
        self.assertEqual(self.crop.reqs, self.new_reqs)

    def test_validate_reqs(self):
        initdict = {"name": self.crop_name, "reqs": Temp(4)}
        self.assertRaises(CropError, Crop.from_dict, initdict)

    def test_str(self) -> None:
        self.assertEqual(self.crop.__str__(), self.crop_name)

    def test_reqs(self) -> None:
        self.assertEqual(self.crop.reqs, self.reqs)

    def test_blank_name(self):
        name = ""
        self.assertRaises(CropError, Crop, name, self.reqs)

    def test_float_name(self):
        name = 14.3
        self.assertRaises(CropError, Crop, name, self.reqs)
