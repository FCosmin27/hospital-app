import secrets
SECRET_KEY = secrets.token_urlsafe(32)
MARIADB_HOSPITAL_ROOT_PASSWORD = 123456789
DATABASE_URL = f"mysql+pymysql://root:{MARIADB_HOSPITAL_ROOT_PASSWORD}@mariadb_hospital/hospital_db"
ACCESS_TOKEN_EXPIRE_MINUTES = 30