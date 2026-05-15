"""FastAPI backend for the Agent UI."""
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

api_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(api_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from main import Application


app_instance: Optional[Application] = None

CREATE_KEYWORDS = ("create", "add", "new")
QUERY_KEYWORDS = ("query", "search", "find", "get")
LIST_KEYWORDS = ("all", "list", "users")
DELETE_KEYWORDS = ("delete", "remove")
STATS_KEYWORDS = ("stats", "statistics", "analyze", "analysis")
HELP_KEYWORDS = ("help", "commands")
AD_KEYWORDS = ("ad", "ads", "campaign", "campaigns", "acos", "roas")
AGENT_KEYWORDS = ("agent", "workflow", "optimize ads", "run analysis")


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


class AgentRunRequest(BaseModel):
    objective: str = "Improve campaign efficiency while protecting profitable growth."
    filters: Optional[Dict[str, Any]] = None


class PromptTemplateRequest(BaseModel):
    system_role: str
    task_template: str
    output_style: str


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def _require_app() -> Application:
    if not app_instance:
        raise HTTPException(status_code=503, detail="Service is not initialized")
    return app_instance


def _build_statistics_payload(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    app = _require_app()
    result = app.analysis_service.get_statistics(filters)

    if not result.success or not result.data:
        raise HTTPException(
            status_code=500,
            detail=result.error_message or "Failed to load statistics",
        )

    stats = result.data
    return {
        "total_users": stats.total_users,
        "status_distribution": stats.status_distribution,
        "tag_distribution": stats.tag_distribution,
        "attributes_distribution": stats.attributes_distribution,
    }


def _build_ad_summary_payload(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    app = _require_app()
    result = app.ad_agent_service.get_summary(filters)

    if not result.success or not result.data:
        raise HTTPException(
            status_code=500,
            detail=result.error_message or "Failed to load ad summary",
        )

    return result.data.to_dict()


def _run_analysis(analysis_type: str, params: Optional[Dict[str, Any]] = None):
    app = _require_app()
    normalized = (analysis_type or "basic").lower()
    params = params or {}

    if normalized == "basic":
        return app.analysis_service.get_statistics(params.get("filters"))
    if normalized == "anomalies":
        return app.analysis_service.detect_anomalies()
    if normalized == "suggestions":
        return app.analysis_service.get_operation_suggestions(params)
    if normalized == "classification":
        return app.analysis_service.get_classification_suggestions(
            params.get("criteria", "group users by status"),
            params.get("filters"),
        )
    if normalized == "ads":
        return app.ad_agent_service.get_summary(params.get("filters"))
    if normalized == "ad_recommendations":
        return app.ad_agent_service.get_recommendations(params.get("filters"))

    raise HTTPException(status_code=400, detail=f"Unknown analysis type: {analysis_type}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global app_instance
    app_instance = Application()

    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config",
        "config.yaml",
    )

    if not app_instance.initialize(config_path):
        raise RuntimeError("Application initialization failed")

    yield

    app_instance.shutdown()


app = FastAPI(
    title="User Management Agent API",
    description="Agent UI backend API service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ui_dir = os.path.join(os.path.dirname(__file__), "ui")
app.mount("/ui", StaticFiles(directory=ui_dir), name="ui")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Return the bundled Agent UI page."""
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Agent UI</h1><p>Please create ui/index.html first.</p>")


@app.get("/api/health")
async def health_check():
    """Service health check."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Simple chat-style interface for common user-management actions."""
    app = _require_app()

    try:
        msg = message.message.lower().strip()
        response_text = ""
        data = None

        if _contains_any(msg, CREATE_KEYWORDS):
            response_text = "Provide user data in the form: create username email [phone]"
            data = {"action": "create", "hint": "username email [phone]"}
        elif _contains_any(msg, QUERY_KEYWORDS):
            if _contains_any(msg, LIST_KEYWORDS):
                result = app.user_service.list_users()
                if result.success:
                    users = result.data.get("users", [])
                    response_text = f"Found {len(users)} users"
                    data = {"users": users}
                else:
                    response_text = f"Query failed: {result.error_message}"
            else:
                response_text = "Please provide a user ID to query."
                data = {"action": "query", "hint": "user_id"}
        elif _contains_any(msg, DELETE_KEYWORDS):
            response_text = "Please provide the user ID to delete."
            data = {"action": "delete", "hint": "user_id"}
        elif _contains_any(msg, AD_KEYWORDS):
            ad_summary = _build_ad_summary_payload()
            response_text = (
                f"Ad campaigns: {ad_summary['total_campaigns']}\n"
                f"Spend: {ad_summary['total_cost']}\n"
                f"Sales: {ad_summary['total_sales']}\n"
                f"ROAS: {ad_summary['average_roas']}"
            )
            data = {"ad_summary": ad_summary}
        elif _contains_any(msg, AGENT_KEYWORDS):
            result = app.ad_agent_service.run_agent_workflow()
            if result.success and result.data:
                agent_run = result.data.to_dict()
                response_text = (
                    f"Agent workflow completed.\n"
                    f"Objective: {agent_run['objective']}\n"
                    f"Top next action: {agent_run['next_actions'][0]}"
                )
                data = {"agent_run": agent_run}
            else:
                response_text = f"Agent workflow failed: {result.error_message}"
        elif _contains_any(msg, STATS_KEYWORDS):
            statistics = _build_statistics_payload()
            active_users = statistics["status_distribution"].get("active", 0)
            response_text = f"Total users: {statistics['total_users']}\nActive users: {active_users}"
            data = {"statistics": statistics}
        elif _contains_any(msg, HELP_KEYWORDS):
            response_text = (
                "Available commands:\n"
                "1. create user\n"
                "2. query all users\n"
                "3. query user by id\n"
                "4. delete user\n"
                "5. stats\n"
                "6. help"
            )
        else:
            response_text = "Unknown command. Enter help to view available commands."

        return {
            "success": True,
            "message": response_text,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Processing failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
        }


@app.post("/api/execute")
async def execute_command(request: CommandRequest):
    """Execute a structured command from the UI."""
    app = _require_app()

    try:
        command = request.command
        params = request.params or {}
        result = None

        if command == "create_user":
            result = app.user_service.create_user(
                params,
                operator=params.get("operator", "ui_user"),
            )
        elif command == "get_user":
            result = app.user_service.get_user(params.get("user_id"))
        elif command == "update_user":
            result = app.user_service.update_user(
                params.get("user_id"),
                params.get("update_data", {}),
                operator=params.get("operator", "ui_user"),
            )
        elif command == "delete_user":
            result = app.user_service.delete_user(
                params.get("user_id"),
                logical=params.get("logical", True),
                operator=params.get("operator", "ui_user"),
            )
        elif command == "list_users":
            result = app.user_service.list_users(
                filters=params.get("filters"),
                page=params.get("page", 1),
                page_size=params.get("page_size", 20),
            )
        elif command == "analyze":
            result = _run_analysis(
                params.get("analysis_type", "basic"),
                params.get("params"),
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown command: {command}")

        if result and result.success:
            response_data = result.data
            if hasattr(response_data, "to_dict"):
                response_data = response_data.to_dict()
            return {
                "success": True,
                "data": response_data,
                "message": "Execution succeeded",
            }

        return {
            "success": False,
            "error": result.error_message if result else "Execution failed",
            "error_code": result.error_code if result else -1,
        }
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/users")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
):
    """Fetch a page of users."""
    app = _require_app()

    filters = {}
    if status:
        filters["status"] = status

    result = app.user_service.list_users(filters, page, page_size)
    if result.success:
        return result.data

    raise HTTPException(status_code=500, detail=result.error_message)


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Fetch one user by id."""
    app = _require_app()

    result = app.user_service.get_user(user_id)
    if result.success:
        return result.data.to_dict()

    raise HTTPException(status_code=404, detail=result.error_message)


@app.post("/api/users")
async def create_user(user_data: Dict[str, Any] = Body(...)):
    """Create a user."""
    app = _require_app()

    result = app.user_service.create_user(
        user_data,
        operator=user_data.get("operator", "ui_user"),
    )
    if result.success:
        return {"success": True, "user": result.data.to_dict()}

    return {"success": False, "error": result.error_message}


@app.put("/api/users/{user_id}")
async def update_user(user_id: str, update_data: Dict[str, Any] = Body(...)):
    """Update a user."""
    app = _require_app()

    result = app.user_service.update_user(
        user_id,
        update_data,
        operator=update_data.get("operator", "ui_user"),
    )
    if result.success:
        return {"success": True, "user": result.data.to_dict()}

    return {"success": False, "error": result.error_message}


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: str, logical: bool = True):
    """Delete a user."""
    app = _require_app()

    result = app.user_service.delete_user(
        user_id,
        logical=logical,
        operator="ui_user",
    )
    if result.success:
        return {"success": True}

    return {"success": False, "error": result.error_message}


@app.get("/api/statistics")
async def get_statistics():
    """Return aggregate user statistics."""
    return _build_statistics_payload()


@app.get("/api/ad-insights/summary")
async def get_ad_summary():
    """Return aggregate ad performance metrics."""
    return _build_ad_summary_payload()


@app.get("/api/ad-insights/campaigns")
async def get_ad_campaigns(status: Optional[str] = None):
    """Return seeded ad campaign performance rows."""
    app = _require_app()
    filters = {"status": status} if status else None
    result = app.ad_agent_service.list_campaigns(filters)
    if result.success:
        return {"campaigns": result.data}

    raise HTTPException(status_code=500, detail=result.error_message)


@app.get("/api/ad-insights/recommendations")
async def get_ad_recommendations(status: Optional[str] = None):
    """Return starter optimization recommendations for ad campaigns."""
    app = _require_app()
    filters = {"status": status} if status else None
    result = app.ad_agent_service.get_recommendations(filters)
    if result.success:
        return {"recommendations": result.data}

    raise HTTPException(status_code=500, detail=result.error_message)


@app.post("/api/ad-agent/run")
async def run_ad_agent(request: AgentRunRequest):
    """Run the starter ad agent workflow."""
    app = _require_app()
    result = app.ad_agent_service.run_agent_workflow(
        objective=request.objective,
        filters=request.filters,
    )
    if result.success and result.data:
        return {"success": True, "run": result.data.to_dict()}

    return {"success": False, "error": result.error_message}


@app.get("/api/ad-agent/prompt-template")
async def get_ad_agent_prompt_template():
    """Return the current ad agent prompt template."""
    app = _require_app()
    result = app.prompt_engineering_service.get_template()
    if result.success:
        return {"success": True, "template": result.data}

    return {"success": False, "error": result.error_message}


@app.post("/api/ad-agent/prompt-template")
async def update_ad_agent_prompt_template(request: PromptTemplateRequest):
    """Update the current ad agent prompt template."""
    app = _require_app()
    result = app.prompt_engineering_service.update_template(request.model_dump())
    if result.success:
        return {"success": True, "template": result.data}

    return {"success": False, "error": result.error_message}


@app.get("/api/config")
async def get_config():
    """Return the current application config."""
    app = _require_app()
    return app.config.to_dict()


@app.get("/api/config/llm")
async def get_llm_config():
    """Return LLM integration settings."""
    app = _require_app()
    return {
        "enabled": app.config.enable_llm_integration,
        "config": app.config.llm_api_config,
    }


@app.post("/api/config/llm")
async def update_llm_config(config: LLMConfigRequest):
    """Update LLM integration settings."""
    app = _require_app()

    try:
        import yaml

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config",
            "config.yaml",
        )

        with open(config_path, "r", encoding="utf-8") as f:
            current_config = yaml.safe_load(f) or {}

        current_config["enable_llm_integration"] = config.enabled
        current_config["llm_api_config"] = {
            "provider": config.provider,
            "api_key": config.api_key,
            "api_endpoint": config.api_endpoint,
            "model": config.model,
            "timeout": config.timeout,
            "max_retries": config.max_retries,
        }

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(current_config, f, allow_unicode=True, default_flow_style=False)

        app.config.enable_llm_integration = config.enabled
        app.config.llm_api_config = current_config["llm_api_config"]

        from infrastructure.llm_client import create_llm_client

        app.analysis_service.llm_client = create_llm_client(current_config["llm_api_config"])

        return {
            "success": True,
            "message": "Config updated",
            "config": current_config["llm_api_config"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/config/llm/test")
async def test_llm_connection(config: LLMConfigRequest):
    """Test the configured LLM connection."""
    try:
        from infrastructure.llm_client import create_llm_client

        llm_config = {
            "provider": config.provider,
            "api_key": config.api_key,
            "api_endpoint": config.api_endpoint,
            "model": config.model,
            "timeout": config.timeout,
            "max_retries": config.max_retries,
        }

        llm_client = create_llm_client(llm_config)

        if config.provider == "mock":
            return {
                "success": True,
                "message": "Mock client is always available.",
            }

        try:
            result = llm_client.call("test connection")
            return {
                "success": True,
                "message": "Connection succeeded",
                "response": result[:100] if result else "",
            }
        except NotImplementedError:
            return {
                "success": False,
                "error": "The configured LLM client is still a placeholder implementation.",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection failed: {str(e)}",
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI service."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
