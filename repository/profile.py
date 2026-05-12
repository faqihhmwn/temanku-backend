from sqlalchemy.orm import Session
from tables.users import Users
from jose import jwt
from config import SECRET_KEY, ALGORITHM
from pydantic import BaseModel
from passlib.context import CryptContext

# def get_profile_by_token(db: Session, token: str):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     username = payload.get("sub")

#     user = db.query(user).filter(user.username == username).first()

#     return user

def get_profile(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        return {"message": "User not found"}

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.create_date,
        "updated_at": user.update_date
    }

def update_profile(db, user_id: int, data):
    user = db.query(Users).filter(Users.id == user_id).first()
    
    if not user:
        return None

    if data.username is not None:
        user.username = data.username
    if data.email is not None:
        user.email = data.email
    if data.phone_number is not None:
        user.phone_number = data.phone_number
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name

    db.commit()
    db.refresh(user)

    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def change_password(db, user_id: int, current_password: str, new_password: str):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        return None

    # cek password lama
    if not pwd_context.verify(current_password, user.password):
        return "wrong_password"

    # hash password baru
    user.password = pwd_context.hash(new_password)

    db.commit()
    db.refresh(user)

    return user