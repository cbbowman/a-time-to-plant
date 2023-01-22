import requests
import re
from bs4 import BeautifulSoup
import numpy as np
from django.core.exceptions import ValidationError


def historic_temp(lat: str, long: str) -> int:
    url = weather_url(lat, long, 'historic')
    soup = get_soup(url)
    row = soup.find('tr', {'class': 'sep-t'})
    cells = row.find_all('td')
    historic_temp = int(re.findall(r'\d+', cells[0].text)[0])
    return historic_temp


def forecast_high_low(lat: str, long: str):
    url = weather_url(lat, long, 'forecast')
    soup = get_soup(url)
    forecast_table = soup.find('table', id='wt-ext')
    table_body = forecast_table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cells = row.find_all('td')
        temps = re.findall(r'\d+', cells[1].text)
        data.append(list((int(temps[0]), int(temps[1]))))
    data_t = np.transpose(data)
    high = np.max(data_t[0])
    low = np.min(data_t[1])
    return [high, low]


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    head_tag = soup.head
    title = head_tag.title
    if 'Unknown address' in title.contents[0]:
        raise ValidationError(
            "Scraping error: address not found.")
    return soup


def weather_url(lat, long, forecast_or_historic: str):
    url_prefix = 'https://www.timeanddate.com/weather/@'
    if forecast_or_historic == 'forecast':
        return url_prefix + str(lat) + ',' + str(long) + '/ext'
    elif forecast_or_historic == 'historic':
        return url_prefix + str(lat) + ',' + str(long) + '/historic'
    else:
        raise ValidationError(
            "weather_url called incorrectly")
