import random
import string


def generate_video_id(rk):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    code = 'SV' + salt
    video_ids.append([str(rk), code])


def generate_series_id(rk):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    code = 'S' + salt
    series_ids.append([str(rk), code])


def write_series_id():
    with open('./data/series_id.txt', 'a', encoding='UTF-8') as fp:
        for i in range(len(series_ids)):
            fp.write('\n')
            fp.write(series_ids[i][0] + ';' + series_ids[i][1])
    fp.close()
    print('series_id finished')


def write_video_id():
    with open('./data/video_id.txt', 'a', encoding='UTF-8') as fp:
        for i in range(len(video_ids)):
            fp.write('\n')
            fp.write(video_ids[i][0] + ';' + video_ids[i][1])
    fp.close()
    print('video_id finished')


if __name__ == '__main__':
    series_length = 210
    video_length = 605
    series_ids = []
    video_ids = []
    for i in range(1, series_length + 1):
        generate_series_id(i)
    write_series_id()
    for i in range(1, video_length + 1):
        generate_video_id(i)
    write_video_id()