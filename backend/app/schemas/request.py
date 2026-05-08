from pydantic import BaseModel, Field


class ValidateRequest(BaseModel):
    term: str = Field(min_length=1, max_length=64)