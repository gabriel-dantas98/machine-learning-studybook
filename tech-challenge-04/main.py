from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.main import api_router
from core.config import PROJECT_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url="/openapi.json",
    debug=True
)

FastAPIInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


app.include_router(api_router)

@app.get("/")
def root():
    return RedirectResponse("/docs")
