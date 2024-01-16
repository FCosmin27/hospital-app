from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

class Link(BaseModel):
    href: str
    rel: str

class PatientSchema(BaseModel):
    id : Optional[int] = None
    cnp : str
    id_user: int
    last_name : str
    first_name : str
    email : str
    phone : str
    birth_date : date
    is_active : bool = True
    
    class Config:
        from_attributes = True
        
class PatientSchemaWithLinks(PatientSchema):
    links : List[Link] = []
        
class PatientCreate(BaseModel):
    cnp: str
    id_user: int
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
    id_user: int
    last_name : str
    first_name : str
    email : str
    phone : str
    specialization : str
    
    class Config:
        from_attributes = True
        
class DoctorSchemaWithLinks(DoctorSchema):
    links : List[Link] = []
        
class DoctorCreate(BaseModel):
    id_user: int
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
        
class AppointmentSchemaWithLinks(AppointmentSchema):
    links : List[Link] = []