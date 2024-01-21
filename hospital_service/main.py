from fastapi import FastAPI, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
import crud, models, schemas
from datetime import date
from database import engine
from typing import List
from dependencies import get_db

#delete_tables(engine)    

#create_db_users()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def generate_url(name: str, **path_params: str):
    return app.url_path_for(name, **path_params)
        
@app.post("/patients/", response_model=schemas.PatientSchemaWithLinks, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientSchema, db: Session = Depends(get_db)):
    if crud.patient_exists(db, patient.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patient already exists.")
    patient = crud.create_patient(db=db, patient=patient)
    return {
            **patient.to_dict(),
            "links": [
                {"href": generate_url("read_patient", patient_id=patient.id), "rel": "get"},
                {"href": generate_url("delete_patient", patient_id=patient.id), "rel": "delete"}
            ]
        }
    

@app.get("/patients/{patient_id}", response_model=schemas.PatientSchemaWithLinks)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return {
            **patient.to_dict(),
            "links": [
                {"href": generate_url("read_patient", patient_id=patient.id), "rel": "get"},
                {"href": generate_url("delete_patient", patient_id=patient.id), "rel": "delete"}
            ]
        }
    

@app.get("/patients/", response_model=List[schemas.PatientSchemaWithLinks])
def read_patients(db: Session = Depends(get_db)):
    patients = crud.get_all_patients(db)
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No patients found.")
    return [
        {
            **patient.to_dict(), 
            "links": [
                {"href": generate_url("read_patient", patient_id=patient.id), "rel": "get"},
                {"href": generate_url("delete_patient", patient_id=patient.id), "rel": "delete"}
            ]
        }
        for patient in patients
    ]

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    if crud.delete_patient(db, patient_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/doctors/", response_model=schemas.DoctorSchemaWithLinks, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: schemas.DoctorSchema, db: Session = Depends(get_db)):
    if crud.doctor_exists(db, doctor.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor already exists.")
    doctor = crud.create_doctor(db=db, doctor=doctor)
    return {
        **doctor.to_dict(),
        "links": [
            {"href": generate_url("read_doctor", doctor_id=doctor.id), "rel": "get"},
            {"href": generate_url("delete_doctor", doctor_id=doctor.id), "rel": "delete"}
        ]
    }

@app.get("/doctors/{doctor_id}", response_model=schemas.DoctorSchemaWithLinks)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    return {
        **doctor.to_dict(),
        "links": [
            {"href": generate_url("read_doctor", doctor_id=doctor.id), "rel": "get"},
            {"href": generate_url("delete_doctor", doctor_id=doctor.id), "rel": "delete"}
        ]
    }

@app.get("/doctors/", response_model=List[schemas.DoctorSchemaWithLinks])
def read_doctors(db: Session = Depends(get_db)):
    doctors = crud.get_all_doctors(db)
    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No doctors found.")
    return [
        {
            **doctor.to_dict(),
            "links": [
                {"href": generate_url("read_doctor", doctor_id=doctor.id), "rel": "get"},
                {"href": generate_url("delete_doctor", doctor_id=doctor.id), "rel": "delete"}
            ]
        }
        for doctor in doctors
    ]

@app.get("/doctors/specialization/{specialization}", response_model=List[schemas.DoctorSchemaWithLinks])
def read_doctors_by_specialization(specialization: str, db: Session = Depends(get_db)):
    doctors = crud.get_doctors_by_specialization(db, specialization)
    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No doctors with specialization = {specialization} found.")
    return [
        {
            **doctor.to_dict(),
            "links": [
                {"href": generate_url("read_doctor", doctor_id=doctor.id), "rel": "get"},
                {"href": generate_url("delete_doctor", doctor_id=doctor.id), "rel": "delete"}
            ]
        }
        for doctor in doctors
    ]
    
@app.get("/doctors/last_name/{last_name}", response_model=List[schemas.DoctorSchemaWithLinks])
def read_doctors_by_last_name(last_name: str, db: Session = Depends(get_db)):
    doctors = crud.get_doctors_by_last_name(db, last_name)
    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No doctors with last name = {last_name} found.")
    return [
        {
            **doctor.to_dict(),
            "links": [
                {"href": generate_url("read_doctor", doctor_id=doctor.id), "rel": "get"},
                {"href": generate_url("delete_doctor", doctor_id=doctor.id), "rel": "delete"}
            ]
        }
        for doctor in doctors
    ]

@app.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    if crud.delete_doctor(db, doctor_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/appointments/", response_model=schemas.AppointmentSchemaWithLinks, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentSchema, db: Session = Depends(get_db)):
    try:
        appointment = crud.create_appointment(db=db, appointment=appointment)
        return {
            **appointment.to_dict(),
            "links": [
                {"href": generate_url("read_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "get"},
                {"href": generate_url("update_appointment_status", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date, status=appointment.status), "rel": "update"},
                {"href": generate_url("delete_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "delete"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/appointments/{patient_id}/{doctor_id}/{date}", response_model=schemas.AppointmentSchemaWithLinks)
def read_appointment(patient_id: int, doctor_id: int, date: date, db: Session = Depends(get_db)):
    appointment = crud.get_appointment_by_composite_id(db, patient_id, doctor_id, date)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
    return {
        **appointment.to_dict(),
        "links": [
            {"href": generate_url("read_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "get"},
            {"href": generate_url("update_appointment_status", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date, status=appointment.status), "rel": "update"},
            {"href": generate_url("delete_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "delete"}
        ]
    }

@app.get("/appointments/", response_model=List[schemas.AppointmentSchemaWithLinks])
def read_appointments(db: Session = Depends(get_db)):
    appointments = crud.get_all_appointments(db)
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No appointments found.")
    return [
        {
            **appointment.to_dict(),
            "links": [
                {"href": generate_url("read_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "get"},
                {"href": generate_url("update_appointment_status", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date, status=appointment.status), "rel": "update"},
                {"href": generate_url("delete_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "delete"}
            ]
        }
        for appointment in appointments
    ]
    
@app.get("/appointments/patient_id/{patient_id}", response_model=List[schemas.AppointmentSchemaWithLinks])
def read_appointments_by_patient_id(patient_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_patient_id(db, patient_id)
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No appointments with patient_id = {patient_id} found.")
    return [
        {
            **appointment.to_dict(),
            "links": [
                {"href": generate_url("read_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "get"},
                {"href": generate_url("update_appointment_status", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date, status=appointment.status), "rel": "update"},
                {"href": generate_url("delete_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "delete"}
            ]
        }
        for appointment in appointments
    ]

@app.get("/appointments/doctor_id/{doctor_id}", response_model=List[schemas.AppointmentSchemaWithLinks])
def read_appointments_by_doctor_id(doctor_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_doctor_id(db, doctor_id)
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No appointments with doctor_id = {doctor_id} found.")
    return [
        {
            **appointment.to_dict(),
            "links": [
                {"href": generate_url("read_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "get"},
                {"href": generate_url("update_appointment_status", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date, status=appointment.status), "rel": "update"},
                {"href": generate_url("delete_appointment", patient_id=appointment.id_patient, doctor_id=appointment.id_doctor, date=appointment.date), "rel": "delete"}
            ]
        }
        for appointment in appointments
    ]

@app.put("/appointments/{patient_id}/{doctor_id}/{date}/{status}", response_model=schemas.AppointmentSchema)
def update_appointment_status(patient_id: int, doctor_id: int, date: date, status: str, db: Session = Depends(get_db)):
    if not crud.get_appointment_by_composite_id(db, patient_id, doctor_id, date):
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.update_appointment_status(db=db, patient_id=patient_id, doctor_id=doctor_id, date=date, status=status)

@app.delete("/appointments/{patient_id}/{doctor_id}/{date}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(patient_id: int, doctor_id: int, date: date, db: Session = Depends(get_db)):
    if crud.delete_appointment(db, patient_id, doctor_id, date) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
