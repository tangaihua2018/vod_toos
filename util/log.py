import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

# 创建一个logger
logger = logging.getLogger('vod')
logger.setLevel(logging.DEBUG)  # 设置日志级别
curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
# 创建一个handler，用于写入日志文件，每天更换一次日志文件
file_handler = TimedRotatingFileHandler(
    f'vod-{curr_date}.log',  # 基础文件名
    when='midnight',  # 每天午夜更换
    interval=1,  # 每1天更换一次
    backupCount=7  # 保留7天的日志文件
)
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个handler，用于写入日志文件
# file_handler = logging.FileHandler('./vod.log')  # 替换为你的日志文件路径
file_handler.setLevel(logging.DEBUG)  # 可以为该handler设置不同的日志级别

# 创建一个formatter，设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将handler添加到logger
logger.addHandler(file_handler)

# 记录一条日志
# logger.debug("This is a debug message")
# logger.info('zheshisha')

log = logger
