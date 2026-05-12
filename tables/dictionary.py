from sqlalchemy import Column, Integer, String
from config import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True, index=True)
    letter = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)