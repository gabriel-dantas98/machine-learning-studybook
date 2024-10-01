from fastapi import APIRouter

from api.routes import iris, healthcheck
api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
api_router.include_router(iris.router, prefix="/iris", tags=["iris"])
