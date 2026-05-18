import urllib.request
try:
    response = urllib.request.urlopen("http://127.0.0.1:9000/", timeout=3)
    print("服务运行正常!")
    print("响应状态码:", response.status)
    print("响应内容长度:", len(response.read()))
except Exception as e:
    print("服务未响应:", e)
