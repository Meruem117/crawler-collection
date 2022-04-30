import requests
import pymysql
import json
import time
import constant


def get_ups():
    host = 'localhost'
    user = 'root'
    password = 'abc123'
    port = 3306
    mysql = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = mysql.cursor()

    sql = 'select * from bili.up'
    cursor.execute(sql)
    result = cursor.fetchall()

    result = list(result)
    res = []
    for r in result:
        res.append(r)

    cursor.close()
    mysql.close()
    return res


def get_up_info(mid: str) -> None:
    """
    get up info by mid

    :param mid: up id
    :return: up info
    """

    url = 'https://api.bilibili.com/x/web-interface/card?mid=' + mid
    response = requests.get(url=url, headers=constant.HEADERS)
    dataset = json.loads(response.text)
    # data = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(data)

    # data
    data = dataset.get('data')
    # base info
    card = data.get('card')
    name = card.get('name')
    gender = card.get('sex')
    avatar = card.get('face')
    fans = card.get('fans')
    attention = card.get('attention')
    sign = card.get('sign')
    # official description
    official = card.get('Official')
    title = official.get('title')
    desc = official.get('desc')
    # statistics
    video_num = data.get('archive_count')
    article_num = data.get('article_count')
    follower_num = data.get('follower')
    like_num = data.get('like_num')


def get_videos(mid: str, name: str, pn: int) -> None:
    """
    get videos

    :param mid: up id
    :param name: up name
    :param pn: page number
    :return: video list
    """
    url = 'https://api.bilibili.com/x/space/arc/search?mid=' + mid + '&ps=30&tid=0&pn=' + str(
        pn) + '&keyword=&order=pubdate&jsonp=jsonp'
    response = requests.get(url=url, headers=constant.HEADERS)
    dataset = json.loads(response.text)
    # data = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(data)

    v_data = []
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
                v_data.append([bvid, mid, author, title, pic, play, review, comment, length, description, tm])
            # print(v_data)


if __name__ == '__main__':
    up_id = '12890453'
    get_up_info(up_id)
    # path = './data/ups.csv'

    # with open(path, 'a', encoding="utf-8", newline="") as csv_file:
    #     writer = csv.writer(csv_file)
    #     # first create needed
    #     # writer.writerow(['mid', 'name', 'face', 'gender', 'fans', 'sign', 'title'])
    #     writer.writerows(u_data)
    # print('finished')
