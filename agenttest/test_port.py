from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

def run_server():
    server = HTTPServer(("127.0.0.1", 8001), SimpleHTTPRequestHandler)
    print("HTTP服务器启动在 http://127.0.0.1:8001")
    server.serve_forever()

thread = threading.Thread(target=run_server, daemon=True)
thread.start()

time.sleep(2)

import urllib.request
try:
    response = urllib.request.urlopen("http://127.0.0.1:8001/", timeout=3)
    print("端口8001可用,服务响应正常!")
except Exception as e:
    print("测试失败:", e)
