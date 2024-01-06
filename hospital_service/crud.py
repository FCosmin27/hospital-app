from sqlalchemy.orm import Session
from . import models, schemas

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient_by_id(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def patient_exists(db: Session, cnp: str):
    return db.query(models.Patient).filter(models.Patient.cnp == cnp).first() is not None

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    # Check if patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == appointment.id_patient).first()
    if not patient:
        raise Exception("Patient not found")

    # Check if doctor exists
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.id_doctor).first()
    if not doctor:
        raise Exception("Doctor not found")

    # Check if the doctor is available at the given date
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.id_doctor == appointment.id_doctor,
        models.Appointment.date == appointment.date
    ).first()
    if existing_appointment:
        raise Exception("Doctor is not available at the selected date")

    # Create the appointment
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
