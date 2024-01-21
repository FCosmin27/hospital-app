from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL
from models import Appointments, Doctors, Patients

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

    if inspector.has_table('appointments'):
        Appointments.__table__.drop(engine)
    
    if inspector.has_table('doctors'):
        Doctors.__table__.drop(engine)
    
    if inspector.has_table('patients'):
        Patients.__table__.drop(engine)


def create_db_users():
    conn = engine.connect()

    conn.execute("CREATE USER 'admin'@'%' IDENTIFIED BY '123456789';")
    conn.execute("GRANT ALL PRIVILEGES ON hospital_db.* TO 'admin'@'%';")
    
    conn.execute("CREATE USER 'doctor'@'%' IDENTIFIED BY '123456789';")
    conn.execute("GRANT SELECT, UPDATE, INSERT ON hospital_db.appointments TO 'doctor'@'%';")
    conn.execute("GRANT DELETE ON hospital_db.patients TO 'doctor'@'%';")
    conn.execute("GRANT SELECT ON hospital_db.patients TO 'doctor'@'%';")
    
    conn.execute("CREATE USER 'patient'@'%' IDENTIFIED BY '123456789';")
    conn.execute("GRANT INSERT ON hospital_db.patients TO 'patient'@'%';")
    conn.execute("GRANT INSERT, UPDATE ON hospital_db.appointments TO 'patient'@'%';")
    conn.execute("GRANT SELECT ON hospital_db.doctors TO 'patient'@'%';")
    
    conn.execute("FLUSH PRIVILEGES;")

    conn.close()