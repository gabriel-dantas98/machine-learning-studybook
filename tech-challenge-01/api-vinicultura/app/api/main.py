from fastapi import APIRouter

from api.routes import production, healthcheck
api_router = APIRouter()

api_router.include_router(production.router, prefix="/production", tags=["items"])
api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
