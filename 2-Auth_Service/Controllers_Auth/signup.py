from Helper_Auth.loghandler import logger
from sqlalchemy.orm import Session
from Helper_Auth.verifytoken import jwt_required
from Helper_Auth.rabbitmq import startPuplishingMessage
from Helper_Auth.cloudinary import uploadPhoto
from Services_Auth.authservices import createAuthUser
from Models_Auth.Users import User
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import RedirectResponse, JSONResponse
# from urllib.parse import parse_qs
from fastapi import status, UploadFile, File
from dotenv import load_dotenv
from databas import get_db
import json
import os 


load_dotenv('.env')

signup_router = APIRouter()
templates = Jinja2Templates(directory="Templates")



# @signup_router.get('/admin', name='getSignupAdmin')
# # jwt_required
# async def adminPage(request: Request):
#     try:
#         return templates.TemplateResponse(request=request, name='adminsignup.html') 
#     except Exception as err:
#         logger.error(f"Error in adminPage() Controller Method: {err}")
#         return {"message": "Error in adminPage() process."}


@signup_router.post("/admin", name="signupAdmin")
@jwt_required
async def admin(request: Request, db: Session = Depends(get_db), profile_pic: UploadFile=File(None)):
    try:
        data = await request.form()
        user = db.query(User).filter(User.username==data['username']).first()
        if user is not None:
            logger.info(f"sinup admin() Controller, User Already exists")
            return JSONResponse(f"User Already exists")
        else:
            if profile_pic is not None:
                file = await profile_pic.read()
                print(f"Type of the profile_pic is {type(file)}")
                pic = await uploadPhoto(file=file)
            user_create = {
                "first_name": data.get('first_name'),
                "last_name": data.get('last_name'),
                "username": data.get('username'),
                "email": data.get('email'),
                "password": data.get('password'),
                "profile_pic": pic,
                "address": data.get('address'),
            }
            user = await createAuthUser(user_create=user_create, db=db)
            logger.info(f"signupAdmin() Controller Method, Admin user created successfully.")
            user_create['user_type'] = 'admin'
            del user_create['password']
            del user_create['email']
            user_create['id'] = user.id
            print(f"User_create is: {user_create}")
            await startPuplishingMessage(queue='user-signup', exchange_name='', routing_key='user-signup', body=json.dumps(user_create))
            # return RedirectResponse(url=f"{os.getenv('API_BASE_URL')}/api/v1/auth/login/admin", status_code=303)
            return True
    except Exception as err:
        logger.error(f"Error in signupAdmin() Controller Method: {err}")
        return {"message": "Error in signupAdmin() process."}




# @signup_router.get('/doctor', name='getSignupDoctor')
# @jwt_required
# async def doctorPage(request: Request):
#     try:
#         return templates.TemplateResponse(request=request, name="doctorsignup.html")
#     except Exception as err:
#         logger.error(f"Error in doctorPage() Controller Method: {err}")
#         return {"message": "Error in doctorPage() process."}
    

@signup_router.post('/doctor', name="signupDoctor")
@jwt_required
async def doctor(request: Request, db: Session = Depends(get_db), profile_pic: UploadFile = File(None)):
    try:
        data = await request.form()
        user = db.query(User).filter(User.username==data['username']).first()
        print(f"The user is: {user}")
        if user is not None:
            logger.info(f"sinup doctor() Controller, User Already exists")
            return JSONResponse(f"User Already exists")
        else:
            if profile_pic is not None:
                file = await profile_pic.read()
                print(f"Type of the profile_pic is {type(file)}")
                pic = await uploadPhoto(file=file)
            user_create = {
                "first_name": data.get('first_name'),
                "last_name": data.get('last_name'),
                "username": data.get('username'),
                "email": data.get('email'),
                "password": data.get('password'),
                "profile_pic": pic,
                "address": data.get('address'),
            }
            user = await createAuthUser(user_create=user_create, db=db)
            work_days = []
            start_time =[]
            hours = []
            for key, value in data.items():
                if key.startswith('work_days'):
                    day = key.split('[')[1].split(']')[0]
                    if day not in work_days:  # Extracts 'sunday'
                        work_days.append(day)
                    field = key.split('[')[2].split(']')[0]
                    if field == 'start_time':
                      start_time.append(value)
                    elif field == 'hours':
                        hours.append(value)
            print(f"doctor work times are: {work_days}, {start_time}, {hours}")  
            print(f"Work Days are: {work_days}")
            logger.info(f"signupDoctor() Controller Method, Doctor user created successfully.")
            user_create['user_type'] = 'doctor'
            del user_create['password']
            del user_create['email']
            user_create['department'] = data.get('department')
            user_create['mobile'] = data.get('mobile')
            user_create['id'] = user.id
            user_create['work_days'] = work_days
            user_create['work_hours'] = hours
            user_create['work_start'] = start_time
            print(f"User_create is: {user_create}")
            await startPuplishingMessage(queue='user-signup', exchange_name='', routing_key='user-signup', body=json.dumps(user_create))
    except Exception as err:
        logger.error(f"Error in signupDoctor() Controller Method: {err}")
        return {"message": "Error in signupDoctor() process."}
    
    

# @signup_router.get('/patient', name='getSignupPatient')   
# # @jwt_required
# async def patienPage(request: Request):
#     try:
#         return templates.TemplateResponse(request=request, name="patientsignup.html")
#     except Exception as err:
#         logger.error(f"Error in patientPage() Controller Method: {err}")
#         return {"message": "Error in patientPage() process."}


@signup_router.post("/patient", name="signupPatient")
# @jwt_required
async def patient(request: Request, db: Session = Depends(get_db), profile_pic: UploadFile = File(None)):
    try:
        form_data = await request.form()
        if profile_pic is not None:
            file = await profile_pic.read()
            pic = await uploadPhoto(file)
        user_create = {
            "first_name": form_data.get('first_name'),
            "last_name": form_data.get('last_name'),
            "username": form_data.get('username'),
            "email": form_data.get('email'),
            "password": form_data.get('password'),
            "profile_pic": pic,
            "address": form_data.get('address'),
        }
        user = await createAuthUser(user_create=user_create, db=db)
        user_create['user_type'] = 'patient'
        user_create['id'] = user.id
        user_create['mobile'] = form_data.get('mobile')
        user_create['symptoms'] = form_data.get('symptoms')
        del user_create['password']
        del user_create['email']
        logger.info(f"signupPatient() Controller Method, Patient user created successfully.")
        await startPuplishingMessage(queue='user-signup', exchange_name='', routing_key='user-signup', body=json.dumps(user_create))
    except Exception as err:
        logger.error(f"Error in signupPatient() Controller Method: {err}")
        return {"message": "Error in signupPatient() process."}



            