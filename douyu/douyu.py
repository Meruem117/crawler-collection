import requests
from bs4 import BeautifulSoup
import json
import constant


def get_room_info(rid: str) -> object:
    """
    获取斗鱼直播间信息

    :param rid: 房间号
    :return:
    """
    url = 'https://www.douyu.com/' + rid
    response = requests.get(url=url, headers=constant.HEADERS)
    html = response.text.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_='layout-Player').find('div', class_='layout-Player-main')
    head = content.find('div', class_='layout-Player-title')

    # 直播间标题
    title = head.find('h3', class_='Title-header').text
    # print(title)

    # 分类
    cate_list = head.find('div', class_='Title-category').find_all('a', class_='Title-categoryItem')
    cate_text_list = []
    for cate in cate_list:
        if cate.text != '':
            cate_text_list.append(cate.text)
    category = '/'.join(cate_text_list)
    # print(category)

    # 主播
    name = head.find('h2', class_='Title-anchorNameH2').text
    # print(name)

    # 关注数
    # follower = head.find('span', class_='Title-followNum').text
    # print(follower)

    # 等级
    level_class = head.find('div', class_='Title-AnchorLevel').find('div', class_='AnchorLevel').get('class')
    level = level_class[-1].split('-')[-1]
    # print(level)

    # 头像
    avatar = head.find('div', class_='Title-anchorPic').find('img').get('src')
    # print(avatar)

    # 热度
    heat = head.find('a', class_='Title-anchorHot').find('div', class_='Title-anchorText').text
    # print(heat)

    # 工会
    society = head.find('div', class_='SociatyLabel').get('title').split('：')[-1]
    # print(society)

    data = {
        'rid': rid,
        'title': title,
        'category': category,
        'name': name,
        'level': level,
        'avatar': avatar,
        'heat': heat,
        'society': society
    }
    json_data = json.dumps(data, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(json_data)
    return data


if __name__ == '__main__':
    get_room_info('71415')
