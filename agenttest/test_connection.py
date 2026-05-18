import urllib.request
import time

time.sleep(3)
try:
    response = urllib.request.urlopen("http://127.0.0.1:8001/", timeout=3)
    print("服务运行正常!")
    print("响应:", response.read().decode())
except Exception as e:
    print("服务未响应:", e)
