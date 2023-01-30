from django.test import TestCase
from at2p_app.domain.entities.location import (
    Country,
    CountryError,
    Place,
    PlaceError,
)
from at2p_app.domain.entities.lat_long import LatLong, LatLongError


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

    def test_code_unsupported(self):
        code = "GR"
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
        self.assertRaises(LatLongError, LatLong, lat=self.lat, long=bad_long)


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
        bad_value = "GR"
        self.assertRaises(PlaceError, Place, zip=self.zip, country=bad_value)
