from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import Question
from app.repositories.answer_repository import AnswerRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas import QuestionCreate, QuestionUpdate

class QuestionService:
    def __init__(self, db: Session):
        self.question_repository = QuestionRepository(db)
        self.answer_repository = AnswerRepository(db)

    def get_question(self, question_id: int) -> Question:
        question = self.question_repository.get_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        return question

    def get_all_questions(self) -> List[Question]:
        return self.question_repository.get_all()

    def create_question(self, question_data: QuestionCreate) -> Question:
        return self.question_repository.create(question_data)

    def update_question(self, question_id: int, question_data: QuestionUpdate) -> Question:
        question = self.get_question(question_id)
        if self.answer_repository.count_by_question(question_id) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Question already has answers - delete them before updating",
            )
        return self.question_repository.update(question, question_data)

    def delete_question(self, question_id: int) -> None:
        question = self.get_question(question_id)
        self.question_repository.delete(question)
