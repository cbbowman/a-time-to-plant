from at2p_app.entities import (
    Temp,
    TempRange,
    TempReqList,
    Crop,
    Country,
    LatLong,
)
from django.test import TestCase


class TestTempRange(TestCase):
    def test_create_temp_range(self) -> None:
        small_float = 1.0
        big_int = 100
        tr = TempRange(min=small_float, max=big_int)
        self.assertTrue(isinstance(tr, TempRange))

        tr_str = f"{round(small_float)} \u00B0F \u2013 {big_int} \u00B0F"
        self.assertEqual(tr.__str__(), tr_str)

    def test_value_cleaning(self) -> None:
        max = "Not an integer"
        self.assertRaises(ValueError, Temp, max)
        min = None
        self.assertRaises(ValueError, Temp, min)

    def test_correct_order(self) -> None:
        larger = Temp(100)
        smaller = Temp(1)
        self.assertRaises(ValueError, TempRange, min=larger, max=smaller)


class TestTempReqList(TestCase):
    def test_create_temp_req_list(self):
        abs_range = TempRange(0, 100)
        opt_range = TempRange(40, 60)
        req = TempReqList({"absolute": abs_range, "optimal": opt_range})
        self.assertTrue(isinstance(req, TempReqList))

    def test_validate_abs_and_opt(self):
        abs_range = TempRange(0, 50)
        opt_range = TempRange(75, 100)
        self.assertRaises(
            ValueError,
            TempReqList,
            {"absolute": abs_range, "optimal": opt_range},
        )


class TestCrop(TestCase):
    def test_crop_creation(self):
        abs = TempRange(0, 100)
        opt = TempRange(40, 60)
        req = TempReqList({"absolute": abs, "optimal": opt})
        boberries = Crop("Boberries", req)
        self.assertTrue(isinstance(boberries, Crop))
        self.assertEqual(boberries.__str__(), "Boberries")
        self.assertEqual(boberries.reqs, req)

    def test_value_errors(self):
        abs = TempRange(0, 100)
        opt = TempRange(40, 60)
        req = TempReqList({"absolute": abs, "optimal": opt})

        name = ""
        self.assertRaises(ValueError, Crop, name, req)


class CountryTest(TestCase):
    def test_create_country(self) -> None:
        name = "Greece"
        code = "GR"
        c = Country(name=name, code=code)
        self.assertTrue(isinstance(c, Country))

        c_str = name
        self.assertEqual(c.__str__(), c_str)

    def test_value_errors(self) -> None:
        name = ""
        code = "us"
        self.assertRaises(ValueError, Country, name=name, code=code)
        name = 3
        code = "us"
        self.assertRaises(ValueError, Country, name=name, code=code)
        name = "United States"
        code = True
        self.assertRaises(ValueError, Country, name=name, code=code)
        name = "Greece"
        code = None
        self.assertRaises(ValueError, Country, name=name, code=code)
        name = "Greece"
        code = "GRE"
        self.assertRaises(ValueError, Country, name=name, code=code)


class LatLongTest(TestCase):
    def test_create_lat_long(self) -> None:
        ll = LatLong(10.5, -10.5)
        self.assertTrue(isinstance(ll, LatLong))
        ll_str = "10\u00B030\u20320\u2033N 10\u00B030\u20320\u2033W"
        self.assertEqual(ll.__str__(), ll_str)

#     def test_check_values(self) -> None:
#         ll_fact = LatLongFactory()
#         lat = 100
#         self.assertRaises(ValueError, ll_fact._get_lat_long, lat=lat)

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
