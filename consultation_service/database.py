from mongoengine import connect
from pymongo.errors import OperationFailure
from config import (
    MONGODB_URI,
    MONGODB_CONSULTATION_ROOT_USERNAME,
    MONGODB_CONSULTATION_ROOT_PASSWORD,
    MONGODB_CONSULTATION_DB_NAME
)

def init_db():
    connection = connect(
        db=MONGODB_CONSULTATION_DB_NAME,
        username=MONGODB_CONSULTATION_ROOT_USERNAME,
        password=MONGODB_CONSULTATION_ROOT_PASSWORD,
        host=MONGODB_URI
    )

def create_users():
    connection = connect(
        db=MONGODB_CONSULTATION_DB_NAME,
        username=MONGODB_CONSULTATION_ROOT_USERNAME,
        password=MONGODB_CONSULTATION_ROOT_PASSWORD,
        host=MONGODB_URI
    )
     
    db = connection[MONGODB_CONSULTATION_DB_NAME]

    try:
        db.command(f"createUser", "doctor",
                   pwd="{MONGODB_CONSULTATION_ROOT_PASSWORD}",
                   roles=["readWrite"])
        print("Doctor user created.")
    except OperationFailure as e:
        print(f"Doctor user creation failed: {e}")

    try:
        db.command(f"createUser", "patient",
                   pwd="{MONGODB_CONSULTATION_ROOT_PASSWORD}",
                   roles=["read"])
        print("Patient user created.")
    except OperationFailure as e:
        print(f"Patient user creation failed: {e}")

    return connection
