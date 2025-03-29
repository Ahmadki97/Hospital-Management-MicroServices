from Helper_Appointment.loghandler import logger
from database import get_db
from dotenv import load_dotenv
import pika 
import json
import os 


load_dotenv('.env')




async def checkRabbitmqConnection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        if connection:
            logger.info(f"CheckRabbitMQConnection() Method, Appointments Service Connected to RabbitMQ Server")
            connection.close()    
        else:
            logger.error(f"Error in checkRabbitMQConnection() Method, Users Service could not connect to RabbitMQ Server")
    except Exception as err:
        logger.error(f"Error in checkRabbitMQConnection() Method: {err}")


async def startPuplishingMessage(queue: str, exchange_name: str, routing_key: str, body):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)
        logger.info(f"startPuplishingMessage() Method, New Message Published to RabbitMQ Server queue name is  {queue}")
        connection.close()   # Close connection after publishing message
    except Exception as err:
        logger.error(f"Error in startPuplishingMessage() Method: {err}")


def startConsumeUserSignupMessage():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        while True:
            print(f"Hello from startConsumeUserSignupMessage() Function..")
            channel.basic_consume(queue='appointment-queue', on_message_callback='', auto_ack=True)
            logger.info(f"startConsumeUserSignupMessage() Method, Finished Consuming Message Successfully..")
            channel.start_consuming()
    except Exception as err:
        logger.error(f"Error in startConsumeUserSignupMessage() Method: {err}")


        