from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum
from database import Base
from typing import Any

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True, index=True)
    cnp = Column(String(13), unique= True)
    id_user = Column(Integer, unique=True)
    last_name = Column(String(50))
    first_name = Column(String(50))
    email = Column(String(70), unique=True)
    phone = Column(String(10))
    birth_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "cnp": self.cnp,
            "id_user": self.id_user,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date,
            "is_active": self.is_active
        }
    
    
class Doctor(Base):
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, unique=True)
    last_name = Column(String(50))
    first_name = Column(String(50))
    email = Column(String(70), unique=True)
    phone = Column(String(10))
    specialization = Column(Enum('cardiologist', 'neurologist', 'surgeon', 'gynecologist', 'pediatrician', 'dermatologist', 'psychiatrist', 'dentist', 'ophthalmologist', 'orthopedist', 'urologist', 'endocrinologist', 'gastroenterologist', 'pulmonologist', 'rheumatologist', 'nephrologist', 'oncologist', 'allergist', 'hematologist', 'infectious_disease_specialist', 'pathologist', 'radiologist', 'anesthesiologist', 'other'))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "id_user": self.id_user,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "phone": self.phone,
            "specialization": self.specialization
        }
        
class Appointment(Base):
    __tablename__ = 'appointments'
    
    id_patient = Column(Integer, ForeignKey('patients.id'), primary_key=True)
    id_doctor = Column(Integer, ForeignKey('doctors.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    status = Column(Enum('done', 'not_presented', 'canceled'))
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id_patient": self.id_patient,
            "id_doctor": self.id_doctor,
            "date": self.date,
            "status": self.status
        }