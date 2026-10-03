from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import Settings


settings = Settings()
app = FastAPI(title=settings.app_name)


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Confirm that the backend can serve requests."""
    return HealthResponse()
