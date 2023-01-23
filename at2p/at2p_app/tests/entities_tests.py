from at2p_app.entities import TempRange, Crop, Country, LatLong
from django.test import TestCase


class TestTempRange(TestCase):
    def test_create_temp_range(self):

        tr = TempRange(10, 20)
        self.assertTrue(isinstance(tr, TempRange))
        tr_str = 'Minimum: 10\nMaximum: 20'
        self.assertEqual(tr.__str__(), tr_str)
        self.assertEqual(tr.__repr__(), (10, 20))
        self.assertRaises(ValueError, TempRange, minimum='A', maximum=None)

    def test_value_cleaning(self):

        tr = TempRange(9.5, 20.2)
        self.assertEqual(tr.__repr__(), (10, 20))
        self.assertRaises(ValueError, TempRange, minimum='A', maximum=None)

    def test_correct_order(self):

        tr = TempRange(20, 30)
        self.assertEqual(tr.minimum, 20)
        self.assertEqual(tr.maximum, 30)

        tr = TempRange(30, 20)
        self.assertEqual(tr.minimum, 20)
        self.assertEqual(tr.maximum, 30)

        tr = TempRange(30, 30)
        self.assertEqual(tr.minimum, 30)
        self.assertEqual(tr.maximum, 30)


class CropTest(TestCase):
    def test_create_crop(self):
        name = 'Boberries'
        abs = TempRange(10, 60)
        opt = TempRange(30, 40)
        c = Crop(name, abs, opt)
        self.assertTrue(isinstance(c, Crop))

        c_str = name
        self.assertEqual(c.__str__(), c_str)
        self.assertEqual(c.__repr__(), c_str)

    def test_value_errors(self) -> None:
        name = None
        abs = TempRange(10, 60)
        opt = TempRange(30, 40)
        self.assertRaises(
            ValueError, Crop, name=name, abs_temp=abs, opt_temp=opt
        )

        name = ''
        self.assertRaises(
            ValueError, Crop, name=name, abs_temp=abs, opt_temp=opt
        )

    def test_check_temp_ranges(self):
        name = 'Boberries'
        abs_temp = TempRange(30, 60)
        opt_temp = TempRange(10, 40)
        self.assertRaises(
            ValueError, Crop, name=name, abs_temp=abs_temp, opt_temp=opt_temp
        )


class CountryTest(TestCase):
    def test_create_country(self):
        full_name = 'greece'
        code = 'gr'
        c = Country(full_name=full_name, code=code)
        self.assertTrue(isinstance(c, Country))

        c_str = 'Greece'
        c_repr = 'GR'
        self.assertEqual(c.__str__(), c_str)
        self.assertEqual(c.__repr__(), c_repr)

    def test_value_errors(self):
        name = ''
        code = None
        self.assertRaises(ValueError, Country, full_name=name, code=code)
        
        name = 'Greece'
        code = 'grc'
        self.assertRaises(ValueError, Country, full_name=name, code=code)


class LatLongTest(TestCase):
    def test_create_lat_long(self):
        lat_long = LatLong(10, 20)
        self.assertTrue(isinstance(lat_long, LatLong))
        lat_long_str = 'Latitude: 10.0000\nLongitude: 20.0000'
        lat_long_repr = (10.0, 20.0)
        self.assertEqual(lat_long.__str__(), lat_long_str)
        self.assertEqual(lat_long.__repr__(), lat_long_repr)

    def test_check_values(self):
        lat = 100
        long = 200
        self.assertRaises(ValueError, LatLong, lat=lat, long=long)

        lat = 'latitude'
        long = None
        self.assertRaises(ValueError, LatLong, lat=lat, long=long)
