import sys
import os
import uvicorn
import logging

print("=" * 60)
print("启动用户管理智能体系统")
print("=" * 60)

api_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api"
src_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src"

os.chdir(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

print(f"\n工作目录: {os.getcwd()}")
print(f"Python: {sys.version.split()[0]}")

print("\n导入应用...")
from server import app
print("导入成功!")

print("\n服务配置:")
print("  主机: 127.0.0.1")
print("  端口: 8001")
print("  访问地址: http://127.0.0.1:8001")
print("  API文档: http://127.0.0.1:8001/docs")
print("  健康检查: http://127.0.0.1:8001/api/health")

print("\n启动服务器...")
print("按 Ctrl+C 停止服务\n")
print("=" * 60 + "\n")

try:
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info",
        access_log=True
    )
except KeyboardInterrupt:
    print("\n服务已停止")
except Exception as e:
    print(f"\n启动失败: {e}")
    import traceback
    traceback.print_exc()
