from sqlalchemy.orm import Session
import models, schemas
from crypto.encrypt import generate_password_hash
from crypto.decrypt import check_password_hash
from fastapi import HTTPException

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not user.is_active:
        return False
    if not check_password_hash(password, user.hashed_password):
        return False
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def get_users(db: Session):
    return db.query(models.Users).all()

def create_user(db: Session, user: schemas.UserCreate, role_name: str):
    existing_user = db.query(models.Users).filter(
        (models.Users.username == user.username) | 
        (models.Users.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_password = generate_password_hash(user.password)
    new_user = models.Users(username=user.username, email=user.email, hashed_password=hashed_password)
    role = db.query(models.Roles).filter(models.Roles.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found")
    new_user.role = role
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        db_user.hashed_password = generate_password_hash(user_update.password)
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    db.delete(user)
    db.commit()
    return user
