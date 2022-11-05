import urllib3
import codecs

http = urllib3.PoolManager()
headers = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; ru-ru; Redmi 5 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.2.4-g'}

fundaUrl = 'http://www.funda.nl/koop/utrecht/beschikbaar/'

response = http.request('GET', fundaUrl, headers=headers)
dataDecoded = response.data.decode('utf-8')

print('STATUS: ', response.status, '/n/n')
print('HEADERS: ', response.headers, '/n/n')
print('DATA: ', response.data, '/n/n')
print('DATA DECODED: ', dataDecoded, '/n/n') # Do we need this?



file = codecs.open("utrecht", "w", "utf-8")
file.write(dataDecoded)
file.close()
