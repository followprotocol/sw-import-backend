from fastapi import APIRouter
from api.routes_v1.captcha import captcha
from api.routes_v1.getinfo import getinfo

api_routes = APIRouter()

api_routes.include_router(captcha.router, prefix="/api/v1", tags=["Captcha"])
api_routes.include_router(getinfo.router, prefix="/api/v1", tags=["Get Player information"])