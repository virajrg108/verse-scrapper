from importlib.resources import contents
import requests
import json
from bs4 import BeautifulSoup


verse = {}
html = requests.get('https://vedabase.io/en/library/sb/1/15/21')
parsed_html = BeautifulSoup(html.text, features="html.parser")
verse['verseNbr'] = parsed_html.body.select('div.r-title.r-verse')[0].decode_contents().strip()
verse['sanskritText'] = parsed_html.body.find('div', attrs={'class':'r-devanagari'}).decode_contents().strip()
verse['englishText'] = parsed_html.body.find('div', attrs={'class':'r-verse-text'}).decode_contents().strip()
verse['synonyms'] = parsed_html.body.find('div', attrs={'class':'r-synonyms'}).decode_contents().strip()
verse['translation'] = parsed_html.body.find('div', attrs={'class':'r-translation'}).decode_contents().strip()
verse['purport'] = parsed_html.body.find('div', attrs={'class':'wrapper-puport'})
if verse['purport'] is not None:
    verse['purport'] = verse['purport'].decode_contents().strip()
print(verse)