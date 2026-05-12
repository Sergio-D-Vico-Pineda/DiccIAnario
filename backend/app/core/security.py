import base64
import hashlib
import hmac
import json
import time

from fastapi import Cookie, HTTPException, status

from app.core.config import settings



def _base64url_encode(raw_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(raw_bytes).rstrip(b"=").decode("ascii")


def _base64url_decode(encoded_value: str) -> bytes:
    padding = "=" * (-len(encoded_value) % 4)
    return base64.urlsafe_b64decode(encoded_value + padding)


def create_session_token() -> str:
    if not settings.session_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session secret key not configured on server",
        )

    issued_at = int(time.time())
    payload = {"iat": issued_at, "exp": issued_at + settings.session_ttl_seconds}
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_segment = _base64url_encode(payload_bytes)
    signature = hmac.new(
        settings.session_secret_key.encode("utf-8"),
        payload_segment.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return f"{payload_segment}.{_base64url_encode(signature)}"


def verify_session_token(session_token: str | None = Cookie(default=None, alias="session_token")) -> str:
    if not settings.session_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session secret key not configured on server",
        )

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing session cookie",
        )

    try:
        payload_segment, signature_segment = session_token.split(".", 1)
        expected_signature = hmac.new(
            settings.session_secret_key.encode("utf-8"),
            payload_segment.encode("ascii"),
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(signature_segment, _base64url_encode(expected_signature)):
            raise ValueError("invalid signature")

        payload = json.loads(_base64url_decode(payload_segment).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("expired token")
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session cookie",
        )

    return session_token
