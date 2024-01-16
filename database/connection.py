from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from .models import Patient

# Load environment variables from .env file
load_dotenv()

# Database Configuration
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_patient_names() -> list:
    """Retrieve a list of patient names from the database."""
    with SessionLocal() as session:
        return [patient.patient_name for patient in session.query(Patient.patient_name).all()]


def get_patient_clinical_data(patient_name: str) -> list:
    """Get clinical data for a specific patient."""
    with SessionLocal() as session:
        return [patient.clinical_data for patient in session.query(Patient).filter(Patient.patient_name == patient_name).all()]
