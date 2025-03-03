from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/repository")
def github_path() -> str:
    return RedirectResponse("https://github.com/gabriel-dantas98/machine-learning-studybook/blob/main/datathon-globo-recommendation/README.md")
