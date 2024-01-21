from client import IDMClient
from fastapi import FastAPI, HTTPException, Body, status
import schemas

app = FastAPI()
grpc_client = IDMClient()

@app.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest):
    response = grpc_client.login(request.username, request.password)
    if not response.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return schemas.LoginResponse(token=response.token)

@app.post("/register", response_model=schemas.RegisterResponse)
def register(request: schemas.RegisterRequest):
    response = grpc_client.register(request.username, request.email, request.password)
    return schemas.RegisterResponse(id=response.id)

@app.get("/user/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int):
    response = grpc_client.get_user(user_id)
    if not response.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_response = schemas.UserResponse(
        id=response.id,
        username=response.username,
        email=response.email,
        is_active=response.is_active,
        role=response.role
    )
    return user_response

@app.put("/user/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, request: schemas.UpdateUserRequest):
    response = grpc_client.update_user(user_id, request.email, request.password, request.is_active)
    if not response.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_response = schemas.UserResponse(
        id=response.id,
        username=response.username,
        email=response.email,
        is_active=response.is_active,
        role=response.role
    )
    return user_response

@app.delete("/user/{user_id}", response_model=schemas.DeleteUserResponse)
def delete_user(user_id: int):
    response = grpc_client.delete_user(user_id)
    return schemas.DeleteUserResponse(message=response.message)