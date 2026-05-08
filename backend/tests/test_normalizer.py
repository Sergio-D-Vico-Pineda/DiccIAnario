from app.utils.text_normalizer import is_allowed_term, normalize_term


def test_normalize_term_trims_and_lowercases() -> None:
    assert normalize_term("  Corriendo ") == "corriendo"


def test_allowed_term_rejects_numbers() -> None:
    assert not is_allowed_term("abc123")