from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ---------- Questions ----------

class QuestionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    option_1: str = Field(..., min_length=1, max_length=255)
    option_2: str = Field(..., min_length=1, max_length=255)
    option_3: str = Field(..., min_length=1, max_length=255)
    option_4: str = Field(..., min_length=1, max_length=255)


class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    option_1: Optional[str] = Field(None, min_length=1, max_length=255)
    option_2: Optional[str] = Field(None, min_length=1, max_length=255)
    option_3: Optional[str] = Field(None, min_length=1, max_length=255)
    option_4: Optional[str] = Field(None, min_length=1, max_length=255)


class QuestionResponse(BaseModel):
    id: int
    title: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Answers ----------

class AnswerCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    question_id: int = Field(..., gt=0)
    selected_option: int = Field(..., ge=1, le=4)


class AnswerUpdate(BaseModel):
    selected_option: int = Field(..., ge=1, le=4)


class AnswerResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    question_title: str
    selected_option: int
    selected_text: str
    answered_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeletedAnswersResponse(BaseModel):
    user_id: int
    deleted_answers: int


# ---------- Statistics ----------

class OptionCount(BaseModel):
    option: int
    text: str
    count: int


class QuestionStats(BaseModel):
    question_id: int
    title: str
    total_answers: int
    options: List[OptionCount]


class QuestionTotal(BaseModel):
    question_id: int
    total_answers: int


class UserAnswer(BaseModel):
    answer_id: int
    question_id: int
    question_title: str
    selected_option: int
    selected_text: str
    answered_at: datetime


class UserAnswers(BaseModel):
    user_id: int
    answers: List[UserAnswer]


class UserTotal(BaseModel):
    user_id: int
    total_answered: int
