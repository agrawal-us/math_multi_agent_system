from fastapi import APIRouter

from app.schemas.traces import TraceDetailResponse, TraceSummary

router = APIRouter(prefix="/traces", tags=["traces"])


@router.get("/", response_model=list[TraceSummary])
def list_traces() -> list[TraceSummary]:
    return []


@router.get("/{request_id}", response_model=TraceDetailResponse)
def get_trace(request_id: str) -> TraceDetailResponse:
    return TraceDetailResponse(request_id=request_id, status="pending", trace={"todo": "Persist traces"})
