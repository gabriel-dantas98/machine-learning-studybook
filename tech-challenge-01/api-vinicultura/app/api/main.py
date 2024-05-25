from fastapi import APIRouter

from api.routes import production, processing, importing, exporting, download, commercialization, healthcheck
api_router = APIRouter()

api_router.include_router(production.router, prefix="/production", tags=["items"])
api_router.include_router(processing.router, prefix="/processing", tags=["items"])
api_router.include_router(importing.router, prefix="/importing", tags=["items"])
api_router.include_router(exporting.router, prefix="/exporting", tags=["items"])
api_router.include_router(download.router, prefix="/download", tags=["items"])
api_router.include_router(commercialization.router, prefix="/commercialization", tags=["items"])
api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
