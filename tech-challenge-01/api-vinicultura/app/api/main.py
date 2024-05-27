from fastapi import APIRouter

from api.routes import production, processing, importing, exporting, download, commercialization, healthcheck
api_router = APIRouter()

api_router.include_router(production.router, prefix="/production", tags=["production"])
api_router.include_router(processing.router, prefix="/processing", tags=["processing"])
api_router.include_router(importing.router, prefix="/importing", tags=["importing"])
api_router.include_router(exporting.router, prefix="/exporting", tags=["exporting"])
api_router.include_router(commercialization.router, prefix="/commercialization", tags=["commercialization"])
api_router.include_router(download.router, prefix="/download", tags=["download"])
api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
