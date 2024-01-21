from sqlalchemy.orm import Session
import models, schemas
from crypto.encrypt import generate_password_hash
from fastapi import HTTPException

def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def get_users(db: Session):
    return db.query(models.Users).all()

def create_user(db: Session, user: schemas.UserCreate, role_name: str):
    hashed_password = generate_password_hash(user.password)
    new_user = models.Users(username=user.username, email=user.email, hashed_password=hashed_password)
    role = db.query(models.Roles).filter(models.Roles.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found")
    new_user.roles.append(role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.email is not None:
        user.email = user.email
    if user.password is not None:
        user.hashed_password = generate_password_hash(user.password)
    if user.is_active is not None:
        user.is_active = user.is_active
 
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    db.delete(user)
    db.commit()
    return user
