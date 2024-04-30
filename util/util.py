import datetime
import secrets
import string


def get_curr_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_curr_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 分割不同的源
def isolate_source(vod_play_from):
    v_from = vod_play_from.split('$$$')

    have = False
    index = 0
    length = len(v_from)
    for i in range(0, length):
        if v_from[i] == 'haiwaikan':
            have = True
            index = i
            break
    return have, index, length


# 生成安全随机字符串的函数
def generate_random_string(length):
    # 字符集包括大小写字母和数字
    alphabet = string.ascii_letters + string.digits
    # 从字符集中随机选择字符，生成指定长度的字符串
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string
