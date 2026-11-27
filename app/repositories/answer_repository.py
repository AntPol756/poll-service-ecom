from typing import Dict, List, Optional, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.models import Answer
from app.schemas import AnswerCreate

class AnswerRepository:
    def __init__(self, db: Session):
        self.db = db


    def get_by_id(self, answer_id: int) -> Optional[Answer]:
        return self.db.query(Answer).filter(Answer.id == answer_id).first()

    def get_by_user_and_question(self, user_id: int, question_id: int) -> Optional[Answer]:
        return (
            self.db.query(Answer)
            .filter(Answer.user_id == user_id, Answer.question_id == question_id)
            .first()
        )

    def create(self, answer_data: AnswerCreate) -> Answer:
        db_answer = Answer(**answer_data.model_dump())
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        return db_answer

    def update_option(self, answer: Answer, selected_option: int) -> Answer:
        answer.selected_option = selected_option
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def delete(self, answer: Answer) -> None:
        self.db.delete(answer)
        self.db.commit()

    def delete_by_user(self, user_id: int) -> int:
        deleted = self.db.query(Answer).filter(Answer.user_id == user_id).delete()
        self.db.commit()
        return deleted

    def rollback(self) -> None:
        self.db.rollback()


    def count_by_question(self, question_id: int) -> int:
        return self.db.query(Answer).filter(Answer.question_id == question_id).count()

    def count_by_user(self, user_id: int) -> int:
        return self.db.query(Answer).filter(Answer.user_id == user_id).count()

    def get_by_user(self, user_id: int) -> List[Answer]:
        return (
            self.db.query(Answer)
            .options(joinedload(Answer.question))
            .filter(Answer.user_id == user_id)
            .order_by(Answer.question_id)
            .all()
        )

    def count_per_option(self, question_id: int) -> Dict[int, int]:
        rows = (
            self.db.query(Answer.selected_option, func.count(Answer.id))
            .filter(Answer.question_id == question_id)
            .group_by(Answer.selected_option)
            .all()
        )
        return {option: count for option, count in rows}

    def count_per_option_all(self) -> Dict[Tuple[int, int], int]:

        rows = (
            self.db.query(Answer.question_id, Answer.selected_option, func.count(Answer.id))
            .group_by(Answer.question_id, Answer.selected_option)
            .all()
        )
        return {(question_id, option): count for question_id, option, count in rows}
