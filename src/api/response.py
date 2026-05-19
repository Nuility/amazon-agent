from datetime import datetime
from typing import Any, Dict, Optional
import uuid


def success_response(
    data: Any = None,
    message: str = "Success",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "message": message,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "request_id": str(uuid.uuid4()),
            **(metadata or {})
        }
    }


def error_response(
    code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        },
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    }


class ErrorCode:
    SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
    SKILL_VALIDATION_ERROR = "SKILL_VALIDATION_ERROR"
    SKILL_EXECUTION_ERROR = "SKILL_EXECUTION_ERROR"
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    INVALID_REQUEST = "INVALID_REQUEST"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    CHANGELOG_NOT_FOUND = "CHANGELOG_NOT_FOUND"
