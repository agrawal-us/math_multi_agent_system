from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Login scaffold only. Received {payload.email}.",
    )


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest) -> TokenResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Register scaffold only. Received {payload.email}.",
    )


@router.get("/me")
def me() -> dict:
    return {
        "id": "scaffold-user",
        "email": "scaffold@example.com",
        "authenticated": False,
        "todo": "Implement authenticated user lookup.",
    }
