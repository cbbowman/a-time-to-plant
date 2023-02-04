from django.test import TestCase
from at2p_app.domain.value_objects.temperature import (
    TempRange,
    Temperature,
    TempScale,
)
from at2p_app.domain.common.error import TemperatureError


class TempScaleTests(TestCase):
    def test_str_repr(self):
        s = TempScale.F
        f_str = f"\u00b0{s.name}"
        self.assertEqual(f_str, s.__str__())
        self.assertEqual(f_str, s.__repr__())


class TemperatureObjectTests(TestCase):
    def setUp(self) -> None:
        self.n = 40
        self.t = Temperature.new(self.n)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.t, Temperature)
        self.assertIsInstance(self.t.scale, TempScale)
        self.assertEqual(self.t.temp, self.n)

    def test_comparison(self):
        low = 40
        high = low + 10
        low_temp = Temperature.new(low)
        high_temp = Temperature.new(high)
        self.assertTrue(high_temp > low_temp)

        temp1 = Temperature.new(low)
        temp2 = Temperature.new(low)
        self.assertEqual(temp1, temp2)

        temp1 = Temperature.new(low, TempScale.F)
        temp2 = Temperature.new(low, TempScale.C)
        self.assertNotEqual(temp1, temp2)

    def test_addition(self):
        t1 = Temperature.new(10)
        t2 = Temperature.new(20)
        t3 = Temperature.new(30)
        self.assertEqual(t1 + t2, t3)

    def test_subtraction(self):
        t1 = Temperature.new(10)
        t2 = Temperature.new(20)
        t3 = Temperature.new(30)
        self.assertEqual(t3 - t2, t1)

    def test_str(self):
        t_str = f"{self.t.temp} {self.t.scale}"
        self.assertEqual(self.t.__str__(), t_str)
        self.assertEqual(self.t.__repr__(), t_str)

    def test_validation(self):
        self.assertRaises(TemperatureError, Temperature.new, "string")
        self.assertRaises(TemperatureError, Temperature.new, 10, "F")


class TempRangeTests(TestCase):
    def setUp(self) -> None:
        self.r = TempRange.new(10, 100)

        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.r, TempRange)
        self.assertIsInstance(self.r.min, Temperature)
        self.assertIsInstance(self.r.max, Temperature)
        self.assertIsInstance(self.r.scale, TempScale)

    def test_validation(self):
        bad_value = "Bad Value"
        self.assertRaises(TemperatureError, TempRange.new, bad_value, 100)
        self.assertRaises(TemperatureError, TempRange.new, 100, bad_value)
        self.assertRaises(TemperatureError, TempRange.new, 50, 100, bad_value)

    def test_str_repr(self):
        t_str = f"{self.r.min.temp} \u2013 {self.r.max.temp} {self.r.scale}"
        self.assertEqual(self.r.__str__(), t_str)
        self.assertEqual(self.r.__repr__(), t_str)

    def test_includes_temp(self):
        t = Temperature.new(50)
        self.assertTrue(self.r.includes_temp(t))
        self.assertRaises(TemperatureError, self.r.includes_temp, "temp")

    def test_includes_range(self):
        r = TempRange.new(50, 60)
        self.assertTrue(self.r.includes_range(r))
        self.assertRaises(TemperatureError, self.r.includes_range, "temp")
