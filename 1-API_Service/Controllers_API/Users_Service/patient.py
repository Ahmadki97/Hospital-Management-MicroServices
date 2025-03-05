from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from Helper_API.requesthandler import RequestHandler
from Helper_API.loghandler import logger
from dotenv import load_dotenv
import os 


load_dotenv('.env')



templates = Jinja2Templates(directory="Templates")
patient_router = APIRouter()
patient_handler = RequestHandler(service_url=os.getenv('USERS_BASE_URL'))
appointment_handler = RequestHandler(service_url = os.getenv('APPOINTMENT_BASE_URL'))


@patient_router.get('/get-patient')
async def getPatient(request: Request):
    try:
        patient = await patient_handler.makeRequest(endpoint='patient/get-patient', service_token='users', request=request)
        data = {
            "patient": patient
        }
        return data
    except Exception as err:
        logger.error(f"Error in getPatient() Controller: {err}")
        return {"message": "Error in getPatient() process."}


@patient_router.get('/dashboard')
async def getDashboard(request: Request):
    try:
        data = await patient_handler.makeRequest(endpoint='patient/dashboard', service_token='users', request=request)        
        print(f"Data is: {data}")
        logger.info(f"getDashboard() Controller, Request sent to the Aplicable Service")
        return templates.TemplateResponse(request=request, name='patient_dashboard.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getDashboard() Controller: {err}")
        return {"message": "Error in getDashboard() process."}
    

@patient_router.get('/appointments')
async def getAppointmentsView(request: Request):
    try:
        patient = await patient_handler.makeRequest(endpoint='patient/get-patient', service_token='users', request=request)
        logger.info(f"getAppointments() Controller, Request sent to the Aplicable Service")
        data = {
            "patient": patient
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='patient_appointment.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getAppointments() Controller: {err}")
        return {"message": "Error in getAppointments() process."}
    

@patient_router.get('/show-appointments')
async def getAppointments(request: Request):
    try:
        patient = await patient_handler.makeRequest(endpoint='patient/get-patient', service_token='users', request=request)
        appointments = await appointment_handler.makeRequest(endpoint='appointments/patient/appointments', service_token='appointment', request=request)
        logger.info(f"getAppointments() Controller, Request sent to applicable service")
        data = {
            "patient": patient,
            "appointments": appointments
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='patient_view_appointment.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getAppointments() Controller: {err}")
        return {"message": "Error in getAppointments() process."}
    

@patient_router.get('/book-appointment')
async def bookAppointmentView(request: Request):
    try:
        patient = await patient_handler.makeRequest(endpoint='patient/get-patient', service_token='users', request=request)
        data = {
            "patient": patient
        }
        return templates.TemplateResponse(request=request, name="patient_book_appointment.html", context={"data": data}) 
    except Exception as err:
        logger.error(f"Error in bookAppointmentView() Controller: {err}")
        return {"message": "Error in bookAppointmentView() process, Please try again later.."}
    


@patient_router.post('/patient-add-appointment')
async def bookAppointment(request: Request):
    try:
        await appointment_handler.makeRequest(endpoint="appointments/create-appointment", service_token="appoiintment", request=request)
        return JSONResponse("New Appointment Created Succefully.")
    except Exception as err:
        logger.error(f"Error in bookAppointment() Controller: {err}")
        return {"message": "Error in bookAppointment() process, Please try again later.."}



@patient_router.get("/doctors")
async def getDoctorsView(request: Request):
    try:
        patient = await patient_handler.makeRequest(endpoint='patient/get-patient', service_token='users', request=request)
        doctors = await patient_handler.makeRequest(endpoint="admin/doctors", service_token='users', request=request)
        data = {
            "patient": patient,
            "doctors": doctors
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='patient_view_doctor.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getDoctorsView() Controller: {err}")
        return {"message": "Error in getDoctorsView() process, Please try again later.."}
    

@patient_router.get("/patient-discharge")
async def dischargePatientView(request: Request):
    try:
        patient = await patient_handler.makeRequest(endpoint="patient/get-patient", service_token='users', request=request)
        data = {
            "patient": patient
        }
        return templates.TemplateResponse(request=request, name='patient_discharge.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in dischargePatientView() Controller: {err}")
        return {"message": "Error in dischargePatientView() process, Please try again later.."}