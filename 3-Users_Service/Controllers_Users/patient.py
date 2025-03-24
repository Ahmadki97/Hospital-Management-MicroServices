from Helper_Users.loghandler import logger
from database import get_db
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from Services_Users.patientservices import *
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="Templates")
patient_router = APIRouter()


@patient_router.get('/get-patient')
async def getPatient(request: Request, db: Session = Depends(get_db)):
    try:
        patient_id = request.state.user['id']
        patient = await getPatientById(id=patient_id, db=db)
        return patient.to_dict()
    except Exception as err:
        logger.error(f"Error in getPatient() Controller: {err}")
        return JSONResponse({"message": "Error in getPatient() process."})


@patient_router.get("/dashboard")
async def getDashboard(request: Request, db: Session = Depends(get_db)):
    try:
        patient_id = request.state.user['id']
        patient = await getPatientById(id=patient_id, db=db)
        response = {
            "patient": patient.to_dict(),
        }
        return response
    except Exception as err:
        logger.error(f"Error in getDashboard() Controller: {err}")
        return JSONResponse({"message": "Error in getDashboard() process."})
    

# @patient_router.get('/appointments')
# async def getAppointments(request: Request, db: Session = Depends(get_db)):
#     try:
#         patient_id = request.state.user['id']
#         appointments = await getPatientAppointments(id=patient_id, db=db)
        
#         return [appointment.to_dict() for appointment in appointments]
#     except Exception as err:
#         logger.error(f"Error in getAppointments() Controller: {err}")
#         return JSONResponse({"message": "Error in getAppointments() process."})