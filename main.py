from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.controllers.answer_controller import router as answer_router
from app.controllers.question_controller import router as question_router
from app.controllers.stats_controller import router as stats_router
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(stats_router)
