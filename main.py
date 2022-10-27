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
    
    return cantoTitle, chapters

def cleanVerseNbrs(verseList):
    # print("verseList1:", verseList)
    verseList = list(filter(lambda x: "Text" in x.decode_contents(), verseList))
    verseList = map(lambda x: str(x), verseList)
    # print("verseList2:", verseList)
    newVerseList = []
    for v in verseList:
        if "Texts" in v:
            newVerseList.append(str(v[v.find('Texts')+6:v.find(':')]))
        else:
            newVerseList.append(str(v[v.find('Text')+5:v.find(':')]))
    print("verseList3:", list(newVerseList))
    return newVerseList

def fetchCanto(canto_nbr):
    cantoTitle, chapters = get_canto_details(canto_nbr)
    cantoDetails = { 'name': cantoTitle.strip(), 'totalChapters': len(chapters), 'chapters': chapters }
    with open('/content/drive/MyDrive/Colab Notebooks/sb/sb_canto{}_details.json'.format(canto_nbr), 'w+') as outfile:
        outfile.seek(0)
        outfile.write(json.dumps(cantoDetails, indent=4))

    print(cantoDetails)

    # fetch all the chapters one by one
    # determine the total verses in this chapter
    for chapterNbr in range(len(chapters)):
        chapter = {}
        html = requests.get('https://vedabase.io/en/library/sb/{}/{}'.format(canto_nbr, chapterNbr+1))
        parsed_html = BeautifulSoup(html.text, features="html.parser")
        chapterTitleDiv = parsed_html.find('div', attrs={'class':'r-chapter-title'}).decode_contents()
        versesDiv =  parsed_html.findAll('dl', attrs={'class':'r-verse'})
        chapter['verseNbrs'] = cleanVerseNbrs(versesDiv)
        print(versesDiv)
        chapter['totalVerses'] = len(chapter['verseNbrs'])
        chapter['name'] = chapterTitleDiv
        print(chapter['verseNbrs'])

        verses = []

        for i in range(chapter['totalVerses']):
            verse = {}
            print('https://vedabase.io/en/library/sb/{}/{}/{}'.format(canto_nbr, chapterNbr+1, chapter['verseNbrs'][i]))
            html = requests.get('https://vedabase.io/en/library/sb/{}/{}/{}'.format(canto_nbr, chapterNbr+1, chapter['verseNbrs'][i]))
            parsed_html = BeautifulSoup(html.text, features="html.parser")
            verse['verseNbr'] = parsed_html.body.select('div.r-title.r-verse')[0].decode_contents().strip()
            verse['sanskritText'] = parsed_html.body.find('div', attrs={'class':'r-devanagari'}).decode_contents().strip()
            verse['englishText'] = parsed_html.body.find('div', attrs={'class':'r-verse-text'}).decode_contents().strip()
            verse['synonyms'] = parsed_html.body.find('div', attrs={'class':'r-synonyms'}).decode_contents().strip()
            verse['translation'] = parsed_html.body.find('div', attrs={'class':'r-translation'}).decode_contents().strip()
            verse['purport'] = parsed_html.body.find('div', attrs={'class':'wrapper-puport'})
            if verse['purport'] is not None:
                verse['purport'] = verse['purport'].decode_contents().strip()
            verses.append(verse)
        
        chapter['verses'] = verses
        with open('/content/drive/MyDrive/Colab Notebooks/sb/sb_canto{}_chapter{}.json'.format(canto_nbr, chapterNbr+1), 'w+') as outfile:
            outfile.seek(0)
            outfile.write(json.dumps(chapter))


if __name__ == "__main__":
    with open('/content/drive/MyDrive/Colab Notebooks/sb/config.json', 'r') as openfile:
        config_json = json.load(openfile)

    for key in config_json['sb']:
        if config_json['sb'][key]['fetch']:
            print("Fetch Canto {} of SB".format(key))
            # code to call fetch function of canto scrapper
            fetchCanto(key, config_json['sb'][key]['excludeChapters'])

    for key in config_json['bg']:
        if config_json['bg'][key]:
            print("Fetch Chapter {} of BG".format(key))
            # code to call fetch function of bg chapter scrapper

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