from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional

from ..services.changelog_service import ChangeLogManager
from ..domain.enums import UpdateType
from ..api.response import success_response, error_response, ErrorCode

router = APIRouter(prefix="/api/v1/changelogs", tags=["ChangeLogs"])

changelog_manager = ChangeLogManager()


@router.get("")
async def list_changelogs(limit: int = 10):
    logs = changelog_manager.list_logs(limit)
    
    return success_response(
        data=[log.model_dump() for log in logs],
        message=f"Found {len(logs)} changelogs"
    )


@router.get("/{log_id}")
async def get_changelog(log_id: str):
    log = changelog_manager.get_log(log_id)
    
    if not log:
        return error_response(
            code=ErrorCode.CHANGELOG_NOT_FOUND,
            message=f"Changelog not found: {log_id}"
        )
    
    return success_response(data=log.model_dump())


@router.post("")
async def create_changelog(request: Dict[str, Any]):
    version = request.get("version")
    title = request.get("title")
    update_type_str = request.get("update_type", "feature")
    description = request.get("description", "")
    changes = request.get("changes", [])
    breaking_changes = request.get("breaking_changes", [])
    related_docs = request.get("related_docs", [])
    author = request.get("author", "System")
    tags = request.get("tags", [])
    
    if not version or not title:
        return error_response(
            code=ErrorCode.INVALID_REQUEST,
            message="version and title are required"
        )
    
    try:
        update_type = UpdateType(update_type_str.lower())
    except ValueError:
        update_type = UpdateType.FEATURE
    
    log = changelog_manager.generate_log(
        version=version,
        title=title,
        update_type=update_type,
        description=description,
        changes=changes,
        breaking_changes=breaking_changes,
        related_docs=related_docs,
        author=author,
        tags=tags
    )
    
    return success_response(
        data=log.model_dump(),
        message="Changelog created successfully"
    )


@router.get("/{log_id}/content")
async def get_changelog_content(log_id: str):
    log = changelog_manager.get_log(log_id)
    
    if not log:
        return error_response(
            code=ErrorCode.CHANGELOG_NOT_FOUND,
            message=f"Changelog not found: {log_id}"
        )
    
    markdown_content = log.to_markdown()
    
    return success_response(
        data={"content": markdown_content, "format": "markdown"},
        message="Changelog content retrieved"
    )
