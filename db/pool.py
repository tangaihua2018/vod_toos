import datetime
import os
import concurrent.futures
import m3u8
import requests

from util.http import http_get
from util.log import log
from util.util import debug_log


def gen_new_m3u8_url(url_list, vod_name):
    # 使用线程池处理数据
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交任务到线程池
        futures = [executor.submit(download_and_modify_m3u8, i, url_list, vod_name) for i in range(len(url_list))]

        # 等待所有线程完成
        concurrent.futures.wait(futures)

    return '#'.join([f'{url[0]}${url[1]}' for url in url_list])


def mod_m3u8(url_list, vod_name):
    new_vod_play_url = ""
    # 现在，url_list包含了所有集的（集数, URL）元组
    for episode, url in url_list:

        # EXTINF:2,
        # 获取当前日期
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        debug_log(f"{current_time}: 正在处理{vod_name}-{episode}")
        try:
            url = download_and_modify_m3u8(url)
            tmp = ''
            if len(new_vod_play_url) > 0:
                tmp = '#'
            new_vod_play_url = f'{new_vod_play_url}{tmp}{episode}${url}'

        except requests.RequestException as e:
            debug_log(f"Error fetching {url}: {e}")


def download_and_modify_m3u8(index, url_list, vod_name):
    episode = url_list[index][0]
    debug_log(f'正在处理[{vod_name}]:[{episode}]')

    url = url_list[index][1]
    # 发送请求获取M3U8内容
    try:
        m3u8text = http_get(url)
        debug_log(f'{vod_name}-{episode}通了')
        m3u8_obj = m3u8.loads(m3u8text)  # 从字符串加载M3U8数据
    except Exception as e:
        debug_log(f'http error: {e}')
        return

    # 修改每个segment的URI
    for segment in m3u8_obj.segments:
        segment.uri = segment.uri.replace('cdnb.v82u1l.com', 'hv.118318.xyz')
        segment.uri = segment.uri.replace('cdn.v82u1l.com', 'h.118318.xyz')
        segment.uri = segment.uri.replace('cdn.kin6c1.com', 'v3.118318.xyz')
        segment.uri = segment.uri.replace('cdn.iz8qkg.com', 'v4.118318.xyz')
        segment.uri = segment.uri.replace('cdnb.kin6c1.com', 'v5.118318.xyz')
        segment.uri = segment.uri.replace('cdnb.iz8qkg.com', 'v6.118318.xyz')
        segment.discontinuity = False

    # 构造新的文件名和URL
    m3u8_filename = f"m3u8/{url.split('/')[-1]}"
    new_url = f'http://v.118318.xyz/{m3u8_filename}'

    safe_write_file(m3u8_filename, m3u8_obj.dumps())

    url_list[index][1] = new_url


def safe_write_file(path, content):
    # 确保目录存在
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # 写入文件
    with open(path, 'w') as file:
        file.write(content)
