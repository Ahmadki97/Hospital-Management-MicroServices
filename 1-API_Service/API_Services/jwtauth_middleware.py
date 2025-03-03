from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from Helper_API.errorhandlers import NotAuthorizedError
from jose import JWTError, jwt
from functools import wraps
import os 






# To verify the Protected Routes, Routes that only logged-in users can access
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

def verify_jwt_in_request(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return payload
    except JWTError as err:
        raise NotAuthorizedError(f"Token is not available or invalid. Please login again.", 'GatewayService verifyUser() method')
    

    

def loginJwt(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
       request: Request = kwargs.get('request')
       csrf_token = request.cookies.get('csrf')
       try:
           token_data = kwargs.get('token_data')
           if not token_data:
               raise NotAuthorizedError("Token is not available, Please Login again.")
       except NotAuthorizedError as err:
           raise (f"The Error is {err}")
       
       return await fn(*args, **kwargs)
    return wrapper