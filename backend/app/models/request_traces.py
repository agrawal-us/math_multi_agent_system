from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RequestTrace(Base):
    __tablename__ = "request_traces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    request_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    session_id: Mapped[int | None] = mapped_column(ForeignKey("chat_sessions.id"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    trace_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
