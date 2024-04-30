import datetime
import os
import m3u8
import requests


def parse_urls(vod_play_url, index, length, vod_name):
    src_list = vod_play_url.split('$$$')
    tmp = ''
    if length > 1:
        tmp = src_list[index]

    # 将数据分割成单独的集数和URL
    episode_blocks = tmp.split('#')
    url_list = []

    # 遍历每个块，进一步分解并提取URL
    for block in episode_blocks:
        parts = block.split('$')
        if len(parts) == 2:
            episode = parts[0]
            url = parts[1]
            url_list.append((episode, url))

    new_vod_play_url = ""
    # 现在，url_list包含了所有集的（集数, URL）元组
    for episode, url in url_list:

        # EXTINF:2,
        # 获取当前日期
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{current_time}: 正在处理{vod_name}-{episode}")
        try:
            url = download_and_modify_m3u8(url)
            tmp = ''
            if len(new_vod_play_url) > 0:
                tmp = '#'
            new_vod_play_url = f'{new_vod_play_url}{tmp}{episode}${url}'

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    if length > 1:
        src_list[index] = new_vod_play_url
        return '$$$'.join(src_list)

    return new_vod_play_url


def download_and_modify_m3u8(url):
    # 发送请求获取M3U8内容
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download M3U8 file from {url}")
        return

    m3u8_content = response.text
    m3u8_obj = m3u8.loads(m3u8_content)  # 从字符串加载M3U8数据

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

    return new_url


def safe_write_file(path, content):
    # 确保目录存在
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # 写入文件
    with open(path, 'w') as file:
        file.write(content)
