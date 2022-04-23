import pymysql
import requests
import json
import csv
import time


def get_ups():
    host = 'localhost'
    user = 'root'
    password = 'abc123'
    port = 3306
    mysql = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = mysql.cursor()

    sql = 'select * from p3.up'
    cursor.execute(sql)
    result = cursor.fetchall()

    result = list(result)
    res = []
    for r in result:
        res.append(r)

    cursor.close()
    mysql.close()
    return res


def get_up_info(mid: str, res: list):
    url = 'https://api.bilibili.com/x/web-interface/card?mid=' + mid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3237.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    dataset = json.loads(response.text)

    card = dataset.get('data').get('card')
    archive_count = dataset.get('data').get('archive_count')
    mid = card.get('mid')
    name = card.get('name')
    face = card.get('face')
    gender = card.get('sex')
    fans = card.get('fans')
    sign = card.get('sign')
    title = card.get('official_verify').get('desc')

    res.append([mid, name, face, gender, fans, sign, title, archive_count])


def get_single_page(mid: str, name: str, pn: int, res: list):
    url = 'https://api.bilibili.com/x/space/arc/search?mid=' + mid + '&ps=30&tid=0&pn=' + str(
        pn) + '&keyword=&order=pubdate&jsonp=jsonp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3237.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    dataset = json.loads(response.text)

    v_list = dataset.get('data').get('list').get('vlist')
    if len(v_list) != 0:
        for v in v_list:
            bvid = v.get('bvid')
            author = v.get('author')
            title = v.get('title')
            pic = v.get('pic')
            play = v.get('play')
            review = v.get('video_review')
            comment = v.get('comment')
            length = v.get('length')
            description = v.get('description')
            created = v.get('created')
            tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created))

            if author == name:
                res.append([bvid, mid, author, title, pic, play, review, comment, length, description, tm])


if __name__ == '__main__':
    ups = get_ups()

    ups_info = []
    for up in ups:
        get_up_info(up[1], ups_info)
    for info in ups_info:
        count = info[-1]
        total_page = count // 30 if count % 30 == 0 else count // 30 + 1
        info.append(total_page)

    videos = []
    for item in ups_info:
        for pn in range(1, item[-1] + 1):
            get_single_page(item[0], item[1], pn, videos)
            print('finish ' + item[1] + '_page' + str(pn))

    with open('./data/ups_tmp', 'w', encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['mid', 'name', 'face', 'gender', 'fans', 'sign', 'title', 'archive_count', 'total_page'])
        writer.writerows(ups_info)
        csv_file.close()
        print('ups inserted')

    with open('./data/videos_tmp', 'w', encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['bvid', 'mid', 'author', 'title', 'pic', 'play', 'review', 'comment', 'length', 'description', 'tm'])
        writer.writerows(videos)
        csv_file.close()
        print('videos inserted')

    print('finished')
