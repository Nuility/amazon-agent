from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

from .routes import skill_routes, dialog_routes, changelog_routes
from .response import error_response, ErrorCode


def create_app() -> FastAPI:
    app = FastAPI(
        title="Amazon Agent",
        description="Amazon广告助手 - 具有Skill系统和智能对话功能",
        version="2.2.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(skill_routes.router)
    app.include_router(dialog_routes.router)
    app.include_router(changelog_routes.router)
    
    @app.get("/api/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": "2.2.0",
            "timestamp": "2026-05-19T19:45:00"
        }
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error_response(
                code=ErrorCode.INTERNAL_ERROR,
                message=str(exc),
                details={"traceback": traceback.format_exc()}
            )
        )
    
    return app


app = create_app()
