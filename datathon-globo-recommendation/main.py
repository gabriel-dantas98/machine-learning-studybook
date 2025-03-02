from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.main import api_router
from core.config import PROJECT_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from core.database import get_database, engine, Base

Base.metadata.create_all(engine)

app = FastAPI(title=PROJECT_NAME, openapi_url="/openapi.json", debug=True)

FastAPIInstrumentor().instrument_app(app)

get_database()

app.include_router(api_router)


@app.get("/")
def root():
    return RedirectResponse("/docs")
