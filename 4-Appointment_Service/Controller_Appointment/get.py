from Helper_Appointment.loghandler import logger
from Services_Appointment.appointments import *
from fastapi import HTTPException, status, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from database import get_db


get_router = APIRouter()




@get_router.get('/appointments')
async def appointments(request: Request, db: Session = Depends(get_db)):
    try:
        appointments = await getAppointments(db=db)
        if len(appointments) == 0:
            logger.info(f"getAppointments() Controller, No Appointments found.")
            return []
        appointments_list = []
        logger.info(f"getAppointments() Controller, Appointments successfully fetched.")
        for appointment in appointments:
            appointments_list.append(appointment.to_dict())
        return(appointments_list)
    except Exception as err:
        logger.error(f"Error in getAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getAppointments() process.")
    

@get_router.get('/num-all')
async def numAllAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        num = await getNumofAppointments(db=db)
        logger.info(f"getNumofAppointments() Controller, Number of Appointments successfully fetched.")
        return num
    except Exception as err:
        logger.error(f"Error in getNumofAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getNumofAppointments() process.")


@get_router.get('/pending')
async def pendingAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        pending_appointments = await getPendingAppointments(db)
        logger.info(f"get pendingAppointments() Controller, pending Appointments successfully Calculated.")
        return JSONResponse(pending_appointments)
    except Exception as err:
        logger.error(f"Error in get pendingAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in get pendingAppointments() process.")
    

@get_router.get('/num-pending')
async def numPendingAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        num = await getNumPendingAppointments(db=db)
        logger.info(f"getNumPendingAppointments() Controller, Number of pending Appointments successfully fetched.")
        return num
    except Exception as err:
        logger.error(f"Error in getNumPendingAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getNumPendingAppointments() process.")
    

@get_router.get("/doctor/num-appointments")
async def doctorNumAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        num = await getNumOfAppointmentsForDoctor(doctor_id=doctor_id, db=db)
        logger.info(f"getDoctorNumAppointments() Controller, Number of Appointments for doctor with id {doctor_id} successfully fetched.")
        return num
    except Exception as err:
        logger.error(f"Error in getDoctorNumAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getDoctorNumAppointments() process.")
    

@get_router.get("/doctor/appointments")
async def doctorAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        appointments = await getDoctorAppointments(doctor_id=doctor_id, db=db)
        if appointments is None:
            logger.info(f"getDoctorAppointments() Controller, No Appointments found for doctor with id {doctor_id}.")
            return []
        return appointments
    except Exception as err:
        logger.error(f"Error in doctorAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in doctorAppointments() process.")
    

@get_router.get("/patient/appointments")
async def patientAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        patient_id = request.state.user['id']
        appointments = await getPatientAppointments(id=patient_id, db=db)
        if appointments is None:
            logger.info(f"getPatientAppointments() Controller, No Appointments found for patient with id {patient_id}.")
            return []
        return appointments
    except Exception as err:
        logger.error(f"Error in patientAppointments() Controller: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in patientAppointments() process.")



