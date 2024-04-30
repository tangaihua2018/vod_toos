from db.pool import gen_new_m3u8_url


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
        elif len(parts) == 1:
            url_list.append(block)

    new_vod_play_url = gen_new_m3u8_url(url_list, vod_name)
    if length > 1:
        src_list[index] = new_vod_play_url
        return '$$$'.join(src_list)

    return new_vod_play_url
