import requests
from bs4 import BeautifulSoup
import json
import constant


def get_room_info(rid: str) -> object:
    """
    获取虎牙直播间信息

    :param rid: 房间号
    :return:
    """
    url = 'https://www.huya.com/' + rid
    response = requests.get(url=url, headers=constant.HEADERS)
    html = response.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find('div', class_='host-info')

    # 标题
    title = info.find('h1', id='J_roomTitle').text
    # print(title)

    # 主播
    name = info.find('h3', class_='host-name').text
    # print(name)

    # 头像
    avatar = soup.find('div', class_='host-pic').find('img', id='avatar-img').get('src')
    # print(avatar)

    # 订阅
    follower = soup.find('div', id='activityCount').text
    # print(follower)

    # 等级
    # level_class = info.find('div', class_='host-level').find('i').get('class')
    # print(level_class)

    # 分类
    cate_list = info.find('span', class_='host-channel').find_all('a', class_='host-spl clickstat')
    cate_text_list = []
    for cate in cate_list:
        cate_text_list.append(cate.text.strip())
    category = '/'.join(cate_text_list)
    # print(category)

    # 人气值
    heat = info.find('span', class_='host-spectator').find('em').text
    # print(heat)

    data = {
        'rid': rid,
        'title': title,
        'name': name,
        'avatar': avatar,
        'follower': follower,
        'category': category,
        'heat': heat
    }
    json_data = json.dumps(data, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(json_data)
    return data


if __name__ == '__main__':
    get_room_info('433357')
