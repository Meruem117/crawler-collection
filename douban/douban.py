import requests
from bs4 import BeautifulSoup
from urllib import parse
import time
import constant


def search_key(kw):
    search_url = 'https://www.douban.com/search'
    param = {
        'q': kw
    }
    response = requests.get(url=search_url, params=param, headers=constant.HEADERS)
    html = response.text.encode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for item in soup.find_all('div', class_="title"):
        bs = BeautifulSoup(str(item), 'html.parser')
        if bs.find_all('span') and bs.find_all('span')[0].text == '[电影]':
            a = bs.find_all('a', target="_blank")[0]
            name = a.text
            if kw.split()[0] == name.split()[0]:
                h = a.get('href')
                href = h.split('&')[0].split('=')[1]
                video_url = parse.unquote(href)
                urls.append(video_url)
    print(urls)
