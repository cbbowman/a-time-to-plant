import numpy as np
import requests
import re
from abc import ABC, abstractmethod, abstractclassmethod
from bs4 import BeautifulSoup
from dataclasses import dataclass
from django.core.exceptions import ValidationError
from at2p_app.domain.common.error import WeatherError
from at2p_app.domain.value_objects.weather import Weather
from at2p_app.domain.value_objects.temperature import Temperature
from at2p_app.domain.entities.place import Place


class WeatherSource(ABC):

    _place: Place

    @abstractclassmethod
    def new(self):
        pass

    def _validate(cls):
        pass

    @abstractmethod
    def get(self):
        pass


@dataclass
class WeatherScraper(WeatherSource):

    _place: Place
    _url_prefix: str = "https://www.timeanddate.com/weather/@z-"

    @classmethod
    def new(cls, place: Place):
        cls._validate(place)
        return cls(place)

    @classmethod
    def _validate(cls, place: Place):
        cls._check_place(place)
        return

    @classmethod
    def _check_place(cls, place: Place):
        if not isinstance(place, Place):
            return WeatherError

    def get(self):
        avg = self.historic_temp()
        high, low = self.forecast_high_low()
        weather_report = Weather.new(self._place.id, high, low, avg)
        return weather_report

    def historic_temp(self) -> Temperature:
        url = self.weather_url("historic")
        soup = self.get_soup(url)
        row = soup.find("tr", {"class": "sep-t"})
        cells = row.find_all("td")
        historic_temp = int(re.findall(r"\d+", cells[0].text)[0])
        return Temperature.new(historic_temp)

    def forecast_high_low(self) -> Temperature:
        url = self.weather_url("ext")
        soup = self.get_soup(url)
        forecast_table = soup.find("table", id="wt-ext")
        table_body = forecast_table.find("tbody")
        rows = table_body.find_all("tr")
        data = []
        for row in rows:
            cells = row.find_all("td")
            temps = re.findall(r"\d+", cells[1].text)
            data.append(list((int(temps[0]), int(temps[1]))))
        data_t = np.transpose(data)
        high = np.max(data_t[0])
        low = np.min(data_t[1])
        return Temperature.new(int(high)), Temperature.new(int(low))

    def get_soup(self, url) -> BeautifulSoup:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")
        head_tag = soup.head
        title = head_tag.title
        if "Unknown address" in title.contents[0]:
            raise ValidationError("Scraping error: address not found.")
        return soup

    def weather_url(self, type_postfix: str):
        country = self._place.country.code
        zip_code = self._place.zip_code.zip
        return f"{self._url_prefix}{country.lower()}-{zip_code}/{type_postfix}"
