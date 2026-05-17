import sys
import os

os.chdir("D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api")
sys.path.insert(0, "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src")

print("Python:", sys.version.split()[0])
print("工作目录:", os.getcwd())
print("\n导入server...")
from server import app
print("导入成功!")
print("app类型:", type(app))
print("app名称:", app.title)

print("\n准备启动服务器...")
print("地址: http://127.0.0.1:8001")
print("\n按Ctrl+C停止\n")

import uvicorn.config
import uvicorn.server

config = uvicorn.config.Config(app, host="127.0.0.1", port=8001, log_level="debug")
server = uvicorn.server.Server(config)

import asyncio
asyncio.run(server.serve())
