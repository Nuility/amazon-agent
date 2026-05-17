import os
import sys

print("=" * 50)
print("用户管理智能体系统")
print("=" * 50)

project_root = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest"
src_dir = os.path.join(project_root, "src")
api_dir = os.path.join(src_dir, "api")

os.chdir(api_dir)
sys.path.insert(0, src_dir)

print(f"\n工作目录: {os.getcwd()}")
print(f"Python路径: {sys.path[0]}")

print("\n正在初始化应用...")

try:
    from server import app as fastapi_app
    print("[成功] FastAPI应用加载完成")
except Exception as e:
    print(f"[失败] 应用加载错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n服务启动中...")
print("访问地址: http://127.0.0.1:8001")
print("API文档: http://127.0.0.1:8001/docs")
print("Web界面: http://127.0.0.1:8001")
print("\n按 Ctrl+C 停止服务\n")

import uvicorn
uvicorn.run(
    fastapi_app,
    host="127.0.0.1",
    port=8001,
    log_level="info",
    access_log=True
)
