from fastapi import FastAPI

from app.api.routes import auth, chat, quiz, traces
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
    app.include_router(chat.router, prefix=settings.API_V1_PREFIX)
    app.include_router(quiz.router, prefix=settings.API_V1_PREFIX)
    app.include_router(traces.router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
