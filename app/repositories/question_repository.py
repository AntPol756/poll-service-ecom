from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Question
from app.schemas import QuestionCreate, QuestionUpdate


class QuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, question_id: int) -> Optional[Question]:
        return self.db.query(Question).filter(Question.id == question_id).first()

    def get_all(self) -> List[Question]:
        return self.db.query(Question).order_by(Question.id).all()

    def create(self, question_data: QuestionCreate) -> Question:
        db_question = Question(**question_data.model_dump())
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question

    def update(self, question: Question, question_data: QuestionUpdate) -> Question:
        update_fields = question_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(question, field, value)
        self.db.commit()
        self.db.refresh(question)
        return question

    def delete(self, question: Question) -> None:
        self.db.delete(question)  # answers are removed by the cascade
        self.db.commit()
