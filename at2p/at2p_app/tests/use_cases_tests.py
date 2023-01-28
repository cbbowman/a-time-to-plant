from ..entities import Temp, TempRange, Country, LatLong
from ..use_cases import (
    CropRequirement,
    CropRequirementError,
    TempRequirement,
    TempRequirementError,
    ReqList,
)
from ..use_cases import Crop, CropError
from django.test import TestCase


class TestTempReq(TestCase):
    def setUp(self) -> None:
        self.temp_range = TempRange(10, 100)
        self.temp_req = TempRequirement(absolute=self.temp_range)
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
            TempRequirementError, TempRequirement, self.abs_range, bad_range
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


# class PlaceFactory:
#     def _get_place(
#         self,
#         country: Country = Country('Greece', 'GR'),
#         state: str = 'Virginia',
#         city: str = 'Fredericksburg',
#         zip: str = '22401',
#         latlong: LatLong = LatLong(0, 0),
#         elev: int = 100,
#     ) -> Place:
#         return Place(country, state, city, zip, latlong, elev)


# class PlaceTest(TestCase):
#     def test_create_place(self) -> None:
#         p_fact = PlaceFactory()
#         p = p_fact._get_place()
#         p_str = f'{p.city}, {p.state}, {p.country.code}'
#         p_repr = (p.country.code, p.zip)
#         self.assertIsInstance(p, Place)
#         self.assertEqual(p.__str__(), p_str)
#         self.assertEqual(p.__repr__(), p_repr)
#         return

#     def test_check_str_values(self) -> None:
#         p_fact = PlaceFactory()

#         bad_value = 12
#         self.assertRaises(ValueError, p_fact._get_place, state=bad_value)
#         bad_value = True
#         self.assertRaises(ValueError, p_fact._get_place, state=bad_value)
#         bad_value = None
#         self.assertRaises(ValueError, p_fact._get_place, state=bad_value)
#         bad_value = ''
#         self.assertRaises(ValueError, p_fact._get_place, state=bad_value)

#         bad_value = 12
#         self.assertRaises(ValueError, p_fact._get_place, city=bad_value)
#         bad_value = True
#         self.assertRaises(ValueError, p_fact._get_place, city=bad_value)
#         bad_value = None
#         self.assertRaises(ValueError, p_fact._get_place, city=bad_value)
#         bad_value = ''
#         self.assertRaises(ValueError, p_fact._get_place, city=bad_value)

#         bad_value = 12
#         self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)
#         bad_value = True
#         self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)
#         bad_value = None
#         self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)
#         bad_value = ''
#         self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)

#     def test_correct_types(self) -> None:
#         p_fact = PlaceFactory()

#         bad_value = 0
#         self.assertRaises(ValueError, p_fact._get_place, country=bad_value)
#         self.assertRaises(ValueError, p_fact._get_place, latlong=bad_value)

#         bad_value = 'Not an integer'
#         self.assertRaises(ValueError, p_fact._get_place, elev=bad_value)
