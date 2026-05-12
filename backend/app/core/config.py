import os
from dataclasses import dataclass
from urllib.parse import urlparse
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(usecwd=True), override=False)


def _is_local_origin(origin: str) -> bool:
    hostname = urlparse(origin).hostname
    return hostname in {"localhost", "127.0.0.1", "::1"}


@dataclass(frozen=True)
class Settings:
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:4321")
    session_secret_key: str = os.getenv("SESSION_SECRET_KEY", "")
    session_cookie_name: str = os.getenv("SESSION_COOKIE_NAME", "session_token")
    session_ttl_seconds: int = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
    session_cookie_secure: bool = (
        os.getenv("SESSION_COOKIE_SECURE", "").lower() == "true"
        or not _is_local_origin(os.getenv("FRONTEND_ORIGIN", "http://localhost:4321"))
    )
    session_cookie_samesite: str = (
        os.getenv("SESSION_COOKIE_SAMESITE")
        if os.getenv("SESSION_COOKIE_SAMESITE") is not None
        else ("lax" if _is_local_origin(os.getenv("FRONTEND_ORIGIN", "http://localhost:4321")) else "none")
    )


settings = Settings()