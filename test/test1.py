from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# 定义Base类
Base = declarative_base()


# 定义MacVod模型
class MacVod(Base):
    __tablename__ = 'mac_vod'
    vod_id = Column(Integer, primary_key=True)
    vod_play_url = Column(String)


# 创建数据库连接
engine = create_engine('mysql+pymysql://root:123456@localhost/tv2')
Base.metadata.create_all(engine)  # 创建表结构
session = Session(bind=engine)


# 假设我们要实现分页查询
def query_vods(page, page_size):
    # 计算跳过的记录数
    offset = (page - 1) * page_size
    # 执行查询，限制记录数和跳过的记录数
    results = session.query(MacVod).offset(offset).limit(page_size).all()
    return results


# 示例：查询第2页，每页显示10条记录
page_number = 1
page_size = 10
vods = query_vods(page_number, page_size)
for vod in vods:
    print(vod.vod_id, vod.vod_play_url)

# 不要忘记关闭会话
session.close()
