from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/patients/", response_model=schemas.PatientSchema, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientSchema, db: Session = Depends(get_db)):
    if crud.patient_exists(db, patient.cnp):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patient already exists.")
    return crud.create_patient(db=db, patient=patient)

@app.get("/patients/{patient_id}", response_model=schemas.PatientSchema)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return patient

@app.post("/appointments/", response_model=schemas.AppointmentSchema)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db=db, appointment=appointment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/appointments/{appointment_id}", response_model=schemas.AppointmentSchema)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment