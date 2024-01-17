import mongoengine as me

class Inverstigation(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True, primary_key=True)
    name = me.StringField(required=True)
    processing_duration = me.IntField(required=True)
    result = me.StringField(required=True)
    
class Consultation(me.Document):
    id_consulation = me.ObjectIdField(required=True, primary_key=True)
    id_patient = me.IntField(required=True)
    id_doctor = me.IntField(required=True)
    date = me.DateTimeField(required=True)
    diagnosis = me.StringField(required=True)
    inverstigations = me.ListField(me.EmbeddedDocumentField(Inverstigation))