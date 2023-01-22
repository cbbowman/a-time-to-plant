from django.test import TestCase
from django.core.exceptions import ValidationError
import at2p_app.scrape as s


class TestScrape(TestCase):

    def test_forecast_url(self):
        lat = 38.3365
        long = -77.4366
        url = 'https://www.timeanddate.com/weather/@38.3365,-77.4366/ext'
        self.assertEqual(url, s.weather_url(lat, long, 'forecast'))

    def test_historic_url(self):
        lat = 38.3365
        long = -77.4366
        url = 'https://www.timeanddate.com/weather/@38.3365,-77.4366/historic'
        self.assertEqual(url, s.weather_url(lat, long, 'historic'))
