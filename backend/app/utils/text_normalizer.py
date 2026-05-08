import re
import unicodedata


_ALLOWED_PATTERN = re.compile(r"^[a-záéíóúüñ]+$", re.IGNORECASE)


def normalize_term(term: str) -> str:
    return unicodedata.normalize("NFC", term.strip()).lower()


def is_allowed_term(term: str) -> bool:
    return bool(_ALLOWED_PATTERN.fullmatch(term))