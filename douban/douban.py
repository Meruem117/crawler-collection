import requests
from bs4 import BeautifulSoup
from urllib import parse
import time
import constant


def search_common(key):
    search_url = 'https://www.douban.com/search'
    param = {
        'q': key
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
            if key.split()[0] == name.split()[0]:
                h = a.get('href')
                href = h.split('&')[0].split('=')[1]
                video_url = parse.unquote(href)
                urls.append(video_url)
    print(urls)


def search_movie(key):
    url = 'https://search.douban.com/movie/subject_search'
    params = {
        'search_text': key
    }
    response = requests.get(url=url, params=params, headers=constant.HEADERS)
    html = response.text.encode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for item in soup.find_all('div', class_="title"):
        sp = BeautifulSoup(str(item), 'html.parser')
        if sp.find_all('span') and sp.find_all('span')[0].text == '[剧集]':
            a = sp.find_all('a')[0]
            name = a.text
            if key.split()[0] == name.split()[0]:
                h = a.get('href')
                urls.append(h)
    print(urls)


if __name__ == '__main__':
    search_common("hhh")
