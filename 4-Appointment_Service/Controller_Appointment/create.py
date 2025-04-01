from Helper_Appointment.loghandler import logger
from Services_Appointment.appointments import createAppointment
from RabbitMq_Appointment.rabbitmq import startPuplishingMessage
from database import get_db
from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import json



create_router = APIRouter()

@create_router.post("/create-appointment")
async def appointment(request: Request, db: Session =  Depends(get_db)):
    try:
        appointment_data = await request.form()
        print(f"Appointment_data is {appointment_data}")
        data = {
            "doctor_id": appointment_data.get("doctor"),
            "doctor_name": appointment_data.get("doctor_name"),
            "patient_id": appointment_data.get("patient"),
            "patient_name": appointment_data.get("patient_name"),
            "slote_id": appointment_data.get("time"),
            "slote_date": appointment_data.get("slot_date"),
            "slote_start_time": appointment_data.get("slot_start_time"),
            "description": appointment_data.get("description"),
        }
        print(f"Data is: {data}")
        appointment = await createAppointment(data, db)
        message = {
            "doctor_id": appointment.doctor_id,
            "patient_id": appointment.patient_id,
            "slot_id": appointment.slote_id,
            "appointment_id": appointment.id
        }
        await startPuplishingMessage(queue='appointment', exchange_name='', routing_key='appointment', body=json.dumps(message))
    except Exception as err:
        logger.error(f"Error in adminCreateAppointment() Controller: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error in adminCreateAppointment() process."})
