from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL
from crypto.encrypt import generate_password_hash
import models

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def delete_tables():
    inspector = inspect(engine)

    if inspector.has_table('user_roles'):
        models.user_roles.drop(engine)

    if inspector.has_table('users'):
        models.Users.__table__.drop(engine)
    
    if inspector.has_table('roles'):
        models.Roles.__table__.drop(engine)

def insert_roles_into_table():
    roles_to_insert = ['admin', 'doctor', 'patient']
    
    with SessionLocal() as db:
        existing_roles = db.query(models.Roles).all()
        existing_roles_names = [role.name for role in existing_roles]
        
        for role in roles_to_insert:
            if role not in existing_roles_names:
                db.add(models.Roles(name=role))
                
        db.commit()
        db.close()
        
def insert_admin_user():
    admin_username = "admin"
    admin_email = "admin@admin.com"
    admin_password = "admin"
    
    with SessionLocal() as db:
        existing_admin = db.query(models.Users).filter(models.Users.username == admin_username).first()
        if not existing_admin:
            hashed_password = generate_password_hash(admin_password)
            admin_role = db.query(models.Roles).filter(models.Roles.name == "admin").first()
            admin_user = models.Users(username=admin_username, email=admin_email, hashed_password=hashed_password, is_active=True)
            admin_user.roles.append(admin_role)
            db.add(admin_user)
            db.commit()
            db.close()