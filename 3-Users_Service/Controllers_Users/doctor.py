from fastapi import Depends, APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from Helper_Users.loghandler import logger
from Services_Users.doctorservices import *
from Helper_Users.verifytoken import jwt_required
from database import get_db


doctor_router = APIRouter()
templates = Jinja2Templates(directory="Templates")


@doctor_router.get('/get-doctor')
async def getDoctor(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        doctor = await getDoctorById(id=doctor_id, db=db)
        return JSONResponse(doctor.to_dict())
    except Exception as err:
        logger.error(f"Error in doctor getDoctor() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    


@doctor_router.get('/dashboard')
async def getDashboard(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        print(f"Doctor id is {doctor_id}")
        doctor = await getDoctorById(id=doctor_id, db=db)
        logger.info(f"doctor getDashboard() Controller, No Errors..")
        doctor_dict = doctor.to_dict()
        print(F"The response is {doctor_dict}")
        return doctor_dict
    except Exception as err:
        logger.error(f"Error in doctor getDashboard() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")


@doctor_router.get('/appointments')
async def getAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        appointments = await getDoctorAppointments(id=doctor_id, db=db)
        logger.info(f"doctor getAppointments() Controller, appointments for doctor with id {doctor_id} retreived successfully")
        appointemnts_list = []
        for appointment in appointments:
            appointemnts_list.append(appointment.to_dict())
        return appointemnts_list
    except Exception as err:
        logger.error(f"Error in doctor getAppointments() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    
    

@doctor_router.get('/timeslots')
async def getDoctorTimeSlots(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        slots = await getDoctorAllTimeSlots(id=doctor_id, db=db)
        logger.info(f"doctor getDoctorTimeSlots() Controller, doctor with id {doctor_id} retreived successfully")
        return slots
    except Exception as err:
        logger.error(f"Error in doctor getDoctorTimeSlots() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

@doctor_router.post('/add-timeslot')
async def addDoctorTimeSlot(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        await createTimeSlot(doctor_id=doctor_id, db=db) 
        logger.info(f"doctor addDoctorTimeSlot() Controller, doctor with id {doctor_id} time slot added successfully")
    except Exception as err:
        logger.error(f"Error in doctor addDoctorTimeSlot() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

@doctor_router.delete("/delete-timeslot/{id}")
async def deleteDoctorTimeSlot(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        await deleteAvailableSlots(slot_id=id, db=db)
        logger.info(f"doctor deleteDoctorTimeSlot() Controller, doctor time slot with id {id} deleted successfully") 
    except Exception as err:
        logger.error(f"Error in doctor deleteDoctorTimeSlot() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

