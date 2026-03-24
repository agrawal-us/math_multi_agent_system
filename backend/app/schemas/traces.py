from pydantic import BaseModel


class TraceSummary(BaseModel):
    request_id: str
    status: str
    duration_ms: float | None = None


class TraceDetailResponse(BaseModel):
    request_id: str
    status: str
    trace: dict
