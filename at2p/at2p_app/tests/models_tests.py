from django.test import TestCase
from at2p_app.models import Crop, Planter, WeatherInfo


class CropTest(TestCase):
    def create_crop(
        self, name, min_temp, max_temp, min_opt_temp, max_opt_temp
    ):
        return Crop.objects.create(
            name=name,
            min_temp=min_temp,
            max_temp=max_temp,
            min_opt_temp=min_opt_temp,
            max_opt_temp=max_opt_temp,
        )

    def test_crop_creation(self):
        name = 'Boberries'
        min_temp = 0
        max_temp = 100
        min_opt_temp = 20
        max_opt_temp = 80
        c = self.create_crop(
            name=name,
            min_temp=min_temp,
            max_temp=max_temp,
            min_opt_temp=min_opt_temp,
            max_opt_temp=max_opt_temp,
        )
        self.assertTrue(isinstance(c, Crop))
        self.assertEqual(c.__str__(), name)
        self.assertEqual(c.__repr__(), name)

    def test_get_absolute_url(self):
        name = 'Boberries'
        min_temp = 0
        max_temp = 100
        min_opt_temp = 20
        max_opt_temp = 80
        c = self.create_crop(
            name=name,
            min_temp=min_temp,
            max_temp=max_temp,
            min_opt_temp=min_opt_temp,
            max_opt_temp=max_opt_temp,
        )
        self.assertEqual(c.get_absolute_url(), '/crop/' + c.slug)


class PlanterTest(TestCase):
    def create_planter(
        self, zip, country, username='rusty', password='b@A6&Zb!N&^W'
    ):
        return Planter.objects.create(
            username=username, password=password, zip=zip, country=country
        )

    def test_planter_creation(self):
        username = 'shackleford'
        pw = 'b@A6&Zb!N&^W'
        zip = '22401'
        country = 'US'
        p = self.create_planter(
            username=username, password=pw, zip=zip, country=country
        )
        self.assertTrue(isinstance(p, Planter))
        self.assertEqual(p.__str__(), username)
        self.assertEqual(p.__repr__(), username)


class WeatherInfoTest(TestCase):
    def create_weather(
        self, country, zip, lat=None, long=None, avg=None, high=None, low=None
    ):

        return WeatherInfo.objects.create(
            country=country,
            zip=zip,
            lat=lat,
            long=long,
            historic_avg_temp=avg,
            forecast_high_temp=high,
            forecast_low_temp=low,
        )

    def test_weather_creation(self):
        country = 'US'
        zip = '22407'
        w = self.create_weather(country, zip)
        self.assertTrue(isinstance(w, WeatherInfo))
        self.assertEqual(w.__str__(), zip + ', ' + country)
        self.assertEqual(w.__repr__(), zip + ', ' + country)

    def test_set_lat_long(self):
        country = 'US'
        zip = '22407'
        w = self.create_weather(country, zip)
        w.set_lat_and_long()
        self.assertEquals(w.lat, 38.2688)
        self.assertEquals(w.long, -77.5476)

    def test_clean(self):
        country = 'US'
        zip = '22407'
        w = self.create_weather(country, zip)
        w.clean()
        self.assertIsNotNone(w.lat)
        self.assertIsNotNone(w.long)

    def test_update_weather(self):
        country = 'US'
        zip = '22407'
        w = self.create_weather(country, zip)
        w.update_weather()
        self.assertIsNotNone(w.historic_avg_temp)
        self.assertIsNotNone(w.forecast_high_temp)
        self.assertIsNotNone(w.forecast_low_temp)
