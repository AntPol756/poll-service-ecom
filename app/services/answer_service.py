from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.clients.user_client import UserClient
from app.models import Answer
from app.repositories.answer_repository import AnswerRepository
from app.repositories.question_repository import QuestionRepository
from app.schemas import AnswerCreate, AnswerUpdate


class AnswerService:
    def __init__(self, db: Session):
        self.answer_repository = AnswerRepository(db)
        self.question_repository = QuestionRepository(db)
        self.user_client = UserClient()

    def get_answer(self, answer_id: int) -> Answer:
        answer = self.answer_repository.get_by_id(answer_id)
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
            )
        return answer

    def answer_question(self, answer_data: AnswerCreate) -> Answer:
        # cheap local check first, then the network call to the User Service
        if not self.question_repository.get_by_id(answer_data.question_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
        self.user_client.ensure_registered(answer_data.user_id)

        if self.answer_repository.get_by_user_and_question(
            answer_data.user_id, answer_data.question_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already answered this question - use PUT /answers/{answer_id} to change it",
            )
        try:
            return self.answer_repository.create(answer_data)
        except IntegrityError:
            # two requests at the same time: the UNIQUE constraint catches it
            self.answer_repository.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already answered this question",
            )

    def update_answer(self, answer_id: int, answer_data: AnswerUpdate) -> Answer:
        answer = self.get_answer(answer_id)
        self.user_client.ensure_registered(answer.user_id)
        return self.answer_repository.update_option(answer, answer_data.selected_option)

    def delete_answer(self, answer_id: int) -> None:
        answer = self.get_answer(answer_id)
        self.answer_repository.delete(answer)

    def delete_user_answers(self, user_id: int) -> int:
        """Called by the User Service when a user is deleted."""
        return self.answer_repository.delete_by_user(user_id)
