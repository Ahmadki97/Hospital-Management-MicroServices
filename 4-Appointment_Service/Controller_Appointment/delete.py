from Helper_Appointment.loghandler import logger
from Services_Appointment.appointments import declineAppointment
from fastapi import APIRouter, HTTPException, Depends, status, Request
from database import get_db
from sqlalchemy.orm import Session


delete_router = APIRouter()


@delete_router.delete("/decline-appointment/{id}")
async def refuseAppointment(id: int, request: Request, db: Session = Depends(get_db)):
    try:
        await declineAppointment(id=id, db=db)
        logger.info(f"Delete Controller, refuseAppointment() Method, Successfully Declined Appointment with id {id}") 
    except Exception as err:
        logger.error(f"Delete Controller, refuseAppointment() Method, Failed to decline appointment with ID {id}: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to decline appointment")