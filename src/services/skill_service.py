import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from threading import Lock

from ..domain.skill import Skill, SkillExecutionResult, SkillParameter
from ..domain.enums import SkillStatus, ParameterType
from ..infrastructure.logger import get_logger


class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._lock = Lock()
        self.logger = get_logger("skill_registry")
    
    def register(self, skill: Skill) -> None:
        with self._lock:
            if skill.skill_id in self._skills:
                self.logger.warning(
                    operation="register",
                    result="skill_exists",
                    skill_id=skill.skill_id
                )
            self._skills[skill.skill_id] = skill
            self.logger.info(
                operation="register",
                result="success",
                skill_id=skill.skill_id,
                skill_name=skill.skill_name
            )
    
    def unregister(self, skill_id: str) -> bool:
        with self._lock:
            if skill_id in self._skills:
                del self._skills[skill_id]
                self.logger.info(
                    operation="unregister",
                    result="success",
                    skill_id=skill_id
                )
                return True
            return False
    
    def get(self, skill_id: str) -> Optional[Skill]:
        return self._skills.get(skill_id)
    
    def list_all(self, status: Optional[SkillStatus] = None) -> List[Skill]:
        skills = list(self._skills.values())
        if status:
            skills = [s for s in skills if s.status == status]
        return skills
    
    def search_by_tags(self, tags: List[str]) -> List[Skill]:
        matching_skills = []
        for skill in self._skills.values():
            if any(tag in skill.tags for tag in tags):
                matching_skills.append(skill)
        return matching_skills
    
    def search_by_name(self, name: str) -> List[Skill]:
        matching_skills = []
        for skill in self._skills.values():
            if name.lower() in skill.skill_name.lower():
                matching_skills.append(skill)
        return matching_skills


class SkillExecutor:
    def __init__(self, registry: SkillRegistry, timeout: int = 30):
        self.registry = registry
        self.timeout = timeout
        self.logger = get_logger("skill_executor")
    
    async def execute_skill(
        self,
        skill_id: str,
        params: Dict[str, Any],
        execution_func: Optional[callable] = None
    ) -> SkillExecutionResult:
        start_time = datetime.now()
        
        skill = self.registry.get(skill_id)
        if not skill:
            self.logger.error(
                operation="execute_skill",
                result="skill_not_found",
                skill_id=skill_id
            )
            return SkillExecutionResult(
                status="error",
                message=f"Skill not found: {skill_id}",
                execution_time_ms=0,
                skill_id=skill_id
            )
        
        if not skill.validate_params(params):
            self.logger.error(
                operation="execute_skill",
                result="validation_failed",
                skill_id=skill_id
            )
            return SkillExecutionResult(
                status="error",
                message="Parameter validation failed",
                execution_time_ms=0,
                skill_id=skill_id
            )
        
        try:
            if execution_func:
                result_data = await asyncio.wait_for(
                    execution_func(params),
                    timeout=self.timeout
                )
            else:
                result_data = await self._default_execution(skill, params)
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            self.logger.info(
                operation="execute_skill",
                result="success",
                skill_id=skill_id,
                execution_time_ms=execution_time
            )
            
            return SkillExecutionResult(
                status="success",
                data=result_data,
                message="Execution completed successfully",
                execution_time_ms=execution_time,
                skill_id=skill_id
            )
        
        except asyncio.TimeoutError:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(
                operation="execute_skill",
                result="timeout",
                skill_id=skill_id,
                timeout=self.timeout
            )
            return SkillExecutionResult(
                status="timeout",
                message=f"Execution timeout after {self.timeout} seconds",
                execution_time_ms=execution_time,
                skill_id=skill_id
            )
        
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(
                operation="execute_skill",
                result="error",
                skill_id=skill_id,
                error=str(e)
            )
            return SkillExecutionResult(
                status="error",
                message=f"Execution error: {str(e)}",
                execution_time_ms=execution_time,
                skill_id=skill_id
            )
    
    async def _default_execution(self, skill: Skill, params: Dict[str, Any]) -> Any:
        return {"skill": skill.skill_name, "params": params, "result": "mock_execution"}


def create_default_skills() -> List[Skill]:
    skills = []
    
    ad_analysis_skill = Skill(
        skill_id="ad_analysis",
        skill_name="广告分析",
        description="分析Amazon广告数据，计算关键指标如ACOS、ROAS、CTR等",
        parameters=[
            SkillParameter(
                name="campaign_ids",
                type=ParameterType.ARRAY,
                description="要分析的活动ID列表",
                required=True
            ),
            SkillParameter(
                name="date_range",
                type=ParameterType.OBJECT,
                description="日期范围 {start, end}",
                required=False
            )
        ],
        tags=["advertising", "analysis", "metrics"],
        status=SkillStatus.ACTIVE,
        examples=[
            {
                "description": "分析特定活动的表现",
                "params": {"campaign_ids": ["camp001", "camp002"]}
            }
        ]
    )
    skills.append(ad_analysis_skill)
    
    keyword_query_skill = Skill(
        skill_id="keyword_query",
        skill_name="关键词查询",
        description="查询关键词表现数据，包括排名、点击、转化等指标",
        parameters=[
            SkillParameter(
                name="keywords",
                type=ParameterType.ARRAY,
                description="关键词列表",
                required=True
            ),
            SkillParameter(
                name="match_type",
                type=ParameterType.STRING,
                description="匹配类型",
                required=False,
                enum=["exact", "phrase", "broad"]
            )
        ],
        tags=["advertising", "keyword", "query"],
        status=SkillStatus.ACTIVE
    )
    skills.append(keyword_query_skill)
    
    optimization_skill = Skill(
        skill_id="optimization_suggest",
        skill_name="优化建议生成",
        description="基于广告数据生成优化建议，包括竞价调整、关键词添加等",
        parameters=[
            SkillParameter(
                name="target_acos",
                type=ParameterType.FLOAT,
                description="目标ACOS值",
                required=False,
                default=25.0
            ),
            SkillParameter(
                name="analysis_scope",
                type=ParameterType.STRING,
                description="分析范围",
                required=False,
                enum=["all", "underperforming", "high_potential"]
            )
        ],
        tags=["advertising", "optimization", "recommendation"],
        status=SkillStatus.ACTIVE
    )
    skills.append(optimization_skill)
    
    return skills
