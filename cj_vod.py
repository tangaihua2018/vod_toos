import json
import time
import requests

from datetime import datetime
from marshmallow import EXCLUDE, fields, pre_load, ValidationError

from db.parseUrls import parse_urls
from model.MacVod import MacVod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.log import log

db_user = 'root'
db_password = '123456'
db_name = 'apple'
db_address = 'localhost'
sign_file = 'start'

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_address}/{db_name}?charset=utf8')
Session = sessionmaker(bind=engine)
session = Session()

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class MacVodSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MacVod
        sqla_session = session  # 使用 SQLAlchemy session
        load_instance = True  # Optional: for deserialization
        unknown = EXCLUDE  # 自动排除所有不在 schema 中定义的字段

    vod_time = fields.Integer()  # 保持字段为整数

    @pre_load
    def convert_vod_time_to_timestamp(self, in_data, **kwargs):
        vod_time_str = in_data.get('vod_time', None)
        if vod_time_str:
            try:
                # 解析日期时间字符串到 datetime 对象
                dt = datetime.strptime(vod_time_str, '%Y-%m-%d %H:%M:%S')
                # 转换 datetime 对象到 Unix 时间戳
                in_data['vod_time'] = int(time.mktime(dt.timetuple()))
            except ValueError as e:
                raise ValidationError(f"Invalid date format for vod_time: {vod_time_str}")
        return in_data


# url = 'https://cj.lziapi.com/api.php/provide/vod/from/lzm3u8?ac='
url = 'https://haiwaikan.com/api.php/provide/vod?ac='


def _get_list(page):
    res = requests.get(f'{url}videolist&pg={page}', timeout=5)
    if res.status_code != 200:
        return
    return json.loads(res.text)


def get_list(page):
    content = _get_list(page)

    if len(content['list']) <= 0:
        return

    log.info(f'共{content["total"]}页正在处理第{content["page"]}页的内容')
    print(f"正在处理第{content['page']}页的内容")

    with open(sign_file, 'w+') as f:
        f.write(content['page'])

    ids = [vod['vod_id'] for vod in content['list']]
    print(f'count = {len(ids)}')
    response = requests.get(f'{url}detail&ids={ids}', timeout=5)
    schema = MacVodSchema()
    vod_detail_list = [schema.load(json_o) for json_o in json.loads(response.text)['list']]

    for index in range(0, len(vod_detail_list)):
        vod_detail_list[index].vod_play_url = parse_urls(
            vod_detail_list[index].vod_play_url, 0, vod_detail_list[index].vod_name)

    for vod_detail in vod_detail_list:
        session.add(vod_detail)

    session.commit()


def main():
    # 获取起始页
    try:
        with open(sign_file, 'r') as file:
            content = file.read()
            start_page = int(content)
    except FileNotFoundError as e:
        start_page = 1

    content = _get_list(1)
    pagecount = content['pagecount']

    # 分页处理采集数据
    for pg in range(start_page, pagecount):
        get_list(pg)
    session.close()


if __name__ == '__main__':
    main()
