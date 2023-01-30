from at2p_app.domain.entities.temperature import TempRange, Temp, TempScale
from at2p_app.domain.entities.location import Place
from datetime import datetime

from at2p_app.domain.use_cases.weather import (
    WeatherReport,
    WeatherReportType,
    WeatherReportError,
)
from at2p_app.domain.use_cases.recommend import (
    Crop,
    TempRequirement,
    ReqList,
    CropError,
    TempRequirementError,
)

from django.test import TestCase


class TestTempReq(TestCase):
    def setUp(self) -> None:
        self.absolute = TempRange(10, 100)
        self.optimal = TempRange(50, 60)
        self.temp_req = TempRequirement(
            absolute=self.absolute, optimal=self.optimal
        )
        return super().setUp()

    def test_create_temp_req_list(self):
        self.assertIsInstance(self.temp_req, TempRequirement)

    def test_validation(self):
        range_in_C = TempRange(50, 60, TempScale.C)
        self.assertRaises(
            TempRequirementError,
            TempRequirement,
            absolute=self.absolute,
            optimal=range_in_C,
        )


class TestTempReqList(TestCase):
    def setUp(self) -> None:
        self.abs_range = TempRange(10, 100)
        self.opt_range = TempRange(40, 60)
        self.temp_reqs = TempRequirement(
            absolute=self.abs_range, optimal=self.opt_range
        )
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.temp_reqs, TempRequirement)

    def test_validation(self):
        bad_range = TempRange(50, 200)
        self.assertRaises(
            TempRequirementError,
            TempRequirement,
            absolute=self.abs_range,
            optimal=bad_range,
        )


class TestReqList(TestCase):
    def setUp(self) -> None:
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        self.temp_req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp_req=self.temp_req)
        return super().setUp()

    def test_creation(self):
        self.assertTrue(type(self.reqs) == dict)


class TestCrop(TestCase):
    def setUp(self) -> None:
        opt = TempRange(30, 50)
        abs = TempRange(10, 100)
        req = TempRequirement(absolute=abs, optimal=opt)
        self.reqs = ReqList(temp=req)
        self.crop_name = "Boberries"
        self.crop = Crop(name=self.crop_name, reqs=self.reqs)
        return super().setUp()

    def test_create_from_dict(self):
        initdict = {"name": self.crop_name, "reqs": self.reqs}
        c = Crop.from_dict(initdict)
        self.assertTrue(isinstance(c, Crop))

    def test_crop_creation(self):
        self.assertTrue(isinstance(self.crop, Crop))

    def test_replace_reqs(self):
        opt = TempRange(40, 45)
        abs = TempRange(20, 90)
        reqs = TempRequirement(absolute=abs, optimal=opt)
        self.new_reqs = reqs
        self.crop.reqs = self.new_reqs
        self.assertEqual(self.crop.reqs, self.new_reqs)

    def test_validate_reqs(self):
        initdict = {"name": self.crop_name, "reqs": Temp(4)}
        self.assertRaises(CropError, Crop.from_dict, initdict)

    def test_str(self) -> None:
        self.assertEqual(self.crop.__str__(), self.crop_name)

    def test_reqs(self) -> None:
        self.assertEqual(self.crop.reqs, self.reqs)

    def test_blank_name(self):
        name = ""
        self.assertRaises(CropError, Crop, name, self.reqs)

    def test_float_name(self):
        name = 14.3
        self.assertRaises(CropError, Crop, name, self.reqs)

    def test_bad_req(self):
        self.reqs["bad"] = 15
        self.assertRaises(CropError, Crop, self.crop_name, self.reqs)


class WeatherReportTypeTest(TestCase):
    def test_str(self):
        t = WeatherReportType.FORECAST
        t_str = t.name.title()
        self.assertEqual(t.__str__(), t_str)


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
        self.forecast = WeatherReport.from_dict(init_dict)

        self.average = Temp(45)
        init_dict = {
            "report_type": WeatherReportType.HISTORIC,
            "location": self.location,
            "average": self.average,
        }
        self.historic = WeatherReport.from_dict(init_dict)
        return super().setUp()

    def test_creation(self):
        self.assertIsInstance(self.forecast, WeatherReport)
        self.assertEqual(self.forecast.location, self.location)
        self.assertEqual(self.forecast.highs, self.highs)
        self.assertEqual(self.forecast.lows, self.lows)
        self.assertIsInstance(self.forecast.time_reported, datetime)

        self.assertIsInstance(self.historic, WeatherReport)
        self.assertEqual(self.historic.location, self.location)
        self.assertEqual(self.historic.average, self.average)
        self.assertIsInstance(self.historic.time_reported, datetime)

    def test_validation(self):
        bad_dict = {
            "location": "Bad Value",
            "highs": self.highs,
            "lows": self.lows,
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )

        bad_dict = {
            "location": self.location,
            "highs": self.highs,
            "lows": self.lows,
            "report_type": "bad type",
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )

        bad_dict = {
            "location": self.location,
            "highs": "bad highs",
            "lows": self.lows,
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )

        bad_dict = {
            "location": self.location,
            "highs": self.highs,
            "lows": "bad lows",
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )

        bad_dict = {
            "location": self.location,
            "average": "bad average",
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )

        bad_dict = {
            "location": self.location,
            "highs": self.highs,
            "lows": self.lows,
            "time_reported": "bad time",
        }
        self.assertRaises(
            WeatherReportError, WeatherReport.from_dict, bad_dict
        )
