from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import QuestionCreate, QuestionResponse, QuestionUpdate
from app.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question_data: QuestionCreate, db: Session = Depends(get_db)):
    return QuestionService(db).create_question(question_data)


@router.get("", response_model=List[QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return QuestionService(db).get_all_questions()


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    return QuestionService(db).get_question(question_id)


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int, question_data: QuestionUpdate, db: Session = Depends(get_db)
):
    return QuestionService(db).update_question(question_id, question_data)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    QuestionService(db).delete_question(question_id)
    return None
