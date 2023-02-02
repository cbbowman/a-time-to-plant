from django.test import TestCase
from at2p_app.domain.value_objects.temperature import (
    TempRange,
    Temperature,
    TempScale,
    TemperatureError
)


class TemperatureObjectTests(TestCase):
    def setUp(self) -> None:
        self.n = 40
        self.t = Temperature.new(self.n)
        return super().setUp()

    def test_instantiation(self):
        self.assertIsInstance(self.t, Temperature)
        self.assertIsInstance(self.t.scale, TempScale)
        self.assertEqual(self.t.temp, self.n)
        self.assertEqual(self.t.scale, TempScale.F)

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

    def test_str(self):
        t_str = f"{self.r.min.temp} \u2013 {self.r.max.temp} {self.r.scale}"
        self.assertEqual(self.r.__str__(), t_str)
        self.assertEqual(self.r.__repr__(), t_str)
