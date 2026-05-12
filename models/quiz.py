from typing import Optional
from pydantic import BaseModel


class CreateQuizQuestion(BaseModel):
    question_text: str
    question_type: str
    category: str
    answer: str

    image_url: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None


class UpdateQuizQuestion(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    category: Optional[str] = None
    answer: Optional[str] = None

    image_url: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None