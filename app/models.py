from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    option_1 = Column(String(255), nullable=False)
    option_2 = Column(String(255), nullable=False)
    option_3 = Column(String(255), nullable=False)
    option_4 = Column(String(255), nullable=False)

    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )

    def option_text(self, option_number: int) -> str:
        return getattr(self, f"option_{option_number}")


class Answer(Base):
    __tablename__ = "answers"
    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_user_question"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    selected_option = Column(Integer, nullable=False)  # 1..4
    answered_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    question = relationship("Question", back_populates="answers")

    @property
    def question_title(self) -> str:
        return self.question.title

    @property
    def selected_text(self) -> str:
        return self.question.option_text(self.selected_option)
