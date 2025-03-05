from Helper_API.loghandler import logger
from Helper_API.requesthandler import RequestHandler
from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from dotenv import load_dotenv
import os 


load_dotenv('.env')


templates = Jinja2Templates(directory="Templates")
doctor_router = APIRouter()
doctor_handler = RequestHandler(service_url=os.getenv('USERS_BASE_URL'))
auth_handler = RequestHandler(service_url=os.getenv('AUTH_BASE_URL'))
appointment_handler = RequestHandler(service_url=os.getenv('APPOINTMENT_BASE_URL'))

@doctor_router.get('/dashboard')
async def getDashboard(request: Request):
    print(f"Users Url is : {os.getenv('USERS_BASE_URL')}")
    try:
        data = await doctor_handler.makeRequest(endpoint='doctor/dashboard', service_token='users', request=request)
        appointment_data = await appointment_handler.makeRequest(endpoint='appointments/doctor/appointments', service_token='appointments', request=request)
        print(f"Data is: {data}")
        data = {
            "doctor": data,
            "appointments": appointment_data,
        }
        print(f"Data is: {data}")
        logger.info(f"getDashboard() Controller, Request sent to the Aplicable Service")
        return templates.TemplateResponse(request=request, name='doctor_dashboard.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in getDashboard() Method: {err}")
        return {"message": "Error in getDashboard() process."}
    

@doctor_router.get('/appointments')
async def getAppointments(request: Request):
    try:
        # Fetch doctor and appointments data
        doctor = await doctor_handler.makeRequest(endpoint='doctor/get-doctor', service_token='users', request=request)
        appointments = await appointment_handler.makeRequest(endpoint='appointments/doctor/appointments', service_token='users', request=request)
        # Add patient details to each appointment
        for appointment in appointments:
            patient = next((p for p in doctor['patients'] if p['id'] == appointment['patient_id']), None)
            if patient:
                appointment['mobile'] = patient['mobile']
                appointment['address'] = patient['address']
        # Combine the data
        data = {
            "doctor": doctor,
            "appointments": appointments,
        }

        print(f"Data in Appointments: {data}")
        logger.info(f"getAppointments() Controller, Request sent to the Applicable Service")
        return templates.TemplateResponse(
            request=request,
            name='doctor_view_appointment.html',
            context={"data": data}
        )
    except Exception as err:
        logger.error(f"Error in getAppointments() Method: {err}")
        return {"message": "Error in getAppointments() process."}

    

@doctor_router.get('/doctor-patients')
async def getPatientsView(request: Request):
    try:
        doctor = await doctor_handler.makeRequest(endpoint='doctor/get-doctor', service_token='users', request=request)
        data = {
            "doctor": doctor,
        }
        print(f"Data is {data}")
        logger.info(f"getPatients() Controller, Request sent to the Aplicable Service")
        return templates.TemplateResponse(request=request, name='doctor_patient.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getPatients() Method: {err}")
        return {"message": "Error in getPatients() process."}
    

@doctor_router.get('/doctor-patients-record')
async def getPatients(request: Request):
    try:
        doctor = await doctor_handler.makeRequest('doctor/get-doctor', service_token='users', request=request)
        # patients = await doctor_handler.makeRequest(endpoint='doctor/patients', service_token='users', request=request)
        data = {
            "doctor": doctor,
            # "patients": patients
        }
        print(f"Data is {data}")
        logger.info(f"getPatientsRecord() Controller, Request sent to the Aplicable Service")
        return templates.TemplateResponse(request=request, name='doctor_view_patient.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getPatients Controller: {err}")
        return JSONResponse("Could not View Patients, Please try again Later..")
    

@doctor_router.get('/discharged-patients')
async def getDischargedPatients(request: Request):
    try:
        doctor = await doctor_handler.makeRequest(endpoint='doctor/get-doctor', service_token='users', request=request)
        data = {
            "doctor": doctor,
        }
        print(f"Data is: {data}")
        logger.info(f"getDischargedPatients() Controller, Request Sent to applicable service")
        return templates.TemplateResponse(request=request, name='doctor_view_discharge_patient.html', context={"data": data}) 
    except Exception as err:
        logger.error(f"Error in getDischargedPatients() Controller: {err}")
        return JSONResponse("Could not Get Discharged Patients, Please try again Later..")
    


# @doctor_router.get("/patient-report/")
# async def getPatientReport(request: Request):
#     try:
#         doctor = await doctor_handler.makeRequest(endpoint=f"doctor/get-doctor", service_token='users', request=request)
#         data = {
#             "doctor": doctor
#         }
#         return templates.TemplateResponse(request=request, name='doctor_add_report.html', context={"data": data})
#     except Exception as err:
#         logger.error(f"Error in getPatientReport() Controller: {err}")
#         return JSONResponse("Could not Get Patient Report, Please try again Later..")
    


@doctor_router.get('/doctor-timeslots-view')
async def getDoctorTimeslotsView(request: Request):
    try:
        doctor = await doctor_handler.makeRequest(endpoint='doctor/get-doctor', service_token='users', request=request)
        data = {
            "doctor": doctor,
        }
        logger.info(f"getDoctorTimeslotsView() Controller, Request Sent to applicable service")
        return templates.TemplateResponse(request=request, name='doctor_timeslot_view.html', context={"data": data}) 
    except Exception as err:
        logger.error(f"Error in getDoctorTimeslots() Controller: {err}")
        return JSONResponse("Could not Get Timeslots View, Please try again Later..")
    

@doctor_router.get('/doctor-timeslots')
async def getDoctorTimeSlots(request: Request):
    try:
        doctor = await doctor_handler.makeRequest(endpoint='doctor/get-doctor', service_token='users', request=request)
        slots = await doctor_handler.makeRequest(endpoint='doctor/timeslots', service_token='users', request=request)
        data = {
            "doctor":doctor,
            "slots": slots
        }
        print(f"Data is: {data}")
        logger.info(f"getDoctorTimeslots() Controller, Request Sent to applicable service")
        return templates.TemplateResponse(request=request, name='doctor_view_timeslots.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in getDoctorTimeslots() Controller: {err}")
        return JSONResponse("Could not get Doctor Timeslots, please Try again later")
    

@doctor_router.get("/add-timeslot")
async def addDoctorTimeSlotView(request: Request):
    try:
        doctor = await doctor_handler.makeRequest(endpoint='doctor/get-doctor', service_token='users', request=request)
        data = {
            "doctor": doctor,
        }
        return templates.TemplateResponse(request=request, name='doctor_add_timeslot_view.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in addDoctorTimeSlotView() Controller: {err}")
        return JSONResponse("Could not Add Timeslot, Please try again later")
    

@doctor_router.post("add-timeslot")
async def addDoctorTimeSlot(request: Request):
    try:
        await appointment_handler.makeRequest(endpoint='doctor/add-timeslot', service_token='users', request=request)
        logger.info(f"addDoctorTimeSlot() Controller, Request Sent to applicable service")
        return RedirectResponse(url='api/v1/users/doctor/add-timeslot', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in addDoctorTimeSlot() Controller: {err}")
        return JSONResponse("Could not Add Timeslot, Please try again later")
    

@doctor_router.delete("/delete-timeslot/{id}")
async def deleteDoctorTimeSlot(id: int, request: Request):
    try:
        await doctor_handler.makeRequest(endpoint=f"doctor/delete-timeslot/{id}", service_token='users', request=request)
        logger.info(f"deleteDoctorTimeSlot() Controller, Request Sent to applicable service")
        return 
    except Exception as err:
        logger.error(f"Error in deleteDoctorTimeSlot() Controller: {err}")
        return JSONResponse("Could not Delete Timeslot, Please Try again later")