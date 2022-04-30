import requests
from bs4 import BeautifulSoup
import re
import datetime
import json
import random
import string
import constant


def search_common(key: str, cate: str = '1002') -> None:
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


def get_series_data(douban_id: str) -> object:
    """
    获取剧集信息

    :param douban_id: 豆瓣id
    :return:
    """
    douban_url = 'https://movie.douban.com/subject/' + douban_id + '/'
    response = requests.get(url=douban_url, headers=constant.HEADERS)
    html = response.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find('div', id='content')
    interest = content.find('div', id='interest_sectl')
    info = content.find('div', id='info')

    # 剧集中文名
    name_cn = ''
    # 剧集英文名
    name_en = ''
    # 系列中文名
    series_cn = ''
    # 系列英文名
    series_en = ''
    try:
        title = content.find('h1')
        names = title.find('span', property='v:itemreviewed').text.split()
        if names[-2] == 'Season':
            name_cn = ' '.join(names[0:2])
            name_en = ' '.join(names[2:])
            series_cn = names[0]
            series_en = ' '.join(names[2:-2])
        else:
            name_cn = series_cn = names[0]
            name_en = series_en = ' '.join(names[1:])
    except Exception as e:
        print('name: ', e.args)
    # else:
    #     print(name_cn, name_en, series_cn, series_en)

    # 图片
    image = ''
    try:
        image = content.find('div', id='mainpic').find('img').get('src')
    except Exception as e:
        print('image: ', e.args)
    # else:
    #     print(image)

    # 评分
    score = ''
    try:
        score = interest.find('div', class_='rating_self').find('strong').text
    except Exception as e:
        print('score: ', e.args)
    # else:
    #     print(score)

    # 热度 - 评价人数
    heat = ''
    try:
        heat = interest.find('span', property="v:votes").text
    except Exception as e:
        print('heat: ', e.args)
    # else:
    #     print(heat)

    # 类型
    types = ''
    try:
        cate_list = info.find_all('span', property='v:genre')
        cate_text_list = []
        for cate in cate_list:
            cate_text_list.append(cate.text)
        types = '/'.join(cate_text_list)
    except Exception as e:
        print('types: ', e.args)
    # else:
    #     print(types)

    # 首播日期
    date = ''
    try:
        date_text = info.find('span', property='v:initialReleaseDate').text
        date = date_text[0:10]
    except Exception as e:
        print('date: ', e.args)
    # else:
    #     print(date)

    # 国家/地区
    region = ''
    get_region = re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')
    try:
        region = re.search(get_region, str(info)).group(1).strip()
    except Exception as e:
        print('region: ', e.args)
    # else:
    #     print(region)

    # 语言
    language = ''
    get_language = re.compile(r'<span class="pl">语言:</span>(.*?)<br/>')
    try:
        language = re.search(get_language, str(info)).group(1).strip()
    except Exception as e:
        print('language: ', e.args)
    # else:
    #     print(language)

    # IMDb
    imdb = ''
    get_imdb = re.compile(r'<span class="pl">IMDb:</span>(.*?)<br/>')
    try:
        imdb = re.search(get_imdb, str(info)).group(1).strip()
    except Exception as e:
        print('imdb: ', e.args)
    # else:
    #     print(imdb)

    # 当前季
    current_season = ''
    try:
        select = info.find('select', id='season')
        if select:
            current_season = select.find('option', selected='selected').text
        else:
            current_season = '1'
    except Exception as e:
        print('current_season: ', e.args)
    # else:
    #     print(current_season)

    # 总季数
    total_season = ''
    try:
        select = info.find('select', id='season')
        if select:
            total_season = select.find_all('option')[-1].text
        else:
            total_season = '1'
    except Exception as e:
        print('total_season: ', e.args)
    # else:
    #     print(total_season)

    # 是否最新季
    if current_season == total_season:
        is_latest = '1'
    else:
        is_latest = '0'
    # print(is_latest)

    # 当季集数
    episodes = ''
    get_episodes = re.compile(r'<span class="pl">集数:</span>(.*?)<br/>')
    try:
        episodes = re.search(get_episodes, str(info)).group(1).strip()
    except Exception as e:
        print('episodes: ', e.args)
    # else:
    #     print(episodes)

    # 单集片长
    length = ''
    get_length = re.compile(r'<span class="pl">单集片长:</span>(.*?)<br/>')
    try:
        length = re.search(get_length, str(info)).group(1).strip()
    except Exception as e:
        print('length: ', e.args)
    # else:
    #     print(length)

    # 简介
    summary = ''
    try:
        summary = content.find('div', class_='related-info').find('span', property='v:summary').text.strip()
    except Exception as e:
        print('summary: ', e.args)
    # else:
    #     print(summary)

    # 时间
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(time)

    data = {
        'douban_url': douban_url,
        'douban_id': douban_id,
        'name_cn': name_cn,
        'name_en': name_en,
        'series_cn': series_cn,
        'series_en': series_en,
        'image': image,
        'score': score,
        'heat': heat,
        'types': types,
        'date': date,
        'region': region,
        'language': language,
        'imdb': imdb,
        'current_season': current_season,
        'total_season': total_season,
        'is_latest': is_latest,
        'episodes': episodes,
        'length': length,
        'summary': summary,
        'time': time
    }
    json_data = json.dumps(data, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(json_data)
    return data


def generate_series_id() -> str:
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    sid = 'S' + salt
    return sid


def generate_video_id() -> str:
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    vid = 'SV' + salt
    return vid


if __name__ == '__main__':
    # search_common('蝙蝠侠')
    get_series_data('26358318')
    # get_series_data('30450371')
