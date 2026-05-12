from dataclasses import dataclass
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(usecwd=True), override=False)


@dataclass(frozen=True)
class Settings:
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:4321")
    session_secret_key: str = os.getenv("SESSION_SECRET_KEY", ""))
    session_cookie_name: str = os.getenv("SESSION_COOKIE_NAME", "session_token")
    session_ttl_seconds: int = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
    session_cookie_secure: bool = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"


settings = Settings()