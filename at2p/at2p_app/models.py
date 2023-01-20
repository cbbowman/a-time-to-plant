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
# COUNTRIES_ONLY = ['AD', 'AR', 'AS', 'AT', 'AU', 'AX', 'AZ', 'BD', 'BE', 'BG', 'BM',
#                   'BR', 'BY', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK',
#                   'DO', 'DZ', 'EE', 'ES', 'FI', 'FM', 'FO', 'FR', 'GB', 'GF', 'GG',
#                   'GL', 'GP', 'GT', 'GU', 'HR', 'HT', 'HU', 'IE', 'IM', 'IN', 'IS',
#                   'IT', 'JE', 'JP', 'KR', 'LI', 'LK', 'LT', 'LU', 'LV', 'MC', 'MD',
#                   'MH', 'MK', 'MP', 'MQ', 'MT', 'MW', 'MX', 'MY', 'NC', 'NL', 'NO',
#                   'NZ', 'PE', 'PH', 'PK', 'PL', 'PM', 'PR', 'PT', 'PW', 'RE', 'RO',
#                   'RS', 'RU', 'SE', 'SG', 'SI', 'SJ', 'SK', 'SM', 'TH', 'TR', 'UA',
#                   'US', 'UY', 'VA', 'VI', 'WF', 'YT', 'ZA']


class Crop(models.Model):
    name = models.CharField(max_length=50)
    min_temp = models.SmallIntegerField()
    min_opt_temp = models.SmallIntegerField()
    max_opt_temp = models.SmallIntegerField()
    max_temp = models.SmallIntegerField()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class Planter(AbstractUser):
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)
    crops = models.ManyToManyField(Crop, through='TimeToPlant')

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
        return self.username


class TimeToPlant(models.Model):
    planter = models.ForeignKey(Planter, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    plantable = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)


class WeatherInfo(models.Model):
    historic_avg_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_high_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_low_temp = models.SmallIntegerField(blank=True, null=True)
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)
    lat = models.CharField(max_length=10, blank=True, null=True)
    long = models.CharField(max_length=10, blank=True, null=True)

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
