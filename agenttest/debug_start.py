import os
import sys

os.chdir("D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api")
sys.path.insert(0, "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src")
sys.path.insert(0, "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api")

print("1. 测试导入...")
try:
    from server import app
    print("   [OK] server.app导入成功")
except Exception as e:
    print(f"   [FAIL] 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2. 测试应用初始化...")
try:
    from main import Application
    print("   [OK] Application类导入成功")
except Exception as e:
    print(f"   [FAIL] Application导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. 启动uvicorn...")
import uvicorn
print("   监听: http://127.0.0.1:8001")
uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
