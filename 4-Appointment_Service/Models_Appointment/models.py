from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey, Time
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from database import Base


class Appointment(Base):
    __tablename__ = 'Appointments'
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True, nullable=False)
    patient_name = Column(String(30), nullable=False)
    doctor_id = Column(Integer, index=True, nullable=False)
    doctor_name = Column(String(30), nullable=False)
    slote_id = Column(Integer, index=True, nullable=False)
    slote_date = Column(DateTime, nullable=False)
    slote_start_time = Column(Time, nullable=False)
    description = Column(String)
    patient_report = Column(String)
    status = Column(Boolean, default=False)
    passed = Column(Boolean, default=False)
    

    def to_dict(self):
        appointemnt = {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor_name,
            'patient_name': self.patient_name,
            'slote_date': str(self.slote_date),
            'slote_start_time': str(self.slote_start_time),
            'description': self.description,
            'patient_report': self.patient_report,
            'status': self.status,
            'passed': self.passed,
        }
        return appointemnt


    