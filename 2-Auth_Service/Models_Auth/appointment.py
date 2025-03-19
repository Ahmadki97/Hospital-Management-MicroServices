from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()



class Appointment(Base):
    __tablename__ = 'Appointment'
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    patient = relationship("Patient", back_populates="appointments")
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    doctor = relationship("Doctor", back_populates="appointments")
    date = Column(DateTime, nullable=False, onupdate=func.now())
    description = Column(String)
    patient_report = Column(String(255))
    status = Column(Boolean, default=False)
    passed = Column(Boolean, default=False)