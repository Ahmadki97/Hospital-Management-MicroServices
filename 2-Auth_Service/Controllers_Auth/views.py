from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates


auth_service_views_router = APIRouter()
templates = Jinja2Templates(directory="Templates")

@auth_service_views_router.get("/patient-click", name='patient-click')
async def view_patien_login(request: Request):
    return templates.TemplateResponse(request=request, name="patientclick.html")