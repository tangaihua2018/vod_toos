from db.pool import gen_new_m3u8_url


def parse_urls(vod_play_url, index, length, vod_name):
    src_list = vod_play_url.split('$$$')
    vod_source = src_list[index]

    url_list = [item.split('$') for item in vod_source.split("#")]

    new_vod_play_url = gen_new_m3u8_url(url_list, vod_name)
    src_list[index] = new_vod_play_url
    return '$$$'.join(src_list)
