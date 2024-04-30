from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker

# 定义Base类
from db.parseUrls import parse_urls
from util.util import isolate_source, debug_log

Base = declarative_base()

user = 'root'
password = '123456'
dbname = 'tv2'

# 创建数据库连接
engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost/{dbname}')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)  # 创建表结构


# 定义MacVod模型
class MacVod(Base):
    __tablename__ = 'mac_vod'
    vod_id = Column(Integer, primary_key=True)
    vod_play_url = Column(String)
    vod_play_from = Column(String)
    vod_name = Column(String)
    vod_pic = Column(String)
    vod_pic_thumb = Column(String)
    vod_pic_slide = Column(String)
    vod_pic_screenshot = Column(String)


# 假设我们要实现分页查询
def query_vods(page, page_size):
    with Session() as session:
        # 计算跳过的记录数
        offset = (page - 1) * page_size
        # 执行查询，限制记录数和跳过的记录数
        results = session.query(MacVod).filter(MacVod.vod_play_from.like('%haiwaikan%')).offset(offset).limit(page_size)
        return results


def process_data(record):
    with Session() as session:
        have, index, length = isolate_source(record.vod_play_from)
        if not have:
            debug_log(f'{record.vod_name}没有那啥海外看的')
            return
        new_vod_play_url = parse_urls(record.vod_play_url, index, length, record.vod_name)
        session.query(MacVod).filter(MacVod.vod_id == record.vod_id).update({"vod_play_url": new_vod_play_url})
        session.commit()
