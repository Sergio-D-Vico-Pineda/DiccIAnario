from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse

from app.api.routes_validate import router as validate_router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Validador Lingüístico Inteligente", version="1.0.0")

# Extract hostname from frontend_origin URL for TrustedHostMiddleware
frontend_hostname = urlparse(settings.frontend_origin).netloc or "localhost:4321"
# Allow both the frontend origin and localhost for development
allowed_hosts = [frontend_hostname, "localhost", "localhost:8000", "127.0.0.1"]

# Security middleware: only allow requests from trusted origins
# Note: This validates the Host header to prevent Host Header Injection attacks
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(validate_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}