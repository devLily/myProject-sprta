import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

gtrs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for trs in gtrs:
    rank = trs.select_one('td.number').text[0:2].strip()
    # print(len(rank))
    title = trs.select_one('a.title').text.strip()
    artist = trs.select_one('a.artist').text
    print(rank, title, artist)
    doc = {
        'rank': rank,
        'title': title,
        'artist': artist
    }
    db.ginielist.insert_one(doc)
