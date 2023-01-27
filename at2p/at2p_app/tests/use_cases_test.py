from at2p_app.use_cases import (
    TempRequirement,
    TempRequirementError,
    ReqList,
)
from at2p_app.entities import TempRange
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
        self.req_list = TempRequirement(
            absolute=self.abs_range, optimal=self.opt_range
        )
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.req_list, ReqList)

    def test_validation(self):
        bad_range = TempRange(50, 200)
        self.assertRaises(
            TempRequirementError, TempRequirement, self.abs_range, bad_range
        )


# class TestCrop(TestCase):
#     def setUp(self) -> None:
#         self.reqs = TempReqList(
#             {
#                 "abs": TempRange(0, 100),
#                 "opt": TempRange(40, 60),
#             }
#         )
#         self.crop_name = "Boberries"
#         self.crop = Crop(self.crop_name, self.reqs)
#         return super().setUp()

#     def test_create_from_dict(self):
#         initdict = {"name": self.crop_name, "reqs": self.reqs}
#         c = Crop.from_dict(initdict)
#         self.assertTrue(isinstance(c, Crop))

#     def test_crop_creation(self):
#         self.assertTrue(isinstance(self.crop, Crop))

#     def test_str(self) -> None:
#         self.assertEqual(self.crop.__str__(), self.crop_name)

#     def test_reqs(self) -> None:
#         self.assertEqual(self.crop.reqs, self.reqs)

#     def test_blank_name(self):
#         name = ""
#         self.assertRaises(ValueError, Crop, name, self.reqs)

#     def test_none_name(self):
#         name = None
#         self.assertRaises(ValueError, Crop, name, self.reqs)

#     def test_float_name(self):
#         name = 14.3
#         self.assertRaises(ValueError, Crop, name, self.reqs)

#     def test_bool_name(self):
#         name = True
#         self.assertRaises(ValueError, Crop, name, self.reqs)

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
