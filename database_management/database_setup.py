from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey, Enum, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymysql import install_as_MySQLdb
import enum
from sqlalchemy import Enum

class Specialization(enum.Enum):
    CARDIOLOGY = "Cardiology"
    NEUROLOGY = "Neurology"
    PEDIATRICS = "Pediatrics"
    ORTHOPEDICS = "Orthopedics"
    DERMATOLOGY = "Dermatology"
    GASTROENTEROLOGY = "Gastroenterology"
    ONCOLOGY = "Oncology"
    GYNECOLOGY = "Gynecology"
    OPHTHALMOLOGY = "Ophthalmology"
    PSYCHIATRY = "Psychiatry"
    ENDOCRINOLOGY = "Endocrinology"


class Status(enum.Enum):
    NOTPRESENT = "Not present"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

install_as_MySQLdb()

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    cnp = Column(CHAR(13), primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(70), unique=True, nullable=False)
    phone = Column(CHAR(10), nullable=False)  # Assuming a specific format is validated
    date_of_birth = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

class Doctor(Base):
    __tablename__ = "doctors"
    id_doctor = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(70), unique=True, nullable=False)
    phone = Column(CHAR(10), nullable=False)  # Assuming a specific format is validated
    specialization = Column(Enum(Specialization))

class Appointment(Base):
    __tablename__ = "appointments"
    id_patient = Column(Integer, ForeignKey('patients.cnp'), primary_key=True)
    id_doctor = Column(Integer, ForeignKey('doctors.id_doctor'), primary_key=True)
    date = Column(Date, primary_key=True)
    status = Column(Enum(Status), default=Status.NOTPRESENT)

# Database configuration
DATABASE_URL = "mysql+pymysql://root:123456789@mariadb:3306/hospital"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
