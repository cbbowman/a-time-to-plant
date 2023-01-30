from datetime import datetime
from django.test import TestCase
from at2p_app.domain.entities.weather import (
    Temp,
    TempRange,
    TemperatureError,
    TempRangeError,
    TempScale,
    WeatherReport,
    WeatherReportError,
)
from at2p_app.domain.entities.location import (
    Country,
    LatLong,
    CountryError,
    LatLongError,
    Place,
    PlaceError,
)


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
            "scale": TempScale.F,
        }
        t = Temp.from_dict(init_dict)
        self.assertTrue(isinstance(t, Temp))
        self.assertEqual(
            (t.value, t.scale), (init_dict["value"], init_dict["scale"])
        )

    def test_value(self) -> None:
        self.assertEqual(self.t.value, self.value)

    def test_default_scale(self) -> None:
        scale = TempScale.F
        self.assertEqual(self.t.scale, scale)

    def test_scale(self) -> None:
        scale = TempScale.C
        temp_in_c = Temp(self.value, scale)
        self.assertEqual(temp_in_c.scale, scale)

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
        low = self.t.value - 10
        high = self.t.value + 10
        self.assertTrue(self.t.is_in_range(low, high))
        self.assertRaises(
            TemperatureError, self.t.is_in_range, low, high, TempScale.C
        )


class TestTempRange(TestCase):
    def setUp(self) -> None:
        self.low = 1.0
        self.high = 100
        self.tr = TempRange(low=self.low, high=self.high)
        return super().setUp()

    def test_creation(self) -> None:
        self.assertTrue(isinstance(self.tr, TempRange))

    def test_create_from_dict(self) -> None:
        init_dict = {
            "low": 10,
            "high": 100,
        }
        tr = TempRange.from_dict(init_dict)
        self.assertEqual(
            (init_dict["low"], init_dict["high"]), (tr.low, tr.high)
        )

    def test_str(self) -> None:
        tr_str = f"{self.low} \u2013 {self.high} {self.tr.scale}"
        self.assertEqual(self.tr.__str__(), tr_str)

    def test_validation(self) -> None:
        smaller = 1
        larger = 100
        self.assertRaises(TempRangeError, TempRange, low=larger, high=smaller)

    def test_in_range_check(self) -> None:
        t = Temp(60)
        temp_range = TempRange(10, 100)
        self.assertTrue(temp_range.includes(t))

        t = Temp(110)
        self.assertFalse(temp_range.includes(t))

        t = Temp(50, TempScale.C)
        self.assertRaises(TempRangeError, temp_range.includes, t)


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
        bad_long = "one hundred"
        self.assertRaises(LatLongError, LatLong, lat=bad_long, long=self.long)


class PlaceTest(TestCase):
    def setUp(self) -> None:
        self.zip = "22407"
        self.place = Place(zip=self.zip)

        return super().setUp()

    def test_create_place(self) -> None:
        p_str = f"{self.place.zip}, {self.place.country}"
        self.assertIsInstance(self.place, Place)
        self.assertEqual(self.place.__str__(), p_str)
        return

    def test_validation(self) -> None:
        bad_value = 12
        self.assertRaises(PlaceError, Place, zip=bad_value)
        self.assertRaises(PlaceError, Place, zip=self.zip, country=bad_value)


class WeatherReportTest(TestCase):
    def setUp(self) -> None:
        self.location = Place("22407")
        self.highs = TempRange(80, 90)
        self.lows = TempRange(40, 50)
        init_dict = {
            "location": self.location,
            "highs": self.highs,
            "lows": self.lows,
        }
        self.wr = WeatherReport.from_dict(init_dict)
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.wr, WeatherReport)
        self.assertEqual(self.wr.location, self.location)
        self.assertEqual(self.wr.highs, self.highs)
        self.assertEqual(self.wr.lows, self.lows)
        self.assertIsInstance(self.wr.time_reported, datetime)

    def test_validation(self):
        bad_dict = {
            "location": "Bad Value",
            "highs": self.highs,
            "lows": self.lows,
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )
