from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    
class GetUserRequest(BaseModel):
    id: int
    
class UpdateUserRequest(BaseModel):
    email: str = None
    password: str = None
    is_active: bool = None
    
class DeleteUserRequest(BaseModel):
    id: int
    
class LoginResponse(BaseModel):
    token: str
    
class RegisterResponse(BaseModel):
    id: int
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

class DeleteUserResponse(BaseModel):
    message: str