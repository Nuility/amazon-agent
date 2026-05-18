from fastapi import FastAPI
import uvicorn
import sys

app = FastAPI()

@app.get("/")
def root():
    return {"message": "测试成功", "port": 8001}

@app.get("/health")
def health():
    return {"status": "ok"}

print("=" * 60)
print("测试FastAPI服务")
print("=" * 60)
print(f"\nPython版本: {sys.version.split()[0]}")
print(f"启动地址: http://0.0.0.0:8001")
print("访问测试: http://localhost:8001")
print("\n按Ctrl+C停止\n")
print("=" * 60 + "\n")

uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
