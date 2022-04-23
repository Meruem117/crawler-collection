import requests
from bs4 import BeautifulSoup
from urllib import parse


def get_url(kw):
    search_url = 'https://www.douban.com/search'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'
    }
    param = {
        'q': kw
    }
    response = requests.get(url=search_url, params=param, headers=header)
    html = response.text.encode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('div', class_="title"):
        sp = BeautifulSoup(str(item), 'html.parser')
        if sp.find_all('span') and sp.find_all('span')[0].text == '[电影]':
            a = sp.find_all('a', target="_blank")[0]
            name = a.text
            if kw.split()[0] == name.split()[0]:
                h = a.get('href')
                href = h.split('&')[0].split('=')[1]
                video_url = parse.unquote(href)
                target_urls.append(video_url)
                print(video_url)

# 后来才发现在电影板块下搜素剧名会有更符合需求的搜索结果，但是下面这个方法并没有成功...
# 有大佬能看看哪不对吗~
def get_url_movie(st):
    search_url = 'https://search.douban.com/movie/subject_search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'
    }
    params = {
        'search_text': st
    }
    response = requests.get(url=search_url, params=params, headers=headers)
    html = response.text.encode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('div', class_="title"):
        sp = BeautifulSoup(str(item), 'html.parser')
        if sp.find_all('span') and sp.find_all('span')[0].text == '[剧集]':
            a = sp.find_all('a')[0]
            name = a.text
            if st.split()[0] == name.split()[0]:
                h = a.get('href')
                target_urls.append(h)
                print(h)


if __name__ == '__main__':
    target_urls = []
    key = input('输入要搜索的剧名: ')
    get_url(key)
    # 记录
    for url in target_urls:
        with open('urls.txt', 'a', encoding='UTF-8') as fp:
            fp.write(url + '\n')
            fp.close()
    print('finished')