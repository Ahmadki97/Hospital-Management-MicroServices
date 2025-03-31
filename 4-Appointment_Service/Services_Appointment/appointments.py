from Helper_Appointment.loghandler import logger
from RabbitMq_Appointment.rabbitmq import startPuplishingMessage
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Models_Appointment.models import Appointment
import json




async def createAppointment(appointment: dict, db: Session):
    try:
        user = db.query()
        appointment = Appointment(**appointment)
        db.add(appointment)
        db.commit()
        logger.info(f"createAppointment() Method, Appointment with id {appointment.id} created successfully.")
        return appointment
    except Exception as err:
        logger.error(f"Error in createAppointment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in createAppointment() process.")


async def acceptAppointment(id: int, db: Session):
    try:
        appointment = db.query(Appointment).filter(Appointment.id == id).first()
        if appointment is None:
            logger.info(f"acceptAppointment() Method, could not find appointment with id {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        appointment.status = True
        db.commit()
        logger.info(f"acceptAppointment() Method, appointment with id {id} accepted successfully.")
        db.refresh(appointment)
        return appointment
    except Exception as err:
        logger.error(f"Error in acceptAppointment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in acceptAppointment() process.")
    


async def declineAppointment(id: int, db: Session):
    try:
        appointment = db.query(Appointment).filter(Appointment.id == id).first()
        message = {
            'slot_id': appointment.slote_id,
            'doctor_id': appointment.doctor_id,
            'patient_id': appointment.patient_id,
        }
        db.delete(appointment)
        db.commit()
        logger.info(f"delcineAppointment() Method, Appointment with id {id} removed successfully from db")
        startPuplishingMessage(queue='appointment-delete', exchange_name='', routing_key='appointment-delete', body=json.dumps(message))
    except Exception as err:
        logger.error(f"Error in declineAppointment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in declineAppointment() process.")
    

async def patientReport(id: int, report: str, db: Session):
    try:
        appointment = db.query(Appointment).filter(Appointment.id == id).first()
        if appointment is None:
            logger.info(f"patientReport() Method, could not find appointment with id {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        appointment.patient_report = report
        db.commit()
        logger.info(f"patientReport() Method, patient report for appointment with id {id} updated successfully.")
        return {"message": "Patient report updated successfully."}
    except Exception as err:
        logger.error(f"Error in patientReport() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in patientReport() process.")
    

async def getAppointments(db: Session):
    try:
        appointments = db.query(Appointment).all()
        return appointments 
    except Exception as err:
        logger.error(f"Error in getAppointments() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getAppointments() process.")
    

async def getAppointmentById(id:int, db: Session):
    try:
        appointment = db.query(Appointment).filter(Appointment.id == id).first()
        if appointment is None:
            logger.info(f"getAppointment() Method, could not find appointment with id {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        else:
            return appointment
    except Exception as err:
        logger.error(f"Error in getAppointment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getAppointment() process.")
    

async def getAppointmentDoctor(id: int, db: Session):
    try:
        appointment = db.query(Appointment).filter(Appointment.id == id).first()
        if appointment is None:
            logger.info(f"getAppointmentDoctor() Method, could not find appointment with id {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        doctor_id = appointment.doctor_id
        return doctor_id
    except Exception as err:
        logger.error(f"Error in getAppointmentDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getAppointmentDoctor() process.")

   

async def getNumofAppointments(db: Session):
    try:
        num_appointments = db.query(Appointment).count()
        logger.info(f"getNumofAppointments() Method, found {num_appointments} appointments.")
        return num_appointments
    except Exception as err:
        logger.error(f"Error in getNumofAppointments() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getNumofAppointments() process.")
    

async def getPendingAppointments(db: Session):
    try:
        appointments = db.query(Appointment).filter(Appointment.status == False).all()
        if len(appointments) == 0:
            logger.info("getPendingAppointments() Method, no pending appointments found.")
            return []
        else:
            appointments_list = []
            for appointment in appointments:
                appointments_list.append(appointment.to_dict())
            return appointments_list
    except Exception as err:
        logger.error(f"Error in getPendingAppointments() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getPendingAppointments() process.")
    

async def getNumPendingAppointments(db: Session):
    try:
        num_pending_appointments = db.query(Appointment).filter(Appointment.status == False).count()
        logger.info(f"getNumPendingAppointments() Method, found {num_pending_appointments} pending appointments.")
        return num_pending_appointments
    except Exception as err:
        logger.error(f"Error in getNumPendingAppointments() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getNumPendingAppointments() process.")
    

async def getNumOfAppointmentsForDoctor(doctor_id: int, db: Session):
    try:
        num_appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).count()
        logger.info(f"getNumOfAppointmentsForDoctor() Method, found {num_appointments} appointments for doctor with id {doctor_id}.")
        return num_appointments
    except Exception as err:
        logger.error(f"Error in getNumOfAppointmentsForDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getNumOfAppointmentsForDoctor() process.")
    

async def getNumOfAppointmentsForPatient(patient_id: int, db: Session):
    try:
        num_appointments = db.query(Appointment).filter(Appointment.patient_id == patient_id).count()
        logger.info(f"getNumOfAppointmentsForPatient() Method, found {num_appointments} appointments for patient with id {patient_id}.")
        return num_appointments
    except Exception as err:
        logger.error(f"Error in getNumOfAppointmentsForPatient() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getNumOfAppointmentsForPatient() process.")
    

async def getDoctorAppointments(doctor_id: int, db: Session):
    try:
        appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()
        if len(appointments) == 0:
            logger.info(f"getDoctorAppointments() Method, no appointments found for doctor with id {doctor_id}.")
            return []
        else:
            appointments_list = []
            for appointment in appointments:
                appointments_list.append(appointment.to_dict())
            return appointments_list
    except Exception as err:
        logger.error(f"Error in getDoctorAppointments() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getDoctorAppointments() process.")



async def getPatientAppointments(id: int, db: Session):
    try:
        appointments = db.query(Appointment).filter(Appointment.patient_id == id).all()
        if appointments is None:
            logger.info(f"getAppointmentPatient() Method, could not find appointment with id {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        else:
            appointments_list = []
            for appointment in appointments:
                appointments_list.append(appointment.to_dict())
            logger.info(f"getPatientAppointments() Method, appointments for patient with id {id} retreived successfully.")
            return appointments_list
    except Exception as err:
        logger.error(f"Error in getAppointmentPatient() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in getAppointmentPatient() process.")
 



async def addPatientReport(id: int, report: str, db: Session):
    try:
        appointemnt = db.query(Appointment).filter(Appointment.id == id).first()
        if appointemnt is None:
            logger.info(f"addPatientReport() Method, could not find appointment with id {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        appointemnt.patient_report = report
        db.commit()
        db.refresh(appointemnt)
        logger.info(f"addPatientReport() Method, patient report for appointment {id} updated successfully.")
    except Exception as err:
        logger.error(f"Error in addPatientReport() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in addPatientReport() process.")