from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Link(BaseModel):
    href: str
    rel: str

class InvestigationSchema(BaseModel):
    id: str
    name: str
    processing_duration: int
    result: str

class ConsultationCreateSchema(BaseModel):
    id_patient: int
    id_doctor: int
    date: datetime
    diagnosis: str
    investigations: List[InvestigationSchema]

class ConsultationSchema(ConsultationCreateSchema):
    id_consultation: str

class ConsultationUpdateSchema(BaseModel):
    diagnosis: Optional[str] = None
    investigations: Optional[List[InvestigationSchema]] = None

class ConsulationSchemaWithLinks(ConsultationSchema):
    links: List[Link] = []