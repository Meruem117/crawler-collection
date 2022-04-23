import requests
import json
import csv
import time

import requests
import json
import csv
import time


def get_up_info(mid: str):
    url = 'https://api.bilibili.com/x/web-interface/card?mid=' + mid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3237.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    dataset = json.loads(response.text)
    # data = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(data)

    card = dataset.get('data').get('card')
    mid = card.get('mid')
    name = card.get('name')
    face = card.get('face')
    gender = card.get('sex')
    fans = card.get('fans')
    sign = card.get('sign')
    title = card.get('official_verify').get('desc')
    u_data.append([mid, name, face, gender, fans, sign, title])
    # print(u_data)


if __name__ == '__main__':
    # params: mid
    # 'https://api.bilibili.com/x/web-interface/card?mid=?'
    u_data = []
    up_id = ''
    get_up_info(up_id)
    path = './data/ups.csv'

    with open(path, 'a', encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # first create needed
        # writer.writerow(['mid', 'name', 'face', 'gender', 'fans', 'sign', 'title'])
        writer.writerows(u_data)
    print('finished')
