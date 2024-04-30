url = "https://cdn.v82u1l.com/fvod/ff34b26f50d33f1ae55a2829e158d4cb38c589bed8d09f6732bd9df94b6858c7443f7dcc59e4d6044059e302b8d175eb4e752d0cdb061898cc78e6414057410c12d36432dd03b38b921c07e8bfad6789b64f007a85e475d1.ts"
url.replace('cdn.v82u1l.com', 'h.118318.xyz')
url.replace('h.118318.xyz', 'cdn.v82u1l.com')
url.replace('cdn.v82u1l.com', 'h.118318.xyz')
print(url)

# 原始字符串
text = "Hello world, world is great."

# 替换字符串中的 'world' 为 'everyone'
new_text = text.replace("world", "everyone")

print(new_text)
# 输出: Hello everyone, everyone is great.

from urllib.parse import urlparse

Url = urlparse(url)
if Url.netloc == 'cdn.v82u1l.com':
    # Url.netloc = 'h.118318.xyz'
    Url.__setattr__('netloc', 'h.118318.xyz')
print(Url.geturl())
