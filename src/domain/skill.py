import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

from .enums import ParameterType, SkillStatus


class SkillParameter(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="参数名称")
    type: ParameterType = Field(..., description="参数类型")
    description: str = Field(..., min_length=1, max_length=200, description="参数描述")
    required: bool = Field(default=True, description="是否必填")
    default: Optional[Any] = Field(default=None, description="默认值")
    enum: Optional[List[Any]] = Field(default=None, description="枚举值列表")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', v):
            raise ValueError('参数名称只能包含字母、数字和下划线，且不能以数字开头')
        return v
    
    def validate_value(self, value: Any) -> bool:
        if value is None:
            return not self.required
        
        if self.enum and value not in self.enum:
            return False
        
        type_mapping = {
            ParameterType.STRING: str,
            ParameterType.INTEGER: int,
            ParameterType.FLOAT: (int, float),
            ParameterType.BOOLEAN: bool,
            ParameterType.OBJECT: dict,
            ParameterType.ARRAY: list,
        }
        
        expected_type = type_mapping.get(self.type)
        if expected_type:
            if not isinstance(value, expected_type):
                return False
        
        return True


class Skill(BaseModel):
    skill_id: str = Field(..., min_length=5, max_length=50, description="Skill唯一标识")
    skill_name: str = Field(..., min_length=2, max_length=100, description="Skill名称")
    description: str = Field(..., min_length=10, max_length=500, description="Skill描述")
    parameters: List[SkillParameter] = Field(default_factory=list, description="参数列表")
    tags: List[str] = Field(default_factory=list, description="标签列表")
    status: SkillStatus = Field(default=SkillStatus.ACTIVE, description="Skill状态")
    version: str = Field(default="1.0.0", description="Skill版本")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    examples: List[Dict[str, Any]] = Field(default_factory=list, description="使用示例")
    
    @field_validator('skill_id')
    @classmethod
    def validate_skill_id(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\-]*$', v):
            raise ValueError('skill_id只能包含字母、数字、下划线和连字符')
        return v
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        for param in self.parameters:
            if param.required and param.name not in params:
                return False
            if param.name in params:
                if not param.validate_value(params[param.name]):
                    return False
        return True
    
    def get_help(self) -> str:
        help_text = f"## {self.skill_name}\n\n{self.description}\n\n"
        help_text += "### 参数说明\n\n"
        
        if not self.parameters:
            help_text += "无参数\n\n"
        else:
            for param in self.parameters:
                required_mark = "**必填**" if param.required else "可选"
                help_text += f"- **{param.name}** ({param.type.value}) - {required_mark}: {param.description}\n"
                if param.default is not None:
                    help_text += f"  - 默认值: {param.default}\n"
                if param.enum:
                    help_text += f"  - 可选值: {', '.join(map(str, param.enum))}\n"
        
        if self.examples:
            help_text += "\n### 使用示例\n\n"
            for i, example in enumerate(self.examples, 1):
                help_text += f"{i}. {example.get('description', '示例')}\n"
                help_text += f"   ```json\n   {example.get('params', {})}\n   ```\n"
        
        return help_text


class SkillExecutionResult(BaseModel):
    status: str = Field(..., description="执行状态: success, error, timeout")
    data: Optional[Any] = Field(default=None, description="执行结果数据")
    message: str = Field(default="", description="执行消息")
    execution_time_ms: float = Field(..., ge=0, description="执行耗时(毫秒)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    skill_id: str = Field(..., description="执行的Skill ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="执行时间戳")
