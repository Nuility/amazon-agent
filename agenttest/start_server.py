import os
import sys
import uvicorn

api_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api"
src_dir = os.path.dirname(api_dir)

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

os.chdir(api_dir)

print("启动服务...")
print("访问地址: http://127.0.0.1:8001")
print("API文档: http://127.0.0.1:8001/docs")
print("按 Ctrl+C 停止\n")

from server import app

uvicorn.run(app, host="127.0.0.1", port=8001)
