import requests
import json
import constant


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
    name: str = card.get('name')
    gender: str = card.get('sex')
    avatar: str = card.get('face')
    fans: int = card.get('fans')
    attention: int = card.get('attention')
    sign: str = card.get('sign')
    # official description
    official = card.get('Official')
    title: str = official.get('title')
    desc: str = official.get('desc')
    # statistics
    video_num: int = data.get('archive_count')
    article_num: int = data.get('article_count')
    follower_num: int = data.get('follower')
    like_num: int = data.get('like_num')


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
