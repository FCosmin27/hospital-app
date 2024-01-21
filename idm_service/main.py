from fastapi import FastAPI, Depends, HTTPException, status, Response
import crud, models, schemas, security
from crypto.decrypt import check_password_hash
from sqlalchemy.orm import Session
from database import engine, get_db, delete_tables, insert_roles_into_table, insert_admin_user
from security import check_current_user_is_admin, get_current_user
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

#Uncommnet to delete tables
delete_tables()

models.Base.metadata.create_all(bind=engine)

#Uncommnet at first run
insert_roles_into_table() 
insert_admin_user()

app = FastAPI()

def generate_url(name: str, **path_params: str):
    return app.url_path_for(name, **path_params)

def generate_user_links(user_id: int, roles: List[str]):
    links = [
        {"href": generate_url("read_user", user_id=user_id), "rel": "get"}
    ]
    if 'patient' in roles:
        links.append({"href": generate_url("update_patient", user_id=user_id), "rel": "put"})
        links.append({"href": generate_url("delete_patient", user_id=user_id), "rel": "delete"})
    if 'doctor' in roles:
        links.append({"href": generate_url("update_doctor", user_id=user_id), "rel": "put"})
        links.append({"href": generate_url("delete_doctor", user_id=user_id), "rel": "delete"})
    return links

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not check_password_hash(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/patient/", response_model=schemas.UserWithLinks)
def create_patient(user: schemas.UserCreate, db: Session = Depends(get_db)):
    patient_user = crud.get_user_by_username(db, user.username)
    if patient_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_patient = crud.create_user(db=db, user=user, role_name="patient")
    return {
        **new_patient.to_dict(),
        "links": [
            {"href": generate_url("read_user", user_id=new_patient.id), "rel": "get"},
            {"href": generate_url("update_patient", user_id=new_patient.id), "rel": "put"},
            {"href": generate_url("delete_patient", user_id=new_patient.id), "rel": "delete"}
        ]
    }
    
@app.post("/users/doctor/", response_model=schemas.UserWithLinks, dependencies=[Depends(check_current_user_is_admin)])
def create_doctor(user: schemas.UserCreate, db: Session = Depends(get_db)):
    doctor_user = crud.get_user_by_username(db, user.username)
    if doctor_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_doctor = crud.create_user(db=db, user=user, role_name='doctor')
    return {
        **new_doctor.to_dict(),
        "links": [
            {"href": generate_url("read_user", user_id=new_doctor.id), "rel": "get"},
            {"href": generate_url("update_doctor", user_id=new_doctor.id), "rel": "put"},
            {"href": generate_url("delete_doctor", user_id=new_doctor.id), "rel": "delete"}
        ]
    }

@app.get("/users/{user_id}", response_model=schemas.UserWithLinks)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.id != user_id and not any(role.name == 'admin' for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Access denied")
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        **user.to_dict(),
        "links": generate_user_links(user_id, user.to_dict()['roles'])
    }

@app.get("/users/", response_model=List[schemas.UserWithLinks], dependencies=[Depends(check_current_user_is_admin)])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return [
        {
            **user.to_dict(),
            "links": generate_user_links(user.id, user.to_dict()['roles'])
        }
        for user in users
    ]

@app.put("/users/patient/{user_id}", response_model=schemas.UserWithLinks)
def update_patient(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.id != user_id or not any(role.name == 'admin' for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Access denied")
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_patient = crud.update_user(db=db, user_id=user_id, user=user)
    return {
        **updated_patient.to_dict(),
        "links": [
            {"href": generate_url("read_user", user_id=user_id), "rel": "get"},
            {"href": generate_url("delete_user", user_id=user_id), "rel": "delete"}
        ]
    }
    
@app.delete("/users/patient/{user_id}", response_model=schemas.UserWithLinks)
def delete_patient(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.id != user_id or not any(role.name == 'admin' for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Access denied")
    if crud.delete_user(db, user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/users/doctor/{doctor_id}", response_model=schemas.UserWithLinks, dependencies=[Depends(check_current_user_is_admin)])
def update_doctor(doctor_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    doctor_user = crud.get_user(db, doctor_id)
    if not doctor_user:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not any(role.name == 'doctor' for role in doctor_user.roles):
        raise HTTPException(status_code=403, detail="User is not a doctor")

    updated_doctor = crud.update_user(db, doctor_id, user)
    return {
        **updated_doctor.to_dict(),
        "links": [
            {"href": generate_url("read_user", user_id=updated_doctor.id), "rel": "get"},
            {"href": generate_url("delete_user", user_id=updated_doctor.id), "rel": "delete"},
            {"href": generate_url("update_user", user_id=updated_doctor.id), "rel": "put"}
        ]
    }

@app.delete("/users/doctor/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_current_user_is_admin)])
def delete_doctor(user_id: int, db: Session = Depends(get_db)):
    doctor_user = crud.get_user(db, user_id)
    if not doctor_user:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not any(role.name == 'doctor' for role in doctor_user.roles):
        raise HTTPException(status_code=403, detail="User is not a doctor")

    crud.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
