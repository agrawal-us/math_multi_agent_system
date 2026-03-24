from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.orchestration_service import process_chat_message

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(payload: ChatMessageRequest) -> ChatMessageResponse:
    if not payload.message.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty.")

    workflow_output = process_chat_message(payload.message)
    return ChatMessageResponse(
        session_id=payload.session_id or 0,
        response_type=workflow_output.get("type", "error"),
        content=workflow_output.get("data", {}).get("response")
        or workflow_output.get("data", {}).get("message", "No response"),
        metadata=workflow_output.get("metadata", {}),
    )


@router.get("/sessions")
def list_sessions() -> dict:
    return {"items": [], "todo": "Implement session persistence"}
