from pydantic import BaseModel
from typing import Optional


class CreateQuizPackage(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty: str


class UpdateQuizPackage(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None


class CreateQuizQuestion(BaseModel):
    package_id: int

    question_text: str
    answer: str

    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None


class UpdateQuizQuestion(BaseModel):
    question_text: Optional[str] = None
    answer: Optional[str] = None

    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None