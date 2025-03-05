from Helper_API.loghandler import logger
from Helper_API.requesthandler import RequestHandler
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os 


load_dotenv('.env')


templates = Jinja2Templates(directory="Templates")
admin_router = APIRouter()
admin_handler = RequestHandler(service_url=os.getenv('USERS_BASE_URL'))
auth_handler = RequestHandler(service_url=os.getenv('AUTH_BASE_URL'))
appointment_handler = RequestHandler(service_url=os.getenv('APPOINTMENT_BASE_URL'))



####################################Admin Main Views##########################################
@admin_router.get('/dashboard')
async def getDashboard(request: Request):
    print(f"Users Url is : {os.getenv('USERS_BASE_URL')}")
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        admin_data = await admin_handler.makeRequest(endpoint='admin/dashboard', service_token='users', request=request)
        pending_appointments = await appointment_handler.makeRequest(endpoint='appointments/num-pending', service_token='appointments', request=request)
        all_appointments = await appointment_handler.makeRequest(endpoint='appointments/num-all', service_token='appointments', request=request)
        logger.info(f"getDashboard() Controller, Request sent to the Aplicable Service")
        data = {
            "admin": admin,
            "admin_data": admin_data,
            "pending_appointments": pending_appointments,
            "appointments": all_appointments
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name='admin_dashboard.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in getDashboard() Method: {err}")
        return {"message": "Error in getDashboard() process."}
    

@admin_router.get('/admin-doctor')
async def adminGetDoctorView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        print(f"Data is: {data}")        
        return templates.TemplateResponse(request=request, name='admin_doctor.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in adminGetDoctorView() Method: {err}")
        return {"message": "Error in adminGetDoctorView() process."}
    

@admin_router.get('/admin-patient')
async def adminGetPatientView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='admin_patient.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in adminGetPatientView() Method: {err}")
        return {"message": "Error in adminGetPatientView() process."}
    

@admin_router.get('/admin-appointment')
async def adminGetAppointmentView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='admin_appointment.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in adminGetAppointmentView() Method: {err}")
        return {"message": "Error in adminGetAppointmentView() process."}
    

#########################Admin Doctor Views##############################################


@admin_router.get('/doctors')
async def getDoctors(request: Request):
    try:
        doctors = await admin_handler.makeRequest(endpoint='admin/doctors', service_token='users', request=request)
        data = {"doctors": doctors}
        print(f"Data is: {data}")
        return data        
    except Exception as err:
        logger.error(f"Error in getDoctors() Method: {err}")
        return {"message": "Error in getDoctors() process."}
    

@admin_router.get('/working-doctors')
async def getWorkingDoctors(request: Request):
    try:
        working_doctors = await admin_handler.makeRequest(endpoint='admin/working-doctors', service_token='users', request=request)
        print(f"Working Doctors are: {working_doctors}")
        return working_doctors
    except Exception as err:
        logger.error(f"Error in getWorkingDoctors() Method: {err}")
        return {"message": "Error in getWorkingDoctors() process."}
    

@admin_router.get('/admin-view-doctors')
async def adminViewDoctros(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        doctors = await admin_handler.makeRequest(endpoint='admin/doctors', service_token='users', request=request)
        data = {
            "admin": admin,
            "doctors": doctors
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='admin_view_doctor.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in adminViewDoctros() Method: {err}")
        return {"message": "Error in adminViewDoctros() process."}
    

@admin_router.get("/admin-update-doctor")
async def adminUpdateDoctorView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        return templates.TemplateResponse(request=request, name='admin_update_doctor.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in adminUpdateDoctorView() Controller: {err}")
        return {"message": "Error in adminUpdateDoctorView(), please try again later."}
    

@admin_router.post("/admin-update-doctor/{id}")
async def adminUpdateDoctor(request: Request, id: int):
    try:
        await admin_handler.makeRequest(endpoint=f"admin-update-doctor/{id}", service_token='users', request=request) 
    except Exception as err:
        logger.error(f"Error in adminUpdateDoctor() Controller Method: {err}")
        return {"message": "Error in adminUpdateDoctor() process, Please try again later."}
    

@admin_router.get("/admin-delete-doctor/{id}")
async def deleteDoctor(request: Request, id: int):
    try:
        await admin_handler.makeRequest(endpoint=f'admin/admin-delete-doctor/{id}', service_token='users', request=request)
        logger.info(f"deleteDoctor() Controller, Request sent to the Aplicable Service")
        return JSONResponse(f"Doctor was Deleted Successfully")
    except Exception as err:
        logger.error(f"Error in deleteDoctor() Controller Method: {err}")
        return {"message": "Error in deleteDoctor() process, Please try again later."}
    

@admin_router.get('/admin-add-doctor')
async def addDoctorView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        return templates.TemplateResponse(request=request, name='admin_add_doctor.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in addDoctor() Method: {err}")
        return {"message": "Error in addDoctor() process."}
    

@admin_router.post('/admin-add-doctor')
async def addDoctor(request: Request):
    try:
        await auth_handler.makeRequest(endpoint='signup/doctor', service_token='auth', request=request)        
        logger.info(f"signupdoctor() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='/api/v1/users/admin/admin-add-doctor', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in addDoctor() Controller Method: {err}")
        return {"message": "Error in addDoctor() process, Please try again later."}
    
@admin_router.get('/admin-approve-doctor')
async def approveDocor(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        print(f"Admin is: {admin}")
        doctors = await admin_handler.makeRequest(endpoint='admin/pending-doctors', service_token='users', request=request)
        print(f"Doctors are: {doctors}") 
        data = {
            "admin": admin,
            "doctors": list(doctors)
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name='admin_approve_doctor.html', context={"data": data})        
    except Exception as err:
        logger.error(f"Error in approveDocor() Method: {err}")
        return {"message": "Error in approveDocor() process."}
    

@admin_router.put("/approve-doctor/{id}")
async def adminApproveDoctor(id:int, request: Request):
    try:
        await admin_handler.makeRequest(endpoint=f"admin/approve-doctor/{id}", service_token='users', request=request)
        logger.info(f"approveDoctor() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='/api/v1/users/admin/admin-approve-doctor', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in approveDoctor() Controller Method: {err}")
        return {"message": "Error in approveDoctor() process, Please try again later."}
    

@admin_router.delete("/decline-doctor/{id}")
async def adminDeclineDoctor(id: int, request: Request):
    try:
        await admin_handler.makeRequest(endpoint=f"admin/decline-doctor/{id}", service_token='users', request=request)
        logger.info(f"declineDoctor() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='/api/v1/users/admin/admin-approve-doctor', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in declineDoctor() Controller Method: {err}")
        return {"message": "Error in declineDoctor() process, Please try again later."}
    
    

@admin_router.get('/admin-doctor-specialization')
async def doctorSpecializationView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        doctors = await admin_handler.makeRequest(endpoint='admin/doctors', service_token='users', request=request) 
        data = {
            "admin": admin,
            "doctors": doctors
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name='admin_view_doctor_Specialisation.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in doctorSpecializationView() Method: {err}")
        return {"message": "Error in doctorSpecializationView() process."}
    

@admin_router.get("/timeslots/{id}")
async def getDoctorTimeSlots(id: int, request: Request):
    try:
        time_slots = await admin_handler.makeRequest(endpoint=f"admin/timeslots/{id}", service_token='users', request=request)
        print(f"Timeslots are: {time_slots}")
        return JSONResponse(time_slots)
    except Exception as err:
        logger.error(f"Error in getDoctorTimeSlots() Method: {err}")
        return {"message": "Error in getDoctorTimeSlots() process."}
    
    


###################################Admin Patient Views#################################


@admin_router.get('/patients')
async def getPatients(request: Request):
    try:
        patients = await admin_handler.makeRequest(endpoint='admin/patients', service_token='users', request=request)
        data = {
            "patients": patients
        }
        print(f"patients are: {patients}")
        return data
    except Exception as err:
        logger.error(f"Error in getDoctors() Method: {err}")
        return {"message": "Error in getDoctors() process."}

@admin_router.get('/admin-view-patients')
async def adminViewPatients(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        print(f"Admin is: {admin}")
        patients = await admin_handler.makeRequest(endpoint='admin/patients', service_token='users', request=request)
        print(f"Patients are: {patients}") 
        data = {
            "admin": admin,
            "patients": patients
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name='admin_view_patient.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in adminViewPatients() Method: {err}")
        return {"message": "Error in adminViewPatients() process."}
    

@admin_router.get('/admin-add-patient')
async def addPatientView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='admin_add_patient.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in addPatient() Method: {err}")
        return {"message": "Error in addPatient() process."}
    

@admin_router.post('/admin-add-patient')
async def addPatient(request: Request):
    try:
        await auth_handler.makeRequest(endpoint='signup/patient', service_token='auth', request=request)
        return RedirectResponse(url='/api/v1/users/admin/admin-add-patient', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in addPatient() Controller Method: {err}")
        return {"message": "Error in addPatient() process, Please try again later."}
    

@admin_router.get('/admin-approve-patient')
async def approvePatientView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        print(f"Admin is: {admin}")
        patients = await admin_handler.makeRequest(endpoint='admin/pending-patients', service_token='users', request=request)
        print(f"Patients are: {patients}") 
        data = {
            "admin": admin,
            "patients": patients
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name='admin_approve_patient.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in approvePatientView() Method: {err}")
        return {"message": "Error in approvePatientView() process."}
    

@admin_router.put("/approve-patient/{id}")
async def adminApprovePatient(id: int, request: Request):
    try:
        await admin_handler.makeRequest(endpoint=f"admin/approve-patient/{id}", service_token='users', request=request)
        logger.info(f"approvePatient() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='/api/v1/users/admin/admin-approve-patient', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in approvePatient() Controller Method: {err}")
        return {"message": "Error in approvePatient() process, Please try again later."}
    

@admin_router.delete("/decline-patient/{id}")
async def adminDeclinePatient(id: int, request: Request):
    try:
        await admin_handler.makeRequest(endpoint=f"admin/decline-patient/{id}", service_token='users', request=request)
        logger.info(f"declinePatient() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='/api/v1/users/admin/admin-approve-patient', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in declinePatient() Controller Method: {err}")
        return {"message": "Error in declinePatient() process, Please try again later."}
    

@admin_router.get("/admin-discharge-patient")
async def adminDischargePatientView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        print(f"Admin is: {admin}")
        patients = await admin_handler.makeRequest(endpoint='admin/patients', service_token='users', request=request)
        print(f"Patients are: {patients}") 
        data = {
            "admin": admin,
            "patients": list(patients)
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name='admin_discharge_patient.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in adminDischargePatientView() Method: {err}")
        return {"message": "Error in adminDischargePatientView() process."}
    

@admin_router.get("/discharge-patient/{id}")
async def dischargePatientView(id: int, request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        patient = await admin_handler.makeRequest(endpoint=f"admin/patient/{id}", service_token='users', request=request)
        data = {
            "admin": admin,
            "patient": patient
        }
        print(f"Data is: {data}")
        return templates.TemplateResponse(request=request, name='patient_discharge.html', context={"data": data})
    except Exception as err:
        logger.error(f"Error in dischargePatientView() Controller Method: {err}")
        return {"message": "Error in dischargePatientView() process, Please try again later."}


@admin_router.post("/discharge-patient/{id}")
async def dischargePatient(id: int, request: Request):
    try:
        await admin_handler.makeRequest(endpoint=f"admin/discharge-patient/{id}", service_token='users', request=request)
        logger.info(f"dischargePatient() Controller, Request sent to the Aplicable Service")
        return JSONResponse(content="Patient Discharged Successfully..", status_code=status.HTTP_200_OK)
    except Exception as err:
        logger.error(f"Error in dischargePatient() Controller Method: {err}")
        return {"message": "Error in dischargePatient() process, Please try again later."}
    

################################Admin Appointment Views#######################################


@admin_router.get('/admin-view-appointments')
async def adminViewAppointments(request: Request):
    appointments= await appointment_handler.makeRequest(endpoint='appointments/appointments', service_token='appointment', request=request)
    admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
    #appointments = appointments_response.get('appointments', []) if 'appointments' in appointments_response else []
    data = {
        "admin": admin,
        "appointments": appointments
    }
    print(f"Data is {data}")
    return templates.TemplateResponse(request=request, name='admin_view_appointment.html', context={"data": data})

@admin_router.get("/admin-add-appointment", name="add-appointment")
async def addAppointmentView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        data = {
            "admin": admin
        }
        return templates.TemplateResponse(name='admin_add_appointment.html', context={"data": data}, request=request) 
    except Exception as err:
        logger.error(f"Error in createAppointment() Controller: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error in createAppointment() process."})
    

@admin_router.post("/admin-add-appointment")
async def addAppointment(request: Request):
    try:
        await appointment_handler.makeRequest(endpoint="appointments/create-appointment", service_token='appointment', request=request)
        return JSONResponse("New Appointment Created Succefully.") 
    except Exception as err:
        logger.error(f"Error in createAppointment() Controller: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error in createAppointment() process."})
    

@admin_router.get('/admin-approve-appointment')
async def approveAppointmentView(request: Request):
    try:
        admin = await admin_handler.makeRequest(endpoint='admin/get-admin', service_token='users', request=request)
        appointments = await appointment_handler.makeRequest(endpoint='appointments/pending', service_token='appointments', request=request)
        data = {
            "admin": admin,
            "appointments": appointments
        }
        print(f"Data is {data}")
        return templates.TemplateResponse(request=request, name="admin_approve_appointment.html", context={"data": data})
    except Exception as err:
        logger.error(f"Error in approveAppointmentView() Method: {err}")
        return {"message": "Error in approveAppointmentView() process."}
    

@admin_router.put("/admin-approve-appointment/{id}")
async def approveAppointment(id: int, request: Request):
    try:
        await appointment_handler.makeRequest(endpoint=f"appointments/approve-appointment/{id}", service_token='appointments', request=request)
        return RedirectResponse(url="/api/v1/users/admin/admin-approve-appointment", status=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in approveAppointment() Controller Method: {err}")
        return {"message": "Error in approveAppointment() process, Please try again later."}
    

@admin_router.delete("/admin-decline-appointment/{id}")
async def declineAppointment(id: int, request: Request):
    try:
        await appointment_handler.makeRequest(endpoint=f"appointments/decline-appointment/{id}", service_token="appointments", request=request)
        return RedirectResponse(url="/api/v1/users/admin/admin-approve-appointments", status=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in declineAppointment() Controller Method: {err}")
        return {"message": "Error in declineAppointment() process, Please try again later."}