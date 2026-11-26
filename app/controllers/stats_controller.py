from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import QuestionStats, QuestionTotal, UserAnswers, UserTotal
from app.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/questions", response_model=List[QuestionStats])
def all_questions_stats(db: Session = Depends(get_db)):
    return StatsService(db).all_questions_stats()


@router.get("/questions/{question_id}/options", response_model=QuestionStats)
def question_option_counts(question_id: int, db: Session = Depends(get_db)):
    return StatsService(db).question_option_counts(question_id)


@router.get("/questions/{question_id}/total", response_model=QuestionTotal)
def question_total(question_id: int, db: Session = Depends(get_db)):
    return StatsService(db).question_total(question_id)


@router.get("/users/{user_id}/answers", response_model=UserAnswers)
def user_answers(user_id: int, db: Session = Depends(get_db)):
    return StatsService(db).user_answers(user_id)


@router.get("/users/{user_id}/total", response_model=UserTotal)
def user_total(user_id: int, db: Session = Depends(get_db)):
    return StatsService(db).user_total(user_id)
