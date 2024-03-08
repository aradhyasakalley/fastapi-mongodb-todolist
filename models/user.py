from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    password: str
    email:str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
