from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey, Time, Date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, backref
from database import Base
import datetime

class Admin(Base):
    __tablename__ = 'Admins'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    profile_pic = Column(String(255))
    address = Column(String(255))

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'profile_pic': self.profile_pic,
        }

class Patient(Base):
    __tablename__ = 'Patients'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    profile_pic = Column(String(255))
    address = Column(String(255))
    mobile = Column(String(255))
    status = Column(Boolean, default=False)
    symptoms = Column(String(500))
    birth = Column(DateTime)
    admit_date = Column(DateTime, default=datetime.datetime.now)
    doctor_id = Column(Integer, ForeignKey("Doctors.id"), nullable=True)
    doctor = relationship("Doctor", back_populates='patients')
    appointments = Column(ARRAY(Integer), default=[])
    is_discharged = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'address': self.address,
            'status': self.status,
            'symptoms': self.symptoms,
            'birth': self.birth,
            'mobile': self.mobile,
            'admit_date': str(self.admit_date.date()),
            'doctor_id': self.doctor_id,
            "doctor": self.doctor.to_dictPatient(),
            'appointments': self.appointments,
            "is_discharged": self.is_discharged
        }


class Doctor(Base):
    __tablename__ = 'Doctors'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    profile_pic = Column(String(255))
    address = Column(String(255))
    status = Column(Boolean, default=False)
    department = Column(String(255))
    mobile = Column(String(15))
    work_days = Column(ARRAY(String(255)), default=[])
    work_hours = Column(ARRAY(Integer), default=[])
    work_start = Column(ARRAY(String(15)), default=[])
    patients = relationship("Patient", back_populates='doctor')
    appointments = Column(ARRAY(Integer), default=[]) 
    available_slots = relationship("AvailableSlots", back_populates="doctor")

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'address': self.address,
            'department': self.department,
            'mobile': self.mobile,
            'status': self.status,
            'patients': [patient.to_dict() for patient in self.patients or []],
            'appointments': self.appointments,
            'available_slots': [slot.to_dict() for slot in self.available_slots or []],
            'work_days': self.work_days,
            'work_hours': self.work_hours,
            'work_start': self.work_start,
        }


    def to_dictPatient(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'address': self.address,
            'department': self.department,
            'mobile': self.mobile,
            'status': self.status,
            'appointments': self.appointments,
            'available_slots': [slot.to_dict() for slot in self.available_slots or []],
            'work_days': self.work_days,
            'work_hours': self.work_hours,
            'work_start': self.work_start,
        }

class AvailableSlots(Base):
    __tablename__ = 'AvailableSlots'
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('Doctors.id'), index=True)
    slot_date = Column(Date, nullable=False)
    slot_start_time = Column(Time, nullable=False)
    slot_end_time = Column(Time, nullable=False)
    is_booked = Column(Boolean, default=False, index=True)
    doctor = relationship("Doctor", back_populates="available_slots")

    def to_dict(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "slot_date": str(self.slot_date),
            "slot_start_time": str(self.slot_start_time),
            "slot_end_time": str(self.slot_end_time),
            "is_booked": self.is_booked,
        }
