from Helper_Appointment.loghandler import logger
from Services_Appointment.appointments import acceptAppointment, addPatientReport
from RabbitMq_Appointment.rabbitmq import startPuplishingMessage
from fastapi import Request, Depends, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from database import get_db
from sqlalchemy.orm import Session
import json


update_router = APIRouter()



@update_router.put("/approve-appointment/{id}")
async def aproveAppointment(id: int, request: Request, db: Session = Depends(get_db)):
    try:
        appointment = await acceptAppointment(id=id, db=db)
        message = {
            "doctor_id": appointment.doctor_id,
            "patient_id": appointment.patient_id,
            "slot_id": appointment.slote_id,
            "appointment_id": appointment.id
        }
        logger.info(f"update appointments controller, approveAppointment() Method, appointment with id {id} approved successfully.")
        await startPuplishingMessage(queue='appointment', exchange_name='', routing_key='appointment', body=json.dumps(message))
        await startPuplishingMessage(queue='discharge-patient', exchange_name='', routing_key='discharge-patient', body=json.dumps(message)) 
    except Exception as err:
        logger.error(f"Error in update controller, acceptAppointment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in acceptAppointment() process.")
    


@update_router.post("/patient-report/{id}")
async def patientReport(id: int, request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        print(f"Form data is: {form_data}")
        report = form_data.get('report')
        print(f"report is: {report}")
        await addPatientReport(id=id, report=report, db=db)
        return JSONResponse(content={"success": True})

        
    except Exception as err:
        logger.error(f"Error in update controller, patientReport() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in patientReport() process.")