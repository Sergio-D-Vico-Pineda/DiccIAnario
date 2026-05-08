from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_validate import router as validate_router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Validador Lingüístico Inteligente", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(validate_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}