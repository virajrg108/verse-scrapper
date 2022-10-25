import requests
from bs4 import BeautifulSoup

html = requests.get('https://vedabase.io/en/library/sb/1/1/1')
parsed_html = BeautifulSoup(html.text)
print(parsed_html.body.find('div', attrs={'id': 'bb13392'}).decode_contents())
print(parsed_html.body.find('div', attrs={'id':'bb554882'}).decode_contents())
print(parsed_html.body.find('div', attrs={'id':'bb13393'}).decode_contents())
print(parsed_html.body.find('div', attrs={'id':'bb13394'}).decode_contents())
print(parsed_html.body.find('div', attrs={'id':'bb13394'}).decode_contents())
print(parsed_html.body.find('div', attrs={'id':'bb13395'}).decode_contents())
print(parsed_html.body.find('div', attrs={'id':'bb13395'}).decode_contents())
