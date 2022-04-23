import requests
import json
import csv
import time


def get_single_page(mid: str, pn: int):
    url = 'https://api.bilibili.com/x/space/arc/search?mid=' + mid + '&ps=30&tid=0&pn=' + str(
        pn) + '&keyword=&order=pubdate&jsonp=jsonp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3237.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    dataset = json.loads(response.text)
    # data = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    # print(data)

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
            if author == up_name:
                v_data.append([bvid, mid, author, title, pic, play, review, comment, length, description, tm])
            # print(v_data)


if __name__ == '__main__':
    # params: mid, pn
    # 'https://api.bilibili.com/x/space/arc/search?mid=?&ps=30&tid=0&pn=?&keyword=&order=pubdate&jsonp=jsonp'
    v_data = []
    up_id = ''
    up_name = ''
    total_page = 0
    path = './data/' + up_name + '.csv'

    for i in range(1, total_page + 1):
        get_single_page(up_id, i)
        print('page_', i, ' inserted')

    with open(path, 'w', encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['bvid', 'mid', 'author', 'title', 'pic', 'play', 'review', 'comment', 'length', 'description', 'tm'])
        writer.writerows(v_data)
    print('finished')
