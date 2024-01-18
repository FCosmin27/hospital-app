from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class DiagnosisEnum(str, Enum):
    Sick = "Sick"
    Healthy = "Healthy"
    
class Link(BaseModel):
    href: str
    rel: str

class InvestigationSchema(BaseModel):
    name: str
    processing_duration: int
    result: str

class ConsultationCreateSchema(BaseModel):
    id_patient: int
    id_doctor: int
    date: date
    diagnosis: DiagnosisEnum
    investigations: List[InvestigationSchema]

class ConsultationSchema(ConsultationCreateSchema):
    id_consultation: str

class ConsultationUpdateSchema(BaseModel):
    diagnosis: Optional[str] = None
    investigations: Optional[List[InvestigationSchema]] = None

class ConsultationSchemaWithLinks(ConsultationSchema):
    links: List[Link] = []