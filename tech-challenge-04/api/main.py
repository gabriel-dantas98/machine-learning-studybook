from fastapi import APIRouter

from api.routes import healthcheck, lstm
api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
api_router.include_router(lstm.router, prefix="/lstm", tags=["lstm"])
