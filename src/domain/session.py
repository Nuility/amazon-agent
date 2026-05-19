import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

from .enums import MessageRole, SessionStatus


class Message(BaseModel):
    message_id: str = Field(..., min_length=1, max_length=100, description="消息ID")
    session_id: str = Field(..., min_length=1, max_length=100, description="会话ID")
    role: MessageRole = Field(..., description="消息角色")
    content: str = Field(..., min_length=1, max_length=10000, description="消息内容")
    intent: Optional[str] = Field(default=None, description="识别的意图")
    entities: Dict[str, Any] = Field(default_factory=dict, description="提取的实体")
    timestamp: datetime = Field(default_factory=datetime.now, description="消息时间戳")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError('消息内容不能为空')
        return v


class Session(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100, description="会话ID")
    user_id: str = Field(..., min_length=1, max_length=100, description="用户ID")
    status: SessionStatus = Field(default=SessionStatus.ACTIVE, description="会话状态")
    messages: List[Message] = Field(default_factory=list, description="消息列表")
    context: Dict[str, Any] = Field(default_factory=dict, description="上下文数据")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    expires_at: Optional[datetime] = Field(default=None, description="过期时间")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    def add_message(self, message: Message) -> None:
        if message.session_id != self.session_id:
            raise ValueError('消息的session_id与会话不匹配')
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def get_context(self, limit: Optional[int] = None) -> List[Message]:
        messages = self.messages
        if limit is not None:
            messages = messages[-limit:]
        return messages
    
    def clear_messages(self) -> None:
        self.messages.clear()
        self.updated_at = datetime.now()
    
    def archive(self) -> None:
        self.status = SessionStatus.ARCHIVED
        self.updated_at = datetime.now()
    
    def expire(self) -> None:
        self.status = SessionStatus.EXPIRED
        self.updated_at = datetime.now()


class IntentResult(BaseModel):
    intent: str = Field(..., min_length=1, description="识别的意图")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")
    entities: Dict[str, Any] = Field(default_factory=dict, description="提取的实体")
    suggested_action: Optional[str] = Field(default=None, description="建议的操作")
    clarifications: List[str] = Field(default_factory=list, description="澄清问题列表")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
