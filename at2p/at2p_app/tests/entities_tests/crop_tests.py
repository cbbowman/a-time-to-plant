from django.test import TestCase
from at2p_app.domain.entities.crop import (
    Crop,
    TempRequirement,
    ReqList,
    CropError,
    TempRequirementError,
)
from at2p_app.domain.entities.temperature import TempRange, Temp, TempScale


class TestTempReq(TestCase):
    def setUp(self) -> None:
        self.temp_req = TempRequirement()
        return super().setUp()

    def test_create_temp_req_list(self):
        self.assertIsInstance(self.temp_req, TempRequirement)

    def test_validation(self):
        range_in_C = TempRange(50, 60, TempScale.C)
        self.assertRaises(
            TempRequirementError,
            TempRequirement,
            optimal=range_in_C,
        )


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

    def test_as_dict(self):
        self.assertIsInstance(self.temp_req.dict(), dict)


class TestCrop(TestCase):
    def setUp(self) -> None:
        req = TempRequirement()
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
        self.assertEqual(
            self.crop.__str__(), f"{self.crop.name}[{self.crop.id}]"
        )

    def test_reqs(self) -> None:
        self.assertEqual(self.crop.reqs, self.reqs)

    def test_blank_name(self):
        name = ""
        self.assertRaises(CropError, Crop, name, self.reqs)

    def test_float_name(self):
        name = 14.3
        self.assertRaises(CropError, Crop, name, self.reqs)

    def test_bad_req(self):
        self.reqs["bad"] = 15
        self.assertRaises(CropError, Crop, self.crop_name, self.reqs)
