from Helper_Users.loghandler import logger
from Models_Users.models import Doctor, AvailableSlots, Patient
from Models_Users.schemas import AppointmentSchema, DoctorSchema, PatientSchema
from fastapi import HTTPException , status
from sqlalchemy.orm import Session
import datetime

day_to_num = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}


async def getDoctors(db: Session):
    try:
        doctors = db.query(Doctor).all() 
        print(f"Doctors are: {doctors}")
        if len(doctors) == 0:
            logger.info(f"adminservices, getDoctors() Method, No doctors found.")
            return []
        doctor_list = []
        for doctor in doctors:
            print(f"Doctor id is: {doctor.id}")
            doctor_list.append(doctor.to_dict())
        return doctor_list
    except Exception as err:
        logger.error(f"adminservices, Error in getDoctors() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getPendingDoctors(db: Session):
    try:
        doctors = db.query(Doctor).filter(Doctor.status == False).all() 
        print(f"Pending Doctors are: {doctors}")
        if len(doctors) == 0:
            logger.info(f"adminservices, getPendingDoctors() Method, No pending doctors found.")
            return []
        doctor_list = []
        for doctor in doctors:
            print(f"Doctor id is: {doctor.id}")
            doctor_list.append(doctor.to_dict())
        return doctor_list
    except Exception as err:
        logger.error(f"Error in getPendingDoctors() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getAcceptedDoctors(db: Session):
    try:
        doctors = db.query(Doctor).filter(Doctor.status == True).all() 
        print(f"Accepted Doctors are: {doctors}")
        if len(doctors) == 0:
            logger.info(f"adminservices, getAcceptedDoctors() Method, No accepted doctors found.")
            return []
        doctor_list = []
        for doctor in doctors:
            print(f"Doctor id is: {doctor.id}")
            doctor_list.append(doctor.to_dict())
        return doctor_list
    except Exception as err:
        logger.error(f"Error in getAcceptedDoctors() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def updateDoctor(id: int, data: dict, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"updateDoctor() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        for key, value in data.items():
            setattr(doctor, key, value)
        db.commit()
        db.refresh(doctor)
        logger.info(f"updateDoctor() Method, Doctor with id {id} updated successfully..")
    except Exception as err:
        logger.error(f"Error in updateDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def deleteDoctor(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"deleteDoctor() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        db.delete(doctor)
        db.commit()
        logger.info(f"deleteDoctor() Method, Doctor with id {id} deleted successfully..")
    except Exception as err:
        logger.error(f"Error in deleteDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def acceptDoctor(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"approveDoctor() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        doctor.status = True
        db.commit()
        logger.info(f"approveDoctor() Method, Doctor with id {id} approved successfully.")
    except Exception as err:
        logger.error(f"Error in approveDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def refuseDoctor(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"declineDoctor() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        db.delete(doctor)
        db.commit()
        logger.info(f"declineDoctor() Method, Doctor with id {id} declined successfully.")
    except Exception as err:
        logger.error(f"Error in declineDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    



def calculateUpcomingWorkDays(work_days: list, current_date=None):
    try:
        current_date = datetime.datetime.now().date()
        upcoming_workdays = []
        for day in work_days:
            days_ahead = (day - current_date.weekday() + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            next_workdays = current_date + datetime.timedelta(days=days_ahead)
            upcoming_workdays.append(next_workdays)
        return upcoming_workdays
    except Exception as err:
        logger.error(f"Error in calculateUpcomingWorkDays() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

def createTimeSlot(doctor_id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor is None:
            logger.info(f"createTimeSlot() Method, Doctor with id {doctor_id} not found in the db")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found in the db")
        work_days = doctor.work_days
        if len(work_days) == 0:
            logger.info(f"createTimeSlot() Method, Doctor with id {doctor_id} has no work days")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor has no work days")
        numeric_work_days = [day_to_num[day.lower()] for day in work_days]
        upcoming_dates = calculateUpcomingWorkDays(numeric_work_days)
        for day, start_time, hours in zip(upcoming_dates, doctor.work_start, doctor.work_hours):
            work_start_time = start_time if isinstance(start_time, datetime.time) else datetime.datetime.strptime(start_time, "%H:%M").time()
            work_start_datetime = datetime.datetime.combine(day, work_start_time)  # Use `day` for correct date
            work_end_datetime = work_start_datetime + datetime.timedelta(hours=hours)
            work_ends = work_end_datetime.time()
            current_work_start = work_start_time
            available_slots = []
            while current_work_start < work_ends:
                end_time = (datetime.datetime.combine(day, current_work_start) + datetime.timedelta(minutes=30)).time()
                if end_time > work_ends:
                    break
                time_slot = {
                    "doctor_id": doctor.id,
                    "slot_date": day,
                    "slot_start_time": current_work_start,
                    "slot_end_time": end_time
                }
                slot = AvailableSlots(**time_slot)
                db.add(slot)
                db.commit()
                available_slots.append(slot.to_dict())
                logger.info(f"createTimeSlot() Method, new Slot created with id {slot.id} for doctor {slot.doctor_id}")
                # Move to the next 30-minute slot
                current_work_start = (datetime.datetime.combine(day, current_work_start) + datetime.timedelta(minutes=30)).time()
        return available_slots
    except Exception as err:
        logger.error(f"Error in createTimeSlot() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def createDoctor(doctor: dict, db: Session):
    try:
        doctor_create = Doctor(**doctor)
        db.add(doctor_create)
        db.commit()
        logger.info(f"createDoctor() Method, Doctor {doctor_create.first_name} {doctor_create.last_name} created successfully..")
        available_slots = createTimeSlot(doctor_id=doctor_create.id, db=db)
        doctor_create.available_slots = available_slots
    except Exception as err:
        logger.error(f"Error in createDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorById(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"getDoctorById() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor
    except Exception as err:
        logger.error(f"Error in getDoctorById() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorByUsername(username: str, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.username == username).first()
        if doctor is None:
            logger.info(f"getDoctorByUsername() Method, Doctor with username {username} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return DoctorSchema.model_dump(doctor)
    except Exception as err:
        logger.error(f"Error in getDoctorByUsername() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorsByDepartment(department: str, db: Session):
    try:
        doctors = db.query(Doctor).filter(Doctor.department == department).all()
        if len(doctors) == 0:
            logger.info(f"getDoctorsByDepartment() Method, No doctors found for department {department}.")
            return []
        else:
            logger.info(f"getDoctorsByDepartment() Method, {len(doctors)} doctors found for department {department}.")
            return [DoctorSchema.model_dump(doctor) for doctor in doctors]
    except Exception as err:
        logger.error(f"Error in getDoctorsByDepartment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorPatients(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"getDoctorPatients() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        patients = doctor.patients
        if len(patients) == 0:
            logger.info(f"getDoctorPatients() Method, No patients found for doctor with id {id}.")
            return []
        else:
            logger.info(f"getDoctorPatients() Method, {len(patients)} patients found for doctor with id {id}.")
            patients_list = []
            for patient in patients:
                patients_list.append(patient.to_dict())
            return patients_list
    except Exception as err:
        logger.error(f"Error in getDoctorPatients() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

# async def getDoctorDischargedPatients(id: int, db: Session):
#     try:
#         doctor = db.query(Doctor).filter(Doctor.id == id).first()
#         if doctor is None:
#             logger.info(f"getDoctorDischargedPatients() Method, Doctor with id {id} not found.")
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
#         patients = doctor.patients
#         if len(patients) == 0:
#             logger.info(f"getDoctorDischargedPatients() Method, No patients found for doctor with id {id}.")
#             return []
#         else:
#             patients_list = []
#             logger.info(f"getDoctorDischargedPatients() Method, {len(patients)} discharged patients found for doctor with id {id}.")
#             for patient in patients:
#                 if patient.is_discharged:
#                     patients_list.append(patient.to_dict())
#             print(f"Discharged Patients are: {patients}")
#             return patients_list
#     except Exception as err:
#         logger.error(f"Error in getDoctorDischargedPatients() Method: {err}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorAppointments(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"getDoctorAppointments() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        appointments = doctor.appointments
        if len(appointments) == 0:
            logger.info(f"getDoctorAppointments() Method, No appointments found for doctor with id {id}.")
            return []
        else:
            logger.info(f"getDoctorAppointments() Method, {len(appointments)} appointments found for doctor with id {id}.")
            appointments = [AppointmentSchema.model_dump(appointment) for appointment in appointments]
            return appointments
    except Exception as err:
        logger.error(f"Error in getDoctorAppointments() Method: {err}.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

# async def getDoctorAvailableTimeSlots(id: int, db: Session):
#     try:
#         available_time_slots = db.query(AvailableSlots).filter(AvailableSlots.is_booked == False).all()
#         logger.info(f"Successfully loaded available slots for doctor {id}")
#         if len(available_time_slots) == 0:
#             return []
#         available_slots = []
#         for slot in available_time_slots:
#             available_slots.append(slot.to_dict())
#             print(f"Available Slot is: {available_slots}")
#         return available_slots
#     except Exception as err:
#         logger.error(f"Error in getDoctorAvailableTimeSlots() Method: {err}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorAllTimeSlots(id: int, db: Session):
    try:
        timeslots = db.query(AvailableSlots).filter(AvailableSlots.doctor_id == id).all()
        logger.info(f"getDoctorTimeSlots() Method, Time Slots for doctor with id {id} founded successfully.")
        if len(timeslots) == 0:
            return []
        slots = []
        for slot in timeslots:
            slots.append(slot.to_dict())
        return slots
    except Exception as err:
        logger.error(f"Error in getDoctorTimeSlots() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    

def doctorAddAppointment(appointment_id: int, doctor_id: int, patient_id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        print(f"doctor id is {doctor_id} and doctor is {doctor.username}")
        print(f"Doctor appointments is {doctor.appointments}")
        if doctor is None:
            logger.info(f"doctorAddAppointment() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        elif doctor.appointments is None:
            print(f"Doctor Appointments is None")
            doctor.appointments = []
        doctor.appointments = doctor.appointments + [appointment_id]
        doctor.patients = doctor.patients = [patient]   
        db.commit()
        db.refresh(doctor)
        print(f"Doctor new Appointments are: {doctor.appointments}")
        logger.info(f"doctorAddAppointment() Method, New appointment created with id {appointment_id} for doctor {doctor.id}")
    except Exception as err:
        logger.error(f"Error in doctorAddAppointment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

def reserveSlot(slot_id: int, db: Session):
    try:
        slot = db.query(AvailableSlots).filter(AvailableSlots.id == slot_id).first()
        if slot is None:
            logger.info(f"reserveSlot() Method, Slot with id {slot_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
        slot.is_booked = True
        db.commit()
        db.refresh(slot)
        logger.info(f"reserveSlot() Method, Slot {slot_id} has been reserved.")
    except Exception as err:
        logger.error(f"Error in reserveSlot() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

def deleteAvailableSlots(slot_id: int, db: Session):
    try:
        slot = db.query(AvailableSlots).filter(AvailableSlots.id == slot_id).first()
        if slot is None:
            logger.info(f"deleteAvailableSlots() Method, Slot with id {slot_id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
        db.delete(slot)
        db.commit()
        logger.info(f"deleteAvailableSlots() Method, Slot {slot_id} has been deleted.")
    except Exception as err:
        logger.error(f"Error in deleteAvailableSlots() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    



    