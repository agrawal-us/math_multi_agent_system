from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.orchestration_service import process_chat_message

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(payload: ChatMessageRequest) -> ChatMessageResponse:
    if not payload.message.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty.")

    workflow_output = process_chat_message(payload.message)
    response_type = workflow_output.get("type", "error")
    data = workflow_output.get("data", {})

    if response_type == "solve":
        result = data.get("result")
        steps = data.get("steps", [])
        steps_text = "\n".join(str(step) for step in steps if step)
        content = f"Result: {result}"
        if steps_text:
            content = f"{content}\nSteps:\n{steps_text}"
    elif response_type == "concept":
        content = str(data.get("explanation") or "No response")
    elif response_type == "quiz":
        quiz_items = data.get("quiz", [])
        content = f"Quiz generated with {len(quiz_items)} question(s)."
    else:
        content = str(data.get("message") or "No response")

    return ChatMessageResponse(
        session_id=payload.session_id or 0,
        response_type=response_type,
        content=content,
        metadata=workflow_output.get("metadata", {}),
    )


@router.get("/sessions")
def list_sessions() -> dict:
    return {"items": [], "todo": "Implement session persistence"}
