from datetime import datetime
from django.test import TestCase
from at2p_app.domain.entities.location import Place
from at2p_app.domain.entities.temperature import TempRange, Temp
from at2p_app.domain.entities.weather import (
    WeatherReport,
    WeatherReportType,
    WeatherReportError,
)


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
