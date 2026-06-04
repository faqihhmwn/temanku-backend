from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from config import Base
import datetime


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)

    package_id = Column(
        Integer,
        ForeignKey("quiz_packages.id"),
        nullable=False
    )

    question_text = Column(String(255), nullable=False)

    image_url = Column(String(500), nullable=True)

    option_a = Column(String(255), nullable=True)
    option_b = Column(String(255), nullable=True)
    option_c = Column(String(255), nullable=True)
    option_d = Column(String(255), nullable=True)

    answer = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.datetime.now
    )

    updated_at = Column(
        DateTime,
        nullable=True
    )