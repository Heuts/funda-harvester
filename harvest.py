import re
import urllib3
import json
from bs4 import BeautifulSoup
from house import House
import time
import datetime

start = time.time()
http = urllib3.PoolManager()
headers = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; ru-ru; Redmi 5 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.2.4-g'}

municipality = 'lopik'
fundaUrl = f'http://www.funda.nl/koop/{municipality}/beschikbaar/'

response = http.request('GET', fundaUrl, headers=headers)
data = response.data

soup = BeautifulSoup(data, 'html.parser')
search_result_header_class = 'search-result__header'
search_result_price_class = 'search-result-price'
search_result_header_title_class = 'search-result__header-title'
search_result_header_subtitle_class = 'search-result__header-subtitle'
pagination_class = 'pagination-pages'

pagination_hyperlinks = soup.find(
    'div', {'class': pagination_class}).find_all('a')

# TODO: Improve nested for loop
maxPage = 0
for hyperlink in pagination_hyperlinks:
    pages = [int(s) for s in hyperlink.text.split() if s.isdigit()]
    for page in pages:
        if page > maxPage:
            maxPage = page


def retrieve_house_id_from_div(div):
    href = (div.find('a')['href'])
    id = href.split('/')[3].replace('huis-', '').replace('appartement-', '').replace('parkeergelegenheid', '').split('-')[0]
    return id


def extract_street_and_housenumber(title_h2s, index):
    return title_h2s[index].text.strip()


def extract_postal_code_and_city(subtitle_h4s, index):
    return subtitle_h4s[index].text


def extract_postal_code(postal_code_and_city):
    split_postal_code_and_city = postal_code_and_city.split()
    return split_postal_code_and_city[0] + ' ' + split_postal_code_and_city[1]


def extract_city(postal_code_and_city):
    if (len(postal_code_and_city.split()) < 3):
        return 'default-city'
    return postal_code_and_city.split()[2]


def extract_price(price_spans, index):
    prices = re.findall('([0-9]+[,.]+[0-9]+)', price_spans[index].text)
    if (len(prices) < 1):
        return 0
    return prices[0]

houses = []

for index in range(maxPage):
    fundaUrl = f'http://www.funda.nl/koop/{municipality}/beschikbaar'
    if (index != 0):
        fundaUrl = fundaUrl + f'/p{index+1}'

    response = http.request('GET', fundaUrl, headers=headers)
    data = response.data

    soup = BeautifulSoup(data, 'html.parser')
    
    header_divs = soup.find_all('div', {'class': search_result_header_class})
    title_h2s = soup.find_all(
        'h2', {'class': search_result_header_title_class})
    subtitle_h4s = soup.find_all(
        'h4', {'class': search_result_header_subtitle_class})
    price_spans = soup.find_all('span', {'class': search_result_price_class})
    
    for index, div in enumerate(header_divs):
        id = retrieve_house_id_from_div(div)
        street_and_house_number = extract_street_and_housenumber(
            title_h2s, index)
        postal_code_and_city = extract_postal_code_and_city(
            subtitle_h4s, index)
        postalCode = extract_postal_code(postal_code_and_city)
        city = extract_city(postal_code_and_city)
        price = extract_price(price_spans, index)

        house = House(id, street_and_house_number, postalCode, city, price)
        houses.append(house)

with open('houses.json', 'w', encoding='utf-8') as f:
    json.dump([house.__dict__ for house in houses], f, indent=2)

end = time.time()
print(str(datetime.timedelta(seconds=end-start)))