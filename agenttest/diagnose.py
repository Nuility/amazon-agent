import sys
import os
import traceback

print("=" * 60)
print("服务诊断工具")
print("=" * 60)

print("\n【1. 检查Python环境】")
print(f"   Python版本: {sys.version}")
print(f"   Python路径: {sys.executable}")

print("\n【2. 检查项目路径】")
project_root = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest"
src_dir = os.path.join(project_root, "src")
api_dir = os.path.join(src_dir, "api")
config_dir = os.path.join(project_root, "config")

print(f"   项目根目录: {project_root}")
print(f"   是否存在: {os.path.exists(project_root)}")
print(f"   src目录: {src_dir}")
print(f"   是否存在: {os.path.exists(src_dir)}")
print(f"   api目录: {api_dir}")
print(f"   是否存在: {os.path.exists(api_dir)}")
print(f"   config目录: {config_dir}")
print(f"   是否存在: {os.path.exists(config_dir)}")

print("\n【3. 检查关键文件】")
server_py = os.path.join(api_dir, "server.py")
run_server_py = os.path.join(api_dir, "run_server.py")
config_yaml = os.path.join(config_dir, "config.yaml")
main_py = os.path.join(src_dir, "main.py")

print(f"   server.py: {os.path.exists(server_py)}")
print(f"   run_server.py: {os.path.exists(run_server_py)}")
print(f"   config.yaml: {os.path.exists(config_yaml)}")
print(f"   main.py: {os.path.exists(main_py)}")

print("\n【4. 设置Python路径】")
os.chdir(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)
print(f"   工作目录: {os.getcwd()}")
print(f"   sys.path[0]: {sys.path[0]}")

print("\n【5. 检查依赖包】")
try:
    import uvicorn
    print(f"   uvicorn: {uvicorn.__version__}")
except ImportError as e:
    print(f"   uvicorn: 未安装 - {e}")

try:
    import fastapi
    print(f"   fastapi: {fastapi.__version__}")
except ImportError as e:
    print(f"   fastapi: 未安装 - {e}")

try:
    import pydantic
    print(f"   pydantic: {pydantic.__version__}")
except ImportError as e:
    print(f"   pydantic: 未安装 - {e}")

print("\n【6. 尝试导入server模块】")
try:
    from server import app
    print(f"   导入成功!")
    print(f"   app类型: {type(app)}")
    print(f"   app标题: {app.title}")
    print(f"   路由数量: {len(app.routes)}")
    
    print("\n【7. 检查路由】")
    for i, route in enumerate(app.routes[:5]):
        print(f"   路由{i+1}: {route.path if hasattr(route, 'path') else route}")
    if len(app.routes) > 5:
        print(f"   ... 还有 {len(app.routes) - 5} 个路由")
        
except Exception as e:
    print(f"   导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n【8. 检查配置文件】")
try:
    import yaml
    with open(config_yaml, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print(f"   配置加载成功")
    print(f"   enable_llm_integration: {config.get('enable_llm_integration')}")
    print(f"   log_level: {config.get('log_level')}")
except Exception as e:
    print(f"   配置加载失败: {e}")

print("\n【9. 测试端口可用性】")
import socket
try:
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.bind(('127.0.0.1', 8001))
    test_socket.close()
    print("   端口8001可用")
except Exception as e:
    print(f"   端口8001被占用: {e}")

print("\n" + "=" * 60)
print("诊断完成！所有检查通过，准备启动服务...")
print("=" * 60)
