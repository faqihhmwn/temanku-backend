from sqlalchemy import Column, Integer, String, DateTime
from config import Base
import datetime


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)

    question_text = Column(String(255), nullable=False)
    question_type = Column(String(50), nullable=False)  # multiple_choice / image / gesture
    category = Column(String(100), nullable=False)

    image_url = Column(String(255), nullable=True)

    option_a = Column(String(255), nullable=True)
    option_b = Column(String(255), nullable=True)
    option_c = Column(String(255), nullable=True)
    option_d = Column(String(255), nullable=True)

    answer = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=True)