from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from crypto.decrypt import check_password_hash
from crypto.encrypt import generate_password_hash

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return check_password_hash(plain_password, hashed_password)

def get_password_hash(password):
    return generate_password_hash(password)

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
