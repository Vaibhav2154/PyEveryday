from pydantic import BaseModel
import uuid
from datetime import datetime
from sqlmodel import Field
class UserCreate(BaseModel):
    email: str
    username: str
    password: str = Field(min_length=8, max_length=15)
    
class User(BaseModel):
    uid: uuid.UUID
    email: str
    username: str
    hash_pwd : str = Field(exclude=True)
    is_verified : str
    created_on: datetime
    updated_on : datetime

class UserLogin(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=15)