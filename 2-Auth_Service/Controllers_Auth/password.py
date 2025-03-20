from Helper_Auth.loghandler import logger
from Helper_Auth.verifytoken import jwt_required
from Services_Auth.authservices import passwordResetToken, updateAuthUserPassword
from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from databas import get_db



password_router = APIRouter()
templates = Jinja2Templates(directory="Templates")

@password_router.put('/change/<int:id>', name="change_password")
@jwt_required
async def change(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        old_password = form_data.get('old_password')
        new_password = form_data.get('new_password')
        await updateAuthUserPassword(id=id, old_password=old_password, new_password=new_password, db=db)
        return (f"Password for user with id {id} changed successfully.")
    except Exception as err:
        logger.error(f"Error in changepassword() Controller: {err}")
        return(f"Could not change password for user with id {id}, please try again.")
    

@password_router.put('/reset', name="Reset Password")
@jwt_required
async def reset(request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        email = form_data.get('email')
        await passwordResetToken(email=email, db=db)
        return(f"Password reset link sent to your email.") 
    except Exception as err:
        logger.error(f"Error in resetPassword() Controller: {err}")
        return(f"Could not reset password, please try again later.")