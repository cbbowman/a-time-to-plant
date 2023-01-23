from at2p_app.entities import TempRange, Crop
from django.test import TestCase


class TestTempRange(TestCase):
    def test_create_temp_range(self):
        tr = TempRange(10, 20)
        self.assertTrue(isinstance(tr, TempRange))
        tr_str = "Minimum: 10\nMaximum: 20"
        self.assertEqual(tr.__str__(), tr_str)
        self.assertEqual(tr.__repr__(), tr_str)

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
        name = "Boberries"
        abs_temp = TempRange(10, 60)
        opt_temp = TempRange(30, 40)
        c = Crop(name, abs_temp, opt_temp)
        self.assertTrue(isinstance(c, Crop))

        c_str = name
        self.assertEqual(c.__str__(), c_str)
        self.assertEqual(c.__repr__(), c_str)

    def test_check_temp_ranges(self):
        name = "Boberries"
        abs_temp = TempRange(30, 60)
        opt_temp = TempRange(10, 40)
        self.assertRaises(
            ValueError, Crop, name=name, abs_temp=abs_temp, opt_temp=opt_temp
        )
