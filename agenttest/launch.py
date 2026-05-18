import subprocess
import sys
import time
import os

print("=" * 60)
print("启动用户管理智能体系统")
print("=" * 60)

script_path = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/start.py"

print(f"\n启动脚本: {script_path}")
print("启动服务...\n")

env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"

process = subprocess.Popen(
    [sys.executable, "-u", script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    env=env
)

print(f"进程ID: {process.pid}")
print("\n等待服务启动...\n")

startup_output = []
start_time = time.time()
timeout = 15

while time.time() - start_time < timeout:
    line = process.stdout.readline()
    if line:
        startup_output.append(line)
        print(line.rstrip())
    
    import urllib.request
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8001/api/health", timeout=1)
        if response.status == 200:
            print("\n" + "=" * 60)
            print("✓ 服务启动成功!")
            print("=" * 60)
            print("\n访问地址:")
            print("  Web界面: http://127.0.0.1:8001")
            print("  API文档: http://127.0.0.1:8001/docs")
            print("  健康检查: http://127.0.0.1:8001/api/health")
            print(f"\n进程ID: {process.pid}")
            print("服务正在运行,关闭此窗口将停止服务")
            print("=" * 60)
            
            while True:
                line = process.stdout.readline()
                if line:
                    print(line.rstrip())
                if process.poll() is not None:
                    break
            break
    except:
        pass
    
    if process.poll() is not None:
        print("\n服务进程已退出!")
        print(f"退出码: {process.returncode}")
        print("\n输出:")
        for line in startup_output:
            print(line.rstrip())
        break

if time.time() - start_time >= timeout:
    print("\n启动超时!")
    process.terminate()
    stdout, _ = process.communicate(timeout=5)
    print("\n输出:")
    print(stdout)
