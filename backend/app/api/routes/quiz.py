from fastapi import APIRouter, HTTPException, status

from app.schemas.quiz import (
    QuizGenerateRequest,
    QuizGenerateResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
)

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizGenerateResponse)
def generate_quiz(payload: QuizGenerateRequest) -> QuizGenerateResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Quiz generation scaffold only for topic={payload.topic}",
    )


@router.post("/submit", response_model=QuizSubmitResponse)
def submit_quiz(payload: QuizSubmitRequest) -> QuizSubmitResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Quiz submit scaffold only for quiz_id={payload.quiz_id}",
    )
