import sys
import os

api_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

print("步骤1: 导入模块...")
import uvicorn
print("  uvicorn导入成功")

from server import app
print("  server.app导入成功")
print(f"  app类型: {type(app)}")
print(f"  app标题: {app.title}")

print("\n步骤2: 配置uvicorn...")
config = uvicorn.Config(app, host="127.0.0.1", port=8001, log_level="debug")
print(f"  配置完成: {config}")

print("\n步骤3: 创建server...")
server = uvicorn.Server(config)
print(f"  server创建成功: {type(server)}")

print("\n步骤4: 准备启动...")
print("  访问地址: http://127.0.0.1:8001")
print("  按Ctrl+C停止\n")

import asyncio
print("步骤5: 运行server...")
asyncio.run(server.serve())
