from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class PatientSchema(BaseModel):
    id : Optional[int] = None
    cnp : str
    last_name : str
    first_name : str
    email : str
    phone : str
    birth_date : date
    is_active : bool = True
    
    class Config:
        from_attributes = True
        
class PatientCreate(BaseModel):
    cnp: str
    last_name: str
    first_name: str
    email: str
    phone: str
    birth_date: date
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        
class DoctorSchema(BaseModel):
    id : Optional[int] = None
    last_name : str
    first_name : str
    email : str
    phone : str
    specialization : str
    
    class Config:
        from_attributes = True
        
class DoctorCreate(BaseModel):
    last_name: str
    first_name: str
    email: str
    phone: str
    specialization: str

    class Config:
        from_attributes = True
        
class AppointmentStatus(str, Enum):
    done = 'done'
    not_presented = 'not_presented'
    canceled = 'canceled'

class AppointmentSchema(BaseModel):
    id_patient: int
    id_doctor: int
    date: date
    status: AppointmentStatus
    
    class Config:
        from_attributes = True