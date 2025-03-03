from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
# from pydantic_settings import BaseSettings
from Controllers_API.home import api_service_router
from Helper_API.elastic import elastic_connection
from Controllers_API.Auth_Service.authservice import auth_router
from Controllers_API.Users_Service.doctor import doctor_router
from Controllers_API.Users_Service.admin import admin_router
from Controllers_API.Users_Service.patient import patient_router
from Controllers_API.Appointment_Service.appointment import appointment_router
import uvicorn




@asynccontextmanager
async def lifeSpan(app: FastAPI):
    elastic_connection.checkElasticsearchConnection()
    yield

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], 
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_service_router, prefix="/api/v1/home", tags=["home"])
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(doctor_router, prefix="/api/v1/users/doctor", tags=["doctor"])
app.include_router(admin_router, prefix="/api/v1/users/admin", tags=["admin"])
app.include_router(patient_router, prefix="/api/v1/users/patient", tags=["patient"])
app.include_router(appointment_router, prefix="/api/v1/appointment", tags=["appointment"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)