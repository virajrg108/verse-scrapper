import requests
import json
from bs4 import BeautifulSoup

def scrap_sb():
    html = requests.get('https://vedabase.io/en/library/sb/1/1/1')
    parsed_html = BeautifulSoup(html.text)
    verseNbr = parsed_html.body.find('div', attrs={'id': 'bb13392'}).decode_contents()
    sanskritText = parsed_html.body.find('div', attrs={'id':'bb554882'}).decode_contents()
    englishText = parsed_html.body.find('div', attrs={'id':'bb13393'}).decode_contents()
    synonyms = parsed_html.body.find('div', attrs={'id':'bb13394'}).decode_contents()
    translation = parsed_html.body.find('div', attrs={'id':'bb13395'}).decode_contents()
    purport = parsed_html.body.find('div', attrs={'class':'wrapper-puport'})

    for title in purport.select('h2.section-title'):
        title.decompose()

    print(purport)

if __name__ == "__main__":
    scrap_sb()

