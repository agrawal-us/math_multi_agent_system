from pydantic import BaseModel


class QuizGenerateRequest(BaseModel):
    topic: str
    difficulty: str | None = None


class QuizGenerateResponse(BaseModel):
    quiz_id: str
    questions: list[dict]


class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: list[dict]


class QuizSubmitResponse(BaseModel):
    score: float
    feedback: str | None = None
