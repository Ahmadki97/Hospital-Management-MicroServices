from fastapi import HTTPException, status



class NotAuthorizedError(HTTPException):
    def __init__(self, detail: str = "Not Authorized", *args):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class BadRequestError(HTTPException):
    def __init__(self, detail: str = "Bad Request", *args):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)