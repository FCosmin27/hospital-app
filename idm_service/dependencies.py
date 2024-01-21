from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from security import verify_token
from sqlalchemy.orm import Session
from database import get_db
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

def check_current_user_is_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token)
    db_user = db.query(models.User).filter(models.Users.id == current_user.id).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if any(role.name == 'admin' for role in db_user.roles):
        return db_user
    else:
        raise HTTPException(status_code=403, detail="Access denied")