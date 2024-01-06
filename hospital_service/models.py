from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum
from database import Base

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True, index=True)
    cnp = Column(String(13), unique= True)
    id_user = Column(Integer, ForeignKey('users.id'))
    last_name = Column(String(50))
    first_name = Column(String(50))
    email = Column(String(70), unique=True)
    phone = Column(String(10))
    birth_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
class Doctor(Base):
    _tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    last_name = Column(String(50))
    first_name = Column(String(50))
    email = Column(String(70), unique=True)
    phone = Column(String(10))
    specialization = Column(Enum('cardiologist', 'neurologist', 'surgeon', 'gynecologist', 'pediatrician', 'dermatologist', 'psychiatrist', 'dentist', 'ophthalmologist', 'orthopedist', 'urologist', 'endocrinologist', 'gastroenterologist', 'pulmonologist', 'rheumatologist', 'nephrologist', 'oncologist', 'allergist', 'hematologist', 'infectious_disease_specialist', 'pathologist', 'radiologist', 'anesthesiologist', 'other'))
    

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id_patient = Column(Integer, ForeignKey('patients.id'), primary_key=True)
    id_doctor = Column(Integer, ForeignKey('doctors.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    status = Column(Enum('done', 'not presented', 'canceled'))