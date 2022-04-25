import requests
from bs4 import BeautifulSoup





if __name__ == '__main__':
    target_urls = []
    key = input('输入要搜索的剧名: ')
    get_url(key)
    # 记录
    for url in target_urls:
        with open('urls.txt', 'a', encoding='UTF-8') as fp:
            fp.write(url + '\n')
            fp.close()
    print('finished')
