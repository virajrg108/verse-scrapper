from importlib.resources import contents
import requests
import json
from bs4 import BeautifulSoup

def get_canto_details(canto_nbr):
    # print('getting details of Canto ', canto_nbr)
    html = requests.get('https://vedabase.io/en/library/sb/{}'.format(canto_nbr))
    parsed_html = BeautifulSoup(html.text, features="html.parser")
    cantoTitle = parsed_html.body.find('div', attrs={'class': 'r-canto'}).decode_contents()
    # print(cantoTitle)
    chaptersRaw = parsed_html.body.select('div.bb.r-chapter')

    chaptersRaw = list(filter(lambda x: "CHAPTER" in x.decode_contents(), chaptersRaw))
    # print(chaptersRaw)

    chapters = []
    for i in range(len(chaptersRaw)):
        chapters.append({ "id": i, "name": chaptersRaw[i].find('a').decode_contents().strip()})
    
    return chapters


def scrap_sb():
    chapters = get_canto_details(2)
    
    # html = requests.get('https://vedabase.io/en/library/sb/1/1/1')
    # parsed_html = BeautifulSoup(html.text)
    # verseNbr = parsed_html.body.find('div', attrs={'id': 'bb13392'}).decode_contents()
    # sanskritText = parsed_html.body.find('div', attrs={'id':'bb554882'}).decode_contents()
    # englishText = parsed_html.body.find('div', attrs={'id':'bb13393'}).decode_contents()
    # synonyms = parsed_html.body.find('div', attrs={'id':'bb13394'}).decode_contents()
    # translation = parsed_html.body.find('div', attrs={'id':'bb13395'}).decode_contents()
    # purport = parsed_html.body.find('div', attrs={'class':'wrapper-puport'})

    # for title in purport.select('h2.section-title'):
    #     title.decompose()

    # print(purport)

if __name__ == "__main__":
    scrap_sb()

