import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout

from util.util import debug_log


def request_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求返回4xx或5xx响应码，抛出HTTPError
        if response.status_code == 200:
            return response.text
    except HTTPError as e:
        debug_log(f"HTTP error occurred: {e}")  # HTTP错误
    except ConnectionError as e:
        debug_log(f"Connection error occurred: {e}")  # 连接问题，如DNS查询失败、拒绝连接等
    except Timeout as e:
        debug_log(f"Timeout occurred: {e}")  # 请求超时
    except Exception as e:
        debug_log(f"An error occurred: {e}")  # 其他所有异常


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=5,  # 总重试次数
                backoff_factor=1,  # 重试间隔时间的增长因子
                status_forcelist=[500, 502, 503, 504, 408, 429])  # 状态码在此列表中的会进行重试
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))


def http_get(url):
    response = session.get(url, timeout=10)
    if response.status_code == 200:
        return response.text

