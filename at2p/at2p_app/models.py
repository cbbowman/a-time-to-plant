from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from . import country_codes
from .scrape import historic_temp, forecast_high_low
from django.core.exceptions import ValidationError
import pgeocode


COUNTRIES_ONLY = country_codes.COUNTRIES_ONLY


class Planter(AbstractUser):
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)

    def clean(self) -> None:
        n = pgeocode.Nominatim(self.country.code)
        print(n.query_postal_code(self.zip).country_code)
        if self.country.code == n.query_postal_code(self.zip).country_code:
            return
        else:
            raise ValidationError("Submitted value is not a valid ZIP code")

    def __str__(self) -> str:
        return self.username


class WeatherInfo(models.Model):
    historic_avg_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_high_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_low_temp = models.SmallIntegerField(blank=True, null=True)
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.historic_avg_temp = 0
        self.forecast_high_temp = 1
        self.forecast_low_temp = 2
        super().__init__(*args, **kwargs)

    def update_weather(self):
        self.historic_avg_temp = historic_temp(self.zip, self.country.code)
        forecast = forecast_high_low(self.zip, self.country.code)
        self.forecast_high_temp = forecast[0]
        self.forecast_low_temp = forecast[1]
        self.save()
