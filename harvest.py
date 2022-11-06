import re
import urllib3
from bs4 import BeautifulSoup
from house import House

http = urllib3.PoolManager()
headers = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; ru-ru; Redmi 5 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.2.4-g'}

municipality = 'amsterdam'
fundaUrl = f'http://www.funda.nl/koop/{municipality}/beschikbaar/'

response = http.request('GET', fundaUrl, headers=headers)
data = response.data

soup = BeautifulSoup(data, 'html.parser')
search_result_header_class = 'search-result__header'
search_result_price_class = 'search-result-price'
search_result_header_title_class = 'search-result__header-title'
search_result_header_subtitle_class = 'search-result__header-subtitle'

header_divs = soup.find_all('div', {'class': search_result_header_class})
title_h2s = soup.find_all(
    'h2', {'class': search_result_header_title_class})
subtitle_h4s = soup.find_all(
    'h4', {'class': search_result_header_subtitle_class})
price_spans = soup.find_all('span', {'class': search_result_price_class})


def retrieve_id_from_div(div):
    href = (div.find('a')['href'])
    str = href.split('/')[3]
    lol = str.replace('huis-', '')
    id = lol.split('-')[0]
    return id


def extract_street_and_housenumber(title_h2s, index):
    return title_h2s[index].text.strip()


def extract_postal_code_and_city(subtitle_h4s, index):
    return subtitle_h4s[index].text


def extract_postal_code(postal_code_and_city):
    split_postal_code_and_city = postal_code_and_city.split()
    return split_postal_code_and_city[0] + ' ' + split_postal_code_and_city[1]


def extract_city(postal_code_and_city):
    return postal_code_and_city.split()[2]


def extract_price(price_spans, index):
    return re.findall('([0-9]+[,.]+[0-9]+)', price_spans[index].text)


for index, div in enumerate(header_divs):
    id = retrieve_id_from_div(div)
    street_and_house_number = extract_street_and_housenumber(title_h2s, index)
    postal_code_and_city = extract_postal_code_and_city(subtitle_h4s, index)
    postalCode = extract_postal_code(postal_code_and_city)
    city = extract_city(postal_code_and_city)
    price = extract_price(price_spans, index)

    house = House(id, street_and_house_number, postalCode, city, price)
    print(house)
