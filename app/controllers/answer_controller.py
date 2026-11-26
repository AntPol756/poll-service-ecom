from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AnswerCreate, AnswerResponse, AnswerUpdate, DeletedAnswersResponse
from app.services.answer_service import AnswerService

router = APIRouter(prefix="/answers", tags=["Answers"])


@router.post("", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
def answer_question(answer_data: AnswerCreate, db: Session = Depends(get_db)):
    return AnswerService(db).answer_question(answer_data)


@router.get("/{answer_id}", response_model=AnswerResponse)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    return AnswerService(db).get_answer(answer_id)


@router.put("/{answer_id}", response_model=AnswerResponse)
def update_answer(answer_id: int, answer_data: AnswerUpdate, db: Session = Depends(get_db)):
    return AnswerService(db).update_answer(answer_id, answer_data)


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    AnswerService(db).delete_answer(answer_id)
    return None


# internal endpoint - called by the User Service when a user is deleted
@router.delete("/user/{user_id}", response_model=DeletedAnswersResponse)
def delete_user_answers(user_id: int, db: Session = Depends(get_db)):
    deleted = AnswerService(db).delete_user_answers(user_id)
    return DeletedAnswersResponse(user_id=user_id, deleted_answers=deleted)
