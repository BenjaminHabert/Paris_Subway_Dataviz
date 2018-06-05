import logging
import re

import requests
from bs4 import BeautifulSoup

from smallstations import io


def run():
    logging.info('Getting additional line infos from wikipedia: ...')

    stations = io.load_dataframe('stations_and_lines.csv')
    lines = stations.drop_duplicates(subset=['line']).copy()
    lines = add_color_info(lines)
    lines = add_index_info(lines)
    stations = stations.merge(
        lines.loc[:, ['line', 'line_color', 'line_index']],
        how='left', on='line'
    )
    io.save_dataframe(stations, 'stations_and_lines_with_color.csv')

    logging.info('Getting additional line infos: completed!')


def add_color_info(lines):
    lines['line_color'] = lines['line_url'].apply(_get_color_from_url)
    return lines

def add_index_info(lines):
    lines['line_number'] = lines['line'].apply(lambda s: int(re.findall('\d+', s)[0]))
    lines['line_text_length'] = lines['line'].apply(len)
    lines.sort_values(by=['line_number', 'line_text_length'], inplace=True)
    lines['line_index'] = range(len(lines))
    return lines


def _get_color_from_url(line_url):
    # example url: https://fr.wikipedia.org/wiki/Ligne_9_du_m%C3%A9tro_de_Paris
    result = requests.get(line_url)
    soup = BeautifulSoup(result.content,'html5lib')
    div_with_color = soup.find_all('td', 'entete defaut')[0]
    div_style = div_with_color.attrs['style']
    color = re.search(r'background-color:(#[\w\d]{6})', div_style).group(1)
    return color
