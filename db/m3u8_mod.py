import requests

from db.parseUrls import parse_urls
from util.util import debug_log


def mod_one(vod_play_url, index, length, vod_name, cursor, connection, vod_id):
    # 修改链接，以及保存m3u8文件在本地
    new_vod_play_url = parse_urls(vod_play_url, index, length, vod_name)

    try:
        # 更新数据库中的链接，包括日期
        update_sql = "UPDATE mac_vod SET vod_play_url = %s " \
                     "WHERE vod_id = %s"
        cursor.execute(update_sql, (new_vod_play_url, vod_id))
        connection.commit()

    except requests.RequestException as e:
        debug_log(f"Error fetching {vod_play_url}: {e}")
