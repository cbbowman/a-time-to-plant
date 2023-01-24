from at2p_app.entities import TempRange, Crop, Country, LatLong, Place
from django.test import TestCase


class TempRangeFactory:
    def _get_temp_range(self, min: int = 1, max: int = 100) -> TempRange:
        return TempRange(min, max)


class TestTempRange(TestCase):
    def test_create_temp_range(self) -> None:
        tr_fact = TempRangeFactory()
        min = 1
        max = 100
        tr = tr_fact._get_temp_range(min, max)
        self.assertTrue(isinstance(tr, TempRange))

        tr_str = f"Minimum: {min}\nMaximum: {max}"
        self.assertEqual(tr.__str__(), tr_str)

        tr_repr = (min, max)
        self.assertEqual(tr.__repr__(), tr_repr)

    def test_value_cleaning(self) -> None:
        tr_fact = TempRangeFactory()
        min = 9.5
        max = 20.2
        tr = tr_fact._get_temp_range(min, max)
        tr_repr = (10, 20)
        self.assertEqual(tr.__repr__(), tr_repr)

        max = "Not an integer"
        self.assertRaises(ValueError, tr_fact._get_temp_range, max)

        min = None
        self.assertRaises(ValueError, tr_fact._get_temp_range, min)

    def test_correct_order(self) -> None:
        larger = 100
        smaller = 1
        tr_fact = TempRangeFactory()
        tr = tr_fact._get_temp_range(larger, smaller)
        self.assertEqual(tr.minimum, smaller)
        self.assertEqual(tr.maximum, larger)

        tr = tr_fact._get_temp_range(smaller, smaller)
        self.assertEqual(tr.minimum, smaller)
        self.assertEqual(tr.maximum, smaller)


class CropFactory:
    def _get_crop(
        self,
        name: str = "Boberries",
        abs: TempRange = TempRange(1, 100),
        opt: TempRange = TempRange(45, 55),
    ) -> Crop:
        return Crop(name, abs, opt)


class CropTest(TestCase):
    def test_create_crop(self) -> None:
        c_fact = CropFactory()
        c = c_fact._get_crop()
        self.assertTrue(isinstance(c, Crop))

        c_str = c.name
        c_repr = c.name
        self.assertEqual(c.__str__(), c_str)
        self.assertEqual(c.__repr__(), c_repr)

    def test_value_errors(self) -> None:
        c_fact = CropFactory()
        name = None
        self.assertRaises(ValueError, c_fact._get_crop, name=name)

        name = ""
        self.assertRaises(ValueError, c_fact._get_crop, name=name)

    def test_check_temp_ranges(self) -> None:
        c_fact = CropFactory()
        abs = TempRange(30, 60)
        opt = TempRange(10, 40)
        self.assertRaises(ValueError, c_fact._get_crop, abs=abs, opt=opt)


class CountryFactory:
    def _get_country(self, name: str = "Greece", code: str = "GR") -> Country:
        return Country(name, code)


class CountryTest(TestCase):
    def test_create_country(self) -> None:
        c_fact = CountryFactory()
        c = c_fact._get_country()
        self.assertTrue(isinstance(c, Country))

        c_str = c.full_name
        c_repr = c.code
        self.assertEqual(c.__str__(), c_str)
        self.assertEqual(c.__repr__(), c_repr)

    def test_value_errors(self) -> None:
        c_fact = CountryFactory()
        name = ""
        self.assertRaises(ValueError, c_fact._get_country, name=name)

        name = None
        self.assertRaises(ValueError, c_fact._get_country, name=name)

        code = "grc"
        self.assertRaises(ValueError, c_fact._get_country, code=code)

        code = None
        self.assertRaises(ValueError, c_fact._get_country, code=code)


class LatLongFactory:
    def _get_lat_long(self, lat: float = 10.0, long: float = 10.0) -> LatLong:
        return LatLong(lat, long)


class LatLongTest(TestCase):
    def test_create_lat_long(self) -> None:
        ll_fact = LatLongFactory()
        ll = ll_fact._get_lat_long()
        self.assertTrue(isinstance(ll, LatLong))

        ll_str = f"Latitude: {ll.lat:.4f}\nLongitude: {ll.long:.4f}"
        ll_repr = (ll.lat, ll.long)
        self.assertEqual(ll.__str__(), ll_str)
        self.assertEqual(ll.__repr__(), ll_repr)

    def test_check_values(self) -> None:
        ll_fact = LatLongFactory()
        lat = 100
        self.assertRaises(ValueError, ll_fact._get_lat_long, lat=lat)

        lat = "latitude"
        self.assertRaises(ValueError, ll_fact._get_lat_long, lat=lat)

        lat = None
        self.assertRaises(ValueError, ll_fact._get_lat_long, lat=lat)

        long = 200
        self.assertRaises(ValueError, ll_fact._get_lat_long, long=long)

        long = "Longitude"
        self.assertRaises(ValueError, ll_fact._get_lat_long, long=long)

        long = None
        self.assertRaises(ValueError, ll_fact._get_lat_long, long=long)


class PlaceFactory:
    def _get_place(
        self,
        country: Country = Country("Greece", "GR"),
        state: str = "Virginia",
        city: str = "Fredericksburg",
        zip: str = "22401",
        latlong: LatLong = LatLong(0, 0),
        elev: int = 100,
    ) -> Place:
        return Place(country, state, city, zip, latlong, elev)


class PlaceTest(TestCase):
    def test_create_place(self) -> None:
        p_fact = PlaceFactory()
        p = p_fact._get_place()
        p_str = f"{p.city}, {p.state}, {p.country.code}"
        p_repr = (p.country.code, p.zip)
        self.assertIsInstance(p, Place)
        self.assertEqual(p.__str__(), p_str)
        self.assertEqual(p.__repr__(), p_repr)
        return

    def test_check_str_values(self) -> None:
        p_fact = PlaceFactory()

        bad_value = 12
        self.assertRaises(ValueError, p_fact._get_place, state=bad_value)
        bad_value = True
        self.assertRaises(ValueError, p_fact._get_place, state=bad_value)
        bad_value = None
        self.assertRaises(ValueError, p_fact._get_place, state=bad_value)
        bad_value = ""
        self.assertRaises(ValueError, p_fact._get_place, state=bad_value)

        bad_value = 12
        self.assertRaises(ValueError, p_fact._get_place, city=bad_value)
        bad_value = True
        self.assertRaises(ValueError, p_fact._get_place, city=bad_value)
        bad_value = None
        self.assertRaises(ValueError, p_fact._get_place, city=bad_value)
        bad_value = ""
        self.assertRaises(ValueError, p_fact._get_place, city=bad_value)

        bad_value = 12
        self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)
        bad_value = True
        self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)
        bad_value = None
        self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)
        bad_value = ""
        self.assertRaises(ValueError, p_fact._get_place, zip=bad_value)

    def test_correct_types(self) -> None:
        p_fact = PlaceFactory()

        bad_value = 0
        self.assertRaises(ValueError, p_fact._get_place, country=bad_value)
        self.assertRaises(ValueError, p_fact._get_place, latlong=bad_value)

        bad_value = "Not an integer"
        self.assertRaises(ValueError, p_fact._get_place, elev=bad_value)
