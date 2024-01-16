from sqlalchemy.orm import Session
import models, schemas
from datetime import date

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patients(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient_by_id(db: Session, patient_id: int):
    return db.query(models.Patients).filter(models.Patients.id == patient_id).first()

def get_all_patients(db: Session):
    return db.query(models.Patients).all()

def patient_exists(db: Session, id: int):
    return db.query(models.Patients).filter(models.Patients.id == id).first() is not None

def delete_patient(db: Session, patient_id: int):
    existing_patient = db.query(models.Patients).filter(models.Patients.id == patient_id).first()
    
    if not existing_patient:
        return None
    
    db.delete(existing_patient)
    db.commit()
    
    return patient_id

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctors(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(models.Doctors).filter(models.Doctors.id == doctor_id).first()

def get_all_doctors(db: Session):
    return db.query(models.Doctors).all()

def get_doctors_by_specialization(db: Session, specialization: str):
    db_doctors = db.query(models.Doctors).filter(models.Doctors.specialization == specialization).all()
    return db_doctors

def get_doctors_by_last_name(db: Session, last_name: str):
    db_doctors = db.query(models.Doctors).filter(models.Doctors.last_name == last_name).all()
    return db_doctors

def doctor_exists(db: Session, id: int):
    return db.query(models.Doctors).filter(models.Doctors.id == id).first() is not None

def delete_doctor(db: Session, doctor_id: int):
    existing_doctor = db.query(models.Doctors).filter(models.Doctors.id == doctor_id).first()
    
    if not existing_doctor:
        return None
    
    db.delete(existing_doctor)
    db.commit()
    
    return doctor_id

def create_appointment(db: Session, appointment: schemas.AppointmentSchema):
    patient = db.query(models.Patients).filter(models.Patients.id == appointment.id_patient).first()
    if not patient:
        raise Exception("Patient not found")

    doctor = db.query(models.Doctors).filter(models.Doctors.id == appointment.id_doctor).first()
    if not doctor:
        raise Exception("Doctor not found")

    existing_appointment = db.query(models.Appointments).filter(
        models.Appointments.id_doctor == appointment.id_doctor,
        models.Appointments.date == appointment.date
    ).first()
    if existing_appointment:
        raise Exception("Doctor is not available at the selected date")

    db_appointment = models.Appointments(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment_by_composite_id(db: Session, patient_id: int, doctor_id: int, date: date):
    return db.query(models.Appointments).filter(models.Appointments.id_patient == patient_id
                                               and models.Appointments.id_doctor == doctor_id
                                               and models.Appointments.date == date).first()
    
def get_all_appointments(db: Session):
    return db.query(models.Appointments).all()

def get_appointments_by_patient_id(db: Session, patient_id: int):
    return db.query(models.Appointments).filter(models.Appointments.id_patient == patient_id).all()

def get_appointments_by_doctor_id(db: Session, doctor_id: int):
    return db.query(models.Appointments).filter(models.Appointments.id_doctor == doctor_id).all()

def update_appointment_status(db: Session, patient_id: int, doctor_id: int, date: date, status: str):
    db_appointment = db.query(models.Appointments).filter(models.Appointments.id_patient == patient_id
                                               and models.Appointments.id_doctor == doctor_id
                                               and models.Appointments.date == date).first()
    db_appointment.status = status
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, patient_id: int, doctor_id: int, date: date):
    existing_appointment = db.query(models.Appointments).filter(models.Appointments.id_patient == patient_id
                                               and models.Appointments.id_doctor == doctor_id
                                               and models.Appointments.date == date).first()
    
    if not existing_appointment:
        return None
    
    db.delete(existing_appointment)
    db.commit()
    
    return patient_id