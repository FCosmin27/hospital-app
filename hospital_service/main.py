from fastapi import FastAPI, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
import crud, models, schemas
from datetime import date
from database import SessionLocal, engine
    
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
    if crud.patient_exists(db, patient.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patient already exists.")
    return crud.create_patient(db=db, patient=patient)

@app.get("/patients/{patient_id}", response_model=schemas.PatientSchema)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return patient

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    if crud.delete_patient(db, patient_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/doctors/", response_model=schemas.DoctorSchema, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: schemas.DoctorSchema, db: Session = Depends(get_db)):
    if crud.doctor_exists(db, doctor.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor already exists.")
    return crud.create_doctor(db=db, doctor=doctor)

@app.get("/doctors/{doctor_id}", response_model=schemas.DoctorSchema)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    return doctor

@app.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    if crud.delete_doctor(db, doctor_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/appointments/", response_model=schemas.AppointmentSchema, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentSchema, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db=db, appointment=appointment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/appointments/{patient_id}/{doctor_id}/{date}", response_model=schemas.AppointmentSchema)
def read_appointment(patient_id: int, doctor_id: int, date: date, db: Session = Depends(get_db)):
    appointment = crud.get_appointment_by_composite_id(db, patient_id, doctor_id, date)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
    return appointment

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
