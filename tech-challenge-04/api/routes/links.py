from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from core.config import MLFLOW_SERVER_URL

router = APIRouter()

@router.get("/mlflow")
def mlflow() -> str:
    return RedirectResponse(MLFLOW_SERVER_URL)
