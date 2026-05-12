# from fastapi import Depends, HTTPException, status
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from config import get_db
# from tables.users import Users
# from config import SECRET_KEY, ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: int = payload.get("user_id")

#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token error")

#     user = db.query(Users).filter(Users.id == user_id).first()

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     return user

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from config import get_db, SECRET_KEY, ALGORITHM
from tables.users import Users

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")

    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user