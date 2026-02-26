from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.words import router as words_router
from core.config import settings
from services.ai_service import AIService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ai_service = AIService(credentials=settings.AI_CREDENTIALS)
    yield
    app.state.ai_service = None


app = FastAPI(lifespan=lifespan)

app.include_router(words_router)


def get_ai_service() -> AIService:
    return app.state.ai_service
