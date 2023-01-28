from ..entities import Temp, TemperatureError, TempRange, TempRangeError
from ..entities import Country, CountryError, LatLong, LatLongError
from django.test import TestCase


class TestTemp(TestCase):
    def setUp(self) -> None:
        self.value = 4
        self.t = Temp(self.value)
        return super().setUp()

    def test_creation(self) -> None:
        self.assertTrue(isinstance(self.t, Temp))

    def test_create_from_dict(self) -> None:
        init_dict = {
            "value": 10,
            "scale": "F",
        }
        t = Temp.from_dict(init_dict)
        self.assertTrue(isinstance(t, Temp))
        self.assertEqual(
            (t.value, t.scale), (init_dict["value"], init_dict["scale"])
        )

    def test_value(self) -> None:
        self.assertEqual(self.t.value, self.value)

    def test_default_scale(self) -> None:
        scale = "F"
        self.assertEqual(self.t.scale, scale)

    def test_scale(self) -> None:
        scale = "C"
        t_c = Temp(self.value, scale)
        self.assertEqual(t_c.scale, scale)

    def test_str(self) -> None:
        t_str = f"{self.t.value} \u00b0F"
        self.assertEqual(self.t.__str__(), t_str)

    def test_validation(self) -> None:
        t = "Not an integer"
        self.assertRaises(TemperatureError, Temp, t)

    def test_clean(self) -> None:
        t = 10.1
        t_from_float = Temp(t)
        self.assertIsInstance(t_from_float.value, int)

    def test_is_in_range(self) -> None:
        self.assertTrue(
            self.t.is_in_range(self.t.value - 10, self.t.value + 10)
        )


class TestTempRange(TestCase):
    def setUp(self) -> None:
        self.min = 1.0
        self.max = 100
        self.tr = TempRange(min=self.min, max=self.max)
        return super().setUp()

    def test_creation(self) -> None:
        self.assertTrue(isinstance(self.tr, TempRange))

    def test_create_from_dict(self) -> None:
        init_dict = {
            "min": 10,
            "max": 100,
        }
        tr = TempRange.from_dict(init_dict)
        self.assertEqual(
            (init_dict["min"], init_dict["max"]), (tr.min.value, tr.max.value)
        )

    def test_str(self) -> None:
        tr_str = f"{round(self.min)} \u00B0F \u2013 {self.max} \u00B0F"
        self.assertEqual(self.tr.__str__(), tr_str)

    def test_validation(self) -> None:
        smaller = 1
        larger = 100
        self.assertRaises(TempRangeError, TempRange, min=larger, max=smaller)


class CountryTest(TestCase):
    def setUp(self) -> None:
        self.code = "US"
        self.country = Country(code=self.code)
        self.name = self.country.name
        return super().setUp()

    def test_create_country(self) -> None:
        self.assertTrue(isinstance(self.country, Country))

    def test_str(self):
        self.assertEqual(self.country.__str__(), self.name)

    def test_code_isnt_a_str(self) -> None:
        code = 42
        self.assertRaises(CountryError, Country, code=code)

    def test_code_wrong_length(self):
        code = "GRE"
        self.assertRaises(CountryError, Country, code=code)

    def test_cleaning(self):
        code = " U s  \n"
        c = Country(code)
        self.assertEqual(c.code, "US")


class LatLongTest(TestCase):
    def setUp(self) -> None:
        self.lat = -10.55
        self.long = -10.55
        self.lat_long = LatLong(self.lat, self.long)
        return super().setUp()

    def test_create_lat_long(self) -> None:
        self.assertTrue(isinstance(self.lat_long, LatLong))

    def test_str(self) -> None:
        ns = "N"
        if self.lat < 0:
            ns = "S"

        ew = "E"
        if self.long < 0:
            ew = "W"

        lat_str = f"{abs(self.lat):.2f}\u00b0{ns}"
        long_str = f"{abs(self.long):.2f}\u00B0{ew}"
        lat_long_str = f"{lat_str} {long_str}"
        self.assertEqual(self.lat_long.__str__(), lat_long_str)

    def test_check_invalid_numbers(self) -> None:
        bad_lat = 100
        self.assertRaises(LatLongError, LatLong, lat=bad_lat, long=self.long)
        bad_long = 200
        self.assertRaises(LatLongError, LatLong, lat=self.lat, long=bad_long)

    def test_validation(self):
        bad_lat = "one hundred"
        self.assertRaises(LatLongError, LatLong, lat=bad_lat, long=self.long)
