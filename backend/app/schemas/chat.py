from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    session_id: int | None = None
    message: str


class ChatMessageResponse(BaseModel):
    session_id: int
    response_type: str
    content: str
    metadata: dict


class ChatSessionSummary(BaseModel):
    id: int
    title: str | None = None
