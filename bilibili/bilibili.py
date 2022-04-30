import requests
import time
import json
import constant


def get_up_info(mid: str) -> object:
    """
    获取up主信息

    :param mid: up主id
    :return:
    """

    url = 'https://api.bilibili.com/x/web-interface/card?mid=' + mid
    response = requests.get(url=url, headers=constant.HEADERS)
    dataset = json.loads(response.text)
    # data = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(data)

    data = dataset.get('data')
    card = data.get('card')
    official = card.get('Official')

    # 昵称
    name = card.get('name')
    # 性别
    gender = card.get('sex')
    # 头像
    avatar = card.get('face')
    # 粉丝数
    fans = card.get('fans')
    # 关注数
    attention = card.get('attention')
    # 签名
    sign = card.get('sign')
    # 官方认证
    title = official.get('title')
    # 认证描述
    desc = official.get('desc')
    # 视频数
    video_num = data.get('archive_count')
    # 文章数
    article_num = data.get('article_count')
    # 粉丝数
    follower_num = data.get('follower')
    # 点赞数
    like_num = data.get('like_num')

    info = {
        'name': name,
        'gender': gender,
        'avatar': avatar,
        'fans': fans,
        'attention': attention,
        'sign': sign,
        'title': title,
        'desc': desc,
        'video_num': video_num,
        'article_num': article_num,
        'follower_num': follower_num,
        'like_num': like_num,
    }
    json_data = json.dumps(info, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(json_data)
    return info


def get_videos(mid: str, name: str, page: int) -> list:
    """
    获取分页视频列表

    :param mid: up主id
    :param name: up名
    :param page: 页号
    :return:
    """
    url = 'https://api.bilibili.com/x/space/arc/search?mid=' + mid + '&ps=30&tid=0&pn=' + str(
        page) + '&keyword=&order=pubdate&jsonp=jsonp'
    response = requests.get(url=url, headers=constant.HEADERS)
    dataset = json.loads(response.text)
    # data = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(data)

    video_list = []
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
                video_list.append([bvid, mid, author, title, pic, play, review, comment, length, description, tm])
    return video_list


if __name__ == '__main__':
    up_id = '546195'
    get_up_info(up_id)
