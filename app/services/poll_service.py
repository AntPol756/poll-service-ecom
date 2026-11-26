import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate

class PollService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

# QuestionService.update_question
   # question = self.get_question(question_id)
   # if self.answer_repository.count_by_question(question_id) > 0:
    #    raise HTTPException(status.HTTP_409_CONFLICT,
    #                    "Question already has answers - delete them before updating")
  #  return self.question_repository.update(question, data)

# AnswerService.answer_question
def answer_question(self, data: AnswerCreate) -> Answer:
    if not self.question_repository.get_by_id(data.question_id):     # cheap local check first
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Question not found")
    self.user_client.ensure_registered(data.user_id)                 # then the network call
    if self.answer_repository.get_by_user_and_question(data.user_id, data.question_id):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "Already answered - use PUT /answers/{id} to change it")
    return self.answer_repository.create(data)

# StatsService
def option_counts(self, question_id: int) -> dict:
    question = self.question_service.get_question(question_id)   # 404 if missing
    counts = self.answer_repository.count_per_option(question_id)
    return {
        "question_id": question.id,
        "title": question.title,
        "options": [
            {"option": i, "text": getattr(question, f"option_{i}"), "count": counts.get(i, 0)}
            for i in range(1, 5)
        ],
    }