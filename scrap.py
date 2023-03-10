from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup
import csv
import sys
from sys import argv

if len(argv) != 3:
    sys.exit("Usage: python srap.py \"[page url]\" \"[output filename]\"")


URL = argv[1]
r = requests.get(URL)

es = Elasticsearch("http://localhost:9200")
mapping = {
    "question": {
        "title": {"type": "text", "analyzer": "english"},
        "description": {"type": "text", "analyzer": "english"},
        "tags": {"type": "text", "analyzer": "english"},
        "user": {"type": "keyword", "analyzer": "english"}
    }
}

es.indices.create(index="questions", mappings=mappings)

soup = BeautifulSoup(r.content, 'html.parser')

questions = []

list_of_questions = soup.find('div', id="questions")

for row in list_of_questions.find_all('div', attrs={'class':'s-post-summary js-post-summary'}):
    question = {}
    question['title'] = row.find('div', attrs = {'class', 's-post-summary--content'}).h3.text.strip().replace('\r', ' ').replace('\n', ' ')
    question['description'] = row.find('div', attrs = {'class', 's-post-summary--content'}).find('div', attrs={'class': 's-post-summary--content-excerpt'}).text.strip().replace('\r', ' ').replace('\n', ' ')
    tags_div = row.find('div', attrs = {'class', 's-post-summary--content'}).find('div', attrs={'class': 's-post-summary--meta'}).find('div', attrs={'class': 's-post-summary--meta-tags'}).find("ul")
    list_of_tags = []
    for l in tags_div.find_all("li"):
        list_of_tags.append(l.a.text)
    question['tags'] = list_of_tags
    question['user'] = row.find('div', attrs = {'class', 's-post-summary--content'}).find('div', attrs={'class': 's-post-summary--meta'}).find('div', attrs={"class":"s-user-card"}).find('div', attrs={"class":"s-user-card--info"}).find('div', attrs={"class":"s-user-card--link"}).a.text
    questions.append(question)

filename = argv[2]+'.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['title', 'description', 'tags', 'user'])
    w.writeheader()
    for i, q in questions:
        w.writerow(q)
        doc = {
                "title": q["title"],
                "description": q["description"],
                "tags": q['tags'],
                "user": q["user"]
                }
        es.index(index="questions", id=i, document=doc)
print('done')
