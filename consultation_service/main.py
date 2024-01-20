from fastapi import FastAPI, HTTPException, Response, status
from typing import Optional, List
from database import init_db
import crud, models, schemas
from datetime import date, datetime
import mongoengine

app = FastAPI()

init_db()

def generate_url(name: str, **path_params: str):
    return app.url_path_for(name, **path_params)


@app.post("/consultations/", response_model=schemas.ConsultationSchemaWithLinks, status_code=201)
async def create_consultation(consultation_data: schemas.ConsultationCreateSchema):
    existing_consultation = models.Consultation.objects(id_patient=consultation_data.id_patient, id_doctor=consultation_data.id_doctor, date=consultation_data.date).first()
    if existing_consultation:
        raise HTTPException(status_code=409, detail="Consultation already exists.")

    consultation = models.Consultation(
        id_patient=consultation_data.id_patient,
        id_doctor=consultation_data.id_doctor,
        date=consultation_data.date,
        diagnosis=consultation_data.diagnosis,
        investigations=[models.Investigation(**invest.dict()) for invest in consultation_data.investigations]
    ).save()

    consultation_dict = consultation.to_mongo().to_dict()
    consultation_dict['id_consultation'] = str(consultation.id)

    links = [
        {"href": generate_url("read_consultation", consultation_id=str(consultation.id)), "rel": "get"},
        {"href": generate_url("delete_consultation", consultation_id=str(consultation.id)), "rel": "delete"},
        {"href": generate_url("update_consultation", consultation_id=str(consultation.id)), "rel": "put"}
    ]

    return {
        **consultation_dict,
        "links": links
    }

@app.get("/consultations/doctor/{doctor_id}/patient/{patient_id}/date/{date_str}", response_model=schemas.ConsultationSchemaWithLinks)
async def read_consultation_by_doctor_patient_date(doctor_id: int, patient_id: int, date_str: str):
    try:
        consultation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use yyyy-mm-dd.")

    consultation = models.Consultation.objects(id_doctor=doctor_id, id_patient=patient_id, date=consultation_date).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    consultation_dict = consultation.to_mongo().to_dict()
    consultation_dict['id_consultation'] = str(consultation.id)

    return {
        **consultation_dict,
        "links": [
            {"href": generate_url("read_consultation", consultation_id=str(consultation.id)), "rel": "self"},
            {"href": generate_url("delete_consultation", consultation_id=str(consultation.id)), "rel": "delete"},
            {"href": generate_url("update_consultation", consultation_id=str(consultation.id)), "rel": "put"}
        ]
    }
    
@app.get("/consultations/{consultation_id}", response_model=schemas.ConsultationSchemaWithLinks)
async def read_consultation(consultation_id: str):
    consultation = models.Consultation.objects(id=consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    consultation_dict = consultation.to_mongo().to_dict()
    consultation_dict['id_consultation'] = str(consultation.id)

    return {
        **consultation_dict,
        "links": [
            {"href": generate_url("read_consultation", consultation_id=consultation_id), "rel": "self"},
            {"href": generate_url("delete_consultation", consultation_id=consultation_id), "rel": "delete"},
            {"href": generate_url("update_consultation", consultation_id=consultation_id), "rel": "put"}
        ]
    }
    
@app.get("/consultations/", response_model=List[schemas.ConsultationSchemaWithLinks])
async def read_all_consultations():
    consultations = models.Consultation.objects().all()

    consultations_with_links = []
    for consultation in consultations:
        consultation_dict = consultation.to_mongo().to_dict()
        consultation_dict['id_consultation'] = str(consultation.id)
        consultation_with_links = {
            **consultation_dict,
            "links": [
                {"href": generate_url("read_consultation", consultation_id=str(consultation.id)), "rel": "self"},
                {"href": generate_url("delete_consultation", consultation_id=str(consultation.id)), "rel": "delete"},
                {"href": generate_url("update_consultation", consultation_id=str(consultation.id)), "rel": "put"}
            ]
        }
        consultations_with_links.append(consultation_with_links)

    return consultations_with_links


@app.get("/consultations/doctor/{doctor_id}", response_model=List[schemas.ConsultationSchemaWithLinks])
async def read_consultations_by_doctor(doctor_id: int):
    consultations = models.Consultation.objects(id_doctor=doctor_id).all()
    
    consultations_with_links = []
    for consultation in consultations:
        consultation_dict = consultation.to_mongo().to_dict()
        consultation_dict['id_consultation'] = str(consultation.id)
        consultation_with_links = {
            **consultation_dict,
            "links": [
                {"href": generate_url("read_consultation", consultation_id=str(consultation.id)), "rel": "self"},
                {"href": generate_url("delete_consultation", consultation_id=str(consultation.id)), "rel": "delete"},
                {"href": generate_url("update_consultation", consultation_id=str(consultation.id)), "rel": "put"}
            ]
        }
        consultations_with_links.append(consultation_with_links)

    return consultations_with_links

@app.get("/consultations/patient/{patient_id}", response_model=List[schemas.ConsultationSchemaWithLinks])
async def read_consultations_by_patient(patient_id: int):
    consultations = models.Consultation.objects(id_patient=patient_id).all()
    
    consultations_with_links = []
    for consultation in consultations:
        consultation_dict = consultation.to_mongo().to_dict()
        consultation_dict['id_consultation'] = str(consultation.id)
        consultation_with_links = {
            **consultation_dict,
            "links": [
                {"href": generate_url("read_consultation", consultation_id=str(consultation.id)), "rel": "self"},
                {"href": generate_url("delete_consultation", consultation_id=str(consultation.id)), "rel": "delete"},
                {"href": generate_url("update_consultation", consultation_id=str(consultation.id)), "rel": "put"}
            ]
        }
        consultations_with_links.append(consultation_with_links)

    return consultations_with_links

    
@app.delete("/consultations/consultation_id/{consultation_id}", status_code=204)
async def delete_consultation(consultation_id: str):
    consultation = models.Consultation.objects(id=consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    consultation.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/consultations/{consultation_id}", response_model=schemas.ConsultationSchemaWithLinks)
async def update_consultation(consultation_id: str, update_data: schemas.ConsultationUpdateSchema):
    consultation = models.Consultation.objects(id=consultation_id).first()
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")


    consultation.update(**update_data.dict(exclude_unset=True))
    consultation.reload()

    consultation_dict = consultation.to_mongo().to_dict()
    consultation_dict['id_consultation'] = str(consultation.id)

    return {
        **consultation_dict,
        "links": [
            {"href": generate_url("read_consultation", consultation_id=consultation_id), "rel": "self"},
            {"href": generate_url("delete_consultation", consultation_id=consultation_id), "rel": "delete"},
            {"href": generate_url("update_consultation", consultation_id=consultation_id), "rel": "put"}
        ]
    }

@app.delete("/consultations/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_consultations():
    models.Consultation.drop_collection()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

