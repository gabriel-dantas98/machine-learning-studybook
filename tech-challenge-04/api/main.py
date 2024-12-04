from fastapi import APIRouter

from api.routes import healthcheck, lstm, links
api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
api_router.include_router(lstm.router, prefix="/lstm", tags=["lstm"])
api_router.include_router(links.router, prefix="/links", tags=["links"])
