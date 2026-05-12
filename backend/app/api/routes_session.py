from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.security import create_session_token

router = APIRouter(prefix="/api", tags=["session"])


@router.post("/session")
async def create_session() -> JSONResponse:
    session_token = create_session_token()
    response = JSONResponse({"detail": "session created"})
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_token,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
        max_age=settings.session_ttl_seconds,
        path="/",
    )
    return response