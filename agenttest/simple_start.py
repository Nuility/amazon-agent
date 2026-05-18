import sys
import os

print("Python版本:", sys.version)
print("当前工作目录:", os.getcwd())
print("\n切换到api目录...")
os.chdir("D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api")
print("新工作目录:", os.getcwd())

print("\n添加路径...")
src_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src"
api_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api"
sys.path.insert(0, src_dir)
sys.path.insert(0, api_dir)
print("sys.path前3项:", sys.path[:3])

print("\n导入server模块...")
try:
    import server
    print("server模块导入成功")
    print("server.app:", server.app)
except Exception as e:
    print("导入失败:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n启动服务在 http://127.0.0.1:8001")
import uvicorn
uvicorn.run(server.app, host="127.0.0.1", port=8001)
