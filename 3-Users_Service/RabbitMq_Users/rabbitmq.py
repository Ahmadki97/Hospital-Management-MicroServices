from Helper_Users.loghandler import logger
import logging
from Services_Users.doctorservices import createDoctor, doctorAddAppointment, reserveSlot
from Services_Users.patientservices import createPatient, patientAddAppointment
from Services_Users.adminservices import createAdmin
from Models_Users.models import Patient
from database import get_db
from dotenv import load_dotenv
import aio_pika
import pika
import json
import os 
import asyncio


load_dotenv('.env')



async def checkRabbitmqConnection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        if connection:
            logger.info(f"CheckRabbitMQConnection() Method, Users Service Connected to RabbitMQ Server")
            connection.close()    
        else:
            logger.error(f"Error in checkRabbitMQConnection() Method, Users Service could not connect to RabbitMQ Server")
    except Exception as err:
        logger.error(f"Error in checkRabbitMQConnection() Method: {err}")


async def startPuplishingMessage(queue: str, exchange_name: str, routing_key: str, body):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)
        logger.info(f"startPuplishingMessage() Method, New Message Published to RabbitMQ Server queue name is  {queue}")
        connection.close()
    except Exception as err:
        logger.error(f"Error in startPuplishingMessage() Method: {err}")


def startConsumeUserSignupMessage():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
            channel = connection.channel()
            channel.queue_declare('user-signup')
            channel.basic_consume(queue='user-signup', on_message_callback=consumeUsersignupMessage, auto_ack=True)
            logger.info(f"startConsumeUserSignupMessage() Method, Finished Consuming Message Successfully..")
            channel.start_consuming()
        except Exception as err:
            logger.error(f"Error in startConsumeUserSignupMessage() Method: {err}")

# async def startConsumeUserSignupMessage():
#     try:
#         connection = await aio_pika.connect_robust(host="rabbit", port=5672)
#         channel = await connection.channel()
#         queue = await channel.declare_queue('user-signup', durable=True)
#         await queue.consume(consumeUsersignupMessage)
#         logger.info("Started consuming user signup messages...")
#         await asyncio.Future()
#     except Exception as err:
#         logger.error(f"Error in startConsumeUserSignupMessage() Method: {err}")

def startConsumeAppointment():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.queue_declare('appointment')
        channel.basic_consume(queue='appointment', on_message_callback=consumeAppointment, auto_ack=True)
        logger.info(f"startConsumeAppointment() Method, Finished Consuming Message Successfully..") 
        channel.start_consuming()
    except Exception as err:
        logger.error(f"Error in startConsumeAppointment() Method: {err}")



def startConsumePatientDischarge():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("RABBITMQ_URL")))
        channel = connection.channel()
        channel.queue_declare('discharge-patient')
        channel.basic_consume(queue='discharge-patient', on_message_callback=consumePatientDischarge, auto_ack=True)
        logger.info(f"startConsumePatientDischarge() Method, Finished Message Successfully..")
        channel.start_consuming()
    except Exception as err:
        logger.error(f"startConsumePatientDischarge() Method: {err}")


def consumeUsersignupMessage(ch, method,properties, body):
    db = next(get_db())
    message  = json.loads(body)
    if message['user_type'] == 'doctor':
        del message['user_type']
        createDoctor(doctor=message, db=db)
        logger.info(f"consumeUsersignupMessage() Method, Doctor user created successfully.")
        ch.basic_ack(delivery_tag=method.delivery_tag, requeue=False)
    elif message['user_type'] == 'patient':
        del message['user_type']
        createPatient(patient=message, db=db)
        logger.info(f"consumeUsersignupMessage() Method, Patient user created successfully.")
        ch.basic_ack(delivery_tag=method.delivery_tag, requeue=False)
    elif message['user_type'] == 'admin':
        del message['user_type']
        createAdmin(admin=message, db=db)
        logger.info(f"consumeUsersignupMessage() Method, Admin user created successfully.")
        ch.basic_ack(delivery_tag=method.delivery_tag, requeue=False)


def consumeAppointment(ch, method,properties, body):
    try:
        db = next(get_db())
        message  = json.loads(body)
        print(f"Message is {message}")
        appointment_id = message['appointment_id']
        doctor_id = message['doctor_id']
        patient_id = message['patient_id']
        slot_id = message['slot_id']
        doctorAddAppointment(appointment_id=appointment_id, doctor_id=doctor_id, patient_id=patient_id, db=db)
        patientAddAppointment(appointment_id=appointment_id, patient_id=patient_id, db=db)
        reserveSlot(slot_id=slot_id, db=db)
    except Exception as err:
        logger.error(f"Error in consumeAppointent() Method, {err}")
    
        


def consumePatientDischarge(ch, method, properties, body):
    try:
        db = next(get_db())
        message = json.loads(body)
        print(f"Message is: {message}")
        patient = db.query(Patient).filter(Patient.id == message['patient_id']).first()
        patient.is_discharged = False
        db.commit()
        db.refresh(patient)
        logger.info(f"consumePatientDischarge() Method, Successfully changed patient {message['patient_id']} discharged status...")
    except Exception as err:
        logger.error(f"Error in consumePatientDischarge() Method, {err}")

