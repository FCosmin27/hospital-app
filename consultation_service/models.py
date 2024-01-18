import mongoengine as me
from bson import ObjectId
from typing import List
from enum import Enum

class DiagnosisEnum(Enum):
    Sick = "Sick"
    Healthy = "Healthy"

class Investigation(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True, default=lambda: ObjectId())
    name = me.StringField(required=True)
    processing_duration = me.IntField(required=True)
    result = me.StringField(required=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "processing_duration": self.processing_duration,
            "result": self.result
        }

class Consultation(me.Document):
    id_consultation = me.ObjectIdField(required=True, default=lambda: ObjectId())
    id_patient = me.IntField(required=True)
    id_doctor = me.IntField(required=True)
    date = me.DateTimeField(required=True)
    diagnosis = me.StringField(choices=[e.value for e in DiagnosisEnum])
    investigations = me.ListField(me.EmbeddedDocumentField(Investigation))

    def to_dict(self):
        return {
            "id_consultation": str(self.id_consultation),
            "id_patient": self.id_patient,
            "id_doctor": self.id_doctor,
            "date": self.date.isoformat(),
            "diagnosis": self.diagnosis,
            "investigations": [investigation.to_dict() for investigation in self.investigations]
        }
