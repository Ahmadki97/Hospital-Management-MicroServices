from Helper_Users.loghandler import logger
from Services_Users.adminservices import *
from Services_Users.doctorservices import getDoctors, getPendingDoctors, acceptDoctor, refuseDoctor, updateDoctor, deleteDoctor, getDoctorAllTimeSlots
from Services_Users.patientservices import getPatients, getPendingPatients, acceptPatient, refusePatient, getPatientById
from RabbitMq_Users.rabbitmq import startPuplishingMessage
from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db



admin_router = APIRouter()


@admin_router.get('/get-admin')
async def getAdmin(request: Request, db: Session=Depends(get_db)):
    try:
        admin_id = request.state.user['id']
        admin = await getAdminById(id=admin_id, db=db)
        return JSONResponse(admin)
    except Exception as err:
        logger.error(f"Error in getAdmin() Method: {err}")
        return JSONResponse("Could not load admin data, please try again later..")


@admin_router.get('/dashboard')
async def getDashboard(request: Request, db: Session=Depends(get_db)):
    try:
        doctors = await getDoctors(db=db)
        patients = await getPatients(db=db)
        pending_doctors = await getPendingDoctors(db=db)
        pending_patients = await getPendingPatients(db=db)
        admin_id = request.state.user['id']
        print(f"Admin ID is: {admin_id}")
        data = {
            "doctors": doctors,
            "patients": patients,   
            "pending_doctors": pending_doctors,
            "pending_patients": pending_patients,
        }
        print(f"Data is: {data}")
        return JSONResponse(data)
    except Exception as err:
        logger.error(f"Error in getDashboard() Controller: {err}")
        return JSONResponse("Could not load admin data, please try again later..")
    

#####################################################Doctor Controllers#####################################################    

@admin_router.get('/doctors')
async def viewDoctors(request: Request, db: Session=Depends(get_db)):
    try:
        doctors = await getDoctors(db=db)
        logger.info(f"admin viewDoctors Controller, Successfully Found Doctors")
        return doctors
    except Exception as err:
        logger.error(f"Error in viewDoctors() Controller: {err}")
        return JSONResponse("Could not load doctor data, please try again later..")
    

@admin_router.get('/working-doctors')
async def getWorkingDoctors(request: Request, db: Session = Depends(get_db)):
    try:
        doctors = db.query(Doctor).filter(Doctor.status == True).all()
        if len(doctors) == 0:
            logger.info(f"getWorkingDoctors() Controller, No Working Doctors Found in the db.")
            return []
        working_doctors = []
        for doctor in doctors:
            working_doctors.append(doctor.to_dict())
        return working_doctors
    except Exception as err:
        logger.error(f"Error in getWorkingDoctors() Controller: {err}")
        return JSONResponse("Could not load working doctor data, please try again later..")
    

@admin_router.get('/pending-doctors')
async def viewPendingDoctors(request: Request, db: Session=Depends(get_db)):
    try:
        doctors = await getPendingDoctors(db=db)
        logger.info(f"admin viewPendingDoctors Controller, Successfully Found Pending Doctors")
        print(f"Data is: {doctors}")
        return JSONResponse(doctors) 
    except Exception as err:
        logger.error(f"Error in viewPendingDoctors() Controller: {err}")
        return JSONResponse("Could not load pending doctor data, please try again later..")
    

@admin_router.put("/approve-doctor/{id}")
async def approveDoctor(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await acceptDoctor(id=id, db=db)
        logger.info(f"admin approveDoctor Controller, Successfully Approved Doctor with id {id}")
        return JSONResponse("Doctor approved successfully.")
    except Exception as err:
        logger.error(f"Error in approveDoctor() Controller: {err}")
        return JSONResponse("Could not approve doctor, please try again later..")
    

@admin_router.delete("/decline-doctor/{id}")
async def declineDoctor(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await refuseDoctor(id=id, db=db)
        logger.info(f"admin refuseDoctor Controller, Successfully refused Doctor with id {id}")
        return JSONResponse("Doctor refused successfully.")
    except Exception as err:
        logger.error(f"Error in refuseDoctor() Controller: {err}")
        return JSONResponse("Could not refuse doctor, please try again later..")
    

@admin_router.post("/update-doctor/{id}")
async def adminUpdateDoctor(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        doctor_data = await request.form()
        await updateDoctor(id=id, data=doctor_data, db=db)
        logger.info(f"admin adminUpdateDoctor Controller, Successfully Updated Doctor with id {id}")
    except Exception as err:
        logger.error(f"Error in adminUupdateDoctor() Controller: {err}")
        return JSONResponse("Could not update doctor data, please try again later..")
    


# TODO add user Delete Also in the Auth Service  
@admin_router.get("/admin-delete-doctor/{id}")
async def adminDeleteDoctor(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await deleteDoctor(id=id, db=db)
        await startPuplishingMessage(queue='user-delete', exchange_name='', routing_key='user-delete', body=id)
        logger.info(f"admin adminDeleteDoctor Controller, Successfully Deleted Doctor with id {id}")
        return JSONResponse("Doctor deleted successfully.")
    except Exception as err:
        logger.error(f"Error in adminDeleteDoctor() Controller: {err}")
        return JSONResponse("Could not delete doctor, please try again later..")
    

@admin_router.get("/timeslots/{id}")
async def getDoctorTimeSlots(id: int, request: Request, db: Session = Depends(get_db)):
    try:
        time_slots = await getDoctorAllTimeSlots(id, db)
        logger.info(f"admin getDoctorAllTimeSlots Controller, Successfully Found Doctor's Time Slots with id {id}")
        return JSONResponse(time_slots) 
    except Exception as err:
        logger.error(f"Error in getDoctorTimeSlots() Controller: {err}")
        return JSONResponse("Could not get doctor's time slots, please try again later..")
    

###########################################Patient Controllers########################################################


@admin_router.get("/patient/{id}")
async def getPatient(id: int, request: Request, db: Session=Depends(get_db)):
    try:
        patient = await getPatientById(id, db)
        logger.info(f"admin getPatient Controller, Successfully Found Patient with id {id}")
        return patient.to_dict()
    except Exception as err:
        logger.error(f"Error in getPatient() Controller: {err}")
        return JSONResponse("Could not load patient data, please try again later..")
    

@admin_router.get('/patients')
async def viewPatients(request: Request, db: Session=Depends(get_db)):
    try:
        patients = await getPatients(db=db)
        logger.info(f"admin viewPatients Controller, Successfully Found Patients")
        print(f"Patients are {patients}")
        return patients
    except Exception as err:
        logger.error(f"Error in viewPatients() Controller: {err}")
        return JSONResponse("Could not load patient data, please try again later..")
    

@admin_router.get('/pending-patients')
async def viewPendingPatients(request: Request, db: Session=Depends(get_db)):
    try:
        patients = await getPendingPatients(db=db)
        logger.info(f"admin viewPendingPatients Controller, Successfully Found Pending Patients")
        return JSONResponse(patients)
    except Exception as err:
        logger.error(f"Error in viewPendingPatients() Controller: {err}")
        return JSONResponse("Could not load pending patient data, please try again later..")
    


@admin_router.put("/approve-patient/{id}")
async def approvePatient(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await acceptPatient(id=id, db=db)
        logger.info(f"admin approvePatient Controller, Successfully approved Patient with id {id}")
        return JSONResponse("Patient approved successfully.")
    except Exception as err:
        logger.error(f"Error in approvePatient() Controller: {err}")
        return JSONResponse("Could not approve patient, please try again later..")
    

@admin_router.delete("/decline-patient/{id}")
async def declinePatient(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        await refusePatient(id=id, db=db)
        logger.info(f"admin refusePatient Controller, Successfully refused Patient with id {id}")
        return JSONResponse("Patient refused successfully.")
    except Exception as err:
        logger.error(f"Error in refusePatient() Controller: {err}")
        return JSONResponse("Could not refuse patient, please try again later..")
    

@admin_router.post("/discharge-patient/{id}")
async def dischargePatient(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        patient = await getPatientById(id=id, db=db)
        patient.is_discharged = True
        db.commit()
        db.refresh(patient)
        logger.info(f"admin dischargePatient Controller, Successfully Discharged Patient with id {id}")
        return JSONResponse(f"Patient with id {id} Discharged Successfully")
    except Exception as err:
        logger.error(f"Error in dischargePatient() Controller: {err}")
        return JSONResponse("Could not discharge patient, please try again later..")
    


    

###########################################Appointments Controllers################################################




    

