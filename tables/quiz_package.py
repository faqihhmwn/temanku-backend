from sqlalchemy import Column, Integer, String, DateTime
from config import Base
import datetime


class QuizPackage(Base):
    __tablename__ = "quiz_packages"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    difficulty = Column(String(50), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.datetime.now
    )

    updated_at = Column(
        DateTime,
        nullable=True
    )