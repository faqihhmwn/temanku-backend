from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field, EmailStr

T = TypeVar('T')

#login
class Login(BaseModel):
    email: str
    password: str

#register
class Register(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)

    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
#response model
class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None

# token
class tokenResponse(BaseModel):
    access_token: str
    token_type: str