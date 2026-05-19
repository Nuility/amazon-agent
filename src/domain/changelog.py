import re
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from .enums import UpdateType


class ChangeLog(BaseModel):
    log_id: str = Field(..., description="日志ID，格式YYMMDD.N")
    version: str = Field(..., description="版本号，格式vX.Y.Z")
    title: str = Field(..., min_length=5, max_length=100, description="更新标题")
    update_type: UpdateType = Field(..., description="更新类型")
    description: str = Field(..., min_length=10, max_length=2000, description="更新描述")
    changes: List[str] = Field(default_factory=list, description="变更项列表")
    breaking_changes: List[str] = Field(default_factory=list, description="破坏性变更列表")
    related_docs: List[str] = Field(default_factory=list, description="相关文档列表")
    author: str = Field(default="System", description="作者")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    tags: List[str] = Field(default_factory=list, description="标签列表")
    
    @field_validator('log_id')
    @classmethod
    def validate_log_id(cls, v: str) -> str:
        if not re.match(r'^\d{6}\.\d+$', v):
            raise ValueError('log_id格式必须为YYMMDD.N，例如260519.1')
        return v
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        if not re.match(r'^v\d+\.\d+\.\d+$', v):
            raise ValueError('version格式必须为vX.Y.Z，例如v2.2.0')
        return v
    
    def to_markdown(self) -> str:
        md_content = f"# {self.title}\n\n"
        md_content += f"**版本**: {self.version}\n"
        md_content += f"**日期**: {self.created_at.strftime('%Y-%m-%d')}\n"
        md_content += f"**类型**: {self.update_type.value}\n"
        md_content += f"**作者**: {self.author}\n\n"
        
        md_content += f"## 更新说明\n\n{self.description}\n\n"
        
        if self.changes:
            md_content += "## 变更详情\n\n"
            for change in self.changes:
                md_content += f"- {change}\n"
            md_content += "\n"
        
        if self.breaking_changes:
            md_content += "## ⚠️ 破坏性变更\n\n"
            for change in self.breaking_changes:
                md_content += f"- {change}\n"
            md_content += "\n"
        
        if self.related_docs:
            md_content += "## 相关文档\n\n"
            for doc in self.related_docs:
                md_content += f"- {doc}\n"
            md_content += "\n"
        
        if self.tags:
            md_content += f"## 标签\n\n{', '.join(self.tags)}\n"
        
        return md_content
