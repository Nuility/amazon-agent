import os
import sys

api_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api"
src_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src"

os.chdir(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

import uvicorn
import fastapi
print(f"uvicorn版本: {uvicorn.__version__}")
print(f"fastapi版本: {fastapi.__version__}")

print(f"\n工作目录: {os.getcwd()}")
print(f"Python路径: {sys.path[0]}")

print("\n导入server模块...")
from server import app
print(f"app类型: {type(app)}")
print(f"app标题: {app.title}")
print(f"路由数量: {len(app.routes)}")

print("\n准备启动服务...")
print("访问地址: http://127.0.0.1:8001")
print("API文档: http://127.0.0.1:8001/docs")
print("\n按Ctrl+C停止\n")

uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
