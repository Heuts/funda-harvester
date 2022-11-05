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
dataDecoded = data.decode('utf-8')

soup = BeautifulSoup(data, 'html.parser')
houseSearchResultClass = 'search-result__header'
priceClass = 'search-result-price'
houseSearchResultClassTitleClass = 'search-result__header-title'
houseSearchResultClassSubtitleClass = 'search-result__header-subtitle'
houseSearchResultDivs = soup.find_all('div', {'class': houseSearchResultClass})
houseSearchResultClassTitleh2s = soup.find_all(
    'h2', {'class': houseSearchResultClassTitleClass})
houseSearchResultClassSubtitle4s = soup.find_all(
    'h4', {'class': houseSearchResultClassSubtitleClass})
priceSpans = soup.find_all('span', {'class': priceClass})

for index, div in enumerate(houseSearchResultDivs):
    href = (div.find('a')['href'])
    str = href.split('/')[3]
    lol = str.replace('huis-', '')
    id = lol.split('-')[0]
    streetAndHouseNumber = houseSearchResultClassTitleh2s[index].text.strip()
    postalCodeAndCity = houseSearchResultClassSubtitle4s[index].text
    splitted = postalCodeAndCity.split()
    postalCode = splitted[0] + ' ' + splitted[1]
    city = splitted[2]
    price = re.findall("([0-9]+[,.]+[0-9]+)", priceSpans[index].text)


    house = House(id, streetAndHouseNumber, postalCode, city, price)
    print(house)

