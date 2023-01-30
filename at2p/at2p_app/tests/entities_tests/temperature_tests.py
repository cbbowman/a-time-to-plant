from django.test import TestCase
from at2p_app.domain.entities.temperature import (
    Temp,
    TempRange,
    TemperatureError,
    TempRangeError,
    TempScale,
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

        t = 50
        self.assertRaises(TempRangeError, temp_range.includes, t)
