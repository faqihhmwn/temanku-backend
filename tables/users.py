from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config import Base
import datetime

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255), unique=True)
    phone_number = Column(String(50))

    first_name = Column(String(255))
    last_name = Column(String(255))

    profile_image_url = Column(String(500), nullable=True)

    role = Column(String(50), default="user")
    create_date = Column(DateTime, default=datetime.datetime.now)
    update_date = Column(DateTime)