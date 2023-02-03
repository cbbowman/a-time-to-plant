from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField
from .static import COUNTRIES_ONLY
from .scrape import historic_temp, forecast_high_low
import pgeocode
from django.urls import reverse_lazy
from math import exp


COUNTRIES_ONLY = COUNTRIES_ONLY
COUNTRIES_FIRST = ["US"]


class CropModel(models.Model):
    id = models.PositiveIntegerField("Crop ID", primary_key=True)
    name = models.CharField("Name", max_length=64)
    abs_low = models.SmallIntegerField("Absolute Low Temperature")
    abs_high = models.SmallIntegerField("Absolute High Temperature")
    opt_low = models.SmallIntegerField("Optimal Low Temperature")
    opt_high = models.SmallIntegerField("Optimal High Temperature")


class Crop(models.Model):
    name = models.CharField("Name", max_length=50)
    min_temp = models.SmallIntegerField("Minimum Temperature")
    min_opt_temp = models.SmallIntegerField("Optimum Lower Temperature")
    max_opt_temp = models.SmallIntegerField("Optimum Upper Temperature")
    max_temp = models.SmallIntegerField("Maximum Temperature")
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)

    def get_absolute_url(self):
        return reverse_lazy("crop-detail", kwargs={"slug": self.slug})


class Planter(AbstractUser):
    country = CountryField(default="US", blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    crops = models.ManyToManyField(Crop, through="TimeToPlant", blank=True)

    def __str__(self) -> str:
        return str(self.username)

    def __repr__(self) -> str:
        return str(self.username)


class WeatherInfo(models.Model):
    country = CountryField(default="US")
    zip = models.CharField(max_length=10)
    lat = models.DecimalField(
        max_digits=7, decimal_places=4, blank=True, null=True
    )
    long = models.DecimalField(
        max_digits=7, decimal_places=4, blank=True, null=True
    )
    historic_avg_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_high_temp = models.SmallIntegerField(blank=True, null=True)
    forecast_low_temp = models.SmallIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.zip + ", " + self.country.code

    def __repr__(self) -> str:
        return self.zip + ", " + self.country.code

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.historic_avg_temp = 0
        self.forecast_high_temp = 1
        self.forecast_low_temp = 2
        self.lat = 0
        self.long = 0
        super().__init__(*args, **kwargs)

    def set_lat_and_long(self):
        n = pgeocode.Nominatim(self.country.code)
        place = n.query_postal_code(self.zip)
        self.lat = float(place.latitude)
        self.long = float(place.longitude)
        self.save()
        return

    def clean(self) -> None:
        self.set_lat_and_long()
        return super().clean()

    def update_weather(self):
        self.clean()
        self.historic_avg_temp = historic_temp(self.lat, self.long)
        forecast = forecast_high_low(self.lat, self.long)
        self.forecast_high_temp = forecast[0]
        self.forecast_low_temp = forecast[1]
        self.save()


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
        ordering = ["-plantable_score", "crop"]

    def __str__(self) -> str:
        return f"{self.planter}'s {self.crop}"

    def __repr__(self) -> str:
        return f"{self.planter}'s {self.crop}"

    def update_plantable(self, w):
        mn = self.crop.min_temp
        mx = self.crop.max_temp
        ol = self.crop.min_opt_temp
        oh = self.crop.max_opt_temp
        low = w.forecast_low_temp
        high = w.forecast_high_temp
        soil = w.historic_avg_temp

        chill = max((mn - low), 0) / max((ol - mn), 1)
        cook = max((high - mx), 0) / max((mx - oh), 1)
        sl = max(max(soil - oh, 0), max(ol - soil, 0)) / (oh - ol)
        score = round(exp(-max(chill, cook, sl)), 2)

        self.chill = chill
        self.cook = cook
        self.soil = sl
        self.plantable_score = score
        self.plantable = score == 1.00
        self.save()
