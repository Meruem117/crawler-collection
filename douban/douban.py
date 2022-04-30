import requests
from bs4 import BeautifulSoup
import re
import uuid
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


def get_series_data(douban_id: str):
    """
    获取剧集信息

    :param douban_id: 豆瓣id
    :return:
    """
    url = 'https://movie.douban.com/subject/' + douban_id
    response = requests.get(url=url, headers=constant.HEADERS)
    html = response.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', id='content')
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
        print(e.args)
    finally:
        print(name_cn, name_en, series_cn, series_en)

    # 图片
    image = ''
    try:
        image = content.find('div', id='mainpic').find('img').get('src')
    except Exception as e:
        print(e.args)
    finally:
        print(image)

    # 评分
    score = ''
    try:
        score = content.find('div', id='interest_sectl').find('div', class_='rating_self').find('strong').text
    except Exception as e:
        print('score: ', e.args)
    finally:
        print(score)

    # 类型
    types = ''
    try:
        cate_list = info.find_all('span', property='v:genre')
        cate_text_list = []
        for cate in cate_list:
            cate_text_list.append(cate.text)
        types = '/'.join(cate_text_list)
    except Exception as e:
        print(e.args)
    finally:
        print(types)

    # 首播日期
    date = ''
    try:
        date_text = info.find('span', property='v:initialReleaseDate').text
        date = date_text[0:10]
    except Exception as e:
        print(e.args)
    finally:
        print(date)

    # 国家/地区
    region = ''
    get_region = re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')
    try:
        region = re.search(get_region, str(info)).group(1).strip()
    except Exception as e:
        print(e.args)
    finally:
        print(region)

    # 当季集数
    episodes = ''
    get_episodes = re.compile(r'<span class="pl">集数:</span>(.*?)<br/>')
    try:
        episodes = re.findall(get_episodes, item)[0].strip()
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
        a_soup = BeautifulSoup(a_content, "html.parser")
        imdb_url = a_soup.find_all('a')[0].get('href')
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
        season_soup = BeautifulSoup(season, "html.parser")
        total_season = season_soup.find_all('option')[-1].text
        # print(total_season)
    except Exception as e:
        print('total_season: ', e.args)
    # total_season = '8'

    # 简介
    summary = '暂无'
    try:
        summary_text = soup.find_all('span', property="v:summary")[0].text.strip()
        summary = re.sub('/s', '', summary_text)
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
    # with open('./data/videos.txt', 'a', encoding='UTF-8') as fp:
    #     fp.write('\n')
    #     for vd in video_data:
    #         fp.write(vd + ';')
    #     fp.close()
    # print('data_video inserted')
    # 写入csv
    # with open("./data/video.csv", "a") as csv_file:
    #     writer = csv.writer(csv_file)
    #     # 多行 writerows,单行 writerow
    #     writer.writerow(video_data)

    # 下载图片
    # path = './picture/' + series + ' S' + current_season + '.jpg'
    # r = requests.get(img)
    # with open(path, "wb") as f:
    #     f.write(r.content)
    #     f.close()
    #
    # # 豆瓣链接
    # with open('./data/url_list.txt', 'a', encoding='UTF-8') as fp:
    #     fp.write(url + '\n')
    #     fp.close()
    #
    # if is_latest == '1':
    #     # series数据
    #     uid = str(uuid.uuid4())
    #     sid = ''.join(uid.split('-'))
    #     series_data = [sid, series, region, media, total_season, tm, tm]
    #     with open('./data/series.txt', 'a', encoding='UTF-8') as fp:
    #         fp.write('\n')
    #         for sd in series_data:
    #             fp.write(sd + ';')
    #         fp.close()
    #     # 分割url
    #     with open('./data/url_list.txt', 'a', encoding='UTF-8') as fp:
    #         fp.write('# ' + series_cn + '\n')
    # fp.close()


if __name__ == '__main__':
    # search_common('蝙蝠侠')
    get_series_data('26358318')
    # get_series_data('30450371')
