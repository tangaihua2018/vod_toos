import pymysql

# 数据库连接配置
from db.m3u8_mod import mod_one
from util.util import isolate_source

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'tv2',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def main():
    # 创建数据库连接
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 分批查询数据
            offset = 0
            while True:
                sql = "SELECT vod_id, vod_name, vod_play_url, " \
                      "vod_play_from FROM mac_vod LIMIT %s, 1"
                cursor.execute(sql, (offset,))
                results = cursor.fetchall()
                if not results:
                    break

                for result in results:
                    vod_play_url = result['vod_play_url']
                    vod_play_from = result['vod_play_from']
                    vod_name = result['vod_name']

                    have, index, length = isolate_source(vod_play_from)
                    if not have:
                        continue

                    # 处理单个记录
                    mod_one(vod_play_url, index, length, vod_name, cursor, connection, result['vod_id'])

                offset += 20
    finally:
        connection.close()


if __name__ == '__main__':
    main()
