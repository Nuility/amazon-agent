"""FastAPI服务端 - Agent UI后端API"""
import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

api_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from main import Application


app_instance: Optional[Application] = None


class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class CommandRequest(BaseModel):
    command: str
    params: Optional[Dict[str, Any]] = None


class LLMConfigRequest(BaseModel):
    enabled: bool
    provider: str
    api_key: str
    api_endpoint: str
    model: str
    timeout: int = 30
    max_retries: int = 3


@asynccontextmanager
async def lifespan(app: FastAPI):
    global app_instance
    app_instance = Application()
    
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config",
        "config.yaml"
    )
    
    if not app_instance.initialize(config_path):
        raise RuntimeError("应用初始化失败")
    
    yield
    
    app_instance.shutdown()


app = FastAPI(
    title="用户管理智能体 API",
    description="Agent UI 后端API服务",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回Agent UI页面"""
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Agent UI</h1><p>请创建 ui/index.html 文件</p>")


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """聊天式交互接口"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    try:
        msg = message.message.lower().strip()
        response_text = ""
        data = None
        
        if "创建" in msg or "添加" in msg or "新增" in msg:
            response_text = "请提供用户信息，格式：创建用户 用户名 邮箱 [手机号]"
            data = {"action": "create", "hint": "username email [phone]"}
            
        elif "查询" in msg or "查找" in msg or "搜索" in msg:
            if "所有" in msg or "列表" in msg:
                result = app_instance.user_service.list_users()
                if result.success:
                    users = result.data.get("users", [])
                    response_text = f"共找到 {len(users)} 个用户"
                    data = {"users": users}
                else:
                    response_text = f"查询失败: {result.error_message}"
            else:
                response_text = "请提供用户ID进行查询"
                data = {"action": "query", "hint": "user_id"}
                
        elif "删除" in msg:
            response_text = "请提供要删除的用户ID"
            data = {"action": "delete", "hint": "user_id"}
            
        elif "统计" in msg or "分析" in msg:
            result = app_instance.user_service.list_users()
            if result.success:
                users = result.data.get("users", [])
                total = result.data.get("total", 0)
                response_text = f"用户总数: {total}\n活跃用户: {len([u for u in users if u.get('status') == 'active'])}"
                data = {"statistics": {"total": total, "users": users}}
            else:
                response_text = f"统计失败: {result.error_message}"
                
        elif "帮助" in msg or "help" in msg:
            response_text = """可用命令：
1. 创建用户 - 创建新用户
2. 查询所有用户 - 查看用户列表
3. 查询用户 - 按ID查询用户
4. 删除用户 - 删除指定用户
5. 统计 - 查看用户统计信息
6. 帮助 - 显示此帮助信息"""
            
        else:
            response_text = "未识别的命令。输入'帮助'查看可用命令。"
        
        return {
            "success": True,
            "message": response_text,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"处理失败: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@app.post("/api/execute")
async def execute_command(request: CommandRequest):
    """执行具体命令"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    try:
        command = request.command
        params = request.params or {}
        result = None
        
        if command == "create_user":
            result = app_instance.user_service.create_user(
                params,
                operator=params.get("operator", "ui_user")
            )
            
        elif command == "get_user":
            result = app_instance.user_service.get_user(params.get("user_id"))
            
        elif command == "update_user":
            result = app_instance.user_service.update_user(
                params.get("user_id"),
                params.get("update_data", {}),
                operator=params.get("operator", "ui_user")
            )
            
        elif command == "delete_user":
            result = app_instance.user_service.delete_user(
                params.get("user_id"),
                logical=params.get("logical", True),
                operator=params.get("operator", "ui_user")
            )
            
        elif command == "list_users":
            result = app_instance.user_service.list_users(
                filters=params.get("filters"),
                page=params.get("page", 1),
                page_size=params.get("page_size", 20)
            )
            
        elif command == "analyze":
            result = app_instance.analysis_service.analyze_users(
                analysis_type=params.get("analysis_type", "basic"),
                params=params.get("params")
            )
            
        else:
            raise HTTPException(status_code=400, detail=f"未知命令: {command}")
        
        if result and result.success:
            response_data = result.data
            if hasattr(response_data, 'to_dict'):
                response_data = response_data.to_dict()
            return {
                "success": True,
                "data": response_data,
                "message": "执行成功"
            }
        else:
            return {
                "success": False,
                "error": result.error_message if result else "执行失败",
                "error_code": result.error_code if result else -1
            }
            
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/api/users")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None
):
    """获取用户列表"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    filters = {}
    if status:
        filters["status"] = status
    
    result = app_instance.user_service.list_users(filters, page, page_size)
    
    if result.success:
        return result.data
    raise HTTPException(status_code=500, detail=result.error_message)


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """获取用户详情"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    result = app_instance.user_service.get_user(user_id)
    
    if result.success:
        return result.data.to_dict()
    raise HTTPException(status_code=404, detail=result.error_message)


@app.post("/api/users")
async def create_user(user_data: Dict[str, Any] = Body(...)):
    """创建用户"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    result = app_instance.user_service.create_user(
        user_data,
        operator=user_data.get("operator", "ui_user")
    )
    
    if result.success:
        return {"success": True, "user": result.data.to_dict()}
    return {"success": False, "error": result.error_message}


@app.put("/api/users/{user_id}")
async def update_user(user_id: str, update_data: Dict[str, Any] = Body(...)):
    """更新用户"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    result = app_instance.user_service.update_user(
        user_id,
        update_data,
        operator=update_data.get("operator", "ui_user")
    )
    
    if result.success:
        return {"success": True, "user": result.data.to_dict()}
    return {"success": False, "error": result.error_message}


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: str, logical: bool = True):
    """删除用户"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    result = app_instance.user_service.delete_user(
        user_id,
        logical=logical,
        operator="ui_user"
    )
    
    if result.success:
        return {"success": True}
    return {"success": False, "error": result.error_message}


@app.get("/api/statistics")
async def get_statistics():
    """获取统计数据"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    result = app_instance.analysis_service.analyze_users("basic")
    
    if result.success:
        return result.data if isinstance(result.data, dict) else {"data": result.data}
    raise HTTPException(status_code=500, detail=result.error_message)


@app.get("/api/config")
async def get_config():
    """获取配置信息"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    return app_instance.config.to_dict()


@app.get("/api/config/llm")
async def get_llm_config():
    """获取大模型配置"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    config = app_instance.config
    return {
        "enabled": config.enable_llm_integration,
        "config": config.llm_api_config
    }


@app.post("/api/config/llm")
async def update_llm_config(config: LLMConfigRequest):
    """更新大模型配置"""
    if not app_instance:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    try:
        import yaml
        
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config",
            "config.yaml"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            current_config = yaml.safe_load(f) or {}
        
        current_config['enable_llm_integration'] = config.enabled
        current_config['llm_api_config'] = {
            'provider': config.provider,
            'api_key': config.api_key,
            'api_endpoint': config.api_endpoint,
            'model': config.model,
            'timeout': config.timeout,
            'max_retries': config.max_retries
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(current_config, f, allow_unicode=True, default_flow_style=False)
        
        app_instance.config.enable_llm_integration = config.enabled
        app_instance.config.llm_api_config = current_config['llm_api_config']
        
        from infrastructure.llm_client import create_llm_client
        app_instance.analysis_service.llm_client = create_llm_client(
            current_config['llm_api_config']
        )
        
        return {
            "success": True,
            "message": "配置已更新",
            "config": current_config['llm_api_config']
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/config/llm/test")
async def test_llm_connection(config: LLMConfigRequest):
    """测试大模型连接"""
    try:
        from infrastructure.llm_client import create_llm_client
        
        llm_config = {
            'provider': config.provider,
            'api_key': config.api_key,
            'api_endpoint': config.api_endpoint,
            'model': config.model,
            'timeout': config.timeout,
            'max_retries': config.max_retries
        }
        
        llm_client = create_llm_client(llm_config)
        
        if config.provider == "mock":
            return {
                "success": True,
                "message": "模拟客户端无需测试，始终可用"
            }
        
        try:
            result = llm_client.call("测试连接")
            return {
                "success": True,
                "message": "连接成功",
                "response": result[:100] if result else ""
            }
        except NotImplementedError:
            return {
                "success": False,
                "error": "该大模型客户端尚未完整实现，请等待后续更新"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"连接失败: {str(e)}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """启动服务器"""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
