import os
import sys
import subprocess
import time
import signal

api_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api"
src_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src"

os.chdir(api_dir)
env = os.environ.copy()
env["PYTHONPATH"] = src_dir

print("=" * 60)
print("用户管理智能体系统 - 服务启动器")
print("=" * 60)
print("\n启动配置:")
print(f"  主机: 0.0.0.0 (允许外部访问)")
print(f"  端口: 8001")
print(f"  访问地址: http://localhost:8001")
print(f"  API文档: http://localhost:8001/docs")
print("\n按 Ctrl+C 停止服务\n")
print("=" * 60 + "\n")

process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--log-level", "info"],
    env=env,
    cwd=api_dir
)

def signal_handler(sig, frame):
    print("\n\n正在停止服务...")
    process.terminate()
    process.wait()
    print("服务已停止")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    while process.poll() is None:
        time.sleep(1)
except KeyboardInterrupt:
    signal_handler(None, None)

if process.poll() is not None:
    print(f"\n服务已退出，退出码: {process.returncode}")
