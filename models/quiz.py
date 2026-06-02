from pydantic import BaseModel, ConfigDict
from typing import Optional


class QuizResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    category: str

    image_url: Optional[str] = None

    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None

    answer: str

    model_config = ConfigDict(
        from_attributes=True
    )