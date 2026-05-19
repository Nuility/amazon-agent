from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any

from ..services.skill_service import SkillRegistry, SkillExecutor, create_default_skills
from ..api.response import success_response, error_response, ErrorCode

router = APIRouter(prefix="/api/v1/skills", tags=["Skills"])

registry = SkillRegistry()
executor = SkillExecutor(registry)

for skill in create_default_skills():
    registry.register(skill)


@router.get("")
async def list_skills(
    status: Optional[str] = Query(None, description="Filter by status")
):
    from ..domain.enums import SkillStatus
    
    status_filter = SkillStatus(status) if status else None
    skills = registry.list_all(status_filter)
    
    return success_response(
        data=[skill.model_dump() for skill in skills],
        message=f"Found {len(skills)} skills"
    )


@router.get("/{skill_id}")
async def get_skill(skill_id: str):
    skill = registry.get(skill_id)
    
    if not skill:
        return error_response(
            code=ErrorCode.SKILL_NOT_FOUND,
            message=f"Skill not found: {skill_id}"
        )
    
    return success_response(data=skill.model_dump())


@router.post("/search")
async def search_skills(request: Dict[str, Any]):
    tags = request.get("tags", [])
    name = request.get("name", "")
    
    results = []
    
    if tags:
        results = registry.search_by_tags(tags)
    elif name:
        results = registry.search_by_name(name)
    else:
        results = registry.list_all()
    
    return success_response(
        data=[skill.model_dump() for skill in results],
        message=f"Found {len(results)} matching skills"
    )


@router.get("/{skill_id}/help")
async def get_skill_help(skill_id: str):
    skill = registry.get(skill_id)
    
    if not skill:
        return error_response(
            code=ErrorCode.SKILL_NOT_FOUND,
            message=f"Skill not found: {skill_id}"
        )
    
    help_text = skill.get_help()
    
    return success_response(
        data={"help": help_text},
        message="Skill help generated"
    )


@router.post("/{skill_id}/execute")
async def execute_skill(skill_id: str, params: Dict[str, Any]):
    result = await executor.execute_skill(skill_id, params)
    
    return success_response(
        data=result.model_dump(),
        message=result.message
    )
