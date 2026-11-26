from typing import Dict, List

from sqlalchemy.orm import Session

from app.models import Question
from app.repositories.answer_repository import AnswerRepository
from app.schemas import (
    OptionCount,
    QuestionStats,
    QuestionTotal,
    UserAnswer,
    UserAnswers,
    UserTotal,
)
from app.services.question_service import QuestionService


class StatsService:
    def __init__(self, db: Session):
        self.answer_repository = AnswerRepository(db)
        self.question_service = QuestionService(db)

    @staticmethod
    def _build_question_stats(question: Question, counts: Dict[int, int]) -> QuestionStats:
        # options nobody picked are missing from GROUP BY, so default to 0
        options = [
            OptionCount(option=i, text=question.option_text(i), count=counts.get(i, 0))
            for i in range(1, 5)
        ]
        return QuestionStats(
            question_id=question.id,
            title=question.title,
            total_answers=sum(option.count for option in options),
            options=options,
        )

    def question_option_counts(self, question_id: int) -> QuestionStats:
        question = self.question_service.get_question(question_id)  # 404 if missing
        counts = self.answer_repository.count_per_option(question_id)
        return self._build_question_stats(question, counts)

    def question_total(self, question_id: int) -> QuestionTotal:
        self.question_service.get_question(question_id)
        return QuestionTotal(
            question_id=question_id,
            total_answers=self.answer_repository.count_by_question(question_id),
        )

    def user_answers(self, user_id: int) -> UserAnswers:
        answers = self.answer_repository.get_by_user(user_id)
        return UserAnswers(
            user_id=user_id,
            answers=[
                UserAnswer(
                    answer_id=answer.id,
                    question_id=answer.question_id,
                    question_title=answer.question.title,
                    selected_option=answer.selected_option,
                    selected_text=answer.question.option_text(answer.selected_option),
                    answered_at=answer.answered_at,
                )
                for answer in answers
            ],
        )

    def user_total(self, user_id: int) -> UserTotal:
        return UserTotal(
            user_id=user_id,
            total_answered=self.answer_repository.count_by_user(user_id),
        )

    def all_questions_stats(self) -> List[QuestionStats]:
        questions = self.question_service.get_all_questions()
        all_counts = self.answer_repository.count_per_option_all()  # one query, not N
        return [
            self._build_question_stats(
                question,
                {option: all_counts.get((question.id, option), 0) for option in range(1, 5)},
            )
            for question in questions
        ]
