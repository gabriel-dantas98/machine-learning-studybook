from fastapi import APIRouter

from api.routes import healthcheck, news, links, users, recommend, raw_data

api_router = APIRouter()

api_router.include_router(healthcheck.router, prefix="/healthcheck", tags=["internal"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
api_router.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
api_router.include_router(raw_data.router, prefix="/raw_data", tags=["raw_data"])
api_router.include_router(links.router, prefix="/links", tags=["links"])
