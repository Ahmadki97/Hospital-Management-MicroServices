from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from Helper_Users.elastic import checkElasticConnection
from RabbitMq_Users.rabbitmq import checkRabbitmqConnection, startConsumeUserSignupMessage, startConsumeAppointment, startConsumePatientDischarge
from Services_Users.jwtmiddleware import JwtMiddleware
from Controllers_Users.doctor import doctor_router
from Controllers_Users.admin import admin_router
from Controllers_Users.patient import patient_router
from database import createTable
import uvicorn
import threading




@asynccontextmanager
async def lifeSpan(app: FastAPI):
    print("Welcome from lIfeSpan..")
    await checkElasticConnection()
    await checkRabbitmqConnection()
    signup_user_thread = threading.Thread(target=startConsumeUserSignupMessage)
    # await startConsumeUserSignupMessage()
    appointment_thread = threading.Thread(target=startConsumeAppointment)
    patient_discharge_thread = threading.Thread(target=startConsumePatientDischarge)
    signup_user_thread.start()
    appointment_thread.start()
    patient_discharge_thread.start()
    createTable()
    yield


app = FastAPI(lifespan=lifeSpan)
app.add_middleware(CORSMiddleware, allow_origins=['*'], 
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.add_middleware(JwtMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(doctor_router, prefix="/api/v1/doctor", tags=["doctor"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(patient_router, prefix="/api/v1/patient", tags=["patient"])



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0",port=8003, reload=True)
