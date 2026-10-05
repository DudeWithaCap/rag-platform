from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import Settings
from app.api.documents import router as documents_router

settings = Settings()
app = FastAPI(title=settings.app_name)
app.include_router(documents_router)

class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Confirm that the backend can serve requests."""
    return HealthResponse()
