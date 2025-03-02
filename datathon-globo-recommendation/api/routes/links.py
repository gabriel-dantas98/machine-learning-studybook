from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/github")
def mlflow() -> str:
    return RedirectResponse("www.github.com")
