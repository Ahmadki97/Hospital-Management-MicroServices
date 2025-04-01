from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from Helper_Appointment.elastic import checkElasticConnection
from RabbitMq_Appointment.rabbitmq import checkRabbitmqConnection, startConsumeUserSignupMessage
from Services_Appointment.jwtmiddleware import JwtMiddleware
from database import createTable
from Controller_Appointment.get import get_router
from Controller_Appointment.create import create_router
from Controller_Appointment.update import update_router
from Controller_Appointment.delete import delete_router
import uvicorn




@asynccontextmanager
async def lifeSpan(app: FastAPI):
    print("Welcome from lIfeSpan..")
    await checkElasticConnection()
    await checkRabbitmqConnection()
    createTable()
    yield


app = FastAPI(lifespan=lifeSpan)
app.add_middleware(CORSMiddleware, allow_origins=['*'], 
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.add_middleware(JwtMiddleware)
app.include_router(router=get_router, prefix="/api/v1/appointments")
app.include_router(router=create_router, prefix="/api/v1/appointments")
app.include_router(router=update_router, prefix="/api/v1/appointments")
app.include_router(router=delete_router, prefix="/api/v1/appointments")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0",port=8004, reload=True)
