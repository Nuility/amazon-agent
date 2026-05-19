from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List

from ..domain.enums import MessageRole
from ..infrastructure.storage_adapter import MemoryStorageAdapter
from ..services.dialog_service import DialogManager, StreamingResponder
from ..services.intent_service import IntentParser
from ..api.response import success_response, error_response, ErrorCode

router = APIRouter(prefix="/api/v1/dialog", tags=["Dialog"])

storage = MemoryStorageAdapter()
dialog_manager = DialogManager(storage)
intent_parser = IntentParser()


@router.post("/sessions")
async def create_session(request: Dict[str, Any]):
    user_id = request.get("user_id", "anonymous")
    
    session = await dialog_manager.create_session(user_id)
    
    return success_response(
        data=session.model_dump(),
        message="Session created successfully"
    )


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    session = await dialog_manager.get_session(session_id)
    
    if not session:
        return error_response(
            code=ErrorCode.SESSION_NOT_FOUND,
            message=f"Session not found: {session_id}"
        )
    
    return success_response(data=session.model_dump())


@router.delete("/sessions/{session_id}")
async def close_session(session_id: str):
    success = await dialog_manager.close_session(session_id)
    
    if not success:
        return error_response(
            code=ErrorCode.SESSION_NOT_FOUND,
            message=f"Session not found: {session_id}"
        )
    
    return success_response(message="Session closed successfully")


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str, limit: int = 20):
    messages = await dialog_manager.get_history(session_id, limit)
    
    return success_response(
        data=[msg.model_dump() for msg in messages],
        message=f"Retrieved {len(messages)} messages"
    )


@router.post("/sessions/{session_id}/messages")
async def send_message(session_id: str, request: Dict[str, Any]):
    content = request.get("content", "")
    
    if not content:
        return error_response(
            code=ErrorCode.INVALID_REQUEST,
            message="Message content is required"
        )
    
    try:
        intent_result = await intent_parser.parse(content)
        
        user_message = await dialog_manager.add_message(
            session_id,
            MessageRole.USER,
            content,
            intent=intent_result.intent,
            entities=intent_result.entities
        )
        
        response_content = f"收到您的消息。识别意图: {intent_result.intent}"
        if intent_result.clarifications:
            response_content += f"\n需要澄清: {', '.join(intent_result.clarifications)}"
        
        assistant_message = await dialog_manager.add_message(
            session_id,
            MessageRole.ASSISTANT,
            response_content
        )
        
        return success_response(
            data={
                "user_message": user_message.model_dump(),
                "assistant_message": assistant_message.model_dump(),
                "intent": intent_result.model_dump()
            },
            message="Message processed"
        )
    
    except ValueError as e:
        return error_response(
            code=ErrorCode.SESSION_NOT_FOUND,
            message=str(e)
        )


@router.websocket("/ws/{session_id}")
async def websocket_dialog(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    responder = StreamingResponder()
    
    try:
        session = await dialog_manager.get_session(session_id)
        if not session:
            await websocket.send_json(error_response(
                code=ErrorCode.SESSION_NOT_FOUND,
                message="Session not found"
            ))
            await websocket.close()
            return
        
        while True:
            data = await websocket.receive_json()
            content = data.get("content", "")
            
            if not content:
                continue
            
            intent_result = await intent_parser.parse(content)
            
            await dialog_manager.add_message(
                session_id,
                MessageRole.USER,
                content,
                intent=intent_result.intent
            )
            
            response = f"处理中... 识别意图: {intent_result.intent}"
            
            async def send_chunk(chunk_data):
                await websocket.send_json(chunk_data)
            
            await responder.stream(response, send_chunk)
            
            await dialog_manager.add_message(
                session_id,
                MessageRole.ASSISTANT,
                response
            )
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json(error_response(
            code=ErrorCode.INTERNAL_ERROR,
            message=str(e)
        ))
