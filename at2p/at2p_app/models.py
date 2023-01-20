from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from . import country_codes
from .scrape import historic_temp, forecast_high_low
from django.core.exceptions import ValidationError
import pgeocode


COUNTRIES_ONLY = country_codes.COUNTRIES_ONLY
COUNTRIES_FIRST = ['US']


class Crop(models.Model):
    name = models.CharField(max_length=50)
    min_temp = models.SmallIntegerField()
    min_opt_temp = models.SmallIntegerField()
    max_opt_temp = models.SmallIntegerField()
    max_temp = models.SmallIntegerField()

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)


class Planter(AbstractUser):
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)
    crops = models.ManyToManyField(Crop, through='TimeToPlant', blank=True)

    def clean(self) -> None:
        if self.zip is None:
            return
        n = pgeocode.Nominatim(self.country.code)
        if self.country.code == n.query_postal_code(self.zip).country_code:
            return
        else:
            raise ValidationError(
                "Model error: Country / ZIP combination is invalid.")

    def __str__(self) -> str:
        return str(self.username)

    def __repr__(self) -> str:
        return str(self.username)


class TimeToPlant(models.Model):
    planter = models.ForeignKey(Planter, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    plantable = models.BooleanField(default=False)
    chill = models.FloatField(blank=True, null=True)
    cook = models.FloatField(blank=True, null=True)
    soil = models.FloatField(blank=True, null=True)
    plantable_score = models.FloatField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-plantable_score', 'crop']

    def __str__(self) -> str:
        return self.planter + "'s " + self.crop

    def __repr__(self) -> str:
        return self.planter + "'s " + self.crop

    def update_plantable(self, w):
        mn = self.crop.min_temp
        mx = self.crop.max_temp
        ol = self.crop.min_opt_temp
        oh = self.crop.max_opt_temp
        low = w.forecast_low_temp
        high = w.forecast_high_temp
        soil = w.historic_avg_temp

        chill = (low - mn) / max((ol - mn), 1)
        cook = (mx - high) / max((mx - oh), 1)
        sl = min(soil - ol, oh - soil) / ((oh - ol) / 2)
        score = min(chill, cook, sl)

        self.chill = chill
        self.cook = cook
        self.soil = sl
        self.plantable_score = score
        soil_ok = (self.crop.max_opt_temp > w.historic_avg_temp) \
            and (self.crop.min_opt_temp < w.historic_avg_temp)
        high_ok = self.crop.max_temp > w.forecast_high_temp
        low_ok = self.crop.min_temp < w.forecast_low_temp
        self.plantable = soil_ok and high_ok and low_ok
        self.save()


class WeatherInfo(models.Model):
    historic_avg_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_high_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_low_temp = models.SmallIntegerField(blank=True, null=True)
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)
    lat = models.CharField(max_length=10, blank=True, null=True)
    long = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return self.zip + ', ' + self.country

    def __repr__(self) -> str:
        return self.zip + ', ' + self.country

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.historic_avg_temp = 0
        self.forecast_high_temp = 1
        self.forecast_low_temp = 2
        self.lat = 0
        self.long = 0
        super().__init__(*args, **kwargs)

    def clean(self) -> None:
        n = pgeocode.Nominatim(self.country.code)
        place = n.query_postal_code(self.zip)
        self.lat = str(place.latitude)
        self.long = str(place.longitude)
        return super().clean()

    def update_weather(self):
        self.historic_avg_temp = historic_temp(self.lat, self.long)
        forecast = forecast_high_low(self.lat, self.long)
        self.forecast_high_temp = forecast[0]
        self.forecast_low_temp = forecast[1]
        self.save()
