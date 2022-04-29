import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import uuid
import time
import datetime
import constant


def search_common(key: str, cate: str = '1002'):
    """
    基础搜索

    :param key: 关键词
    :param cate: 类别, 默认 1002 电影/剧集
    :return:
    """
    search_url = 'https://www.douban.com/search'
    param = {
        'cat': cate,
        'q': key
    }
    response = requests.get(url=search_url, params=param, headers=constant.HEADERS)
    html = response.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    result_list = soup.find('div', class_='result-list')
    for result in result_list.find_all('div', class_='result'):
        title = result.find('span').text + ' ' + result.find_all('a')[1].text
        link = result.find_all('a')[1].get('href')
        desc = result.find('p').text
        print(title + '\n' + link + '\n' + desc)


def search_movie(key):
    url = 'https://search.douban.com/movie/subject_search'
    params = {
        'search_text': key
    }
    response = requests.get(url=url, params=params, headers=constant.HEADERS)
    html = response.text.encode('utf-8')
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


def get_data(url):
    request = urllib.request.Request(url, headers=constant.HEADERS)
    html = ""
    # 获取网页源码
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    item = str(soup.find_all('div', id='content'))  # 只有一个

    # 获取剧名
    series = name_cn = name_en = ''
    try:
        name = soup.find_all('span', property="v:itemreviewed")[0].text.split()
        s = ' '
        if name[-2] == 'Season':
            series = s.join(name[2:-2])
            series_cn = name[0]
            name_cn = s.join(name[0:2])
            name_en = series + ' ' + s.join(name[-2:])
        else:
            series_cn = name_cn = name[0]
            series = name_en = s.join(name[1:])
    except Exception as e:
        print('name: ', e.args)

    # 图片
    img = ''
    try:
        img = soup.find_all('img', title="点击看更多海报")[0].get('src')
        # print(img)
    except Exception as e:
        print('img: ', e.args)

    # 评分
    score = ''
    try:
        score = soup.find_all('strong', property="v:average")[0].text
        # print(score)
    except Exception as e:
        print('score: ', e.args)

    # 类型
    types = ''
    try:
        t = soup.find_all('span', property="v:genre")
        types = t[0].text
        for tt in range(1, len(t)):
            types += ' / ' + t[tt].text
        # print(types)
    except Exception as e:
        print('types: ', e.args)

    # 首播日期
    date = ''
    try:
        d = soup.find_all('span', property="v:initialReleaseDate")[0].text
        date = re.sub(u"\\(.*?\\)", "", d)
        # print(date)
    except Exception as e:
        print('date: ', e.args)

    # 国家/地区
    region = '暂无'
    get_region = re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')
    try:
        region = re.findall(get_region, item)[0].strip()
        # print(region)
    except Exception as e:
        print('region: ', e.args)

    # 当季集数
    episodes = ''
    get_episode = re.compile(r'<span class="pl">集数:</span>(.*?)<br/>')
    try:
        episodes = re.findall(get_episode, item)[0].strip()
        # print(episodes)
    except Exception as e:
        print('episodes: ', e.args)

    # 单集片长
    length = ''
    get_length = re.compile(r'<span class="pl">单集片长:</span>(.*?)<br/>')
    try:
        length = re.findall(get_length, item)[0].strip()
        # print(length)
    except Exception as e:
        print('length: ', e.args)

    # IMDb链接
    imdb_url = ''
    get_url = re.compile(r'<span class="pl">IMDb链接:</span>(.*?)<br/>')
    try:
        a_content = re.findall(get_url, item)[0].strip()
        asp = BeautifulSoup(a_content, "html.parser")
        imdb_url = asp.find_all('a')[0].get('href')
        # print(imdb_url)
    except Exception as e:
        print('imdb_url: ', e.args)

    # 当前季
    current_season = '1'
    try:
        current_season = soup.find_all('option', selected=True)[0].text
        # print(current_season)
    except Exception as e:
        print('current_season: ', e.args)

    # 总季数
    total_season = '1'
    try:
        season = str(soup.find_all('select', id="season"))
        ts = BeautifulSoup(season, "html.parser")
        total_season = ts.find_all('option')[-1].text
        # print(total_season)
    except Exception as e:
        print('total_season: ', e.args)
    # total_season = '8'

    # 简介
    summary = '暂无'
    try:
        summary = soup.find_all('span', property="v:summary")[0].text.strip()
        summary = re.sub('\s', '', summary)
        # print(summary)
    except Exception as e:
        print('summary: ', e.args)

    # 热度
    heat = '0'
    try:
        heat = soup.find_all('span', property="v:votes")[0].text
        # print(heat)
    except Exception as e:
        print('heat: ', e.args)

    # id
    uid = str(uuid.uuid4())
    vid = ''.join(uid.split('-'))
    # print(vid)

    # 时间
    tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(tm)

    # 暂时没有的数据
    # 媒体
    media = ''
    # 是否完结(完结/连载)
    is_end = '1'

    # 是否最新季
    if current_season == total_season:
        is_latest = '1'
    else:
        is_latest = '0'
    # print(is_latest)

    # video数据
    video_data = [vid, name_cn, name_en, img, series, types, score, date, current_season, episodes, length,
                  is_latest, heat, url, imdb_url, summary, is_end, tm, tm]

    # video数据
    with open('./data/videos.txt', 'a', encoding='UTF-8') as fp:
        fp.write('\n')
        for vd in video_data:
            fp.write(vd + ';')
        fp.close()
    print('data_video inserted')
    # 写入csv
    with open("./data/video.csv", "a") as csv_file:
        writer = csv.writer(csv_file)
        # 多行 writerows,单行 writerow
        writer.writerow(video_data)

    # 下载图片
    path = './picture/' + series + ' S' + current_season + '.jpg'
    r = requests.get(img)
    with open(path, "wb") as f:
        f.write(r.content)
        f.close()

    # 豆瓣链接
    with open('./data/url_list.txt', 'a', encoding='UTF-8') as fp:
        fp.write(url + '\n')
        fp.close()

    if is_latest == '1':
        # series数据
        uid = str(uuid.uuid4())
        sid = ''.join(uid.split('-'))
        series_data = [sid, series, region, media, total_season, tm, tm]
        with open('./data/series.txt', 'a', encoding='UTF-8') as fp:
            fp.write('\n')
            for sd in series_data:
                fp.write(sd + ';')
            fp.close()
        # 分割url
        with open('./data/url_list.txt', 'a', encoding='UTF-8') as fp:
            fp.write('# ' + series_cn + '\n')
    fp.close()


if __name__ == '__main__':
    search_common('蝙蝠侠')
