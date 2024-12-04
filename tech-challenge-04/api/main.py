from fastapi import APIRouter

from api.routes import healthcheck, lst
api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
api_router.include_router(lst.router, prefix="/lst", tags=["lst"])
