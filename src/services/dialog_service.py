import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from ..domain.session import Session, Message, IntentResult
from ..domain.enums import MessageRole, SessionStatus
from ..infrastructure.storage_adapter import StorageAdapter
from ..infrastructure.logger import get_logger


class DialogManager:
    def __init__(
        self,
        storage: StorageAdapter,
        session_timeout_minutes: int = 30
    ):
        self.storage = storage
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self.logger = get_logger("dialog_manager")
    
    async def create_session(self, user_id: str) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id,
            user_id=user_id,
            status=SessionStatus.ACTIVE,
            expires_at=datetime.now() + self.session_timeout
        )
        
        await self._save_session(session)
        
        self.logger.info(
            operation="create_session",
            result="success",
            session_id=session_id,
            user_id=user_id
        )
        
        return session
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        session_data = await self.storage.read(f"session_{session_id}")
        
        if not session_data:
            return None
        
        session = Session(**session_data)
        
        if session.expires_at and datetime.now() > session.expires_at:
            await self.close_session(session_id)
            return None
        
        return session
    
    async def close_session(self, session_id: str) -> bool:
        session = await self.get_session(session_id)
        
        if not session:
            return False
        
        session.archive()
        await self._save_session(session)
        
        self.logger.info(
            operation="close_session",
            result="success",
            session_id=session_id
        )
        
        return True
    
    async def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
        intent: Optional[str] = None,
        entities: Optional[Dict[str, Any]] = None
    ) -> Message:
        session = await self.get_session(session_id)
        
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        message = Message(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            role=role,
            content=content,
            intent=intent,
            entities=entities or {}
        )
        
        session.add_message(message)
        session.expires_at = datetime.now() + self.session_timeout
        
        await self._save_session(session)
        
        self.logger.info(
            operation="add_message",
            result="success",
            session_id=session_id,
            message_id=message.message_id,
            role=role.value
        )
        
        return message
    
    async def get_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Message]:
        session = await self.get_session(session_id)
        
        if not session:
            return []
        
        return session.get_context(limit)
    
    async def clear_history(self, session_id: str) -> bool:
        session = await self.get_session(session_id)
        
        if not session:
            return False
        
        session.clear_messages()
        await self._save_session(session)
        
        return True
    
    async def _save_session(self, session: Session) -> None:
        await self.storage.write(
            f"session_{session.session_id}",
            session.model_dump()
        )


class ContextManager:
    def __init__(
        self,
        max_context_messages: int = 20,
        max_context_size_kb: int = 10
    ):
        self.max_messages = max_context_messages
        self.max_size_kb = max_context_size_kb
        self.logger = get_logger("context_manager")
    
    def get_relevant_context(
        self,
        session: Session,
        current_message: Optional[Message] = None
    ) -> List[Message]:
        messages = session.messages
        
        if len(messages) > self.max_messages:
            messages = messages[-self.max_messages:]
        
        total_size = sum(len(msg.content.encode('utf-8')) for msg in messages)
        max_size_bytes = self.max_size_kb * 1024
        
        while total_size > max_size_bytes and messages:
            removed_msg = messages.pop(0)
            total_size -= len(removed_msg.content.encode('utf-8'))
        
        return messages
    
    def truncate_if_needed(self, history: List[Message]) -> List[Message]:
        total_size = sum(len(msg.content.encode('utf-8')) for msg in history)
        max_size_bytes = self.max_size_kb * 1024
        
        while total_size > max_size_bytes and history:
            removed_msg = history.pop(0)
            total_size -= len(removed_msg.content.encode('utf-8'))
        
        return history


class StreamingResponder:
    def __init__(self, chunk_size: int = 100, interval_ms: int = 100):
        self.chunk_size = chunk_size
        self.interval_ms = interval_ms
        self.logger = get_logger("streaming_responder")
    
    async def stream(self, response: str, callback: callable):
        import asyncio
        
        chunks = [
            response[i:i+self.chunk_size]
            for i in range(0, len(response), self.chunk_size)
        ]
        
        for i, chunk in enumerate(chunks):
            await callback(self.format_chunk(chunk, i == len(chunks) - 1))
            await asyncio.sleep(self.interval_ms / 1000)
    
    def format_chunk(self, content: str, is_last: bool) -> Dict[str, Any]:
        return {
            "type": "complete" if is_last else "chunk",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
