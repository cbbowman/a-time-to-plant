import requests
import re
from bs4 import BeautifulSoup
import numpy as np


def weather_url(zip: str, country: str, forecast_or_historic: str):
    if forecast_or_historic == 'forecast':
        return 'https://www.timeanddate.com/weather/@z-' + \
            country.lower() + '-' + zip + '/ext'
    elif forecast_or_historic == 'historic':
        return 'https://www.timeanddate.com/weather/@z-' + \
            country.lower() + '-' + zip + '/historic'
    else:
        return 'Error'



def historic_temp(zip: str, country: str) -> int:
    url = weather_url(zip, country, 'historic')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    head_tag = soup.head
    title = head_tag.title
    if 'Unknown address' in title.contents[0]:
        return 200
    row = soup.find('tr', {'class': 'sep-t'})
    cells = row.find_all('td')
    historic_temp = int(re.findall(r'\d+', cells[0].text)[0])
    return historic_temp


def forecast_high(zip: str, country: str) -> int:
    url = weather_url(zip, country, 'forecast')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    head_tag = soup.head
    title = head_tag.title
    data = []
    if 'Unknown address' in title.contents[0]:
        return 200
    forecast_table = soup.find('table', id='wt-ext')
    table_body = forecast_table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        temps = re.findall(r'\d+', cells[1].text)
        data.append(list((int(temps[0]), int(temps[1]))))
    data = np.transpose(data)
    high = data[0].max()
    return high


def forecast_low(zip: str, country: str) -> int:
    url = weather_url(zip, country, 'forecast')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    head_tag = soup.head
    title = head_tag.title
    data = []
    if 'Unknown address' in title.contents[0]:
        return 200
    forecast_table = soup.find('table', id='wt-ext')
    table_body = forecast_table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        temps = re.findall(r'\d+', cells[1].text)
        data.append(list((int(temps[0]), int(temps[1]))))
    data = np.transpose(data)
    low = data[1].min()
    return low
