from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.security import create_session_token

router = APIRouter(prefix="/api", tags=["session"])


@router.post("/session")
async def create_session(request: Request) -> JSONResponse:
    """Create a session cookie. For local HTTP requests (tests/dev) avoid setting the Secure flag so
    the cookie is sent over plain HTTP; in production the `settings.session_cookie_secure` controls this.
    """
    session_token = create_session_token()
    response = JSONResponse({"detail": "session created"})

    # If the incoming request is over HTTP, do not force the Secure flag even if settings recommend it.
    secure_flag = settings.session_cookie_secure and request.url.scheme == "https"

    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_token,
        httponly=True,
        secure=secure_flag,
        samesite=settings.session_cookie_samesite,
        max_age=settings.session_ttl_seconds,
        path="/",
    )
    return response