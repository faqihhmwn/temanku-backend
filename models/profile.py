from pydantic import BaseModel, ConfigDict
from typing import Optional 


class ProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)

    
class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password:str
    new_password:str