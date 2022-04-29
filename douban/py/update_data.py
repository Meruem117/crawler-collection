import csv
import datetime
import re
import time
import urllib.error
import urllib.request
import requests
from bs4 import BeautifulSoup
import random
import string


def generate_video_id():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    code = 'SV' + salt
    return code


def generate_series_id():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    code = 'S' + salt
    return code


def write_video_data(path, dataset):
    # 用于数据库更新video
    with open(path, 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(
            [['id', 'video_id', 'name_cn', 'name_en', 'video_img', 'series', 'type', 'score', 'date', 'current_season',
              'total_episode', 'length', 'is_latest', 'heat', 'douban_url', 'imdb_url', 'summary', 'status',
              'create_time', 'last_modified'], dataset])
    print('data_video inserted')


def write_series_data(path, dataset):
    # 用于数据库更新series
    with open(path, 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(
            [['id', 'series_id', 'series_name', 'region', 'media', 'total_season', 'create_time', 'last_modified'],
             dataset])
    print('data_series inserted')


if __name__ == '__main__':
    data_video = []
    data_series = []
    # 单个url
    get_data('https://movie.douban.com/subject/35027568/')
    # 多个url
    # for line in open("url.txt", encoding='utf-8'):
    #     get_data(line.split()[0])
    #     print('finished')
    #     time.sleep(2)
    if len(data_video) > 0:
        write_video_data('./data/update_video.csv', data_video)
    if len(data_series) > 0:
        write_series_data('./data/update_series.csv', data_series)
