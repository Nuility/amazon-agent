import os
import sys
import traceback

try:
    api_dir = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/src/api"
    os.chdir(api_dir)
    
    src_dir = os.path.dirname(api_dir)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    if api_dir not in sys.path:
        sys.path.insert(0, api_dir)
    
    print("当前目录:", os.getcwd())
    print("Python路径:", sys.path[:4])
    
    print("\n导入模块...")
    from main import Application
    print("Application导入成功")
    
    print("\n初始化应用...")
    app = Application()
    config_path = "D:/云码道/amazon-agent-feature-ui-enhancement/agenttest/config/config.yaml"
    
    if not app.initialize(config_path):
        print("应用初始化失败!")
        sys.exit(1)
    
    print("应用初始化成功!")
    print("\n启动服务器...")
    print("访问地址: http://127.0.0.1:8001")
    print("API文档: http://127.0.0.1:8001/docs")
    
    import uvicorn
    from server import app as fastapi_app
    
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8001, log_level="info")
    
except Exception as e:
    print("\n启动失败!")
    print(f"错误: {e}")
    traceback.print_exc()
