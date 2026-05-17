"""启动脚本"""
import os
import sys

api_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import uvicorn
from server import app

if __name__ == "__main__":
    print("启动服务在端口9000...")
    uvicorn.run(app, host="127.0.0.1", port=9000)
