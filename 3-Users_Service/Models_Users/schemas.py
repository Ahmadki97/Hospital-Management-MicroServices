from pydantic import BaseModel, HttpUrl
from datetime import datetime


class DoctorSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    address: str
    department: str
    mobile: str
    work_hours: int
    work_starts: datetime
    work_days: str
    patients: list
    appointments: list


class PatientSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    address: str
    profile_pic: HttpUrl
    birth: datetime
    doctor: DoctorSchema
    appointments: list


class AppointmentSchema(BaseModel):
    id: int
    doctor: DoctorSchema
    patient: PatientSchema
    time: datetime
    description: str
    patient_report: str
    passed: bool