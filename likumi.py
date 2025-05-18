from pyquery import PyQuery as pq
import json
import requests
import re

BASE_ELEMENT = 'div.doc-body div'

def GetHtmlContent(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            response.encoding = 'utf-8'
            
            return response.text
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

classTypes = {
    'TV207':'Title',
    'TV213':'Article'
}

def IsNotActive(text):
    pattern = r'\(?(I|i)zslēgt(a|s).*?\d{2}\.\d{2}\.\d{4}\..*?likumu\)?'
    return re.search(pattern, text)

def GetLawContent(law):
    html_content = GetHtmlContent(law['url'])
    lawContent = pq(html_content)(BASE_ELEMENT)
    title = law['nosaukums']
    articles = []
    for paragraph in lawContent.items():
        if paragraph.attr('class') != None:
            divType = paragraph.attr('class')[:5]
            if divType == 'TV213':
                prefix = paragraph.attr('data-pfx')
                if prefix == 'p':
                    articleNr = paragraph.attr('data-num')
                    if articleNr == None:
                        articleNr = paragraph('p.TV213.TVP').attr('id')[1:]
                    points = []
                    correction = paragraph('p.labojumu_pamats')
                    if IsNotActive(correction.text()): continue
                    texts = paragraph('p.TV213')
                    for text in texts.items():
                        if IsNotActive(text.text()): continue
                        points.append(text.text())
                    temp = {
                        'Number': articleNr.replace('_','.'),
                        'Point': '\n'.join(points)
                    }
                    if temp['Point'] == "": continue
                    articles.append(temp)
    return {
        'LawSource':law['url'],
        'LawTitle': title,
        'LawId': law['number'],
        'Articles':articles
    }


### Uses LikumuSaraksts.json to get all laws and stored them all in separate JSON files.
with open('LikumuSaraksts.json', 'r', encoding='utf-8') as f:
    laws = json.load(f)

for law in laws:
    law = GetLawContent(law)
    with open(f'Laws/{law['LawTitle'].replace('"',"'").split("\n", 1)[0]}.json', 'w', encoding='utf-8') as f:
        json.dump(law, f, ensure_ascii=False, indent=4)

### Combines all law files in one single file.
import os
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('Laws') if isfile(join('Laws', f))]

combined = []
for file in onlyfiles:
    with open('Laws/'+file, 'r', encoding='utf-8') as f:
        laws = json.load(f)
    combined.append(laws)

with open(f'CombinedLaws.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=4)