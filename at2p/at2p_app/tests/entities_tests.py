from at2p_app.entities import (
    Temp,
    TempRange,
    TempReqList,
    Crop,
    Country,
    LatLong,
)
from django.test import TestCase
from math import trunc


class TestTemp(TestCase):
    def test_creation(self) -> None:
        t = Temp(4)
        self.assertTrue(isinstance(t, Temp))

    def test_create_from_dict(self) -> None:
        init_dict = {
            "temp": 10,
            "scale": "F",
        }
        temp = Temp.from_dict(init_dict)
        self.assertEqual(temp.temp, init_dict["temp"])
        self.assertEqual(temp.scale, init_dict["scale"])

    def test_value(self) -> None:
        t = 4
        self.assertEqual(Temp(4).temp, t)

    def test_default_scale(self) -> None:
        t = Temp(4)
        scale = "F"
        self.assertEqual(t.scale, scale)

    def test_default_scale(self) -> None:
        t = Temp(4, "C")
        scale = "C"
        self.assertEqual(t.scale, scale)

    def test_str(self) -> None:
        t = Temp(4)
        t_str = f"{t.temp} \u00b0F"
        self.assertEqual(t.__str__(), t_str)

    def test_validation_str(self) -> None:
        t = "Not an integer"
        with self.assertRaises(ValueError):
            Temp(t)

    def test_validation_none(self) -> None:
        t = None
        with self.assertRaises(ValueError):
            Temp(t)


# class TestTempRange(TestCase):
#     def test_creation(self) -> None:
#         small_float = 1.0
#         big_int = 100
#         tr = TempRange(min=small_float, max=big_int)
#         self.assertTrue(isinstance(tr, TempRange))

#     def test_create_from_dict(self) -> None:
#         init_dict = {
#             "min": 10,
#             "max": 100,
#         }
#         tr = TempRange.from_dict(init_dict)
#         self.assertEqual(tr.min.temp, init_dict["min"])
#         self.assertEqual(tr.max.temp, init_dict["max"])

#     def test_str(self) -> None:
#         small_float = 1.0
#         big_int = 100
#         tr = TempRange(min=small_float, max=big_int)
#         tr_str = f"{round(small_float)} \u00B0F \u2013 {big_int} \u00B0F"
#         self.assertEqual(tr.__str__(), tr_str)

#     def test_validation_order(self) -> None:
#         smaller = 1
#         larger = 100
#         tr = TempRange(min=smaller, max=larger)
#         tr.min = Temp(larger)
#         tr.max = Temp(smaller)
#         with self.assertRaises(ValueError):
#             tr._validate()


# class TestTempReqList(TestCase):
#     def test_create_temp_req_list(self):
#         abs_range = TempRange(0, 100)
#         opt_range = TempRange(40, 60)
#         initdict = {
#             "abs": abs_range,
#             "opt": opt_range,
#         }
#         req = TempReqList(initdict)
#         self.assertTrue(isinstance(req, TempReqList))
#         self.assertEqual(req.requirements["abs"], initdict["abs"])
#         self.assertEqual(req.requirements["opt"], initdict["opt"])

#     def test_validation(self):
#         abs_range = TempRange(0, 50)
#         opt_range = TempRange(75, 100)
#         initdict = {
#             "abs": abs_range,
#             "opt": opt_range,
#         }
#         self.assertRaises(ValueError, TempReqList, initdict)


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


# class CountryTest(TestCase):
#     def setUp(self) -> None:
#         self.name = "Greece"
#         self.code = "GR"
#         self.country = Country(name=self.name, code=self.code)
#         return super().setUp()

#     def test_create_from_dict(self):
#         initdict = {
#             "name": self.name,
#             "code": self.code,
#         }
#         c = Country.from_dict(initdict)
#         self.assertTrue(isinstance(c, Country))

#     def test_create_country(self) -> None:
#         self.assertTrue(isinstance(self.country, Country))

#     def test_str(self):
#         self.assertEqual(self.country.__str__(), self.name)

#     def test_name_is_blank(self) -> None:
#         name = ""
#         self.assertRaises(ValueError, Country, name=name, code=self.code)

#     def test_name_is_int(self) -> None:
#         name = 3
#         self.assertRaises(ValueError, Country, name=name, code=self.code)

#     def test_code_is_bool(self) -> None:
#         code = True
#         self.assertRaises(ValueError, Country, name=self.name, code=code)

#     def test_code_not_two(self):
#         code = "GRE"
#         self.assertRaises(ValueError, Country, name=self.name, code=code)


# class LatLongTest(TestCase):
#     def setUp(self) -> None:
#         self.lat = -10.55
#         self.long = -10.55
#         self.lat_long = LatLong(self.lat, self.long)
#         return super().setUp()

#     def test_create_lat_long(self) -> None:
#         self.assertTrue(isinstance(self.lat_long, LatLong))

#     def test_str(self) -> None:
#         ns = "N"
#         if self.lat < 0:
#             ns = "S"
#         lat_deg = trunc(abs(self.lat))
#         m = 60 * (abs(self.lat) % 1)
#         lat_min = trunc(m)
#         lat_sec = round(60 * (m % 1))

#         ew = "E"
#         if self.long < 0:
#             ew = "W"
#         long_deg = trunc(abs(self.long))
#         m = 60 * (abs(self.long) % 1)
#         long_min = trunc(m)
#         long_sec = round(60 * (m % 1))

#         lat_str = f"{lat_deg}\u00B0{lat_min}\u2032{lat_sec}\u2033{ns}"
#         long_str = f"{long_deg}\u00B0{long_min}\u2032{long_sec}\u2033{ew}"
#         lat_long_str = f"{lat_str} {long_str}"
#         self.assertEqual(self.lat_long.__str__(), lat_long_str)

#     def test_check_values(self) -> None:
#         lat = 100
#         self.assertRaises(ValueError, LatLong, lat=lat, long=self.long)


#         lat = 'latitude'
#         self.assertRaises(ValueError, ll_fact._get_lat_long, lat=lat)

#         lat = None
#         self.assertRaises(ValueError, ll_fact._get_lat_long, lat=lat)

#         long = 200
#         self.assertRaises(ValueError, ll_fact._get_lat_long, long=long)

#         long = 'Longitude'
#         self.assertRaises(ValueError, ll_fact._get_lat_long, long=long)

#         long = None
#         self.assertRaises(ValueError, ll_fact._get_lat_long, long=long)


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
