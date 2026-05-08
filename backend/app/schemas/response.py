from pydantic import BaseModel


class ValidateResponse(BaseModel):
    input: str
    normalized: str
    is_valid: bool
    lemma: str | None = None