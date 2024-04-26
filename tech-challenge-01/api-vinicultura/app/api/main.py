from fastapi import APIRouter

from api.routes import production

api_router = APIRouter()
api_router.include_router(production.router, prefix="/production", tags=["items"])
