import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout


def request_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求返回4xx或5xx响应码，抛出HTTPError
        if response.status_code != 200:
            return response.text
    except HTTPError as e:
        debug_log(f"HTTP error occurred: {e}")  # HTTP错误
    except ConnectionError as e:
        debug_log(f"Connection error occurred: {e}")  # 连接问题，如DNS查询失败、拒绝连接等
    except Timeout as e:
        debug_log(f"Timeout occurred: {e}")  # 请求超时
    except Exception as e:
        debug_log(f"An error occurred: {e}")  # 其他所有异常
