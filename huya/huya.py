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
    print(title)

    # data = {
    #     'rid': rid,
    #     'title': title,
    #     'category': category,
    #     'name': name,
    #     'level': level,
    #     'avatar': avatar,
    #     'heat': heat,
    #     'society': society
    # }
    # json_data = json.dumps(data, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(json_data)
    # return data


if __name__ == '__main__':
    get_room_info('433357')
