import logging

import requests
from bs4 import BeautifulSoup
import pandas as pd

from smallstations import io


def run():
    logging.info('Getting station and lines from wikipedia: ...')

    stations_url = 'https://fr.wikipedia.org/wiki/Liste_des_stations_du_m%C3%A9tro_de_Paris'
    table = get_table_from_wiki(stations_url)
    stations = parse_station_table_as_dataframe(table)
    io.save_dataframe(stations, 'stations_and_lines.csv')

    logging.info('Getting station and lines from wikipedia: completed!')


def get_table_from_wiki(stations_url):
    logging.info('Getting table from url: ' + stations_url)
    result = requests.get(stations_url)
    soup = BeautifulSoup(result.content,'html5lib')
    table = soup.find_all('table')[0]
    return table


def parse_station_table_as_dataframe(table):
    stations = []
    for i, row in enumerate(table.findAll('tr')):
        station = {}
        columns = row.findAll('td')
        try:
            stations += _parse_columns_as_dicts(columns)
        except IndexError:
            continue
    stations = pd.DataFrame.from_records(stations)
    return stations

def _parse_columns_as_dicts(columns):
    stations = []
    station = _parse_station_name(columns[0])
    frequentation = _parse_frequentation(columns[6])

    lines_infos = columns[1].findAll('a')
    for infos in lines_infos:
        line_name = _parse_line_name(infos)
        line_url = _parse_line_url(infos)

        stations.append({
            'station': station,
            'frequentation': frequentation,
            'line': line_name,
            'line_url': line_url,
        })

    return stations


def _parse_station_name(elt):
    return elt.text.strip().replace('\u200d', '')

def _parse_frequentation(elt):
    return int(elt.text.strip().replace('\xa0', '').replace('+0', '').replace(',', ''))

def _parse_line_name(elt):
    return elt.attrs['title'].replace('\xa0', ' ').replace(' du métro de Paris', '')

def _parse_line_url(elt):
    return 'https://fr.wikipedia.org' + elt.attrs['href']
