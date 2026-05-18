import subprocess
import sys
import time
import urllib.request

print("启动用户管理智能体系统...\n")

script_path = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api/run_server.py"

process = subprocess.Popen(
    [sys.executable, script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print(f"进程ID: {process.pid}")
print("等待服务启动...\n")

for i in range(10):
    time.sleep(1)
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8001/api/health", timeout=2)
        print(f"[成功] 服务已启动! (尝试 {i+1}/10)")
        print(f"\n访问地址:")
        print(f"  Web界面: http://127.0.0.1:8001")
        print(f"  API文档: http://127.0.0.1:8001/docs")
        print(f"  健康检查: http://127.0.0.1:8001/api/health")
        print(f"\n进程ID: {process.pid}")
        print("服务正在后台运行,关闭此窗口不会停止服务")
        sys.exit(0)
    except Exception as e:
        print(f"[等待中] 尝试 {i+1}/10 - {e}")
        continue

print("\n[失败] 服务未能启动")
stdout, stderr = process.communicate(timeout=1)
print(f"标准输出: {stdout}")
print(f"错误输出: {stderr}")
sys.exit(1)
