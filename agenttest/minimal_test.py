from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

if __name__ == "__main__":
    print("启动最小化FastAPI服务...")
    print("访问: http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
