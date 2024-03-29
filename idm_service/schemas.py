from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class Link(BaseModel):
    href: str
    rel: str

class RoleName(str, Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"

class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    email : str

class User(UserBase):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True
        
class UserWithLinks(User):
    links : List[Link] = []
    
class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class RoleBase(BaseModel):
    name: RoleName

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

class UserRole(BaseModel):
    user_id: int
    role_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str