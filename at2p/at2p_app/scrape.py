import requests
import re
from bs4 import BeautifulSoup
import numpy as np


def historic_temp(zip: str, country: str) -> int:
    url = weather_url(zip, country, 'historic')
    soup = get_soup(url)
    row = soup.find('tr', {'class': 'sep-t'})
    cells = row.find_all('td')
    historic_temp = int(re.findall(r'\d+', cells[0].text)[0])
    return historic_temp


def forecast_high_low(zip: str, country: str):
    url = weather_url(zip, country, 'forecast')
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
    data = []
    if 'Unknown address' in title.contents[0]:
        return 200
    return soup


def weather_url(zip: str, country: str, forecast_or_historic: str):
    url_prefix = 'https://www.timeanddate.com/weather/@z-'
    if forecast_or_historic == 'forecast':
        return url_prefix + \
            country.lower() + '-' + zip + '/ext'
    elif forecast_or_historic == 'historic':
        return url_prefix + \
            country.lower() + '-' + zip + '/historic'
    else:
        return 'Error'
