from Helper_API.requesthandler import RequestHandler
from Helper_API.loghandler import logger
from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from dotenv import load_dotenv
import os 



load_dotenv('.env')

appointment_router = APIRouter()
templates = Jinja2Templates(directory="Templates")
appointment_handler = RequestHandler(service_url=os.getenv('APPOINTMENT_BASE_URL'))
admin_handler = RequestHandler(service_url=os.getenv('USERS_BASE_URL'))


@appointment_router.post("/patient-report/{id}")
async def addPatientReport(request: Request, id: int):
    try:
        await appointment_handler.makeRequest(endpoint=f"appointments/patient-report/{id}", service_token='users', request=request)
        return JSONResponse(content={"success": True})
    except Exception as err:
        logger.error(f"Error in addPatientReport() Controller: {err}")
        return JSONResponse("Could not Add Patient Report, Please try again Later..")


