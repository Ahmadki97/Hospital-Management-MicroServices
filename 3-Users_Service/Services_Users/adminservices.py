from Helper_Users.loghandler import logger
from Models_Users.models import Admin, Patient, Doctor
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def createAdmin(admin: dict, db: Session):
    try:
        admin = Admin(**admin)
        db.add(admin)
        db.commit()
        logger.info(f"createAdmin() Method, admin with id {admin.id} created successfully..")
    except Exception as err:
        logger.error(f"Error in createAdmin() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


async def getAdminById(id: int, db: Session):
    try:
        admin = db.query(Admin).filter(Admin.id == id).first()
        if admin is None:
            logger.info(f"getAdminById() Method, admin with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return admin.to_dict()
    except Exception as err:
        logger.error(f"Error in getAdminById() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getAdminByUsername(username: str, db: Session):
    try:
        admin = db.query(Admin).filter(Admin.username == username).first()
        if admin is None:
            logger.info(f"getAdminByUsername() Method, admin with username {username} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return admin
    except Exception as err:
        logger.error(f"Error in getAdminByUsername() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    




    

