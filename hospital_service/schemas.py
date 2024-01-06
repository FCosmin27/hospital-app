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
        orm_mode = True
        
class PatientCreate(BaseModel):
    cnp: str
    last_name: str
    first_name: str
    email: str
    phone: str
    birth_date: date
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        
class DoctorSchema(BaseModel):
    id : Optional[int] = None
    last_name : str
    first_name : str
    email : str
    phone : str
    specialization : str
    
    class Config:
        orm_mode = True
        
class AppointmentStatus(str, Enum):
    done = 'done'
    not_presented = 'not presented'
    canceled = 'canceled'

class AppointmentCreate(BaseModel):
    id_patient: int
    id_doctor: int
    date: date
    status: AppointmentStatus

class AppointmentSchema(AppointmentCreate):
    id: Optional[int] = None

    class Config:
        orm_mode = True        

        
        
        
        