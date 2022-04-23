import requests
from bs4 import BeautifulSoup
from urllib import parse
import re
import urllib.request
import urllib.error
import uuid
import datetime


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
                print(name, video_url)


def get_data(url):
    # 定义代理池
    proxy_list = [
        '182.39.6.245:38634',
        '115.210.181.31:34301',
        '123.161.152.38:23201',
        '222.85.5.187:26675',
        '123.161.152.31:23127',
    ]
    proxy = random.choice(proxy_list)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(handler)

    user_agents = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': user_agent
    }
    request = urllib.request.Request(url, headers=headers)
    html = ""
    # 获取网页源码
    try:
        response = opener.open(request)
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
    video_data = [vid, name_cn, name_en, img, series, types, score, date, current_season, episodes, length, is_latest, heat, url, imdb_url, summary, is_end, tm, tm]

    # video数据
    with open('./data/videos.txt', 'a', encoding='UTF-8') as fp:
        fp.write('\n')
        for vd in video_data:
            fp.write(vd + ';')
        fp.close()
    print('data_video inserted')

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
        print('data_series inserted')


if __name__ == '__main__':
    target_urls = []
    key = input('输入要搜索的剧名: ')   # 匹配采用的是全匹配所以输入完整剧名为最佳
    get_url(key)
    for url in target_urls:
        print(url)
        try:
            get_data(url)
        except Exception as e:
            print(e.args)